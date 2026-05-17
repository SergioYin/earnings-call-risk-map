# Schema Authoring Reference

This page explains fixture fields in human terms for authors filling out JSON by hand or from a worksheet.
For the generated machine-readable contract, see [`schema-reference.json`](schema-reference.json).
For validation commands and the full technical schema notes, see [JSON Fixture Schema Reference](input-schema.md).

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Authoring Model

A fixture is a static review packet. It describes one company, the date of the review, the latest source date represented by the packet, and optional notes, KPIs, and catalysts.

A fixture has three optional collections:

- `notes`: source excerpts or research notes that should be scored for language.
- `kpis`: numeric or labeled observations that should be shown alongside the review.
- `catalysts`: dated events or follow-up triggers.

Do not invent source names, publishers, URLs, dates, speaker labels, KPI values, or fiscal periods to make the fixture look complete.

## Top-Level Fields

| Field | Plain-English Meaning | Authoring Guidance |
| --- | --- | --- |
| `schema_version` | Which fixture shape this file was written for. | Use `0.1` for the current format when you include it. |
| `company` | The company name shown in reports and dashboards. | Required. Use the display name a reviewer will recognize. |
| `ticker` | The ticker or short company identifier. | Required. Use the public ticker when available; otherwise use a stable short label. |
| `as_of` | The date of this review. | Required. Use `YYYY-MM-DD`. This is the anchor date for stale/static-data checks. |
| `data_cutoff` | The newest source date represented in the fixture. | Required. Use `YYYY-MM-DD`. Do not set this later than the material actually reviewed. |
| `notes` | Text snippets or research notes to score. | Use an array of note objects. Use `[]` when there are no notes yet. |
| `kpis` | Metrics or operational observations to show in the review. | Use an array of KPI objects. Keep values as they appeared in source material. |
| `catalysts` | Dated future events or review reminders. | Use an array of catalyst objects. These should be events, not recommendations. |
| `source_attribution` | Source records that apply to the whole fixture. | Use this for the source bundle behind the file. Item-level source attribution can override or add detail. |

## Note Fields

| Field | Plain-English Meaning | Authoring Guidance |
| --- | --- | --- |
| `id` | A stable label for the note. | Useful for review comments and diffs. Keep it short, such as `n1` or `margin-qna-1`. |
| `date` | The date of the source text. | Use `YYYY-MM-DD`. If omitted, the tool falls back to `data_cutoff`. |
| `topic` | The section label for the note. | Use reviewer-friendly wording such as `demand`, `margin`, or `capital allocation`. |
| `type` | How the text should be treated. | Use values like `management_claim`, `analyst_question`, `user_synthesis`, `transcript_excerpt`, or `note`. |
| `text` | The actual language to score. | Paste only the static excerpt or authored note you want reviewed. Do not blend source text with your interpretation unless the type is `user_synthesis`. |
| `evidence_url` | A public URL supporting the note. | Leave blank or omit when unavailable; missing URLs are surfaced in the review queue. |
| `source_attribution` | Source record for this note. | Use when the note comes from a specific filing, transcript, presentation, or user-authored source. |

## KPI Fields

| Field | Plain-English Meaning | Authoring Guidance |
| --- | --- | --- |
| `name` | Metric name. | Use the label from the source when possible, such as `Revenue growth` or `Net retention`. |
| `value` | Metric value as reported. | Use a string for values with units, percentages, or ranges; a number is also accepted. |
| `direction` | Whether the movement reads positive or negative. | `up`, `better`, or `positive` adds opportunity weight. `down`, `worse`, or `negative` adds risk weight. |
| `date` | Date of the KPI observation. | Use `YYYY-MM-DD`. If omitted, the tool falls back to `data_cutoff`. |
| `observation` | Short context about the KPI. | Use this for source-grounded context, not a forecast or valuation call. |
| `evidence_url` | A public URL supporting the KPI. | Leave blank or omit when unavailable; missing URLs can be reviewed later. |
| `source_attribution` | Source record for this KPI. | Use when the KPI comes from a specific table, filing, deck, or user worksheet. |

## Catalyst Fields

| Field | Plain-English Meaning | Authoring Guidance |
| --- | --- | --- |
| `date` | Event or review-trigger date. | Use `YYYY-MM-DD`. The timeline sorts catalysts by this date. |
| `title` | Short event name. | Use a concise label such as `Investor day`, `Product launch`, or `Next earnings report`. |
| `description` | Why the event matters for review. | Describe what should be checked, not what an investor should do. |
| `expected_impact` | High-level risk/opportunity label. | Use neutral labels such as `risk review`, `opportunity review`, or `risk/opportunity review`. |
| `evidence_url` | A public URL supporting the catalyst. | Leave blank or omit when unavailable. |
| `source_attribution` | Source record for this catalyst. | Use when the catalyst came from an events page, filing, transcript, or user-authored plan. |

## Source Attribution Fields

| Field | Plain-English Meaning | Authoring Guidance |
| --- | --- | --- |
| `source_name` | Human-readable source label. | Example: `Q1 2026 earnings call transcript` or `FY2025 Form 10-K`. |
| `publisher` | Who published or supplied the source. | Example: a company name, `U.S. SEC EDGAR`, a transcript provider, or `User worksheet`. |
| `source_type` | Provenance category. | Use the closest allowed category from the generated schema, such as `company_investor_relations`, `sec_filing`, `transcript`, `shareholder_letter`, or `user_synthesis`. |
| `source_url` | Public URL for the static source. | The tool records the URL but does not fetch, refresh, or verify it. |
| `accessed_at` | Date the URL was checked by the fixture author. | Use `YYYY-MM-DD` only when the URL was actually checked. This is not the event date. |
| `static_notice` | A short boundary note. | Use to remind readers that the fixture is static, non-live, or source-limited. |

`source_attribution` can be one object or an array of objects. Each source record should include at least one supported field. Use item-level records when a note, KPI, or catalyst has a more specific source than the fixture-level bundle.

## Date Rules

Use exact calendar dates in YYYY-MM-DD format. Invalid dates such as 2026/05/15, 05-15-2026, or 2026-02-30 should be fixed before running the CLI.

## Extra Metadata

Additional properties are allowed for local metadata, but documented fields should be used for anything that affects reports, review queues, or snapshots.

## Minimal Starting Point

```json
{
  "schema_version": "0.1",
  "company": "Example Systems Inc.",
  "ticker": "EXM",
  "as_of": "2026-05-15",
  "data_cutoff": "2026-04-30",
  "notes": [],
  "kpis": [],
  "catalysts": []
}
```
