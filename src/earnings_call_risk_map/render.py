"""Markdown and static HTML renderers."""

from __future__ import annotations

from html import escape
from typing import Any

from .models import SAFETY_NOTICE

SOURCE_BOUNDARY_LINES = [
    "## Source Boundaries",
    "",
    "- Management claims: source-provided company statements or prepared remarks; verify against filings and transcripts.",
    "- Analyst questions: source-provided questions or prompts; they are not treated as factual claims.",
    "- User synthesis: user-authored notes, tags, and deterministic tool scores; they are review prompts, not advice.",
    "",
]


def render_markdown(snapshot: dict[str, Any]) -> str:
    lines = [
        f"# Earnings Call Risk Map: {snapshot['company']} ({snapshot['ticker']})",
        "",
        f"- As of: `{snapshot['as_of']}`",
        f"- Static data cutoff: `{snapshot['data_cutoff']}`",
        f"- Tool version: `{snapshot['tool_version']}`",
        "",
        f"> {snapshot['safety_notice']}",
        "",
    ]
    lines.extend(SOURCE_BOUNDARY_LINES)
    lines.extend(_source_attribution_section(snapshot.get("source_attribution", [])))
    lines.extend(
        [
            "## Summary",
            "",
            f"- Risks: {snapshot['summary']['risk_count']}",
            f"- Opportunities: {snapshot['summary']['opportunity_count']}",
            f"- Review queue: {snapshot['summary']['review_queue_count']}",
            f"- Stale/static badges: {snapshot['summary']['stale_badge_count']}",
            "",
        ]
    )
    lines.extend(_section("Risks", snapshot.get("risks", []), "risk_score", "risk_level"))
    lines.extend(_section("Opportunities", snapshot.get("opportunities", []), "opportunity_score", "opportunity_level"))
    lines.extend(_review_queue(snapshot.get("review_queue", [])))
    lines.extend(_stale_badges(snapshot.get("stale_badges", [])))
    lines.extend(_catalysts(snapshot.get("catalyst_timeline", [])))
    return "\n".join(lines).rstrip() + "\n"


def render_compare_markdown(compare: dict[str, Any]) -> str:
    lines = [
        f"# Snapshot Compare: {compare.get('company')} ({compare.get('ticker')})",
        "",
        f"- Before: `{compare.get('before_as_of')}`",
        f"- After: `{compare.get('after_as_of')}`",
        f"- Review queue delta: {compare.get('review_queue_delta')}",
        f"- Stale/static badge delta: {compare.get('stale_badge_delta')}",
        "",
        f"> {compare.get('safety_notice', SAFETY_NOTICE)}",
        "",
    ]
    lines.extend(SOURCE_BOUNDARY_LINES)
    lines.extend(_source_attribution_section(compare.get("source_attribution", [])))
    lines.extend(_compare_interpretation(compare.get("interpretation", [])))
    lines.extend(_changes("Risk Changes", compare.get("risk_changes", [])))
    lines.extend(_changes("Opportunity Changes", compare.get("opportunity_changes", [])))
    return "\n".join(lines).rstrip() + "\n"


def render_review_queue_markdown(export: dict[str, Any]) -> str:
    summary = export.get("summary", {})
    lines = [
        f"# Review Queue Export: {export.get('company')} ({export.get('ticker')})",
        "",
        f"- As of: `{export.get('as_of')}`",
        f"- Static data cutoff: `{export.get('data_cutoff')}`",
        f"- Tool version: `{export.get('tool_version')}`",
        "",
        f"> {export.get('safety_notice')}",
        "",
    ]
    lines.extend(SOURCE_BOUNDARY_LINES)
    lines.extend(_source_attribution_section(export.get("source_attribution", [])))
    lines.extend(
        [
            "## Focus",
            "",
            "- stale data",
            "- missing evidence",
            "- high-impact language",
            "",
            "## Summary",
            "",
            f"- Review items: {summary.get('review_item_count', 0)}",
            f"- Stale data: {summary.get('stale_data_count', 0)}",
            f"- Missing evidence: {summary.get('missing_evidence_count', 0)}",
            f"- High-impact language: {summary.get('high_impact_language_count', 0)}",
            "",
            "## Items",
            "",
        ]
    )
    items = export.get("items", [])
    if not items:
        lines.append("- Empty.")
        return "\n".join(lines).rstrip() + "\n"
    for item in items:
        label = item.get("topic") or item.get("id")
        reasons = "; ".join(item.get("reasons", []))
        badge = item.get("stale_badge") or {}
        badge_label = badge.get("label") or "n/a"
        age = badge.get("age_days")
        age_text = "n/a" if age is None else str(age)
        evidence = item.get("evidence_url") or "missing evidence URL"
        lines.append(f"- **{label}** ({item.get('source_type')}): {reasons}")
        lines.append(
            f"  Date: `{item.get('date') or 'unknown'}`; badge: `{badge_label}` age={age_text}; "
            f"risk={item.get('risk_score', 0)}; opportunity={item.get('opportunity_score', 0)}"
        )
        lines.append(f"  Evidence: {evidence}")
        lines.extend(f"  Source attribution: {line}" for line in _source_attribution_lines(item.get("source_attribution", [])))
    return "\n".join(lines).rstrip() + "\n"


