# Source Boundary Evidence

- Tool version: `0.8.0`
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

## Fixture Evidence

| Fixture | Ticker | Cutoff | Boundary | Source domains | Static notices | Private path |
| --- | --- | --- | --- | --- | ---: | --- |
| examples/input/demo_company.json | EXM | 2026-04-30 | static_fixture | example.com | 0 | False |
| examples/input/demo_energy_infrastructure.json | NGLP | 2026-04-25 | static_fixture | example.com | 0 | False |
| examples/input/consumer_hardware.json | LOGI | 2024-04-29 | static_public_source_fixture | ir.logitech.com | 7 | False |
| examples/input/semiconductor_equipment.json | ASML | 2025-01-29 | static_public_source_fixture | www.asml.com | 10 | False |
| examples/input/public_apple_static_case_study.json | AAPL | 2024-05-02 | static_public_source_fixture | www.apple.com, www.sec.gov | 8 | False |
| examples/input/demo_company_prior.json | EXM | 2026-01-31 | static_compare_baseline | example.com | 0 | False |

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
