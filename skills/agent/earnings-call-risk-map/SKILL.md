# earnings-call-risk-map

Use this skill when a user needs a public, deterministic earnings-call research review artifact from JSON fixtures containing transcript excerpts, research notes, KPI observations, catalysts, evidence URLs, source attribution, and stale/static data dates.

## What It Does

- Produces Markdown and JSON risk/opportunity maps.
- Builds a human review queue for missing evidence, stale/static data, or high-impact language.
- Preserves source attribution for public investor-relations, SEC, transcript, or user-authored source records.
- Creates stale/static data badges for inputs older than the configured freshness threshold.
- Sorts catalysts into a timeline.
- Compares two analyzed snapshots.
- Lists blank input templates, recommended fields, and starter commands.
- Summarizes fixture source coverage, stale badges, and counts for cold-user onboarding.
- Maps bundled case-study fixtures to sectors, reviewer questions, and generated artifacts.
- Provides a data-entry checklist for turning source packets into public-safe JSON fixtures.
- Guides sector adaptation for semiconductor-equipment review without adding sector-only schema fields.
- Prints a public command cheat sheet.
- Renders current release notes evidence from the audit, release assets, and changelog.
- Points reviewers to the static local demo index.
- Generates a release manifest.
- Renders public-safe promotion packs for README, release, project-page, or static-demo copy.
- Renders fresh-clone verification plans for clean-checkout package review.
- Renders schema authoring references for hand-filled or worksheet-derived JSON fixtures.
- Guides generic agent workflows for coding, research, review, and boundary tasks.

## Safety Boundary

Keep wording educational and research-oriented. Do not present the output as personalized investment, buy, sell, hold, tax, legal, or accounting advice. Preserve stale/static data warnings and ask the user to verify source materials.

Keep the workflow local-only unless the user explicitly asks for a separate integration outside this package boundary. Do not request, infer, store, or depend on API keys, tokens, passwords, cloud credentials, proxies, databases, hosted services, live market feeds, or workflow runners for package commands. Do not add `.github/workflows` files as part of this skill workflow.

Follow `docs/known-limitations.md` for the consolidated static-data, no-live-fetching, scoring, source-trust, no-advice, and no-portfolio-suitability limits. Follow `docs/non-advice-boundary.md` when drafting responses around generated artifacts. Follow `docs/security-and-privacy.md` when discussing local-only operation, credential assumptions, workflow-file boundaries, or privacy scan results.

## Response Rules

- State that outputs are educational research review only when summarizing or sharing results.
- State that package commands are local-only and credential-free when discussing setup, audit, or release evidence.
- Do not tell a user to buy, sell, hold, short, overweight, underweight, enter, exit, rebalance, or otherwise take a securities action.
- Do not ask for credentials or suggest adding workflow files to run standard package commands.
- Describe score movement as deterministic risk/opportunity attention, not as an investment conclusion.
- Preserve `safety_notice`, `source_boundaries`, source attribution, and stale/static badges in JSON or Markdown handoffs.
- Keep management claims, analyst questions, and user synthesis separated. Do not restate management claims as verified facts or analyst questions as assertions.
- Mention exact `as_of`, `data_cutoff`, and relevant access dates when freshness matters.
- If evidence is missing, stale, static, or high-impact, route it to human review rather than resolving it in the response.
- Treat `scripts/privacy_scan.py` as a lightweight pattern scan, not proof that user fixtures are free of confidential information or personal data.
- Keep public handoffs limited to checked-in public docs, examples, generated outputs, and package reports. Do not expose private notes, credentials, unpublished customer data, or internal-only review commentary unless the user explicitly asks to inspect local internal files.
- For promotion, onboarding, and agent handoffs, keep claims factual and artifact-led. Do not imply live coverage, hosted services, API-backed operation, current company analysis, source verification, price targets, expected returns, workflow automation, or credential-backed integrations.
- For fresh-clone instructions, distinguish `git clone` and optional package install network use from package commands, which remain local-file only.

## Workflow

1. Prepare a JSON input with `company`, `ticker`, `as_of`, `data_cutoff`, and optional `notes`, `kpis`, and `catalysts`.
2. When authoring a new fixture from earnings-call notes, follow `docs/examples-from-scratch.md` so management claims, analyst questions, and user synthesis stay separate.
3. Run:

   ```bash
   python -m earnings_call_risk_map analyze input.json --json-out snapshot.json --md-out report.md
   ```

4. For a demo bundle:

   ```bash
   python -m earnings_call_risk_map demo --out-dir examples/output
   ```

5. To compare two analyzed snapshots:

   ```bash
   python -m earnings_call_risk_map compare before.json after.json --json-out compare.json --md-out compare.md
   ```

