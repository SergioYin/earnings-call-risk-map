# Agent Workflow

Route generic coding or research agents through deterministic local CLI commands while preserving source attribution, stale/static warnings, human review queues, and non-advice boundaries.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

- Source doc: `docs/agent-workflow.md`
- Routes: 4

## Routing Map

Choose the narrowest route that answers the user's request. For a complete review bundle, run:

1. analyze
2. review-queue
3. compare when prior/current snapshots exist
4. summarize with source attribution

## Analyze Route

Use when the user provides one raw input fixture or asks for a report, dashboard, or snapshot.

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze input.json --json-out snapshot.json --md-out report.md
```

Agent checks:
- `safety_notice`
- `source_boundaries`
- risk and opportunity scores
- stale/static badges
- review queue count
- evidence URLs and source attribution records

## Compare Route

Use when the user provides two analyzed JSON snapshots or asks what changed between reviews.

```bash
PYTHONPATH=src python -m earnings_call_risk_map compare before.json after.json --json-out compare.json --md-out compare.md
```

Agent checks:
- before and after snapshot dates
- comparison scope
- risk and opportunity score deltas
- interpretation text that describes review attention, not real-world company quality

## Review Queue Route

Use when the user asks what needs checking, evidence cleanup, stale-data review, or handoff.

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue input.json --json-out review_queue.json --md-out review_queue.md
```

Agent checks:
- stale or unverified dates
- missing evidence URLs
- high-impact language
- visible review reasons for every queued item

## Source Attribution Route

Use whenever an answer repeats or summarizes source-backed content from a fixture.

Agent checks:
- source name
- publisher
- source type
- source URL
- access date
- `as_of` and `data_cutoff`
- static-data notice

## Source Boundaries

- Management claims are source-provided company statements or prepared remarks.
- Analyst questions are source-provided questions or prompts; they are not assertions.
- User synthesis covers user-authored notes, labels, tags, and deterministic scoring output.

## Handoff Checklist

- Confirm the output includes the educational research boundary.
- Confirm source boundaries are preserved.
- Confirm stale/static badges are still visible.
- Confirm missing evidence and high-impact language remain in the review queue.
- Confirm compare language describes scoring movement, not a recommendation.
- Confirm cited source attribution uses fixture records and does not imply live-data freshness.

## Stop Boundaries

- Do not fetch or refresh live market data unless the user explicitly changes scope and provides an approved method.
- Do not verify source URLs by network access as part of this local-only workflow.
- Do not create price targets, ratings, forecasts, expected returns, allocations, or trade instructions.
- Do not recommend buy, sell, hold, short, reduce, add, underweight, or overweight actions.
- Do not remove stale/static warnings, missing-evidence reasons, or safety notices.
