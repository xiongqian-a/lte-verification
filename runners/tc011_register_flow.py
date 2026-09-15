#!/usr/bin/env python3
"""TC-011 IMS registration flow field-level judgement engine.

Internal TC-011 is "IMS APN PDN connection / initial REGISTER 401 -> 200".
This script checks the SIP-layer registration evidence from a real pjsua/demo
log or an already normalized SIP log:

  - initial REGISTER sent
  - 401 Unauthorized challenge from the network
  - WWW-Authenticate is Digest with algorithm AKAv1-MD5
  - second REGISTER carries Authorization with a non-empty response
  - same Call-ID is reused
  - network answers 200 OK
  - 200 OK carries P-Associated-URI and Service-Route

This is field/behaviour evidence, not a 36.523-1 conformance verdict.
"""

from __future__ import annotations

import argparse
import re
import sys

from pjsua_sip_extract import extract_pjsua_messages


LINE = "=" * 78


def parse_digest_params(value: str) -> dict[str, str]:
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


def split_messages(text: str) -> list[str]:
    """Split text into discrete SIP messages.

    Prefer pjsua extraction; fall back to blank-line / [MESSAGE] separated
    fixtures for selfcheck and already-normalized logs.
    """
    pjsua_msgs = extract_pjsua_messages(text)
    if pjsua_msgs:
        return pjsua_msgs

    text = text.replace("[MESSAGE]", "\n===MSG===")
    parts = re.split(r"\n\s*\n|===MSG===", text.strip())
    return [p.strip() for p in parts if p.strip()]


