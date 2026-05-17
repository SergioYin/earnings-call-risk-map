"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path

from .agent_workflow import agent_workflow_json, agent_workflow_markdown
from .audit import package_audit_json, package_audit_markdown
from .case_study_map import case_study_map_json, case_study_map_markdown
from .core import (
    analyze_document,
    build_handoff_packet,
    build_review_queue_export,
    build_review_queue_jsonl_records,
    compare_snapshots,
    render_jsonl,
)
from .data_entry_checklist import data_entry_checklist_json, data_entry_checklist_markdown
from .demo_screenshot_guide import demo_screenshot_guide_json, demo_screenshot_guide_markdown
from .doctor import (
    build_doctor_report,
    doctor_report_json,
    doctor_report_markdown,
    render_doctor_report_markdown,
)
from .examples_index import examples_index_json, examples_index_markdown
from .fixture_catalog import fixture_catalog_markdown
from .fresh_clone_plan import fresh_clone_plan_json, fresh_clone_plan_markdown
from .fixture_summary import fixture_summary_json, fixture_summary_markdown
from .io import read_json, write_json, write_text
from .manifest import manifest_json
from .maturity import write_maturity_evidence
from .models import SAFETY_NOTICE
from .playbooks import (
    playbook_catalog_json,
    playbook_catalog_markdown,
    playbook_output_examples_json,
    playbook_output_examples_markdown,
)
from .publication_checklist import publication_checklist_json, publication_checklist_markdown
from .promotion_pack import promotion_pack_json, promotion_pack_markdown
from .release_assets import build_release_asset_checklist, render_release_asset_checklist_markdown
from .release_notes import release_notes_summary_markdown
from .release_owner_handoff import release_owner_handoff_json, release_owner_handoff_markdown
from .render import (
    render_compare_markdown,
    render_dashboard_html,
    render_handoff_packet_examples_markdown,
    render_handoff_packet_markdown,
    render_markdown,
    render_review_queue_markdown,
)
from .risk_taxonomy import risk_language_taxonomy_markdown
from .schema_authoring_reference import schema_authoring_reference_json, schema_authoring_reference_markdown
from .schema_reference import schema_reference_json
from .template_catalog import template_catalog_json, template_catalog_markdown
from .version import __version__

