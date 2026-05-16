import unittest

from earnings_call_risk_map.io import validate_input


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

    def test_bad_nested_source_attribution_item_includes_field_path(self):
        fixture = self.valid_fixture()
        fixture["notes"][0]["source_attribution"] = [{"source_name": "Example release"}, "bad source"]

        with self.assertRaisesRegex(
            ValueError,
            r"fixture\.notes\[0\]\.source_attribution\[1\] must be a JSON object",
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
