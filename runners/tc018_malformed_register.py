#!/usr/bin/env python3
"""TC-018 malformed REGISTER robustness harness (implementation-level).

34.229-1 has no standalone malformed REGISTER conformance TC, so this does not
claim an official PO/F. It verifies that a malformed REGISTER does not crash the
stack and is either ignored or answered with a graceful 4xx/5xx while the stack
stays responsive.
"""

import argparse
import re
import sys


REGISTER_RE = re.compile(r"REGISTER\s+sip:", re.IGNORECASE)
INVITE_RE = re.compile(r"INVITE\s+sip:", re.IGNORECASE)
GRACEFUL_RE = re.compile(r"SIP/2\.0\s+(?:4\d\d|5\d\d)", re.IGNORECASE)
FATAL_RE = re.compile(r"(?i)\b(?:fatal(?:ly)?|segmentation|crash|abort|panic)\b")
MALFORMED_RE = re.compile(r"(?i)malformed register|invalid register|bad register|PARSING_ERROR")


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def check_tc018(text):
    lines = split_lines(text)
    malformed_lines = [idx for idx, line in enumerate(lines) if MALFORMED_RE.search(line)]
    malformed_seen = bool(malformed_lines)

    last_malformed = malformed_lines[-1] if malformed_lines else None
    after_malformed = lines[last_malformed + 1:] if last_malformed is not None else []
    graceful = bool(GRACEFUL_RE.search(text)) or "IGNORED=true" in text
    responsive_after = any(REGISTER_RE.search(line) or INVITE_RE.search(line) for line in after_malformed)
    no_fatal = FATAL_RE.search(text) is None

    checks = [
        ("malformed REGISTER observed", malformed_seen, "malformed_lines=%d" % len(malformed_lines)),
        ("graceful 4xx/5xx or explicit ignore", graceful, "graceful=%s" % graceful),
        ("no fatal/crash", no_fatal, "fatal=%s" % (not no_fatal)),
        ("stack responsive after malformed", responsive_after, "responsive=%s" % responsive_after),
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
    pass_log = """[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
Call-ID: malformed-1
From: <sip:alice@ims.example.com>
PARSING_ERROR malformed Authorization header
[CHECK] IGNORED=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
Call-ID: ok-after-malformed
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Expires: 600
[MESSAGE] SIP/2.0 200 OK
Call-ID: ok-after-malformed
"""
    fail_crash = pass_log + """FATAL segmentation failure
"""
    fail_no_recovery = pass_log.replace(
        "[MESSAGE] REGISTER sip:ims.example.com SIP/2.0\nCall-ID: ok-after-malformed",
        "[MESSAGE] SUBSCRIBE sip:ims.example.com SIP/2.0\nCall-ID: ok-after-malformed",
        1,
    )
    return {
        "pass": (pass_log, "PASS"),
        "fail_crash": (fail_crash, "FAIL"),
        "fail_no_recovery": (fail_no_recovery, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc018(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-018 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
    actual, checks = check_tc018(text)
    expected_bool = (args.expect == "pass") if args.expect else None
    render_checks(checks, None)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
