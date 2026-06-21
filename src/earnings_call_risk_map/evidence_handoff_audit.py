"""Evidence handoff audit report generation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

SCHEMA_LABEL = "earnings-call-risk-map.evidence-handoff-audit.v1"

BOUNDARIES = (
    "static/local-source only",
    "no live data",
    "no broker connection",
    "no personalized investment advice",
    "no legal advice",
    "no accounting advice",
    "no tax advice",
    "no buy advice",
    "no sell advice",
    "no hold advice",
)

EXPECTED_ARTIFACTS: tuple[tuple[str, str], ...] = (
    ("README.md", "documentation"),
    ("docs/usage.md", "documentation"),
    ("docs/source-attribution-guide.md", "source_boundary_documentation"),
    ("docs/security-and-privacy.md", "source_boundary_documentation"),
    ("docs/non-advice-boundary.md", "source_boundary_documentation"),
    ("docs/reviewer-evidence.md", "reviewer_handoff_documentation"),
    ("docs/case-study-limitations.md", "freshness_documentation"),
    ("examples/output/demo_report.md", "generated_report"),
    ("examples/output/demo_review_queue.md", "generated_review_queue"),
    ("examples/output/demo_review_queue_items.jsonl", "generated_review_queue"),
    ("examples/output/demo_compare.md", "generated_compare"),
    ("examples/output/demo_dashboard.html", "generated_dashboard"),
    ("examples/output/handoff_packet.md", "generated_handoff_packet"),
    ("examples/output/source_boundary_evidence.md", "generated_source_boundary_evidence"),
    ("examples/output/visual_evidence_receipt.md", "generated_visual_evidence"),
    ("examples/output/package_audit.md", "generated_local_only_audit"),
    ("reports/maturity/maturity_evidence.md", "release_evidence"),
)
INPUT_GLOB = "examples/input/*.json"
OUTPUT_GLOB = "examples/output/*"
SELF_OUTPUTS = {
    "examples/output/evidence_handoff_audit.json",
    "examples/output/evidence_handoff_audit.md",
}
SELF_REFERENTIAL_OUTPUTS = {
    "examples/output/release_manifest.json",
}

REGENERATION_COMMANDS = (
    "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
    "PYTHONPATH=src python -m earnings_call_risk_map evidence-handoff-audit --root . --format markdown --output examples/output/evidence_handoff_audit.md",
    "PYTHONPATH=src python -m earnings_call_risk_map evidence-handoff-audit --root . --format json --output examples/output/evidence_handoff_audit.json",
    "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
)


def build_evidence_handoff_audit(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root).resolve()
    catalog = _artifact_catalog(base)
    artifacts = [_artifact_entry(base, path, role) for path, role in catalog]
    missing = [entry["relative_path"] for entry in artifacts if not entry["present"]]
    present_count = len(artifacts) - len(missing)
    source_fixture_count = sum(1 for entry in artifacts if entry["role"] == "source_fixture" and entry["present"])
    output_artifact_count = sum(1 for entry in artifacts if entry["role"].startswith("generated_") and entry["present"])
    readiness_status = "ready_with_review" if not missing else "needs_artifact_regeneration"
    return {
        "schema": SCHEMA_LABEL,
        "package": "earnings-call-risk-map",
        "version": __version__,
        "root": "<redacted-root>",
        "summary": {
            "checked_artifact_count": len(artifacts),
            "present_artifact_count": present_count,
            "missing_artifact_count": len(missing),
            "source_fixture_count": source_fixture_count,
            "generated_output_count": output_artifact_count,
            "readiness_status": readiness_status,
        },
        "checked_artifacts": artifacts,
        "source_notes": [
            "Audit uses local repository files only and records metadata, not artifact contents.",
            "Source fixtures are user-authored or static public-source examples; reviewers must verify source URLs and filings/transcripts before relying on them.",
            "Generated reports preserve source-boundary labels for management claims, analyst questions, and user synthesis.",
        ],
        "freshness_notes": [
            "The audit does not fetch live market data, current filings, current transcripts, quotes, prices, or broker data.",
            "Freshness readiness depends on each fixture's as_of, data_cutoff, item dates, stale badges, and reviewer source checks.",
            "Regenerate demo artifacts after changing fixtures, scoring, rendering, docs, or release evidence.",
        ],
        "review_readiness_notes": [
            "Ready means handoff artifacts are present and hashable; it does not mean source evidence has been independently verified.",
            "Reviewers should inspect missing-evidence and stale-data queues before using reports in any downstream research workflow.",
            "Use the generated handoff packet and source-boundary evidence together so downstream owners see cautions and provenance.",
        ],
        "missing_evidence_items": missing,
        "recommended_evidence_items": _recommended_evidence_items(missing),
        "regeneration_commands": list(REGENERATION_COMMANDS),
        "boundaries": list(BOUNDARIES),
        "safety_notice": SAFETY_NOTICE,
    }


def evidence_handoff_audit_json(root: str | Path = ".") -> str:
    return json.dumps(build_evidence_handoff_audit(root), indent=2, sort_keys=True) + "\n"


def evidence_handoff_audit_markdown(root: str | Path = ".") -> str:
    return render_evidence_handoff_audit_markdown(build_evidence_handoff_audit(root))


def render_evidence_handoff_audit_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Evidence Handoff Audit",
        "",
        f"- Schema: `{report['schema']}`",
        f"- Package: `{report['package']}`",
        f"- Version: `{report['version']}`",
        f"- Root: `{report['root']}`",
        f"- Checked artifacts: {summary['checked_artifact_count']}",
        f"- Present artifacts: {summary['present_artifact_count']}",
        f"- Missing artifacts: {summary['missing_artifact_count']}",
        f"- Source fixtures: {summary['source_fixture_count']}",
        f"- Generated outputs: {summary['generated_output_count']}",
        f"- Readiness: `{summary['readiness_status']}`",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Boundaries",
        "",
    ]
    lines.extend(f"- {_escape_markdown_text(boundary)}" for boundary in report["boundaries"])
    lines.extend(["", "## Checked Artifacts", ""])
    lines.append("| Relative path | Role | Present | Bytes | SHA-256 |")
    lines.append("| --- | --- | --- | ---: | --- |")
    for entry in report["checked_artifacts"]:
        lines.append(
            "| {path} | {role} | {present} | {bytes} | {sha} |".format(
                path=_escape_table_cell(entry["relative_path"]),
                role=_escape_table_cell(entry["role"]),
                present="yes" if entry["present"] else "no",
                bytes=entry["bytes"] if entry["bytes"] is not None else "",
                sha=_escape_table_cell(entry["sha256"] or ""),
            )
        )
    lines.extend(["", "## Source Notes", ""])
    lines.extend(f"- {_escape_markdown_text(note)}" for note in report["source_notes"])
    lines.extend(["", "## Freshness Notes", ""])
    lines.extend(f"- {_escape_markdown_text(note)}" for note in report["freshness_notes"])
    lines.extend(["", "## Review Readiness Notes", ""])
    lines.extend(f"- {_escape_markdown_text(note)}" for note in report["review_readiness_notes"])
    lines.extend(["", "## Missing Evidence Items", ""])
    if report["missing_evidence_items"]:
        lines.extend(f"- `{item}`" for item in report["missing_evidence_items"])
    else:
        lines.append("- None")
    lines.extend(["", "## Recommended Evidence Items", ""])
    lines.extend(f"- {_escape_markdown_text(item)}" for item in report["recommended_evidence_items"])
    lines.extend(["", "## Regeneration Commands", ""])
    lines.extend(f"- `{command}`" for command in report["regeneration_commands"])
    return "\n".join(lines) + "\n"


def cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="evidence-handoff-audit",
        description="Audit local evidence handoff artifacts without reading live data or embedding file contents.",
    )
    parser.add_argument("--root", default=".", metavar="DIR", help="Repository root to inspect")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    parser.add_argument("--output", metavar="PATH", help="Write report to this path")
    args = parser.parse_args(argv)
    payload = evidence_handoff_audit_json(args.root)
    if args.format == "markdown":
        payload = evidence_handoff_audit_markdown(args.root)
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


def _artifact_catalog(base: Path) -> list[tuple[str, str]]:
    artifacts: dict[str, str] = dict(EXPECTED_ARTIFACTS)
    for path in sorted(base.glob(INPUT_GLOB)):
        if path.is_file():
            artifacts[path.relative_to(base).as_posix()] = "source_fixture"
    for path in sorted(base.glob(OUTPUT_GLOB)):
        relative = path.relative_to(base).as_posix()
        if path.is_file() and relative not in SELF_OUTPUTS and relative not in SELF_REFERENTIAL_OUTPUTS:
            artifacts.setdefault(relative, _role_for_output(relative))
    return sorted(artifacts.items(), key=lambda item: item[0])


def _artifact_entry(base: Path, relative_path: str, role: str) -> dict[str, Any]:
    path = base / relative_path
    if not path.is_file():
        return {
            "relative_path": relative_path,
            "role": role,
            "present": False,
            "bytes": None,
            "sha256": None,
        }
    data = path.read_bytes()
    return {
        "relative_path": relative_path,
        "role": role,
        "present": True,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _role_for_output(relative_path: str) -> str:
    suffix = Path(relative_path).suffix
    name = Path(relative_path).name
    if "review_queue" in name:
        return "generated_review_queue"
    if "dashboard" in name or suffix == ".html":
        return "generated_dashboard"
    if "compare" in name:
        return "generated_compare"
    if "handoff" in name:
        return "generated_handoff_packet"
    if "audit" in name or "doctor" in name:
        return "generated_local_only_audit"
    if suffix == ".json":
        return "generated_json"
    if suffix == ".md":
        return "generated_markdown"
    return "generated_artifact"


def _recommended_evidence_items(missing: list[str]) -> list[str]:
    items = [
        "Confirm source URLs, source names, publishers, and accessed_at dates before public handoff.",
        "Confirm stale/static badges are acceptable or regenerate fixtures from current source documents.",
        "Keep screenshot or visual evidence receipts paired with static HTML dashboards.",
        "Keep review queue and handoff packet artifacts beside the main Markdown report.",
    ]
    if missing:
        items.insert(0, "Regenerate or intentionally remove missing checked artifacts before reviewer handoff.")
    return items


def _escape_table_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def _escape_markdown_text(value: str) -> str:
    return value.replace("\n", " ")
