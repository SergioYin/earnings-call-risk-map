"""Fresh-clone verification plan rendering."""

from __future__ import annotations

import json
from typing import Any

from .models import SAFETY_NOTICE
from .version import __version__

ASSUMPTIONS = (
    "Shell: bash-compatible shell on Linux or macOS.",
    "`python` resolves to Python 3.9 or newer.",
    (
        "Network is needed only for `git clone` and optional `pip` upgrade/install steps. "
        "Package commands themselves are local-file only."
    ),
    "Replace `<repo-url>` with the review source URL or local bare repository path.",
)

COMMANDS = (
    "set -euo pipefail",
    "",
    "git clone <repo-url> earnings-call-risk-map",
    "cd earnings-call-risk-map",
    "",
    "python -m venv .venv",
    ". .venv/bin/activate",
    "python -m pip install --upgrade pip",
    "python -m pip install -e .",
    "",
    "mkdir -p verification/fresh-clone",
    "",
    "earnings-call-risk-map version | tee verification/fresh-clone/version.txt",
    "PYTHONPATH=src python -m unittest discover -s tests | tee verification/fresh-clone/unittest.txt",
    "PYTHONPATH=src python scripts/selfcheck.py | tee verification/fresh-clone/selfcheck.txt",
    "",
    "earnings-call-risk-map demo --out-dir verification/fresh-clone/demo",
    (
        "earnings-call-risk-map analyze examples/input/demo_company.json \\\n"
        "  --json-out verification/fresh-clone/demo_company_snapshot.json \\\n"
        "  --md-out verification/fresh-clone/demo_company_report.md \\\n"
        "  --html-out verification/fresh-clone/demo_company_dashboard.html"
    ),
    (
        "earnings-call-risk-map review-queue examples/input/demo_company.json \\\n"
        "  --json-out verification/fresh-clone/demo_company_review_queue.json \\\n"
        "  --md-out verification/fresh-clone/demo_company_review_queue.md"
    ),
    (
        "earnings-call-risk-map compare \\\n"
        "  verification/fresh-clone/demo/demo_prior_snapshot.json \\\n"
        "  verification/fresh-clone/demo/demo_snapshot.json \\\n"
        "  --json-out verification/fresh-clone/demo_compare.json \\\n"
        "  --md-out verification/fresh-clone/demo_compare.md"
    ),
    "earnings-call-risk-map audit --format json --out verification/fresh-clone/package_audit.json",
    "earnings-call-risk-map doctor --format json --out verification/fresh-clone/doctor.json",
    "earnings-call-risk-map release-assets --format json --out verification/fresh-clone/release_assets.json",
    "earnings-call-risk-map manifest --out verification/fresh-clone/release_manifest.json",
    "earnings-call-risk-map maturity-evidence --out-dir verification/fresh-clone/maturity",
    "",
    "python scripts/privacy_scan.py | tee verification/fresh-clone/privacy_scan.txt",
    "git diff --check | tee verification/fresh-clone/git_diff_check.txt",
    (
        "find verification/fresh-clone -maxdepth 3 -type f | sort | "
        "tee verification/fresh-clone/artifact_inventory.txt"
    ),
)

EXPECTED_COMMAND_EVIDENCE = (
    {
        "path": "verification/fresh-clone/version.txt",
        "expectation": f"contains exactly `{__version__}`",
    },
    {
        "path": "verification/fresh-clone/unittest.txt",
        "expectation": "contains `OK` and a `Ran ... tests` line",
    },
    {
        "path": "verification/fresh-clone/selfcheck.txt",
        "expectation": (
            "contains selfcheck section headers such as `== unit tests ==`, `== demo ==`, "
            "`== audit ==`, `== release assets ==`, `== privacy scan ==`, and `selfcheck passed`"
        ),
    },
    {
        "path": "verification/fresh-clone/privacy_scan.txt",
        "expectation": "reports the privacy scan status without credential or network findings",
    },
    {
        "path": "verification/fresh-clone/git_diff_check.txt",
        "expectation": "empty file, because `git diff --check` should produce no whitespace warnings",
    },
    {
        "path": "verification/fresh-clone/artifact_inventory.txt",
        "expectation": "sorted list of generated evidence files under `verification/fresh-clone`",
    },
)

DIRECT_ARTIFACTS = (
    "verification/fresh-clone/demo_company_snapshot.json",
    "verification/fresh-clone/demo_company_report.md",
    "verification/fresh-clone/demo_company_dashboard.html",
    "verification/fresh-clone/demo_company_review_queue.json",
    "verification/fresh-clone/demo_company_review_queue.md",
    "verification/fresh-clone/demo_compare.json",
    "verification/fresh-clone/demo_compare.md",
    "verification/fresh-clone/package_audit.json",
    "verification/fresh-clone/doctor.json",
    "verification/fresh-clone/release_assets.json",
    "verification/fresh-clone/release_manifest.json",
    "verification/fresh-clone/maturity/maturity_evidence.json",
    "verification/fresh-clone/maturity/maturity_evidence.md",
)

