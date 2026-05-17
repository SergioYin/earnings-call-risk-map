# Sector Adaptation: Semiconductor Equipment

Use this guide to adapt `earnings-call-risk-map` for semiconductor-equipment earnings review. The goal is a deterministic source-review packet for lithography, process equipment, metrology, inspection, deposition, etch, and wafer-fab-equipment companies.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Semiconductor-equipment outputs are source-bound review aids, not forecasts, ratings, price targets, or portfolio actions.

Start from the checked-in ASML public-source fixture, then replace it with your own dated source notes:

- Fixture: [examples/input/semiconductor_equipment.json](../examples/input/semiconductor_equipment.json)
- Generated report: [examples/output/semiconductor_equipment_report.md](../examples/output/semiconductor_equipment_report.md)
- Review queue: [examples/output/semiconductor_equipment_review_queue.md](../examples/output/semiconductor_equipment_review_queue.md)
- Dashboard: [examples/output/semiconductor_equipment_dashboard.html](../examples/output/semiconductor_equipment_dashboard.html)

For schema and attribution rules, keep [JSON Fixture Schema Reference](input-schema.md), [Source Attribution Guide](source-attribution-guide.md), [Risk Language Taxonomy](risk-language-taxonomy.md), [Case Study Limitations](case-study-limitations.md), and [Non-Advice Boundary](non-advice-boundary.md) open while editing.

## Adaptation Frame

Semiconductor-equipment reviews usually need sector-specific rows for:

- demand timing by end market, such as foundry, logic, memory, advanced packaging, and mature nodes
- order intake, backlog, cancellations, shipment timing, and customer pushouts
- export controls, licensing restrictions, China exposure, and regulatory uncertainty
- gross margin, installed-base services, utilization, mix, and high-NA or next-generation tool ramps
- supply-chain constraints, single-source components, field-service capacity, and lead times
- customer concentration, fab build schedules, capex digestion, and tool acceptance timing

Map these rows into the existing fixture shape instead of adding sector-only fields:

- Put company statements, prepared remarks, and release language in `notes` with `type: "management_claim"` or another provenance-focused type already accepted by the project.
- Put analyst Q&A prompts in `notes` with `type: "analyst_question"` so questions are not treated as factual assertions.
- Put reviewer interpretations in `notes` with `type: "user_synthesis"` and source attribution that identifies them as review aids.
- Put numerical observations such as bookings, backlog, revenue, margin, service mix, or installed-base metrics in `kpis`.
- Put earnings dates, investor days, annual-report checks, export-control updates, and major customer capex updates in `catalysts`.

## Minimum Source Packet

Before scoring, collect dated source records outside the tool. A practical semiconductor-equipment packet includes:

- latest earnings release or shareholder letter
- prepared remarks and Q&A transcript, when available
- annual report or 10-K/20-F risk factors
- investor presentation or capital markets day deck
- source notes for major regulatory or export-control updates when those are material to the fixture
- reviewer notes that explicitly say `user_synthesis` when they summarize or interpret the sources

Each source note should record `source_name`, `publisher`, `source_type`, `source_url`, `accessed_at`, and a `static_notice`. Use `accessed_at` only for the date the reviewer actually checked the source. Do not update it just because the local fixture was regenerated.

## Suggested Rows

Use rows like these as starting points, then replace the placeholder text with source-bound language:

| Area | Fixture location | Review wording |
| --- | --- | --- |
| Bookings and backlog | `kpis` or `notes` | "Review whether order intake and backlog support the stated shipment outlook." |
| Customer pushouts | `notes` | "Management or analyst discussion flagged customer schedule timing; verify against transcript context." |
| Export controls | `notes` and `catalysts` | "Review restrictions, licensing, and revenue-exposure language against current filings." |
| Memory cycle | `notes` | "Treat cycle commentary as date-sensitive; stale memory-demand notes should remain visible." |
| Gross margin mix | `kpis` | "Separate reported margin value from user interpretation about mix, utilization, or services." |
| New platform ramp | `catalysts` | "Track tool qualification, shipment, or customer acceptance milestones without calling them investment catalysts." |

## Local Workflow

Run the bundled semiconductor-equipment fixture:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze \
  examples/input/semiconductor_equipment.json \
  --md-out examples/output/semiconductor_equipment_report.md \
  --json-out examples/output/semiconductor_equipment_snapshot.json \
  --html-out examples/output/semiconductor_equipment_dashboard.html
```

Build the focused review queue:

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue \
  examples/input/semiconductor_equipment.json \
  --md-out examples/output/semiconductor_equipment_review_queue.md \
  --json-out examples/output/semiconductor_equipment_review_queue.json
```

Read score movement as review attention only. If you compare two periods, first analyze each period to JSON snapshots, then run `compare`. Positive deltas mean the later snapshot triggered more deterministic keyword attention for that topic. They do not mean business conditions improved or deteriorated without source verification.

## Static-Data Boundaries

The bundled ASML fixture is a static public-source example. It does not fetch current ASML data, current market prices, live filings, current transcripts, or real-time regulatory updates.

Preserve these boundaries in every semiconductor-equipment adaptation:

- Keep `as_of` and `data_cutoff` visible in the fixture and generated artifacts.
- Preserve stale/static badges instead of deleting rows that look old.
- Treat `accessed_at` as source-check metadata, not a freshness guarantee.
- Do not describe checked-in fixtures as current analysis merely because a public URL still resolves.
- Replace source text only after a reviewer has checked current source materials and updated the dates.
- Keep source attribution on management claims, analyst questions, KPIs, and catalysts.

## Non-Advice Boundaries

Semiconductor-equipment companies often have highly cyclical demand, large customer concentration, and regulation-sensitive revenue exposure. That makes the review queue useful, but it does not change the advice boundary.

Do not:

- convert deterministic risk or opportunity scores into buy, sell, hold, short, overweight, underweight, portfolio-weight, or price-target language
- infer suitability for a user's investment, tax, legal, or accounting situation
- present management claims as verified facts without independent review
- treat analyst questions as evidence that a condition exists
- call a product ramp, export-control update, or customer capex change an investable catalyst

Safer language:

- "risk attention increased for export controls; verify current filings and transcript language"
- "the fixture records management commentary about bookings and backlog"
- "this KPI is static and should be refreshed before reuse"
- "the analyst question raises a demand-timing topic; it is not a factual assertion"

## Review Checklist

Before sharing a semiconductor-equipment artifact:

- Run `analyze` and `review-queue` on the adapted fixture.
- Check that every material source has source attribution and an evidence URL or an explicit missing-evidence review item.
- Confirm stale rows still show `stale>90d` or `date-unverified` where appropriate.
- Confirm generated Markdown still includes the educational non-advice notice and source-boundary section.
- Run the local docs and validation checks described in [Non-Advice Boundary](non-advice-boundary.md#validation).
