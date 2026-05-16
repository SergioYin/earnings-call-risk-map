# Gallery

The repository includes deterministic artifacts under `examples/output/` for quick inspection and downstream handoff tests.

## Dashboards

- `examples/output/demo_dashboard.html`: compact software-style example dashboard.
- `examples/output/energy_infrastructure_dashboard.html`: capital-intensive energy/infrastructure example with project catalysts and stale/static data.
- `examples/output/public_apple_static_case_study_dashboard.html`: static public-source Apple case-study dashboard with source attribution and non-live-data labels.
- `examples/output/showcase_dashboard_preview.svg`: PNG-free static dashboard preview for release pages and screenshots.
- `docs/assets/showcase-dashboard-preview.svg`: documentation asset copy of the static dashboard preview.

See `docs/pages-demo.md` for local static HTML viewing and screenshot framing guidance.

## Reports And Queues

- `examples/output/demo_report.md` and `examples/output/energy_infrastructure_report.md`: Markdown research review reports.
- `examples/output/demo_prior_report.md`: prior-period software fixture report used by the compare example.
- `examples/output/public_apple_static_case_study_report.md`: Markdown report for the static public-source case study.
- `examples/output/demo_compare.md`: Markdown compare report for `demo_company_prior` versus `demo_company`, including a "How To Read This Compare" interpretation section.
- `examples/output/demo_review_queue.md` and `examples/output/energy_infrastructure_review_queue.md`: focused human-review queues.
- `examples/output/public_apple_static_case_study_review_queue.md`: focused review queue for the static public-source case study.
- `examples/output/demo_snapshot.json` and `examples/output/energy_infrastructure_snapshot.json`: full machine-readable snapshots.
- `examples/output/demo_prior_snapshot.json`: analyzed prior-period snapshot used as the compare baseline.
- `examples/output/public_apple_static_case_study_snapshot.json`: full machine-readable static case-study snapshot.
- `examples/output/demo_compare.json`: machine-readable score deltas and interpretation lines for the prior/current software comparison.
- `examples/output/demo_review_queue.json` and `examples/output/energy_infrastructure_review_queue.json`: focused machine-readable review queues.
- `examples/output/public_apple_static_case_study_review_queue.json`: focused machine-readable static case-study review queue.

## Compare Example

The compare example uses `examples/input/demo_company_prior.json` as the earlier snapshot and `examples/input/demo_company.json` as the later snapshot. Positive risk or opportunity deltas mean the later snapshot triggered more deterministic keyword score for that topic; negative deltas mean less score. The interpretation section is a reading aid for reviewer triage, not a claim that the company's risk profile improved or worsened.

## Integration Examples

- `examples/output/integration_notes.json`: static example notes showing how risk-map outputs can be handed to a thesis ledger or portfolio risk review without adding runtime dependencies on those tools.
