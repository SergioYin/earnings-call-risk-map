# Earnings Review Templates

`examples/templates/` contains reusable blank JSON templates for software, energy infrastructure, and consumer hardware review starting points:

- `examples/templates/software_earnings_review.json`
- `examples/templates/energy_infrastructure_earnings_review.json`
- `examples/templates/consumer_hardware_earnings_review.json`

Each template is valid input for `earnings-call-risk-map analyze` before any company-specific data is added. The required top-level fields use template placeholders, dates use valid `YYYY-MM-DD` strings, and the note, KPI, and catalyst arrays provide domain-specific rows with empty values for source text, KPI values, observations, descriptions, and evidence URLs.

## Template Catalog

Use `template-catalog` to list the blank templates, recommended field groups, suggested domain rows, and starter commands:

```bash
PYTHONPATH=src python -m earnings_call_risk_map template-catalog
PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format json --out examples/output/template_catalog.json
PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format markdown --out examples/output/template_catalog.md
```

The `demo` command writes both `examples/output/template_catalog.md` and `examples/output/template_catalog.json`.

## Use A Template

Start by copying the nearest template into a scratch or research folder, then replace:

- `company`, `ticker`, `as_of`, and `data_cutoff`
- note `text`, `date`, `type`, `topic`, and `evidence_url`
- KPI `value`, `direction`, `date`, `observation`, and `evidence_url`
- catalyst `date`, `description`, `expected_impact`, and `evidence_url`

Keep management claims, analyst questions, and user synthesis separated by `type`. Empty `evidence_url` fields are allowed so the review queue can surface missing source links instead of hiding them.

For a deterministic end-to-end sample that starts with `examples/templates/software_earnings_review.json`, fills the rows, and generates an analyzed report, see [Filled-From-Template Workflow](filled-template-workflow.md). The filled sample fixture is `examples/input/sample_filled_template_workflow.json`.

## Validate A Template

Run the same validator used for normal fixtures:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/templates/software_earnings_review.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/templates/energy_infrastructure_earnings_review.json
PYTHONPATH=src python -m earnings_call_risk_map analyze examples/templates/consumer_hardware_earnings_review.json
```

The test suite also validates every JSON file under `examples/templates/` against the runtime input validator and the documented schema fields.

> Educational research review only. Templates are authoring aids and do not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.
