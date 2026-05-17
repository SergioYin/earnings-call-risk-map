# Release Owner Handoff

Use this as the final v0.8 release owner checklist before tagging, publishing release notes, or promoting public artifacts. It summarizes the release gates recorded in [Reviewer Evidence](reviewer-evidence.md), [Release Readiness](release-readiness.md), [Publication Checklist](publication-checklist.md), [Distribution](distribution.md), and the final review at [reports/reviews/2026-05-17-v0.8.0-final-review.md](../reports/reviews/2026-05-17-v0.8.0-final-review.md).

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Preserve this boundary in release notes, promotion copy, screenshots, and demos.

## Final v0.8 Release Owner Checklist

Complete these gates in order:

1. Confirm release metadata agrees on `0.8.0` in `README.md`, `CHANGELOG.md`, `pyproject.toml`, `src/earnings_call_risk_map/version.py`, and [docs/release-notes-v0.8.0.md](release-notes-v0.8.0.md).
2. Inspect the current worktree with `git status --short` and confirm every modified or untracked file is intended for the v0.8.0 release.
3. Rerun the exact verification command set below after any release metadata, documentation, fixture, generated artifact, or promotion-copy change.
4. Review the generated evidence bundle at [reports/maturity/maturity_evidence.md](../reports/maturity/maturity_evidence.md) and [reports/maturity/maturity_evidence.json](../reports/maturity/maturity_evidence.json).
5. Review the final internal maturity review, promotion gate review, and reviewer feedback summary before release execution.
6. If package publishing is in scope, complete the wheel build dry run in [Distribution](distribution.md). Do not upload package-index artifacts without separate package owner approval.
7. If a hosted demo is in scope, verify [Pages Demo](pages-demo.md) locally first. Do not deploy a hosted demo from this handoff alone.
8. Review public copy against [Non-Advice Boundary](non-advice-boundary.md), [Case Study Limitations](case-study-limitations.md), [Known Limitations](known-limitations.md), [Source Attribution Guide](source-attribution-guide.md), and [Security And Privacy](security-and-privacy.md).
9. Create an annotated tag only after the release owner accepts the worktree and evidence set: `git tag -a v0.8.0 -m "v0.8.0"`.
10. Create the GitHub release only after the tag has been pushed and the release notes have been reviewed: `gh release create v0.8.0 --title "v0.8.0" --notes-file docs/release-notes-v0.8.0.md`.
11. Run the post-publish smoke checks from [Publication Checklist](publication-checklist.md) before announcing the release.

## Exact Verification Commands

Run these commands from the repository root before release execution:

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map audit --format json
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
python scripts/privacy_scan.py
git diff --check
```

Expected results:

- `PYTHONPATH=src python -m earnings_call_risk_map version` prints exactly `0.8.0`.
- `PYTHONPATH=src python -m unittest discover -s tests` ends with `OK`.
- `PYTHONPATH=src python scripts/selfcheck.py` ends with `selfcheck passed`.
- `PYTHONPATH=src python -m earnings_call_risk_map audit --format json` reports local-only checks as passed.
- `PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json` reports `missing_count` as `0`.
- `PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity` refreshes the maturity evidence bundle.
- `python scripts/privacy_scan.py` prints `privacy scan passed`.
- `git diff --check` exits with no whitespace findings.

Run these package dry-run commands only if package publishing is in scope:

```bash
python -m pip install --upgrade build
rm -rf dist-dry-run
python -m build --wheel --outdir dist-dry-run
python -m zipfile --list dist-dry-run/*.whl
python -m pip install --force-reinstall --no-deps dist-dry-run/*.whl
earnings-call-risk-map version
```

Expected package dry-run version output: `0.8.0`.

## Promotion Evidence Paths

Use these paths as the promotion evidence set for owner review:

- `docs/release-notes-v0.8.0.md`
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
- `reports/reviews/2026-05-17-v0.8.0-final-review.md`
- `reports/reviews/2026-05-17-v0.8.0-promotion-review.md`
- `reports/reviews/2026-05-17-v0.8.0-internal-review.md`
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

The final v0.8 evidence supports owner handoff and small-scope public promotion after release owner approval. It does not itself perform or approve tag creation, pushing, package-index publication, hosted demo deployment, or broad public announcement.

Before public promotion, confirm the announcement copy does not claim live market data, investment recommendations, buy, sell, or hold conclusions, portfolio suitability, valuation conclusions, price targets, source verification, or current analysis from stale/static fixtures.
