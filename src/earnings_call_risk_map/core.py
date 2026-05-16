"""Core analysis and comparison functions."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE, SOURCE_BOUNDARIES
from .scoring import score_kpi, score_note, sort_catalysts
from .version import __version__

REVIEW_CATEGORY_ORDER = ("stale_data", "missing_evidence", "high_impact_language")
REVIEW_REASON_LABELS = {
    "stale_data": "stale or unverified data",
    "missing_evidence": "missing evidence URL",
    "high_impact_language": "high-impact language",
}


def analyze_document(data: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic risk/opportunity map for one earnings-call fixture."""

    as_of = str(data["as_of"])
    data_cutoff = str(data["data_cutoff"])
    notes = [score_note(note, as_of, data_cutoff) for note in data.get("notes", [])]
    kpis = [score_kpi(kpi, as_of, data_cutoff) for kpi in data.get("kpis", [])]
    risks = sorted(
        [item for item in notes + kpis if item["risk_score"] > 0],
        key=lambda item: (-item["risk_score"], item.get("topic", item.get("name", ""))),
    )
    opportunities = sorted(
        [item for item in notes + kpis if item["opportunity_score"] > 0],
        key=lambda item: (-item["opportunity_score"], item.get("topic", item.get("name", ""))),
    )
    review_queue = [
        {
            "id": item.get("id") or item.get("name"),
            "topic": item.get("topic") or item.get("name"),
            "reasons": item.get("review_reasons") or ["review evidence and freshness"],
            "evidence_url": item.get("evidence_url"),
            "source_attribution": _source_attribution(item),
        }
        for item in notes
        if item.get("review_required")
    ]
    stale_badges = [
        {
            "id": item.get("id") or item.get("name"),
            "topic": item.get("topic") or item.get("name"),
            "badge": item["stale_badge"],
        }
        for item in notes + kpis
        if item["stale_badge"]["status"] != "current"
    ]
    return {
        "schema_version": "0.1",
        "tool_version": __version__,
        "company": data["company"],
        "ticker": data["ticker"],
        "as_of": as_of,
        "data_cutoff": data_cutoff,
        "safety_notice": SAFETY_NOTICE,
        "source_boundaries": SOURCE_BOUNDARIES,
        "source_attribution": _source_attribution(data),
        "summary": {
            "risk_count": len(risks),
            "opportunity_count": len(opportunities),
            "review_queue_count": len(review_queue),
            "stale_badge_count": len(stale_badges),
        },
        "risks": risks,
        "opportunities": opportunities,
        "review_queue": review_queue,
        "stale_badges": stale_badges,
        "catalyst_timeline": sort_catalysts(data.get("catalysts", [])),
    }


