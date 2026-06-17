# Review Queue Export: Apple Inc. Public-Source Static Case Study (AAPL)

- As of: `2024-05-03`
- Static data cutoff: `2024-05-02`
- Tool version: `0.9.0`

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Source Boundaries

- Management claims: source-provided company statements or prepared remarks; verify against filings and transcripts.
- Analyst questions: source-provided questions or prompts; they are not treated as factual claims.
- User synthesis: user-authored notes, tags, and deterministic tool scores; they are review prompts, not advice.

## Source Attribution

- Apple reports second quarter results; type=company_investor_relations; publisher=Apple; accessed=2026-05-17; Static educational case-study fixture assembled from public URLs; not live data.; https://www.apple.com/newsroom/2024/05/apple-reports-second-quarter-results/
- Apple FY2023 Form 10-K; type=sec_filing; publisher=U.S. SEC EDGAR; accessed=2026-05-17; Static educational case-study fixture assembled from a public SEC URL; not live data.; https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm

## Focus

- stale data
- missing evidence
- high-impact language

## Summary

- Review items: 3
- Stale data: 1
- Missing evidence: 0
- High-impact language: 3

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

- **risk factors** (sec_filing_excerpt): stale or unverified data; high-impact language
  Date: `2023-09-30`; badge: `stale>90d` age=216; risk=10; opportunity=0
  Evidence: https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm
  Source attribution: Apple FY2023 Form 10-K; type=sec_filing; publisher=U.S. SEC EDGAR; accessed=2026-05-17; Static public SEC filing reference; stale badge is expected.; https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm
- **Services revenue** (kpi): high-impact language
  Date: `2024-05-02`; badge: `current` age=1; risk=0; opportunity=7
  Evidence: https://www.apple.com/newsroom/2024/05/apple-reports-second-quarter-results/
  Source attribution: Apple Q2 FY2024 results release; type=company_investor_relations; publisher=Apple; accessed=2026-05-17; Static case-study KPI; not live data.; https://www.apple.com/newsroom/2024/05/apple-reports-second-quarter-results/
- **services revenue** (management_claim): high-impact language
  Date: `2024-05-02`; badge: `current` age=1; risk=0; opportunity=7
  Evidence: https://www.apple.com/newsroom/2024/05/apple-reports-second-quarter-results/
  Source attribution: Apple Q2 FY2024 results release; type=company_investor_relations; publisher=Apple; accessed=2026-05-17; Static public-source excerpt; verify against the original release.; https://www.apple.com/newsroom/2024/05/apple-reports-second-quarter-results/
