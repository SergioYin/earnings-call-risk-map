import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocsTests(unittest.TestCase):
    def test_tutorial_exists_and_covers_review_flow(self):
        path = ROOT / "docs" / "tutorial-earnings-review.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "fixture",
            "report",
            "review queue",
            "compare",
            "Educational research review only",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_readme_links_to_tutorial(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/tutorial-earnings-review.md", readme)

    def test_docs_cover_local_only_no_network_guarantee(self):
        for relative_path in ("README.md", "docs/usage.md"):
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("Local-Only No-Network Guarantee", text)
                self.assertIn("network", text.lower())
                self.assertIn("credential", text.lower())
                self.assertIn("audit", text)

    def test_fixture_catalog_document_covers_bundled_fixtures(self):
        path = ROOT / "docs" / "fixture-catalog.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "examples/input/demo_company.json",
            "examples/input/demo_energy_infrastructure.json",
            "examples/input/public_apple_static_case_study.json",
            "examples/input/demo_company_prior.json",
            "Static/live status",
            "fixture-catalog",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_scoring_document_covers_severity_calibration_edges(self):
        path = ROOT / "docs" / "scoring.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Severity calibration",
            "`score >= 7`",
            "`4 <= score <= 6`",
            "`1 <= score <= 3`",
            "`score = 0`",
            "`7` is the first `high` score",
            "Stale note data adds `+1`",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
