# Release Notes Draft: v0.6.0

Draft date: 2026-05-17

## Scope

v0.6.0 starts a playbook-oriented release line. It adds deterministic research playbooks for recurring review workflows and validates that those playbooks stay present in tests and selfcheck.

## Added

- Research playbook index at [examples/playbooks/README.md](../examples/playbooks/README.md).
- Quarterly review playbook at [examples/playbooks/quarterly-review.md](../examples/playbooks/quarterly-review.md).
- Catalyst check-in playbook at [examples/playbooks/catalyst-check-in.md](../examples/playbooks/catalyst-check-in.md).
- Post-earnings thesis refresh playbook at [examples/playbooks/post-earnings-thesis-refresh.md](../examples/playbooks/post-earnings-thesis-refresh.md).
- Internal maturity review at [reports/reviews/2026-05-17-v0.6.0-internal-review.md](../reports/reviews/2026-05-17-v0.6.0-internal-review.md).
- Selfcheck and unit-test coverage for playbook presence, deterministic commands, expected artifacts, and safety markers.

## Changed

- Package version is now `0.6.0`.
- README links now include the playbook index and v0.6.0 release notes draft.
- Reviewer evidence, release manifests, package audit outputs, release-asset checks, and maturity evidence now include the v0.6.0 playbook, handoff-packet, and internal-review evidence set.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map release-assets
python scripts/privacy_scan.py
git diff --check
```

Expected version output: `0.6.0`.

## Safety Boundary

The release remains educational research review only. The playbooks are deterministic research-review workflows and do not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice.
