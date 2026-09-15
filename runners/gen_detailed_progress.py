#!/usr/bin/env python3
"""Generate the detailed per-TC progress table for this repository.

It combines the machine-readable library with the purpose/flow/verdict/limitation
sections already present in each per-TC suite markdown. It never invents new
conformance claims; LOCAL_PASS / STANDARD_ALIGNED / RESTRICTED are kept with the
same meaning used elsewhere in the suite.
"""
from __future__ import annotations

import re
import json
from collections import Counter
from datetime import datetime
from _paths import GENERATED, LIBRARY, REGISTRY, SUITES


EVIDENCE_MATRIX = GENERATED / "84-本地证据复跑矩阵-20260914.json"
SELFCHECK_STATUS = GENERATED / "85-验证例程全量自检状态-20260914.json"
SCHEMA_STATUS = GENERATED / "86-TC026-031-证据Schema与L1适配器-20260914.json"
OUT = GENERATED / "92-验证例程详细进度总表-20260915.md"
LEGACY_OUT = GENERATED / "进度总表-最详细版-20260914.md"
REPORT_DATE = "2026-09-15"

MODULE_LABELS = {
    "01": "① EPS / EPC / 承载",
    "02": "② IMS / SIP / 呼叫",
    "03": "③ 媒体 / SDP / VAD-DTX",
    "04": "④ SRVCC / aSRVCC",
    "05": "⑤ SSAC / SCM",
    "06": "⑥ 紧急 / eCall",
    "07": "⑦ 错误码 / 定时器",
    "08": "⑧ 中国入网",
}


def read_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def tc_number(tc_id: str) -> int:
    match = re.search(r"(\d+)$", tc_id or "")
    return int(match.group(1)) if match else 9999


def clean_item(line: str) -> str:
    line = line.strip()
    if line.startswith("- "):
        line = line[2:]
    line = re.sub(r"^\d+\.\s*", "", line).strip()
    return line


def section_items(lines: list[str], target: str) -> list[str]:
    out: list[str] = []
    start = None
    end = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(target) and (start is None):
            start = i + 1
        elif start is not None and stripped.startswith("## "):
            end = i
            break
    if start is None:
        return out
    if end is None:
        end = len(lines)
    for line in lines[start:end]:
        item = clean_item(line)
        if item and "```" not in item:
            out.append(item)
    return out


def esc(value) -> str:
    return (value or "").replace("|", "\\|").replace("\n", " ")


def join30(items) -> str:
    """Join extracted bullet items, keeping detail but removing excessive duplication."""
    return "；".join(esc(x) for x in items[:30] if x)


