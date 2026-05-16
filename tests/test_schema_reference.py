import json
import unittest
from pathlib import Path

from earnings_call_risk_map.io import validate_input
from earnings_call_risk_map.models import REQUIRED_TOP_LEVEL

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "schema-reference.json"
INPUT_FIXTURES = sorted((ROOT / "examples" / "input").glob("*.json"))


class SchemaReferenceTests(unittest.TestCase):
    def load_schema(self):
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_schema_reference_json_is_valid_and_example_is_accepted(self):
        schema = self.load_schema()
        self.assertEqual(schema["type"], "object")
        self.assertEqual(schema["required"], list(REQUIRED_TOP_LEVEL))

        example = schema["examples"][0]
        validate_input(example, "docs/schema-reference.json.examples[0]")

    def test_schema_reference_covers_checked_in_fixture_fields(self):
        schema = self.load_schema()
        top_level_fields = set(schema["properties"])
        note_fields = set(schema["$defs"]["note"]["properties"])
        kpi_fields = set(schema["$defs"]["kpi"]["properties"])
        catalyst_fields = set(schema["$defs"]["catalyst"]["properties"])
        source_fields = set(schema["$defs"]["source_record"]["properties"])

        self.assertTrue(INPUT_FIXTURES)
        for fixture_path in INPUT_FIXTURES:
            with self.subTest(fixture=fixture_path.name):
                fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
                validate_input(fixture, fixture_path.name)

                self.assertLessEqual(set(fixture), top_level_fields)
                for note in fixture.get("notes", []):
                    self.assertLessEqual(set(note), note_fields)
                    self.assert_source_attribution_fields_are_documented(note, source_fields)
                for kpi in fixture.get("kpis", []):
                    self.assertLessEqual(set(kpi), kpi_fields)
                    self.assert_source_attribution_fields_are_documented(kpi, source_fields)
                for catalyst in fixture.get("catalysts", []):
                    self.assertLessEqual(set(catalyst), catalyst_fields)
                    self.assert_source_attribution_fields_are_documented(catalyst, source_fields)
                self.assert_source_attribution_fields_are_documented(fixture, source_fields)

    def assert_source_attribution_fields_are_documented(self, item, source_fields):
        attribution = item.get("source_attribution") or []
        if isinstance(attribution, dict):
            attribution = [attribution]
        for source in attribution:
            self.assertLessEqual(set(source), source_fields)


if __name__ == "__main__":
    unittest.main()
