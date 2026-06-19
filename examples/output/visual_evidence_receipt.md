# Visual Evidence Receipt

Deterministic checklist for reviewing public demo screenshots from checked-in static artifacts.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

- Tool version: `0.9.3`
- Source doc: `docs/demo-screenshot-guide.md`
- Source-boundary artifact: `examples/output/source_boundary_evidence.json`
- Primary screenshot target: `examples/output/public_apple_static_case_study_dashboard.html`

## Boundary Claims

- No live data: This evidence bundle is generated from bundled local fixture JSON files only. It does not fetch live market data, broker data, filings, API data, or earnings-call transcripts.
- No broker: No broker, portfolio, order, account, credential, or personalized holding data is used.
- No personalized advice: No personalized investment, legal, accounting, tax, buy, sell, or hold advice is provided.
- No advice: Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.
- Public-source fixture limit: Public-source fixtures are checked-in static examples with source attribution metadata. They are limited to repository evidence and must not be presented as current market data, verified transcript coverage, broker data, or personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## Checks

- All Screenshot Targets Exist: `True`
- Primary Target Exists: `True`
- Primary Target Has Required Markers: `True`
- All Visual Targets Public Safe: `True`
- Source Attribution Referenced: `True`
- Stale Or Static Warning Referenced: `True`
- Public Source Fixture Limits Recorded: `True`
- No Live Data Boundary Recorded: `True`
- No Broker Boundary Recorded: `True`
- No Personalized Advice Boundary Recorded: `True`

## Screenshot Evidence Checklist

- Keep visible source attribution, source-boundary labels, or stale/static warnings in the screenshot crop.
- Use checked-in static HTML, Markdown, or SVG artifacts only; do not imply live dashboards or monitoring.
- Do not include browser profiles, private paths, account names, credentials, portfolio holdings, or secrets.
- Do not add price targets, ratings, recommendations, or buy/sell/hold language to screenshot captions.

## Screenshot Targets

| Target | Exists | Required markers | Blocked markers | Use |
| --- | --- | --- | --- | --- |
| examples/output/public_apple_static_case_study_dashboard.html | `True` | all present or not required | none | Best primary README screenshot. It shows the static public-source case study, source attribution, stale/static labels, risk and opportunity panels, review queue signals, and the non-advice boundary. |
| examples/output/demo_dashboard.html | `True` | all present or not required | none | Good compact fallback when the README needs a smaller software-style fixture. |
| examples/output/energy_infrastructure_dashboard.html | `True` | all present or not required | none | Good sector-contrast screenshot for capital projects, catalysts, and stale/static project data. |
| examples/output/consumer_hardware_dashboard.html | `True` | all present or not required | none | Good sector-contrast screenshot for hardware launch, supply chain, inventory, and margin review examples. |
| examples/output/semiconductor_equipment_dashboard.html | `True` | all present or not required | none | Good sector-contrast screenshot for backlog, export control, China exposure, and equipment-cycle examples. |
| docs/assets/showcase-dashboard-preview.svg | `True` | all present or not required | none | Best PNG-free README visual when the repository page should render without a browser screenshot file. |
| examples/output/showcase_dashboard_preview.svg | `True` | all present or not required | none | Best release artifact copy of the PNG-free preview SVG. |
| docs/demo-index.html | `True` | all present or not required | none | Good overview screenshot for the local static demo launcher and bundled artifacts. |

## Public-Source Fixture Limits

| Fixture | Ticker | Cutoff | Source domains | Static notices | Freshness boundary |
| --- | --- | --- | --- | ---: | --- |
| examples/input/consumer_hardware.json | LOGI | 2024-04-29 | ir.logitech.com | 7 | review freshness before reuse; static fixture dates are evidence metadata, not current analysis |
| examples/input/semiconductor_equipment.json | ASML | 2025-01-29 | www.asml.com | 10 | review freshness before reuse; static fixture dates are evidence metadata, not current analysis |
| examples/input/public_apple_static_case_study.json | AAPL | 2024-05-02 | www.apple.com, www.sec.gov | 8 | review freshness before reuse; static fixture dates are evidence metadata, not current analysis |

## Source Boundaries

- Management Claims: source-provided company statements or prepared remarks; verify against filings and transcripts
- Analyst Questions: source-provided questions or prompts; they are not treated as factual claims
- User Synthesis: user-authored notes, tags, and deterministic tool scores; review prompts, not advice
