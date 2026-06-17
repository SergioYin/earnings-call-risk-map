# Maturity Evidence Bundle

- Package: `earnings-call-risk-map`
- Version: `0.9.0`
- Commands: 31
- Fixtures: 7
- Skill path: `skills/agent/earnings-call-risk-map/SKILL.md` (present)
- Review template: `reports/reviews/release-readiness-review.md` (present)
- Release assets: passed (95/95 present)
- Privacy scan: passed (`python scripts/privacy_scan.py`)
- Latest review score: 94/100 (reports/reviews/2026-06-18-v0.9.0-final-review.md)

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Test Commands

- `PYTHONPATH=src python -m unittest discover -s tests`
- `PYTHONPATH=src python scripts/selfcheck.py`
- `python scripts/privacy_scan.py`

## Verification Commands

- `PYTHONPATH=src python -m unittest discover -s tests`
- `PYTHONPATH=src python scripts/selfcheck.py`
- `PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output`
- `PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl`
- `PYTHONPATH=src python -m earnings_call_risk_map agent-workflow --format markdown --out examples/output/agent_workflow.md`
- `PYTHONPATH=src python -m earnings_call_risk_map agent-workflow --format json --out examples/output/agent_workflow.json`
- `PYTHONPATH=src python -m earnings_call_risk_map examples-index --format markdown --out examples/output/examples_index.md`
- `PYTHONPATH=src python -m earnings_call_risk_map examples-index --format json --out examples/output/examples_index.json`
- `PYTHONPATH=src python -m earnings_call_risk_map case-study-map --format markdown --out examples/output/case_study_map.md`
- `PYTHONPATH=src python -m earnings_call_risk_map case-study-map --format json --out examples/output/case_study_map.json`
- `PYTHONPATH=src python -m earnings_call_risk_map risk-taxonomy --out examples/output/risk_language_taxonomy.md`
- `PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format markdown --out examples/output/source_boundary_evidence.md`
- `PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format json --out examples/output/source_boundary_evidence.json`
- `PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format markdown --out examples/output/template_catalog.md`
- `PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format markdown --out examples/output/schema_authoring_reference.md`
- `PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format json --out examples/output/schema_authoring_reference.json`
- `PYTHONPATH=src python -m earnings_call_risk_map playbooks --format markdown --out examples/output/playbooks.md`
- `PYTHONPATH=src python -m earnings_call_risk_map promotion-pack --format markdown --out examples/output/promotion_pack.md`
- `PYTHONPATH=src python -m earnings_call_risk_map promotion-pack --format json --out examples/output/promotion_pack.json`
- `PYTHONPATH=src python -m earnings_call_risk_map publication-checklist --format markdown --out examples/output/publication_checklist.md`
- `PYTHONPATH=src python -m earnings_call_risk_map data-entry-checklist --format markdown --out examples/output/data_entry_checklist.md`
- `PYTHONPATH=src python -m earnings_call_risk_map demo-screenshot-guide --format markdown --out examples/output/demo_screenshot_guide.md`
- `PYTHONPATH=src python -m earnings_call_risk_map demo-screenshot-guide --format json --out examples/output/demo_screenshot_guide.json`
- `PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format markdown --out examples/output/fresh_clone_plan.md`
- `PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format json --out examples/output/fresh_clone_plan.json`
- `PYTHONPATH=src python -m earnings_call_risk_map cheat-sheet --format markdown --out examples/output/command_cheat_sheet.md`
- `PYTHONPATH=src python -m earnings_call_risk_map doctor --format json --out examples/output/doctor.json`
- `PYTHONPATH=src python -m earnings_call_risk_map doctor --format markdown --out examples/output/doctor.md`
- `PYTHONPATH=src python -m earnings_call_risk_map audit`
- `PYTHONPATH=src python -m earnings_call_risk_map release-assets`
- `PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json`
- `PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity`
- `python scripts/privacy_scan.py`
- `git diff --check`

## Fresh Clone Procedure

1. `git clone <repo-url> earnings-call-risk-map`
2. `cd earnings-call-risk-map`
3. `python -m venv .venv`
4. `source .venv/bin/activate`
5. `python -m pip install --upgrade pip`
6. `PYTHONPATH=src python -m earnings_call_risk_map version`
7. `PYTHONPATH=src python -m unittest discover -s tests`
8. `PYTHONPATH=src python scripts/selfcheck.py`
9. `python -m pip install .`
10. `earnings-call-risk-map version`

## Maturity Scores

- Source: `reports/reviews/2026-06-18-v0.9.0-final-review.md`
- Review date: `2026-06-18`
- Overall: `94/100`
- Level: `L4+`
- Release gate: `PASS for owner-controlled v0.9.0 release after final worktree inspection`
- Promotion gate: `PASS for small-scope public promotion after release owner approval`

### Scorecard

- Product Clarity: `15/15`
- Reproducibility: `15/15`
- User Value: `19/20`
- Evidence Quality: `15/15`
- Engineering Quality: `14/15`
- Showcase: `9/10`
- Risk Boundary: `7/10`

### Four-Role Review

- Product: `5/5 accept`
- Engineering: `5/5 accept`
- Cold User: `4/5 accept`
- Risk: `4/5 accept for controlled promotion`

## Release Assets

