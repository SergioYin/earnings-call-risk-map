# Reviewer Evidence Appendix

This appendix is for maintainers and reviewers validating a release candidate from a checkout or fresh clone. It records the exact local commands, release assets, and maturity score evidence used for review.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## Exact Verification Commands

Run these commands from the repository root:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl
PYTHONPATH=src python -m earnings_call_risk_map playbooks --format markdown --out examples/output/playbooks.md
PYTHONPATH=src python -m earnings_call_risk_map audit
PYTHONPATH=src python -m earnings_call_risk_map release-assets
PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
python scripts/privacy_scan.py
git diff --check
```

`scripts/selfcheck.py` also runs unit tests, regenerates the demo bundle, runs package audit, validates release assets, regenerates `release_manifest.json`, runs the privacy scan, regenerates maturity evidence, and verifies the static dashboard/SVG previews, integration examples, compare examples, playbooks, handoff packet examples, and selected documentation links.

## Fresh Clone Procedure

Use this procedure to validate the repository without relying on an existing local environment. Replace `<repo-url>` with the review source URL or local bare repository path.

```bash
git clone <repo-url> earnings-call-risk-map
cd earnings-call-risk-map
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python -m pip install .
earnings-call-risk-map version
```

Expected version for this release line: `0.6.0`.

## Release Assets

Primary release and reviewer assets:

- `README.md`
- `CHANGELOG.md`
- `docs/release-notes-v0.6.0.md`
- `examples/playbooks/README.md`
- `examples/playbooks/quarterly-review.md`
- `examples/playbooks/catalyst-check-in.md`
- `examples/playbooks/post-earnings-thesis-refresh.md`
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
- `examples/output/demo_review_queue_items.jsonl`
- `examples/output/fixture_catalog.md`
- `examples/output/demo_snapshot.json`
- `examples/output/demo_prior_snapshot.json`
- `examples/output/energy_infrastructure_snapshot.json`
- `examples/output/public_apple_static_case_study_snapshot.json`
- `examples/output/demo_compare.md`
- `examples/output/demo_compare.json`
- `examples/output/package_audit.md`
- `examples/output/package_audit.json`
- `examples/output/playbooks.md`
- `examples/output/playbooks.json`
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
- `reports/reviews/2026-05-17-v0.6.0-internal-review.md`
- `skills/agent/earnings-call-risk-map/SKILL.md`
- `reports/reviews/release-readiness-review.md`

Generated release hashes are recorded in `release_manifest.json`. The demo-copy manifest is `examples/output/release_manifest.json`.

## Maturity Scores

Latest recorded internal maturity review:

- Source: `reports/reviews/2026-05-17-v0.6.0-internal-review.md`
- Review date: `2026-05-17`
- Overall score: `95/100`
- Level: `L4 -> target L4+`
- Release gate: `PASS for owner handoff`
- Promotion gate: `PASS small-scope after release owner approval`

Scorecard:

- Product clarity: `15/15`
- Reproducibility: `15/15`
- User value: `19/20`
- Evidence quality: `15/15`
- Engineering quality: `14/15`
- Showcase: `9/10`
- Risk boundary: `8/10`

Four-role review:

- Product reviewer: `5/5 accept`
- Engineering reviewer: `5/5 accept`
- Cold-user reviewer: `4/5 accept`
- Risk reviewer: `4/5 accept`

## Generated Evidence Bundle

Regenerate the machine-readable and Markdown evidence bundle with:

```bash
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

Outputs:

- `reports/maturity/maturity_evidence.json`
- `reports/maturity/maturity_evidence.md`