DEMO_ARTIFACTS = (
    "verification/fresh-clone/demo/demo_snapshot.json",
    "verification/fresh-clone/demo/demo_report.md",
    "verification/fresh-clone/demo/demo_dashboard.html",
    "verification/fresh-clone/demo/demo_review_queue.json",
    "verification/fresh-clone/demo/demo_review_queue.md",
    "verification/fresh-clone/demo/demo_review_queue_items.jsonl",
    "verification/fresh-clone/demo/demo_prior_snapshot.json",
    "verification/fresh-clone/demo/demo_compare.json",
    "verification/fresh-clone/demo/demo_compare.md",
    "verification/fresh-clone/demo/package_audit.json",
    "verification/fresh-clone/demo/doctor.json",
    "verification/fresh-clone/demo/release_manifest.json",
)

JSON_CHECK_COMMANDS = (
    "python -m json.tool verification/fresh-clone/demo_company_snapshot.json >/dev/null",
    "python -m json.tool verification/fresh-clone/demo_company_review_queue.json >/dev/null",
    "python -m json.tool verification/fresh-clone/demo_compare.json >/dev/null",
    "python -m json.tool verification/fresh-clone/package_audit.json >/dev/null",
    "python -m json.tool verification/fresh-clone/doctor.json >/dev/null",
    "python -m json.tool verification/fresh-clone/release_assets.json >/dev/null",
    "python -m json.tool verification/fresh-clone/release_manifest.json >/dev/null",
    "python -m json.tool verification/fresh-clone/maturity/maturity_evidence.json >/dev/null",
)

CONTENT_SIGNALS = (
    "`doctor.json`: `status` is `passed`, `workflow_files_absent` is `true`, and `version` matches the package.",
    (
        "`package_audit.json`: `local_only.status` is `passed`, `network_required` is `false`, "
        "`credentials_required` is `false`, and `has_workflow_files` is `false`."
    ),
    "`release_assets.json`: `missing_count` is `0`.",
    (
        "`demo_company_snapshot.json`: includes ticker `EXM`, source boundaries, stale/static badges, "
        "and the educational non-advice safety notice."
    ),
    "`demo_company_review_queue.json`: includes stale, missing-evidence, or high-impact review items.",
    "`maturity_evidence.json`: records generated maturity evidence paths and release-review context.",
)

FAILURE_TRIAGE = (
    "If `python -m pip install -e .` fails, confirm the clone includes `pyproject.toml` and Python is 3.9 or newer.",
    (
        "If `release-assets` reports missing files, run `PYTHONPATH=src python scripts/selfcheck.py` "
        "and review missing paths in `verification/fresh-clone/release_assets.json`."
    ),
    (
        "If generated files differ from a committed checkout, confirm you are verifying the intended tag or branch "
        "before treating the difference as a release issue."
    ),
)


def build_fresh_clone_plan() -> dict[str, Any]:
    return {
        "artifact_type": "fresh_clone_verification_plan",
        "name": "earnings-call-risk-map",
        "version": __version__,
        "source_doc": "docs/fresh-clone-verification.md",
        "purpose": (
            "Local evidence that a clean clone imports, tests, generates artifacts, "
            "and keeps local-only boundaries."
        ),
        "safety_notice": SAFETY_NOTICE,
        "assumptions": list(ASSUMPTIONS),
        "commands": list(COMMANDS),
        "expected_command_evidence": [dict(item) for item in EXPECTED_COMMAND_EVIDENCE],
        "expected_generated_artifacts": {
            "direct": list(DIRECT_ARTIFACTS),
            "demo_bundle": list(DEMO_ARTIFACTS),
        },
        "json_check_commands": list(JSON_CHECK_COMMANDS),
        "expected_content_signals": list(CONTENT_SIGNALS),
        "failure_triage": list(FAILURE_TRIAGE),
    }


def fresh_clone_plan_json() -> str:
    return json.dumps(build_fresh_clone_plan(), indent=2, sort_keys=True) + "\n"


def fresh_clone_plan_markdown() -> str:
    plan = build_fresh_clone_plan()
    lines = [
        "# Fresh Clone Verification Plan",
        "",
        plan["purpose"],
        "",
        f"> {plan['safety_notice']}",
        "",
        f"- Package: `{plan['name']}`",
        f"- Version: `{plan['version']}`",
        f"- Source doc: `{plan['source_doc']}`",
        "",
        "## Assumptions",
        "",
    ]
    lines.extend(f"- {assumption}" for assumption in plan["assumptions"])
    lines.extend(["", "## Exact Commands", "", "```bash"])
    lines.extend(plan["commands"])
    lines.extend(["```", "", "## Expected Command Evidence", ""])
    lines.extend(
        f"- `{item['path']}`: {item['expectation']}"
        for item in plan["expected_command_evidence"]
    )
    lines.extend(["", "## Expected Generated Artifacts", "", "### Direct Artifacts", ""])
    lines.extend(f"- `{path}`" for path in plan["expected_generated_artifacts"]["direct"])
    lines.extend(["", "### Demo Bundle", ""])
    lines.extend(f"- `{path}`" for path in plan["expected_generated_artifacts"]["demo_bundle"])
    lines.extend(["", "## Expected JSON Checks", "", "```bash"])
    lines.extend(plan["json_check_commands"])
    lines.extend(["```", "", "Expected content signals:", ""])
    lines.extend(f"- {signal}" for signal in plan["expected_content_signals"])
    lines.extend(["", "## Failure Triage", ""])
    lines.extend(f"- {item}" for item in plan["failure_triage"])
    return "\n".join(lines) + "\n"
