"""Release owner blocker checklist from evidence handoff comparison artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .evidence_handoff_audit import BOUNDARIES, _escape_markdown_text, _escape_table_cell
from .evidence_handoff_compare import _safe_input_label
from .models import SAFETY_NOTICE
from .version import __version__

SCHEMA_LABEL = "earnings-call-risk-map.release-owner-compare-blockers.v1"

SOURCE_AND_FRESHNESS_FIELDS = {
    "freshness",
    "freshness_note",
    "freshness_status",
    "boundary_note",
    "boundary_status",
    "source_boundary",
    "source_boundary_note",
}
HASH_OR_SIZE_FIELDS = {"bytes", "sha256"}


def build_release_owner_compare_blockers(compare_path: str | Path) -> dict[str, Any]:
    compare = _read_compare(compare_path)
    compare_summary = compare.get("summary", {})
    changed_entries = _object_list(compare.get("changed", []), "changed")
    added_entries = _object_list(compare.get("added", []), "added")
    removed_entries = _object_list(compare.get("removed", []), "removed")
    boundary_comparison = compare.get("boundary_comparison", {})
    if not isinstance(boundary_comparison, dict):
        boundary_comparison = {}

    checks = [
        _check(
            "no-removed-evidence-artifacts",
            "No evidence handoff artifacts were removed.",
            "blocker" if removed_entries else "clear",
            removed_entries,
            "Restore the artifact, regenerate the handoff bundle, or record owner acceptance before release.",
        ),
        _check(
            "no-artifacts-became-missing",
            "No previously present evidence artifact became missing.",
            "blocker" if _entries_with_field_after(changed_entries, "present", False) else "clear",
            _entries_with_field_after(changed_entries, "present", False),
            "Regenerate missing artifacts before release or explicitly remove them from the release evidence set.",
        ),
        _check(
            "release-boundaries-preserved",
            "No existing local-only, no-live-data, no-private-data, or non-advice boundary was removed.",
            "blocker" if boundary_comparison.get("removed") else "clear",
            [{"key": value, "relative_path": ""} for value in _string_list(boundary_comparison.get("removed", []))],
            "Do not release until removed boundary language is restored or the release owner accepts the changed boundary.",
        ),
        _check(
            "safety-notice-preserved",
            "The safety notice did not change between evidence handoff audits.",
            "blocker" if compare_summary.get("safety_notice_changed") else "clear",
            [{"key": "safety_notice", "relative_path": ""}] if compare_summary.get("safety_notice_changed") else [],
            "Review safety notice text against the non-advice boundary before release.",
        ),
        _check(
            "added-artifacts-reviewed",
            "Added evidence artifacts are reviewed for public-source, local-only, and non-advice boundaries.",
            "review_required" if added_entries else "clear",
            added_entries,
            "Inspect added artifacts for source scope, stale/static labeling, and release-owner relevance.",
        ),
        _check(
            "content-hash-or-size-changes-reviewed",
            "Changed byte counts or SHA-256 hashes are explained by intentional generated artifact or documentation updates.",
            "review_required" if _entries_with_any_field(changed_entries, HASH_OR_SIZE_FIELDS) else "clear",
            _entries_with_any_field(changed_entries, HASH_OR_SIZE_FIELDS),
            "Review the changed artifact diff or regeneration command before release.",
        ),
        _check(
            "role-changes-reviewed",
            "Evidence role changes are intentional and do not hide release evidence.",
            "review_required" if _entries_with_any_field(changed_entries, {"role"}) else "clear",
            _entries_with_any_field(changed_entries, {"role"}),
            "Confirm role changes still route artifacts to the right reviewer handoff bucket.",
        ),
        _check(
            "source-and-freshness-changes-reviewed",
            "Freshness and source-boundary metadata changes are reviewed before release.",
            "review_required" if _entries_with_any_field(changed_entries, SOURCE_AND_FRESHNESS_FIELDS) else "clear",
            _entries_with_any_field(changed_entries, SOURCE_AND_FRESHNESS_FIELDS),
            "Review source-boundary and freshness notes; do not treat stale/static artifacts as current analysis.",
        ),
        _check(
            "added-boundaries-reviewed",
            "New boundary language is reviewed for consistency across public docs and generated artifacts.",
            "review_required" if boundary_comparison.get("added") else "clear",
            [{"key": value, "relative_path": ""} for value in _string_list(boundary_comparison.get("added", []))],
            "Confirm added boundary text is consistent with public docs and generated evidence.",
        ),
    ]
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    review_required_count = sum(1 for check in checks if check["status"] == "review_required")
    release_decision = "blocked" if blocker_count else "review_required" if review_required_count else "clear"
    return {
        "schema": SCHEMA_LABEL,
        "package": "earnings-call-risk-map",
        "version": __version__,
        "inputs": {
            "compare": _safe_input_label(compare_path),
        },
        "source_schema": compare.get("schema"),
        "source_inputs": compare.get("inputs", {}),
        "summary": {
            "release_decision": release_decision,
            "blocker_count": blocker_count,
            "review_required_count": review_required_count,
            "clear_count": sum(1 for check in checks if check["status"] == "clear"),
            "compare_added_count": compare_summary.get("added_count", 0),
            "compare_removed_count": compare_summary.get("removed_count", 0),
            "compare_changed_count": compare_summary.get("changed_count", 0),
            "compare_unchanged_count": compare_summary.get("unchanged_count", 0),
        },
        "checklist": checks,
        "release_owner_notes": [
            "This checklist summarizes metadata from evidence handoff compare artifacts; it does not embed artifact contents.",
            "A clear checklist does not approve tagging, publishing, hosted demo deployment, or public announcement.",
            "The release owner must review changed evidence, stale/static labels, and source boundaries before relying on the handoff.",
        ],
        "boundaries": list(BOUNDARIES),
        "safety_notice": SAFETY_NOTICE,
    }


def release_owner_compare_blockers_json(compare_path: str | Path) -> str:
    return json.dumps(build_release_owner_compare_blockers(compare_path), indent=2, sort_keys=True) + "\n"


def release_owner_compare_blockers_markdown(compare_path: str | Path) -> str:
    return render_release_owner_compare_blockers_markdown(build_release_owner_compare_blockers(compare_path))


def render_release_owner_compare_blockers_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Release Owner Compare Blocker Checklist",
        "",
        f"- Schema: `{report['schema']}`",
        f"- Package: `{report['package']}`",
        f"- Version: `{report['version']}`",
        f"- Compare input: `{report['inputs']['compare']}`",
        f"- Release decision: `{summary['release_decision']}`",
        f"- Blockers: {summary['blocker_count']}",
        f"- Review-required checks: {summary['review_required_count']}",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Checklist",
        "",
        "| Gate | Status | Evidence | Release-owner action |",
        "| --- | --- | --- | --- |",
    ]
    for check in report["checklist"]:
        lines.append(
            "| {gate} | `{status}` | {evidence} | {action} |".format(
                gate=_escape_table_cell(check["title"]),
                status=check["status"],
                evidence=_escape_table_cell(_evidence_label(check["evidence"])),
                action=_escape_table_cell(check["reviewer_action"]),
            )
        )
    lines.extend(["", "## Source Compare Summary", ""])
    lines.append(f"- Added artifacts: {summary['compare_added_count']}")
    lines.append(f"- Removed artifacts: {summary['compare_removed_count']}")
    lines.append(f"- Changed artifacts: {summary['compare_changed_count']}")
    lines.append(f"- Unchanged artifacts: {summary['compare_unchanged_count']}")
    lines.extend(["", "## Release Owner Notes", ""])
    lines.extend(f"- {_escape_markdown_text(note)}" for note in report["release_owner_notes"])
    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {_escape_markdown_text(boundary)}" for boundary in report["boundaries"])
    return "\n".join(lines) + "\n"


def cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="release-owner-compare-blockers",
        description="Render a release-owner blocker checklist from a local evidence handoff compare JSON file.",
    )
    parser.add_argument("--compare", required=True, metavar="PATH", help="Evidence handoff compare JSON")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    parser.add_argument("--output", metavar="PATH", help="Write release-owner blocker checklist to this path")
    args = parser.parse_args(argv)
    try:
        payload = (
            release_owner_compare_blockers_json(args.compare)
            if args.format == "json"
            else release_owner_compare_blockers_markdown(args.compare)
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


def _read_compare(path: str | Path) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"compare JSON could not be read: {_safe_input_label(path)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"compare JSON is invalid at line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(payload, dict):
        raise ValueError("compare JSON must be an object")
    if not isinstance(payload.get("summary"), dict):
        raise ValueError("compare JSON must contain a summary object")
    return payload


def _object_list(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"compare JSON {label} must be a list")
    items = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"compare JSON {label} item {index} must be an object")
        items.append(item)
    return items


def _string_list(value: Any) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _check(
    slug: str,
    title: str,
    status: str,
    evidence: list[dict[str, Any]],
    reviewer_action: str,
) -> dict[str, Any]:
    return {
        "slug": slug,
        "title": title,
        "status": status,
        "blocking": status == "blocker",
        "evidence_count": len(evidence),
        "evidence": [_evidence_entry(item) for item in evidence],
        "reviewer_action": reviewer_action,
    }


def _evidence_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "key": entry.get("key") or entry.get("evidence_id") or entry.get("relative_path") or "",
        "relative_path": entry.get("relative_path") or "",
    }


def _entries_with_any_field(entries: list[dict[str, Any]], fields: set[str]) -> list[dict[str, Any]]:
    return [
        entry
        for entry in entries
        if any(difference.get("field") in fields for difference in _object_list(entry.get("differences", []), "differences"))
    ]


def _entries_with_field_after(entries: list[dict[str, Any]], field: str, after: Any) -> list[dict[str, Any]]:
    return [
        entry
        for entry in entries
        if any(
            difference.get("field") == field and difference.get("after") == after
            for difference in _object_list(entry.get("differences", []), "differences")
        )
    ]


def _evidence_label(entries: list[dict[str, Any]]) -> str:
    if not entries:
        return "None"
    labels = []
    for entry in entries[:5]:
        key = entry.get("key") or entry.get("relative_path") or ""
        path = entry.get("relative_path") or ""
        labels.append(f"{key} ({path})" if path and path != key else str(key))
    if len(entries) > 5:
        labels.append(f"+{len(entries) - 5} more")
    return ", ".join(labels)


if __name__ == "__main__":
    raise SystemExit(cli_main())
