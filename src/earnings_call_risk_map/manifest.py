"""Release manifest generation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .version import __version__

DEFAULT_INCLUDE_DIRS = ("src", "tests", "scripts", "examples", "docs", "reports", "skills")
DEFAULT_INCLUDE_FILES = ("README.md", "LICENSE", "CHANGELOG.md", "pyproject.toml")
SELF_REFERENTIAL_MANIFESTS = {"release_manifest.json", "examples/output/release_manifest.json"}


def build_manifest(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    files = []
    for name in DEFAULT_INCLUDE_FILES:
        path = base / name
        if path.is_file():
            files.append(_file_entry(base, path))
    for dirname in DEFAULT_INCLUDE_DIRS:
        directory = base / dirname
        if directory.is_dir():
            for path in sorted(directory.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    files.append(_file_entry(base, path))
    return {
        "name": "earnings-call-risk-map",
        "version": __version__,
        "file_count": len(files),
        "files": sorted(files, key=lambda item: item["path"]),
    }


def manifest_json(root: str | Path = ".") -> str:
    return json.dumps(build_manifest(root), indent=2, sort_keys=True) + "\n"


def _file_entry(base: Path, path: Path) -> dict[str, Any]:
    relative_path = path.relative_to(base).as_posix()
    if relative_path in SELF_REFERENTIAL_MANIFESTS:
        return {
            "path": relative_path,
            "bytes": None,
            "sha256": "<self-referential-manifest>",
        }
    content = path.read_bytes()
    return {
        "path": relative_path,
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }
