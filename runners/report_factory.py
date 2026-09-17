#!/usr/bin/env python3
"""Generate an official-style TP registry report (not a conformance verdict).

Output uses the same disclaimer as the rest of the suite: local PASS /
STANDARD_ALIGNED / RESTRICTED are not 36.523-1 or 34.229-1 Verdicts.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _paths import GENERATED, LIBRARY, ROOT, ensure_output_dirs
from _repro import generated_timestamp, portable_path, write_text_lf


def main() -> None:
    ensure_output_dirs()
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", default=str(LIBRARY))
    parser.add_argument("--out", default=str(GENERATED / "official_report.md"))
    args = parser.parse_args()

    data = json.loads(Path(args.library).read_text(encoding="utf-8"))
    entries = data["entries"]
    lines = [
        "# 官方 TP 映射与本地执行报告",
        "",
        f"> 生成时间：{generated_timestamp()}",
        "> 口径：本报告不产出官方一致性 Verdict。`LOCAL_PASS`/`SELFCHECK_PASS`/`STANDARD_ALIGNED`/`RESTRICTED` 均不等于一致性测试仪 P/F。",
        "",
        "| TC | 名称 | 模块 | 官方规范 | 官方章节 | 映射置信 | 当前证据 | 阶段 | 行号证据 | 主要受限 |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            "| {tc} | {name} | {module} | {spec} | {clause} | {conf} | {level} | {phase} | {refs} | {limit} |".format(
                tc=e["tc_id"],
                name=e["name"].replace("|", "\\|"),
                module=e["module"],
                spec=e["official_spec"].replace("|", "\\|"),
                clause=e["official_clause"].replace("|", "\\|"),
                conf=e["mapping_confidence"],
                level=e["evidence_level"],
                phase=e["phase"],
                refs=", ".join(e.get("source_evidence_lines", [])) or "N/A",
                limit=e.get("limitation", "").replace("|", "\\|"),
            )
        )
    lines.append("")
    lines.append("## 统计")
    lines.append("")
    lines.append(f"- 用例总数：{len(entries)}")
    with_refs = [e for e in entries if e.get("source_evidence_lines")]
    without_refs = [e for e in entries if not e.get("source_evidence_lines")]
    lines.append(f"- 带正文行号锚：{len(with_refs)}")
    lines.append(f"- 仅条款级/待补齐行号锚：{len(without_refs)}")
    lines.append("")
    lines.append("> 说明：`mappingConfidence=exact` 表示已定位到具体规范条款；是否逐行核对正文、是否覆盖 `.3.2` 子例，以“行号证据”和受限项为准。")
    lines.append(
        f"- 已生成机器可读库：`{portable_path(Path(args.library), ROOT)}`"
    )
    lines.append(f"- 官方一致性 Verdict：需要 R&S / Anritsu / Keysight / 检测机构按官方 TP 执行。")
    write_text_lf(Path(args.out), "\n".join(lines) + "\n")
    print(f"WROTE {args.out} rows={len(entries)}")


if __name__ == "__main__":
    main()
