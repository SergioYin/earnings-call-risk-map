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

    def test_version(self):
        result = self.run_cli("version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "0.4.0")

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

    def test_audit_reports_package_parity_json_and_markdown(self):
        result = self.run_cli("audit")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["version"], "0.4.0")
        self.assertIn("audit", payload["commands"])
        self.assertEqual(payload["fixture_count"], 4)
        self.assertGreaterEqual(payload["output_artifact_count"], 5)
        self.assertFalse(payload["has_workflow_files"])
        self.assertTrue(payload["skill"]["present"])

        md_result = self.run_cli("audit", "--format", "markdown")
        self.assertEqual(md_result.returncode, 0, md_result.stderr)
        self.assertIn("# Package Audit", md_result.stdout)
        self.assertIn("Workflow files present: no", md_result.stdout)
        self.assertIn("Skill present: yes", md_result.stdout)
        self.assertIn(NON_ADVICE_TEXT, md_result.stdout)

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
            self.assertIn("review-queue", audit["commands"])
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
