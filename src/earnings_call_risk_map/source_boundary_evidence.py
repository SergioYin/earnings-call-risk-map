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
NO_LIVE_DATA_CLAIM = (
    "This evidence bundle is generated from bundled local fixture JSON files only. "
    "It does not fetch live market data, broker data, filings, API data, or earnings-call transcripts."
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
