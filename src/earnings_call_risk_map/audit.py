"""Package audit report generation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

COMMANDS = (
    "agent-workflow",
    "analyze",
    "audit",
    "case-study-map",
    "cheat-sheet",
    "compare",
    "data-entry-checklist",
    "demo",
    "demo-screenshot-guide",
    "doctor",
    "evidence-handoff-audit",
    "evidence-handoff-compare",
    "examples-index",
    "fixture-catalog",
    "fixture-summary",
    "fresh-clone-plan",
    "handoff-packet",
    "manifest",
    "maturity-evidence",
    "playbooks",
    "promotion-pack",
    "publication-checklist",
    "release-owner-handoff",
    "release-assets",
    "release-notes",
    "review-queue",
    "review-queue-jsonl",
    "risk-taxonomy",
    "schema-authoring-reference",
    "schema-reference",
    "source-boundary-evidence",
    "template-catalog",
    "version",
    "visual-evidence-receipt",
)
FIXTURE_PATTERN = "examples/input/*.json"
OUTPUT_DIR = "examples/output"
AUDIT_OUTPUTS = {
    "examples/output/package_audit.json",
    "examples/output/package_audit.md",
}
SKILL_PATH = "skills/agent/earnings-call-risk-map/SKILL.md"
WORKFLOW_DIR = ".github/workflows"
LOCAL_COMMAND_SCOPE = "All CLI commands read local JSON/text inputs and write local Markdown, JSON, JSONL, HTML, or manifest files only."
NETWORK_IMPORT_RE = re.compile(
    r"^\s*(?:import|from)\s+"
    r"(?:requests|httpx|urllib|urllib3|socket|http\.client|ftplib|smtplib|imaplib|poplib|websocket)\b",
    re.MULTILINE,
)
CREDENTIAL_ENV_RE = re.compile(
    r"\b(?:os\.environ|os\.getenv)\s*(?:\.get|\[|\().*(?:API|TOKEN|SECRET|KEY|PASSWORD|CREDENTIAL)",
    re.IGNORECASE,
)
LOCAL_AUDIT_SOURCE_PATTERNS = (
    "src/earnings_call_risk_map/*.py",
    "scripts/*.py",
)


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
        "local_only": _local_only_audit(base),
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
        f"- Local-only audit: {audit['local_only']['status']}",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Local-Only No-Network Guarantee",
        "",
        f"- Network access required: {'yes' if audit['local_only']['network_required'] else 'no'}",
        f"- Credentials required: {'yes' if audit['local_only']['credentials_required'] else 'no'}",
        f"- External services required: {', '.join(audit['local_only']['external_services']) or 'none'}",
        f"- Command scope: {audit['local_only']['command_scope']}",
        "",
        "### Local-Only Checks",
        "",
    ]
    lines.extend(
        f"- {check['name']}: {check['status']} - {check['detail']}"
        for check in audit["local_only"]["checks"]
    )
    lines.extend(["", "### Command Credential And Network Requirements", ""])
    lines.extend(
        "- `{command}`: network required `{network}`, credentials required `{credentials}`".format(
            command=command["name"],
            network=str(command["network_required"]).lower(),
            credentials=str(command["credentials_required"]).lower(),
        )
        for command in audit["local_only"]["commands"]
    )
    lines.extend(
        [
            "",
            "## Fixtures",
            "",
        ]
    )
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


def _local_only_audit(base: Path) -> dict[str, Any]:
    checks = [
        _runtime_dependency_check(base),
        _network_import_check(base),
        _credential_environment_check(base),
        {
            "name": "workflow_files_absent",
            "status": "passed" if not _relative_files(base, f"{WORKFLOW_DIR}/*") else "failed",
            "detail": "no GitHub workflow files are required for package commands",
        },
    ]
    status = "passed" if all(check["status"] == "passed" for check in checks) else "failed"
    return {
        "status": status,
        "network_required": False,
        "credentials_required": False,
        "external_services": [],
        "command_scope": LOCAL_COMMAND_SCOPE,
        "commands": [
            {
                "name": command,
                "network_required": False,
                "credentials_required": False,
            }
            for command in COMMANDS
        ],
        "checks": checks,
    }


def _runtime_dependency_check(base: Path) -> dict[str, str]:
    pyproject = base / "pyproject.toml"
    if not pyproject.is_file():
        return {
            "name": "runtime_dependencies_empty",
            "status": "failed",
            "detail": "pyproject.toml is missing",
        }
    text = pyproject.read_text(encoding="utf-8")
    status = "passed" if "dependencies = []" in text else "failed"
    detail = "project declares no runtime package dependencies" if status == "passed" else "project dependencies are not empty"
    return {"name": "runtime_dependencies_empty", "status": status, "detail": detail}


def _network_import_check(base: Path) -> dict[str, str]:
    findings = []
    for path in _local_audit_sources(base):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if NETWORK_IMPORT_RE.search(text):
            findings.append(path.relative_to(base).as_posix())
    status = "passed" if not findings else "failed"
    detail = (
        "no network-client imports found in package or local scripts"
        if status == "passed"
        else "network-client imports found in " + ", ".join(findings)
    )
    return {"name": "no_network_client_imports", "status": status, "detail": detail}


def _credential_environment_check(base: Path) -> dict[str, str]:
    findings = []
    for path in _local_audit_sources(base):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if CREDENTIAL_ENV_RE.search(text):
            findings.append(path.relative_to(base).as_posix())
    status = "passed" if not findings else "failed"
    detail = (
        "no credential environment variable reads found in package or local scripts"
        if status == "passed"
        else "credential environment variable reads found in " + ", ".join(findings)
    )
    return {"name": "no_credential_environment_reads", "status": status, "detail": detail}


def _local_audit_sources(base: Path) -> list[Path]:
    paths: set[Path] = set()
    for pattern in LOCAL_AUDIT_SOURCE_PATTERNS:
        paths.update(path for path in base.glob(pattern) if path.is_file())
    return sorted(paths)
