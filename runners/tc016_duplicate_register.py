#!/usr/bin/env python3
"""TC-016 duplicate REGISTER idempotency harness.

There is no standalone 34.229-1 TC for "duplicate REGISTER idempotency", so this
script is an implementation-level behavioural check derived from 24.229 SIP
registration semantics. A PASS here is a functional evidence point, not a
36.523/34.229-1 conformance verdict.
"""

import argparse
import re
import sys

from pjsua_sip_extract import extract_pjsua_messages


REGISTER_RE = re.compile(r"REGISTER\s+sip:", re.IGNORECASE)
CALLID_RE = re.compile(r"Call-ID\s*:\s*(\S+)", re.IGNORECASE)
OK_RE = re.compile(r"SIP/2\.0\s+200", re.IGNORECASE)
RESET_RE = re.compile(r"REGISTER[^\n]*(?:\n[^\n]*){0,4}Expires\s*:\s*0", re.IGNORECASE)
FATAL_RE = re.compile(r"(?i)fatal|segmentation|crash|abort|panic")


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def check_tc016(text):
    lines = split_lines(text)
    blocks = []
    current = None
    for line in lines:
        if REGISTER_RE.search(line):
            current = {"headers": {}}
            blocks.append(current)
        elif current is not None and ":" in line:
            name, value = line.split(":", 1)
            current["headers"][name.strip().lower()] = value.strip()

    registers = [b for b in blocks]
    call_ids = [b["headers"].get("call-id") for b in blocks]
    call_ids = [cid for cid in call_ids if cid]
    duplicate_seen = (
        len(registers) >= 2
        and len(call_ids) >= 2
        and all(cid == call_ids[0] for cid in call_ids)
        and len(set(call_ids)) == 1
    )
    got_ok = bool(OK_RE.search(text))
    no_reset = RESET_RE.search(text) is None
    no_fatal = FATAL_RE.search(text) is None
    state_saved = "REG_STATE_UNCHANGED=true" in text

    checks = [
        ("duplicate REGISTER with same Call-ID", duplicate_seen, "registers=%d call_ids=%s" % (len(registers), call_ids[:5])),
        ("200 OK observed for registration", got_ok, "ok200=%s" % got_ok),
        ("no Expires: 0 reset after active registration", no_reset, "reset=%s" % (not no_reset)),
        ("registration state unchanged marker", state_saved, "state=%s" % state_saved),
        ("no fatal/abort in log", no_fatal, "fatal=%s" % (not no_fatal)),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def check_pjsua_tc016(text):
    """Check a real pjsua/ims_client log for duplicate REGISTER idempotency."""
    messages = extract_pjsua_messages(text)
    regs = [m for m in messages if REGISTER_RE.search(m)]
    responses = [m for m in messages if re.match(r"SIP/2\.0\s+", m, re.IGNORECASE)]

    def call_id(body):
        m = re.search(r"Call-ID\s*:\s*(\S+)", body, re.IGNORECASE)
        return m.group(1) if m else None

    reg_call_ids = [call_id(m) for m in regs]
    ok_call_ids = [call_id(m) for m in responses if re.search(r"SIP/2\.0\s+200", m, re.IGNORECASE)]
    ok_call_ids = [c for c in ok_call_ids if c]
    reg_call_ids = [c for c in reg_call_ids if c]

    duplicate_seen = (
        len(reg_call_ids) >= 2
        and len(set(reg_call_ids)) == 1
    )
    got_ok = len(ok_call_ids) >= 2
    no_reset = re.search(r"REGISTER[^\n]*(?:\n[^\n]*){0,4}Expires\s*:\s*0", text, re.IGNORECASE) is None
    state_saved = len(re.findall(r"registration success.*status=200", text, re.IGNORECASE)) >= 2
    no_fatal = FATAL_RE.search(text) is None

    checks = [
        ("duplicate REGISTER with same Call-ID", duplicate_seen, "registers=%d call_ids=%s" % (len(reg_call_ids), reg_call_ids[:5])),
        ("200 OK observed for duplicate REGISTER", got_ok, "ok200=%d call_ids=%s" % (len(ok_call_ids), ok_call_ids[:5])),
        ("no Expires: 0 reset after active registration", no_reset, "reset=%s" % (not no_reset)),
        ("registration state unchanged derived from repeated success", state_saved, "successes=%d" % len(re.findall(r"registration success.*status=200", text, re.IGNORECASE))),
        ("no fatal/abort in log", no_fatal, "fatal=%s" % (not no_fatal)),
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


def render_pjsua_checks(checks, expected):
    ok = True
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))
        if expected is not None and is_ok != expected:
            ok = False
    return ok


def fixtures():
    pass_log = """[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
Call-ID: dup-reg-1
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Contact: <sip:alice@10.45.0.2:5002>;ob
Expires: 600
[MESSAGE] SIP/2.0 200 OK
Call-ID: dup-reg-1
Expires: 600
[CHECK] REG_STATE_UNCHANGED=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
Call-ID: dup-reg-1
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Contact: <sip:alice@10.45.0.2:5002>;ob
Expires: 600
[MESSAGE] SIP/2.0 200 OK
Call-ID: dup-reg-1
Expires: 600
[CHECK] REG_STATE_UNCHANGED=true
"""
    fail_id = """[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
Call-ID: dup-reg-1
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Contact: <sip:alice@10.45.0.2:5002>;ob
Expires: 600
[MESSAGE] SIP/2.0 200 OK
Call-ID: dup-reg-1
Expires: 600
[CHECK] REG_STATE_UNCHANGED=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
Call-ID: dup-reg-2
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Contact: <sip:alice@10.45.0.2:5002>;ob
Expires: 600
[MESSAGE] SIP/2.0 200 OK
Call-ID: dup-reg-2
Expires: 600
[CHECK] REG_STATE_UNCHANGED=true
"""
    fail_reset = pass_log + """[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
Call-ID: dup-reg-1
Expires: 0
"""
    return {
        "pass": (pass_log, "PASS"),
        "fail_different_callid": (fail_id, "FAIL"),
        "fail_reset": (fail_reset, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc016(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-016 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
    parser.add_argument("--raw", action="store_true", help="pjsua/ims_client raw log mode")
    parser.add_argument("--log")
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    if args.selfcheck:
        return run_selfcheck()
    if not args.log:
        parser.error("provide --log <sip-log> or --selfcheck")

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    actual, checks = check_pjsua_tc016(text) if args.raw else check_tc016(text)
    expected_bool = (args.expect == "pass") if args.expect else None
    if args.raw:
        render_pjsua_checks(checks, expected_bool)
    else:
        render_checks(checks, None)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
