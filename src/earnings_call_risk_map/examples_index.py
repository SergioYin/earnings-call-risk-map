"""Aggregate examples index rendering."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .fixture_catalog import build_fixture_catalog
from .io import read_json
from .models import SAFETY_NOTICE
from .template_catalog import build_template_catalog

OUTPUT_DIR = Path("examples/output")
RECOMMENDED_NEXT_COMMAND = "earnings-call-risk-map demo --out-dir examples/output"


def build_examples_index(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    fixtures = [
        _with_recommended_next_command(entry)
        for entry in _all_fixture_entries(base)
    ]
    template_catalog = build_template_catalog(base)
    templates = [
        _with_recommended_next_command(entry)
        for entry in template_catalog["templates"]
    ]
    generated_outputs = _generated_outputs(base)
    return {
        "schema_version": "0.1",
        "artifact_type": "examples_index",
        "safety_notice": SAFETY_NOTICE,
        "recommended_next_command": RECOMMENDED_NEXT_COMMAND,
        "summary": {
            "fixture_count": len(fixtures),
            "template_count": len(templates),
            "generated_output_count": len(generated_outputs),
        },
        "fixtures": fixtures,
        "templates": templates,
        "generated_outputs": generated_outputs,
    }


def examples_index_json(root: str | Path = ".") -> str:
    return json.dumps(build_examples_index(root), indent=2, sort_keys=True) + "\n"


def examples_index_markdown(root: str | Path = ".") -> str:
    return render_examples_index_markdown(build_examples_index(root))


def render_examples_index_markdown(index: dict[str, Any]) -> str:
    summary = index["summary"]
    lines = [
        "# Examples Index",
        "",
        "Bundled examples are local deterministic fixtures, templates, and generated artifacts.",
        "",
        f"> {index['safety_notice']}",
        "",
        "## Summary",
        "",
        f"- Fixtures: {summary['fixture_count']}",
        f"- Templates: {summary['template_count']}",
        f"- Generated outputs: {summary['generated_output_count']}",
        f"- Recommended next command: `{index['recommended_next_command']}`",
        "",
        "## Bundled Fixtures",
        "",
        "| Fixture | Ticker | Data cutoff | Status | Recommended next command |",
        "| --- | --- | --- | --- | --- |",
    ]
    for fixture in index["fixtures"]:
        lines.append(
            f"| `{fixture['path']}` | `{fixture['ticker']}` | `{fixture['data_cutoff']}` | "
            f"{fixture['static_live_status']} | `{fixture['recommended_next_command']}` |"
        )
    lines.extend(
        [
            "",
            "## Templates",
            "",
            "| Template | Path | Purpose | Recommended next command |",
            "| --- | --- | --- | --- |",
        ]
    )
    for template in index["templates"]:
        lines.append(
            f"| {template['title']} | `{template['path']}` | {template['purpose']} | "
            f"`{template['recommended_next_command']}` |"
        )
    lines.extend(
        [
            "",
            "## Generated Outputs",
            "",
            "| Output | Format | Artifact group | Recommended next command |",
            "| --- | --- | --- | --- |",
        ]
    )
    for output in index["generated_outputs"]:
        lines.append(
            f"| `{output['path']}` | `{output['format']}` | {output['artifact_group']} | "
            f"`{output['recommended_next_command']}` |"
        )
    return "\n".join(lines).rstrip() + "\n"


def _with_recommended_next_command(entry: dict[str, Any]) -> dict[str, Any]:
    commands = entry.get("recommended_commands", [])
    return {
        **entry,
        "recommended_next_command": commands[0] if commands else RECOMMENDED_NEXT_COMMAND,
    }


def _all_fixture_entries(base: Path) -> list[dict[str, Any]]:
    entries = build_fixture_catalog(base)
    known_paths = {entry["path"] for entry in entries}
    for path in sorted((base / "examples/input").glob("*.json")):
        relative_path = path.relative_to(base).as_posix()
        if relative_path in known_paths:
            continue
        payload = read_json(path)
        entries.append(
            {
                "slug": path.stem,
                "path": relative_path,
                "company": payload["company"],
                "ticker": payload["ticker"],
                "as_of": payload["as_of"],
                "data_cutoff": payload["data_cutoff"],
                "static_live_status": "static filled-template workflow fixture",
                "recommended_commands": [
                    f"earnings-call-risk-map analyze {relative_path}",
                    f"earnings-call-risk-map review-queue {relative_path}",
                ],
            }
        )
    return entries


def _generated_outputs(base: Path) -> list[dict[str, str]]:
    output_root = base / OUTPUT_DIR
    if not output_root.is_dir():
        return []
    return [
        {
            "path": path.relative_to(base).as_posix(),
            "format": _format_for_path(path),
            "artifact_group": _artifact_group(path.name),
            "recommended_next_command": _recommended_command_for_output(path.name),
        }
        for path in sorted(output_root.iterdir())
        if path.is_file()
    ]


def _format_for_path(path: Path) -> str:
    if path.name.endswith(".jsonl"):
        return "jsonl"
    suffix = path.suffix.lower().lstrip(".")
    return suffix or "unknown"


def _artifact_group(name: str) -> str:
    if "review_queue" in name:
        return "review queue"
    if "dashboard" in name:
        return "dashboard"
    if "snapshot" in name:
        return "analyzed snapshot"
    if "report" in name:
        return "markdown report"
    if "compare" in name:
        return "snapshot compare"
    if "catalog" in name:
        return "catalog"
    if "case_study_map" in name:
        return "case study map"
    if "taxonomy" in name:
        return "taxonomy"
    if "playbook" in name:
        return "playbook"
    if "handoff" in name:
        return "handoff packet"
    if "audit" in name:
        return "audit"
    if "doctor" in name:
        return "doctor"
    if "manifest" in name:
        return "manifest"
    if "cheat" in name:
        return "command cheat sheet"
    return "generated output"


def _recommended_command_for_output(name: str) -> str:
    if name == "fixture_catalog.md":
        return "earnings-call-risk-map fixture-catalog --out examples/output/fixture_catalog.md"
    if name == "case_study_map.md":
        return "earnings-call-risk-map case-study-map --format markdown --out examples/output/case_study_map.md"
    if name == "case_study_map.json":
        return "earnings-call-risk-map case-study-map --format json --out examples/output/case_study_map.json"
    if name == "risk_language_taxonomy.md":
        return "earnings-call-risk-map risk-taxonomy --out examples/output/risk_language_taxonomy.md"
    if name == "template_catalog.md":
        return "earnings-call-risk-map template-catalog --format markdown --out examples/output/template_catalog.md"
    if name == "template_catalog.json":
        return "earnings-call-risk-map template-catalog --format json --out examples/output/template_catalog.json"
    if name == "playbooks.md":
        return "earnings-call-risk-map playbooks --format markdown --out examples/output/playbooks.md"
    if name == "playbooks.json":
        return "earnings-call-risk-map playbooks --format json --out examples/output/playbooks.json"
    if name == "doctor.md":
        return "earnings-call-risk-map doctor --format markdown --out examples/output/doctor.md"
    if name == "doctor.json":
        return "earnings-call-risk-map doctor --format json --out examples/output/doctor.json"
    if name == "examples_index.md":
        return "earnings-call-risk-map examples-index --format markdown --out examples/output/examples_index.md"
    if name == "examples_index.json":
        return "earnings-call-risk-map examples-index --format json --out examples/output/examples_index.json"
    return RECOMMENDED_NEXT_COMMAND
