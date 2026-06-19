#!/usr/bin/env python3
"""Run the local MVP verification suite."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = {"PYTHONPATH": str(ROOT / "src")}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
DOC_LINK_CHECK_PATHS = (
    Path("README.md"),
    Path("examples/playbooks/README.md"),
    Path("examples/playbooks/quarterly-review.md"),
    Path("examples/playbooks/catalyst-check-in.md"),
    Path("examples/playbooks/post-earnings-thesis-refresh.md"),
    Path("docs/tutorial-earnings-review.md"),
    Path("docs/distribution.md"),
    Path("docs/non-advice-boundary.md"),
    Path("docs/comparison-to-spreadsheets.md"),
    Path("docs/release-readiness.md"),
    Path("docs/reviewer-evidence.md"),
    Path("docs/release-notes-v0.9.3.md"),
)
REQUIRED_DOC_PATHS = (
    Path("docs/tutorial-earnings-review.md"),
    Path("docs/comparison-to-spreadsheets.md"),
    Path("examples/playbooks/README.md"),
    Path("examples/playbooks/quarterly-review.md"),
    Path("examples/playbooks/catalyst-check-in.md"),
    Path("examples/playbooks/post-earnings-thesis-refresh.md"),
)


def run(label: str, command: list[str]) -> int:
    print(f"== {label} ==", flush=True)
    result = subprocess.run(command, cwd=ROOT, env=ENV, text=True)
    if result.returncode != 0:
        print(f"{label} failed with exit code {result.returncode}")
    return result.returncode


def check_demo_dashboard() -> int:
    print("== demo dashboard ==", flush=True)
    path = ROOT / "examples/output/demo_dashboard.html"
    if not path.is_file():
        print(f"{path.relative_to(ROOT)} is missing")
        return 1
    text = path.read_text(encoding="utf-8")
    required = ("<!doctype html>", "Review Queue", "Stale Badges", "Catalysts")
    missing = [value for value in required if value not in text]
    forbidden = ("<script", "<link")
    blocked = [value for value in forbidden if value in text.lower()]
    if missing or blocked:
        if missing:
            print("missing dashboard marker(s): " + ", ".join(missing))
        if blocked:
            print("external asset marker(s) found: " + ", ".join(blocked))
        return 1
    print("demo dashboard passed")
    return 0


def check_showcase_previews() -> int:
    print("== showcase previews ==", flush=True)
    paths = [
        ROOT / "examples/output/demo_dashboard.html",
        ROOT / "examples/output/energy_infrastructure_dashboard.html",
        ROOT / "examples/output/consumer_hardware_dashboard.html",
        ROOT / "examples/output/semiconductor_equipment_dashboard.html",
        ROOT / "examples/output/public_apple_static_case_study_dashboard.html",
        ROOT / "examples/output/showcase_dashboard_preview.svg",
        ROOT / "docs/assets/showcase-dashboard-preview.svg",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in paths if not path.is_file()]
    if missing:
        print("missing preview file(s): " + ", ".join(missing))
        return 1

    blocked_markers = ("<script", "<link", "<img", " src=", "xlink:href=", "url(http://", "url(https://")
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        blocked = [marker for marker in blocked_markers if marker in text]
        if blocked:
            rel = path.relative_to(ROOT).as_posix()
            print(f"{rel} contains external asset marker(s): " + ", ".join(blocked))
            return 1
    print("showcase previews passed")
    return 0


def check_semiconductor_equipment_report_bundle() -> int:
    print("== semiconductor equipment report bundle ==", flush=True)
    paths = [
        ROOT / "examples/output/semiconductor_equipment_report/report.md",
        ROOT / "examples/output/semiconductor_equipment_report/dashboard/dashboard.html",
        ROOT / "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json",
        ROOT / "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md",
        ROOT / "examples/output/semiconductor_equipment_report/review_queue/review_queue.json",
        ROOT / "examples/output/semiconductor_equipment_report/review_queue/review_queue.md",
        ROOT / "examples/output/semiconductor_equipment_report/snapshot/snapshot.json",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in paths if not path.is_file()]
    if missing:
        print("missing semiconductor equipment report bundle artifact(s): " + ", ".join(missing))
        return 1

    snapshot = json.loads((ROOT / "examples/output/semiconductor_equipment_report/snapshot/snapshot.json").read_text(encoding="utf-8"))
    review_queue = json.loads(
        (ROOT / "examples/output/semiconductor_equipment_report/review_queue/review_queue.json").read_text(
            encoding="utf-8"
        )
    )
    fixture_summary = json.loads(
        (ROOT / "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json").read_text(
            encoding="utf-8"
        )
    )
    if snapshot.get("ticker") != "ASML" or snapshot.get("summary", {}).get("review_queue_count", 0) < 1:
        print("semiconductor equipment snapshot has unexpected ticker or review queue count")
        return 1
    if review_queue.get("ticker") != "ASML" or not review_queue.get("items"):
        print("semiconductor equipment review queue is missing expected ASML items")
        return 1
    if fixture_summary.get("artifact_type") != "fixture_summary" or fixture_summary.get("ticker") != "ASML":
        print("semiconductor equipment fixture summary has unexpected type or ticker")
        return 1

    dashboard = (ROOT / "examples/output/semiconductor_equipment_report/dashboard/dashboard.html").read_text(
        encoding="utf-8"
    )
    blocked_markers = ("<script", "<link", "<img", " src=", "xlink:href=", "url(http://", "url(https://")
    blocked = [marker for marker in blocked_markers if marker in dashboard.lower()]
    required_markers = ("<!doctype html>", "ASML", "Review Queue", "Source Attribution")
    missing_markers = [marker for marker in required_markers if marker not in dashboard]
    if blocked or missing_markers:
        if blocked:
            print("semiconductor equipment dashboard contains external asset marker(s): " + ", ".join(blocked))
        if missing_markers:
            print("semiconductor equipment dashboard missing marker(s): " + ", ".join(missing_markers))
        return 1

    manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    for path in (item.relative_to(ROOT).as_posix() for item in paths):
        if path not in manifest_paths:
            print(f"release manifest missing semiconductor equipment report bundle path: {path}")
            return 1
    print("semiconductor equipment report bundle passed")
    return 0


def check_integration_examples() -> int:
    print("== integration examples ==", flush=True)
    docs = [
        ROOT / "docs/integrations.md",
        ROOT / "docs/gallery.md",
    ]
    missing_docs = [path.relative_to(ROOT).as_posix() for path in docs if not path.is_file()]
    if missing_docs:
        print("missing integration doc(s): " + ", ".join(missing_docs))
        return 1

    path = ROOT / "examples/output/integration_notes.json"
    if not path.is_file():
        print(f"{path.relative_to(ROOT)} is missing")
        return 1
    payload = json.loads(path.read_text(encoding="utf-8"))
    notes = payload.get("notes", [])
    integrations = {note.get("integration") for note in notes}
    required = {"thesis_ledger", "portfolio_risk_review"}
    if payload.get("source_tool") != "earnings-call-risk-map" or not required.issubset(integrations):
        print("integration notes missing required source_tool or integration labels")
        return 1
    for note in notes:
        if not note.get("source_artifact") or not note.get("source_notice"):
            print("integration note missing source artifact or safety notice")
            return 1
    print("integration examples passed")
    return 0


def check_compare_examples() -> int:
    print("== compare examples ==", flush=True)
    json_path = ROOT / "examples/output/demo_compare.json"
    md_path = ROOT / "examples/output/demo_compare.md"
    prior_path = ROOT / "examples/output/demo_prior_snapshot.json"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path, prior_path)
        if not path.is_file()
    ]
    if missing:
        print("missing compare artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("before_as_of") != "2026-02-15" or payload.get("after_as_of") != "2026-05-15":
        print("compare artifact has unexpected before/after dates")
        return 1
    if not payload.get("interpretation"):
        print("compare artifact missing interpretation")
        return 1
    risk_topics = {item.get("topic") for item in payload.get("risk_changes", [])}
    opportunity_topics = {item.get("topic") for item in payload.get("opportunity_changes", [])}
    if "gross margin" not in risk_topics or "product launch" not in opportunity_topics:
        print("compare artifact missing expected demo score movement")
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required = ("Snapshot Compare", "How To Read This Compare", "Risk Changes", "Opportunity Changes")
    missing_markers = [marker for marker in required if marker not in markdown]
    if missing_markers:
        print("compare markdown missing marker(s): " + ", ".join(missing_markers))
        return 1
    print("compare examples passed")
    return 0


def check_review_queue_jsonl() -> int:
    print("== review queue jsonl ==", flush=True)
    path = ROOT / "examples/output/demo_review_queue_items.jsonl"
    if not path.is_file():
        print(f"{path.relative_to(ROOT)} is missing")
        return 1
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        print("review queue JSONL is empty")
        return 1
    try:
        records = [json.loads(line) for line in lines]
    except json.JSONDecodeError as exc:
        print(f"review queue JSONL is invalid at line {exc.lineno}, column {exc.colno}")
        return 1
    slugs = {record.get("fixture_slug") for record in records}
    required_slugs = {
        "demo",
        "energy_infrastructure",
        "consumer_hardware",
        "semiconductor_equipment",
        "public_apple_static_case_study",
        "demo_prior",
    }
    if not required_slugs.issubset(slugs):
        print("review queue JSONL missing fixture slug(s): " + ", ".join(sorted(required_slugs - slugs)))
        return 1
    for record in records:
        if record.get("record_type") != "review_queue_item" or not record.get("review_item"):
            print("review queue JSONL contains a malformed review item record")
            return 1
    print("review queue jsonl passed")
    return 0


def check_source_boundary_evidence() -> int:
    print("== source boundary evidence ==", flush=True)
    json_path = ROOT / "examples/output/source_boundary_evidence.json"
    md_path = ROOT / "examples/output/source_boundary_evidence.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing source boundary evidence artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "source_boundary_evidence" or payload.get("fixture_count") != 6:
        print("source boundary evidence has unexpected artifact type or fixture count")
        return 1
    checks = payload.get("checks", {})
    required_true_checks = (
        "all_fixture_paths_exist",
        "all_fixtures_are_static_or_local",
        "no_private_paths_found",
        "no_live_fetching_required",
        "no_broker_or_api_credentials_required",
        "no_advice_claim_present",
    )
    for check in required_true_checks:
        if checks.get(check) is not True:
            print(f"source boundary evidence failed check: {check}")
            return 1
    if checks.get("walkthrough_receipt_present") is not True:
        print("source boundary evidence is missing walkthrough receipt check")
        return 1

    fixture_paths = {fixture.get("path") for fixture in payload.get("fixtures", [])}
    required_fixtures = {
        "examples/input/demo_company.json",
        "examples/input/demo_company_prior.json",
        "examples/input/demo_energy_infrastructure.json",
        "examples/input/consumer_hardware.json",
        "examples/input/semiconductor_equipment.json",
        "examples/input/public_apple_static_case_study.json",
    }
    if fixture_paths != required_fixtures:
        print("source boundary evidence fixture path mismatch")
        return 1
    for fixture in payload.get("fixtures", []):
        if fixture.get("has_private_path") or not (ROOT / fixture.get("path", "")).is_file():
            print(f"source boundary evidence fixture has private or missing path: {fixture.get('path')}")
            return 1
        if fixture.get("fixture_boundary") not in {
            "static_fixture",
            "static_public_source_fixture",
            "static_compare_baseline",
        }:
            print(f"source boundary evidence fixture has unexpected boundary: {fixture.get('path')}")
            return 1
    receipt = payload.get("walkthrough_receipt", {})
    if receipt.get("receipt_type") != "public_source_boundary_walkthrough":
        print("source boundary evidence has unexpected walkthrough receipt type")
        return 1
    if receipt.get("public_source_fixture_count") != 3 or receipt.get("static_or_local_fixture_count") != 6:
        print("source boundary evidence walkthrough receipt has unexpected fixture counts")
        return 1
    if receipt.get("public_source_demo_receipt_count") != 3:
        print("source boundary evidence walkthrough receipt has unexpected fixture-scoped demo receipt count")
        return 1
    receipt_checks = receipt.get("checks", {})
    for check in (
        "public_source_fixtures_present",
        "all_public_source_demo_receipts_present",
        "all_public_source_demo_receipt_artifacts_exist",
        "all_receipt_artifacts_exist",
        "all_fixture_boundaries_static_or_local",
        "dashboard_handoff_paths_recorded",
        "no_live_data_boundary_recorded",
        "no_advice_boundary_recorded",
    ):
        if receipt_checks.get(check) is not True:
            print(f"source boundary walkthrough receipt failed check: {check}")
            return 1
    if receipt.get("missing_artifact_count") != 0 or len(receipt.get("steps", [])) != 4:
        print("source boundary walkthrough receipt has missing artifacts or malformed steps")
        return 1
    demo_receipts = receipt.get("public_source_demo_receipts", [])
    demo_receipt_slugs = {item.get("fixture_slug") for item in demo_receipts}
    required_demo_receipt_slugs = {
        "consumer_hardware",
        "semiconductor_equipment",
        "public_apple_static_case_study",
    }
    if demo_receipt_slugs != required_demo_receipt_slugs:
        print("source boundary walkthrough receipt has unexpected fixture-scoped demo receipt slugs")
        return 1
    for demo_receipt in demo_receipts:
        if demo_receipt.get("receipt_type") != "fixture_scoped_public_source_demo":
            print(f"source boundary walkthrough receipt has unexpected demo receipt type: {demo_receipt.get('fixture_slug')}")
            return 1
        if demo_receipt.get("missing_demo_artifact_count") != 0:
            print(f"source boundary walkthrough receipt has missing demo artifacts: {demo_receipt.get('fixture_slug')}")
            return 1
        demo_checks = demo_receipt.get("checks", {})
        for check in (
            "fixture_exists",
            "fixture_is_public_source",
            "source_metadata_present",
            "source_urls_recorded",
            "static_notices_recorded",
            "all_demo_artifacts_exist",
            "local_only_demo_scope",
            "no_live_data_boundary_recorded",
            "no_advice_boundary_recorded",
        ):
            if demo_checks.get(check) is not True:
                print(f"source boundary fixture-scoped demo receipt failed check: {demo_receipt.get('fixture_slug')} {check}")
                return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Source Boundary Evidence",
        "Walkthrough Receipt",
        "Fixture-Scoped Public-Source Demo Receipts",
        "Verify bundled static fixtures",
        "Verify dashboard and release-owner handoff",
        "No live data",
        "No advice",
        "examples/input/public_apple_static_case_study.json",
        "examples/input/semiconductor_equipment.json",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("source boundary evidence markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    release_manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    demo_manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8")).get(
            "files", []
        )
    }
    for path in ("examples/output/source_boundary_evidence.md", "examples/output/source_boundary_evidence.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing source boundary evidence path: {path}")
            return 1
        if path not in release_manifest_paths:
            print(f"release manifest missing source boundary evidence path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing source boundary evidence path: {path}")
            return 1
    print("source boundary evidence passed")
    return 0


def check_docs_links() -> int:
    print("== docs links ==", flush=True)
    failures = []
    for relative_path in DOC_LINK_CHECK_PATHS:
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"{relative_path.as_posix()} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or _is_external_or_anchor(target):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                failures.append(f"{relative_path.as_posix()} links outside repo: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{relative_path.as_posix()} has missing link target: {target}")
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("docs links passed")
    return 0


def check_required_docs() -> int:
    print("== required docs ==", flush=True)
    missing = [path.as_posix() for path in REQUIRED_DOC_PATHS if not (ROOT / path).is_file()]
    if missing:
        print("missing required doc(s): " + ", ".join(missing))
        return 1

    tutorial = ROOT / "docs/tutorial-earnings-review.md"
    text = tutorial.read_text(encoding="utf-8")
    required_markers = (
        "fixture",
        "report",
        "review queue",
        "compare",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in text]
    if missing_markers:
        print("tutorial missing marker(s): " + ", ".join(missing_markers))
        return 1

    print("required docs passed")
    return 0


def check_playbooks() -> int:
    print("== research playbooks ==", flush=True)
    required = {
        Path("examples/playbooks/README.md"): (
            "Quarterly Review",
            "Catalyst Check-In",
            "Post-Earnings Thesis Refresh",
            "deterministic",
            "Educational research review only",
        ),
        Path("examples/playbooks/quarterly-review.md"): (
            "Deterministic Steps",
            "review-queue",
            "compare",
            "Expected Artifacts",
            "Educational research review only",
        ),
        Path("examples/playbooks/catalyst-check-in.md"): (
            "Deterministic Steps",
            "catalyst",
            "review-queue-jsonl",
            "Expected Artifacts",
            "Educational research review only",
        ),
        Path("examples/playbooks/post-earnings-thesis-refresh.md"): (
            "Deterministic Steps",
            "Source Boundaries",
            "integration_notes.json",
            "Expected Artifacts",
            "Educational research review only",
        ),
    }
    failures = []
    for relative_path, markers in required.items():
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"{relative_path.as_posix()} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            failures.append(f"{relative_path.as_posix()} missing marker(s): " + ", ".join(missing))
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("research playbooks passed")
    return 0


def check_playbook_output_examples() -> int:
    print("== playbook output examples ==", flush=True)
    json_path = ROOT / "examples/output/playbook_output_examples.json"
    md_path = ROOT / "examples/output/playbook_output_examples.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing playbook output example artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "playbook_output_examples" or payload.get("playbook_count") != 3:
        print("playbook output examples have unexpected type or count")
        return 1
    required_slugs = {"quarterly-review", "catalyst-check-in", "post-earnings-thesis-refresh"}
    slugs = {example.get("slug") for example in payload.get("examples", [])}
    if slugs != required_slugs:
        print("playbook output examples missing slug(s): " + ", ".join(sorted(required_slugs - slugs)))
        return 1
    for example in payload.get("examples", []):
        artifacts = example.get("generated_artifacts", [])
        if not artifacts:
            print(f"{example.get('slug')} has no generated artifacts")
            return 1
        for artifact in artifacts:
            path = artifact.get("path", "")
            if not path.startswith("examples/output/") or not artifact.get("format") or not artifact.get("role"):
                print(f"{example.get('slug')} has malformed generated artifact metadata")
                return 1
            if not (ROOT / path).is_file():
                print(f"{example.get('slug')} points at missing artifact: {path}")
                return 1
    markdown = md_path.read_text(encoding="utf-8")
    required_markers = ("Playbook Output Examples", "Quarterly Review", "Catalyst Check-In", "Selfcheck")
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("playbook output examples markdown missing marker(s): " + ", ".join(missing_markers))
        return 1
    print("playbook output examples passed")
    return 0


def check_handoff_packet_examples() -> int:
    print("== handoff packet examples ==", flush=True)
    json_path = ROOT / "examples/output/handoff_packet_examples.json"
    md_path = ROOT / "examples/output/handoff_packet_examples.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing handoff packet example artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "handoff_packet_examples" or payload.get("example_count") != 3:
        print("handoff packet examples have unexpected type or count")
        return 1
    for example in payload.get("examples", []):
        packet = example.get("packet", {})
        if packet.get("packet_type") != "portfolio_thesis_handoff":
            print(f"{example.get('slug')} has unexpected handoff packet type")
            return 1
        artifacts = packet.get("artifacts", [])
        if len(artifacts) != 3 or artifacts[1].get("format") != "jsonl":
            print(f"{example.get('slug')} has malformed handoff artifact metadata")
            return 1
        if packet.get("handoff_targets") != ["portfolio_risk_review", "thesis_ledger"]:
            print(f"{example.get('slug')} has unexpected handoff targets")
            return 1
        for artifact in artifacts:
            path = artifact.get("path", "")
            if not path.startswith("examples/output/") or not (ROOT / path).is_file():
                print(f"{example.get('slug')} points at missing handoff artifact: {path}")
                return 1
    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Handoff Packet Examples",
        "Quarterly Review Handoff",
        "Catalyst Check-In Handoff",
        "Post-Earnings Thesis Refresh Handoff",
        "Downstream portfolio and thesis systems own exposure sizing",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("handoff packet examples markdown missing marker(s): " + ", ".join(missing_markers))
        return 1
    print("handoff packet examples passed")
    return 0


def check_template_catalog() -> int:
    print("== template catalog ==", flush=True)
    json_path = ROOT / "examples/output/template_catalog.json"
    md_path = ROOT / "examples/output/template_catalog.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing template catalog artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "template_catalog" or payload.get("template_count") != 3:
        print("template catalog has unexpected type or count")
        return 1
    required_slugs = {"software", "energy_infrastructure", "consumer_hardware"}
    slugs = {template.get("slug") for template in payload.get("templates", [])}
    if slugs != required_slugs:
        print("template catalog missing slug(s): " + ", ".join(sorted(required_slugs - slugs)))
        return 1
    for template in payload.get("templates", []):
        path = template.get("path", "")
        fields = template.get("recommended_fields", {})
        commands = template.get("recommended_commands", [])
        if not path.startswith("examples/templates/") or not (ROOT / path).is_file():
            print(f"{template.get('slug')} points at missing template: {path}")
            return 1
        if fields.get("top_level") != ["company", "ticker", "as_of", "data_cutoff"]:
            print(f"{template.get('slug')} has malformed top-level field guidance")
            return 1
        if not fields.get("note_fields") or not fields.get("kpi_fields") or not fields.get("catalyst_fields"):
            print(f"{template.get('slug')} has incomplete recommended field metadata")
            return 1
        if not any(path in command for command in commands):
            print(f"{template.get('slug')} has no command for its template path")
            return 1
    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Template Catalog",
        "Recommended Fields And Commands",
        "Software Earnings Review",
        "Consumer Hardware Earnings Review",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("template catalog markdown missing marker(s): " + ", ".join(missing_markers))
        return 1
    print("template catalog passed")
    return 0


def check_schema_authoring_reference() -> int:
    print("== schema authoring reference ==", flush=True)
    json_path = ROOT / "examples/output/schema_authoring_reference.json"
    md_path = ROOT / "examples/output/schema_authoring_reference.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing schema authoring reference artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "schema_authoring_reference":
        print("schema authoring reference has unexpected artifact type")
        return 1
    if payload.get("source_doc") != "docs/schema-authoring-reference.md":
        print("schema authoring reference has unexpected source doc")
        return 1
    if payload.get("schema_reference") != "docs/schema-reference.json":
        print("schema authoring reference has unexpected schema reference")
        return 1
    section_slugs = {section.get("slug") for section in payload.get("sections", [])}
    required_slugs = {"top_level", "notes", "kpis", "catalysts", "source_attribution"}
    if section_slugs != required_slugs:
        missing_slugs = sorted(required_slugs - section_slugs)
        extra_slugs = sorted(section_slugs - required_slugs)
        print(
            "schema authoring reference section mismatch; missing: "
            + (", ".join(missing_slugs) or "none")
            + "; extra: "
            + (", ".join(extra_slugs) or "none")
        )
        return 1
    minimal = payload.get("minimal_starting_point", {})
    for field in ("company", "ticker", "as_of", "data_cutoff", "notes", "kpis", "catalysts"):
        if field not in minimal:
            print(f"schema authoring reference minimal starting point missing field: {field}")
            return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Schema Authoring Reference",
        "Top-Level Fields",
        "Source Attribution Fields",
        "Minimal Starting Point",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("schema authoring reference markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets_result = subprocess.run(
        [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
        cwd=ROOT,
        env=ENV,
        text=True,
        capture_output=True,
        check=False,
    )
    if release_assets_result.returncode != 0:
        print("release assets command failed while checking agent workflow examples")
        if release_assets_result.stderr:
            print(release_assets_result.stderr)
        return 1
    release_assets = json.loads(release_assets_result.stdout)
    release_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    demo_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    for path in ("examples/output/schema_authoring_reference.md", "examples/output/schema_authoring_reference.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing schema authoring reference path: {path}")
            return 1
        if path not in release_manifest_paths:
            print(f"release manifest missing schema authoring reference path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing schema authoring reference path: {path}")
            return 1
    print("schema authoring reference passed")
    return 0


def check_examples_index() -> int:
    print("== examples index ==", flush=True)
    json_path = ROOT / "examples/output/examples_index.json"
    md_path = ROOT / "examples/output/examples_index.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing examples index artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "examples_index":
        print("examples index has unexpected artifact type")
        return 1
    summary = payload.get("summary", {})
    if summary.get("fixture_count") != 7 or summary.get("template_count") != 3:
        print("examples index has unexpected fixture or template count")
        return 1
    if summary.get("generated_output_count", 0) < 5:
        print("examples index has too few generated outputs")
        return 1
    if payload.get("recommended_next_command") != "earnings-call-risk-map demo --out-dir examples/output":
        print("examples index has unexpected recommended next command")
        return 1
    for section in ("fixtures", "templates", "generated_outputs"):
        if not payload.get(section) or not all(item.get("recommended_next_command") for item in payload[section]):
            print(f"examples index missing recommended command metadata in {section}")
            return 1

    generated_paths = {item.get("path") for item in payload.get("generated_outputs", [])}
    required_generated_paths = {
        "examples/output/demo_report.md",
        "examples/output/examples_index.md",
        "examples/output/examples_index.json",
        "examples/output/template_catalog.md",
        "examples/output/template_catalog.json",
    }
    if not required_generated_paths.issubset(generated_paths):
        print("examples index missing generated output path(s): " + ", ".join(sorted(required_generated_paths - generated_paths)))
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Examples Index",
        "Bundled Fixtures",
        "Templates",
        "Generated Outputs",
        "Recommended next command",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("examples index markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    for path in ("examples/output/examples_index.md", "examples/output/examples_index.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing examples index path: {path}")
            return 1

    manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    for path in ("examples/output/examples_index.md", "examples/output/examples_index.json"):
        if path not in manifest_paths:
            print(f"release manifest missing examples index path: {path}")
            return 1
    print("examples index passed")
    return 0


def check_case_study_map() -> int:
    print("== case study map ==", flush=True)
    json_path = ROOT / "examples/output/case_study_map.json"
    md_path = ROOT / "examples/output/case_study_map.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing case study map artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "case_study_map" or payload.get("fixture_count") != 7:
        print("case study map has unexpected artifact type or fixture count")
        return 1
    required_fixtures = {
        "examples/input/demo_company.json",
        "examples/input/demo_company_prior.json",
        "examples/input/demo_energy_infrastructure.json",
        "examples/input/consumer_hardware.json",
        "examples/input/semiconductor_equipment.json",
        "examples/input/public_apple_static_case_study.json",
        "examples/input/sample_filled_template_workflow.json",
    }
    fixtures = {case_study.get("fixture") for case_study in payload.get("case_studies", [])}
    if fixtures != required_fixtures:
        missing_fixtures = sorted(required_fixtures - fixtures)
        extra_fixtures = sorted(fixtures - required_fixtures)
        print(
            "case study map fixture mismatch; missing: "
            + (", ".join(missing_fixtures) or "none")
            + "; extra: "
            + (", ".join(extra_fixtures) or "none")
        )
        return 1
    for case_study in payload.get("case_studies", []):
        fixture = case_study.get("fixture", "")
        if not (ROOT / fixture).is_file():
            print(f"case study map points at missing fixture: {fixture}")
            return 1
        if not case_study.get("target_sector") or not case_study.get("useful_question"):
            print(f"case study map fixture missing sector or question: {fixture}")
            return 1
        artifacts = case_study.get("generated_artifacts", [])
        if not artifacts:
            print(f"case study map fixture has no generated artifacts: {fixture}")
            return 1
        for artifact in artifacts:
            if not artifact.startswith("examples/output/") or not (ROOT / artifact).is_file():
                print(f"case study map points at missing generated artifact: {artifact}")
                return 1

    for artifact in payload.get("shared_generated_artifacts", []):
        if not artifact.startswith("examples/output/") or not (ROOT / artifact).is_file():
            print(f"case study map points at missing shared artifact: {artifact}")
            return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Case Study Map",
        "Fixture Map",
        "Shared Generated Artifacts",
        "examples/input/public_apple_static_case_study.json",
        "examples/output/case_study_map.json",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("case study map markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    for path in ("examples/output/case_study_map.md", "examples/output/case_study_map.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing case study map path: {path}")
            return 1

    manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    for path in ("examples/output/case_study_map.md", "examples/output/case_study_map.json"):
        if path not in manifest_paths:
            print(f"release manifest missing case study map path: {path}")
            return 1
    print("case study map passed")
    return 0


def check_publication_checklist() -> int:
    print("== publication checklist ==", flush=True)
    json_path = ROOT / "examples/output/publication_checklist.json"
    md_path = ROOT / "examples/output/publication_checklist.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing publication checklist artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "publication_checklist" or payload.get("step_count") != 7:
        print("publication checklist has unexpected artifact type or step count")
        return 1
    if payload.get("source_doc") != "docs/publication-checklist.md":
        print("publication checklist has unexpected source doc")
        return 1
    slugs = {step.get("slug") for step in payload.get("steps", [])}
    required_slugs = {
        "confirm-release-candidate",
        "run-smoke-checks",
        "run-privacy-scan",
        "check-public-skill-path",
        "create-and-push-tag",
        "create-github-release",
        "post-publish-smoke",
    }
    if slugs != required_slugs:
        missing_slugs = sorted(required_slugs - slugs)
        extra_slugs = sorted(slugs - required_slugs)
        print(
            "publication checklist slug mismatch; missing: "
            + (", ".join(missing_slugs) or "none")
            + "; extra: "
            + (", ".join(extra_slugs) or "none")
        )
        return 1
    for step in payload.get("steps", []):
        if not step.get("checks") or not step.get("commands"):
            print(f"publication checklist step missing checks or commands: {step.get('slug')}")
            return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Publication Checklist",
        "Confirm The Release Candidate",
        "Create The GitHub Release",
        "gh release create v0.9.3",
        "python scripts/privacy_scan.py",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("publication checklist markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    for path in ("examples/output/publication_checklist.md", "examples/output/publication_checklist.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing publication checklist path: {path}")
            return 1

    manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    for path in ("examples/output/publication_checklist.md", "examples/output/publication_checklist.json"):
        if path not in manifest_paths:
            print(f"release manifest missing publication checklist path: {path}")
            return 1
    print("publication checklist passed")
    return 0


def check_promotion_pack() -> int:
    print("== promotion pack ==", flush=True)
    json_path = ROOT / "examples/output/promotion_pack.json"
    md_path = ROOT / "examples/output/promotion_pack.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing promotion pack artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "promotion_pack" or payload.get("name") != "earnings-call-risk-map":
        print("promotion pack has unexpected artifact type or package name")
        return 1
    required_demo_paths = {
        "examples/output/public_apple_static_case_study_dashboard.html",
        "examples/output/demo_review_queue.md",
        "examples/output/demo_compare.md",
        "examples/output/public_apple_static_case_study_report.md",
        "examples/output/handoff_packet.md",
        "examples/output/case_study_map.md",
    }
    demo_paths = {demo.get("path") for demo in payload.get("demos", [])}
    if not required_demo_paths.issubset(demo_paths):
        print("promotion pack missing demo path(s): " + ", ".join(sorted(required_demo_paths - demo_paths)))
        return 1
    for path in demo_paths:
        if not path or not path.startswith("examples/output/") or not (ROOT / path).is_file():
            print(f"promotion pack points at missing demo artifact: {path}")
            return 1
    required_sources = {"README.md", "docs/promotion-page-outline.md", "examples/output/case_study_map.md"}
    if not required_sources.issubset(set(payload.get("source_evidence", []))):
        print("promotion pack missing source evidence path(s): " + ", ".join(sorted(required_sources - set(payload.get("source_evidence", [])))))
        return 1
    if "PYTHONPATH=src python scripts/selfcheck.py" not in payload.get("proof_commands", []):
        print("promotion pack missing selfcheck proof command")
        return 1
    if not any("No live market data" in boundary for boundary in payload.get("boundaries", [])):
        print("promotion pack missing public boundary language")
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Public Promotion Pack",
        "Quickstart",
        "Proof Commands",
        "examples/output/public_apple_static_case_study_dashboard.html",
        "docs/promotion-page-outline.md",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("promotion pack markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    demo_manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8")).get(
            "files", []
        )
    }
    for path in ("examples/output/promotion_pack.md", "examples/output/promotion_pack.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing promotion pack path: {path}")
            return 1
        if path not in manifest_paths:
            print(f"release manifest missing promotion pack path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing promotion pack path: {path}")
            return 1
    print("promotion pack passed")
    return 0


def check_data_entry_checklist() -> int:
    print("== data entry checklist ==", flush=True)
    json_path = ROOT / "examples/output/data_entry_checklist.json"
    md_path = ROOT / "examples/output/data_entry_checklist.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing data entry checklist artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "data_entry_checklist" or payload.get("section_count") != 4:
        print("data entry checklist has unexpected artifact type or section count")
        return 1
    if payload.get("source_doc") != "docs/data-entry-checklist.md":
        print("data entry checklist has unexpected source doc")
        return 1
    section_slugs = {section.get("slug") for section in payload.get("sections", [])}
    required_slugs = {"before-entry", "source-boundary-rules", "entry-steps", "final-review"}
    if section_slugs != required_slugs:
        missing_slugs = sorted(required_slugs - section_slugs)
        extra_slugs = sorted(section_slugs - required_slugs)
        print(
            "data entry checklist slug mismatch; missing: "
            + (", ".join(missing_slugs) or "none")
            + "; extra: "
            + (", ".join(extra_slugs) or "none")
        )
        return 1
    if not payload.get("field_mappings") or not payload.get("validation_commands"):
        print("data entry checklist is missing field mappings or validation commands")
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Data Entry Checklist",
        "Source Boundary Rules",
        "Do not invent source URLs",
        "Fixture field",
        "PYTHONPATH=src python -m earnings_call_risk_map analyze path/to/fixture.json",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("data entry checklist markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    for path in ("examples/output/data_entry_checklist.md", "examples/output/data_entry_checklist.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing data entry checklist path: {path}")
            return 1

    manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    demo_manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8")).get(
            "files", []
        )
    }
    for path in ("examples/output/data_entry_checklist.md", "examples/output/data_entry_checklist.json"):
        if path not in manifest_paths:
            print(f"release manifest missing data entry checklist path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing data entry checklist path: {path}")
            return 1
    print("data entry checklist passed")
    return 0


def check_demo_screenshot_guide() -> int:
    print("== demo screenshot guide ==", flush=True)
    json_path = ROOT / "examples/output/demo_screenshot_guide.json"
    md_path = ROOT / "examples/output/demo_screenshot_guide.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing demo screenshot guide artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "demo_screenshot_guide":
        print("demo screenshot guide has unexpected artifact type")
        return 1
    if payload.get("source_doc") != "docs/demo-screenshot-guide.md":
        print("demo screenshot guide has unexpected source doc")
        return 1
    required_targets = {
        "examples/output/public_apple_static_case_study_dashboard.html",
        "examples/output/demo_dashboard.html",
        "docs/assets/showcase-dashboard-preview.svg",
        "examples/output/showcase_dashboard_preview.svg",
        "docs/demo-index.html",
    }
    target_paths = {target.get("path") for target in payload.get("best_screenshot_targets", [])}
    if not required_targets.issubset(target_paths):
        print("demo screenshot guide missing target path(s): " + ", ".join(sorted(required_targets - target_paths)))
        return 1
    for path in target_paths:
        if not path or not (ROOT / path).is_file():
            print(f"demo screenshot guide points at missing target: {path}")
            return 1
    if not payload.get("good_readme_visuals") or not payload.get("boundaries"):
        print("demo screenshot guide missing visual guidance or boundaries")
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Demo Screenshot Guide",
        "Best Screenshot Targets",
        "examples/output/public_apple_static_case_study_dashboard.html",
        "docs/assets/showcase-dashboard-preview.svg",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("demo screenshot guide markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    release_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    demo_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    for path in ("examples/output/demo_screenshot_guide.md", "examples/output/demo_screenshot_guide.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing demo screenshot guide path: {path}")
            return 1
        if path not in release_manifest_paths:
            print(f"release manifest missing demo screenshot guide path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing demo screenshot guide path: {path}")
            return 1
    print("demo screenshot guide passed")
    return 0


def check_visual_evidence_receipt() -> int:
    print("== visual evidence receipt ==", flush=True)
    json_path = ROOT / "examples/output/visual_evidence_receipt.json"
    md_path = ROOT / "examples/output/visual_evidence_receipt.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing visual evidence receipt artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "visual_evidence_receipt":
        print("visual evidence receipt has unexpected artifact type")
        return 1
    checks = payload.get("checks", {})
    for check in (
        "all_screenshot_targets_exist",
        "primary_target_exists",
        "primary_target_has_required_markers",
        "all_visual_targets_public_safe",
        "source_attribution_referenced",
        "stale_or_static_warning_referenced",
        "public_source_fixture_limits_recorded",
        "no_live_data_boundary_recorded",
        "no_broker_boundary_recorded",
        "no_personalized_advice_boundary_recorded",
    ):
        if checks.get(check) is not True:
            print(f"visual evidence receipt failed check: {check}")
            return 1
    primary = payload.get("primary_screenshot_target", {})
    if primary.get("path") != "examples/output/public_apple_static_case_study_dashboard.html":
        print("visual evidence receipt has unexpected primary screenshot target")
        return 1
    if primary.get("blocked_markers_found") or not primary.get("has_required_markers"):
        print("visual evidence receipt primary target is missing markers or has blocked markers")
        return 1
    fixture_paths = {fixture.get("path") for fixture in payload.get("public_source_fixtures", [])}
    required_fixture_paths = {
        "examples/input/consumer_hardware.json",
        "examples/input/semiconductor_equipment.json",
        "examples/input/public_apple_static_case_study.json",
    }
    if fixture_paths != required_fixture_paths:
        print("visual evidence receipt public-source fixture path mismatch")
        return 1
    if "broker" not in payload.get("no_broker_claim", "").lower():
        print("visual evidence receipt missing no-broker claim")
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Visual Evidence Receipt",
        "Screenshot Evidence Checklist",
        "Public-Source Fixture Limits",
        "Source Boundaries",
        "No live data",
        "No broker",
        "No personalized investment, legal, accounting, tax, buy, sell, or hold advice",
        "examples/output/public_apple_static_case_study_dashboard.html",
        "examples/input/public_apple_static_case_study.json",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("visual evidence receipt markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    release_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    demo_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    for path in ("examples/output/visual_evidence_receipt.md", "examples/output/visual_evidence_receipt.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing visual evidence receipt path: {path}")
            return 1
        if path not in release_manifest_paths:
            print(f"release manifest missing visual evidence receipt path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing visual evidence receipt path: {path}")
            return 1
    print("visual evidence receipt passed")
    return 0


def check_command_cheat_sheet() -> int:
    print("== command cheat sheet ==", flush=True)
    json_path = ROOT / "examples/output/command_cheat_sheet.json"
    md_path = ROOT / "examples/output/command_cheat_sheet.md"
    alias_json_path = ROOT / "examples/output/command_cheatsheet.json"
    alias_md_path = ROOT / "examples/output/command_cheatsheet.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path, alias_json_path, alias_md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing command cheat sheet artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    alias_payload = json.loads(alias_json_path.read_text(encoding="utf-8"))
    if alias_payload != payload:
        print("command cheatsheet alias JSON does not match canonical artifact")
        return 1
    if payload.get("artifact_type") != "command_cheat_sheet":
        print("command cheat sheet has unexpected artifact type")
        return 1
    commands = payload.get("commands", [])
    command_names = {item.get("command") for item in commands}
    required_commands = {
        "agent-workflow",
        "analyze",
        "audit",
        "case-study-map",
        "cheat-sheet",
        "compare",
        "data-entry-checklist",
        "demo",
        "demo-screenshot-guide",
        "doctor",
        "examples-index",
        "fixture-summary",
        "fixture-catalog",
        "fresh-clone-plan",
        "handoff-packet",
        "manifest",
        "maturity-evidence",
        "playbooks",
        "promotion-pack",
        "publication-checklist",
        "release-owner-handoff",
        "release-assets",
        "release-notes",
        "review-queue",
        "review-queue-jsonl",
        "risk-taxonomy",
        "schema-authoring-reference",
        "schema-reference",
        "source-boundary-evidence",
        "template-catalog",
        "version",
        "visual-evidence-receipt",
    }
    if command_names != required_commands or payload.get("command_count") != len(required_commands):
        missing = sorted(required_commands - command_names)
        extra = sorted(command_names - required_commands)
        print(
            "command cheat sheet command mismatch; missing: "
            + (", ".join(missing) or "none")
            + "; extra: "
            + (", ".join(extra) or "none")
        )
        return 1
    for item in commands:
        if not item.get("purpose"):
            print(f"{item.get('command')} is missing a short purpose")
            return 1

    markdown = md_path.read_text(encoding="utf-8")
    if alias_md_path.read_text(encoding="utf-8") != markdown:
        print("command cheatsheet alias Markdown does not match canonical artifact")
        return 1
    required_markers = (
        "Command Cheat Sheet",
        "| Command | Purpose |",
        "`agent-workflow`",
        "Render generic agent workflow instructions as Markdown or JSON",
        "`analyze`",
        "`cheat-sheet`",
        "Print lightweight command cheat sheet as Markdown or JSON",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("command cheat sheet markdown missing marker(s): " + ", ".join(missing_markers))
        return 1
    print("command cheat sheet passed")
    return 0


def check_agent_workflow_examples() -> int:
    print("== agent workflow examples ==", flush=True)
    json_path = ROOT / "examples/output/agent_workflow.json"
    md_path = ROOT / "examples/output/agent_workflow.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing agent workflow artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "agent_workflow":
        print("agent workflow JSON has unexpected artifact type")
        return 1
    if payload.get("source_doc") != "docs/agent-workflow.md":
        print("agent workflow JSON has unexpected source doc")
        return 1
    route_slugs = {route.get("slug") for route in payload.get("routes", [])}
    required_routes = {"analyze", "compare", "review-queue", "source-attribution"}
    if route_slugs != required_routes:
        missing_routes = sorted(required_routes - route_slugs)
        extra_routes = sorted(route_slugs - required_routes)
        print(
            "agent workflow route mismatch; missing: "
            + (", ".join(missing_routes) or "none")
            + "; extra: "
            + (", ".join(extra_routes) or "none")
        )
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Agent Workflow",
        "Analyze Route",
        "Review Queue Route",
        "Source Attribution Route",
        "Educational research review only",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("agent workflow markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    release_manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8")).get("files", [])
    }
    demo_manifest_paths = {
        item.get("path")
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8")).get(
            "files", []
        )
    }
    for path in ("examples/output/agent_workflow.md", "examples/output/agent_workflow.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing agent workflow path: {path}")
            return 1
        if path not in release_manifest_paths:
            print(f"release manifest missing agent workflow path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing agent workflow path: {path}")
            return 1
    print("agent workflow examples passed")
    return 0


def check_fresh_clone_plan() -> int:
    print("== fresh clone plan ==", flush=True)
    json_path = ROOT / "examples/output/fresh_clone_plan.json"
    md_path = ROOT / "examples/output/fresh_clone_plan.md"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path)
        if not path.is_file()
    ]
    if missing:
        print("missing fresh clone plan artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("artifact_type") != "fresh_clone_verification_plan":
        print("fresh clone plan has unexpected artifact type")
        return 1
    if payload.get("source_doc") != "docs/fresh-clone-verification.md":
        print("fresh clone plan has unexpected source doc")
        return 1
    commands = payload.get("commands", [])
    required_commands = (
        "git clone <repo-url> earnings-call-risk-map",
        "earnings-call-risk-map demo --out-dir verification/fresh-clone/demo",
        "earnings-call-risk-map audit --format json --out verification/fresh-clone/package_audit.json",
    )
    missing_commands = [command for command in required_commands if command not in commands]
    if missing_commands:
        print("fresh clone plan missing command(s): " + ", ".join(missing_commands))
        return 1
    direct_artifacts = payload.get("expected_generated_artifacts", {}).get("direct", [])
    if "verification/fresh-clone/demo_company_snapshot.json" not in direct_artifacts:
        print("fresh clone plan missing expected direct artifact")
        return 1
    if not payload.get("json_check_commands"):
        print("fresh clone plan missing JSON check commands")
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required_markers = (
        "Fresh Clone Verification Plan",
        "git clone <repo-url> earnings-call-risk-map",
        "verification/fresh-clone/demo_company_snapshot.json",
    )
    missing_markers = [marker for marker in required_markers if marker not in markdown]
    if missing_markers:
        print("fresh clone plan markdown missing marker(s): " + ", ".join(missing_markers))
        return 1

    release_assets = json.loads(
        subprocess.run(
            [sys.executable, "-m", "earnings_call_risk_map", "release-assets"],
            cwd=ROOT,
            env=ENV,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    for path in ("examples/output/fresh_clone_plan.md", "examples/output/fresh_clone_plan.json"):
        if path not in release_assets.get("expected_assets", []):
            print(f"release assets missing fresh clone plan path: {path}")
            return 1

    release_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    demo_manifest_paths = {
        item["path"]
        for item in json.loads((ROOT / "examples/output/release_manifest.json").read_text(encoding="utf-8"))["files"]
    }
    for path in ("examples/output/fresh_clone_plan.md", "examples/output/fresh_clone_plan.json"):
        if path not in release_manifest_paths:
            print(f"release manifest missing fresh clone plan path: {path}")
            return 1
        if path not in demo_manifest_paths:
            print(f"demo release manifest missing fresh clone plan path: {path}")
            return 1
    print("fresh clone plan passed")
    return 0


def check_doctor_report() -> int:
    print("== doctor report ==", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "earnings_call_risk_map", "doctor", "--format", "json"],
        cwd=ROOT,
        env=ENV,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print("doctor command failed")
        if result.stderr:
            print(result.stderr)
        return 1
    payload = json.loads(result.stdout)
    if payload.get("artifact_type") != "doctor_report" or payload.get("status") != "passed":
        print("doctor report has unexpected type or status")
        return 1
    if payload.get("fixture_count") != 7 or payload.get("output_artifact_count", 0) < 5:
        print("doctor report has unexpected fixture or output count")
        return 1
    if payload.get("docs_links", {}).get("status") != "passed":
        print("doctor report docs link check did not pass")
        return 1
    if not payload.get("workflow_files_absent"):
        print("doctor report expected workflow files to be absent")
        return 1
    if "python scripts/privacy_scan.py" not in payload.get("privacy_scan_command_hints", []):
        print("doctor report missing privacy scan command hint")
        return 1
    print("doctor report passed")
    return 0


def _is_external_or_anchor(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
    )


def main() -> int:
    checks = [
        ("unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
        ("demo", [sys.executable, "-m", "earnings_call_risk_map", "demo", "--out-dir", "examples/output"]),
        ("audit", [sys.executable, "-m", "earnings_call_risk_map", "audit"]),
        ("doctor", [sys.executable, "-m", "earnings_call_risk_map", "doctor"]),
        ("release assets", [sys.executable, "-m", "earnings_call_risk_map", "release-assets"]),
        ("manifest", [sys.executable, "-m", "earnings_call_risk_map", "manifest", "--out", "release_manifest.json"]),
        ("privacy scan", [sys.executable, "scripts/privacy_scan.py"]),
        ("maturity evidence", [sys.executable, "-m", "earnings_call_risk_map", "maturity-evidence", "--out-dir", "reports/maturity"]),
    ]
    for label, command in checks:
        code = run(label, command)
        if code:
            return code
        if label == "demo":
            code = check_demo_dashboard()
            if code:
                return code
            code = check_showcase_previews()
            if code:
                return code
            code = check_semiconductor_equipment_report_bundle()
            if code:
                return code
            code = check_integration_examples()
            if code:
                return code
            code = check_compare_examples()
            if code:
                return code
            code = check_review_queue_jsonl()
            if code:
                return code
            code = check_source_boundary_evidence()
            if code:
                return code
            code = check_required_docs()
            if code:
                return code
            code = check_playbooks()
            if code:
                return code
            code = check_playbook_output_examples()
            if code:
                return code
            code = check_handoff_packet_examples()
            if code:
                return code
            code = check_template_catalog()
            if code:
                return code
            code = check_schema_authoring_reference()
            if code:
                return code
            code = check_examples_index()
            if code:
                return code
            code = check_case_study_map()
            if code:
                return code
            code = check_publication_checklist()
            if code:
                return code
            code = check_promotion_pack()
            if code:
                return code
            code = check_data_entry_checklist()
            if code:
                return code
            code = check_demo_screenshot_guide()
            if code:
                return code
            code = check_visual_evidence_receipt()
            if code:
                return code
            code = check_fresh_clone_plan()
            if code:
                return code
            code = check_agent_workflow_examples()
            if code:
                return code
            code = check_command_cheat_sheet()
            if code:
                return code
            code = check_docs_links()
            if code:
                return code
            code = check_doctor_report()
            if code:
                return code
    print("selfcheck passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
