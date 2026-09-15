#!/usr/bin/env python3
"""Run every TC script's --selfcheck and optionally write a Markdown report."""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(errors="backslashreplace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(errors="backslashreplace")


TOOL_SCRIPTS = {
    "tc004_state_patch.py": "srsUE source patch helper; selfcheck is dry-run readiness only",
    "tc021_conference_join_remote.py": "remote log checker; selfcheck uses a synthetic PASS fixture",
    "tc025_rtp_capture.py": "AF_PACKET capture helper; selfcheck exercises the parser with a synthetic RTP frame",
}


def classify(name):
    return TOOL_SCRIPTS.get(name, "verdict script")


def extract_last(lines):
    for line in reversed(lines):
        if line.strip():
            return line.strip()
    return ""


def run_one(script):
    cmd = [sys.executable, str(script), "--selfcheck"]
    proc = subprocess.run(
        cmd,
        cwd=str(script.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (proc.stdout + proc.stderr).strip()
    lines = output.splitlines()
    selfcheck_pass = "SELFCHECK PASS" in output
    ok = proc.returncode == 0 and selfcheck_pass
    return {
        "name": script.name,
        "path": str(script),
        "category": classify(script.name),
        "returncode": proc.returncode,
        "status": "PASS" if ok else "FAIL",
        "last_line": extract_last(lines),
        "output": output,
    }


def render_markdown(results, generated_at):
    ok_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = len(results) - ok_count
    lines = [
        "# 验证例程全量自检状态",
        "",
        "- 生成时间：%s" % generated_at,
        "- 脚本总数：%d" % len(results),
        "- SELFCHECK PASS：%d" % ok_count,
        "- SELFCHECK FAIL：%d" % fail_count,
        "- 口径：这里的 PASS 仅表示脚本自身可执行、可用合成夹具触发预期判定路径，不代表 36.523-1 一致性、pjsua 合规或第三方入网结论。",
        "",
        "## 汇总",
        "",
        "| 脚本 | 类别 | 返回码 | 自检 | 最后一行 |",
        "|---|---|---:|---|---|",
    ]
    for r in results:
        last = r["last_line"].replace("|", "\\|")
        lines.append("| `%s` | %s | %d | %s | %s |" % (
            r["name"], r["category"], r["returncode"], r["status"], last
        ))
    lines += [
        "",
        "## 复跑命令",
        "",
        "```powershell",
        "python runners/run_tc_selfchecks.py",
        "python runners/run_tc_selfchecks.py --report generated/85-验证例程全量自检状态-20260914.md",
        "```",
        "",
        "## 详细输出",
        "",
    ]
    for r in results:
        lines += [
            "### `%s`" % r["name"],
            "",
            "```text",
            r["output"] or "(no output)",
            "```",
            "",
        ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", help="write Markdown report to this path")
    parser.add_argument("--json", help="write machine-readable JSON to this path")
    args = parser.parse_args()

    work_dir = Path(__file__).resolve().parent
    scripts = sorted(work_dir.glob("tc*.py"))
    results = [run_one(script) for script in scripts]
    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")

    for r in results:
        print("%-36s %s rc=%d  %s" % (r["name"], r["status"], r["returncode"], r["last_line"]))

    failures = [r for r in results if r["status"] != "PASS"]
    print("SUMMARY total=%d pass=%d fail=%d" % (len(results), len(results) - len(failures), len(failures)))

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_markdown(results, generated_at), encoding="utf-8")
        print("REPORT_WRITTEN %s" % report_path)

    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps({
            "generated_at": generated_at,
            "total": len(results),
            "pass": len(results) - len(failures),
            "fail": len(failures),
            "results": results,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print("JSON_WRITTEN %s" % json_path)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
