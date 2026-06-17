# Reviewer Feedback Consumption

This note summarizes how prior reviewer feedback shaped v0.8 and carries that evidence forward for v0.9. It is a companion to the reviewer command appendix in [Reviewer Evidence](reviewer-evidence.md), the v0.9 release summary in [Release Notes v0.9.0](release-notes-v0.9.0.md), and the final score evidence in [Maturity Evidence](../reports/maturity/maturity_evidence.md).

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.

## Product Clarity

Early reviews accepted the core earnings-call risk-map concept but repeatedly asked for a clearer first-run story and stronger public examples. v0.8 reflects that feedback by keeping the product scope narrow: local deterministic review of source-provided notes, KPIs, catalysts, stale badges, review queues, dashboards, compare outputs, playbooks, and handoff artifacts.

Feedback consumed:

- v0.1 flagged synthetic data as the main trust gap and asked for a public static fixture and clearer promotion path in [the v0.1 internal review](../reports/reviews/2026-05-17-v0.1.0-internal-review.md).
- v0.2 closed the public static fixture gap and shifted the remaining clarity work toward preview and distribution evidence in [the v0.2 internal review](../reports/reviews/2026-05-17-v0.2.0-internal-review.md).
- v0.7 added the adoption-positioning layer with [Comparison To Spreadsheets](comparison-to-spreadsheets.md), clarifying when deterministic artifacts are better or worse than spreadsheets and generic notes.
- v0.8 aligns README, usage docs, release notes, reviewer evidence, publication checklist, templates, examples index, doctor output, and generated maturity evidence around the `0.8.0` release line.
- v0.9 adds source-boundary walkthrough receipt evidence in [the v0.9 internal review](../reports/reviews/2026-06-18-v0.9.0-internal-review.md).

Result in v0.8: product clarity is scored `15/15` in [the v0.8 internal review](../reports/reviews/2026-05-17-v0.8.0-internal-review.md).

## Reproducibility

Reviewer feedback consistently pushed the project to prove that a release can be regenerated locally without network calls, credentials, workflow runners, databases, or runtime dependencies. v0.8 carries that through with local unit tests, `selfcheck`, release asset checks, privacy scan, package audit, manifest generation, maturity evidence, and docs link verification.

Feedback consumed:

- v0.3 and v0.4 reviews treated deterministic previews, manifests, and reviewer evidence as release-quality requirements rather than optional polish.
- v0.6 expanded reproducibility evidence to include playbooks, playbook output examples, handoff packet examples, release assets, and maturity evidence.
- v0.8 records exact verification commands and fresh clone validation in [Reviewer Evidence](reviewer-evidence.md), while [Release Readiness](release-readiness.md) names the current release docs and evidence regeneration commands.

Result in v0.8: reproducibility is scored `15/15`, with evidence for unit tests, `selfcheck`, `release-assets`, privacy scan, `git diff --check`, and local-only audit in [the v0.8 internal review](../reports/reviews/2026-05-17-v0.8.0-internal-review.md).

## Demo Evidence

The earliest reviews asked for proof that cold users could understand the tool without reading every fixture. v0.8 inherits the demo evidence built across prior releases: static HTML dashboards, SVG preview assets, public/static case-study outputs, generated reports, review queues, JSON snapshots, compare reports, playbooks, examples index, command cheat sheet, and publication checklist artifacts.

Feedback consumed:

- v0.1 and v0.2 requested a screenshot, GIF, or Pages-style preview; v0.3 closed that with a PNG-free SVG preview and local static dashboard guidance in [Pages Demo](pages-demo.md).
- v0.4 improved evidence quality with schema, compare artifacts, package/reviewer evidence docs, and generated manifests.
- v0.6 added recurring workflow evidence through [Research Playbooks](../examples/playbooks/README.md) and generated playbook examples.
- v0.8 keeps demo evidence inspectable through [Gallery](gallery.md), [Public Case Study](public-case-study.md), [Case Study Map](case-study-map.md), and generated files listed in [Reviewer Evidence](reviewer-evidence.md).

Result in v0.8: showcase and distribution readiness remain strong but intentionally bounded because hosted demo deployment is still a release-owner decision, not a package requirement.

## Risk Boundaries

Reviewer feedback also shaped what the project must not become. Each release preserved the educational, non-advice, static-data, local-only, no-credentials boundary while adding clearer source attribution and human handoff language.

Feedback consumed:

- v0.1 and v0.2 risk reviewers accepted the boundary but warned against implying that source data is live, current, or verified.
- v0.4 and later reviews reinforced that public examples, dashboards, and promotion copy must preserve stale/static badges and source-boundary labels.
- v0.7 made the product boundary sharper by documenting where spreadsheets, generic notes, or other tools are better fits.
- v0.8 keeps public copy and handoff docs inside the limits described in [Non-Advice Boundary](non-advice-boundary.md), [Case Study Limitations](case-study-limitations.md), [Source Attribution Guide](source-attribution-guide.md), and [Security And Privacy](security-and-privacy.md).

Result in v0.8: risk boundary is scored `7/10` in the internal review, with no P0 or P1 blockers for small-scope owner handoff. The remaining constraint is deliberate: release-owner approval is required before public promotion, hosted deployment, package publishing, or any live-source integration.

## v0.8 Summary

Prior reviewer feedback moved v0.8 toward a narrower and more reviewable release: clearer product positioning, stronger local reproducibility, more demo evidence, and stricter risk boundaries. The release still avoids live market data, recommendations, ratings, price targets, portfolio actions, workflow automation, and personalized advice.

For final validation, use the commands in [Reviewer Evidence](reviewer-evidence.md) and the release-owner gates in [Publication Checklist](publication-checklist.md).
