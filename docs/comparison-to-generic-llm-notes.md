# Comparison To Generic LLM Notes

`earnings-call-risk-map` is a deterministic local CLI. It does not call an LLM, summarize transcripts, infer facts, draft investment conclusions, or fetch current market data. It turns structured user-provided fixtures into repeatable Markdown, JSON, JSONL, and static HTML review artifacts.

Generic LLM notes are one-off notes produced by prompting a general-purpose LLM with transcripts, filings, articles, meeting notes, or user summaries. They can be useful during exploration, but they have different reliability and audit properties from this CLI.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Outputs are source-review prompts and should be checked against filings, transcripts, and other source material.

## Short Answer

Use this CLI when the same earnings-review workflow needs to be repeated, audited, compared, exported, and handed off with stable source boundaries.

Use one-off LLM notes when the work is exploratory, the source material is unstructured, the user needs a first-pass summary, or the goal is drafting prose before a deterministic schema is known.

Do not treat either output as a substitute for source verification, financial modeling, valuation work, suitability review, or professional advice.

## Where This CLI Is Better

### Repeatable Deterministic Runs

The CLI applies the same local rules to the same fixture every time:

- `analyze` writes deterministic reports, JSON snapshots, and static dashboards.
- `review-queue` applies stable stale-data, missing-evidence, and high-impact-language checks.
- `compare` shows score movement between two analyzed snapshots without claiming real-world causality.
- Outputs can be checked into a repo, regenerated, diffed, and reviewed.

One-off LLM notes can vary by prompt wording, model version, context window, temperature, hidden system behavior, and omitted source excerpts. They are useful for fast reading support, but less suitable as the only audit trail for a repeated review process.

### Source-Boundary Discipline

This CLI keeps source categories visible:

- Management claims are source-provided company statements or prepared remarks.
- Analyst questions are questions or prompts, not factual assertions.
- User synthesis is user-authored context and deterministic scoring output.
- Evidence URLs and dates remain attached to the reviewed item.

Generic LLM notes can blur source text, user interpretation, and model-generated phrasing unless the prompt and review process enforce strict attribution.

### Review Queues And Handoff Artifacts

The CLI writes compact artifacts for recurring human review:

- Markdown reports
- JSON snapshots
- JSON Lines review items
- static HTML dashboards
- compare reports
- handoff packets

Those formats are better when another reviewer, agent, or release process needs the same fields every time. One-off LLM notes are usually better as prose inputs to a later review step, not as the canonical record of the review step.

### Local, Inspectable, No-Network Runs

The package is designed to run from local files without runtime dependencies, API calls, live market feeds, credential reads, hosted workflow runners, databases, or LLM services.

LLM notes usually depend on an external model, local model runtime, or hosted product. That may be acceptable for exploration, but it adds model availability, privacy, prompt retention, versioning, and reproducibility questions that this CLI intentionally avoids.

## Where One-Off LLM Notes Are Better

### Raw Transcript And Filing Triage

Use one-off LLM notes when the input is still raw:

- transcript excerpts
- filing sections
- press releases
- news clips
- meeting notes
- open-ended source packets

An LLM can help summarize long text, extract candidate topics, propose questions, or draft a first-pass memo. This CLI expects a known JSON fixture shape and does not parse raw documents into that fixture.

### Open-Ended Thinking

LLM notes are better when the user does not yet know the schema, topics, or review categories. They can help brainstorm risks, opportunities, counterarguments, and missing source questions before the user decides what belongs in a structured fixture.

### Narrative Drafting

Use an LLM or notes app for long-form thesis drafts, memo prose, meeting summaries, and communication polish. This CLI produces review artifacts, not polished investment memos.

## Limitations Of This CLI

This CLI is intentionally narrow:

- It does not ingest raw transcripts, PDFs, filings, audio, images, tables, or web pages.
- It does not summarize source documents.
- It does not infer missing facts, dates, KPI values, speakers, publishers, or evidence URLs.
- It does not verify whether a URL is reachable or whether a source is current.
- It does not fetch live market data, estimates, filings, news, prices, or transcripts.
- It does not produce recommendations, ratings, price targets, expected returns, valuation ranges, or portfolio actions.
- It is not a writing environment, live collaborative editor, financial model, or generic research notebook.

If the fixture is incomplete or stale, the output will preserve that incompleteness. The right next step is source review, not treating the deterministic score as a conclusion.

## Limitations Of One-Off LLM Notes

One-off LLM notes have their own limits:

- They can hallucinate facts, citations, dates, source names, URLs, speakers, or numerical values.
- They can omit stale-data context or make static examples sound current.
- They can merge management claims, analyst questions, user synthesis, and model wording into one narrative.
- They can produce different notes for the same input after prompt, model, or product changes.
- They can overstate confidence when the source packet is incomplete.
- They may create privacy, retention, credential, or network-dependency concerns.
- They usually do not create stable JSON, JSONL, dashboard, compare, and handoff artifacts without extra tooling.

LLM notes should be checked against source materials before being moved into a fixture, memo, model, or decision ledger.

## When To Use Each

| Need | Best fit | Why |
| --- | --- | --- |
| Summarize a long transcript for first-pass reading | One-off LLM notes | Better at reducing raw prose before the schema is known |
| Build a repeatable earnings-review queue | This CLI | Deterministic stale-data, missing-evidence, and high-impact checks |
| Draft narrative memo language | One-off LLM notes | Better prose surface and flexible structure |
| Preserve management claims, analyst questions, and user synthesis separately | This CLI | Explicit source-boundary fields and generated boundary language |
| Compare prior and current structured review snapshots | This CLI | Stable `compare` output over deterministic scores |
| Brainstorm possible risks before data entry | One-off LLM notes | Useful for exploratory ideation, subject to source verification |
| Generate local artifacts without API keys or network calls | This CLI | Designed for checked-out files and zero runtime dependencies |
| Fill missing facts or evidence URLs | Neither | Return to source documents instead of inventing data |

## Practical Workflow Split

A practical workflow is:

1. Use one-off LLM notes or manual notes to explore raw source material.
2. Verify candidate facts, quotes, dates, KPIs, speakers, and source links against primary materials.
3. Enter only verified review inputs into a dated JSON fixture.
4. Run `analyze`, `review-queue`, and `compare`.
5. Use the generated artifacts as review prompts for a human owner.
6. Return to sources, models, and decision ledgers for final interpretation.

The LLM can assist exploration and drafting. The CLI owns deterministic review artifact generation. The reviewer owns verification, interpretation, model updates, and decisions.

## Non-Advice Boundary

The output is a research-review aid. It does not say whether a security is attractive, expensive, cheap, risky enough to sell, safe enough to buy, or suitable for a person or portfolio.

For adjacent tradeoffs, see [Comparison To Spreadsheets And Generic Notes](comparison-to-spreadsheets.md). For safety language, see [Non-Advice Boundary](non-advice-boundary.md), [Case Study Limitations](case-study-limitations.md), and [Source Attribution Guide](source-attribution-guide.md).
