#!/usr/bin/env python3
"""Check TC-005 dual-PDN evidence from a captured co1750 testbed run."""

import argparse
import sys
from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def window(text, since):
    if not since:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if since in line:
            return "\n".join(lines[index:])
    return ""


def evaluate(ue, mme, smf, sgwc):
    core = smf + "\n" + sgwc
    checks = [
        ("UE second default bearer request (APN=ims, EBI=6)",
         "Received Activate Default EPS Bearer Context Request (second PDN). APN=ims, bearer_id=6" in ue),
        ("UE registers second default bearer EBI=6",
         "Registered default EPS bearer EBI=6 for APN=ims." in ue),
        ("UE accepts second default bearer EBI=6",
         "Sending Activate Default EPS Bearer context accept (eps_bearer_id=6" in ue),
        ("UE receives dedicated bearer EBI=7 linked to EBI=6",
         "Received Activate Dedicated EPS bearer context request (eps_bearer_id=7, linked_bearer_id=6" in ue),
        ("UE accepts dedicated bearer EBI=7",
         "Sending Activate Dedicated EPS Bearer context accept (eps_bearer_id=7" in ue),
        ("MME allocates default bearer EBI=6", "EBI allocated [6]" in mme),
        ("MME allocates dedicated bearer EBI=7", "EBI allocated [7]" in mme),
        ("MME receives dedicated bearer accept TYPE=198", "TYPE:198" in mme),
        ("MME keeps two sessions", "Number of MME-Sessions is now 2" in mme),
        ("SMF assigns internet IPv4 PDN address", "APN[internet] IPv4[" in smf),
        ("SMF assigns ims IPv4 PDN address", "APN[ims] IPv4[" in smf),
        ("SGW-C completes Create Bearer Response", "Create Bearer Response" in sgwc),
    ]
    forbidden = [
        ("UE has no linked-bearer lookup failure",
         "No linked default EPS bearer found" in ue),
        ("MME has no single-session assertion",
         "There should only be one SESSION" in mme),
        ("Core has no missing Create Bearer Response",
         "No Create Bearer Response" in core),
    ]
    restricted = (
        "No IPv6 subnet" in core
        or "APN[internet] IPv4[10.45.0.2] IPv6[]" in smf
        or "APN[ims] IPv4[10.46.0.2] IPv6[]" in smf
    )
    return checks, forbidden, restricted


def report(checks, forbidden, restricted):
    failed = False
    for label, ok in checks:
        print("[%s] %s" % ("OK" if ok else "BAD", label))
        failed = failed or not ok
    for label, bad in forbidden:
        print("[%s] %s" % ("BAD" if bad else "OK", label))
        failed = failed or bad

    if restricted:
        print("[WARN] IPv4 dual-PDN behavior observed; IPv6/dual-stack assignment is RESTRICTED")
        print("OFFICIAL_VERDICT: RESTRICTED (requires SS/consistency instrument)")
    else:
        print("OFFICIAL_VERDICT: RESTRICTED (requires SS/consistency instrument)")

    if failed:
        print("LOCAL_BEHAVIOR: FAIL")
        print("RESULT: FAIL")
        return 1
    if restricted:
        print("LOCAL_BEHAVIOR: PASS")
        print("RESULT: LIMITED_PASS")
        return 0
    print("LOCAL_BEHAVIOR: PASS")
    print("RESULT: PASS")
    return 0


def selfcheck():
    ue = "\n".join([
        "Received Activate Default EPS Bearer Context Request (second PDN). APN=ims, bearer_id=6",
        "Registered default EPS bearer EBI=6 for APN=ims.",
        "Sending Activate Default EPS Bearer context accept (eps_bearer_id=6, proc_id=2)",
        "Received Activate Dedicated EPS bearer context request (eps_bearer_id=7, linked_bearer_id=6, proc_id=0)",
        "Sending Activate Dedicated EPS Bearer context accept (eps_bearer_id=7, proc_id=0)",
    ])
    mme = "\n".join([
        "EBI allocated [6]",
        "EBI allocated [7]",
        "TYPE:198",
        "Number of MME-Sessions is now 2",
    ])
    smf = "\n".join([
        "APN[internet] IPv4[10.45.0.2] IPv6[]",
        "APN[ims] IPv4[10.46.0.2] IPv6[]",
        "No IPv6 subnet or set to /63 or /64, only IPv4 assigned",
    ])
    sgwc = "Create Bearer Response"

    checks, forbidden, restricted = evaluate(ue, mme, smf, sgwc)
    pass_ok = all(ok for _, ok in checks) and not any(bad for _, bad in forbidden) and restricted

    bad_ue = ue.replace("Registered default EPS bearer EBI=6 for APN=ims.", "")
    bad_checks, _, _ = evaluate(bad_ue, mme, smf, sgwc)
    fail_ok = not all(ok for _, ok in bad_checks)

    if pass_ok and fail_ok:
        print("SELFCHECK PASS: TC-005 dual-PDN checker accepts conformant fixture and rejects missing EBI=6 registration")
        return 0
    print("SELFCHECK FAIL: fixture behavior mismatch")
    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ue")
    parser.add_argument("--mme")
    parser.add_argument("--smf")
    parser.add_argument("--sgwc")
    parser.add_argument("--ue-since")
    parser.add_argument("--core-since")
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()

    if args.selfcheck:
        return selfcheck()
    if not all([args.ue, args.mme, args.smf, args.sgwc]):
        parser.error("--ue, --mme, --smf and --sgwc are required unless --selfcheck is used")

    ue = window(read(args.ue), args.ue_since)
    mme = window(read(args.mme), args.core_since)
    smf = window(read(args.smf), args.core_since)
    sgwc = window(read(args.sgwc), args.core_since)
    if not ue or not mme or not smf or not sgwc:
        print("FAIL evidence window start marker not found")
        return 1
    checks, forbidden, restricted = evaluate(ue, mme, smf, sgwc)
    return report(checks, forbidden, restricted)


if __name__ == "__main__":
    sys.exit(main())
