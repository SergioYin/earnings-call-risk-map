# Release Owner Compare Blocker Checklist

- Schema: `earnings-call-risk-map.release-owner-compare-blockers.v1`
- Package: `earnings-call-risk-map`
- Version: `0.9.7`
- Compare input: `examples/output/evidence_handoff_compare.json`
- Release decision: `blocked`
- Blockers: 1
- Review-required checks: 4

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

## Checklist

| Gate | Status | Evidence | Release-owner action |
| --- | --- | --- | --- |
| No evidence handoff artifacts were removed. | `blocker` | examples/output/old_review_queue.md | Restore the artifact, regenerate the handoff bundle, or record owner acceptance before release. |
| No previously present evidence artifact became missing. | `clear` | None | Regenerate missing artifacts before release or explicitly remove them from the release evidence set. |
| No existing local-only, no-live-data, no-private-data, or non-advice boundary was removed. | `clear` | None | Do not release until removed boundary language is restored or the release owner accepts the changed boundary. |
| The safety notice did not change between evidence handoff audits. | `clear` | None | Review safety notice text against the non-advice boundary before release. |
| Added evidence artifacts are reviewed for public-source, local-only, and non-advice boundaries. | `review_required` | examples/output/demo_review_queue.md | Inspect added artifacts for source scope, stale/static labeling, and release-owner relevance. |
| Changed byte counts or SHA-256 hashes are explained by intentional generated artifact or documentation updates. | `review_required` | examples/output/demo_report.md | Review the changed artifact diff or regeneration command before release. |
| Evidence role changes are intentional and do not hide release evidence. | `clear` | None | Confirm role changes still route artifacts to the right reviewer handoff bucket. |
| Freshness and source-boundary metadata changes are reviewed before release. | `review_required` | examples/output/demo_report.md | Review source-boundary and freshness notes; do not treat stale/static artifacts as current analysis. |
| New boundary language is reviewed for consistency across public docs and generated artifacts. | `review_required` | no accounting advice, no buy advice, no hold advice, no legal advice, no sell advice, +1 more | Confirm added boundary text is consistent with public docs and generated evidence. |

## Source Compare Summary

- Added artifacts: 1
- Removed artifacts: 1
- Changed artifacts: 1
- Unchanged artifacts: 1

## Release Owner Notes

- This checklist summarizes metadata from evidence handoff compare artifacts; it does not embed artifact contents.
- A clear checklist does not approve tagging, publishing, hosted demo deployment, or public announcement.
- The release owner must review changed evidence, stale/static labels, and source boundaries before relying on the handoff.

## Boundaries

- local/static fixtures only
- no live data
- no broker connection
- no personalized investment advice
- no legal advice
- no accounting advice
- no tax advice
- no buy advice
- no sell advice
- no hold advice
- no private data
