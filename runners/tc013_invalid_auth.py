#!/usr/bin/env python3
"""TC-013 invalid AKA challenge verdict harness.

This script is an executable wrapper around the official TP anchors from
3GPP TS 34.229-1 Invalid Behaviour -> MAC Parameter Invalid / SQN out of range.

It parses SIP message sequences and verifies the 24.229 5.1.1.5 behavior:
  - MAC invalid: second REGISTER contains no auts and an empty response,
    updates Security-Client and does not create temporary SAs.
  - SQN out of range: second REGISTER contains auts, updates Security-Client,
    does not create temporary SAs, and later a valid challenge leads to a
    REGISTER over the temporary SA.

Use --log to run against a real/pjsua/demo log and --selfcheck to verify the
harness with embedded fixtures.
"""

from __future__ import annotations

import argparse
import re
import sys

try:
    from pjsua_sip_extract import normalize_log
except ImportError:  # pragma: no cover
    normalize_log = None


LINE = "=" * 78


def split_messages(text: str) -> list[str]:
    """Split a log into discrete SIP messages.

    Messages may be separated by one or more blank lines or by ===MSG===.
    """
    text = text.replace("\r\n", "\n")
    parts = re.split(r"\n\s*\n|===MSG===", text.strip())
    return [p.strip() for p in parts if p.strip()]


def parse_appearance_params(value: str) -> dict[str, str]:
    """Extract digest-style key=value parameters from an Authorization header."""
    params: dict[str, str] = {}
    if not value:
        return params
    if " " in value:
        value = value.split(" ", 1)[1]
    pattern = re.compile(r"(\w+)\s*=\s*(?:\"([^\"]*)\"|([^,\s]+))")
    for m in pattern.finditer(value):
        key = m.group(1).lower()
        val = m.group(2) if m.group(2) is not None else (m.group(3) or "")
        params[key] = val
    return params