DEMO_FIXTURES = (
    ("demo", Path("examples/input/demo_company.json")),
    ("energy_infrastructure", Path("examples/input/demo_energy_infrastructure.json")),
    ("consumer_hardware", Path("examples/input/consumer_hardware.json")),
    ("semiconductor_equipment", Path("examples/input/semiconductor_equipment.json")),
    ("public_apple_static_case_study", Path("examples/input/public_apple_static_case_study.json")),
)
DEMO_COMPARE = (
    "demo_compare",
    "demo_prior",
    Path("examples/input/demo_company_prior.json"),
    Path("examples/input/demo_company.json"),
)
DEMO_REVIEW_QUEUE_JSONL_FIXTURES = DEMO_FIXTURES + (
    ("demo_prior", Path("examples/input/demo_company_prior.json")),
)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="earnings-call-risk-map",
        description=(
            "Build deterministic earnings-call risk review artifacts from public or user-authored JSON notes. "
            "Educational research review only; outputs are not personalized investment, legal, accounting, "
            "tax, buy, sell, or hold advice."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    analyze = sub.add_parser("analyze", help="Analyze one earnings-call JSON input")
    analyze.add_argument("input", metavar="INPUT_JSON", help="Input JSON object using the documented schema")
    analyze.add_argument("--json-out", metavar="PATH", help="Write the full JSON snapshot")
    analyze.add_argument("--md-out", metavar="PATH", help="Write the Markdown review report")
    analyze.add_argument("--html-out", metavar="PATH", help="Write a self-contained static HTML dashboard")
    analyze.set_defaults(func=cmd_analyze)

    demo = sub.add_parser("demo", help="Generate demo bundles from examples/input fixtures")
    demo.add_argument("--out-dir", default="examples/output", metavar="DIR", help="Directory for generated demo artifacts")
    demo.set_defaults(func=cmd_demo)

    doctor = sub.add_parser("doctor", help="Report deterministic package health and release-readiness hints")
    doctor.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    doctor.add_argument("--out", metavar="PATH", help="Write doctor report to this path")
    doctor.add_argument("--root", default=".", metavar="DIR", help="Repository root to inspect")
    doctor.set_defaults(func=cmd_doctor)

    compare = sub.add_parser("compare", help="Compare two analyzed JSON snapshots")
    compare.add_argument("before", metavar="BEFORE_JSON", help="Earlier analyzed JSON snapshot")
    compare.add_argument("after", metavar="AFTER_JSON", help="Later analyzed JSON snapshot")
    compare.add_argument("--json-out", metavar="PATH", help="Write the JSON compare result")
    compare.add_argument("--md-out", metavar="PATH", help="Write the Markdown compare report")
    compare.set_defaults(func=cmd_compare)

    review_queue = sub.add_parser("review-queue", help="Export only stale, missing-evidence, and high-impact review items")
    review_queue.add_argument("input", metavar="INPUT_JSON", help="Input JSON object using the documented schema")
    review_queue.add_argument("--json-out", metavar="PATH", help="Write focused review queue JSON")
    review_queue.add_argument("--md-out", metavar="PATH", help="Write focused review queue Markdown")
    review_queue.set_defaults(func=cmd_review_queue)

    review_queue_jsonl = sub.add_parser(
        "review-queue-jsonl",
        help="Export deterministic JSON Lines review items across bundled demo fixtures",
    )
    review_queue_jsonl.add_argument("--out", metavar="PATH", help="Write JSON Lines to this path")
    review_queue_jsonl.set_defaults(func=cmd_review_queue_jsonl)

    handoff_packet = sub.add_parser(
        "handoff-packet",
        help="Export deterministic portfolio/thesis handoff packet paths and cautions",
    )
    handoff_packet.add_argument(
        "--report-path",
        default="examples/output/demo_report.md",
        metavar="PATH",
        help="Markdown report path to include in the handoff packet",
    )
    handoff_packet.add_argument(
        "--review-queue-jsonl-path",
        default="examples/output/demo_review_queue_items.jsonl",
        metavar="PATH",
        help="Review queue JSON Lines path to include in the handoff packet",
    )
    handoff_packet.add_argument(
        "--compare-path",
        default="examples/output/demo_compare.md",
        metavar="PATH",
        help="Compare artifact path to include in the handoff packet",
    )
    handoff_packet.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Stdout format")
    handoff_packet.add_argument("--json-out", metavar="PATH", help="Write handoff packet JSON")
    handoff_packet.add_argument("--md-out", metavar="PATH", help="Write handoff packet Markdown")
    handoff_packet.set_defaults(func=cmd_handoff_packet)

    audit = sub.add_parser("audit", help="Report package audit parity as JSON or Markdown")
    audit.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    audit.add_argument("--out", metavar="PATH", help="Write audit report to this path")
    audit.set_defaults(func=cmd_audit)

    agent_workflow = sub.add_parser(
        "agent-workflow",
        help="Render generic agent workflow instructions as Markdown or JSON",
    )
    agent_workflow.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    agent_workflow.add_argument("--out", metavar="PATH", help="Write agent workflow instructions to this path")
    agent_workflow.set_defaults(func=cmd_agent_workflow)

    cheat_sheet = sub.add_parser("cheat-sheet", help="Print lightweight command cheat sheet as Markdown or JSON")
    cheat_sheet.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    cheat_sheet.add_argument("--out", metavar="PATH", help="Write command cheat sheet to this path")
    cheat_sheet.set_defaults(func=cmd_cheat_sheet)

    case_study_map = sub.add_parser("case-study-map", help="Render bundled case study map as Markdown or JSON")
    case_study_map.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    case_study_map.add_argument("--out", metavar="PATH", help="Write case study map to this path")
    case_study_map.set_defaults(func=cmd_case_study_map)

    release_assets = sub.add_parser(
        "release-assets",
        help="Validate expected release assets for the current version",
    )
    release_assets.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    release_assets.add_argument("--out", metavar="PATH", help="Write release asset checklist to this path")
    release_assets.add_argument("--root", default=".", metavar="DIR", help="Repository root to validate")
    release_assets.set_defaults(func=cmd_release_assets)

    release_notes = sub.add_parser(
        "release-notes",
        help="Render current audit, release assets, and changelog excerpt as Markdown",
    )
    release_notes.add_argument("--out", metavar="PATH", help="Write rendered release notes Markdown to this path")
    release_notes.add_argument("--root", default=".", metavar="DIR", help="Repository root to summarize")
    release_notes.set_defaults(func=cmd_release_notes)

    fixture_catalog = sub.add_parser("fixture-catalog", help="List bundled fixtures and recommended commands")
    fixture_catalog.add_argument("--out", metavar="PATH", help="Write fixture catalog Markdown to this path")
    fixture_catalog.set_defaults(func=cmd_fixture_catalog)

    fixture_summary = sub.add_parser(
        "fixture-summary",
        help="Summarize one input fixture's source types, stale badges, and counts",
    )
    fixture_summary.add_argument("input", metavar="INPUT_JSON", help="Input JSON object using the documented schema")
    fixture_summary.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    fixture_summary.add_argument("--out", metavar="PATH", help="Write fixture summary to this path")
    fixture_summary.set_defaults(func=cmd_fixture_summary)

    risk_taxonomy = sub.add_parser(
        "risk-taxonomy",
        help="Render deterministic risk language taxonomy Markdown",
    )
    risk_taxonomy.add_argument("--out", metavar="PATH", help="Write risk language taxonomy Markdown to this path")
    risk_taxonomy.set_defaults(func=cmd_risk_taxonomy)

    examples_index = sub.add_parser(
        "examples-index",
        help="Summarize bundled examples, generated outputs, and recommended next commands",
    )
    examples_index.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    examples_index.add_argument("--out", metavar="PATH", help="Write examples index to this path")
    examples_index.set_defaults(func=cmd_examples_index)

    template_catalog = sub.add_parser("template-catalog", help="List blank templates with recommended fields and commands")
    template_catalog.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    template_catalog.add_argument("--out", metavar="PATH", help="Write template catalog to this path")
    template_catalog.set_defaults(func=cmd_template_catalog)

    schema_reference = sub.add_parser("schema-reference", help="Render the JSON fixture schema reference")
    schema_reference.add_argument("--out", metavar="PATH", help="Write schema reference JSON to this path")
    schema_reference.set_defaults(func=cmd_schema_reference)

    schema_authoring_reference = sub.add_parser(
        "schema-authoring-reference",
        help="Render fixture schema authoring reference as Markdown or JSON",
    )
    schema_authoring_reference.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format",
    )
    schema_authoring_reference.add_argument("--out", metavar="PATH", help="Write schema authoring reference to this path")
    schema_authoring_reference.set_defaults(func=cmd_schema_authoring_reference)

    playbooks = sub.add_parser("playbooks", help="List research playbooks and recommended CLI sequences")
    playbooks.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    playbooks.add_argument("--out", metavar="PATH", help="Write playbook catalog to this path")
    playbooks.set_defaults(func=cmd_playbooks)

    publication_checklist = sub.add_parser(
        "publication-checklist",
        help="Render public release owner steps as Markdown or JSON",
    )
    publication_checklist.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    publication_checklist.add_argument("--out", metavar="PATH", help="Write publication checklist to this path")
    publication_checklist.set_defaults(func=cmd_publication_checklist)

    release_owner_handoff = sub.add_parser(
        "release-owner-handoff",
        help="Render final release owner handoff as Markdown or JSON",
    )
    release_owner_handoff.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    release_owner_handoff.add_argument("--out", metavar="PATH", help="Write release owner handoff to this path")
    release_owner_handoff.set_defaults(func=cmd_release_owner_handoff)

    promotion_pack = sub.add_parser(
        "promotion-pack",
        help="Render public promotion pack as Markdown or JSON",
    )
    promotion_pack.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    promotion_pack.add_argument("--out", metavar="PATH", help="Write promotion pack to this path")
    promotion_pack.set_defaults(func=cmd_promotion_pack)

    data_entry_checklist = sub.add_parser(
        "data-entry-checklist",
        help="Render fixture author data-entry checklist as Markdown or JSON",
    )
    data_entry_checklist.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    data_entry_checklist.add_argument("--out", metavar="PATH", help="Write data-entry checklist to this path")
    data_entry_checklist.set_defaults(func=cmd_data_entry_checklist)

    demo_screenshot_guide = sub.add_parser(
        "demo-screenshot-guide",
        help="Render demo screenshot guide as Markdown or JSON",
    )
    demo_screenshot_guide.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    demo_screenshot_guide.add_argument("--out", metavar="PATH", help="Write demo screenshot guide to this path")
    demo_screenshot_guide.set_defaults(func=cmd_demo_screenshot_guide)

    fresh_clone_plan = sub.add_parser(
        "fresh-clone-plan",
        help="Render fresh clone verification plan as Markdown or JSON",
    )
    fresh_clone_plan.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    fresh_clone_plan.add_argument("--out", metavar="PATH", help="Write fresh clone verification plan to this path")
    fresh_clone_plan.set_defaults(func=cmd_fresh_clone_plan)

    manifest = sub.add_parser("manifest", help="Print or write release manifest")
    manifest.add_argument("--out", metavar="PATH", help="Write manifest JSON to this path")
    manifest.set_defaults(func=cmd_manifest)

    maturity = sub.add_parser("maturity-evidence", help="Generate a basic maturity evidence bundle")
    maturity.add_argument("--out-dir", default="reports/maturity", metavar="DIR", help="Directory for generated evidence files")
    maturity.set_defaults(func=cmd_maturity_evidence)

    version = sub.add_parser("version", help="Print version")
    version.set_defaults(func=cmd_version)
    return parser


