#!/usr/bin/env python3
"""Build a machine-readable evidence schema for the official TC-026..031 steps.

The schema is derived from the already extracted 3GPP TS 36.523-1 tables. It
contains the official step anchors and TP Verdict rows, but it does not contain
or imply an execution result. Real observations must be supplied separately by
an SS/conformance instrument or a qualified test lab.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path

from l1_skeleton_026_031 import TC_META
from _paths import SUBSTEPS, SUITE_EVIDENCE, ensure_output_dirs


SOURCE = SUBSTEPS / "TC-026-031-3.2-main-behaviour.json"
OUT_DIR = SUITE_EVIDENCE
SCHEMA_OUT = OUT_DIR / "TC-026-031-evidence-schema.json"
TEMPLATE_OUT = OUT_DIR / "TC-026-031-evidence-manifest.template.json"

ARROW_RE = re.compile(r"(?P<arrow>-->|<--)\s*(?P<body>.*)$")
STEP_RE = re.compile(
    r"^(?P<step>(?:\d+[A-Za-z]?|\d+-\d+[A-Za-z]?))\s+"
    r"(?P<body>[A-Za-z].{8,})$"
)
VERDICT_RE = re.compile(r"(?:^|\s)(?:[12]\s+)?(?P<verdict>[PF])\s*$")
VERDICT_ONLY_RE = re.compile(r"^(?:[12]\s+)?[PF]$")
TABLE_STEP_START_RE = re.compile(
    r"^(?P<step>\d+(?:[A-Za-z]\d*)?(?:-\s*\d+)?)(?:\s+|$)"
)
STEP_LINE_RE = re.compile(
    r"^(?P<leading>\d+(?:[A-Za-z]\d*)?|\d+-\s*\d+[A-Za-z]?)"
    r"(?:\s+(?P<trailing>\d+))?"
    r"(?:\s+(?P<body>[A-Za-z].*))?$"
)
STEP_TOKEN_RE = re.compile(r"^(?P<leading>\d+(?:[A-Za-z]\d*)?)$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def clean_message(text: str) -> str:
    text = re.sub(r"(?:\s+-\s*)+$", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -")
    text = re.sub(r"\s+\d+$", "", text)
    return text.strip()


def direction_for(arrow: str) -> str:
    return "UE_TO_SS" if arrow == "-->" else "SS_TO_UE"


def find_step(rows: list[list[object]], arrow_index: int) -> str | None:
    """Find the nearest official step label before an arrow row.

    PDF extraction can split labels such as ``4a10`` into ``4a1`` and ``0``.
    The helper recombines those only when the adjacent tokens form a step label.
    """
    first = max(0, arrow_index - 10)
    for index in range(arrow_index - 1, first - 1, -1):
        text = str(rows[index][1]).strip()
        if not text or text.startswith(("-->", "<--", "Table ", "St Procedure")):
            continue
        if VERDICT_ONLY_RE.fullmatch(text):
            continue

        match = STEP_LINE_RE.match(text)
        if not match:
            continue
        leading = match.group("leading")
        trailing = match.group("trailing")
        if trailing:
            return f"{leading}{trailing}"
        if match.group("body"):
            return leading
        if leading.isdigit() and len(leading) == 1 and index > 0:
            previous = str(rows[index - 1][1]).strip()
            previous_match = STEP_TOKEN_RE.match(previous)
            if previous_match and previous_match.group("leading"):
                return f"{previous_match.group('leading')}{leading}"
        if any(ch.isalpha() for ch in leading):
            return leading
        if index + 1 < arrow_index:
            following = str(rows[index + 1][1]).strip()
            if following and following[0].isupper():
                return leading
    return None


def parse_message_checkpoints(tc_id: str, section: str, item: dict) -> list[dict]:
    rows = item.get("main_behaviour_steps", [])
    checkpoints: list[dict] = []
    index = 0
    while index < len(rows):
        line_no, raw = rows[index]
        text = raw.rstrip()

        arrow_match = ARROW_RE.search(text)
        if not arrow_match:
            index += 1
            continue
        current_step = find_step(rows, index)

        arrow_body = arrow_match.group("body").strip()
        expected_verdict = None
        inline_verdict = VERDICT_RE.search(arrow_body)
        if inline_verdict:
            expected_verdict = inline_verdict.group("verdict")
            arrow_body = arrow_body[: inline_verdict.start()].rstrip()
        chunk = [arrow_body]
        cursor = index + 1
        while cursor < len(rows):
            next_line = rows[cursor][1].strip()
            if not next_line:
                cursor += 1
                continue
            if next_line.startswith("- "):
                break
            if VERDICT_ONLY_RE.fullmatch(next_line):
                chunk.append(next_line)
                cursor += 1
                break
            if ARROW_RE.search(next_line) or TABLE_STEP_START_RE.match(next_line):
                break
            chunk.append(next_line)
            cursor += 1

        joined = " ".join(part for part in chunk if part)
        if expected_verdict is None:
            verdict_match = VERDICT_RE.search(joined)
            expected_verdict = verdict_match.group("verdict") if verdict_match else None
            if verdict_match:
                joined = joined[: verdict_match.start()].rstrip()
        message = clean_message(joined)
        if message and not re.fullmatch(r"[-\s]+", message):
            checkpoint = {
                "checkpoint_id": f"{tc_id}:{section}:msg-{len(checkpoints) + 1:03d}",
                "step": current_step,
                "direction": direction_for(arrow_match.group("arrow")),
                "arrow": arrow_match.group("arrow"),
                "expected_message_fragment": message,
                "tp_verdict_expected": expected_verdict,
                "source_line": line_no,
            }
            checkpoints.append(checkpoint)
        index = cursor if cursor > index else index + 1
    return checkpoints


def parse_specific_tables(item: dict) -> list[dict]:
    tables: list[dict] = []
    for table in item.get("specific_message_tables", []):
        rows = [
            {"line": line_no, "text": text}
            for line_no, text in table.get("raw_rows", [])
        ]
        tables.append(
            {
                "table": table.get("table"),
                "caption": table.get("caption"),
                "source_line": table.get("table_line"),
                "end_line": table.get("table_end_line"),
                "derivation_paths": table.get("derivation_paths", []),
                "raw_rows": rows,
            }
        )
    return tables


def build_case(tc_id: str, items: list[dict]) -> dict:
    meta = TC_META[tc_id]
    sections = []
    for item in items:
        section = item["section"]
        checkpoints = parse_message_checkpoints(tc_id, section, item)
        verdict_checkpoints = [
            checkpoint
            for checkpoint in checkpoints
            if checkpoint["tp_verdict_expected"] is not None
        ]
        sections.append(
            {
                "section": section,
                "official_behavior_table": item.get("main_behaviour_table"),
                "main_behaviour_line": item.get("main_behaviour_line"),
                "main_behaviour_end_line": item.get("main_behaviour_end_line"),
                "specific_message_line": item.get("specific_message_line"),
                "message_checkpoints": checkpoints,
                "tp_verdict_checkpoints": verdict_checkpoints,
                "specific_message_tables": parse_specific_tables(item),
                "environment_dependencies": meta["deps"],
            }
        )
    return {
        "tc_id": tc_id,
        "title": meta["title"],
        "official_spec": "ETSI TS 136 523-1 V14.3.0",
        "environment_dependencies": meta["deps"],
        "sections": sections,
    }


def build_template(schema: dict) -> dict:
    cases = {}
    for tc in schema["cases"]:
        case_entries = []
        for section in tc["sections"]:
            case_entries.append(
                {
                    "section": section["section"],
                    "source": {
                        "type": None,
                        "qualified": False,
                        "manufacturer": None,
                        "product": None,
                        "laboratory": None,
                        "evidence_bundle": None,
                    },
                    "message_observations": {
                        item["checkpoint_id"]: {
                            "observed": None,
                            "message": None,
                            "artifact": None,
                            "sha256": None,
                        }
                        for item in section["message_checkpoints"]
                    },
                    "tp_verdicts": [
                        {
                            "checkpoint_id": item["checkpoint_id"],
                            "expected": item["tp_verdict_expected"],
                            "actual": None,
                            "artifact": None,
                            "source_line": item["source_line"],
                        }
                        for item in section["tp_verdict_checkpoints"]
                    ],
                }
            )
        cases[tc["tc_id"]] = case_entries
    return {
        "schema_version": schema["schema_version"],
        "instructions": (
            "Fill only with captured evidence. Official PASS/FAIL is emitted "
            "only when source.type is a qualified SS/conformance instrument or "
            "accredited laboratory and every TP Verdict row is supplied."
        ),
        "cases": cases,
    }


def main() -> None:
    ensure_output_dirs()
    if not SOURCE.exists():
        raise SystemExit(f"missing extraction JSON: {SOURCE}")
    extracted = json.loads(SOURCE.read_text(encoding="utf-8"))
    cases = [build_case(tc_id, extracted[tc_id]) for tc_id in TC_META]
    schema = {
        "schema_version": "1.0",
        "generated_at_epoch": int(time.time()),
        "source_spec": "ETSI TS 136 523-1 V14.3.0",
        "source_extraction": str(SOURCE),
        "source_extraction_sha256": sha256(SOURCE),
        "layer_policy": {
            "L0": "official 3.2 step and 3.3 message-content anchors",
            "L1": "local or simulated evidence; never an official verdict",
            "L2": "SS/conformance instrument or accredited lab verdict only",
        },
        "verdict_rule": (
            "An official PASS/FAIL is emitted only for a qualified "
            "L2 source with an actual verdict for every TP Verdict row. "
            "Otherwise the result is NOT_EXECUTED, INCONCLUSIVE or LOCAL_ONLY."
        ),
        "cases": cases,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SCHEMA_OUT.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    TEMPLATE_OUT.write_text(
        json.dumps(build_template(schema), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    checkpoint_count = sum(
        len(section["message_checkpoints"])
        for tc in cases
        for section in tc["sections"]
    )
    verdict_count = sum(
        len(section["tp_verdict_checkpoints"])
        for tc in cases
        for section in tc["sections"]
    )
    table_count = sum(
        len(section["specific_message_tables"])
        for tc in cases
        for section in tc["sections"]
    )
    print(
        "TC026-031 EVIDENCE SCHEMA: OK "
        f"cases={len(cases)} sections="
        f"{sum(len(tc['sections']) for tc in cases)} "
        f"message_checkpoints={checkpoint_count} "
        f"tp_verdicts={verdict_count} specific_tables={table_count}"
    )
    print(f"schema={SCHEMA_OUT}")
    print(f"template={TEMPLATE_OUT}")


if __name__ == "__main__":
    main()
