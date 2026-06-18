# Release Notes Draft: v0.9.2

Draft date: 2026-06-19

## Scope

v0.9.2 adds fixture-scoped public-source demo receipts to the deterministic source-boundary walkthrough evidence. The patch records the expected local snapshot, report, dashboard, and review-queue artifacts for each bundled public-source fixture while preserving the local-only, static-data, non-advice boundary described in the [comparison guide](comparison-to-spreadsheets.md).

## Added

- Release notes draft at [docs/release-notes-v0.9.2.md](release-notes-v0.9.2.md).
- Fixture-scoped `fixture_scoped_public_source_demo` receipts for each bundled public-source fixture in `examples/output/source_boundary_evidence.json`.
- Fixture-scoped public-source demo receipt section in `examples/output/source_boundary_evidence.md`.
- Selfcheck validation for receipt type, fixture counts, fixture-scoped demo receipt checks, step count, and Markdown markers.
- CLI test coverage for the fixture-scoped receipt fields.

## Changed

- Package version is now `0.9.2`.
- README, release readiness, publication checklist, distribution docs, release owner handoff, reviewer evidence, release asset checks, maturity evidence, and generated examples now identify v0.9.2 as the current release line.
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

Expected version output: `0.9.2`.

## Safety Boundary

The release remains educational research review only. It does not add live data, network calls, credentials, workflows, recommendations, ratings, price targets, portfolio actions, or personalized investment, legal, accounting, tax, buy, sell, or hold advice.
