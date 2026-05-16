"""Core analysis and comparison functions."""

from __future__ import annotations

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
    return {
        "schema_version": "0.1",
        "tool_version": __version__,
        "company": after.get("company") or before.get("company"),
        "ticker": after.get("ticker") or before.get("ticker"),
        "before_as_of": before.get("as_of"),
        "after_as_of": after.get("as_of"),
        "safety_notice": after.get("safety_notice") or before.get("safety_notice") or SAFETY_NOTICE,
        "source_boundaries": after.get("source_boundaries") or before.get("source_boundaries") or SOURCE_BOUNDARIES,
        "risk_changes": _diff_scores(before_risks, after_risks),
        "opportunity_changes": _diff_scores(before_opps, after_opps),
        "review_queue_delta": int(after.get("summary", {}).get("review_queue_count", 0))
        - int(before.get("summary", {}).get("review_queue_count", 0)),
        "stale_badge_delta": int(after.get("summary", {}).get("stale_badge_count", 0))
        - int(before.get("summary", {}).get("stale_badge_count", 0)),
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
        "summary": {
            "review_item_count": len(items),
            "stale_data_count": counts["stale_data"],
            "missing_evidence_count": counts["missing_evidence"],
            "high_impact_language_count": counts["high_impact_language"],
        },
        "items": items,
    }


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
    existing["issue_categories"] = [
        category
        for category in REVIEW_CATEGORY_ORDER
        if category in set(existing["issue_categories"]) | set(record["issue_categories"])
    ]
    existing["reasons"] = [REVIEW_REASON_LABELS[category] for category in existing["issue_categories"]]
    existing["risk_score"] = max(int(existing.get("risk_score", 0)), int(record.get("risk_score", 0)))
    existing["opportunity_score"] = max(
        int(existing.get("opportunity_score", 0)), int(record.get("opportunity_score", 0))
    )
    existing["evidence_url"] = existing.get("evidence_url") or record.get("evidence_url")
    existing["date"] = existing.get("date") or record.get("date")
    existing["stale_badge"] = existing.get("stale_badge") or record.get("stale_badge")
    existing["excerpt"] = existing.get("excerpt") or record.get("excerpt")
