# Usage

`earnings-call-risk-map` is a zero-dependency Python CLI for turning earnings-call notes, KPI observations, evidence links, and static-data dates into deterministic review artifacts.

Related docs: [Comparison To Spreadsheets And Generic Notes](comparison-to-spreadsheets.md), [Comparison To Generic LLM Notes](comparison-to-generic-llm-notes.md), [Promotion Page Outline](promotion-page-outline.md), [Decision Ledger Integration](decision-ledger-integration.md), [Data Entry Checklist](data-entry-checklist.md), [Earnings Review Templates](templates.md), [Fixture Summary](fixture-summary.md), [Semiconductor Equipment Adaptation](sector-adaptation-semiconductor-equipment.md), [Troubleshooting](troubleshooting.md), [Risk Language Taxonomy](risk-language-taxonomy.md), and [Security And Privacy](security-and-privacy.md).

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
PYTHONPATH=src python -m earnings_call_risk_map handoff-packet --md-out examples/output/handoff_packet.md --json-out examples/output/handoff_packet.json
PYTHONPATH=src python -m earnings_call_risk_map playbooks --format markdown --out examples/output/playbooks.md
PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json
PYTHONPATH=src python -m earnings_call_risk_map fixture-catalog --out examples/output/fixture_catalog.md
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary examples/input/semiconductor_equipment.json --out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md
PYTHONPATH=src python -m earnings_call_risk_map case-study-map --format markdown --out examples/output/case_study_map.md
PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format markdown --out examples/output/template_catalog.md
PYTHONPATH=src python -m earnings_call_risk_map cheat-sheet --format markdown --out examples/output/command_cheat_sheet.md
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map evidence-handoff-audit --root . --format markdown --output examples/output/evidence_handoff_audit.md
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

These commands verify imports, generate Markdown/JSON/JSONL/HTML review artifacts, list fixtures/templates/playbooks/commands, and write release evidence. The public Apple case study demonstrates static investor-relations/SEC-style attribution without claiming live data.

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
python -m earnings_call_risk_map handoff-packet --json-out examples/output/handoff_packet.json --md-out examples/output/handoff_packet.md
python -m earnings_call_risk_map playbooks --format json --out examples/output/playbooks.json
python -m earnings_call_risk_map template-catalog --format json --out examples/output/template_catalog.json
python -m earnings_call_risk_map fixture-summary examples/input/semiconductor_equipment.json --format json --out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json
python -m earnings_call_risk_map demo --out-dir examples/output
python -m earnings_call_risk_map compare before.json after.json --json-out compare.json --md-out compare.md
python -m earnings_call_risk_map fixture-catalog --out examples/output/fixture_catalog.md
python -m earnings_call_risk_map audit --format json --out package_audit.json
python -m earnings_call_risk_map audit --format markdown --out package_audit.md
python -m earnings_call_risk_map evidence-handoff-audit --root . --format json --output examples/output/evidence_handoff_audit.json
python -m earnings_call_risk_map evidence-handoff-audit --root . --format markdown --output examples/output/evidence_handoff_audit.md
python -m earnings_call_risk_map release-assets --format markdown --out release_assets.md
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

Review queue prioritization is deterministic and explained in both JSON and Markdown output. JSON uses `prioritization.ordered_by`, `prioritization.severity_stale_interaction`, and `prioritization.human_handoff`:

- Items with more review issue categories appear first.
- Higher risk score is the next ordering key, followed by higher opportunity score.
- Topic and id are final tie-breakers so repeated runs stay stable.
- Severity and stale badges interact in two places: stale note data can add `+1` to risk severity before high-impact checks, and stale or unverified dates add a separate `stale_data` review category with a visible badge.
- A stale-only item can rank below a current item that combines missing evidence with high-impact language.

For human handoff, reviewers should verify stale data against current source documents, fill or reject missing evidence URLs with notes, and send high-impact or multi-issue items to portfolio-risk or thesis-ledger owners for their approval workflow.

