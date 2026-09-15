#!/usr/bin/env python3
"""TC-019 MT call judgement engine.

TC-019 is an internal MT/Voice call test case anchored to TS 34.229-1
12.13 / 12.13a family for field-level verification. The script checks the
message flow that can be read from a SIP log: MT INVITE, ringing or session
progress, 200 OK, ACK, BYE and final 200.

This is a field/behaviour verification harness, not a 36.523/34.229-1
conformance verdict.
"""

import argparse
import re
import sys


INVITE_RE = re.compile(r"INVITE\s+sip:", re.IGNORECASE)
ACK_RE = re.compile(r"ACK\s+sip:", re.IGNORECASE)
BYE_RE = re.compile(r"BYE\s+sip:", re.IGNORECASE)
STATUS_RE = re.compile(r"SIP/2\.0\s+(\d{3})", re.IGNORECASE)


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def has(line, needle):
    return needle.lower() in line.lower()


def check_tc019(text):
    lines = split_lines(text)

    has_invite = any(INVITE_RE.search(line) for line in lines)
    has_ack = any(ACK_RE.search(line) for line in lines)
    has_bye = any(BYE_RE.search(line) for line in lines)

    statuses = []
    for idx, line in enumerate(lines):
        match = STATUS_RE.search(line)
        if match:
            statuses.append((idx, match.group(1), line))

    has_180 = any(code == "180" for _, code, _ in statuses)
    has_183 = any(code == "183" for _, code, _ in statuses)
    has_200 = any(code == "200" for _, code, _ in statuses)
    has_200_after_bye = False
    bye_idx = None
    for idx, line in enumerate(lines):
        if BYE_RE.search(line):
            bye_idx = idx
            break
    if bye_idx is not None:
        has_200_after_bye = any(
            idx > bye_idx and code == "200"
            for idx, code, _ in statuses
        )

    has_sdp = any(has(line, "application/sdp") for line in lines)
    accepted_progress = has_180 or has_183

    checks = [
        ("MT INVITE present", has_invite, "invite=%s" % has_invite),
        ("ringing or session progress", accepted_progress, "180=%s 183=%s" % (has_180, has_183)),
        ("200 OK present", has_200, "200=%s" % has_200),
        ("ACK present", has_ack, "ack=%s" % has_ack),
        ("BYE present", has_bye, "bye=%s" % has_bye),
        ("200 OK after BYE", has_200_after_bye, "bye_200=%s" % has_200_after_bye),
        ("SDP content exchanged", has_sdp, "sdp=%s" % has_sdp),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks):
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


def fixtures():
    base_pass = """[MESSAGE] INVITE sip:alice@ims.example.com SIP/2.0
From: <sip:bob@ims.example.com>
To: <sip:alice@ims.example.com>
Call-ID: mt-call-1@ims.example.com
CSeq: 2 INVITE
Content-Type: application/sdp

v=0
m=audio 40000 RTP/AVP 96
[MESSAGE] SIP/2.0 180 Ringing
Call-ID: mt-call-1@ims.example.com
[MESSAGE] SIP/2.0 200 OK
Call-ID: mt-call-1@ims.example.com
Content-Type: application/sdp
[MESSAGE] ACK sip:bob@ims.example.com SIP/2.0
Call-ID: mt-call-1@ims.example.com
[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0
Call-ID: mt-call-1@ims.example.com
[MESSAGE] SIP/2.0 200 OK
Call-ID: mt-call-1@ims.example.com
"""
    fail_no_bye = base_pass.replace(
        "[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0",
        "[MESSAGE] SUBSCRIBE sip:alice@ims.example.com SIP/2.0",
    )
    fail_no_ring = base_pass.replace(
        "[MESSAGE] SIP/2.0 180 Ringing",
        "[MESSAGE] SIP/2.0 183 Session Progress",
    ).replace(
        "[MESSAGE] SIP/2.0 183 Session Progress",
        "[MESSAGE] SIP/2.0 480 Temporarily Unavailable",
    )
    return {
        "pass_mt_call": (base_pass, "PASS"),
        "fail_no_bye": (fail_no_bye, "FAIL"),
        "fail_no_progress": (fail_no_ring, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc019(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-019 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
        render_checks(checks)
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
    actual, checks = check_tc019(text)
    render_checks(checks)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
