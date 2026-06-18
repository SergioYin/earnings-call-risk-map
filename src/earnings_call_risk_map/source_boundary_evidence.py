"""Source-boundary evidence bundle generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .fixture_catalog import build_fixture_catalog
from .io import read_json
from .models import SAFETY_NOTICE, SOURCE_BOUNDARIES
from .version import __version__

SOURCE_DOCS = (
    "docs/reviewer-evidence.md",
    "docs/non-advice-boundary.md",
    "docs/security-and-privacy.md",
    "docs/source-attribution-guide.md",
    "docs/fixture-catalog.md",
)
GENERATED_ARTIFACTS = (
    "examples/output/source_boundary_evidence.md",
    "examples/output/source_boundary_evidence.json",
    "examples/output/fixture_catalog.md",
    "examples/output/demo_review_queue_items.jsonl",
    "examples/output/handoff_packet.md",
    "examples/output/handoff_packet.json",
)
WALKTHROUGH_ARTIFACTS = (
    "examples/output/fixture_catalog.md",
    "examples/output/source_boundary_evidence.md",
    "examples/output/source_boundary_evidence.json",
    "examples/output/demo_review_queue_items.jsonl",
    "examples/output/handoff_packet.md",
    "examples/output/handoff_packet.json",
    "examples/output/release_manifest.json",
    "release_manifest.json",
)
NO_LIVE_DATA_CLAIM = (
    "This evidence bundle is generated from bundled local fixture JSON files only. "
    "It does not fetch live market data, broker data, filings, API data, or earnings-call transcripts."
)
WALKTHROUGH_STEPS = (
    {
        "step": "Verify bundled static fixtures",
        "reviewer_action": (
            "Open each examples/input/*.json fixture listed in this receipt and confirm company, ticker, as_of, "
            "data_cutoff, source attribution, evidence URLs, and static notices are checked-in metadata."
        ),
        "evidence_paths": ("examples/input/*.json", "examples/output/fixture_catalog.md"),
        "boundary": "Fixtures are static local examples; runtime generation does not fetch transcripts or live data.",
    },
    {
        "step": "Verify source-boundary separation",
        "reviewer_action": (
            "Confirm management_claim, analyst_question, user_synthesis, source_type, accessed_at, and stale badge "
            "language stay visible in generated reports and review queues."
        ),
        "evidence_paths": (
            "docs/source-attribution-guide.md",
            "examples/output/source_boundary_evidence.md",
            "examples/output/demo_review_queue_items.jsonl",
        ),
        "boundary": "Source labels describe provenance and review posture; they are not source verification.",
    },
    {
        "step": "Verify dashboard and release-owner handoff",
        "reviewer_action": (
            "Open the generated dashboard/report paths and handoff packet, then confirm downstream owners receive "
            "local artifact paths, review queues, and cautions rather than portfolio actions."
        ),
        "evidence_paths": (
            "docs/release-owner-handoff.md",
            "examples/output/handoff_packet.md",
            "examples/output/handoff_packet.json",
            "examples/output/public_apple_static_case_study_dashboard.html",
        ),
        "boundary": "Dashboard and handoff artifacts are static local outputs for reviewer workflow ownership.",
    },
    {
        "step": "Verify no-live-data and no-advice boundaries",
        "reviewer_action": (
            "Check the safety notice, no-live-data claim, release manifest, and privacy/security docs before treating "
            "any fixture as a public demo or review handoff."
        ),
        "evidence_paths": (
            "docs/non-advice-boundary.md",
            "docs/security-and-privacy.md",
            "examples/output/source_boundary_evidence.json",
            "release_manifest.json",
        ),
        "boundary": "Outputs are educational review prompts, not current analysis or buy, sell, or hold advice.",
    },
)


def build_source_boundary_evidence(root: str | Path = ".") -> dict[str, Any]:
    """Build deterministic reviewer evidence for bundled fixture source boundaries."""

    base = Path(root)
    fixture_entries = []
    for fixture in build_fixture_catalog(base):
        path = Path(fixture["path"])
        data = read_json(base / path)
        source_records = _source_records(data)
        evidence_urls = _evidence_urls(data)
        fixture_entries.append(
            {
                "slug": fixture["slug"],
                "path": fixture["path"],
                "exists": (base / path).is_file(),
                "company": fixture["company"],
                "ticker": fixture["ticker"],
                "as_of": fixture["as_of"],
                "data_cutoff": fixture["data_cutoff"],
                "static_live_status": fixture["static_live_status"],
                "source_record_count": len(source_records),
                "source_url_count": len([record for record in source_records if record.get("source_url")]),
                "evidence_url_count": len(evidence_urls),
                "source_types": sorted(
                    {str(record.get("source_type")) for record in source_records if record.get("source_type")}
                ),
                "source_domains": sorted({_url_domain(url) for url in _source_urls(source_records, evidence_urls)}),
                "static_notice_count": len([record for record in source_records if record.get("static_notice")]),
                "has_private_path": _contains_private_path(data),
                "fixture_boundary": _fixture_boundary_status(fixture["static_live_status"]),
                "freshness_boundary": (
                    "review freshness before reuse; static fixture dates are evidence metadata, not current analysis"
                ),
            }
        )

    return {
        "artifact_type": "source_boundary_evidence",
        "schema_version": "0.1",
        "tool_version": __version__,
        "safety_notice": SAFETY_NOTICE,
        "source_boundaries": SOURCE_BOUNDARIES,
        "no_live_data_claim": NO_LIVE_DATA_CLAIM,
        "no_advice_claim": SAFETY_NOTICE,
        "reviewer_handoff_claim": (
            "Cold reviewers can verify fixture existence, source metadata, static boundaries, and generated handoff "
            "artifacts from repository files without broker/API credentials or private paths."
        ),
        "source_docs": list(SOURCE_DOCS),
        "generated_artifacts": list(GENERATED_ARTIFACTS),
        "fixture_count": len(fixture_entries),
        "fixtures": fixture_entries,
        "walkthrough_receipt": _build_walkthrough_receipt(base, fixture_entries),
        "checks": {
            "all_fixture_paths_exist": all(item["exists"] for item in fixture_entries),
            "all_fixtures_are_static_or_local": all(
                item["fixture_boundary"] in {"static_fixture", "static_public_source_fixture", "static_compare_baseline"}
                for item in fixture_entries
            ),
            "no_private_paths_found": not any(item["has_private_path"] for item in fixture_entries),
            "no_live_fetching_required": True,
            "no_broker_or_api_credentials_required": True,
            "no_advice_claim_present": "buy, sell, or hold advice" in SAFETY_NOTICE,
            "walkthrough_receipt_present": True,
        },
    }


def source_boundary_evidence_json(root: str | Path = ".") -> str:
    return json.dumps(build_source_boundary_evidence(root), indent=2, sort_keys=True) + "\n"


def source_boundary_evidence_markdown(root: str | Path = ".") -> str:
    return render_source_boundary_evidence_markdown(build_source_boundary_evidence(root))


def render_source_boundary_evidence_markdown(evidence: dict[str, Any]) -> str:
    lines = [
        "# Source Boundary Evidence",
        "",
        f"- Tool version: `{evidence['tool_version']}`",
        f"- Fixture count: {evidence['fixture_count']}",
        "",
        f"> {evidence['safety_notice']}",
        "",
        "## Boundary Claims",
        "",
        f"- No live data: {evidence['no_live_data_claim']}",
        f"- No advice: {evidence['no_advice_claim']}",
        f"- Reviewer handoff: {evidence['reviewer_handoff_claim']}",
        "",
        "## Checks",
        "",
    ]
    lines.extend(f"- {key.replace('_', ' ').title()}: `{value}`" for key, value in evidence["checks"].items())
    lines.extend(
        [
            "",
            "## Fixture Evidence",
            "",
            "| Fixture | Ticker | Cutoff | Boundary | Source domains | Static notices | Private path |",
            "| --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for fixture in evidence["fixtures"]:
        domains = ", ".join(fixture["source_domains"]) if fixture["source_domains"] else "none recorded"
        lines.append(
            f"| {_markdown_table_cell(fixture['path'])} | {_markdown_table_cell(fixture['ticker'])} | "
            f"{_markdown_table_cell(fixture['data_cutoff'])} | "
            f"{_markdown_table_cell(fixture['fixture_boundary'])} | {_markdown_table_cell(domains)} | "
            f"{_markdown_table_cell(fixture['static_notice_count'])} | "
            f"{_markdown_table_cell(fixture['has_private_path'])} |"
        )
    receipt = evidence["walkthrough_receipt"]
    lines.extend(
        [
            "",
            "## Walkthrough Receipt",
            "",
            f"- Receipt type: `{receipt['receipt_type']}`",
            f"- Scope: {receipt['scope']}",
            f"- Public-source fixture count: {receipt['public_source_fixture_count']}",
            f"- Fixture-scoped public-source demo receipts: {receipt.get('public_source_demo_receipt_count', 0)}",
            f"- Static/local fixture count: {receipt['static_or_local_fixture_count']}",
            f"- Missing receipt artifacts: {receipt['missing_artifact_count']}",
            "",
            "### Receipt Checks",
            "",
        ]
    )
    lines.extend(f"- {key.replace('_', ' ').title()}: `{value}`" for key, value in receipt["checks"].items())
    lines.extend(["", "### Reviewer Walkthrough", ""])
    for index, step in enumerate(receipt["steps"], start=1):
        lines.extend(
            [
                f"{index}. {step['step']}",
                f"   - Reviewer action: {step['reviewer_action']}",
                f"   - Boundary: {step['boundary']}",
                f"   - Evidence paths: {', '.join(f'`{path}`' for path in step['evidence_paths'])}",
            ]
        )
    if receipt.get("public_source_demo_receipts"):
        lines.extend(
            [
                "",
                "### Fixture-Scoped Public-Source Demo Receipts",
                "",
                "| Fixture | Ticker | Demo artifacts | Missing | Local-only |",
                "| --- | --- | ---: | ---: | --- |",
            ]
        )
        for demo_receipt in receipt["public_source_demo_receipts"]:
            lines.append(
                f"| {_markdown_table_cell(demo_receipt['fixture_path'])} | "
                f"{_markdown_table_cell(demo_receipt['ticker'])} | "
                f"{len(demo_receipt['demo_artifact_status'])} | "
                f"{demo_receipt['missing_demo_artifact_count']} | "
                f"{_markdown_table_cell(demo_receipt['checks']['local_only_demo_scope'])} |"
            )
        lines.extend(["", "#### Demo Receipt Artifact Paths", ""])
        for demo_receipt in receipt["public_source_demo_receipts"]:
            lines.extend(
                [
                    f"- `{demo_receipt['fixture_slug']}`:",
                    *[
                        f"  - `{artifact['path']}` ({artifact['role']}; exists: `{artifact['exists']}`)"
                        for artifact in demo_receipt["demo_artifact_status"]
                    ],
                ]
            )
    lines.extend(["", "## Source Boundaries", ""])
    lines.extend(f"- {key.replace('_', ' ').title()}: {value}" for key, value in evidence["source_boundaries"].items())
    lines.extend(["", "## Reviewer Artifact Paths", ""])
    lines.extend(f"- `{path}`" for path in evidence["generated_artifacts"])
    lines.extend(["", "## Source Docs", ""])
    lines.extend(f"- `{path}`" for path in evidence["source_docs"])
    return "\n".join(lines) + "\n"


def _fixture_boundary_status(status: str) -> str:
    if "compare baseline" in status:
        return "static_compare_baseline"
    if "public-source" in status or "public-source" in status.replace(" ", "-"):
        return "static_public_source_fixture"
    return "static_fixture"


def _build_walkthrough_receipt(base: Path, fixture_entries: list[dict[str, Any]]) -> dict[str, Any]:
    artifact_status = [
        {"path": path, "exists": (base / path).is_file(), "role": _artifact_role(path)}
        for path in WALKTHROUGH_ARTIFACTS
    ]
    public_fixture_paths = [
        fixture["path"]
        for fixture in fixture_entries
        if fixture["fixture_boundary"] == "static_public_source_fixture"
    ]
    public_source_demo_receipts = [
        _build_public_source_demo_receipt(base, fixture)
        for fixture in fixture_entries
        if fixture["fixture_boundary"] == "static_public_source_fixture"
    ]
    return {
        "receipt_type": "public_source_boundary_walkthrough",
        "scope": (
            "cold reviewer verification of checked-in static fixtures, public-source metadata, dashboard and "
            "release-owner handoff artifacts, and no-live-data/no-advice boundaries"
        ),
        "public_source_fixture_count": len(public_fixture_paths),
        "public_source_fixture_paths": public_fixture_paths,
        "public_source_demo_receipt_count": len(public_source_demo_receipts),
        "public_source_demo_receipts": public_source_demo_receipts,
        "static_or_local_fixture_count": len(
            [
                fixture
                for fixture in fixture_entries
                if fixture["fixture_boundary"]
                in {"static_fixture", "static_public_source_fixture", "static_compare_baseline"}
            ]
        ),
        "artifact_status": artifact_status,
        "missing_artifact_count": len([artifact for artifact in artifact_status if not artifact["exists"]]),
        "steps": [
            {
                "step": step["step"],
                "reviewer_action": step["reviewer_action"],
                "evidence_paths": list(step["evidence_paths"]),
                "boundary": step["boundary"],
            }
            for step in WALKTHROUGH_STEPS
        ],
        "checks": {
            "public_source_fixtures_present": bool(public_fixture_paths),
            "all_public_source_demo_receipts_present": len(public_source_demo_receipts) == len(public_fixture_paths),
            "all_public_source_demo_receipt_artifacts_exist": all(
                receipt["checks"]["all_demo_artifacts_exist"] for receipt in public_source_demo_receipts
            ),
            "all_receipt_artifacts_exist": all(artifact["exists"] for artifact in artifact_status),
            "all_fixture_boundaries_static_or_local": all(
                fixture["fixture_boundary"]
                in {"static_fixture", "static_public_source_fixture", "static_compare_baseline"}
                for fixture in fixture_entries
            ),
            "dashboard_handoff_paths_recorded": any(
                artifact["path"] == "examples/output/handoff_packet.md" and artifact["exists"]
                for artifact in artifact_status
            ),
            "no_live_data_boundary_recorded": True,
            "no_advice_boundary_recorded": "buy, sell, or hold advice" in SAFETY_NOTICE,
        },
    }


def _build_public_source_demo_receipt(base: Path, fixture: dict[str, Any]) -> dict[str, Any]:
    artifact_paths = _public_source_demo_artifact_paths(fixture["slug"])
    artifact_status = [
        {"path": path, "exists": (base / path).is_file(), "role": _public_source_demo_artifact_role(path)}
        for path in artifact_paths
    ]
    return {
        "receipt_type": "fixture_scoped_public_source_demo",
        "fixture_slug": fixture["slug"],
        "fixture_path": fixture["path"],
        "company": fixture["company"],
        "ticker": fixture["ticker"],
        "data_cutoff": fixture["data_cutoff"],
        "scope": "local-only deterministic demo artifacts generated from this checked-in public-source fixture",
        "demo_artifact_status": artifact_status,
        "missing_demo_artifact_count": len([artifact for artifact in artifact_status if not artifact["exists"]]),
        "checks": {
            "fixture_exists": fixture["exists"],
            "fixture_is_public_source": fixture["fixture_boundary"] == "static_public_source_fixture",
            "source_metadata_present": fixture["source_record_count"] > 0,
            "source_urls_recorded": fixture["source_url_count"] > 0,
            "static_notices_recorded": fixture["static_notice_count"] > 0,
            "all_demo_artifacts_exist": all(artifact["exists"] for artifact in artifact_status),
            "local_only_demo_scope": True,
            "no_live_data_boundary_recorded": True,
            "no_advice_boundary_recorded": "buy, sell, or hold advice" in SAFETY_NOTICE,
        },
    }


def _public_source_demo_artifact_paths(slug: str) -> list[str]:
    return [
        f"examples/output/{slug}_snapshot.json",
        f"examples/output/{slug}_report.md",
        f"examples/output/{slug}_dashboard.html",
        f"examples/output/{slug}_review_queue.json",
        f"examples/output/{slug}_review_queue.md",
    ]


def _public_source_demo_artifact_role(path: str) -> str:
    if path.endswith("_snapshot.json"):
        return "deterministic analysis snapshot"
    if path.endswith("_report.md"):
        return "local Markdown report"
    if path.endswith("_dashboard.html"):
        return "self-contained static dashboard"
    if path.endswith("_review_queue.json"):
        return "review queue data"
    if path.endswith("_review_queue.md"):
        return "review queue handoff"
    return "public-source demo artifact"


def _artifact_role(path: str) -> str:
    if "fixture_catalog" in path:
        return "fixture inventory"
    if "source_boundary_evidence" in path:
        return "source boundary receipt"
    if "review_queue" in path:
        return "review queue handoff"
    if "handoff_packet" in path:
        return "dashboard/release-owner handoff"
    if "manifest" in path:
        return "release file receipt"
    return "review artifact"


def _markdown_table_cell(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _source_records(data: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    records.extend(_normalize_source_attribution(data.get("source_attribution")))
    for collection in ("notes", "kpis", "catalysts"):
        for item in data.get(collection, []):
            if isinstance(item, dict):
                records.extend(_normalize_source_attribution(item.get("source_attribution")))
    return records


def _evidence_urls(data: dict[str, Any]) -> list[str]:
    urls = []
    for collection in ("notes", "kpis", "catalysts"):
        for item in data.get(collection, []):
            if isinstance(item, dict) and item.get("evidence_url"):
                urls.append(str(item["evidence_url"]))
    return urls


def _source_urls(source_records: list[dict[str, Any]], evidence_urls: list[str]) -> list[str]:
    urls = [str(record["source_url"]) for record in source_records if record.get("source_url")]
    urls.extend(evidence_urls)
    return urls


def _url_domain(url: str) -> str:
    if "://" not in url:
        return "unparsed"
    remainder = url.split("://", 1)[1]
    return remainder.split("/", 1)[0] or "unparsed"


def _contains_private_path(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_private_path(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_private_path(item) for item in value)
    if not isinstance(value, str):
        return False
    return any(marker in value for marker in ("/home/", "/Users/", "\\Users\\", "file://", "C:\\"))


def _normalize_source_attribution(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []
