"""Release asset checklist report generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .maturity import RELEASE_ASSETS
from .version import __version__


def expected_release_assets() -> tuple[str, ...]:
    versioned_notes = f"docs/release-notes-v{__version__}.md"
    return tuple(
        versioned_notes if path == "docs/release-notes-v0.9.3.md" else path
        for path in RELEASE_ASSETS
    )


def build_release_asset_checklist(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    expected = expected_release_assets()
    present = [path for path in expected if (base / path).is_file()]
    missing = [path for path in expected if not (base / path).is_file()]
    return {
        "name": "earnings-call-risk-map",
        "version": __version__,
        "status": "passed" if not missing else "failed",
        "expected_count": len(expected),
        "present_count": len(present),
        "missing_count": len(missing),
        "expected_assets": list(expected),
        "present_assets": present,
        "missing_assets": missing,
    }


def release_asset_checklist_json(root: str | Path = ".") -> str:
    return json.dumps(build_release_asset_checklist(root), indent=2, sort_keys=True) + "\n"


def release_asset_checklist_markdown(root: str | Path = ".") -> str:
    return render_release_asset_checklist_markdown(build_release_asset_checklist(root))


def render_release_asset_checklist_markdown(checklist: dict[str, Any]) -> str:
    lines = [
        "# Release Asset Checklist",
        "",
        f"- Package: `{checklist['name']}`",
        f"- Version: `{checklist['version']}`",
        f"- Status: `{checklist['status']}`",
        f"- Expected assets: {checklist['expected_count']}",
        f"- Present assets: {checklist['present_count']}",
        f"- Missing assets: {checklist['missing_count']}",
        "",
        "## Assets",
        "",
    ]
    missing = set(checklist["missing_assets"])
    for path in checklist["expected_assets"]:
        marker = " " if path in missing else "x"
        lines.append(f"- [{marker}] `{path}`")
    if checklist["missing_assets"]:
        lines.extend(["", "## Missing Assets", ""])
        lines.extend(f"- `{path}`" for path in checklist["missing_assets"])
    return "\n".join(lines) + "\n"
