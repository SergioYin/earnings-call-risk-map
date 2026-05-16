"""Command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import package_audit_json, package_audit_markdown
from .core import analyze_document, build_review_queue_export, compare_snapshots
from .io import read_json, write_json, write_text
from .manifest import manifest_json
from .maturity import write_maturity_evidence
from .render import render_compare_markdown, render_dashboard_html, render_markdown, render_review_queue_markdown
from .version import __version__

DEMO_FIXTURES = (
    ("demo", Path("examples/input/demo_company.json")),
    ("energy_infrastructure", Path("examples/input/demo_energy_infrastructure.json")),
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

    audit = sub.add_parser("audit", help="Report package audit parity as JSON or Markdown")
    audit.add_argument("--format", choices=("json", "markdown"), default="json", help="Output format")
    audit.add_argument("--out", metavar="PATH", help="Write audit report to this path")
    audit.set_defaults(func=cmd_audit)

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
    for slug, source in DEMO_FIXTURES:
        snapshot = analyze_document(read_json(source))
        review_queue = build_review_queue_export(snapshot)
        write_json(out_dir / f"{slug}_snapshot.json", snapshot)
        write_text(out_dir / f"{slug}_report.md", render_markdown(snapshot))
        write_text(out_dir / f"{slug}_dashboard.html", render_dashboard_html(snapshot))
        write_json(out_dir / f"{slug}_review_queue.json", review_queue)
        write_text(out_dir / f"{slug}_review_queue.md", render_review_queue_markdown(review_queue))
    write_text(out_dir / "package_audit.json", package_audit_json("."))
    write_text(out_dir / "package_audit.md", package_audit_markdown("."))
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


def cmd_maturity_evidence(args: argparse.Namespace) -> int:
    outputs = write_maturity_evidence(args.out_dir, ".")
    print(f"wrote maturity evidence bundle to {outputs['json'].parent}")
    return 0


def cmd_version(args: argparse.Namespace) -> int:
    print(__version__)
    return 0
