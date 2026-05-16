# Changelog

## 0.1.0 - 2026-05-17

Initial deterministic release.

### Added

- Zero-dependency Python package and CLI for public earnings-call risk-map review.
- Commands: `analyze`, `review-queue`, `demo`, `compare`, `audit`, `manifest`, `maturity-evidence`, and `version`.
- Static-data badges for current, stale, and date-unverified notes, KPIs, and catalysts.
- Deterministic Markdown, JSON, and self-contained HTML outputs for the demo fixtures.
- Focused review-queue exports for stale data, missing evidence, and high-impact language.
- Package audit, release manifest, maturity evidence, privacy scan, and local selfcheck tooling.
- Public agent skill at `skills/agent/earnings-call-risk-map/SKILL.md`.
- Release notes at `docs/release-notes-v0.1.0.md`.

### Release Artifacts

- Example inputs: `examples/input/demo_company.json`, `examples/input/demo_company_prior.json`, and `examples/input/demo_energy_infrastructure.json`.
- Example outputs: `examples/output/demo_*`, `examples/output/energy_infrastructure_*`, `examples/output/package_audit.*`, and `examples/output/integration_notes.json`.
- Documentation: `README.md`, `docs/usage.md`, `docs/input-schema.md`, `docs/scoring.md`, `docs/gallery.md`, `docs/integrations.md`, and `docs/release-readiness.md`.
- Verification: `tests/`, `scripts/selfcheck.py`, `scripts/privacy_scan.py`, and `release_manifest.json`.

### Safety

- Outputs include educational research review language and do not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.
- Management claims, analyst questions, and user synthesis are kept as separate source-boundary categories.
- No workflow files, external services, API keys, databases, or runtime package dependencies are required.