def render_dashboard_html(snapshot: dict[str, Any]) -> str:
    """Render a deterministic static dashboard with no external assets."""

    summary = snapshot.get("summary", {})
    title = f"Earnings Call Risk Map: {snapshot.get('company')} ({snapshot.get('ticker')})"
    body = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{_html(title)}</title>",
        "<style>",
        _dashboard_css(),
        "</style>",
        "</head>",
        "<body>",
        '<main class="page">',
        '<header class="hero">',
        '<div class="eyebrow">Deterministic demo dashboard</div>',
        f"<h1>{_html(snapshot.get('company'))} <span>{_html(snapshot.get('ticker'))}</span></h1>",
        '<div class="static-warning">Static educational case study - not live market data or advice</div>',
        '<dl class="meta">',
        f"<div><dt>As of</dt><dd>{_html(snapshot.get('as_of'))}</dd></div>",
        f"<div><dt>Static data cutoff</dt><dd>{_html(snapshot.get('data_cutoff'))}</dd></div>",
        f"<div><dt>Tool version</dt><dd>{_html(snapshot.get('tool_version'))}</dd></div>",
        "</dl>",
        f'<p class="notice">{_html(snapshot.get("safety_notice"))}</p>',
        "</header>",
        _source_attribution_panel(snapshot.get("source_attribution", [])),
        '<section class="summary" aria-label="Summary counts">',
        _metric("Risks", summary.get("risk_count", 0), "risk"),
        _metric("Opportunities", summary.get("opportunity_count", 0), "opportunity"),
        _metric("Review queue", summary.get("review_queue_count", 0), "review"),
        _metric("Stale badges", summary.get("stale_badge_count", 0), "stale"),
        "</section>",
        '<section class="grid">',
        _ranked_panel("Risks", snapshot.get("risks", []), "risk_score", "risk_level"),
        _ranked_panel(
            "Opportunities",
            snapshot.get("opportunities", []),
            "opportunity_score",
            "opportunity_level",
        ),
        _review_panel(snapshot.get("review_queue", [])),
        _stale_panel(snapshot.get("stale_badges", [])),
        "</section>",
        _catalyst_panel(snapshot.get("catalyst_timeline", [])),
        "</main>",
        "</body>",
        "</html>",
    ]
    return "\n".join(body) + "\n"


def _section(title: str, items: list[dict[str, Any]], score_key: str, level_key: str) -> list[str]:
    lines = [f"## {title}", ""]
    if not items:
        return lines + ["- None detected by deterministic keyword rules.", ""]
    for item in items:
        label = item.get("topic") or item.get("name") or item.get("id")
        evidence = item.get("evidence_url") or "missing evidence URL"
        badge = item.get("stale_badge", {}).get("label", "date-unverified")
        lines.append(f"- **{label}**: {item[score_key]} ({item[level_key]}), `{badge}`")
        lines.append(f"  Evidence: {evidence}")
        lines.extend(f"  Source attribution: {line}" for line in _source_attribution_lines(item.get("source_attribution", [])))
    lines.append("")
    return lines


