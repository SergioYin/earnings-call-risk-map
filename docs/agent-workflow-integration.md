# Agent Workflow Integration

This guide shows how a generic coding or research agent should work with this repository without overstepping command, verification, or advice boundaries. Use it with [Agent Workflow](agent-workflow.md), [Reviewer Evidence](reviewer-evidence.md), [Security and Privacy](security-and-privacy.md), and [Non-Advice Boundary](non-advice-boundary.md).

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Agents must keep deterministic outputs, source boundaries, stale-data warnings, and human review queues visible.

## Integration Contract

An agent may help users run local commands, inspect generated artifacts, summarize deterministic outputs, and identify missing evidence. The agent must not convert tool output into portfolio actions, live market conclusions, source verification, or professional advice.

Before acting, classify the request:

- Coding task: inspect files, edit repository code or docs, run focused tests, and report changed files plus verification status.
- Research task: run the CLI on user-provided or bundled fixtures, inspect artifacts, and summarize only what the local files contain.
- Review task: surface stale dates, missing evidence, high-impact language, source attribution, and review queue reasons.
- Boundary task: stop and ask for human action when the request requires live data, credentials, external source verification, portfolio suitability, or buy, sell, hold guidance.

## Calling Commands

Run commands from the repository root unless a command explicitly states another working directory. Prefer local, reproducible commands that do not require network access or credentials.

Use focused commands first:

```bash
PYTHONPATH=src python -m unittest tests/test_docs.py
```

Use broader checks before release-facing handoff:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python scripts/privacy_scan.py
git diff --check
```

Use CLI commands only against explicit local paths:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json \
  --json-out examples/output/demo_snapshot.json \
  --md-out examples/output/demo_report.md

PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json \
  --json-out examples/output/demo_review_queue.json \
  --md-out examples/output/demo_review_queue.md
```

When a command writes files, record the output paths in the response or handoff. When a command fails, report the exact command, exit status when available, and the smallest useful error excerpt. Do not claim a check passed unless the command completed successfully in the current workspace.

## Verifying Outputs

After running a command, verify both process status and artifact content. A zero exit code is necessary, but it is not enough for research handoff.

For generated reports, snapshots, dashboards, review queues, or compare files, inspect for:

- `Educational research review only`
- `safety_notice`
- `source_boundaries`
- `review_queue` or visible review reasons
- stale/static data badges
- missing `evidence_url` records
- source attribution fields such as `source_type`, `source_name`, `publisher`, `source_url`, `accessed_at`, `as_of`, and `data_cutoff`

For code or documentation changes, verify:

- the changed files are limited to the task scope
- relevant tests cover the requested behavior
- local Markdown links resolve when docs were changed
- `git diff --check` has no whitespace findings before release-facing handoff

When verification is partial, label it partial and state what remains unchecked. Do not hide test failures, skipped checks, stale source metadata, or missing evidence.

## Research Summaries

Summaries should be short, attributed, and source-bound. Use deterministic language:

- Say "risk attention increased" instead of "risk increased."
- Say "the fixture records a management claim" instead of "management proved."
- Say "the review queue flags missing evidence" instead of "the claim is false."
- Say "the data is stale as of the fixture dates" instead of "the company is currently stale."

Keep analyst questions as questions, management claims as source-provided statements, and user synthesis as reviewer-authored context. If a fixture lacks source attribution, say it lacks source attribution.

## Stop Boundaries

Stop and ask for human review, a user-provided source file, or an explicit scope change when the user asks the agent to:

- fetch or refresh live market data
- verify a source URL by browsing or using network access
- infer current facts from stale static fixtures
- create price targets, ratings, forecasts, expected returns, allocations, or trade instructions
- recommend buy, sell, hold, short, reduce, add, underweight, or overweight actions
- use credentials, private systems, or external accounts
- remove stale/static warnings, missing-evidence reasons, or safety notices
- treat deterministic scores as securities risk, business quality, valuation, probability, or suitability analysis

The correct response at a boundary is to name the blocked step, explain which human-owned input or review is needed, and preserve the existing local artifact state.

## Handoff Format

For a completed agent task, include:

- files changed or generated
- commands run
- verification result for each command
- remaining review items, if any
- explicit note when no live data, source refresh, or investment advice was performed

For example:

```markdown
Changed: docs/agent-workflow-integration.md, tests/test_docs.py
Verified: PYTHONPATH=src python -m unittest tests/test_docs.py
Boundary: No live data was fetched; no buy, sell, hold, valuation, or suitability conclusion was made.
Remaining: Human reviewer should verify any missing or stale source evidence before relying on the artifact.
```

This workflow keeps generic agents useful for repeatable local work while preserving the repository's local-only, source-bound, non-advisory operating model.
