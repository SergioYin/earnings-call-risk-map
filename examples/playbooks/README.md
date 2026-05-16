# Research Playbooks

These deterministic playbooks describe repeatable research review workflows using only checked-in fixtures and local CLI outputs. They are templates for organizing source review, not investment advice, forecasts, or buy/sell/hold recommendations.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

Each playbook uses the same local-only boundary as the rest of the project:

- Run commands from a checkout with `PYTHONPATH=src`.
- Use bundled JSON fixtures or reviewer-authored fixtures with explicit dates and evidence URLs.
- Treat scores, stale badges, and review queues as triage prompts.
- Verify source documents before changing a thesis, memo, or research note.

## Available Playbooks

- [Quarterly Review](quarterly-review.md): full quarter-end refresh from fixture validation through report, review queue, dashboard, and compare artifact.
- [Catalyst Check-In](catalyst-check-in.md): focused event-date review that emphasizes catalysts, stale badges, and missing evidence before an upcoming milestone.
- [Post-Earnings Thesis Refresh](post-earnings-thesis-refresh.md): post-call refresh that separates management claims, analyst questions, and user synthesis before updating a thesis ledger.

## Deterministic Inputs And Outputs

The playbooks intentionally reference stable example paths:

- `examples/input/demo_company.json`
- `examples/input/demo_company_prior.json`
- `examples/input/demo_energy_infrastructure.json`
- `examples/input/public_apple_static_case_study.json`
- `examples/output/demo_report.md`
- `examples/output/demo_review_queue.md`
- `examples/output/demo_compare.md`
- `examples/output/demo_dashboard.html`

Run `PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output` to refresh the bundled outputs before following a playbook.
