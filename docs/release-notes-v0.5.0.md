# Release Notes Draft: v0.5.0

Draft date: 2026-05-17

## Scope

v0.5.0 is a release-evidence and agent-workflow draft release. It adds deterministic fixture discovery, JSON Lines review-queue exports, stronger local-only/no-network audit evidence, and tutorial documentation for repeatable earnings-call review workflows.

## Added

- `fixture-catalog` CLI command for listing bundled fixtures and recommended local commands.
- Generated fixture catalog artifact at [examples/output/fixture_catalog.md](../examples/output/fixture_catalog.md).
- `review-queue-jsonl` CLI command for deterministic JSON Lines review-item exports across bundled fixtures.
- Generated review-queue JSONL artifact at [examples/output/demo_review_queue_items.jsonl](../examples/output/demo_review_queue_items.jsonl).
- Agent workflow guide at [docs/agent-workflow.md](agent-workflow.md).
- Earnings review tutorial at [docs/tutorial-earnings-review.md](tutorial-earnings-review.md).
- Fixture catalog documentation at [docs/fixture-catalog.md](fixture-catalog.md).
- Local-only package audit evidence for runtime dependencies, network-client imports, credential environment reads, workflow-file absence, and per-command network/credential requirements.
- Selfcheck validation for review-queue JSONL output and required tutorial markers.

## Changed

- Package version is now `0.5.0`.
- README, usage, gallery, scoring, release readiness, reviewer evidence, and the public agent skill now describe the expanded evidence workflow.
- Demo generation now writes review-queue JSONL records and a fixture catalog artifact.
- Package audit JSON and Markdown now include a local-only no-network guarantee section.
- Maturity evidence now records the review-queue JSONL command and JSONL artifact paths.
- Demo artifacts, package audit outputs, release manifests, static dashboard previews, and maturity evidence were regenerated for the v0.5.0 candidate.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
git diff --check
```

Optional local wheel dry run:

```bash
python -m pip install --upgrade build
rm -rf dist-dry-run
python -m build --wheel --outdir dist-dry-run
python -m zipfile --list dist-dry-run/*.whl
python -m pip install --force-reinstall --no-deps dist-dry-run/*.whl
earnings-call-risk-map version
```

Expected version output: `0.5.0`.

## Safety Boundary

The release remains educational research review only. It does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. The local-only audit evidence records no required network access, credentials, external services, workflow files, or runtime package dependencies.
