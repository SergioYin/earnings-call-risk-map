# Author A Fixture From Scratch

This example shows how to turn a short earnings-call note into a minimal JSON fixture for `earnings-call-risk-map analyze`.

> Educational research review only. This workflow does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Keep source claims, analyst questions, and user-authored synthesis separate so a reviewer can verify each item against the original materials.

## Starting Note

Assume the raw review note says:

```text
Q1 call, 2026-04-30. Management said enterprise demand remained resilient, but Europe had longer deal cycles. Analyst asked whether discounting increased late in the quarter. My synthesis: watch regional demand pressure and margin risk next quarter. Source: company investor-relations call transcript, accessed 2026-05-15.
```

Before writing JSON, split the note by provenance:

| Provenance | Fixture `type` | What Belongs Here |
| --- | --- | --- |
| Management claim | `management_claim` | Company statements, prepared remarks, or answers from management. Preserve as claims, not verified facts. |
| Analyst question | `analyst_question` | Analyst prompts and Q&A questions. Keep them as questions instead of turning them into assertions. |
| User synthesis | `user_synthesis` | Your review notes, tags, and interpretation. Treat these as review aids, not source facts. |

## Minimal Fixture

Create a JSON file such as `scratch/example-q1-call.json`:

```json
{
  "schema_version": "0.1",
  "company": "Example Systems Inc.",
  "ticker": "EXM",
  "as_of": "2026-05-15",
  "data_cutoff": "2026-04-30",
  "source_attribution": {
    "source_name": "Q1 2026 earnings call transcript",
    "publisher": "Example Systems Inc. Investor Relations",
    "source_type": "transcript",
    "source_url": "https://example.com/exm/q1-2026-call-transcript",
    "accessed_at": "2026-05-15",
    "static_notice": "Static fixture authoring example; verify against the source transcript before use."
  },
  "notes": [
    {
      "id": "q1-mgmt-1",
      "date": "2026-04-30",
      "topic": "enterprise demand",
      "type": "management_claim",
      "text": "Management said enterprise demand remained resilient, but Europe had longer deal cycles.",
      "evidence_url": "https://example.com/exm/q1-2026-call-transcript",
      "source_attribution": {
        "source_name": "Q1 2026 earnings call transcript",
        "publisher": "Example Systems Inc. Investor Relations",
        "source_type": "transcript",
        "source_url": "https://example.com/exm/q1-2026-call-transcript",
        "accessed_at": "2026-05-15",
        "static_notice": "Static fixture authoring example; verify against the source transcript before use."
      }
    },
    {
      "id": "q1-analyst-1",
      "date": "2026-04-30",
      "topic": "discounting",
      "type": "analyst_question",
      "text": "Analyst asked whether discounting increased late in the quarter.",
      "evidence_url": "https://example.com/exm/q1-2026-call-transcript",
      "source_attribution": {
        "source_name": "Q1 2026 earnings call transcript",
        "publisher": "Example Systems Inc. Investor Relations",
        "source_type": "transcript",
        "source_url": "https://example.com/exm/q1-2026-call-transcript",
        "accessed_at": "2026-05-15",
        "static_notice": "Static fixture authoring example; verify against the source transcript before use."
      }
    },
    {
      "id": "q1-user-1",
      "date": "2026-05-15",
      "topic": "regional demand and margin review",
      "type": "user_synthesis",
      "text": "User synthesis: watch regional demand pressure and margin risk next quarter.",
      "source_attribution": {
        "source_name": "User-authored earnings-call review note",
        "publisher": "Fixture author",
        "source_type": "user_synthesis",
        "accessed_at": "2026-05-15",
        "static_notice": "User synthesis is a review aid and not source evidence."
      }
    }
  ],
  "kpis": [],
  "catalysts": []
}
```

The example is intentionally small. The required top-level fields are `company`, `ticker`, `as_of`, and `data_cutoff`; empty `kpis` and `catalysts` arrays are acceptable.

## Authoring Rules

- Use `management_claim` only for source-backed company statements.
- Use `analyst_question` for questions, even when the question implies risk or opportunity.
- Use `user_synthesis` for your own interpretation, summary, or watchlist language.
- Do not rewrite claims or questions as verified facts.
- Include `evidence_url` when a public transcript, filing, investor-relations page, or other source URL is available.
- Keep `accessed_at`, `as_of`, and `data_cutoff` explicit so stale/static data remains visible.
- Leave missing evidence visible. The review queue should flag it rather than hiding it.

## Validate And Run

Validate the fixture through the same path used for analysis:

```bash
PYTHONPATH=src python -m earnings_call_risk_map analyze \
  scratch/example-q1-call.json \
  --md-out scratch/example-q1-call-report.md \
  --json-out scratch/example-q1-call-snapshot.json
```

Build the human-review queue:

```bash
PYTHONPATH=src python -m earnings_call_risk_map review-queue \
  scratch/example-q1-call.json \
  --md-out scratch/example-q1-call-review-queue.md \
  --json-out scratch/example-q1-call-review-queue.json
```

When reading the output, treat scores as deterministic review attention for this fixture. They are not forecasts, recommendations, price targets, or conclusions about the company.

See [JSON Fixture Schema Reference](input-schema.md) for all supported fields.
