"""Case study map rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE

CASE_STUDIES = (
    {
        "fixture": "examples/input/demo_company.json",
        "target_sector": "Software and enterprise platform",
        "useful_question": "Which software risks need review after a mixed enterprise-demand and margin update?",
        "generated_artifacts": (
            "examples/output/demo_report.md",
            "examples/output/demo_snapshot.json",
            "examples/output/demo_review_queue.md",
            "examples/output/demo_review_queue.json",
            "examples/output/demo_review_queue_items.jsonl",
            "examples/output/demo_dashboard.html",
        ),
    },
    {
        "fixture": "examples/input/demo_company_prior.json",
        "target_sector": "Software and enterprise platform prior-period baseline",
        "useful_question": "What changed between the prior software baseline and the current demo company fixture?",
        "generated_artifacts": (
            "examples/output/demo_prior_report.md",
            "examples/output/demo_prior_snapshot.json",
            "examples/output/demo_compare.md",
            "examples/output/demo_compare.json",
        ),
    },
    {
        "fixture": "examples/input/demo_energy_infrastructure.json",
        "target_sector": "Energy infrastructure, regulated assets, and large capital projects",
        "useful_question": (
            "Which project execution, financing, permitting, and backlog items deserve follow-up before the next "
            "infrastructure review?"
        ),
        "generated_artifacts": (
            "examples/output/energy_infrastructure_report.md",
            "examples/output/energy_infrastructure_snapshot.json",
            "examples/output/energy_infrastructure_review_queue.md",
            "examples/output/energy_infrastructure_review_queue.json",
            "examples/output/energy_infrastructure_dashboard.html",
        ),
    },
    {
        "fixture": "examples/input/consumer_hardware.json",
        "target_sector": "Consumer hardware and device supply chains",
        "useful_question": (
            "Which demand, channel, supply-chain, and revenue-growth items require reviewer attention in a hardware "
            "case study?"
        ),
        "generated_artifacts": (
            "examples/output/consumer_hardware_report.md",
            "examples/output/consumer_hardware_snapshot.json",
            "examples/output/consumer_hardware_review_queue.md",
            "examples/output/consumer_hardware_review_queue.json",
            "examples/output/consumer_hardware_dashboard.html",
        ),
    },
    {
        "fixture": "examples/input/semiconductor_equipment.json",
        "target_sector": "Semiconductor equipment and capital equipment cycles",
        "useful_question": (
            "How should reviewers triage net sales, gross margin, bookings, backlog, demand timing, and "
            "export-control risk in a semiconductor equipment case study?"
        ),
        "generated_artifacts": (
            "examples/output/semiconductor_equipment_report.md",
            "examples/output/semiconductor_equipment_snapshot.json",
            "examples/output/semiconductor_equipment_review_queue.md",
            "examples/output/semiconductor_equipment_review_queue.json",
            "examples/output/semiconductor_equipment_dashboard.html",
            "examples/output/semiconductor_equipment_report/report.md",
            "examples/output/semiconductor_equipment_report/dashboard/dashboard.html",
            "examples/output/semiconductor_equipment_report/review_queue/review_queue.md",
            "examples/output/semiconductor_equipment_report/review_queue/review_queue.json",
            "examples/output/semiconductor_equipment_report/snapshot/snapshot.json",
            "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md",
            "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json",
        ),
    },
    {
        "fixture": "examples/input/public_apple_static_case_study.json",
        "target_sector": "Consumer hardware, services, and mega-cap public-source case study",
        "useful_question": (
            "Which static public-source Apple revenue, services, and risk-factor signals should be reviewed without "
            "treating the fixture as live analysis?"
        ),
        "generated_artifacts": (
            "examples/output/public_apple_static_case_study_report.md",
            "examples/output/public_apple_static_case_study_snapshot.json",
            "examples/output/public_apple_static_case_study_review_queue.md",
            "examples/output/public_apple_static_case_study_review_queue.json",
            "examples/output/public_apple_static_case_study_dashboard.html",
        ),
    },
    {
        "fixture": "examples/input/sample_filled_template_workflow.json",
        "target_sector": "Filled software template workflow",
        "useful_question": (
            "How does a completed blank template become a report, snapshot, and review queue for a software-style "
            "earnings review?"
        ),
        "generated_artifacts": (
            "examples/output/sample_filled_template_report.md",
            "examples/output/sample_filled_template_snapshot.json",
            "examples/output/sample_filled_template_review_queue.md",
            "examples/output/sample_filled_template_review_queue.json",
        ),
    },
)

SHARED_GENERATED_ARTIFACTS = (
    "examples/output/fixture_catalog.md",
    "examples/output/examples_index.md",
    "examples/output/examples_index.json",
    "examples/output/handoff_packet.md",
    "examples/output/handoff_packet.json",
    "examples/output/handoff_packet_examples.md",
    "examples/output/handoff_packet_examples.json",
    "examples/output/playbook_output_examples.md",
    "examples/output/playbook_output_examples.json",
    "examples/output/release_manifest.json",
    "examples/output/showcase_dashboard_preview.svg",
)

REGENERATE_COMMANDS = (
    "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
    (
        "PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/semiconductor_equipment.json "
        "--json-out examples/output/semiconductor_equipment_report/snapshot/snapshot.json "
        "--md-out examples/output/semiconductor_equipment_report/report.md "
        "--html-out examples/output/semiconductor_equipment_report/dashboard/dashboard.html"
    ),
)


def build_case_study_map() -> dict[str, Any]:
    studies = [
        {
            **case_study,
            "generated_artifacts": list(case_study["generated_artifacts"]),
        }
        for case_study in CASE_STUDIES
    ]
    return {
        "schema_version": "0.1",
        "artifact_type": "case_study_map",
        "safety_notice": SAFETY_NOTICE,
        "fixture_count": len(studies),
        "case_studies": studies,
        "shared_generated_artifacts": list(SHARED_GENERATED_ARTIFACTS),
        "regenerate_commands": list(REGENERATE_COMMANDS),
        "related_docs": [
            "docs/fixture-catalog.md",
            "docs/case-study-limitations.md",
            "examples/output/examples_index.md",
        ],
    }


def case_study_map_json() -> str:
    return json.dumps(build_case_study_map(), indent=2, sort_keys=True) + "\n"


def case_study_map_markdown() -> str:
    payload = build_case_study_map()
    lines = [
        "# Case Study Map",
        "",
        (
            "Bundled fixtures are static, deterministic examples for local demos, tests, and documentation. Use this "
            "map to pick the fixture that best matches the review question before generating reports, dashboards, "
            "snapshots, or review queues."
        ),
        "",
        f"> {payload['safety_notice']}",
        "",
        "Machine-readable companion: `examples/output/case_study_map.json`.",
        "",
        "## Fixture Map",
        "",
        "| Fixture | Target sector | Useful question | Generated artifacts |",
        "| --- | --- | --- | --- |",
    ]
    for case_study in payload["case_studies"]:
        artifacts = ", ".join(f"`{artifact}`" for artifact in case_study["generated_artifacts"])
        lines.append(
            f"| `{case_study['fixture']}` | {case_study['target_sector']} | "
            f"{case_study['useful_question']} | {artifacts} |"
        )
    lines.extend(
        [
            "",
            "## Shared Generated Artifacts",
            "",
            "The demo bundle also writes cross-fixture and documentation artifacts that are not owned by a single fixture:",
            "",
        ]
    )
    lines.extend(f"- `{artifact}`" for artifact in payload["shared_generated_artifacts"])
    lines.extend(["", "## Regenerate", "", "Refresh the main case-study artifacts:", "", "```bash"])
    lines.append(payload["regenerate_commands"][0])
    lines.extend(["```", "", "Refresh the nested semiconductor equipment report bundle:", "", "```bash"])
    lines.append(payload["regenerate_commands"][1])
    lines.extend(
        [
            "```",
            "",
            (
                "For fixture metadata, see [Fixture Catalog](fixture-catalog.md). For static-source caveats, see "
                "[Case Study Limitations](case-study-limitations.md). For generated output discovery, see "
                "`examples/output/examples_index.md`."
            ),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
