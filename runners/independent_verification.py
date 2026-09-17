#!/usr/bin/env python3
"""Run an independent, reproducible repository verification pass.

This entry point is intentionally separate from run_official_suite.py. It
records the checkout, command outputs, artifact hashes, and TC-011 evidence
invariants in a report that another agent or reviewer can inspect.

It does not create an official conformance verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
TC011_EVIDENCE_DIR = ROOT / "evidence" / "local" / "tc011-l1-20260916"
TC011_SUMMARY = TC011_EVIDENCE_DIR / "tc011-l1-selftest-summary.json"

REQUIRED_FILES = [
    ROOT / "run_official_suite.py",
    ROOT / "registry" / "official_tp_registry.json",
    ROOT / "registry" / "official_tp_library.json",
    ROOT / "suites" / "official_tp_suites" / "TC-011-IMS初始注册.md",
    ROOT / "runners" / "tc011_register_flow.py",
    ROOT / "runners" / "tc011_ipsec_ss_sim.py",
    TC011_SUMMARY,
    TC011_EVIDENCE_DIR / "tc011-l1-hmac-md5-96-verdict.json",
    TC011_EVIDENCE_DIR / "tc011-l1-hmac-sha-1-96-verdict.json",
]

HASH_FILES = [
    ROOT / "registry" / "official_tp_registry.json",
    ROOT / "registry" / "official_tp_library.json",
    ROOT / "suites" / "official_tp_suites" / "TC-011-IMS初始注册.md",
    ROOT / "runners" / "tc011_register_flow.py",
    ROOT / "runners" / "tc011_ipsec_ss_sim.py",
    TC011_SUMMARY,
    TC011_EVIDENCE_DIR / "tc011-l1-hmac-md5-96-verdict.json",
    TC011_EVIDENCE_DIR / "tc011-l1-hmac-md5-96-transcript.txt",
    TC011_EVIDENCE_DIR / "tc011-l1-hmac-sha-1-96-verdict.json",
    TC011_EVIDENCE_DIR / "tc011-l1-hmac-sha-1-96-transcript.txt",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def portable_text(value: str) -> str:
    return value.replace(str(ROOT), "<repository-root>").replace("\\", "/")


def portable_command(args: list[str]) -> list[str]:
    command: list[str] = []
    for item in args:
        if Path(item).resolve() == Path(sys.executable).resolve():
            command.append("python")
            continue
        candidate = Path(item)
        try:
            resolved = candidate.resolve()
            if resolved.is_relative_to(ROOT):
                command.append(str(resolved.relative_to(ROOT)).replace("\\", "/"))
                continue
        except (OSError, ValueError):
            pass
        command.append(portable_text(item))
    return command


def run_command(
    label: str,
    args: list[str],
    expected_markers: tuple[str, ...],
    timeout_seconds: int,
) -> dict[str, Any]:
    command = [str(item) for item in args]
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=False,
            timeout=timeout_seconds,
        )
        output = ((proc.stdout or b"") + (proc.stderr or b"")).decode(
            "utf-8", errors="replace"
        )
        output = portable_text(output)
        returncode: int | None = proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        output = (stdout + stderr).decode("utf-8", errors="replace")
        output = portable_text(output)
        returncode = None
        timed_out = True

    missing_markers = [marker for marker in expected_markers if marker not in output]
    passed = returncode == 0 and not timed_out and not missing_markers
    return {
        "label": label,
        "command": portable_command(command),
        "returncode": returncode,
        "timed_out": timed_out,
        "expected_markers": list(expected_markers),
        "missing_markers": missing_markers,
        "passed": passed,
        "output": output,
    }


def git_text(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.stdout.strip() if proc.returncode == 0 else ""


def sanitize_remote(value: str) -> str:
    return re.sub(r"(https?://)[^/@]+@", r"\1***@", value)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_tc011_invariants() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append({"check": name, "passed": passed, "detail": detail})

    suite_path = ROOT / "suites" / "official_tp_suites" / "TC-011-IMS初始注册.md"
    suite_text = suite_path.read_text(encoding="utf-8")
    add(
        "suite declares LIMITED_PASS",
        "当前证据层级：`LIMITED_PASS`" in suite_text,
        "当前证据层级：`LIMITED_PASS`",
    )
    add(
        "suite declares L1_LOCAL_SIMULATED",
        "证据范围：`L1_LOCAL_SIMULATED`" in suite_text,
        "证据范围：`L1_LOCAL_SIMULATED`",
    )
    add(
        "suite keeps official verdict empty",
        "official_verdict: null" in suite_text,
        "official_verdict: null",
    )

    summary = read_json(TC011_SUMMARY)
    add("summary tc_id", summary.get("tc_id") == "TC-011", summary.get("tc_id"))
    add(
        "summary layer",
        summary.get("layer") == "L1_LOCAL_SIMULATED",
        summary.get("layer"),
    )
    add(
        "summary official_verdict is null",
        summary.get("official_verdict") is None,
        summary.get("official_verdict"),
    )
    add(
        "summary all_rounds_pass",
        summary.get("all_rounds_pass") is True,
        summary.get("all_rounds_pass"),
    )
    add(
        "summary IPsec realization is explicitly non-kernel",
        summary.get("ipsec_realization") == "port_pair_emulation_no_kernel_xfrm",
        summary.get("ipsec_realization"),
    )

    rounds = summary.get("rounds")
    if not isinstance(rounds, list):
        rounds = []
    round_by_algorithm = {
        item.get("algorithm"): item for item in rounds if isinstance(item, dict)
    }
    for algorithm in ("hmac-md5-96", "hmac-sha-1-96"):
        item = round_by_algorithm.get(algorithm, {})
        passed = (
            item.get("executed") == 8
            and item.get("passed") == 8
            and item.get("verdict") == "PASS"
        )
        add(f"summary round {algorithm}", passed, item)

    for algorithm in ("hmac-md5-96", "hmac-sha-1-96"):
        verdict_path = TC011_EVIDENCE_DIR / f"tc011-l1-{algorithm}-verdict.json"
        verdict = read_json(verdict_path)
        summary = verdict.get("summary")
        if not isinstance(summary, dict):
            summary = {}
        add(
            f"{algorithm} verdict has no official verdict",
            verdict.get("official_verdict") is None,
            verdict.get("official_verdict"),
        )
        add(
            f"{algorithm} verdict layer",
            verdict.get("layer") == "L1_LOCAL_SIMULATED",
            verdict.get("layer"),
        )
        add(
            f"{algorithm} verdict reports 8/8",
            (
                summary.get("executed") == 8
                and summary.get("passed") == 8
                and summary.get("local_l1_verdict") == "PASS"
            ),
            {
                "executed": summary.get("executed"),
                "passed": summary.get("passed"),
                "local_l1_verdict": summary.get("local_l1_verdict"),
            },
        )

    return checks


def hashes() -> dict[str, str]:
    return {
        str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
        for path in HASH_FILES
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Independent Verification Report",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Repository root: `{report['repository_root']}`",
        f"- HEAD: `{report['head']}`",
        f"- Expected commit: `{report['expected_commit'] or '(not specified)'}`",
        f"- Commit match: `{report['commit_match']}`",
        f"- Automated checks: `{report['automated_status']}`",
        "- Scope: repository reproducibility, metadata consistency, local evidence "
        "replay, and TC-011 L1 invariants.",
        "- This report is not an official 3GPP conformance verdict.",
        "",
        "## Preflight",
        "",
        f"- Branch: `{report['branch']}`",
        f"- Remote: `{report['remote']}`",
        f"- Working tree before run: `{report['status_before'] or 'clean'}`",
        f"- Working tree after run: `{report['status_after'] or 'clean'}`",
        "",
        "## Commands",
        "",
        "| Check | Return code | Result | Missing markers |",
        "|---|---:|---|---|",
    ]
    for item in report["commands"]:
        markers = ", ".join(item["missing_markers"]) or "-"
        lines.append(
            f"| `{item['label']}` | {item['returncode']} | "
            f"{'PASS' if item['passed'] else 'FAIL'} | {markers} |"
        )

    lines += [
        "",
        "## TC-011 Invariants",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    for item in report["tc011_checks"]:
        detail = json.dumps(item["detail"], ensure_ascii=False)
        lines.append(
            f"| {item['check']} | {'PASS' if item['passed'] else 'FAIL'} | `{detail}` |"
        )

    lines += [
        "",
        "## Artifact Hashes",
        "",
        "| Artifact | SHA256 before | SHA256 after |",
        "|---|---|---|",
    ]
    for path, before in report["hashes_before"].items():
        after = report["hashes_after"].get(path, "MISSING")
        lines.append(f"| `{path}` | `{before}` | `{after}` |")

    lines += [
        "",
        "## Required Independent Review",
        "",
        "1. Compare the named official clauses and line anchors with the supplied "
        "specification PDFs.",
        "2. Inspect positive and negative fixtures to confirm that the checkers "
        "are not merely matching their own generated output.",
        "3. Verify that every local result remains below `OFFICIAL_PASS`.",
        "4. Report contradictions, missing provenance, or unsupported claims; do "
        "not repair them silently.",
        "",
        "## Boundary",
        "",
        "- A passing automated report proves only that the checked repository "
        "artifacts and local replay path are internally consistent.",
        "- Official `34.229-1`, `36.523-1`, or third-party acceptance verdicts "
        "still require a qualified SS or accredited laboratory.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--expected-commit",
        help="Expected HEAD commit or unique commit prefix.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(ROOT / "outputs" / "independent-verification"),
        help="Directory for JSON and Markdown reports.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Timeout in seconds for each command.",
    )
    args = parser.parse_args()

    generated_at = utc_now()
    head = git_text("rev-parse", "HEAD")
    expected = args.expected_commit.strip() if args.expected_commit else None
    commit_match = (
        bool(head)
        and bool(expected)
        and (head == expected or head.startswith(str(expected)))
    )
    if expected is None:
        commit_match = None

    missing_files = [
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in REQUIRED_FILES
        if not path.is_file()
    ]
    hashes_before = hashes() if not missing_files else {}
    status_before = git_text("status", "--porcelain")

    checks: list[dict[str, Any]] = [
        {
            "check": f"required file {path}",
            "passed": False,
            "detail": "missing",
        }
        for path in missing_files
    ]
    if not missing_files:
        checks = check_tc011_invariants()

    commands: list[dict[str, Any]] = []
    if not missing_files:
        command_specs = [
            (
                "unified-runner",
                [sys.executable, "-X", "utf8", "run_official_suite.py"],
                ("UNIFIED RUNNER RESULT: OK",),
            ),
            (
                "tc011-register-flow-selfcheck",
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "runners/tc011_register_flow.py",
                    "--selfcheck",
                ],
                ("SELFCHECK PASS",),
            ),
            (
                "tc011-ipsec-selfcheck",
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "runners/tc011_ipsec_ss_sim.py",
                    "--selfcheck",
                ],
                ("SELFCHECK PASS",),
            ),
        ]
        commands = [
            run_command(label, command, markers, args.timeout)
            for label, command, markers in command_specs
        ]

    hashes_after = hashes() if not missing_files else {}
    status_after = git_text("status", "--porcelain")
    diff_stat = git_text("diff", "--stat")

    all_command_pass = bool(commands) and all(item["passed"] for item in commands)
    all_tc011_pass = bool(checks) and all(item["passed"] for item in checks)
    commit_ok = commit_match is not False
    automated_status = (
        "PASS" if commit_ok and not missing_files and all_command_pass and all_tc011_pass
        else "FAIL"
    )

    report = {
        "generated_at": generated_at,
        "repository_root": "<repository-root>",
        "head": head,
        "expected_commit": expected,
        "commit_match": commit_match,
        "branch": git_text("branch", "--show-current"),
        "remote": sanitize_remote(git_text("remote", "get-url", "origin")),
        "status_before": status_before,
        "status_after": status_after,
        "diff_stat": diff_stat,
        "missing_files": missing_files,
        "commands": commands,
        "tc011_checks": checks,
        "hashes_before": hashes_before,
        "hashes_after": hashes_after,
        "automated_status": automated_status,
        "official_verdict": None,
    }

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = generated_at.replace(":", "").replace("-", "").replace("+00:00", "Z")
    json_path = out_dir / f"independent-verification-{stamp}.json"
    markdown_path = out_dir / f"independent-verification-{stamp}.md"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_markdown(report), encoding="utf-8")

    print(f"INDEPENDENT VERIFICATION: {automated_status}")
    print(f"HEAD: {head}")
    print(f"COMMIT_MATCH: {commit_match}")
    for item in commands:
        print(
            f"{item['label']}: {'PASS' if item['passed'] else 'FAIL'} "
            f"rc={item['returncode']}"
        )
    print(f"TC011_INVARIANTS: {'PASS' if all_tc011_pass else 'FAIL'}")
    print(f"JSON_REPORT: {portable_text(str(json_path))}")
    print(f"MARKDOWN_REPORT: {portable_text(str(markdown_path))}")
    print("OFFICIAL_VERDICT: null")
    return 0 if automated_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
