# earnings-call-risk-map

Use this skill when a user needs a public, deterministic earnings-call research review artifact from JSON fixtures containing transcript excerpts, research notes, KPI observations, catalysts, evidence URLs, and stale/static data dates.

## What It Does

- Produces Markdown and JSON risk/opportunity maps.
- Builds a human review queue for missing evidence, stale/static data, or high-impact language.
- Creates stale/static data badges for inputs older than the configured freshness threshold.
- Sorts catalysts into a timeline.
- Compares two analyzed snapshots.
- Generates a release manifest.

## Safety Boundary

Keep wording educational and research-oriented. Do not present the output as personalized investment, buy, sell, hold, tax, legal, or accounting advice. Preserve stale/static data warnings and ask the user to verify source materials.

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
   python scripts/selfcheck.py
   python scripts/privacy_scan.py
   ```

## Input Notes

Use ISO dates (`YYYY-MM-DD`). Include evidence URLs where possible. Missing evidence and stale or unverified dates should remain visible in the review queue.
