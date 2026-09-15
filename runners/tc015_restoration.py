#!/usr/bin/env python3
"""TC-015 restoration judgement engine.

TC-015 is split from "network/IMS restart recovery" into the official
restoration trigger that 34.229-1 can anchor: a 504 Server Time-out with the
3gpp-alternative-service body shall cause the UE to start initial registration.

This script is a field/behaviour verification harness, not a 36.523/34.229-1
conformance verdict.
"""

import argparse
import re
import sys


CODE_RE = re.compile(r"SIP/2\.0\s+(\d{3})", re.IGNORECASE)
INVITE_RE = re.compile(r"INVITE\s+sip:", re.IGNORECASE)
REGISTER_RE = re.compile(r"REGISTER\s+sip:", re.IGNORECASE)


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def has(line, needle):
    return needle.lower() in line.lower()


def check_tc015(text):
    lines = split_lines(text)

    invite_present = any(INVITE_RE.search(line) for line in lines)
    register_present = any(REGISTER_RE.search(line) for line in lines)

    # 34.229-1 12.2a / restoration body check
    has_504 = False
    has_p_asserted_identity = False
    has_ims_xml = False
    has_restoration = False
    has_action_initial_registration = False
    for line in lines:
        if CODE_RE.search(line) and "504" in line:
            has_504 = True
        if "P-Asserted-Identity" in line:
            has_p_asserted_identity = True
        if "application/3gpp-ims+xml" in line:
            has_ims_xml = True
        if "<type>" in line and "restoration" in line:
            has_restoration = True
        if "<action>" in line and "initial-registration" in line:
            has_action_initial_registration = True

    # The UE shall initiate an initial registration after the restoration trigger.
    last_504_idx = None
    for idx, line in enumerate(lines):
        if CODE_RE.search(line) and "504" in line:
            last_504_idx = idx
    register_after_504 = False
    if last_504_idx is not None:
        register_after_504 = any(
            REGISTER_RE.search(line) and idx > last_504_idx
            for idx, line in enumerate(lines)
        )

    checks = [
        ("INVITE present before restoration", invite_present, "invite=%s" % invite_present),
        ("504 response present", has_504, "has_504=%s" % has_504),
        ("P-Asserted-Identity in 504", has_p_asserted_identity, "p_asserted=%s" % has_p_asserted_identity),
        ("Content-Type 3gpp-ims+xml", has_ims_xml, "ims_xml=%s" % has_ims_xml),
        ("alternative-service type=restoration", has_restoration, "restoration=%s" % has_restoration),
        ("action=initial-registration", has_action_initial_registration, "action=%s" % has_action_initial_registration),
        ("initial REGISTER after 504", register_after_504, "register_after=%s" % register_after_504),
        ("stack still has REGISTER traffic", register_present, "any_register=%s" % register_present),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks, expected):
    ok = True
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))
        if expected is not None and is_ok != expected:
            ok = False
    return ok


def fixtures():
    base_pass = """[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0
Route: <sip:pcscf.ims.example.com;lr>
P-Asserted-Identity: <sip:pcscf.ims.example.com>
Content-Type: application/sdp
[MESSAGE] SIP/2.0 504 Server Time-out
P-Asserted-Identity: <sip:scscf.ims.example.com>
Content-Type: application/3gpp-ims+xml
<ims-3gpp version="1">
<alternative-service>
<type>restoration</type>
<action>initial-registration</action>
</alternative-service>
</ims-3gpp>
[MESSAGE] ACK sip:bob@ims.example.com SIP/2.0
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Expires: 600
"""
    fail_missing_trigger = base_pass.replace(
        "Content-Type: application/3gpp-ims+xml", "Content-Type: application/sdp"
    )
    fail_no_rereg = base_pass.replace(
        "[MESSAGE] REGISTER sip:ims.example.com SIP/2.0", "[MESSAGE] SUBSCRIBE sip:ims.example.com SIP/2.0"
    )
    return {
        "pass": (base_pass, "PASS"),
        "fail_missing_trigger": (fail_missing_trigger, "FAIL"),
        "fail_no_rereg": (fail_no_rereg, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc015(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-015 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
        render_checks(checks, None)
        if expected_bool != actual:
            failed = True
    if not failed:
        print("SELFCHECK PASS")
        return 0
    print("SELFCHECK FAIL")
    return 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selfcheck", action="store_true")
    parser.add_argument("--log")
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    if args.selfcheck:
        return run_selfcheck()
    if not args.log:
        parser.error("provide --log <sip-log> or --selfcheck")

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    actual, checks = check_tc015(text)
    expected_bool = (args.expect == "pass") if args.expect else None
    render_checks(checks, None)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
