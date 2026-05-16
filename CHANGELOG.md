# Changelog

## 0.2.0 - 2026-05-17

Promotion-oriented public release.

### Added

- Public-source static Apple case-study fixture with Apple investor-relations/newsroom and SEC EDGAR source URLs.
- `source_attribution` fields in fixtures, analyzed snapshots, scored items, catalysts, and review-queue exports.
- Source Attribution sections in Markdown reports, review-queue Markdown, and static HTML dashboards.
- Stronger static educational case-study warning in dashboards.
- Public case-study documentation at `docs/public-case-study.md`.
- Release notes at `docs/release-notes-v0.2.0.md`.

### Changed

- `demo` now emits `public_apple_static_case_study_*` artifacts in addition to the synthetic software and energy/infrastructure examples.
- Package version is now `0.2.0`.

### Safety

- Public case-study artifacts are explicitly static, source-attributed, and non-advice.
- No workflow files, private context, API keys, databases, or runtime package dependencies are added.

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
