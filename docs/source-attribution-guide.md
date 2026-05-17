# Source Attribution Guide

Use source attribution to make fixture provenance inspectable without implying that the project fetched, verified, or refreshed the source. Attribution records are static metadata supplied by the fixture author.

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and preserve stale/static warnings.

See [JSON Fixture Schema Reference](input-schema.md) for accepted fields and [Non-Advice Boundary](non-advice-boundary.md) for wording rules when sharing outputs.

## Attribution Scope

`source_attribution` can appear at the top level of a fixture and on individual notes, KPIs, and catalysts.

- Top-level attribution describes the fixture or source bundle.
- Item-level attribution describes the specific note, KPI, or catalyst.
- Multiple attribution records are allowed when an item combines source labels, such as a transcript excerpt plus a user-authored synthesis note.

Attribution does not replace `evidence_url`. Missing `evidence_url` values still enter the review queue when evidence is required.

## `source_type` Choices

Use `source_type` for the source container or provenance class, not for the conclusion you want a reviewer to draw. The field is intentionally descriptive and static.

| `source_type` | Use when | Review posture |
| --- | --- | --- |
| `company_investor_relations` | A company IR page, earnings release page, presentation page, or event page is the source. | Treat as company-provided material; verify before relying on claims. |
| `sec_filing` | A public filing or SEC EDGAR page is the source. | Treat as a formal filing reference; still check date, filing period, and whether later filings supersede it. |
| `transcript` | The source is an earnings-call transcript or prepared remarks/Q&A transcript. | Pair with note `type` to separate management statements from analyst questions. |
| `shareholder_letter` | The source is a shareholder letter or similar company communication. | Treat as company-authored context, not independent verification. |
| `press_release` | The source is a company or wire-service press release. | Preserve publisher and source date; verify against filings or later corrections when material. |
| `news_article` | The source is an article or external publication. | Preserve publisher; do not promote article summaries into verified fixture facts without review. |
| `user_synthesis` | The source is a user-authored summary, tag, worksheet note, or deterministic review note. | Treat as a review aid, not source evidence or advice. |

Prefer the closest specific value already used in the repository before adding a new one. If a new value is necessary, keep it lowercase, concise, and provenance-focused.

## `accessed_at`

`accessed_at` records the date the fixture author last captured or checked the source URL. It should use `YYYY-MM-DD`.

Use it to answer "when did this static fixture author look at this source?", not "when was the source published?" Publication or event dates belong in item `date`, fixture `data_cutoff`, or the source title.

Guidelines:

- Set `accessed_at` when a `source_url` points to a web page, filing, transcript, or public artifact.
- Update `accessed_at` only when a reviewer actually re-checks the source.
- Do not use today's date merely because the fixture was regenerated locally.
- Keep old `accessed_at` dates visible in static case studies so stale-source review remains possible.

## Stale Badges

Stale badges are based on item dates compared with fixture `as_of`, not on `accessed_at`.

- `current`: the item date is within 90 days of `as_of`.
- `stale>90d`: the item date is more than 90 days older than `as_of`.
- `date-unverified`: the item date is missing or cannot be validated.

An old `accessed_at` date is still important context, but it does not by itself create the stale badge. A recent `accessed_at` also does not make old source content current.

When resolving stale review items, update the item `date`, `data_cutoff`, and attribution only after checking current source material. Do not hide stale badges by deleting dates.

## Management, Analyst, And User Synthesis

Keep `source_type` separate from note `type`.

`source_type` answers where the source record came from. Note `type` answers how to treat the text inside the review.

| Note `type` | Use for | Boundary |
| --- | --- | --- |
| `management_claim` | Company statements, prepared remarks, shareholder-letter assertions, guidance language, or IR claims. | Do not present as verified fact unless a reviewer has independently verified the source. |
| `analyst_question` | Analyst prompts, Q&A questions, or external questions quoted from a transcript. | Treat as a question or concern, not as a factual assertion. |
| `user_synthesis` | User-authored summaries, tags, interpretations, thesis notes, or deterministic scoring notes. | Treat as a review prompt, not source evidence, personalized advice, or a recommendation. |
| `transcript_excerpt` | Neutral transcript snippets where the speaker role is not separated. | Use a more specific type when the speaker role is known. |
| `note` | Generic notes that do not fit a more specific category. | Prefer a more specific type when provenance matters. |

Examples:

```json
{
  "type": "management_claim",
  "text": "Management said supply constraints improved during the quarter.",
  "source_attribution": {
    "source_name": "Q1 earnings call transcript",
    "publisher": "Example Corp Investor Relations",
    "source_type": "transcript",
    "source_url": "https://example.com/investors/q1-transcript",
    "accessed_at": "2026-05-17",
    "static_notice": "Static transcript reference; verify against current source materials."
  }
}
```

```json
{
  "type": "user_synthesis",
  "text": "User synthesis: review whether margin pressure is still unresolved.",
  "source_attribution": {
    "source_name": "Reviewer worksheet note",
    "publisher": "Fixture author",
    "source_type": "user_synthesis",
    "accessed_at": "2026-05-17",
    "static_notice": "User synthesis is a review aid and not source evidence."
  }
}
```

## Review Checklist

Before adding or updating attribution:

- Confirm the source record has a clear `source_name`, `publisher`, and `source_type`.
- Use `accessed_at` only for the date the source was actually checked.
- Keep `management_claim`, `analyst_question`, and `user_synthesis` distinct in note `type`.
- Preserve stale badges until item dates and source materials have been refreshed.
- Keep the non-advice disclaimer and source boundaries in downstream Markdown, JSON, and handoff artifacts.
