"""Maturity evidence bundle generation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from .audit import COMMANDS, FIXTURE_PATTERN
from .models import SAFETY_NOTICE
from .version import __version__

TEST_COMMANDS = (
    "PYTHONPATH=src python -m unittest discover -s tests",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "python scripts/privacy_scan.py",
)
VERIFICATION_COMMANDS = (
    "PYTHONPATH=src python -m unittest discover -s tests",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "PYTHONPATH=src python -m earnings_call_risk_map demo --out-dir examples/output",
    "PYTHONPATH=src python -m earnings_call_risk_map review-queue-jsonl --out examples/output/demo_review_queue_items.jsonl",
    "PYTHONPATH=src python -m earnings_call_risk_map agent-workflow --format markdown --out examples/output/agent_workflow.md",
    "PYTHONPATH=src python -m earnings_call_risk_map agent-workflow --format json --out examples/output/agent_workflow.json",
    "PYTHONPATH=src python -m earnings_call_risk_map examples-index --format markdown --out examples/output/examples_index.md",
    "PYTHONPATH=src python -m earnings_call_risk_map examples-index --format json --out examples/output/examples_index.json",
    "PYTHONPATH=src python -m earnings_call_risk_map case-study-map --format markdown --out examples/output/case_study_map.md",
    "PYTHONPATH=src python -m earnings_call_risk_map case-study-map --format json --out examples/output/case_study_map.json",
    "PYTHONPATH=src python -m earnings_call_risk_map risk-taxonomy --out examples/output/risk_language_taxonomy.md",
    "PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format markdown --out examples/output/source_boundary_evidence.md",
    "PYTHONPATH=src python -m earnings_call_risk_map source-boundary-evidence --format json --out examples/output/source_boundary_evidence.json",
    "PYTHONPATH=src python -m earnings_call_risk_map template-catalog --format markdown --out examples/output/template_catalog.md",
    "PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format markdown --out examples/output/schema_authoring_reference.md",
    "PYTHONPATH=src python -m earnings_call_risk_map schema-authoring-reference --format json --out examples/output/schema_authoring_reference.json",
    "PYTHONPATH=src python -m earnings_call_risk_map playbooks --format markdown --out examples/output/playbooks.md",
    "PYTHONPATH=src python -m earnings_call_risk_map promotion-pack --format markdown --out examples/output/promotion_pack.md",
    "PYTHONPATH=src python -m earnings_call_risk_map promotion-pack --format json --out examples/output/promotion_pack.json",
    "PYTHONPATH=src python -m earnings_call_risk_map publication-checklist --format markdown --out examples/output/publication_checklist.md",
    "PYTHONPATH=src python -m earnings_call_risk_map data-entry-checklist --format markdown --out examples/output/data_entry_checklist.md",
    "PYTHONPATH=src python -m earnings_call_risk_map demo-screenshot-guide --format markdown --out examples/output/demo_screenshot_guide.md",
    "PYTHONPATH=src python -m earnings_call_risk_map demo-screenshot-guide --format json --out examples/output/demo_screenshot_guide.json",
    "PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format markdown --out examples/output/fresh_clone_plan.md",
    "PYTHONPATH=src python -m earnings_call_risk_map fresh-clone-plan --format json --out examples/output/fresh_clone_plan.json",
    "PYTHONPATH=src python -m earnings_call_risk_map cheat-sheet --format markdown --out examples/output/command_cheat_sheet.md",
    "PYTHONPATH=src python -m earnings_call_risk_map doctor --format json --out examples/output/doctor.json",
    "PYTHONPATH=src python -m earnings_call_risk_map doctor --format markdown --out examples/output/doctor.md",
    "PYTHONPATH=src python -m earnings_call_risk_map audit",
    "PYTHONPATH=src python -m earnings_call_risk_map release-assets",
    "PYTHONPATH=src python -m earnings_call_risk_map manifest --out release_manifest.json",
    "PYTHONPATH=src python -m earnings_call_risk_map maturity-evidence --out-dir reports/maturity",
    "python scripts/privacy_scan.py",
    "git diff --check",
)
FRESH_CLONE_COMMANDS = (
    "git clone <repo-url> earnings-call-risk-map",
    "cd earnings-call-risk-map",
    "python -m venv .venv",
    "source .venv/bin/activate",
    "python -m pip install --upgrade pip",
    "PYTHONPATH=src python -m earnings_call_risk_map version",
    "PYTHONPATH=src python -m unittest discover -s tests",
    "PYTHONPATH=src python scripts/selfcheck.py",
    "python -m pip install .",
    "earnings-call-risk-map version",
)
ARTIFACT_GLOBS = (
    "examples/output/*.json",
    "examples/output/*.md",
    "examples/output/*.html",
    "examples/output/*.svg",
    "examples/output/*.jsonl",
    "examples/output/**/*.json",
    "examples/output/**/*.md",
    "examples/output/**/*.html",
    "docs/assets/*.svg",
    "release_manifest.json",
)
SKILL_PATH = "skills/agent/earnings-call-risk-map/SKILL.md"
REVIEW_TEMPLATE_PATH = "reports/reviews/release-readiness-review.md"
RELEASE_ASSETS = (
    "README.md",
    "CHANGELOG.md",
    "docs/release-notes-v0.8.0.md",
    "docs/comparison-to-spreadsheets.md",
    "examples/playbooks/README.md",
    "examples/playbooks/quarterly-review.md",
    "examples/playbooks/catalyst-check-in.md",
    "examples/playbooks/post-earnings-thesis-refresh.md",
    "docs/release-readiness.md",
    "docs/reviewer-evidence.md",
    "docs/distribution.md",
    "docs/troubleshooting.md",
    "docs/security-and-privacy.md",
    "docs/non-advice-boundary.md",
    "docs/pages-demo.md",
    "docs/gallery.md",
    "docs/public-case-study.md",
    "docs/schema-authoring-reference.md",
    "docs/schema-reference.json",
    "docs/assets/showcase-dashboard-preview.svg",
    "examples/output/demo_dashboard.html",
    "examples/output/energy_infrastructure_dashboard.html",
    "examples/output/semiconductor_equipment_dashboard.html",
    "examples/output/semiconductor_equipment_report/report.md",
    "examples/output/semiconductor_equipment_report/dashboard/dashboard.html",
    "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.json",
    "examples/output/semiconductor_equipment_report/fixture_summary/fixture_summary.md",
    "examples/output/semiconductor_equipment_report/review_queue/review_queue.json",
    "examples/output/semiconductor_equipment_report/review_queue/review_queue.md",
    "examples/output/semiconductor_equipment_report/snapshot/snapshot.json",
    "examples/output/public_apple_static_case_study_dashboard.html",
    "examples/output/showcase_dashboard_preview.svg",
    "examples/output/demo_report.md",
    "examples/output/energy_infrastructure_report.md",
    "examples/output/semiconductor_equipment_report.md",
    "examples/output/public_apple_static_case_study_report.md",
    "examples/output/demo_review_queue.md",
    "examples/output/energy_infrastructure_review_queue.md",
    "examples/output/semiconductor_equipment_review_queue.md",
    "examples/output/public_apple_static_case_study_review_queue.md",
    "examples/output/demo_review_queue_items.jsonl",
    "examples/output/demo_snapshot.json",
    "examples/output/demo_prior_snapshot.json",
    "examples/output/energy_infrastructure_snapshot.json",
    "examples/output/semiconductor_equipment_snapshot.json",
    "examples/output/public_apple_static_case_study_snapshot.json",
    "examples/output/demo_compare.md",
    "examples/output/demo_compare.json",
    "examples/output/package_audit.md",
    "examples/output/package_audit.json",
    "examples/output/agent_workflow.md",
    "examples/output/agent_workflow.json",
    "examples/output/doctor.md",
    "examples/output/doctor.json",
    "examples/output/examples_index.md",
    "examples/output/examples_index.json",
    "examples/output/case_study_map.md",
    "examples/output/case_study_map.json",
    "examples/output/command_cheat_sheet.md",
    "examples/output/command_cheat_sheet.json",
    "examples/output/command_cheatsheet.md",
    "examples/output/command_cheatsheet.json",
    "examples/output/risk_language_taxonomy.md",
    "examples/output/source_boundary_evidence.md",
    "examples/output/source_boundary_evidence.json",
    "examples/output/template_catalog.md",
    "examples/output/template_catalog.json",
    "examples/output/schema_authoring_reference.md",
    "examples/output/schema_authoring_reference.json",
    "examples/output/playbooks.md",
    "examples/output/playbooks.json",
    "examples/output/promotion_pack.md",
    "examples/output/promotion_pack.json",
    "examples/output/publication_checklist.md",
    "examples/output/publication_checklist.json",
    "examples/output/data_entry_checklist.md",
    "examples/output/data_entry_checklist.json",
    "examples/output/demo_screenshot_guide.md",
    "examples/output/demo_screenshot_guide.json",
    "examples/output/fresh_clone_plan.md",
    "examples/output/fresh_clone_plan.json",
    "examples/output/playbook_output_examples.md",
    "examples/output/playbook_output_examples.json",
    "examples/output/handoff_packet.md",
    "examples/output/handoff_packet.json",
    "examples/output/handoff_packet_examples.md",
    "examples/output/handoff_packet_examples.json",
    "examples/output/release_manifest.json",
    "release_manifest.json",
    "reports/maturity/maturity_evidence.md",
    "reports/maturity/maturity_evidence.json",
    "reports/reviews/2026-05-17-v0.8.0-internal-review.md",
    "reports/reviews/2026-05-17-v0.8.0-final-review.md",
    SKILL_PATH,
    REVIEW_TEMPLATE_PATH,
)
MATURITY_SCORES = {
    "source": "reports/reviews/2026-05-17-v0.8.0-final-review.md",
    "review_date": "2026-05-17",
    "overall": "94/100",
    "level": "L4+",
    "release_gate": "PASS for owner-controlled v0.8.0 release after final worktree inspection",
    "promotion_gate": "PASS for small-scope public promotion after release owner approval",
    "categories": {
        "product_clarity": "15/15",
        "reproducibility": "15/15",
        "user_value": "19/20",
        "evidence_quality": "15/15",
        "engineering_quality": "14/15",
        "showcase": "9/10",
        "risk_boundary": "7/10",
    },
    "four_role_review": {
        "product": "5/5 accept",
        "engineering": "5/5 accept",
        "cold_user": "4/5 accept",
        "risk": "4/5 accept for controlled promotion",
    },
}


def build_maturity_evidence(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    fixture_count = _fixture_count(base)
    release_asset_checklist = _release_asset_checklist(base)
    privacy_scan = _privacy_scan_status(base)
    latest_review_score = _latest_review_score()
    return {
        "name": "earnings-call-risk-map",
        "version": __version__,
        "command_count": len(COMMANDS),
        "fixture_count": fixture_count,
        "test_commands": list(TEST_COMMANDS),
        "verification_commands": list(VERIFICATION_COMMANDS),
        "fresh_clone_commands": list(FRESH_CLONE_COMMANDS),
        "artifact_paths": _artifact_paths(base),
        "release_assets": _existing_paths(base, RELEASE_ASSETS),
        "release_asset_checklist": release_asset_checklist,
        "maturity_scores": MATURITY_SCORES,
        "latest_review_score": latest_review_score,
        "skill": {
            "path": SKILL_PATH,
            "present": (base / SKILL_PATH).is_file(),
        },
        "review_template": {
            "path": REVIEW_TEMPLATE_PATH,
            "present": (base / REVIEW_TEMPLATE_PATH).is_file(),
        },
        "privacy_scan": privacy_scan,
        "evidence_summary": {
            "command_count": len(COMMANDS),
            "fixture_count": fixture_count,
            "release_asset_status": release_asset_checklist["status"],
            "release_assets_present": release_asset_checklist["present_count"],
            "release_assets_expected": release_asset_checklist["expected_count"],
            "privacy_scan_status": privacy_scan["status"],
            "latest_review_score": latest_review_score["overall"],
            "latest_review_source": latest_review_score["source"],
        },
    }


def write_maturity_evidence(out_dir: str | Path, root: str | Path = ".") -> dict[str, Path]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    evidence = build_maturity_evidence(root)
    json_path = target / "maturity_evidence.json"
    md_path = target / "maturity_evidence.md"
    json_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_maturity_evidence_markdown(evidence), encoding="utf-8")
    return {"json": json_path, "markdown": md_path}


def render_maturity_evidence_markdown(evidence: dict[str, Any]) -> str:
    privacy = evidence["privacy_scan"]
    skill = evidence["skill"]
    template = evidence["review_template"]
    lines = [
        "# Maturity Evidence Bundle",
        "",
        f"- Package: `{evidence['name']}`",
        f"- Version: `{evidence['version']}`",
        f"- Commands: {evidence['command_count']}",
        f"- Fixtures: {evidence['fixture_count']}",
        f"- Skill path: `{skill['path']}` ({'present' if skill['present'] else 'missing'})",
        f"- Review template: `{template['path']}` ({'present' if template['present'] else 'missing'})",
        f"- Release assets: {evidence['release_asset_checklist']['status']} "
        f"({evidence['release_asset_checklist']['present_count']}/"
        f"{evidence['release_asset_checklist']['expected_count']} present)",
        f"- Privacy scan: {privacy['status']} (`{privacy['command']}`)",
        f"- Latest review score: {evidence['latest_review_score']['overall']} "
        f"({evidence['latest_review_score']['source']})",
        "",
        f"> {SAFETY_NOTICE}",
        "",
        "## Test Commands",
        "",
    ]
    lines.extend(f"- `{command}`" for command in evidence["test_commands"])
    lines.extend(["", "## Verification Commands", ""])
    lines.extend(f"- `{command}`" for command in evidence["verification_commands"])
    lines.extend(["", "## Fresh Clone Procedure", ""])
    lines.extend(f"{index}. `{command}`" for index, command in enumerate(evidence["fresh_clone_commands"], start=1))
    lines.extend(["", "## Maturity Scores", ""])
    scores = evidence["maturity_scores"]
    lines.extend(
        [
            f"- Source: `{scores['source']}`",
            f"- Review date: `{scores['review_date']}`",
            f"- Overall: `{scores['overall']}`",
            f"- Level: `{scores['level']}`",
            f"- Release gate: `{scores['release_gate']}`",
            f"- Promotion gate: `{scores['promotion_gate']}`",
        ]
    )
    lines.extend(["", "### Scorecard", ""])
    lines.extend(f"- {name.replace('_', ' ').title()}: `{score}`" for name, score in scores["categories"].items())
    lines.extend(["", "### Four-Role Review", ""])
    lines.extend(f"- {name.replace('_', ' ').title()}: `{score}`" for name, score in scores["four_role_review"].items())
    lines.extend(["", "## Release Assets", ""])
    if evidence["release_assets"]:
        lines.extend(f"- `{path}`" for path in evidence["release_assets"])
    else:
        lines.append("- None")
    lines.extend(["", "## Artifact Paths", ""])
    if evidence["artifact_paths"]:
        lines.extend(f"- `{path}`" for path in evidence["artifact_paths"])
    else:
        lines.append("- None")
    lines.extend(["", "## Privacy Scan", ""])
    lines.append(f"- Exit code: `{privacy['exit_code']}`")
    if privacy["stdout"]:
        lines.append(f"- Output: `{privacy['stdout']}`")
    if privacy["stderr"]:
        lines.append(f"- Error: `{privacy['stderr']}`")
    return "\n".join(lines) + "\n"


def maturity_evidence_json(root: str | Path = ".") -> str:
    return json.dumps(build_maturity_evidence(root), indent=2, sort_keys=True) + "\n"


def _artifact_paths(base: Path) -> list[str]:
    paths = set()
    for pattern in ARTIFACT_GLOBS:
        for path in base.glob(pattern):
            if path.is_file():
                paths.add(path.relative_to(base).as_posix())
    return sorted(paths)


def _existing_paths(base: Path, paths: tuple[str, ...]) -> list[str]:
    return [path for path in paths if (base / path).is_file()]


def _fixture_count(base: Path) -> int:
    return len([path for path in base.glob(FIXTURE_PATTERN) if path.is_file()])


def _release_asset_checklist(base: Path) -> dict[str, Any]:
    present = [path for path in RELEASE_ASSETS if (base / path).is_file()]
    missing = [path for path in RELEASE_ASSETS if not (base / path).is_file()]
    return {
        "status": "passed" if not missing else "failed",
        "expected_count": len(RELEASE_ASSETS),
        "present_count": len(present),
        "missing_count": len(missing),
        "missing_assets": missing,
    }


def _latest_review_score() -> dict[str, Any]:
    return {
        "source": MATURITY_SCORES["source"],
        "review_date": MATURITY_SCORES["review_date"],
        "overall": MATURITY_SCORES["overall"],
        "level": MATURITY_SCORES["level"],
        "release_gate": MATURITY_SCORES["release_gate"],
        "promotion_gate": MATURITY_SCORES["promotion_gate"],
    }


def _privacy_scan_status(base: Path) -> dict[str, Any]:
    command = [sys.executable, "scripts/privacy_scan.py"]
    script = base / "scripts/privacy_scan.py"
    if not script.is_file():
        return {
            "command": "python scripts/privacy_scan.py",
            "status": "missing",
            "exit_code": None,
            "stdout": "",
            "stderr": "scripts/privacy_scan.py is missing",
        }
    result = subprocess.run(command, cwd=base, text=True, capture_output=True, check=False)
    stdout = " ".join(result.stdout.split())
    stderr = " ".join(result.stderr.split())
    return {
        "command": "python scripts/privacy_scan.py",
        "status": "passed" if result.returncode == 0 else "failed",
        "exit_code": result.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