def compare_snapshots(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Compare two analyzed snapshots."""

    before_risks = _score_by_key(before.get("risks", []))
    after_risks = _score_by_key(after.get("risks", []))
    before_opps = _score_by_key(before.get("opportunities", []))
    after_opps = _score_by_key(after.get("opportunities", []))
    risk_changes = _diff_scores(before_risks, after_risks)
    opportunity_changes = _diff_scores(before_opps, after_opps)
    review_queue_delta = int(after.get("summary", {}).get("review_queue_count", 0)) - int(
        before.get("summary", {}).get("review_queue_count", 0)
    )
    stale_badge_delta = int(after.get("summary", {}).get("stale_badge_count", 0)) - int(
        before.get("summary", {}).get("stale_badge_count", 0)
    )
    return {
        "schema_version": "0.1",
        "tool_version": __version__,
        "company": after.get("company") or before.get("company"),
        "ticker": after.get("ticker") or before.get("ticker"),
        "before_as_of": before.get("as_of"),
        "after_as_of": after.get("as_of"),
        "safety_notice": after.get("safety_notice") or before.get("safety_notice") or SAFETY_NOTICE,
        "source_boundaries": after.get("source_boundaries") or before.get("source_boundaries") or SOURCE_BOUNDARIES,
        "source_attribution": after.get("source_attribution") or before.get("source_attribution") or [],
        "risk_changes": risk_changes,
        "opportunity_changes": opportunity_changes,
        "review_queue_delta": review_queue_delta,
        "stale_badge_delta": stale_badge_delta,
        "interpretation": _compare_interpretation(
            risk_changes,
            opportunity_changes,
            review_queue_delta,
            stale_badge_delta,
        ),
    }


def build_review_queue_export(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Build a focused deterministic export for human review."""

    records: dict[tuple[str, str, str], dict[str, Any]] = {}
    for item in snapshot.get("risks", []) + snapshot.get("opportunities", []):
        record = _record_for_scored_item(item)
        _merge_review_record(records, record)

    for item in snapshot.get("stale_badges", []):
        badge = item.get("badge", {})
        if badge.get("status") == "current":
            continue
        matched = [
            record
            for key, record in records.items()
            if key[0] == str(item.get("id") or item.get("topic") or "item")
            and key[1] == str(item.get("topic") or "general")
        ]
        if matched:
            for record in matched:
                _merge_review_record(
                    records,
                    {
                        **record,
                        "stale_badge": badge,
                        "issue_categories": ["stale_data"],
                        "reasons": [REVIEW_REASON_LABELS["stale_data"]],
                    },
                )
            continue
        key = (str(item.get("id") or item.get("topic") or "item"), str(item.get("topic") or "general"), "item")
        _merge_review_record(
            records,
            {
                "id": key[0],
                "topic": key[1],
                "source_type": key[2],
                "date": None,
                "evidence_url": None,
                "source_attribution": [],
                "stale_badge": badge,
                "risk_score": 0,
                "risk_level": "none",
                "opportunity_score": 0,
                "opportunity_level": "none",
                "excerpt": "",
                "issue_categories": ["stale_data"],
                "reasons": [REVIEW_REASON_LABELS["stale_data"]],
            },
        )

    for catalyst in snapshot.get("catalyst_timeline", []):
        if catalyst.get("evidence_url"):
            continue
        topic = str(catalyst.get("title") or "Untitled catalyst")
        _merge_review_record(
            records,
            {
                "id": f"catalyst:{catalyst.get('date')}:{topic}",
                "topic": topic,
                "source_type": "catalyst",
                "date": catalyst.get("date"),
                "evidence_url": None,
                "source_attribution": _source_attribution(catalyst),
                "stale_badge": None,
                "risk_score": 0,
                "risk_level": "none",
                "opportunity_score": 0,
                "opportunity_level": "none",
                "excerpt": str(catalyst.get("description") or ""),
                "issue_categories": ["missing_evidence"],
                "reasons": [REVIEW_REASON_LABELS["missing_evidence"]],
            },
        )

    items = sorted(
        records.values(),
        key=lambda item: (
            -len(item["issue_categories"]),
            -int(item.get("risk_score", 0)),
            -int(item.get("opportunity_score", 0)),
            item["topic"],
            item["id"],
        ),
    )
    counts = {category: 0 for category in REVIEW_CATEGORY_ORDER}
    for item in items:
        for category in item["issue_categories"]:
            counts[category] += 1

    return {
        "schema_version": "0.1",
        "tool_version": __version__,
        "company": snapshot.get("company"),
        "ticker": snapshot.get("ticker"),
        "as_of": snapshot.get("as_of"),
        "data_cutoff": snapshot.get("data_cutoff"),
        "safety_notice": snapshot.get("safety_notice", SAFETY_NOTICE),
        "source_boundaries": snapshot.get("source_boundaries", SOURCE_BOUNDARIES),
        "source_attribution": snapshot.get("source_attribution", []),
        "summary": {
            "review_item_count": len(items),
            "stale_data_count": counts["stale_data"],
            "missing_evidence_count": counts["missing_evidence"],
            "high_impact_language_count": counts["high_impact_language"],
        },
        "items": items,
    }


def build_review_queue_jsonl_records(
    fixture_slug: str,
    fixture_path: str,
    review_queue_export: dict[str, Any],
) -> list[dict[str, Any]]:
    """Flatten one review queue export into deterministic JSONL records."""

    records = []
    for index, item in enumerate(review_queue_export.get("items", []), start=1):
        records.append(
            {
                "schema_version": "0.1",
                "record_type": "review_queue_item",
                "fixture_slug": fixture_slug,
                "fixture_path": fixture_path,
                "item_index": index,
                "company": review_queue_export.get("company"),
                "ticker": review_queue_export.get("ticker"),
                "as_of": review_queue_export.get("as_of"),
                "data_cutoff": review_queue_export.get("data_cutoff"),
                "safety_notice": review_queue_export.get("safety_notice", SAFETY_NOTICE),
                "source_boundaries": review_queue_export.get("source_boundaries", SOURCE_BOUNDARIES),
                "source_attribution": review_queue_export.get("source_attribution", []),
                "review_item": item,
            }
        )
    return records


def render_jsonl(records: list[dict[str, Any]]) -> str:
    """Render records as deterministic JSON Lines."""

    if not records:
        return ""
    return "\n".join(_json_dumps(record) for record in records) + "\n"


def _json_dumps(payload: dict[str, Any]) -> str:
    """Return one compact deterministic JSON object."""

    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _score_by_key(items: list[dict[str, Any]]) -> dict[str, int]:
    scores: dict[str, int] = {}
    for item in items:
        key = str(item.get("topic") or item.get("name") or item.get("id") or "general")
        scores[key] = max(scores.get(key, 0), int(item.get("risk_score") or item.get("opportunity_score") or 0))
    return scores


def _diff_scores(before: dict[str, int], after: dict[str, int]) -> list[dict[str, Any]]:
    changes = []
    for key in sorted(set(before) | set(after)):
        old = before.get(key, 0)
        new = after.get(key, 0)
        if old != new:
            changes.append({"topic": key, "before": old, "after": new, "delta": new - old})
    return sorted(changes, key=lambda item: (-abs(item["delta"]), item["topic"]))


def _compare_interpretation(
    risk_changes: list[dict[str, Any]],
    opportunity_changes: list[dict[str, Any]],
    review_queue_delta: int,
    stale_badge_delta: int,
) -> list[str]:
    lines = [
        "Deltas compare deterministic keyword scores between analyzed snapshots; they are prompts for source review, not investment conclusions.",
    ]
    lines.extend(_attention_movement_lines("Risk", risk_changes, "risk-score"))
    lines.extend(_attention_movement_lines("Opportunity", opportunity_changes, "opportunity-score"))
    if review_queue_delta > 0:
        lines.append(f"Review workload increased by {review_queue_delta}; inspect new stale, missing-evidence, or high-impact items.")
    elif review_queue_delta < 0:
        lines.append(f"Review workload decreased by {abs(review_queue_delta)}; confirm whether evidence or freshness improved.")
    else:
        lines.append("Review workload count was unchanged.")

    if stale_badge_delta > 0:
        lines.append(f"Stale/static badge count increased by {stale_badge_delta}; verify whether older sources still apply.")
    elif stale_badge_delta < 0:
        lines.append(f"Stale/static badge count decreased by {abs(stale_badge_delta)}; confirm dates and source freshness.")
    else:
        lines.append("Stale/static badge count was unchanged.")
    return lines


def _attention_movement_lines(label: str, changes: list[dict[str, Any]], score_name: str) -> list[str]:
    if not changes:
        return [f"No {score_name} movement was detected."]
    lines = []
    for direction, comparator in (("increased", 1), ("decreased", -1)):
        matching_topics = [item["topic"] for item in changes if int(item["delta"]) * comparator > 0]
        topics = ", ".join(matching_topics[:3])
        if topics:
            lines.append(f"{label} attention {direction} for: {topics}.")
    return lines


def _record_for_scored_item(item: dict[str, Any]) -> dict[str, Any]:
    badge = item.get("stale_badge", {})
    risk_score = int(item.get("risk_score") or 0)
    opportunity_score = int(item.get("opportunity_score") or 0)
    categories = []
    if badge.get("status") != "current":
        categories.append("stale_data")
    if not item.get("evidence_url"):
        categories.append("missing_evidence")
    if risk_score >= 7 or opportunity_score >= 7:
        categories.append("high_impact_language")
    categories = [category for category in REVIEW_CATEGORY_ORDER if category in categories]
    topic = str(item.get("topic") or item.get("name") or "general")
    source_type = str(item.get("type") or ("kpi" if item.get("name") else "item"))
    return {
        "id": str(item.get("id") or item.get("name") or topic),
        "topic": topic,
        "source_type": source_type,
        "date": item.get("date"),
        "evidence_url": item.get("evidence_url"),
        "source_attribution": _source_attribution(item),
        "stale_badge": badge,
        "risk_score": risk_score,
        "risk_level": item.get("risk_level", "none"),
        "opportunity_score": opportunity_score,
        "opportunity_level": item.get("opportunity_level", "none"),
        "excerpt": str(item.get("text") or item.get("observation") or ""),
        "issue_categories": categories,
        "reasons": [REVIEW_REASON_LABELS[category] for category in categories],
    }


def _merge_review_record(records: dict[tuple[str, str, str], dict[str, Any]], record: dict[str, Any]) -> None:
    if not record.get("issue_categories"):
        return
    key = (str(record["id"]), str(record["topic"]), str(record["source_type"]))
    existing = records.get(key)
    if existing is None:
        records[key] = record
        return
    categories = set(existing["issue_categories"]) | set(record["issue_categories"])
    existing["issue_categories"] = [
        category
        for category in REVIEW_CATEGORY_ORDER
        if category in categories
    ]
    existing["reasons"] = [REVIEW_REASON_LABELS[category] for category in existing["issue_categories"]]
    existing["risk_score"] = max(int(existing.get("risk_score", 0)), int(record.get("risk_score", 0)))
    existing["opportunity_score"] = max(
        int(existing.get("opportunity_score", 0)), int(record.get("opportunity_score", 0))
    )
    existing["evidence_url"] = existing.get("evidence_url") or record.get("evidence_url")
    existing["source_attribution"] = existing.get("source_attribution") or record.get("source_attribution") or []
    existing["date"] = existing.get("date") or record.get("date")
    existing["stale_badge"] = existing.get("stale_badge") or record.get("stale_badge")
    existing["excerpt"] = existing.get("excerpt") or record.get("excerpt")


def _source_attribution(item: dict[str, Any]) -> list[dict[str, Any]]:
    attribution = item.get("source_attribution") or []
    if isinstance(attribution, dict):
        attribution = [attribution]
    if not isinstance(attribution, list):
        return []
    normalized = []
    allowed = {"source_name", "publisher", "source_type", "source_url", "accessed_at", "static_notice"}
    for source in attribution:
        if not isinstance(source, dict):
            continue
        clean = {key: str(value) for key, value in source.items() if key in allowed and value is not None}
        if clean:
            normalized.append(clean)
    return normalized
