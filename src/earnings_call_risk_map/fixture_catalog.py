"""Bundled fixture catalog rendering."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import read_json

FIXTURE_CATALOG = (
    {
        "slug": "demo_company",
        "path": Path("examples/input/demo_company.json"),
        "status": "static demo fixture",
        "recommended_commands": (
            "earnings-call-risk-map analyze examples/input/demo_company.json",
            "earnings-call-risk-map review-queue examples/input/demo_company.json --md-out examples/output/demo_review_queue.md --json-out examples/output/demo_review_queue.json",
            "earnings-call-risk-map analyze examples/input/demo_company.json --html-out examples/output/demo_dashboard.html",
        ),
    },
    {
        "slug": "demo_energy_infrastructure",
        "path": Path("examples/input/demo_energy_infrastructure.json"),
        "status": "static demo fixture",
        "recommended_commands": (
            "earnings-call-risk-map analyze examples/input/demo_energy_infrastructure.json",
            "earnings-call-risk-map review-queue examples/input/demo_energy_infrastructure.json --md-out examples/output/energy_infrastructure_review_queue.md --json-out examples/output/energy_infrastructure_review_queue.json",
            "earnings-call-risk-map analyze examples/input/demo_energy_infrastructure.json --html-out examples/output/energy_infrastructure_dashboard.html",
        ),
    },
    {
        "slug": "consumer_hardware",
        "path": Path("examples/input/consumer_hardware.json"),
        "status": "static public-source consumer hardware fixture",
        "recommended_commands": (
            "earnings-call-risk-map analyze examples/input/consumer_hardware.json",
            "earnings-call-risk-map review-queue examples/input/consumer_hardware.json --md-out examples/output/consumer_hardware_review_queue.md --json-out examples/output/consumer_hardware_review_queue.json",
            "earnings-call-risk-map analyze examples/input/consumer_hardware.json --html-out examples/output/consumer_hardware_dashboard.html",
        ),
    },
    {
        "slug": "semiconductor_equipment",
        "path": Path("examples/input/semiconductor_equipment.json"),
        "status": "static public-source semiconductor equipment fixture",
        "recommended_commands": (
            "earnings-call-risk-map analyze examples/input/semiconductor_equipment.json",
            "earnings-call-risk-map review-queue examples/input/semiconductor_equipment.json --md-out examples/output/semiconductor_equipment_review_queue.md --json-out examples/output/semiconductor_equipment_review_queue.json",
            "earnings-call-risk-map analyze examples/input/semiconductor_equipment.json --html-out examples/output/semiconductor_equipment_dashboard.html",
        ),
    },
    {
        "slug": "public_apple_static_case_study",
        "path": Path("examples/input/public_apple_static_case_study.json"),
        "status": "static public-source case study",
        "recommended_commands": (
            "earnings-call-risk-map analyze examples/input/public_apple_static_case_study.json",
            "earnings-call-risk-map review-queue examples/input/public_apple_static_case_study.json --md-out examples/output/public_apple_static_case_study_review_queue.md --json-out examples/output/public_apple_static_case_study_review_queue.json",
            "earnings-call-risk-map analyze examples/input/public_apple_static_case_study.json --html-out examples/output/public_apple_static_case_study_dashboard.html",
        ),
    },
    {
        "slug": "demo_company_prior",
        "path": Path("examples/input/demo_company_prior.json"),
        "status": "static compare baseline",
        "recommended_commands": (
            "earnings-call-risk-map analyze examples/input/demo_company_prior.json --json-out examples/output/demo_prior_snapshot.json --md-out examples/output/demo_prior_report.md",
            "earnings-call-risk-map compare examples/output/demo_prior_snapshot.json examples/output/demo_snapshot.json --md-out examples/output/demo_compare.md --json-out examples/output/demo_compare.json",
        ),
    },
)


def build_fixture_catalog(root: str | Path = ".") -> list[dict[str, Any]]:
    base = Path(root)
    entries: list[dict[str, Any]] = []
    for fixture in FIXTURE_CATALOG:
        payload = read_json(base / fixture["path"])
        entries.append(
            {
                "slug": fixture["slug"],
                "path": fixture["path"].as_posix(),
                "company": payload["company"],
                "ticker": payload["ticker"],
                "as_of": payload["as_of"],
                "data_cutoff": payload["data_cutoff"],
                "static_live_status": fixture["status"],
                "recommended_commands": list(fixture["recommended_commands"]),
            }
        )
    return entries


def render_fixture_catalog_markdown(catalog: list[dict[str, Any]]) -> str:
    lines = [
        "# Fixture Catalog",
        "",
        "Bundled fixtures are deterministic examples for local demos and tests. None of the bundled fixtures fetch live market, filing, or transcript data at runtime.",
        "",
        "Regenerate this catalog with `earnings-call-risk-map fixture-catalog`.",
        "",
        "| Fixture | Ticker | Data cutoff | Static/live status | Recommended command |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in catalog:
        command = entry["recommended_commands"][0]
        lines.append(
            f"| `{entry['path']}` | `{entry['ticker']}` | `{entry['data_cutoff']}` | "
            f"{entry['static_live_status']} | `{command}` |"
        )

    lines.extend(["", "## Recommended Commands", ""])
    for entry in catalog:
        lines.extend(
            [
                f"### {entry['slug']}",
                "",
                f"- Company: {entry['company']}",
                f"- Ticker: `{entry['ticker']}`",
                f"- As of: `{entry['as_of']}`",
                f"- Data cutoff: `{entry['data_cutoff']}`",
                f"- Static/live status: {entry['static_live_status']}",
                "",
                "```bash",
            ]
        )
        lines.extend(entry["recommended_commands"])
        lines.extend(["```", ""])
    return "\n".join(lines).rstrip() + "\n"


def fixture_catalog_markdown(root: str | Path = ".") -> str:
    return render_fixture_catalog_markdown(build_fixture_catalog(root))
