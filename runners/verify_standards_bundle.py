#!/usr/bin/env python3
"""Verify the private standards handoff bundle without modifying it."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "standards" / "official" / "manifest.json"
OFFICIAL = ROOT / "standards" / "official"
VERSION_RE = re.compile(r"(?i)-V(?P<version>\d+(?:\.\d+){0,2})")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def safe_relative_path(raw: object) -> Path | None:
    if not isinstance(raw, str) or not raw:
        return None
    posix = PurePosixPath(raw)
    if posix.is_absolute() or ".." in posix.parts:
        return None
    if "\\" in raw:
        return None
    return ROOT.joinpath(*posix.parts)


def main() -> int:
    failures: list[str] = []
    if not MANIFEST.is_file():
        print("STANDARDS BUNDLE: FAIL")
        print(f"  - missing manifest: {MANIFEST.relative_to(ROOT).as_posix()}")
        return 2

    try:
        payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("STANDARDS BUNDLE: FAIL")
        print(f"  - cannot read manifest: {exc}")
        return 2

    files = payload.get("files")
    if not isinstance(files, list) or not files:
        print("STANDARDS BUNDLE: FAIL")
        print("  - manifest contains no files")
        return 2

    declared_count = payload.get("file_count")
    if declared_count != len(files):
        failures.append(
            f"manifest file_count mismatch: declared={declared_count!r} actual={len(files)}"
        )

    manifest_paths: set[str] = set()
    total_bytes = 0
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            failures.append(f"entry {index} is not an object")
            continue
        raw_path = item.get("path")
        path = safe_relative_path(raw_path)
        if path is None:
            failures.append(f"entry {index} has unsafe path: {raw_path!r}")
            continue
        try:
            path.relative_to(OFFICIAL)
        except ValueError:
            failures.append(
                f"entry {index} is outside standards/official: {raw_path!r}"
            )
            continue
        relative = path.relative_to(ROOT).as_posix()
        manifest_paths.add(relative)
        if not path.is_file():
            failures.append(f"missing file: {relative}")
            continue
        actual_size = path.stat().st_size
        expected_size = item.get("bytes")
        if expected_size != actual_size:
            failures.append(
                f"size mismatch: {relative} expected={expected_size!r} actual={actual_size}"
            )
        expected_hash = str(item.get("sha256", "")).upper()
        actual_hash = sha256(path)
        if expected_hash != actual_hash:
            failures.append(
                f"sha256 mismatch: {relative} expected={expected_hash} actual={actual_hash}"
            )
        version_match = VERSION_RE.search(path.stem)
        expected_version = (
            version_match.group("version") if version_match else None
        )
        declared_version = item.get("version")
        if expected_version is None:
            failures.append(f"cannot derive version from filename: {relative}")
        elif declared_version != expected_version:
            failures.append(
                "version mismatch: "
                f"{relative} declared={declared_version!r} "
                f"filename={expected_version!r}"
            )
        total_bytes += actual_size

    if isinstance(declared_count, int) and declared_count == len(files):
        declared_total = payload.get("total_bytes")
        if declared_total != total_bytes:
            failures.append(
                "manifest total_bytes mismatch: "
                f"declared={declared_total!r} actual={total_bytes}"
            )

    if OFFICIAL.is_dir():
        actual_paths = {
            path.relative_to(ROOT).as_posix()
            for path in OFFICIAL.rglob("*")
            if path.is_file() and path != MANIFEST
        }
        unlisted = sorted(actual_paths - manifest_paths)
        if unlisted:
            failures.append("unlisted standard files: " + ", ".join(unlisted))

    if failures:
        print("STANDARDS BUNDLE: FAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("STANDARDS BUNDLE: PASS")
    print(f"FILES: {len(files)}")
    print(f"TOTAL BYTES: {total_bytes}")
    print(f"MANIFEST: {MANIFEST.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
