# Data Entry Checklist

Use this checklist when converting an earnings transcript, prepared remarks, Q&A notes, filing excerpts, or reviewer notes into a JSON fixture.

> Educational research review only. This checklist does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. It is an authoring aid for static fixtures; verify source materials before relying on any output.

## Goal

Create a valid JSON fixture without hallucinating sources.

The fixture author should copy only source details that are visible in the transcript, notes, filing, release, or reviewer worksheet in front of them. If a URL, publisher, date, speaker role, KPI value, or evidence link is missing, leave it blank or mark it as user synthesis instead of inventing it.

## Before Entry

- Save the transcript or notes in a stable review location outside the fixture.
- Record the exact review date as `as_of`.
- Record the latest source date represented by the material as `data_cutoff`.
- Identify the source container: transcript, company investor-relations page, SEC filing, shareholder letter, press release, news article, or user synthesis.
- Keep a list of source URLs that were actually opened. Do not add source URLs from memory, search snippets, or likely investor-relations paths.

## Source Boundary Rules

- Do not invent `source_url`, `publisher`, `source_name`, `accessed_at`, speaker names, KPI values, dates, or fiscal periods.
- Do not promote an analyst question into a company fact.
- Do not promote user summaries into source evidence.
- Do not rewrite uncertain notes as verified claims. Use `user_synthesis` and describe the uncertainty.
- Do not fill missing `evidence_url` just to clear the review queue. Missing evidence should remain visible.
- Use `accessed_at` only when the source URL was actually checked. Do not use today's date merely because the fixture was edited or regenerated.
- Do not remove stale dates to avoid stale badges.

## Field Mapping

| Fixture field | Use | No-hallucination rule |
| --- | --- | --- |
| `company` | Company name shown in the source packet. | Use the visible legal or display name; do not normalize from memory. |
| `ticker` | Ticker or short identifier used by the author. | If the source does not show a ticker, use the user's provided identifier. |
| `as_of` | Date of this review. | Use the actual authoring/review date in `YYYY-MM-DD`. |
| `data_cutoff` | Latest date represented by the source packet. | Use the latest transcript, filing, release, or note date that is present. |
| `notes[].type` | Provenance label for text. | Use `management_claim`, `analyst_question`, or `user_synthesis` based on who made the statement. |
| `notes[].text` | Short source excerpt or author note. | Preserve source meaning; do not add claims that are not present. |
| `kpis[].value` | KPI value as shown in source material. | Keep the source's units and wording; do not calculate new metrics unless labeled as `user_synthesis`. |
| `evidence_url` | Public URL for the item. | Leave empty when no URL was actually captured. |
| `source_attribution` | Static provenance metadata. | Use only observed source details and allowed `source_type` values. |

## Entry Steps

1. Start from a valid template in [Earnings Review Templates](templates.md) or the minimal example below.
2. Fill top-level `company`, `ticker`, `as_of`, and `data_cutoff`.
3. Add top-level `source_attribution` for the source packet only when the source details are known.
4. Split transcript content by role:
   - management statements become `management_claim`;
   - analyst questions become `analyst_question`;
   - reviewer interpretation becomes `user_synthesis`.
5. Add KPIs only when the transcript, filing, release, or notes contain the exact KPI label and value.
6. Add catalysts only when the date or event is present in the source packet or clearly labeled as user synthesis.
7. Keep blank `evidence_url` fields when evidence is missing.
8. Run validation before committing the fixture.

## Minimal Valid Example

This example is intentionally generic. Replace values only with details visible in your source packet.

```json
{
  "schema_version": "0.1",
  "company": "Example Systems Inc.",
  "ticker": "EXM",
  "as_of": "2026-05-16",
  "data_cutoff": "2026-05-10",
  "source_attribution": {
    "source_name": "Q1 earnings call transcript",
    "publisher": "Example Systems Investor Relations",
    "source_type": "transcript",
    "source_url": "https://example.com/investors/q1-transcript",
    "accessed_at": "2026-05-16",
    "static_notice": "Static transcript reference supplied by fixture author; verify against current source materials."
  },
  "notes": [
    {
      "id": "note-1",
      "date": "2026-05-10",
      "topic": "demand",
      "type": "management_claim",
      "text": "Management said enterprise demand remained steady during the quarter.",
      "evidence_url": "https://example.com/investors/q1-transcript"
    },
    {
      "id": "note-2",
      "date": "2026-05-10",
      "topic": "retention",
      "type": "analyst_question",
      "text": "An analyst asked whether retention could weaken if renewals slow.",
      "evidence_url": "https://example.com/investors/q1-transcript"
    },
    {
      "id": "note-3",
      "date": "2026-05-16",
      "topic": "review follow-up",
      "type": "user_synthesis",
      "text": "User synthesis: verify whether renewal commentary is supported by the latest filing.",
      "evidence_url": ""
    }
  ],
  "kpis": [],
  "catalysts": []
}
```

## Validation

Run the same parser used by the CLI:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze path/to/fixture.json
```

For a quieter syntax and schema check:

```bash
PYTHONPATH=src python - <<'PY'
from earnings_call_risk_map.io import read_json

read_json("path/to/fixture.json")
print("valid")
PY
```

Validation confirms required top-level fields, JSON object shape, date formats, list fields, item objects, evidence URL types, and source-attribution records. It cannot verify whether a source exists or whether a transcript was copied accurately; that remains a human review responsibility.

## Final Review

- The fixture is valid JSON.
- `as_of`, `data_cutoff`, item `date`, and `accessed_at` dates are real calendar dates.
- Every `source_url` and `evidence_url` was actually captured from source material.
- Missing evidence remains blank and will be surfaced in the review queue.
- Management claims, analyst questions, and user synthesis are separated.
- Stale badges are preserved until sources are refreshed.
- The non-advice disclaimer is preserved in downstream Markdown, JSON, and handoff artifacts.

See [JSON Fixture Schema Reference](input-schema.md), [Source Attribution Guide](source-attribution-guide.md), [Troubleshooting](troubleshooting.md), and [Non-Advice Boundary](non-advice-boundary.md) for the surrounding rules.
