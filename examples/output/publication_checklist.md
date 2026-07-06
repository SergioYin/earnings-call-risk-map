# Publication Checklist

- Package: `earnings-call-risk-map`
- Version: `0.9.7`
- Source doc: `docs/publication-checklist.md`
- Owner scope: public GitHub release owner steps
- Steps: 7

> Educational research review only. This tool does not provide personalized investment, legal, accounting, tax, buy, sell, or hold advice. Verify source materials and note that stale/static data may no longer reflect current conditions.

> Do not publish private fixtures, unreleased company information, account identifiers, secrets, or proprietary research notes.

## 1. Confirm The Release Candidate

Confirm version alignment, fresh generated artifacts, and unresolved reviewer notes.

### Checks

- Confirm `README.md`, `CHANGELOG.md`, `pyproject.toml`, `src/earnings_call_risk_map/version.py`, and the current release notes agree on the version.
- Confirm generated artifacts are fresh.
- Review `docs/reviewer-evidence.md`, `reports/maturity/maturity_evidence.md`, and `reports/reviews/release-readiness-review.md` for unresolved reviewer notes.

### Commands

```bash
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json
PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity
```

## 2. Run Smoke Checks

Run the public smoke path from a clean checkout or clean working tree.

### Checks

- Run the unit tests, selfcheck, package audit, and release asset checklist.
- Open `docs/demo-index.html`, `examples/output/demo_dashboard.html`, and `examples/output/showcase_dashboard_preview.svg`.

### Commands

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python scripts/selfcheck.py
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
PYTHONPATH=src python -m earnings_call_risk_map release-assets --format markdown
```

## 3. Run Privacy Scan

Run the privacy scan and manually review public fixtures or generated examples touched since the last release.

### Checks

- Treat a passing scan as one signal, not a full privacy review.
- Confirm static public-source examples remain covered by the security, case-study, source-attribution, and non-advice docs.

### Commands

```bash
python scripts/privacy_scan.py
```

## 4. Check The Public Skill Path

Confirm the public agent skill path exists and references current package behavior.

### Checks

- Expected public skill path: `skills/agent/earnings-call-risk-map/SKILL.md`.
- If the skill was edited, re-run smoke checks and the privacy scan before tagging.

### Commands

```bash
test -f skills/agent/earnings-call-risk-map/SKILL.md
PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown
```

## 5. Create And Push The Tag

Create an annotated tag only after the repository state is the intended public release state.

### Checks

- If the version changes, update the tag name and release-note path consistently before running this checklist.

### Commands

```bash
git status --short
git tag -a v0.9.7 -m "v0.9.7"
git push origin v0.9.7
```

## 6. Create The GitHub Release

Create the GitHub release from the pushed tag.

### Checks

- Confirm the release page links back to public docs.
- Confirm the release notes preserve the educational research review boundary.
- Do not attach private or locally generated scratch artifacts.
- Do not upload package-index artifacts unless the separate distribution owner has approved that step.

### Commands

```bash
gh release create v0.9.7 \
  --title "v0.9.7" \
  --notes-file docs/release-notes-v0.9.7.md
```

## 7. Post-Publish Smoke

After GitHub shows the release, verify the public release and run a tagged-clone smoke path.

### Checks

- Open the release page and verify the tag, title, and notes render correctly.
- Check that README docs, release notes, preview assets, and public skill path links resolve in GitHub.
- Record any exceptions in the release notes or a follow-up issue before announcing the release.

### Commands

```bash
PYTHONPATH=src python -m earnings_call_risk_map version
PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output
PYTHONPATH=src python scripts/selfcheck.py
python scripts/privacy_scan.py
```
