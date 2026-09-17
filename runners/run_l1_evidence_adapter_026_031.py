#!/usr/bin/env python3
"""Evaluate optional real evidence against the TC-026..031 official step schema.

Without an evidence manifest this is a readiness check and reports
NOT_EXECUTED. It only emits an official verdict when the evidence declares a
qualified SS/conformance instrument or accredited laboratory and supplies
actual results for every official TP Verdict row.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _paths import GENERATED, ROOT, SUITE_EVIDENCE, ensure_output_dirs
from _repro import generated_epoch, portable_path, write_text_lf

SCHEMA = SUITE_EVIDENCE / "TC-026-031-evidence-schema.json"
DEFAULT_MANIFEST = SUITE_EVIDENCE / "TC-026-031-evidence-manifest.json"
DEFAULT_JSON = GENERATED / "86-TC026-031-证据Schema与L1适配器-20260914.json"
DEFAULT_REPORT = GENERATED / "86-TC026-031-证据Schema与L1适配器-20260914.md"

OFFICIAL_SOURCE_TYPES = {"ss_conformance_instrument", "accredited_lab"}
STATUS_ORDER = [
    "OFFICIAL_PASS",
    "OFFICIAL_FAIL",
    "INCONCLUSIVE",
    "LOCAL_ONLY",
    "NOT_EXECUTED",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(schema: dict) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for tc in schema.get("cases", []):
        tc_id = tc.get("tc_id")
        if not tc_id:
            errors.append("case without tc_id")
            continue
        if not tc.get("sections"):
            errors.append(f"{tc_id}: no sections")
        for section in tc["sections"]:
            section_id = f"{tc_id}:{section.get('section')}"
            if not section.get("message_checkpoints"):
                errors.append(f"{section_id}: no message checkpoints")
            if not section.get("tp_verdict_checkpoints"):
                errors.append(f"{section_id}: no TP Verdict checkpoints")
            for checkpoint in section.get("message_checkpoints", []):
                checkpoint_id = checkpoint.get("checkpoint_id")
                if not checkpoint_id:
                    errors.append(f"{section_id}: checkpoint without id")
                    continue
                if checkpoint_id in seen:
                    errors.append(f"duplicate checkpoint id: {checkpoint_id}")
                seen.add(checkpoint_id)
            for table in section.get("specific_message_tables", []):
                if not table.get("table"):
                    errors.append(f"{section_id}: specific table without caption")
    return errors


def index_manifest_cases(manifest: dict) -> dict[tuple[str, str], dict]:
    indexed: dict[tuple[str, str], dict] = {}
    for tc_id, cases in manifest.get("cases", {}).items():
        if not isinstance(cases, list):
            continue
        for case in cases:
            if not isinstance(case, dict):
                continue
            section = case.get("section")
            if section:
                indexed[(tc_id, str(section))] = case
    return indexed


def source_is_official(case: dict) -> tuple[bool, str]:
    source = case.get("source") or {}
    source_type = source.get("type")
    if source_type not in OFFICIAL_SOURCE_TYPES:
        return False, "SOURCE_NOT_CONFORMANCE"
    if source.get("qualified") is not True:
        return False, "SOURCE_NOT_QUALIFIED"
    if not source.get("evidence_bundle"):
        return False, "SOURCE_EVIDENCE_BUNDLE_MISSING"
    return True, "QUALIFIED_CONFORMANCE_SOURCE"


def evaluate_tp_verdicts(section: dict, case: dict) -> tuple[list[dict], list[dict]]:
    supplied = {
        item.get("checkpoint_id"): item
        for item in case.get("tp_verdicts", [])
        if isinstance(item, dict) and item.get("checkpoint_id")
    }
    matches: list[dict] = []
    mismatches: list[dict] = []
    for expected in section["tp_verdict_checkpoints"]:
        checkpoint_id = expected["checkpoint_id"]
        record = supplied.get(checkpoint_id)
        expected_verdict = expected["tp_verdict_expected"]
        artifact = record.get("artifact") if record else None
        actual = record.get("actual") if record else None
        item = {
            "checkpoint_id": checkpoint_id,
            "step": expected.get("step"),
            "expected": expected_verdict,
            "actual": actual,
            "source_line": expected.get("source_line"),
            "artifact": artifact,
        }
        if actual == expected_verdict and artifact:
            matches.append(item)
        else:
            mismatches.append(item)
    return matches, mismatches


def summarize_observations(section: dict, case: dict) -> dict:
    observations = case.get("message_observations") or {}
    observed = 0
    missing = 0
    negative = 0
    for checkpoint in section["message_checkpoints"]:
        record = observations.get(checkpoint["checkpoint_id"])
        if isinstance(record, dict) and record.get("observed") is True:
            observed += 1
        elif isinstance(record, dict) and record.get("observed") is False:
            negative += 1
        else:
            missing += 1
    return {
        "total": len(section["message_checkpoints"]),
        "observed": observed,
        "negative": negative,
        "missing": missing,
    }


def evaluate_section(tc: dict, section: dict, case: dict | None) -> dict:
    if case is None:
        return {
            "tc_id": tc["tc_id"],
            "title": tc["title"],
            "section": section["section"],
            "status": "NOT_EXECUTED",
            "reason": "EVIDENCE_MISSING",
            "official_verdict": None,
            "source_qualification": None,
            "message_checkpoints": summarize_observations(section, {}),
            "tp_verdicts": {
                "total": len(section["tp_verdict_checkpoints"]),
                "matched": 0,
                "mismatched": 0,
                "missing": len(section["tp_verdict_checkpoints"]),
            },
            "details": [],
            "artifacts": [],
        }

    official, qualification = source_is_official(case)
    matches, mismatches = evaluate_tp_verdicts(section, case)
    total_verdicts = len(section["tp_verdict_checkpoints"])
    missing_verdicts = total_verdicts - len(matches) - len(mismatches)
    observations = summarize_observations(section, case)

    if official and not mismatches and not missing_verdicts:
        status = "OFFICIAL_PASS"
        official_verdict = "PASS"
        reason = "ALL_TP_VERDICTS_MATCH"
    elif official and mismatches:
        status = "OFFICIAL_FAIL"
        official_verdict = "FAIL"
        reason = "TP_VERDICT_MISMATCH"
    elif official:
        status = "INCONCLUSIVE"
        official_verdict = None
        reason = "TP_VERDICT_EVIDENCE_INCOMPLETE"
    else:
        status = "LOCAL_ONLY"
        official_verdict = None
        reason = qualification

    details: list[dict] = []
    details.extend({"result": "MATCH", **item} for item in matches)
    details.extend({"result": "MISMATCH", **item} for item in mismatches)
    artifacts = sorted(
        {
            item.get("artifact")
            for item in (case.get("tp_verdicts") or [])
            if isinstance(item, dict) and item.get("artifact")
        }
    )
    return {
        "tc_id": tc["tc_id"],
        "title": tc["title"],
        "section": section["section"],
        "status": status,
        "reason": reason,
        "official_verdict": official_verdict,
        "source_qualification": qualification,
        "message_checkpoints": observations,
        "tp_verdicts": {
            "total": total_verdicts,
            "matched": len(matches),
            "mismatched": len(mismatches),
            "missing": missing_verdicts,
        },
        "details": details,
        "artifacts": artifacts,
    }


def build_result(schema: dict, manifest: dict | None, manifest_path: Path) -> dict:
    indexed = index_manifest_cases(manifest) if manifest else {}
    results = []
    for tc in schema["cases"]:
        for section in tc["sections"]:
            case = indexed.get((tc["tc_id"], section["section"]))
            results.append(evaluate_section(tc, section, case))

    counts = {status: 0 for status in STATUS_ORDER}
    for item in results:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    official_verdicts = [
        item
        for item in results
        if item["official_verdict"] in {"PASS", "FAIL"}
    ]
    return {
        "schema_version": schema.get("schema_version"),
        "generated_at_epoch": generated_epoch(),
        "manifest_path": portable_path(manifest_path, ROOT),
        "manifest_found": manifest_path.exists(),
        "source_spec": schema.get("source_spec"),
        "source_extraction_sha256": schema.get("source_extraction_sha256"),
        "policy": schema.get("verdict_rule"),
        "summary": {
            "sections": len(results),
            "by_status": counts,
            "official_verdict_count": len(official_verdicts),
            "local_only": counts.get("LOCAL_ONLY", 0),
            "not_executed": counts.get("NOT_EXECUTED", 0),
        },
        "results": results,
    }


def write_markdown(result: dict, path: Path) -> None:
    lines = [
        "# TC-026~TC-031 证据 Schema 与 L1 适配器",
        "",
        "> 本文只登记官方步骤和可选真实证据的映射。没有真实 SS/仪表日志时，"
        "状态为 `NOT_EXECUTED`；本地或模拟证据只能标 `LOCAL_ONLY`。"
        "官方一致性 Verdict 仅在合格 SS/检测机构且 TP Verdict 行完整时生成。",
        "",
        "## 基线",
        "",
        f"- 规范：`{result['source_spec']}`",
        f"- 抽取文件 SHA-256：`{result['source_extraction_sha256']}`",
        f"- 证据清单：`{result['manifest_path']}`",
        f"- 清单存在：`{str(result['manifest_found']).lower()}`",
        f"- 章节数：`{result['summary']['sections']}`",
        f"- 官方 Verdict 数：`{result['summary']['official_verdict_count']}`",
        "",
        "## 状态汇总",
        "",
        "| 状态 | 数量 |",
        "|---|---:|",
    ]
    for status in STATUS_ORDER:
        lines.append(f"| `{status}` | {result['summary']['by_status'].get(status, 0)} |")

    lines += [
        "",
        "## 逐章节结果",
        "",
        "| TC | 官方章节 | 状态 | 原因 | 消息检查点(观测/缺失/否定) | TP Verdict(匹配/不一致/缺失) |",
        "|---|---|---|---|---:|---:|",
    ]
    for item in result["results"]:
        msg = item["message_checkpoints"]
        tp = item["tp_verdicts"]
        lines.append(
            f"| {item['tc_id']} | {item['section']} | `{item['status']}` | "
            f"`{item['reason']}` | {msg['observed']}/{msg['missing']}/{msg['negative']} | "
            f"{tp['matched']}/{tp['mismatched']}/{tp['missing']} |"
        )

    incomplete = [
        item
        for item in result["results"]
        if item["status"] in {"NOT_EXECUTED", "INCONCLUSIVE", "LOCAL_ONLY"}
    ]
    if incomplete:
        lines += [
            "",
            "## 尚不能形成官方结论的章节",
            "",
        ]
        for item in incomplete:
            lines.append(
                f"- `{item['tc_id']} {item['section']}`：`{item['status']}`，"
                f"`{item['reason']}`。"
            )

    lines += [
        "",
        "## 使用方式",
        "",
        "1. 复制 `official_tp_suites/_evidence/"
        "TC-026-031-evidence-manifest.template.json` 并填入真实证据。",
        "2. 把 `source.type` 设为 `ss_conformance_instrument` 或 "
        "`accredited_lab`，并将 `qualified` 设为 `true`。",
        "3. 每个 `tp_verdicts` 条目必须提供 `actual`，值只能是 `P` 或 `F`。",
        "4. 运行：",
        "",
        "```powershell",
        "python -X utf8 runners/run_l1_evidence_adapter_026_031.py "
        "--manifest suites/official_tp_suites/_evidence/"
        "TC-026-031-evidence-manifest.json",
        "```",
        "",
        "5. 只有 L2 合格来源且所有 TP Verdict 行匹配时，报告才会出现 "
        "`OFFICIAL_PASS`；不匹配时出现 `OFFICIAL_FAIL`。",
    ]
    write_text_lf(path, "\n".join(lines) + "\n")


def main() -> None:
    ensure_output_dirs()
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    if not args.schema.exists():
        raise SystemExit(f"missing evidence schema: {args.schema}")
    schema = load_json(args.schema)
    errors = validate_schema(schema)
    if errors:
        for error in errors:
            print(f"[SCHEMA] {error}")
        raise SystemExit(1)

    manifest = load_json(args.manifest) if args.manifest.exists() else None
    result = build_result(schema, manifest, args.manifest)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    write_text_lf(
        args.json,
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
    )
    write_markdown(result, args.report)

    counts = result["summary"]["by_status"]
    print(
        "TC026-031 L1 EVIDENCE ADAPTER: OK "
        f"sections={result['summary']['sections']} "
        f"official_verdicts={result['summary']['official_verdict_count']} "
        f"local_only={counts.get('LOCAL_ONLY', 0)} "
        f"not_executed={counts.get('NOT_EXECUTED', 0)}"
    )
    print(f"json={args.json}")
    print(f"report={args.report}")


if __name__ == "__main__":
    main()
