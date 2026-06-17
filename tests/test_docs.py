import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from earnings_call_risk_map.io import validate_input
from earnings_call_risk_map.schema_reference import build_schema_reference


ROOT = Path(__file__).resolve().parents[1]
LOCAL_DOC_ROOTS = (
    ROOT / "README.md",
    ROOT / "docs",
    ROOT / "examples" / "playbooks",
)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


class DemoIndexParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.local_targets = []
        self.external_targets = []

    def handle_starttag(self, tag, attrs):
        attr_map = dict(attrs)
        if tag == "script":
            self.scripts.append(attr_map)
        for attr_name in ("href", "src", "poster"):
            target = attr_map.get(attr_name)
            if not target:
                continue
            parsed = urlparse(unquote(target))
            if parsed.scheme or parsed.netloc or target.startswith("//"):
                self.external_targets.append(target)
            else:
                self.local_targets.append(target)


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
    def test_data_entry_checklist_covers_no_hallucinated_sources(self):
        path = ROOT / "docs" / "data-entry-checklist.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Data Entry Checklist",
            "Create a valid JSON fixture without hallucinating sources",
            "Do not invent `source_url`, `publisher`, `source_name`, `accessed_at`, speaker names, KPI values, dates, or fiscal periods",
            "Do not promote an analyst question into a company fact",
            "Do not promote user summaries into source evidence",
            "Do not fill missing `evidence_url` just to clear the review queue",
            "Use `accessed_at` only when the source URL was actually checked",
            "management_claim",
            "analyst_question",
            "user_synthesis",
            "PYTHONPATH=src python -m earnings_call_risk_map analyze path/to/fixture.json",
            "JSON Fixture Schema Reference",
            "Source Attribution Guide",
            "Educational research review only",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_data_entry_checklist_embedded_fixture_is_valid(self):
        path = ROOT / "docs" / "data-entry-checklist.md"
        text = path.read_text(encoding="utf-8")
        match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
        self.assertIsNotNone(match)
        fixture = json.loads(match.group(1))
        validate_input(fixture, "docs/data-entry-checklist.md example")

    def test_first_run_docs_link_to_data_entry_checklist(self):
        expected_links = {
            "README.md": "docs/data-entry-checklist.md",
            "docs/usage.md": "data-entry-checklist.md",
            "docs/filled-template-workflow.md": "data-entry-checklist.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

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

    def test_first_30_minutes_tutorial_covers_cold_user_flow(self):
        path = ROOT / "docs" / "tutorial-first-30-minutes.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "git clone <repo-url>",
            "template-catalog",
            "examples/templates/software_earnings_review.json",
            "examples/input/first_30_minutes_workflow.json",
            "review-queue",
            "handoff-packet",
            "portfolio-risk or thesis-ledger",
            "Educational research review only",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_readme_and_tutorial_link_first_30_minutes(self):
        expected_links = {
            "README.md": "docs/tutorial-first-30-minutes.md",
            "docs/tutorial-earnings-review.md": "tutorial-first-30-minutes.md",
            "docs/tutorial-first-30-minutes.md": "tutorial-earnings-review.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_comparison_to_spreadsheets_document_covers_tradeoffs(self):
        path = ROOT / "docs" / "comparison-to-spreadsheets.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Where This Tool Is Better",
            "Where Spreadsheets Are Better",
            "Where Generic Notes Are Better",
            "Where This Tool Is Worse",
            "Decision Table",
            "financial models",
            "live collaborative editor",
            "Open-ended research",
            "Local, Inspectable, No-Network Runs",
            "Educational research review only",
            "does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice",
            "Non-Advice Boundary",
            "Case Study Limitations",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_comparison_to_generic_llm_notes_document_covers_tradeoffs(self):
        path = ROOT / "docs" / "comparison-to-generic-llm-notes.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Comparison To Generic LLM Notes",
            "deterministic local CLI",
            "one-off notes produced by prompting a general-purpose LLM",
            "Where This CLI Is Better",
            "Where One-Off LLM Notes Are Better",
            "Limitations Of This CLI",
            "Limitations Of One-Off LLM Notes",
            "When To Use Each",
            "Practical Workflow Split",
            "Repeatable Deterministic Runs",
            "Source-Boundary Discipline",
            "Local, Inspectable, No-Network Runs",
            "Raw Transcript And Filing Triage",
            "It does not ingest raw transcripts",
            "They can hallucinate facts, citations, dates, source names, URLs, speakers, or numerical values",
            "Fill missing facts or evidence URLs",
            "Neither",
            "Educational research review only",
            "does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice",
            "Non-Advice Boundary",
            "Case Study Limitations",
            "Source Attribution Guide",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_first_run_docs_link_to_generic_llm_notes_comparison(self):
        expected_links = {
            "README.md": "docs/comparison-to-generic-llm-notes.md",
            "docs/usage.md": "comparison-to-generic-llm-notes.md",
            "docs/comparison-to-spreadsheets.md": "comparison-to-generic-llm-notes.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_promotion_page_outline_covers_public_copy_artifacts_and_boundaries(self):
        path = ROOT / "docs" / "promotion-page-outline.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Promotion Page Outline",
            "public landing-page copy",
            "Hero Copy",
            "Demo Artifacts To Screenshot",
            "Comparison Narrative",
            "Boundaries",
            "examples/output/public_apple_static_case_study_dashboard.html",
            "docs/assets/showcase-dashboard-preview.svg",
            "docs/demo-index.html",
            "examples/output/demo_review_queue.md",
            "examples/output/demo_compare.md",
            "examples/output/public_apple_static_case_study_report.md",
            "examples/output/handoff_packet.md",
            "examples/output/case_study_map.md",
            "Compared with spreadsheets",
            "Compared with generic notes",
            "Compared with LLM summarizers",
            "Compared with hosted research tools",
            "Do not claim live market data",
            "Do not describe deterministic scores as facts",
            "Do not present bundled fixtures as current analysis",
            "Educational research review only",
            "buy, sell, hold",
            "Non-Advice Boundary",
            "Case Study Limitations",
            "Source Attribution Guide",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_link_to_promotion_page_outline(self):
        expected_links = {
            "README.md": "docs/promotion-page-outline.md",
            "docs/usage.md": "promotion-page-outline.md",
            "docs/gallery.md": "promotion-page-outline.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_readme_links_to_promotion_pack(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("examples/output/promotion_pack.md", readme)

    def test_demo_screenshot_guide_covers_visual_artifact_choices(self):
        path = ROOT / "docs" / "demo-screenshot-guide.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Demo Screenshot Guide",
            "Best Screenshot Targets",
            "Good README Visuals",
            "Screenshot Framing",
            "Less Useful Visuals",
            "examples/output/public_apple_static_case_study_dashboard.html",
            "examples/output/demo_dashboard.html",
            "examples/output/energy_infrastructure_dashboard.html",
            "examples/output/consumer_hardware_dashboard.html",
            "examples/output/semiconductor_equipment_dashboard.html",
            "docs/assets/showcase-dashboard-preview.svg",
            "examples/output/showcase_dashboard_preview.svg",
            "docs/demo-index.html",
            "examples/output/demo_review_queue.md",
            "examples/output/public_apple_static_case_study_review_queue.md",
            "examples/output/demo_compare.md",
            "examples/output/case_study_map.md",
            "examples/output/handoff_packet.md",
            "examples/output/promotion_pack.md",
            "examples/output/*_snapshot.json",
            "examples/output/*_review_queue.json",
            "examples/output/demo_review_queue_items.jsonl",
            "examples/output/release_manifest.json",
            "Educational research review only",
            "buy, sell, or hold advice",
            "Pages Demo",
            "Gallery",
            "Promotion Page Outline",
            "Source Attribution Guide",
            "Non-Advice Boundary",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_link_to_demo_screenshot_guide(self):
        expected_links = {
            "README.md": "docs/demo-screenshot-guide.md",
            "docs/gallery.md": "demo-screenshot-guide.md",
            "docs/pages-demo.md": "demo-screenshot-guide.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_first_run_docs_link_to_spreadsheet_comparison(self):
        expected_links = {
            "README.md": "docs/comparison-to-spreadsheets.md",
            "docs/usage.md": "comparison-to-spreadsheets.md",
            "docs/release-notes-v0.9.0.md": "comparison-to-spreadsheets.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_reviewer_feedback_consumption_covers_v08_feedback_threads(self):
        path = ROOT / "docs" / "reviewer-feedback-consumption.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Reviewer Feedback Consumption",
            "Product Clarity",
            "Reproducibility",
            "Demo Evidence",
            "Risk Boundaries",
            "prior reviewer feedback shaped v0.8",
            "15/15",
            "7/10",
            "release-owner approval",
            "Educational research review only",
            "reviewer-evidence.md",
            "release-notes-v0.9.0.md",
            "../reports/reviews/2026-05-17-v0.1.0-internal-review.md",
            "../reports/reviews/2026-05-17-v0.2.0-internal-review.md",
            "../reports/reviews/2026-06-18-v0.9.0-internal-review.md",
            "comparison-to-spreadsheets.md",
            "pages-demo.md",
            "non-advice-boundary.md",
            "case-study-limitations.md",
            "source-attribution-guide.md",
            "security-and-privacy.md",
            "publication-checklist.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/reviewer-feedback-consumption.md", readme)

    def test_reviewer_feedback_consumption_json_matches_summary(self):
        path = ROOT / "reports" / "reviews" / "reviewer_feedback_consumption.json"
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(payload["release"], "0.9.0")
        self.assertEqual(payload["source_doc"], "docs/reviewer-feedback-consumption.md")
        self.assertIn("Educational research review only", payload["safety_notice"])

        threads = {thread["id"]: thread for thread in payload["feedback_threads"]}
        self.assertEqual(
            set(threads),
            {"product_clarity", "reproducibility", "demo_evidence", "risk_boundaries"},
        )
        self.assertEqual(threads["product_clarity"]["v0_8_result"]["score"], "15/15")
        self.assertEqual(threads["reproducibility"]["v0_8_result"]["score"], "15/15")
        self.assertEqual(threads["risk_boundaries"]["v0_8_result"]["score"], "7/10")
        for thread_id, thread in threads.items():
            with self.subTest(thread=thread_id):
                self.assertIn(thread["status"], {"consumed", "consumed_with_owner_gate"})
                self.assertGreaterEqual(len(thread["feedback_consumed"]), 3)
                self.assertGreaterEqual(len(thread["evidence"]), 2)
                for evidence_path in thread["evidence"]:
                    self.assertTrue((ROOT / evidence_path).exists(), evidence_path)

        self.assertEqual(payload["p0"]["status"], "none_found")
        self.assertEqual(payload["p1"]["status"], "none_found_for_small_scope_release")
        self.assertIn("v0.9.0 aligned checkout", payload["p0"]["scope"])
        self.assertIn("small-scope owner handoff", payload["p1"]["scope"])
        self.assertIn("hosted demo decision", payload["p1"]["owner_gates"])
        for severity in ("p0", "p1"):
            with self.subTest(severity=severity):
                self.assertGreaterEqual(len(payload[severity]["evidence"]), 3)
                for evidence_path in payload[severity]["evidence"]:
                    self.assertTrue((ROOT / evidence_path).exists(), evidence_path)

    def test_fresh_clone_verification_document_covers_exact_commands(self):
        path = ROOT / "docs" / "fresh-clone-verification.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")

        for marker in (
            "Fresh Clone Verification",
            "git clone <repo-url> earnings-call-risk-map",
            "cd earnings-call-risk-map",
            "python -m venv .venv",
            ". .venv/bin/activate",
            "python -m pip install --upgrade pip",
            "python -m pip install -e .",
            "mkdir -p verification/fresh-clone",
            "earnings-call-risk-map version | tee verification/fresh-clone/version.txt",
            "PYTHONPATH=src python -m unittest discover -s tests | tee verification/fresh-clone/unittest.txt",
            "PYTHONPATH=src python scripts/selfcheck.py | tee verification/fresh-clone/selfcheck.txt",
            "earnings-call-risk-map demo --out-dir verification/fresh-clone/demo",
            "--json-out verification/fresh-clone/demo_company_snapshot.json",
            "--md-out verification/fresh-clone/demo_company_report.md",
            "--html-out verification/fresh-clone/demo_company_dashboard.html",
            "earnings-call-risk-map review-queue examples/input/demo_company.json",
            "verification/fresh-clone/demo/demo_prior_snapshot.json",
            "verification/fresh-clone/demo/demo_snapshot.json",
            "earnings-call-risk-map audit --format json --out verification/fresh-clone/package_audit.json",
            "earnings-call-risk-map doctor --format json --out verification/fresh-clone/doctor.json",
            "earnings-call-risk-map release-assets --format json --out verification/fresh-clone/release_assets.json",
            "earnings-call-risk-map manifest --out verification/fresh-clone/release_manifest.json",
            "earnings-call-risk-map maturity-evidence --out-dir verification/fresh-clone/maturity",
            "python scripts/privacy_scan.py | tee verification/fresh-clone/privacy_scan.txt",
            "git diff --check | tee verification/fresh-clone/git_diff_check.txt",
            "find verification/fresh-clone -maxdepth 3 -type f | sort | tee verification/fresh-clone/artifact_inventory.txt",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_fresh_clone_verification_document_covers_expected_evidence_artifacts(self):
        path = ROOT / "docs" / "fresh-clone-verification.md"
        text = path.read_text(encoding="utf-8")

        for marker in (
            "contains exactly `0.9.0`",
            "contains `OK` and a `Ran ... tests` line",
            "`== unit tests ==`",
            "`== demo ==`",
            "`== audit ==`",
            "`== release assets ==`",
            "`== privacy scan ==`",
            "`selfcheck passed`",
            "reports the privacy scan status without credential or network findings",
            "empty file, because `git diff --check` should produce no whitespace warnings",
            "`doctor.json`: `status` is `passed`",
            "`package_audit.json`: `local_only.status` is `passed`",
            "`release_assets.json`: `missing_count` is `0`",
            "`demo_company_snapshot.json`: includes ticker `EXM`",
            "Educational research review only",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

        expected_artifacts = (
            "verification/fresh-clone/demo_company_snapshot.json",
            "verification/fresh-clone/demo_company_report.md",
            "verification/fresh-clone/demo_company_dashboard.html",
            "verification/fresh-clone/demo_company_review_queue.json",
            "verification/fresh-clone/demo_company_review_queue.md",
            "verification/fresh-clone/demo_compare.json",
            "verification/fresh-clone/demo_compare.md",
            "verification/fresh-clone/package_audit.json",
            "verification/fresh-clone/doctor.json",
            "verification/fresh-clone/release_assets.json",
            "verification/fresh-clone/release_manifest.json",
            "verification/fresh-clone/maturity/maturity_evidence.json",
            "verification/fresh-clone/maturity/maturity_evidence.md",
            "verification/fresh-clone/demo/demo_snapshot.json",
            "verification/fresh-clone/demo/demo_report.md",
            "verification/fresh-clone/demo/demo_dashboard.html",
            "verification/fresh-clone/demo/demo_review_queue.json",
            "verification/fresh-clone/demo/demo_review_queue.md",
            "verification/fresh-clone/demo/demo_review_queue_items.jsonl",
            "verification/fresh-clone/demo/demo_prior_snapshot.json",
            "verification/fresh-clone/demo/demo_compare.json",
            "verification/fresh-clone/demo/demo_compare.md",
            "verification/fresh-clone/demo/package_audit.json",
            "verification/fresh-clone/demo/doctor.json",
            "verification/fresh-clone/demo/release_manifest.json",
        )
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, text)

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

    def test_docs_cover_blank_json_templates(self):
        path = ROOT / "docs" / "templates.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "examples/templates/software_earnings_review.json",
            "examples/templates/energy_infrastructure_earnings_review.json",
            "examples/templates/consumer_hardware_earnings_review.json",
            "software",
            "energy infrastructure",
            "consumer hardware",
            "Educational research review only",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        usage = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
        self.assertIn("docs/templates.md", readme)
        self.assertIn("templates.md", usage)

    def test_schema_authoring_reference_explains_generated_schema_fields(self):
        path = ROOT / "docs" / "schema-authoring-reference.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        schema = build_schema_reference()

        for marker in (
            "Schema Authoring Reference",
            "schema-reference.json",
            "input-schema.md",
            "Plain-English Meaning",
            "Authoring Guidance",
            "Do not invent source names, publishers, URLs, dates, speaker labels, KPI values, or fiscal periods",
            "does not fetch, refresh, or verify",
            "Educational research review only",
            "buy, sell, or hold advice",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

        field_groups = [
            schema["properties"],
            schema["$defs"]["note"]["properties"],
            schema["$defs"]["kpi"]["properties"],
            schema["$defs"]["catalyst"]["properties"],
            schema["$defs"]["source_record"]["properties"],
        ]
        for properties in field_groups:
            for field in properties:
                with self.subTest(field=field):
                    self.assertIn(f"`{field}`", text)

    def test_input_schema_links_to_schema_authoring_reference(self):
        text = (ROOT / "docs" / "input-schema.md").read_text(encoding="utf-8")
        self.assertIn("schema-authoring-reference.md", text)

    def test_docs_cover_local_only_no_network_guarantee(self):
        for relative_path in ("README.md", "docs/usage.md"):
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("Local-Only No-Network Guarantee", text)
                self.assertIn("network", text.lower())
                self.assertIn("credential", text.lower())
                self.assertIn("audit", text)

    def test_security_and_privacy_document_covers_boundaries(self):
        path = ROOT / "docs" / "security-and-privacy.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Local-Only Operation",
            "No Credentials",
            "No Workflow Files",
            "Privacy Scan Assumptions",
            "does not fetch live data",
            "credential environment variable reads",
            "`.github/workflows`",
            "`python scripts/privacy_scan.py`",
            "not a full data-loss-prevention system",
            "Local-Only No-Network Guarantee",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        usage = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
        self.assertIn("docs/security-and-privacy.md", readme)
        self.assertIn("security-and-privacy.md", usage)

    def test_maintenance_document_covers_release_owner_routine_and_boundaries(self):
        path = ROOT / "docs" / "maintenance.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Release Owner Routine",
            "Regeneration Commands",
            "Known Boundaries",
            "No-Workflow-Scope Policy",
            "PYTHONPATH=src python scripts/selfcheck.py",
            "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
            "PYTHONPATH=src python -m earnings_call_risk_map release-assets --format markdown",
            "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
            "PYTHONPATH=src python -m unittest",
            "PYTHONPATH=src python scripts/privacy_scan.py",
            "release owner",
            "local-only",
            "must not fetch live market data",
            "read credential environment variables",
            "must not be converted into price targets",
            "`source_type`",
            "`accessed_at`",
            "not a full data-loss-prevention system",
            "no required `.github/workflows` scope",
            "Do not add CI, release automation, scheduled jobs, hosted runners, or workflow-only release steps",
            "Educational research review only",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_release_docs_link_to_maintenance(self):
        expected_links = {
            "README.md": "docs/maintenance.md",
            "docs/release-readiness.md": "docs/maintenance.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_release_owner_handoff_covers_final_v08_owner_gates(self):
        path = ROOT / "docs" / "release-owner-handoff.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Release Owner Handoff",
            "Final v0.9 Release Owner Checklist",
            "Exact Verification Commands",
            "Promotion Evidence Paths",
            "Owner-Controlled Promotion Gates",
            "Confirm release metadata agrees on `0.9.0`",
            "git status --short",
            "git tag -a v0.9.0 -m \"v0.9.0\"",
            "gh release create v0.9.0 --title \"v0.9.0\" --notes-file docs/release-notes-v0.9.0.md",
            "PYTHONPATH=src python -m earnings_call_risk_map version",
            "PYTHONPATH=src python -m unittest discover -s tests",
            "PYTHONPATH=src python scripts/selfcheck.py",
            "PYTHONPATH=src python -m earnings_call_risk_map audit --format json",
            "PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json",
            "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
            "python scripts/privacy_scan.py",
            "git diff --check",
            "selfcheck passed",
            "privacy scan passed",
            "missing_count",
            "reports/reviews/2026-06-18-v0.9.0-final-review.md",
            "reports/reviews/2026-06-18-v0.9.0-promotion-review.md",
            "reports/maturity/maturity_evidence.md",
            "examples/output/promotion_pack.md",
            "examples/output/public_apple_static_case_study_dashboard.html",
            "docs/assets/showcase-dashboard-preview.svg",
            "skills/agent/earnings-call-risk-map/SKILL.md",
            "does not itself perform or approve tag creation",
            "Educational research review only",
            "buy, sell, or hold advice",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_release_docs_link_to_release_owner_handoff(self):
        expected_links = {
            "README.md": "docs/release-owner-handoff.md",
            "docs/release-readiness.md": "docs/release-owner-handoff.md",
            "docs/publication-checklist.md": "release-owner-handoff.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_faq_covers_cold_user_and_analyst_boundaries(self):
        path = ROOT / "docs" / "faq.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "cold users",
            "analysts",
            "does not fetch live market data",
            "static educational fixtures",
            "Why JSON?",
            "inspectable, repeatable",
            "How Do I Use This With Transcripts?",
            "Use transcripts as source material, not as live input",
            "management_claim",
            "analyst_question",
            "user_synthesis",
            "The tool is deterministic and conservative",
            "does not forecast revenue, margins, cash flow, valuation, price targets",
            "Where Is The Advice Boundary?",
            "Do not convert risk scores",
            "buy, sell, hold",
            "Non-Advice Boundary",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_fixture_catalog_document_covers_bundled_fixtures(self):
        path = ROOT / "docs" / "fixture-catalog.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "examples/input/demo_company.json",
            "examples/input/demo_energy_infrastructure.json",
            "examples/input/consumer_hardware.json",
            "examples/input/semiconductor_equipment.json",
            "examples/input/public_apple_static_case_study.json",
            "examples/input/demo_company_prior.json",
            "Static/live status",
            "fixture-catalog",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_fixture_summary_document_covers_command_and_cold_user_onboarding(self):
        path = ROOT / "docs" / "fixture-summary.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "fixture-summary",
            "cold-user onboarding",
            "source types",
            "stale badges",
            "source-boundary labels",
            "notes, KPIs, catalysts, risks, opportunities",
            "artifact_type: \"fixture_summary\"",
            "examples/input/semiconductor_equipment.json",
            "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md",
            "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json",
            "Educational research review only",
            "Tutorial: First 30 Minutes",
            "Source Attribution Guide",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_case_study_map_covers_fixtures_questions_and_artifacts(self):
        path = ROOT / "docs" / "case-study-map.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Target sector",
            "Useful question",
            "Generated artifacts",
            "examples/input/demo_company.json",
            "examples/input/demo_company_prior.json",
            "examples/input/demo_energy_infrastructure.json",
            "examples/input/consumer_hardware.json",
            "examples/input/semiconductor_equipment.json",
            "examples/input/public_apple_static_case_study.json",
            "examples/input/sample_filled_template_workflow.json",
            "Software and enterprise platform",
            "Energy infrastructure",
            "Consumer hardware",
            "Semiconductor equipment",
            "examples/output/demo_report.md",
            "examples/output/demo_compare.md",
            "examples/output/energy_infrastructure_report.md",
            "examples/output/consumer_hardware_report.md",
            "examples/output/semiconductor_equipment_report.md",
            "examples/output/public_apple_static_case_study_report.md",
            "examples/output/sample_filled_template_report.md",
            "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md",
            "Educational research review only",
            "Fixture Catalog",
            "Case Study Limitations",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_link_to_fixture_summary(self):
        expected_links = {
            "README.md": "docs/fixture-summary.md",
            "docs/usage.md": "fixture-summary.md",
            "docs/tutorial-first-30-minutes.md": "fixture-summary.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
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
            "Review queue prioritization",
            "Items with more review issue categories first",
            "A stale-only item can still rank below a current item",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_risk_language_taxonomy_covers_review_rules(self):
        path = ROOT / "docs" / "risk-language-taxonomy.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Deterministic Score Bands",
            "`score = 0`",
            "`1 <= score <= 3`",
            "`4 <= score <= 6`",
            "`score >= 7`",
            "High-Impact Trigger",
            "risk score is `>= 7`",
            "opportunity score is `>= 7`",
            "stale adjustment",
            "Stale And Missing Evidence Priority",
            "stale or unverified date metadata",
            "missing evidence URL",
            "Items with more review issue categories appear first",
            "A stale-only item can rank below a current item",
            "Human Review Boundary",
            "portfolio-risk or thesis-ledger",
            "buy, sell, or hold actions",
            "scoring.md",
            "source-attribution-guide.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_link_to_risk_language_taxonomy(self):
        expected_links = {
            "README.md": "docs/risk-language-taxonomy.md",
            "docs/gallery.md": "examples/output/risk_language_taxonomy.md",
            "docs/usage.md": "risk-language-taxonomy.md",
            "docs/scoring.md": "risk-language-taxonomy.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_generated_risk_language_taxonomy_artifact_links_to_static_docs(self):
        path = ROOT / "examples" / "output" / "risk_language_taxonomy.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Risk Language Taxonomy",
            "../../docs/scoring.md",
            "../../docs/source-attribution-guide.md",
            "Items with more review issue categories appear first",
            "buy, sell, or hold actions",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_cover_review_queue_prioritization_and_human_handoff(self):
        usage = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
        integrations = (ROOT / "docs" / "integrations.md").read_text(encoding="utf-8")
        for text in (usage, integrations):
            for marker in (
                "prioritization",
                "severity",
                "stale",
                "human_handoff",
                "portfolio-risk or thesis-ledger",
            ):
                with self.subTest(marker=marker):
                    self.assertIn(marker, text)

    def test_decision_ledger_integration_document_covers_paste_workflow_and_boundaries(self):
        path = ROOT / "docs" / "decision-ledger-integration.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "investment thesis ledger",
            "handoff_packet.md",
            "demo_review_queue.md",
            "demo_compare.md",
            "demo_report.md",
            "Ledger Entry Template",
            "Paste Pattern",
            "Non-Advice Guardrails",
            "Educational research review only",
            "not personalized investment, legal, accounting, tax, buy, sell, or hold advice",
            "Deterministic scores and compare deltas are review prompts, not portfolio actions",
            "risk attention increased",
            "management claims",
            "analyst questions",
            "source attribution",
            "Non-Advice Boundary",
            "Integration Notes",
            "Case Study Limitations",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_link_to_decision_ledger_integration(self):
        expected_links = {
            "README.md": "docs/decision-ledger-integration.md",
            "docs/usage.md": "decision-ledger-integration.md",
            "docs/integrations.md": "decision-ledger-integration.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_agent_workflow_integration_document_covers_commands_verification_and_boundaries(self):
        path = ROOT / "docs" / "agent-workflow-integration.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Agent Workflow Integration",
            "generic coding or research agent",
            "Integration Contract",
            "Calling Commands",
            "Verifying Outputs",
            "Research Summaries",
            "Stop Boundaries",
            "Handoff Format",
            "PYTHONPATH=src python -m unittest tests/test_docs.py",
            "PYTHONPATH=src python -m unittest discover -s tests",
            "PYTHONPATH=src python scripts/selfcheck.py",
            "PYTHONPATH=src python scripts/privacy_scan.py",
            "git diff --check",
            "PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json",
            "PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json",
            "Do not claim a check passed unless the command completed successfully in the current workspace",
            "`safety_notice`",
            "`source_boundaries`",
            "`review_queue`",
            "stale/static data badges",
            "missing `evidence_url` records",
            "risk attention increased",
            "the fixture records a management claim",
            "the review queue flags missing evidence",
            "fetch or refresh live market data",
            "verify a source URL by browsing or using network access",
            "recommend buy, sell, hold",
            "remove stale/static warnings, missing-evidence reasons, or safety notices",
            "files changed or generated",
            "commands run",
            "verification result for each command",
            "No live data was fetched; no buy, sell, hold, valuation, or suitability conclusion was made",
            "Educational research review only",
            "Non-Advice Boundary",
            "Security and Privacy",
            "Reviewer Evidence",
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

    def test_known_limitations_consolidates_public_boundaries(self):
        path = ROOT / "docs" / "known-limitations.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Known Limitations",
            "Static Data Only",
            "No Live Fetching",
            "Scoring Limits",
            "Source Trust Limits",
            "No Advice",
            "No Portfolio Suitability",
            "static JSON fixtures",
            "does not refresh source packets",
            "does not call APIs",
            "fetch live market data",
            "Evidence URLs are attribution metadata",
            "Scores are deterministic attention signals",
            "not measure business quality, probability, valuation, expected return, price movement, or securities risk",
            "does not verify source truth",
            "Management claims remain company-provided statements",
            "Analyst questions remain questions or prompts",
            "User synthesis remains reviewer-authored context",
            "Missing evidence, stale dates, and `date-unverified` badges are human review triggers",
            "educational research review only",
            "not personalized investment, legal, accounting, tax, buy, sell, hold",
            "price targets, ratings, forecasts, allocation changes, trade instructions, or professional advice",
            "cannot assess whether any security, issuer, sector, thesis, catalyst, exposure, or risk is suitable",
            "Case Study Limitations",
            "Non-Advice Boundary",
            "Scoring",
            "Source Attribution Guide",
            "Security and Privacy",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_readme_and_skill_link_to_known_limitations(self):
        expected_links = {
            "README.md": "docs/known-limitations.md",
            "skills/agent/earnings-call-risk-map/SKILL.md": "docs/known-limitations.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_source_attribution_guide_covers_provenance_boundaries(self):
        path = ROOT / "docs" / "source-attribution-guide.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Source Attribution Guide",
            "`source_type` Choices",
            "`accessed_at`",
            "Stale Badges",
            "Management, Analyst, And User Synthesis",
            "company_investor_relations",
            "sec_filing",
            "transcript",
            "shareholder_letter",
            "user_synthesis",
            "management_claim",
            "analyst_question",
            "`source_type` answers where the source record came from",
            "Note `type` answers how to treat the text inside the review",
            "Stale badges are based on item dates compared with fixture `as_of`, not on `accessed_at`",
            "User synthesis is a review aid and not source evidence",
            "Educational research review only",
            "input-schema.md",
            "non-advice-boundary.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_docs_link_to_source_attribution_guide(self):
        expected_links = {
            "README.md": "docs/source-attribution-guide.md",
            "docs/input-schema.md": "source-attribution-guide.md",
            "docs/usage.md": "source-attribution-guide.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_troubleshooting_covers_common_review_failures_with_field_paths(self):
        path = ROOT / "docs" / "troubleshooting.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for marker in (
            "Validation Errors",
            "Stale Badges",
            "Missing Evidence",
            "Compare Interpretation",
            "Educational research review only",
            "input-schema.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

        field_paths = (
            "fixture.company",
            "fixture.as_of",
            "fixture.data_cutoff",
            "fixture.notes[0].date",
            "fixture.kpis[0].source_attribution[0].accessed_at",
            "fixture.catalysts[0].source_attribution",
            "fixture.kpis[0].date",
            "fixture.notes[0].evidence_url",
            "fixture.catalysts[0].evidence_url",
            "fixture.notes[*].date",
            "fixture.kpis[*].evidence_url",
        )
        for field_path in field_paths:
            with self.subTest(field_path=field_path):
                self.assertIn(field_path, text)

    def test_first_run_docs_link_to_troubleshooting(self):
        expected_links = {
            "README.md": "docs/troubleshooting.md",
            "docs/usage.md": "troubleshooting.md",
        }
        for relative_path, marker in expected_links.items():
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(marker, text)

    def test_docs_cover_software_vs_energy_compare_without_advice(self):
        for relative_path in ("README.md", "docs/usage.md", "docs/gallery.md"):
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("software", text)
                self.assertIn("energy infrastructure", text)
                self.assertIn("cross-fixture", text)
                self.assertIn("investment", text)
                self.assertTrue("buy, sell, hold" in text or "buy, sell, or hold advice" in text)

        usage = (ROOT / "docs" / "usage.md").read_text(encoding="utf-8")
        for marker in (
            "examples/input/demo_company.json",
            "examples/input/demo_energy_infrastructure.json",
            "examples/output/software_vs_energy_compare.md",
            "examples/output/software_vs_energy_compare.json",
            "must not be converted into buy, sell, hold",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, usage)

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

    def test_demo_index_is_local_static_page(self):
        path = ROOT / "docs" / "demo-index.html"
        self.assertTrue(path.is_file())

        parser = DemoIndexParser()
        parser.feed(path.read_text(encoding="utf-8"))

        self.assertEqual([], parser.scripts)
        self.assertEqual([], parser.external_targets)
        self.assertIn("../examples/output/demo_dashboard.html", parser.local_targets)
        self.assertIn("../examples/output/showcase_dashboard_preview.svg", parser.local_targets)
        self.assertIn("../examples/output/demo_report.md", parser.local_targets)

        for raw_target in parser.local_targets:
            parsed = urlparse(unquote(raw_target))
            if parsed.path:
                with self.subTest(target=raw_target):
                    self.assertTrue((path.parent / parsed.path).resolve().exists())


if __name__ == "__main__":
    unittest.main()
