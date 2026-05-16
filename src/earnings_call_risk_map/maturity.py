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


def build_maturity_evidence(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    return {
        "name": "earnings-call-risk-map",
        "version": __version__,
        "test_commands": list(TEST_COMMANDS),
        "artifact_paths": _artifact_paths(base),
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