def _dashboard_css() -> str:
    return """
:root{color-scheme:light;--ink:#17202a;--muted:#5d6978;--line:#d9e0e8;--panel:#ffffff;--risk:#a1372f;--opp:#1f7652;--review:#6f4a9e;--stale:#8b621e;--bg:#f5f7f9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Arial,Helvetica,sans-serif}
.page{max-width:1180px;margin:0 auto;padding:28px 18px 40px}
.hero{border-bottom:1px solid var(--line);padding-bottom:20px}
.eyebrow{color:var(--muted);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
h1{font-size:32px;line-height:1.15;margin:8px 0 14px}
h1 span{color:var(--muted);font-weight:600}
.meta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0 0 16px}
.meta div,.metric,.panel{background:var(--panel);border:1px solid var(--line);border-radius:8px}
.meta div{padding:10px 12px}
dt{color:var(--muted);font-size:12px;font-weight:700;text-transform:uppercase}
dd{margin:2px 0 0;font-weight:700}
.notice{max-width:900px;margin:0;color:var(--muted)}
.static-warning{display:inline-block;margin:0 0 12px;padding:5px 8px;border:1px solid #d7b56d;background:#fff8e8;color:var(--stale);font-size:12px;font-weight:700;text-transform:uppercase}
.summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0}
.metric{padding:14px}
.metric strong{display:block;font-size:30px;line-height:1}
.metric span{color:var(--muted);font-weight:700}
.metric.risk{border-top:4px solid var(--risk)}
.metric.opportunity{border-top:4px solid var(--opp)}
.metric.review{border-top:4px solid var(--review)}
.metric.stale{border-top:4px solid var(--stale)}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.panel{padding:16px}
h2{font-size:18px;margin:0 0 12px}
ol,ul{margin:0;padding-left:20px}
li{margin:0 0 11px}
.item-title{font-weight:700}
.item-meta{color:var(--muted);font-size:13px}
.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 7px;margin-left:4px;font-size:12px;font-weight:700}
.badge.stale,.badge.date-unverified{border-color:#d7b56d;color:var(--stale);background:#fff8e8}
.badge.current{color:#2d6b4f;background:#eaf6ef}
a{color:#235c96;overflow-wrap:anywhere}
.catalysts{margin-top:14px}
@media(max-width:760px){.page{padding:20px 12px 28px}h1{font-size:26px}.meta,.summary,.grid{grid-template-columns:1fr}}
""".strip()


def _metric(label: str, value: Any, class_name: str) -> str:
    return f'<article class="metric {class_name}"><strong>{_html(value)}</strong><span>{_html(label)}</span></article>'


def _ranked_panel(title: str, items: list[dict[str, Any]], score_key: str, level_key: str) -> str:
    lines = [f'<article class="panel"><h2>{_html(title)}</h2>']
    if not items:
        lines.append("<p>No items detected by deterministic keyword rules.</p></article>")
        return "\n".join(lines)
    lines.append("<ol>")
    for item in items:
        label = item.get("topic") or item.get("name") or item.get("id")
        badge = item.get("stale_badge", {})
        lines.append("<li>")
        lines.append(
            f'<div class="item-title">{_html(label)}: {_html(item.get(score_key, 0))} '
            f'({_html(item.get(level_key, "none"))}){_badge(badge)}</div>'
        )
        lines.append(f'<div class="item-meta">Evidence: {_evidence(item.get("evidence_url"))}</div>')
        lines.extend(_item_attribution_html(item.get("source_attribution", [])))
        lines.append("</li>")
    lines.append("</ol></article>")
    return "\n".join(lines)


def _review_panel(items: list[dict[str, Any]]) -> str:
    lines = ['<article class="panel"><h2>Review Queue</h2>']
    if not items:
        lines.append("<p>Empty.</p></article>")
        return "\n".join(lines)
    lines.append("<ul>")
    for item in items:
        reasons = "; ".join(item.get("reasons", []))
        lines.append(f'<li><span class="item-title">{_html(item.get("topic"))}</span>: {_html(reasons)}</li>')
    lines.append("</ul></article>")
    return "\n".join(lines)


def _stale_panel(items: list[dict[str, Any]]) -> str:
    lines = ['<article class="panel"><h2>Stale Badges</h2>']
    if not items:
        lines.append("<p>No stale or unverified dates detected.</p></article>")
        return "\n".join(lines)
    lines.append("<ul>")
    for item in items:
        badge = item.get("badge", {})
        age = badge.get("age_days")
        age_text = "n/a" if age is None else str(age)
        lines.append(
            f'<li><span class="item-title">{_html(item.get("topic"))}</span>: '
            f'{_badge(badge)} <span class="item-meta">age={_html(age_text)}</span></li>'
        )
    lines.append("</ul></article>")
    return "\n".join(lines)


def _catalyst_panel(items: list[dict[str, Any]]) -> str:
    lines = ['<section class="panel catalysts"><h2>Catalysts</h2>']
    if not items:
        lines.append("<p>No catalysts supplied.</p></section>")
        return "\n".join(lines)
    lines.append("<ol>")
    for item in items:
        lines.append(
            f'<li><span class="item-title">{_html(item.get("date"))} - {_html(item.get("title"))}</span> '
            f'<span class="item-meta">({_html(item.get("expected_impact", "n/a"))})</span><br>'
            f'{_html(item.get("description", ""))}<br>'
            f'<span class="item-meta">Evidence: {_evidence(item.get("evidence_url"))}</span>'
            f'{_catalyst_attribution_html(item.get("source_attribution", []))}</li>'
        )
    lines.append("</ol></section>")
    return "\n".join(lines)


