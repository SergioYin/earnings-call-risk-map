# Release Notes: v0.3.0

Release date: 2026-05-17

## Scope

v0.3.0 is a showcase release focused on static previewability: deterministic SVG dashboard previews, local Pages-style viewing guidance, and stronger release artifact checks while preserving the zero-dependency and public-safe boundary.

## Added

- PNG-free dashboard preview SVG at `examples/output/showcase_dashboard_preview.svg`.
- Documentation asset copy at `docs/assets/showcase-dashboard-preview.svg`.
- Static demo viewing and screenshot guidance at `docs/pages-demo.md`.
- README badge/link section pointing to the local SVG preview, gallery, Pages demo guidance, release notes, and generated dashboard HTML.
- Selfcheck validation that dashboard HTML and SVG preview files exist and contain no script, linked stylesheet, image, or linked SVG asset markers.

## Changed

- Package version is now `0.3.0`.
- Maturity evidence includes SVG preview artifacts.
- Release readiness documentation now points to the v0.3.0 notes and preview assets.

## Verification

The release is expected to pass:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
```

## Safety Boundary

The release remains educational research review only. It does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Preview assets are deterministic, self-contained SVG or HTML files with no external asset loads.
