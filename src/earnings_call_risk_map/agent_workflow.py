"""Generic agent workflow instruction rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE

ROUTES: tuple[dict[str, Any], ...] = (
    {
        "slug": "analyze",
        "title": "Analyze Route",
        "when_to_use": "Use when the user provides one raw input fixture or asks for a report, dashboard, or snapshot.",
        "command": (
            "PYTHONPATH=src python -m earnings_call_risk_map analyze input.json "
            "--json-out snapshot.json --md-out report.md"
        ),
        "agent_checks": [
            "`safety_notice`",
            "`source_boundaries`",
            "risk and opportunity scores",
            "stale/static badges",
            "review queue count",
            "evidence URLs and source attribution records",
        ],
    },
    {
        "slug": "compare",
        "title": "Compare Route",
        "when_to_use": "Use when the user provides two analyzed JSON snapshots or asks what changed between reviews.",
        "command": (
            "PYTHONPATH=src python -m earnings_call_risk_map compare before.json after.json "
            "--json-out compare.json --md-out compare.md"
        ),
        "agent_checks": [
            "before and after snapshot dates",
            "comparison scope",
            "risk and opportunity score deltas",
            "interpretation text that describes review attention, not real-world company quality",
        ],
    },
    {
        "slug": "review-queue",
        "title": "Review Queue Route",
        "when_to_use": "Use when the user asks what needs checking, evidence cleanup, stale-data review, or handoff.",
        "command": (
            "PYTHONPATH=src python -m earnings_call_risk_map review-queue input.json "
            "--json-out review_queue.json --md-out review_queue.md"
        ),
        "agent_checks": [
            "stale or unverified dates",
            "missing evidence URLs",
            "high-impact language",
            "visible review reasons for every queued item",
        ],
    },
    {
        "slug": "source-attribution",
        "title": "Source Attribution Route",
        "when_to_use": "Use whenever an answer repeats or summarizes source-backed content from a fixture.",
        "command": "",
        "agent_checks": [
            "source name",
            "publisher",
            "source type",
            "source URL",
            "access date",
            "`as_of` and `data_cutoff`",
            "static-data notice",
        ],
    },
)

SOURCE_BOUNDARIES = (
    "Management claims are source-provided company statements or prepared remarks.",
    "Analyst questions are source-provided questions or prompts; they are not assertions.",
    "User synthesis covers user-authored notes, labels, tags, and deterministic scoring output.",
)

HANDOFF_CHECKS = (
    "Confirm the output includes the educational research boundary.",
    "Confirm source boundaries are preserved.",
    "Confirm stale/static badges are still visible.",
    "Confirm missing evidence and high-impact language remain in the review queue.",
    "Confirm compare language describes scoring movement, not a recommendation.",
    "Confirm cited source attribution uses fixture records and does not imply live-data freshness.",
)

STOP_BOUNDARIES = (
    "Do not fetch or refresh live market data unless the user explicitly changes scope and provides an approved method.",
    "Do not verify source URLs by network access as part of this local-only workflow.",
    "Do not create price targets, ratings, forecasts, expected returns, allocations, or trade instructions.",
    "Do not recommend buy, sell, hold, short, reduce, add, underweight, or overweight actions.",
    "Do not remove stale/static warnings, missing-evidence reasons, or safety notices.",
)

RECOMMENDED_SEQUENCE = (
    "analyze",
    "review-queue",
    "compare when prior/current snapshots exist",
    "summarize with source attribution",
)


def build_agent_workflow() -> dict[str, Any]:
    return {
        "artifact_type": "agent_workflow",
        "source_doc": "docs/agent-workflow.md",
        "goal": (
            "Route generic coding or research agents through deterministic local CLI commands while preserving "
            "source attribution, stale/static warnings, human review queues, and non-advice boundaries."
        ),
        "safety_notice": SAFETY_NOTICE,
        "recommended_sequence": list(RECOMMENDED_SEQUENCE),
        "routes": [dict(route) for route in ROUTES],
        "source_boundaries": list(SOURCE_BOUNDARIES),
        "handoff_checklist": list(HANDOFF_CHECKS),
        "stop_boundaries": list(STOP_BOUNDARIES),
    }


def agent_workflow_json() -> str:
    return json.dumps(build_agent_workflow(), indent=2, sort_keys=True) + "\n"


def agent_workflow_markdown() -> str:
    workflow = build_agent_workflow()
    lines = [
        "# Agent Workflow",
        "",
        workflow["goal"],
        "",
        f"> {workflow['safety_notice']}",
        "",
        f"- Source doc: `{workflow['source_doc']}`",
        f"- Routes: {len(workflow['routes'])}",
        "",
        "## Routing Map",
        "",
        "Choose the narrowest route that answers the user's request. For a complete review bundle, run:",
        "",
    ]
    lines.extend(f"{index}. {step}" for index, step in enumerate(workflow["recommended_sequence"], start=1))
    for route in workflow["routes"]:
        lines.extend(["", f"## {route['title']}", "", route["when_to_use"], ""])
        if route["command"]:
            lines.extend(["```bash", route["command"], "```", ""])
        lines.append("Agent checks:")
        lines.extend(f"- {check}" for check in route["agent_checks"])
    lines.extend(["", "## Source Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in workflow["source_boundaries"])
    lines.extend(["", "## Handoff Checklist", ""])
    lines.extend(f"- {check}" for check in workflow["handoff_checklist"])
    lines.extend(["", "## Stop Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in workflow["stop_boundaries"])
    return "\n".join(lines) + "\n"
