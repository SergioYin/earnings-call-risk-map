"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import package_audit_json, package_audit_markdown
from .core import (
    analyze_document,
    build_handoff_packet,
    build_review_queue_export,
    build_review_queue_jsonl_records,
    compare_snapshots,
    render_jsonl,
)
from .fixture_catalog import fixture_catalog_markdown
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
from .release_assets import build_release_asset_checklist, render_release_asset_checklist_markdown
from .render import (
    render_compare_markdown,
    render_dashboard_html,
    render_handoff_packet_examples_markdown,
    render_handoff_packet_markdown,
    render_markdown,
    render_review_queue_markdown,
)
from .version import __version__

DEMO_FIXTURES = (
    ("demo", Path("examples/input/demo_company.json")),
    ("energy_infrastructure", Path("examples/input/demo_energy_infrastructure.json")),
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

    release_assets = sub.add_parser(
        "release-assets",
        help="Validate expected release assets for the current version",
    )
    release_assets.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    release_assets.add_argument("--out", metavar="PATH", help="Write release asset checklist to this path")
    release_assets.add_argument("--root", default=".", metavar="DIR", help="Repository root to validate")
    release_assets.set_defaults(func=cmd_release_assets)

    fixture_catalog = sub.add_parser("fixture-catalog", help="List bundled fixtures and recommended commands")
    fixture_catalog.add_argument("--out", metavar="PATH", help="Write fixture catalog Markdown to this path")
    fixture_catalog.set_defaults(func=cmd_fixture_catalog)

    playbooks = sub.add_parser("playbooks", help="List research playbooks and recommended CLI sequences")
    playbooks.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format")
    playbooks.add_argument("--out", metavar="PATH", help="Write playbook catalog to this path")
    playbooks.set_defaults(func=cmd_playbooks)

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
    write_text(out_dir / "fixture_catalog.md", fixture_catalog_markdown("."))
    write_text(out_dir / "playbooks.md", playbook_catalog_markdown())
    write_text(out_dir / "playbooks.json", playbook_catalog_json())
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


def cmd_fixture_catalog(args: argparse.Namespace) -> int:
    payload = fixture_catalog_markdown(".")
    if args.out:
        write_text(args.out, payload)
    else:
        print(payload, end="")
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


def cmd_maturity_evidence(args: argparse.Namespace) -> int:
    outputs = write_maturity_evidence(args.out_dir, ".")
    print(f"wrote maturity evidence bundle to {outputs['json'].parent}")
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    print(__version__)
    return 0


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
