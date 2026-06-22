# Release Notes Draft: v0.9.6

v0.9.6 adds release-to-release evidence handoff audit comparison. The package-internal version remains `0.9.3` for this bounded evidence increment, matching the current deterministic release evidence pattern.

## Added

- `evidence-handoff-compare` CLI route and standalone console script.
- JSON and Markdown comparison output for two local `evidence-handoff-audit` JSON files.
- Checked-in demo comparison inputs and outputs:
  - `examples/output/evidence_handoff_compare_demo_before.json`
  - `examples/output/evidence_handoff_compare_demo_after.json`
  - `examples/output/evidence_handoff_compare.json`
  - `examples/output/evidence_handoff_compare.md`
- Tests covering stable key matching, changed metadata fields, Markdown rendering, and CLI file output.

## Behavior

The comparison matches entries by stable `evidence_id` when present and otherwise by `relative_path`. It reports added, removed, changed, and unchanged counts. Changed entries include byte count, SHA-256 hash, presence, role, freshness, and source-boundary differences when those fields are available.

## Boundaries

The command is local-only and metadata-only. It uses checked-in or user-supplied static audit JSON files, does not fetch live market data, does not connect to brokers, does not use private data, and does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## Verification

```bash
PYTHONPATH=src python -m unittest tests.test_evidence_handoff_compare tests.test_evidence_handoff_audit
PYTHONPATH=src python -m earnings_call_risk_map evidence-handoff-compare --before examples/output/evidence_handoff_compare_demo_before.json --after examples/output/evidence_handoff_compare_demo_after.json --format json --output examples/output/evidence_handoff_compare.json
PYTHONPATH=src python -m earnings_call_risk_map evidence-handoff-compare --before examples/output/evidence_handoff_compare_demo_before.json --after examples/output/evidence_handoff_compare_demo_after.json --format markdown --output examples/output/evidence_handoff_compare.md
python scripts/privacy_scan.py
```
