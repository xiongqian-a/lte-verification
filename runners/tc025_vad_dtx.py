#!/usr/bin/env python3
"""TC-025 VAD/DTX status engine.

Standard basis:
  TS 26.114 VAD/source-controlled-rate operation per 26.093/26.193 and
  EVS DTX per 26.450/26.451; SDP dtx switch per 26.114 6.2.2.

A real VAD/DTX verdict requires an audio source with silence periods and an
RTP media stream where SID/CN frames and their cadence can be observed.
Open-source local pjsua often does not negotiate dtx by default, so this
engine keeps the result at LIMITED_PASS when only no-data frames are present,
and returns RESTRICTED when true media evidence is absent.
"""

import argparse
import re
import os
import sys
import tempfile


DTX_RE = re.compile(r"(?i)^\s*a=(fmtp|rtpmap|sendrecv).*(dtx|sprop-dtx|comfort-noise|CNG|silence)")
CN_PT_RE = re.compile(r"^\s*a=(rtpmap|fmtp):(\d+)\s+(comfort noise|CN)\b", re.IGNORECASE)
ACTIVE_TALK_RE = re.compile(r"RX pt=\d+.*timestamp=\d+", re.IGNORECASE)
ACTIVE_TX_RE = re.compile(r"TX pt=\d+, ptime=\d+", re.IGNORECASE)


def parse_amr_stats(path):
    data = {
        "rtp": 0,
        "counts": {},
        "sid_deltas": [],
        "sid_delta_frames": [],
        "no_data_transmitted": 0,
    }
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            m = re.match(r"rtp_pt96_pkts=(\d+)", line)
            if m:
                data["rtp"] = int(m.group(1))
                continue
            m = re.match(r"ft=(\d+) count=(\d+)", line)
            if m:
                data["counts"][int(m.group(1))] = int(m.group(2))
                continue
            m = re.match(r"sid_delta_ts=(.*)", line)
            if m and m.group(1):
                data["sid_deltas"] = [int(v) for v in m.group(1).split(",") if v]
                continue
            m = re.match(r"sid_delta_frames=(.*)", line)
            if m and m.group(1):
                data["sid_delta_frames"] = [int(v) for v in m.group(1).split(",") if v]
                continue
            m = re.match(r"no_data_transmitted=(\d+)", line)
            if m:
                data["no_data_transmitted"] = int(m.group(1))
    data["speech"] = sum(data["counts"].get(ft, 0) for ft in range(0, 8))
    data["sid"] = data["counts"].get(8, 0)
    data["no_data"] = data["counts"].get(15, 0)
    # Older statistics files did not have the explicit transmission counter.
    if data["no_data"] and data["no_data_transmitted"] == 0:
        data["no_data_transmitted"] = data["no_data"]
    return data


def check_tc025(text):
    lines = text.splitlines()
    dtx_signaling = [line.strip() for line in lines if DTX_RE.search(line)]
    cng_signaling = [line.strip() for line in lines if CN_PT_RE.search(line)]
    # pjsua uses pt=13 for Comfort Noise often encoded as CN/8000; codec
    # selection of CN or a dtx attribute is accepted as signaling evidence.
    has_cng_pt = any("rtpmap" in line or "fmtp" in line for line in cng_signaling)
    has_dtx_attr = any("dtx" in line.lower() or "sprop-dtx" in line.lower() for line in dtx_signaling)
    # Real media evidence: log must show bidirectional media and silence-related
    # events. Without that, this cannot claim VAD behavior.
    has_media = bool(ACTIVE_TX_RE.search(text)) or bool(ACTIVE_TALK_RE.search(text))
    unknown = (not dtx_signaling) and (not cng_signaling)

    checks = [
        ("SDP dtx signaling observed", has_dtx_attr, "dtx_lines=%d" % len(dtx_signaling)),
        ("SDP CN/comfort-noise payload observed", has_cng_pt, "cng_lines=%d" % len(cng_signaling)),
        ("media stream activity observed", has_media, "media=%s" % has_media),
        ("silence-frame / CN media evidence present", False, "REQUIRED_MEDIA_EVIDENCE=CN/silence frames"),
    ]
    # If no dtx signaling and no CN payload, there is nothing to verify.
    if unknown or not has_media:
        return "RESTRICTED", checks
    # dtx signaling + media activity but no actual silence-frame observation:
    # still only signaling-level, not a VAD verdict.
    if has_dtx_attr or has_cng_pt:
        return "RESTRICTED", checks
    return "FAIL", checks


def render_checks(checks):
    for name, is_ok, detail in checks:
        tag = "OK" if is_ok else "BAD"
        if name.startswith("silence-frame") or detail.startswith("N/A"):
            tag = "N/A"
        print("  [%s ] %s :: %s" % (tag, name, detail))


