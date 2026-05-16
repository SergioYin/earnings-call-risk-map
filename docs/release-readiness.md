# Release Readiness

Use the release readiness review template at `reports/reviews/release-readiness-review.md` before publishing a demo bundle or tagged release.

Use `docs/release-notes-v0.3.0.md` as the deterministic release notes source for v0.3.0. Prior notes remain in `docs/release-notes-v0.2.0.md` and `docs/release-notes-v0.1.0.md`.

Use `docs/pages-demo.md` to verify the local static HTML demo path and screenshot framing. The PNG-free preview assets are:

- `docs/assets/showcase-dashboard-preview.svg`
- `examples/output/showcase_dashboard_preview.svg`

Generate the basic maturity evidence bundle with either entry point:

```bash
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
python scripts/maturity_evidence.py --out-dir reports/maturity
```

The generated bundle writes:

- `reports/maturity/maturity_evidence.json`
- `reports/maturity/maturity_evidence.md`

The evidence bundle lists the local test commands, generated artifact paths, public skill path, release review template path, and current privacy scan status.

Recommended release check:

```bash
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```
