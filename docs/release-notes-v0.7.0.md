# Release Notes Draft: v0.7.0

Draft date: 2026-05-17

## Scope

v0.7.0 adds decision-support documentation for when to use `earnings-call-risk-map` instead of spreadsheets or generic notes, and when not to. The release keeps the package behavior unchanged and strengthens documentation link coverage.

## Added

- Comparison guide at [docs/comparison-to-spreadsheets.md](comparison-to-spreadsheets.md).
- README and usage links to the comparison guide.
- Unit-test coverage that the comparison guide exists, covers better/worse tradeoffs, preserves the non-advice boundary, and is linked from first-run docs.
- Selfcheck link coverage for the comparison guide and v0.7.0 release notes.
- Internal maturity review at [reports/reviews/2026-05-17-v0.7.0-internal-review.md](../reports/reviews/2026-05-17-v0.7.0-internal-review.md).

## Changed

- Package version is now `0.7.0`.
- README links now point to the v0.7.0 release notes draft.
- Release-asset checks and maturity evidence now include the comparison guide and v0.7.0 review evidence.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map release-assets
python scripts/privacy_scan.py
git diff --check
```

Expected version output: `0.7.0`.

## Safety Boundary

The release remains educational research review only. The comparison guide explicitly says the tool does not replace financial models, notes, source verification, reviewer judgment, or personalized investment, legal, accounting, tax, buy, sell, or hold advice.