def header(msg: str, name: str) -> str | None:
    for line in msg.splitlines():
        if line.lower().startswith(name.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return None


def is_request_register(msg: str) -> bool:
    line = msg.strip().splitlines()[0] if msg.strip() else ""
    return bool(re.match(r"(?i)^REGISTER\s+\S+\s+SIP/2\.0", line))


def is_response_status(msg: str, status: int) -> bool:
    line = msg.strip().splitlines()[0] if msg.strip() else ""
    return bool(re.match(r"(?i)^SIP/2\.0\s+" + str(status) + r"\b", line))


def assert_true(results: list[dict], check: str, ok: bool, detail: str = "") -> None:
    results.append({"check": check, "ok": bool(ok), "detail": detail})


def check_tc011(text: str) -> tuple[bool, list[dict], list[str]]:
    messages = split_messages(text)
    results: list[dict] = []

    registers = [i for i, m in enumerate(messages) if is_request_register(m)]
    unauthorized = [i for i, m in enumerate(messages) if is_response_status(m, 401)]
    ok200 = [i for i, m in enumerate(messages) if is_response_status(m, 200)]

    assert_true(results, "initial REGISTER present", len(registers) >= 1, f"n_registers={len(registers)}")
    assert_true(results, "401 challenge present", len(unauthorized) >= 1, f"n_401={len(unauthorized)}")
    assert_true(results, "second REGISTER present", len(registers) >= 2, f"n_registers={len(registers)}")

    second_idx = -1
    if unauthorized and len(registers) >= 2:
        second_idx = next((i for i in registers if i > unauthorized[0]), -1)
    assert_true(results, "second REGISTER after 401 present", second_idx >= 0, f"idx={second_idx}")

    if registers:
        first = messages[registers[0]]
        first_callid = header(first, "Call-ID")
        first_contact = header(first, "Contact")
        first_expires = header(first, "Expires") or ""
        assert_true(results, "initial REGISTER has Contact", bool(first_contact), first_contact or "")
        assert_true(results, "initial REGISTER has Expires", bool(first_expires), first_expires)

    if unauthorized:
        www = header(messages[unauthorized[0]], "WWW-Authenticate") or ""
        auth_params = parse_digest_params(www)
        assert_true(results, "401 has WWW-Authenticate Digest", www.lower().startswith("digest "), www[:80])
        assert_true(results, "401 uses algorithm AKAv1-MD5", auth_params.get("algorithm", "").upper() == "AKAV1-MD5",
                    f"algorithm={auth_params.get('algorithm')!r}")
        assert_true(results, "401 challenge carries nonce", bool(auth_params.get("nonce")),
                    f"nonce_present={bool(auth_params.get('nonce'))}")

    if second_idx >= 0:
        second = messages[second_idx]
        auth = header(second, "Authorization") or ""
        auth_params = parse_digest_params(auth)
        response = auth_params.get("response", "")
        assert_true(results, "second REGISTER has Authorization", bool(auth), auth[:80])
        assert_true(results, "second REGISTER response non-empty", bool(response), f"response_len={len(response)}")

        if registers:
            first = messages[registers[0]]
            first_callid = header(first, "Call-ID")
            second_callid = header(second, "Call-ID")
            same_callid = bool(first_callid) and first_callid == second_callid
            assert_true(results, "same Call-ID reused", same_callid,
                        f"first={first_callid!r} second={second_callid!r}")

    after_second = messages[second_idx + 1:] if second_idx >= 0 else messages
    have_ok_after_second = any(is_response_status(m, 200) for m in after_second)
    assert_true(results, "200 OK after second REGISTER", have_ok_after_second,
                f"200_messages={len(ok200)}")

    ok200_msg = None
    for i in ok200:
        if second_idx < 0 or i > second_idx:
            ok200_msg = messages[i]
            break
    if ok200_msg is not None:
        assert_true(results, "200 OK has P-Associated-URI", bool(header(ok200_msg, "P-Associated-URI")),
                    header(ok200_msg, "P-Associated-URI") or "")
        assert_true(results, "200 OK has Service-Route", bool(header(ok200_msg, "Service-Route")),
                    header(ok200_msg, "Service-Route") or "")

    ok = all(r["ok"] for r in results)
    return ok, results, messages


def print_checks(path: str, ok: bool, results: list[dict], messages: list[str]) -> None:
    print(LINE)
    print(f"LOG: {path} messages={len(messages)} verdict={'PASS' if ok else 'FAIL'}")
    for r in results:
        mark = "OK " if r["ok"] else "BAD"
        print(f"  [{mark}] {r['check']} :: {r['detail']}")


GOOD_FIXTURE = """REGISTER sip:ims.mnc001.mcc001.3gppnetwork.org SIP/2.0
Via: SIP/2.0/UDP 10.45.0.1:5062;rport;branch=z9hG4bK-a1
From: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>;tag=tag-a
To: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>
Call-ID: call-id-reg-1
CSeq: 1 REGISTER
Contact: <sip:001010123456780@10.45.0.1:5062;ob>
Expires: 300

SIP/2.0 401 Unauthorized
Via: SIP/2.0/UDP 10.45.0.1:5062;rport;branch=z9hG4bK-a1
From: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>;tag=tag-a
To: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>;tag=tag-s
Call-ID: call-id-reg-1
CSeq: 1 REGISTER
WWW-Authenticate: Digest realm="ims.mnc001.mcc001.3gppnetwork.org", nonce="nonce-abc", algorithm=AKAv1-MD5, ck="ck", ik="ik", qop="auth,auth-int"

REGISTER sip:ims.mnc001.mcc001.3gppnetwork.org SIP/2.0
Via: SIP/2.0/UDP 10.45.0.1:5062;rport;branch=z9hG4bK-a2
From: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>;tag=tag-a
To: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>
Call-ID: call-id-reg-1
CSeq: 2 REGISTER
Contact: <sip:001010123456780@10.45.0.1:5062;ob>
Expires: 300
Authorization: Digest username="001010123456780", realm="ims.mnc001.mcc001.3gppnetwork.org", nonce="nonce-abc", uri="sip:ims.mnc001.mcc001.3gppnetwork.org", response="res-123", algorithm=AKAv1-MD5, cnonce="cn", qop=auth, nc=00000001

SIP/2.0 200 OK
Via: SIP/2.0/UDP 10.45.0.1:5062;rport;branch=z9hG4bK-a2
From: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>;tag=tag-a
To: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>;tag=tag-s
Call-ID: call-id-reg-1
CSeq: 2 REGISTER
P-Associated-URI: <sip:001010123456780@ims.mnc001.mcc001.3gppnetwork.org>, <tel:001010123456780>
Service-Route: <sip:orig@10.45.0.1:6060;lr>
"""


def fail_fixture_missing_service_route() -> str:
    return GOOD_FIXTURE.replace("Service-Route: <sip:orig@10.45.0.1:6060;lr>\n", "")


def fail_fixture_no_authorization() -> str:
    return GOOD_FIXTURE.replace(
        "Authorization: Digest username=\"001010123456780\", realm=\"ims.mnc001.mcc001.3gppnetwork.org\", nonce=\"nonce-abc\", uri=\"sip:ims.mnc001.mcc001.3gppnetwork.org\", response=\"res-123\", algorithm=AKAv1-MD5, cnonce=\"cn\", qop=auth, nc=00000001\n",
        "",
    )


def cmd_selfcheck() -> int:
    scenarios = [
        ("TC-011 conformant registration", GOOD_FIXTURE, True),
        ("TC-011 fail missing Service-Route", fail_fixture_missing_service_route(), False),
        ("TC-011 fail missing Authorization", fail_fixture_no_authorization(), False),
    ]
    failures = 0
    for name, text, expected in scenarios:
        ok, results, messages = check_tc011(text)
        print(LINE)
        print(f"SCENARIO: {name} expected={'PASS' if expected else 'FAIL'} actual={'PASS' if ok else 'FAIL'}")
        for r in results:
            mark = "OK " if r["ok"] else "BAD"
            print(f"  [{mark}] {r['check']} :: {r['detail']}")
        if ok != expected:
            failures += 1
    print(LINE)
    if failures:
        print(f"SELFCHECK FAIL: {failures} scenario(s) did not behave as expected")
        return 1
    print("SELFCHECK PASS: harness matches expected pass/fail behavior")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selfcheck", action="store_true", help="run embedded fixtures")
    group.add_argument("--log", metavar="FILE", help="SIP/pjsua log file")
    args = parser.parse_args()

    if args.selfcheck:
        return cmd_selfcheck()

    with open(args.log, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    ok, results, messages = check_tc011(text)
    print_checks(args.log, ok, results, messages)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
