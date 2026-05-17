# Release Notes Draft: v0.8.0

Draft date: 2026-05-17

## Scope

v0.8.0 aligns the package metadata, release asset checklist, generated manifests, maturity evidence, publication checklist, and public docs around the current release line. The release keeps package behavior unchanged and preserves the decision-support boundary described in the [comparison guide](comparison-to-spreadsheets.md).

## Added

- Release notes draft at [docs/release-notes-v0.8.0.md](release-notes-v0.8.0.md).
- Internal maturity review at [reports/reviews/2026-05-17-v0.8.0-internal-review.md](../reports/reviews/2026-05-17-v0.8.0-internal-review.md).

## Changed

- Package version is now `0.8.0`.
- README links now point to the v0.8.0 release notes draft.
- Release-asset checks now expect the v0.8.0 release notes and v0.8.0 internal review evidence.
- Maturity evidence and manifests now report the v0.8.0 package version and latest review source.
- Distribution and publication checklist docs now use v0.8.0 tag, release, and smoke-check examples.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map release-assets
python scripts/privacy_scan.py
git diff --check
```

Expected version output: `0.8.0`.

## Safety Boundary

The release remains educational research review only. It does not add live data, network calls, credentials, workflows, recommendations, ratings, price targets, portfolio actions, or personalized investment, legal, accounting, tax, buy, sell, or hold advice.
