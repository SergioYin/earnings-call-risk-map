# Source Boundary Evidence

- Tool version: `0.9.2`
- Fixture count: 6

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Boundary Claims

- No live data: This evidence bundle is generated from bundled local fixture JSON files only. It does not fetch live market data, broker data, filings, API data, or earnings-call transcripts.
- No advice: Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.
- Reviewer handoff: Cold reviewers can verify fixture existence, source metadata, static boundaries, and generated handoff artifacts from repository files without broker/API credentials or private paths.

## Checks

- All Fixture Paths Exist: `True`
- All Fixtures Are Static Or Local: `True`
- No Private Paths Found: `True`
- No Live Fetching Required: `True`
- No Broker Or Api Credentials Required: `True`
- No Advice Claim Present: `True`
- Walkthrough Receipt Present: `True`

## Fixture Evidence

| Fixture | Ticker | Cutoff | Boundary | Source domains | Static notices | Private path |
| --- | --- | --- | --- | --- | ---: | --- |
| examples/input/demo_company.json | EXM | 2026-04-30 | static_fixture | example.com | 0 | False |
| examples/input/demo_energy_infrastructure.json | NGLP | 2026-04-25 | static_fixture | example.com | 0 | False |
| examples/input/consumer_hardware.json | LOGI | 2024-04-29 | static_public_source_fixture | ir.logitech.com | 7 | False |
| examples/input/semiconductor_equipment.json | ASML | 2025-01-29 | static_public_source_fixture | www.asml.com | 10 | False |
| examples/input/public_apple_static_case_study.json | AAPL | 2024-05-02 | static_public_source_fixture | www.apple.com, www.sec.gov | 8 | False |
| examples/input/demo_company_prior.json | EXM | 2026-01-31 | static_compare_baseline | example.com | 0 | False |

## Walkthrough Receipt

- Receipt type: `public_source_boundary_walkthrough`
- Scope: cold reviewer verification of checked-in static fixtures, public-source metadata, dashboard and release-owner handoff artifacts, and no-live-data/no-advice boundaries
- Public-source fixture count: 3
- Fixture-scoped public-source demo receipts: 3
- Static/local fixture count: 6
- Missing receipt artifacts: 0

### Receipt Checks

- Public Source Fixtures Present: `True`
- All Public Source Demo Receipts Present: `True`
- All Public Source Demo Receipt Artifacts Exist: `True`
- All Receipt Artifacts Exist: `True`
- All Fixture Boundaries Static Or Local: `True`
- Dashboard Handoff Paths Recorded: `True`
- No Live Data Boundary Recorded: `True`
- No Advice Boundary Recorded: `True`

### Reviewer Walkthrough

1. Verify bundled static fixtures
   - Reviewer action: Open each examples/input/*.json fixture listed in this receipt and confirm company, ticker, as_of, data_cutoff, source attribution, evidence URLs, and static notices are checked-in metadata.
   - Boundary: Fixtures are static local examples; runtime generation does not fetch transcripts or live data.
   - Evidence paths: `examples/input/*.json`, `examples/output/fixture_catalog.md`
2. Verify source-boundary separation
   - Reviewer action: Confirm management_claim, analyst_question, user_synthesis, source_type, accessed_at, and stale badge language stay visible in generated reports and review queues.
   - Boundary: Source labels describe provenance and review posture; they are not source verification.
   - Evidence paths: `docs/source-attribution-guide.md`, `examples/output/source_boundary_evidence.md`, `examples/output/demo_review_queue_items.jsonl`
3. Verify dashboard and release-owner handoff
   - Reviewer action: Open the generated dashboard/report paths and handoff packet, then confirm downstream owners receive local artifact paths, review queues, and cautions rather than portfolio actions.
   - Boundary: Dashboard and handoff artifacts are static local outputs for reviewer workflow ownership.
   - Evidence paths: `docs/release-owner-handoff.md`, `examples/output/handoff_packet.md`, `examples/output/handoff_packet.json`, `examples/output/public_apple_static_case_study_dashboard.html`
4. Verify no-live-data and no-advice boundaries
   - Reviewer action: Check the safety notice, no-live-data claim, release manifest, and privacy/security docs before treating any fixture as a public demo or review handoff.
   - Boundary: Outputs are educational review prompts, not current analysis or buy, sell, or hold advice.
   - Evidence paths: `docs/non-advice-boundary.md`, `docs/security-and-privacy.md`, `examples/output/source_boundary_evidence.json`, `release_manifest.json`

### Fixture-Scoped Public-Source Demo Receipts

| Fixture | Ticker | Demo artifacts | Missing | Local-only |
| --- | --- | ---: | ---: | --- |
| examples/input/consumer_hardware.json | LOGI | 5 | 0 | True |
| examples/input/semiconductor_equipment.json | ASML | 5 | 0 | True |
| examples/input/public_apple_static_case_study.json | AAPL | 5 | 0 | True |

#### Demo Receipt Artifact Paths

- `consumer_hardware`:
  - `examples/output/consumer_hardware_snapshot.json` (deterministic analysis snapshot; exists: `True`)
  - `examples/output/consumer_hardware_report.md` (local Markdown report; exists: `True`)
  - `examples/output/consumer_hardware_dashboard.html` (self-contained static dashboard; exists: `True`)
  - `examples/output/consumer_hardware_review_queue.json` (review queue data; exists: `True`)
  - `examples/output/consumer_hardware_review_queue.md` (review queue handoff; exists: `True`)
- `semiconductor_equipment`:
  - `examples/output/semiconductor_equipment_snapshot.json` (deterministic analysis snapshot; exists: `True`)
  - `examples/output/semiconductor_equipment_report.md` (local Markdown report; exists: `True`)
  - `examples/output/semiconductor_equipment_dashboard.html` (self-contained static dashboard; exists: `True`)
  - `examples/output/semiconductor_equipment_review_queue.json` (review queue data; exists: `True`)
  - `examples/output/semiconductor_equipment_review_queue.md` (review queue handoff; exists: `True`)
- `public_apple_static_case_study`:
  - `examples/output/public_apple_static_case_study_snapshot.json` (deterministic analysis snapshot; exists: `True`)
  - `examples/output/public_apple_static_case_study_report.md` (local Markdown report; exists: `True`)
  - `examples/output/public_apple_static_case_study_dashboard.html` (self-contained static dashboard; exists: `True`)
  - `examples/output/public_apple_static_case_study_review_queue.json` (review queue data; exists: `True`)
  - `examples/output/public_apple_static_case_study_review_queue.md` (review queue handoff; exists: `True`)

## Source Boundaries

- Management Claims: source-provided company statements or prepared remarks; verify against filings and transcripts
- Analyst Questions: source-provided questions or prompts; they are not treated as factual claims
- User Synthesis: user-authored notes, tags, and deterministic tool scores; review prompts, not advice

## Reviewer Artifact Paths

- `examples/output/source_boundary_evidence.md`
- `examples/output/source_boundary_evidence.json`
- `examples/output/fixture_catalog.md`
- `examples/output/demo_review_queue_items.jsonl`
- `examples/output/handoff_packet.md`
- `examples/output/handoff_packet.json`

## Source Docs

- `docs/reviewer-evidence.md`
- `docs/non-advice-boundary.md`
- `docs/security-and-privacy.md`
- `docs/source-attribution-guide.md`
- `docs/fixture-catalog.md`
