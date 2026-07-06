"""Release owner handoff rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

RELEASE_OWNER_CHECKLIST: tuple[dict[str, Any], ...] = (
    {
        "number": 1,
        "slug": "confirm-release-metadata",
        "title": "Confirm Release Metadata",
        "summary": "Confirm all release metadata agrees on the current package version.",
        "checks": [
            (
                f"Confirm `README.md`, `CHANGELOG.md`, `pyproject.toml`, "
                f"`src/earnings_call_risk_map/version.py`, and `docs/release-notes-v{__version__}.md` "
                f"all identify `{__version__}`."
            ),
        ],
    },
    {
        "number": 2,
        "slug": "inspect-worktree",
        "title": "Inspect Worktree",
        "summary": "Confirm every modified or untracked file belongs in the release.",
        "checks": ["Run `git status --short` and review every path before tagging."],
    },
    {
        "number": 3,
        "slug": "rerun-verification",
        "title": "Rerun Verification",
        "summary": "Rerun the full verification command set after any release-facing change.",
        "checks": [
            "Rerun verification after release metadata, documentation, fixture, generated artifact, or promotion-copy changes.",
        ],
    },
    {
        "number": 4,
        "slug": "review-evidence-bundle",
        "title": "Review Evidence Bundle",
        "summary": "Review generated maturity evidence and final review records.",
        "checks": [
            "Review `reports/maturity/maturity_evidence.md` and `reports/maturity/maturity_evidence.json`.",
            "Review `examples/output/release_owner_compare_blockers.md` before accepting evidence handoff changes.",
            "Review the final internal maturity review, promotion gate review, and reviewer feedback summary.",
        ],
    },
    {
        "number": 5,
        "slug": "confirm-owner-controlled-gates",
        "title": "Confirm Owner-Controlled Gates",
        "summary": "Keep package publishing, hosted demo deployment, tagging, and announcements owner-controlled.",
        "checks": [
            "Complete the wheel build dry run only if package publishing is in scope.",
            "Verify the Pages demo locally only if a hosted demo is in scope.",
            f"Create the annotated tag only after the release owner accepts the worktree and evidence set: `git tag -a v{__version__} -m \"v{__version__}\"`.",
            (
                "Create the GitHub release only after the tag has been pushed and release notes have been reviewed: "
                f"`gh release create v{__version__} --title \"v{__version__}\" --notes-file docs/release-notes-v{__version__}.md`."
            ),
        ],
    },
    {
        "number": 6,
        "slug": "review-public-boundaries",
        "title": "Review Public Boundaries",
        "summary": "Confirm public copy preserves the educational, local-only, static-data boundary.",
        "checks": [
            "Review public copy against `docs/non-advice-boundary.md`, `docs/case-study-limitations.md`, and `docs/security-and-privacy.md`.",
            (
                "Do not claim live market data, investment recommendations, buy, sell, or hold conclusions, "
                "portfolio suitability, valuation conclusions, price targets, source verification, or current analysis from stale/static fixtures."
            ),
        ],
    },
)

VERIFICATION_COMMANDS: tuple[str, ...] = (
    "PYTHONPATH=src python -m earnings_call_risk_map version",
    "PYTHONPATH=src python -m unittest discover -s tests",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "PYTHONPATH=src python -m earnings_call_risk_map audit --format json",
    "PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json",
    "PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format json",
    "PYTHONPATH=src python -m earnings_call_risk_map release-owner-compare-blockers --compare examples/output/evidence_handoff_compare.json --format json",
    "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
    "python scripts/privacy_scan.py",
    "git diff --check",
)

EXPECTED_RESULTS: tuple[str, ...] = (
    f"`PYTHONPATH=src python -m earnings_call_risk_map version` prints exactly `{__version__}`.",
    "`PYTHONPATH=src python -m unittest discover -s tests` ends with `OK`.",
    "`PYTHONPATH=src python scripts/selfcheck.py` ends with `selfcheck passed`.",
    "`PYTHONPATH=src python -m earnings_call_risk_map audit --format json` reports local-only checks as passed.",
    "`PYTHONPATH=src python -m earnings_call_risk_map release-assets --format json` reports `missing_count` as `0`.",
    "`PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format json` reports fixture paths, source boundaries, no-live-data, and no-advice checks.",
    "`PYTHONPATH=src python -m earnings_call_risk_map release-owner-compare-blockers --compare examples/output/evidence_handoff_compare.json --format json` reports blocker and review-required counts from the evidence handoff compare artifact.",
    "`PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity` refreshes the maturity evidence bundle.",
    "`python scripts/privacy_scan.py` prints `privacy scan passed`.",
    "`git diff --check` exits with no whitespace findings.",
)

PACKAGE_DRY_RUN_COMMANDS: tuple[str, ...] = (
    "python -m pip install --upgrade build",
    "rm -rf dist-dry-run",
    "python -m build --wheel --outdir dist-dry-run",
    "python -m zipfile --list dist-dry-run/*.whl",
    "python -m pip install --force-reinstall --no-deps dist-dry-run/*.whl",
    "earnings-call-risk-map version",
)

PROMOTION_EVIDENCE_PATHS: tuple[str, ...] = (
    f"docs/release-notes-v{__version__}.md",
    "docs/release-readiness.md",
    "docs/reviewer-evidence.md",
    "docs/reviewer-feedback-consumption.md",
    "docs/publication-checklist.md",
    "docs/distribution.md",
    "docs/promotion-page-outline.md",
    "docs/demo-screenshot-guide.md",
    "docs/pages-demo.md",
    "docs/security-and-privacy.md",
    "docs/non-advice-boundary.md",
    "docs/source-attribution-guide.md",
    "docs/case-study-limitations.md",
    "docs/known-limitations.md",
    "reports/reviews/2026-06-18-v0.9.0-final-review.md",
    "reports/reviews/2026-06-18-v0.9.0-promotion-review.md",
    "reports/reviews/2026-06-18-v0.9.0-internal-review.md",
    "reports/reviews/reviewer_feedback_consumption.json",
    "reports/maturity/maturity_evidence.md",
    "reports/maturity/maturity_evidence.json",
    "examples/output/promotion_pack.md",
    "examples/output/promotion_pack.json",
    "examples/output/release_manifest.json",
    "release_manifest.json",
    "examples/output/package_audit.md",
    "examples/output/package_audit.json",
    "examples/output/doctor.md",
    "examples/output/doctor.json",
    "examples/output/source_boundary_evidence.md",
    "examples/output/source_boundary_evidence.json",
    "examples/output/release_owner_compare_blockers.md",
    "examples/output/release_owner_compare_blockers.json",
    "docs/assets/showcase-dashboard-preview.svg",
    "examples/output/showcase_dashboard_preview.svg",
    "docs/demo-index.html",
    "examples/output/public_apple_static_case_study_dashboard.html",
    "examples/output/public_apple_static_case_study_report.md",
    "examples/output/public_apple_static_case_study_review_queue.md",
    "examples/output/handoff_packet.md",
    "examples/output/handoff_packet.json",
    "skills/agent/earnings-call-risk-map/SKILL.md",
)


def build_release_owner_handoff() -> dict[str, Any]:
    return {
        "artifact_type": "release_owner_handoff",
        "name": "earnings-call-risk-map",
        "version": __version__,
        "source_doc": "docs/release-owner-handoff.md",
        "owner_scope": "final release owner handoff before tagging, publishing, or promoting public artifacts",
        "safety_notice": SAFETY_NOTICE,
        "checklist": [dict(item) for item in RELEASE_OWNER_CHECKLIST],
        "check_count": len(RELEASE_OWNER_CHECKLIST),
        "verification_commands": list(VERIFICATION_COMMANDS),
        "expected_results": list(EXPECTED_RESULTS),
        "package_dry_run_commands": list(PACKAGE_DRY_RUN_COMMANDS),
        "package_dry_run_condition": "Run only if package publishing is in scope.",
        "promotion_evidence_paths": list(PROMOTION_EVIDENCE_PATHS),
        "owner_controlled_promotion_gate": (
            "The evidence supports owner handoff and small-scope public promotion after release owner approval; "
            "it does not itself perform or approve tag creation, pushing, package-index publication, "
            "hosted demo deployment, or broad public announcement."
        ),
    }


def release_owner_handoff_json() -> str:
    return json.dumps(build_release_owner_handoff(), indent=2, sort_keys=True) + "\n"


def release_owner_handoff_markdown() -> str:
    return render_release_owner_handoff_markdown(build_release_owner_handoff())


def render_release_owner_handoff_markdown(handoff: dict[str, Any]) -> str:
    lines = [
        "# Release Owner Handoff",
        "",
        f"- Package: `{handoff['name']}`",
        f"- Version: `{handoff['version']}`",
        f"- Source doc: `{handoff['source_doc']}`",
        f"- Owner scope: {handoff['owner_scope']}",
        "",
        f"> {handoff['safety_notice']}",
        "",
        "## Final Release Owner Checklist",
        "",
        f"Final v{'.'.join(str(handoff['version']).split('.')[:2])} Release Owner Checklist.",
        "",
    ]
    for item in handoff["checklist"]:
        lines.extend([f"### {item['number']}. {item['title']}", "", item["summary"], ""])
        if item["slug"] == "confirm-release-metadata":
            lines.extend([f"Confirm release metadata agrees on `{handoff['version']}`.", ""])
        lines.extend(f"- {check}" for check in item["checks"])
        lines.append("")

    lines.extend(["## Exact Verification Commands", "", "```bash"])
    lines.extend(handoff["verification_commands"])
    lines.extend(["```", "", "## Expected Results", ""])
    lines.extend(f"- {result}" for result in handoff["expected_results"])
    lines.extend(["", "## Package Dry Run", "", handoff["package_dry_run_condition"], "", "```bash"])
    lines.extend(handoff["package_dry_run_commands"])
    lines.extend(["```", "", f"Expected package dry-run version output: `{handoff['version']}`.", ""])
    lines.extend(["## Promotion Evidence Paths", ""])
    lines.extend(f"- `{path}`" for path in handoff["promotion_evidence_paths"])
    lines.extend(["", "## Owner-Controlled Promotion Gates", "", handoff["owner_controlled_promotion_gate"], ""])
    return "\n".join(lines)
