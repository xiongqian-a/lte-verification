#!/usr/bin/env python3
"""Local verdict for TC-001 UE-side IMS APN PDN evidence from nas_test log."""
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", default=None)
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()
    if args.selfcheck:
        print("SELFCHECK PASS: TC-001 verdict script is importable and arg-validating")
        return 0
    if not args.log:
        parser.error("--log is required unless --selfcheck is used")
    text = Path(args.log).read_text(encoding="utf-8", errors="replace")
    required = [
        "PDN Connectivity Request with APN ims",
        "Sending IMS PDN connectivity request (APN=ims)",
        "IMS event: Pdn_Event IMS-PDN-REQUESTED (apn=ims qci=5)",
        "Sending Activate Dedicated EPS Bearer context accept",
    ]
    missing = [needle for needle in required if needle not in text]
    if missing:
        print("FAIL missing=%s" % (", ".join(missing)))
        return 1
    print("PASS IMS_APN_PDN_UE_SIDE nas_test evidence found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
