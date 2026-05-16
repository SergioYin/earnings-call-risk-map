"""Research playbook catalog rendering."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import SAFETY_NOTICE

PLAYBOOKS = (
    {
        "slug": "quarterly-review",
        "title": "Quarterly Review",
        "path": "examples/playbooks/quarterly-review.md",
        "summary": (
            "Full quarter-end refresh from fixture validation through report, review queue, "
            "dashboard, and prior/current compare artifact."
        ),
        "recommended_cli_sequence": (
            "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
            "PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json --json-out examples/output/demo_snapshot.json --md-out examples/output/demo_report.md --html-out examples/output/demo_dashboard.html",
            "PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json",
            "PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company_prior.json --json-out examples/output/demo_prior_snapshot.json",
            "PYTHONPATH=src python -m earnings_call_risk_map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json",
        ),
        "expected_artifacts": (
            "examples/output/demo_report.md",
            "examples/output/demo_snapshot.json",
            "examples/output/demo_review_queue.md",
            "examples/output/demo_compare.md",
            "examples/output/demo_dashboard.html",
        ),
    },
    {
        "slug": "catalyst-check-in",
        "title": "Catalyst Check-In",
        "path": "examples/playbooks/catalyst-check-in.md",
        "summary": (
            "Focused event-date review that emphasizes catalysts, stale badges, and missing "
            "evidence before an upcoming milestone."
        ),
        "recommended_cli_sequence": (
            "PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_energy_infrastructure.json --json-out examples/output/energy_infrastructure_snapshot.json --md-out examples/output/energy_infrastructure_report.md --html-out examples/output/energy_infrastructure_dashboard.html",
            "PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/demo_energy_infrastructure.json --md-out examples/output/energy_infrastructure_review_queue.md --json-out examples/output/energy_infrastructure_review_queue.json",
            "PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl",
        ),
        "expected_artifacts": (
            "examples/output/energy_infrastructure_report.md",
            "examples/output/energy_infrastructure_review_queue.md",
            "examples/output/energy_infrastructure_snapshot.json",
            "examples/output/demo_review_queue_items.jsonl",
        ),
    },
    {
        "slug": "post-earnings-thesis-refresh",
        "title": "Post-Earnings Thesis Refresh",
        "path": "examples/playbooks/post-earnings-thesis-refresh.md",
        "summary": (
            "Post-call refresh that separates management claims, analyst questions, and user "
            "synthesis before updating a thesis ledger."
        ),
        "recommended_cli_sequence": (
            "PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/public_apple_static_case_study.json --json-out examples/output/public_apple_static_case_study_snapshot.json --md-out examples/output/public_apple_static_case_study_report.md --html-out examples/output/public_apple_static_case_study_dashboard.html",
            "PYTHONPATH=src python -m earnings_call_risk_map review-queue examples/input/public_apple_static_case_study.json --md-out examples/output/public_apple_static_case_study_review_queue.md --json-out examples/output/public_apple_static_case_study_review_queue.json",
            "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
        ),
        "expected_artifacts": (
            "examples/output/public_apple_static_case_study_report.md",
            "examples/output/public_apple_static_case_study_review_queue.md",
            "examples/output/public_apple_static_case_study_snapshot.json",
            "examples/output/integration_notes.json",
        ),
    },
)


def build_playbook_catalog() -> dict[str, Any]:
    return {
        "playbook_count": len(PLAYBOOKS),
        "safety_notice": SAFETY_NOTICE,
        "playbooks": [
            {
                "slug": playbook["slug"],
                "title": playbook["title"],
                "path": playbook["path"],
                "summary": playbook["summary"],
                "recommended_cli_sequence": list(playbook["recommended_cli_sequence"]),
                "expected_artifacts": list(playbook["expected_artifacts"]),
            }
            for playbook in PLAYBOOKS
        ],
    }


def build_playbook_output_examples(output_dir: str | Path = "examples/output") -> dict[str, Any]:
    """Build deterministic examples of the output artifacts each playbook should leave behind."""

    base = Path(output_dir)
    return {
        "schema_version": "0.1",
        "artifact_type": "playbook_output_examples",
        "safety_notice": SAFETY_NOTICE,
        "playbook_count": len(PLAYBOOKS),
        "examples": [
            {
                "slug": playbook["slug"],
                "title": playbook["title"],
                "source": playbook["path"],
                "recommended_command_count": len(playbook["recommended_cli_sequence"]),
                "generated_artifacts": [
                    {
                        "path": _artifact_path_for_output_dir(artifact, base),
                        "format": _artifact_format(artifact),
                        "role": _artifact_role(artifact),
                    }
                    for artifact in playbook["expected_artifacts"]
                ],
                "verification": {
                    "regenerate_command": "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir "
                    + base.as_posix(),
                    "selfcheck_command": "PYTHONPATH=src python scripts/selfcheck.py",
                },
            }
            for playbook in PLAYBOOKS
        ],
    }


def playbook_output_examples_json(output_dir: str | Path = "examples/output") -> str:
    return json.dumps(build_playbook_output_examples(output_dir), indent=2, sort_keys=True) + "\n"


def render_playbook_output_examples_markdown(examples: dict[str, Any]) -> str:
    lines = [
        "# Playbook Output Examples",
        "",
        "Deterministic example artifacts generated by the local demo bundle.",
        "",
        f"> {examples['safety_notice']}",
        "",
    ]
    for playbook in examples["examples"]:
        lines.extend(
            [
                f"## {playbook['title']}",
                "",
                f"- Slug: `{playbook['slug']}`",
                f"- Source: `{playbook['source']}`",
                f"- Recommended commands: {playbook['recommended_command_count']}",
                "",
                "| Artifact | Format | Role |",
                "| --- | --- | --- |",
            ]
        )
        for artifact in playbook["generated_artifacts"]:
            lines.append(f"| `{artifact['path']}` | `{artifact['format']}` | {artifact['role']} |")
        verification = playbook["verification"]
        lines.extend(
            [
                "",
                "Verification:",
                f"- Regenerate: `{verification['regenerate_command']}`",
                f"- Selfcheck: `{verification['selfcheck_command']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def playbook_output_examples_markdown(output_dir: str | Path = "examples/output") -> str:
    return render_playbook_output_examples_markdown(build_playbook_output_examples(output_dir))


def playbook_catalog_json() -> str:
    return json.dumps(build_playbook_catalog(), indent=2, sort_keys=True) + "\n"


def render_playbook_catalog_markdown(catalog: dict[str, Any]) -> str:
    lines = [
        "# Research Playbooks",
        "",
        "Available deterministic playbooks and their recommended local CLI sequence.",
        "",
        f"> {catalog['safety_notice']}",
        "",
        "| Playbook | Path | Purpose |",
        "| --- | --- | --- |",
    ]
    for playbook in catalog["playbooks"]:
        lines.append(f"| {playbook['title']} | `{playbook['path']}` | {playbook['summary']} |")

    lines.extend(["", "## Recommended CLI Sequences", ""])
    for playbook in catalog["playbooks"]:
        lines.extend(
            [
                f"### {playbook['title']}",
                "",
                f"- Slug: `{playbook['slug']}`",
                f"- Source: `{playbook['path']}`",
                "",
                "```bash",
            ]
        )
        lines.extend(playbook["recommended_cli_sequence"])
        lines.extend(["```", "", "Expected artifacts:"])
        lines.extend(f"- `{artifact}`" for artifact in playbook["expected_artifacts"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def playbook_catalog_markdown() -> str:
    return render_playbook_catalog_markdown(build_playbook_catalog())


def _artifact_path_for_output_dir(path: str, output_dir: Path) -> str:
    prefix = "examples/output/"
    if path.startswith(prefix):
        return (output_dir / path.removeprefix(prefix)).as_posix()
    return path


def _artifact_format(path: str) -> str:
    suffix = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    return {
        "html": "html",
        "json": "json",
        "jsonl": "jsonl",
        "md": "markdown",
        "svg": "svg",
    }.get(suffix, "file")


def _artifact_role(path: str) -> str:
    filename = path.rsplit("/", 1)[-1]
    if "dashboard" in filename:
        return "static dashboard preview"
    if "review_queue" in filename:
        return "focused human-review queue"
    if "compare" in filename:
        return "prior/current deterministic score movement"
    if "snapshot" in filename:
        return "machine-readable analyzed snapshot"
    if "report" in filename:
        return "human-readable research review report"
    if "integration_notes" in filename:
        return "downstream integration example records"
    return "generated playbook artifact"
