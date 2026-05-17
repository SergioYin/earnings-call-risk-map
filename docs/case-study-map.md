# Case Study Map

Bundled fixtures are static, deterministic examples for local demos, tests, and documentation. Use this map to pick the fixture that best matches the review question before generating reports, dashboards, snapshots, or review queues.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Fixture Map

| Fixture | Target sector | Useful question | Generated artifacts |
| --- | --- | --- | --- |
| `examples/input/demo_company.json` | Software and enterprise platform | Which software risks need review after a mixed enterprise-demand and margin update? | `examples/output/demo_report.md`, `examples/output/demo_snapshot.json`, `examples/output/demo_review_queue.md`, `examples/output/demo_review_queue.json`, `examples/output/demo_review_queue_items.jsonl`, `examples/output/demo_dashboard.html` |
| `examples/input/demo_company_prior.json` | Software and enterprise platform prior-period baseline | What changed between the prior software baseline and the current demo company fixture? | `examples/output/demo_prior_report.md`, `examples/output/demo_prior_snapshot.json`, `examples/output/demo_compare.md`, `examples/output/demo_compare.json` |
| `examples/input/demo_energy_infrastructure.json` | Energy infrastructure, regulated assets, and large capital projects | Which project execution, financing, permitting, and backlog items deserve follow-up before the next infrastructure review? | `examples/output/energy_infrastructure_report.md`, `examples/output/energy_infrastructure_snapshot.json`, `examples/output/energy_infrastructure_review_queue.md`, `examples/output/energy_infrastructure_review_queue.json`, `examples/output/energy_infrastructure_dashboard.html` |
| `examples/input/consumer_hardware.json` | Consumer hardware and device supply chains | Which demand, channel, supply-chain, and revenue-growth items require reviewer attention in a hardware case study? | `examples/output/consumer_hardware_report.md`, `examples/output/consumer_hardware_snapshot.json`, `examples/output/consumer_hardware_review_queue.md`, `examples/output/consumer_hardware_review_queue.json`, `examples/output/consumer_hardware_dashboard.html` |
| `examples/input/semiconductor_equipment.json` | Semiconductor equipment and capital equipment cycles | How should reviewers triage net sales, gross margin, bookings, backlog, demand timing, and export-control risk in a semiconductor equipment case study? | `examples/output/semiconductor_equipment_report.md`, `examples/output/semiconductor_equipment_snapshot.json`, `examples/output/semiconductor_equipment_review_queue.md`, `examples/output/semiconductor_equipment_review_queue.json`, `examples/output/semiconductor_equipment_dashboard.html`, `examples/output/semiconductor_equipment_report/report.md`, `examples/output/semiconductor_equipment_report/dashboard/dashboard.html`, `examples/output/semiconductor_equipment_report/review_queue/review_queue.md`, `examples/output/semiconductor_equipment_report/review_queue/review_queue.json`, `examples/output/semiconductor_equipment_report/snapshot/snapshot.json`, `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md`, `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json` |
| `examples/input/public_apple_static_case_study.json` | Consumer hardware, services, and mega-cap public-source case study | Which static public-source Apple revenue, services, and risk-factor signals should be reviewed without treating the fixture as live analysis? | `examples/output/public_apple_static_case_study_report.md`, `examples/output/public_apple_static_case_study_snapshot.json`, `examples/output/public_apple_static_case_study_review_queue.md`, `examples/output/public_apple_static_case_study_review_queue.json`, `examples/output/public_apple_static_case_study_dashboard.html` |
| `examples/input/sample_filled_template_workflow.json` | Filled software template workflow | How does a completed blank template become a report, snapshot, and review queue for a software-style earnings review? | `examples/output/sample_filled_template_report.md`, `examples/output/sample_filled_template_snapshot.json`, `examples/output/sample_filled_template_review_queue.md`, `examples/output/sample_filled_template_review_queue.json` |

## Shared Generated Artifacts

The demo bundle also writes cross-fixture and documentation artifacts that are not owned by a single fixture:

- `examples/output/fixture_catalog.md`
- `examples/output/examples_index.md`
- `examples/output/examples_index.json`
- `examples/output/handoff_packet.md`
- `examples/output/handoff_packet.json`
- `examples/output/handoff_packet_examples.md`
- `examples/output/handoff_packet_examples.json`
- `examples/output/playbook_output_examples.md`
- `examples/output/playbook_output_examples.json`
- `examples/output/release_manifest.json`
- `examples/output/showcase_dashboard_preview.svg`

## Regenerate

Refresh the main case-study artifacts:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

Refresh the nested semiconductor equipment report bundle:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/semiconductor_equipment.json --json-out examples/output/semiconductor_equipment_report/snapshot/snapshot.json --md-out examples/output/semiconductor_equipment_report/report.md --html-out examples/output/semiconductor_equipment_report/dashboard/dashboard.html
```

For fixture metadata, see [Fixture Catalog](fixture-catalog.md). For static-source caveats, see [Case Study Limitations](case-study-limitations.md). For generated output discovery, see `examples/output/examples_index.md`.
