import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from earnings_call_risk_map.evidence_handoff_audit import (
    SCHEMA_LABEL,
    build_evidence_handoff_audit,
    render_evidence_handoff_audit_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}


class EvidenceHandoffAuditTests(unittest.TestCase):
    def test_report_uses_relative_metadata_without_embedding_contents_or_root(self):
        report = build_evidence_handoff_audit(ROOT)

        self.assertEqual(report["schema"], SCHEMA_LABEL)
        self.assertEqual(report["root"], "<redacted-root>")
        self.assertGreater(report["summary"]["checked_artifact_count"], 10)
        self.assertGreater(report["summary"]["present_artifact_count"], 10)
        self.assertIn("no live data", report["boundaries"])
        self.assertIn("no broker connection", report["boundaries"])
        self.assertIn("no personalized investment advice", report["boundaries"])
        self.assertIn("no legal advice", report["boundaries"])
        self.assertIn("no accounting advice", report["boundaries"])
        self.assertIn("no tax advice", report["boundaries"])
        self.assertIn("no buy advice", report["boundaries"])
        self.assertIn("no sell advice", report["boundaries"])
        self.assertIn("no hold advice", report["boundaries"])
        self.assertIn("no private data", report["boundaries"])

        root_text = str(ROOT)
        encoded = json.dumps(report, sort_keys=True)
        self.assertNotIn(root_text, encoded)
        self.assertNotIn("Turn earnings-call notes into deterministic risk maps", encoded)

        readme = next(entry for entry in report["checked_artifacts"] if entry["relative_path"] == "README.md")
        self.assertEqual(readme["role"], "documentation")
        self.assertTrue(readme["present"])
        self.assertIsInstance(readme["bytes"], int)
        self.assertRegex(readme["sha256"], r"^[0-9a-f]{64}$")

    def test_report_excludes_self_outputs_and_self_referential_manifest(self):
        report = build_evidence_handoff_audit(ROOT)
        paths = {entry["relative_path"] for entry in report["checked_artifacts"]}

        self.assertNotIn("examples/output/evidence_handoff_audit.json", paths)
        self.assertNotIn("examples/output/evidence_handoff_audit.md", paths)
        self.assertNotIn("examples/output/release_manifest.json", paths)
        self.assertIn("examples/output/visual_evidence_receipt.md", paths)

    def test_markdown_escapes_table_cells(self):
        markdown = render_evidence_handoff_audit_markdown(
            {
                "schema": SCHEMA_LABEL,
                "package": "earnings-call-risk-map",
                "version": "test",
                "root": "<redacted-root>",
                "summary": {
                    "checked_artifact_count": 1,
                    "present_artifact_count": 1,
                    "missing_artifact_count": 0,
                    "source_fixture_count": 0,
                    "generated_output_count": 1,
                    "readiness_status": "ready_with_review",
                },
                "checked_artifacts": [
                    {
                        "relative_path": "examples/output/a|b.md",
                        "role": "generated|markdown",
                        "present": True,
                        "bytes": 12,
                        "sha256": "abc|def",
                    }
                ],
                "source_notes": ["local only"],
                "freshness_notes": ["static only"],
                "review_readiness_notes": ["review required"],
                "missing_evidence_items": [],
                "recommended_evidence_items": ["keep queue"],
                "regeneration_commands": ["python -m earnings_call_risk_map demo --out-dir examples/output"],
                "boundaries": ["no live data"],
            }
        )

        self.assertIn("examples/output/a\\|b.md", markdown)
        self.assertIn("generated\\|markdown", markdown)
        self.assertIn("abc\\|def", markdown)

    def test_cli_writes_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "audit.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "earnings_call_risk_map",
                    "evidence-handoff-audit",
                    "--root",
                    str(ROOT),
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
            self.assertEqual(payload["root"], "<redacted-root>")


if __name__ == "__main__":
    unittest.main()