6. Before sharing a public artifact, run:

   ```bash
   PYTHONPATH=src python -m unittest discover -s tests
   python scripts/selfcheck.py
   python scripts/privacy_scan.py
   ```

7. For release evidence, run:

   ```bash
   PYTHONPATH=src python -m earnings_call_risk_map audit
   PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
   ```

## Agent Workflow Integration

Use `docs/agent-workflow-integration.md` together with `docs/agent-workflow.md` when operating as a generic coding or research agent. Classify the request before acting:

- Coding task: inspect or edit repository files, run focused tests, and report changed files plus verification.
- Research task: run local CLI commands on explicit fixtures and summarize only what generated artifacts contain.
- Review task: surface stale dates, missing evidence, high-impact language, source attribution, and review queue reasons.
- Boundary task: stop for human review or a user-provided source when the request needs live data, credentials, external verification, portfolio suitability, buy/sell/hold guidance, ratings, forecasts, allocations, or source-warning removal.

Run commands from the repository root against explicit local paths. After a command writes files, inspect both command status and artifact content for educational-only notices, `safety_notice`, `source_boundaries`, stale/static badges, evidence gaps, source attribution, `as_of`, and `data_cutoff`.

When handing off agent work, include files changed or generated, commands run, verification result for each command, remaining review items, and a note that no live data, source refresh, or investment advice was performed.

## Template Catalog Workflow

Use `template-catalog` when the user needs a blank fixture starting point, recommended fields, suggested domain rows, or starter commands:

```bash
PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format markdown --out examples/output/template_catalog.md
PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format json --out examples/output/template_catalog.json
```

In responses, describe the catalog as local fixture-authoring guidance. Do not imply that template rows are live data, verified coverage, or investment recommendations.

## Fixture Summary Workflow

Use `fixture-summary` when the user needs a short onboarding check before reading a full report, dashboard, or handoff packet. It reports source-type counts, stale/static badge rows, source-boundary labels, and fixture counts for notes, KPIs, catalysts, risks, opportunities, review queue items, stale badges, and source attribution records.

```bash
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary examples/input/semiconductor_equipment.json --out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary examples/input/semiconductor_equipment.json --format json --out examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json
```

Treat the summary as a source-coverage checkpoint, not as a scored conclusion. If counts, stale badges, source types, or source-boundary labels do not match the user's intended fixture shape, pause the analysis route and fix the fixture or route the gap to the review queue.

## Case Study Map Workflow

Use `case-study-map` when the user needs to choose or explain a bundled static fixture by sector, reviewer question, generated artifacts, or regeneration command:

```bash
PYTHONPATH=src python -m earnings_call_risk_map case-study-map --format markdown --out examples/output/case_study_map.md
PYTHONPATH=src python -m earnings_call_risk_map case-study-map --format json --out examples/output/case_study_map.json
```

Keep case-study language public-safe. Describe checked-in fixtures as static deterministic examples, not live company analysis. Point users to `docs/case-study-map.md`, `docs/case-study-limitations.md`, and `docs/public-case-study.md` when static-source freshness, fixture replacement, or public-source attribution matters.

## Data Entry Checklist Workflow

Use `data-entry-checklist` and `docs/data-entry-checklist.md` when the user is converting earnings-call notes, prepared remarks, Q&A, filings, press releases, investor-relations pages, or reviewer worksheets into a JSON fixture:

```bash
PYTHONPATH=src python -m earnings_call_risk_map data-entry-checklist --format markdown --out examples/output/data_entry_checklist.md
PYTHONPATH=src python -m earnings_call_risk_map data-entry-checklist --format json --out examples/output/data_entry_checklist.json
```

Do not invent source URLs, publishers, accessed dates, speaker roles, KPI values, fiscal periods, or evidence links. Leave missing evidence blank so the review queue can surface it. Keep management claims, analyst questions, and user synthesis separate, and use `accessed_at` only for sources the reviewer actually checked.

## Sector Adaptation Workflow

Use `docs/sector-adaptation-semiconductor-equipment.md` when the user wants a semiconductor-equipment earnings-review fixture or needs to adapt the workflow to lithography, process equipment, metrology, inspection, deposition, etch, wafer-fab equipment, or capital-equipment cycle review.

Start from `examples/input/semiconductor_equipment.json` only as a public static example. Map sector-specific topics into the existing schema: demand timing, order intake, backlog, cancellations, customer pushouts, export controls, gross margin, installed-base services, utilization, customer concentration, capex digestion, tool ramps, and acceptance timing should become `notes`, `kpis`, or `catalysts`, not new sector-only fields.