- `README.md`
- `CHANGELOG.md`
- `docs/release-notes-v0.9.0.md`
- `docs/comparison-to-spreadsheets.md`
- `examples/playbooks/README.md`
- `examples/playbooks/quarterly-review.md`
- `examples/playbooks/catalyst-check-in.md`
- `examples/playbooks/post-earnings-thesis-refresh.md`
- `docs/release-readiness.md`
- `docs/reviewer-evidence.md`
- `docs/distribution.md`
- `docs/troubleshooting.md`
- `docs/security-and-privacy.md`
- `docs/non-advice-boundary.md`
- `docs/pages-demo.md`
- `docs/gallery.md`
- `docs/public-case-study.md`
- `docs/schema-authoring-reference.md`
- `docs/schema-reference.json`
- `docs/assets/showcase-dashboard-preview.svg`
- `examples/output/demo_dashboard.html`
- `examples/output/energy_infrastructure_dashboard.html`
- `examples/output/semiconductor_equipment_dashboard.html`
- `examples/output/semiconductor_equipment_report/report.md`
- `examples/output/semiconductor_equipment_report/dashboard/dashboard.html`
- `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json`
- `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md`
- `examples/output/semiconductor_equipment_report/review_queue/review_queue.json`
- `examples/output/semiconductor_equipment_report/review_queue/review_queue.md`
- `examples/output/semiconductor_equipment_report/snapshot/snapshot.json`
- `examples/output/public_apple_static_case_study_dashboard.html`
- `examples/output/showcase_dashboard_preview.svg`
- `examples/output/demo_report.md`
- `examples/output/energy_infrastructure_report.md`
- `examples/output/semiconductor_equipment_report.md`
- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/demo_review_queue.md`
- `examples/output/energy_infrastructure_review_queue.md`
- `examples/output/semiconductor_equipment_review_queue.md`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/demo_review_queue_items.jsonl`
- `examples/output/demo_snapshot.json`
- `examples/output/demo_prior_snapshot.json`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/semiconductor_equipment_snapshot.json`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/demo_compare.md`
- `examples/output/demo_compare.json`
- `examples/output/package_audit.md`
- `examples/output/package_audit.json`
- `examples/output/agent_workflow.md`
- `examples/output/agent_workflow.json`
- `examples/output/doctor.md`
- `examples/output/doctor.json`
- `examples/output/examples_index.md`
- `examples/output/examples_index.json`
- `examples/output/case_study_map.md`
- `examples/output/case_study_map.json`
- `examples/output/command_cheat_sheet.md`
- `examples/output/command_cheat_sheet.json`
- `examples/output/command_cheatsheet.md`
- `examples/output/command_cheatsheet.json`
- `examples/output/risk_language_taxonomy.md`
- `examples/output/source_boundary_evidence.md`
- `examples/output/source_boundary_evidence.json`
- `examples/output/template_catalog.md`
- `examples/output/template_catalog.json`
- `examples/output/schema_authoring_reference.md`
- `examples/output/schema_authoring_reference.json`
- `examples/output/playbooks.md`
- `examples/output/playbooks.json`
- `examples/output/promotion_pack.md`
- `examples/output/promotion_pack.json`
- `examples/output/publication_checklist.md`
- `examples/output/publication_checklist.json`
- `examples/output/data_entry_checklist.md`
- `examples/output/data_entry_checklist.json`
- `examples/output/demo_screenshot_guide.md`
- `examples/output/demo_screenshot_guide.json`
- `examples/output/fresh_clone_plan.md`
- `examples/output/fresh_clone_plan.json`
- `examples/output/playbook_output_examples.md`
- `examples/output/playbook_output_examples.json`
- `examples/output/handoff_packet.md`
- `examples/output/handoff_packet.json`
- `examples/output/handoff_packet_examples.md`
- `examples/output/handoff_packet_examples.json`
- `examples/output/release_manifest.json`
- `release_manifest.json`
- `reports/maturity/maturity_evidence.md`
- `reports/maturity/maturity_evidence.json`
- `reports/reviews/2026-06-18-v0.9.0-internal-review.md`
- `reports/reviews/2026-06-18-v0.9.0-final-review.md`
- `skills/agent/earnings-call-risk-map/SKILL.md`
- `reports/reviews/release-readiness-review.md`

## Artifact Paths

- `docs/assets/showcase-dashboard-preview.svg`
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
- `examples/output/package_audit.json`
- `examples/output/package_audit.md`
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
- `examples/output/semiconductor_equipment_report/dashboard/dashboard.html`
- `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json`
- `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md`
- `examples/output/semiconductor_equipment_report/report.md`
- `examples/output/semiconductor_equipment_report/review_queue/review_queue.json`
- `examples/output/semiconductor_equipment_report/review_queue/review_queue.md`
- `examples/output/semiconductor_equipment_report/snapshot/snapshot.json`
- `examples/output/semiconductor_equipment_review_queue.json`
- `examples/output/semiconductor_equipment_review_queue.md`
- `examples/output/semiconductor_equipment_snapshot.json`
- `examples/output/showcase_dashboard_preview.svg`
- `examples/output/source_boundary_evidence.json`
- `examples/output/source_boundary_evidence.md`
- `examples/output/template_catalog.json`
- `examples/output/template_catalog.md`
- `release_manifest.json`

## Privacy Scan

- Exit code: `0`
- Output: `privacy scan passed`
