"""Human-readable schema authoring reference rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE

TOP_LEVEL_FIELDS: tuple[dict[str, str], ...] = (
    {
        "field": "schema_version",
        "meaning": "Which fixture shape this file was written for.",
        "guidance": "Use `0.1` for the current format when you include it.",
    },
    {
        "field": "company",
        "meaning": "The company name shown in reports and dashboards.",
        "guidance": "Required. Use the display name a reviewer will recognize.",
    },
    {
        "field": "ticker",
        "meaning": "The ticker or short company identifier.",
        "guidance": "Required. Use the public ticker when available; otherwise use a stable short label.",
    },
    {
        "field": "as_of",
        "meaning": "The date of this review.",
        "guidance": "Required. Use `YYYY-MM-DD`. This is the anchor date for stale/static-data checks.",
    },
    {
        "field": "data_cutoff",
        "meaning": "The newest source date represented in the fixture.",
        "guidance": "Required. Use `YYYY-MM-DD`. Do not set this later than the material actually reviewed.",
    },
    {
        "field": "notes",
        "meaning": "Text snippets or research notes to score.",
        "guidance": "Use an array of note objects. Use `[]` when there are no notes yet.",
    },
    {
        "field": "kpis",
        "meaning": "Metrics or operational observations to show in the review.",
        "guidance": "Use an array of KPI objects. Keep values as they appeared in source material.",
    },
    {
        "field": "catalysts",
        "meaning": "Dated future events or review reminders.",
        "guidance": "Use an array of catalyst objects. These should be events, not recommendations.",
    },
    {
        "field": "source_attribution",
        "meaning": "Source records that apply to the whole fixture.",
        "guidance": "Use this for the source bundle behind the file. Item-level source attribution can override or add detail.",
    },
)

NOTE_FIELDS: tuple[dict[str, str], ...] = (
    {
        "field": "id",
        "meaning": "A stable label for the note.",
        "guidance": "Useful for review comments and diffs. Keep it short, such as `n1` or `margin-qna-1`.",
    },
    {
        "field": "date",
        "meaning": "The date of the source text.",
        "guidance": "Use `YYYY-MM-DD`. If omitted, the tool falls back to `data_cutoff`.",
    },
    {
        "field": "topic",
        "meaning": "The section label for the note.",
        "guidance": "Use reviewer-friendly wording such as `demand`, `margin`, or `capital allocation`.",
    },
    {
        "field": "type",
        "meaning": "How the text should be treated.",
        "guidance": "Use values like `management_claim`, `analyst_question`, `user_synthesis`, `transcript_excerpt`, or `note`.",
    },
    {
        "field": "text",
        "meaning": "The actual language to score.",
        "guidance": (
            "Paste only the static excerpt or authored note you want reviewed. Do not blend source text "
            "with your interpretation unless the type is `user_synthesis`."
        ),
    },
    {
        "field": "evidence_url",
        "meaning": "A public URL supporting the note.",
        "guidance": "Leave blank or omit when unavailable; missing URLs are surfaced in the review queue.",
    },
    {
        "field": "source_attribution",
        "meaning": "Source record for this note.",
        "guidance": "Use when the note comes from a specific filing, transcript, presentation, or user-authored source.",
    },
)

KPI_FIELDS: tuple[dict[str, str], ...] = (
    {
        "field": "name",
        "meaning": "Metric name.",
        "guidance": "Use the label from the source when possible, such as `Revenue growth` or `Net retention`.",
    },
    {
        "field": "value",
        "meaning": "Metric value as reported.",
        "guidance": "Use a string for values with units, percentages, or ranges; a number is also accepted.",
    },
    {
        "field": "direction",
        "meaning": "Whether the movement reads positive or negative.",
        "guidance": (
            "`up`, `better`, or `positive` adds opportunity weight. `down`, `worse`, or `negative` "
            "adds risk weight."
        ),
    },
    {
        "field": "date",
        "meaning": "Date of the KPI observation.",
        "guidance": "Use `YYYY-MM-DD`. If omitted, the tool falls back to `data_cutoff`.",
    },
    {
        "field": "observation",
        "meaning": "Short context about the KPI.",
        "guidance": "Use this for source-grounded context, not a forecast or valuation call.",
    },
    {
        "field": "evidence_url",
        "meaning": "A public URL supporting the KPI.",
        "guidance": "Leave blank or omit when unavailable; missing URLs can be reviewed later.",
    },
    {
        "field": "source_attribution",
        "meaning": "Source record for this KPI.",
        "guidance": "Use when the KPI comes from a specific table, filing, deck, or user worksheet.",
    },
)

CATALYST_FIELDS: tuple[dict[str, str], ...] = (
    {
        "field": "date",
        "meaning": "Event or review-trigger date.",
        "guidance": "Use `YYYY-MM-DD`. The timeline sorts catalysts by this date.",
    },
    {
        "field": "title",
        "meaning": "Short event name.",
        "guidance": "Use a concise label such as `Investor day`, `Product launch`, or `Next earnings report`.",
    },
    {
        "field": "description",
        "meaning": "Why the event matters for review.",
        "guidance": "Describe what should be checked, not what an investor should do.",
    },
    {
        "field": "expected_impact",
        "meaning": "High-level risk/opportunity label.",
        "guidance": "Use neutral labels such as `risk review`, `opportunity review`, or `risk/opportunity review`.",
    },
    {
        "field": "evidence_url",
        "meaning": "A public URL supporting the catalyst.",
        "guidance": "Leave blank or omit when unavailable.",
    },
    {
        "field": "source_attribution",
        "meaning": "Source record for this catalyst.",
        "guidance": "Use when the catalyst came from an events page, filing, transcript, or user-authored plan.",
    },
)

SOURCE_ATTRIBUTION_FIELDS: tuple[dict[str, str], ...] = (
    {
        "field": "source_name",
        "meaning": "Human-readable source label.",
        "guidance": "Example: `Q1 2026 earnings call transcript` or `FY2025 Form 10-K`.",
    },
    {
        "field": "publisher",
        "meaning": "Who published or supplied the source.",
        "guidance": "Example: a company name, `U.S. SEC EDGAR`, a transcript provider, or `User worksheet`.",
    },
    {
        "field": "source_type",
        "meaning": "Provenance category.",
        "guidance": (
            "Use the closest allowed category from the generated schema, such as "
            "`company_investor_relations`, `sec_filing`, `transcript`, `shareholder_letter`, or `user_synthesis`."
        ),
    },
    {
        "field": "source_url",
        "meaning": "Public URL for the static source.",
        "guidance": "The tool records the URL but does not fetch, refresh, or verify it.",
    },
    {
        "field": "accessed_at",
        "meaning": "Date the URL was checked by the fixture author.",
        "guidance": "Use `YYYY-MM-DD` only when the URL was actually checked. This is not the event date.",
    },
    {
        "field": "static_notice",
        "meaning": "A short boundary note.",
        "guidance": "Use to remind readers that the fixture is static, non-live, or source-limited.",
    },
)

FIELD_SECTIONS = (
    ("top_level", "Top-Level Fields", TOP_LEVEL_FIELDS),
    ("notes", "Note Fields", NOTE_FIELDS),
    ("kpis", "KPI Fields", KPI_FIELDS),
    ("catalysts", "Catalyst Fields", CATALYST_FIELDS),
    ("source_attribution", "Source Attribution Fields", SOURCE_ATTRIBUTION_FIELDS),
)

MINIMAL_STARTING_POINT = {
    "schema_version": "0.1",
    "company": "Example Systems Inc.",
    "ticker": "EXM",
    "as_of": "2026-05-15",
    "data_cutoff": "2026-04-30",
    "notes": [],
    "kpis": [],
    "catalysts": [],
}


def build_schema_authoring_reference() -> dict[str, Any]:
    sections = [
        {
            "slug": slug,
            "title": title,
            "fields": [dict(field) for field in fields],
        }
        for slug, title, fields in FIELD_SECTIONS
    ]
    return {
        "artifact_type": "schema_authoring_reference",
        "source_doc": "docs/schema-authoring-reference.md",
        "schema_reference": "docs/schema-reference.json",
        "technical_reference": "docs/input-schema.md",
        "safety_notice": SAFETY_NOTICE,
        "authoring_model": (
            "A fixture is a static review packet. It describes one company, the date of the review, "
            "the latest source date represented by the packet, and optional notes, KPIs, and catalysts."
        ),
        "no_hallucination_rule": (
            "Do not invent source names, publishers, URLs, dates, speaker labels, KPI values, or fiscal periods "
            "to make the fixture look complete."
        ),
        "date_rule": (
            "Use exact calendar dates in YYYY-MM-DD format. Invalid dates such as 2026/05/15, "
            "05-15-2026, or 2026-02-30 should be fixed before running the CLI."
        ),
        "extra_metadata_rule": (
            "Additional properties are allowed for local metadata, but documented fields should be used for "
            "anything that affects reports, review queues, or snapshots."
        ),
        "field_section_count": len(sections),
        "field_count": sum(len(section["fields"]) for section in sections),
        "sections": sections,
        "minimal_starting_point": dict(MINIMAL_STARTING_POINT),
    }


def schema_authoring_reference_json() -> str:
    return json.dumps(build_schema_authoring_reference(), indent=2, sort_keys=True) + "\n"


def schema_authoring_reference_markdown() -> str:
    reference = build_schema_authoring_reference()
    lines = [
        "# Schema Authoring Reference",
        "",
        "This page explains fixture fields in human terms for authors filling out JSON by hand or from a worksheet.",
        "For the generated machine-readable contract, see [`schema-reference.json`](schema-reference.json).",
        "For validation commands and the full technical schema notes, see [JSON Fixture Schema Reference](input-schema.md).",
        "",
        f"> {reference['safety_notice']}",
        "",
        "## Authoring Model",
        "",
        reference["authoring_model"],
        "",
        "A fixture has three optional collections:",
        "",
        "- `notes`: source excerpts or research notes that should be scored for language.",
        "- `kpis`: numeric or labeled observations that should be shown alongside the review.",
        "- `catalysts`: dated events or follow-up triggers.",
        "",
        reference["no_hallucination_rule"],
    ]
    for section in reference["sections"]:
        lines.extend(["", f"## {section['title']}", "", "| Field | Plain-English Meaning | Authoring Guidance |", "| --- | --- | --- |"])
        lines.extend(
            f"| `{field['field']}` | {field['meaning']} | {field['guidance']} |"
            for field in section["fields"]
        )
        if section["slug"] == "source_attribution":
            lines.extend(
                [
                    "",
                    "`source_attribution` can be one object or an array of objects. Each source record should include "
                    "at least one supported field. Use item-level records when a note, KPI, or catalyst has a more "
                    "specific source than the fixture-level bundle.",
                ]
            )
    lines.extend(
        [
            "",
            "## Date Rules",
            "",
            reference["date_rule"],
            "",
            "## Extra Metadata",
            "",
            reference["extra_metadata_rule"],
            "",
            "## Minimal Starting Point",
            "",
            "```json",
            json.dumps(reference["minimal_starting_point"], indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"
