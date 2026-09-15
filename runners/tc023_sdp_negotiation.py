#!/usr/bin/env python3
"""TC-023 SDP offer/answer negotiation judgement engine.

Official skeleton:
  TS 34.229-1 12.12 (MO) / 12.13 (MT) SDP exchange TP.
Field source:
  TS 26.114 5.2.1 / 6.2.2.1 / 6.2.5 / 7.3.1 (speech offer/answer, RTP profile,
  AMR/AMR-WB, telephone-event, bandwidth attributes).

Verifies the field-level SDP convergence observable in a local pjsua /
IMS-simulator log: m=audio, rtpmap, ptime, direction, RTCP, telephone-event
and "SDP negotiation done: Success". Local functional verdict, not conformance.
"""

import argparse
import re
import sys


MEDIA_RE = re.compile(r"^\s*m=audio\s+\d+\s+RTP/AVP\s+(.+)$", re.IGNORECASE)
RTPMAP_RE = re.compile(r"^\s*a=rtpmap:(\d+)\s+([A-Za-z0-9_.-]+)/(\d+)", re.IGNORECASE)
FMRT_RE = re.compile(r"^\s*a=fmtp:(\d+)\s+(.+)$", re.IGNORECASE)
PTIME_RE = re.compile(r"^\s*a=ptime:(\d+)", re.IGNORECASE)
DIRECTION_RE = re.compile(r"^\s*a=(sendrecv|sendonly|recvonly|inactive)", re.IGNORECASE)
RTCP_RE = re.compile(r"^\s*a=rtcp:\d+", re.IGNORECASE)
NEGO_OK_RE = re.compile(r"SDP negotiation done: Success", re.IGNORECASE)
BANDWIDTH_RE = re.compile(r"^\s*b=(AS|TIAS|RS|RR):(\d+)", re.IGNORECASE)


def sdp_blocks(text):
    """Split a pjsua log into SDP blocks starting at each v=0 line."""
    blocks = []
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "v=0":
            if current:
                blocks.append(current)
            current = [stripped]
            continue
        if current is not None:
            # Skip pjsua log prefixes before the SDP payload line.
            if re.match(r"^[vmosctab]=|^a=", stripped):
                current.append(stripped)
            elif re.match(r"^\d{2}:\d{2}:\d{2}", stripped) is None and stripped:
                current.append(stripped)
    if current:
        blocks.append(current)
    return ["\n".join(block) for block in blocks]


def analyze_block(block):
    info = {
        "payloads": set(),
        "rtpmap": {},
        "ptime": None,
        "direction": None,
        "rtcp": False,
        "bandwidth": {},
        "fmtp": {},
        "has_audio": False,
    }
    for line in block.splitlines():
        match = MEDIA_RE.match(line)
        if match:
            info["has_audio"] = True
            info["payloads"] = set(match.group(1).split())
            continue
        match = RTPMAP_RE.match(line)
        if match:
            pt, name, rate = match.groups()
            info["rtpmap"][pt] = (name, int(rate))
            continue
        match = FMRT_RE.match(line)
        if match:
            info["fmtp"][match.group(1)] = match.group(2).strip()
            continue
        match = PTIME_RE.match(line)
        if match:
            info["ptime"] = int(match.group(1))
            continue
        match = DIRECTION_RE.match(line)
        if match:
            info["direction"] = match.group(1).lower()
            continue
        if RTCP_RE.match(line):
            info["rtcp"] = True
            continue
        match = BANDWIDTH_RE.match(line)
        if match:
            info["bandwidth"][match.group(1).upper()] = int(match.group(2))
    return info


def check_tc023(text):
    blocks = [analyze_block(block) for block in sdp_blocks(text)]
    audio_blocks = [block for block in blocks if block["has_audio"]]
    negotiation_ok = bool(NEGO_OK_RE.search(text))

    def pcm(rate):
        return any(
            name.upper() in ("PCMU", "PCMA") and r == rate
            for block in audio_blocks
            for name, r in block["rtpmap"].values()
        )

    def telephone_event():
        return any(
            name.lower() == "telephone-event"
            for block in audio_blocks
            for name, _ in block["rtpmap"].values()
        )

    ptime_20 = any(block["ptime"] == 20 for block in audio_blocks)
    sendrecv = any(block["direction"] == "sendrecv" for block in audio_blocks)
    rtcp = any(block["rtcp"] for block in audio_blocks)
    # G.711 8 kHz narrowband is the negotiated baseline for these VoLTE runs.
    g711_8k = pcm(8000)
    has_bandwidth = any(block["bandwidth"] for block in audio_blocks)

    checks = [
        ("m=audio media description present", bool(audio_blocks), "audio_blocks=%d" % len(audio_blocks)),
        ("offer and answer SDP both present", len(audio_blocks) >= 2, "blocks=%d" % len(audio_blocks)),
        ("a=rtpmap G.711 (PCMU/PCMA) @8000", g711_8k, "g711_8k=%s" % g711_8k),
        ("a=rtpmap telephone-event present", telephone_event(), "telephone_event=%s" % telephone_event()),
        ("a=ptime:20 present", ptime_20, "ptime20=%s" % ptime_20),
        ("a=sendrecv direction present", sendrecv, "sendrecv=%s" % sendrecv),
        ("a=rtcp attribute present", rtcp, "rtcp=%s" % rtcp),
        ("bandwidth attribute (b=AS/TIAS/RS/RR) present", has_bandwidth, "bandwidth=%s" % has_bandwidth),
        ("SDP negotiation done: Success", negotiation_ok, "negotiation_ok=%s" % negotiation_ok),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks, audio_blocks


def render_checks(checks):
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


def fixtures():
    offer = """v=0
o=- 1 1 IN IP4 10.45.0.2
s=pjmedia
b=AS:84
m=audio 4000 RTP/AVP 0 8 120
c=IN IP4 10.45.0.2
b=TIAS:64000
a=rtcp:4001 IN IP4 10.45.0.2
a=sendrecv
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:120 telephone-event/8000
a=fmtp:120 0-16
"""
    answer = """v=0
o=FS 1 1 IN IP4 10.45.0.1
m=audio 17812 RTP/AVP 0 120
c=IN IP4 10.45.0.1
a=rtpmap:0 PCMU/8000
a=rtpmap:120 telephone-event/8000
a=fmtp:120 0-15
a=ptime:20
a=rtcp:17813 IN IP4 10.45.0.1
"""
    pass_text = offer + answer + "\nSDP negotiation done: Success\n"
    fail_no_te = (offer + answer).replace("a=rtpmap:120 telephone-event/8000", "a=rtpmap:120 x-unknown/8000") + "\nSDP negotiation done: Success\n"
    fail_no_nego = offer + answer + "\nSDP negotiation done: Failed\n"
    return {
        "pass_sdp": (pass_text, "PASS"),
        "fail_no_telephone_event": (fail_no_te, "FAIL"),
        "fail_negotiation": (fail_no_nego, "FAIL"),
    }


def run_selfcheck():
    failed = False
    for name, (text, expected) in fixtures().items():
        actual, checks, _ = check_tc023(text)
        expected_bool = expected == "PASS"
        print("SCENARIO: TC-023 %s expected=%s actual=%s" % (name, expected, "PASS" if actual else "FAIL"))
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
        parser.error("provide --log <pjsua-log> or --selfcheck")

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    actual, checks, _ = check_tc023(text)
    render_checks(checks)
    print("RESULT: %s" % ("PASS" if actual else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if actual else 1
    return 0 if actual == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
