"""Fixture summary report generation."""

from __future__ import annotations

from collections import Counter
from typing import Any

from .core import analyze_document
from .models import SAFETY_NOTICE, SOURCE_BOUNDARIES
from .version import __version__


def build_fixture_summary(data: dict[str, Any]) -> dict[str, Any]:
    """Build a compact Markdown/JSON-friendly summary for one input fixture."""

    snapshot = analyze_document(data)
    source_type_counts = _source_type_counts(data)
    stale_status_counts = Counter(
        str(item.get("badge", {}).get("status") or "unknown")
        for item in snapshot.get("stale_badges", [])
    )
    counts = {
        "notes": len(data.get("notes", [])),
        "kpis": len(data.get("kpis", [])),
        "catalysts": len(data.get("catalysts", [])),
        "risks": snapshot["summary"]["risk_count"],
        "opportunities": snapshot["summary"]["opportunity_count"],
        "review_queue": snapshot["summary"]["review_queue_count"],
        "stale_badges": snapshot["summary"]["stale_badge_count"],
        "source_attribution_records": sum(source_type_counts.values()),
    }
    return {
        "schema_version": "0.1",
        "tool_version": __version__,
        "artifact_type": "fixture_summary",
        "company": snapshot["company"],
        "ticker": snapshot["ticker"],
        "as_of": snapshot["as_of"],
        "data_cutoff": snapshot["data_cutoff"],
        "safety_notice": SAFETY_NOTICE,
        "source_boundaries": SOURCE_BOUNDARIES,
        "source_types": [
            {"source_type": source_type, "count": count}
            for source_type, count in sorted(source_type_counts.items())
        ],
        "stale_badges": snapshot.get("stale_badges", []),
        "stale_status_counts": dict(sorted(stale_status_counts.items())),
        "counts": counts,
    }


def render_fixture_summary_markdown(summary: dict[str, Any]) -> str:
    """Render a fixture summary as Markdown."""

    counts = summary["counts"]
    lines = [
        "# Fixture Summary",
        "",
        f"- Company: {summary['company']}",
        f"- Ticker: `{summary['ticker']}`",
        f"- As of: `{summary['as_of']}`",
        f"- Data cutoff: `{summary['data_cutoff']}`",
        "",
        f"> {summary['safety_notice']}",
        "",
        "## Counts",
        "",
        "| Count | Value |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {label.replace('_', ' ').title()} | {counts[label]} |" for label in counts)
    lines.extend(["", "## Source Types", ""])
    if summary["source_types"]:
        lines.extend(
            [
                "| Source type | Count |",
                "| --- | ---: |",
            ]
        )
        lines.extend(f"| `{item['source_type']}` | {item['count']} |" for item in summary["source_types"])
    else:
        lines.append("- None recorded")

    lines.extend(["", "## Stale Badges", ""])
    if summary["stale_badges"]:
        lines.extend(
            [
                "| ID | Topic | Status | Age days | Label |",
                "| --- | --- | --- | ---: | --- |",
            ]
        )
        for item in summary["stale_badges"]:
            badge = item.get("badge", {})
            age_days = badge.get("age_days")
            lines.append(
                f"| `{item.get('id')}` | {item.get('topic')} | `{badge.get('status')}` | "
                f"{age_days if age_days is not None else ''} | {badge.get('label')} |"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Source Boundaries", ""])
    lines.extend(f"- {key.replace('_', ' ').title()}: {value}" for key, value in summary["source_boundaries"].items())
    return "\n".join(lines) + "\n"


def fixture_summary_json(data: dict[str, Any]) -> dict[str, Any]:
    return build_fixture_summary(data)


def fixture_summary_markdown(data: dict[str, Any]) -> str:
    return render_fixture_summary_markdown(build_fixture_summary(data))


def _source_type_counts(data: dict[str, Any]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for source in _iter_source_attribution(data):
        counts[str(source.get("source_type") or "unspecified")] += 1
    return counts


def _iter_source_attribution(data: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    records.extend(_normalize_source_attribution(data.get("source_attribution")))
    for collection in ("notes", "kpis", "catalysts"):
        for item in data.get(collection, []):
            if isinstance(item, dict):
                records.extend(_normalize_source_attribution(item.get("source_attribution")))
    return records


def _normalize_source_attribution(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []
