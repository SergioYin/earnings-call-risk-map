# Fixture Summary

`fixture-summary` prints a compact Markdown or JSON audit of one input fixture before a user reads the full report. It is intended for cold-user onboarding: a new reviewer can confirm what kind of source material is present, how much stale data exists, and whether the fixture has enough notes, KPIs, catalysts, and attribution records to continue.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## When To Use It

Run `fixture-summary` after choosing or filling a fixture and before treating the analysis report as review-ready.

Use it to answer first-run questions:

- Which company, ticker, `as_of`, and `data_cutoff` did this file declare?
- How many notes, KPIs, catalysts, risks, opportunities, review-queue items, stale badges, and source attribution records are present?
- Which `source_type` values appear in the fixture?
- Which items are `current`, `stale>90d`, or `date-unverified`?
- Are the source-boundary labels for management claims, analyst questions, and user synthesis visible before handoff?

This helps a cold user inspect fixture shape and source coverage without starting from a long dashboard or full report.

## Command

Print Markdown:

```bash
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary examples/input/semiconductor_equipment.json
```

Write Markdown:

```bash
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary \
  examples/input/semiconductor_equipment.json \
  --out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md
```

Write JSON:

```bash
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary \
  examples/input/semiconductor_equipment.json \
  --format json \
  --out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json
```

The generated demo bundle includes both:

- `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md`
- `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json`

## Output Sections

Markdown output includes:

- `Counts`: note, KPI, catalyst, risk, opportunity, review queue, stale badge, and source-attribution totals.
- `Source Types`: counts by `source_type`, such as `company_investor_relations`, `sec_filing`, `transcript`, or `user_synthesis`.
- `Stale Badges`: item IDs, topics, freshness status, age in days, and badge labels.
- `Source Boundaries`: the same management-claim, analyst-question, and user-synthesis definitions used by reports.

JSON output uses `artifact_type: "fixture_summary"` and includes the same fields in machine-readable form for onboarding checks or release evidence.

## Cold-User Onboarding Flow

For a first run, pair `fixture-summary` with the first 30 minutes workflow:

1. Use [Earnings Review Templates](templates.md) or `template-catalog` to choose a starting fixture.
2. Fill required fields and a small set of source-backed notes as described in [Tutorial: First 30 Minutes](tutorial-first-30-minutes.md).
3. Run `fixture-summary` to confirm source types, stale badges, and counts before reading the full report.
4. Run `analyze` and `review-queue` only after the fixture summary matches the intended source coverage.
5. Use [Troubleshooting](troubleshooting.md) when counts, missing evidence, or stale badge status do not match expectations.

The command does not replace `analyze`. It is a shorter checkpoint for source coverage and fixture freshness before the reviewer spends time on the full report, dashboard, or handoff packet.

## Related Docs

- [Fixture Catalog](fixture-catalog.md) lists bundled fixtures, tickers, data cutoffs, and recommended commands.
- [Source Attribution Guide](source-attribution-guide.md) explains `source_type`, `accessed_at`, stale badges, and provenance boundaries.
- [Input Schema](input-schema.md) documents required fixture fields and validation behavior.
- [Usage](usage.md) lists every CLI command.
