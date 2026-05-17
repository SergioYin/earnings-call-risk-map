# Review Queue Export: Northwind Analytics Inc. (NWA)

- As of: `2026-05-16`
- Static data cutoff: `2026-05-10`
- Tool version: `0.8.0`

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Source Boundaries

- Management claims: source-provided company statements or prepared remarks; verify against filings and transcripts.
- Analyst questions: source-provided questions or prompts; they are not treated as factual claims.
- User synthesis: user-authored notes, tags, and deterministic tool scores; they are review prompts, not advice.

## Source Attribution

- Q1 2026 earnings-call template fill sample; type=user_synthesis; publisher=Fixture author; accessed=2026-05-16; Fictional deterministic sample derived from the software earnings review template; not live company data.; https://example.com/nwa/q1-2026-template-sample

## Focus

- stale data
- missing evidence
- high-impact language

## Summary

- Review items: 4
- Stale data: 1
- Missing evidence: 3
- High-impact language: 2

## Prioritization

Ordering:
- items with more review issue categories first
- higher risk score next
- higher opportunity score next
- topic and id as deterministic tie-breakers

Severity and stale badges:
- high-impact language is triggered by risk or opportunity score >= 7
- stale or unverified dates add a stale_data issue category and keep the stale badge visible
- stale note data can add +1 to risk severity before high-impact review checks
- stale-only items can rank below current items that combine missing evidence with high-impact language

Human handoff:
- verify stale data against current source documents before treating it as resolved or material
- fill or reject missing evidence URLs with source-specific reviewer notes
- send high-impact or multi-issue items to portfolio-risk or thesis-ledger owners for approval workflow

## Items

- **margin and retention watchlist** (user_synthesis): missing evidence URL; high-impact language
  Date: `2026-05-16`; badge: `current` age=0; risk=12; opportunity=0
  Evidence: missing evidence URL
  Source attribution: User-authored template fill notes; type=user_synthesis; publisher=Fixture author; accessed=2026-05-16; User synthesis is a review aid and not source evidence.
- **Gross margin** (kpi): stale or unverified data; missing evidence URL
  Date: `2026-02-01`; badge: `stale>90d` age=104; risk=4; opportunity=0
  Evidence: missing evidence URL
  Source attribution: Prior quarter operating metrics note; type=user_synthesis; publisher=Fixture author; accessed=2026-05-16; Static prior-quarter note intentionally keeps missing evidence visible.
- **enterprise demand** (analyst_question): high-impact language
  Date: `2026-05-10`; badge: `current` age=6; risk=9; opportunity=0
  Evidence: https://example.com/nwa/q1-2026-call-transcript
  Source attribution: Q1 2026 earnings call transcript; type=transcript; publisher=Northwind Analytics Investor Relations; accessed=2026-05-16; Fictional source URL for deterministic documentation workflow.; https://example.com/nwa/q1-2026-call-transcript
- **Next earnings report** (catalyst): missing evidence URL
  Date: `2026-08-08`; badge: `n/a` age=n/a; risk=0; opportunity=0
  Evidence: missing evidence URL
  Source attribution: User-authored catalyst watchlist; type=user_synthesis; publisher=Fixture author; accessed=2026-05-16; User synthesis is a review aid and not source evidence.
