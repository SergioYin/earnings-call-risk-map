# Usage

`earnings-call-risk-map` is a zero-dependency Python CLI for turning public earnings-call notes, transcript excerpts, KPI observations, evidence links, and static-data dates into a deterministic research review artifact.

It is intentionally conservative:

- It uses keyword scoring, not financial forecasting.
- It preserves stale/static data warnings.
- It does not produce personalized buy, sell, hold, tax, legal, or accounting advice.
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
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --html-out examples/output/demo_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

The first command verifies imports, the next two print Markdown reports for the software fixture and the capital-intensive energy/infrastructure fixture, the fourth writes a self-contained HTML dashboard, the fifth writes a focused review-queue export, the sixth reports package audit parity, and the seventh writes deterministic demo bundles under `examples/output/`.

The final command writes a basic release maturity evidence bundle listing test commands, generated artifact paths, the public skill path, the release review template path, and privacy scan status.

`demo` preserves the original `demo_*` filenames for `examples/input/demo_company.json` and also writes `energy_infrastructure_snapshot.json`, `energy_infrastructure_report.md`, `energy_infrastructure_dashboard.html`, `energy_infrastructure_review_queue.json`, and `energy_infrastructure_review_queue.md` for `examples/input/demo_energy_infrastructure.json`.

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
python -m earnings_call_risk_map analyze examples/input/demo_company.json --html-out dashboard.html
python -m earnings_call_risk_map review-queue examples/input/demo_company.json --json-out review_queue.json --md-out review_queue.md
python -m earnings_call_risk_map demo --out-dir examples/output
python -m earnings_call_risk_map compare before.json after.json --md-out compare.md
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
- catalysts in date order

## Focused Review Queue

`review-queue` analyzes one fixture and emits only items that need source review for at least one of these deterministic reasons:

- stale or unverified data
- missing evidence URL
- high-impact language, defined as risk or opportunity score `>= 7`

When no output path is supplied, the command prints Markdown. Supplying `--json-out`, `--md-out`, or both writes deterministic files suitable for review handoff or demos.

## Package Audit

`audit` emits a deterministic parity report in JSON or Markdown. It includes the package version, command list, fixture count, output artifact count, workflow-file absence, and whether the public agent skill exists at `skills/agent/earnings-call-risk-map/SKILL.md`.

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

Optional lists:

- `notes`: transcript excerpts or research notes with `id`, `date`, `topic`, `type`, `text`, and `evidence_url`; use `type` values such as `management_claim`, `analyst_question`, or `user_synthesis` when provenance matters
- `kpis`: KPI observations with `name`, `value`, `direction`, `date`, `observation`, and `evidence_url`
- `catalysts`: dated events with `date`, `title`, `description`, `expected_impact`, and `evidence_url`

The repository includes two current demo fixtures plus one prior-period comparison fixture:

- `examples/input/demo_company.json`: compact software-style company example.
- `examples/input/demo_energy_infrastructure.json`: capital-intensive energy/infrastructure example with project catalysts, KPI observations, stale static data, and intentionally missing evidence URLs.
- `examples/input/demo_company_prior.json`: earlier snapshot for `compare` examples.

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
