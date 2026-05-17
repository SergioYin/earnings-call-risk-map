# Comparison To Spreadsheets And Generic Notes

`earnings-call-risk-map` is not a spreadsheet replacement and it is not a general note-taking system. It is a narrow local CLI for turning earnings-call notes, KPI observations, catalysts, dates, and evidence links into deterministic review artifacts.

Use this comparison when deciding whether to keep a workflow in a spreadsheet, keep it in generic notes, or move the repeatable review step into this tool.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Outputs are source-review prompts and should be checked against filings, transcripts, and other source material.

## Short Answer

This tool is better when the same earnings-review workflow needs to be repeated, reviewed, exported, and audited without hidden formulas or live services.

Spreadsheets are better when the primary job is financial modeling, numerical scenario analysis, portfolio math, ad hoc tabulation, or collaborative editing.

Generic notes are better when the primary job is open-ended thinking, meeting notes, long-form thesis writing, or collecting unstructured material before it is ready for deterministic scoring.

## Where This Tool Is Better

### Repeatable Earnings Review

The CLI is built for repeatable review runs:

- The same fixture shape feeds `analyze`, `review-queue`, `compare`, dashboard output, and handoff packets.
- Outputs use deterministic rules instead of cell formulas that can drift silently across copied sheets.
- The review queue consistently surfaces stale data, missing evidence, and high-impact language.
- `compare` separates before/after score movement from real-world conclusions.

This is useful when a reviewer wants the same triage process applied across multiple companies, quarters, or demo fixtures.

### Source-Boundary Discipline

Spreadsheets and notes often blur source material, user interpretation, and conclusions in adjacent cells or paragraphs. This tool keeps those boundaries explicit:

- Management claims are source-provided statements or prepared remarks.
- Analyst questions are prompts or questions, not factual claims.
- User synthesis is user-authored notes plus deterministic scoring output.
- Evidence URLs and static-data dates remain attached to the reviewed item.

That structure is valuable when the artifact is handed to another reviewer who needs to know what came from source material and what came from user synthesis.

### Stale-Data Visibility

In a spreadsheet, old values can look current unless every sheet has carefully maintained date logic. In generic notes, date context can disappear entirely.

This tool labels items as `current`, `stale>90d`, or `date-unverified` relative to the fixture `as_of` date. It does not hide stale items. It keeps them visible so reviewers can decide whether to refresh, discard, or preserve the source.

### Focused Review Queues

The `review-queue` and `review-queue-jsonl` commands produce compact artifacts for items that need human attention:

- stale or unverified data
- missing evidence URL
- high-impact deterministic language

That is harder to maintain in generic notes and easy to break in spreadsheets when filters, helper columns, or formulas are edited manually.

### Local, Inspectable, No-Network Runs

The package is designed to run from local files without runtime dependencies, API calls, live market feeds, credential reads, workflow runners, or databases. This makes it a better fit when the review process needs to be reproducible from a checkout.

Spreadsheets can be local too, but cloud spreadsheets, linked data functions, add-ons, and shared-drive formulas can introduce external state that is hard to audit. Generic notes can also sync through external services and may not preserve machine-readable structure.

### Artifact Generation

The tool writes:

- Markdown reports
- JSON snapshots
- JSON Lines review items
- self-contained static HTML dashboards
- compare reports
- handoff packets
- release and maturity evidence

Spreadsheets can export CSV or PDF, and notes can export Markdown or HTML, but those exports usually do not preserve a consistent review schema across reports, queues, comparisons, and handoffs.

## Where Spreadsheets Are Better

### Financial Models

Use a spreadsheet for:

- financial models
- revenue build-ups
- margin bridges
- DCF models
- balance-sheet and cash-flow models
- sensitivity tables
- scenario matrices
- portfolio weighting and exposure math

This tool does not calculate intrinsic value, price targets, valuation ranges, risk-adjusted returns, or position sizes.

### Flexible Ad Hoc Analysis

