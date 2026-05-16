# Tutorial: Earnings Review Walkthrough

This walkthrough follows one analyst-style review from a checked-in fixture to a Markdown report, focused review queue, and prior/current compare report.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Use the output as a review aid and verify source documents before relying on any item.

## Contents

- [Goal](#goal)
- [1. Inspect The Fixture](#1-inspect-the-fixture)
- [2. Generate The Report And Snapshot](#2-generate-the-report-and-snapshot)
- [3. Read The Report Like A Reviewer](#3-read-the-report-like-a-reviewer)
- [4. Build The Focused Review Queue](#4-build-the-focused-review-queue)
- [5. Compare Prior And Current Snapshots](#5-compare-prior-and-current-snapshots)
- [6. Complete The Analyst Pass](#6-complete-the-analyst-pass)
- [7. Regenerate The Full Demo Bundle](#7-regenerate-the-full-demo-bundle)

## Goal

Start with the demo software fixture and produce four artifacts:

- a full Markdown research report
- a machine-readable JSON snapshot
- a focused human-review queue
- a prior/current compare report

The flow is deterministic and uses only local files.

## 1. Inspect The Fixture

Open the current-period fixture:

```bash
sed -n '1,220p' examples/input/demo_company.json
```

Read it like an analyst intake packet:

- `company`, `ticker`, `as_of`, and `data_cutoff` define the review frame.
- `notes` contain management claims, analyst questions, and user synthesis.
- `kpis` provide dated observations that may become stale.
- `catalysts` identify future events or checkpoints.
- `evidence_url` fields preserve the source trail when available.

The fixture intentionally includes stale data, missing evidence, and high-impact wording so the review queue has something useful to surface.

## 2. Generate The Report And Snapshot

Run `analyze` with both Markdown and JSON outputs:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze \
  examples/input/demo_company.json \
  --md-out examples/output/demo_report.md \
  --json-out examples/output/demo_snapshot.json
```

Open the Markdown report:

```bash
sed -n '1,220p' examples/output/demo_report.md
```

What to review first:

- `Source Boundaries`: confirms whether each item is a management claim, analyst question, or user synthesis.
- `Summary`: gives counts for risks, opportunities, review queue items, and stale/static badges.
- `Risks`: shows deterministic risk topics and scores.
- `Opportunities`: shows deterministic opportunity topics and scores.
- `KPIs` and `Catalysts`: keep dated observations visible instead of folding them into a black-box score.

Interpretation rule: scores rank review attention inside this fixture. They are not forecasts, fair-value estimates, ratings, or buy/sell/hold conclusions.

## 3. Read The Report Like A Reviewer

Use the report to decide what needs source work.

For a risk item, check:

- Does the topic have evidence?
- Is the item stale, current, or date-unverified?
- Is the text a company claim, an analyst question, or user-authored synthesis?
- Does high-impact language appear in the source text or in user synthesis?

For an opportunity item, ask the same questions. A higher opportunity score is still only a prompt for verification; it does not mean the opportunity is likely or investable.

For a catalyst, check:

- Is the catalyst date after the fixture `as_of` date?
- Is the expected impact direction source-supported?
- Does the catalyst need an external filing, transcript, or press release check before review notes are updated?

## 4. Build The Focused Review Queue

Generate the human-review queue:

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue \
  examples/input/demo_company.json \
  --md-out examples/output/demo_review_queue.md \
  --json-out examples/output/demo_review_queue.json
```

Open the Markdown queue:

```bash
sed -n '1,220p' examples/output/demo_review_queue.md
```

The queue contains only items that match at least one deterministic review reason:

- stale or unverified dates
- missing evidence URL
- high-impact language

Use this as a handoff list. A reviewer can work through each item, attach better evidence, refresh dates, or decide that an item should remain flagged.

## 5. Compare Prior And Current Snapshots

First generate a prior-period snapshot:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze \
  examples/input/demo_company_prior.json \
  --json-out examples/output/demo_prior_snapshot.json \
  --md-out examples/output/demo_prior_report.md
```

Then compare prior and current snapshots:

```bash
PYTHONPATH=src python -m earnings_call_risk_map compare \
  examples/output/demo_prior_snapshot.json \
  examples/output/demo_snapshot.json \
  --md-out examples/output/demo_compare.md \
  --json-out examples/output/demo_compare.json
```

Open the compare report:

```bash
sed -n '1,220p' examples/output/demo_compare.md
```

Read positive deltas as topics that drew more deterministic attention in the later snapshot. Read negative deltas as topics that drew less attention. The compare report does not claim that the real-world business improved or deteriorated; it shows how the checked-in review inputs changed under the same scoring rules.

## 6. Complete The Analyst Pass

After reading the report, review queue, and compare output, capture decisions outside the tool:

- Which source documents need to be refreshed?
- Which stale items are still relevant?
- Which missing evidence links should be replaced with filing, transcript, or investor-relations URLs?
- Which high-impact claims should be softened, removed, or escalated for review?
- Which score movements are explained by new source text rather than by true business change?

The expected end state is a source-backed research checklist, not a recommendation.

## 7. Regenerate The Full Demo Bundle

When the walkthrough artifacts look right, regenerate the full deterministic bundle:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

This refreshes the demo reports, snapshots, dashboards, review queues, compare outputs, package audit files, and example release manifest.

Run the local verification suite:

```bash
PYTHONPATH=src python scripts/selfcheck.py
```

If selfcheck passes, the tutorial path, README links, generated examples, privacy scan, and selected documentation links are aligned with the repository.
