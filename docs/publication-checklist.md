# Publication Checklist

Use this owner checklist immediately before creating a public GitHub release. It assumes the release candidate has already passed the final [Release Owner Handoff](release-owner-handoff.md), the local readiness flow in [Release Readiness](release-readiness.md), and the package distribution dry run in [Distribution](distribution.md).

Do not publish private fixtures, unreleased company information, account identifiers, secrets, or proprietary research notes. This repository is intended for public, deterministic, educational research review artifacts only.

## 1. Confirm The Release Candidate

1. Confirm `README.md`, `CHANGELOG.md`, `pyproject.toml`, `src/earnings_call_risk_map/version.py`, and the current release notes in [docs/release-notes-v0.8.0.md](release-notes-v0.8.0.md) agree on the version.
2. Confirm generated artifacts are fresh:

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

3. Review [docs/reviewer-evidence.md](reviewer-evidence.md), [reports/maturity/maturity_evidence.md](../reports/maturity/maturity_evidence.md), and [reports/reviews/release-readiness-review.md](../reports/reviews/release-readiness-review.md) for unresolved reviewer notes.

## 2. Run Smoke Checks

Run the public smoke path from a clean checkout or a clean working tree:

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format markdown
```

Open the local preview files named in [Pages Demo](pages-demo.md), especially `docs/demo-index.html`, `examples/output/demo_dashboard.html`, and `examples/output/showcase_dashboard_preview.svg`.

## 3. Run Privacy Scan

Run the privacy scan and manually review any public fixtures or generated examples touched since the last release:

```bash
python scripts/privacy_scan.py
```

Treat a passing scan as one signal, not a full privacy review. Follow the assumptions in [Security And Privacy](security-and-privacy.md), and confirm static public-source examples remain covered by [Case Study Limitations](case-study-limitations.md), [Source Attribution Guide](source-attribution-guide.md), and [Non-Advice Boundary](non-advice-boundary.md).

## 4. Check The Public Skill Path

Confirm the public agent skill path exists and references the current package behavior:

```bash
test -f skills/agent/earnings-call-risk-map/SKILL.md
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
```

The expected public skill path is [skills/agent/earnings-call-risk-map/SKILL.md](../skills/agent/earnings-call-risk-map/SKILL.md). If the skill was edited, re-run the smoke checks and privacy scan before tagging.

## 5. Create And Push The Tag

Create an annotated tag only after the repository state is the intended public release state:

```bash
git status --short
git tag -a v0.8.0 -m "v0.8.0"
git push origin v0.8.0
```

If the version changes, update the tag name and release-note path consistently before running this checklist.

## 6. Create The GitHub Release

Create the GitHub release from the pushed tag:

```bash
gh release create v0.8.0 \
  --title "v0.8.0" \
  --notes-file docs/release-notes-v0.8.0.md
```

Before publishing, confirm the release page links back to the public docs, includes the educational research review boundary, and does not attach private or locally generated scratch artifacts. Do not upload package-index artifacts unless the separate distribution owner has approved that step.

## 7. Post-Publish Smoke

After GitHub shows the release:

1. Open the release page and verify the tag, title, and notes render correctly.
2. Check that links to README docs, release notes, preview assets, and the public skill path resolve in the GitHub UI.
3. Clone the tagged release into a temporary directory and run:

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
```

Record any exceptions in the release notes or a follow-up issue before announcing the release.
