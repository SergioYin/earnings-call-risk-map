# earnings-call-risk-map

Turn public earnings-call notes into a deterministic risk, opportunity, catalyst, and human-review map.

This is a zero-dependency Python CLI for researchers who want inspectable outputs without an LLM, database, API key, workflow dependency, or live market feed. It reads JSON fixtures, scores review topics with deterministic rules, preserves source boundaries, and writes Markdown, JSON, and self-contained HTML dashboards.

Start from a checkout:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json
```

Open [examples/output/demo_dashboard.html](examples/output/demo_dashboard.html) for the static dashboard, or read [docs/usage.md](docs/usage.md) for command details.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Outputs preserve stale/static data warnings and should be reviewed against source materials.

## Contents

- [Badges And Links](#badges-and-links)
- [Local-Only No-Network Guarantee](#local-only-no-network-guarantee)
- [2-Minute Walkthrough](#2-minute-walkthrough)
- [Static-Data Badge](#static-data-badge)
- [Integration Examples](#integration-examples)
- [Research Playbooks](#research-playbooks)
- [Quickstart](#quickstart)
- [Commands](#commands)
- [Fixture Schema](#fixture-schema)
- [Repository Layout](#repository-layout)
- [Verification](#verification)

## Badges And Links

![Static dashboard preview](docs/assets/showcase-dashboard-preview.svg)

**Release:** `v0.6.0` | **Runtime dependencies:** `0` | **Workflows:** `none` | **Preview format:** `SVG + static HTML`

- [Pages demo guide](docs/pages-demo.md)
- [Analyst tutorial](docs/tutorial-earnings-review.md)
- [Gallery](docs/gallery.md)
- [Distribution guide](docs/distribution.md)
- [Research playbooks](examples/playbooks/README.md)
- [Non-advice boundary](docs/non-advice-boundary.md)
- [Case study limitations](docs/case-study-limitations.md)
- [v0.6.0 release notes draft](docs/release-notes-v0.6.0.md)
- [Demo dashboard HTML](examples/output/demo_dashboard.html)
- [PNG-free screenshot substitute](examples/output/showcase_dashboard_preview.svg)

The project keeps financial-safety boundaries explicit:

- Management claims are source-provided company statements or prepared remarks. The tool surfaces them for review and does not verify them as facts.
- Analyst questions are source-provided prompts from Q&A or research materials. They are treated as questions, not assertions.
- User synthesis is user-authored notes, tags, and deterministic tool scoring. It is a review aid, not investment advice or a recommendation.

## Local-Only No-Network Guarantee

All package commands are designed to run from local files only. They do not call APIs, open sockets, fetch live market data, read credential environment variables, require workflow runners, or require a database.

The `audit` command records this guarantee in machine-readable form. Its local-only checks verify:

- `pyproject.toml` declares no runtime package dependencies.
- Package and script sources contain no network-client imports.
- Package and script sources contain no credential environment variable reads.
- No `.github/workflows` files are required to run the package commands.

The test suite also runs every CLI subcommand with a minimal credential-free environment to confirm the commands do not need API keys, tokens, secrets, passwords, proxies, or cloud credentials.

## 2-Minute Walkthrough

From a source checkout:

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/public_apple_static_case_study.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --html-out examples/output/demo_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json
PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl
PYTHONPATH=src python -m earnings_call_risk_map handoff-packet --md-out examples/output/handoff_packet.md --json-out examples/output/handoff_packet.json
PYTHONPATH=src python -m earnings_call_risk_map playbooks --format markdown --out examples/output/playbooks.md
PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format markdown
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

What just happened:

1. `version` confirms the package imports cleanly.
2. `analyze` reads the software demo fixture and prints a Markdown risk map.
3. The second `analyze` command runs a capital-intensive energy/infrastructure fixture with project catalysts, KPIs, stale badges, and missing evidence.
4. The public Apple static case study demonstrates source attribution from public investor-relations/newsroom and SEC EDGAR URLs without claiming live data.
5. `analyze --html-out` writes a self-contained static dashboard with no external JS or CSS.
6. `review-queue` writes a focused queue containing only stale data, missing evidence, and high-impact language.
7. `review-queue-jsonl` writes deterministic JSON Lines across the bundled demo fixtures for downstream review handoff.
8. `handoff-packet` writes portfolio/thesis handoff metadata with report, review-queue JSONL, compare paths, and cautions.
9. `playbooks` writes available research playbooks and recommended CLI sequences.
10. `compare` writes deterministic before/after score movement for the prior and current software snapshots.
11. `audit` reports package parity: version, commands, fixture count, output artifact count, workflow absence, and skill presence.
12. `release-assets` validates the expected release notes, docs, generated examples, manifests, maturity evidence, skill, and review template for the current package version.
13. `demo` writes reproducible bundles for all fixtures: legacy `demo_*`, `demo_prior_*`, `demo_compare.*`, `energy_infrastructure_*`, `public_apple_static_case_study_*`, `demo_review_queue_items.jsonl`, `handoff_packet.*`, `handoff_packet_examples.*`, playbook catalogs, playbook output examples, package audit files, and `release_manifest.json`.
14. `maturity-evidence` writes a basic release evidence bundle with test commands, artifact paths, skill path, review template path, and privacy scan status.

Sample output excerpt:

```markdown
> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## Source Boundaries

