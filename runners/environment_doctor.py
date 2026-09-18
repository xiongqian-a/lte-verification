#!/usr/bin/env python3
"""Report which verification environments are available on this machine.

The doctor never installs or starts infrastructure. It separates:

* repository replay/checking, which only needs Git and Python;
* fresh-DUT testbed prerequisites;
* official conformance execution, which always requires a qualified SS or lab.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_REPO_FILES = (
    "run_official_suite.py",
    "standards/official/manifest.json",
    "registry/official_tp_registry.json",
    "suites/official_tp_suites/TC-011-IMS初始注册.md",
)

TOOL_GROUPS = {
    "network_core": {
        "label": "EPC / 5GC",
        "any": (
            "open5gs-mmed",
            "open5gs-smfd",
            "open5gs-amfd",
        ),
    },
    "radio": {
        "label": "eNB / gNB",
        "any": (
            "srsenb",
            "srsran_gnb",
            "gnb",
            "nr-softmodem",
        ),
    },
    "container": {
        "label": "container runtime",
        "any": ("docker", "podman"),
    },
    "ims_sip": {
        "label": "IMS / SIP UA",
        "any": (
            "pjsua",
            "pjsua-x86_64-unknown-linux-gnu",
            "kamailio",
            "asterisk",
            "freeswitch",
        ),
    },
    "capture": {
        "label": "packet capture",
        "any": ("tshark", "tcpdump"),
    },
    "media": {
        "label": "media inspection",
        "any": ("ffmpeg", "ffprobe", "sox"),
    },
}

COMMON_INSTALL_HINTS = {
    "network_core": "Use an approved Open5GS testbed or an equivalent EPC/5GC.",
    "radio": "Use srsRAN or the target eNB/gNB testbed.",
    "container": "Install Docker Desktop/Docker Engine or Podman.",
    "ims_sip": "Use pjsua plus an approved IMS/MMTel testbed or SIP peer.",
    "capture": "Install Wireshark/tshark or tcpdump.",
    "media": "Install ffmpeg/ffprobe or sox.",
}


def find_executable(names: tuple[str, ...]) -> str | None:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def find_python() -> str | None:
    candidates = (
        sys.executable,
        shutil.which("python3"),
        shutil.which("python"),
        shutil.which("py"),
    )
    for candidate in candidates:
        if candidate:
            return candidate
    return None


def repo_files_present() -> tuple[bool, list[str]]:
    missing = [
        relative
        for relative in REQUIRED_REPO_FILES
        if not (ROOT / relative).is_file()
    ]
    return not missing, missing


def doctor() -> tuple[dict[str, object], int]:
    python = find_python()
    git = shutil.which("git")
    repo_ok, missing_repo = repo_files_present()
    tools: dict[str, dict[str, object]] = {}
    missing_fresh_dut: list[str] = []

    for key, definition in TOOL_GROUPS.items():
        names = tuple(definition["any"])
        found = find_executable(names)
        tools[key] = {
            "label": definition["label"],
            "available": bool(found),
            "path": found,
            "accepted_commands": list(names),
            "install_hint": COMMON_INSTALL_HINTS[key],
        }
        if not found:
            missing_fresh_dut.append(key)

    checker_ready = bool(python and repo_ok)
    golden_replay_ready = bool(python and git and repo_ok)
    # A complete local fresh-DUT environment is intentionally conservative:
    # core, radio, IMS/SIP, capture, and media are all required for the broad
    # suite. A narrower TC may still be runnable with a smaller subset.
    fresh_dut_ready = not missing_fresh_dut

    result: dict[str, object] = {
        "platform": platform.platform(),
        "python": python,
        "python_version": platform.python_version(),
        "git": git,
        "repository_files_present": repo_ok,
        "repository_files_missing": missing_repo,
        "golden_replay_ready": golden_replay_ready,
        "checker_only_ready": checker_ready,
        "fresh_dut_env_ready": fresh_dut_ready,
        "fresh_dut_env_missing": missing_fresh_dut,
        "official_ss_required": True,
        "official_ss_detectable": False,
        "tools": tools,
        "notes": [
            "Golden replay uses committed evidence and does not need IMS/EPC/eNB.",
            "Fresh DUT execution needs a new environment run and cannot reuse old logs.",
            "Official 36.523-1/34.229-1 verdict requires a qualified SS or lab.",
        ],
    }

    return result, 0 if checker_ready else 2


def print_text(result: dict[str, object]) -> None:
    print("ENVIRONMENT DOCTOR")
    print(f"PLATFORM: {result['platform']}")
    print(f"PYTHON: {result['python'] or 'NOT FOUND'}")
    print(f"PYTHON_VERSION: {result['python_version']}")
    print(f"GIT: {result['git'] or 'NOT FOUND'}")
    print(
        "REPOSITORY_FILES_PRESENT: "
        + ("YES" if result["repository_files_present"] else "NO")
    )
    if result["repository_files_missing"]:
        print(
            "REPOSITORY_FILES_MISSING: "
            + ", ".join(result["repository_files_missing"])
        )

    print("")
    print("TOOL GROUPS")
    for key, item in result["tools"].items():
        status = "YES" if item["available"] else "NO"
        location = item["path"] or "-"
        print(f"  {key}: {status} ({item['label']})")
        print(f"    path: {location}")
        if not item["available"]:
            print(f"    next: {item['install_hint']}")

    print("")
    print("READINESS")
    print(
        "GOLDEN_REPLAY_READY: "
        + ("YES" if result["golden_replay_ready"] else "NO")
    )
    print(
        "CHECKER_ONLY_READY: "
        + ("YES" if result["checker_only_ready"] else "NO")
    )
    print(
        "FRESH_DUT_ENV_READY: "
        + ("YES" if result["fresh_dut_env_ready"] else "NO")
    )
    print(
        "FRESH_DUT_ENV_MISSING: "
        + (", ".join(result["fresh_dut_env_missing"]) or "none")
    )
    print("OFFICIAL_SS_REQUIRED: YES")
    print("OFFICIAL_SS_DETECTED: NO (must be supplied or confirmed externally)")
    print("")
    print("BOUNDARY")
    for note in result["notes"]:
        print(f"  - {note}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    result, returncode = doctor()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
