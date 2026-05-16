# Agent Workflow

This guide shows generic agent routing for `earnings-call-risk-map`. Use it when deciding whether an agent should analyze a fixture, compare snapshots, export a human review queue, or cite source attribution in a handoff.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Agents must preserve stale/static data warnings and route uncertain items to human review.

## Routing Map

Choose the narrowest route that answers the user's request:

- Analyze when the user provides one company fixture or asks for a risk, opportunity, KPI, catalyst, dashboard, Markdown report, or JSON snapshot from current inputs.
- Compare when the user provides two already analyzed snapshots or asks what changed between a prior and current review.
- Export review queue when the user asks what needs checking, evidence cleanup, source verification, stale-data review, or reviewer handoff.
- Cite source attribution when the answer repeats or summarizes any management claim, analyst question, KPI, catalyst, public case-study source, or static-data boundary.

If the user asks for a complete review bundle, run the routes in this order: analyze, export review queue, compare if prior/current snapshots exist, then summarize with source attribution.

## Analyze Route

Use `analyze` for one raw input fixture:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze input.json \
  --json-out snapshot.json \
  --md-out report.md
```

Add `--html-out dashboard.html` when the user needs a static dashboard.

The agent should inspect:

- `safety_notice`
- `source_boundaries`
- risk and opportunity scores
- stale/static badges
- review queue count
- evidence URLs and source attribution records

Summaries should describe scores as deterministic attention signals, not investment conclusions.

## Compare Route

Use `compare` only with analyzed JSON snapshots:

```bash
PYTHONPATH=src python -m earnings_call_risk_map compare before.json after.json \
  --json-out compare.json \
  --md-out compare.md
```

The agent should explain deltas as movement in deterministic review attention. A positive delta means the later snapshot triggered more score for that topic; a negative delta means it triggered less. Do not claim the real-world company improved or deteriorated unless the user has independently supplied verified source evidence.

## Review Queue Route

Use `review-queue` when the user needs a focused human handoff:

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue input.json \
  --json-out review_queue.json \
  --md-out review_queue.md
```

Use `review-queue-jsonl` for agent-ingestion records across bundled fixtures:

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl \
  --out examples/output/demo_review_queue_items.jsonl
```

Queue items exist because at least one review reason applies:

- stale or unverified dates
- missing evidence URL
- high-impact language

The agent may group or summarize the queue, but must keep review reasons visible and must not remove stale/static warnings.

## Source Attribution Route

Use source attribution whenever an answer mentions source-backed content. Preserve the boundary between:

- Management claims: source-provided company statements or prepared remarks.
- Analyst questions: source-provided questions or prompts; they are not assertions.
- User synthesis: user-authored notes, labels, tags, or deterministic scoring output.

When available, include the relevant source name, publisher, source type, source URL, access date, static notice, `as_of`, and `data_cutoff`. If attribution or evidence is missing, say that it is missing and keep the item in the review queue.

## Handoff Checklist

Before sharing an agent-generated artifact or summary:

- Confirm the output includes the educational research boundary.
- Confirm source boundaries are preserved.
- Confirm stale/static badges are still visible.
- Confirm missing evidence and high-impact language remain in the review queue.
- Confirm compare language describes scoring movement, not a recommendation.
- Confirm cited source attribution uses the fixture's records and does not imply live-data freshness.

For public or release-facing work, run the repository verification commands listed in `docs/reviewer-evidence.md`.
