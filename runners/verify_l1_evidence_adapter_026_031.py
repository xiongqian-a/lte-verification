#!/usr/bin/env python3
"""Semantic self-test for the TC-026..031 evidence adapter.

The test uses synthetic in-memory records to prove that the adapter only emits
OFFICIAL_PASS for a qualified source with complete TP Verdict and artifact
evidence. No synthetic result is written to the delivery directory.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import run_l1_evidence_adapter_026_031 as adapter


def section_cases(schema: dict, qualified: bool) -> dict:
    cases: dict[str, list[dict]] = {}
    for tc in schema["cases"]:
        entries = []
        for section in tc["sections"]:
            entries.append(
                {
                    "section": section["section"],
                    "source": {
                        "type": (
                            "ss_conformance_instrument"
                            if qualified
                            else "local_simulator"
                        ),
                        "qualified": qualified,
                        "evidence_bundle": "synthetic-log" if qualified else None,
                    },
                    "message_observations": {
                        item["checkpoint_id"]: {
                            "observed": True,
                            "message": item["expected_message_fragment"],
                            "artifact": "synthetic-log",
                        }
                        for item in section["message_checkpoints"]
                    },
                    "tp_verdicts": [
                        {
                            "checkpoint_id": item["checkpoint_id"],
                            "expected": item["tp_verdict_expected"],
                            "actual": item["tp_verdict_expected"],
                            "artifact": "synthetic-log",
                        }
                        for item in section["tp_verdict_checkpoints"]
                    ],
                }
            )
        cases[tc["tc_id"]] = entries
    return {"cases": cases}


def statuses(result: dict) -> list[str]:
    return [item["status"] for item in result["results"]]


def main() -> None:
    if not adapter.SCHEMA.exists():
        print("L1 ADAPTER SELF-TEST: FAIL missing schema")
        raise SystemExit(1)
    schema = adapter.load_json(adapter.SCHEMA)

    qualified = section_cases(schema, qualified=True)
    result = adapter.build_result(schema, qualified, Path("synthetic-qualified.json"))
    if any(status != "OFFICIAL_PASS" for status in statuses(result)):
        print("L1 ADAPTER SELF-TEST: FAIL qualified-source case")
        raise SystemExit(1)

    mismatch_manifest = copy.deepcopy(qualified)
    first_tp = mismatch_manifest["cases"]["TC-026"][0]["tp_verdicts"][0]
    first_tp["actual"] = "F" if first_tp["expected"] == "P" else "P"
    mismatch = adapter.build_result(
        schema, mismatch_manifest, Path("synthetic-mismatch.json")
    )
    if "OFFICIAL_FAIL" not in statuses(mismatch):
        print("L1 ADAPTER SELF-TEST: FAIL mismatch case")
        raise SystemExit(1)

    local = section_cases(schema, qualified=False)
    result = adapter.build_result(schema, local, Path("synthetic-local.json"))
    if any(status != "LOCAL_ONLY" for status in statuses(result)):
        print("L1 ADAPTER SELF-TEST: FAIL local-only case")
        raise SystemExit(1)

    missing = adapter.build_result(schema, None, Path("synthetic-missing.json"))
    if any(status != "NOT_EXECUTED" for status in statuses(missing)):
        print("L1 ADAPTER SELF-TEST: FAIL missing-evidence case")
        raise SystemExit(1)

    print("L1 ADAPTER SELF-TEST: OK")


if __name__ == "__main__":
    sys.exit(main())
