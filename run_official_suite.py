#!/usr/bin/env python3
"""One-command runner for the official-TP-aligned verification baseline.

The runner performs repository integrity checks, rebuilds derived registries and
reports, runs every verdict-script self-check, replays the included local
evidence, evaluates the optional TC-026..031 L2 evidence manifest, and writes
the generated reports under ``generated/``.

It does not create or imply an official conformance verdict.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RUNNERS = ROOT / "runners"
GENERATED = ROOT / "generated"


@dataclass(frozen=True)
class Step:
    script: str
    label: str
    args: tuple[str, ...] = ()


def emit(text: str) -> None:
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="replace").decode(encoding))


def run(step: Step) -> int:
    script = RUNNERS / step.script
    command = [sys.executable, "-X", "utf8", str(script), *step.args]
    print(f"[RUN ] {step.label}: {script.name}")
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=False,
    )
    output = (proc.stdout or b"") + (proc.stderr or b"")
    text = output.decode("utf-8", errors="replace")
    if proc.returncode != 0:
        emit(text[-8000:])
    elif text.strip():
        last_lines = text.strip().splitlines()[-3:]
        for line in last_lines:
            print(f"       {line}")
    return proc.returncode


def build_steps(include_evidence: bool) -> list[Step]:
    steps = [
        Step("build_official_library.py", "build machine-readable official TP library"),
        Step(
            "verify_official_suite_metadata.py",
            "verify suite metadata against the official TP registry",
        ),
        Step(
            "gen_detailed_progress.py",
            "regenerate the detailed progress table",
        ),
        Step("run_official_suite_checks.py", "suite document integrity"),
        Step(
            "run_tc_selfchecks.py",
            "local verdict-script self-checks",
            (
                "--report",
                str(GENERATED / "85-验证例程全量自检状态-20260914.md"),
                "--json",
                str(GENERATED / "85-验证例程全量自检状态-20260914.json"),
            ),
        ),
    ]
    if include_evidence:
        steps.append(
            Step(
                "run_tc_evidence.py",
                "replay included local evidence",
                (
                    "--report",
                    str(GENERATED / "84-本地证据复跑矩阵-20260914.md"),
                    "--json",
                    str(GENERATED / "84-本地证据复跑矩阵-20260914.json"),
                ),
            )
        )
    steps.extend(
        [
            Step("l1_skeleton_026_031.py", "TC-026..031 official boundary guard"),
            Step(
                "build_tc026_031_evidence_schema.py",
                "build TC-026..031 evidence schema",
            ),
            Step(
                "run_l1_evidence_adapter_026_031.py",
                "evaluate optional TC-026..031 L2 evidence manifest",
            ),
            Step(
                "verify_l1_evidence_adapter_026_031.py",
                "verify TC-026..031 evidence-adapter semantics",
            ),
        ]
    )
    steps.append(Step("report_factory.py", "generate official-style report"))
    return steps


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-evidence",
        action="store_true",
        help="skip replaying the included local evidence logs",
    )
    args = parser.parse_args()

    if not RUNNERS.exists():
        print("missing runners directory", file=sys.stderr)
        return 2
    GENERATED.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    for step in build_steps(not args.skip_evidence):
        returncode = run(step)
        if returncode != 0:
            failures.append(f"{step.label} rc={returncode}")

    if failures:
        print("UNIFIED RUNNER RESULT: FAIL")
        for failure in failures:
            print("  -", failure)
        return 2

    print("UNIFIED RUNNER RESULT: OK")
    print(f"Generated reports: {GENERATED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
