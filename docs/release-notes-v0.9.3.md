# Release Notes Draft: v0.9.3

Draft date: 2026-06-19

## Scope

v0.9.3 adds the public demo visual evidence receipt and evidence handoff audit as a patch release on top of v0.9.2. The patch records deterministic screenshot-review checks and reviewer handoff metadata for source attribution markers, stale/static warnings, public-source fixture limits, no-live-data boundaries, broker/account-data absence, and non-advice claims while preserving the local-only boundary described in the [comparison guide](comparison-to-spreadsheets.md).

## Added

- Release notes draft at [docs/release-notes-v0.9.3.md](release-notes-v0.9.3.md).
- `visual-evidence-receipt` CLI route with generated `examples/output/visual_evidence_receipt.md` and `examples/output/visual_evidence_receipt.json` for public demo screenshot review.
- `evidence-handoff-audit` CLI route and standalone console script with generated `examples/output/evidence_handoff_audit.md` and `examples/output/evidence_handoff_audit.json` for reviewer handoff readiness.
- Visual evidence checks for source attribution markers, stale/static warnings, public-source fixture limits, no live data, no broker or account data, and no personalized investment, legal, accounting, tax, buy, sell, or hold advice.
- Artifact metadata checks for relative path, role, present/missing status, bytes, SHA-256, source/freshness/review notes, recommended evidence items, regeneration commands, and explicit static/local-source/no-live-data/no-broker/non-advice boundaries.
- Selfcheck validation for visual evidence receipt files, receipt type, fixture counts, check fields, and Markdown markers.
- CLI test coverage for the visual evidence receipt and evidence handoff audit Markdown, JSON, and file output paths.

## Changed

- Package version is now `0.9.3`.
- README, release readiness, publication checklist, distribution docs, release owner handoff, reviewer evidence, release asset checks, maturity evidence, and generated examples now identify v0.9.3 as the current release line.
- Demo screenshot guidance now links to the deterministic visual evidence receipt command.
- Release manifests now include the visual evidence receipt, evidence handoff audit artifacts, and current release documents.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map release-assets
python scripts/privacy_scan.py
git diff --check
```

Expected version output: `0.9.3`.

## Safety Boundary

The release remains educational research review only. It does not add live data, network calls, credentials, workflows, recommendations, ratings, price targets, portfolio actions, broker connections, or personalized investment, legal, accounting, tax, buy, sell, or hold advice.
