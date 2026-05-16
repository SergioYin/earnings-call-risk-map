# Changelog

## 0.5.0 - 2026-05-17

Release-evidence and agent-workflow draft release.

### Added

- Release notes draft at `docs/release-notes-v0.5.0.md`.
- `fixture-catalog` CLI command and generated `examples/output/fixture_catalog.md`.
- `review-queue-jsonl` CLI command and generated `examples/output/demo_review_queue_items.jsonl`.
- Agent workflow guide at `docs/agent-workflow.md`.
- Earnings review tutorial at `docs/tutorial-earnings-review.md`.
- Fixture catalog documentation at `docs/fixture-catalog.md`.
- Local-only package audit section covering runtime dependencies, network-client imports, credential environment reads, workflow absence, and per-command network/credential requirements.
- Selfcheck coverage for review-queue JSONL output and required tutorial documentation markers.

### Changed

- README, usage, gallery, scoring, reviewer evidence, release readiness, and agent skill documentation now cover the v0.5.0 evidence workflow.
- Package audit JSON and Markdown now include local-only/no-network guarantee evidence.
- Demo output generation now writes review-queue JSONL records and a fixture catalog artifact.
- Maturity evidence now includes JSONL artifacts and the review-queue JSONL verification command.
- Package version is now `0.5.0`.

### Safety

- Local-only audit evidence explicitly records that commands require no network access, credentials, external services, workflow files, or runtime package dependencies.
- The release remains educational research review only and preserves the non-advice boundary.

## 0.4.0 - 2026-05-17

Packaging-readiness and final-polish release.

### Added

- Package distribution guide at `docs/distribution.md`.
- Local `pipx`, `pip`, editable install, and wheel build dry-run instructions.
- Supported Python version guidance for Python `3.9` or newer.
- Packaging troubleshooting notes for build tools, stale local installs, path issues, and stale artifacts.
- Release notes at `docs/release-notes-v0.4.0.md`.
- Selfcheck validation for local Markdown links in README and release documentation.

### Changed

- README links now point to v0.4.0 release notes and package distribution guidance.
- README first screen now gives cold users the project purpose, two quickest commands, static dashboard path, and non-advice boundary before deeper documentation.
- Release readiness references now point to v0.4.0 release notes and wheel dry-run guidance.
- Demo outputs, release manifests, package audit files, static dashboard previews, and maturity evidence were refreshed for the release candidate.
- Package version is now `0.4.0`.

### Safety

- Distribution instructions explicitly avoid publishing to PyPI or another package index.
- No workflow files, private context, API keys, databases, or runtime package dependencies are added.

## 0.3.0 - 2026-05-17

Showcase-oriented public release.

### Added

- Deterministic SVG dashboard preview at `examples/output/showcase_dashboard_preview.svg`.
- PNG-free documentation screenshot substitute at `docs/assets/showcase-dashboard-preview.svg`.
- Static Pages-style demo instructions at `docs/pages-demo.md`.
- README badge/link section for the local preview, gallery, Pages demo guide, release notes, and generated dashboard HTML.
- Release notes at `docs/release-notes-v0.3.0.md`.
- Internal review record at `reports/reviews/2026-05-17-v0.3.0-internal-review.md`.

### Changed

- `selfcheck` now verifies dashboard HTML and SVG preview files exist and do not contain script, linked stylesheet, image, or linked SVG asset markers.
- Maturity evidence includes SVG preview artifacts.
- Release readiness references now point to v0.3.0 release notes and preview assets.
- Package version is now `0.3.0`.

### Safety

- Preview assets are self-contained SVG/HTML and load no external assets.
- No workflow files, private context, API keys, databases, or runtime package dependencies are added.

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
