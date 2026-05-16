# Integration Notes

`earnings-call-risk-map` does not depend on a thesis ledger, portfolio risk system, database, or workflow runner. The intended integration boundary is a file handoff: downstream tools can read the generated JSON and choose what to import.

The two most useful artifacts are:

- `*_snapshot.json`: full deterministic analysis with risks, opportunities, catalysts, stale badges, review queue, source boundaries, and the safety notice.
- `*_review_queue.json`: focused handoff of stale data, missing evidence, and high-impact language.
- `handoff_packet.json`: compact path summary for the Markdown report, review queue JSONL, compare artifact, handoff targets, source boundaries, and cautions.

The examples below show how those outputs can feed adjacent research tools without making this package aware of those tools.

## Thesis Ledger Handoff

A thesis ledger usually tracks claims, evidence, dates, and review status. Treat each risk, opportunity, or catalyst as a candidate ledger note, then preserve the source artifact path and stale/static badge so the ledger can decide whether to accept, reject, or refresh it.

Example mapping:

| Risk-map field | Thesis-ledger note field |
| --- | --- |
| `ticker` | `subject.ticker` |
| `company` | `subject.company` |
| `as_of` | `as_of` |
| `risks[].topic` or `opportunities[].topic` | `thesis_point` |
| `risk_score` / `opportunity_score` | `signals.score` |
| `risk_level` / `opportunity_level` | `signals.level` |
| `evidence_url` | `evidence.url` |
| `stale_badge` | `freshness` |
| `review_reasons` | `review.reasons` |
| `safety_notice` | `source_notice` |

Minimal standard-library extraction:

```python
import json
from pathlib import Path

snapshot = json.loads(Path("examples/output/demo_snapshot.json").read_text(encoding="utf-8"))

ledger_notes = []
for section in ("risks", "opportunities"):
    for item in snapshot[section]:
        ledger_notes.append(
            {
                "integration": "thesis_ledger",
                "source_tool": "earnings-call-risk-map",
                "source_artifact": "examples/output/demo_snapshot.json",
                "as_of": snapshot["as_of"],
                "subject": {"ticker": snapshot["ticker"], "company": snapshot["company"]},
                "thesis_point": item.get("topic") or item.get("name"),
                "direction": "risk" if section == "risks" else "opportunity",
                "signals": {
                    "score": item.get("risk_score") if section == "risks" else item.get("opportunity_score"),
                    "level": item.get("risk_level") if section == "risks" else item.get("opportunity_level"),
                },
                "evidence": {"url": item.get("evidence_url")},
                "freshness": item.get("stale_badge"),
                "review": {"required": item.get("review_required", False), "reasons": item.get("review_reasons", [])},
                "source_notice": snapshot["safety_notice"],
            }
        )
```

The downstream ledger should own deduplication, human approval, position linking, and retention policy. This project only supplies deterministic source notes.

## Portfolio Risk Review Handoff

A portfolio risk review usually wants issue categories, affected ticker, severity hints, and evidence gaps. Use `review-queue` output for this because it is already scoped to items that need attention.

Example mapping:

| Review-queue field | Portfolio-risk review field |
| --- | --- |
| `ticker` | `exposure.ticker` |
| `company` | `exposure.company` |
| `items[].topic` | `issue.title` |
| `items[].issue_categories` | `issue.categories` |
| `items[].reasons` | `issue.review_reasons` |
| `items[].evidence_url` | `evidence.url` |
| `summary.*_count` | `rollup` |
| `source_boundaries` | `review_boundaries` |

Minimal standard-library extraction:

```python
import json
from pathlib import Path

queue = json.loads(Path("examples/output/demo_review_queue.json").read_text(encoding="utf-8"))

risk_review_items = [
    {
        "integration": "portfolio_risk_review",
        "source_tool": "earnings-call-risk-map",
        "source_artifact": "examples/output/demo_review_queue.json",
        "as_of": queue["as_of"],
        "exposure": {"ticker": queue["ticker"], "company": queue["company"]},
        "issue": {
            "title": item["topic"],
            "categories": item["issue_categories"],
            "review_reasons": item["reasons"],
        },
        "evidence": {"url": item.get("evidence_url")},
        "review_boundaries": queue["source_boundaries"],
        "source_notice": queue["safety_notice"],
    }
    for item in queue["items"]
]
```

The portfolio tool should own exposure sizing, portfolio weights, limits, escalation rules, and any investment decision workflow. This project does not infer those fields.

## Machine-Readable Examples

See `examples/output/integration_notes.json` for static example records derived from the demo outputs. The file is intentionally generic and uses `integration` labels instead of importing a ledger or portfolio schema.

For a deterministic handoff index, generate:

```bash
PYTHONPATH=src python -m earnings_call_risk_map handoff-packet \
  --json-out examples/output/handoff_packet.json \
  --md-out examples/output/handoff_packet.md
```

The packet does not import a portfolio or thesis schema. It only summarizes artifact paths and cautions so downstream systems can decide what to ingest.
