# Release Notes: v0.4.0

Release date: 2026-05-17

## Scope

v0.4.0 is a post-v0.3 packaging-readiness and final-polish release. It documents local package distribution paths without publishing artifacts, refreshes demo/release outputs, tightens the README first screen for cold users, and adds selfcheck coverage for local documentation links.

## Added

- Package distribution guide at [docs/distribution.md](distribution.md).
- `pipx` install and one-off run instructions from a local checkout.
- Local `pip` install and editable install instructions.
- Wheel build dry-run instructions using `python -m build --wheel --outdir dist-dry-run`.
- Supported Python version guidance: Python `3.9` or newer.
- Packaging troubleshooting notes for missing build tools, stale installs, path issues, and stale build artifacts.
- Selfcheck validation for local Markdown links in README and release documentation.

## Changed

- Package version is now `0.4.0`.
- README first screen now states the core user value, quickest demo commands, static dashboard path, and non-advice boundary before deeper documentation links.
- README links now point to v0.4.0 release notes and the distribution guide.
- Release readiness documentation now points to the v0.4.0 notes and packaging dry-run guidance.
- Demo artifacts, release manifests, package audit outputs, static dashboard previews, and maturity evidence were regenerated for the v0.4.0 candidate.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
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

Expected version output: `0.4.0`.

## Safety Boundary

The release remains educational research review only. It does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Distribution documentation is local-only and does not instruct publishing to a package index.
