import unittest
import re
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
LOCAL_DOC_ROOTS = (
    ROOT / "README.md",
    ROOT / "docs",
    ROOT / "examples" / "playbooks",
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def markdown_files():
    for root in LOCAL_DOC_ROOTS:
        if root.is_file():
            yield root
        else:
            yield from sorted(root.rglob("*.md"))


def github_anchor_slug(heading):
    slug = heading.strip().lower()
    slug = re.sub(r"`([^`]*)`", r"\1", slug)
    slug = re.sub(r"<[^>]+>", "", slug)
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def markdown_anchors(path):
    anchors = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            anchors.add(github_anchor_slug(match.group(2)))
    return anchors


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

    def test_playbooks_exist_and_cover_deterministic_workflows(self):
        playbook_dir = ROOT / "examples" / "playbooks"
        expected = {
            "README.md": ("Quarterly Review", "Catalyst Check-In", "Post-Earnings Thesis Refresh"),
            "quarterly-review.md": ("Deterministic Steps", "review-queue", "compare", "Expected Artifacts"),
            "catalyst-check-in.md": ("Deterministic Steps", "catalyst", "review-queue-jsonl", "Expected Artifacts"),
            "post-earnings-thesis-refresh.md": ("Deterministic Steps", "Source Boundaries", "integration_notes.json", "Expected Artifacts"),
        }
        for filename, markers in expected.items():
            with self.subTest(playbook=filename):
                path = playbook_dir / filename
                self.assertTrue(path.is_file())
                text = path.read_text(encoding="utf-8")
                self.assertIn("Educational research review only", text)
                for marker in markers:
                    self.assertIn(marker, text)

    def test_readme_links_to_playbooks(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for marker in (
            "examples/playbooks/README.md",
            "examples/playbooks/quarterly-review.md",
            "examples/playbooks/catalyst-check-in.md",
            "examples/playbooks/post-earnings-thesis-refresh.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, readme)

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

    def test_case_study_limitations_cover_static_sources_and_safeguards(self):
        path = ROOT / "docs" / "case-study-limitations.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Static Source Limitations",
            "Source Freshness",
            "Replacing Fixtures With User-Collected Notes",
            "Non-Advice Safeguards",
            "`as_of`",
            "`data_cutoff`",
            "`accessed_at`",
            "educational research review only",
            "not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice",
            "Do not translate scores into price targets",
            "management_claim",
            "analyst_question",
            "user_synthesis",
            "source_attribution",
            "Non-Advice Boundary",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_link_to_case_study_limitations(self):
        expected_links = {
            "README.md": "docs/case-study-limitations.md",
            "docs/public-case-study.md": "case-study-limitations.md",
            "docs/non-advice-boundary.md": "case-study-limitations.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_local_docs_links_resolve(self):
        for path in markdown_files():
            text = path.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK_RE.findall(text):
                parsed = urlparse(unquote(raw_target))
                if parsed.scheme or parsed.netloc:
                    continue
                if raw_target.startswith("mailto:"):
                    continue
                target_path = parsed.path
                fragment = parsed.fragment
                with self.subTest(path=str(path.relative_to(ROOT)), target=raw_target):
                    if target_path:
                        resolved = (path.parent / target_path).resolve()
                        self.assertTrue(
                            resolved.exists(),
                            f"{path.relative_to(ROOT)} links to missing {raw_target}",
                        )
                    else:
                        resolved = path
                    if fragment and resolved.suffix == ".md":
                        self.assertIn(
                            fragment,
                            markdown_anchors(resolved),
                            f"{path.relative_to(ROOT)} links to missing anchor {raw_target}",
                        )


if __name__ == "__main__":
    unittest.main()
