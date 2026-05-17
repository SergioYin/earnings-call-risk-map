# Filled-From-Template Workflow

This deterministic sample shows how a user moves from a blank software earnings review template to a filled fixture and analyzed report.

> Educational research review only. This workflow does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. It is a source-bound authoring example; verify source materials before relying on any conclusion.

## 1. Start With A Blank Template

Use the software template as the starting point:

```bash
cp examples/templates/software_earnings_review.json scratch/northwind-analytics-q1.json
```

The blank template already has the required top-level fields, three note rows, three KPI rows, and two catalyst rows. Its empty text, value, observation, description, and evidence fields make missing source work visible.

## 2. Fill The Template

Replace placeholder identity and date fields:

| Field | Blank value | Filled sample value |
| --- | --- | --- |
| `company` | `Software Earnings Review Template` | `Northwind Analytics Inc.` |
| `ticker` | `SOFTWARE-TEMPLATE` | `NWA` |
| `as_of` | `2026-01-01` | `2026-05-16` |
| `data_cutoff` | `2026-01-01` | `2026-05-10` |

Then fill the domain rows while preserving provenance:

| Template row | Filled provenance | Example topic |
| --- | --- | --- |
| `software-note-1` | `management_claim` | revenue durability |
| `software-note-2` | `analyst_question` | enterprise demand |
| `software-note-3` | `user_synthesis` | margin and retention watchlist |
| `Revenue growth` | source-backed KPI | growth described as steady |
| `Net retention` | source-backed KPI | retention improved |
| `Gross margin` | stale/missing-evidence review item | older migration support costs |
| `Next earnings report` | user-authored catalyst watchlist | demand and churn-risk review |

The checked-in filled fixture is [sample_filled_template_workflow.json](../examples/input/sample_filled_template_workflow.json).

## 3. Analyze The Filled Fixture

Run the same deterministic analyzer used for all examples:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze \
  examples/input/sample_filled_template_workflow.json \
  --md-out examples/output/sample_filled_template_report.md \
  --json-out examples/output/sample_filled_template_snapshot.json
```

The Markdown report contains the safety notice, source boundaries, score summary, stale badges, review queue, source attribution, and catalyst timeline. The JSON snapshot preserves the same machine-readable fields for downstream review.

## 4. Review The Report

Read the report as deterministic review attention, not advice:

- Risk and opportunity scores are keyword-based review signals.
- Missing evidence remains visible instead of being silently discarded.
- Stale/static data badges stay in the report.
- Management claims, analyst questions, and user synthesis remain separated.
- Scores are not forecasts, price targets, expected returns, or instructions to buy, sell, hold, short, enter, exit, or rebalance.

For a focused source-check list, run:

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue \
  examples/input/sample_filled_template_workflow.json \
  --md-out examples/output/sample_filled_template_review_queue.md \
  --json-out examples/output/sample_filled_template_review_queue.json
```

## 5. Refresh With Real Sources

When replacing this fictional sample with user-collected notes:

- Use current transcript, filing, shareholder-letter, event, or internal note sources.
- Record exact `as_of`, `data_cutoff`, and `accessed_at` dates.
- Keep `management_claim`, `analyst_question`, and `user_synthesis` rows distinct.
- Keep empty `evidence_url` fields when evidence is missing so the review queue flags them.
- Preserve the non-advice boundary in any copied report or handoff.

See [Data Entry Checklist](data-entry-checklist.md), [Earnings Review Templates](templates.md), [Author A Fixture From Scratch](examples-from-scratch.md), and [Non-Advice Boundary](non-advice-boundary.md) for the surrounding authoring rules.
