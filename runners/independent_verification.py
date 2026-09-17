#!/usr/bin/env python3
"""Compatibility alias for the former independent-verification entry point.

Use ``colleague_replay_verification.py`` for new instructions. This alias is
kept so earlier automation continues to work.
"""
from __future__ import annotations

from colleague_replay_verification import main


if __name__ == "__main__":
    raise SystemExit(main())
