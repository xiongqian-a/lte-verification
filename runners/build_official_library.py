#!/usr/bin/env python3
"""Build a machine-readable official TP library from suite docs + registry.

This is a derived artifact generator. It does not invent new conformance IDs:
it copies what is already present in registry/official_tp_registry.json and
the per-TC suite markdown files.
"""
from __future__ import annotations

import json
import re
from _paths import GENERATED, LIBRARY, REGISTRY, SUITES, ensure_output_dirs


OUT = LIBRARY


_REF_RE = re.compile(r"(?:line|行|L)\s*(\d+(?:[-\/]\d+)?)", flags=re.IGNORECASE)
_TABLE_REF_RE = re.compile(
    r"^\|\s*[^|]+\|\s*(\d+(?:[-\/]\d+)?)\s*\|",
    flags=re.MULTILINE,
)


def normalize_ref(raw: str) -> str:
    """Normalise a line reference to the `line N` style used by the library."""
    digits = "".join(ch for ch in raw if ch.isdigit() or ch in "-/")
    return f"line {digits}"


def collect_refs(text: str) -> list[str]:
    refs = []
    matches = list(_REF_RE.finditer(text))
    matches += list(_TABLE_REF_RE.finditer(text))
    for m in matches:
        raw = m.group(1) if m.re is _TABLE_REF_RE else m.group(0)
        nums = [int(x) for x in re.findall(r"\d+", raw)]
        if any(n <= 0 for n in nums):
            continue
        # Heuristic: 34.229-1/24.229 extracts are multi-thousand-line texts.
        # Tiny numbers or filename/date artifacts like "baseline20-20260831"
        # are not usable as page/paragraph anchors and should not pollute the library.
        if max(nums) <= 5:
            continue
        if len(nums) == 2 and nums[1] > nums[0] + 10000:
            continue
        refs.append(normalize_ref(raw))
    return sorted(set(refs), key=lambda s: [int(x) for x in re.findall(r"\d+", s)])


def clean_item(line: str) -> str:
    line = line.strip()
    if line.startswith("- "):
        line = line[2:]
    line = re.sub(r"^\d+\.\s*", "", line).strip()
    return line


def section_items(lines: list[str], target: str) -> list[str]:
    out: list[str] = []
    start = None
    end = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(target):
            start = i + 1
        elif start is not None and stripped.startswith("## "):
            end = i
            break
    if start is None:
        return out
    if end is None:
        end = len(lines)
    for line in lines[start:end]:
        item = clean_item(line)
        if item and "```" not in item:
            out.append(item)
    return out


def evidence_lines_section(entry: dict, extra: list[str]) -> list[str]:
    """Convert line references in registry notes/blockers/suite docs into a list."""
    joined_extra = "\n".join(extra)
    raw = f"{entry.get('note', '')} {entry.get('blocker', '')} {joined_extra}"
    return collect_refs(raw)


def all_line_refs(lines: list[str]) -> list[str]:
    """Collect every `line N[-M]` style reference from a suite markdown file."""
    return collect_refs("\n".join(lines))


def main() -> None:
    ensure_output_dirs()
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries: list[dict] = []
    suite_files = {p.stem: p for p in SUITES.glob("TC-*.md")}
    previous = {}
    if OUT.exists():
        try:
            previous = {p["tc_id"]: p for p in json.loads(OUT.read_text(encoding="utf-8"))["entries"]}
        except Exception:
            previous = {}

    for item in reg["entries"]:
        tc = item["tc"]
        suite = next((p for name, p in suite_files.items() if name.startswith(tc + "-")), None)
        lines = suite.read_text(encoding="utf-8").splitlines() if suite else []
        official_skeleton = section_items(lines, "## 2. 官方骨架")
        # Registry may carry an explicit primary-evidence list. When present,
        # it is authoritative for the generated report; suite-document refs
        # remain the fallback for entries not yet migrated to explicit anchors.
        evidence_refs = item.get("sourceEvidenceLines") or []
        if not evidence_refs:
            evidence_refs = evidence_lines_section(item, official_skeleton)
            all_refs = all_line_refs(lines)
            if all_refs:
                evidence_refs = all_refs
        evidence_level = item.get("evidenceLevel", "RESTRICTED")
        phase = "L0"
        if evidence_level in ("RESTRICTED", "STANDARD_ALIGNED"):
            phase = "L2_PENDING"
        elif evidence_level in ("LOCAL_PASS", "SELFCHECK_PASS", "LIMITED_PASS"):
            phase = "L0"

        prev = previous.get(tc, {})
        entries.append(
            {
                "tc_id": tc,
                "name": item["name"],
                "module": item.get("module", ""),
                "official_spec": item.get("officialSpec", ""),
                "official_clause": item.get("officialClause", ""),
                "mapping_confidence": item.get("mappingConfidence", "none"),
                "source_evidence_lines": evidence_refs,
                "primary_evidence": item.get("primaryEvidence", []),
                "cross_reference_evidence": item.get("crossReferenceEvidence", []),
                "preconditions": section_items(lines, "## 3. 前置条件"),
                "steps": section_items(lines, "## 4. 验证流程"),
                "verdicts": section_items(lines, "## 5. TP Verdict 判据"),
                "official_skeleton": official_skeleton,
                "official_boundaries": item.get("officialBoundaries", []),
                "evidence_level": evidence_level,
                "local_script": item.get("localScript") or None,
                "phase": phase,
                "limitation": item.get("blocker", ""),
                # Registry is the source of truth for current status notes.
                # Keeping a previous note can silently preserve stale evidence.
                "note": item.get("note", ""),
                "evidence_dir": prev.get("evidence_dir"),
                "last_updated": prev.get("last_updated"),
            }
        )

    OUT.write_text(json.dumps({"schema": "official_tp_library", "version": reg.get("version"), "entries": entries}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"WROTE {OUT} entries={len(entries)}")


if __name__ == "__main__":
    main()
