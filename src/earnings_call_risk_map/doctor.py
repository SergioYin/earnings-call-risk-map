"""Deterministic package health report."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .audit import build_package_audit
from .models import SAFETY_NOTICE

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
DOC_LINK_CHECK_PATHS = (
    Path("README.md"),
    Path("examples/playbooks/README.md"),
    Path("examples/playbooks/quarterly-review.md"),
    Path("examples/playbooks/catalyst-check-in.md"),
    Path("examples/playbooks/post-earnings-thesis-refresh.md"),
    Path("docs/tutorial-earnings-review.md"),
    Path("docs/distribution.md"),
    Path("docs/non-advice-boundary.md"),
    Path("docs/comparison-to-spreadsheets.md"),
    Path("docs/decision-ledger-integration.md"),
    Path("docs/faq.md"),
    Path("docs/filled-template-workflow.md"),
    Path("docs/publication-checklist.md"),
    Path("docs/release-readiness.md"),
    Path("docs/reviewer-evidence.md"),
    Path("docs/release-notes-v0.9.0.md"),
    Path("docs/risk-language-taxonomy.md"),
    Path("docs/roadmap.md"),
    Path("docs/security-and-privacy.md"),
    Path("docs/source-attribution-guide.md"),
    Path("docs/templates.md"),
    Path("docs/troubleshooting.md"),
    Path("docs/usage.md"),
)
PRIVACY_SCAN_COMMAND_HINTS = (
    "python scripts/privacy_scan.py",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
)


def build_doctor_report(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    audit = build_package_audit(base)
    docs_links = _docs_link_report(base)
    workflow_files_absent = not audit["has_workflow_files"]
    status = (
        "passed"
        if audit["local_only"]["status"] == "passed" and workflow_files_absent and docs_links["status"] == "passed"
        else "failed"
    )
    return {
        "artifact_type": "doctor_report",
        "package": audit["name"],
        "version": audit["version"],
        "status": status,
        "package_health": {
            "local_only_status": audit["local_only"]["status"],
            "runtime_dependency_status": _check_status(audit, "runtime_dependencies_empty"),
            "network_import_status": _check_status(audit, "no_network_client_imports"),
            "credential_environment_status": _check_status(audit, "no_credential_environment_reads"),
        },
        "fixture_count": audit["fixture_count"],
        "output_artifact_count": audit["output_artifact_count"],
        "docs_links": docs_links,
        "workflow_files_absent": workflow_files_absent,
        "workflow_files": audit["workflow_files"],
        "privacy_scan_command_hints": list(PRIVACY_SCAN_COMMAND_HINTS),
        "safety_notice": SAFETY_NOTICE,
    }


def doctor_report_json(root: str | Path = ".") -> str:
    return json.dumps(build_doctor_report(root), indent=2, sort_keys=True) + "\n"


def render_doctor_report_markdown(report: dict[str, Any]) -> str:
    docs_links = report["docs_links"]
    lines = [
        "# Doctor Report",
        "",
        f"- Package: `{report['package']}`",
        f"- Version: `{report['version']}`",
        f"- Status: `{report['status']}`",
        f"- Local-only package health: `{report['package_health']['local_only_status']}`",
        f"- Fixture count: {report['fixture_count']}",
        f"- Output artifact count: {report['output_artifact_count']}",
        f"- Docs links: `{docs_links['status']}` ({docs_links['checked_link_count']} checked)",
        f"- Workflow files absent: {'yes' if report['workflow_files_absent'] else 'no'}",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Package Health",
        "",
    ]
    lines.extend(
        f"- {name.replace('_', ' ').title()}: `{status}`"
        for name, status in report["package_health"].items()
    )
    lines.extend(["", "## Docs Links", ""])
    lines.extend(
        [
            f"- Checked documents: {docs_links['checked_document_count']}",
            f"- Checked links: {docs_links['checked_link_count']}",
            f"- Failures: {docs_links['failure_count']}",
        ]
    )
    if docs_links["failures"]:
        lines.extend(f"- {failure}" for failure in docs_links["failures"])
    lines.extend(["", "## Workflow Files", ""])
    if report["workflow_files"]:
        lines.extend(f"- `{path}`" for path in report["workflow_files"])
    else:
        lines.append("- None")
    lines.extend(["", "## Privacy Scan Command Hints", ""])
    lines.extend(f"- `{command}`" for command in report["privacy_scan_command_hints"])
    return "\n".join(lines) + "\n"


def doctor_report_markdown(root: str | Path = ".") -> str:
    return render_doctor_report_markdown(build_doctor_report(root))


def _docs_link_report(base: Path) -> dict[str, Any]:
    failures = []
    checked_link_count = 0
    present_documents = 0
    for relative_path in DOC_LINK_CHECK_PATHS:
        path = base / relative_path
        if not path.is_file():
            failures.append(f"{relative_path.as_posix()} is missing")
            continue
        present_documents += 1
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or _is_external_or_anchor(target):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            checked_link_count += 1
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(base.resolve())
            except ValueError:
                failures.append(f"{relative_path.as_posix()} links outside repo: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{relative_path.as_posix()} has missing link target: {target}")
    return {
        "status": "passed" if not failures else "failed",
        "checked_document_count": present_documents,
        "expected_document_count": len(DOC_LINK_CHECK_PATHS),
        "checked_link_count": checked_link_count,
        "failure_count": len(failures),
        "failures": failures,
    }


def _check_status(audit: dict[str, Any], name: str) -> str:
    for check in audit["local_only"]["checks"]:
        if check["name"] == name:
            return check["status"]
    return "missing"


def _is_external_or_anchor(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
    )
