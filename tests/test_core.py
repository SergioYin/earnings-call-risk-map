import json
import unittest
from pathlib import Path

from earnings_call_risk_map.core import analyze_document, build_review_queue_export, compare_snapshots

ROOT = Path(__file__).resolve().parents[1]


class CoreTests(unittest.TestCase):
    def fixture(self):
        return {
            "company": "Example Systems Inc.",
            "ticker": "EXM",
            "as_of": "2026-05-15",
            "data_cutoff": "2026-04-30",
            "notes": [
                {
                    "id": "n1",
                    "date": "2025-11-01",
                    "topic": "gross margin",
                    "text": "Margin compression and supply delay risk remain under review.",
                    "evidence_url": "https://example.com/source",
                },
                {
                    "id": "n2",
                    "topic": "launch",
                    "text": "The launch may expand pipeline growth.",
                },
                {
                    "id": "n3",
                    "date": "2026-04-30",
                    "topic": "regional demand",
                    "text": "Regional demand remained stable.",
                    "evidence_url": "https://example.com/regional-demand",
                },
            ],
            "kpis": [
                {
                    "name": "Net retention",
                    "direction": "up",
                    "date": "2026-04-30",
                    "observation": "Growth improved.",
                }
            ],
            "catalysts": [
                {"date": "2026-08-01", "title": "Later"},
                {"date": "2026-06-01", "title": "Earlier"},
            ],
        }

    def test_analyze_scores_and_review_queue(self):
        snapshot = analyze_document(self.fixture())
        self.assertEqual(snapshot["tool_version"], "0.1.0")
        self.assertEqual(snapshot["summary"]["risk_count"], 1)
        self.assertEqual(snapshot["summary"]["opportunity_count"], 2)
        self.assertEqual(snapshot["review_queue"][0]["topic"], "gross margin")
        self.assertEqual(snapshot["stale_badges"][0]["badge"]["status"], "stale")
        self.assertEqual(snapshot["catalyst_timeline"][0]["title"], "Earlier")
        self.assertIn("does not provide personalized", snapshot["safety_notice"])

    def test_compare_snapshots_reports_deltas(self):
        before = analyze_document(self.fixture())
        after_fixture = self.fixture()
        after_fixture["as_of"] = "2026-09-15"
        after_fixture["notes"].append(
            {
                "id": "n3",
                "date": "2026-06-01",
                "topic": "regulatory",
                "text": "Regulatory investigation risk was newly disclosed.",
                "evidence_url": "https://example.com/regulatory",
            }
        )
        after = analyze_document(after_fixture)
        result = compare_snapshots(before, after)
        topics = {item["topic"] for item in result["risk_changes"]}
        self.assertIn("regulatory", topics)
        self.assertGreaterEqual(result["stale_badge_delta"], 1)

    def test_review_queue_export_is_focused(self):
        snapshot = analyze_document(self.fixture())
        export = build_review_queue_export(snapshot)
        topics = {item["topic"] for item in export["items"]}
        self.assertIn("gross margin", topics)
        self.assertIn("launch", topics)
        self.assertIn("Net retention", topics)
        self.assertNotIn("regional demand", topics)
        gross_margin = next(item for item in export["items"] if item["topic"] == "gross margin")
        self.assertEqual(gross_margin["issue_categories"], ["stale_data", "high_impact_language"])
        launch = next(item for item in export["items"] if item["topic"] == "launch")
        self.assertEqual(launch["issue_categories"], ["missing_evidence", "high_impact_language"])

    def test_energy_infrastructure_fixture_exercises_review_paths(self):
        fixture = json.loads((ROOT / "examples/input/demo_energy_infrastructure.json").read_text(encoding="utf-8"))
        snapshot = analyze_document(fixture)
        self.assertEqual(snapshot["company"], "Northstar Grid & LNG Partners")
        self.assertEqual(snapshot["summary"]["stale_badge_count"], 4)
        self.assertEqual(snapshot["catalyst_timeline"][0]["title"], "Federal permit milestone")
        self.assertIn("Rate-case filing", {item["title"] for item in snapshot["catalyst_timeline"]})

        export = build_review_queue_export(snapshot)
        self.assertEqual(export["summary"]["review_item_count"], 8)
        self.assertEqual(export["summary"]["stale_data_count"], 4)
        self.assertEqual(export["summary"]["missing_evidence_count"], 4)
        self.assertEqual(export["summary"]["high_impact_language_count"], 5)
        topics = {item["topic"] for item in export["items"]}
        self.assertIn("Project cost variance", topics)
        self.assertIn("Contracted capacity backlog", topics)
        self.assertIn("Rate-case filing", topics)


if __name__ == "__main__":
    unittest.main()
