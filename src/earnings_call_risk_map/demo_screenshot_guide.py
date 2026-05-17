"""Demo screenshot guide rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE

BEST_SCREENSHOT_TARGETS: tuple[dict[str, str], ...] = (
    {
        "path": "examples/output/public_apple_static_case_study_dashboard.html",
        "use": (
            "Best primary README screenshot. It shows the static public-source case study, source attribution, "
            "stale/static labels, risk and opportunity panels, review queue signals, and the non-advice boundary."
        ),
    },
    {
        "path": "examples/output/demo_dashboard.html",
        "use": "Good compact fallback when the README needs a smaller software-style fixture.",
    },
    {
        "path": "examples/output/energy_infrastructure_dashboard.html",
        "use": "Good sector-contrast screenshot for capital projects, catalysts, and stale/static project data.",
    },
    {
        "path": "examples/output/consumer_hardware_dashboard.html",
        "use": "Good sector-contrast screenshot for hardware launch, supply chain, inventory, and margin review examples.",
    },
    {
        "path": "examples/output/semiconductor_equipment_dashboard.html",
        "use": "Good sector-contrast screenshot for backlog, export control, China exposure, and equipment-cycle examples.",
    },
    {
        "path": "docs/assets/showcase-dashboard-preview.svg",
        "use": "Best PNG-free README visual when the repository page should render without a browser screenshot file.",
    },
    {
        "path": "examples/output/showcase_dashboard_preview.svg",
        "use": "Best release artifact copy of the PNG-free preview SVG.",
    },
    {
        "path": "docs/demo-index.html",
        "use": "Good overview screenshot for the local static demo launcher and bundled artifacts.",
    },
)

GOOD_README_VISUALS = (
    "Static HTML dashboards that can be opened directly from disk.",
    "The PNG-free preview SVG when a stable README image is better than a manually captured screenshot.",
    "A short crop of `examples/output/demo_review_queue.md` or `examples/output/public_apple_static_case_study_review_queue.md` for human review handoff.",
    "A short crop of `examples/output/demo_compare.md` for deterministic prior-vs-current comparison.",
    "A short crop of `examples/output/case_study_map.md` for bundled fixtures and sector coverage.",
    "A short crop of `examples/output/handoff_packet.md` for downstream thesis-ledger or portfolio-risk handoff.",
    "A short crop of `examples/output/promotion_pack.md` for a release page or external project listing.",
)

DASHBOARD_FRAMING = (
    "Capture the top of the dashboard through the summary tiles.",
    "Keep the static educational case-study warning or non-advice notice visible.",
    "Include source attribution or stale/static labels when space allows.",
    "Include the review queue panel when the screenshot is meant to explain analyst handoff.",
    "Use a browser window wide enough that summary tiles and risk panels are legible.",
)

MARKDOWN_FRAMING = (
    "Use sections with headings, counts, artifact paths, source-boundary notes, or review queue items.",
    "Keep crops short enough for README readability.",
    "Prefer generated Markdown artifacts over manually rewritten summaries.",
)

LESS_USEFUL_VISUALS = (
    "examples/output/*_snapshot.json",
    "examples/output/*_review_queue.json",
    "examples/output/demo_review_queue_items.jsonl",
    "examples/output/release_manifest.json",
    "examples/output/package_audit.json",
    "examples/output/doctor.json",
    "docs/schema-reference.json",
)

BOUNDARIES = (
    "Do not use screenshots to imply live market data.",
    "Do not use screenshots to imply real-time monitoring, price targets, buy/sell/hold recommendations, or personalized investment advice.",
    "Preserve stale/static badges, source attribution, and the visible non-advice notice.",
)

RELATED_DOCS = (
    "docs/pages-demo.md",
    "docs/gallery.md",
    "docs/promotion-page-outline.md",
    "docs/source-attribution-guide.md",
    "docs/non-advice-boundary.md",
)


def build_demo_screenshot_guide() -> dict[str, Any]:
    return {
        "artifact_type": "demo_screenshot_guide",
        "source_doc": "docs/demo-screenshot-guide.md",
        "goal": (
            "Choose generated artifacts for README visuals, release notes, gallery pages, or a public demo page "
            "without implying live data or investment advice."
        ),
        "safety_notice": SAFETY_NOTICE,
        "best_screenshot_targets": [dict(target) for target in BEST_SCREENSHOT_TARGETS],
        "good_readme_visuals": list(GOOD_README_VISUALS),
        "screenshot_framing": {
            "dashboard": list(DASHBOARD_FRAMING),
            "markdown": list(MARKDOWN_FRAMING),
        },
        "less_useful_visuals": list(LESS_USEFUL_VISUALS),
        "boundaries": list(BOUNDARIES),
        "related_docs": list(RELATED_DOCS),
    }


def demo_screenshot_guide_json() -> str:
    return json.dumps(build_demo_screenshot_guide(), indent=2, sort_keys=True) + "\n"


def demo_screenshot_guide_markdown() -> str:
    guide = build_demo_screenshot_guide()
    lines = [
        "# Demo Screenshot Guide",
        "",
        guide["goal"],
        "",
        f"> {guide['safety_notice']}",
        "",
        f"- Source doc: `{guide['source_doc']}`",
        f"- Best screenshot targets: {len(guide['best_screenshot_targets'])}",
        "",
        "## Best Screenshot Targets",
        "",
    ]
    lines.extend(f"- `{target['path']}`: {target['use']}" for target in guide["best_screenshot_targets"])
    lines.extend(["", "## Good README Visuals", ""])
    lines.extend(f"- {visual}" for visual in guide["good_readme_visuals"])
    lines.extend(["", "## Screenshot Framing", "", "### Dashboards", ""])
    lines.extend(f"- {item}" for item in guide["screenshot_framing"]["dashboard"])
    lines.extend(["", "### Markdown", ""])
    lines.extend(f"- {item}" for item in guide["screenshot_framing"]["markdown"])
    lines.extend(["", "## Less Useful Visuals", ""])
    lines.extend(f"- `{path}`" for path in guide["less_useful_visuals"])
    lines.extend(["", "Use these JSON and JSONL files as linked evidence or downloadable artifacts instead of README images."])
    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in guide["boundaries"])
    lines.extend(["", "## Related Docs", ""])
    lines.extend(f"- `{path}`" for path in guide["related_docs"])
    return "\n".join(lines) + "\n"
