"""Publication owner checklist rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

PUBLICATION_OWNER_STEPS: tuple[dict[str, Any], ...] = (
    {
        "number": 1,
        "slug": "confirm-release-candidate",
        "title": "Confirm The Release Candidate",
        "summary": "Confirm version alignment, fresh generated artifacts, and unresolved reviewer notes.",
        "checks": [
            (
                "Confirm `README.md`, `CHANGELOG.md`, `pyproject.toml`, "
                "`src/earnings_call_risk_map/version.py`, and the current release notes agree on the version."
            ),
            "Confirm generated artifacts are fresh.",
            (
                "Review `docs/reviewer-evidence.md`, `reports/maturity/maturity_evidence.md`, "
                "and `reports/reviews/release-readiness-review.md` for unresolved reviewer notes."
            ),
        ],
        "commands": [
            "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
            "PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json",
            "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
        ],
    },
    {
        "number": 2,
        "slug": "run-smoke-checks",
        "title": "Run Smoke Checks",
        "summary": "Run the public smoke path from a clean checkout or clean working tree.",
        "checks": [
            "Run the unit tests, selfcheck, package audit, and release asset checklist.",
            (
                "Open `docs/demo-index.html`, `examples/output/demo_dashboard.html`, "
                "and `examples/output/showcase_dashboard_preview.svg`."
            ),
        ],
        "commands": [
            "PYTHONPATH=src python -m unittest discover -s tests",
            "PYTHONPATH=src python scripts/selfcheck.py",
            "PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown",
            "PYTHONPATH=src python -m earnings_call_risk_map release-assets --format markdown",
        ],
    },
    {
        "number": 3,
        "slug": "run-privacy-scan",
        "title": "Run Privacy Scan",
        "summary": "Run the privacy scan and manually review public fixtures or generated examples touched since the last release.",
        "checks": [
            "Treat a passing scan as one signal, not a full privacy review.",
            (
                "Confirm static public-source examples remain covered by the security, case-study, "
                "source-attribution, and non-advice docs."
            ),
        ],
        "commands": ["python scripts/privacy_scan.py"],
    },
    {
        "number": 4,
        "slug": "check-public-skill-path",
        "title": "Check The Public Skill Path",
        "summary": "Confirm the public agent skill path exists and references current package behavior.",
        "checks": [
            "Expected public skill path: `skills/agent/earnings-call-risk-map/SKILL.md`.",
            "If the skill was edited, re-run smoke checks and the privacy scan before tagging.",
        ],
        "commands": [
            "test -f skills/agent/earnings-call-risk-map/SKILL.md",
            "PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown",
        ],
    },
    {
        "number": 5,
        "slug": "create-and-push-tag",
        "title": "Create And Push The Tag",
        "summary": "Create an annotated tag only after the repository state is the intended public release state.",
        "checks": [
            "If the version changes, update the tag name and release-note path consistently before running this checklist.",
        ],
        "commands": [
            "git status --short",
            f'git tag -a v{__version__} -m "v{__version__}"',
            f"git push origin v{__version__}",
        ],
    },
    {
        "number": 6,
        "slug": "create-github-release",
        "title": "Create The GitHub Release",
        "summary": "Create the GitHub release from the pushed tag.",
        "checks": [
            "Confirm the release page links back to public docs.",
            "Confirm the release notes preserve the educational research review boundary.",
            "Do not attach private or locally generated scratch artifacts.",
            "Do not upload package-index artifacts unless the separate distribution owner has approved that step.",
        ],
        "commands": [
            (
                f"gh release create v{__version__} \\\n"
                f'  --title "v{__version__}" \\\n'
                f"  --notes-file docs/release-notes-v{__version__}.md"
            ),
        ],
    },
    {
        "number": 7,
        "slug": "post-publish-smoke",
        "title": "Post-Publish Smoke",
        "summary": "After GitHub shows the release, verify the public release and run a tagged-clone smoke path.",
        "checks": [
            "Open the release page and verify the tag, title, and notes render correctly.",
            "Check that README docs, release notes, preview assets, and public skill path links resolve in GitHub.",
            "Record any exceptions in the release notes or a follow-up issue before announcing the release.",
        ],
        "commands": [
            "PYTHONPATH=src python -m earnings_call_risk_map version",
            "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
            "PYTHONPATH=src python scripts/selfcheck.py",
            "python scripts/privacy_scan.py",
        ],
    },
)


def build_publication_checklist() -> dict[str, Any]:
    return {
        "artifact_type": "publication_checklist",
        "name": "earnings-call-risk-map",
        "version": __version__,
        "source_doc": "docs/publication-checklist.md",
        "owner_scope": "public GitHub release owner steps",
        "step_count": len(PUBLICATION_OWNER_STEPS),
        "safety_notice": SAFETY_NOTICE,
        "privacy_notice": (
            "Do not publish private fixtures, unreleased company information, account identifiers, "
            "secrets, or proprietary research notes."
        ),
        "steps": [dict(step) for step in PUBLICATION_OWNER_STEPS],
    }


def publication_checklist_json() -> str:
    return json.dumps(build_publication_checklist(), indent=2, sort_keys=True) + "\n"


def publication_checklist_markdown() -> str:
    return render_publication_checklist_markdown(build_publication_checklist())


def render_publication_checklist_markdown(checklist: dict[str, Any]) -> str:
    lines = [
        "# Publication Checklist",
        "",
        f"- Package: `{checklist['name']}`",
        f"- Version: `{checklist['version']}`",
        f"- Source doc: `{checklist['source_doc']}`",
        f"- Owner scope: {checklist['owner_scope']}",
        f"- Steps: {checklist['step_count']}",
        "",
        f"> {checklist['safety_notice']}",
        "",
        f"> {checklist['privacy_notice']}",
    ]
    for step in checklist["steps"]:
        lines.extend(
            [
                "",
                f"## {step['number']}. {step['title']}",
                "",
                step["summary"],
                "",
                "### Checks",
                "",
            ]
        )
        lines.extend(f"- {check}" for check in step["checks"])
        if step["commands"]:
            lines.extend(["", "### Commands", "", "```bash"])
            lines.extend(step["commands"])
            lines.append("```")
    return "\n".join(lines) + "\n"
