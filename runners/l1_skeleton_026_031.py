#!/usr/bin/env python3
"""L1 skeleton and official-TP extraction guard for TC-026..TC-031.

This is not a conformance runner. It checks that each suite document contains
the official TP excerpt, the corrected Main/Parallel table boundaries, the
`.3.3` message-content index, and the L1 environment-gap declaration. It does
not emit an official conformance verdict.
"""
from __future__ import annotations

import json
import sys
from _paths import SUBSTEPS, SUITES


SUBSTEPS = SUBSTEPS / "TC-026-031-3.2-main-behaviour.json"

TC_META = {
    "TC-026": {
        "title": "SRVCC",
        "deps": "real eNB/EPC + UTRA/GERAN CS voice + SS/仪表",
        "probe": "MobilityFromEUTRACommand",
        "probe2": "HANDOVER TO UTRAN COMPLETE",
        "sections": {
            "13.4.3.1": (254445, 254529, 1),
            "13.4.3.2": (255101, 255185, 2),
            "13.4.3.3": (255687, 255740, 0),
        },
        "specific_markers": {
            "13.4.3.1": (
                "cs-FallbackIndicator False",
                "targetRAT-Type Utra",
                "nas-SecurityParamFromEUTRA",
                "Ciphering mode info",
                "PDP context status",
            ),
            "13.4.3.2": (
                "cs-FallbackIndicator False",
                "targetRAT-Type Utra",
                "PDP context status",
            ),
            "13.4.3.3": (
                "targetRAT-Type geran",
                "bandIndicator",
                "Network Colour Code",
                "Base Station Colour Code",
            ),
        },
    },
    "TC-027": {
        "title": "aSRVCC",
        "deps": "real eNB/EPC + aSRVCC access transfer + SS/仪表",
        "probe": "MobilityFromEUTRACommand",
        "probe2": "MO/MT alerting",
        "sections": {
            "13.4.3.7": (257924, 258033, 2),
            "13.4.3.10": (259967, 260057, 1),
        },
        "specific_markers": {
            "13.4.3.7": (
                "targetRAT-Type utra",
                "CONNECT (step 30",
                "TI flag",
                "TIO",
            ),
            "13.4.3.10": (
                "targetRAT-Type utra",
                "CONNECT (step 39",
                "TI flag",
                "TIO",
            ),
        },
    },
    "TC-028": {
        "title": "SSAC 接入控制",
        "deps": "SIB2 ssac-BarringForMMTEL-Voice-r9 = 0%, back-off Ty + real RRC",
        "probe": "ssac-BarringForMMTEL-Voice-r9",
        "probe2": "back-off Ty",
        "sections": {
            "13.5.1": (275717, 275752, 0),
            "13.5.1a": (275881, 275931, 0),
        },
        "specific_markers": {
            "13.5.1": (
                "ssac-BarringForMMTEL-Voice-r9",
                "ac-BarringFactor p00",
                "ac-BarringTime s64",
                "ac-BarringForSpecialAC '11111'B",
                "systemInfoModification TRUE",
            ),
            "13.5.1a": (
                "ssac-BarringForMMTEL-Voice-r9",
                "ac-BarringFactor p00",
                "ac-BarringTime s64",
                "ac-BarringForSpecialAC '11111'B",
            ),
        },
    },
    "TC-029": {
        "title": "SCM 接入控制",
        "deps": "SIB2 ac-BarringForMO-data=0% + ac-BarringSkipForMMTELVoice-r12 + real RRC",
        "probe": "ac-BarringSkipForMMTELVoice-r12",
        "probe2": "ac-BarringForMO-data",
        "sections": {
            "13.5.4": (276828, 276861, 0),
        },
        "specific_markers": {
            "13.5.4": (
                "ac-BarringForMO-Data",
                "ac-BarringFactor p0",
                "ac-BarringTime s512",
                "ac-BarringSkipForMMTELVoice-r12 TRUE",
            ),
        },
    },
    "TC-030": {
        "title": "IMS 紧急呼叫",
        "deps": "emergency RRC/SERVICE REQUEST + emergency PDN + real IMS/eNB/EPC",
        "probe": "PDN CONNECTIVITY REQUEST",
        "probe2": "request type=emergency",
        "sections": {
            "11.2.1": (235400, 235467, 0),
        },
        "specific_markers": {
            "11.2.1": (
                "Emergency number list",
                "TS 24.008, 10.5.3.13",
            ),
        },
    },
    "TC-031": {
        "title": "eCall over IMS",
        "deps": "eCall Only mode + MSD + RACH failure injection + PSAP/SLR + SS/仪表",
        "probe": "MSD",
        "probe2": "eCall Only",
        "sections": {
            "11.3.5": (240686, 240820, 1),
            "11.3.8": (241142, 241207, 0),
        },
        "specific_markers": {
            "11.3.5": (
                "Establishment cause Emergency Call",
                "CM service type 0010 Emergency call",
                "Establishment cause 101 Emergency call",
            ),
            "11.3.8": (
                "targetRAT-Type GERAN",
                "Network Colour Code",
                "Base Station Colour Code",
                "PDP context status",
            ),
        },
    },
}

