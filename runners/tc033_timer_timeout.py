#!/usr/bin/env python3
"""TC-033 SIP timer timeout judgement engine.

Standard basis: TS 24.229 timers / RFC 3261. 34.229-1 has no standalone
timer test case, so this is an implementation-level behaviour verdict: when a
request gets no response, the stack retransmits and eventually times out
gracefully without crashing.
"""

import argparse
import re
import sys


INVITE_RE = re.compile(r"INVITE\s+sip:|Request msg INVITE/", re.IGNORECASE)
REGISTER_RE = re.compile(r"REGISTER\s+sip:|Request msg REGISTER/", re.IGNORECASE)
TIMEOUT_RE = re.compile(r"(?i)(408.{0,20}Request Timeout|408.{0,20}Timeout|Transaction.*tim(e|ed) out|Trying to call.*timed out|Call.*state\s*:?\s+DISCONNECTED|Call \d+ is DISCONNECTED.*(?:408|Timeout)|Unexpected timeout|SIP transaction timed-out|Timeout waiting for response)")
FATAL_RE = re.compile(r"(?i)(fatal(?:ly)?|segmentation|crash|abort|panic)")


def check_tc033(text):
    lines = text.splitlines()
    invites = [idx for idx, line in enumerate(lines) if INVITE_RE.search(line)]
    has_retransmission = len(invites) >= 2
    has_timeout = bool(TIMEOUT_RE.search(text))
    no_fatal = FATAL_RE.search(text) is None
    # Ensure the stack remained alive: REGISTER or a log of responsive app.
    responsive_after = bool(REGISTER_RE.search(text)) or len(lines) > 20

    checks = [
        ("INVITE attempted", bool(invites), "invite_attempts=%d" % len(invites)),
        ("retransmission observed", has_retransmission, "invites=%d" % len(invites)),
        ("timeout / give-up observed", has_timeout, "timeout=%s" % has_timeout),
        ("no fatal/crash", no_fatal, "fatal=%s" % (not no_fatal)),
        ("stack remains responsive", responsive_after, "responsive=%s" % responsive_after),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks):
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


def run_selfcheck():
    failed = False

    pass_log = (
        "[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0\n"
        "[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0\n"
        "[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0\n"
        "08:01:02.123 SIP transaction timed out\n"
        "08:01:03.001 Call 1 state changed to DISCONNECTED\n"
        "... still responsive log lines ...\n"
        "REGISTER sip:ims.example.com SIP/2.0\n"
    )
    ok, checks = check_tc033(pass_log)
    print("SCENARIO: TC-033 timeout pass expected=PASS actual=%s" % ("PASS" if ok else "FAIL"))
    render_checks(checks)
    failed = failed or not ok

    fail_log = (
        "[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0\n"
        "Call still waiting\n"
    )
    ok, checks = check_tc033(fail_log)
    print("SCENARIO: TC-033 timeout fail expected=FAIL actual=%s" % ("PASS" if ok else "FAIL"))
    render_checks(checks)
    failed = failed or ok

    if failed:
        print("SELFCHECK FAIL")
        return 1
    print("SELFCHECK PASS")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selfcheck", action="store_true")
    parser.add_argument("--log")
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()
    if args.selfcheck:
        return run_selfcheck()
    if not args.log:
        parser.error("provide --log <pjsua-log>")
    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    overall, checks = check_tc033(text)
    render_checks(checks)
    print("RESULT: %s" % ("PASS" if overall else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if overall else 1
    return 0 if overall == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
