#!/usr/bin/env python3
"""TC-017 two calls with clean termination harness.

Sequence is a 34.229-1 12.12 repeat variant: call A and call B shall both
reach CONFIRMED and terminate cleanly with BYE/200. This is a behavioural
repetition check, not a standalone official 36.523 TC.
"""

import argparse
import re
import sys


INVITE_RE = re.compile(r"INVITE\s+sip:", re.IGNORECASE)
BYE_RE = re.compile(r"\bBYE\s+sip:", re.IGNORECASE)
OK_RE = re.compile(r"SIP/2\.0\s+200", re.IGNORECASE)
CONFIRMED_RE = re.compile(r"(?i)confirmed|call[ _-]?established|CALL_CONFIRMED")


def split_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def check_tc017(text):
    lines = split_lines(text)
    invites = [idx for idx, line in enumerate(lines) if INVITE_RE.search(line)]
    byes = [idx for idx, line in enumerate(lines) if BYE_RE.search(line)]
    oks = [idx for idx, line in enumerate(lines) if OK_RE.search(line)]

    call_sequences = {}
    for call_no, inv_idx in enumerate(invites, start=1):
        ok_after_invite = next((idx for idx in oks if idx > inv_idx), None)
        bye_after_invite = next((idx for idx in byes if idx > (ok_after_invite or inv_idx)), None)
        ok_after_bye = next((idx for idx in oks if bye_after_invite is not None and idx > bye_after_invite), None)
        end = bye_after_invite + 1 if bye_after_invite is not None else len(lines)
        confirmed = any(CONFIRMED_RE.search(line) for line in lines[inv_idx:end])
        call_sequences[call_no] = (
            ok_after_invite is not None,
            bye_after_invite is not None,
            ok_after_bye is not None,
            confirmed,
        )

    enough_calls = len(invites) >= 2
    all_clean = enough_calls and all(all(v for v in seq) for seq in call_sequences.values())
    trials = [("call %d %s" % (no, "->".join(["CONFIRMED" if s[3] else "-", "BYE" if s[1] else "-", "200afterBYE" if s[2] else "-"]))) for no, s in call_sequences.items()]

    checks = [
        ("at least two INVITE call attempts", enough_calls, "invites=%d" % len(invites)),
        ("every call reached CONFIRMED", all_clean, "details=%s" % trials),
        ("every call has BYE", all_clean, "byes=%d" % len(byes)),
        ("every call has 200 after BYE", all_clean, "oks=%d" % len(oks)),
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
    pass_log = """[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0
Call-ID: call-a
[MESSAGE] SIP/2.0 200 OK
Call-ID: call-a
[CHECK] CALL_CONFIRMED
[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0
Call-ID: call-a
[MESSAGE] SIP/2.0 200 OK
Call-ID: call-a
[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0
Call-ID: call-b
[MESSAGE] SIP/2.0 200 OK
Call-ID: call-b
[CHECK] CALL_CONFIRMED
[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0
Call-ID: call-b
[MESSAGE] SIP/2.0 200 OK
Call-ID: call-b
"""
    fail_one_bye_missing = pass_log.replace(
        "[MESSAGE] BYE sip:alice@ims.example.com SIP/2.0\nCall-ID: call-b",
        "[MESSAGE] CANCEL sip:bob@ims.example.com SIP/2.0\nCall-ID: call-b",
        1,
    )
    fail_one_call = pass_log.split("[MESSAGE] INVITE", 2)[0] + "[MESSAGE] INVITE" + pass_log.split("[MESSAGE] INVITE", 2)[1]
    return {
        "pass": (pass_log, "PASS"),
        "fail_missing_bye": (fail_one_bye_missing, "FAIL"),
        "fail_one_call": (fail_one_call, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc017(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-017 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
    actual, checks = check_tc017(text)
    expected_bool = (args.expect == "pass") if args.expect else None
    render_checks(checks, None)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
