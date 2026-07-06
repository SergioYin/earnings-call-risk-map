import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from earnings_call_risk_map.release_owner_compare_blockers import (
    SCHEMA_LABEL,
    build_release_owner_compare_blockers,
    render_release_owner_compare_blockers_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


class ReleaseOwnerCompareBlockersTests(unittest.TestCase):
    def test_classifies_removed_boundary_and_hash_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            compare_path = Path(tmp) / "compare.json"
            compare_path.write_text(
                json.dumps(
                    {
                        "schema": "earnings-call-risk-map.evidence-handoff-compare.v1",
                        "inputs": {"before": "before.json", "after": "after.json"},
                        "summary": {
                            "added_count": 1,
                            "removed_count": 1,
                            "changed_count": 2,
                            "unchanged_count": 1,
                            "boundary_changed": True,
                            "safety_notice_changed": False,
                        },
                        "added": [
                            {
                                "key": "examples/output/new.md",
                                "relative_path": "examples/output/new.md",
                                "present": True,
                            }
                        ],
                        "removed": [
                            {
                                "key": "examples/output/old.md",
                                "relative_path": "examples/output/old.md",
                                "present": True,
                            }
                        ],
                        "changed": [
                            {
                                "key": "examples/output/demo_report.md",
                                "relative_path": "examples/output/demo_report.md",
                                "differences": [
                                    {"field": "bytes", "before": 10, "after": 12},
                                    {"field": "sha256", "before": "a", "after": "b"},
                                    {"field": "freshness_status", "before": "static", "after": "static_reviewed"},
                                ],
                            },
                            {
                                "key": "examples/output/missing.md",
                                "relative_path": "examples/output/missing.md",
                                "differences": [{"field": "present", "before": True, "after": False}],
                            },
                        ],
                        "boundary_comparison": {
                            "added": ["no tax advice"],
                            "removed": ["no live data"],
                            "unchanged": ["local/static fixtures only"],
                        },
                        "boundaries": ["local/static fixtures only", "no live data", "no private data"],
                    }
                ),
                encoding="utf-8",
            )

            report = build_release_owner_compare_blockers(compare_path)

        self.assertEqual(report["schema"], SCHEMA_LABEL)
        self.assertEqual(report["summary"]["release_decision"], "blocked")
        self.assertEqual(report["summary"]["blocker_count"], 3)
        self.assertGreaterEqual(report["summary"]["review_required_count"], 3)
        checks = {item["slug"]: item for item in report["checklist"]}
        self.assertEqual(checks["no-removed-evidence-artifacts"]["status"], "blocker")
        self.assertEqual(checks["no-artifacts-became-missing"]["status"], "blocker")
        self.assertEqual(checks["release-boundaries-preserved"]["status"], "blocker")
        self.assertEqual(checks["added-artifacts-reviewed"]["status"], "review_required")
        self.assertEqual(checks["content-hash-or-size-changes-reviewed"]["status"], "review_required")
        self.assertEqual(checks["source-and-freshness-changes-reviewed"]["status"], "review_required")
        self.assertIn("no live data", report["boundaries"])
        self.assertNotIn(str(ROOT), json.dumps(report, sort_keys=True))

    def test_markdown_includes_blocker_table_and_boundaries(self):
        markdown = render_release_owner_compare_blockers_markdown(
            {
                "schema": SCHEMA_LABEL,
                "package": "earnings-call-risk-map",
                "version": "test",
                "inputs": {"compare": "examples/output/evidence_handoff_compare.json"},
                "summary": {
                    "release_decision": "review_required",
                    "blocker_count": 0,
                    "review_required_count": 1,
                    "compare_added_count": 1,
                    "compare_removed_count": 0,
                    "compare_changed_count": 1,
                    "compare_unchanged_count": 2,
                },
                "checklist": [
                    {
                        "title": "Hash changed | review",
                        "status": "review_required",
                        "evidence": [{"key": "a|b", "relative_path": "examples/output/a|b.md"}],
                        "reviewer_action": "Review diff | regenerate",
                    }
                ],
                "release_owner_notes": ["metadata only"],
                "boundaries": ["local/static fixtures only", "no live data", "no private data"],
            }
        )

        self.assertIn("Release Owner Compare Blocker Checklist", markdown)
        self.assertIn("`review_required`", markdown)
        self.assertIn("Hash changed \\| review", markdown)
        self.assertIn("a\\|b", markdown)
        self.assertIn("no private data", markdown)

    def test_cli_writes_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            compare_path = Path(tmp) / "compare.json"
            out = Path(tmp) / "blockers.json"
            compare_path.write_text(
                json.dumps(
                    {
                        "summary": {
                            "added_count": 0,
                            "removed_count": 0,
                            "changed_count": 0,
                            "unchanged_count": 1,
                            "safety_notice_changed": False,
                        },
                        "added": [],
                        "removed": [],
                        "changed": [],
                        "boundary_comparison": {"added": [], "removed": [], "unchanged": []},
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "earnings_call_risk_map",
                    "release-owner-compare-blockers",
                    "--compare",
                    str(compare_path),
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
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], SCHEMA_LABEL)
            self.assertEqual(payload["summary"]["release_decision"], "clear")

    def test_standalone_cli_reports_missing_compare_without_private_path(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "earnings_call_risk_map.release_owner_compare_blockers",
                "--compare",
                "/tmp/private-compare.json",
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
        self.assertIn("error: compare JSON could not be read: private-compare.json", result.stderr)
        self.assertNotIn("/tmp/private-compare.json", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
