# Public-Source Static Case Study

`examples/input/public_apple_static_case_study.json` is a clearly labeled static case-study fixture for Apple Inc. (`AAPL`). It is included to show how a well-known company's public investor-relations and SEC-style URLs can be attributed without claiming live data.

The fixture uses public URLs only:

- Apple Q2 FY2024 results release: `https://www.apple.com/newsroom/2024/05/apple-reports-second-quarter-results/`
- Apple FY2023 Form 10-K on SEC EDGAR: `https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm`

The fixture is dated `as_of: 2024-05-03` with `data_cutoff: 2024-05-02`. Reports render the case-study warning, static data cutoff, stale/static badges, and source-attribution records so readers can see that the artifact is not live market data.

Run it directly:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/public_apple_static_case_study.json --json-out examples/output/public_apple_static_case_study_snapshot.json --md-out examples/output/public_apple_static_case_study_report.md --html-out examples/output/public_apple_static_case_study_dashboard.html
```

This project remains for educational research review only. It does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. The static case study is a fixture-format demonstration, not a recommendation or a current-company analysis.
