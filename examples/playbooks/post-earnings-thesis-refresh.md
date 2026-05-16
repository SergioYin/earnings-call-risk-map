# Post-Earnings Thesis Refresh Playbook

Use this playbook after an earnings call when the reviewer needs to update a thesis ledger or research memo from structured notes. The goal is to separate management claims, analyst questions, and user synthesis before deciding what source follow-up is needed.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## When To Use

- New earnings-call notes have been converted into a JSON fixture.
- The reviewer wants to refresh risks, opportunities, and catalysts without relying on live feeds.
- A thesis memo needs source-backed changes and explicit unresolved review items.

## Inputs

- Public-source case-study fixture: `examples/input/public_apple_static_case_study.json`
- Standard demo fixture: `examples/input/demo_company.json`
- Evidence policy: preserve source attribution records and static-data notices when using public company materials.

## Deterministic Steps

1. Analyze the post-earnings fixture.

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/public_apple_static_case_study.json --json-out examples/output/public_apple_static_case_study_snapshot.json --md-out examples/output/public_apple_static_case_study_report.md --html-out examples/output/public_apple_static_case_study_dashboard.html
```

2. Generate the post-earnings review queue.

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/public_apple_static_case_study.json --md-out examples/output/public_apple_static_case_study_review_queue.md --json-out examples/output/public_apple_static_case_study_review_queue.json
```

3. Refresh integration notes after the demo bundle is regenerated.

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

## Review Gates

- Confirm every thesis update points back to an evidence URL or an explicit missing-evidence review item.
- Preserve `Source Boundaries` language when copying excerpts into a thesis ledger.
- Treat static public-source examples as non-live data.
- Do not convert deterministic risk or opportunity scores into recommendations.

## Expected Artifacts

- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/integration_notes.json`