Spreadsheets are better when the shape of the work is still changing:

- You need to add columns freely during analysis.
- You are exploring many possible dimensions before standardizing the workflow.
- You want quick pivot tables, charts, conditional formatting, or manual filters.
- You need to reconcile large tabular datasets.

The CLI is intentionally opinionated. It expects a known JSON fixture shape and produces known output artifacts.

### Collaborative Editing

A spreadsheet is usually better when several people need to edit the same table directly, leave comments cell by cell, or make live updates during a meeting.

This tool is better for deterministic artifact generation and review handoff. It is not a live collaborative editor.

### Numeric Audit Trails Inside A Model

If the central question is "which assumption changed this model output?", spreadsheets can show formula-level dependencies and scenario tabs directly in the model file.

This tool can show deterministic score movement, but it does not replace model-level formula auditability.

## Where Generic Notes Are Better

### Open-Ended Research

Use generic notes for:

- first-pass reading notes
- meeting notes
- open questions
- long-form thesis memos
- article clippings
- qualitative observations that do not yet fit a schema

This tool works best after the user has enough structure to express notes, KPIs, catalysts, evidence URLs, and dates.

### Narrative Writing

Generic notes are better for drafting a thesis, investment memo, or research journal entry. This tool can generate review artifacts that feed those documents, but it is not a writing environment.

### Personal Knowledge Management

Use a notes app when the goal is broad knowledge capture across companies, industries, documents, and meetings. Use this tool when the goal is a deterministic earnings-review pass over structured inputs.

## Where This Tool Is Worse

This tool is worse than spreadsheets or generic notes when:

- the input data is messy and not ready for a schema
- the team needs live multi-user editing
- the workflow depends on spreadsheet formulas, pivots, or charts
- the analysis requires live market data or external APIs
- the user wants an LLM to summarize transcripts or draft conclusions
- the user wants a recommendation, price target, rating, or portfolio action
- the primary output should be a polished memo rather than a review queue

The tool intentionally avoids those jobs.

## Practical Workflow Split

A pragmatic workflow is:

1. Collect raw notes in a notes app.
2. Model financial assumptions in a spreadsheet.
3. Convert the repeatable review items into a JSON fixture.
4. Run `analyze`, `review-queue`, and `compare`.
5. Use the generated Markdown, JSON, JSONL, and dashboard artifacts as review inputs.
6. Return to the source documents, notes, or spreadsheet for final judgment and model updates.

The CLI owns deterministic triage. The reviewer owns interpretation, source verification, model changes, and decisions.

## Decision Table

| Need | Best fit | Why |
| --- | --- | --- |
| Repeatable earnings-call risk triage | This tool | Deterministic scoring, stale badges, source boundaries, review queues |
| Financial model with formulas | Spreadsheet | Native formulas, scenarios, sensitivity tables, model audit trails |
| Open-ended research capture | Generic notes | Flexible writing before the schema is known |
| Evidence-linked review handoff | This tool | Markdown, JSON, JSONL, dashboard, and handoff artifacts share the same source boundary |
| Live collaborative table editing | Spreadsheet | Direct multi-user editing and cell comments |
| Long-form thesis memo | Generic notes | Better writing surface and narrative control |
| Local no-network artifact generation | This tool | Designed for checked-out files, no runtime dependencies, and no external service calls |
| Live data pulls or market feeds | Spreadsheet or another data tool | This package does not fetch live data |

## Non-Advice Boundary

The output is a research-review aid. It does not say whether a security is attractive, expensive, cheap, risky enough to sell, safe enough to buy, or suitable for a person or portfolio.

For LLM-specific tradeoffs, see [Comparison To Generic LLM Notes](comparison-to-generic-llm-notes.md). For the full safety language, see [Non-Advice Boundary](non-advice-boundary.md). For static public-source caveats, see [Case Study Limitations](case-study-limitations.md). For command usage, see [Usage](usage.md).
