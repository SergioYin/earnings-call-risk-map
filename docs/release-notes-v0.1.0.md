# Release Notes: v0.1.0

Release date: 2026-05-17

## Scope

v0.1.0 is the first deterministic public release of `earnings-call-risk-map`. It packages a standard-library-only Python CLI for converting public earnings-call notes into risk, opportunity, catalyst, stale-data, and human-review outputs.

## Included Capabilities

- `analyze` reads a fixture and writes Markdown, JSON, and optional static HTML outputs.
- `review-queue` emits focused stale-data, missing-evidence, and high-impact-language review items.
- `compare` reports deterministic deltas between analyzed snapshots.
- `demo` regenerates the bundled example outputs for the software and energy infrastructure fixtures.
- `audit` reports package parity, command inventory, fixture count, output artifact count, workflow absence, and skill presence.
- `manifest` writes file size and SHA-256 metadata for release contents.
- `maturity-evidence` writes JSON and Markdown evidence for local release review.
- `version` prints the package version.

## Release Contents

- Example inputs are in `examples/input/`.
- Generated example outputs are in `examples/output/`.
- User documentation is in `README.md` and `docs/`.
- Release review evidence is in `reports/`.
- Local verification tooling is in `scripts/`.
- The public agent skill is in `skills/agent/earnings-call-risk-map/SKILL.md`.
- Unit tests are in `tests/`.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
```

The root `release_manifest.json` records deterministic hashes for the release files, including key examples, docs, the agent skill, selfcheck tooling, and tests.

## Safety Boundary

This release is for educational research review only. It does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Outputs preserve source boundaries for management claims, analyst questions, and user synthesis.
