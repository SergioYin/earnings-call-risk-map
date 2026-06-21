# Release Notes Draft: v0.9.4

Draft date: 2026-06-22

## Scope

v0.9.4 is a bounded post-release evidence hygiene increment for the v0.9.x evidence set. It makes the release evidence trail explicit without changing package internals, fixture behavior, scoring, generated report semantics, CLI routes, or the package version expected by the current test suite.

The package-internal version remains `0.9.3` for this hygiene increment. Treat this note as the public evidence pointer for the post-release documentation pass layered on top of the v0.9.3 package line.

## Added

- Release notes draft at [docs/release-notes-v0.9.4.md](release-notes-v0.9.4.md).
- README and changelog references that identify v0.9.4 as the post-release evidence hygiene increment while preserving the package-internal `0.9.3` version.
- Release-readiness and reviewer-evidence pointers that distinguish the v0.9.4 documentation evidence note from the v0.9.3 package release assets.

## Changed

- The top-level release evidence pointer now links to the v0.9.4 evidence hygiene note.
- The v0.9.3 package version, CLI version output, release-owner command examples, and generated package-version fields remain unchanged where tests and deterministic artifacts expect `0.9.3`.
- Deterministic release manifests should be regenerated after this note is added so the new document and updated hashes are captured.

## Verification

Targeted verification for this increment:

```bash
PYTHONPATH=src python -m unittest tests.test_docs tests.test_cli
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json
PYTHONPATH=src python -m earnings_call_risk_map manifest --out examples/output/release_manifest.json
git diff --check
```

Expected package version output remains `0.9.3`.

## Safety Boundary

This increment remains documentation and evidence hygiene only. It does not add live data, network calls, credentials, workflow requirements, recommendations, ratings, price targets, portfolio actions, broker connections, or personalized investment, legal, accounting, tax, buy, sell, or hold advice.