def _badge(badge: dict[str, Any]) -> str:
    label = str(badge.get("label") or "date-unverified")
    status = str(badge.get("status") or "date-unverified")
    return f'<span class="badge {_html(status)}">{_html(label)}</span>'


def _source_attribution_section(sources: list[dict[str, Any]]) -> list[str]:
    lines = ["## Source Attribution", ""]
    if not sources:
        return lines + ["- No source attribution supplied beyond item evidence URLs.", ""]
    for source in sources:
        lines.append(f"- {_source_attribution_text(source)}")
    lines.append("")
    return lines


def _source_attribution_panel(sources: list[dict[str, Any]]) -> str:
    lines = ['<section class="panel attribution"><h2>Source Attribution</h2>']
    if not sources:
        lines.append("<p>No source attribution supplied beyond item evidence URLs.</p></section>")
        return "\n".join(lines)
    lines.append("<ul>")
    for source in sources:
        lines.append(f"<li>{_html(_source_attribution_text(source))}</li>")
    lines.append("</ul></section>")
    return "\n".join(lines)


def _item_attribution_html(sources: list[dict[str, Any]]) -> list[str]:
    return [f'<div class="item-meta">Source attribution: {_html(_source_attribution_text(source))}</div>' for source in sources]


def _catalyst_attribution_html(sources: list[dict[str, Any]]) -> str:
    if not sources:
        return ""
    lines = ["<br>" + _html("Source attribution: " + _source_attribution_text(sources[0]))]
    for source in sources[1:]:
        lines.append("<br>" + _html("Source attribution: " + _source_attribution_text(source)))
    return "".join(lines)


def _source_attribution_lines(sources: list[dict[str, Any]]) -> list[str]:
    return [_source_attribution_text(source) for source in sources]


def _source_attribution_text(source: dict[str, Any]) -> str:
    label = source.get("source_name") or source.get("source_url") or "Unnamed source"
    source_type = source.get("source_type") or "source"
    publisher = source.get("publisher")
    url = source.get("source_url")
    accessed = source.get("accessed_at")
    static_notice = source.get("static_notice")
    parts = [str(label), f"type={source_type}"]
    if publisher:
        parts.append(f"publisher={publisher}")
    if accessed:
        parts.append(f"accessed={accessed}")
    if static_notice:
        parts.append(str(static_notice))
    if url:
        parts.append(str(url))
    return "; ".join(parts)


def _evidence(url: Any) -> str:
    if not url:
        return "missing evidence URL"
    escaped = _html(url)
    return f'<a href="{escaped}">{escaped}</a>'


def _html(value: Any) -> str:
    return escape("" if value is None else str(value), quote=True)


def _review_queue(items: list[dict[str, Any]]) -> list[str]:
    lines = ["## Review Queue", ""]
    if not items:
        return lines + ["- Empty.", ""]
    for item in items:
        reasons = "; ".join(item.get("reasons", []))
        lines.append(f"- **{item.get('topic')}**: {reasons}")
    lines.append("")
    return lines


def _stale_badges(items: list[dict[str, Any]]) -> list[str]:
    lines = ["## Stale/static Data Badges", ""]
    if not items:
        return lines + ["- No stale or unverified dates detected.", ""]
    for item in items:
        badge = item["badge"]
        lines.append(f"- **{item.get('topic')}**: `{badge['label']}` age={badge['age_days']}")
    lines.append("")
    return lines


def _catalysts(items: list[dict[str, Any]]) -> list[str]:
    lines = ["## Catalyst Timeline", ""]
    if not items:
        return lines + ["- No catalysts supplied.", ""]
    for item in items:
        lines.append(f"- `{item['date']}` **{item['title']}** ({item['expected_impact']}): {item['description']}")
        lines.extend(f"  Source attribution: {line}" for line in _source_attribution_lines(item.get("source_attribution", [])))
    lines.append("")
    return lines


def _compare_interpretation(items: list[str]) -> list[str]:
    lines = ["## How To Read This Compare", ""]
    if not items:
        return lines + [
            "- Score deltas are deterministic review prompts; verify them against source materials before using them.",
            "",
        ]
    lines.extend(f"- {item}" for item in items)
    lines.append("")
    return lines


def _changes(title: str, items: list[dict[str, Any]]) -> list[str]:
    lines = [f"## {title}", ""]
    if not items:
        return lines + ["- No score changes.", ""]
    for item in items:
        lines.append(f"- **{item['topic']}**: {item['before']} -> {item['after']} ({item['delta']:+d})")
    lines.append("")
    return lines
