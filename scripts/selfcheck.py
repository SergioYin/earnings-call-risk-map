#!/usr/bin/env python3
"""Run the local MVP verification suite."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = {"PYTHONPATH": str(ROOT / "src")}


def run(label: str, command: list[str]) -> int:
    print(f"== {label} ==", flush=True)
    result = subprocess.run(command, cwd=ROOT, env=ENV, text=True)
    if result.returncode != 0:
        print(f"{label} failed with exit code {result.returncode}")
    return result.returncode


def check_demo_dashboard() -> int:
    print("== demo dashboard ==", flush=True)
    path = ROOT / "examples/output/demo_dashboard.html"
    if not path.is_file():
        print(f"{path.relative_to(ROOT)} is missing")
        return 1
    text = path.read_text(encoding="utf-8")
    required = ("<!doctype html>", "Review Queue", "Stale Badges", "Catalysts")
    missing = [value for value in required if value not in text]
    forbidden = ("<script", "<link")
    blocked = [value for value in forbidden if value in text.lower()]
    if missing or blocked:
        if missing:
            print("missing dashboard marker(s): " + ", ".join(missing))
        if blocked:
            print("external asset marker(s) found: " + ", ".join(blocked))
        return 1
    print("demo dashboard passed")
    return 0


def check_showcase_previews() -> int:
    print("== showcase previews ==", flush=True)
    paths = [
        ROOT / "examples/output/demo_dashboard.html",
        ROOT / "examples/output/energy_infrastructure_dashboard.html",
        ROOT / "examples/output/public_apple_static_case_study_dashboard.html",
        ROOT / "examples/output/showcase_dashboard_preview.svg",
        ROOT / "docs/assets/showcase-dashboard-preview.svg",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in paths if not path.is_file()]
    if missing:
        print("missing preview file(s): " + ", ".join(missing))
        return 1

    blocked_markers = ("<script", "<link", "<img", " src=", "xlink:href=", "url(http://", "url(https://")
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        blocked = [marker for marker in blocked_markers if marker in text]
        if blocked:
            rel = path.relative_to(ROOT).as_posix()
            print(f"{rel} contains external asset marker(s): " + ", ".join(blocked))
            return 1
    print("showcase previews passed")
    return 0


def check_integration_examples() -> int:
    print("== integration examples ==", flush=True)
    docs = [
        ROOT / "docs/integrations.md",
        ROOT / "docs/gallery.md",
    ]
    missing_docs = [path.relative_to(ROOT).as_posix() for path in docs if not path.is_file()]
    if missing_docs:
        print("missing integration doc(s): " + ", ".join(missing_docs))
        return 1

    path = ROOT / "examples/output/integration_notes.json"
    if not path.is_file():
        print(f"{path.relative_to(ROOT)} is missing")
        return 1
    payload = json.loads(path.read_text(encoding="utf-8"))
    notes = payload.get("notes", [])
    integrations = {note.get("integration") for note in notes}
    required = {"thesis_ledger", "portfolio_risk_review"}
    if payload.get("source_tool") != "earnings-call-risk-map" or not required.issubset(integrations):
        print("integration notes missing required source_tool or integration labels")
        return 1
    for note in notes:
        if not note.get("source_artifact") or not note.get("source_notice"):
            print("integration note missing source artifact or safety notice")
            return 1
    print("integration examples passed")
    return 0


def main() -> int:
    checks = [
        ("unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests"]),
        ("demo", [sys.executable, "-m", "earnings_call_risk_map", "demo", "--out-dir", "examples/output"]),
        ("audit", [sys.executable, "-m", "earnings_call_risk_map", "audit"]),
        ("manifest", [sys.executable, "-m", "earnings_call_risk_map", "manifest", "--out", "release_manifest.json"]),
        ("privacy scan", [sys.executable, "scripts/privacy_scan.py"]),
        ("maturity evidence", [sys.executable, "-m", "earnings_call_risk_map", "maturity-evidence", "--out-dir", "reports/maturity"]),
    ]
    for label, command in checks:
        code = run(label, command)
        if code:
            return code
        if label == "demo":
            code = check_demo_dashboard()
            if code:
                return code
            code = check_showcase_previews()
            if code:
                return code
            code = check_integration_examples()
            if code:
                return code
    print("selfcheck passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
