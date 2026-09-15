#!/usr/bin/env python3
"""Helpers to extract SIP message bodies from pjsua-style logs.

pjsua logs the raw SIP message body right after a line like:

  17:51:59.093 pjsua_core.c ...TX 599 bytes Request msg REGISTER/cseq=...:
  REGISTER sip:... SIP/2.0
  ...
  --end msg--

This module pulls those message bodies out so the existing TC judgement
scripts can consume real/demo pjsua logs without manual extraction.
"""

from __future__ import annotations

import re


_SIP_METHODS = "REGISTER|INVITE|ACK|BYE|CANCEL|UPDATE|INFO|SUBSCRIBE|NOTIFY|REFER|MESSAGE|OPTIONS|PRACK|PUBLISH"
_SIP_START_RE = re.compile(
    r"^\s*(?:(?:" + _SIP_METHODS + r")\s+\S+\s+SIP/2\.0|SIP/2\.0\s+\d{3})\s*",
    re.IGNORECASE,
)
_PJ_MSG_RE = re.compile(r"(?:Request msg |Response msg )", re.IGNORECASE)


def extract_pjsua_messages(text: str) -> list[str]:
    """Return SIP message bodies found in a pjsua-style log.

    The returned items start at the SIP start line (for example
    ``REGISTER sip:... SIP/2.0`` or ``SIP/2.0 401 Unauthorized``) and contain
    the headers/body until pjsua's ``--end msg--`` marker.
    """

    lines = text.splitlines()
    messages: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not _PJ_MSG_RE.search(line):
            i += 1
            continue

        payload: list[str] = []
        j = i + 1
        while j < len(lines):
            item = lines[j]
            if item.strip() == "--end msg--":
                break
            payload.append(item.rstrip())
            j += 1

        # Sometimes pjsua prints an informational line containing "Request msg"
        # before the real TX log line; in that case payload includes another
        # pjsua-prefixed line before the SIP body.  We find the first SIP
        # start line in the raw payload.
        start_idx = None
        for idx, raw in enumerate(payload):
            if _SIP_START_RE.match(raw):
                start_idx = idx
                break
        if start_idx is not None:
            body = "\n".join(payload[start_idx:]).strip()
            if body:
                messages.append(body)

        i = j + 1

    return messages


def normalize_log(text: str) -> str:
    """Return a blank-line-separated SIP log usable by the TC scripts.

    If no pjsua-style messages are found the input is returned unchanged so
    the function is safe for already-normal SIP logs.
    """

    messages = extract_pjsua_messages(text)
    if not messages:
        return text
    return "\n\n".join(messages)


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("log", help="pjsua log file")
    args = parser.parse_args()

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        sys.stdout.write(normalize_log(fh.read()))
