import re
import unittest

from earnings_call_risk_map.io import ALLOWED_SOURCE_TYPES, validate_input


class InputValidationTests(unittest.TestCase):
    def valid_fixture(self):
        return {
            "company": "Example Systems Inc.",
            "ticker": "EXM",
            "as_of": "2026-05-15",
            "data_cutoff": "2026-04-30",
            "notes": [{"id": "n1", "date": "2026-04-30", "text": "growth with pressure"}],
            "kpis": [{"name": "Net retention", "date": "2026-04-30"}],
            "catalysts": [{"title": "Investor day", "date": "2026-06-10"}],
        }

    def test_valid_fixture_passes(self):
        validate_input(self.valid_fixture())

    def test_valid_nested_source_attribution_passes(self):
        fixture = self.valid_fixture()
        fixture["source_attribution"] = {
            "source_name": "Example release",
            "accessed_at": "2026-05-15",
        }
        fixture["notes"][0]["source_attribution"] = [
            {
                "source_name": "Example call transcript",
                "accessed_at": "2026-05-15",
            }
        ]

        validate_input(fixture)

    def test_missing_company_ticker_and_as_of_are_readable(self):
        fixture = self.valid_fixture()
        del fixture["company"]
        del fixture["ticker"]
        del fixture["as_of"]

        with self.assertRaisesRegex(ValueError, "missing required field\\(s\\): company, ticker, as_of"):
            validate_input(fixture, "fixture")

    def test_blank_required_values_are_missing(self):
        fixture = self.valid_fixture()
        fixture["company"] = ""

        with self.assertRaisesRegex(ValueError, "fixture is missing required field\\(s\\): company"):
            validate_input(fixture, "fixture")

    def test_company_and_ticker_must_be_strings(self):
        fixture = self.valid_fixture()
        fixture["ticker"] = 123

        with self.assertRaisesRegex(ValueError, "fixture.ticker must be a non-empty string"):
            validate_input(fixture, "fixture")

    def test_bad_top_level_date_shape_is_readable(self):
        fixture = self.valid_fixture()
        fixture["as_of"] = "2026/05/15"

        with self.assertRaisesRegex(ValueError, r"fixture\.as_of must use YYYY-MM-DD format"):
            validate_input(fixture, "fixture")

    def test_bad_nested_date_shape_is_readable(self):
        fixture = self.valid_fixture()
        fixture["notes"][0]["date"] = "04-30-2026"

        with self.assertRaisesRegex(ValueError, r"fixture\.notes\[0\]\.date must use YYYY-MM-DD format"):
            validate_input(fixture, "fixture")

    def test_bad_catalyst_date_values_include_field_path(self):
        cases = (
            ("", r"fixture\.catalysts\[0\]\.date must use YYYY-MM-DD format"),
            (None, r"fixture\.catalysts\[0\]\.date must be a string in YYYY-MM-DD format"),
            ("2026-02-30", r"fixture\.catalysts\[0\]\.date must be a valid calendar date"),
        )
        for value, message in cases:
            with self.subTest(value=value):
                fixture = self.valid_fixture()
                fixture["catalysts"][0]["date"] = value

                with self.assertRaisesRegex(ValueError, message):
                    validate_input(fixture, "fixture")

    def test_evidence_url_must_be_string_when_provided(self):
        cases = (
            ("notes", None, r"fixture\.notes\[0\]\.evidence_url must be a string"),
            ("kpis", 123, r"fixture\.kpis\[0\]\.evidence_url must be a string"),
            ("catalysts", [], r"fixture\.catalysts\[0\]\.evidence_url must be a string"),
        )
        for collection, value, message in cases:
            with self.subTest(collection=collection):
                fixture = self.valid_fixture()
                fixture[collection][0]["evidence_url"] = value

                with self.assertRaisesRegex(ValueError, message):
                    validate_input(fixture, "fixture")

    def test_blank_evidence_url_placeholder_is_allowed(self):
        fixture = self.valid_fixture()
        fixture["notes"][0]["evidence_url"] = ""
        fixture["kpis"][0]["evidence_url"] = ""
        fixture["catalysts"][0]["evidence_url"] = ""

        validate_input(fixture, "fixture")

    def test_bad_nested_source_attribution_shape_includes_field_path(self):
        cases = (
            ("notes", r"fixture\.notes\[0\]\.source_attribution must be a JSON object or list"),
            ("kpis", r"fixture\.kpis\[0\]\.source_attribution must be a JSON object or list"),
            ("catalysts", r"fixture\.catalysts\[0\]\.source_attribution must be a JSON object or list"),
        )
        for collection, message in cases:
            with self.subTest(collection=collection):
                fixture = self.valid_fixture()
                fixture[collection][0]["source_attribution"] = "Example release"

                with self.assertRaisesRegex(ValueError, message):
                    validate_input(fixture, "fixture")

    def test_bad_top_level_source_attribution_shape_includes_field_path(self):
        fixture = self.valid_fixture()
        fixture["source_attribution"] = "Example release"

        with self.assertRaisesRegex(
            ValueError,
            r"fixture\.source_attribution must be a JSON object or list of JSON objects when provided",
        ):
            validate_input(fixture, "fixture")

    def test_bad_nested_source_attribution_item_includes_field_path(self):
        fixture = self.valid_fixture()
        fixture["notes"][0]["source_attribution"] = [{"source_name": "Example release"}, "bad source"]

        with self.assertRaisesRegex(
            ValueError,
            r"fixture\.notes\[0\]\.source_attribution\[1\] must be a JSON object",
        ):
            validate_input(fixture, "fixture")

    def test_empty_source_attribution_record_includes_field_path(self):
        fixture = self.valid_fixture()
        fixture["source_attribution"] = [{}]

        with self.assertRaisesRegex(
            ValueError,
            r"fixture\.source_attribution\[0\] must include at least one supported source-attribution field",
        ):
            validate_input(fixture, "fixture")

    def test_source_attribution_text_fields_must_be_non_empty_strings(self):
        cases = (
            ("source_name", "", r"fixture\.source_attribution\.source_name must be a non-empty string"),
            ("publisher", 123, r"fixture\.source_attribution\.publisher must be a non-empty string"),
            ("source_type", None, r"fixture\.source_attribution\.source_type must be a non-empty string"),
            ("source_url", [], r"fixture\.source_attribution\.source_url must be a non-empty string"),
            ("static_notice", {}, r"fixture\.source_attribution\.static_notice must be a non-empty string"),
        )
        for field, value, message in cases:
            with self.subTest(field=field):
                fixture = self.valid_fixture()
                fixture["source_attribution"] = {field: value}

                with self.assertRaisesRegex(ValueError, message):
                    validate_input(fixture, "fixture")

    def test_source_attribution_metadata_fields_must_be_strings_with_field_paths(self):
        cases = (
            (
                "source_attribution",
                "source_name",
                123,
                r"fixture\.source_attribution\[0\]\.source_name must be a non-empty string",
            ),
            (
                "notes",
                "publisher",
                ["Example Systems"],
                r"fixture\.notes\[0\]\.source_attribution\[0\]\.publisher must be a non-empty string",
            ),
            (
                "kpis",
                "source_type",
                {"type": "transcript"},
                r"fixture\.kpis\[0\]\.source_attribution\[0\]\.source_type must be a non-empty string",
            ),
            (
                "catalysts",
                "static_notice",
                False,
                r"fixture\.catalysts\[0\]\.source_attribution\[0\]\.static_notice must be a non-empty string",
            ),
        )
        for location, field, value, message in cases:
            with self.subTest(location=location, field=field):
                fixture = self.valid_fixture()
                source_attribution = [{field: value}]
                if location == "source_attribution":
                    fixture["source_attribution"] = source_attribution
                else:
                    fixture[location][0]["source_attribution"] = source_attribution

                with self.assertRaisesRegex(ValueError, message):
                    validate_input(fixture, "fixture")

    def test_empty_top_level_source_name_includes_field_path(self):
        fixture = self.valid_fixture()
        fixture["source_attribution"] = [{"source_name": "   "}]

        with self.assertRaisesRegex(
            ValueError,
            r"fixture\.source_attribution\[0\]\.source_name must be a non-empty string",
        ):
            validate_input(fixture, "fixture")

    def test_empty_nested_source_name_includes_field_path(self):
        cases = (
            ("notes", r"fixture\.notes\[0\]\.source_attribution\[0\]\.source_name must be a non-empty string"),
            ("kpis", r"fixture\.kpis\[0\]\.source_attribution\[0\]\.source_name must be a non-empty string"),
            ("catalysts", r"fixture\.catalysts\[0\]\.source_attribution\[0\]\.source_name must be a non-empty string"),
        )
        for collection, message in cases:
            with self.subTest(collection=collection):
                fixture = self.valid_fixture()
                fixture[collection][0]["source_attribution"] = [{"source_name": ""}]

                with self.assertRaisesRegex(ValueError, message):
                    validate_input(fixture, "fixture")

    def test_invalid_top_level_source_type_lists_allowed_values(self):
        fixture = self.valid_fixture()
        fixture["source_attribution"] = {"source_type": "blog_post"}
        allowed = ", ".join(ALLOWED_SOURCE_TYPES)

        with self.assertRaisesRegex(
            ValueError,
            re.escape(f"fixture.source_attribution.source_type must be one of: {allowed}; got 'blog_post'"),
        ):
            validate_input(fixture, "fixture")

    def test_invalid_note_source_type_lists_allowed_values(self):
        fixture = self.valid_fixture()
        fixture["notes"][0]["source_attribution"] = {"source_type": "blog_post"}
        allowed = ", ".join(ALLOWED_SOURCE_TYPES)

        with self.assertRaisesRegex(
            ValueError,
            re.escape(f"fixture.notes[0].source_attribution.source_type must be one of: {allowed}; got 'blog_post'"),
        ):
            validate_input(fixture, "fixture")

    def test_invalid_kpi_source_type_lists_allowed_values(self):
        fixture = self.valid_fixture()
        fixture["kpis"][0]["source_attribution"] = {"source_type": "blog_post"}
        allowed = ", ".join(ALLOWED_SOURCE_TYPES)

        with self.assertRaisesRegex(
            ValueError,
            re.escape(f"fixture.kpis[0].source_attribution.source_type must be one of: {allowed}; got 'blog_post'"),
        ):
            validate_input(fixture, "fixture")

    def test_invalid_catalyst_source_type_lists_allowed_values(self):
        fixture = self.valid_fixture()
        fixture["catalysts"][0]["source_attribution"] = {"source_type": "blog_post"}
        allowed = ", ".join(ALLOWED_SOURCE_TYPES)

        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                f"fixture.catalysts[0].source_attribution.source_type must be one of: {allowed}; got 'blog_post'"
            ),
        ):
            validate_input(fixture, "fixture")

    def test_bad_nested_source_attribution_accessed_at_includes_field_path(self):
        cases = (
            ("notes", r"fixture\.notes\[0\]\.source_attribution\[0\]\.accessed_at must use YYYY-MM-DD format"),
            ("kpis", r"fixture\.kpis\[0\]\.source_attribution\[0\]\.accessed_at must use YYYY-MM-DD format"),
            ("catalysts", r"fixture\.catalysts\[0\]\.source_attribution\[0\]\.accessed_at must use YYYY-MM-DD format"),
        )
        for collection, message in cases:
            with self.subTest(collection=collection):
                fixture = self.valid_fixture()
                fixture[collection][0]["source_attribution"] = [
                    {"source_name": "Example release", "accessed_at": "05-15-2026"}
                ]

                with self.assertRaisesRegex(ValueError, message):
                    validate_input(fixture, "fixture")

    def test_empty_source_attribution_accessed_at_includes_field_path(self):
        fixture = self.valid_fixture()
        fixture["catalysts"][0]["source_attribution"] = {"source_name": "Example release", "accessed_at": ""}

        with self.assertRaisesRegex(
            ValueError,
            r"fixture\.catalysts\[0\]\.source_attribution\.accessed_at must use YYYY-MM-DD format",
        ):
            validate_input(fixture, "fixture")

    def test_bad_top_level_source_attribution_includes_field_path(self):
        fixture = self.valid_fixture()
        fixture["source_attribution"] = [
            {"source_name": "Example release", "accessed_at": "2026-02-30"}
        ]

        with self.assertRaisesRegex(
            ValueError,
            r"fixture\.source_attribution\[0\]\.accessed_at must be a valid calendar date",
        ):
            validate_input(fixture, "fixture")

    def test_invalid_calendar_date_is_readable(self):
        fixture = self.valid_fixture()
        fixture["data_cutoff"] = "2026-02-30"

        with self.assertRaisesRegex(ValueError, "fixture.data_cutoff must be a valid calendar date"):
            validate_input(fixture, "fixture")


if __name__ == "__main__":
    unittest.main()
