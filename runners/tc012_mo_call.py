#!/usr/bin/env python3
"""TC-012 MO call setup field-level judgement engine.

Internal TC-012 is "MO voice call establishment over IMS".  This script checks
the SIP-layer shape visible in a real pjsua/demo log:

  - UE sends INVITE with SDP
  - remote side answers 200 OK with SDP
  - UE sends ACK
  - call becomes established (CONFIRMED marker, if present in the log)
  - later disconnect uses BYE followed by a final 200 OK

This is field/behaviour evidence, not a 36.523-1 conformance verdict.
"""

from __future__ import annotations

import argparse
import re
import sys

from pjsua_sip_extract import extract_pjsua_messages


LINE = "=" * 78

INVITE_RE = re.compile(r"INVITE\s+sip:", re.IGNORECASE)
ACK_RE = re.compile(r"ACK\s+sip:", re.IGNORECASE)
BYE_RE = re.compile(r"\bBYE\s+sip:", re.IGNORECASE)
STATUS_RE = re.compile(r"SIP/2\.0\s+(\d{3})", re.IGNORECASE)
CONFIRMED_RE = re.compile(r"(?i)confirmed|call[ _-]?established|CALL_CONFIRMED|call state: CONFIRMED")
FAILED_RE = re.compile(r"(?i)\b(?:4\d\d|5\d\d)\b")


def split_lines(text: str):
    return [line.strip() for line in text.splitlines() if line.strip()]


def has(line: str, needle: str) -> bool:
    return needle.lower() in line.lower()


def check_tc012(text: str) -> tuple[bool, list[dict]]:
    lines = split_lines(text)

    invites = [idx for idx, line in enumerate(lines) if INVITE_RE.search(line)]
    ack = any(ACK_RE.search(line) for line in lines)
    bye_idx = next((idx for idx, line in enumerate(lines) if BYE_RE.search(line)), None)

    statuses = []
    for idx, line in enumerate(lines):
        match = STATUS_RE.search(line)
        if match:
            statuses.append((idx, match.group(1), line))
    has_200 = any(code == "200" for _, code, _ in statuses)
    has_200_after_bye = False
    if bye_idx is not None:
        has_200_after_bye = any(idx > bye_idx and code == "200" for idx, code, _ in statuses)

    sdp_in_invite = False
    if invites:
        after_invite = lines[invites[0]:]
        sdp_in_invite = any(has(line, "application/sdp") or has(line, "m=audio") for line in after_invite[:20])
    sdp_in_response = False
    for idx, code, _ in statuses:
        if idx > (invites[0] if invites else -1) and code == "200":
            after = lines[idx:]
            sdp_in_response = any(has(line, "application/sdp") or has(line, "m=audio") for line in after[:20])
            break

    established = any(CONFIRMED_RE.search(line) for line in lines)
    # A 401/403/423 later in the log is often a REGISTER challenge after the
    # call has already been established.  Treat 4xx/5xx as a call failure only
    # between the INVITE and the first 200 OK of that dialog.
    fail_status = False
    if invites:
        first_call_200 = next((idx for idx, code, _ in statuses if idx > invites[0] and code == "200"), None)
        end = first_call_200 if first_call_200 is not None else len(lines)
        fail_status = any(
            invites[0] < idx < end and code not in ("100", "180", "183", "200", "202")
            for idx, code, _ in statuses
        )

    checks = [
        ("MO INVITE present", bool(invites), f"invites={len(invites)}"),
        ("INVITE carries SDP", sdp_in_invite, f"sdp_invite={sdp_in_invite}"),
        ("200 OK present", has_200, f"200={has_200}"),
        ("200 OK carries SDP", sdp_in_response, f"sdp_response={sdp_in_response}"),
        ("ACK present", ack, f"ack={ack}"),
        ("call established marker", established, f"established={established}"),
        ("no 4xx/5xx call failure", not fail_status, f"fail_status={fail_status}"),
        ("BYE present", bye_idx is not None, f"bye={bye_idx is not None}"),
        ("200 OK after BYE", has_200_after_bye, f"bye_200={has_200_after_bye}"),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks: list[dict]) -> None:
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


GOOD_FIXTURE = """REGISTER sip:ims.example.com SIP/2.0
Call-ID: reg-1

SIP/2.0 200 OK
Call-ID: reg-1

INVITE sip:bob@ims.example.com SIP/2.0
Call-ID: call-1
Content-Type: application/sdp
m=audio 4000 RTP/AVP 96
a=sendrecv

SIP/2.0 200 OK
Call-ID: call-1
Content-Type: application/sdp
m=audio 17812 RTP/AVP 0 120
a=sendrecv
[STATE] call state: CONFIRMED

ACK sip:bob@ims.example.com SIP/2.0
Call-ID: call-1

BYE sip:alice@ims.example.com SIP/2.0
Call-ID: call-1

SIP/2.0 200 OK
Call-ID: call-1
"""


def fail_no_ack() -> str:
    return GOOD_FIXTURE.replace("ACK sip:bob@ims.example.com SIP/2.0", "SUBSCRIBE sip:bob@ims.example.com SIP/2.0")


def fail_no_bye_200() -> str:
    return GOOD_FIXTURE.replace(
        "BYE sip:alice@ims.example.com SIP/2.0\nCall-ID: call-1\n\nSIP/2.0 200 OK\nCall-ID: call-1",
        "BYE sip:alice@ims.example.com SIP/2.0\nCall-ID: call-1\n\nSIP/2.0 408 Request Timeout\nCall-ID: call-1",
    )


def cmd_selfcheck() -> int:
    scenarios = [
        ("TC-012 conformant MO call", GOOD_FIXTURE, True),
        ("TC-012 fail missing ACK", fail_no_ack(), False),
        ("TC-012 fail BYE not 200", fail_no_bye_200(), False),
    ]
    failures = 0
    for name, text, expected in scenarios:
        ok, checks = check_tc012(text)
        print(LINE)
        print(f"SCENARIO: {name} expected={'PASS' if expected else 'FAIL'} actual={'PASS' if ok else 'FAIL'}")
        render_checks(checks)
        if ok != expected:
            failures += 1
    print(LINE)
    if failures:
        print(f"SELFCHECK FAIL: {failures} scenario(s) did not behave as expected")
        return 1
    print("SELFCHECK PASS: harness matches expected pass/fail behavior")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selfcheck", action="store_true", help="run embedded fixtures")
    group.add_argument("--log", metavar="FILE", help="SIP/pjsua log file")
    args = parser.parse_args()

    if args.selfcheck:
        return cmd_selfcheck()

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    ok, checks = check_tc012(text)
    print(LINE)
    print(f"LOG: {args.log} verdict={'PASS' if ok else 'FAIL'}")
    render_checks(checks)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
