# Examples Index

Bundled examples are local deterministic fixtures, templates, and generated artifacts.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Summary

- Fixtures: 7
- Templates: 3
- Generated outputs: 75
- Recommended next command: `earnings-call-risk-map demo --out-dir examples/output`

## Bundled Fixtures

| Fixture | Ticker | Data cutoff | Status | Recommended next command |
| --- | --- | --- | --- | --- |
| `examples/input/demo_company.json` | `EXM` | `2026-04-30` | static demo fixture | `earnings-call-risk-map analyze examples/input/demo_company.json` |
| `examples/input/demo_energy_infrastructure.json` | `NGLP` | `2026-04-25` | static demo fixture | `earnings-call-risk-map analyze examples/input/demo_energy_infrastructure.json` |
| `examples/input/consumer_hardware.json` | `LOGI` | `2024-04-29` | static public-source consumer hardware fixture | `earnings-call-risk-map analyze examples/input/consumer_hardware.json` |
| `examples/input/semiconductor_equipment.json` | `ASML` | `2025-01-29` | static public-source semiconductor equipment fixture | `earnings-call-risk-map analyze examples/input/semiconductor_equipment.json` |
| `examples/input/public_apple_static_case_study.json` | `AAPL` | `2024-05-02` | static public-source case study | `earnings-call-risk-map analyze examples/input/public_apple_static_case_study.json` |
| `examples/input/demo_company_prior.json` | `EXM` | `2026-01-31` | static compare baseline | `earnings-call-risk-map analyze examples/input/demo_company_prior.json --json-out examples/output/demo_prior_snapshot.json --md-out examples/output/demo_prior_report.md` |
| `examples/input/sample_filled_template_workflow.json` | `NWA` | `2026-05-10` | static filled-template workflow fixture | `earnings-call-risk-map analyze examples/input/sample_filled_template_workflow.json` |

## Templates

| Template | Path | Purpose | Recommended next command |
| --- | --- | --- | --- |
| Software Earnings Review | `examples/templates/software_earnings_review.json` | SaaS, cloud, platform, or other software earnings review starting point. | `earnings-call-risk-map analyze examples/templates/software_earnings_review.json` |
| Energy Infrastructure Earnings Review | `examples/templates/energy_infrastructure_earnings_review.json` | Capital-intensive utility, energy infrastructure, project, or regulated-asset review starting point. | `earnings-call-risk-map analyze examples/templates/energy_infrastructure_earnings_review.json` |
| Consumer Hardware Earnings Review | `examples/templates/consumer_hardware_earnings_review.json` | Device, channel inventory, product launch, supply chain, or warranty review starting point. | `earnings-call-risk-map analyze examples/templates/consumer_hardware_earnings_review.json` |

## Generated Outputs

