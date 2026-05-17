# Promotion Page Outline

This outline is public landing-page copy for `earnings-call-risk-map`. It is meant for a README badge link, project page, release page, or static demo page. Keep the copy factual, artifact-led, and bounded by the same non-advice language used in generated reports.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Outputs are source-review prompts and should be checked against filings, transcripts, and other source material.

## Audience

- Analysts, builders, and reviewers who already collect earnings-call notes, KPI observations, catalysts, dates, and evidence links.
- Users who want deterministic local artifacts instead of a hosted workflow, API-backed product, spreadsheet formula sheet, or LLM summarizer.
- Review owners who need visible stale/static labels, source attribution, and handoff files before discussion in a portfolio-risk or thesis-ledger process.

## Hero Copy

Headline:

Turn earnings-call notes into deterministic risk maps, review queues, and static dashboards.

Subhead:

A zero-dependency Python CLI that reads local JSON fixtures and writes Markdown, JSON, JSONL, and self-contained HTML artifacts. No LLM, database, API key, workflow dependency, live market feed, or network call is required.

Primary calls to action:

- View the [static demo index](demo-index.html).
- Read the [2-minute usage guide](usage.md).
- Open the [gallery](gallery.md).

Proof points:

- Local-only, inspectable runs from checked-out files.
- Deterministic scoring with visible stale/static badges.
- Review queues for stale data, missing evidence, and high-impact language.
- Source boundaries for management claims, analyst questions, and user synthesis.
- Generated handoff packets for adjacent review workflows.

## Demo Artifacts To Screenshot

Use artifacts that already exist in `examples/output/` so the page remains reproducible from a fresh checkout.

| Screenshot | Artifact | Why It Belongs On The Page |
| --- | --- | --- |
| Main dashboard hero | `examples/output/public_apple_static_case_study_dashboard.html` | Shows static public-source attribution, non-live-data labels, stale/static badges, summary tiles, and review panels in one view. |
| Static preview fallback | `docs/assets/showcase-dashboard-preview.svg` | PNG-free preview for places that need a lightweight image without rendering HTML. |
| Demo index | `docs/demo-index.html` | Shows the local static artifact hub and proves the demo does not need a hosted service. |
| Review queue | `examples/output/demo_review_queue.md` | Shows concise human-review output for stale data, missing evidence, and high-impact language. |
| Compare narrative | `examples/output/demo_compare.md` | Shows deterministic before/after score movement with interpretation language that stays away from investment conclusions. |
| Source-rich case study report | `examples/output/public_apple_static_case_study_report.md` | Shows public-source attribution and static case-study warnings in Markdown. |
| Handoff packet | `examples/output/handoff_packet.md` | Shows how generated artifacts can move into portfolio-risk or thesis-ledger review without creating advice. |
| Fixture map | `examples/output/case_study_map.md` | Shows sector coverage, reviewer questions, and generated artifacts across bundled fixtures. |

Screenshot framing should follow [Pages Demo](pages-demo.md): capture the dashboard top through the summary tiles, keep the static educational case-study warning visible, and include either source attribution or the first risk/review rows when space allows.

## Page Sections

1. Hero: state the local deterministic workflow and show the dashboard screenshot.
2. What It Generates: Markdown reports, JSON snapshots, JSON Lines review queues, static HTML dashboards, compare reports, handoff packets, and release evidence.
3. Why It Exists: repeatable earnings-review triage with explicit source and freshness boundaries.
4. Compare Narrative: explain how this differs from spreadsheets, generic notes, LLM summarizers, and hosted research tools.
5. Artifact Walkthrough: link to dashboard, review queue, compare report, public static case study, gallery, and demo index.
6. Boundary Statement: repeat the educational research review and non-advice language.
7. Local Verification: show the `demo`, `audit`, `selfcheck`, and `unittest` commands.

## Comparison Narrative

Use this positioning:

- Compared with spreadsheets, this tool is narrower but more repeatable for source-bound earnings-review triage. It does not replace financial models, formulas, pivots, charts, scenario tables, or live collaborative editing.
- Compared with generic notes, this tool is less flexible but better at producing consistent reports, review queues, snapshots, dashboard HTML, and machine-readable handoff files.
- Compared with LLM summarizers, this tool does not infer, summarize, or draft conclusions from raw transcripts. It scores explicit user-provided fixture fields with deterministic keyword rules.
- Compared with hosted research tools, this package is local-first and no-network by design. It does not fetch live market data, read credentials, store user data, or require workflow runners.

Short version:

Use notes for open-ended thinking, spreadsheets for models, and this CLI for repeatable review artifacts.

Link to [Comparison To Spreadsheets And Generic Notes](comparison-to-spreadsheets.md) for the full tradeoff table.

## Boundaries

The public page must preserve these boundaries:

- Do not claim live market data, current company coverage, investment recommendations, valuation support, price targets, expected returns, or portfolio actions.
- Do not describe deterministic scores as facts about company quality, security attractiveness, or future performance.
- Do not present bundled fixtures as current analysis. The public Apple fixture is a static educational case study with explicit `as_of` and `data_cutoff` dates.
- Do not hide stale/static data warnings, missing-evidence prompts, source attribution, or the non-advice disclaimer for cleaner marketing copy.
- Do not imply the tool verifies management claims or analyst questions. It preserves them as source-bound review inputs.
- Do not imply a hosted service, database, API, workflow automation, or network-backed product exists.

Safe phrasing:

- "Risk attention increased in the deterministic score."
- "Review this stale/static item against current source materials."
- "The fixture records this as a management claim."
- "The source contains an analyst question; treat it as a prompt, not a factual claim."
- "The output is a review artifact, not buy, sell, hold, tax, legal, or accounting advice."

For canonical safety language, see [Non-Advice Boundary](non-advice-boundary.md), [Case Study Limitations](case-study-limitations.md), and [Source Attribution Guide](source-attribution-guide.md).

## Verification Commands

Use these commands before publishing or updating screenshots:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m unittest discover -s tests
python scripts/privacy_scan.py
```

These commands should stay local-only and should not require API keys, tokens, proxies, hosted runners, or live network access.
