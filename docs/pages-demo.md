# Pages Demo

The dashboard examples are static HTML files. They do not need a server, package install, JavaScript bundle, CSS framework, API key, database, workflow, or network access.

## View Locally

From a checkout, regenerate the examples if needed:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

Open one of these files directly in a browser:

- `examples/output/demo_dashboard.html`
- `examples/output/energy_infrastructure_dashboard.html`
- `examples/output/public_apple_static_case_study_dashboard.html`

For a Pages-style preview, use the same files as static artifacts. The repository also includes a PNG-free screenshot substitute at `docs/assets/showcase-dashboard-preview.svg` and a release artifact copy at `examples/output/showcase_dashboard_preview.svg`.

## What To Screenshot

Use `examples/output/public_apple_static_case_study_dashboard.html` for the main showcase screenshot because it demonstrates public source attribution, stale/static labels, the review queue, and the non-advice boundary.

Recommended framing:

- Capture the top of the dashboard through the four summary tiles.
- Include the static educational case-study warning.
- Include either the Source Attribution panel or the first row of risk/review panels when there is enough vertical space.
- Do not crop away the browser address or file path if the screenshot is meant to show local static viewing.

Do not add external fonts, hosted images, analytics snippets, or generated workflow files for the demo.