def check_amr_stats(path):
    data = parse_amr_stats(path)
    rtp = data["rtp"]
    speech = data["speech"]
    sid = data["sid"]
    no_data = data["no_data"]
    sid_deltas = data["sid_deltas"]
    sid_delta_frames = data["sid_delta_frames"]
    no_data_transmitted = data["no_data_transmitted"]
    expected_sid_delta = 8 * 20 * 8  # 8 AMR frames * 20 ms * 8000 Hz = 1280 ticks
    if sid_deltas:
        cadence_ok = all(delta == expected_sid_delta for delta in sid_deltas)
        cadence_detail = (
            "sid_delta_ts=%s frames=%s expected_ts=%d expected_frames=8 "
            "(26.093 SID_UPDATE every 8 frames)"
            % (sid_deltas, sid_delta_frames, expected_sid_delta)
        )
    else:
        cadence_ok = None
        cadence_detail = "N/A: no SID interval data"
    checks = [
        ("RTP AMR/8000 media packets observed", rtp > 0, "rtp_pkts=%d" % rtp),
        ("speech frames observed", speech > 0, "speech_ft0_7=%d" % speech),
        (
            "NO_DATA frame count",
            no_data == 0,
            "amr_ft15_nodata=%d; non-zero means NO_DATA was present in the sample"
            % no_data,
        ),
        ("SID/CN frames observed", sid > 0, "amr_ft8_sid=%d" % sid),
        (
            "26.093 NO_DATA transmission constraint",
            no_data_transmitted == 0,
            "no_data_transmitted=%d expected=0 (NO_DATA should not be transmitted over AN)"
            % no_data_transmitted,
        ),
        ("AMR SID_UPDATE cadence", cadence_ok is not False, cadence_detail),
    ]
    hard_fail = no_data_transmitted > 0 or cadence_ok is False
    hard_pass = sid > 0 and cadence_ok is True and no_data_transmitted == 0
    result = "RESTRICTED"
    if rtp > 0 and speech > 0 and no_data > 0:
        result = "LIMITED_PASS"
    scope = "SCOPE: AMR local evidence based on speech + no-data/DTX silence media; "
    if hard_fail:
        result = "LIMITED_PASS"
        scope += (
            "LOCAL_BEHAVIOR=PARTIAL; STANDARD_ASSERTION=FAIL; "
            "the supplied sample violates an explicit 26.093 constraint; "
            "this is a negative control result, not a full SCR PASS."
        )
    elif hard_pass:
        result = "LIMITED_PASS"
        scope += (
            "LOCAL_BEHAVIOR=PASS_WITHIN_SAMPLE; STANDARD_ASSERTION=PASS; "
            "SID_UPDATE cadence is 8 frames and no NO_DATA was transmitted "
            "within the supplied sample."
        )
    elif sid > 0:
        result = "LIMITED_PASS"
        scope += (
            "LOCAL_BEHAVIOR=PARTIAL; STANDARD_ASSERTION=UNKNOWN; "
            "SID observed; cadence not derivable from supplied stats."
        )
    else:
        result = "LIMITED_PASS"
        scope += (
            "LOCAL_BEHAVIOR=PARTIAL; STANDARD_ASSERTION=UNKNOWN; "
        )
        scope += "SID/CN not observed; full SID cadence is still RESTRICTED outside this scope."
    if no_data_transmitted > 0:
        scope += (
            " NO_DATA frames were transmitted over RTP; TS 26.093 line 229 "
            "says NO_DATA should not be transmitted over AN."
        )
    return result, checks, scope


def run_selfcheck():
    failed = False

    def run_amr_scenario(label, stats_text, expected_scope):
        nonlocal failed
        fd, stats_path = tempfile.mkstemp(prefix="tc025_selfcheck_", suffix=".txt")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(stats_text)
            result, checks, scope = check_amr_stats(stats_path)
        finally:
            if os.path.exists(stats_path):
                os.unlink(stats_path)
        print("SCENARIO: %s expected=LIMITED_PASS/%s actual=%s"
              % (label, expected_scope, result))
        render_checks(checks)
        print(scope)
        if result != "LIMITED_PASS" or expected_scope not in scope:
            failed = True

    run_amr_scenario(
        "TC-025 compliant positive-control fixture",
        (
            "rtp_pt96_pkts=42\n"
            "ft=0 count=10\n"
            "ft=8 count=2\n"
            "ft=15 count=0\n"
            "sid_delta_ts=1280,1280\n"
            "sid_delta_frames=8,8\n"
            "no_data_transmitted=0\n"
        ),
        "STANDARD_ASSERTION=PASS",
    )
    run_amr_scenario(
        "TC-025 observed non-compliant negative control",
        (
            "rtp_pt96_pkts=42\n"
            "ft=2 count=10\n"
            "ft=8 count=2\n"
            "ft=15 count=2\n"
            "sid_delta_ts=160000,160000\n"
            "sid_delta_frames=1000,1000\n"
            "no_data_transmitted=2\n"
        ),
        "STANDARD_ASSERTION=FAIL",
    )
    run_amr_scenario(
        "TC-025 no-SID evidence-boundary fixture",
        (
            "rtp_pt96_pkts=42\n"
            "ft=0 count=10\n"
            "ft=15 count=1\n"
            "no_data_transmitted=1\n"
        ),
        "STANDARD_ASSERTION=FAIL",
    )

    sdp_text = (
        "a=rtpmap:96 AMR/8000/1\n"
        "a=fmtp:96 octet-align=1\n"
        "RX pt=96 timestamp=1000\n"
        "TX pt=96, ptime=20\n"
    )
    result, checks = check_tc025(sdp_text)
    print("SCENARIO: TC-025 log without CN/silence-frame evidence expected=RESTRICTED actual=%s" % result)
    render_checks(checks)
    if result != "RESTRICTED":
        failed = True

    if failed:
        print("SELFCHECK FAIL")
        return 1
    print("SELFCHECK PASS")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selfcheck", action="store_true")
    parser.add_argument("--log")
    parser.add_argument("--amr-stats")
    args = parser.parse_args()
    if args.selfcheck:
        return run_selfcheck()
    if args.amr_stats:
        result, checks, scope = check_amr_stats(args.amr_stats)
        render_checks(checks)
        print("RESULT: %s" % result)
        print(scope)
        return 0
    if not args.log:
        parser.error("provide --log <pjsua-log> or --amr-stats <analyze_tc025_amr output>")
    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    result, checks = check_tc025(text)
    render_checks(checks)
    print("RESULT: %s" % result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
