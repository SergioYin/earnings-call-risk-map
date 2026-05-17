"""Public promotion pack rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

PURPOSE = (
    "Turn earnings-call notes into deterministic risk maps, review queues, snapshots, "
    "handoff packets, and static dashboards from local JSON fixtures."
)
QUICKSTART = (
    {
        "label": "Generate the bundled demo artifacts",
        "command": "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
    },
    {
        "label": "Analyze one fixture",
        "command": "PYTHONPATH=src python -m earnings_call_risk_map analyze examples/input/demo_company.json",
    },
    {
        "label": "Open the static demo index",
        "command": "open docs/demo-index.html",
    },
)
DEMOS = (
    {
        "label": "Static public-source dashboard",
        "path": "examples/output/public_apple_static_case_study_dashboard.html",
        "why": "Shows attribution, static educational labels, summary tiles, and review panels.",
    },
    {
        "label": "Review queue",
        "path": "examples/output/demo_review_queue.md",
        "why": "Shows stale-data, missing-evidence, and high-impact-language prompts.",
    },
    {
        "label": "Compare narrative",
        "path": "examples/output/demo_compare.md",
        "why": "Shows deterministic before/after score movement without investment conclusions.",
    },
    {
        "label": "Public case-study report",
        "path": "examples/output/public_apple_static_case_study_report.md",
        "why": "Shows public-source attribution and static case-study warnings in Markdown.",
    },
    {
        "label": "Handoff packet",
        "path": "examples/output/handoff_packet.md",
        "why": "Shows generated artifact paths and cautions for adjacent review workflows.",
    },
    {
        "label": "Case study map",
        "path": "examples/output/case_study_map.md",
        "why": "Shows bundled fixtures, reviewer questions, and generated artifacts.",
    },
)
PROOF_COMMANDS = (
    "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
    "PYTHONPATH=src python -m earnings_call_risk_map audit --format markdown",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "PYTHONPATH=src python -m unittest discover -s tests",
    "python scripts/privacy_scan.py",
)
BOUNDARIES = (
    "Educational research review only; not personalized investment, legal, accounting, tax, buy, sell, or hold advice.",
    "No live market data, current company coverage, price targets, expected returns, portfolio actions, or valuation support.",
    "Scores are deterministic review prompts, not facts about company quality, security attractiveness, or future performance.",
    "Bundled fixtures are static examples; public-source fixtures are not live analysis.",
    "The tool preserves management claims, analyst questions, and user synthesis as source-bound review inputs.",
    "No hosted service, database, API, workflow automation, credentials, or network-backed product is implied.",
)
SOURCE_EVIDENCE = (
    "README.md",
    "docs/promotion-page-outline.md",
    "docs/non-advice-boundary.md",
    "docs/case-study-limitations.md",
    "docs/source-attribution-guide.md",
    "docs/reviewer-evidence.md",
    "examples/output/case_study_map.md",
)


def build_promotion_pack() -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "artifact_type": "promotion_pack",
        "name": "earnings-call-risk-map",
        "version": __version__,
        "purpose": PURPOSE,
        "audience": [
            "Analysts, builders, and reviewers who already collect earnings-call notes and evidence links.",
            "Users who want deterministic local artifacts instead of a hosted workflow or LLM summarizer.",
            "Review owners who need visible stale/static labels, source attribution, and handoff files.",
        ],
        "quickstart": [dict(item) for item in QUICKSTART],
        "demos": [dict(item) for item in DEMOS],
        "proof_commands": list(PROOF_COMMANDS),
        "boundaries": list(BOUNDARIES),
        "source_evidence": list(SOURCE_EVIDENCE),
        "safety_notice": SAFETY_NOTICE,
    }


def promotion_pack_json() -> str:
    return json.dumps(build_promotion_pack(), indent=2, sort_keys=True) + "\n"


def promotion_pack_markdown() -> str:
    pack = build_promotion_pack()
    lines = [
        "# Public Promotion Pack",
        "",
        f"- Package: `{pack['name']}`",
        f"- Version: `{pack['version']}`",
        f"- Purpose: {pack['purpose']}",
        "",
        f"> {pack['safety_notice']}",
        "",
        "## Quickstart",
        "",
    ]
    for index, item in enumerate(pack["quickstart"], start=1):
        lines.extend([f"{index}. {item['label']}:", "", "```bash", item["command"], "```", ""])
    lines.extend(["## Demos", "", "| Demo | Artifact | Why it matters |", "| --- | --- | --- |"])
    lines.extend(f"| {item['label']} | `{item['path']}` | {item['why']} |" for item in pack["demos"])
    lines.extend(["", "## Proof Commands", "", "```bash"])
    lines.extend(pack["proof_commands"])
    lines.extend(["```", "", "## Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in pack["boundaries"])
    lines.extend(["", "## Source Evidence", ""])
    lines.extend(f"- `{path}`" for path in pack["source_evidence"])
    return "\n".join(lines) + "\n"
