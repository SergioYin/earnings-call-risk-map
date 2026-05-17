# Roadmap

This roadmap covers v0.7 and later ideas for `earnings-call-risk-map`. It is intentionally scoped around the project boundary: local deterministic review artifacts from static or user-authored inputs.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Roadmap items are review-workflow ideas, not commitments to produce recommendations, ratings, price targets, or portfolio actions.

## Direction

The project should stay narrow:

- Keep the CLI local-only, inspectable, and dependency-light.
- Preserve source boundaries between management claims, analyst questions, and user synthesis.
- Keep stale/static data warnings visible in every review artifact.
- Prefer deterministic JSON, Markdown, JSONL, and static HTML outputs over hidden state.
- Make handoffs easier without importing downstream portfolio, thesis, database, workflow, or market-data systems.

The best future work makes repeated earnings-review passes easier to run, compare, audit, and hand to a human reviewer.

## v0.7 Baseline

v0.7 establishes the public-facing decision support around the tool:

- comparison guidance for spreadsheets and generic notes
- reusable templates for common earnings-review fixture shapes
- static dashboard and gallery artifacts
- review queues, JSONL handoff records, and handoff packets
- playbook examples for quarterly review, catalyst check-in, and post-earnings thesis refresh
- release-readiness, maturity-evidence, and local-only audit checks

That baseline makes the repo useful as a small deterministic research utility, not just a code sample.

## v0.8 Ideas

Near-term work should improve reviewer ergonomics without changing the project model:

- Add more template variants for banks, insurers, semiconductors, retailers, and industrials.
- Add fixture validation messages that point to exact field paths and likely fixes.
- Add an optional `--strict` validation mode for teams that want missing evidence, invalid dates, or unknown source-boundary labels to fail a run.
- Add more compare explanations that separate score movement, stale-data changes, and evidence changes.
- Add a compact HTML review-queue dashboard alongside the existing full dashboard.
- Expand the fixture catalog with clearer sample-selection guidance.

## v0.9 Ideas

Medium-term work can strengthen handoff and audit surfaces:

- Emit JSON Schema examples for every bundled template.
- Add deterministic artifact manifests for each playbook run.
- Add a `doctor` command that checks paths, fixture shape, date freshness, generated output presence, and local-only assumptions.
- Add redaction and privacy checks for accidental credentials, internal notes, or personal data in fixtures before public sharing.
- Add stable IDs for review items so downstream tools can track unresolved items across quarters.
- Add optional severity calibration files that remain local and explicit.

## v1.0 Bar

A v1.0 release should mean the command surface, schema, and safety boundary are stable enough for external users to build lightweight workflows around them.

Before v1.0, the project should have:

- documented schema stability rules
- fixture migration notes for any breaking field changes
- a full command reference with examples for every output mode
- link-checked docs and release assets
- deterministic regeneration steps for all bundled examples
- tested no-network, no-credential, no-workflow assumptions
- a clear policy for what the tool will not do

## Integration Ideas

Integrations should remain file-based. This package should write artifacts that other systems can choose to read, while those systems keep ownership of their own schemas and decisions.

Good integration targets:

- Thesis ledgers that import evidence-linked risk, opportunity, and catalyst notes.
- Portfolio risk review systems that import review-queue items for human triage.
- Research notebooks that read snapshots and compare files for charting or internal analysis.
- Static sites that publish sanitized Markdown reports and HTML dashboards.
- CI or release scripts that run `audit`, `release-assets`, `maturity-evidence`, and docs link checks.
- Agent workflows that call the CLI on user-provided fixtures and preserve the non-advice boundary in summaries.

The handoff contract should stay simple: artifact paths, source boundaries, freshness labels, evidence URLs, deterministic scores, review reasons, and safety notices.

## Boundaries

The roadmap should not pull the project into jobs that belong elsewhere.

Out of scope:

- live market data, transcript fetching, or external API calls
- valuation models, price targets, ratings, expected returns, or position sizing
- personalized investment, legal, accounting, or tax advice
- automated buy, sell, hold, rebalance, overweight, or underweight decisions
- database servers, hosted dashboards, workflow runners, or required cloud services
- LLM-generated conclusions presented as verified facts
- replacing source review, spreadsheet models, or long-form research memos

Adjacent systems may do some of those things, but this package should not become the system of record for them.

## Star-Worthy Use Cases

The project is most compelling when it demonstrates useful workflows that are small, deterministic, and easy to inspect:

- Run a post-earnings review from a JSON fixture and get a Markdown report, JSON snapshot, review queue, and static dashboard.
- Compare a prior-quarter fixture to a current fixture and see which topics drew more deterministic attention.
- Generate a review queue that only contains stale data, missing evidence, and high-impact language.
- Hand a JSONL review queue and handoff packet to a thesis ledger without adding runtime dependencies.
- Build a static demo page for a public case study while preserving source-access dates and static-data warnings.
- Start from a blank sector template and produce a repeatable review artifact in a few commands.
- Use the CLI in a local audit workflow that does not need credentials, network access, or a database.
- Show reviewers exactly where management claims, analyst questions, and user synthesis differ before they update a memo or model.

For current examples, see the [Gallery](gallery.md), [Integration Notes](integrations.md), and [Research Playbooks](../examples/playbooks/README.md).