FORBIDDEN_CLAIMS = (
    "官方一致性 PASS",
    "官方一致性PASS",
    "CONFORMANCE PASS",
    "PASS: 36.523-1",
)


def check_tc(tc_id: str, extracted: dict[str, list[dict]]) -> bool:
    meta = TC_META[tc_id]
    suite = next(p for p in SUITES.glob(f"{tc_id}-*.md"))
    text = suite.read_text(encoding="utf-8")
    ok = True
    probes = tuple(m for m in (meta["probe"], meta.get("probe2")) if m)
    for marker in (
        "官方 TP 原文要点",
        "官方 .3.2/.3.3 子例级原文抽取",
        "关键官方判据",
        "Main behaviour 原文（逐行）",
        ".3.3 行",
        "L1 测试骨架",
        *probes,
    ):
        if marker not in text:
            ok = False
            print(f"[L1-SKELETON] {tc_id} missing marker: {marker}")
    for claim in FORBIDDEN_CLAIMS:
        if claim in text:
            ok = False
            print(f"[L1-SKELETON] {tc_id} forbidden claim: {claim}")

    sections = {item["section"]: item for item in extracted.get(tc_id, [])}
    for section, (main_line, main_end, parallel_count) in meta["sections"].items():
        item = sections.get(section)
        if item is None:
            ok = False
            print(f"[L1-SKELETON] {tc_id} {section} missing from JSON")
            continue
        got = (
            item.get("main_behaviour_line"),
            item.get("main_behaviour_end_line"),
            len(item.get("parallel_behaviour_tables", [])),
        )
        expected = (main_line, main_end, parallel_count)
        if got != expected:
            ok = False
            print(
                f"[L1-SKELETON] {tc_id} {section} boundary mismatch: "
                f"got={got} expected={expected}"
            )
        if item.get("specific_message_line") is None:
            ok = False
            print(f"[L1-SKELETON] {tc_id} {section} missing .3.3 anchor")
        raw_rows = "\n".join(
            text
            for table in item.get("specific_message_tables", [])
            for _, text in table.get("raw_rows", [])
        )
        for marker in meta.get("specific_markers", {}).get(section, ()):
            if not raw_rows or marker not in raw_rows:
                ok = False
                print(
                    f"[L1-SKELETON] {tc_id} {section} missing .3.3 IE marker: "
                    f"{marker}"
                )
            if marker not in text:
                ok = False
                print(
                    f"[L1-SKELETON] {tc_id} {section} marker absent from suite: "
                    f"{marker}"
                )
    print(
        f"{tc_id} {meta['title']}: official_tp={'OK' if ok else 'MISSING'}; "
        f"need={meta['deps']}; probe={meta['probe']}"
    )
    return ok


def main() -> None:
    print("L1 SKELETON + OFFICIAL-TP BOUNDARY CHECK (TC-026..031)")
    if not SUBSTEPS.exists():
        print(f"[L1-SKELETON] missing extraction JSON: {SUBSTEPS}")
        print("L1_SKELETON RESULT: MISSING")
        return 1
    extracted = json.loads(SUBSTEPS.read_text(encoding="utf-8"))
    ok = all(check_tc(tc, extracted) for tc in TC_META)
    if not ok:
        print("L1_SKELETON RESULT: MISSING")
        return 1
    print("L1_SKELETON RESULT: OK (no official conformance verdict emitted)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
