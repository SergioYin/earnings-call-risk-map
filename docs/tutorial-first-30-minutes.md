# Tutorial: First 30 Minutes

This tutorial takes a cold user from clone to template selection, analysis, review queue, and handoff using only local files.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Use outputs as review aids and verify source documents before relying on any item.

## Contents

- [0-5 Minutes: Clone And Verify](#0-5-minutes-clone-and-verify)
- [5-10 Minutes: Select A Template](#5-10-minutes-select-a-template)
- [10-18 Minutes: Fill The First Fixture](#10-18-minutes-fill-the-first-fixture)
- [18-23 Minutes: Run Analysis](#18-23-minutes-run-analysis)
- [23-27 Minutes: Build The Review Queue](#23-27-minutes-build-the-review-queue)
- [27-30 Minutes: Prepare The Handoff](#27-30-minutes-prepare-the-handoff)
- [Next References](#next-references)

## 0-5 Minutes: Clone And Verify

Clone the repository and enter the checkout:

```bash
git clone <repo-url> earnings-call-risk-map
cd earnings-call-risk-map
```

Confirm Python can import the package from source:

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
```

Generate the bundled demo artifacts once so the examples are present:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

Open the static dashboard at `examples/output/demo_dashboard.html`, or inspect the Markdown report:

```bash
sed -n '1,180p' examples/output/demo_report.md
```

The first checkpoint is simple: the CLI runs locally, writes deterministic files, and does not require credentials, live data, workflow runners, or network access.

## 5-10 Minutes: Select A Template

List the available blank templates:

```bash
PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format markdown
```

Choose the closest starting point:

- `examples/templates/software_earnings_review.json` for software, cloud, subscription, platform, or margin review.
- `examples/templates/energy_infrastructure_earnings_review.json` for capital projects, utilization, capacity, permits, or commodity-exposed infrastructure.
- `examples/templates/consumer_hardware_earnings_review.json` for devices, channel inventory, launches, supply chain, or unit economics.

For this first pass, copy the software template into a scratch fixture path:

```bash
cp examples/templates/software_earnings_review.json examples/input/first_30_minutes_workflow.json
```

If another template better matches the company, use that file instead. The key decision is the review shape, not the score result.

## 10-18 Minutes: Fill The First Fixture

Edit `examples/input/first_30_minutes_workflow.json` and replace placeholders with source-backed notes.

Start with the required frame:

- `company`
- `ticker`
- `as_of`
- `data_cutoff`

Then add a small, auditable set of rows:

- one `management_claim` note from prepared remarks or a shareholder letter
- one `analyst_question` note from Q&A or an analyst prompt
- one `user_synthesis` note that states your own review concern
- one dated KPI observation
- one catalyst with a future or recent date

Keep `evidence_url` empty only when the source is truly missing. Empty evidence is allowed because the review queue is designed to surface missing source links instead of hiding them.

Validate the fixture before moving on:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/first_30_minutes_workflow.json
```

If validation fails, use [Troubleshooting](troubleshooting.md) and [Input Schema](input-schema.md) to fix the field path reported by the CLI.

Before reading a full report, run a short fixture summary checkpoint:

```bash
PYTHONPATH=src python -m earnings_call_risk_map fixture-summary examples/input/first_30_minutes_workflow.json
```

Use [Fixture Summary](fixture-summary.md) to confirm source types, stale badges, and fixture counts match the review shape you intended.

## 18-23 Minutes: Run Analysis

Write the first report, snapshot, and dashboard:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze \
  examples/input/first_30_minutes_workflow.json \
  --md-out examples/output/first_30_minutes_report.md \
  --json-out examples/output/first_30_minutes_snapshot.json \
  --html-out examples/output/first_30_minutes_dashboard.html
```

Read the report in this order:

- `Source Boundaries` to confirm management claims, analyst questions, and user synthesis are separated.
- `Summary` to see risk, opportunity, review queue, and stale/static counts.
- `Risks` and `Opportunities` to find topics that need attention.
- `KPIs` and `Catalysts` to check dates, stale badges, and evidence URLs.

Scores are deterministic review triage. They are not forecasts, price targets, ratings, or buy/sell/hold conclusions.

## 23-27 Minutes: Build The Review Queue

Generate the focused human-review queue:

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue \
  examples/input/first_30_minutes_workflow.json \
  --md-out examples/output/first_30_minutes_review_queue.md \
  --json-out examples/output/first_30_minutes_review_queue.json
```

Open the queue:

```bash
sed -n '1,220p' examples/output/first_30_minutes_review_queue.md
```

Work it as a checklist:

- stale or date-unverified items need source freshness review
- missing evidence items need a filing, transcript, investor-relations page, or explicit rejection note
- high-impact language needs human review before it is copied into a memo or thesis ledger

The queue is the handoff surface for a reviewer. The full report gives context; the queue shows what needs action first.

## 27-30 Minutes: Prepare The Handoff

Create a small packet that points downstream reviewers to the report and review queue:

```bash
PYTHONPATH=src python -m earnings_call_risk_map handoff-packet \
  --report-path examples/output/first_30_minutes_report.md \
  --review-queue-jsonl-path examples/output/demo_review_queue_items.jsonl \
  --compare-path examples/output/demo_compare.md \
  --md-out examples/output/first_30_minutes_handoff_packet.md \
  --json-out examples/output/first_30_minutes_handoff_packet.json
```

For a real handoff, replace the demo JSONL and compare paths after you have generated workflow-specific files. The packet should tell a portfolio-risk or thesis-ledger owner where to find:

- the full analysis report
- the focused review queue
- any prior/current compare report
- stale data and source verification cautions
- the downstream owner of final research decisions

At the 30-minute mark, the expected result is not an investment conclusion. It is a local, source-bounded review package with visible gaps and a clear human queue.

## Next References

- [Earnings Review Templates](templates.md) explains the blank templates and filled-template workflow.
- [Fixture Summary](fixture-summary.md) explains the short source-coverage checkpoint for cold-user onboarding.
- [Analyst Tutorial](tutorial-earnings-review.md) walks through the bundled demo fixture, review queue, and prior/current compare.
- [Usage](usage.md) documents each CLI command.
- [Integrations](integrations.md) shows portfolio-risk and thesis-ledger handoff mappings.
- [Non-Advice Boundary](non-advice-boundary.md) states the financial-safety boundary.
