"""Maturity evidence bundle generation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

TEST_COMMANDS = (
    "PYTHONPATH=src python -m unittest discover -s tests",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "python scripts/privacy_scan.py",
)
VERIFICATION_COMMANDS = (
    "PYTHONPATH=src python -m unittest discover -s tests",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
    "PYTHONPATH=src python -m earnings_call_risk_map audit",
    "PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json",
    "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
    "python scripts/privacy_scan.py",
    "git diff --check",
)
FRESH_CLONE_COMMANDS = (
    "git clone <repo-url> earnings-call-risk-map",
    "cd earnings-call-risk-map",
    "python -m venv .venv",
    "source .venv/bin/activate",
    "python -m pip install --upgrade pip",
    "PYTHONPATH=src python -m earnings_call_risk_map version",
    "PYTHONPATH=src python -m unittest discover -s tests",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "python -m pip install .",
    "earnings-call-risk-map version",
)
ARTIFACT_GLOBS = (
    "examples/output/*.json",
    "examples/output/*.md",
    "examples/output/*.html",
    "examples/output/*.svg",
    "docs/assets/*.svg",
    "release_manifest.json",
)
SKILL_PATH = "skills/agent/earnings-call-risk-map/SKILL.md"
REVIEW_TEMPLATE_PATH = "reports/reviews/release-readiness-review.md"
RELEASE_ASSETS = (
    "README.md",
    "CHANGELOG.md",
    "docs/release-notes-v0.4.0.md",
    "docs/release-readiness.md",
    "docs/reviewer-evidence.md",
    "docs/distribution.md",
    "docs/non-advice-boundary.md",
    "docs/pages-demo.md",
    "docs/gallery.md",
    "docs/public-case-study.md",
    "docs/schema-reference.json",
    "docs/assets/showcase-dashboard-preview.svg",
    "examples/output/demo_dashboard.html",
    "examples/output/energy_infrastructure_dashboard.html",
    "examples/output/public_apple_static_case_study_dashboard.html",
    "examples/output/showcase_dashboard_preview.svg",
    "examples/output/demo_report.md",
    "examples/output/energy_infrastructure_report.md",
    "examples/output/public_apple_static_case_study_report.md",
    "examples/output/demo_review_queue.md",
    "examples/output/energy_infrastructure_review_queue.md",
    "examples/output/public_apple_static_case_study_review_queue.md",
    "examples/output/demo_snapshot.json",
    "examples/output/demo_prior_snapshot.json",
    "examples/output/energy_infrastructure_snapshot.json",
    "examples/output/public_apple_static_case_study_snapshot.json",
    "examples/output/demo_compare.md",
    "examples/output/demo_compare.json",
    "examples/output/package_audit.md",
    "examples/output/package_audit.json",
    "examples/output/release_manifest.json",
    "release_manifest.json",
    "reports/maturity/maturity_evidence.md",
    "reports/maturity/maturity_evidence.json",
    SKILL_PATH,
    REVIEW_TEMPLATE_PATH,
)
MATURITY_SCORES = {
    "source": "reports/reviews/2026-05-17-v0.3.0-internal-review.md",
    "review_date": "2026-05-17",
    "overall": "89/100",
    "level": "L3 -> target L4",
    "release_gate": "PASS",
    "promotion_gate": "PASS small-scope",
    "categories": {
        "product_clarity": "14/15",
        "reproducibility": "14/15",
        "user_value": "18/20",
        "evidence_quality": "15/15",
        "engineering_quality": "13/15",
        "showcase": "8/10",
        "risk_boundary": "7/10",
    },
    "four_role_review": {
        "product": "4/5 accept",
        "engineering": "4/5 accept",
        "cold_user": "4/5 accept",
        "risk": "4/5 accept",
    },
}


def build_maturity_evidence(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    return {
        "name": "earnings-call-risk-map",
        "version": __version__,
        "test_commands": list(TEST_COMMANDS),
        "verification_commands": list(VERIFICATION_COMMANDS),
        "fresh_clone_commands": list(FRESH_CLONE_COMMANDS),
        "artifact_paths": _artifact_paths(base),
        "release_assets": _existing_paths(base, RELEASE_ASSETS),
        "maturity_scores": MATURITY_SCORES,
        "skill": {
            "path": SKILL_PATH,
            "present": (base / SKILL_PATH).is_file(),
        },
        "review_template": {
            "path": REVIEW_TEMPLATE_PATH,
            "present": (base / REVIEW_TEMPLATE_PATH).is_file(),
        },
        "privacy_scan": _privacy_scan_status(base),
    }


def write_maturity_evidence(out_dir: str | Path, root: str | Path = ".") -> dict[str, Path]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    evidence = build_maturity_evidence(root)
    json_path = target / "maturity_evidence.json"
    md_path = target / "maturity_evidence.md"
    json_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_maturity_evidence_markdown(evidence), encoding="utf-8")
    return {"json": json_path, "markdown": md_path}


def render_maturity_evidence_markdown(evidence: dict[str, Any]) -> str:
    privacy = evidence["privacy_scan"]
    skill = evidence["skill"]
    template = evidence["review_template"]
    lines = [
        "# Maturity Evidence Bundle",
        "",
        f"- Package: `{evidence['name']}`",
        f"- Version: `{evidence['version']}`",
        f"- Skill path: `{skill['path']}` ({'present' if skill['present'] else 'missing'})",
        f"- Review template: `{template['path']}` ({'present' if template['present'] else 'missing'})",
        f"- Privacy scan: {privacy['status']} (`{privacy['command']}`)",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Test Commands",
        "",
    ]
    lines.extend(f"- `{command}`" for command in evidence["test_commands"])
    lines.extend(["", "## Verification Commands", ""])
    lines.extend(f"- `{command}`" for command in evidence["verification_commands"])
    lines.extend(["", "## Fresh Clone Procedure", ""])
    lines.extend(f"{index}. `{command}`" for index, command in enumerate(evidence["fresh_clone_commands"], start=1))
    lines.extend(["", "## Maturity Scores", ""])
    scores = evidence["maturity_scores"]
    lines.extend(
        [
            f"- Source: `{scores['source']}`",
            f"- Review date: `{scores['review_date']}`",
            f"- Overall: `{scores['overall']}`",
            f"- Level: `{scores['level']}`",
            f"- Release gate: `{scores['release_gate']}`",
            f"- Promotion gate: `{scores['promotion_gate']}`",
        ]
    )
    lines.extend(["", "### Scorecard", ""])
    lines.extend(f"- {name.replace('_', ' ').title()}: `{score}`" for name, score in scores["categories"].items())
    lines.extend(["", "### Four-Role Review", ""])
    lines.extend(f"- {name.replace('_', ' ').title()}: `{score}`" for name, score in scores["four_role_review"].items())
    lines.extend(["", "## Release Assets", ""])
    if evidence["release_assets"]:
        lines.extend(f"- `{path}`" for path in evidence["release_assets"])
    else:
        lines.append("- None")
    lines.extend(["", "## Artifact Paths", ""])
    if evidence["artifact_paths"]:
        lines.extend(f"- `{path}`" for path in evidence["artifact_paths"])
    else:
        lines.append("- None")
    lines.extend(["", "## Privacy Scan", ""])
    lines.append(f"- Exit code: `{privacy['exit_code']}`")
    if privacy["stdout"]:
        lines.append(f"- Output: `{privacy['stdout']}`")
    if privacy["stderr"]:
        lines.append(f"- Error: `{privacy['stderr']}`")
    return "\n".join(lines) + "\n"


def maturity_evidence_json(root: str | Path = ".") -> str:
    return json.dumps(build_maturity_evidence(root), indent=2, sort_keys=True) + "\n"


def _artifact_paths(base: Path) -> list[str]:
    paths = set()
    for pattern in ARTIFACT_GLOBS:
        for path in base.glob(pattern):
            if path.is_file():
                paths.add(path.relative_to(base).as_posix())
    return sorted(paths)


def _existing_paths(base: Path, paths: tuple[str, ...]) -> list[str]:
    return [path for path in paths if (base / path).is_file()]


def _privacy_scan_status(base: Path) -> dict[str, Any]:
    command = [sys.executable, "scripts/privacy_scan.py"]
    script = base / "scripts/privacy_scan.py"
    if not script.is_file():
        return {
            "command": "python scripts/privacy_scan.py",
            "status": "missing",
            "exit_code": None,
            "stdout": "",
            "stderr": "scripts/privacy_scan.py is missing",
        }
    result = subprocess.run(command, cwd=base, text=True, capture_output=True, check=False)
    stdout = " ".join(result.stdout.split())
    stderr = " ".join(result.stderr.split())
    return {
        "command": "python scripts/privacy_scan.py",
        "status": "passed" if result.returncode == 0 else "failed",
        "exit_code": result.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