When no output path is supplied, the command prints Markdown. Supplying `--json-out`, `--md-out`, or both writes deterministic files suitable for review handoff or demos.

## JSON Lines Review Queue

`review-queue-jsonl` analyzes the bundled demo fixtures and writes compact JSON Lines for downstream agents. Each line is one `review_queue_item` record with fixture context (`fixture_slug`, `fixture_path`, `company`, `ticker`, `as_of`, and `data_cutoff`), source boundaries, safety notice, and the normalized `review_item` payload.

The generated demo bundle writes `examples/output/demo_review_queue_items.jsonl`. It includes the current software, energy/infrastructure, public Apple static case-study, and prior-period software fixtures in deterministic fixture order.

## Portfolio/Thesis Handoff Packet

`handoff-packet` writes a small deterministic packet for downstream portfolio-risk and thesis-ledger workflows. It records the Markdown report path, review queue JSONL path, compare path, handoff targets, source boundaries, safety notice, and cautions about stale data, source verification, deterministic score movement, and downstream ownership of decisions.

By default it points at the generated demo artifacts:

```bash
python -m earnings_call_risk_map handoff-packet
python -m earnings_call_risk_map handoff-packet --format json
```

Use explicit paths when handing off a custom run:

```bash
python -m earnings_call_risk_map handoff-packet \
  --report-path reports/acme_report.md \
  --review-queue-jsonl-path reports/acme_review_items.jsonl \
  --compare-path reports/acme_compare.md \
  --json-out reports/acme_handoff_packet.json \
  --md-out reports/acme_handoff_packet.md
```

## Research Playbooks

`playbooks` prints available research playbooks and the recommended local CLI sequence for each. Markdown is the default output for reviewer handoff; `--format json` writes the same catalog as structured data for automation.

The generated demo bundle writes `examples/output/playbooks.md`, `examples/output/playbooks.json`, `examples/output/playbook_output_examples.md`, and `examples/output/playbook_output_examples.json`.

## Publication Checklist

`publication-checklist` prints the public GitHub release owner checklist in Markdown or JSON. It mirrors the owner steps in `docs/publication-checklist.md`, including release-candidate checks, smoke checks, privacy scan, public skill path review, tag creation, `gh release create`, and post-publish smoke commands.

The generated demo bundle writes `examples/output/publication_checklist.md` and `examples/output/publication_checklist.json`.

## Template Catalog

`template-catalog` prints available blank templates, recommended top-level, note, KPI, and catalyst fields, suggested domain rows, and starter `analyze`/`review-queue` commands. Markdown is the default output; `--format json` writes the same catalog as structured data for automation.

The generated demo bundle writes `examples/output/template_catalog.md` and `examples/output/template_catalog.json`.

## Fixture Summary

`fixture-summary` prints a compact Markdown or JSON checkpoint for one fixture. It reports company context, source type counts, stale badge rows, source-boundary labels, and counts for notes, KPIs, catalysts, risks, opportunities, review queue items, stale badges, and source attribution records.

Use it during cold-user onboarding after selecting or filling a fixture and before reading the full report. It helps a reviewer confirm source coverage and freshness without starting from the dashboard or a long analysis report. See [Fixture Summary](fixture-summary.md) for the onboarding workflow.

The generated demo bundle writes `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md` and `examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json`.

## Case Study Map

`case-study-map` prints the bundled case study map in Markdown or JSON. It lists each fixture, target sector, useful reviewer question, generated artifacts, shared demo artifacts, and regenerate commands.

The generated demo bundle writes `examples/output/case_study_map.md` and `examples/output/case_study_map.json`.

## Data Entry Checklist

`data-entry-checklist` prints the fixture author checklist in Markdown or JSON. It covers source-boundary rules, field mappings, final review checks, and validation commands for converting transcripts, filing excerpts, and reviewer notes into JSON fixtures.

The generated demo bundle writes `examples/output/data_entry_checklist.md` and `examples/output/data_entry_checklist.json`.

## Demo Screenshot Guide

