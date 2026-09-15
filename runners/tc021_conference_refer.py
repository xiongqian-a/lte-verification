#!/usr/bin/env python3
"""TC-021 conference / REFER judgement engine.

TC-021 is anchored to TS 34.229-1 15.17 / 15.18 / 15.19 / 15.19a / 15.21
for the conference and call-transfer family. This script verifies the
field-level REFER / 202 / NOTIFY / isfocus flow from a SIP log.

This is a field/behaviour verification harness, not a 36.523/34.229-1
conformance verdict.
"""

import argparse
import re
import sys


INVITE_RE = re.compile(r"INVITE\s+sip:", re.IGNORECASE)
REFER_RE = re.compile(r"REFER\s+sip:", re.IGNORECASE)
NOTIFY_RE = re.compile(r"NOTIFY\s+sip:", re.IGNORECASE)
STATUS_RE = re.compile(r"SIP/2\.0\s+(\d{3})", re.IGNORECASE)


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def has(line, needle):
    return needle.lower() in line.lower()


def check_tc021(text):
    lines = split_lines(text)

    has_invite = any(INVITE_RE.search(line) for line in lines)
    has_refer = any(REFER_RE.search(line) for line in lines)
    has_refer_to = any(has(line, "Refer-To") for line in lines)
    has_isfocus = any(has(line, "isfocus") for line in lines)
    # 34.229-1 15.17/15.21 only require the Contact ;isfocus marker when the
    # test exercises conference creation/joining. For a REFER-to-single-user
    # transfer variant there is no conference focus to create, so the marker
    # is not applicable instead of a false FAIL.
    # The conference.c lines from pjsua's media bridge are not SIP-level
    # conference creation; only SIP URIs/contacts carrying conference focus
    # semantics should trigger the isfocus assertion.
    sip_conference_uri = re.compile(
        r"(sip:[^ >;\"]*(conf-factory|conference)[^ >;\"]*)",
        re.IGNORECASE,
    )
    conference_created = has_isfocus or any(
        sip_conference_uri.search(line) for line in lines
    )
    focus_ok = has_isfocus or not conference_created
    focus_detail = "isfocus=%s required=%s" % (has_isfocus, conference_created)

    has_202 = False
    has_notify_refer = False
    notify_idx = None
    has_notify_200 = False
    statuses = []
    pending_notify = False

    for idx, line in enumerate(lines):
        match = STATUS_RE.search(line)
        if match:
            statuses.append((idx, match.group(1), line))
            if match.group(1) == "202":
                has_202 = True
        if NOTIFY_RE.search(line):
            pending_notify = True
            if has(line, "Event: refer") or has(line, "event=refer"):
                has_notify_refer = True
                if notify_idx is None:
                    notify_idx = idx
        elif pending_notify and (has(line, "Event: refer") or has(line, "event=refer")):
            has_notify_refer = True
            if notify_idx is None:
                # The NOTIFY line is the most recent SIP request before this
                # header; use that nearest preceding NOTIFY index if possible.
                prev_notify = None
                for j in range(idx - 1, -1, -1):
                    if NOTIFY_RE.search(lines[j]):
                        prev_notify = j
                        break
                notify_idx = prev_notify

    if notify_idx is not None:
        has_notify_200 = any(
            idx > notify_idx and code == "200"
            for idx, code, _ in statuses
        )

    checks = [
        ("conference INVITE or call present", has_invite, "invite=%s" % has_invite),
        ("REFER present", has_refer, "refer=%s" % has_refer),
        ("Refer-To header present", has_refer_to, "refer_to=%s" % has_refer_to),
        ("202 Accepted present", has_202, "202=%s" % has_202),
        ("NOTIFY with event refer present", has_notify_refer, "notify_refer=%s" % has_notify_refer),
        ("200 OK after NOTIFY", has_notify_200, "notify_200=%s" % has_notify_200),
        ("focus marker isfocus present where expected", focus_ok, focus_detail),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks):
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


def fixtures():
    base_pass = """[MESSAGE] INVITE sip:conf-factory@ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:conf-factory@ims.example.com>
Call-ID: conf-1
[MESSAGE] SIP/2.0 200 OK
Contact: <sip:conf@ims.example.com>;isfocus
Call-ID: conf-1
[MESSAGE] ACK sip:conf@ims.example.com SIP/2.0
Call-ID: conf-1
[MESSAGE] REFER sip:bob@ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
Refer-To: <sip:conf@ims.example.com>
Event: refer
Call-ID: conf-1
[MESSAGE] SIP/2.0 202 Accepted
Call-ID: conf-1
[MESSAGE] NOTIFY sip:alice@ims.example.com SIP/2.0
Event: refer
Call-ID: conf-1
[MESSAGE] SIP/2.0 200 OK
Call-ID: conf-1
"""
    fail_no_refer = base_pass.replace(
        "[MESSAGE] REFER sip:bob@ims.example.com SIP/2.0",
        "[MESSAGE] NOTIFY sip:bob@ims.example.com SIP/2.0",
    )
    fail_no_notify = base_pass.replace(
        "[MESSAGE] NOTIFY sip:alice@ims.example.com SIP/2.0\nEvent: refer\nCall-ID: conf-1\n[MESSAGE] SIP/2.0 200 OK\nCall-ID: conf-1",
        "[MESSAGE] NOTIFY sip:alice@ims.example.com SIP/2.0\nEvent: reg\nCall-ID: conf-1\n[MESSAGE] SIP/2.0 200 OK\nCall-ID: conf-1",
    )
    pass_refer_transfer = base_pass.replace(
        "INVITE sip:conf-factory@ims.example.com SIP/2.0",
        "INVITE sip:bob@ims.example.com SIP/2.0",
    ).replace("conf-factory@ims.example.com", "carol@ims.example.com")
    pass_refer_transfer = pass_refer_transfer.replace(
        "Contact: <sip:conf@ims.example.com>;isfocus",
        "Contact: <sip:bob@ims.example.com>",
    ).replace(
        "Refer-To: <sip:conf@ims.example.com>",
        "Refer-To: <sip:carol@ims.example.com>",
    )
    return {
        "pass_conference_refer": (base_pass, "PASS"),
        "pass_refer_transfer_without_focus": (pass_refer_transfer, "PASS"),
        "fail_missing_refer": (fail_no_refer, "FAIL"),
        "fail_notify_not_refer_event": (fail_no_notify, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc021(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-021 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
    actual, checks = check_tc021(text)
    render_checks(checks)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
