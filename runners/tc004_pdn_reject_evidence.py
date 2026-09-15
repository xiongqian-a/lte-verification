#!/usr/bin/env python3
"""Local verdict for TC-004 PDN REJECT state/backoff evidence from nas_test log."""
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", default=None)
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()
    if args.selfcheck:
        print("SELFCHECK PASS: TC-004 verdict script is importable and arg-validating")
        return 0
    if not args.log:
        parser.error("--log is required unless --selfcheck is used")
    text = Path(args.log).read_text(encoding="utf-8", errors="replace")
    required = [
        "TC-004 test hook: PDN connectivity PROCEDURE TRANSACTION PENDING (pti=1), T3482 running",
        "PDN connectivity reject: pti=1 cause=0x20 state=INACTIVE t3482_stopped=true backoff_ms=720000",
    ]
    missing = [needle for needle in required if needle not in text]
    if missing:
        print("FAIL missing=%s" % (", ".join(missing)))
        return 1
    print("PASS PDN_REJECT_STATE_T3482_BACKOFF nas_test evidence found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
