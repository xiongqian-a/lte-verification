#!/usr/bin/env python3
"""TC-021 conference-join subset checker for co1750 + FreeSWITCH logs.

This is NOT a conformance verdict. It checks the field-level evidence that
two UAs registered via the co1750 IMS testbed, both sent INVITE to the
FreeSWITCH conference URI sip:888@..., both reached CONFIRMED, FreeSWITCH
listed the conference with 2 members, and both left with a 200/BYE exchange.
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def check(paths):
    list_text = read(paths.list)
    ua1 = read(paths.ua1)
    ua2 = read(paths.ua2)
    console = read(paths.console)

    checks = []

    two_members = re.search(
        r"Conference\s+888\s+\(2\s+members", list_text,
        re.IGNORECASE,
    ) is not None
    checks.append(("FreeSWITCH list shows Conference 888 with 2 members", two_members))

    for name, txt in (("UA1", ua1), ("UA2", ua2)):
        confirmed = "call state: CONFIRMED" in txt
        invite_888 = "INVITE sip:888@ims.mnc001.mcc001.3gppnetwork.org" in txt
        bye = re.search(r"\bBYE\b", txt) is not None
        bye_200 = re.search(r"200/BYE", txt) is not None
        checks.append(("%s CONFIRMED and INVITE to 888" % name, confirmed and invite_888))
        checks.append(("%s BYE + 200/BYE" % name, bye and bye_200))

    fs_join = console.count("conference(888@default)") >= 2
    fs_normal_clear = "NORMAL_CLEARING" in console
    checks.append(("FreeSWITCH executes conference(888@default) twice", fs_join))
    checks.append(("FreeSWITCH shows NORMAL_CLEARING", fs_normal_clear))

    all_ok = all(ok for _, ok in checks)
    for name, ok in checks:
        print("  [%s ] %s" % ("OK" if ok else "BAD", name))
    print("RESULT: %s" % ("PASS" if all_ok else "FAIL"))
    return 0 if all_ok else 1


def run_selfcheck():
    with tempfile.TemporaryDirectory(prefix="tc021-selfcheck-") as tmp:
        root = Path(tmp)
        (root / "list.txt").write_text(
            "Conference 888 (2 members)\n", encoding="utf-8"
        )
        for name in ("ua1.txt", "ua2.txt"):
            (root / name).write_text(
                "call state: CONFIRMED\n"
                "INVITE sip:888@ims.mnc001.mcc001.3gppnetwork.org\n"
                "BYE\n"
                "200/BYE\n",
                encoding="utf-8",
            )
        (root / "console.txt").write_text(
            "conference(888@default)\n"
            "conference(888@default)\n"
            "NORMAL_CLEARING\n",
            encoding="utf-8",
        )
        args = argparse.Namespace(
            list=str(root / "list.txt"),
            ua1=str(root / "ua1.txt"),
            ua2=str(root / "ua2.txt"),
            console=str(root / "console.txt"),
        )
        rc = check(args)
        print(
            "SELFCHECK %s: conference log checker exercised with synthetic PASS fixture"
            % ("PASS" if rc == 0 else "FAIL")
        )
        return rc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list")
    parser.add_argument("--ua1")
    parser.add_argument("--ua2")
    parser.add_argument("--console")
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()
    if args.selfcheck:
        return run_selfcheck()
    missing = [name for name in ("list", "ua1", "ua2", "console") if not getattr(args, name)]
    if missing:
        parser.error("the following arguments are required: --" + ", --".join(missing))
    return check(args)


if __name__ == "__main__":
    sys.exit(main())
