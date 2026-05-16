#!/usr/bin/env python3
"""Generate the local maturity evidence bundle."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from earnings_call_risk_map.maturity import write_maturity_evidence  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate maturity evidence JSON and Markdown.")
    parser.add_argument("--out-dir", default="reports/maturity", help="Output directory")
    args = parser.parse_args()
    outputs = write_maturity_evidence(args.out_dir, ROOT)
    rel = os.path.relpath(outputs["json"].parent, ROOT)
    print(f"wrote maturity evidence bundle to {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