`demo-screenshot-guide` prints screenshot target, README visual, framing, and boundary guidance in Markdown or JSON. It mirrors `docs/demo-screenshot-guide.md` as structured CLI output for release artifacts and automation.

The generated demo bundle writes `examples/output/demo_screenshot_guide.md` and `examples/output/demo_screenshot_guide.json`.

## Command Cheat Sheet

`cheat-sheet` prints every public CLI command with a short purpose. Markdown is the default output; `--format json` writes the same command list as structured data for automation.

The generated demo bundle writes `examples/output/command_cheat_sheet.md` and `examples/output/command_cheat_sheet.json`.

## Compare Reports

`compare` expects two analyzed snapshots, not raw input fixtures. The demo bundle writes `examples/output/demo_prior_snapshot.json`, `examples/output/demo_snapshot.json`, `examples/output/demo_compare.json`, and `examples/output/demo_compare.md` to show the intended flow.

Positive deltas mean the later snapshot triggered more deterministic keyword score for that risk or opportunity topic. Negative deltas mean the later snapshot triggered less score. The "How To Read This Compare" section explains the movement as reviewer triage: it does not claim that a risk or opportunity has changed in the real world without source verification.

You can also compare two different fixture domains, such as the software demo and the energy infrastructure demo:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --json-out examples/output/demo_snapshot.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json --json-out examples/output/energy_infrastructure_snapshot.json
PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_snapshot.json examples/output/energy_infrastructure_snapshot.json --md-out examples/output/software_vs_energy_compare.md --json-out examples/output/software_vs_energy_compare.json
```

Read this as a cross-fixture contrast, not a time-series delta. Software-vs-energy infrastructure differences usually reflect fixture vocabulary, business model assumptions, source freshness, project/capital intensity, and evidence coverage. They do not rank companies, sectors, securities, or investment attractiveness, and they must not be converted into buy, sell, hold, portfolio-weight, or price-target advice.

## Package Audit

`audit` emits a deterministic parity report in JSON or Markdown. It includes the package version, command list, fixture count, output artifact count, workflow-file absence, and whether the public agent skill exists at `skills/agent/earnings-call-risk-map/SKILL.md`.

The audit report also includes a "Local-Only No-Network Guarantee" section. That section records `network_required: false` and `credentials_required: false` for every public command, plus checks for an empty runtime dependency list, absence of network-client imports, absence of credential environment variable reads, and absence of required workflow files.

For the security boundary behind those checks, see [Security And Privacy](security-and-privacy.md).

The demo bundle writes both `examples/output/package_audit.json` and `examples/output/package_audit.md`, then includes them in `examples/output/release_manifest.json`. The audit output files themselves are excluded from the output artifact count so repeated audit runs do not change the count.

## Evidence Handoff Audit

`evidence-handoff-audit` emits a deterministic reviewer handoff audit in JSON or Markdown. It checks local source fixtures, generated reports, review queues, dashboards, handoff packets, source-boundary evidence, visual evidence receipts, docs, and release evidence.

The report includes a schema label, summary counts, checked artifact rows with relative path, role, present/missing status, byte count, and SHA-256 hash, plus source, freshness, and review-readiness notes. It also lists missing and recommended evidence items, regeneration commands, and explicit local/static-fixture, no-live-data, no-broker, no-private-data, no-personalized-investment, legal, accounting, tax, buy, sell, and hold advice boundaries.

The command never embeds artifact file contents and redacts the absolute checkout root:

```bash
python -m earnings_call_risk_map evidence-handoff-audit --root . --format markdown
python -m earnings_call_risk_map evidence-handoff-audit --root . --format json --output examples/output/evidence_handoff_audit.json
```

After installation, the standalone console command is also available:

```bash
evidence-handoff-audit --root . --format markdown --output examples/output/evidence_handoff_audit.md
```

The demo bundle writes both `examples/output/evidence_handoff_audit.json` and `examples/output/evidence_handoff_audit.md`.

## Evidence Handoff Compare

`evidence-handoff-compare` compares two local evidence handoff audit JSON files and emits deterministic JSON or Markdown. It matches entries by stable `evidence_id` when available and otherwise by `relative_path`, then reports added, removed, changed, and unchanged counts.

Changed entries list metadata differences only: byte count, SHA-256 hash, presence, role, freshness fields, and source-boundary fields when present. The command does not read live market data, connect to brokers, fetch URLs, inspect private data, or provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

```bash
python -m earnings_call_risk_map evidence-handoff-compare --before examples/output/evidence_handoff_compare_demo_before.json --after examples/output/evidence_handoff_compare_demo_after.json --format markdown
python -m earnings_call_risk_map evidence-handoff-compare --before examples/output/evidence_handoff_compare_demo_before.json --after examples/output/evidence_handoff_compare_demo_after.json --format json --output examples/output/evidence_handoff_compare.json
```

After installation, the standalone console command is also available:

```bash
evidence-handoff-compare --before examples/output/evidence_handoff_compare_demo_before.json --after examples/output/evidence_handoff_compare_demo_after.json --format markdown --output examples/output/evidence_handoff_compare.md
```

The demo bundle writes `examples/output/evidence_handoff_compare_demo_before.json`, `examples/output/evidence_handoff_compare_demo_after.json`, `examples/output/evidence_handoff_compare.json`, and `examples/output/evidence_handoff_compare.md`.

## Release Readiness

`release-assets` validates the expected release notes, documentation, generated examples, manifests, maturity evidence, public skill, and review template for the current package version. It emits JSON or Markdown and exits with code `1` when any expected asset is missing.

`manifest` writes deterministic file metadata for release contents. The included `examples/output/release_manifest.json` entry uses the `<self-referential-manifest>` SHA marker and a null byte count so rerunning the command does not change only because the manifest contains that generated manifest entry.

`maturity-evidence` writes `maturity_evidence.json` and `maturity_evidence.md` under the selected output directory. The bundle records local test commands, generated artifact paths, the public skill path, release review template presence, and the current result from `scripts/privacy_scan.py`.

The same generator is available as a script:

```bash
python scripts/maturity_evidence.py --out-dir reports/maturity
```

See [Release Readiness](release-readiness.md) for the checklist workflow and template path.

## Input Shape

See [JSON Fixture Schema Reference](input-schema.md) for the complete field reference and validation examples, and [Source Attribution Guide](source-attribution-guide.md) for `source_type`, `accessed_at`, stale badges, and source-boundary choices.

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

The repository includes public/static demo fixtures plus one prior-period comparison fixture:

- `examples/input/demo_company.json`: compact software-style company example.
- `examples/input/demo_energy_infrastructure.json`: capital-intensive energy/infrastructure example with project catalysts, KPI observations, stale static data, and intentionally missing evidence URLs.
- `examples/input/consumer_hardware.json`: public-source consumer hardware fixture with investor-relations source attribution.
- `examples/input/semiconductor_equipment.json`: public-source semiconductor equipment fixture with ASML investor-relations source attribution.
- `examples/input/public_apple_static_case_study.json`: static public-source Apple case study with Apple and SEC URLs, source attribution, and non-live-data labels.
- `examples/input/demo_company_prior.json`: earlier snapshot for `compare` examples.

See [Fixture Catalog](fixture-catalog.md) for tickers, data cutoffs, static/live status, and recommended commands for each bundled fixture.

For a sector-specific walkthrough of the ASML-style fixture, see [Semiconductor Equipment Adaptation](sector-adaptation-semiconductor-equipment.md). It covers demand timing, bookings, backlog, export controls, product ramps, non-advice wording, and static-data boundaries.

Reusable blank templates live under `examples/templates/`:

- `examples/templates/software_earnings_review.json`
- `examples/templates/energy_infrastructure_earnings_review.json`
- `examples/templates/consumer_hardware_earnings_review.json`

See [Earnings Review Templates](templates.md) or run `python -m earnings_call_risk_map template-catalog` for recommended fields and commands.

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
