# Maintenance

This routine is for the release owner maintaining the local demo bundle, docs, and generated evidence before a public tag or internal review.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Outputs preserve stale/static data warnings and should be reviewed against source materials.

## Release Owner Routine

Use this sequence when preparing a release candidate:

1. Review open changes and confirm unrelated work is intentionally included or excluded.
2. Run the self-check from a clean local environment.
3. Regenerate demo outputs, release assets, and maturity evidence.
4. Review generated diffs for fixture, schema, dashboard, and documentation drift.
5. Run the full test suite.
6. Complete `docs/release-readiness.md`, `docs/publication-checklist.md`, and `docs/reviewer-evidence.md` before tagging.

The release owner is responsible for checking that bundled fixtures remain static, source-attributed, and non-advice. Do not treat deterministic score changes as investment conclusions.

## Regeneration Commands

From the repository root:

```bash
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format markdown
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
PYTHONPATH=src python -m unittest
```

Useful focused checks:

```bash
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map fixture-catalog --format markdown --out examples/output/fixture_catalog.md
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary examples/input/semiconductor_equipment.json --md-out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md --json-out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json
PYTHONPATH=src python scripts/privacy_scan.py
```

If generated files change, inspect the Markdown, JSON, SVG, and HTML outputs before publishing. Generated artifacts are review evidence, not a substitute for release owner review.

## Known Boundaries

- Runtime dependencies remain zero unless a release explicitly changes that contract.
- Commands are local-only and must not fetch live market data, call APIs, open sockets, read credential environment variables, require a database, or depend on workflow runners.
- Fixtures are static educational examples. Replace stale or placeholder fixture data with user-collected source material only when provenance fields are available.
- Scores are deterministic review prompts. They must not be converted into price targets, financial forecasts, or buy, sell, hold actions.
- `source_type`, note `type`, `evidence_url`, `accessed_at`, `as_of`, and `data_cutoff` are part of the review boundary and should not be filled with invented values.
- The privacy scan is a maintenance guardrail, not a full data-loss-prevention system.

## No-Workflow-Scope Policy

This project intentionally has no required `.github/workflows` scope. Do not add CI, release automation, scheduled jobs, hosted runners, or workflow-only release steps as part of routine maintenance.

Maintainers may document commands that a human release owner runs locally. Any future workflow proposal should be handled as a separate scoped change with explicit review of local-only guarantees, credential handling, and public release risk.

