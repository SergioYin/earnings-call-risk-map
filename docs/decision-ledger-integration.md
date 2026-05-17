# Decision Ledger Integration

This guide shows how to paste `earnings-call-risk-map` outputs into an investment thesis ledger while keeping the handoff educational, source-bound, and non-advisory.

The ledger should be treated as a decision record and review workflow, not as an automated investment-decision engine. This project supplies deterministic review artifacts. The ledger owner remains responsible for source verification, approval, suitability checks, portfolio context, and any buy, sell, hold, sizing, tax, legal, or accounting decision.

See [Non-Advice Boundary](non-advice-boundary.md), [Integration Notes](integrations.md), and [Case Study Limitations](case-study-limitations.md) before publishing or sharing ledger entries.

## Recommended Source Artifacts

Generate a report, review queue, compare file, and handoff packet from local files:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json \
  --md-out examples/output/demo_report.md \
  --json-out examples/output/demo_snapshot.json

PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json \
  --md-out examples/output/demo_review_queue.md \
  --json-out examples/output/demo_review_queue.json

PYTHONPATH=src python -m earnings_call_risk_map compare \
  examples/output/demo_prior_snapshot.json \
  examples/output/demo_snapshot.json \
  --md-out examples/output/demo_compare.md \
  --json-out examples/output/demo_compare.json

PYTHONPATH=src python -m earnings_call_risk_map handoff-packet \
  --md-out examples/output/handoff_packet.md \
  --json-out examples/output/handoff_packet.json
```

Paste from these artifacts in this order:

1. `examples/output/handoff_packet.md` for the source paths, cautions, and review boundaries.
2. `examples/output/demo_review_queue.md` for items requiring human review.
3. `examples/output/demo_compare.md` for deterministic attention movement between snapshots.
4. `examples/output/demo_report.md` for the broader risk, opportunity, catalyst, and source-boundary context.

## Ledger Entry Template

Use one ledger row per reviewable thesis point. Copy the language as a review prompt, not as a conclusion.

| Ledger field | Paste from output | Boundary to preserve |
| --- | --- | --- |
| `subject` | `company`, `ticker`, `as_of`, `data_cutoff` | Keep exact dates visible. |
| `source_artifact` | report, review queue, compare, or handoff packet path | Keep local artifact provenance. |
| `thesis_point` | risk, opportunity, catalyst, or review-queue topic | Treat as a review prompt. |
| `evidence` | evidence URL and source attribution | Verify before relying on it. |
| `freshness` | `current`, `stale>90d`, or `date-unverified` badge | Do not hide stale/static warnings. |
| `source_boundary` | management claim, analyst question, or user synthesis | Do not convert source type into verified fact. |
| `deterministic_signal` | risk score, opportunity score, level, review reasons, or compare delta | Do not convert scores into price targets, expected returns, or actions. |
| `review_status` | open, verified, rejected, refreshed, or archived | Ledger owner controls approval. |
| `decision_note` | reviewer-authored conclusion after source checks | Keep investment decisions outside this tool. |

## Paste Pattern

Paste compact, attributed notes. The example below is intentionally framed as a review record:

```markdown
Subject: EXM / Example Software Inc.
As of: 2026-02-15
Source artifact: examples/output/demo_review_queue.md
Thesis point: gross margin
Source boundary: user_synthesis
Freshness: stale>90d
Deterministic signal: high-impact language; data is stale
Evidence: https://example.com/exm/channel-check
Review status: open

Non-advice boundary: Educational research review only. This is not personalized
investment, legal, accounting, tax, buy, sell, or hold advice. Verify source
materials before relying on this ledger note.

Reviewer task: Refresh the source, confirm whether the stale channel-check note
is still relevant, and record the verification result before any internal thesis
or portfolio workflow uses this item.
```

When pasting compare output, use movement language:

```markdown
Deterministic signal: risk attention increased for gross margin versus the prior
snapshot. This is a source-review prompt only and does not establish that the
real-world risk changed.
```

## Non-Advice Guardrails

Keep these sentences or equivalent meaning in ledger imports:

- Educational research review only.
- This is not personalized investment, legal, accounting, tax, buy, sell, or hold advice.
- Verify source materials before relying on any conclusion.
- Deterministic scores and compare deltas are review prompts, not portfolio actions.
- Stale/static data warnings must remain visible until refreshed or rejected.

Avoid these ledger transformations:

- Changing "risk attention increased" into "sell", "short", "reduce", or "underweight".
- Changing an opportunity score into a price target, expected return, or position size.
- Treating management claims as verified facts without independent review.
- Treating analyst questions as assertions.
- Dropping `as_of`, `data_cutoff`, `accessed_at`, stale badges, or source attribution.

## Review Workflow

1. Create ledger entries only from local artifacts whose paths are recorded.
2. Preserve source boundaries and the safety notice verbatim where practical.
3. Mark every imported item `open` until a human verifies or rejects the source.
4. Add reviewer notes in the ledger rather than editing generated artifacts.
5. Link accepted entries back to the exact artifact path and source URL.
6. Keep portfolio sizing, suitability, and execution decisions in a separate governed workflow.

This separation keeps the CLI output useful for repeatable research review without turning it into personalized advice or an automated investment recommendation.
