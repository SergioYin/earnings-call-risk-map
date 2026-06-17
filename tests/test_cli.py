import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from earnings_call_risk_map.cli import build_parser
from earnings_call_risk_map.source_boundary_evidence import render_source_boundary_evidence_markdown


ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
NON_ADVICE_TEXT = "does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice"
LOCAL_ONLY_ENV = {
    "PATH": os.environ.get("PATH", ""),
    "PYTHONPATH": str(ROOT / "src"),
    "PYTHONNOUSERSITE": "1",
    "HOME": str(ROOT),
}
README_BASH_BLOCK_RE = re.compile(r"```bash\n(.*?)```", re.DOTALL)


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", *args],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_cli_local_only(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", *args],
            cwd=ROOT,
            env=LOCAL_ONLY_ENV,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_readme_command(self, args):
        return subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", *args],
            cwd=ROOT,
            env=LOCAL_ONLY_ENV,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_version(self):
        result = self.run_cli("version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "0.9.0")

    def test_help_uses_public_safe_wording(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        help_text = " ".join(result.stdout.split())
        self.assertIn("Educational research review only", help_text)
        self.assertIn("not personalized investment, legal, accounting, tax, buy, sell, or hold advice", help_text)
        self.assertIn("analyze", result.stdout)

    def test_all_public_commands_expose_help(self):
        parser = build_parser()
        subparsers_action = next(
            action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
        )
        commands = sorted(subparsers_action.choices)

        root_result = self.run_cli_local_only("--help")
        self.assertEqual(root_result.returncode, 0, root_result.stderr)
        self.assertIn("usage: earnings-call-risk-map", root_result.stdout)
        for command in commands:
            self.assertIn(command, root_result.stdout)

        for command in commands:
            with self.subTest(command=command):
                result = self.run_cli_local_only(command, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertIn(f"usage: earnings-call-risk-map {command}", result.stdout)

    def test_readme_cli_command_snippets_run_without_external_dependencies(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        commands = _extract_readme_module_cli_commands(readme)
        self.assertGreaterEqual(len(commands), 10)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            before_snapshot = tmp_path / "readme_before.json"
            after_snapshot = tmp_path / "readme_after.json"
            self.assertEqual(
                self.run_readme_command(
                    ("analyze", "examples/input/demo_company_prior.json", "--json-out", str(before_snapshot))
                ).returncode,
                0,
            )
            self.assertEqual(
                self.run_readme_command(
                    ("analyze", "examples/input/demo_company.json", "--json-out", str(after_snapshot))
                ).returncode,
                0,
            )

            for index, command in enumerate(commands, start=1):
                args = _rewrite_readme_cli_args_for_temp_outputs(command, tmp_path, before_snapshot, after_snapshot)
                with self.subTest(command=" ".join(command)):
                    result = self.run_readme_command(args)
                    self.assertEqual(result.returncode, 0, f"README command #{index} failed: {result.stderr}")

    def test_analyze_outputs_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_out = Path(tmp) / "snapshot.json"
            md_out = Path(tmp) / "report.md"
            html_out = Path(tmp) / "dashboard.html"
            result = self.run_cli(
                "analyze",
                "examples/input/demo_company.json",
                "--json-out",
                str(json_out),
                "--md-out",
                str(md_out),
                "--html-out",
                str(html_out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["ticker"], "EXM")
            self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
            self.assertEqual(
                payload["source_boundaries"]["management_claims"],
                "source-provided company statements or prepared remarks; verify against filings and transcripts",
            )
            self.assertIn("analyst_questions", payload["source_boundaries"])
            markdown = md_out.read_text(encoding="utf-8")
            self.assertIn(NON_ADVICE_TEXT, markdown)
            self.assertIn("## Source Boundaries", markdown)
            self.assertIn("## Source Attribution", markdown)
            self.assertIn("Management claims", markdown)
            self.assertIn("Analyst questions", markdown)
            self.assertIn("User synthesis", markdown)
            html = html_out.read_text(encoding="utf-8")
            self.assertIn("<!doctype html>", html)
            self.assertIn("Deterministic demo dashboard", html)
            self.assertIn("Review Queue", html)
            self.assertIn("Source Attribution", html)
            self.assertIn("Static educational case study", html)
            self.assertNotIn("<script", html)
            self.assertNotIn("<link", html)

    def test_consumer_hardware_fixture_has_attributed_deterministic_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_out = Path(tmp) / "consumer_hardware_snapshot.json"
            review_queue_out = Path(tmp) / "consumer_hardware_review_queue.json"
            result = self.run_cli(
                "analyze",
                "examples/input/consumer_hardware.json",
                "--json-out",
                str(json_out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            review_result = self.run_cli(
                "review-queue",
                "examples/input/consumer_hardware.json",
                "--json-out",
                str(review_queue_out),
            )
            self.assertEqual(review_result.returncode, 0, review_result.stderr)

            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["ticker"], "LOGI")
            self.assertEqual(payload["summary"]["risk_count"], 2)
            self.assertEqual(payload["summary"]["opportunity_count"], 2)
            self.assertEqual(payload["summary"]["review_queue_count"], 1)
            self.assertEqual(payload["summary"]["stale_badge_count"], 0)
            self.assertEqual(
                [source["source_type"] for source in payload["source_attribution"]],
                ["company_investor_relations", "shareholder_letter"],
            )
            self.assertTrue(all(source["source_url"].startswith("https://") for source in payload["source_attribution"]))

            review_queue = json.loads(review_queue_out.read_text(encoding="utf-8"))
            self.assertEqual(review_queue["summary"]["review_item_count"], 1)
            self.assertEqual(review_queue["summary"]["high_impact_language_count"], 1)
            self.assertEqual(review_queue["summary"]["missing_evidence_count"], 0)
            self.assertEqual(review_queue["items"][0]["issue_categories"], ["high_impact_language"])

    def test_semiconductor_equipment_fixture_has_attributed_deterministic_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_out = Path(tmp) / "semiconductor_equipment_snapshot.json"
            review_queue_out = Path(tmp) / "semiconductor_equipment_review_queue.json"
            result = self.run_cli(
                "analyze",
                "examples/input/semiconductor_equipment.json",
                "--json-out",
                str(json_out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            review_result = self.run_cli(
                "review-queue",
                "examples/input/semiconductor_equipment.json",
                "--json-out",
                str(review_queue_out),
            )
            self.assertEqual(review_result.returncode, 0, review_result.stderr)

            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["ticker"], "ASML")
            self.assertEqual(payload["summary"]["risk_count"], 2)
            self.assertEqual(payload["summary"]["opportunity_count"], 5)
            self.assertEqual(payload["summary"]["review_queue_count"], 2)
            self.assertEqual(payload["summary"]["stale_badge_count"], 1)
            self.assertEqual(
                [source["source_type"] for source in payload["source_attribution"]],
                ["company_investor_relations", "press_release"],
            )
            self.assertTrue(all(source["source_url"].startswith("https://") for source in payload["source_attribution"]))

            review_queue = json.loads(review_queue_out.read_text(encoding="utf-8"))
            self.assertEqual(review_queue["summary"]["review_item_count"], 5)
            self.assertEqual(review_queue["summary"]["stale_data_count"], 1)
            self.assertEqual(review_queue["summary"]["missing_evidence_count"], 1)
            self.assertEqual(review_queue["summary"]["high_impact_language_count"], 4)
            topics = {item["topic"] for item in review_queue["items"]}
            self.assertIn("demand timing and export controls", topics)
            self.assertIn("Annual report review", topics)

    def test_analyze_reports_bad_date_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "bad.json"
            fixture.write_text(
                json.dumps(
                    {
                        "company": "Example Systems Inc.",
                        "ticker": "EXM",
                        "as_of": "2026/05/15",
                        "data_cutoff": "2026-04-30",
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_cli("analyze", str(fixture))

            self.assertEqual(result.returncode, 2)
            self.assertIn(f"{fixture}.as_of must use YYYY-MM-DD format", result.stderr)

    def test_analyze_reports_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "bad.json"
            fixture.write_text('{"company": "Example Systems Inc.",', encoding="utf-8")

            result = self.run_cli("analyze", str(fixture))

            self.assertEqual(result.returncode, 2)
            self.assertIn(f"error: {fixture} is not valid JSON at line 1, column", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_analyze_reports_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "missing.json"
            fixture.write_text(
                json.dumps(
                    {
                        "company": "Example Systems Inc.",
                        "data_cutoff": "2026-04-30",
                    }
                ),
                encoding="utf-8",
            )

            result = self.run_cli("analyze", str(fixture))

            self.assertEqual(result.returncode, 2)
            self.assertIn(f"error: {fixture} is missing required field(s): ticker, as_of", result.stderr)

    def test_analyze_reports_bad_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "not-a-dir"
            blocker.write_text("blocks output parent creation", encoding="utf-8")
            output = blocker / "snapshot.json"

            result = self.run_cli("analyze", "examples/input/demo_company.json", "--json-out", str(output))

            self.assertEqual(result.returncode, 2)
            self.assertIn(f"error: cannot write {output}: parent path {blocker} is not a directory", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_compare_outputs_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before.json"
            after = Path(tmp) / "after.json"
            md_out = Path(tmp) / "compare.md"
            self.assertEqual(
                self.run_cli("analyze", "examples/input/demo_company_prior.json", "--json-out", str(before)).returncode,
                0,
            )
            self.assertEqual(
                self.run_cli("analyze", "examples/input/demo_company.json", "--json-out", str(after)).returncode,
                0,
            )
            result = self.run_cli("compare", str(before), str(after), "--md-out", str(md_out))
            self.assertEqual(result.returncode, 0, result.stderr)
            markdown = md_out.read_text(encoding="utf-8")
            self.assertIn("Snapshot Compare", markdown)
            self.assertIn(NON_ADVICE_TEXT, markdown)
            self.assertIn("## Source Boundaries", markdown)
            json_out = Path(tmp) / "compare.json"
            json_result = self.run_cli("compare", str(before), str(after), "--json-out", str(json_out))
            self.assertEqual(json_result.returncode, 0, json_result.stderr)
            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
            self.assertIn("user_synthesis", payload["source_boundaries"])

    def test_compare_software_vs_energy_fixture_explains_cross_fixture_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            software = Path(tmp) / "software.json"
            energy = Path(tmp) / "energy.json"
            md_out = Path(tmp) / "software_vs_energy.md"
            json_out = Path(tmp) / "software_vs_energy.json"
            self.assertEqual(
                self.run_cli("analyze", "examples/input/demo_company.json", "--json-out", str(software)).returncode,
                0,
            )
            self.assertEqual(
                self.run_cli(
                    "analyze",
                    "examples/input/demo_energy_infrastructure.json",
                    "--json-out",
                    str(energy),
                ).returncode,
                0,
            )

            result = self.run_cli("compare", str(software), str(energy), "--md-out", str(md_out), "--json-out", str(json_out))

            self.assertEqual(result.returncode, 0, result.stderr)
            markdown = md_out.read_text(encoding="utf-8")
            self.assertIn("- Comparison scope: cross-fixture", markdown)
            self.assertIn("Before fixture: Example Systems Inc. (EXM)", markdown)
            self.assertIn("After fixture: Northstar Grid & LNG Partners (NGLP)", markdown)
            self.assertIn("do not rank companies, sectors, or securities", markdown)
            self.assertIn(NON_ADVICE_TEXT, markdown)

            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["comparison_scope"], "cross_fixture")
            self.assertEqual(payload["before_ticker"], "EXM")
            self.assertEqual(payload["after_ticker"], "NGLP")

    def test_review_queue_outputs_focused_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_out = Path(tmp) / "review_queue.json"
            md_out = Path(tmp) / "review_queue.md"
            result = self.run_cli(
                "review-queue",
                "examples/input/demo_company.json",
                "--json-out",
                str(json_out),
                "--md-out",
                str(md_out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["review_item_count"], 4)
            self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
            self.assertIn("management_claims", payload["source_boundaries"])
            categories = {category for item in payload["items"] for category in item["issue_categories"]}
            self.assertEqual(categories, {"stale_data", "missing_evidence", "high_impact_language"})
            markdown = md_out.read_text(encoding="utf-8")
            self.assertIn("Review Queue Export", markdown)
            self.assertIn("high-impact language", markdown)
            self.assertIn("## Prioritization", markdown)
            self.assertIn("items with more review issue categories first", markdown)
            self.assertIn("stale note data can add +1 to risk severity", markdown)
            self.assertIn("portfolio-risk or thesis-ledger owners", markdown)
            self.assertIn(NON_ADVICE_TEXT, markdown)
            self.assertIn("## Source Boundaries", markdown)

    def test_fixture_catalog_lists_bundled_fixtures(self):
        result = self.run_cli("fixture-catalog")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Fixture Catalog", result.stdout)
        self.assertIn("examples/input/demo_company.json", result.stdout)
        self.assertIn("`EXM`", result.stdout)
        self.assertIn("`2026-04-30`", result.stdout)
        self.assertIn("static demo fixture", result.stdout)
        self.assertIn("earnings-call-risk-map analyze examples/input/demo_company.json", result.stdout)
        self.assertIn("examples/input/consumer_hardware.json", result.stdout)
        self.assertIn("`LOGI`", result.stdout)
        self.assertIn("static public-source consumer hardware fixture", result.stdout)
        self.assertIn("examples/input/semiconductor_equipment.json", result.stdout)
        self.assertIn("`ASML`", result.stdout)
        self.assertIn("static public-source semiconductor equipment fixture", result.stdout)
        self.assertIn("examples/input/public_apple_static_case_study.json", result.stdout)
        self.assertIn("`AAPL`", result.stdout)
        self.assertIn("static public-source case study", result.stdout)
        self.assertIn("earnings-call-risk-map compare examples/output/demo_prior_snapshot.json", result.stdout)

    def test_fixture_catalog_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "fixture_catalog.md"
            result = self.run_cli("fixture-catalog", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            text = out.read_text(encoding="utf-8")
            self.assertIn("# Fixture Catalog", text)
            self.assertIn("examples/input/demo_energy_infrastructure.json", text)
            self.assertIn("`NGLP`", text)
            self.assertIn("examples/input/consumer_hardware.json", text)
            self.assertIn("`LOGI`", text)
            self.assertIn("examples/input/semiconductor_equipment.json", text)
            self.assertIn("`ASML`", text)

    def test_fixture_summary_outputs_markdown(self):
        result = self.run_cli("fixture-summary", "examples/input/semiconductor_equipment.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Fixture Summary", result.stdout)
        self.assertIn("- Company: ASML Holding N.V. Public-Source Semiconductor Equipment Fixture", result.stdout)
        self.assertIn("- Ticker: `ASML`", result.stdout)
        self.assertIn("| Source type | Count |", result.stdout)
        self.assertIn("| `company_investor_relations` | 9 |", result.stdout)
        self.assertIn("| `press_release` | 1 |", result.stdout)
        self.assertIn("| Risks | 2 |", result.stdout)
        self.assertIn("| Opportunities | 5 |", result.stdout)
        self.assertIn("| Stale Badges | 1 |", result.stdout)
        self.assertIn("| `asml-q3-memory-cycle` | memory customer cycle | `stale` | 107 | stale>90d |", result.stdout)
        self.assertIn(NON_ADVICE_TEXT, result.stdout)

    def test_fixture_summary_outputs_json_and_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "fixture_summary.json"
            result = self.run_cli(
                "fixture-summary",
                "examples/input/semiconductor_equipment.json",
                "--format",
                "json",
                "--out",
                str(out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_type"], "fixture_summary")
            self.assertEqual(payload["company"], "ASML Holding N.V. Public-Source Semiconductor Equipment Fixture")
            self.assertEqual(payload["ticker"], "ASML")
            self.assertEqual(payload["counts"]["notes"], 4)
            self.assertEqual(payload["counts"]["kpis"], 3)
            self.assertEqual(payload["counts"]["catalysts"], 2)
            self.assertEqual(payload["counts"]["risks"], 2)
            self.assertEqual(payload["counts"]["opportunities"], 5)
            self.assertEqual(payload["counts"]["review_queue"], 2)
            self.assertEqual(payload["counts"]["stale_badges"], 1)
            self.assertEqual(
                {item["source_type"]: item["count"] for item in payload["source_types"]},
                {"company_investor_relations": 9, "press_release": 1},
            )
            self.assertEqual(payload["stale_status_counts"], {"stale": 1})
            self.assertEqual(payload["stale_badges"][0]["badge"]["label"], "stale>90d")
            self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])

    def test_source_boundary_evidence_outputs_markdown_and_json(self):
        md_result = self.run_cli("source-boundary-evidence")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Source Boundary Evidence", md_result.stdout)
        self.assertIn("examples/input/public_apple_static_case_study.json", md_result.stdout)
        self.assertIn("examples/input/semiconductor_equipment.json", md_result.stdout)
        self.assertIn("No live data", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("source-boundary-evidence", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "source_boundary_evidence")
        self.assertEqual(payload["fixture_count"], 6)
        self.assertTrue(payload["checks"]["all_fixture_paths_exist"])
        self.assertTrue(payload["checks"]["all_fixtures_are_static_or_local"])
        self.assertTrue(payload["checks"]["no_private_paths_found"])
        self.assertTrue(payload["checks"]["no_live_fetching_required"])
        self.assertTrue(payload["checks"]["no_advice_claim_present"])
        self.assertTrue(payload["checks"]["walkthrough_receipt_present"])
        fixture_paths = {fixture["path"] for fixture in payload["fixtures"]}
        self.assertIn("examples/input/public_apple_static_case_study.json", fixture_paths)
        self.assertIn("examples/input/semiconductor_equipment.json", fixture_paths)
        receipt = payload["walkthrough_receipt"]
        self.assertEqual(receipt["receipt_type"], "public_source_boundary_walkthrough")
        self.assertEqual(receipt["public_source_fixture_count"], 3)
        self.assertIn("examples/input/public_apple_static_case_study.json", receipt["public_source_fixture_paths"])
        self.assertTrue(receipt["checks"]["all_fixture_boundaries_static_or_local"])
        self.assertTrue(receipt["checks"]["dashboard_handoff_paths_recorded"])
        self.assertEqual(receipt["missing_artifact_count"], 0)
        self.assertEqual(len(receipt["steps"]), 4)
        public_fixture = next(
            fixture for fixture in payload["fixtures"] if fixture["path"] == "examples/input/public_apple_static_case_study.json"
        )
        self.assertEqual(public_fixture["fixture_boundary"], "static_public_source_fixture")
        self.assertIn("www.apple.com", public_fixture["source_domains"])
        self.assertIn("www.sec.gov", public_fixture["source_domains"])
        self.assertGreaterEqual(public_fixture["static_notice_count"], 1)
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])

    def test_source_boundary_evidence_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "source_boundary_evidence.json"
            result = self.run_cli("source-boundary-evidence", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_type"], "source_boundary_evidence")
            self.assertIn("examples/output/source_boundary_evidence.md", payload["generated_artifacts"])

    def test_source_boundary_evidence_markdown_escapes_fixture_table_cells(self):
        markdown = render_source_boundary_evidence_markdown(
            {
                "tool_version": "0.test",
                "fixture_count": 1,
                "safety_notice": NON_ADVICE_TEXT,
                "no_live_data_claim": "No live fetches.",
                "no_advice_claim": NON_ADVICE_TEXT,
                "reviewer_handoff_claim": "Local files only.",
                "checks": {"no_live_fetching_required": True},
                "fixtures": [
                    {
                        "path": "examples/input/public|fixture.json",
                        "ticker": "ABC|DEF\nGHI",
                        "data_cutoff": "2026-05-17",
                        "fixture_boundary": "static|fixture",
                        "source_domains": ["issuer.example|sec.example", "docs.example\\archive"],
                        "static_notice_count": 1,
                        "has_private_path": False,
                    }
                ],
                "walkthrough_receipt": {
                    "receipt_type": "public_source_boundary_walkthrough",
                    "scope": "Cold reviewer receipt.",
                    "public_source_fixture_count": 1,
                    "static_or_local_fixture_count": 1,
                    "missing_artifact_count": 0,
                    "checks": {"all_receipt_artifacts_exist": True},
                    "steps": [
                        {
                            "step": "Verify fixture",
                            "reviewer_action": "Open the local fixture.",
                            "boundary": "Static only.",
                            "evidence_paths": ["examples/input/public|fixture.json"],
                        }
                    ],
                },
                "source_boundaries": {},
                "generated_artifacts": [],
                "source_docs": [],
            }
        )

        fixture_row = next(line for line in markdown.splitlines() if "public\\|fixture" in line)
        self.assertIn("examples/input/public\\|fixture.json", fixture_row)
        self.assertIn("ABC\\|DEF GHI", fixture_row)
        self.assertIn("static\\|fixture", fixture_row)
        self.assertIn("issuer.example\\|sec.example", fixture_row)
        self.assertIn("docs.example\\\\archive", fixture_row)

    def test_playbooks_outputs_markdown_and_json(self):
        md_result = self.run_cli("playbooks")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Research Playbooks", md_result.stdout)
        self.assertIn("Quarterly Review", md_result.stdout)
        self.assertIn("Catalyst Check-In", md_result.stdout)
        self.assertIn("Post-Earnings Thesis Refresh", md_result.stdout)
        self.assertIn("## Recommended CLI Sequences", md_result.stdout)
        self.assertIn("PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output", md_result.stdout)
        self.assertIn("review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("playbooks", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["playbook_count"], 3)
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        titles = {playbook["title"] for playbook in payload["playbooks"]}
        self.assertEqual(titles, {"Quarterly Review", "Catalyst Check-In", "Post-Earnings Thesis Refresh"})
        quarterly = next(playbook for playbook in payload["playbooks"] if playbook["slug"] == "quarterly-review")
        self.assertIn("examples/playbooks/quarterly-review.md", quarterly["path"])
        self.assertIn("examples/output/demo_compare.md", quarterly["expected_artifacts"])
        self.assertTrue(
            any("compare examples/output/demo_prior_snapshot.json" in command for command in quarterly["recommended_cli_sequence"])
        )

    def test_playbooks_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "playbooks.json"
            result = self.run_cli("playbooks", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["playbook_count"], 3)
            self.assertEqual(payload["playbooks"][0]["slug"], "quarterly-review")

    def test_promotion_pack_outputs_markdown_and_json(self):
        md_result = self.run_cli("promotion-pack")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Public Promotion Pack", md_result.stdout)
        self.assertIn("## Quickstart", md_result.stdout)
        self.assertIn("## Demos", md_result.stdout)
        self.assertIn("## Proof Commands", md_result.stdout)
        self.assertIn("## Boundaries", md_result.stdout)
        self.assertIn("examples/output/public_apple_static_case_study_dashboard.html", md_result.stdout)
        self.assertIn("PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output", md_result.stdout)
        self.assertIn("docs/promotion-page-outline.md", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("promotion-pack", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "promotion_pack")
        self.assertEqual(payload["name"], "earnings-call-risk-map")
        self.assertEqual(payload["version"], "0.9.0")
        self.assertGreaterEqual(len(payload["demos"]), 5)
        self.assertIn("docs/promotion-page-outline.md", payload["source_evidence"])
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertTrue(any("No live market data" in boundary for boundary in payload["boundaries"]))

    def test_promotion_pack_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "promotion_pack.json"
            result = self.run_cli("promotion-pack", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_type"], "promotion_pack")
            self.assertIn("PYTHONPATH=src python -m unittest discover -s tests", payload["proof_commands"])

    def test_publication_checklist_outputs_markdown_and_json(self):
        md_result = self.run_cli("publication-checklist")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Publication Checklist", md_result.stdout)
        self.assertIn("## 1. Confirm The Release Candidate", md_result.stdout)
        self.assertIn("## 6. Create The GitHub Release", md_result.stdout)
        self.assertIn("git tag -a v0.9.0", md_result.stdout)
        self.assertIn("gh release create v0.9.0", md_result.stdout)
        self.assertIn("python scripts/privacy_scan.py", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("publication-checklist", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "publication_checklist")
        self.assertEqual(payload["version"], "0.9.0")
        self.assertEqual(payload["step_count"], 7)
        self.assertEqual(payload["source_doc"], "docs/publication-checklist.md")
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertEqual(payload["steps"][0]["slug"], "confirm-release-candidate")
        self.assertTrue(
            any("maturity-evidence --out-dir reports/maturity" in command for command in payload["steps"][0]["commands"])
        )
        release_step = next(step for step in payload["steps"] if step["slug"] == "create-github-release")
        self.assertIn("--notes-file docs/release-notes-v0.9.0.md", release_step["commands"][0])

    def test_publication_checklist_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "publication_checklist.json"
            result = self.run_cli("publication-checklist", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["step_count"], 7)
            self.assertEqual(payload["steps"][-1]["slug"], "post-publish-smoke")

    def test_release_owner_handoff_outputs_markdown_and_json(self):
        md_result = self.run_cli("release-owner-handoff")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Release Owner Handoff", md_result.stdout)
        self.assertIn("## Final Release Owner Checklist", md_result.stdout)
        self.assertIn("## Exact Verification Commands", md_result.stdout)
        self.assertIn("PYTHONPATH=src python -m earnings_call_risk_map version", md_result.stdout)
        self.assertIn("git diff --check", md_result.stdout)
        self.assertIn("gh release create", md_result.stdout)
        self.assertIn("docs/release-notes-v0.9.0.md", md_result.stdout)
        self.assertIn("Owner-Controlled Promotion Gate", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("release-owner-handoff", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "release_owner_handoff")
        self.assertEqual(payload["version"], "0.9.0")
        self.assertEqual(payload["source_doc"], "docs/release-owner-handoff.md")
        self.assertEqual(payload["check_count"], 6)
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertIn("git diff --check", payload["verification_commands"])
        self.assertIn("examples/output/handoff_packet.json", payload["promotion_evidence_paths"])
        self.assertEqual(payload["checklist"][0]["slug"], "confirm-release-metadata")
        self.assertTrue(
            any("missing_count" in expected for expected in payload["expected_results"])
        )

    def test_release_owner_handoff_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "release_owner_handoff.json"
            result = self.run_cli("release-owner-handoff", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_type"], "release_owner_handoff")
            self.assertIn("python -m build --wheel --outdir dist-dry-run", payload["package_dry_run_commands"])

    def test_data_entry_checklist_outputs_markdown_and_json(self):
        md_result = self.run_cli("data-entry-checklist")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Data Entry Checklist", md_result.stdout)
        self.assertIn("Create a valid JSON fixture without hallucinating sources.", md_result.stdout)
        self.assertIn("## Field Mapping", md_result.stdout)
        self.assertIn("| `source_attribution` | Static provenance metadata.", md_result.stdout)
        self.assertIn("PYTHONPATH=src python -m earnings_call_risk_map analyze path/to/fixture.json", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("data-entry-checklist", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "data_entry_checklist")
        self.assertEqual(payload["source_doc"], "docs/data-entry-checklist.md")
        self.assertEqual(payload["section_count"], 4)
        self.assertGreaterEqual(payload["field_mapping_count"], 8)
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertEqual(payload["sections"][0]["slug"], "before-entry")

    def test_data_entry_checklist_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "data_entry_checklist.json"
            result = self.run_cli("data-entry-checklist", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_type"], "data_entry_checklist")
            self.assertTrue(any(section["slug"] == "final-review" for section in payload["sections"]))

    def test_agent_workflow_outputs_markdown_and_json(self):
        md_result = self.run_cli("agent-workflow")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Agent Workflow", md_result.stdout)
        self.assertIn("## Routing Map", md_result.stdout)
        self.assertIn("## Analyze Route", md_result.stdout)
        self.assertIn("## Compare Route", md_result.stdout)
        self.assertIn("## Review Queue Route", md_result.stdout)
        self.assertIn("## Source Attribution Route", md_result.stdout)
        self.assertIn("PYTHONPATH=src python -m earnings_call_risk_map analyze input.json", md_result.stdout)
        self.assertIn("missing evidence and high-impact language remain in the review queue", md_result.stdout)
        self.assertIn("Do not recommend buy, sell, hold", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("agent-workflow", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "agent_workflow")
        self.assertEqual(payload["source_doc"], "docs/agent-workflow.md")
        self.assertEqual([route["slug"] for route in payload["routes"]], ["analyze", "compare", "review-queue", "source-attribution"])
        self.assertIn("summarize with source attribution", payload["recommended_sequence"])
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])

    def test_agent_workflow_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "agent_workflow.json"
            result = self.run_cli("agent-workflow", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_type"], "agent_workflow")
            self.assertTrue(any(route["slug"] == "review-queue" for route in payload["routes"]))

    def test_demo_screenshot_guide_outputs_markdown_and_json(self):
        md_result = self.run_cli("demo-screenshot-guide")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Demo Screenshot Guide", md_result.stdout)
        self.assertIn("examples/output/public_apple_static_case_study_dashboard.html", md_result.stdout)
        self.assertIn("docs/assets/showcase-dashboard-preview.svg", md_result.stdout)
        self.assertIn("## Screenshot Framing", md_result.stdout)
        self.assertIn("Do not use screenshots to imply live market data.", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("demo-screenshot-guide", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "demo_screenshot_guide")
        self.assertEqual(payload["source_doc"], "docs/demo-screenshot-guide.md")
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertGreaterEqual(len(payload["best_screenshot_targets"]), 8)
        self.assertIn("docs/pages-demo.md", payload["related_docs"])

    def test_demo_screenshot_guide_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "demo_screenshot_guide.json"
            result = self.run_cli("demo-screenshot-guide", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(any(target["path"].endswith("_dashboard.html") for target in payload["best_screenshot_targets"]))

    def test_fresh_clone_plan_outputs_markdown_and_json(self):
        md_result = self.run_cli("fresh-clone-plan")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Fresh Clone Verification Plan", md_result.stdout)
        self.assertIn("git clone <repo-url> earnings-call-risk-map", md_result.stdout)
        self.assertIn("earnings-call-risk-map demo --out-dir verification/fresh-clone/demo", md_result.stdout)
        self.assertIn("verification/fresh-clone/demo_company_snapshot.json", md_result.stdout)
        self.assertIn("python -m json.tool verification/fresh-clone/doctor.json >/dev/null", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("fresh-clone-plan", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "fresh_clone_verification_plan")
        self.assertEqual(payload["version"], "0.9.0")
        self.assertEqual(payload["source_doc"], "docs/fresh-clone-verification.md")
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertIn("git clone <repo-url> earnings-call-risk-map", payload["commands"])
        self.assertIn(
            "verification/fresh-clone/demo_company_report.md",
            payload["expected_generated_artifacts"]["direct"],
        )
        self.assertIn(
            "verification/fresh-clone/demo/demo_review_queue_items.jsonl",
            payload["expected_generated_artifacts"]["demo_bundle"],
        )

    def test_fresh_clone_plan_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "fresh_clone_plan.json"
            result = self.run_cli("fresh-clone-plan", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(any("release-assets" in command for command in payload["commands"]))

    def test_template_catalog_outputs_markdown_and_json(self):
        md_result = self.run_cli("template-catalog")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Template Catalog", md_result.stdout)
        self.assertIn("Software Earnings Review", md_result.stdout)
        self.assertIn("Energy Infrastructure Earnings Review", md_result.stdout)
        self.assertIn("Consumer Hardware Earnings Review", md_result.stdout)
        self.assertIn("Recommended Fields And Commands", md_result.stdout)
        self.assertIn("examples/templates/software_earnings_review.json", md_result.stdout)
        self.assertIn("`company`, `ticker`, `as_of`, `data_cutoff`", md_result.stdout)
        self.assertIn("earnings-call-risk-map analyze examples/templates/software_earnings_review.json", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("template-catalog", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "template_catalog")
        self.assertEqual(payload["template_count"], 3)
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        slugs = {template["slug"] for template in payload["templates"]}
        self.assertEqual(slugs, {"software", "energy_infrastructure", "consumer_hardware"})
        software = next(template for template in payload["templates"] if template["slug"] == "software")
        self.assertEqual(software["recommended_fields"]["top_level"], ["company", "ticker", "as_of", "data_cutoff"])
        self.assertIn("Revenue growth", software["recommended_fields"]["kpi_names"])
        self.assertTrue(
            any("review-queue examples/templates/software_earnings_review.json" in command for command in software["recommended_commands"])
        )

    def test_template_catalog_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "template_catalog.json"
            result = self.run_cli("template-catalog", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["template_count"], 3)
            self.assertEqual(payload["templates"][0]["path"], "examples/templates/software_earnings_review.json")

    def test_schema_authoring_reference_outputs_markdown_and_json(self):
        md_result = self.run_cli("schema-authoring-reference")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Schema Authoring Reference", md_result.stdout)
        self.assertIn("Plain-English Meaning", md_result.stdout)
        self.assertIn("Authoring Guidance", md_result.stdout)
        self.assertIn("Do not invent source names, publishers, URLs, dates", md_result.stdout)
        self.assertIn("does not fetch, refresh, or verify", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("schema-authoring-reference", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "schema_authoring_reference")
        self.assertEqual(payload["source_doc"], "docs/schema-authoring-reference.md")
        self.assertEqual(payload["schema_reference"], "docs/schema-reference.json")
        self.assertGreaterEqual(payload["field_count"], 30)
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertTrue(any(section["slug"] == "source_attribution" for section in payload["sections"]))

    def test_schema_authoring_reference_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "schema_authoring_reference.json"
            result = self.run_cli("schema-authoring-reference", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["minimal_starting_point"]["ticker"], "EXM")

    def test_examples_index_outputs_markdown_and_json(self):
        md_result = self.run_cli("examples-index")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Examples Index", md_result.stdout)
        self.assertIn("## Bundled Fixtures", md_result.stdout)
        self.assertIn("## Templates", md_result.stdout)
        self.assertIn("## Generated Outputs", md_result.stdout)
        self.assertIn("examples/input/demo_company.json", md_result.stdout)
        self.assertIn("examples/templates/software_earnings_review.json", md_result.stdout)
        self.assertIn("examples/output/demo_report.md", md_result.stdout)
        self.assertIn("Recommended next command", md_result.stdout)
        self.assertIn("earnings-call-risk-map demo --out-dir examples/output", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("examples-index", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "examples_index")
        self.assertEqual(payload["summary"]["fixture_count"], 7)
        self.assertEqual(payload["summary"]["template_count"], 3)
        self.assertGreaterEqual(payload["summary"]["generated_output_count"], 5)
        self.assertEqual(payload["recommended_next_command"], "earnings-call-risk-map demo --out-dir examples/output")
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        self.assertIn("recommended_next_command", payload["fixtures"][0])
        self.assertIn("recommended_next_command", payload["templates"][0])
        self.assertIn("recommended_next_command", payload["generated_outputs"][0])
        self.assertIn(
            "examples/output/demo_report.md",
            {output["path"] for output in payload["generated_outputs"]},
        )

    def test_examples_index_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "examples_index.json"
            result = self.run_cli("examples-index", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["artifact_type"], "examples_index")
            self.assertEqual(payload["summary"]["template_count"], 3)

    def test_audit_reports_package_parity_json_and_markdown(self):
        result = self.run_cli("audit")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["version"], "0.9.0")
        self.assertIn("agent-workflow", payload["commands"])
        self.assertIn("audit", payload["commands"])
        self.assertIn("case-study-map", payload["commands"])
        self.assertIn("cheat-sheet", payload["commands"])
        self.assertIn("data-entry-checklist", payload["commands"])
        self.assertIn("doctor", payload["commands"])
        self.assertIn("examples-index", payload["commands"])
        self.assertIn("fixture-catalog", payload["commands"])
        self.assertIn("playbooks", payload["commands"])
        self.assertIn("promotion-pack", payload["commands"])
        self.assertIn("publication-checklist", payload["commands"])
        self.assertIn("release-owner-handoff", payload["commands"])
        self.assertIn("release-assets", payload["commands"])
        self.assertIn("release-notes", payload["commands"])
        self.assertIn("review-queue-jsonl", payload["commands"])
        self.assertIn("risk-taxonomy", payload["commands"])
        self.assertIn("schema-authoring-reference", payload["commands"])
        self.assertIn("schema-reference", payload["commands"])
        self.assertIn("template-catalog", payload["commands"])
        self.assertEqual(payload["fixture_count"], 7)
        self.assertGreaterEqual(payload["output_artifact_count"], 5)
        self.assertFalse(payload["has_workflow_files"])
        self.assertTrue(payload["skill"]["present"])
        self.assertEqual(payload["local_only"]["status"], "passed")
        self.assertFalse(payload["local_only"]["network_required"])
        self.assertFalse(payload["local_only"]["credentials_required"])
        self.assertEqual(payload["local_only"]["external_services"], [])
        self.assertEqual(
            {item["name"] for item in payload["local_only"]["commands"]},
            set(payload["commands"]),
        )
        self.assertTrue(
            all(not item["network_required"] and not item["credentials_required"] for item in payload["local_only"]["commands"])
        )
        self.assertEqual(
            {check["name"] for check in payload["local_only"]["checks"]},
            {
                "runtime_dependencies_empty",
                "no_network_client_imports",
                "no_credential_environment_reads",
                "workflow_files_absent",
            },
        )
        self.assertTrue(all(check["status"] == "passed" for check in payload["local_only"]["checks"]))

        md_result = self.run_cli("audit", "--format", "markdown")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Package Audit", md_result.stdout)
        self.assertIn("Workflow files present: no", md_result.stdout)
        self.assertIn("Skill present: yes", md_result.stdout)
        self.assertIn("Local-Only No-Network Guarantee", md_result.stdout)
        self.assertIn("Network access required: no", md_result.stdout)
        self.assertIn("Credentials required: no", md_result.stdout)
        self.assertIn("no_network_client_imports: passed", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

    def test_doctor_reports_package_health_and_hints(self):
        result = self.run_cli("doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Doctor Report", result.stdout)
        self.assertIn("- Status: `passed`", result.stdout)
        self.assertIn("- Fixture count: 7", result.stdout)
        self.assertIn("- Workflow files absent: yes", result.stdout)
        self.assertIn("Docs Links", result.stdout)
        self.assertIn("Privacy Scan Command Hints", result.stdout)
        self.assertIn("`python scripts/privacy_scan.py`", result.stdout)
        self.assertIn(NON_ADVICE_TEXT, result.stdout)

        json_result = self.run_cli("doctor", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "doctor_report")
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["fixture_count"], 7)
        self.assertGreaterEqual(payload["output_artifact_count"], 5)
        self.assertEqual(payload["docs_links"]["status"], "passed")
        self.assertGreater(payload["docs_links"]["checked_link_count"], 0)
        self.assertTrue(payload["workflow_files_absent"])
        self.assertIn("python scripts/privacy_scan.py", payload["privacy_scan_command_hints"])

    def test_doctor_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "doctor.json"
            result = self.run_cli("doctor", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["package_health"]["local_only_status"], "passed")

    def test_cheat_sheet_outputs_all_commands_as_markdown_and_json(self):
        parser = build_parser()
        subparsers_action = next(
            action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
        )
        expected_commands = set(subparsers_action.choices)

        md_result = self.run_cli("cheat-sheet")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Command Cheat Sheet", md_result.stdout)
        self.assertIn("| Command | Purpose |", md_result.stdout)
        self.assertIn("| `agent-workflow` | Render generic agent workflow instructions as Markdown or JSON |", md_result.stdout)
        self.assertIn("| `analyze` | Analyze one earnings-call JSON input |", md_result.stdout)
        self.assertIn("| `cheat-sheet` | Print lightweight command cheat sheet as Markdown or JSON |", md_result.stdout)
        self.assertIn("| `data-entry-checklist` | Render fixture author data-entry checklist as Markdown or JSON |", md_result.stdout)
        self.assertIn("| `demo-screenshot-guide` | Render demo screenshot guide as Markdown or JSON |", md_result.stdout)
        self.assertIn("| `fresh-clone-plan` | Render fresh clone verification plan as Markdown or JSON |", md_result.stdout)

        json_result = self.run_cli("cheat-sheet", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "command_cheat_sheet")
        self.assertEqual(payload["command_count"], len(expected_commands))
        self.assertEqual({item["command"] for item in payload["commands"]}, expected_commands)
        self.assertTrue(all(item["purpose"] for item in payload["commands"]))

    def test_cheat_sheet_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "command_cheat_sheet.json"
            result = self.run_cli("cheat-sheet", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertIn("review-queue-jsonl", {item["command"] for item in payload["commands"]})

    def test_case_study_map_outputs_markdown_and_json(self):
        md_result = self.run_cli("case-study-map")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Case Study Map", md_result.stdout)
        self.assertIn("| Fixture | Target sector | Useful question | Generated artifacts |", md_result.stdout)
        self.assertIn("examples/input/demo_company.json", md_result.stdout)
        self.assertIn("examples/input/sample_filled_template_workflow.json", md_result.stdout)
        self.assertIn("examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

        json_result = self.run_cli("case-study-map", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        payload = json.loads(json_result.stdout)
        self.assertEqual(payload["artifact_type"], "case_study_map")
        self.assertEqual(payload["fixture_count"], 7)
        self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
        fixtures = {case_study["fixture"] for case_study in payload["case_studies"]}
        self.assertIn("examples/input/public_apple_static_case_study.json", fixtures)
        semiconductor = next(
            case_study
            for case_study in payload["case_studies"]
            if case_study["fixture"] == "examples/input/semiconductor_equipment.json"
        )
        self.assertIn("Semiconductor equipment", semiconductor["target_sector"])
        self.assertIn(
            "examples/output/semiconductor_equipment_report/dashboard/dashboard.html",
            semiconductor["generated_artifacts"],
        )
        self.assertIn("examples/output/examples_index.md", payload["shared_generated_artifacts"])

    def test_case_study_map_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "case_study_map.json"
            result = self.run_cli("case-study-map", "--format", "json", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["case_studies"][0]["fixture"], "examples/input/demo_company.json")

    def test_release_assets_reports_current_version_assets(self):
        result = self.run_cli("release-assets")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["version"], "0.9.0")
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["missing_assets"], [])
        self.assertIn("docs/release-notes-v0.9.0.md", payload["expected_assets"])
        self.assertIn("docs/comparison-to-spreadsheets.md", payload["expected_assets"])
        self.assertIn("docs/schema-authoring-reference.md", payload["expected_assets"])
        self.assertIn("examples/output/template_catalog.md", payload["expected_assets"])
        self.assertIn("examples/output/template_catalog.json", payload["expected_assets"])
        self.assertIn("examples/output/schema_authoring_reference.md", payload["expected_assets"])
        self.assertIn("examples/output/schema_authoring_reference.json", payload["expected_assets"])
        self.assertIn("examples/output/command_cheatsheet.md", payload["expected_assets"])
        self.assertIn("examples/output/command_cheatsheet.json", payload["expected_assets"])
        self.assertIn("examples/output/semiconductor_equipment_dashboard.html", payload["expected_assets"])
        self.assertIn("examples/output/semiconductor_equipment_report.md", payload["expected_assets"])
        self.assertIn("examples/output/semiconductor_equipment_review_queue.md", payload["expected_assets"])
        self.assertIn("examples/output/semiconductor_equipment_snapshot.json", payload["expected_assets"])
        self.assertIn("examples/output/doctor.md", payload["expected_assets"])
        self.assertIn("examples/output/doctor.json", payload["expected_assets"])
        self.assertIn("examples/output/examples_index.md", payload["expected_assets"])
        self.assertIn("examples/output/examples_index.json", payload["expected_assets"])
        self.assertIn("examples/output/case_study_map.md", payload["expected_assets"])
        self.assertIn("examples/output/case_study_map.json", payload["expected_assets"])
        self.assertIn("examples/output/publication_checklist.md", payload["expected_assets"])
        self.assertIn("examples/output/publication_checklist.json", payload["expected_assets"])
        self.assertIn("examples/output/agent_workflow.md", payload["expected_assets"])
        self.assertIn("examples/output/agent_workflow.json", payload["expected_assets"])
        self.assertIn("examples/output/data_entry_checklist.md", payload["expected_assets"])
        self.assertIn("examples/output/data_entry_checklist.json", payload["expected_assets"])
        self.assertIn("examples/output/demo_screenshot_guide.md", payload["expected_assets"])
        self.assertIn("examples/output/demo_screenshot_guide.json", payload["expected_assets"])
        self.assertIn("examples/output/fresh_clone_plan.md", payload["expected_assets"])
        self.assertIn("examples/output/fresh_clone_plan.json", payload["expected_assets"])
        self.assertIn("reports/reviews/2026-06-18-v0.9.0-final-review.md", payload["expected_assets"])
        self.assertIn("reports/reviews/release-readiness-review.md", payload["present_assets"])

        md_result = self.run_cli("release-assets", "--format", "markdown")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Release Asset Checklist", md_result.stdout)
        self.assertIn("- Status: `passed`", md_result.stdout)
        self.assertIn("- [x] `docs/release-notes-v0.9.0.md`", md_result.stdout)
        self.assertIn("- [x] `docs/comparison-to-spreadsheets.md`", md_result.stdout)
        self.assertIn("- [x] `docs/schema-authoring-reference.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/template_catalog.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/template_catalog.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/schema_authoring_reference.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/schema_authoring_reference.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/command_cheatsheet.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/command_cheatsheet.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/semiconductor_equipment_dashboard.html`", md_result.stdout)
        self.assertIn("- [x] `examples/output/doctor.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/doctor.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/examples_index.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/examples_index.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/case_study_map.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/case_study_map.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/publication_checklist.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/publication_checklist.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/agent_workflow.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/agent_workflow.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/data_entry_checklist.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/data_entry_checklist.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/demo_screenshot_guide.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/demo_screenshot_guide.json`", md_result.stdout)
        self.assertIn("- [x] `examples/output/fresh_clone_plan.md`", md_result.stdout)
        self.assertIn("- [x] `examples/output/fresh_clone_plan.json`", md_result.stdout)
        self.assertIn("- [x] `reports/reviews/2026-06-18-v0.9.0-final-review.md`", md_result.stdout)

    def test_release_assets_reports_missing_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "release-notes-v0.9.0.md").write_text("release notes", encoding="utf-8")
            out = root / "missing_assets.md"

            result = self.run_cli("release-assets", "--root", str(root), "--format", "markdown", "--out", str(out))

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(result.stdout, "")
            markdown = out.read_text(encoding="utf-8")
            self.assertIn("- Status: `failed`", markdown)
            self.assertIn("## Missing Assets", markdown)
            self.assertIn("- [x] `docs/release-notes-v0.9.0.md`", markdown)
            self.assertIn("- [ ] `README.md`", markdown)

            json_result = self.run_cli("release-assets", "--root", str(root))
            self.assertEqual(json_result.returncode, 1, json_result.stderr)
            payload = json.loads(json_result.stdout)
            self.assertEqual(payload["status"], "failed")
            self.assertGreater(payload["missing_count"], 0)
            self.assertIn("README.md", payload["missing_assets"])

    def test_release_notes_renders_current_audit_assets_and_changelog(self):
        result = self.run_cli("release-notes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Release Notes Summary", result.stdout)
        self.assertIn("- Version: `0.9.0`", result.stdout)
        self.assertIn("- Local-only audit: passed", result.stdout)
        self.assertIn("- Release assets: `passed`", result.stdout)
        self.assertIn("## Package Audit", result.stdout)
        self.assertIn("`release-notes`", result.stdout)
        self.assertIn("## Release Assets", result.stdout)
        self.assertIn("### Missing Assets", result.stdout)
        self.assertIn("- None", result.stdout)
        self.assertIn("## Changelog Excerpt", result.stdout)
        self.assertIn("## 0.9.0 - 2026-06-18", result.stdout)
        self.assertIn("Source-boundary walkthrough receipt release.", result.stdout)
        self.assertNotIn("## 0.6.0 - 2026-05-17", result.stdout)
        self.assertIn(NON_ADVICE_TEXT, result.stdout)

    def test_release_notes_writes_output_file_and_reports_missing_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            root.mkdir()
            (root / "docs").mkdir()
            (root / "src").mkdir()
            (root / "scripts").mkdir()
            (root / "CHANGELOG.md").write_text(
                "# Changelog\n\n"
                "## 0.9.0 - 2026-06-18\n\n"
                "Current release excerpt.\n\n"
                "### Added\n\n"
                "- Deterministic renderer coverage.\n\n"
                "## 0.6.0 - 2026-05-17\n\n"
                "Older release.\n",
                encoding="utf-8",
            )
            (root / "pyproject.toml").write_text("[project]\ndependencies = []\n", encoding="utf-8")
            (root / "docs" / "release-notes-v0.9.0.md").write_text("release notes", encoding="utf-8")
            out = Path(tmp) / "release_notes.md"

            result = self.run_cli("release-notes", "--root", str(root), "--out", str(out))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            markdown = out.read_text(encoding="utf-8")
            self.assertIn("# Release Notes Summary", markdown)
            self.assertIn("- Release assets: `failed`", markdown)
            self.assertIn("- Missing release assets:", markdown)
            self.assertIn("- `README.md`", markdown)
            self.assertIn("Current release excerpt.", markdown)
            self.assertIn("- Deterministic renderer coverage.", markdown)
            self.assertNotIn("Older release.", markdown)

    def test_commands_run_without_network_or_credential_environment(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            commands = [
                ("version",),
                ("analyze", "examples/input/demo_company_prior.json", "--json-out", str(tmp_path / "before.json")),
                ("analyze", "examples/input/demo_company.json", "--json-out", str(tmp_path / "after.json")),
                (
                    "analyze",
                    "examples/input/demo_company.json",
                    "--json-out",
                    str(tmp_path / "snapshot.json"),
                    "--md-out",
                    str(tmp_path / "report.md"),
                    "--html-out",
                    str(tmp_path / "dashboard.html"),
                ),
                (
                    "compare",
                    str(tmp_path / "before.json"),
                    str(tmp_path / "after.json"),
                    "--json-out",
                    str(tmp_path / "compare.json"),
                    "--md-out",
                    str(tmp_path / "compare.md"),
                ),
                (
                    "review-queue",
                    "examples/input/demo_company.json",
                    "--json-out",
                    str(tmp_path / "review_queue.json"),
                    "--md-out",
                    str(tmp_path / "review_queue.md"),
                ),
                ("review-queue-jsonl", "--out", str(tmp_path / "review_items.jsonl")),
                ("agent-workflow", "--format", "markdown", "--out", str(tmp_path / "agent_workflow.md")),
                ("agent-workflow", "--format", "json", "--out", str(tmp_path / "agent_workflow.json")),
                ("examples-index", "--format", "markdown", "--out", str(tmp_path / "examples_index.md")),
                ("examples-index", "--format", "json", "--out", str(tmp_path / "examples_index.json")),
                ("case-study-map", "--format", "markdown", "--out", str(tmp_path / "case_study_map.md")),
                ("case-study-map", "--format", "json", "--out", str(tmp_path / "case_study_map.json")),
                (
                    "handoff-packet",
                    "--json-out",
                    str(tmp_path / "handoff_packet.json"),
                    "--md-out",
                    str(tmp_path / "handoff_packet.md"),
                ),
                ("fixture-catalog", "--out", str(tmp_path / "fixture_catalog.md")),
                ("risk-taxonomy", "--out", str(tmp_path / "risk_language_taxonomy.md")),
                ("template-catalog", "--format", "markdown", "--out", str(tmp_path / "template_catalog.md")),
                ("template-catalog", "--format", "json", "--out", str(tmp_path / "template_catalog.json")),
                ("schema-reference", "--out", str(tmp_path / "schema-reference.json")),
                (
                    "schema-authoring-reference",
                    "--format",
                    "markdown",
                    "--out",
                    str(tmp_path / "schema_authoring_reference.md"),
                ),
                (
                    "schema-authoring-reference",
                    "--format",
                    "json",
                    "--out",
                    str(tmp_path / "schema_authoring_reference.json"),
                ),
                ("playbooks", "--format", "markdown", "--out", str(tmp_path / "playbooks.md")),
                ("playbooks", "--format", "json", "--out", str(tmp_path / "playbooks.json")),
                ("promotion-pack", "--format", "markdown", "--out", str(tmp_path / "promotion_pack.md")),
                ("promotion-pack", "--format", "json", "--out", str(tmp_path / "promotion_pack.json")),
                ("publication-checklist", "--format", "markdown", "--out", str(tmp_path / "publication_checklist.md")),
                ("publication-checklist", "--format", "json", "--out", str(tmp_path / "publication_checklist.json")),
                ("release-owner-handoff", "--format", "markdown", "--out", str(tmp_path / "release_owner_handoff.md")),
                ("release-owner-handoff", "--format", "json", "--out", str(tmp_path / "release_owner_handoff.json")),
                ("data-entry-checklist", "--format", "markdown", "--out", str(tmp_path / "data_entry_checklist.md")),
                ("data-entry-checklist", "--format", "json", "--out", str(tmp_path / "data_entry_checklist.json")),
                ("demo-screenshot-guide", "--format", "markdown", "--out", str(tmp_path / "demo_screenshot_guide.md")),
                ("demo-screenshot-guide", "--format", "json", "--out", str(tmp_path / "demo_screenshot_guide.json")),
                ("fresh-clone-plan", "--format", "markdown", "--out", str(tmp_path / "fresh_clone_plan.md")),
                ("fresh-clone-plan", "--format", "json", "--out", str(tmp_path / "fresh_clone_plan.json")),
                ("audit", "--format", "json", "--out", str(tmp_path / "package_audit.json")),
                ("doctor", "--format", "json", "--out", str(tmp_path / "doctor.json")),
                ("cheat-sheet", "--format", "markdown", "--out", str(tmp_path / "command_cheat_sheet.md")),
                ("cheat-sheet", "--format", "json", "--out", str(tmp_path / "command_cheat_sheet.json")),
                ("release-assets", "--format", "json", "--out", str(tmp_path / "release_assets.json")),
                ("release-notes", "--out", str(tmp_path / "release_notes.md")),
                ("manifest", "--out", str(tmp_path / "release_manifest.json")),
                ("maturity-evidence", "--out-dir", str(tmp_path / "maturity")),
                ("demo", "--out-dir", str(tmp_path / "demo")),
            ]
            for command in commands:
                with self.subTest(command=" ".join(command)):
                    result = self.run_cli_local_only(*command)
                    self.assertEqual(result.returncode, 0, result.stderr)

            audit = json.loads((tmp_path / "package_audit.json").read_text(encoding="utf-8"))
            self.assertEqual(audit["local_only"]["status"], "passed")
            self.assertFalse(audit["local_only"]["network_required"])
            self.assertFalse(audit["local_only"]["credentials_required"])
            doctor = json.loads((tmp_path / "doctor.json").read_text(encoding="utf-8"))
            self.assertEqual(doctor["status"], "passed")

    def test_demo_writes_static_dashboard(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("demo", "--out-dir", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("wrote demo bundles", result.stdout)
            html = (Path(tmp) / "demo_dashboard.html").read_text(encoding="utf-8")
            self.assertIn("Risks", html)
            self.assertIn("Opportunities", html)
            self.assertIn("Stale Badges", html)
            self.assertIn("Catalysts", html)
            energy_snapshot = json.loads((Path(tmp) / "energy_infrastructure_snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(energy_snapshot["ticker"], "NGLP")
            self.assertEqual(energy_snapshot["summary"]["stale_badge_count"], 4)
            self.assertEqual(len(energy_snapshot["catalyst_timeline"]), 3)
            energy_review_queue = json.loads(
                (Path(tmp) / "energy_infrastructure_review_queue.json").read_text(encoding="utf-8")
            )
            self.assertGreaterEqual(energy_review_queue["summary"]["missing_evidence_count"], 4)
            self.assertIn(
                "Rate-case filing",
                {item["topic"] for item in energy_review_queue["items"]},
            )
            prior_snapshot = json.loads((Path(tmp) / "demo_prior_snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(prior_snapshot["as_of"], "2026-02-15")
            compare = json.loads((Path(tmp) / "demo_compare.json").read_text(encoding="utf-8"))
            self.assertEqual(compare["before_as_of"], "2026-02-15")
            self.assertEqual(compare["after_as_of"], "2026-05-15")
            self.assertIn("interpretation", compare)
            self.assertIn("gross margin", {item["topic"] for item in compare["risk_changes"]})
            compare_report = (Path(tmp) / "demo_compare.md").read_text(encoding="utf-8")
            self.assertIn("How To Read This Compare", compare_report)
            self.assertIn("Opportunity attention increased", compare_report)
            energy_report = (Path(tmp) / "energy_infrastructure_report.md").read_text(encoding="utf-8")
            self.assertIn("Northstar Grid & LNG Partners", energy_report)
            energy_dashboard = (Path(tmp) / "energy_infrastructure_dashboard.html").read_text(encoding="utf-8")
            self.assertIn("capital cost inflation", energy_dashboard)
            apple_snapshot = json.loads((Path(tmp) / "public_apple_static_case_study_snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(apple_snapshot["ticker"], "AAPL")
            self.assertEqual(apple_snapshot["source_attribution"][0]["source_type"], "company_investor_relations")
            apple_report = (Path(tmp) / "public_apple_static_case_study_report.md").read_text(encoding="utf-8")
            self.assertIn("Static educational case-study fixture", apple_report)
            self.assertIn("U.S. SEC EDGAR", apple_report)
            apple_dashboard = (Path(tmp) / "public_apple_static_case_study_dashboard.html").read_text(encoding="utf-8")
            self.assertIn("Static educational case study", apple_dashboard)
            semiconductor_snapshot = json.loads((Path(tmp) / "semiconductor_equipment_snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(semiconductor_snapshot["ticker"], "ASML")
            self.assertEqual(semiconductor_snapshot["summary"]["review_queue_count"], 2)
            semiconductor_report = (Path(tmp) / "semiconductor_equipment_report.md").read_text(encoding="utf-8")
            self.assertIn("ASML Holding N.V.", semiconductor_report)
            self.assertIn("ASML Investor Relations", semiconductor_report)
            semiconductor_dashboard = (Path(tmp) / "semiconductor_equipment_dashboard.html").read_text(encoding="utf-8")
            self.assertIn("demand timing and export controls", semiconductor_dashboard)
            audit = json.loads((Path(tmp) / "package_audit.json").read_text(encoding="utf-8"))
            self.assertIn("agent-workflow", audit["commands"])
            self.assertIn("doctor", audit["commands"])
            self.assertIn("review-queue-jsonl", audit["commands"])
            self.assertIn("handoff-packet", audit["commands"])
            doctor = json.loads((Path(tmp) / "doctor.json").read_text(encoding="utf-8"))
            self.assertEqual(doctor["artifact_type"], "doctor_report")
            self.assertEqual(doctor["status"], "passed")
            doctor_markdown = (Path(tmp) / "doctor.md").read_text(encoding="utf-8")
            self.assertIn("Doctor Report", doctor_markdown)
            self.assertIn(NON_ADVICE_TEXT, doctor_markdown)
            jsonl_lines = (Path(tmp) / "demo_review_queue_items.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertGreaterEqual(len(jsonl_lines), 10)
            jsonl_records = [json.loads(line) for line in jsonl_lines]
            self.assertEqual(jsonl_records[0]["record_type"], "review_queue_item")
            self.assertEqual(jsonl_records[0]["fixture_slug"], "demo")
            self.assertEqual(jsonl_records[0]["fixture_path"], "examples/input/demo_company.json")
            self.assertIn("review_item", jsonl_records[0])
            self.assertIn("demo_prior", {record["fixture_slug"] for record in jsonl_records})
            handoff = json.loads((Path(tmp) / "handoff_packet.json").read_text(encoding="utf-8"))
            self.assertEqual(handoff["artifacts"][0]["path"], f"{tmp}/demo_report.md")
            self.assertEqual(handoff["artifacts"][1]["format"], "jsonl")
            handoff_markdown = (Path(tmp) / "handoff_packet.md").read_text(encoding="utf-8")
            self.assertIn("Portfolio/Thesis Handoff Packet", handoff_markdown)
            self.assertIn("demo_review_queue_items.jsonl", handoff_markdown)
            playbook_examples = json.loads((Path(tmp) / "playbook_output_examples.json").read_text(encoding="utf-8"))
            self.assertEqual(playbook_examples["artifact_type"], "playbook_output_examples")
            self.assertEqual(playbook_examples["playbook_count"], 3)
            quarterly_example = next(
                example for example in playbook_examples["examples"] if example["slug"] == "quarterly-review"
            )
            self.assertIn(f"{tmp}/demo_compare.md", {artifact["path"] for artifact in quarterly_example["generated_artifacts"]})
            playbook_examples_markdown = (Path(tmp) / "playbook_output_examples.md").read_text(encoding="utf-8")
            self.assertIn("Playbook Output Examples", playbook_examples_markdown)
            self.assertIn("Selfcheck", playbook_examples_markdown)
            handoff_examples = json.loads((Path(tmp) / "handoff_packet_examples.json").read_text(encoding="utf-8"))
            self.assertEqual(handoff_examples["artifact_type"], "handoff_packet_examples")
            self.assertEqual(handoff_examples["example_count"], 3)
            catalyst_handoff = next(
                example for example in handoff_examples["examples"] if example["slug"] == "catalyst-check-in"
            )
            self.assertEqual(catalyst_handoff["packet"]["artifacts"][1]["format"], "jsonl")
            self.assertIn(f"{tmp}/energy_infrastructure_report.md", catalyst_handoff["packet"]["artifacts"][0]["path"])
            handoff_examples_markdown = (Path(tmp) / "handoff_packet_examples.md").read_text(encoding="utf-8")
            self.assertIn("Handoff Packet Examples", handoff_examples_markdown)
            self.assertIn("Post-Earnings Thesis Refresh Handoff", handoff_examples_markdown)
            fixture_catalog = (Path(tmp) / "fixture_catalog.md").read_text(encoding="utf-8")
            self.assertIn("Fixture Catalog", fixture_catalog)
            self.assertIn("examples/input/public_apple_static_case_study.json", fixture_catalog)
            self.assertIn("examples/input/semiconductor_equipment.json", fixture_catalog)
            self.assertIn("static public-source case study", fixture_catalog)
            source_boundary_evidence = json.loads((Path(tmp) / "source_boundary_evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(source_boundary_evidence["artifact_type"], "source_boundary_evidence")
            self.assertTrue(source_boundary_evidence["checks"]["no_live_fetching_required"])
            self.assertTrue(source_boundary_evidence["checks"]["no_advice_claim_present"])
            source_boundary_markdown = (Path(tmp) / "source_boundary_evidence.md").read_text(encoding="utf-8")
            self.assertIn("Source Boundary Evidence", source_boundary_markdown)
            self.assertIn("examples/input/semiconductor_equipment.json", source_boundary_markdown)
            risk_taxonomy = (Path(tmp) / "risk_language_taxonomy.md").read_text(encoding="utf-8")
            self.assertIn("Risk Language Taxonomy", risk_taxonomy)
            self.assertIn("../../docs/scoring.md", risk_taxonomy)
            self.assertIn("Items with more review issue categories appear first", risk_taxonomy)
            template_catalog = json.loads((Path(tmp) / "template_catalog.json").read_text(encoding="utf-8"))
            self.assertEqual(template_catalog["artifact_type"], "template_catalog")
            self.assertEqual(template_catalog["template_count"], 3)
            self.assertIn("consumer_hardware", {template["slug"] for template in template_catalog["templates"]})
            template_markdown = (Path(tmp) / "template_catalog.md").read_text(encoding="utf-8")
            self.assertIn("Template Catalog", template_markdown)
            self.assertIn("Recommended Fields And Commands", template_markdown)
            self.assertIn("examples/templates/consumer_hardware_earnings_review.json", template_markdown)
            playbooks = json.loads((Path(tmp) / "playbooks.json").read_text(encoding="utf-8"))
            self.assertEqual(playbooks["playbook_count"], 3)
            self.assertIn("Post-Earnings Thesis Refresh", {playbook["title"] for playbook in playbooks["playbooks"]})
            playbook_markdown = (Path(tmp) / "playbooks.md").read_text(encoding="utf-8")
            self.assertIn("Recommended CLI Sequences", playbook_markdown)
            self.assertIn(NON_ADVICE_TEXT, playbook_markdown)
            promotion_pack = json.loads((Path(tmp) / "promotion_pack.json").read_text(encoding="utf-8"))
            self.assertEqual(promotion_pack["artifact_type"], "promotion_pack")
            self.assertIn(
                "examples/output/public_apple_static_case_study_dashboard.html",
                {demo["path"] for demo in promotion_pack["demos"]},
            )
            self.assertIn("docs/promotion-page-outline.md", promotion_pack["source_evidence"])
            promotion_pack_md = (Path(tmp) / "promotion_pack.md").read_text(encoding="utf-8")
            self.assertIn("Public Promotion Pack", promotion_pack_md)
            self.assertIn("Proof Commands", promotion_pack_md)
            self.assertIn(NON_ADVICE_TEXT, promotion_pack_md)
            publication_checklist = json.loads((Path(tmp) / "publication_checklist.json").read_text(encoding="utf-8"))
            self.assertEqual(publication_checklist["artifact_type"], "publication_checklist")
            self.assertEqual(publication_checklist["step_count"], 7)
            publication_checklist_md = (Path(tmp) / "publication_checklist.md").read_text(encoding="utf-8")
            self.assertIn("Create The GitHub Release", publication_checklist_md)
            self.assertIn("gh release create v0.9.0", publication_checklist_md)
            data_entry_checklist = json.loads((Path(tmp) / "data_entry_checklist.json").read_text(encoding="utf-8"))
            self.assertEqual(data_entry_checklist["artifact_type"], "data_entry_checklist")
            data_entry_checklist_md = (Path(tmp) / "data_entry_checklist.md").read_text(encoding="utf-8")
            self.assertIn("Data Entry Checklist", data_entry_checklist_md)
            agent_workflow = json.loads((Path(tmp) / "agent_workflow.json").read_text(encoding="utf-8"))
            self.assertEqual(agent_workflow["artifact_type"], "agent_workflow")
            self.assertEqual(agent_workflow["source_doc"], "docs/agent-workflow.md")
            agent_workflow_md = (Path(tmp) / "agent_workflow.md").read_text(encoding="utf-8")
            self.assertIn("Agent Workflow", agent_workflow_md)
            self.assertIn("Review Queue Route", agent_workflow_md)
            demo_screenshot_guide = json.loads((Path(tmp) / "demo_screenshot_guide.json").read_text(encoding="utf-8"))
            self.assertEqual(demo_screenshot_guide["artifact_type"], "demo_screenshot_guide")
            self.assertIn("docs/demo-screenshot-guide.md", demo_screenshot_guide["source_doc"])
            demo_screenshot_guide_md = (Path(tmp) / "demo_screenshot_guide.md").read_text(encoding="utf-8")
            self.assertIn("Demo Screenshot Guide", demo_screenshot_guide_md)
            self.assertIn("examples/output/public_apple_static_case_study_dashboard.html", demo_screenshot_guide_md)
            fresh_clone_plan = json.loads((Path(tmp) / "fresh_clone_plan.json").read_text(encoding="utf-8"))
            self.assertEqual(fresh_clone_plan["artifact_type"], "fresh_clone_verification_plan")
            self.assertIn("docs/fresh-clone-verification.md", fresh_clone_plan["source_doc"])
            fresh_clone_plan_md = (Path(tmp) / "fresh_clone_plan.md").read_text(encoding="utf-8")
            self.assertIn("Fresh Clone Verification Plan", fresh_clone_plan_md)
            self.assertIn("verification/fresh-clone/demo_company_snapshot.json", fresh_clone_plan_md)
            manifest_paths = {
                item["path"]
                for item in json.loads((Path(tmp) / "release_manifest.json").read_text(encoding="utf-8"))["files"]
            }
            self.assertIn("src/earnings_call_risk_map/audit.py", manifest_paths)
            self.assertIn("examples/output/doctor.md", manifest_paths)
            self.assertIn("examples/output/doctor.json", manifest_paths)
            self.assertIn("examples/output/examples_index.md", manifest_paths)
            self.assertIn("examples/output/examples_index.json", manifest_paths)
            self.assertIn("examples/output/publication_checklist.md", manifest_paths)
            self.assertIn("examples/output/publication_checklist.json", manifest_paths)
            self.assertIn("examples/output/agent_workflow.md", manifest_paths)
            self.assertIn("examples/output/agent_workflow.json", manifest_paths)
            self.assertIn("examples/output/data_entry_checklist.md", manifest_paths)
            self.assertIn("examples/output/data_entry_checklist.json", manifest_paths)
            self.assertIn("examples/output/demo_screenshot_guide.md", manifest_paths)
            self.assertIn("examples/output/demo_screenshot_guide.json", manifest_paths)
            self.assertIn("examples/output/fresh_clone_plan.md", manifest_paths)
            self.assertIn("examples/output/fresh_clone_plan.json", manifest_paths)
            report = (Path(tmp) / "demo_report.md").read_text(encoding="utf-8")
            review_queue = (Path(tmp) / "demo_review_queue.md").read_text(encoding="utf-8")
            package_audit = (Path(tmp) / "package_audit.md").read_text(encoding="utf-8")
            self.assertIn(NON_ADVICE_TEXT, report)
            self.assertIn(NON_ADVICE_TEXT, review_queue)
            self.assertIn(NON_ADVICE_TEXT, package_audit)
            self.assertIn("Package Audit", package_audit)
            command_cheat_sheet = json.loads((Path(tmp) / "command_cheat_sheet.json").read_text(encoding="utf-8"))
            self.assertEqual(command_cheat_sheet["artifact_type"], "command_cheat_sheet")
            self.assertIn("agent-workflow", {item["command"] for item in command_cheat_sheet["commands"]})
            self.assertIn("cheat-sheet", {item["command"] for item in command_cheat_sheet["commands"]})
            self.assertIn("data-entry-checklist", {item["command"] for item in command_cheat_sheet["commands"]})
            self.assertIn("fresh-clone-plan", {item["command"] for item in command_cheat_sheet["commands"]})
            command_cheat_sheet_md = (Path(tmp) / "command_cheat_sheet.md").read_text(encoding="utf-8")
            self.assertIn("Command Cheat Sheet", command_cheat_sheet_md)
            self.assertIn("| `analyze` | Analyze one earnings-call JSON input |", command_cheat_sheet_md)
            command_cheatsheet = json.loads((Path(tmp) / "command_cheatsheet.json").read_text(encoding="utf-8"))
            self.assertEqual(command_cheatsheet, command_cheat_sheet)
            command_cheatsheet_md = (Path(tmp) / "command_cheatsheet.md").read_text(encoding="utf-8")
            self.assertEqual(command_cheatsheet_md, command_cheat_sheet_md)
            examples_index = json.loads((Path(tmp) / "examples_index.json").read_text(encoding="utf-8"))
            self.assertEqual(examples_index["artifact_type"], "examples_index")
            self.assertEqual(examples_index["summary"]["fixture_count"], 7)
            self.assertEqual(examples_index["summary"]["template_count"], 3)
            examples_index_md = (Path(tmp) / "examples_index.md").read_text(encoding="utf-8")
            self.assertIn("Examples Index", examples_index_md)
            self.assertIn("Recommended next command", examples_index_md)
            case_study_map = json.loads((Path(tmp) / "case_study_map.json").read_text(encoding="utf-8"))
            self.assertEqual(case_study_map["artifact_type"], "case_study_map")
            self.assertEqual(case_study_map["fixture_count"], 7)
            case_study_map_md = (Path(tmp) / "case_study_map.md").read_text(encoding="utf-8")
            self.assertIn("Case Study Map", case_study_map_md)
            self.assertIn("examples/input/sample_filled_template_workflow.json", case_study_map_md)

    def test_review_queue_jsonl_outputs_demo_fixture_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "review_items.jsonl"
            result = self.run_cli("review-queue-jsonl", "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            lines = out.read_text(encoding="utf-8").splitlines()
            self.assertGreaterEqual(len(lines), 10)
            records = [json.loads(line) for line in lines]
            self.assertEqual(records[0]["fixture_slug"], "demo")
            self.assertEqual(records[0]["item_index"], 1)
            self.assertEqual(records[0]["ticker"], "EXM")
            self.assertIn("source_boundaries", records[0])
            self.assertIn("review_item", records[0])
            self.assertIn("public_apple_static_case_study", {record["fixture_slug"] for record in records})
            self.assertIn("semiconductor_equipment", {record["fixture_slug"] for record in records})

    def test_handoff_packet_outputs_markdown_and_json(self):
        result = self.run_cli("handoff-packet")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Portfolio/Thesis Handoff Packet", result.stdout)
        self.assertIn("examples/output/demo_report.md", result.stdout)
        self.assertIn("examples/output/demo_review_queue_items.jsonl", result.stdout)
        self.assertIn("examples/output/demo_compare.md", result.stdout)
        self.assertIn("Downstream portfolio and thesis systems own exposure sizing", result.stdout)
        self.assertIn(NON_ADVICE_TEXT, result.stdout)

        json_result = self.run_cli("handoff-packet", "--format", "json")
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        stdout_payload = json.loads(json_result.stdout)
        self.assertEqual(stdout_payload["artifacts"][0]["path"], "examples/output/demo_report.md")
        self.assertEqual(stdout_payload["artifacts"][1]["format"], "jsonl")

        with tempfile.TemporaryDirectory() as tmp:
            json_out = Path(tmp) / "handoff_packet.json"
            md_out = Path(tmp) / "handoff_packet.md"
            jsonl_path = Path(tmp) / "queue.jsonl"
            compare_path = Path(tmp) / "compare.json"
            result = self.run_cli(
                "handoff-packet",
                "--report-path",
                str(Path(tmp) / "report.md"),
                "--review-queue-jsonl-path",
                str(jsonl_path),
                "--compare-path",
                str(compare_path),
                "--json-out",
                str(json_out),
                "--md-out",
                str(md_out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["packet_type"], "portfolio_thesis_handoff")
            self.assertEqual(payload["artifacts"][1]["path"], str(jsonl_path))
            self.assertEqual(payload["artifacts"][2]["format"], "json")
            self.assertEqual(payload["handoff_targets"], ["portfolio_risk_review", "thesis_ledger"])
            self.assertGreaterEqual(len(payload["cautions"]), 5)
            self.assertIn(NON_ADVICE_TEXT, payload["safety_notice"])
            markdown = md_out.read_text(encoding="utf-8")
            self.assertIn("Artifact Paths", markdown)
            self.assertIn(str(compare_path), markdown)

    def test_manifest_lists_package_file(self):
        result = self.run_cli("manifest")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        paths = {item["path"] for item in payload["files"]}
        self.assertIn("src/earnings_call_risk_map/cli.py", paths)

    def test_maturity_evidence_writes_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli("maturity-evidence", "--out-dir", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("wrote maturity evidence bundle", result.stdout)
            json_path = Path(tmp) / "maturity_evidence.json"
            md_path = Path(tmp) / "maturity_evidence.md"
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["command_count"], 31)
            self.assertEqual(payload["fixture_count"], 7)
            self.assertIn("PYTHONPATH=src python -m unittest discover -s tests", payload["test_commands"])
            self.assertIn("PYTHONPATH=src python -m earnings_call_risk_map release-assets", payload["verification_commands"])
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map promotion-pack --format markdown --out examples/output/promotion_pack.md",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map publication-checklist --format markdown --out examples/output/publication_checklist.md",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map agent-workflow --format markdown --out examples/output/agent_workflow.md",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map agent-workflow --format json --out examples/output/agent_workflow.json",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map data-entry-checklist --format markdown --out examples/output/data_entry_checklist.md",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format markdown --out examples/output/schema_authoring_reference.md",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format json --out examples/output/schema_authoring_reference.json",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map demo-screenshot-guide --format markdown --out examples/output/demo_screenshot_guide.md",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map demo-screenshot-guide --format json --out examples/output/demo_screenshot_guide.json",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format markdown --out examples/output/fresh_clone_plan.md",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format json --out examples/output/fresh_clone_plan.json",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format json --out examples/output/source_boundary_evidence.json",
                payload["verification_commands"],
            )
            self.assertIn(
                "PYTHONPATH=src python -m earnings_call_risk_map doctor --format json --out examples/output/doctor.json",
                payload["verification_commands"],
            )
            self.assertIn("examples/output/demo_report.md", payload["artifact_paths"])
            self.assertIn("examples/output/doctor.json", payload["artifact_paths"])
            self.assertIn("examples/output/promotion_pack.md", payload["artifact_paths"])
            self.assertIn("examples/output/publication_checklist.md", payload["artifact_paths"])
            self.assertIn("examples/output/agent_workflow.md", payload["artifact_paths"])
            self.assertIn("examples/output/agent_workflow.json", payload["artifact_paths"])
            self.assertIn("examples/output/data_entry_checklist.md", payload["artifact_paths"])
            self.assertIn("examples/output/schema_authoring_reference.md", payload["artifact_paths"])
            self.assertIn("examples/output/schema_authoring_reference.json", payload["artifact_paths"])
            self.assertIn("examples/output/demo_screenshot_guide.md", payload["artifact_paths"])
            self.assertIn("examples/output/fresh_clone_plan.md", payload["artifact_paths"])
            self.assertIn("examples/output/source_boundary_evidence.json", payload["artifact_paths"])
            self.assertEqual(payload["release_asset_checklist"]["status"], "passed")
            self.assertEqual(payload["release_asset_checklist"]["missing_assets"], [])
            self.assertGreater(payload["release_asset_checklist"]["present_count"], 0)
            self.assertEqual(payload["latest_review_score"]["overall"], "94/100")
            self.assertEqual(
                payload["latest_review_score"]["source"],
                "reports/reviews/2026-06-18-v0.9.0-final-review.md",
            )
            self.assertEqual(payload["evidence_summary"]["command_count"], payload["command_count"])
            self.assertEqual(payload["evidence_summary"]["fixture_count"], payload["fixture_count"])
            self.assertEqual(payload["evidence_summary"]["release_asset_status"], "passed")
            self.assertEqual(payload["evidence_summary"]["privacy_scan_status"], payload["privacy_scan"]["status"])
            self.assertEqual(payload["evidence_summary"]["latest_review_score"], "94/100")
            self.assertEqual(payload["skill"]["path"], "skills/agent/earnings-call-risk-map/SKILL.md")
            self.assertTrue(payload["skill"]["present"])
            self.assertEqual(payload["review_template"]["path"], "reports/reviews/release-readiness-review.md")
            self.assertTrue(payload["review_template"]["present"])
            self.assertIn(payload["privacy_scan"]["status"], {"passed", "failed"})
            markdown = md_path.read_text(encoding="utf-8")
            self.assertIn("Maturity Evidence Bundle", markdown)
            self.assertIn("- Commands: 31", markdown)
            self.assertIn("- Fixtures: 7", markdown)
            self.assertIn("- Release assets: passed", markdown)
            self.assertIn("- Latest review score: 94/100", markdown)
            self.assertIn("Privacy scan", markdown)
            self.assertIn(NON_ADVICE_TEXT, markdown)

    def test_maturity_evidence_script_writes_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, "scripts/maturity_evidence.py", "--out-dir", tmp],
                cwd=ROOT,
                env=ENV,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("wrote maturity evidence bundle", result.stdout)
            payload = json.loads((Path(tmp) / "maturity_evidence.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["command_count"], 31)
            self.assertEqual(payload["fixture_count"], 7)
            self.assertEqual(payload["release_asset_checklist"]["status"], "passed")
            self.assertEqual(payload["latest_review_score"]["overall"], "94/100")
            self.assertEqual(payload["privacy_scan"]["status"], "passed")


def _extract_readme_module_cli_commands(readme: str) -> list[tuple[str, ...]]:
    commands: list[tuple[str, ...]] = []
    for block in README_BASH_BLOCK_RE.findall(readme):
        for line in _logical_shell_lines(block):
            parts = shlex.split(line)
            if not parts:
                continue
            while parts and "=" in parts[0] and not parts[0].startswith("-"):
                key, _value = parts[0].split("=", 1)
                if not key.replace("_", "").isalnum():
                    break
                parts = parts[1:]
            if parts[:3] == ["python", "-m", "earnings_call_risk_map"]:
                commands.append(tuple(parts[3:]))
            elif parts and parts[0] == "earnings-call-risk-map":
                commands.append(tuple(parts[1:]))
    return commands


def _logical_shell_lines(block: str) -> list[str]:
    lines: list[str] = []
    pending = ""
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if pending:
            line = f"{pending} {line}"
        if line.endswith("\\"):
            pending = line[:-1].strip()
            continue
        pending = ""
        lines.append(line)
    if pending:
        lines.append(pending)
    return lines


def _rewrite_readme_cli_args_for_temp_outputs(
    command: tuple[str, ...],
    tmp_path: Path,
    before_snapshot: Path,
    after_snapshot: Path,
) -> tuple[str, ...]:
    rewritten = list(command)
    if rewritten and rewritten[0] == "compare":
        for index, value in enumerate(rewritten):
            if value == "examples/output/demo_prior_snapshot.json":
                rewritten[index] = str(before_snapshot)
            elif value == "examples/output/demo_snapshot.json":
                rewritten[index] = str(after_snapshot)
            elif value == "before.json":
                rewritten[index] = str(before_snapshot)
            elif value == "after.json":
                rewritten[index] = str(after_snapshot)

    output_flags = {"--json-out", "--md-out", "--html-out", "--out", "--out-dir"}
    for index, value in enumerate(rewritten[:-1]):
        if value in output_flags:
            rewritten[index + 1] = str(tmp_path / _temp_output_name(rewritten[index + 1], value))
    return tuple(rewritten)


def _temp_output_name(path_text: str, flag: str) -> str:
    path = Path(path_text)
    if flag == "--out-dir":
        return f"{path.name or 'out'}_{_safe_path_suffix(path_text)}"
    if path.name:
        return path.name
    return f"readme_output_{_safe_path_suffix(path_text)}"


def _safe_path_suffix(path_text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", path_text).strip("_") or "out"


if __name__ == "__main__":
    unittest.main()
