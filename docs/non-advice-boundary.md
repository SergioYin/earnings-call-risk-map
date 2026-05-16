# Non-Advice Boundary

This project produces deterministic research review artifacts from static public or user-authored inputs. Agents using it must keep outputs educational, source-bound, and review-oriented.

## Required Boundary

Always preserve this meaning in user-facing responses and generated artifacts:

- The output is educational research review only.
- It is not personalized investment, legal, accounting, tax, buy, sell, or hold advice.
- Stale/static data warnings remain visible.
- Management claims, analyst questions, and user synthesis remain separated.
- Source materials must be verified before relying on any conclusion.

## Do

- Say "risk attention increased" or "deterministic score increased" when describing score movement.
- Say "review this source" or "verify this filing/transcript" when evidence is missing, stale, or high-impact.
- Say "the fixture records this as a management claim" when summarizing company-provided language.
- Say "analyst question" when the source text is a prompt or question rather than a factual assertion.
- Say "user synthesis" for user-authored notes, tags, interpretations, and deterministic tool scores.
- Keep `safety_notice`, `source_boundaries`, stale/static badges, and source attribution in downstream JSON or Markdown handoffs.
- Mention exact `as_of`, `data_cutoff`, and source access dates when discussing freshness.

## Do Not

- Do not tell a user to buy, sell, hold, short, overweight, underweight, enter, exit, or rebalance a security.
- Do not convert deterministic risk or opportunity scores into price targets, expected returns, or portfolio actions.
- Do not present management claims as verified facts unless a reviewer has independently verified the source.
- Do not treat analyst questions as assertions.
- Do not remove stale/static data warnings because they make the report look less current.
- Do not describe static public fixtures as live market data.
- Do not infer suitability for a user's personal financial, tax, legal, or accounting situation.

## Safer Rewrites

| Risky wording | Boundary-preserving wording |
| --- | --- |
| "Buy because opportunity score increased." | "Opportunity attention increased in the deterministic score; verify the source materials before drawing any investment conclusion." |
| "The company proved margins will recover." | "The fixture records a management claim about margin recovery; verify it against filings and transcripts." |
| "Ignore this item because the data is old." | "This item is stale/static and should stay visible for source refresh." |
| "The analyst said demand is weak." | "The source contains an analyst question about demand weakness; treat it as a prompt, not a factual claim." |
| "This is a current Apple analysis." | "This is a static educational case-study fixture with the stated `as_of` and `data_cutoff` dates." |

## Validation

Before sharing a public artifact or agent response derived from this repo, run:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
```

For release evidence, also run:

```bash
PYTHONPATH=src python -m earnings_call_risk_map audit
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```