def cmd_analyze(args: argparse.Namespace) -> int:
    snapshot = analyze_document(read_json(args.input))
    md = render_markdown(snapshot)
    html = render_dashboard_html(snapshot)
    if args.json_out:
        write_json(args.json_out, snapshot)
    if args.md_out:
        write_text(args.md_out, md)
    if args.html_out:
        write_text(args.html_out, html)
    if not args.json_out and not args.md_out and not args.html_out:
        print(md, end="")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir)
    jsonl_records = []
    for slug, source in DEMO_FIXTURES:
        snapshot = analyze_document(read_json(source))
        review_queue = build_review_queue_export(snapshot)
        jsonl_records.extend(build_review_queue_jsonl_records(slug, source.as_posix(), review_queue))
        write_json(out_dir / f"{slug}_snapshot.json", snapshot)
        write_text(out_dir / f"{slug}_report.md", render_markdown(snapshot))
        write_text(out_dir / f"{slug}_dashboard.html", render_dashboard_html(snapshot))
        write_json(out_dir / f"{slug}_review_queue.json", review_queue)
        write_text(out_dir / f"{slug}_review_queue.md", render_review_queue_markdown(review_queue))
        if slug == "semiconductor_equipment":
            _write_semiconductor_equipment_report_bundle(out_dir, source, snapshot, review_queue)
    compare_slug, before_slug, before_source, after_source = DEMO_COMPARE
    before_snapshot = analyze_document(read_json(before_source))
    after_snapshot = analyze_document(read_json(after_source))
    compare = compare_snapshots(before_snapshot, after_snapshot)
    before_review_queue = build_review_queue_export(before_snapshot)
    jsonl_records.extend(build_review_queue_jsonl_records(before_slug, before_source.as_posix(), before_review_queue))
    write_json(out_dir / f"{before_slug}_snapshot.json", before_snapshot)
    write_text(out_dir / f"{before_slug}_report.md", render_markdown(before_snapshot))
    write_json(out_dir / f"{compare_slug}.json", compare)
    write_text(out_dir / f"{compare_slug}.md", render_compare_markdown(compare))
    write_text(out_dir / "demo_review_queue_items.jsonl", render_jsonl(jsonl_records))
    packet = build_handoff_packet(
        (out_dir / "demo_report.md").as_posix(),
        (out_dir / "demo_review_queue_items.jsonl").as_posix(),
        (out_dir / "demo_compare.md").as_posix(),
    )
    write_json(out_dir / "handoff_packet.json", packet)
    write_text(out_dir / "handoff_packet.md", render_handoff_packet_markdown(packet))
    write_text(out_dir / "playbook_output_examples.json", playbook_output_examples_json(out_dir))
    write_text(out_dir / "playbook_output_examples.md", playbook_output_examples_markdown(out_dir))
    handoff_examples = _build_handoff_packet_examples(out_dir)
    write_json(out_dir / "handoff_packet_examples.json", handoff_examples)
    write_text(out_dir / "handoff_packet_examples.md", render_handoff_packet_examples_markdown(handoff_examples))
    write_text(out_dir / "package_audit.json", package_audit_json("."))
    write_text(out_dir / "package_audit.md", package_audit_markdown("."))
    write_text(out_dir / "agent_workflow.md", agent_workflow_markdown())
    write_text(out_dir / "agent_workflow.json", agent_workflow_json())
    write_text(out_dir / "doctor.json", doctor_report_json("."))
    write_text(out_dir / "doctor.md", doctor_report_markdown("."))
    command_cheat_sheet_parser = build_parser()
    command_cheat_sheet_json_payload = render_command_cheat_sheet(command_cheat_sheet_parser, "json")
    command_cheat_sheet_markdown_payload = render_command_cheat_sheet(command_cheat_sheet_parser, "markdown")
    write_text(out_dir / "command_cheat_sheet.json", command_cheat_sheet_json_payload)
    write_text(out_dir / "command_cheat_sheet.md", command_cheat_sheet_markdown_payload)
    write_text(out_dir / "command_cheatsheet.json", command_cheat_sheet_json_payload)
    write_text(out_dir / "command_cheatsheet.md", command_cheat_sheet_markdown_payload)
    write_text(out_dir / "fixture_catalog.md", fixture_catalog_markdown("."))
    write_text(out_dir / "case_study_map.md", case_study_map_markdown())
    write_text(out_dir / "case_study_map.json", case_study_map_json())
    write_text(
        out_dir / "risk_language_taxonomy.md",
        risk_language_taxonomy_markdown("../../docs/scoring.md", "../../docs/source-attribution-guide.md"),
    )
    write_text(out_dir / "template_catalog.md", template_catalog_markdown("."))
    write_text(out_dir / "template_catalog.json", template_catalog_json("."))
    write_text(out_dir / "schema_authoring_reference.md", schema_authoring_reference_markdown())
    write_text(out_dir / "schema_authoring_reference.json", schema_authoring_reference_json())
    write_text(out_dir / "playbooks.md", playbook_catalog_markdown())
    write_text(out_dir / "playbooks.json", playbook_catalog_json())
    write_text(out_dir / "publication_checklist.md", publication_checklist_markdown())
    write_text(out_dir / "publication_checklist.json", publication_checklist_json())
    write_text(out_dir / "promotion_pack.md", promotion_pack_markdown())
    write_text(out_dir / "promotion_pack.json", promotion_pack_json())
    write_text(out_dir / "data_entry_checklist.md", data_entry_checklist_markdown())
    write_text(out_dir / "data_entry_checklist.json", data_entry_checklist_json())
    write_text(out_dir / "demo_screenshot_guide.md", demo_screenshot_guide_markdown())
    write_text(out_dir / "demo_screenshot_guide.json", demo_screenshot_guide_json())
    write_text(out_dir / "fresh_clone_plan.md", fresh_clone_plan_markdown())
    write_text(out_dir / "fresh_clone_plan.json", fresh_clone_plan_json())
    write_json(out_dir / "release_manifest.json", json.loads(manifest_json(".")))
    # Seed then rewrite so a fresh output directory indexes both index files.
    write_text(out_dir / "examples_index.md", examples_index_markdown("."))
    write_text(out_dir / "examples_index.json", examples_index_json("."))
    write_text(out_dir / "examples_index.md", examples_index_markdown("."))
    write_text(out_dir / "examples_index.json", examples_index_json("."))
    write_json(out_dir / "release_manifest.json", json.loads(manifest_json(".")))
    print(f"wrote demo bundles to {out_dir}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    result = compare_snapshots(read_json(args.before), read_json(args.after))
    md = render_compare_markdown(result)
    if args.json_out:
        write_json(args.json_out, result)
    if args.md_out:
        write_text(args.md_out, md)
    if not args.json_out and not args.md_out:
        print(md, end="")
    return 0


def cmd_review_queue(args: argparse.Namespace) -> int:
    snapshot = analyze_document(read_json(args.input))
    export = build_review_queue_export(snapshot)
    md = render_review_queue_markdown(export)
    if args.json_out:
        write_json(args.json_out, export)
    if args.md_out:
        write_text(args.md_out, md)
    if not args.json_out and not args.md_out:
        print(md, end="")
    return 0


def cmd_review_queue_jsonl(args: argparse.Namespace) -> int:
    records = []
    for slug, source in DEMO_REVIEW_QUEUE_JSONL_FIXTURES:
        snapshot = analyze_document(read_json(source))
        export = build_review_queue_export(snapshot)
        records.extend(build_review_queue_jsonl_records(slug, source.as_posix(), export))
    payload = render_jsonl(records)
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_handoff_packet(args: argparse.Namespace) -> int:
    packet = build_handoff_packet(args.report_path, args.review_queue_jsonl_path, args.compare_path)
    md = render_handoff_packet_markdown(packet)
    if args.json_out:
        write_json(args.json_out, packet)
    if args.md_out:
        write_text(args.md_out, md)
    if not args.json_out and not args.md_out:
        if args.format == "json":
            print(json.dumps(packet, indent=2, sort_keys=True))
        else:
            print(md, end="")
    return 0


def cmd_manifest(args: argparse.Namespace) -> int:
    payload = manifest_json(".")
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = package_audit_json(".")
    else:
        payload = package_audit_markdown(".")
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_agent_workflow(args: argparse.Namespace) -> int:
    _write_or_print(
        _render_format(args.format, json_payload=agent_workflow_json, markdown_payload=agent_workflow_markdown),
        args.out,
    )
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    report = build_doctor_report(args.root)
    if args.format == "json":
        payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    else:
        payload = render_doctor_report_markdown(report)
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0 if report["status"] == "passed" else 1


def cmd_cheat_sheet(args: argparse.Namespace) -> int:
    payload = render_command_cheat_sheet(build_parser(), args.format)
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_case_study_map(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = case_study_map_json()
    else:
        payload = case_study_map_markdown()
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_release_assets(args: argparse.Namespace) -> int:
    checklist = build_release_asset_checklist(args.root)
    if args.format == "json":
        payload = json.dumps(checklist, indent=2, sort_keys=True) + "\n"
    else:
        payload = render_release_asset_checklist_markdown(checklist)
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 1 if checklist["missing_count"] else 0


def cmd_release_notes(args: argparse.Namespace) -> int:
    payload = release_notes_summary_markdown(args.root)
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_fixture_catalog(args: argparse.Namespace) -> int:
    payload = fixture_catalog_markdown(".")
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_fixture_summary(args: argparse.Namespace) -> int:
    data = read_json(args.input)
    if args.format == "json":
        summary = fixture_summary_json(data)
        if args.out:
            write_json(args.out, summary)
        else:
            print(json.dumps(summary, indent=2, sort_keys=True))
        return 0

    payload = fixture_summary_markdown(data)
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_risk_taxonomy(args: argparse.Namespace) -> int:
    payload = risk_language_taxonomy_markdown("../../docs/scoring.md", "../../docs/source-attribution-guide.md")
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_examples_index(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = examples_index_json(".")
    else:
        payload = examples_index_markdown(".")
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_template_catalog(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = template_catalog_json(".")
    else:
        payload = template_catalog_markdown(".")
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_schema_reference(args: argparse.Namespace) -> int:
    payload = schema_reference_json()
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_schema_authoring_reference(args: argparse.Namespace) -> int:
    _write_or_print(
        _render_format(
            args.format,
            json_payload=schema_authoring_reference_json,
            markdown_payload=schema_authoring_reference_markdown,
        ),
        args.out,
    )
    return 0


def cmd_playbooks(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = playbook_catalog_json()
    else:
        payload = playbook_catalog_markdown()
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_publication_checklist(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = publication_checklist_json()
    else:
        payload = publication_checklist_markdown()
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_release_owner_handoff(args: argparse.Namespace) -> int:
    _write_or_print(
        _render_format(
            args.format,
            json_payload=release_owner_handoff_json,
            markdown_payload=release_owner_handoff_markdown,
        ),
        args.out,
    )
    return 0


def cmd_promotion_pack(args: argparse.Namespace) -> int:
    _write_or_print(
        _render_format(args.format, json_payload=promotion_pack_json, markdown_payload=promotion_pack_markdown),
        args.out,
    )
    return 0


def cmd_data_entry_checklist(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = data_entry_checklist_json()
    else:
        payload = data_entry_checklist_markdown()
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_demo_screenshot_guide(args: argparse.Namespace) -> int:
    if args.format == "json":
        payload = demo_screenshot_guide_json()
    else:
        payload = demo_screenshot_guide_markdown()
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
    return 0


def cmd_fresh_clone_plan(args: argparse.Namespace) -> int:
    _write_or_print(
        _render_format(args.format, json_payload=fresh_clone_plan_json, markdown_payload=fresh_clone_plan_markdown),
        args.out,
    )
    return 0


def cmd_maturity_evidence(args: argparse.Namespace) -> int:
    outputs = write_maturity_evidence(args.out_dir, ".")
    print(f"wrote maturity evidence bundle to {outputs['json'].parent}")
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    print(__version__)
    return 0


def _render_format(
    output_format: str,
    *,
    json_payload: Callable[[], str],
    markdown_payload: Callable[[], str],
) -> str:
    if output_format == "json":
        return json_payload()
    return markdown_payload()


def _write_or_print(payload: str, out: str | None) -> None:
    if out:
        write_text(out, payload)
    else:
        print(payload, end="")


def _write_semiconductor_equipment_report_bundle(
    out_dir: Path,
    source: Path,
    snapshot: dict[str, object],
    review_queue: dict[str, object],
) -> None:
    bundle_dir = out_dir / "semiconductor_equipment_report"
    write_text(bundle_dir / "report.md", render_markdown(snapshot))
    write_json(bundle_dir / "snapshot" / "snapshot.json", snapshot)
    write_text(bundle_dir / "dashboard" / "dashboard.html", render_dashboard_html(snapshot))
    write_json(bundle_dir / "review_queue" / "review_queue.json", review_queue)
    write_text(bundle_dir / "review_queue" / "review_queue.md", render_review_queue_markdown(review_queue))

    fixture = read_json(source)
    write_json(bundle_dir / "fixture_summary" / "fixture_summary.json", fixture_summary_json(fixture))
    write_text(bundle_dir / "fixture_summary" / "fixture_summary.md", fixture_summary_markdown(fixture))


def build_command_cheat_sheet(parser: argparse.ArgumentParser) -> dict[str, object]:
    subparsers_action = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    )
    purposes = {action.dest: action.help for action in subparsers_action._choices_actions}
    commands = [
        {
            "command": command,
            "purpose": purposes[command],
        }
        for command in subparsers_action.choices
    ]
    return {
        "artifact_type": "command_cheat_sheet",
        "command_count": len(commands),
        "commands": commands,
    }


def command_cheat_sheet_json(parser: argparse.ArgumentParser) -> str:
    return json.dumps(build_command_cheat_sheet(parser), indent=2, sort_keys=True) + "\n"


def command_cheat_sheet_markdown(parser: argparse.ArgumentParser) -> str:
    payload = build_command_cheat_sheet(parser)
    lines = [
        "# Command Cheat Sheet",
        "",
        "| Command | Purpose |",
        "| --- | --- |",
    ]
    lines.extend(
        f"| `{item['command']}` | {item['purpose']} |"
        for item in payload["commands"]
    )
    return "\n".join(lines) + "\n"


def render_command_cheat_sheet(parser: argparse.ArgumentParser, output_format: str) -> str:
    if output_format == "json":
        return command_cheat_sheet_json(parser)
    return command_cheat_sheet_markdown(parser)


def _build_handoff_packet_examples(out_dir: Path) -> dict[str, object]:
    specs = (
        (
            "quarterly-review",
            "Quarterly Review Handoff",
            out_dir / "demo_report.md",
            out_dir / "demo_review_queue_items.jsonl",
            out_dir / "demo_compare.md",
        ),
        (
            "catalyst-check-in",
            "Catalyst Check-In Handoff",
            out_dir / "energy_infrastructure_report.md",
            out_dir / "demo_review_queue_items.jsonl",
            out_dir / "demo_compare.md",
        ),
        (
            "post-earnings-thesis-refresh",
            "Post-Earnings Thesis Refresh Handoff",
            out_dir / "public_apple_static_case_study_report.md",
            out_dir / "demo_review_queue_items.jsonl",
            out_dir / "demo_compare.md",
        ),
    )
    return {
        "schema_version": "0.1",
        "artifact_type": "handoff_packet_examples",
        "safety_notice": SAFETY_NOTICE,
        "example_count": len(specs),
        "examples": [
            {
                "slug": slug,
                "title": title,
                "packet": build_handoff_packet(
                    report_path.as_posix(),
                    review_queue_jsonl_path.as_posix(),
                    compare_path.as_posix(),
                ),
            }
            for slug, title, report_path, review_queue_jsonl_path, compare_path in specs
        ],
    }
