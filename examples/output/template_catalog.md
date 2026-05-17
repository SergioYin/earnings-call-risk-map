# Template Catalog

Reusable blank templates for starting deterministic earnings-review fixtures.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

| Template | Path | Purpose |
| --- | --- | --- |
| Software Earnings Review | `examples/templates/software_earnings_review.json` | SaaS, cloud, platform, or other software earnings review starting point. |
| Energy Infrastructure Earnings Review | `examples/templates/energy_infrastructure_earnings_review.json` | Capital-intensive utility, energy infrastructure, project, or regulated-asset review starting point. |
| Consumer Hardware Earnings Review | `examples/templates/consumer_hardware_earnings_review.json` | Device, channel inventory, product launch, supply chain, or warranty review starting point. |

## Recommended Fields And Commands

### Software Earnings Review

- Slug: `software`
- Path: `examples/templates/software_earnings_review.json`
- Top-level fields: `company`, `ticker`, `as_of`, `data_cutoff`
- Note fields: `date`, `evidence_url`, `id`, `text`, `topic`, `type`
- KPI fields: `date`, `direction`, `evidence_url`, `name`, `observation`, `value`
- Catalyst fields: `date`, `description`, `evidence_url`, `expected_impact`, `title`
- Suggested note topics: `revenue durability`, `enterprise demand`, `margin and retention watchlist`
- Suggested KPIs: `Revenue growth`, `Net retention`, `Gross margin`
- Suggested catalysts: `Next earnings report`, `Investor day or product launch`

```bash
earnings-call-risk-map analyze examples/templates/software_earnings_review.json
earnings-call-risk-map review-queue examples/templates/software_earnings_review.json --md-out examples/output/software_template_review_queue.md --json-out examples/output/software_template_review_queue.json
earnings-call-risk-map analyze examples/templates/software_earnings_review.json --json-out examples/output/software_template_snapshot.json --md-out examples/output/software_template_report.md
```

### Energy Infrastructure Earnings Review

- Slug: `energy_infrastructure`
- Path: `examples/templates/energy_infrastructure_earnings_review.json`
- Top-level fields: `company`, `ticker`, `as_of`, `data_cutoff`
- Note fields: `date`, `evidence_url`, `id`, `text`, `topic`, `type`
- KPI fields: `date`, `direction`, `evidence_url`, `name`, `observation`, `value`
- Catalyst fields: `date`, `description`, `evidence_url`, `expected_impact`, `title`
- Suggested note topics: `project execution`, `permitting and regulatory`, `capital cost and financing watchlist`
- Suggested KPIs: `Construction work in progress`, `Project cost variance`, `Contracted capacity backlog`, `Debt to capital`
- Suggested catalysts: `Permit or rate-case milestone`, `Project commissioning window`

```bash
earnings-call-risk-map analyze examples/templates/energy_infrastructure_earnings_review.json
earnings-call-risk-map review-queue examples/templates/energy_infrastructure_earnings_review.json --md-out examples/output/energy_infrastructure_template_review_queue.md --json-out examples/output/energy_infrastructure_template_review_queue.json
earnings-call-risk-map analyze examples/templates/energy_infrastructure_earnings_review.json --json-out examples/output/energy_infrastructure_template_snapshot.json --md-out examples/output/energy_infrastructure_template_report.md
```

### Consumer Hardware Earnings Review

- Slug: `consumer_hardware`
- Path: `examples/templates/consumer_hardware_earnings_review.json`
- Top-level fields: `company`, `ticker`, `as_of`, `data_cutoff`
- Note fields: `date`, `evidence_url`, `id`, `text`, `topic`, `type`
- KPI fields: `date`, `direction`, `evidence_url`, `name`, `observation`, `value`
- Catalyst fields: `date`, `description`, `evidence_url`, `expected_impact`, `title`
- Suggested note topics: `product demand`, `channel inventory`, `supply chain and margin watchlist`
- Suggested KPIs: `Units shipped`, `Channel inventory`, `Gross margin`, `Warranty accrual`
- Suggested catalysts: `Product launch window`, `Holiday or seasonal demand update`

```bash
earnings-call-risk-map analyze examples/templates/consumer_hardware_earnings_review.json
earnings-call-risk-map review-queue examples/templates/consumer_hardware_earnings_review.json --md-out examples/output/consumer_hardware_template_review_queue.md --json-out examples/output/consumer_hardware_template_review_queue.json
earnings-call-risk-map analyze examples/templates/consumer_hardware_earnings_review.json --json-out examples/output/consumer_hardware_template_snapshot.json --md-out examples/output/consumer_hardware_template_report.md
```
