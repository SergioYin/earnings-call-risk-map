# Data Entry Checklist

Create a valid JSON fixture without hallucinating sources.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

- Source doc: `docs/data-entry-checklist.md`
- Sections: 4
- Field mappings: 9

## Field Mapping

| Fixture field | Use | No-hallucination rule |
| --- | --- | --- |
| `company` | Company name shown in the source packet. | Use the visible legal or display name; do not normalize from memory. |
| `ticker` | Ticker or short identifier used by the author. | If the source does not show a ticker, use the user's provided identifier. |
| `as_of` | Date of this review. | Use the actual authoring or review date in `YYYY-MM-DD`. |
| `data_cutoff` | Latest date represented by the source packet. | Use the latest transcript, filing, release, or note date that is present. |
| `notes[].type` | Provenance label for text. | Use `management_claim`, `analyst_question`, or `user_synthesis` based on who made the statement. |
| `notes[].text` | Short source excerpt or author note. | Preserve source meaning; do not add claims that are not present. |
| `kpis[].value` | KPI value as shown in source material. | Keep the source's units and wording; label any calculation as `user_synthesis`. |
| `evidence_url` | Public URL for the item. | Leave empty when no URL was actually captured. |
| `source_attribution` | Static provenance metadata. | Use only observed source details and allowed `source_type` values. |

## Before Entry

- Save the transcript or notes in a stable review location outside the fixture.
- Record the exact review date as `as_of`.
- Record the latest source date represented by the material as `data_cutoff`.
- Identify the source container: transcript, company investor-relations page, SEC filing, shareholder letter, press release, news article, or user synthesis.
- Keep a list of source URLs that were actually opened.

## Source Boundary Rules

- Do not invent source URLs, publishers, source names, accessed dates, speaker names, KPI values, or fiscal periods.
- Do not promote an analyst question into a company fact.
- Do not promote user summaries into source evidence.
- Use `accessed_at` only when the source URL was actually checked.
- Do not remove stale dates to avoid stale badges.

## Entry Steps

- Start from a valid template in `docs/templates.md`.
- Fill top-level `company`, `ticker`, `as_of`, and `data_cutoff`.
- Add top-level `source_attribution` only when source details are known.
- Split transcript content into `management_claim`, `analyst_question`, and `user_synthesis` notes.
- Add KPIs only when the source packet contains the exact KPI label and value.
- Add catalysts only when the date or event is present or clearly labeled as user synthesis.
- Keep blank `evidence_url` fields when evidence is missing.
- Run validation before committing the fixture.

## Final Review

- The fixture is valid JSON.
- `as_of`, `data_cutoff`, item `date`, and `accessed_at` dates are real calendar dates.
- Every `source_url` and `evidence_url` was actually captured from source material.
- Missing evidence remains blank and will be surfaced in the review queue.
- Management claims, analyst questions, and user synthesis are separated.
- Stale badges are preserved until sources are refreshed.
- The non-advice disclaimer is preserved in downstream Markdown, JSON, and handoff artifacts.

## Validation

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze path/to/fixture.json
PYTHONPATH=src python -m earnings_call_risk_map review-queue path/to/fixture.json
```
