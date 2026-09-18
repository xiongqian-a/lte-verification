#!/usr/bin/env python3
"""Verify that a fresh checkout can run without machine-specific edits.

The static checks are deliberately cheap and run as part of the unified
runner. ``--full`` additionally invokes the unified runner from an unrelated
working directory and verifies that tracked generated artifacts stay stable.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "START-HERE.md",
    "standards/README.md",
    "standards/official/manifest.json",
    "run_official_suite.py",
    "bootstrap.sh",
    "bootstrap.cmd",
    "bootstrap.ps1",
    "run.ps1",
    "runners/colleague_replay_verification.py",
    "runners/environment_doctor.py",
    "runners/verify_standards_bundle.py",
    "runners/build_standards_manifest.py",
    "registry/official_tp_registry.json",
    "registry/official_tp_library.json",
    "suites/official_tp_suites/_templates/TC-TEMPLATE.md",
    "verification-architecture.html",
]

EXECUTABLE_FILES = [
    "run_official_suite.py",
    "bootstrap.sh",
    "bootstrap.cmd",
    "bootstrap.ps1",
    "run.ps1",
    ".github/workflows/verify.yml",
]

HASH_FILES = [
    "registry/official_tp_library.json",
    "verification-architecture.html",
    "generated/official_report.md",
    "generated/84-本地证据复跑矩阵-20260914.json",
    "generated/85-验证例程全量自检状态-20260914.json",
]

# Build the strings at runtime so this checker does not flag its own source.
FORBIDDEN_PATH_MARKERS = (
    "C:" + "\\Users\\" + "co1750",
    "C:" + "/Users/" + "co1750",
    "/home/" + "co1750",
    "C:" + "\\标准例程",
    "C:" + "/标准例程",
    "C:" + "\\11\\523协议",
    "C:" + "/11/523协议",
)

BINARY_SUFFIXES = {
    ".pcap",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".zip",
    ".gz",
    ".tgz",
    ".doc",
    ".docx",
    ".pdf",
}

REPOSITORY_DIRECTORIES = (
    "evidence",
    "outputs",
    "runners",
    "suites",
    "registry",
    "generated",
    "docs",
    "tools",
)
_NONPORTABLE_GENERATED_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?:"
    + "|".join(re.escape(item) for item in REPOSITORY_DIRECTORIES)
    + r")\\{1,2}[^\\/\s\"'<>|]+(?:[\\/]|\.)"
)


def run_git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def tracked_files() -> list[str]:
    proc = run_git("ls-files", "-z")
    if proc.returncode != 0:
        return []
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in proc.stdout.split(b"\0")
        if item
    ]


def read_utf8_text(path: Path) -> str | None:
    if path.suffix.lower() in BINARY_SUFFIXES:
        return None
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\0" in raw:
        return None
    return raw.decode("utf-8", errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def static_checks() -> list[str]:
    failures: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            failures.append(f"required file is missing: {relative}")

    bootstrap = ROOT / "bootstrap.sh"
    if bootstrap.is_file():
        text = bootstrap.read_text(encoding="utf-8")
        if not text.startswith("#!/usr/bin/env sh"):
            failures.append("bootstrap.sh does not have the POSIX sh shebang")
        if "run_official_suite.py" not in text:
            failures.append("bootstrap.sh does not invoke run_official_suite.py")
        if "--colleague-replay" not in text:
            failures.append("bootstrap.sh does not expose colleague replay mode")
        if "--doctor" not in text:
            failures.append("bootstrap.sh does not expose environment doctor mode")
        if "--verify-standards" not in text:
            failures.append("bootstrap.sh does not expose standards verification mode")
        if os.name != "nt" and not os.access(bootstrap, os.X_OK):
            failures.append("bootstrap.sh is not executable on this checkout")

    windows_bootstrap = ROOT / "bootstrap.cmd"
    if windows_bootstrap.is_file():
        text = windows_bootstrap.read_text(encoding="utf-8", errors="replace")
        if "bootstrap.ps1" not in text:
            failures.append("bootstrap.cmd does not invoke bootstrap.ps1")

    powershell_bootstrap = ROOT / "bootstrap.ps1"
    if powershell_bootstrap.is_file():
        text = powershell_bootstrap.read_text(encoding="utf-8")
        if "--colleague-replay" not in text:
            failures.append("bootstrap.ps1 does not expose colleague replay mode")
        if "--doctor" not in text:
            failures.append("bootstrap.ps1 does not expose environment doctor mode")
        if "--verify-standards" not in text:
            failures.append("bootstrap.ps1 does not expose standards verification mode")

    workflow = ROOT / ".github" / "workflows" / "verify.yml"
    if workflow.is_file():
        text = workflow.read_text(encoding="utf-8")
        for marker in ("bootstrap.sh", "bootstrap.cmd"):
            if marker not in text:
                failures.append(f"CI workflow does not run {marker}")

    for relative in EXECUTABLE_FILES:
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in FORBIDDEN_PATH_MARKERS:
            if marker in text:
                failures.append(
                    f"machine-specific path in executable file {relative}: {marker}"
                )

    # Generated documents must not tell a fresh user that a local checkout is
    # required. Raw evidence under evidence/ is provenance and is intentionally
    # excluded from this documentation scan.
    for relative in tracked_files():
        normalized = relative.replace("\\", "/")
        if normalized.startswith(("evidence/", "outputs/")):
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        text = read_utf8_text(path)
        if text is None:
            continue
        for marker in FORBIDDEN_PATH_MARKERS:
            if marker in text:
                failures.append(
                    f"machine-specific path in tracked text {normalized}: {marker}"
                )
                break

    # Generated reports are committed and compared byte-for-byte in CI on
    # Windows and Linux. Catch host-specific separators after known repository
    # directories before a cross-platform run has to expose them.
    for relative in tracked_files():
        normalized = relative.replace("\\", "/")
        if not normalized.startswith("generated/"):
            continue
        path = ROOT / relative
        text = read_utf8_text(path)
        if text is None:
            continue
        match = _NONPORTABLE_GENERATED_PATH_RE.search(text)
        if match:
            failures.append(
                "non-portable generated path separator in "
                f"{normalized}: {match.group(0)}"
            )

    return failures


def full_check(timeout_seconds: int) -> list[str]:
    failures = static_checks()
    if failures:
        return failures

    status_before = run_git("status", "--porcelain")
    if status_before.returncode != 0:
        return ["git status failed; run this check inside the repository"]
    if status_before.stdout.strip():
        return ["full portability check requires a clean working tree"]

    before = {
        relative: sha256(ROOT / relative)
        for relative in HASH_FILES
        if (ROOT / relative).is_file()
    }
    missing_hashes = sorted(set(HASH_FILES) - set(before))
    if missing_hashes:
        return [f"required generated artifact is missing: {item}" for item in missing_hashes]

    command = [sys.executable, "-X", "utf8", str(ROOT / "run_official_suite.py")]
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "0")
    with tempfile.TemporaryDirectory(prefix="lte-verification-cwd-") as temp_dir:
        proc = subprocess.run(
            command,
            cwd=temp_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
            check=False,
        )
    output = proc.stdout.decode("utf-8", errors="replace")
    if proc.returncode != 0 or "UNIFIED RUNNER RESULT: OK" not in output:
        tail = "\n".join(output.splitlines()[-40:])
        return [f"runner failed from an unrelated cwd (rc={proc.returncode}):\n{tail}"]

    diff = run_git("diff", "--exit-code")
    if diff.returncode != 0:
        failures.append("runner changed tracked artifacts from an unrelated cwd")
        failures.extend(
            diff.stdout.decode("utf-8", errors="replace").splitlines()[:40]
        )

    after = {relative: sha256(ROOT / relative) for relative in HASH_FILES}
    for relative in HASH_FILES:
        if before.get(relative) != after.get(relative):
            failures.append(f"generated artifact changed after replay: {relative}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="also run the unified suite from an unrelated working directory",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="timeout in seconds for the full replay (default: 900)",
    )
    args = parser.parse_args()

    failures = full_check(args.timeout) if args.full else static_checks()
    if failures:
        print("PORTABLE INSTALL: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    mode = "FULL" if args.full else "STATIC"
    print(f"PORTABLE INSTALL: PASS ({mode})")
    print(f"REPOSITORY ROOT: {ROOT}")
    if args.full:
        print(f"UNIFIED RUNNER: PASS FROM UNRELATED CWD")
        print(f"GENERATED ARTIFACTS: STABLE ({len(HASH_FILES)} hashes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
