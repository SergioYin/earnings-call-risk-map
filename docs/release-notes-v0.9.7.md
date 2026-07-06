# Release Notes Draft: v0.9.7

v0.9.7 adds the release-owner compare blocker checklist for evidence handoff changes. It makes the release-owner decision surface explicit after `evidence-handoff-compare` by separating release blockers from review-required metadata changes.

## Added

- `release-owner-compare-blockers` CLI route and standalone console script.
- JSON and Markdown blocker checklist output for local `evidence-handoff-compare` JSON files.
- Checked-in generated blocker checklist artifacts:
  - `examples/output/release_owner_compare_blockers.json`
  - `examples/output/release_owner_compare_blockers.md`
- Tests covering blocker classification, review-required classification, Markdown rendering, and CLI file output.

## Behavior

Removed evidence, artifacts that became missing, removed boundaries, and safety notice changes are flagged as blockers. Added artifacts, byte/hash changes, role changes, freshness changes, and source-boundary metadata changes are flagged for release-owner review without approving a release.

## Release Readiness

- Package version is now `0.9.7`.
- Release owner handoff, publication checklist outputs, release assets, maturity evidence, package audit, doctor output, fresh-clone plan, and manifests identify `0.9.7` as the current package line.
- The v0.9.6 evidence handoff compare notes remain part of the evidence trail for the compare input this command consumes.

## Boundaries

The command is local-only and metadata-only. It uses checked-in or user-supplied static compare JSON files, does not fetch live market data, does not connect to brokers, does not use private data, and does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## Verification

```bash
PYTHONPATH=src python -m unittest tests.test_release_owner_compare_blockers tests.test_cli
PYTHONPATH=src python -m earnings_call_risk_map release-owner-compare-blockers --compare examples/output/evidence_handoff_compare.json --format json --output examples/output/release_owner_compare_blockers.json
PYTHONPATH=src python -m earnings_call_risk_map release-owner-compare-blockers --compare examples/output/evidence_handoff_compare.json --format markdown --output examples/output/release_owner_compare_blockers.md
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json
python scripts/privacy_scan.py
```
