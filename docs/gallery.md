# Gallery

The repository includes deterministic artifacts under `examples/output/` for quick inspection and downstream handoff tests.

## Contents

- [Dashboards](#dashboards)
- [Reports And Queues](#reports-and-queues)
- [Case Study Map](#case-study-map)
- [Compare Example](#compare-example)
- [Integration Examples](#integration-examples)
- [Promotion Page Assets](#promotion-page-assets)
- [Roadmap Use Cases](#roadmap-use-cases)

## Dashboards

- `examples/output/demo_dashboard.html`: compact software-style example dashboard.
- `examples/output/energy_infrastructure_dashboard.html`: capital-intensive energy/infrastructure example with project catalysts and stale/static data.
- `examples/output/public_apple_static_case_study_dashboard.html`: static public-source Apple case-study dashboard with source attribution and non-live-data labels.
- `examples/output/showcase_dashboard_preview.svg`: PNG-free static dashboard preview for release pages and screenshots.
- `docs/assets/showcase-dashboard-preview.svg`: documentation asset copy of the static dashboard preview.

See `docs/pages-demo.md` for local static HTML viewing and `docs/demo-screenshot-guide.md` for screenshot and README visual guidance.

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
- `examples/output/demo_review_queue_items.jsonl`: deterministic JSON Lines records for every review item across bundled demo fixtures, including fixture context for downstream review handoff.
- `examples/output/handoff_packet.md` and `examples/output/handoff_packet.json`: portfolio/thesis handoff packet summarizing report, review queue JSONL, compare paths, handoff targets, and cautions.
- `examples/output/handoff_packet_examples.md` and `examples/output/handoff_packet_examples.json`: deterministic handoff packet variants for quarterly review, catalyst check-in, and post-earnings thesis refresh.
- `examples/output/playbook_output_examples.md` and `examples/output/playbook_output_examples.json`: generated artifact inventory for each research playbook with regeneration and selfcheck commands.
- `examples/output/fixture_catalog.md`: bundled fixture catalog with tickers, data cutoffs, static/live status, and recommended commands.
- `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md` and `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json`: compact source-type, stale-badge, source-boundary, and count summaries for the semiconductor equipment fixture.
- `examples/output/risk_language_taxonomy.md`: generated Markdown taxonomy for deterministic score bands, high-impact language, stale or missing-evidence priority, and human review boundaries.
- `examples/output/template_catalog.md` and `examples/output/template_catalog.json`: reusable blank template catalog with recommended fields and starter commands.
- `examples/output/command_cheat_sheet.md` and `examples/output/command_cheat_sheet.json`: lightweight list of every public CLI command and its short purpose.

## Case Study Map

- `examples/output/case_study_map.md`: human-readable map from each bundled fixture to its target sector, useful reviewer question, and generated reports, dashboards, snapshots, and review queues.
- `examples/output/case_study_map.json`: machine-readable companion for docs, release checks, and downstream artifact discovery.
- `docs/case-study-map.md`: documentation page for how to use the fixture map alongside fixture catalogs and static-source limitations.

## Compare Example

The compare example uses `examples/input/demo_company_prior.json` as the earlier snapshot and `examples/input/demo_company.json` as the later snapshot. Positive risk or opportunity deltas mean the later snapshot triggered more deterministic keyword score for that topic; negative deltas mean less score. The interpretation section is a reading aid for reviewer triage, not a claim that the company's risk profile improved or worsened.

For a software-vs-energy infrastructure contrast, generate `examples/output/demo_snapshot.json` and `examples/output/energy_infrastructure_snapshot.json`, then run:

```bash
PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_snapshot.json examples/output/energy_infrastructure_snapshot.json --md-out examples/output/software_vs_energy_compare.md --json-out examples/output/software_vs_energy_compare.json
```

Treat this as a cross-fixture comparison of checked-in inputs. Higher or lower score movement can come from different domain language, source dates, project catalysts, capital intensity, missing evidence, or stale/static badges. It is not an investment ranking and should not be restated as buy, sell, hold, allocation, valuation, or sector-rotation advice.

## Integration Examples

- `examples/output/integration_notes.json`: static example notes showing how risk-map outputs can be handed to a thesis ledger or portfolio risk review without adding runtime dependencies on those tools.
- `examples/output/demo_review_queue_items.jsonl`: checklist handoff with one `review_queue_item` JSON object per line.
- `examples/output/handoff_packet.json`: deterministic packet for adjacent portfolio/thesis systems that need artifact paths plus source and non-advice cautions.
- `examples/output/handoff_packet_examples.json`: multiple packet examples for downstream systems that want playbook-specific routing samples.

## Promotion Page Assets

Use [Promotion Page Outline](promotion-page-outline.md) when preparing a public landing page, README badge link, or release-page description. It lists the dashboard, preview SVG, review queue, compare report, public static case-study report, handoff packet, and fixture map artifacts that are appropriate to screenshot.

Use [Demo Screenshot Guide](demo-screenshot-guide.md) to choose generated HTML, SVG, and Markdown artifacts for screenshots or README visuals without implying live data or investment advice.

- [examples/output/promotion_pack.md](../examples/output/promotion_pack.md): public promotion pack with quickstart commands, demo artifact links, proof commands, and non-advice boundaries.
- [examples/output/promotion_pack.json](../examples/output/promotion_pack.json): machine-readable companion for release pages, galleries, and downstream packaging checks.

## Roadmap Use Cases

For v0.7+ integration ideas, project boundaries, and star-worthy use cases, see [Roadmap](roadmap.md). The gallery artifacts are intended to support those use cases without adding live data, hosted services, or advice-producing workflows.
