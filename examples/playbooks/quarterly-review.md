# Quarterly Review Playbook

Use this playbook when refreshing a company research packet at quarter end. The goal is a deterministic report, focused review queue, dashboard, and prior/current compare artifact that a reviewer can inspect against source documents.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## When To Use

- A quarterly earnings call or investor update has been transcribed into a fixture.
- Prior-period notes exist and can be compared against the current fixture.
- The reviewer needs a reproducible bundle for discussion, not a recommendation.

## Inputs

- Current fixture: `examples/input/demo_company.json`
- Prior fixture or snapshot: `examples/input/demo_company_prior.json`
- Evidence policy: every material note, KPI, and catalyst should include a date and evidence URL when available.

## Deterministic Steps

1. Refresh the demo outputs.

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

2. Generate the current report, JSON snapshot, and static dashboard.

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --json-out examples/output/demo_snapshot.json --md-out examples/output/demo_report.md --html-out examples/output/demo_dashboard.html
```

3. Generate a focused review queue.

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json
```

4. Compare prior and current snapshots.

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company_prior.json --json-out examples/output/demo_prior_snapshot.json
PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json
```

## Review Gates

- Confirm the report includes the non-advice notice and `Source Boundaries`.
- Resolve or explicitly carry every stale/static data badge.
- Check the review queue for missing evidence and high-impact language.
- Treat compare deltas as attention changes in deterministic scoring, not factual changes in the business.

## Expected Artifacts

- `examples/output/demo_report.md`
- `examples/output/demo_snapshot.json`
- `examples/output/demo_review_queue.md`
- `examples/output/demo_compare.md`
- `examples/output/demo_dashboard.html`