Run the adapted fixture locally:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/semiconductor_equipment.json --md-out examples/output/semiconductor_equipment_report.md --json-out examples/output/semiconductor_equipment_snapshot.json --html-out examples/output/semiconductor_equipment_dashboard.html
PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/semiconductor_equipment.json --md-out examples/output/semiconductor_equipment_review_queue.md --json-out examples/output/semiconductor_equipment_review_queue.json
```

When adapting to other sectors, reuse the same pattern: collect a dated source packet, preserve provenance, map sector concepts into the existing fixture fields, keep stale/static labels, and describe outputs as deterministic review aids rather than forecasts, ratings, or portfolio actions.

## Cheatsheet Workflow

Use `cheat-sheet` when the user needs the public CLI surface or a short command reference:

```bash
PYTHONPATH=src python -m earnings_call_risk_map cheat-sheet --format markdown --out examples/output/command_cheat_sheet.md
PYTHONPATH=src python -m earnings_call_risk_map cheat-sheet --format json --out examples/output/command_cheat_sheet.json
```

The demo bundle also writes `examples/output/command_cheatsheet.md` and `examples/output/command_cheatsheet.json` as compatibility aliases. Keep the cheat sheet public-safe: it should list package commands and purposes only, without credentials, private paths, hosted runners, or workflow files.

## Schema Authoring Workflow

Use `schema-authoring-reference` and `docs/schema-authoring-reference.md` when the user needs field-by-field fixture guidance for hand-written JSON, worksheet conversion, or source-packet normalization:

```bash
PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format markdown --out examples/output/schema_authoring_reference.md
PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format json --out examples/output/schema_authoring_reference.json
```

Treat fixtures as static review packets with required `company`, `ticker`, `as_of`, and `data_cutoff` fields plus optional `notes`, `kpis`, `catalysts`, and `source_attribution`. Use exact ISO dates, preserve management claims, analyst questions, and user synthesis as separate note types, and leave unknown URLs, publishers, speaker labels, KPI values, fiscal periods, or access dates blank instead of inventing them.

For machine-readable validation, point to `docs/schema-reference.json` and `docs/input-schema.md`. Do not describe additional fixture metadata as report-affecting unless the documented schema or renderer uses it.

## Promotion Pack Workflow

Use `promotion-pack` and `docs/promotion-page-outline.md` when the user needs public landing-page, README, release-page, project-page, or static-demo copy:

```bash
PYTHONPATH=src python -m earnings_call_risk_map promotion-pack --format markdown --out examples/output/promotion_pack.md
PYTHONPATH=src python -m earnings_call_risk_map promotion-pack --format json --out examples/output/promotion_pack.json
```

Keep promotion copy public-safe, factual, and artifact-led. It may describe deterministic local outputs such as Markdown reports, JSON snapshots, JSONL review queues, static HTML dashboards, compare reports, handoff packets, demo artifacts, and verification commands. It must preserve the educational research notice and avoid claims about live market data, current coverage, recommendations, valuation support, hosted services, databases, APIs, workflow runners, credentials, or network-backed products.

Before sharing a promotion pack, verify screenshots or linked demos come from checked-in docs or generated `examples/output/` artifacts, and keep static fixture warnings visible.

## Fresh Clone Plan Workflow

Use `fresh-clone-plan` and `docs/fresh-clone-verification.md` when the user needs clean-checkout verification instructions or package-review evidence:

```bash
PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format markdown --out examples/output/fresh_clone_plan.md
PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format json --out examples/output/fresh_clone_plan.json
```

Describe the plan as local verification that a clean clone imports, tests, generates artifacts, and preserves local-only boundaries. It may include `git clone`, virtual environment creation, editable install, demo generation, analyze, review queue, compare, audit, doctor, release assets, manifest, maturity evidence, privacy scan, JSON checks, artifact inventory, and `git diff --check`.

State that network is needed only for clone and optional install steps; package commands are local-file commands and do not require API keys, tokens, proxies, workflow runners, live feeds, or hosted services. Do not claim fresh-clone verification passed unless those commands were actually run and succeeded in the current or stated review environment.

## Release Notes Workflow

Use `release-notes` when the user needs current release evidence summarized from package audit, release asset validation, and the current changelog excerpt:

```bash
PYTHONPATH=src python -m earnings_call_risk_map release-notes --out docs/release-notes-v0.8.0.md
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format markdown
```

Before public release-note handoff, verify that the rendered notes preserve the educational-only notice, local-only audit status, release asset status, missing asset list, and changelog excerpt. Do not describe a draft as published, tagged, uploaded, or announced unless the user has explicitly performed that release step.

## v0.8 Verification Criteria

For v0.8 public or release-facing work, use `docs/reviewer-evidence.md` as the source of truth for exact local verification. The expected release line is `0.8.0`, and public handoffs should preserve the v0.8 release notes, maturity evidence, release asset list, and internal review reference.

Run the relevant subset, or the full set when validating a release candidate:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl
PYTHONPATH=src python -m earnings_call_risk_map playbooks --format markdown --out examples/output/playbooks.md
PYTHONPATH=src python -m earnings_call_risk_map audit
PYTHONPATH=src python -m earnings_call_risk_map release-assets
PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
python scripts/privacy_scan.py
git diff --check
```

