#!/usr/bin/env python3
"""TC-020 call hold / retrieve judgement engine.

TC-020 is anchored to TS 34.229-1 15.11 (MO) / 15.12 (MT) Call Hold
without announcement. This engine verifies the field-level SDP direction
and mid-dialog signalling from a SIP log. It is not a conformance verdict.
"""

import argparse
import re
import sys


INVITE_RE = re.compile(r"INVITE\s+sip:", re.IGNORECASE)
UPDATE_RE = re.compile(r"UPDATE\s+sip:", re.IGNORECASE)
ACK_RE = re.compile(r"ACK\s+sip:", re.IGNORECASE)
BYE_RE = re.compile(r"BYE\s+sip:", re.IGNORECASE)
STATUS_RE = re.compile(r"SIP/2\.0\s+(\d{3})", re.IGNORECASE)
SEND_ONLY_RE = re.compile(r"a=sendonly", re.IGNORECASE)
INACTIVE_RE = re.compile(r"a=inactive", re.IGNORECASE)
SEND_RECV_RE = re.compile(r"a=sendrecv", re.IGNORECASE)
RECV_ONLY_RE = re.compile(r"a=recvonly", re.IGNORECASE)


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def check_tc020(text):
    lines = split_lines(text)

    setup_indices = [idx for idx, line in enumerate(lines) if INVITE_RE.search(line)]
    setup_idx = setup_indices[0] if setup_indices else None
    hold_dir_idx = next(
        (
            idx
            for idx, line in enumerate(lines)
            if SEND_ONLY_RE.search(line) or INACTIVE_RE.search(line)
        ),
        None,
    )
    resume_dir_idx = next(
        (
            idx
            for idx, line in enumerate(lines)
            if SEND_RECV_RE.search(line)
            and (hold_dir_idx is not None and idx > hold_dir_idx)
        ),
        None,
    )

    inv_update_indices = [
        idx
        for idx, line in enumerate(lines)
        if (INVITE_RE.search(line) or UPDATE_RE.search(line))
        and (setup_idx is None or idx > setup_idx)
    ]
    has_hold_signal = any(
        hold_dir_idx is not None and hold_dir_idx > idx
        for idx in inv_update_indices
    )
    has_resume_signal = any(
        hold_dir_idx is not None
        and resume_dir_idx is not None
        and hold_dir_idx < idx < resume_dir_idx
        for idx in inv_update_indices
    )
    has_hold_direction = hold_dir_idx is not None
    has_resume_direction = resume_dir_idx is not None

    has_call_setup = setup_idx is not None
    has_bye = any(BYE_RE.search(line) for line in lines)

    statuses = []
    for idx, line in enumerate(lines):
        match = STATUS_RE.search(line)
        if match:
            statuses.append((idx, match.group(1), line))
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

    checks = [
        ("MO/MT call setup INVITE present", has_call_setup, "setup=%s" % has_call_setup),
        ("hold signal present", has_hold_signal, "hold_sig=%s" % has_hold_signal),
        ("hold SDP direction sendonly/inactive", has_hold_direction, "hold_dir_idx=%s" % hold_dir_idx),
        ("resume signal present", has_resume_signal, "resume_sig=%s" % has_resume_signal),
        ("resume SDP direction sendrecv", has_resume_direction, "resume_dir_idx=%s" % resume_dir_idx),
        ("200 OK present for dialog traffic", has_200, "200=%s" % has_200),
        ("BYE present", has_bye, "bye=%s" % has_bye),
        ("200 OK after BYE", has_200_after_bye, "bye_200=%s" % has_200_after_bye),
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
Call-ID: hold-call-1
Content-Type: application/sdp
m=audio 40000 RTP/AVP 96
a=sendrecv
[MESSAGE] SIP/2.0 200 OK
Call-ID: hold-call-1
[MESSAGE] INVITE sip:alice@ims.example.com SIP/2.0
Call-ID: hold-call-1
CSeq: 5 INVITE
Content-Type: application/sdp
m=audio 40000 RTP/AVP 96
a=sendonly
[MESSAGE] SIP/2.0 200 OK
Call-ID: hold-call-1
[MESSAGE] ACK sip:alice@ims.example.com SIP/2.0
Call-ID: hold-call-1
[MESSAGE] INVITE sip:alice@ims.example.com SIP/2.0
Call-ID: hold-call-1
CSeq: 6 INVITE
Content-Type: application/sdp
m=audio 40000 RTP/AVP 96
a=sendrecv
[MESSAGE] SIP/2.0 200 OK
Call-ID: hold-call-1
[MESSAGE] ACK sip:alice@ims.example.com SIP/2.0
Call-ID: hold-call-1
[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0
Call-ID: hold-call-1
[MESSAGE] SIP/2.0 200 OK
Call-ID: hold-call-1
"""
    fail_no_resume = base_pass.replace(
        "CSeq: 6 INVITE\nContent-Type: application/sdp\nm=audio 40000 RTP/AVP 96\na=sendrecv",
        "CSeq: 6 INVITE\nContent-Type: application/sdp\nm=audio 40000 RTP/AVP 96\na=sendonly",
    )
    fail_missing_bye = base_pass.replace(
        "[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0\nCall-ID: hold-call-1\n[MESSAGE] SIP/2.0 200 OK\nCall-ID: hold-call-1",
        "[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0\nCall-ID: hold-call-1\n[MESSAGE] SIP/2.0 408 Request Timeout\nCall-ID: hold-call-1",
    )
    return {
        "pass_hold_resume": (base_pass, "PASS"),
        "fail_no_resume_direction": (fail_no_resume, "FAIL"),
        "fail_bye_not_200": (fail_missing_bye, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc020(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-020 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
    actual, checks = check_tc020(text)
    render_checks(checks)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