def header(msg: str, name: str) -> str | None:
    """Return the value of a SIP header in the message, or None."""
    for line in msg.splitlines():
        if line.lower().startswith(name.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return None


def is_request_register(msg: str) -> bool:
    return bool(re.match(r"(?i)^REGISTER\s+\S+\s+SIP/2\.0", msg.strip().splitlines()[0])) if msg.strip() else False


def is_response_status(msg: str, status: int) -> bool:
    if not msg:
        return False
    return bool(re.match(r"(?i)^SIP/2\.0\s+" + str(status) + r"\b", msg.strip().splitlines()[0]))


def assert_true(results: list[dict], check: str, ok: bool, detail: str = "") -> None:
    results.append(
        {
            "check": check,
            "ok": bool(ok),
            "detail": detail,
        }
    )


def collect_register_after(messages: list[str], start_idx: int) -> int:
    for i, msg in enumerate(messages):
        if i > start_idx and is_request_register(msg):
            return i
    return -1


def run_scenario(name: str, text: str, kind: str, expected: str = "PASS") -> tuple[bool, list[dict], list[str]]:
    messages = split_messages(text)
    results: list[dict] = []

    registers = [i for i, m in enumerate(messages) if is_request_register(m)]
    unauthorized = [i for i, m in enumerate(messages) if is_response_status(m, 401)]

    assert_true(results, "initial REGISTER present", len(registers) >= 1, f"n_registers={len(registers)}")
    assert_true(results, "401 response present", len(unauthorized) >= 1, f"n_401={len(unauthorized)}")

    second_idx = -1
    if unauthorized and registers:
        second_idx = collect_register_after(messages, unauthorized[0])
    assert_true(results, "second REGISTER after first 401 present", second_idx >= 0, f"idx={second_idx}")

    if second_idx >= 0:
        second = messages[second_idx]
        auth = header(second, "Authorization")
        auth_params = parse_appearance_params(auth or "")
        assert_true(results, "second REGISTER has Authorization", bool(auth), auth or "")
        assert_true(results, "second REGISTER has Security-Client", bool(header(second, "Security-Client")),
                    header(second, "Security-Client") or "")

        if registers:
            first = messages[registers[0]]
            sec_first = header(first, "Security-Client") or ""
            sec_second = header(second, "Security-Client") or ""
            assert_true(results, "Security-Client updated", bool(sec_second) and sec_second != sec_first,
                        f"first={sec_first!r} second={sec_second!r}")

        if kind == "mac_invalid":
            assert_true(results, "no auts in second REGISTER", "auts" not in auth_params,
                        dict(auth_params))
            assert_true(results, "empty response in second REGISTER", auth_params.get("response", "MISSING") == "",
                        f"response={auth_params.get('response', 'MISSING')!r}")
        elif kind == "sqn_out_of_range":
            assert_true(results, "auts present in second REGISTER", "auts" in auth_params,
                        dict(auth_params))

        # Official TP: invalid challenge handling must not create a temporary SA.
        prefix = "\n\n".join(messages[:second_idx])
        no_temp_sa_marker = not re.search(
            r"(?i)TEMP_SA_ESTABLISHED|temporary sa established|Security-Verify",
            prefix,
        )
        assert_true(results, "no temporary SA before invalid-challenge REGISTER", no_temp_sa_marker,
                    "marker absent" if no_temp_sa_marker else "SA marker found")

    if kind == "sqn_out_of_range":
        # Recovery: after a valid 401 the UE sends a REGISTER over the temporary SA.
        sa_marker = re.search(r"(?i)TEMP_SA_ESTABLISHED|temporary sa established", text)
        assert_true(results, "recovery REGISTER sent over temporary SA", bool(sa_marker),
                    sa_marker.group(0) if sa_marker else "no SA marker")

    ok = all(r["ok"] for r in results)
    verdict = "PASS" if ok else "FAIL"
    detail = f"expected={expected} actual={verdict}"
    results.insert(
        0,
        {
            "check": "overall",
            "ok": ok == (expected == "PASS"),
            "detail": detail,
        },
    )
    return ok, results, messages


def print_report(scenario: dict) -> tuple[bool, bool]:
    ok, results, messages = run_scenario(
        scenario["name"], scenario["text"], scenario["kind"], scenario["expected"]
    )
    expected_ok = scenario["expected"] == "PASS"
    behave_as_expected = ok == expected_ok
    actual = "PASS" if ok else "FAIL"
    print(LINE)
    print(f"SCENARIO: {scenario['name']} expected={scenario['expected']} actual={actual}")
    print(f"messages={len(messages)}")
    for r in results:
        mark = "OK " if r["ok"] else "BAD"
        print(f"  [{mark}] {r['check']} :: {r['detail']}")
    return behave_as_expected, ok


MAC_INVALID_OK = """REGISTER sip:ims.example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-invalid-test-1;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>
Call-ID: tc13-mac-0001
CSeq: 1 REGISTER
Contact: <sip:alice@192.0.2.10:5060>;ob
Expires: 300
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1000; spi-s=1001; port-c=5001; port-s=5002

SIP/2.0 401 Unauthorized
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-invalid-test-1;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>;tag=ss-1
Call-ID: tc13-mac-0001
CSeq: 1 REGISTER
WWW-Authenticate: Digest realm="ims.example.com", nonce="invalid-mac-nonce-1", algorithm=AKAv1-MD5, opaque="op-1", qop="auth,auth-int", ck="ck", ik="ik"
Security-Server: ipsec-3gpp; alg=hmac-md5-96; spi-c=2000; spi-s=2001; port-c=6001; port-s=6002

REGISTER sip:ims.example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-invalid-test-2;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>
Call-ID: tc13-mac-0001
CSeq: 2 REGISTER
Contact: <sip:alice@192.0.2.10:5060>;ob
Expires: 300
Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="invalid-mac-nonce-1", uri="sip:ims.example.com", response="", algorithm=AKAv1-MD5, opaque="op-1"
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
"""

SQN_OUT_OF_RANGE_OK = """REGISTER sip:ims.example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-sqn-test-1;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>
Call-ID: tc13-sqn-0002
CSeq: 1 REGISTER
Contact: <sip:alice@192.0.2.10:5060>;ob
Expires: 300
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1100; spi-s=1101; port-c=5101; port-s=5102

SIP/2.0 401 Unauthorized
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-sqn-test-1;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>;tag=ss-1
Call-ID: tc13-sqn-0002
CSeq: 1 REGISTER
WWW-Authenticate: Digest realm="ims.example.com", nonce="sqn-out-of-range-nonce", algorithm=AKAv1-MD5, opaque="op-2", qop="auth,auth-int", ck="ck", ik="ik"
Security-Server: ipsec-3gpp; alg=hmac-md5-96; spi-c=2100; spi-s=2101; port-c=6101; port-s=6102

REGISTER sip:ims.example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-sqn-test-2;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>
Call-ID: tc13-sqn-0002
CSeq: 2 REGISTER
Contact: <sip:alice@192.0.2.10:5060>;ob
Expires: 300
Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="sqn-out-of-range-nonce", uri="sip:ims.example.com", response="", algorithm=AKAv1-MD5, auts="YXV0cy12YWx1ZQ==", opaque="op-2"
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1102; spi-s=1103; port-c=5103; port-s=5104

SIP/2.0 401 Unauthorized
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-sqn-test-2;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>;tag=ss-2
Call-ID: tc13-sqn-0002
CSeq: 2 REGISTER
WWW-Authenticate: Digest realm="ims.example.com", nonce="valid-sqn-nonce", algorithm=AKAv1-MD5, opaque="op-3", qop="auth,auth-int", ck="ck", ik="ik"
Security-Server: ipsec-3gpp; alg=hmac-md5-96; spi-c=2200; spi-s=2201; port-c=6201; port-s=6202

# TEMP_SA_ESTABLISHED

REGISTER sip:ims.example.com SIP/2.0
Via: SIP/2.0/UDP 192.0.2.10:5060;branch=z9hG4bK-sqn-test-3;rport
From: <sip:alice@ims.example.com>;tag=abc
To: <sip:alice@ims.example.com>
Call-ID: tc13-sqn-0002
CSeq: 3 REGISTER
Contact: <sip:alice@192.0.2.10:5060>;ob
Expires: 300
Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="valid-sqn-nonce", uri="sip:ims.example.com", response="res-value", algorithm=AKAv1-MD5, cnonce="cnonce-1", qop="auth", nc="00000001"
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1104; spi-s=1105; port-c=5105; port-s=5106
"""

MAC_INVALID_BAD = MAC_INVALID_OK.replace(
    """Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="invalid-mac-nonce-1", uri="sip:ims.example.com", response="", algorithm=AKAv1-MD5, opaque="op-1"
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
""",
    """Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="invalid-mac-nonce-1", uri="sip:ims.example.com", response="res-only-for-valid-challenge", algorithm=AKAv1-MD5, opaque="op-1"
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1000; spi-s=1001; port-c=5001; port-s=5002
""",
)

SQN_OUT_OF_RANGE_BAD = SQN_OUT_OF_RANGE_OK.replace(
    """Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="sqn-out-of-range-nonce", uri="sip:ims.example.com", response="", algorithm=AKAv1-MD5, auts="YXV0cy12YWx1ZQ==", opaque="op-2"
""",
    """Authorization: Digest username="alice@ims.example.com", realm="ims.example.com", nonce="sqn-out-of-range-nonce", uri="sip:ims.example.com", response="", algorithm=AKAv1-MD5, opaque="op-2"
""",
)


SCENARIOS = [
    {"name": "TC-013 MAC invalid - conformant fixture", "kind": "mac_invalid", "text": MAC_INVALID_OK, "expected": "PASS"},
    {"name": "TC-013 SQN out of range - conformant fixture", "kind": "sqn_out_of_range", "text": SQN_OUT_OF_RANGE_OK, "expected": "PASS"},
    {"name": "TC-013 MAC invalid - reject wrong behavior", "kind": "mac_invalid", "text": MAC_INVALID_BAD, "expected": "FAIL"},
    {"name": "TC-013 SQN out of range - reject missing auts", "kind": "sqn_out_of_range", "text": SQN_OUT_OF_RANGE_BAD, "expected": "FAIL"},
]


def cmd_selfcheck() -> int:
    failures = 0
    for sc in SCENARIOS:
        behave, _ = print_report(sc)
        if not behave:
            failures += 1
            print(f"SELFCHECK MISMATCH for {sc['name']}")
    print(LINE)
    if failures:
        print(f"SELFCHECK FAIL: {failures} scenario(s) did not behave as expected")
        return 1
    print("SELFCHECK PASS: harness matches expected pass/fail behavior")
    return 0


def cmd_log(path: str, kind: str) -> int:
    text = open(path, encoding="utf-8", errors="replace").read()
    if normalize_log is not None:
        text = normalize_log(text)
    ok, results, messages = run_scenario(path, text, kind, "PASS")
    print(LINE)
    print(f"LOG: {path} messages={len(messages)}")
    for r in results:
        mark = "OK " if r["ok"] else "BAD"
        print(f"  [{mark}] {r['check']} :: {r['detail']}")
    print(f"VERDICT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selfcheck", action="store_true", help="run embedded fixture self-check")
    group.add_argument("--log", metavar="FILE", help="verify a SIP log against TC-013 MAC-invalid assertions")
    parser.add_argument("--kind", choices=["mac_invalid", "sqn_out_of_range"], default="mac_invalid",
                        help="TC-013 scenario kind to apply to --log")
    args = parser.parse_args()
    if args.selfcheck:
        return cmd_selfcheck()
    return cmd_log(args.log, args.kind)


if __name__ == "__main__":
    sys.exit(main())
