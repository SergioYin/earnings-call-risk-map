# FAQ

This FAQ is for cold users who are opening the project for the first time and for analysts who want to understand where the tool fits in a research review workflow.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source documents before relying on any item.

## Does This Use Live Data?

No. The CLI runs against local JSON fixtures and does not fetch live market data, live transcripts, filings, prices, estimates, news, or investor-relations pages.

Bundled examples are static educational fixtures with explicit `as_of`, `data_cutoff`, and source-date fields. Treat them as stale unless you have refreshed the source material yourself. If you need a current review, collect current transcripts, filings, KPI notes, and evidence URLs, then record their dates in a new fixture.

See [Security And Privacy](security-and-privacy.md) for the local-only no-network boundary and [Case Study Limitations](case-study-limitations.md) for static source limits.

## Why JSON?

JSON keeps the intake packet inspectable, repeatable, and easy to hand off between humans and deterministic tools.

For cold users, JSON makes the expected fields explicit: company metadata, notes, KPIs, catalysts, dates, evidence URLs, and source attribution. For analysts, JSON preserves the difference between management claims, analyst questions, and user synthesis instead of burying those distinctions in prose notes.

JSON also makes review output easier to compare over time. The same fixture can produce a Markdown report for reading, a JSON snapshot for downstream review, and a compare artifact for deterministic prior/current movement.

Start with [Input Schema](input-schema.md) and [Earnings Review Templates](templates.md) before authoring your first fixture.

## How Do I Use This With Transcripts?

Use transcripts as source material, not as live input. Read the transcript, extract only the excerpts or analyst-style notes that matter for the review, and place them in a fixture with source metadata.

Suggested workflow:

1. Record the company, ticker, `as_of`, and `data_cutoff`.
2. Add prepared-remarks excerpts or company claims as `management_claim`.
3. Add Q&A prompts as `analyst_question`; do not rewrite questions as facts.
4. Add your own interpretation as `user_synthesis`, keeping it separate from source evidence.
5. Attach transcript, filing, or investor-relations URLs in `evidence_url` or `source_attribution`.
6. Run `analyze` for the report and `review-queue` for stale, missing-evidence, or high-impact items.

See [Usage](usage.md) for commands and [Source Attribution Guide](source-attribution-guide.md) for provenance fields.

## What Are The Main Limitations?

The tool is deterministic and conservative. It uses keyword scoring and date checks; it does not forecast revenue, margins, cash flow, valuation, price targets, probability-weighted outcomes, or market reaction.

It can miss risks or opportunities when the fixture omits them, phrases them differently from the scoring vocabulary, or records weak source attribution. It can also over-highlight repeated risk language even when a human reviewer would treat the item as routine.

Scores rank review attention inside the provided fixture. They are not business-quality ratings, investment recommendations, model outputs, or proof that a real-world risk increased or decreased.

See [Scoring](scoring.md), [Risk Language Taxonomy](risk-language-taxonomy.md), and [Troubleshooting](troubleshooting.md) when score movement or review-queue priority looks surprising.

## Where Is The Advice Boundary?

Use the output as a source-backed research checklist. Do not convert risk scores, opportunity scores, stale badges, compare deltas, or review-queue placement into buy, sell, hold, short, overweight, underweight, tax, legal, accounting, or portfolio actions.

A boundary-preserving analyst note says that risk attention increased, an item needs source verification, or a management claim should be checked against filings and transcripts. It does not say that the user should enter, exit, resize, or rebalance a position.

See [Non-Advice Boundary](non-advice-boundary.md) before sharing generated artifacts or agent responses.
