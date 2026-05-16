# Usage

`earnings-call-risk-map` is a zero-dependency Python CLI for turning public earnings-call notes, transcript excerpts, KPI observations, evidence links, and static-data dates into a deterministic research review artifact.

It is intentionally conservative:

- It uses keyword scoring, not financial forecasting.
- It preserves stale/static data warnings.
- It does not produce personalized buy, sell, hold, tax, legal, or accounting advice.
- It runs locally from checked-out files and does not require network access, API keys, tokens, secrets, passwords, proxies, cloud credentials, workflow runners, or databases.
- It expects users to verify source documents before relying on the output.

Every Markdown report repeats the non-advice disclaimer and separates source provenance:

- Management claims are company-provided statements or prepared remarks from source material.
- Analyst questions are questions or prompts from Q&A or analyst materials, not factual assertions.
- User synthesis is user-authored notes, labels, and deterministic scoring output; it is a review prompt, not a recommendation.

## 2-Minute Demo

Run the demo directly from a checkout:

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/public_apple_static_case_study.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --html-out examples/output/demo_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json
PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl
PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json
PYTHONPATH=src python -m earnings_call_risk_map fixture-catalog --out examples/output/fixture_catalog.md
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

The first command verifies imports, the next two print Markdown reports for the software fixture and the capital-intensive energy/infrastructure fixture, and the public Apple static case study demonstrates investor-relations/SEC-style source attribution without claiming live data. The HTML command writes a self-contained dashboard, `review-queue` writes a focused review export, `review-queue-jsonl` writes one deterministic JSON Lines record per demo review item for agent ingestion, `compare` writes prior/current score movement with interpretation, `fixture-catalog` lists bundled fixtures and recommended commands, `audit` reports package parity, and `demo` writes deterministic bundles under `examples/output/`.

The final command writes a basic release maturity evidence bundle listing test commands, generated artifact paths, the public skill path, the release review template path, and privacy scan status.

`demo` preserves the original `demo_*` filenames for `examples/input/demo_company.json` and also writes `demo_prior_*` and `demo_compare.*` artifacts for the prior/current compare example, `energy_infrastructure_*` files for `examples/input/demo_energy_infrastructure.json`, and `public_apple_static_case_study_*` files for `examples/input/public_apple_static_case_study.json`.

The report starts with a compact research queue:

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
```

## Commands

```bash
python -m earnings_call_risk_map version
python -m earnings_call_risk_map analyze examples/input/demo_company.json
python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json
python -m earnings_call_risk_map analyze examples/input/public_apple_static_case_study.json
python -m earnings_call_risk_map analyze examples/input/demo_company.json --html-out dashboard.html
python -m earnings_call_risk_map review-queue examples/input/demo_company.json --json-out review_queue.json --md-out review_queue.md
python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl
python -m earnings_call_risk_map demo --out-dir examples/output
python -m earnings_call_risk_map compare before.json after.json --json-out compare.json --md-out compare.md
python -m earnings_call_risk_map fixture-catalog --out examples/output/fixture_catalog.md
python -m earnings_call_risk_map audit --format json --out package_audit.json
python -m earnings_call_risk_map audit --format markdown --out package_audit.md
python -m earnings_call_risk_map manifest --out release_manifest.json
python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

## Static HTML Dashboard

`analyze --html-out dashboard.html` writes a deterministic, self-contained dashboard. It includes inline CSS only, no JavaScript, and no external stylesheets. The demo bundle writes the same view as `examples/output/demo_dashboard.html`.

The dashboard summarizes:

- risk and opportunity counts
- review-queue count and reasons
- stale/static data badges
- source attribution and static case-study labels
- catalysts in date order

## Focused Review Queue

`review-queue` analyzes one fixture and emits only items that need source review for at least one of these deterministic reasons:

- stale or unverified data
- missing evidence URL
- high-impact language, defined as risk or opportunity score `>= 7`

When no output path is supplied, the command prints Markdown. Supplying `--json-out`, `--md-out`, or both writes deterministic files suitable for review handoff or demos.

## JSON Lines Review Queue

`review-queue-jsonl` analyzes the bundled demo fixtures and writes compact JSON Lines for downstream agents. Each line is one `review_queue_item` record with fixture context (`fixture_slug`, `fixture_path`, `company`, `ticker`, `as_of`, and `data_cutoff`), source boundaries, safety notice, and the normalized `review_item` payload.

