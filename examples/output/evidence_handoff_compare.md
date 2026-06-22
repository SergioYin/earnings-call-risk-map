# Evidence Handoff Compare

- Schema: `earnings-call-risk-map.evidence-handoff-compare.v1`
- Package: `earnings-call-risk-map`
- Version: `0.9.3`
- Before: `examples/output/evidence_handoff_compare_demo_before.json`
- After: `examples/output/evidence_handoff_compare_demo_after.json`
- Added: 1
- Removed: 1
- Changed: 1
- Unchanged: 1
- Boundary changed: yes
- Safety notice changed: no

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

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

## Changed Entries

| Key | Relative path | Differences |
| --- | --- | --- |
| examples/output/demo_report.md | examples/output/demo_report.md | bytes, sha256, freshness_status |

## Added Entries

| Key | Relative path | Role | Present | Bytes |
| --- | --- | --- | --- | ---: |
| examples/output/demo_review_queue.md | examples/output/demo_review_queue.md | generated_review_queue | yes | 180 |

## Removed Entries

| Key | Relative path | Role | Present | Bytes |
| --- | --- | --- | --- | ---: |
| examples/output/old_review_queue.md | examples/output/old_review_queue.md | generated_review_queue | no |  |

## Boundary Comparison

- Added boundaries: `no accounting advice`, `no buy advice`, `no hold advice`, `no legal advice`, `no sell advice`, `no tax advice`
- Removed boundaries: None
- Unchanged boundaries: 5

## Comparison Notes

- Stable keys prefer evidence_id when present and otherwise use relative_path.
- Changed entries list metadata differences only; artifact contents are not embedded.
- Byte, SHA-256, presence, role, freshness, and source-boundary fields are compared when available.
