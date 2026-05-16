# earnings-call-risk-map

Zero-dependency Python CLI for turning public earnings-call notes into a deterministic risk, opportunity, catalyst, and human-review map.

**Why star it:** this repo is a small, inspectable reference implementation for finance-adjacent research tooling that stays reproducible, static-data-aware, and public-safe without an LLM, database, API key, or workflow dependency. It is useful as a CLI, a fixture format, and a public agent-skill example.

This project is for educational research review only. It does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Outputs preserve stale/static data warnings and should be reviewed against source materials.

The project keeps financial-safety boundaries explicit:

- Management claims are source-provided company statements or prepared remarks. The tool surfaces them for review and does not verify them as facts.
- Analyst questions are source-provided prompts from Q&A or research materials. They are treated as questions, not assertions.
- User synthesis is user-authored notes, tags, and deterministic tool scoring. It is a review aid, not investment advice or a recommendation.

## 2-Minute Walkthrough

From a source checkout:

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --html-out examples/output/demo_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

What just happened:

1. `version` confirms the package imports cleanly.
2. `analyze` reads the software demo fixture and prints a Markdown risk map.
3. The second `analyze` command runs a capital-intensive energy/infrastructure fixture with project catalysts, KPIs, stale badges, and missing evidence.
4. `analyze --html-out` writes a self-contained static dashboard with no external JS or CSS.
5. `review-queue` writes a focused queue containing only stale data, missing evidence, and high-impact language.
6. `audit` reports package parity: version, commands, fixture count, output artifact count, workflow absence, and skill presence.
7. `demo` writes reproducible bundles for both fixtures: legacy `demo_*` artifacts for `demo_company.json`, `energy_infrastructure_*` artifacts for `demo_energy_infrastructure.json`, package audit files, and `release_manifest.json`.
8. `maturity-evidence` writes a basic release evidence bundle with test commands, artifact paths, skill path, review template path, and privacy scan status.

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

## Static-Data Badge

Each note, KPI, and catalyst carries a date. The tool compares that date to the fixture's `as_of` date and labels the item:

- `current`: dated within 90 days.
- `stale>90d`: older than 90 days and preserved in the output instead of hidden.
- `date-unverified`: missing or invalid date metadata.

These badges are intentionally visible because a stale public KPI can look authoritative after its context has expired.

## Integration Examples

Outputs are plain Markdown, JSON, and self-contained HTML. They can be handed to adjacent research tools without adding runtime dependencies on those tools:

- [docs/integrations.md](docs/integrations.md) shows mappings for thesis-ledger notes and portfolio risk review items.
- [docs/gallery.md](docs/gallery.md) lists the generated demo artifacts and machine-readable handoff examples.
- [docs/release-readiness.md](docs/release-readiness.md) documents the release review template and maturity evidence bundle.
- `examples/output/integration_notes.json` contains static example records derived from the demo snapshot and review queue.

## Quickstart

Optional local install:

```bash
python -m pip install .
earnings-call-risk-map version
earnings-call-risk-map analyze examples/input/demo_company.json --json-out examples/output/demo_snapshot.json --md-out examples/output/demo_report.md --html-out examples/output/demo_dashboard.html
```

## Commands

- `analyze`: reads one JSON fixture and writes or prints a Markdown report plus optional JSON snapshot and static HTML dashboard.
- `review-queue`: writes or prints deterministic Markdown/JSON for only stale data, missing evidence, and high-impact language.
- `demo`: builds `demo_*` output artifacts for `demo_company.json`, `energy_infrastructure_*` artifacts for `demo_energy_infrastructure.json`, package audit files, and a demo release manifest.
- `compare`: compares two analyzed JSON snapshots.
- `audit`: writes or prints package parity in JSON or Markdown.
- `manifest`: writes a deterministic release manifest with file hashes.
- `maturity-evidence`: writes JSON and Markdown release maturity evidence under `reports/maturity` by default.
- `version`: prints the package version.

## Fixture Schema

Input fixtures are documented in [docs/input-schema.md](docs/input-schema.md). Required fields are `company`, `ticker`, `as_of`, and `data_cutoff`; dates must use valid `YYYY-MM-DD` strings. Validation errors include the fixture path and field name so malformed fixtures fail before scoring.

## Repository Layout

- `src/earnings_call_risk_map/`: standard-library-only package.
- `examples/input/`: deterministic public fixtures.
- `examples/output/`: demo output artifacts.
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
