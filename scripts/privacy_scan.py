#!/usr/bin/env python3
"""Lightweight public-safety scan for repo text files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDE_SUFFIXES = {".py", ".md", ".json", ".toml", ".txt"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", "build", "dist", "*.egg-info"}
FORBIDDEN_PATTERNS = [
    re.compile("/" + r"home/[A-Za-z0-9_.-]+/"),
    re.compile(r"github-assets/runtime"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)private agent"),
]


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.relative_to(ROOT).as_posix() == "scripts/privacy_scan.py":
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix in INCLUDE_SUFFIXES or path.name in {"LICENSE"}:
            yield path


def main() -> int:
    findings = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(ROOT)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                findings.append(f"{rel}: matched {pattern.pattern}")
    if findings:
        print("privacy scan failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("privacy scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
