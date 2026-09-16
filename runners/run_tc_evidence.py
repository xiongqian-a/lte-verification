#!/usr/bin/env python3
"""Run TC scripts against current local evidence logs and report statuses.

This is a reproducibility helper, not a conformance judgement. It records
which artifacts were used and whether each verdict script returned PASS,
LIMITED PASS, EXPECTED FAIL, or FAIL in the local/testbed sense.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from _paths import EVIDENCE, ROOT


LOCAL = EVIDENCE / "local"
EXTERNAL = EVIDENCE / "external"


def evidence_path(*parts):
    return str(EVIDENCE.joinpath(*parts))


def cmd(name, script, *args, expected_status="PASS", note=""):
    return {
        "name": name,
        "script": str(ROOT / "runners" / script),
        "args": list(args),
        "expected_status": expected_status,
        "note": note,
    }


def build_cases():
    return [
        cmd("tc001_ims_pdn", "tc001_ims_pdn_evidence.py",
            "--log", evidence_path("local", "tc004-nas-test-20260914", "nas_test_rerun_20260914.log"),
            note="server nas_test rerun 2026-09-14 UE-side IMS APN PDN evidence"),
        cmd("tc004_pdn_reject", "tc004_pdn_reject_evidence.py",
            "--log", evidence_path("local", "tc004-nas-test-20260914", "nas_test_rerun_20260914.log"),
            note="server nas_test rerun 2026-09-14 PDN REJECT state/backoff evidence"),
        cmd("tc005_dual_pdn", "tc005_dual_pdn.py",
            "--ue", evidence_path("external", "TC005-dual-pdn-20260914", "log", "ue.log"),
            "--mme", evidence_path("external", "TC005-dual-pdn-20260914", "log", "mme.log"),
            "--smf", evidence_path("external", "TC005-dual-pdn-20260914", "log", "smf.log"),
            "--sgwc", evidence_path("external", "TC005-dual-pdn-20260914", "log", "sgwc.log"),
            "--ue-since", "2026-09-14T10:47:29",
            "--core-since", "09/14 18:47",
            expected_status="LIMITED_PASS",
            note="co1750 Open5GS dual-PDN: internet + ims, EBI=6/7 and Create Bearer Response; IPv6 and official verdict remain restricted"),
        cmd("tc011_register_flow", "tc011_register_flow.py",
            "--log", evidence_path("external", "tc12-tc13-calls-raw.log"),
            expected_status="LIMITED_PASS",
            note="raw pjsua base registration evidence; Security headers/IPsec SA/reg-event/PIXIT/SS verdict remain restricted"),
        cmd("tc011_ipsec_ss_sim", "tc011_ipsec_ss_sim.py",
            "--selftest",
            "--out-dir", evidence_path("local", "tc011-l1-20260916"),
            note="L1_LOCAL_SIMULATED: Annex C.2 Steps 4-11 over real UDP sockets with Security-Client/Security-Verify, SUBSCRIBE/NOTIFY, and both HMAC PIXIT rounds; no kernel xfrm and no official SS verdict"),
        cmd("tc012_mo_call", "tc012_mo_call.py",
            "--log", evidence_path("external", "tc12-tc13-calls-raw.log"),
            note="raw pjsua MO call evidence"),
        cmd("tc013_invalid_auth", "tc013_invalid_auth.py",
            "--log", evidence_path("external", "step2-tc013-mac-invalid.msg"),
            note="synthetic invalid AKA MAC fixture from 34.229-1-oriented step"),
        cmd("tc013_real_bad_key", "tc013_invalid_auth.py",
            "--log", evidence_path("external", "tc013-real-invalid-key-pjsua-20260903.log"),
            expected_status="EXPECTED_FAIL",
            note="real bad-key pjsua log is not an official invalid AKA challenge; local verdict FAIL is expected"),
        cmd("tc014_rereg", "tc014_rereg.py",
            "--raw", "--log", evidence_path("local", "tc014-longexp-20260914", "tc014-longexp-1800-3rereg-20260914.log"),
            note="2026-09-14 server log: 8 REGISTER, 4x401/4x200, CSeq increments, Expires=1800; official timing/IPSEC/PANI remain N/A"),
        cmd("tc015_restoration", "tc015_restoration.py",
            "--log", evidence_path("external", "tc015-504-local-pty-20260910.log"),
            note="local 504 + restoration REGISTER evidence"),
        cmd("tc016_duplicate_register", "tc016_duplicate_register.py",
            "--raw", "--log", evidence_path("external", "tc014-st06-auto-20260828A.log"),
            note="same Call-ID repeated REGISTER evidence from server auto-registration"),
        cmd("tc017_two_calls", "tc017_two_calls.py",
            "--log", evidence_path("external", "tc12-tc13-calls-raw.log"),
            note="raw pjsua two-call evidence"),
        cmd("tc018_malformed_register", "tc018_malformed_register.py",
            "--log", evidence_path("external", "tc018-local-inject-evidence-20260910.log"),
            note="local malformed REGISTER injection evidence"),
        cmd("tc019_mt_call", "tc019_mt_call.py",
            "--log", evidence_path("external", "tc019-mt-b.log"),
            note="real MT call pjsua log"),
        cmd("tc020_hold_retrieve", "tc020_hold_retrieve.py",
            "--log", evidence_path("external", "tc020-hold-a.log"),
            note="real hold/retrieve pjsua log"),
        cmd("tc021_conference_refer", "tc021_conference_refer.py",
            "--log", evidence_path("external", "tc021-refer-a.log"),
            note="real conference REFER pjsua log"),
        cmd("tc021_conference_join", "tc021_conference_join_remote.py",
            "--list", evidence_path("external", "conference-20260904-full", "conf_dual_capture_list.txt"),
            "--ua1", evidence_path("external", "conference-20260904-full", "conf_dual_capture_ua1.log"),
            "--ua2", evidence_path("external", "conference-20260904-full", "conf_dual_capture_ua2.log"),
            "--console", evidence_path("external", "conference-20260904-full", "conf_dual_capture_console.log"),
            note="co1750 dual-ua conference join + FreeSWITCH 2-member list evidence"),
        cmd("tc022_audio_media", "tc022_audio_media.py",
            "--log", evidence_path("external", "tc12-tc13-calls-raw.log"),
            note="raw pjsua audio media evidence"),
        cmd("tc023_sdp_negotiation", "tc023_sdp_negotiation.py",
            "--log", evidence_path("external", "tc12-tc13-calls-raw.log"),
            note="raw pjsua SDP evidence"),
        cmd("tc024_long_stability", "tc024_long_stability.py",
            "--log", evidence_path("external", "tc024-long-local-pty-20260910.log"),
            note="local 131s stability evidence"),
        cmd("tc025_vad_dtx", "tc025_vad_dtx.py",
            "--amr-stats", evidence_path("local", "tc025-longsilence-20260914", "amr-stats.txt"),
            expected_status="LIMITED_PASS",
            note="2026-09-14 bandwidth-efficient AMR rerun: speech=218, NO_DATA=10, SID=4; SID cadence=1000 frames and NO_DATA transmitted; LOCAL_BEHAVIOR=PARTIAL, STANDARD_ASSERTION=FAIL"),
        cmd("tc032_error_codes", "tc032_error_codes.py",
            "--log503", evidence_path("external", "tc032-503-local-20260910-r2.stdout.log"),
            note="local 503 + Retry-After retry evidence"),
        cmd("tc033_timer_timeout", "tc033_timer_timeout.py",
            "--log", evidence_path("external", "tc033-blackhole-local-20260910.stdout.log"),
            note="local blackhole INVITE timeout evidence"),
    ]


NOT_SCRIPTED_CASES = [
    ("TC-001 IMS APN PDN 连接", "1", "nas_test UE 侧 IMS APN PDN 请求/accept 字段证据",
     "缺真实 eNB/EPC 端到端；当前为 UE 侧/测试台证据",
     str(LOCAL / "tc004-nas-test-20260914" / "nas_test_rerun_20260914.log")),
    ("TC-002 专用 Bearer 建立", "1", "UE 单测注入/字段证据",
     "缺真实 EPC 触发专用承载",
     "suites/official_tp_suites/TC-002-专用 Bearer 建立.md"),
    ("TC-003 专用 Bearer 释放", "1", "UE 单测注入/字段证据",
     "缺真实 EPC 触发释放",
     "suites/official_tp_suites/TC-003-专用 Bearer 释放.md"),
    ("TC-004 IMS PDN 拒绝/重试", "1", "本地单测 REJECT cause=0x20 state=INACTIVE backoff=720s 证据",
     "真实核心网注入 REJECT/Extended wait timer 缺；本地单测注入证据已复跑",
     "suites/official_tp_suites/TC-004-IMS PDN 拒绝 _ 重试.md"),
    ("TC-006 RoHC 能力协商", "1", "官方 TP 8.2.1.8 已对齐",
     "真实 RRC/eNB/SS 或一致性仪表缺；本地静态检查不能出官方 Verdict",
     "suites/official_tp_suites/TC-006-RoHC 能力协商.md"),
    ("TC-007 SPS / DRX", "1", "官方 DRX/eDRX 6 条 TP 已对齐",
     "真实 RRC/SS/仪表缺；SPS 无已核到的独立 LTE 一致性 TP",
     "suites/official_tp_suites/TC-007-SPS _ DRX.md"),
    ("TC-008 DRB 建立/释放/重配置", "1", "标准已对齐",
     "真实 eNB/EPC 端到端缺",
     "suites/official_tp_suites/TC-008-DRB 建立 _ 释放 _ 重配置.md"),
    ("TC-009 上行包路由 TFT", "1", "标准已对齐",
     "真实多承载+UL TFT 环境缺",
     "suites/official_tp_suites/TC-009-上行包路由（TFT）.md"),
    ("TC-010 TAU / Service Request / Paging", "1", "标准已对齐",
     "真实 RAN/EPC 触发缺",
     "suites/official_tp_suites/TC-010-TAU _ Service Request _ Paging.md"),
    ("TC-026 SRVCC", "4", "标准已对齐",
     "真实 eNB/EPC/SS 或一致性仪表缺",
     "suites/official_tp_suites/TC-026-SRVCC.md"),
    ("TC-027 aSRVCC", "4", "标准已对齐",
     "真实 aSRVCC/SS 注入缺",
     "suites/official_tp_suites/TC-027-aSRVCC.md"),
    ("TC-028 SSAC 接入控制", "5", "标准已对齐",
     "真实 SIB2 SSAC/RRC 行为观测缺",
     "suites/official_tp_suites/TC-028-SSAC 接入控制.md"),
    ("TC-029 SCM 接入控制", "5", "标准已对齐",
     "真实 SIB2 SCM skip/RRC 行为观测缺",
     "suites/official_tp_suites/TC-029-SCM 接入控制.md"),
    ("TC-030 IMS 紧急呼叫", "6", "co1750 112/110/119/120 功能级 PASS",
     "官方一致性、紧急 PDN、emergency registration 仍受限；本地证据见 69 号文档，未做成可本地复跑脚本",
     "suites/official_tp_suites/TC-030-IMS 紧急呼叫.md"),
    ("TC-031 eCall over IMS", "6", "标准已对齐",
     "缺 eCall/MSD/SLR/PSAP 或一致性仪表",
     "suites/official_tp_suites/TC-031-eCall over IMS.md"),
    ("TC-034 YD/T + 运营商入库", "8", "RESTRICTED",
     "缺具体 YD/T 编号和运营商 VoLTE 入库清单，不能编造",
     "suites/official_tp_suites/TC-034-YD_T + 运营商入库.md"),
]


def render_not_scripted(lines):
    lines += [
        "",
        "## 未进入本地证据矩阵的受限/不可本地复跑用例",
        "",
        "> 以下 TC 已有标准骨架 / 文档证据，但没有进入本脚本证据矩阵：`RESTRICTED` 表示当前环境无法给出本地脚本级 PASS，不等同失败，更不能伪造成 PASS。",
        "",
        "| TC | 模块 | 当前证据 | 阻塞点 | 引用 |",
        "|---|---|---|---|---|",
    ]
    for tc, module, evidence, blocker, ref in NOT_SCRIPTED_CASES:
        lines.append("| %s | %s | %s | %s | `%s` |" % (
            tc.replace("|", "\\|"),
            module,
            evidence.replace("|", "\\|"),
            blocker.replace("|", "\\|"),
            ref,
        ))


def run_case(case, work_dir):
    full_args = [sys.executable, case["script"]]
    raw_value = False
    for a in case["args"]:
        if raw_value:
            full_args.append(a)
            raw_value = False
        elif a.startswith("--"):
            full_args.append(a)
            raw_value = a.endswith("-since")
        else:
            full_args.append(str(Path(a) if Path(a).is_absolute() else ROOT / a))
    proc = subprocess.run(
        full_args,
        cwd=str(work_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (proc.stdout + proc.stderr).strip()
    lines = output.splitlines()
    last = ""
    for line in reversed(lines):
        if line.strip():
            last = line.strip()
            break
    result_match = re.search(r"^RESULT:\s*([A-Z_]+)\s*$", output, flags=re.MULTILINE)
    observed = result_match.group(1) if result_match else None
    if proc.returncode == 0 and observed in {"PASS", "LIMITED_PASS", "RESTRICTED", "FAIL"}:
        status = observed
    elif proc.returncode == 0:
        status = "LIMITED_PASS" if case["expected_status"] == "LIMITED_PASS" else "PASS"
    elif proc.returncode != 0 and case["expected_status"] == "EXPECTED_FAIL":
        status = "EXPECTED_FAIL"
    elif proc.returncode != 0 and case["expected_status"] == "FAIL":
        status = "FAIL"
    else:
        status = "FAIL"
    return {
        "name": case["name"],
        "script": Path(case["script"]).name,
        "args": full_args,
        "expected": case["expected_status"],
        "status": status,
        "returncode": proc.returncode,
        "last_line": last,
        "note": case["note"],
        "output": output,
    }


def render_markdown(results, generated_at):
    ok = sum(1 for r in results if r["status"] in ("PASS", "LIMITED_PASS"))
    expected_fail = sum(1 for r in results if r["status"] == "EXPECTED_FAIL")
    fail = sum(1 for r in results if r["status"] == "FAIL")
    lines = [
        "# 本地证据复跑矩阵（脚本级）",
        "",
        "- 生成时间：%s" % generated_at,
        "- 复制条目：%d" % len(results),
        "- PASS / LIMITED_PASS：%d" % ok,
        "- EXPECTED_FAIL：%d" % expected_fail,
        "- FAIL：%d" % fail,
        "- 口径：本地脚本返回 PASS 仅代表研发行为符合脚本内字段判据，不等于 36.523-1 一致性、pjsua 新栈合规或第三方入网。",
        "",
        "## 汇总",
        "",
        "| 用例 | 脚本 | 状态 | 返回码 | 说明 |",
        "|---|---|---:|---:|---|",
    ]
    for r in results:
        note = r["note"].replace("|", "\\|")
        lines.append("| %s | `%s` | %s | %d | %s |" % (
            r["name"], r["script"], r["status"], r["returncode"], note
        ))
    render_not_scripted(lines)
    lines += ["", "## 命令矩阵", "", "```powershell", "python runners/run_tc_evidence.py", "```", "", "## 详细输出", ""]
    for r in results:
        lines += ["### %s" % r["name"], "", "```text", r["output"] or "(no output)", "```", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", help="write Markdown report to this path")
    parser.add_argument("--json", help="write machine-readable JSON to this path")
    args = parser.parse_args()
    work_dir = ROOT / "runners"
    cases = build_cases()
    results = [run_case(case, work_dir) for case in cases]
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")

    for r in results:
        print("%-28s %-14s rc=%d  %s" % (r["name"], r["status"], r["returncode"], r["last_line"]))
    print("SUMMARY total=%d pass_or_limited=%d expected_fail=%d fail=%d" % (
        len(results),
        sum(1 for r in results if r["status"] in ("PASS", "LIMITED_PASS")),
        sum(1 for r in results if r["status"] == "EXPECTED_FAIL"),
        sum(1 for r in results if r["status"] == "FAIL"),
    ))

    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_markdown(results, generated_at), encoding="utf-8")
        print("REPORT_WRITTEN %s" % path)
    if args.json:
        path = Path(args.json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "generated_at": generated_at,
            "results": results,
            "not_scripted_cases": [
                {
                    "tc": tc,
                    "module": module,
                    "evidence": evidence,
                    "blocker": blocker,
                    "ref": ref,
                }
                for tc, module, evidence, blocker, ref in NOT_SCRIPTED_CASES
            ],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print("JSON_WRITTEN %s" % path)

    return 1 if any(r["status"] == "FAIL" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
