# Release Owner Handoff

- Package: `earnings-call-risk-map`
- Version: `0.9.7`
- Source doc: `docs/release-owner-handoff.md`
- Owner scope: final release owner handoff before tagging, publishing, or promoting public artifacts

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Final Release Owner Checklist

Final v0.9 Release Owner Checklist.

### 1. Confirm Release Metadata

Confirm all release metadata agrees on the current package version.

Confirm release metadata agrees on `0.9.7`.

- Confirm `README.md`, `CHANGELOG.md`, `pyproject.toml`, `src/earnings_call_risk_map/version.py`, and `docs/release-notes-v0.9.7.md` all identify `0.9.7`.

### 2. Inspect Worktree

Confirm every modified or untracked file belongs in the release.

- Run `git status --short` and review every path before tagging.

### 3. Rerun Verification

Rerun the full verification command set after any release-facing change.

- Rerun verification after release metadata, documentation, fixture, generated artifact, or promotion-copy changes.

### 4. Review Evidence Bundle

Review generated maturity evidence and final review records.

- Review `reports/maturity/maturity_evidence.md` and `reports/maturity/maturity_evidence.json`.
- Review `examples/output/release_owner_compare_blockers.md` before accepting evidence handoff changes.
- Review the final internal maturity review, promotion gate review, and reviewer feedback summary.

### 5. Confirm Owner-Controlled Gates

Keep package publishing, hosted demo deployment, tagging, and announcements owner-controlled.

- Complete the wheel build dry run only if package publishing is in scope.
- Verify the Pages demo locally only if a hosted demo is in scope.
- Create the annotated tag only after the release owner accepts the worktree and evidence set: `git tag -a v0.9.7 -m "v0.9.7"`.
- Create the GitHub release only after the tag has been pushed and release notes have been reviewed: `gh release create v0.9.7 --title "v0.9.7" --notes-file docs/release-notes-v0.9.7.md`.

### 6. Review Public Boundaries

Confirm public copy preserves the educational, local-only, static-data boundary.

- Review public copy against `docs/non-advice-boundary.md`, `docs/case-study-limitations.md`, and `docs/security-and-privacy.md`.
- Do not claim live market data, investment recommendations, buy, sell, or hold conclusions, portfolio suitability, valuation conclusions, price targets, source verification, or current analysis from stale/static fixtures.

## Exact Verification Commands

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map audit --format json
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json
PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format json
PYTHONPATH=src python -m earnings_call_risk_map release-owner-compare-blockers --compare examples/output/evidence_handoff_compare.json --format json
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
python scripts/privacy_scan.py
git diff --check
```

## Expected Results

- `PYTHONPATH=src python -m earnings_call_risk_map version` prints exactly `0.9.7`.
- `PYTHONPATH=src python -m unittest discover -s tests` ends with `OK`.
- `PYTHONPATH=src python scripts/selfcheck.py` ends with `selfcheck passed`.
- `PYTHONPATH=src python -m earnings_call_risk_map audit --format json` reports local-only checks as passed.
- `PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json` reports `missing_count` as `0`.
- `PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format json` reports fixture paths, source boundaries, no-live-data, and no-advice checks.
- `PYTHONPATH=src python -m earnings_call_risk_map release-owner-compare-blockers --compare examples/output/evidence_handoff_compare.json --format json` reports blocker and review-required counts from the evidence handoff compare artifact.
- `PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity` refreshes the maturity evidence bundle.
- `python scripts/privacy_scan.py` prints `privacy scan passed`.
- `git diff --check` exits with no whitespace findings.

## Package Dry Run

Run only if package publishing is in scope.

```bash
python -m pip install --upgrade build
rm -rf dist-dry-run
python -m build --wheel --outdir dist-dry-run
python -m zipfile --list dist-dry-run/*.whl
python -m pip install --force-reinstall --no-deps dist-dry-run/*.whl
earnings-call-risk-map version
```

Expected package dry-run version output: `0.9.7`.

## Promotion Evidence Paths

- `docs/release-notes-v0.9.7.md`
- `docs/release-readiness.md`
- `docs/reviewer-evidence.md`
- `docs/reviewer-feedback-consumption.md`
- `docs/publication-checklist.md`
- `docs/distribution.md`
- `docs/promotion-page-outline.md`
- `docs/demo-screenshot-guide.md`
- `docs/pages-demo.md`
- `docs/security-and-privacy.md`
- `docs/non-advice-boundary.md`
- `docs/source-attribution-guide.md`
- `docs/case-study-limitations.md`
- `docs/known-limitations.md`
- `reports/reviews/2026-06-18-v0.9.0-final-review.md`
- `reports/reviews/2026-06-18-v0.9.0-promotion-review.md`
- `reports/reviews/2026-06-18-v0.9.0-internal-review.md`
- `reports/reviews/reviewer_feedback_consumption.json`
- `reports/maturity/maturity_evidence.md`
- `reports/maturity/maturity_evidence.json`
- `examples/output/promotion_pack.md`
- `examples/output/promotion_pack.json`
- `examples/output/release_manifest.json`
- `release_manifest.json`
- `examples/output/package_audit.md`
- `examples/output/package_audit.json`
- `examples/output/doctor.md`
- `examples/output/doctor.json`
- `examples/output/source_boundary_evidence.md`
- `examples/output/source_boundary_evidence.json`
- `examples/output/release_owner_compare_blockers.md`
- `examples/output/release_owner_compare_blockers.json`
- `docs/assets/showcase-dashboard-preview.svg`
- `examples/output/showcase_dashboard_preview.svg`
- `docs/demo-index.html`
- `examples/output/public_apple_static_case_study_dashboard.html`
- `examples/output/public_apple_static_case_study_report.md`
- `examples/output/public_apple_static_case_study_review_queue.md`
- `examples/output/handoff_packet.md`
- `examples/output/handoff_packet.json`
- `skills/agent/earnings-call-risk-map/SKILL.md`

## Owner-Controlled Promotion Gates

The evidence supports owner handoff and small-scope public promotion after release owner approval; it does not itself perform or approve tag creation, pushing, package-index publication, hosted demo deployment, or broad public announcement.