Verification is only complete for public handoff when unit tests pass, selfcheck passes, privacy scan assumptions are stated, release assets resolve, maturity evidence reports the current v0.8 review source, `git diff --check` is clean, and generated or summarized artifacts still carry the educational-only, local-only, public-safe boundary.

## Demo Index Workflow

Use `docs/demo-index.html` when the user needs a local static entry point for generated demos and showcase artifacts. It must remain a local page with no scripts, no external targets, and links only to checked-in docs or generated example outputs.

If the user asks for a refreshed demo index, run:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m unittest tests.test_docs.DocsTests.test_demo_index_is_local_static_page
```

When describing the demo index, call out that bundled fixtures are static examples and not live market, filing, transcript, estimate, or news data.

## Input Notes

Use ISO dates (`YYYY-MM-DD`). Include evidence URLs and `source_attribution` records where possible. Missing evidence and stale or unverified dates should remain visible in the review queue.

For first-time fixture authoring from a raw earnings-call note, use `docs/examples-from-scratch.md` as the minimal template. Keep `management_claim`, `analyst_question`, and `user_synthesis` records as separate notes and preserve the provenance in `source_attribution`.

## Done Criteria

The task is done when the agent has:

- Selected the correct route from `docs/agent-workflow.md`: analyze, compare, review queue export, source attribution handoff, or a complete bundle.
- Used `docs/examples-from-scratch.md` when creating a fixture from raw earnings-call notes.
- Preserved the educational research boundary and avoided personalized investment, legal, accounting, or tax advice.
- Kept `safety_notice`, `source_boundaries`, source attribution, evidence URLs, `as_of`, `data_cutoff`, stale/static badges, and known limitations visible in generated or summarized outputs when relevant.
- Routed missing evidence, stale/static data, date-unverified items, and high-impact language to the human review queue instead of resolving them silently.
- Explained compare deltas as deterministic score movement between snapshots, not as a real-world business conclusion or securities recommendation.
- Used fixture-provided attribution for management claims, analyst questions, user synthesis, KPIs, and catalysts; any missing attribution is called out as a review item.
- For template-catalog tasks, generated or inspected the Markdown/JSON catalog and described it as fixture-authoring guidance, not live research coverage.
- For fixture-summary tasks, generated or inspected the Markdown/JSON summary and treated it as source-coverage onboarding, not as a replacement for full analysis.
- For case-study-map tasks, generated or inspected the Markdown/JSON map and kept bundled fixture descriptions static, deterministic, and non-live.
- For data-entry-checklist tasks, used the checklist to avoid invented source details and left missing evidence visible.
- For sector-adaptation tasks, mapped sector-specific review topics into existing fixture fields and preserved public-source, stale/static, and non-advice boundaries.
- For cheatsheet tasks, generated or inspected the public command list and kept it free of credentials, private paths, workflow files, and hosted-runner assumptions.
- For release-notes tasks, preserved audit status, release asset status, missing asset disclosure, changelog excerpt, and educational/non-advice wording; draft notes are not represented as a completed release.
- For demo-index tasks, confirmed `docs/demo-index.html` stays script-free, external-link-free, and limited to local checked-in or generated public artifacts.
- For schema-authoring tasks, generated or inspected the Markdown/JSON reference, preserved the documented field meanings, used ISO dates, and left unknown source or KPI details visible instead of fabricating them.
- For promotion-pack tasks, generated or inspected the Markdown/JSON pack, kept copy artifact-led and public-safe, and avoided live-data, recommendation, hosted-service, API, workflow-runner, credential, or source-verification claims.
- For fresh-clone-plan tasks, generated or inspected the Markdown/JSON plan, kept the clone/install assumptions separate from local package command behavior, and did not mark verification passed without executed evidence.
- For agent workflow integration tasks, classified the request as coding, research, review, or boundary work; reported changed/generated files, commands, verification, remaining review items, and the no-live-data/no-advice boundary.
- For v0.8 public or release-facing tasks, verified the expected `0.8.0` release line, v0.8 release notes, release assets, maturity evidence, reviewer evidence, and internal review reference remain aligned.
- Run the relevant local verification for public or release-facing handoffs: unit tests, `scripts/selfcheck.py`, `scripts/privacy_scan.py`, audit, and maturity evidence as applicable.
- Preserved the security boundary in `docs/security-and-privacy.md`: local-only operation, no credentials, no required workflow files, and explicit privacy scan assumptions.
