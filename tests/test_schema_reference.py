import json
import unittest
from pathlib import Path

from earnings_call_risk_map.io import ALLOWED_SOURCE_TYPES, validate_input
from earnings_call_risk_map.models import REQUIRED_TOP_LEVEL
from earnings_call_risk_map.schema_authoring_reference import (
    build_schema_authoring_reference,
    schema_authoring_reference_markdown,
)
from earnings_call_risk_map.schema_reference import build_schema_reference

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "schema-reference.json"
INPUT_FIXTURES = sorted((ROOT / "examples" / "input").glob("*.json"))
TEMPLATE_FIXTURES = sorted((ROOT / "examples" / "templates").glob("*.json"))


class SchemaReferenceTests(unittest.TestCase):
    def load_schema(self):
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_schema_reference_json_is_valid_and_example_is_accepted(self):
        schema = self.load_schema()
        self.assertEqual(schema["type"], "object")
        self.assertEqual(schema["required"], list(REQUIRED_TOP_LEVEL))

        example = schema["examples"][0]
        validate_input(example, "docs/schema-reference.json.examples[0]")

    def test_schema_reference_matches_generated_reference(self):
        self.assertEqual(self.load_schema(), build_schema_reference())

    def test_source_type_enum_and_source_field_descriptions_are_documented(self):
        source_record = self.load_schema()["$defs"]["source_record"]
        source_properties = source_record["properties"]

        self.assertEqual(source_properties["source_type"]["enum"], list(ALLOWED_SOURCE_TYPES))
        for field in ("source_name", "publisher", "source_type", "source_url", "accessed_at", "static_notice"):
            with self.subTest(field=field):
                description = source_properties[field]["description"]
                self.assertIsInstance(description, str)
                self.assertGreater(len(description), 40)

    def test_schema_reference_covers_checked_in_fixture_fields(self):
        schema = self.load_schema()
        top_level_fields = set(schema["properties"])
        note_fields = set(schema["$defs"]["note"]["properties"])
        kpi_fields = set(schema["$defs"]["kpi"]["properties"])
        catalyst_fields = set(schema["$defs"]["catalyst"]["properties"])
        source_fields = set(schema["$defs"]["source_record"]["properties"])

        self.assertTrue(INPUT_FIXTURES)
        self.assertTrue(TEMPLATE_FIXTURES)
        for fixture_path in INPUT_FIXTURES + TEMPLATE_FIXTURES:
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

    def test_blank_templates_cover_expected_review_types(self):
        expected = {
            "software_earnings_review.json": ("Software Earnings Review Template", "Revenue growth"),
            "energy_infrastructure_earnings_review.json": (
                "Energy Infrastructure Earnings Review Template",
                "Construction work in progress",
            ),
            "consumer_hardware_earnings_review.json": (
                "Consumer Hardware Earnings Review Template",
                "Units shipped",
            ),
        }
        self.assertEqual({path.name for path in TEMPLATE_FIXTURES}, set(expected))
        for template_path in TEMPLATE_FIXTURES:
            with self.subTest(template=template_path.name):
                template = json.loads(template_path.read_text(encoding="utf-8"))
                company, kpi_name = expected[template_path.name]
                validate_input(template, template_path.name)
                self.assertEqual(template["company"], company)
                self.assertIn(kpi_name, {kpi["name"] for kpi in template["kpis"]})
                self.assertTrue(template["notes"])
                self.assertTrue(template["catalysts"])

    def test_schema_authoring_reference_covers_generated_schema_fields(self):
        authoring_reference = build_schema_authoring_reference()
        markdown = schema_authoring_reference_markdown()
        schema = self.load_schema()

        self.assertEqual(authoring_reference["artifact_type"], "schema_authoring_reference")
        self.assertEqual(authoring_reference["schema_reference"], "docs/schema-reference.json")
        self.assertIn("Do not invent source names", authoring_reference["no_hallucination_rule"])
        self.assertIn("# Schema Authoring Reference", markdown)
        self.assertIn("Plain-English Meaning", markdown)
        self.assertIn("Authoring Guidance", markdown)

        documented_fields = {
            field["field"]
            for section in authoring_reference["sections"]
            for field in section["fields"]
        }
        schema_fields = set(schema["properties"])
        schema_fields.update(schema["$defs"]["note"]["properties"])
        schema_fields.update(schema["$defs"]["kpi"]["properties"])
        schema_fields.update(schema["$defs"]["catalyst"]["properties"])
        schema_fields.update(schema["$defs"]["source_record"]["properties"])
        self.assertLessEqual(schema_fields, documented_fields)

    def assert_source_attribution_fields_are_documented(self, item, source_fields):
        attribution = item.get("source_attribution") or []
        if isinstance(attribution, dict):
            attribution = [attribution]
        for source in attribution:
            self.assertLessEqual(set(source), source_fields)


if __name__ == "__main__":
    unittest.main()
