# Fixture Catalog

Bundled fixtures are deterministic examples for local demos and tests. None of the bundled fixtures fetch live market, filing, or transcript data at runtime.

Regenerate this catalog with `earnings-call-risk-map fixture-catalog`.

| Fixture | Ticker | Data cutoff | Static/live status | Recommended command |
| --- | --- | --- | --- | --- |
| `examples/input/demo_company.json` | `EXM` | `2026-04-30` | static demo fixture | `earnings-call-risk-map analyze examples/input/demo_company.json` |
| `examples/input/demo_energy_infrastructure.json` | `NGLP` | `2026-04-25` | static demo fixture | `earnings-call-risk-map analyze examples/input/demo_energy_infrastructure.json` |
| `examples/input/consumer_hardware.json` | `LOGI` | `2024-04-29` | static public-source consumer hardware fixture | `earnings-call-risk-map analyze examples/input/consumer_hardware.json` |
| `examples/input/semiconductor_equipment.json` | `ASML` | `2025-01-29` | static public-source semiconductor equipment fixture | `earnings-call-risk-map analyze examples/input/semiconductor_equipment.json` |
| `examples/input/public_apple_static_case_study.json` | `AAPL` | `2024-05-02` | static public-source case study | `earnings-call-risk-map analyze examples/input/public_apple_static_case_study.json` |
| `examples/input/demo_company_prior.json` | `EXM` | `2026-01-31` | static compare baseline | `earnings-call-risk-map analyze examples/input/demo_company_prior.json --json-out examples/output/demo_prior_snapshot.json --md-out examples/output/demo_prior_report.md` |

## Recommended Commands

### demo_company

- Company: Example Systems Inc.
- Ticker: `EXM`
- As of: `2026-05-15`
- Data cutoff: `2026-04-30`
- Static/live status: static demo fixture

```bash
earnings-call-risk-map analyze examples/input/demo_company.json
earnings-call-risk-map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json
earnings-call-risk-map analyze examples/input/demo_company.json --html-out examples/output/demo_dashboard.html
```

### demo_energy_infrastructure

- Company: Northstar Grid & LNG Partners
- Ticker: `NGLP`
- As of: `2026-05-15`
- Data cutoff: `2026-04-25`
- Static/live status: static demo fixture

```bash
earnings-call-risk-map analyze examples/input/demo_energy_infrastructure.json
earnings-call-risk-map review-queue examples/input/demo_energy_infrastructure.json --md-out examples/output/energy_infrastructure_review_queue.md --json-out examples/output/energy_infrastructure_review_queue.json
earnings-call-risk-map analyze examples/input/demo_energy_infrastructure.json --html-out examples/output/energy_infrastructure_dashboard.html
```

### consumer_hardware

- Company: Logitech International S.A. Public-Source Consumer Hardware Fixture
- Ticker: `LOGI`
- As of: `2024-05-01`
- Data cutoff: `2024-04-29`
- Static/live status: static public-source consumer hardware fixture

```bash
earnings-call-risk-map analyze examples/input/consumer_hardware.json
earnings-call-risk-map review-queue examples/input/consumer_hardware.json --md-out examples/output/consumer_hardware_review_queue.md --json-out examples/output/consumer_hardware_review_queue.json
earnings-call-risk-map analyze examples/input/consumer_hardware.json --html-out examples/output/consumer_hardware_dashboard.html
```

### semiconductor_equipment

- Company: ASML Holding N.V. Public-Source Semiconductor Equipment Fixture
- Ticker: `ASML`
- As of: `2025-01-30`
- Data cutoff: `2025-01-29`
- Static/live status: static public-source semiconductor equipment fixture

```bash
earnings-call-risk-map analyze examples/input/semiconductor_equipment.json
earnings-call-risk-map review-queue examples/input/semiconductor_equipment.json --md-out examples/output/semiconductor_equipment_review_queue.md --json-out examples/output/semiconductor_equipment_review_queue.json
earnings-call-risk-map analyze examples/input/semiconductor_equipment.json --html-out examples/output/semiconductor_equipment_dashboard.html
```

### public_apple_static_case_study

- Company: Apple Inc. Public-Source Static Case Study
- Ticker: `AAPL`
- As of: `2024-05-03`
- Data cutoff: `2024-05-02`
- Static/live status: static public-source case study

```bash
earnings-call-risk-map analyze examples/input/public_apple_static_case_study.json
earnings-call-risk-map review-queue examples/input/public_apple_static_case_study.json --md-out examples/output/public_apple_static_case_study_review_queue.md --json-out examples/output/public_apple_static_case_study_review_queue.json
earnings-call-risk-map analyze examples/input/public_apple_static_case_study.json --html-out examples/output/public_apple_static_case_study_dashboard.html
```

### demo_company_prior

- Company: Example Systems Inc.
- Ticker: `EXM`
- As of: `2026-02-15`
- Data cutoff: `2026-01-31`
- Static/live status: static compare baseline

```bash
earnings-call-risk-map analyze examples/input/demo_company_prior.json --json-out examples/output/demo_prior_snapshot.json --md-out examples/output/demo_prior_report.md
earnings-call-risk-map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json
```
