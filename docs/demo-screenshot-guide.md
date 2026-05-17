# Demo Screenshot Guide

Use this guide when choosing generated artifacts for README visuals, release notes, gallery pages, or a public demo page. The best screenshots should show the actual local artifacts, preserve source and stale-data labels, and keep the educational non-advice boundary visible.

## Best Screenshot Targets

- `examples/output/public_apple_static_case_study_dashboard.html`: best primary README screenshot. It shows the static public-source case study, source attribution, stale/static labels, risk and opportunity panels, review queue signals, and the non-advice boundary in one browser-viewable artifact.
- `examples/output/demo_dashboard.html`: good compact fallback when the README needs a smaller software-style fixture with summary tiles and risk/review panels.
- `examples/output/energy_infrastructure_dashboard.html`: good sector-contrast screenshot when the story is capital projects, catalysts, stale/static project data, or software-vs-energy infrastructure comparison.
- `examples/output/consumer_hardware_dashboard.html`: good sector-contrast screenshot for hardware launch, supply chain, inventory, and margin review examples.
- `examples/output/semiconductor_equipment_dashboard.html`: good sector-contrast screenshot for backlog, export control, China exposure, supply chain, and equipment-cycle examples.
- `docs/assets/showcase-dashboard-preview.svg`: best PNG-free README visual when the repository page should render without a browser screenshot file. This is a documentation asset copy.
- `examples/output/showcase_dashboard_preview.svg`: best release artifact copy of the PNG-free preview SVG.
- `docs/demo-index.html`: good overview screenshot when the visual should show the local static demo launcher and the range of bundled artifacts.

## Good README Visuals

Prefer visuals that answer "what does the tool produce?" without requiring live services:

- Static HTML dashboards that can be opened directly from disk.
- The PNG-free preview SVG when a stable README image is better than a manually captured screenshot.
- A short crop of `examples/output/demo_review_queue.md` or `examples/output/public_apple_static_case_study_review_queue.md` when the README section is about human review handoff.
- A short crop of `examples/output/demo_compare.md` when the README section is about deterministic prior-vs-current comparison.
- A short crop of `examples/output/case_study_map.md` when the README section is about bundled fixtures and sector coverage.
- A short crop of `examples/output/handoff_packet.md` when the README section is about downstream thesis-ledger or portfolio-risk handoff.
- A short crop of `examples/output/promotion_pack.md` when preparing a release page or external project listing.

## Screenshot Framing

For dashboard screenshots:

- Capture the top of the dashboard through the summary tiles.
- Keep the static educational case-study warning or non-advice notice visible.
- Include source attribution or stale/static labels when space allows.
- Include the review queue panel when the screenshot is meant to explain analyst handoff.
- Use a browser window wide enough that summary tiles and risk panels are legible.

For Markdown screenshots:

- Use sections with headings, counts, artifact paths, source-boundary notes, or review queue items.
- Keep crops short enough for README readability.
- Prefer generated Markdown artifacts over manually rewritten summaries.

## Less Useful Visuals

These artifacts are useful for tests, integrations, and reproducibility, but they usually make poor screenshots:

- `examples/output/*_snapshot.json`: complete machine-readable analysis snapshots.
- `examples/output/*_review_queue.json`: machine-readable review queues.
- `examples/output/demo_review_queue_items.jsonl`: downstream handoff records.
- `examples/output/release_manifest.json`: release parity inventory.
- `examples/output/package_audit.json` and `examples/output/doctor.json`: machine-readable verification outputs.
- `docs/schema-reference.json`: schema reference for validation and docs tests.

Use these JSON and JSONL files as linked evidence or downloadable artifacts instead of README images.

## Boundaries

Do not use screenshots to imply live market data, real-time monitoring, price targets, buy/sell/hold recommendations, or personalized investment advice. Preserve the stale/static badges, source attribution, and the visible notice:

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

Related docs: [Pages Demo](pages-demo.md), [Gallery](gallery.md), [Promotion Page Outline](promotion-page-outline.md), [Source Attribution Guide](source-attribution-guide.md), and [Non-Advice Boundary](non-advice-boundary.md).
