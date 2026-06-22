"""Release-to-release evidence handoff audit comparison."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .evidence_handoff_audit import BOUNDARIES, _escape_markdown_text, _escape_table_cell
from .models import SAFETY_NOTICE
from .version import __version__

SCHEMA_LABEL = "earnings-call-risk-map.evidence-handoff-compare.v1"

COMPARE_FIELDS = (
    "present",
    "bytes",
    "sha256",
    "role",
    "freshness_status",
    "freshness_note",
    "freshness",
    "boundary_status",
    "boundary_note",
    "source_boundary",
    "source_boundary_note",
)


def build_evidence_handoff_compare(before_path: str | Path, after_path: str | Path) -> dict[str, Any]:
    before = _read_audit(before_path, "before")
    after = _read_audit(after_path, "after")
    before_entries = _index_entries(before, "before")
    after_entries = _index_entries(after, "after")
    before_keys = set(before_entries)
    after_keys = set(after_entries)

    added = [_entry_summary(key, after_entries[key]) for key in sorted(after_keys - before_keys)]
    removed = [_entry_summary(key, before_entries[key]) for key in sorted(before_keys - after_keys)]
    changed = []
    unchanged = []
    for key in sorted(before_keys & after_keys):
        differences = _entry_differences(before_entries[key], after_entries[key])
        if differences:
            changed.append(
                {
                    "key": key,
                    "relative_path": after_entries[key].get("relative_path") or before_entries[key].get("relative_path"),
                    "evidence_id": after_entries[key].get("evidence_id") or before_entries[key].get("evidence_id"),
                    "differences": differences,
                }
            )
        else:
            unchanged.append(_entry_summary(key, after_entries[key]))

    boundary_comparison = _compare_boundaries(before.get("boundaries", []), after.get("boundaries", []))
    return {
        "schema": SCHEMA_LABEL,
        "package": "earnings-call-risk-map",
        "version": __version__,
        "inputs": {
            "before": _safe_input_label(before_path),
            "after": _safe_input_label(after_path),
        },
        "source_schemas": {
            "before": before.get("schema"),
            "after": after.get("schema"),
        },
        "summary": {
            "before_entry_count": len(before_entries),
            "after_entry_count": len(after_entries),
            "added_count": len(added),
            "removed_count": len(removed),
            "changed_count": len(changed),
            "unchanged_count": len(unchanged),
            "boundary_changed": bool(boundary_comparison["added"] or boundary_comparison["removed"]),
            "safety_notice_changed": before.get("safety_notice") != after.get("safety_notice"),
        },
        "added": added,
        "removed": removed,
        "changed": changed,
        "unchanged": unchanged,
        "boundary_comparison": boundary_comparison,
        "comparison_notes": [
            "Stable keys prefer evidence_id when present and otherwise use relative_path.",
            "Changed entries list metadata differences only; artifact contents are not embedded.",
            "Byte, SHA-256, presence, role, freshness, and source-boundary fields are compared when available.",
        ],
        "boundaries": list(BOUNDARIES),
        "safety_notice": SAFETY_NOTICE,
    }


def evidence_handoff_compare_json(before_path: str | Path, after_path: str | Path) -> str:
    return json.dumps(build_evidence_handoff_compare(before_path, after_path), indent=2, sort_keys=True) + "\n"


def evidence_handoff_compare_markdown(before_path: str | Path, after_path: str | Path) -> str:
    return render_evidence_handoff_compare_markdown(build_evidence_handoff_compare(before_path, after_path))


def render_evidence_handoff_compare_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Evidence Handoff Compare",
        "",
        f"- Schema: `{report['schema']}`",
        f"- Package: `{report['package']}`",
        f"- Version: `{report['version']}`",
        f"- Before: `{report['inputs']['before']}`",
        f"- After: `{report['inputs']['after']}`",
        f"- Added: {summary['added_count']}",
        f"- Removed: {summary['removed_count']}",
        f"- Changed: {summary['changed_count']}",
        f"- Unchanged: {summary['unchanged_count']}",
        f"- Boundary changed: {'yes' if summary['boundary_changed'] else 'no'}",
        f"- Safety notice changed: {'yes' if summary['safety_notice_changed'] else 'no'}",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Boundaries",
        "",
    ]
    lines.extend(f"- {_escape_markdown_text(boundary)}" for boundary in report["boundaries"])
    lines.extend(["", "## Changed Entries", ""])
    if report["changed"]:
        lines.append("| Key | Relative path | Differences |")
        lines.append("| --- | --- | --- |")
        for entry in report["changed"]:
            fields = ", ".join(_escape_markdown_text(item["field"]) for item in entry["differences"])
            lines.append(
                "| {key} | {path} | {fields} |".format(
                    key=_escape_table_cell(entry["key"]),
                    path=_escape_table_cell(entry.get("relative_path") or ""),
                    fields=_escape_table_cell(fields),
                )
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Added Entries", ""])
    _append_summary_table(lines, report["added"])
    lines.extend(["", "## Removed Entries", ""])
    _append_summary_table(lines, report["removed"])
    lines.extend(["", "## Boundary Comparison", ""])
    lines.append(f"- Added boundaries: {_list_or_none(report['boundary_comparison']['added'])}")
    lines.append(f"- Removed boundaries: {_list_or_none(report['boundary_comparison']['removed'])}")
    lines.append(f"- Unchanged boundaries: {len(report['boundary_comparison']['unchanged'])}")
    lines.extend(["", "## Comparison Notes", ""])
    lines.extend(f"- {_escape_markdown_text(note)}" for note in report["comparison_notes"])
    return "\n".join(lines) + "\n"


def cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="evidence-handoff-compare",
        description="Compare two local evidence handoff audit JSON files without live data or artifact contents.",
    )
    parser.add_argument("--before", required=True, metavar="PATH", help="Earlier evidence handoff audit JSON")
    parser.add_argument("--after", required=True, metavar="PATH", help="Later evidence handoff audit JSON")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    parser.add_argument("--output", metavar="PATH", help="Write comparison report to this path")
    args = parser.parse_args(argv)
    try:
        payload = (
            evidence_handoff_compare_json(args.before, args.after)
            if args.format == "json"
            else evidence_handoff_compare_markdown(args.before, args.after)
        )
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


def _read_audit(path: str | Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"{label} audit JSON could not be read: {_safe_input_label(path)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} audit JSON is invalid at line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} audit JSON must be an object")
    if not isinstance(payload.get("checked_artifacts"), list):
        raise ValueError(f"{label} audit JSON must contain a checked_artifacts list")
    return payload


def _index_entries(audit: dict[str, Any], label: str) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for index, raw_entry in enumerate(audit.get("checked_artifacts", []), start=1):
        if not isinstance(raw_entry, dict):
            raise ValueError(f"{label} checked_artifacts item {index} must be an object")
        key = raw_entry.get("evidence_id") or raw_entry.get("relative_path")
        if not isinstance(key, str) or not key:
            raise ValueError(f"{label} checked_artifacts item {index} needs evidence_id or relative_path")
        if key in entries:
            raise ValueError(f"{label} checked_artifacts contains duplicate stable key: {key}")
        entries[key] = raw_entry
    return entries


def _entry_differences(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    differences = []
    for field in COMPARE_FIELDS:
        before_value = before.get(field)
        after_value = after.get(field)
        if before_value != after_value:
            differences.append({"field": field, "before": before_value, "after": after_value})
    return differences


def _entry_summary(key: str, entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": key,
        "relative_path": entry.get("relative_path"),
        "evidence_id": entry.get("evidence_id"),
        "role": entry.get("role"),
        "present": entry.get("present"),
        "bytes": entry.get("bytes"),
        "sha256": entry.get("sha256"),
    }


def _compare_boundaries(before: Any, after: Any) -> dict[str, list[str]]:
    before_set = {item for item in before if isinstance(item, str)} if isinstance(before, list) else set()
    after_set = {item for item in after if isinstance(item, str)} if isinstance(after, list) else set()
    return {
        "added": sorted(after_set - before_set),
        "removed": sorted(before_set - after_set),
        "unchanged": sorted(before_set & after_set),
    }


def _safe_input_label(path: str | Path) -> str:
    candidate = Path(path)
    value = candidate.as_posix()
    marker = "examples/"
    if marker in value:
        return value[value.index(marker) :]
    if not candidate.is_absolute() and ".." not in candidate.parts:
        return value
    try:
        return candidate.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except (OSError, ValueError):
        return candidate.name


def _append_summary_table(lines: list[str], entries: list[dict[str, Any]]) -> None:
    if not entries:
        lines.append("- None")
        return
    lines.append("| Key | Relative path | Role | Present | Bytes |")
    lines.append("| --- | --- | --- | --- | ---: |")
    for entry in entries:
        lines.append(
            "| {key} | {path} | {role} | {present} | {bytes} |".format(
                key=_escape_table_cell(entry["key"]),
                path=_escape_table_cell(entry.get("relative_path") or ""),
                role=_escape_table_cell(entry.get("role") or ""),
                present="yes" if entry.get("present") else "no",
                bytes=entry.get("bytes") if entry.get("bytes") is not None else "",
            )
        )


def _list_or_none(values: list[str]) -> str:
    if not values:
        return "None"
    return ", ".join(f"`{_escape_markdown_text(value)}`" for value in values)


if __name__ == "__main__":
    raise SystemExit(cli_main())
