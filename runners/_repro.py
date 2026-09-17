#!/usr/bin/env python3
"""Small helpers for deterministic, repository-relative generated artifacts.

The normal runner is a local verification runner, not a release pipeline.
Generated reports still live in git, so their contents must not depend on the
machine name, clock, or absolute checkout path. Set ``SOURCE_DATE_EPOCH`` to
override the deterministic timestamp in a reproducible build.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_EPOCH = 0
DEFAULT_TIMESTAMP = "1970-01-01T00:00:00Z"
_REPO_PATH_DIRS = (
    "evidence",
    "outputs",
    "runners",
    "suites",
    "registry",
    "generated",
    "docs",
    "tools",
)
_REPO_RELATIVE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?P<path>(?:"
    + "|".join(re.escape(item) for item in _REPO_PATH_DIRS)
    + r")(?:[\\/]{1,2}[^\\/\s\"'<>|]+)+)"
)


def generated_epoch() -> int:
    raw = os.environ.get("SOURCE_DATE_EPOCH")
    if raw is None:
        return DEFAULT_EPOCH
    try:
        return max(0, int(raw))
    except ValueError:
        return DEFAULT_EPOCH


def generated_timestamp() -> str:
    epoch = generated_epoch()
    if epoch == DEFAULT_EPOCH and "SOURCE_DATE_EPOCH" not in os.environ:
        return DEFAULT_TIMESTAMP
    return datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")


def write_text_lf(path: Path, text: str) -> None:
    """Write UTF-8 text with stable LF newlines on every platform."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def portable_path(path: Path, root: Path) -> str:
    """Return a slash-separated path relative to the checkout when possible."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def portable_text(value: str, root: Path) -> str:
    """Remove machine-specific checkout roots from captured command output."""
    text = value or ""
    resolved_root = str(root.resolve())
    roots = {
        resolved_root,
        resolved_root.replace("\\", "/"),
        resolved_root.replace("\\", "\\\\"),
        resolved_root.replace("\\", "/").replace("/", "//"),
    }
    for item in sorted(roots, key=len, reverse=True):
        text = text.replace(item, "<repo>")
    # Some Windows child processes emit the checkout path using the active
    # console code page, which can survive subprocess UTF-8 decoding as
    # replacement characters. Normalize any absolute prefix before a known
    # repository directory, while preserving the path beneath the checkout.
    text = re.sub(
        r"(?i)(?:[A-Z]:[\\/])[^\r\n]*?[\\/](?="
        r"(?:evidence|outputs|runners|suites|registry|generated|docs|tools)"
        r"[\\/])",
        lambda _: "<repo>/",
        text,
    )
    text = re.sub(r"<repo>[\\/]+", "<repo>/", text)
    # Repository-relative paths emitted by child processes can still use the
    # host separator (and JSON may escape it as a double backslash). Normalize
    # only known repository directories and their path suffixes so protocol
    # text and arbitrary command output are left untouched.
    text = _REPO_RELATIVE_PATH_RE.sub(
        lambda match: match.group("path").replace("\\", "/").replace("//", "/"),
        text,
    )
    return text


def normalize_tc011_ports(output: str) -> str:
    """Replace runtime UDP ports with stable semantic placeholders.

    TC-011 intentionally binds real UDP sockets on dynamic ports. The verdict
    still evaluates those real ports; only the report-facing stdout is rendered
    with stable names so generated evidence does not change between runs.
    """
    current_step = None
    normalized = []
    for line in (output or "").splitlines():
        step_match = re.search(r"C\.2 step\s+(\d+)", line)
        if step_match:
            current_step = int(step_match.group(1))

        if "selftest/reference UE:" in line:
            line = re.sub(r"\bclient_port=\d{1,5}\b",
                          "client_port=<PORT_UE_PLAIN>", line)
            line = re.sub(r"\bsa_port=\d{1,5}\b",
                          "sa_port=<PORT_UE_SA_C>", line)

        lowered = line.lower()
        if "security-client" in lowered:
            port_c = "<PORT_UE_SA_C>"
            port_s = "<PORT_UE_SA_S>"
            uri_port = port_c
        elif "security-server" in lowered or "security-verify" in lowered:
            port_c = "<PORT_SS_C>"
            port_s = "<PORT_SS_S>"
            uri_port = port_c
        elif "service-route" in lowered:
            port_c = "<PORT_UE_SA_C>"
            port_s = "<PORT_UE_SA_S>"
            uri_port = "<PORT_SS_C>"
        elif "notify 200 ok keeps the top via" in lowered:
            port_c = "<PORT_UE_SA_C>"
            port_s = "<PORT_UE_SA_S>"
            uri_port = "<PORT_SS_C>"
        elif current_step == 4:
            port_c = "<PORT_UE_PLAIN>"
            port_s = "<PORT_UE_PLAIN>"
            uri_port = "<PORT_UE_PLAIN>"
        else:
            port_c = "<PORT_UE_SA_C>"
            port_s = "<PORT_UE_SA_S>"
            uri_port = "<PORT_UE_SA_C>"

        line = re.sub(r"\bcontact_port=\d{1,5}\b",
                      "contact_port=" + uri_port, line)
        line = re.sub(r"\bsource_port=\d{1,5}\b",
                      "source_port=" + uri_port, line)
        line = re.sub(r"\bsrc_port=\d{1,5}\b",
                      "src_port=" + uri_port, line)
        line = re.sub(r"\bannounced_port-c=\d{1,5}\b",
                      "announced_port-c=" + port_c, line)
        line = re.sub(r"\bdst_port=\d{1,5}\b",
                      "dst_port=" + uri_port, line)
        line = re.sub(r"\bexpected=\d{1,5}\b",
                      "expected=" + uri_port, line)
        line = re.sub(r"\bport-c=\d{1,5}\b",
                      "port-c=" + port_c, line)
        line = re.sub(r"\bport-s=\d{1,5}\b",
                      "port-s=" + port_s, line)
        line = re.sub(r'("port-c"\s*:\s*")\d{1,5}',
                      r"\g<1>" + port_c, line)
        line = re.sub(r'("port-s"\s*:\s*")\d{1,5}',
                      r"\g<1>" + port_s, line)
        line = re.sub(r"(?<=127\.0\.0\.1:)\d{1,5}",
                      uri_port, line)
        normalized.append(line)
    return "\n".join(normalized)
