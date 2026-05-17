"""Deterministic release notes summary rendering."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .audit import build_package_audit
from .models import SAFETY_NOTICE
from .release_assets import build_release_asset_checklist
from .version import __version__


def build_release_notes_summary(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    audit = build_package_audit(base)
    release_assets = build_release_asset_checklist(base)
    changelog_excerpt = extract_current_changelog_excerpt(base / "CHANGELOG.md", __version__)
    return {
        "artifact_type": "release_notes_summary",
        "name": audit["name"],
        "version": __version__,
        "audit": audit,
        "release_assets": release_assets,
        "changelog_excerpt": changelog_excerpt,
        "safety_notice": SAFETY_NOTICE,
    }


def render_release_notes_summary_markdown(summary: dict[str, Any]) -> str:
    audit = summary["audit"]
    release_assets = summary["release_assets"]
    lines = [
        "# Release Notes Summary",
        "",
        f"- Package: `{summary['name']}`",
        f"- Version: `{summary['version']}`",
        f"- Audit commands: {audit['command_count']}",
        f"- Audit fixtures: {audit['fixture_count']}",
        f"- Audit output artifacts: {audit['output_artifact_count']}",
        f"- Local-only audit: {audit['local_only']['status']}",
        f"- Release assets: `{release_assets['status']}` "
        f"({release_assets['present_count']}/{release_assets['expected_count']} present)",
        f"- Missing release assets: {release_assets['missing_count']}",
        "",
        f"> {summary['safety_notice']}",
        "",
        "## Package Audit",
        "",
        f"- Commands: {', '.join(f'`{command}`' for command in audit['commands'])}",
        f"- Workflow files present: {'yes' if audit['has_workflow_files'] else 'no'}",
        f"- Skill present: {'yes' if audit['skill']['present'] else 'no'} (`{audit['skill']['path']}`)",
        f"- Network access required: {'yes' if audit['local_only']['network_required'] else 'no'}",
        f"- Credentials required: {'yes' if audit['local_only']['credentials_required'] else 'no'}",
        "",
        "## Release Assets",
        "",
        f"- Status: `{release_assets['status']}`",
        f"- Expected: {release_assets['expected_count']}",
        f"- Present: {release_assets['present_count']}",
        f"- Missing: {release_assets['missing_count']}",
        "",
        "### Missing Assets",
        "",
    ]
    if release_assets["missing_assets"]:
        lines.extend(f"- `{path}`" for path in release_assets["missing_assets"])
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Changelog Excerpt",
            "",
            summary["changelog_excerpt"].rstrip(),
        ]
    )
    return "\n".join(lines) + "\n"


def release_notes_summary_markdown(root: str | Path = ".") -> str:
    return render_release_notes_summary_markdown(build_release_notes_summary(root))


def extract_current_changelog_excerpt(path: str | Path, version: str) -> str:
    changelog = Path(path)
    if not changelog.is_file():
        raise ValueError(f"{changelog} is missing")
    lines = changelog.read_text(encoding="utf-8").splitlines()
    target_prefix = f"## {version} "
    start = next(
        (index for index, line in enumerate(lines) if line == f"## {version}" or line.startswith(target_prefix)),
        None,
    )
    if start is None:
        raise ValueError(f"{changelog} does not contain a {version} changelog section")
    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[start:end]).rstrip() + "\n"