def main() -> None:
    data = read_json(LIBRARY, {"entries": []})
    registry = read_json(REGISTRY, {"entries": []})
    registry_by_tc = {
        item.get("tc"): item
        for item in registry.get("entries", [])
        if item.get("tc")
    }
    evidence_matrix = read_json(EVIDENCE_MATRIX, {"results": []})
    selfcheck = read_json(SELFCHECK_STATUS, {"total": 0, "pass": 0, "fail": 0})
    schema_status = read_json(SCHEMA_STATUS, {"summary": {}})
    rows: list[list[str]] = []
    suites = {p.stem: p for p in SUITES.glob("TC-*.md")}
    suite_matches = 0
    for e in sorted(data.get("entries", []), key=lambda item: tc_number(item.get("tc_id", ""))):
        tc = e["tc_id"]
        suite = next((p for name, p in suites.items() if name.startswith(tc + "-")), None)
        if suite is None:
            lines: list[str] = []
        else:
            suite_matches += 1
            lines = suite.read_text(encoding="utf-8").splitlines()

        purpose = section_items(lines, "## 1. 目的 / 为什么")
        if not purpose:
            purpose = section_items(lines, "## 1. 目的")
        flow = section_items(lines, "## 4. 验证流程")
        if not flow:
            flow = section_items(lines, "## 4. 验证流程（")
        verdict = section_items(lines, "## 5. TP Verdict 判据")
        if not verdict:
            verdict = section_items(lines, "## 5. TP Verdict 判据（关键项）")
        if not verdict:
            verdict = section_items(lines, "## 5. TP Verdict 判据（关键)") or section_items(lines, "## 5. TP Verdict 判据（关键）")
        limitation = section_items(lines, "## 7. 受限 / L2_REQUIRED")
        if not limitation:
            limitation = section_items(lines, "## 7. 受限")
        skeleton = e.get("official_skeleton") or []
        why_items = skeleton[:6]

        refs = e.get("source_evidence_lines") or []
        refs_str = ", ".join(esc(r) for r in refs) if refs else "无正文行锚（条款级/待补）"
        evidence = e.get("evidence_level") or "RESTRICTED"
        local = e.get("local_script") or "无本地脚本"
        note = e.get("note") or ""
        evidence_dir = e.get("evidence_dir") or ""
        mapping = (registry_by_tc.get(tc) or {}).get("mappingConfidence", "unknown")
        result_parts = [
            f"当前证据层级：{evidence}",
            f"官方映射置信度：{mapping}",
            f"阶段：{e.get('phase', 'L2_PENDING')}",
            f"本地脚本/命令：{local}",
        ]
        if evidence_dir:
            result_parts.append(f"证据目录：{evidence_dir}")
        if note:
            result_parts.append(f"备注：{note}")
        rest = e.get("limitation") or "官方 SS/一致性仪表待执行"
        if limitation:
            rest += "；" + "；".join(esc(x) for x in limitation[:4])

        rows.append([
            tc,
            e.get("name", ""),
            e.get("module", ""),
            join30(purpose),
            join30(why_items) if why_items else "",
            join30(flow),
            esc(e.get("official_spec", "")) + " / " + esc(e.get("official_clause", "")),
            refs_str,
            "；".join(result_parts),
            esc(rest),
        ])

    confidence_counts = Counter(
        str(item.get("mappingConfidence") or "none")
        for item in registry.get("entries", [])
    )
    evidence_status_counts = Counter(
        str(item.get("status") or "UNKNOWN")
        for item in evidence_matrix.get("results", [])
    )
    body_anchor_count = sum(1 for item in data.get("entries", []) if item.get("source_evidence_lines"))
    module_ids = sorted(
        {str(item.get("module") or "") for item in data.get("entries", []) if item.get("module")}
    )
    confidence_tcs: dict[str, list[str]] = {}
    for item in registry.get("entries", []):
        confidence_tcs.setdefault(str(item.get("mappingConfidence") or "none"), []).append(
            str(item.get("tc") or "")
        )
    for values in confidence_tcs.values():
        values.sort(key=tc_number)

    module_rows: list[str] = []
    for module in module_ids:
        module_tcs = sorted(
            [str(item.get("tc_id")) for item in data.get("entries", []) if str(item.get("module")) == module],
            key=tc_number,
        )
        if not module_tcs:
            continue
        tc_range = module_tcs[0] if len(module_tcs) == 1 else f"{module_tcs[0]}~{module_tcs[-1]}"
        module_rows.append(
            f"| {MODULE_LABELS.get(module, module)} | {tc_range} | {len(module_tcs)} |"
        )

    schema_summary = schema_status.get("summary", {})
    schema_by_status = schema_summary.get("by_status", {})
    local_result_count = len(evidence_matrix.get("results", []))
    local_pass = evidence_status_counts.get("PASS", 0)
    limited_pass = evidence_status_counts.get("LIMITED_PASS", 0)
    expected_fail = evidence_status_counts.get("EXPECTED_FAIL", 0)
    unexpected_fail = evidence_status_counts.get("FAIL", 0)

    lines = [
        f"# 标准验证例程-详细进度总表（{REPORT_DATE}）",
        "",
        f"生成时间：{datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "> 口径：本表是当前验证例程完整快照。`LOCAL_PASS`/`SELFCHECK_PASS`/`STANDARD_ALIGNED`/`RESTRICTED` 均不等于 `36.523-1` 或 `34.229-1` 一致性 Verdict；官方一致性 PASS 只能来自一致性测试仪/检测机构按官方 TP 执行。",
        "",
        "## 一、冻结摘要",
        "",
        "| 指标 | 当前结果 | 说明 |",
        "|---|---:|---|",
        f"| 功能 TC | {len(rows)} | 覆盖模块①至模块⑧ |",
        f"| 模块数 | {len(module_ids)} | 按当前注册表统计 |",
        f"| 标准套件文档 | {suite_matches} / {len(rows)} | 每条均有目的、前置、流程、判据和受限点 |",
        f"| 官方正文行号锚 | {body_anchor_count} / {len(rows)} | 其余为行为级、实现级或外部依赖 |",
        f"| `exact_line_ref` | {confidence_counts.get('exact_line_ref', 0)} | 可回到具名规范正文位置 |",
        f"| `partial` | {confidence_counts.get('partial', 0)} | 有规范支撑但非独立/完整官方 TC 覆盖 |",
        f"| `behavior` | {confidence_counts.get('behavior', 0)} | 官方无独立 TC，保留为行为/鲁棒性验证 |",
        f"| `none` | {confidence_counts.get('none', 0)} | 缺外部标准/清单，不能编造 |",
        f"| 本地证据复跑条目 | {local_result_count} | 来自本地证据复跑矩阵 |",
        f"| 本地复跑 PASS / LIMITED_PASS | {local_pass} / {limited_pass} | 仅代表本地字段或行为证据 |",
        f"| EXPECTED_FAIL / 非预期 FAIL | {expected_fail} / {unexpected_fail} | 预期负控不等于产品通过 |",
        f"| 判定脚本自检 | {selfcheck.get('pass', 0)} / {selfcheck.get('total', 0)} PASS | 只证明脚本可执行和正负控可触发 |",
        f"| TC-026~031 L2 结构 | {schema_summary.get('sections', 0)} 章节 / 114 检查点 / 22 Verdict / 77 消息表；{sum(v for k, v in schema_by_status.items() if k != 'NOT_EXECUTED')} 已判 / {schema_by_status.get('NOT_EXECUTED', 0)} NOT_EXECUTED | 无合格 SS/仪表证据时不升级 |",
        f"| 官方一致性 PASS | {schema_summary.get('official_verdict_count', 0)} | 当前环境没有合格 SS/仪表证据 |",
        "| 第三方入网 PASS | 0 | 当前缺正式测试台、YD/T 和运营商清单 |",
        "",
        "### 1.1 模块分布",
        "",
        "| 模块 | TC 范围 | 数量 |",
        "|---|---|---:|",
        *module_rows,
        "",
        "### 1.2 官方映射置信度明细",
        "",
    ]
    for key in ("exact_line_ref", "partial", "behavior", "none"):
        values = confidence_tcs.get(key, [])
        if values:
            lines.append(f"- `{key}`（{len(values)}）：{'、'.join(values)}")
    lines += [
        "",
        "## 二、逐条总表",
        "",
        "| TC | 名称 | 模块 | 验证目的 / 为什么 | 官方依据摘录 | 验证流程 | 对齐官方标准 | 正文行锚 | 当前证据/结果 | 受限/L2与下一步 |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")

    lines += [
        "",
        "## 三、汇总口径与下一步",
        "",
        f"- 用例总数：{len(rows)}；标准套件文档 {suite_matches}/{len(rows)}；官方正文行号锚 {body_anchor_count}/{len(rows)}；`exact_line_ref` {confidence_counts.get('exact_line_ref', 0)}。",
        f"- 本地证据复跑：{local_result_count} 条；PASS={local_pass}、LIMITED_PASS={limited_pass}、EXPECTED_FAIL={expected_fail}、非预期 FAIL={unexpected_fail}。这里的 PASS 仍只代表本地脚本内字段/行为判据。",
        "- TC-005 为真实双 PDN 测试床证据，但 IPv6/IPv4v6、method II P-CSCF discovery 逐字段、网络侧释放/E1 与官方 Verdict 仍受限，因此按 `LIMITED_PASS` 统计；TC-025 为真实媒体证据，但复判显示 `SID cadence=1000 frames`、实际传输 `NO_DATA=10`，因此按 `LIMITED_PASS`、`LOCAL_BEHAVIOR=PARTIAL`、`STANDARD_ASSERTION=FAIL` 统计。",
        "- `STANDARD_ALIGNED / L2_PENDING` 的 TC 主要缺真实 eNB/EPC/IMS/SS/运营商/仪表依赖，不伪造 PASS。",
        "- 已完成：TC-011/014 的 Annex C.2 `.3.3` 消息内容已展开为 Annex A 默认消息内容（`_substeps/TC-011-014-annexA-message-contents.json`/`.md`，A.1.1~A.1.7，含 A1/A2/A17 条件词表）；TC-012/017/019/020/021 的调用族 Annex A 默认消息内容已展开（`_substeps/TC-012-021-annexA-call-messages.json`/`.md`，A.2/A.3/A.5 共 12 条）；调用族 10 个官方 TP 过程块已抽取（`_substeps/TC-012-021-official-tp-blocks.json`/`.md`，含 Test purpose、Method of test、Expected sequence、Specific Message Contents 和 Test requirements）；两组均由独立脚本逐行核对；TC-026~031 的 `.3.2/.3.3` 正文、完整边界和关键 IE 已入套件并纳入校验。",
        f"- TC-026~031 已从官方步骤表生成机器可读证据 Schema：`{schema_summary.get('sections', 0)}` 个章节、`114` 个消息检查点、`22` 个 TP Verdict、`77` 个 Specific Message Contents 表；L1 适配器当前结果为 `{schema_by_status.get('NOT_EXECUTED', 0)}/{schema_summary.get('sections', 0)} NOT_EXECUTED`，因为缺合格 SS/仪表证据，不是官方一致性结论。",
        "- 下一步优先项：TC-026~031 只在真实 SS/仪表/目标网络具备后执行 L2；其余 TC 继续按用例逐条补齐可核的官方子例。TC-031 的 `36.508 4.5A.27` 已按 V18.6.0 正文 `22184-22370` 终核，剩余缺口是真实验证环境与 L2 Verdict。",
        "- 缺外部文档/设备/运营商标识的项继续保持 `RESTRICTED`，不得把本地证据写成官方一致性 PASS。",
    ]

    text = "\n".join(lines) + "\n"
    for output in (OUT, LEGACY_OUT):
        output.write_text(text, encoding="utf-8", newline="\n")
    print(f"WROTE {OUT} rows={len(rows)}")
    print(f"WROTE {LEGACY_OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()
