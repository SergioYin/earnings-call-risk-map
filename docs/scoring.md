# Scoring

The MVP uses deterministic keyword scoring so outputs are reproducible and reviewable.

Scoring is user synthesis. It does not convert management claims into verified facts, does not treat analyst questions as assertions, and does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

For the reviewer-facing taxonomy behind these labels, see [Risk Language Taxonomy](risk-language-taxonomy.md).

Risk and opportunity terms are stored in `src/earnings_call_risk_map/models.py`. Each matched term adds its configured weight. KPI directions add a small directional adjustment:

- `down`, `worse`, or `negative` add risk weight.
- `up`, `better`, or `positive` add opportunity weight.

Severity calibration:

| Label | Inclusive score range | Review meaning |
| --- | --- | --- |
| `high` | `score >= 7` | High-impact language; include in focused review queue. |
| `medium` | `4 <= score <= 6` | Meaningful deterministic signal; include in full risk/opportunity report. |
| `low` | `1 <= score <= 3` | Light deterministic signal; include in full risk/opportunity report. |
| `none` | `score = 0` | No configured keyword or directional score was found. |

Threshold edge cases:

- `0` is `none`; it is not shown as a scored risk or opportunity.
- `1`, `2`, and `3` are `low`; a score of `3` does not round up to `medium`.
- `4`, `5`, and `6` are `medium`; a score of `6` does not round up to `high`.
- `7` is the first `high` score and is also the first score that triggers `high-impact language`.
- Scores above `7` remain `high`; there is no separate critical tier.
- Stale note data adds `+1` to the risk score after keyword scoring, so a stale risk note can move from `6` to `7` and become `high`.

Examples:

| Example score | Label | Edge behavior |
| --- | --- | --- |
| `0` | `none` | No report item from severity alone. |
| `3` | `low` | Highest low score. |
| `4` | `medium` | First medium score. |
| `6` | `medium` | Highest medium score. |
| `7` | `high` | First high score and review-queue high-impact trigger. |

The review queue includes items with missing evidence URLs, stale or unverified dates, or high-impact language. High-impact language is deterministic: a risk or opportunity score of `>= 7`.

Review queue prioritization:

1. Items with more review issue categories first.
2. Higher risk score next.
3. Higher opportunity score next.
4. Topic and id as deterministic tie-breakers.

This means severity and stale badges are related but not identical. Stale or unverified dates create a `stale_data` issue category and keep the badge visible for reviewers. Stale note data can also add `+1` to risk severity before the `>= 7` high-impact check. A stale-only item can still rank below a current item that combines missing evidence with high-impact language because the queue prioritizes multi-issue reviewer workload first.

The `review-queue` command emits a focused Markdown/JSON handoff with only those three concerns. It excludes ordinary current items even when they appear in the full risk or opportunity report. This queue is a prompt for human review, not a trading recommendation.

Source provenance should remain visible before scoring:

- `management_claim`: company statements, prepared remarks, or other management-supplied language.
- `analyst_question`: Q&A prompts or analyst-framed questions; these remain questions unless independently supported.
- `user_synthesis`: user-authored summaries, tags, and deterministic score labels.
