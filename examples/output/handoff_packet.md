# Portfolio/Thesis Handoff Packet

- Packet type: `portfolio_thesis_handoff`
- Tool version: `0.9.3`

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Source Boundaries

- Management claims: source-provided company statements or prepared remarks; verify against filings and transcripts.
- Analyst questions: source-provided questions or prompts; they are not treated as factual claims.
- User synthesis: user-authored notes, tags, and deterministic tool scores; they are review prompts, not advice.

## Artifact Paths

- `report` (markdown): `examples/output/demo_report.md`
  Purpose: human-readable earnings-call risk, opportunity, catalyst, and review summary
- `review_queue_jsonl` (jsonl): `examples/output/demo_review_queue_items.jsonl`
  Purpose: line-delimited triage records for stale data, missing evidence, and high-impact language
- `compare` (markdown): `examples/output/demo_compare.md`
  Purpose: prior/current deterministic score movement and reviewer interpretation

## Handoff Targets

- `portfolio_risk_review`
- `thesis_ledger`

## Cautions

- Educational research review only; not personalized investment, legal, accounting, tax, buy, sell, or hold advice.
- Artifact paths are local file handoffs and should be regenerated from current fixtures before portfolio or thesis use.
- Review queue JSONL is triage input; humans must verify missing evidence, stale data, and high-impact language against source documents.
- Compare output reflects deterministic keyword-score movement between snapshots, not real-world valuation or risk conclusions.
- Downstream portfolio and thesis systems own exposure sizing, approval workflow, retention policy, and investment decisions.
