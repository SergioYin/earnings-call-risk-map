# JSON Fixture Schema Reference

The input fixture is a single JSON object used by `earnings-call-risk-map analyze`.
The CLI validates the top-level contract before scoring so fixture mistakes fail with readable errors.

## Top-Level Object

Required fields:

| Field | Type | Format | Description |
| --- | --- | --- | --- |
| `company` | string | non-empty | Company display name used in reports. |
| `ticker` | string | non-empty | Public ticker or short identifier. |
| `as_of` | string | `YYYY-MM-DD` | Review date used for stale/static-data comparisons. |
| `data_cutoff` | string | `YYYY-MM-DD` | Latest source-data date represented by the fixture. |

Optional fields:

| Field | Type | Description |
| --- | --- | --- |
| `schema_version` | string | Fixture schema version, currently `0.1` when provided. |
| `notes` | array | Transcript excerpts or research notes. |
| `kpis` | array | KPI observations. |
| `catalysts` | array | Dated future events or review triggers. |
| `source_attribution` | object or array | Optional public-source attribution records for the fixture. These are rendered in reports and preserved in snapshots. |

## Source Attribution

`source_attribution` can be supplied at the top level and on individual notes, KPIs, and catalysts. It is intended for public investor-relations, SEC, transcript, or user-authored source labels. It does not make the data live or verified; it records where the static fixture says the item came from.

Supported fields:

| Field | Type | Description |
| --- | --- | --- |
| `source_name` | string | Human-readable source label. |
| `publisher` | string | Publisher or source system, such as a company name or `U.S. SEC EDGAR`. |
| `source_type` | string | Provenance class, such as `company_investor_relations`, `sec_filing`, `transcript`, or `user_synthesis`. |
| `source_url` | string | Public URL for the source. |
| `accessed_at` | string | Date the static fixture author recorded the source URL. |
| `static_notice` | string | Short label clarifying that the fixture is static and not live data. |

## Notes

Each item in `notes` must be a JSON object. Supported fields:

| Field | Type | Format | Description |
| --- | --- | --- | --- |
| `id` | string | optional | Stable note identifier. |
| `date` | string | `YYYY-MM-DD` when present | Source date. Falls back to `data_cutoff` if omitted. |
| `topic` | string | optional | Topic label used in report sections. |
| `type` | string | optional | Note provenance, such as `management_claim`, `analyst_question`, `user_synthesis`, `transcript_excerpt`, or `note`. |
| `text` | string | optional | Text scored for risk and opportunity keywords. |
| `evidence_url` | string | optional | Public source URL. Missing URLs enter the review queue. |
| `source_attribution` | object or array | optional | Public-source attribution rendered with the item. |

Recommended provenance values:

- `management_claim`: company-provided statements or prepared remarks. These should be verified against source filings or transcripts.
- `analyst_question`: analyst prompts or Q&A questions. The tool keeps them separate from factual claims.
- `user_synthesis`: user-authored notes, summaries, and tags. These are review aids and not financial advice.

## KPIs

Each item in `kpis` must be a JSON object. Supported fields:

| Field | Type | Format | Description |
| --- | --- | --- | --- |
| `name` | string | optional | KPI label. |
| `value` | string or number | optional | KPI value as shown in source material. |
| `direction` | string | optional | `up`, `better`, or `positive` adds opportunity weight; `down`, `worse`, or `negative` adds risk weight. |
| `date` | string | `YYYY-MM-DD` when present | KPI observation date. Falls back to `data_cutoff` if omitted. |
| `observation` | string | optional | Text scored alongside the KPI name and direction. |
| `evidence_url` | string | optional | Public source URL. |
| `source_attribution` | object or array | optional | Public-source attribution rendered with the KPI. |

## Catalysts

Each item in `catalysts` must be a JSON object. Supported fields:

| Field | Type | Format | Description |
| --- | --- | --- | --- |
| `date` | string | `YYYY-MM-DD` when present | Catalyst date used for timeline sorting. |
| `title` | string | optional | Catalyst title. |
| `description` | string | optional | Context for the event or review trigger. |
| `expected_impact` | string | optional | Expected risk/opportunity impact label. |
| `evidence_url` | string | optional | Public source URL. |
| `source_attribution` | object or array | optional | Public-source attribution rendered with the catalyst. |

## Date Validation

Dates must be strings shaped exactly as `YYYY-MM-DD` and must be valid calendar dates.
For example, `2026-05-15` is valid, while `2026/05/15`, `05-15-2026`, and `2026-02-30` are rejected.

The validator reports the field path in the error, such as:

```text
error: examples/input/bad.json.as_of must use YYYY-MM-DD format, got '2026/05/15'
error: examples/input/bad.json.notes[0].date must use YYYY-MM-DD format, got '04-30-2026'
```

## Minimal Fixture

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
