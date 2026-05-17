# Package Distribution

This project is prepared for local package distribution, but these instructions do not publish anything to PyPI or another package index.

## Supported Python Versions

- Package metadata supports Python `3.9` or newer.
- Runtime dependencies remain zero.
- Build-time packaging uses `setuptools` through `pyproject.toml`.

Before packaging, verify the target interpreter:

```bash
python --version
PYTHONPATH=src python -m earnings_call_risk_map version
```

## pipx From A Checkout

Use `pipx` when you want the CLI installed as an isolated command from the local checkout:

```bash
python -m pip install --user pipx
python -m pipx ensurepath
pipx install --force .
earnings-call-risk-map version
earnings-call-risk-map analyze examples/input/demo_company.json
```

For a one-off local run without keeping the command installed:

```bash
pipx run --spec . earnings-call-risk-map version
```

Remove the local `pipx` install with:

```bash
pipx uninstall earnings-call-risk-map
```

## Local pip Install

For normal local installation from the checkout:

```bash
python -m pip install .
earnings-call-risk-map version
```

For editable development:

```bash
python -m pip install -e .
earnings-call-risk-map demo --out-dir examples/output
```

## Wheel Build Dry Run

The wheel dry run builds into a local throwaway directory and does not upload artifacts:

```bash
python -m pip install --upgrade build
rm -rf dist-dry-run
python -m build --wheel --outdir dist-dry-run
python -m zipfile --list dist-dry-run/*.whl
python -m pip install --force-reinstall --no-deps dist-dry-run/*.whl
earnings-call-risk-map version
```

Expected result for this release:

```text
0.8.0
```

Do not run `twine upload`, `gh release upload`, or any package-index publishing command as part of this dry run.

## Verification

Run the local release checks after any packaging dry run:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
```

The selfcheck includes local documentation-link validation for README and release documentation.

## Troubleshooting

- `No module named build`: install the build frontend with `python -m pip install --upgrade build`.
- `pipx: command not found`: install it with `python -m pip install --user pipx`, then run `python -m pipx ensurepath` and reopen the shell if needed.
- `earnings-call-risk-map: command not found`: confirm the active environment or `pipx` path, then run `python -m pip show earnings-call-risk-map` or `pipx list`.
- Version output is not `0.8.0`: uninstall stale local installs with `python -m pip uninstall earnings-call-risk-map` or `pipx uninstall earnings-call-risk-map`, then reinstall from the checkout.
- Wheel installs but example paths fail: run commands from the repository root, or pass absolute paths for `examples/input/*.json` and output files.
- Build artifacts are stale: remove `build/`, `dist/`, `dist-dry-run/`, and `*.egg-info/`, then rebuild.
