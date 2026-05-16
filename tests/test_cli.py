import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
NON_ADVICE_TEXT = "does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice"
LOCAL_ONLY_ENV = {
    "PATH": os.environ.get("PATH", ""),
    "PYTHONPATH": str(ROOT / "src"),
    "PYTHONNOUSERSITE": "1",
    "HOME": str(ROOT),
}


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

    def test_version(self):
        result = self.run_cli("version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "0.6.0")

    def test_help_uses_public_safe_wording(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        help_text = " ".join(result.stdout.split())
        self.assertIn("Educational research review only", help_text)
        self.assertIn("not personalized investment, legal, accounting, tax, buy, sell, or hold advice", help_text)
        self.assertIn("analyze", result.stdout)

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

    def test_audit_reports_package_parity_json_and_markdown(self):
        result = self.run_cli("audit")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["version"], "0.6.0")
        self.assertIn("audit", payload["commands"])
        self.assertIn("fixture-catalog", payload["commands"])
        self.assertIn("playbooks", payload["commands"])
        self.assertIn("release-assets", payload["commands"])
        self.assertIn("review-queue-jsonl", payload["commands"])
        self.assertEqual(payload["fixture_count"], 4)
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

    def test_release_assets_reports_current_version_assets(self):
        result = self.run_cli("release-assets")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["version"], "0.6.0")
        self.assertEqual(payload["status"], "passed")
        self.assertEqual(payload["missing_assets"], [])
        self.assertIn("docs/release-notes-v0.6.0.md", payload["expected_assets"])
        self.assertIn("reports/reviews/release-readiness-review.md", payload["present_assets"])

        md_result = self.run_cli("release-assets", "--format", "markdown")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Release Asset Checklist", md_result.stdout)
        self.assertIn("- Status: `passed`", md_result.stdout)
        self.assertIn("- [x] `docs/release-notes-v0.6.0.md`", md_result.stdout)

    def test_release_assets_reports_missing_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "release-notes-v0.6.0.md").write_text("release notes", encoding="utf-8")
            out = root / "missing_assets.md"

            result = self.run_cli("release-assets", "--root", str(root), "--format", "markdown", "--out", str(out))

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(result.stdout, "")
            markdown = out.read_text(encoding="utf-8")
            self.assertIn("- Status: `failed`", markdown)
            self.assertIn("## Missing Assets", markdown)
            self.assertIn("- [x] `docs/release-notes-v0.6.0.md`", markdown)
            self.assertIn("- [ ] `README.md`", markdown)

            json_result = self.run_cli("release-assets", "--root", str(root))
            self.assertEqual(json_result.returncode, 1, json_result.stderr)
            payload = json.loads(json_result.stdout)
            self.assertEqual(payload["status"], "failed")
            self.assertGreater(payload["missing_count"], 0)
            self.assertIn("README.md", payload["missing_assets"])

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
                (
                    "handoff-packet",
                    "--json-out",
                    str(tmp_path / "handoff_packet.json"),
                    "--md-out",
                    str(tmp_path / "handoff_packet.md"),
                ),
                ("fixture-catalog", "--out", str(tmp_path / "fixture_catalog.md")),
                ("playbooks", "--format", "markdown", "--out", str(tmp_path / "playbooks.md")),
                ("playbooks", "--format", "json", "--out", str(tmp_path / "playbooks.json")),
                ("audit", "--format", "json", "--out", str(tmp_path / "package_audit.json")),
                ("release-assets", "--format", "json", "--out", str(tmp_path / "release_assets.json")),
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
            audit = json.loads((Path(tmp) / "package_audit.json").read_text(encoding="utf-8"))
            self.assertIn("review-queue-jsonl", audit["commands"])
            self.assertIn("handoff-packet", audit["commands"])
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
            self.assertIn("static public-source case study", fixture_catalog)
            playbooks = json.loads((Path(tmp) / "playbooks.json").read_text(encoding="utf-8"))
            self.assertEqual(playbooks["playbook_count"], 3)
            self.assertIn("Post-Earnings Thesis Refresh", {playbook["title"] for playbook in playbooks["playbooks"]})
            playbook_markdown = (Path(tmp) / "playbooks.md").read_text(encoding="utf-8")
            self.assertIn("Recommended CLI Sequences", playbook_markdown)
            self.assertIn(NON_ADVICE_TEXT, playbook_markdown)
            self.assertIn("src/earnings_call_risk_map/audit.py", {
                item["path"]
                for item in json.loads((Path(tmp) / "release_manifest.json").read_text(encoding="utf-8"))["files"]
            })
            report = (Path(tmp) / "demo_report.md").read_text(encoding="utf-8")
            review_queue = (Path(tmp) / "demo_review_queue.md").read_text(encoding="utf-8")
            package_audit = (Path(tmp) / "package_audit.md").read_text(encoding="utf-8")
            self.assertIn(NON_ADVICE_TEXT, report)
            self.assertIn(NON_ADVICE_TEXT, review_queue)
            self.assertIn(NON_ADVICE_TEXT, package_audit)
            self.assertIn("Package Audit", package_audit)

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
            self.assertIn("PYTHONPATH=src python -m unittest discover -s tests", payload["test_commands"])
            self.assertIn("PYTHONPATH=src python -m earnings_call_risk_map release-assets", payload["verification_commands"])
            self.assertIn("examples/output/demo_report.md", payload["artifact_paths"])
            self.assertEqual(payload["skill"]["path"], "skills/agent/earnings-call-risk-map/SKILL.md")
            self.assertTrue(payload["skill"]["present"])
            self.assertEqual(payload["review_template"]["path"], "reports/reviews/release-readiness-review.md")
            self.assertTrue(payload["review_template"]["present"])
            self.assertIn(payload["privacy_scan"]["status"], {"passed", "failed"})
            markdown = md_path.read_text(encoding="utf-8")
            self.assertIn("Maturity Evidence Bundle", markdown)
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
            self.assertEqual(payload["privacy_scan"]["status"], "passed")


if __name__ == "__main__":
    unittest.main()
