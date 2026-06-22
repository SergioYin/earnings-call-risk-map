import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from earnings_call_risk_map.evidence_handoff_compare import (
    SCHEMA_LABEL,
    _safe_input_label,
    build_evidence_handoff_compare,
    render_evidence_handoff_compare_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


class EvidenceHandoffCompareTests(unittest.TestCase):
    def test_compares_by_relative_path_and_reports_metadata_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before.json"
            after = Path(tmp) / "after.json"
            before.write_text(
                json.dumps(
                    {
                        "schema": "earnings-call-risk-map.evidence-handoff-audit.v1",
                        "checked_artifacts": [
                            {
                                "relative_path": "README.md",
                                "role": "documentation",
                                "present": True,
                                "bytes": 10,
                                "sha256": "a" * 64,
                            },
                            {
                                "relative_path": "examples/output/old.md",
                                "role": "generated_markdown",
                                "present": True,
                                "bytes": 20,
                                "sha256": "b" * 64,
                            },
                        ],
                        "boundaries": ["local/static fixtures only", "no live data"],
                    }
                ),
                encoding="utf-8",
            )
            after.write_text(
                json.dumps(
                    {
                        "schema": "earnings-call-risk-map.evidence-handoff-audit.v1",
                        "checked_artifacts": [
                            {
                                "relative_path": "README.md",
                                "role": "documentation",
                                "present": True,
                                "bytes": 12,
                                "sha256": "c" * 64,
                                "freshness_status": "static_reviewed",
                            },
                            {
                                "relative_path": "examples/output/new.md",
                                "role": "generated_markdown",
                                "present": True,
                                "bytes": 30,
                                "sha256": "d" * 64,
                            },
                        ],
                        "boundaries": [
                            "local/static fixtures only",
                            "no live data",
                            "no broker connection",
                            "no private data",
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = build_evidence_handoff_compare(before, after)

        self.assertEqual(report["schema"], SCHEMA_LABEL)
        self.assertEqual(report["summary"]["added_count"], 1)
        self.assertEqual(report["summary"]["removed_count"], 1)
        self.assertEqual(report["summary"]["changed_count"], 1)
        self.assertEqual(report["summary"]["unchanged_count"], 0)
        self.assertEqual(report["changed"][0]["key"], "README.md")
        changed_fields = {item["field"] for item in report["changed"][0]["differences"]}
        self.assertEqual(changed_fields, {"bytes", "sha256", "freshness_status"})
        self.assertIn("no broker connection", report["boundary_comparison"]["added"])
        self.assertIn("no private data", report["boundaries"])

    def test_prefers_evidence_id_over_relative_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before.json"
            after = Path(tmp) / "after.json"
            before.write_text(
                json.dumps(
                    {
                        "checked_artifacts": [
                            {
                                "evidence_id": "release-notes",
                                "relative_path": "docs/release-notes-v0.9.4.md",
                                "role": "documentation",
                                "present": True,
                                "bytes": 10,
                                "sha256": "a" * 64,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            after.write_text(
                json.dumps(
                    {
                        "checked_artifacts": [
                            {
                                "evidence_id": "release-notes",
                                "relative_path": "docs/release-notes-v0.9.6.md",
                                "role": "documentation",
                                "present": True,
                                "bytes": 10,
                                "sha256": "a" * 64,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            report = build_evidence_handoff_compare(before, after)

        self.assertEqual(report["summary"]["unchanged_count"], 1)
        self.assertEqual(report["unchanged"][0]["key"], "release-notes")

    def test_markdown_includes_boundaries_and_changed_table(self):
        markdown = render_evidence_handoff_compare_markdown(
            {
                "schema": SCHEMA_LABEL,
                "package": "earnings-call-risk-map",
                "version": "test",
                "inputs": {"before": "before.json", "after": "after.json"},
                "summary": {
                    "added_count": 0,
                    "removed_count": 0,
                    "changed_count": 1,
                    "unchanged_count": 1,
                    "boundary_changed": False,
                    "safety_notice_changed": False,
                },
                "changed": [
                    {
                        "key": "a|b",
                        "relative_path": "examples/output/a|b.md",
                        "differences": [{"field": "sha256", "before": "a", "after": "b"}],
                    }
                ],
                "added": [],
                "removed": [],
                "boundary_comparison": {"added": [], "removed": [], "unchanged": ["no live data"]},
                "comparison_notes": ["metadata only"],
                "boundaries": ["local/static fixtures only", "no live data", "no private data"],
            }
        )

        self.assertIn("Evidence Handoff Compare", markdown)
        self.assertIn("local/static fixtures only", markdown)
        self.assertIn("no private data", markdown)
        self.assertIn("a\\|b", markdown)

    def test_cli_writes_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before.json"
            after = Path(tmp) / "after.json"
            out = Path(tmp) / "compare.json"
            payload = {"checked_artifacts": [{"relative_path": "README.md", "present": True, "bytes": 1}]}
            before.write_text(json.dumps(payload), encoding="utf-8")
            after.write_text(json.dumps(payload), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "earnings_call_risk_map",
                    "evidence-handoff-compare",
                    "--before",
                    str(before),
                    "--after",
                    str(after),
                    "--format",
                    "json",
                    "--output",
                    str(out),
                ],
                cwd=ROOT,
                env=ENV,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["schema"], SCHEMA_LABEL)

    def test_safe_input_label_preserves_relative_paths_without_absolute_checkout(self):
        self.assertEqual(
            _safe_input_label("reports/release/before.json"),
            "reports/release/before.json",
        )
        self.assertEqual(
            _safe_input_label(ROOT / "examples/output/evidence_handoff_compare_demo_before.json"),
            "examples/output/evidence_handoff_compare_demo_before.json",
        )
        self.assertEqual(_safe_input_label("/private/tmp/before.json"), "before.json")

    def test_standalone_cli_reports_invalid_json_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            before = Path(tmp) / "before.json"
            after = Path(tmp) / "after.json"
            before.write_text("{", encoding="utf-8")
            after.write_text(json.dumps({"checked_artifacts": []}), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "earnings_call_risk_map.evidence_handoff_compare",
                    "--before",
                    str(before),
                    "--after",
                    str(after),
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                env=ENV,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("error: before audit JSON is invalid", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_standalone_cli_redacts_absolute_missing_input_path(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "earnings_call_risk_map.evidence_handoff_compare",
                "--before",
                "/tmp/private-before.json",
                "--after",
                "examples/output/evidence_handoff_compare_demo_after.json",
                "--format",
                "json",
            ],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error: before audit JSON could not be read: private-before.json", result.stderr)
        self.assertNotIn("/tmp/private-before.json", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
