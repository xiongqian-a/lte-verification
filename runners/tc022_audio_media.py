#!/usr/bin/env python3
"""TC-022 call + audio media continuity judgement engine.

Official skeleton:
  TS 34.229-1 12.12 (MO) / 12.13 (MT) - correct exchange of SDP messages for
  negotiating media and the call setup/release TP.
Field source:
  TS 26.114 (MTSI) media path, RTP payload and codec requirements.

This engine verifies the field-level evidence available in a local pjsua /
IMS-simulator log: audio media negotiated, RTP stream active, negotiated
codec at 8 kHz and a clean BYE/200 release. It is a local functional verdict,
NOT a 36.523-1 / 34.229-1 conformance verdict.
"""

import argparse
import re
import sys


TS_RE = re.compile(r"\b(\d{2}):(\d{2}):(\d{2})[.:](\d{3})\b")
MEDIA_LINE_RE = re.compile(r"^\s*m=audio\s+\d+\s+RTP/AVP", re.IGNORECASE)
STREAM_RE = re.compile(r"audio updated, stream #\d+:\s*([A-Za-z0-9_.-]+)\s*\((sendrecv|sendonly|recvonly|inactive)\)", re.IGNORECASE)
VALUE_RE = re.compile(r"(\d+)\s+audio\s+([A-Za-z0-9_.-]+)\s*@\s*(\d+)\s*kHz", re.IGNORECASE)
NEGO_OK_RE = re.compile(r"SDP negotiation done: Success", re.IGNORECASE)
CONFIRMED_RE = re.compile(r"Call\s+\d+\s+state\s+(?:changed to\s+)?CONFIRMED|Call\s+\d+\s+state\s*:?\s+CONFIRMED|\[CONFIRMED\]", re.IGNORECASE)
BYE_RE = re.compile(r"\bBYE\s+sip:", re.IGNORECASE)
STATUS_RE = re.compile(r"SIP/2\.0\s+(\d{3})|Response msg\s+(\d{3})/|\[(\d{3})\]", re.IGNORECASE)
BROKEN_RE = re.compile(r"(?i)(no media|media stream error|stream destroyed unexpectedly|media inactive due to error)")
RTP_TX_RE = re.compile(r"TX pt=(\d+),\s*ptime=(\d+)", re.IGNORECASE)


def ts_seconds(line):
    match = TS_RE.search(line)
    if not match:
        return None
    hh, mm, ss, ms = (int(part) for part in match.groups())
    return hh * 3600 + mm * 60 + ss + ms / 1000.0


def check_tc022(text, min_seconds=0.0):
    lines = text.splitlines()

    media_streams = STREAM_RE.findall(text)
    codecs = VALUE_RE.findall(text)
    negotiation_ok = bool(NEGO_OK_RE.search(text))
    call_confirmed = bool(CONFIRMED_RE.search(text))
    has_media_line = any(MEDIA_LINE_RE.search(line) for line in lines)
    tx_ptime = RTP_TX_RE.findall(text)

    # Media duration: from first m=audio/stream negotiation to the first BYE.
    first_media = None
    bye_index = None
    for idx, line in enumerate(lines):
        if first_media is None and (MEDIA_LINE_RE.search(line) or STREAM_RE.search(line)):
            stamp = ts_seconds(line)
            if stamp is not None:
                first_media = stamp
        if bye_index is None and BYE_RE.search(line):
            bye_index = idx
            break
    last_media_before_bye = None
    if bye_index is not None:
        for line in lines[:bye_index]:
            stamp = ts_seconds(line)
            if stamp is not None and (MEDIA_LINE_RE.search(line) or STREAM_RE.search(line) or RTP_TX_RE.search(line)):
                last_media_before_bye = stamp
    duration = None
    if first_media is not None and last_media_before_bye is not None and last_media_before_bye >= first_media:
        duration = last_media_before_bye - first_media

    has_bye = bye_index is not None
    has_200_after_bye = False
    if bye_index is not None:
        has_200_after_bye = False
        for line in lines[bye_index:]:
            match = STATUS_RE.search(line)
            if match:
                code = next(group for group in match.groups() if group is not None)
                if code == "200":
                    has_200_after_bye = True
                    break

    no_media_failure = BROKEN_RE.search(text) is None

    duration_ok = True
    if min_seconds > 0:
        duration_ok = duration is not None and duration >= min_seconds

    checks = [
        ("SDP m=audio media line present", has_media_line, "media_line=%s" % has_media_line),
        (
            "audio stream negotiated sendrecv",
            any(direction.lower() == "sendrecv" for _, direction in media_streams),
            "streams=%s" % (media_streams or "none"),
        ),
        (
            "negotiated codec reported at 8 kHz",
            any(int(rate) == 8 for _, _, rate in codecs),
            "codecs=%s" % (codecs or "none"),
        ),
        ("SDP negotiation done: Success", negotiation_ok, "negotiation_ok=%s" % negotiation_ok),
        ("call state CONFIRMED", call_confirmed, "confirmed=%s" % call_confirmed),
        (
            "RTP tx parameters observed (pt/ptime)",
            bool(tx_ptime),
            "tx=%s" % (tx_ptime or "none"),
        ),
        ("no media failure marker", no_media_failure, "media_failure=%s" % (not no_media_failure)),
        ("call released with BYE", has_bye, "bye=%s" % has_bye),
        ("200 OK after BYE", has_200_after_bye, "bye_200=%s" % has_200_after_bye),
    ]
    if min_seconds > 0:
        checks.append(
            (
                "media observed for >= %ss" % min_seconds,
                duration_ok,
                "duration=%s" % ("%.3fs" % duration if duration is not None else "unknown"),
            )
        )

    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks):
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


def fixtures():
    base_pass = """17:53:02.170         inv0x55d9  ....SDP negotiation done: Success
17:53:02.178          pjsua_media.c  ......audio updated, stream #0: PCMU (sendrecv)
m=audio 4000 RTP/AVP 0 120
17:53:02.200   pjsua_call.c  Call 0 state CONFIRMED
    #0 audio PCMU @8kHz, sendrecv, peer=10.45.0.1:17812
       TX pt=0, ptime=20, last update:never
17:53:22.200  BYE sip:5000@10.45.0.1 SIP/2.0
17:53:22.210 SIP/2.0 200 OK
"""
    fail_no_media = base_pass.replace(
        "audio updated, stream #0: PCMU (sendrecv)", "audio updated, stream #0: (inactive)"
    )
    fail_no_release = base_pass.replace("SIP/2.0 200 OK", "SIP/2.0 408 Request Timeout")
    return {
        "pass_audio": (base_pass, "PASS"),
        "fail_inactive_media": (fail_no_media, "FAIL"),
        "fail_release_not_200": (fail_no_release, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks = check_tc022(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-022 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
    parser.add_argument("--min-seconds", type=float, default=0.0)
    args = parser.parse_args()

    if args.selfcheck:
        return run_selfcheck()
    if not args.log:
        parser.error("provide --log <pjsua-log> or --selfcheck")

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    actual, checks = check_tc022(text, min_seconds=args.min_seconds)
    render_checks(checks)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
