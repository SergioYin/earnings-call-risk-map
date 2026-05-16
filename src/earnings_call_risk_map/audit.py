"""Package audit report generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

COMMANDS = ("analyze", "audit", "compare", "demo", "manifest", "maturity-evidence", "review-queue", "version")
FIXTURE_PATTERN = "examples/input/*.json"
OUTPUT_DIR = "examples/output"
AUDIT_OUTPUTS = {
    "examples/output/package_audit.json",
    "examples/output/package_audit.md",
}
SKILL_PATH = "skills/agent/earnings-call-risk-map/SKILL.md"
WORKFLOW_DIR = ".github/workflows"


def build_package_audit(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    fixtures = _relative_files(base, FIXTURE_PATTERN)
    output_artifacts = [
        path
        for path in _relative_files(base, f"{OUTPUT_DIR}/*")
        if path not in AUDIT_OUTPUTS
    ]
    workflow_files = _relative_files(base, f"{WORKFLOW_DIR}/*")
    skill_path = base / SKILL_PATH
    return {
        "name": "earnings-call-risk-map",
        "version": __version__,
        "commands": list(COMMANDS),
        "command_count": len(COMMANDS),
        "fixtures": fixtures,
        "fixture_count": len(fixtures),
        "output_artifacts": output_artifacts,
        "output_artifact_count": len(output_artifacts),
        "workflow_files": workflow_files,
        "has_workflow_files": bool(workflow_files),
        "skill": {
            "path": SKILL_PATH,
            "present": skill_path.is_file(),
        },
    }


def package_audit_json(root: str | Path = ".") -> str:
    return json.dumps(build_package_audit(root), indent=2, sort_keys=True) + "\n"


def render_package_audit_markdown(audit: dict[str, Any]) -> str:
    skill = audit["skill"]
    lines = [
        "# Package Audit",
        "",
        f"- Package: `{audit['name']}`",
        f"- Version: `{audit['version']}`",
        f"- Commands: {audit['command_count']} ({', '.join(f'`{command}`' for command in audit['commands'])})",
        f"- Fixtures: {audit['fixture_count']}",
        f"- Output artifacts: {audit['output_artifact_count']}",
        f"- Workflow files present: {'yes' if audit['has_workflow_files'] else 'no'}",
        f"- Skill present: {'yes' if skill['present'] else 'no'} (`{skill['path']}`)",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Fixtures",
        "",
    ]
    lines.extend(f"- `{path}`" for path in audit["fixtures"])
    lines.extend(["", "## Output Artifacts", ""])
    lines.extend(f"- `{path}`" for path in audit["output_artifacts"])
    lines.extend(["", "## Workflow Files", ""])
    if audit["workflow_files"]:
        lines.extend(f"- `{path}`" for path in audit["workflow_files"])
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def package_audit_markdown(root: str | Path = ".") -> str:
    return render_package_audit_markdown(build_package_audit(root))


def _relative_files(base: Path, pattern: str) -> list[str]:
    return sorted(
        path.relative_to(base).as_posix()
        for path in base.glob(pattern)
        if path.is_file()
    )
