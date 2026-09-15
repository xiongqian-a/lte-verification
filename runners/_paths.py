#!/usr/bin/env python3
"""Repository-relative paths shared by the runnable verification suite."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SUITES = ROOT / "suites" / "official_tp_suites"
SUBSTEPS = SUITES / "_substeps"
SUITE_EVIDENCE = SUITES / "_evidence"
REGISTRY_DIR = ROOT / "registry"
REGISTRY = REGISTRY_DIR / "official_tp_registry.json"
LIBRARY = REGISTRY_DIR / "official_tp_library.json"
EVIDENCE = ROOT / "evidence"
GENERATED = ROOT / "generated"
DOCS = ROOT / "docs"


def ensure_output_dirs() -> None:
    for path in (REGISTRY_DIR, GENERATED, EVIDENCE / "local", EVIDENCE / "external"):
        path.mkdir(parents=True, exist_ok=True)
