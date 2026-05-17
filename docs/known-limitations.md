# Known Limitations

This project turns static JSON fixtures into deterministic earnings-call research review artifacts. It is intentionally local, source-bound, and conservative.

## Static Data Only

The CLI reads checked-in or user-provided JSON files. It does not refresh source packets, update stale fixtures, or infer that a public URL still represents current information.

Every review should keep these dates visible:

- `as_of`: the review date used for stale/static comparisons.
- `data_cutoff`: the latest source date the fixture author intended to represent.
- item-level `date`: the date attached to each note, KPI, or catalyst.
- `accessed_at`: the date a source URL was recorded in `source_attribution`, when available.

Bundled examples are frozen demonstrations, not current company analysis. Replace them with dated user-collected notes before treating a review as current.

## No Live Fetching

Package commands are designed to run from local files only. The package does not call APIs, open sockets, fetch live market data, pull transcripts, read estimates, collect news, query filings, require credentials, use a database, or depend on workflow runners.

Evidence URLs are attribution metadata for a static fixture. They are not fetched or validated during normal analysis.

## Scoring Limits

Scores are deterministic attention signals over the supplied fixture text and metadata. They help rank review work; they do not measure business quality, probability, valuation, expected return, price movement, or securities risk.

Score movement in `compare` output means deterministic risk or opportunity attention changed between two analyzed snapshots. It is a prompt for source review, not a real-world conclusion.

## Source Trust Limits

The tool preserves source boundaries but does not verify source truth.

- Management claims remain company-provided statements until a reviewer verifies them against filings, transcripts, releases, or other source documents.
- Analyst questions remain questions or prompts, not factual assertions.
- User synthesis remains reviewer-authored context and deterministic tool output, not source evidence.
- Missing evidence, stale dates, and `date-unverified` badges are human review triggers.

The project can help show where source attribution is missing or stale. It cannot decide whether a source is complete, current, unbiased, or sufficient for a real decision.

## No Advice

Outputs are educational research review only. They are not personalized investment, legal, accounting, tax, buy, sell, hold, short, overweight, underweight, rebalance, enter, or exit advice.

Do not translate reports, review queues, dashboards, scores, or compare deltas into price targets, ratings, forecasts, allocation changes, trade instructions, or professional advice.

## No Portfolio Suitability

The project has no knowledge of a user's objectives, time horizon, liquidity needs, constraints, holdings, tax status, risk tolerance, regulatory obligations, or legal/accounting context.

It cannot assess whether any security, issuer, sector, thesis, catalyst, exposure, or risk is suitable for a person, account, fund, strategy, mandate, or portfolio.

## Related Docs

- [Case Study Limitations](case-study-limitations.md)
- [Non-Advice Boundary](non-advice-boundary.md)
- [Scoring](scoring.md)
- [Source Attribution Guide](source-attribution-guide.md)
- [Security and Privacy](security-and-privacy.md)
