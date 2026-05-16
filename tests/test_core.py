import json
import unittest
from pathlib import Path

from earnings_call_risk_map.core import (
    analyze_document,
    build_review_queue_export,
    build_review_queue_jsonl_records,
    compare_snapshots,
    render_jsonl,
)
from earnings_call_risk_map.models import SAFETY_NOTICE, SOURCE_BOUNDARIES
from earnings_call_risk_map.render import render_compare_markdown, render_markdown, render_review_queue_markdown

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
        self.assertEqual(snapshot["tool_version"], "0.6.0")
        self.assertEqual(snapshot["summary"]["risk_count"], 1)
        self.assertEqual(snapshot["summary"]["opportunity_count"], 2)
        self.assertEqual(snapshot["review_queue"][0]["topic"], "gross margin")
        self.assertEqual(snapshot["stale_badges"][0]["badge"]["status"], "stale")
        self.assertEqual(snapshot["catalyst_timeline"][0]["title"], "Earlier")
        self.assertIn("does not provide personalized", snapshot["safety_notice"])

    def test_source_attribution_is_preserved(self):
        fixture = self.fixture()
        fixture["source_attribution"] = {
            "source_name": "Example release",
            "publisher": "Example Systems",
            "source_type": "company_investor_relations",
            "source_url": "https://example.com/source",
            "accessed_at": "2026-05-15",
            "static_notice": "Static fixture; not live data."
        }
        fixture["notes"][0]["source_attribution"] = fixture["source_attribution"]

        snapshot = analyze_document(fixture)
        export = build_review_queue_export(snapshot)

        self.assertEqual(snapshot["source_attribution"][0]["source_name"], "Example release")
        gross_margin = next(item for item in export["items"] if item["topic"] == "gross margin")
        self.assertEqual(gross_margin["source_attribution"][0]["source_type"], "company_investor_relations")

    def test_outputs_preserve_disclaimer_and_source_boundaries(self):
        snapshot = analyze_document(self.fixture())
        queue = build_review_queue_export(snapshot)
        compare = compare_snapshots(snapshot, snapshot)

        for payload in (snapshot, queue, compare):
            self.assertEqual(payload["safety_notice"], SAFETY_NOTICE)
            self.assertEqual(payload["source_boundaries"], SOURCE_BOUNDARIES)

        for markdown in (
            render_markdown(snapshot),
            render_review_queue_markdown(queue),
            render_compare_markdown(compare),
        ):
            self.assertIn(SAFETY_NOTICE, markdown)
            self.assertIn("## Source Boundaries", markdown)
            self.assertIn("Management claims", markdown)
            self.assertIn("Analyst questions", markdown)
            self.assertIn("User synthesis", markdown)
            self.assertIn("not advice", markdown)

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
        self.assertTrue(result["interpretation"])
        self.assertIn("deterministic keyword scores", result["interpretation"][0])

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

    def test_review_queue_jsonl_records_are_deterministic_agent_handoff(self):
        snapshot = analyze_document(self.fixture())
        export = build_review_queue_export(snapshot)
        records = build_review_queue_jsonl_records("unit_fixture", "examples/input/unit_fixture.json", export)
        self.assertEqual(len(records), export["summary"]["review_item_count"])
        self.assertEqual(records[0]["record_type"], "review_queue_item")
        self.assertEqual(records[0]["fixture_slug"], "unit_fixture")
        self.assertEqual(records[0]["fixture_path"], "examples/input/unit_fixture.json")
        self.assertEqual(records[0]["item_index"], 1)
        self.assertEqual(records[0]["ticker"], "EXM")
        self.assertIn("source_boundaries", records[0])
        self.assertIn("review_item", records[0])

        text = render_jsonl(records)
        lines = text.splitlines()
        self.assertEqual(len(lines), len(records))
        parsed = [json.loads(line) for line in lines]
        self.assertEqual(parsed, records)
        self.assertEqual(text, render_jsonl(records))

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
