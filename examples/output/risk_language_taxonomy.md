# Risk Language Taxonomy

This taxonomy explains how deterministic risk and opportunity language becomes report labels and review-queue priority. It is intentionally mechanical: the CLI scores configured phrases, applies fixed thresholds, and surfaces review prompts. It does not verify management claims, infer investment actions, or provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

See [Scoring](../../docs/scoring.md) for the implementation-level calibration and [Source Attribution Guide](../../docs/source-attribution-guide.md) for provenance boundaries.

## Deterministic Score Bands

Each note and KPI is checked against configured risk and opportunity phrases. Matched phrases add their fixed weights. KPI direction can add a small directional adjustment: negative directions add risk score, and positive directions add opportunity score.

The output bands are deterministic and inclusive:

| Band | Score range | Review meaning |
| --- | --- | --- |
| `none` | `score = 0` | No configured language signal was found. |
| `low` | `1 <= score <= 3` | Light language signal for the full report. |
| `medium` | `4 <= score <= 6` | Meaningful language signal for the full report. |
| `high` | `score >= 7` | High-impact language for focused review. |

Boundary behavior is fixed:

- `3` stays `low`.
- `4` is the first `medium` score.
- `6` stays `medium`.
- `7` is the first `high` score.
- Scores above `7` remain `high`; there is no separate critical tier.

## High-Impact Trigger

High-impact language is a review trigger, not a forecast or recommendation. A note enters the focused review queue for high-impact language when either:

- risk score is `>= 7`; or
- opportunity score is `>= 7`.

This trigger uses the final deterministic score after note-level stale-data adjustment. For example, a current risk note with score `6` remains `medium` and does not trigger high-impact language. A stale risk note with the same keyword score receives the stale adjustment, can move from `6` to `7`, and then triggers high-impact language.

## Stale And Missing Evidence Priority

The review queue is built around reviewer workload, not only severity. Items enter the queue when they have at least one of these issue categories:

- stale or unverified date metadata;
- missing evidence URL;
- high-impact language.

Queue order is deterministic:

1. Items with more review issue categories appear first.
2. Higher risk score breaks ties next.
3. Higher opportunity score breaks ties after risk score.
4. Topic and id are final stable tie-breakers.

This means stale and missing-evidence signals can outrank severity when they create more reviewer work. A stale-only item can rank below a current item that has both missing evidence and high-impact language. Missing evidence is prioritized because the reviewer must either add a source URL or explicitly reject the item as unsupported. Stale or unverified evidence is prioritized because old or invalid date metadata can make static source material look current.

## Human Review Boundary

Taxonomy labels are user synthesis. They should be used to decide what to verify next:

- Check stale or date-unverified items against current source materials.
- Fill or reject missing evidence URLs before using an item in a memo.
- Escalate high-impact or multi-issue items to the relevant portfolio-risk or thesis-ledger owner for their own approval workflow.

Do not translate score bands, high-impact language, or review queue rank into price targets, portfolio weights, buy, sell, or hold actions.
