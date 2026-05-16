# Research Playbooks

Available deterministic playbooks and their recommended local CLI sequence.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

| Playbook | Path | Purpose |
| --- | --- | --- |
| Quarterly Review | `examples/playbooks/quarterly-review.md` | Full quarter-end refresh from fixture validation through report, review queue, dashboard, and prior/current compare artifact. |
| Catalyst Check-In | `examples/playbooks/catalyst-check-in.md` | Focused event-date review that emphasizes catalysts, stale badges, and missing evidence before an upcoming milestone. |
| Post-Earnings Thesis Refresh | `examples/playbooks/post-earnings-thesis-refresh.md` | Post-call refresh that separates management claims, analyst questions, and user synthesis before updating a thesis ledger. |

## Recommended CLI Sequences

### Quarterly Review

- Slug: `quarterly-review`
- Source: `examples/playbooks/quarterly-review.md`

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --json-out examples/output/demo_snapshot.json --md-out examples/output/demo_report.md --html-out examples/output/demo_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company_prior.json --json-out examples/output/demo_prior_snapshot.json
PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json
```

Expected artifacts:
- `examples/output/demo_report.md`
- `examples/output/demo_snapshot.json`
- `examples/output/demo_review_queue.md`
- `examples/output/demo_compare.md`
- `examples/output/demo_dashboard.html`

### Catalyst Check-In

- Slug: `catalyst-check-in`
- Source: `examples/playbooks/catalyst-check-in.md`

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json --json-out examples/output/energy_infrastructure_snapshot.json --md-out examples/output/energy_infrastructure_report.md --html-out examples/output/energy_infrastructure_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_energy_infrastructure.json --md-out examples/output/energy_infrastructure_review_queue.md --json-out examples/output/energy_infrastructure_review_queue.json
PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl
```

Expected artifacts:
- `examples/output/energy_infrastructure_report.md`
- `examples/output/energy_infrastructure_review_queue.md`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/demo_review_queue_items.jsonl`

### Post-Earnings Thesis Refresh

- Slug: `post-earnings-thesis-refresh`
- Source: `examples/playbooks/post-earnings-thesis-refresh.md`

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/public_apple_static_case_study.json --json-out examples/output/public_apple_static_case_study_snapshot.json --md-out examples/output/public_apple_static_case_study_report.md --html-out examples/output/public_apple_static_case_study_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/public_apple_static_case_study.json --md-out examples/output/public_apple_static_case_study_review_queue.md --json-out examples/output/public_apple_static_case_study_review_queue.json
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

Expected artifacts:
- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/integration_notes.json`
