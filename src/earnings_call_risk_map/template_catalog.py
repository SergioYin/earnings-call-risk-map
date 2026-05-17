"""Blank template catalog rendering."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .io import read_json
from .models import SAFETY_NOTICE

TEMPLATE_CATALOG = (
    {
        "slug": "software",
        "title": "Software Earnings Review",
        "path": Path("examples/templates/software_earnings_review.json"),
        "purpose": "SaaS, cloud, platform, or other software earnings review starting point.",
    },
    {
        "slug": "energy_infrastructure",
        "title": "Energy Infrastructure Earnings Review",
        "path": Path("examples/templates/energy_infrastructure_earnings_review.json"),
        "purpose": "Capital-intensive utility, energy infrastructure, project, or regulated-asset review starting point.",
    },
    {
        "slug": "consumer_hardware",
        "title": "Consumer Hardware Earnings Review",
        "path": Path("examples/templates/consumer_hardware_earnings_review.json"),
        "purpose": "Device, channel inventory, product launch, supply chain, or warranty review starting point.",
    },
)
RECOMMENDED_TOP_LEVEL_FIELDS = ("company", "ticker", "as_of", "data_cutoff")


def build_template_catalog(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    templates = []
    for template in TEMPLATE_CATALOG:
        path = template["path"]
        payload = read_json(base / path)
        templates.append(
            {
                "slug": template["slug"],
                "title": template["title"],
                "path": path.as_posix(),
                "purpose": template["purpose"],
                "recommended_fields": {
                    "top_level": list(RECOMMENDED_TOP_LEVEL_FIELDS),
                    "note_fields": _field_names(payload.get("notes", [])),
                    "kpi_fields": _field_names(payload.get("kpis", [])),
                    "catalyst_fields": _field_names(payload.get("catalysts", [])),
                    "note_topics": [item.get("topic", "") for item in payload.get("notes", [])],
                    "kpi_names": [item.get("name", "") for item in payload.get("kpis", [])],
                    "catalyst_titles": [item.get("title", "") for item in payload.get("catalysts", [])],
                },
                "recommended_commands": [
                    f"earnings-call-risk-map analyze {path.as_posix()}",
                    f"earnings-call-risk-map review-queue {path.as_posix()} --md-out examples/output/{template['slug']}_template_review_queue.md --json-out examples/output/{template['slug']}_template_review_queue.json",
                    f"earnings-call-risk-map analyze {path.as_posix()} --json-out examples/output/{template['slug']}_template_snapshot.json --md-out examples/output/{template['slug']}_template_report.md",
                ],
            }
        )
    return {
        "schema_version": "0.1",
        "artifact_type": "template_catalog",
        "template_count": len(templates),
        "safety_notice": SAFETY_NOTICE,
        "templates": templates,
    }


def template_catalog_json(root: str | Path = ".") -> str:
    return json.dumps(build_template_catalog(root), indent=2, sort_keys=True) + "\n"


def render_template_catalog_markdown(catalog: dict[str, Any]) -> str:
    lines = [
        "# Template Catalog",
        "",
        "Reusable blank templates for starting deterministic earnings-review fixtures.",
        "",
        f"> {catalog['safety_notice']}",
        "",
        "| Template | Path | Purpose |",
        "| --- | --- | --- |",
    ]
    for template in catalog["templates"]:
        lines.append(f"| {template['title']} | `{template['path']}` | {template['purpose']} |")

    lines.extend(["", "## Recommended Fields And Commands", ""])
    for template in catalog["templates"]:
        fields = template["recommended_fields"]
        lines.extend(
            [
                f"### {template['title']}",
                "",
                f"- Slug: `{template['slug']}`",
                f"- Path: `{template['path']}`",
                f"- Top-level fields: {', '.join(f'`{field}`' for field in fields['top_level'])}",
                f"- Note fields: {', '.join(f'`{field}`' for field in fields['note_fields'])}",
                f"- KPI fields: {', '.join(f'`{field}`' for field in fields['kpi_fields'])}",
                f"- Catalyst fields: {', '.join(f'`{field}`' for field in fields['catalyst_fields'])}",
                f"- Suggested note topics: {', '.join(f'`{topic}`' for topic in fields['note_topics'] if topic)}",
                f"- Suggested KPIs: {', '.join(f'`{name}`' for name in fields['kpi_names'] if name)}",
                f"- Suggested catalysts: {', '.join(f'`{title}`' for title in fields['catalyst_titles'] if title)}",
                "",
                "```bash",
            ]
        )
        lines.extend(template["recommended_commands"])
        lines.extend(["```", ""])
    return "\n".join(lines).rstrip() + "\n"


def template_catalog_markdown(root: str | Path = ".") -> str:
    return render_template_catalog_markdown(build_template_catalog(root))


def _field_names(items: object) -> list[str]:
    fields: set[str] = set()
    if not isinstance(items, list):
        return []
    for item in items:
        if isinstance(item, dict):
            fields.update(str(key) for key in item)
    return sorted(fields)
