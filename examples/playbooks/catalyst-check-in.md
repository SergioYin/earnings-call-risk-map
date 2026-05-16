# Catalyst Check-In Playbook

Use this playbook for a focused pre-event review before an upcoming product, regulatory, capacity, financing, or operating milestone. The goal is to isolate catalyst dates, evidence gaps, and stale context before a reviewer updates a watchlist or meeting agenda.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## When To Use

- A catalyst date is approaching and the reviewer needs a narrow source-check workflow.
- The fixture contains dated catalysts or KPI observations that may now be stale.
- The reviewer wants a deterministic queue before reading source filings, transcripts, or releases.

## Inputs

- Catalyst-heavy fixture: `examples/input/demo_energy_infrastructure.json`
- Optional public-source attribution example: `examples/input/public_apple_static_case_study.json`
- Evidence policy: catalyst descriptions should include a date, expected impact text, and evidence URL when available.

## Deterministic Steps

1. Build the catalyst-heavy report.

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json --json-out examples/output/energy_infrastructure_snapshot.json --md-out examples/output/energy_infrastructure_report.md --html-out examples/output/energy_infrastructure_dashboard.html
```

2. Export only the review items.

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_energy_infrastructure.json --md-out examples/output/energy_infrastructure_review_queue.md --json-out examples/output/energy_infrastructure_review_queue.json
```

3. Build cross-fixture JSON Lines for checklist handoff.

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl
```

## Review Gates

- Sort catalyst dates against the fixture `as_of` date and flag any expired milestone.
- Check whether stale KPI context is still relevant to the catalyst.
- Escalate missing evidence URLs before discussing expected impact.
- Keep source-provided management claims separate from user-authored synthesis.

## Expected Artifacts

- `examples/output/energy_infrastructure_report.md`
- `examples/output/energy_infrastructure_review_queue.md`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/demo_review_queue_items.jsonl`
