# Package Audit

- Package: `earnings-call-risk-map`
- Version: `0.6.0`
- Commands: 13 (`analyze`, `audit`, `compare`, `demo`, `fixture-catalog`, `handoff-packet`, `manifest`, `maturity-evidence`, `playbooks`, `release-assets`, `review-queue`, `review-queue-jsonl`, `version`)
- Fixtures: 4
- Output artifacts: 32
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

- `analyze`: network required `false`, credentials required `false`
- `audit`: network required `false`, credentials required `false`
- `compare`: network required `false`, credentials required `false`
- `demo`: network required `false`, credentials required `false`
- `fixture-catalog`: network required `false`, credentials required `false`
- `handoff-packet`: network required `false`, credentials required `false`
- `manifest`: network required `false`, credentials required `false`
- `maturity-evidence`: network required `false`, credentials required `false`
- `playbooks`: network required `false`, credentials required `false`
- `release-assets`: network required `false`, credentials required `false`
- `review-queue`: network required `false`, credentials required `false`
- `review-queue-jsonl`: network required `false`, credentials required `false`
- `version`: network required `false`, credentials required `false`

## Fixtures

- `examples/input/demo_company.json`
- `examples/input/demo_company_prior.json`
- `examples/input/demo_energy_infrastructure.json`
- `examples/input/public_apple_static_case_study.json`

## Output Artifacts

- `examples/output/demo_compare.json`
- `examples/output/demo_compare.md`
- `examples/output/demo_dashboard.html`
- `examples/output/demo_prior_report.md`
- `examples/output/demo_prior_snapshot.json`
- `examples/output/demo_report.md`
- `examples/output/demo_review_queue.json`
- `examples/output/demo_review_queue.md`
- `examples/output/demo_review_queue_items.jsonl`
- `examples/output/demo_snapshot.json`
- `examples/output/energy_infrastructure_dashboard.html`
- `examples/output/energy_infrastructure_report.md`
- `examples/output/energy_infrastructure_review_queue.json`
- `examples/output/energy_infrastructure_review_queue.md`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/fixture_catalog.md`
- `examples/output/handoff_packet.json`
- `examples/output/handoff_packet.md`
- `examples/output/handoff_packet_examples.json`
- `examples/output/handoff_packet_examples.md`
- `examples/output/integration_notes.json`
- `examples/output/playbook_output_examples.json`
- `examples/output/playbook_output_examples.md`
- `examples/output/playbooks.json`
- `examples/output/playbooks.md`
- `examples/output/public_apple_static_case_study_dashboard.html`
- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/public_apple_static_case_study_review_queue.json`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/release_manifest.json`
- `examples/output/showcase_dashboard_preview.svg`

## Workflow Files

- None
