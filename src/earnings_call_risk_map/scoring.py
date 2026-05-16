"""Deterministic scoring for notes, KPIs, stale data, and review queues."""

from __future__ import annotations

from datetime import date
from typing import Any

from .models import OPPORTUNITY_KEYWORDS, RISK_KEYWORDS


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def days_between(later: str | None, earlier: str | None) -> int | None:
    later_date = parse_date(later)
    earlier_date = parse_date(earlier)
    if not later_date or not earlier_date:
        return None
    return (later_date - earlier_date).days


def keyword_score(text: str, keywords: dict[str, int]) -> tuple[int, list[str]]:
    lowered = text.lower()
    hits = [word for word in sorted(keywords) if word in lowered]
    score = sum(keywords[word] for word in hits)
    return score, hits


def severity_label(score: int) -> str:
    if score >= 7:
        return "high"
    if score >= 4:
        return "medium"
    if score > 0:
        return "low"
    return "none"


def stale_badge(as_of: str, item_date: str | None, stale_after_days: int = 90) -> dict[str, Any]:
    age = days_between(as_of, item_date)
    if age is None:
        return {"status": "unknown", "age_days": None, "label": "date-unverified"}
    if age > stale_after_days:
        return {"status": "stale", "age_days": age, "label": f"stale>{stale_after_days}d"}
    return {"status": "current", "age_days": age, "label": "current"}


def score_note(note: dict[str, Any], as_of: str, data_cutoff: str) -> dict[str, Any]:
    text = str(note.get("text", ""))
    risk_score, risk_hits = keyword_score(text, RISK_KEYWORDS)
    opportunity_score, opportunity_hits = keyword_score(text, OPPORTUNITY_KEYWORDS)
    evidence_url = note.get("evidence_url")
    note_date = str(note.get("date") or data_cutoff)
    badge = stale_badge(as_of, note_date)
    if badge["status"] == "stale":
        risk_score += 1

    review_reasons: list[str] = []
    if not evidence_url:
        review_reasons.append("missing evidence URL")
    if badge["status"] != "current":
        review_reasons.append(f"data is {badge['status']}")
    if risk_score >= 7 or opportunity_score >= 7:
        review_reasons.append("high-impact language")

    return {
        "id": str(note.get("id") or ""),
        "topic": str(note.get("topic") or "general"),
        "type": str(note.get("type") or "note"),
        "text": text,
        "date": note_date,
        "evidence_url": evidence_url,
        "source_attribution": _source_attribution(note),
        "risk_score": risk_score,
        "risk_level": severity_label(risk_score),
        "risk_keywords": risk_hits,
        "opportunity_score": opportunity_score,
        "opportunity_level": severity_label(opportunity_score),
        "opportunity_keywords": opportunity_hits,
        "stale_badge": badge,
        "review_required": bool(review_reasons),
        "review_reasons": review_reasons,
    }


def score_kpi(kpi: dict[str, Any], as_of: str, data_cutoff: str) -> dict[str, Any]:
    name = str(kpi.get("name") or "Unnamed KPI")
    direction = str(kpi.get("direction") or "").lower()
    observation = str(kpi.get("observation") or "")
    text = f"{name} {direction} {observation}"
    risk_score, risk_hits = keyword_score(text, RISK_KEYWORDS)
    opportunity_score, opportunity_hits = keyword_score(text, OPPORTUNITY_KEYWORDS)
    if direction in {"down", "worse", "negative"}:
        risk_score += 2
    if direction in {"up", "better", "positive"}:
        opportunity_score += 2
    kpi_date = str(kpi.get("date") or data_cutoff)
    badge = stale_badge(as_of, kpi_date)
    return {
        "name": name,
        "value": kpi.get("value"),
        "direction": direction or "unspecified",
        "observation": observation,
        "date": kpi_date,
        "evidence_url": kpi.get("evidence_url"),
        "source_attribution": _source_attribution(kpi),
        "risk_score": risk_score,
        "risk_level": severity_label(risk_score),
        "risk_keywords": risk_hits,
        "opportunity_score": opportunity_score,
        "opportunity_level": severity_label(opportunity_score),
        "opportunity_keywords": opportunity_hits,
        "stale_badge": badge,
    }


def sort_catalysts(catalysts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for item in catalysts:
        normalized.append(
            {
                "date": str(item.get("date") or "9999-12-31"),
                "title": str(item.get("title") or "Untitled catalyst"),
                "description": str(item.get("description") or ""),
                "expected_impact": str(item.get("expected_impact") or "review"),
                "evidence_url": item.get("evidence_url"),
                "source_attribution": _source_attribution(item),
            }
        )
    return sorted(normalized, key=lambda item: (item["date"], item["title"]))


def _source_attribution(item: dict[str, Any]) -> list[dict[str, Any]]:
    attribution = item.get("source_attribution") or []
    if isinstance(attribution, dict):
        attribution = [attribution]
    if not isinstance(attribution, list):
        return []
    return [source for source in attribution if isinstance(source, dict)]
