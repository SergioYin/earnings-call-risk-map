# Release Notes: v0.2.0

Release date: 2026-05-17

## Scope

v0.2.0 is a promotion-oriented public release focused on demonstrability: richer source attribution, stronger static-data labeling, and a public-source static case study.

## Added

- Public-source static Apple case-study fixture at `examples/input/public_apple_static_case_study.json`.
- Generated `public_apple_static_case_study_*` demo artifacts via `demo`.
- `source_attribution` fields for fixtures, notes, KPIs, catalysts, snapshots, and review-queue exports.
- Visible Source Attribution sections in Markdown reports, review queues, and static dashboards.
- Stronger static educational case-study warning in HTML dashboards.
- Documentation at `docs/public-case-study.md`.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
```

## Safety Boundary

The release remains educational research review only. It does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. The public case study uses static public-source URLs and does not claim live data.