| Output | Format | Artifact group | Recommended next command |
| --- | --- | --- | --- |
| `examples/output/agent_workflow.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/agent_workflow.md` | `md` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/case_study_map.json` | `json` | case study map | `earnings-call-risk-map case-study-map --format json --out examples/output/case_study_map.json` |
| `examples/output/case_study_map.md` | `md` | case study map | `earnings-call-risk-map case-study-map --format markdown --out examples/output/case_study_map.md` |
| `examples/output/command_cheat_sheet.json` | `json` | command cheat sheet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/command_cheat_sheet.md` | `md` | command cheat sheet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/command_cheatsheet.json` | `json` | command cheat sheet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/command_cheatsheet.md` | `md` | command cheat sheet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/consumer_hardware_dashboard.html` | `html` | dashboard | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/consumer_hardware_report.md` | `md` | markdown report | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/consumer_hardware_review_queue.json` | `json` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/consumer_hardware_review_queue.md` | `md` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/consumer_hardware_snapshot.json` | `json` | analyzed snapshot | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/data_entry_checklist.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/data_entry_checklist.md` | `md` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_compare.json` | `json` | snapshot compare | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_compare.md` | `md` | snapshot compare | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_dashboard.html` | `html` | dashboard | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_prior_report.md` | `md` | markdown report | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_prior_snapshot.json` | `json` | analyzed snapshot | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_report.md` | `md` | markdown report | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_review_queue.json` | `json` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_review_queue.md` | `md` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_review_queue_items.jsonl` | `jsonl` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_screenshot_guide.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_screenshot_guide.md` | `md` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/demo_snapshot.json` | `json` | analyzed snapshot | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/doctor.json` | `json` | doctor | `earnings-call-risk-map doctor --format json --out examples/output/doctor.json` |
| `examples/output/doctor.md` | `md` | doctor | `earnings-call-risk-map doctor --format markdown --out examples/output/doctor.md` |
| `examples/output/energy_infrastructure_dashboard.html` | `html` | dashboard | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/energy_infrastructure_report.md` | `md` | markdown report | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/energy_infrastructure_review_queue.json` | `json` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/energy_infrastructure_review_queue.md` | `md` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/energy_infrastructure_snapshot.json` | `json` | analyzed snapshot | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/examples_index.json` | `json` | generated output | `earnings-call-risk-map examples-index --format json --out examples/output/examples_index.json` |
| `examples/output/examples_index.md` | `md` | generated output | `earnings-call-risk-map examples-index --format markdown --out examples/output/examples_index.md` |
| `examples/output/fixture_catalog.md` | `md` | catalog | `earnings-call-risk-map fixture-catalog --out examples/output/fixture_catalog.md` |
| `examples/output/fresh_clone_plan.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/fresh_clone_plan.md` | `md` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/handoff_packet.json` | `json` | handoff packet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/handoff_packet.md` | `md` | handoff packet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/handoff_packet_examples.json` | `json` | handoff packet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/handoff_packet_examples.md` | `md` | handoff packet | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/integration_notes.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/package_audit.json` | `json` | audit | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/package_audit.md` | `md` | audit | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/playbook_output_examples.json` | `json` | playbook | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/playbook_output_examples.md` | `md` | playbook | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/playbooks.json` | `json` | playbook | `earnings-call-risk-map playbooks --format json --out examples/output/playbooks.json` |
| `examples/output/playbooks.md` | `md` | playbook | `earnings-call-risk-map playbooks --format markdown --out examples/output/playbooks.md` |
| `examples/output/promotion_pack.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/promotion_pack.md` | `md` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/public_apple_static_case_study_dashboard.html` | `html` | dashboard | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/public_apple_static_case_study_report.md` | `md` | markdown report | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/public_apple_static_case_study_review_queue.json` | `json` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/public_apple_static_case_study_review_queue.md` | `md` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/public_apple_static_case_study_snapshot.json` | `json` | analyzed snapshot | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/publication_checklist.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/publication_checklist.md` | `md` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/release_manifest.json` | `json` | manifest | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/risk_language_taxonomy.md` | `md` | taxonomy | `earnings-call-risk-map risk-taxonomy --out examples/output/risk_language_taxonomy.md` |
| `examples/output/sample_filled_template_report.md` | `md` | markdown report | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/sample_filled_template_review_queue.json` | `json` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/sample_filled_template_review_queue.md` | `md` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/sample_filled_template_snapshot.json` | `json` | analyzed snapshot | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/schema_authoring_reference.json` | `json` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/schema_authoring_reference.md` | `md` | generated output | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/semiconductor_equipment_dashboard.html` | `html` | dashboard | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/semiconductor_equipment_report.md` | `md` | markdown report | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/semiconductor_equipment_review_queue.json` | `json` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/semiconductor_equipment_review_queue.md` | `md` | review queue | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/semiconductor_equipment_snapshot.json` | `json` | analyzed snapshot | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/showcase_dashboard_preview.svg` | `svg` | dashboard | `earnings-call-risk-map demo --out-dir examples/output` |
| `examples/output/template_catalog.json` | `json` | catalog | `earnings-call-risk-map template-catalog --format json --out examples/output/template_catalog.json` |
| `examples/output/template_catalog.md` | `md` | catalog | `earnings-call-risk-map template-catalog --format markdown --out examples/output/template_catalog.md` |
