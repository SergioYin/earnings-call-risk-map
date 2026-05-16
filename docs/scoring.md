# Scoring

The MVP uses deterministic keyword scoring so outputs are reproducible and reviewable.

Scoring is user synthesis. It does not convert management claims into verified facts, does not treat analyst questions as assertions, and does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

Risk and opportunity terms are stored in `src/earnings_call_risk_map/models.py`. Each matched term adds its configured weight. KPI directions add a small directional adjustment:

- `down`, `worse`, or `negative` add risk weight.
- `up`, `better`, or `positive` add opportunity weight.

Severity labels:

- `high`: score >= 7
- `medium`: score >= 4
- `low`: score > 0
- `none`: score = 0

The review queue includes items with missing evidence URLs, stale or unverified dates, or high-impact language. High-impact language is deterministic: a risk or opportunity score of `>= 7`.

The `review-queue` command emits a focused Markdown/JSON handoff with only those three concerns. It excludes ordinary current items even when they appear in the full risk or opportunity report. This queue is a prompt for human review, not a trading recommendation.

Source provenance should remain visible before scoring:

- `management_claim`: company statements, prepared remarks, or other management-supplied language.
- `analyst_question`: Q&A prompts or analyst-framed questions; these remain questions unless independently supported.
- `user_synthesis`: user-authored summaries, tags, and deterministic score labels.
