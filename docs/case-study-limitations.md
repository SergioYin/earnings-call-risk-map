# Case Study Limitations

The bundled case studies are static fixtures for demonstrating deterministic review workflows. They are not live company research, market data, investment recommendations, or substitutes for reading current source documents.

## Static Source Limitations

The repository fixtures are checked-in JSON files. Running the CLI does not fetch updated transcripts, filings, investor-relations releases, price data, estimates, or news. Any public URL in a fixture is attribution metadata for the static note, KPI, catalyst, or source record.

Treat fixture content as a frozen example with these limits:

- Management claims remain company-provided statements until a reviewer verifies them against current filings, transcripts, or releases.
- Analyst questions remain questions or prompts; they are not converted into factual assertions.
- User synthesis is reviewer-authored context and deterministic scoring output; it is not advice.
- Missing evidence URLs, stale dates, and `date-unverified` badges are review triggers, not defects to hide.
- Deterministic scores show keyword attention inside the supplied fixture only. They do not estimate price movement, expected return, fair value, or portfolio suitability.

## Source Freshness

Every review should keep the fixture dates visible:

- `as_of`: the review date used for stale/static comparisons.
- `data_cutoff`: the latest source date the fixture author intended to represent.
- item-level `date`: the date for each note, KPI, or catalyst.
- `accessed_at`: the date a source URL was recorded in `source_attribution`, when available.

Before relying on any conclusion, refresh the source pack outside this tool and update the fixture. At minimum, check whether new earnings releases, filings, corrected transcripts, restatements, investor presentations, or material event disclosures were published after `data_cutoff`.

Do not relabel a stale static fixture as current. If the source cannot be refreshed, keep the stale/static warning in the report and treat the output as historical review material.

## Replacing Fixtures With User-Collected Notes

To use this project with your own research notes, create a new JSON fixture instead of editing the bundled demo files in place.

1. Copy `examples/input/demo_company.json` to a new path such as `research/acme_2026_q1.json`.
2. Replace `company`, `ticker`, `as_of`, and `data_cutoff` with the review date and source cutoff for your collected materials.
3. Add only notes, KPIs, and catalysts that you can attribute to a source or clearly mark as user synthesis.
4. For each item, preserve `type` values such as `management_claim`, `analyst_question`, and `user_synthesis`.
5. Add `evidence_url` and `source_attribution` records when available, including `source_name`, `publisher`, `source_type`, `source_url`, `accessed_at`, and a static notice.
6. Leave uncertain or missing evidence visible. The review queue exists to surface those gaps.
7. Run `analyze`, `review-queue`, and any downstream `compare` only after the fixture dates and source boundaries have been reviewed.

Example provenance pattern:

```json
{
  "date": "2026-05-01",
  "topic": "gross margin",
  "type": "management_claim",
  "text": "Prepared remarks summarized by the reviewer.",
  "evidence_url": "https://example.com/investor-relations/transcript",
  "source_attribution": {
    "source_name": "Q1 2026 earnings call transcript",
    "publisher": "Example issuer investor relations",
    "source_type": "transcript",
    "source_url": "https://example.com/investor-relations/transcript",
    "accessed_at": "2026-05-02",
    "static_notice": "User-collected static source note; not live data."
  }
}
```

## Non-Advice Safeguards

Keep these safeguards in any public or downstream artifact:

- State that outputs are educational research review only.
- Do not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.
- Do not translate scores into price targets, return forecasts, allocation changes, ratings, or trade instructions.
- Keep management claims, analyst questions, and user synthesis separated.
- Keep stale/static warnings, source attribution, and safety notices visible.
- Ask reviewers to verify current source materials before relying on any conclusion.

For wording rules and safer rewrites, see [Non-Advice Boundary](non-advice-boundary.md).
