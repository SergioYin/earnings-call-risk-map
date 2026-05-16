#!/usr/bin/env python3
"""Run the local MVP verification suite."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = {"PYTHONPATH": str(ROOT / "src")}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)]+)\)")
DOC_LINK_CHECK_PATHS = (
    Path("README.md"),
    Path("docs/distribution.md"),
    Path("docs/non-advice-boundary.md"),
    Path("docs/release-readiness.md"),
    Path("docs/reviewer-evidence.md"),
    Path("docs/release-notes-v0.4.0.md"),
)


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


def check_compare_examples() -> int:
    print("== compare examples ==", flush=True)
    json_path = ROOT / "examples/output/demo_compare.json"
    md_path = ROOT / "examples/output/demo_compare.md"
    prior_path = ROOT / "examples/output/demo_prior_snapshot.json"
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in (json_path, md_path, prior_path)
        if not path.is_file()
    ]
    if missing:
        print("missing compare artifact(s): " + ", ".join(missing))
        return 1

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    if payload.get("before_as_of") != "2026-02-15" or payload.get("after_as_of") != "2026-05-15":
        print("compare artifact has unexpected before/after dates")
        return 1
    if not payload.get("interpretation"):
        print("compare artifact missing interpretation")
        return 1
    risk_topics = {item.get("topic") for item in payload.get("risk_changes", [])}
    opportunity_topics = {item.get("topic") for item in payload.get("opportunity_changes", [])}
    if "gross margin" not in risk_topics or "product launch" not in opportunity_topics:
        print("compare artifact missing expected demo score movement")
        return 1

    markdown = md_path.read_text(encoding="utf-8")
    required = ("Snapshot Compare", "How To Read This Compare", "Risk Changes", "Opportunity Changes")
    missing_markers = [marker for marker in required if marker not in markdown]
    if missing_markers:
        print("compare markdown missing marker(s): " + ", ".join(missing_markers))
        return 1
    print("compare examples passed")
    return 0


def check_docs_links() -> int:
    print("== docs links ==", flush=True)
    failures = []
    for relative_path in DOC_LINK_CHECK_PATHS:
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"{relative_path.as_posix()} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or _is_external_or_anchor(target):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                failures.append(f"{relative_path.as_posix()} links outside repo: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{relative_path.as_posix()} has missing link target: {target}")
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("docs links passed")
    return 0


def _is_external_or_anchor(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("mailto:")
        or lowered.startswith("#")
    )


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
            code = check_compare_examples()
            if code:
                return code
            code = check_docs_links()
            if code:
                return code
    print("selfcheck passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