The generated demo bundle writes `examples/output/demo_review_queue_items.jsonl`. It includes the current software, energy/infrastructure, public Apple static case-study, and prior-period software fixtures in deterministic fixture order.

## Compare Reports

`compare` expects two analyzed snapshots, not raw input fixtures. The demo bundle writes `examples/output/demo_prior_snapshot.json`, `examples/output/demo_snapshot.json`, `examples/output/demo_compare.json`, and `examples/output/demo_compare.md` to show the intended flow.

Positive deltas mean the later snapshot triggered more deterministic keyword score for that risk or opportunity topic. Negative deltas mean the later snapshot triggered less score. The "How To Read This Compare" section explains the movement as reviewer triage: it does not claim that a risk or opportunity has changed in the real world without source verification.

## Package Audit

`audit` emits a deterministic parity report in JSON or Markdown. It includes the package version, command list, fixture count, output artifact count, workflow-file absence, and whether the public agent skill exists at `skills/agent/earnings-call-risk-map/SKILL.md`.

The audit report also includes a "Local-Only No-Network Guarantee" section. That section records `network_required: false` and `credentials_required: false` for every public command, plus checks for an empty runtime dependency list, absence of network-client imports, absence of credential environment variable reads, and absence of required workflow files.

The demo bundle writes both `examples/output/package_audit.json` and `examples/output/package_audit.md`, then includes them in `examples/output/release_manifest.json`. The audit output files themselves are excluded from the output artifact count so repeated audit runs do not change the count.

## Release Readiness

`maturity-evidence` writes `maturity_evidence.json` and `maturity_evidence.md` under the selected output directory. The bundle records local test commands, generated artifact paths, the public skill path, release review template presence, and the current result from `scripts/privacy_scan.py`.

The same generator is available as a script:

```bash
python scripts/maturity_evidence.py --out-dir reports/maturity
```

See [Release Readiness](release-readiness.md) for the checklist workflow and template path.

## Input Shape

See [JSON Fixture Schema Reference](input-schema.md) for the complete field reference and validation examples.

Required top-level fields:

- `company`
- `ticker`
- `as_of`
- `data_cutoff`

Optional attribution:

- `source_attribution`: top-level or per-item public-source records with `source_name`, `publisher`, `source_type`, `source_url`, `accessed_at`, and `static_notice`

Optional lists:

- `notes`: transcript excerpts or research notes with `id`, `date`, `topic`, `type`, `text`, and `evidence_url`; use `type` values such as `management_claim`, `analyst_question`, or `user_synthesis` when provenance matters
- `kpis`: KPI observations with `name`, `value`, `direction`, `date`, `observation`, and `evidence_url`
- `catalysts`: dated events with `date`, `title`, `description`, `expected_impact`, and `evidence_url`

The repository includes three current demo fixtures plus one prior-period comparison fixture:

- `examples/input/demo_company.json`: compact software-style company example.
- `examples/input/demo_energy_infrastructure.json`: capital-intensive energy/infrastructure example with project catalysts, KPI observations, stale static data, and intentionally missing evidence URLs.
- `examples/input/public_apple_static_case_study.json`: static public-source Apple case study with Apple and SEC URLs, source attribution, and non-live-data labels.
- `examples/input/demo_company_prior.json`: earlier snapshot for `compare` examples.

See [Fixture Catalog](fixture-catalog.md) for tickers, data cutoffs, static/live status, and recommended commands for each bundled fixture.

Dates must use `YYYY-MM-DD` format and must be valid calendar dates. Items older than 90 days relative to `as_of` receive a stale/static data badge.

Invalid fixtures fail before scoring with field-specific messages, for example:

```text
error: examples/input/bad.json.as_of must use YYYY-MM-DD format, got '2026/05/15'
```

## Static-Data Badges

The badge is a freshness warning, not a score modifier by itself:

- `current`: item date is within 90 days of `as_of`.
- `stale>90d`: item date is more than 90 days older than `as_of`.
- `date-unverified`: item date is missing or could not be validated.

Stale and unverified items remain in the output so reviewers can decide whether the underlying source still matters.
