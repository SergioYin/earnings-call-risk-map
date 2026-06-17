# Release Notes Draft: v0.9.0

Draft date: 2026-06-18

## Scope

v0.9.0 adds a deterministic source-boundary walkthrough receipt for cold reviewer handoff. The receipt extends the existing source-boundary evidence bundle with explicit reviewer actions, evidence paths, artifact existence checks, public-source fixture counts, dashboard/release-owner handoff checks, and no-live-data/no-advice boundary checks. The release keeps the decision-support boundary described in the [comparison guide](comparison-to-spreadsheets.md).

## Added

- Release notes draft at [docs/release-notes-v0.9.0.md](release-notes-v0.9.0.md).
- `public_source_boundary_walkthrough` receipt in `examples/output/source_boundary_evidence.json`.
- Walkthrough receipt section in `examples/output/source_boundary_evidence.md`.
- Selfcheck validation for receipt type, fixture counts, receipt checks, step count, and Markdown markers.
- CLI test coverage for the new receipt fields.
- v0.9.0 release-readiness review records under `reports/reviews/`.

## Changed

- Package version is now `0.9.0`.
- README, release readiness, publication checklist, distribution docs, release owner handoff, reviewer evidence, release asset checks, maturity evidence, and generated examples now identify v0.9.0 as the current release line.
- Release manifests now include the updated source-boundary evidence artifacts and current release documents.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map release-assets
python scripts/privacy_scan.py
git diff --check
```

Expected version output: `0.9.0`.

## Safety Boundary

The release remains educational research review only. It does not add live data, network calls, credentials, workflows, recommendations, ratings, price targets, portfolio actions, or personalized investment, legal, accounting, tax, buy, sell, or hold advice.
