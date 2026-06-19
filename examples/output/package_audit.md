# Package Audit

- Package: `earnings-call-risk-map`
- Version: `0.9.3`
- Commands: 32 (`agent-workflow`, `analyze`, `audit`, `case-study-map`, `cheat-sheet`, `compare`, `data-entry-checklist`, `demo`, `demo-screenshot-guide`, `doctor`, `examples-index`, `fixture-catalog`, `fixture-summary`, `fresh-clone-plan`, `handoff-packet`, `manifest`, `maturity-evidence`, `playbooks`, `promotion-pack`, `publication-checklist`, `release-owner-handoff`, `release-assets`, `release-notes`, `review-queue`, `review-queue-jsonl`, `risk-taxonomy`, `schema-authoring-reference`, `schema-reference`, `source-boundary-evidence`, `template-catalog`, `version`, `visual-evidence-receipt`)
- Fixtures: 7
- Output artifacts: 77
- Workflow files present: no
- Skill present: yes (`skills/agent/earnings-call-risk-map/SKILL.md`)
- Local-only audit: passed

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Local-Only No-Network Guarantee

- Network access required: no
- Credentials required: no
- External services required: none
- Command scope: All CLI commands read local JSON/text inputs and write local Markdown, JSON, JSONL, HTML, or manifest files only.

### Local-Only Checks

- runtime_dependencies_empty: passed - project declares no runtime package dependencies
- no_network_client_imports: passed - no network-client imports found in package or local scripts
- no_credential_environment_reads: passed - no credential environment variable reads found in package or local scripts
- workflow_files_absent: passed - no GitHub workflow files are required for package commands

### Command Credential And Network Requirements

- `agent-workflow`: network required `false`, credentials required `false`
- `analyze`: network required `false`, credentials required `false`
- `audit`: network required `false`, credentials required `false`
- `case-study-map`: network required `false`, credentials required `false`
- `cheat-sheet`: network required `false`, credentials required `false`
- `compare`: network required `false`, credentials required `false`
- `data-entry-checklist`: network required `false`, credentials required `false`
- `demo`: network required `false`, credentials required `false`
- `demo-screenshot-guide`: network required `false`, credentials required `false`
- `doctor`: network required `false`, credentials required `false`
- `examples-index`: network required `false`, credentials required `false`
- `fixture-catalog`: network required `false`, credentials required `false`
- `fixture-summary`: network required `false`, credentials required `false`
- `fresh-clone-plan`: network required `false`, credentials required `false`
- `handoff-packet`: network required `false`, credentials required `false`
- `manifest`: network required `false`, credentials required `false`
- `maturity-evidence`: network required `false`, credentials required `false`
- `playbooks`: network required `false`, credentials required `false`
- `promotion-pack`: network required `false`, credentials required `false`
- `publication-checklist`: network required `false`, credentials required `false`
- `release-owner-handoff`: network required `false`, credentials required `false`
- `release-assets`: network required `false`, credentials required `false`
- `release-notes`: network required `false`, credentials required `false`
- `review-queue`: network required `false`, credentials required `false`
- `review-queue-jsonl`: network required `false`, credentials required `false`
- `risk-taxonomy`: network required `false`, credentials required `false`
- `schema-authoring-reference`: network required `false`, credentials required `false`
- `schema-reference`: network required `false`, credentials required `false`
- `source-boundary-evidence`: network required `false`, credentials required `false`
- `template-catalog`: network required `false`, credentials required `false`
- `version`: network required `false`, credentials required `false`
- `visual-evidence-receipt`: network required `false`, credentials required `false`

## Fixtures

- `examples/input/consumer_hardware.json`
- `examples/input/demo_company.json`
- `examples/input/demo_company_prior.json`
- `examples/input/demo_energy_infrastructure.json`
- `examples/input/public_apple_static_case_study.json`
- `examples/input/sample_filled_template_workflow.json`
- `examples/input/semiconductor_equipment.json`

## Output Artifacts

- `examples/output/agent_workflow.json`
- `examples/output/agent_workflow.md`
- `examples/output/case_study_map.json`
- `examples/output/case_study_map.md`
- `examples/output/command_cheat_sheet.json`
- `examples/output/command_cheat_sheet.md`
- `examples/output/command_cheatsheet.json`
- `examples/output/command_cheatsheet.md`
- `examples/output/consumer_hardware_dashboard.html`
- `examples/output/consumer_hardware_report.md`
- `examples/output/consumer_hardware_review_queue.json`
- `examples/output/consumer_hardware_review_queue.md`
- `examples/output/consumer_hardware_snapshot.json`
- `examples/output/data_entry_checklist.json`
- `examples/output/data_entry_checklist.md`
- `examples/output/demo_compare.json`
- `examples/output/demo_compare.md`
- `examples/output/demo_dashboard.html`
- `examples/output/demo_prior_report.md`
- `examples/output/demo_prior_snapshot.json`
- `examples/output/demo_report.md`
- `examples/output/demo_review_queue.json`
- `examples/output/demo_review_queue.md`
- `examples/output/demo_review_queue_items.jsonl`
- `examples/output/demo_screenshot_guide.json`
- `examples/output/demo_screenshot_guide.md`
- `examples/output/demo_snapshot.json`
- `examples/output/doctor.json`
- `examples/output/doctor.md`
- `examples/output/energy_infrastructure_dashboard.html`
- `examples/output/energy_infrastructure_report.md`
- `examples/output/energy_infrastructure_review_queue.json`
- `examples/output/energy_infrastructure_review_queue.md`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/examples_index.json`
- `examples/output/examples_index.md`
- `examples/output/fixture_catalog.md`
- `examples/output/fresh_clone_plan.json`
- `examples/output/fresh_clone_plan.md`
- `examples/output/handoff_packet.json`
- `examples/output/handoff_packet.md`
- `examples/output/handoff_packet_examples.json`
- `examples/output/handoff_packet_examples.md`
- `examples/output/integration_notes.json`
- `examples/output/playbook_output_examples.json`
- `examples/output/playbook_output_examples.md`
- `examples/output/playbooks.json`
- `examples/output/playbooks.md`
- `examples/output/promotion_pack.json`
- `examples/output/promotion_pack.md`
- `examples/output/public_apple_static_case_study_dashboard.html`
- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/public_apple_static_case_study_review_queue.json`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/publication_checklist.json`
- `examples/output/publication_checklist.md`
- `examples/output/release_manifest.json`
- `examples/output/risk_language_taxonomy.md`
- `examples/output/sample_filled_template_report.md`
- `examples/output/sample_filled_template_review_queue.json`
- `examples/output/sample_filled_template_review_queue.md`
- `examples/output/sample_filled_template_snapshot.json`
- `examples/output/schema_authoring_reference.json`
- `examples/output/schema_authoring_reference.md`
- `examples/output/semiconductor_equipment_dashboard.html`
- `examples/output/semiconductor_equipment_report.md`
- `examples/output/semiconductor_equipment_review_queue.json`
- `examples/output/semiconductor_equipment_review_queue.md`
- `examples/output/semiconductor_equipment_snapshot.json`
- `examples/output/showcase_dashboard_preview.svg`
- `examples/output/source_boundary_evidence.json`
- `examples/output/source_boundary_evidence.md`
- `examples/output/template_catalog.json`
- `examples/output/template_catalog.md`
- `examples/output/visual_evidence_receipt.json`
- `examples/output/visual_evidence_receipt.md`

## Workflow Files

- None