- Management claims: source-provided company statements or prepared remarks; verify against filings and transcripts.
- Analyst questions: source-provided questions or prompts; they are not treated as factual claims.
- User synthesis: user-authored notes, tags, and deterministic tool scores; they are review prompts, not advice.

## Summary

- Risks: 3
- Opportunities: 3
- Review queue: 2
- Stale/static badges: 2

## Risks

- **gross margin**: 11 (high), `stale>90d`
  Evidence: https://example.com/exm/channel-check
- **Inventory days**: 4 (medium), `stale>90d`
  Evidence: https://example.com/exm/static-kpi

## Review Queue

- **gross margin**: data is stale; high-impact language
- **product launch**: missing evidence URL
```

Focused review-queue excerpt:

```markdown
## Summary

- Review items: 4
- Stale data: 2
- Missing evidence: 2
- High-impact language: 1
```

Compare interpretation excerpt:

```markdown
## How To Read This Compare

- Deltas compare deterministic keyword scores between analyzed snapshots; they are prompts for source review, not investment conclusions.
- Risk attention increased for: gross margin, Inventory days, revenue durability.
- Opportunity attention increased for: product launch.
```

## Static-Data Badge

Each note, KPI, and catalyst carries a date. The tool compares that date to the fixture's `as_of` date and labels the item:

- `current`: dated within 90 days.
- `stale>90d`: older than 90 days and preserved in the output instead of hidden.
- `date-unverified`: missing or invalid date metadata.

These badges are intentionally visible because a stale public KPI can look authoritative after its context has expired.

## Integration Examples

Outputs are plain Markdown, JSON, and self-contained HTML. They can be handed to adjacent research tools without adding runtime dependencies on those tools:

- [docs/tutorial-earnings-review.md](docs/tutorial-earnings-review.md) walks through an analyst-style review from fixture to report to review queue to compare.
- [docs/integrations.md](docs/integrations.md) shows mappings for thesis-ledger notes and portfolio risk review items.
- [docs/gallery.md](docs/gallery.md) lists the generated demo artifacts and machine-readable handoff examples.
- [docs/pages-demo.md](docs/pages-demo.md) explains how to view the static HTML dashboards locally and what to screenshot.
- [docs/public-case-study.md](docs/public-case-study.md) documents the static public-source Apple case study and its attribution boundary.
- [docs/case-study-limitations.md](docs/case-study-limitations.md) explains static source limitations, source freshness, fixture replacement, and non-advice safeguards.
- [docs/release-readiness.md](docs/release-readiness.md) documents the release review template and maturity evidence bundle.
- [docs/reviewer-evidence.md](docs/reviewer-evidence.md) summarizes exact reviewer verification commands, fresh clone validation, release assets, and maturity scores.
- `examples/output/integration_notes.json` contains static example records derived from the demo snapshot and review queue.

## Research Playbooks

The repo includes deterministic playbooks for recurring research workflows:

- [Quarterly Review](examples/playbooks/quarterly-review.md): full quarter-end report, review queue, dashboard, and compare flow.
- [Catalyst Check-In](examples/playbooks/catalyst-check-in.md): focused catalyst-date, stale-data, and missing-evidence review.
- [Post-Earnings Thesis Refresh](examples/playbooks/post-earnings-thesis-refresh.md): post-call source-boundary review before updating a thesis ledger or memo.

## Quickstart

Supported Python versions: Python `3.9` or newer.

Optional local install:

```bash
python -m pip install .
earnings-call-risk-map version
earnings-call-risk-map analyze examples/input/demo_company.json --json-out examples/output/demo_snapshot.json --md-out examples/output/demo_report.md --html-out examples/output/demo_dashboard.html
```

For `pipx`, wheel dry-run, and troubleshooting notes, see [docs/distribution.md](docs/distribution.md). The package is prepared for local distribution checks, but this repository does not require publishing to use the CLI.

## Commands

- `analyze`: reads one JSON fixture and writes or prints a Markdown report plus optional JSON snapshot and static HTML dashboard.
- `review-queue`: writes or prints deterministic Markdown/JSON for only stale data, missing evidence, and high-impact language.
- `review-queue-jsonl`: writes or prints deterministic JSON Lines review item records across bundled demo fixtures, including fixture context and normalized review item payloads.
- `handoff-packet`: writes or prints deterministic Markdown/JSON summarizing the report path, review queue JSONL path, compare path, handoff targets, and cautions for portfolio/thesis workflows.
- `playbooks`: writes or prints available research playbooks and recommended CLI sequences in Markdown or JSON.
- `demo`: builds `demo_*`, `energy_infrastructure_*`, and `public_apple_static_case_study_*` artifacts, package audit files, and a demo release manifest.
- `compare`: compares two analyzed JSON snapshots and adds a plain-language interpretation section. Positive deltas mean a topic drew more deterministic risk or opportunity score in the later snapshot; negative deltas mean the later snapshot drew less score. Deltas are review prompts only, so reviewers should verify source documents and freshness badges before treating a movement as resolved or newly material.
- `audit`: writes or prints package parity in JSON or Markdown.
- `release-assets`: writes or prints a JSON/Markdown checklist for expected release assets and exits nonzero when any are missing.
- `manifest`: writes a deterministic release manifest with file hashes.
- `maturity-evidence`: writes JSON and Markdown release maturity evidence under `reports/maturity` by default.
- `version`: prints the package version.

## Fixture Schema

Input fixtures are documented in [docs/input-schema.md](docs/input-schema.md). Required fields are `company`, `ticker`, `as_of`, and `data_cutoff`; dates must use valid `YYYY-MM-DD` strings. Validation errors include the fixture path and field name so malformed fixtures fail before scoring.

## Repository Layout

- `src/earnings_call_risk_map/`: standard-library-only package.
- `examples/input/`: deterministic public fixtures.
- `examples/output/`: demo output artifacts.
- `examples/playbooks/`: deterministic research workflow playbooks.
- `docs/assets/`: static documentation assets, including the SVG dashboard preview.
- `docs/`: usage, scoring, gallery, and integration notes.
- `reports/reviews/`: release review templates.
- `tests/`: `unittest` suite.
- `scripts/selfcheck.py`: local verification runner.
- `scripts/privacy_scan.py`: public-safety text scan.
- `scripts/maturity_evidence.py`: standalone release maturity evidence generator.
- `skills/agent/earnings-call-risk-map/SKILL.md`: public agent skill.

## Verification

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map audit
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
python scripts/privacy_scan.py
```

No `.github/workflows` files are included.
