#!/usr/bin/env python3
"""Check that generated official TP suite docs contain required sections."""
import sys

from _paths import SUITES


BASE = SUITES
REQUIRED = [
    "目的",
    "官方骨架",
    "前置条件",
    "验证流程",
    "TP Verdict",
    "当前本地证据",
    "受限",
]

def main() -> int:
    if not BASE.exists():
        print("no_suite_dir\t", BASE)
        return 1
    files = sorted(BASE.glob("*.md"))
    total = 0
    missing_total = 0
    missing_heading_count = 0
    for md in files:
        text = md.read_text(encoding="utf-8")
        missing = [header for header in REQUIRED if header not in text]
        missing_heading_count += len(missing)
        total += 1
        if missing:
            missing_total += 1
            print(f"{md.name}\tMISSING:" + ",".join(missing))
        else:
            print(f"{md.name}\tOK")
    print(f"SUMMARY total={total} incomplete={missing_total} missing_headings={missing_heading_count}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
