# Public Promotion Pack

- Package: `earnings-call-risk-map`
- Version: `0.8.0`
- Purpose: Turn earnings-call notes into deterministic risk maps, review queues, snapshots, handoff packets, and static dashboards from local JSON fixtures.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Quickstart

1. Generate the bundled demo artifacts:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
```

2. Analyze one fixture:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json
```

3. Open the static demo index:

```bash
open docs/demo-index.html
```

## Demos

| Demo | Artifact | Why it matters |
| --- | --- | --- |
| Static public-source dashboard | `examples/output/public_apple_static_case_study_dashboard.html` | Shows attribution, static educational labels, summary tiles, and review panels. |
| Review queue | `examples/output/demo_review_queue.md` | Shows stale-data, missing-evidence, and high-impact-language prompts. |
| Compare narrative | `examples/output/demo_compare.md` | Shows deterministic before/after score movement without investment conclusions. |
| Public case-study report | `examples/output/public_apple_static_case_study_report.md` | Shows public-source attribution and static case-study warnings in Markdown. |
| Handoff packet | `examples/output/handoff_packet.md` | Shows generated artifact paths and cautions for adjacent review workflows. |
| Case study map | `examples/output/case_study_map.md` | Shows bundled fixtures, reviewer questions, and generated artifacts. |

## Proof Commands

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m unittest discover -s tests
python scripts/privacy_scan.py
```

## Boundaries

- Educational research review only; not personalized investment, legal, accounting, tax, buy, sell, or hold advice.
- No live market data, current company coverage, price targets, expected returns, portfolio actions, or valuation support.
- Scores are deterministic review prompts, not facts about company quality, security attractiveness, or future performance.
- Bundled fixtures are static examples; public-source fixtures are not live analysis.
- The tool preserves management claims, analyst questions, and user synthesis as source-bound review inputs.
- No hosted service, database, API, workflow automation, credentials, or network-backed product is implied.

## Source Evidence

- `README.md`
- `docs/promotion-page-outline.md`
- `docs/non-advice-boundary.md`
- `docs/case-study-limitations.md`
- `docs/source-attribution-guide.md`
- `docs/reviewer-evidence.md`
- `examples/output/case_study_map.md`
