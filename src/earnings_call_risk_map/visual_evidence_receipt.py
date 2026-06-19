"""Public demo visual evidence receipt generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .demo_screenshot_guide import BEST_SCREENSHOT_TARGETS
from .models import SAFETY_NOTICE, SOURCE_BOUNDARIES
from .source_boundary_evidence import NO_LIVE_DATA_CLAIM, build_source_boundary_evidence
from .version import __version__

PUBLIC_SOURCE_FIXTURE_LIMIT = (
    "Public-source fixtures are checked-in static examples with source attribution metadata. They are limited to "
    "repository evidence and must not be presented as current market data, verified transcript coverage, broker "
    "data, or personalized investment, legal, accounting, tax, buy, sell, or hold advice."
)
NO_PERSONALIZED_ADVICE_CLAIM = (
    "No personalized investment, legal, accounting, tax, buy, sell, or hold advice is provided."
)
SCREENSHOT_REVIEW_BOUNDARIES = (
    "Keep visible source attribution, source-boundary labels, or stale/static warnings in the screenshot crop.",
    "Use checked-in static HTML, Markdown, or SVG artifacts only; do not imply live dashboards or monitoring.",
    "Do not include browser profiles, private paths, account names, credentials, portfolio holdings, or secrets.",
    "Do not add price targets, ratings, recommendations, or buy/sell/hold language to screenshot captions.",
)
REQUIRED_PUBLIC_SAFE_MARKERS = (
    "Educational research review only",
    "Source Attribution",
    "Static educational case study",
)
BLOCKED_VISUAL_MARKERS = (
    "<script",
    "<link",
    "<img",
    " src=",
    "xlink:href=",
    "url(http://",
    "url(https://",
    "/home/",
    "/Users/",
    "\\Users\\",
    "file://",
    "C:\\",
)


def build_visual_evidence_receipt(root: str | Path = ".") -> dict[str, Any]:
    """Build a deterministic screenshot-review receipt from local public artifacts."""

    base = Path(root)
    source_evidence = build_source_boundary_evidence(base)
    targets = [_build_target_receipt(base, target) for target in BEST_SCREENSHOT_TARGETS]
    primary_target = next(
        target
        for target in targets
        if target["path"] == "examples/output/public_apple_static_case_study_dashboard.html"
    )
    public_source_fixtures = [
        {
            "path": fixture["path"],
            "ticker": fixture["ticker"],
            "data_cutoff": fixture["data_cutoff"],
            "source_domains": fixture["source_domains"],
            "static_notice_count": fixture["static_notice_count"],
            "freshness_boundary": fixture["freshness_boundary"],
        }
        for fixture in source_evidence["fixtures"]
        if fixture["fixture_boundary"] == "static_public_source_fixture"
    ]
    return {
        "artifact_type": "visual_evidence_receipt",
        "schema_version": "0.1",
        "tool_version": __version__,
        "source_doc": "docs/demo-screenshot-guide.md",
        "source_boundary_artifact": "examples/output/source_boundary_evidence.json",
        "safety_notice": SAFETY_NOTICE,
        "no_live_data_claim": NO_LIVE_DATA_CLAIM,
        "no_broker_claim": "No broker, portfolio, order, account, credential, or personalized holding data is used.",
        "no_personalized_advice_claim": NO_PERSONALIZED_ADVICE_CLAIM,
        "no_advice_claim": SAFETY_NOTICE,
        "public_source_fixture_limit": PUBLIC_SOURCE_FIXTURE_LIMIT,
        "source_boundaries": SOURCE_BOUNDARIES,
        "review_boundaries": list(SCREENSHOT_REVIEW_BOUNDARIES),
        "required_public_safe_markers": list(REQUIRED_PUBLIC_SAFE_MARKERS),
        "primary_screenshot_target": primary_target,
        "screenshot_targets": targets,
        "public_source_fixtures": public_source_fixtures,
        "checks": {
            "all_screenshot_targets_exist": all(target["exists"] for target in targets),
            "primary_target_exists": primary_target["exists"],
            "primary_target_has_required_markers": primary_target["has_required_markers"],
            "all_visual_targets_public_safe": all(not target["blocked_markers_found"] for target in targets),
            "source_attribution_referenced": True,
            "stale_or_static_warning_referenced": True,
            "public_source_fixture_limits_recorded": True,
            "no_live_data_boundary_recorded": True,
            "no_broker_boundary_recorded": True,
            "no_personalized_advice_boundary_recorded": "buy, sell, or hold advice" in SAFETY_NOTICE,
        },
    }


def visual_evidence_receipt_json(root: str | Path = ".") -> str:
    return json.dumps(build_visual_evidence_receipt(root), indent=2, sort_keys=True) + "\n"


def visual_evidence_receipt_markdown(root: str | Path = ".") -> str:
    return render_visual_evidence_receipt_markdown(build_visual_evidence_receipt(root))


def render_visual_evidence_receipt_markdown(receipt: dict[str, Any]) -> str:
    lines = [
        "# Visual Evidence Receipt",
        "",
        "Deterministic checklist for reviewing public demo screenshots from checked-in static artifacts.",
        "",
        f"> {receipt['safety_notice']}",
        "",
        f"- Tool version: `{receipt['tool_version']}`",
        f"- Source doc: `{receipt['source_doc']}`",
        f"- Source-boundary artifact: `{receipt['source_boundary_artifact']}`",
        f"- Primary screenshot target: `{receipt['primary_screenshot_target']['path']}`",
        "",
        "## Boundary Claims",
        "",
        f"- No live data: {receipt['no_live_data_claim']}",
        f"- No broker: {receipt['no_broker_claim']}",
        f"- No personalized advice: {receipt['no_personalized_advice_claim']}",
        f"- No advice: {receipt['no_advice_claim']}",
        f"- Public-source fixture limit: {receipt['public_source_fixture_limit']}",
        "",
        "## Checks",
        "",
    ]
    lines.extend(f"- {key.replace('_', ' ').title()}: `{value}`" for key, value in receipt["checks"].items())
    lines.extend(["", "## Screenshot Evidence Checklist", ""])
    lines.extend(f"- {item}" for item in receipt["review_boundaries"])
    lines.extend(["", "## Screenshot Targets", ""])
    lines.extend(
        [
            "| Target | Exists | Required markers | Blocked markers | Use |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for target in receipt["screenshot_targets"]:
        markers = ", ".join(target["missing_required_markers"]) or "all present or not required"
        blocked = ", ".join(target["blocked_markers_found"]) or "none"
        lines.append(
            f"| {_markdown_table_cell(target['path'])} | `{target['exists']}` | "
            f"{_markdown_table_cell(markers)} | {_markdown_table_cell(blocked)} | "
            f"{_markdown_table_cell(target['use'])} |"
        )
    lines.extend(["", "## Public-Source Fixture Limits", ""])
    lines.extend(
        [
            "| Fixture | Ticker | Cutoff | Source domains | Static notices | Freshness boundary |",
            "| --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for fixture in receipt["public_source_fixtures"]:
        lines.append(
            f"| {_markdown_table_cell(fixture['path'])} | {_markdown_table_cell(fixture['ticker'])} | "
            f"{_markdown_table_cell(fixture['data_cutoff'])} | "
            f"{_markdown_table_cell(', '.join(fixture['source_domains']))} | "
            f"{fixture['static_notice_count']} | {_markdown_table_cell(fixture['freshness_boundary'])} |"
        )
    lines.extend(["", "## Source Boundaries", ""])
    lines.extend(f"- {key.replace('_', ' ').title()}: {value}" for key, value in receipt["source_boundaries"].items())
    return "\n".join(lines) + "\n"


def _build_target_receipt(base: Path, target: dict[str, str]) -> dict[str, Any]:
    path = target["path"]
    artifact_path = base / path
    text = artifact_path.read_text(encoding="utf-8") if artifact_path.is_file() else ""
    required_markers = _required_markers_for_path(path)
    missing_required = [marker for marker in required_markers if marker not in text]
    lower_text = text.lower()
    blocked_markers = [marker for marker in BLOCKED_VISUAL_MARKERS if marker.lower() in lower_text]
    return {
        "path": path,
        "use": target["use"],
        "exists": artifact_path.is_file(),
        "artifact_kind": _artifact_kind(path),
        "required_markers": required_markers,
        "missing_required_markers": missing_required,
        "has_required_markers": not missing_required,
        "blocked_markers_found": blocked_markers,
        "static_public_safe_scope": True,
    }


def _required_markers_for_path(path: str) -> list[str]:
    if path.endswith(".html"):
        return list(REQUIRED_PUBLIC_SAFE_MARKERS)
    if path.endswith(".svg"):
        return ["Review Queue", "Static"]
    return []


def _artifact_kind(path: str) -> str:
    suffix = Path(path).suffix
    if suffix == ".html":
        return "static_html_dashboard"
    if suffix == ".svg":
        return "static_svg_preview"
    if suffix == ".md":
        return "markdown_report"
    return "static_artifact"


def _markdown_table_cell(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")
