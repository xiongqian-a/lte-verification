#!/usr/bin/env python3
"""Build the SHA256 manifest for the private standards handoff bundle.

This script only enumerates files under ``standards/official``. It does not
extract, rename, convert, or redistribute the source documents.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STANDARDS = ROOT / "standards"
OFFICIAL = STANDARDS / "official"
MANIFEST = OFFICIAL / "manifest.json"

SPEC_BY_DIR = {
    "22.101": "3GPP TS 22.101",
    "23.003": "3GPP TS 23.003",
    "23.060": "3GPP TS 23.060",
    "23.401": "3GPP TS 23.401",
    "24.008": "3GPP TS 24.008",
    "24.147": "3GPP TS 24.147",
    "24.173": "3GPP TS 24.173",
    "24.229": "3GPP TS 24.229",
    "24.237": "3GPP TS 24.237",
    "24.301": "3GPP TS 24.301",
    "24.341": "3GPP TS 24.341",
    "24.605": "3GPP TS 24.605",
    "24.610": "3GPP TS 24.610",
    "24.628": "3GPP TS 24.628",
    "24.629": "3GPP TS 24.629",
    "26.093": "3GPP TS 26.093",
    "26.114": "3GPP TS 26.114",
    "26.193": "3GPP TS 26.193",
    "26.267": "3GPP TS 26.267",
    "26.450": "3GPP TS 26.450",
    "26.451": "3GPP TS 26.451",
    "29.228": "3GPP TS 29.228",
    "33.102": "3GPP TS 33.102",
    "33.203": "3GPP TS 33.203",
    "33.401": "3GPP TS 33.401",
    "34.108": "3GPP TS 34.108",
    "34.229-1": "3GPP TS 34.229-1",
    "34.229-2": "3GPP TS 34.229-2",
    "36.306": "3GPP TS 36.306",
    "36.323": "3GPP TS 36.323",
    "36.331": "3GPP TS 36.331",
    "36.508": "3GPP TS 36.508",
    "36.509": "3GPP TS 36.509",
    "36.523-1": "3GPP TS 36.523-1",
    "36.523-2": "3GPP TS 36.523-2",
    "44.018": "3GPP TS 44.018",
    "51.010-1": "3GPP TS 51.010-1",
    "RFC3261": "IETF RFC 3261",
    "RFC3515": "IETF RFC 3515",
}

VERSION_RE = re.compile(
    r"(?i)-V(?P<version>\d+(?:\.\d+){0,2})"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def version_from_name(path: Path) -> str:
    match = VERSION_RE.search(path.stem)
    return match.group("version") if match else ""


def main() -> int:
    if not OFFICIAL.is_dir():
        raise SystemExit(f"missing standards directory: {OFFICIAL}")

    files: list[dict[str, object]] = []
    for path in sorted(OFFICIAL.rglob("*")):
        if not path.is_file() or path == MANIFEST:
            continue
        relative = path.relative_to(ROOT).as_posix()
        spec_dir = path.parent.name
        files.append(
            {
                "spec": SPEC_BY_DIR.get(spec_dir, spec_dir),
                "spec_dir": spec_dir,
                "version": version_from_name(path),
                "format": path.suffix.lower().lstrip("."),
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    payload = {
        "schema_version": 1,
        "bundle": "current-suite-official-sources",
        "repository_visibility": "private-internal",
        "redistribution_note": (
            "Internal handoff only. Do not publish or redistribute the source "
            "documents outside the authorized organization."
        ),
        "path_base": "repository-root",
        "file_count": len(files),
        "total_bytes": sum(int(item["bytes"]) for item in files),
        "files": files,
    }
    MANIFEST.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"STANDARDS MANIFEST: WROTE {MANIFEST.relative_to(ROOT).as_posix()}")
    print(f"FILES: {len(files)}")
    print(f"TOTAL BYTES: {payload['total_bytes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
