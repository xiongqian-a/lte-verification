#!/usr/bin/env python3
"""TC-011 IMS registration flow judgement engine.

Internal TC-011 is "IMS APN PDN connection / initial REGISTER 401 -> 200".
The script separates the local SIP registration checks from the official
34.229-1 8.1 / Annex C.2 requirements:

  LOCAL_BASE
  - initial REGISTER sent
  - 401 Unauthorized challenge from the network
  - WWW-Authenticate is Digest with algorithm AKAv1-MD5
  - second REGISTER carries Authorization with a non-empty response
  - same Call-ID is reused
  - network answers 200 OK
  - 200 OK carries P-Associated-URI and Service-Route

  OFFICIAL_GATES
  - Security-Client / Security-Server / Security-Verify negotiation
  - evidence of established IPsec SA state
  - SUBSCRIBE Event: reg and its matching 200 OK
  - NOTIFY Event: reg and the UE's matching 200 OK
  - both HMAC-MD5-96 and HMAC-SHA-1-96 PIXIT rounds
  - a qualified SS/instrument verdict marker

Without every official gate and a qualified SS verdict, the overall result is
LIMITED_PASS or FAIL. A SIP log must never be reported as an official
34.229-1 verdict merely because the plain 401 -> 200 sequence was observed.
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


def assert_true(
    results: list[dict],
    check: str,
    ok: bool,
    detail: str = "",
    scope: str = "LOCAL_BASE",
) -> None:
    results.append({"check": check, "ok": bool(ok), "detail": detail, "scope": scope})


def is_request(msg: str, method: str) -> bool:
    line = msg.strip().splitlines()[0] if msg.strip() else ""
    return bool(re.match(r"(?i)^" + re.escape(method) + r"\s+\S+\s+SIP/2\.0", line))


def response_for_request(messages: list[str], request_idx: int, status: int) -> bool:
    request = messages[request_idx]
    call_id = header(request, "Call-ID")
    cseq = header(request, "CSeq") or ""
    method = cseq.split()[-1].upper() if cseq else ""
    for message in messages[request_idx + 1:]:
        if not is_response_status(message, status):
            continue
        if call_id and header(message, "Call-ID") != call_id:
            continue
        response_cseq = header(message, "CSeq") or ""
        if method and not re.search(r"(?i)\b" + re.escape(method) + r"\s*$", response_cseq):
            continue
        return True
    return False


def has_secure_headers(messages: list[str]) -> dict[str, bool]:
    initial_register = next((m for m in messages if is_request_register(m)), "")
    second_register = ""
    registers = [i for i, m in enumerate(messages) if is_request_register(m)]
    unauthorized = [i for i, m in enumerate(messages) if is_response_status(m, 401)]
    if unauthorized and len(registers) >= 2:
        idx = next((i for i in registers if i > unauthorized[0]), -1)
        if idx >= 0:
            second_register = messages[idx]
    security_server = ""
    if unauthorized:
        security_server = header(messages[unauthorized[0]], "Security-Server") or ""
    return {
        "initial_security_client": bool(header(initial_register, "Security-Client")),
        "security_server": bool(security_server and "ipsec-3gpp" in security_server.lower()),
        "second_security_client": bool(header(second_register, "Security-Client")),
        "security_verify": bool(header(second_register, "Security-Verify")),
    }


def has_established_sa(text: str) -> tuple[bool, str]:
    """Recognize real XFRM/SA evidence, not the Security-* headers alone."""
    markers = re.findall(r"(?im)^\s*IPSEC_SA_ESTABLISHED\s*=\s*(?:true|1|yes)\s*$", text)
    xfrm_esp = re.search(r"(?im)^.*\bproto\s+esp\b.*$", text)
    xfrm_auth = re.search(r"(?im)^.*\b(?:hmac\((?:md5|sha1)\)|auth-trunc)\b.*$", text)
    if markers:
        return True, "explicit IPSEC_SA_ESTABLISHED marker"
    if xfrm_esp and xfrm_auth:
        return True, "XFRM ESP state with authentication algorithm"
    return False, "no XFRM/SA state evidence; Security-Client alone is not an SA"


def has_reg_event_flow(messages: list[str]) -> dict[str, bool]:
    subscribe_ok = False
    notify_ok = False
    for i, message in enumerate(messages):
        if is_request(message, "SUBSCRIBE") and (header(message, "Event") or "").lower().startswith("reg"):
            if response_for_request(messages, i, 200):
                subscribe_ok = True
        if is_request(message, "NOTIFY") and (header(message, "Event") or "").lower().startswith("reg"):
            if response_for_request(messages, i, 200):
                notify_ok = True
    return {"subscribe_200": subscribe_ok, "notify_200": notify_ok}


def has_pixit_round(text: str, algorithm: str) -> bool:
    marker = re.search(
        r"(?im)^\s*(?:PIXIT|px_IMS_IpSecAlgorithm)\s*[:=]\s*"
        + re.escape(algorithm)
        + r"\s*$",
        text,
    )
    if not marker:
        return False
    # A PIXIT label alone is not execution evidence. The selected algorithm
    # must also occur in Security negotiation or XFRM/SA evidence.
    security = re.search(
        r"(?im)^\s*Security-(?:Client|Server|Verify)\s*:.*\balg\s*=\s*"
        + re.escape(algorithm),
        text,
    )
    xfrm = re.search(
        r"(?im)^.*\b(?:hmac\("
        + re.escape(algorithm.replace("HMAC-", "").replace("-96", "").lower())
        + r"\)|alg\s*=\s*"
        + re.escape(algorithm)
        + r")\b.*$",
        text,
    )
    return bool(security or xfrm)


def check_tc011(text: str) -> tuple[str, list[dict], list[str], str]:
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

    security = has_secure_headers(messages)
    assert_true(
        results,
        "official: initial REGISTER Security-Client",
        security["initial_security_client"],
        "present" if security["initial_security_client"] else "missing",
        "OFFICIAL_GATE",
    )
    assert_true(
        results,
        "official: 401 Security-Server ipsec-3gpp",
        security["security_server"],
        "present" if security["security_server"] else "missing",
        "OFFICIAL_GATE",
    )
    assert_true(
        results,
        "official: second REGISTER Security-Client",
        security["second_security_client"],
        "present" if security["second_security_client"] else "missing",
        "OFFICIAL_GATE",
    )
    assert_true(
        results,
        "official: second REGISTER Security-Verify",
        security["security_verify"],
        "present" if security["security_verify"] else "missing",
        "OFFICIAL_GATE",
    )

    sa_ok, sa_detail = has_established_sa(text)
    assert_true(results, "official: temporary IPsec SA established", sa_ok, sa_detail, "OFFICIAL_GATE")

    reg_event = has_reg_event_flow(messages)
    assert_true(
        results,
        "official: SUBSCRIBE Event reg with 200 OK",
        reg_event["subscribe_200"],
        "present" if reg_event["subscribe_200"] else "NOT_EXECUTED",
        "OFFICIAL_GATE",
    )
    assert_true(
        results,
        "official: NOTIFY Event reg with UE 200 OK",
        reg_event["notify_200"],
        "present" if reg_event["notify_200"] else "NOT_EXECUTED",
        "OFFICIAL_GATE",
    )

    for algorithm in ("HMAC-MD5-96", "HMAC-SHA-1-96"):
        pixit_ok = has_pixit_round(text, algorithm)
        assert_true(
            results,
            "official: PIXIT round %s" % algorithm,
            pixit_ok,
            "present" if pixit_ok else "RESTRICTED: no configured execution evidence",
            "OFFICIAL_GATE",
        )

    qualified_ss = bool(re.search(
        r"(?im)^\s*(?:QUALIFIED_SYSTEM_SIMULATOR|OFFICIAL_SS)\s*[:=]\s*(?:true|yes|pass)\s*$",
        text,
    ))
    assert_true(
        results,
        "official: qualified SS/instrument verdict",
        qualified_ss,
        "present" if qualified_ss else "INCONCLUSIVE: no qualified SS verdict",
        "OFFICIAL_GATE",
    )

    base_ok = all(r["ok"] for r in results if r["scope"] == "LOCAL_BASE")
    official_ok = all(r["ok"] for r in results if r["scope"] == "OFFICIAL_GATE")
    if not base_ok:
        result = "FAIL"
    elif official_ok:
        result = "PASS"
    else:
        result = "LIMITED_PASS"
    official_verdict = "PASS" if official_ok else "INCONCLUSIVE"
    return result, results, messages, official_verdict


def print_checks(path: str, result: str, results: list[dict], messages: list[str], official_verdict: str) -> None:
    print(LINE)
    print(f"LOG: {path} messages={len(messages)} result={result}")
    for r in results:
        mark = "OK " if r["ok"] else "BAD"
        print(f"  [{mark}] {r['scope']:<13} {r['check']} :: {r['detail']}")
    print(f"OFFICIAL_VERDICT: {official_verdict}")
    if result == "LIMITED_PASS":
        print("LIMITATION: plain SIP registration evidence is incomplete for 34.229-1 8.1 / Annex C.2")
    print(f"RESULT: {result}")


def run_selfcheck_scenario(name: str, text: str, expected: str) -> bool:
    result, results, messages, official_verdict = check_tc011(text)
    print(LINE)
    print(f"SCENARIO: {name} expected={expected} actual={result}")
    for r in results:
        mark = "OK " if r["ok"] else "BAD"
        print(f"  [{mark}] {r['scope']:<13} {r['check']} :: {r['detail']}")
    print(f"OFFICIAL_VERDICT: {official_verdict}")
    if result != expected:
        print(f"  expected={expected} actual={result}")
        return False
    return True


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
        ("TC-011 base registration only", GOOD_FIXTURE, "LIMITED_PASS"),
        ("TC-011 fail missing Service-Route", fail_fixture_missing_service_route(), "FAIL"),
        ("TC-011 fail missing Authorization", fail_fixture_no_authorization(), "FAIL"),
    ]
    failures = 0
    for name, text, expected in scenarios:
        if not run_selfcheck_scenario(name, text, expected):
            failures += 1
    print(LINE)
    if failures:
        print(f"SELFCHECK FAIL: {failures} scenario(s) did not behave as expected")
        return 1
    print("SELFCHECK PASS: base SIP checks are separated from official gates")
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
    result, results, messages, official_verdict = check_tc011(text)
    print_checks(args.log, result, results, messages, official_verdict)
    return 1 if result == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
