# Troubleshooting

Use this guide when a fixture fails before scoring, a report shows unexpected review items, or a compare report looks larger than expected. The tool is deterministic and local-only, so most issues come from fixture shape, dates, evidence fields, or interpreting score deltas as facts instead of review prompts.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials before relying on any output.

## Validation Errors

Validation errors are raised before scoring. They include a fixture label plus the field path that failed, so fix the named field first and rerun the same command.

Common examples:

```text
error: fixture.company must be a non-empty string
error: fixture.as_of must use YYYY-MM-DD format, got '2026/05/15'
error: fixture.data_cutoff must be a valid calendar date, got '2026-02-30'
error: fixture.notes[0].date must use YYYY-MM-DD format, got '04-30-2026'
error: fixture.kpis[0].source_attribution[0].accessed_at must use YYYY-MM-DD format, got '05-15-2026'
error: fixture.catalysts[0].source_attribution must be a JSON object or list
```

Fixes:

- Keep `company`, `ticker`, `as_of`, and `data_cutoff` present and non-empty.
- Use real calendar dates in `YYYY-MM-DD` form for `as_of`, `data_cutoff`, item `date`, and source-attribution `accessed_at`.
- Keep `notes`, `kpis`, and `catalysts` as arrays of JSON objects when supplied.
- Keep `source_attribution` as either a JSON object or an array of JSON objects.

For the full accepted shape, see [JSON Fixture Schema Reference](input-schema.md).

## Stale Badges

A `stale>90d` badge means an item date is more than 90 days older than the fixture `as_of` date. It does not prove the underlying issue is still active; it means the source is old enough to require review.

Example:

```json
{
  "as_of": "2026-05-15",
  "data_cutoff": "2026-04-30",
  "kpis": [
    {
      "name": "Inventory days",
      "date": "2025-12-31",
      "evidence_url": "https://example.com/exm/static-kpi"
    }
  ]
}
```

The field path to inspect is `fixture.kpis[0].date`. Update the date only when the source itself is newer. If the source is intentionally static, leave the date as-is and treat the badge as a review reminder.

## Missing Evidence

Missing or blank `evidence_url` values enter the review queue. This is intentional: it keeps unsourced notes, KPI observations, and catalyst claims visible instead of silently dropping them.

Example:

```json
{
  "notes": [
    {
      "id": "n1",
      "date": "2026-04-30",
      "topic": "product launch",
      "text": "Launch timing could improve expansion pipeline.",
      "evidence_url": ""
    }
  ]
}
```

The field path to inspect is `fixture.notes[0].evidence_url`. Add a public source URL when available. If the note is user synthesis with no source yet, leave it empty and use the review queue to track follow-up.

Catalysts use the same rule:

```json
{
  "catalysts": [
    {
      "date": "2026-08-05",
      "title": "Next earnings report",
      "expected_impact": "risk validation"
    }
  ]
}
```

The field path to inspect is `fixture.catalysts[0].evidence_url`.

## Compare Interpretation

`compare` reads two analyzed snapshots, not raw input fixtures:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company_prior.json --json-out before.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --json-out after.json
PYTHONPATH=src python -m earnings_call_risk_map compare before.json after.json --md-out compare.md --json-out compare.json
```

Positive deltas mean the later snapshot triggered more deterministic keyword score for that topic. Negative deltas mean it triggered less score. Deltas are reviewer triage signals, not claims that the business risk or opportunity changed in the real world.

When a compare report shows a review workload increase, inspect the later fixture fields that can create review items:

- stale badges: `fixture.notes[*].date`, `fixture.kpis[*].date`, and `fixture.as_of`
- missing evidence: `fixture.notes[*].evidence_url`, `fixture.kpis[*].evidence_url`, and `fixture.catalysts[*].evidence_url`
- high-impact language: `fixture.notes[*].text`, `fixture.kpis[*].observation`, and catalyst descriptions that contain stronger risk or opportunity terms

If the compare report says "Stale/static badge count increased", verify whether older source dates are intentional before changing them.
