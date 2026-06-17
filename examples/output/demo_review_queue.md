# Review Queue Export: Example Systems Inc. (EXM)

- As of: `2026-05-15`
- Static data cutoff: `2026-04-30`
- Tool version: `0.9.0`

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Source Boundaries

- Management claims: source-provided company statements or prepared remarks; verify against filings and transcripts.
- Analyst questions: source-provided questions or prompts; they are not treated as factual claims.
- User synthesis: user-authored notes, tags, and deterministic tool scores; they are review prompts, not advice.

## Source Attribution

- No source attribution supplied beyond item evidence URLs.

## Focus

- stale data
- missing evidence
- high-impact language

## Summary

- Review items: 4
- Stale data: 2
- Missing evidence: 2
- High-impact language: 1

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

- **gross margin** (note): stale or unverified data; high-impact language
  Date: `2025-11-01`; badge: `stale>90d` age=195; risk=11; opportunity=0
  Evidence: https://example.com/exm/channel-check
- **Inventory days** (kpi): stale or unverified data
  Date: `2025-12-31`; badge: `stale>90d` age=135; risk=4; opportunity=0
  Evidence: https://example.com/exm/static-kpi
- **product launch** (transcript_excerpt): missing evidence URL
  Date: `2026-04-30`; badge: `current` age=15; risk=0; opportunity=6
  Evidence: missing evidence URL
- **Next earnings report** (catalyst): missing evidence URL
  Date: `2026-08-05`; badge: `n/a` age=n/a; risk=0; opportunity=0
  Evidence: missing evidence URL
