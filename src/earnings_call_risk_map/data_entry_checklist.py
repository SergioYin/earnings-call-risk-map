"""Data-entry checklist rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE

DATA_ENTRY_CHECKS: tuple[dict[str, Any], ...] = (
    {
        "slug": "before-entry",
        "title": "Before Entry",
        "checks": [
            "Save the transcript or notes in a stable review location outside the fixture.",
            "Record the exact review date as `as_of`.",
            "Record the latest source date represented by the material as `data_cutoff`.",
            (
                "Identify the source container: transcript, company investor-relations page, SEC filing, "
                "shareholder letter, press release, news article, or user synthesis."
            ),
            "Keep a list of source URLs that were actually opened.",
        ],
    },
    {
        "slug": "source-boundary-rules",
        "title": "Source Boundary Rules",
        "checks": [
            "Do not invent source URLs, publishers, source names, accessed dates, speaker names, KPI values, or fiscal periods.",
            "Do not promote an analyst question into a company fact.",
            "Do not promote user summaries into source evidence.",
            "Use `accessed_at` only when the source URL was actually checked.",
            "Do not remove stale dates to avoid stale badges.",
        ],
    },
    {
        "slug": "entry-steps",
        "title": "Entry Steps",
        "checks": [
            "Start from a valid template in `docs/templates.md`.",
            "Fill top-level `company`, `ticker`, `as_of`, and `data_cutoff`.",
            "Add top-level `source_attribution` only when source details are known.",
            "Split transcript content into `management_claim`, `analyst_question`, and `user_synthesis` notes.",
            "Add KPIs only when the source packet contains the exact KPI label and value.",
            "Add catalysts only when the date or event is present or clearly labeled as user synthesis.",
            "Keep blank `evidence_url` fields when evidence is missing.",
            "Run validation before committing the fixture.",
        ],
    },
    {
        "slug": "final-review",
        "title": "Final Review",
        "checks": [
            "The fixture is valid JSON.",
            "`as_of`, `data_cutoff`, item `date`, and `accessed_at` dates are real calendar dates.",
            "Every `source_url` and `evidence_url` was actually captured from source material.",
            "Missing evidence remains blank and will be surfaced in the review queue.",
            "Management claims, analyst questions, and user synthesis are separated.",
            "Stale badges are preserved until sources are refreshed.",
            "The non-advice disclaimer is preserved in downstream Markdown, JSON, and handoff artifacts.",
        ],
    },
)

FIELD_MAPPINGS: tuple[dict[str, str], ...] = (
    {
        "field": "company",
        "use": "Company name shown in the source packet.",
        "rule": "Use the visible legal or display name; do not normalize from memory.",
    },
    {
        "field": "ticker",
        "use": "Ticker or short identifier used by the author.",
        "rule": "If the source does not show a ticker, use the user's provided identifier.",
    },
    {
        "field": "as_of",
        "use": "Date of this review.",
        "rule": "Use the actual authoring or review date in `YYYY-MM-DD`.",
    },
    {
        "field": "data_cutoff",
        "use": "Latest date represented by the source packet.",
        "rule": "Use the latest transcript, filing, release, or note date that is present.",
    },
    {
        "field": "notes[].type",
        "use": "Provenance label for text.",
        "rule": "Use `management_claim`, `analyst_question`, or `user_synthesis` based on who made the statement.",
    },
    {
        "field": "notes[].text",
        "use": "Short source excerpt or author note.",
        "rule": "Preserve source meaning; do not add claims that are not present.",
    },
    {
        "field": "kpis[].value",
        "use": "KPI value as shown in source material.",
        "rule": "Keep the source's units and wording; label any calculation as `user_synthesis`.",
    },
    {
        "field": "evidence_url",
        "use": "Public URL for the item.",
        "rule": "Leave empty when no URL was actually captured.",
    },
    {
        "field": "source_attribution",
        "use": "Static provenance metadata.",
        "rule": "Use only observed source details and allowed `source_type` values.",
    },
)

VALIDATION_COMMANDS = (
    "PYTHONPATH=src python -m earnings_call_risk_map analyze path/to/fixture.json",
    "PYTHONPATH=src python -m earnings_call_risk_map review-queue path/to/fixture.json",
)


def build_data_entry_checklist() -> dict[str, Any]:
    return {
        "artifact_type": "data_entry_checklist",
        "source_doc": "docs/data-entry-checklist.md",
        "goal": "Create a valid JSON fixture without hallucinating sources.",
        "safety_notice": SAFETY_NOTICE,
        "section_count": len(DATA_ENTRY_CHECKS),
        "field_mapping_count": len(FIELD_MAPPINGS),
        "sections": [dict(section) for section in DATA_ENTRY_CHECKS],
        "field_mappings": [dict(mapping) for mapping in FIELD_MAPPINGS],
        "validation_commands": list(VALIDATION_COMMANDS),
    }


def data_entry_checklist_json() -> str:
    return json.dumps(build_data_entry_checklist(), indent=2, sort_keys=True) + "\n"


def data_entry_checklist_markdown() -> str:
    checklist = build_data_entry_checklist()
    lines = [
        "# Data Entry Checklist",
        "",
        checklist["goal"],
        "",
        f"> {checklist['safety_notice']}",
        "",
        f"- Source doc: `{checklist['source_doc']}`",
        f"- Sections: {checklist['section_count']}",
        f"- Field mappings: {checklist['field_mapping_count']}",
        "",
        "## Field Mapping",
        "",
        "| Fixture field | Use | No-hallucination rule |",
        "| --- | --- | --- |",
    ]
    lines.extend(
        f"| `{mapping['field']}` | {mapping['use']} | {mapping['rule']} |"
        for mapping in checklist["field_mappings"]
    )
    for section in checklist["sections"]:
        lines.extend(["", f"## {section['title']}", ""])
        lines.extend(f"- {check}" for check in section["checks"])
    lines.extend(["", "## Validation", "", "```bash"])
    lines.extend(checklist["validation_commands"])
    lines.append("```")
    return "\n".join(lines) + "\n"
