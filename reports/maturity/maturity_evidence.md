# Maturity Evidence Bundle

- Package: `earnings-call-risk-map`
- Version: `0.4.0`
- Skill path: `skills/agent/earnings-call-risk-map/SKILL.md` (present)
- Review template: `reports/reviews/release-readiness-review.md` (present)
- Privacy scan: passed (`python scripts/privacy_scan.py`)

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Test Commands

- `PYTHONPATH=src python -m unittest discover -s tests`
- `PYTHONPATH=src python scripts/selfcheck.py`
- `python scripts/privacy_scan.py`

## Verification Commands

- `PYTHONPATH=src python -m unittest discover -s tests`
- `PYTHONPATH=src python scripts/selfcheck.py`
- `PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output`
- `PYTHONPATH=src python -m earnings_call_risk_map audit`
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

- Source: `reports/reviews/2026-05-17-v0.3.0-internal-review.md`
- Review date: `2026-05-17`
- Overall: `89/100`
- Level: `L3 -> target L4`
- Release gate: `PASS`
- Promotion gate: `PASS small-scope`

### Scorecard

- Product Clarity: `14/15`
- Reproducibility: `14/15`
- User Value: `18/20`
- Evidence Quality: `15/15`
- Engineering Quality: `13/15`
- Showcase: `8/10`
- Risk Boundary: `7/10`

### Four-Role Review

- Product: `4/5 accept`
- Engineering: `4/5 accept`
- Cold User: `4/5 accept`
- Risk: `4/5 accept`

## Release Assets

- `README.md`
- `CHANGELOG.md`
- `docs/release-notes-v0.4.0.md`
- `docs/release-readiness.md`
- `docs/reviewer-evidence.md`
- `docs/distribution.md`
- `docs/non-advice-boundary.md`
- `docs/pages-demo.md`
- `docs/gallery.md`
- `docs/public-case-study.md`
- `docs/schema-reference.json`
- `docs/assets/showcase-dashboard-preview.svg`
- `examples/output/demo_dashboard.html`
- `examples/output/energy_infrastructure_dashboard.html`
- `examples/output/public_apple_static_case_study_dashboard.html`
- `examples/output/showcase_dashboard_preview.svg`
- `examples/output/demo_report.md`
- `examples/output/energy_infrastructure_report.md`
- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/demo_review_queue.md`
- `examples/output/energy_infrastructure_review_queue.md`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/demo_snapshot.json`
- `examples/output/demo_prior_snapshot.json`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/demo_compare.md`
- `examples/output/demo_compare.json`
- `examples/output/package_audit.md`
- `examples/output/package_audit.json`
- `examples/output/release_manifest.json`
- `release_manifest.json`
- `reports/maturity/maturity_evidence.md`
- `reports/maturity/maturity_evidence.json`
- `skills/agent/earnings-call-risk-map/SKILL.md`
- `reports/reviews/release-readiness-review.md`

## Artifact Paths

- `docs/assets/showcase-dashboard-preview.svg`
- `examples/output/demo_compare.json`
- `examples/output/demo_compare.md`
- `examples/output/demo_dashboard.html`
- `examples/output/demo_prior_report.md`
- `examples/output/demo_prior_snapshot.json`
- `examples/output/demo_report.md`
- `examples/output/demo_review_queue.json`
- `examples/output/demo_review_queue.md`
- `examples/output/demo_snapshot.json`
- `examples/output/energy_infrastructure_dashboard.html`
- `examples/output/energy_infrastructure_report.md`
- `examples/output/energy_infrastructure_review_queue.json`
- `examples/output/energy_infrastructure_review_queue.md`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/integration_notes.json`
- `examples/output/package_audit.json`
- `examples/output/package_audit.md`
- `examples/output/public_apple_static_case_study_dashboard.html`
- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/public_apple_static_case_study_review_queue.json`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/release_manifest.json`
- `examples/output/showcase_dashboard_preview.svg`
- `release_manifest.json`

## Privacy Scan

- Exit code: `0`
- Output: `privacy scan passed`
