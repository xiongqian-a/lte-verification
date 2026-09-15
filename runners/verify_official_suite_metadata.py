#!/usr/bin/env python3
"""Verify that every official TP suite matches official_tp_registry.json."""
import json
import re
import sys

from _paths import REGISTRY, SUITES


SUITE_DIR = SUITES
START = "<!-- OFFICIAL_TP_METADATA:START -->"
END = "<!-- OFFICIAL_TP_METADATA:END -->"
TC_RE = re.compile(r"^(TC-\d{3})-")
REQUIRED_HEADINGS = [
    "目的",
    "官方骨架",
    "前置条件",
    "验证流程",
    "TP Verdict",
    "当前本地证据",
    "受限",
]
FIELDS = {
    "officialSpec": "官方主规范",
    "officialClause": "官方章节/TP",
    "mappingConfidence": "映射等级",
    "evidenceLevel": "当前证据层级",
}


def clean(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        return value[1:-1]
    return value


def parse_metadata(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == START]
    ends = [i for i, line in enumerate(lines) if line.strip() == END]
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        return {}, ["metadata marker pair is missing or malformed"]

    metadata: dict[str, str] = {}
    for line in lines[starts[0] + 1 : ends[0]]:
        match = re.match(r"^- ([^：]+)：(.+)$", line.strip())
        if match:
            metadata[match.group(1)] = clean(match.group(2))
    return metadata, errors


def main() -> int:
    if not SUITE_DIR.exists() or not REGISTRY.exists():
        print(f"missing input: suite_dir={SUITE_DIR} registry={REGISTRY}")
        return 1

    registry_payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry = {entry["tc"]: entry for entry in registry_payload["entries"]}
    failures: list[str] = []
    checked = 0
    seen: set[str] = set()

    for path in sorted(SUITE_DIR.glob("*.md")):
        match = TC_RE.match(path.name)
        if not match:
            continue
        tc = match.group(1)
        checked += 1
        seen.add(tc)
        text = path.read_text(encoding="utf-8")
        if tc not in registry:
            failures.append(f"{tc}: missing from registry")
            continue

        metadata, parse_errors = parse_metadata(text)
        for error in parse_errors:
            failures.append(f"{tc}: {error}")
        for registry_key, label in FIELDS.items():
            expected = str(registry[tc].get(registry_key, ""))
            actual = metadata.get(label, "")
            if actual != expected:
                failures.append(
                    f"{tc}: {label} mismatch: registry={expected!r} doc={actual!r}"
                )
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                failures.append(f"{tc}: missing heading {heading!r}")

    missing_docs = sorted(set(registry) - seen)
    for tc in missing_docs:
        failures.append(f"{tc}: missing suite document")
    extra_docs = sorted(seen - set(registry))
    for tc in extra_docs:
        failures.append(f"{tc}: suite document has no registry entry")

    for failure in failures:
        print(f"FAIL\t{failure}")
    print(
        "SUMMARY "
        f"registry={len(registry)} docs={checked} failures={len(failures)}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
