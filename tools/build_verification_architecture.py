#!/usr/bin/env python3
"""Build the self-contained verification architecture HTML page.

The generated page embeds the registry and library JSON so it can be opened
directly in a browser without a web server or network access.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "official_tp_registry.json"
LIBRARY_PATH = ROOT / "registry" / "official_tp_library.json"
SERVER_EVIDENCE_PATH = ROOT / "registry" / "server_evidence_index.json"
SUITE_DIR = ROOT / "suites" / "official_tp_suites"
TEMPLATE_PATH = ROOT / "tools" / "verification_architecture_template.html"
DEFAULT_OUTPUT = ROOT / "verification-architecture.html"

import sys

sys.path.insert(0, str(ROOT / "runners"))
from _repro import generated_timestamp, portable_text  # noqa: E402


MODULES: dict[str, dict[str, Any]] = {
    "01": {
        "title": "LTE / EPS 接入与承载",
        "short": "接入与承载",
        "purpose": "验证 EPS Attach、PDN、默认/专用承载、RRC 能力、DRB、TFT、TAU、Service Request 与 Paging 等基础链路行为。",
        "layer": "L0 官方 TP 骨架 + 局部 L1 证据",
        "accent": "blue",
    },
    "02": {
        "title": "IMS / SIP 注册与呼叫",
        "short": "IMS 注册与呼叫",
        "purpose": "验证 IMS 初始注册、重注册、恢复、MO/MT 呼叫、双呼叫、保持/取回、会议与 REFER 等 SIP 行为。",
        "layer": "L0 官方 TP 骨架 + L1 本地 IMS/媒体台",
        "accent": "teal",
    },
    "03": {
        "title": "媒体面、SDP 与语音活动",
        "short": "媒体与 SDP",
        "purpose": "验证音频媒体、SDP 协商、长稳以及 VAD/DTX、SID、RTP 载荷与静默抑制行为。",
        "layer": "L0 规范判据 + L1 媒体证据",
        "accent": "violet",
    },
    "04": {
        "title": "SRVCC / aSRVCC",
        "short": "SRVCC",
        "purpose": "验证 IMS 语音在 LTE 与 UTRAN/GERAN 之间的 SRVCC/aSRVCC 切换流程、消息序列与状态保持。",
        "layer": "L0 官方 TP 骨架 + L2 仪表待执行",
        "accent": "amber",
    },
    "05": {
        "title": "SSAC / SCM 接入控制",
        "short": "接入控制",
        "purpose": "验证 SIB2 中 SSAC、SCM 与跳过接入控制条件下，UE 对不同接入等级的拦截/放行行为。",
        "layer": "L0 官方 TP 骨架 + L2 仪表待执行",
        "accent": "rose",
    },
    "06": {
        "title": "紧急呼叫与 eCall",
        "short": "紧急与 eCall",
        "purpose": "验证 IMS Emergency Call、eCall over IMS、MSD、SLR/PSAP 交互及紧急承载建立。",
        "layer": "L0 官方 TP 骨架 + 局部 L1 呼叫证据",
        "accent": "red",
    },
    "07": {
        "title": "错误码与 SIP 定时器",
        "short": "错误与定时器",
        "purpose": "验证 503/504、Retry-After、恢复注册以及 SIP Timer A/B/D/E/F/G/H/I/J 等超时与重传行为。",
        "layer": "L0 官方/规范判据 + L1 本地响应器",
        "accent": "orange",
    },
    "08": {
        "title": "YD/T 与运营商准入",
        "short": "入网准入",
        "purpose": "承载 YD/T 与运营商 VoLTE 入库要求的映射、差异分析和外部送测证据。",
        "layer": "L2 外部依赖 / 当前 RESTRICTED",
        "accent": "slate",
    },
}


STANDARD_ROLES = {
    "36.523-1": "E-UTRA / LTE UE 一致性测试流程、前置条件、Expected Sequence 与 TP Verdict。",
    "34.229-1": "IMS UE 一致性测试流程，覆盖注册、鉴权、呼叫、SDP、媒体、保持与会议等。",
    "36.508": "LTE 通用测试环境、默认消息参数、系统配置与 Specific Message Contents 派生来源。",
    "36.509": "测试中的特殊一致性功能、Test Control 与相关测试环境约束。",
    "36.523-2": "36.523-1 测试用例的适用性、UE 能力与实现一致性声明。",
    "34.108": "通用 UE 测试环境、无线承载配置与通用测试流程。",
    "24.229": "IMS 中 IP 多媒体呼叫控制协议、SIP 头域、定时器与服务行为。",
    "24.301": "EPS NAS 协议，覆盖 EMM/ESM 状态机、cause、T3482、T3346 与 back-off。",
    "24.173": "IMS 补充服务，覆盖保持、会议、REFER 等 MMTel 行为。",
    "24.628": "IMS 紧急呼叫相关协议行为与紧急注册/会话流程。",
    "26.114": "MTSI 媒体处理，覆盖 SDP、RTP、编解码与媒体质量约束。",
    "26.093": "AMR 源受控速率、DTX、SID 与静默期行为。",
    "26.193": "AMR 源受控速率测试方法。",
    "26.450": "EVS 编解码器一般描述与媒体能力。",
    "26.451": "EVS 源受控速率、DTX/VAD 与 SID 行为。",
    "RFC 3261": "SIP 基础协议与 Timer A/B/D/E/F/G/H/I/J 等事务/会话定时器。",
}


RUNNERS = [
    {
        "path": "run_official_suite.py",
        "role": "统一入口：重建派生数据、完整性检查、自检、证据复跑、L2 适配器及报告生成。",
        "layer": "L0 + L1",
    },
    {
        "path": "runners/run_official_suite_checks.py",
        "role": "检查 34 份官方 TP 套件文档、元数据、必需章节和模板完整性。",
        "layer": "L0",
    },
    {
        "path": "runners/build_official_library.py",
        "role": "从套件文档生成机器可读 official_tp_library.json。",
        "layer": "L0",
    },
    {
        "path": "runners/run_tc_selfchecks.py",
        "role": "运行所有判定脚本的合成正控/负控自检，验证脚本自身可执行，不产生官方 Verdict。",
        "layer": "L1",
    },
    {
        "path": "runners/run_tc_evidence.py",
        "role": "使用已固化的本地、测试台、pjsua 和抓包日志复跑字段级/行为级断言。",
        "layer": "L1",
    },
    {
        "path": "runners/run_l1_evidence_adapter_026_031.py",
        "role": "评估 TC-026 至 TC-031 的合格 SS/实验室证据；缺 manifest 时保持 NOT_EXECUTED。",
        "layer": "L1 -> L2",
    },
    {
        "path": "runners/report_factory.py",
        "role": "输出官方风格状态报告，明确区分 LOCAL_PASS、RESTRICTED 与 NO_OFFICIAL_VERDICT。",
        "layer": "报告",
    },
    {
        "path": "runners/colleague_replay_verification.py",
        "role": "面向同事的全新目录复跑、已提交证据哈希和结果验收检查。",
        "layer": "审计",
    },
]


WORKFLOW = [
    {
        "step": "01",
        "title": "抽取官方 TP",
        "detail": "从具名规范正文提取章节、前置条件、Expected Sequence、Specific Message Contents 与 TP Verdict。",
        "artifact": "official_tp_library.json / _substeps/",
    },
    {
        "step": "02",
        "title": "建立标准例程",
        "detail": "每条内部 TC 形成目的、官方骨架、前置条件、验证流程、判据、证据与受限边界。",
        "artifact": "suites/official_tp_suites/TC-xxx.md",
    },
    {
        "step": "03",
        "title": "执行 L1 判定",
        "detail": "使用真实日志、pjsua、srsRAN/Open5GS、本地 IMS 或响应器复跑字段级/行为级断言。",
        "artifact": "runners/tc*.py / evidence/",
    },
    {
        "step": "04",
        "title": "分类证据等级",
        "detail": "按 LOCAL_PASS、LIMITED_PASS、SELFCHECK_PASS、STANDARD_ALIGNED、RESTRICTED 如实记录。",
        "artifact": "generated/*.md",
    },
    {
        "step": "05",
        "title": "适配 L2 证据",
        "detail": "合格 SS/仪表/实验室结果进入独立 adapter；本地日志不会自动升级为官方 P/F。",
        "artifact": "evidence manifest / L2 adapter",
    },
    {
        "step": "06",
        "title": "外部一致性裁定",
        "detail": "最终 OFFICIAL_PASS/OFFICIAL_FAIL 只能由合格系统模拟器或认可实验室按官方 TP 给出。",
        "artifact": "实验室/仪表报告",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    # Historical extraction notes are useful, but a published page must not
    # expose or depend on the machine that produced them.
    text = portrait_paths(text)
    return text


def portrait_paths(text: str) -> str:
    text = re.sub(
        r"(?:[A-Za-z]:[\\/]|/Users/|/home/)[^\s`<>)\]]+",
        "<external-path>",
        text,
    )
    return portable_text(text, ROOT)


def extract_markdown_section(text: str, heading_keyword: str) -> str:
    pattern = re.compile(
        rf"^##\s+[^\n]*{re.escape(heading_keyword)}[^\n]*\n(.*?)(?=^##\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_code_blocks(text: str) -> list[str]:
    return [block.strip() for block in re.findall(r"```(?:text|powershell)?\s*\n(.*?)```", text, flags=re.DOTALL)]


def parse_suite_document(tc_id: str) -> dict[str, Any]:
    matches = sorted(SUITE_DIR.glob(f"{tc_id}-*.md"))
    if not matches:
        return {
            "path": None,
            "purpose": "",
            "evidence_text": "",
            "restriction_text": "",
            "commands": [],
        }
    path = matches[0]
    text = path.read_text(encoding="utf-8")
    return {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "purpose": extract_markdown_section(text, "目的"),
        "evidence_text": extract_markdown_section(text, "当前本地证据"),
        "restriction_text": extract_markdown_section(text, "受限"),
        "commands": extract_code_blocks(extract_markdown_section(text, "执行命令")),
    }


def normalize_boundary(boundary: dict[str, Any]) -> dict[str, Any]:
    tables = []
    for table in boundary.get("specific_message_tables") or []:
        tables.append(
            {
                "name": clean_text(table.get("table")),
                "line": table.get("table_line"),
                "end": table.get("table_end_line"),
                "derivations": [clean_text(item) for item in table.get("derivation_paths") or []],
            }
        )
    parallel = []
    for table in boundary.get("parallel_behaviour_tables") or []:
        parallel.append(
            {
                "name": clean_text(table.get("table")),
                "line": table.get("table_line"),
                "end": table.get("table_end_line"),
            }
        )
    return {
        "section": clean_text(boundary.get("section")),
        "title": clean_text(boundary.get("title")),
        "source_spec": clean_text(boundary.get("source_spec")),
        "source_version": clean_text(boundary.get("source_version")),
        "body_line": boundary.get("body_line"),
        "tp_line": boundary.get("tp_line"),
        "conformance_line": boundary.get("conformance_line"),
        "test_description_line": boundary.get("test_description_line"),
        "pre_test_line": boundary.get("pre_test_line"),
        "procedure_line": boundary.get("procedure_line"),
        "main_behaviour_table": clean_text(boundary.get("main_behaviour_table")),
        "main_behaviour_line": boundary.get("main_behaviour_line"),
        "main_behaviour_end_line": boundary.get("main_behaviour_end_line"),
        "parallel_behaviour_tables": parallel,
        "specific_message_line": boundary.get("specific_message_line"),
        "specific_message_end_line": boundary.get("specific_message_end_line"),
        "specific_message_tables": tables,
    }


def split_status(raw: Any) -> str:
    value = clean_text(raw, "NOT_EXECUTED")
    return value.split("|", 1)[0].strip() or "NOT_EXECUTED"


def build_payload(
    registry: dict[str, Any],
    library: dict[str, Any],
    server_evidence: dict[str, Any],
) -> dict[str, Any]:
    registry_entries = {entry["tc"]: entry for entry in registry.get("entries", [])}
    library_entries = {entry["tc_id"]: entry for entry in library.get("entries", [])}
    all_ids = sorted(set(registry_entries) | set(library_entries))

    cases = []
    for tc_id in all_ids:
        reg = registry_entries.get(tc_id, {})
        lib = library_entries.get(tc_id, {})
        suite = parse_suite_document(tc_id)
        cases.append(
            {
                "tc_id": tc_id,
                "name": clean_text(lib.get("name") or reg.get("name"), tc_id),
                "module": clean_text(lib.get("module") or reg.get("module"), "00"),
                "official_spec": clean_text(lib.get("official_spec") or reg.get("officialSpec"), "未指定"),
                "official_clause": clean_text(lib.get("official_clause") or reg.get("officialClause"), "未指定"),
                "mapping_confidence": clean_text(
                    lib.get("mapping_confidence") or reg.get("mappingConfidence"), "none"
                ),
                "evidence_level": clean_text(lib.get("evidence_level") or reg.get("evidenceLevel"), "NOT_EXECUTED"),
                "status": split_status(lib.get("evidence_level") or reg.get("evidenceLevel")),
                "phase": clean_text(lib.get("phase"), "L2_PENDING"),
                "local_script": clean_text(lib.get("local_script") or reg.get("localScript"), "null"),
                "blocker": clean_text(lib.get("limitation") or reg.get("blocker"), ""),
                "note": clean_text(lib.get("note") or reg.get("note"), ""),
                "purpose": suite["purpose"],
                "preconditions": [clean_text(item) for item in lib.get("preconditions") or []],
                "steps": [clean_text(item) for item in lib.get("steps") or []],
                "verdicts": [clean_text(item) for item in lib.get("verdicts") or []],
                "official_skeleton": [
                    clean_text(item) for item in lib.get("official_skeleton") or []
                ],
                "primary_evidence": [
                    clean_text(item) for item in lib.get("primary_evidence") or reg.get("primaryEvidence") or []
                ],
                "cross_reference_evidence": [
                    clean_text(item)
                    for item in lib.get("cross_reference_evidence") or reg.get("crossReferenceEvidence") or []
                ],
                "source_evidence_lines": [
                    clean_text(item) for item in lib.get("source_evidence_lines") or []
                ],
                "official_boundaries": [
                    normalize_boundary(item) for item in lib.get("official_boundaries") or []
                ],
                "evidence_dir": clean_text(lib.get("evidence_dir") or reg.get("evidenceDir"), ""),
                "evidence_scope": clean_text(lib.get("evidence_scope") or reg.get("evidenceScope"), ""),
                "last_updated": clean_text(lib.get("last_updated"), ""),
                "suite_path": suite["path"],
                "evidence_text": suite["evidence_text"],
                "restriction_text": suite["restriction_text"],
                "commands": suite["commands"],
            }
        )

    used_standards: dict[str, set[str]] = {}
    for case in cases:
        spec = case["official_spec"]
        for key in STANDARD_ROLES:
            if key.lower() in spec.lower():
                used_standards.setdefault(key, set()).add(case["tc_id"])

    standards = [
        {
            "id": key,
            "role": role,
            "used_by": sorted(used_standards.get(key, set())),
            "source": clean_text((registry.get("sources") or {}).get(key.replace(".", "").replace("-", "")), ""),
        }
        for key, role in STANDARD_ROLES.items()
    ]

    return {
        "meta": {
            "title": "LTE / IMS 标准验证例程架构",
            "version": registry.get("version") or library.get("version") or "",
            "scope": clean_text(registry.get("scope")),
            "policy": [clean_text(item) for item in registry.get("policy") or []],
            "generated_at": generated_timestamp(),
            "source_files": [
                str(REGISTRY_PATH.relative_to(ROOT)).replace("\\", "/"),
                str(LIBRARY_PATH.relative_to(ROOT)).replace("\\", "/"),
                str(SERVER_EVIDENCE_PATH.relative_to(ROOT)).replace("\\", "/"),
            ],
        },
        "modules": MODULES,
        "cases": cases,
        "standards": standards,
        "runners": RUNNERS,
        "workflow": WORKFLOW,
        "server_evidence": server_evidence,
        "official_verdict": {
            "status": "NO_OFFICIAL_VERDICT",
            "statement": "本页只展示官方 TP 对齐、本地验证与证据状态；真值 P/F 必须由合格 SS、仪表或认可实验室按官方 TP 产生。",
        },
    }


def render(template: str, payload: dict[str, Any]) -> str:
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    data_json = data_json.replace("<", "\\u003c")
    return (
        template.replace("__VERIFICATION_DATA_JSON__", data_json)
        .replace("__GENERATED_AT__", payload["meta"]["generated_at"])
        .replace("__VERSION__", payload["meta"]["version"])
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--template", type=Path, default=TEMPLATE_PATH)
    args = parser.parse_args()

    registry = load_json(REGISTRY_PATH)
    library = load_json(LIBRARY_PATH)
    server_evidence = load_json(SERVER_EVIDENCE_PATH)
    payload = build_payload(registry, library, server_evidence)
    template = args.template.read_text(encoding="utf-8")
    output = render(template, payload)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8", newline="\n")
    print(f"WROTE {args.output}")
    print(f"CASES {len(payload['cases'])}")
    print(f"BYTES {len(output.encode('utf-8'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
