#!/usr/bin/env python3
"""TC-024 media long-stability (>=120s) judgement engine.

Standard basis:
  TS 26.114 media reliability (RTP/RTCP continuity, jitter buffer, packet loss
  recovery). The 120s duration itself is an operator/enterprise acceptance
  metric, not a 3GPP conformance requirement, so this is a local functional
  verdict and never a 36.523-1 / 34.229-1 conformance verdict.

Checks a two-UA pjsua call log: dialog CONFIRMED, media active for >= the
required seconds, no media-failure markers in the window, clean BYE/200.
"""

import argparse
import re
import sys


TS_RE = re.compile(r"\b(\d{2}):(\d{2}):(\d{2})[.:](\d{3})\b")
CONFIRMED_RE = re.compile(r"Call\s+\d+\s+state\s+(?:changed to\s+)?CONFIRMED|Call\s+\d+\s+state\s*:?\s+CONFIRMED|\[CONFIRMED\]", re.IGNORECASE)
DISCONNECTED_RE = re.compile(r"Call\s+\d+\s+state\s+(?:changed to\s+)?DISCONNECTED|Call\s+\d+\s+state\s*:?\s+DISCONNECTED", re.IGNORECASE)
BYE_RE = re.compile(r"\bBYE\s+sip:", re.IGNORECASE)
STATUS_RE = re.compile(r"SIP/2\.0\s+(\d{3})|Response msg\s+(\d{3})/|\[(\d{3})\]", re.IGNORECASE)
STREAM_RE = re.compile(r"audio updated, stream #\d+:", re.IGNORECASE)
RTP_TX_RE = re.compile(r"TX pt=\d+,\s*ptime=\d+", re.IGNORECASE)
BROKEN_RE = re.compile(
    r"(?i)(media stream error|stream destroyed unexpectedly|media inactive due to error|ICE negotiation failed|no active media)"
)
TIMEOUT_RE = re.compile(r"(?i)(408 Request Timeout|transaction timeout|timed out waiting for response)")


def ts_seconds(line):
    match = TS_RE.search(line)
    if not match:
        return None
    hh, mm, ss, ms = (int(part) for part in match.groups())
    return hh * 3600 + mm * 60 + ss + ms / 1000.0


def nearest_ts_seconds(lines, idx):
    """Return the first timestamp at or before idx, walking backwards."""
    for line in reversed(lines[:idx + 1]):
        ts = ts_seconds(line)
        if ts is not None:
            return ts
    return None


def check_tc024(text, min_seconds=120.0):
    lines = text.splitlines()
    confirmed_idx = next((i for i, line in enumerate(lines) if CONFIRMED_RE.search(line)), None)
    bye_idx = next((i for i, line in enumerate(lines) if BYE_RE.search(line)), None)

    confirm_ts = ts_seconds(lines[confirmed_idx]) if confirmed_idx is not None else None
    bye_ts = nearest_ts_seconds(lines, bye_idx) if bye_idx is not None else None
    if confirm_ts is not None and bye_ts is not None and bye_ts < confirm_ts:
        bye_ts += 86400.0
    duration = (bye_ts - confirm_ts) if (confirm_ts is not None and bye_ts is not None) else None

    media_lines = [line for line in lines if STREAM_RE.search(line) or RTP_TX_RE.search(line)]
    media_before_bye = 0
    if bye_idx is not None:
        media_before_bye = sum(1 for line in lines[:bye_idx] if STREAM_RE.search(line) or RTP_TX_RE.search(line))

    no_failure = BROKEN_RE.search(text) is None
    no_timeout = TIMEOUT_RE.search(text) is None
    disconnected = bool(DISCONNECTED_RE.search(text))
    has_200_after_bye = False
    for line in lines[bye_idx:] if bye_idx is not None else []:
        match = STATUS_RE.search(line)
        if match:
            code = next(group for group in match.groups() if group is not None)
            if code == "200":
                has_200_after_bye = True
                break

    duration_ok = duration is not None and duration >= min_seconds

    checks = [
        ("call state CONFIRMED", confirmed_idx is not None, "confirmed=%s" % (confirmed_idx is not None)),
        (
            "media observed during call",
            media_before_bye > 0,
            "media_events_before_bye=%d" % media_before_bye,
        ),
        (
            "dialog held >= %.0fs" % min_seconds,
            duration_ok,
            "duration=%s" % ("%.3fs" % duration if duration is not None else "unknown"),
        ),
        ("no media failure marker", no_failure, "media_failure=%s" % (not no_failure)),
        ("no SIP transaction timeout", no_timeout, "timeout=%s" % (not no_timeout)),
        ("call released with BYE", bye_idx is not None, "bye=%s" % (bye_idx is not None)),
        ("200 OK after BYE", has_200_after_bye, "bye_200=%s" % has_200_after_bye),
        ("no unexpected DISCONNECTED before BYE", not disconnected, "disconnected=%s" % disconnected),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks):
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


def fixtures():
    base = """10:00:00.000   pjsua_call.c  Call 0 state CONFIRMED
10:00:00.010   pjsua_media.c  audio updated, stream #0: PCMU (sendrecv)
10:00:00.020   pjsua_med_tp  TX pt=0, ptime=20, last update:never
10:02:05.000   pjsua_call.c  BYE sip:bob@127.0.0.1 SIP/2.0
10:02:05.010   pjsua_call.c  SIP/2.0 200 OK
"""
    short = base.replace("10:02:05.000", "10:00:30.000").replace("10:02:05.010", "10:00:30.010")
    broken = base.replace(
        "10:02:05.000", "10:01:00.000\n10:01:00.000   pjsua_media.c  media stream error"
    ).replace("10:02:05.010", "10:01:01.010")
    return {
        "pass_long": (base, "PASS", 120.0),
        "fail_too_short": (short, "FAIL", 120.0),
        "fail_media_error": (broken, "FAIL", 120.0),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected, minimum) in fixtures().items():
        actual, checks = check_tc024(text, min_seconds=minimum)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-024 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
    parser.add_argument("--min-seconds", type=float, default=120.0)
    args = parser.parse_args()

    if args.selfcheck:
        return run_selfcheck()
    if not args.log:
        parser.error("provide --log <pjsua-log> or --selfcheck")

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    actual, checks = check_tc024(text, min_seconds=args.min_seconds)
    render_checks(checks)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
