# earnings-call-risk-map

Use this skill when a user needs a public, deterministic earnings-call research review artifact from JSON fixtures containing transcript excerpts, research notes, KPI observations, catalysts, evidence URLs, source attribution, and stale/static data dates.

## What It Does

- Produces Markdown and JSON risk/opportunity maps.
- Builds a human review queue for missing evidence, stale/static data, or high-impact language.
- Preserves source attribution for public investor-relations, SEC, transcript, or user-authored source records.
- Creates stale/static data badges for inputs older than the configured freshness threshold.
- Sorts catalysts into a timeline.
- Compares two analyzed snapshots.
- Generates a release manifest.

## Safety Boundary

Keep wording educational and research-oriented. Do not present the output as personalized investment, buy, sell, hold, tax, legal, or accounting advice. Preserve stale/static data warnings and ask the user to verify source materials.

Follow `docs/non-advice-boundary.md` when drafting responses around generated artifacts.

## Response Rules

- State that outputs are educational research review only when summarizing or sharing results.
- Do not tell a user to buy, sell, hold, short, overweight, underweight, enter, exit, rebalance, or otherwise take a securities action.
- Describe score movement as deterministic risk/opportunity attention, not as an investment conclusion.
- Preserve `safety_notice`, `source_boundaries`, source attribution, and stale/static badges in JSON or Markdown handoffs.
- Keep management claims, analyst questions, and user synthesis separated. Do not restate management claims as verified facts or analyst questions as assertions.
- Mention exact `as_of`, `data_cutoff`, and relevant access dates when freshness matters.
- If evidence is missing, stale, static, or high-impact, route it to human review rather than resolving it in the response.

## Workflow

1. Prepare a JSON input with `company`, `ticker`, `as_of`, `data_cutoff`, and optional `notes`, `kpis`, and `catalysts`.
2. Run:

   ```bash
   python -m earnings_call_risk_map analyze input.json --json-out snapshot.json --md-out report.md
   ```

3. For a demo bundle:

   ```bash
   python -m earnings_call_risk_map demo --out-dir examples/output
   ```

4. To compare two analyzed snapshots:

   ```bash
   python -m earnings_call_risk_map compare before.json after.json --json-out compare.json --md-out compare.md
   ```

5. Before sharing a public artifact, run:

   ```bash
   PYTHONPATH=src python -m unittest discover -s tests
   python scripts/selfcheck.py
   python scripts/privacy_scan.py
   ```

6. For release evidence, run:

   ```bash
   PYTHONPATH=src python -m earnings_call_risk_map audit
   PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
   ```

## Input Notes

Use ISO dates (`YYYY-MM-DD`). Include evidence URLs and `source_attribution` records where possible. Missing evidence and stale or unverified dates should remain visible in the review queue.

## Done Criteria

The task is done when the agent has:

- Selected the correct route from `docs/agent-workflow.md`: analyze, compare, review queue export, source attribution handoff, or a complete bundle.
- Preserved the educational research boundary and avoided personalized investment, legal, accounting, or tax advice.
- Kept `safety_notice`, `source_boundaries`, source attribution, evidence URLs, `as_of`, `data_cutoff`, and stale/static badges visible in generated or summarized outputs.
- Routed missing evidence, stale/static data, date-unverified items, and high-impact language to the human review queue instead of resolving them silently.
- Explained compare deltas as deterministic score movement between snapshots, not as a real-world business conclusion or securities recommendation.
- Used fixture-provided attribution for management claims, analyst questions, user synthesis, KPIs, and catalysts; any missing attribution is called out as a review item.
- Run the relevant local verification for public or release-facing handoffs: unit tests, `scripts/selfcheck.py`, `scripts/privacy_scan.py`, audit, and maturity evidence as applicable.
