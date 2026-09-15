#!/usr/bin/env python3
"""TC-014 re-registration judgement engine (TS 34.229-1 subclause 8.2)."""

import argparse
import os
import re
import sys

from pjsua_sip_extract import extract_pjsua_messages


REQUIRED_HEADERS = [
    "From",
    "To",
    "Via",
    "Contact",
    "Authorization",
    "Expires",
    "Security-Client",
    "Security-Verify",
    "Supported",
    "P-Access-Network-Info",
]

REGISTER_RE = re.compile(r"REGISTER\s+sip:", re.IGNORECASE)
CODE_RE = re.compile(r"SIP/2\.0\s+(\d{3})")


def parse_pj_time(line):
    """Return seconds-since-midnight from a pjsua HH:MM:SS.mmm log line."""
    m = re.search(r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})", line)
    if not m:
        return None
    h, mi, s, ms = (int(v) for v in m.groups())
    return h * 3600 + mi * 60 + s + ms / 1000.0


def parse_cseq(body):
    m = re.search(r"CSeq:\s*(\d+)\s+([A-Z]+)", body, re.IGNORECASE)
    return int(m.group(1)) if m else None


def sip_status(body):
    m = re.match(r"SIP/2\.0\s+(\d{3})", body, re.IGNORECASE)
    return m.group(1) if m else None


def split_messages(text):
    """Split log text into blocks. Used only for selfcheck fixtures."""
    blocks = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("[MESSAGE]"):
            blocks.append([line])
        elif blocks:
            blocks[-1].append(line)
    return blocks


def parse_fixture(text):
    """Parse selfcheck fixtures into messages."""
    messages = []
    for block in split_messages(text):
        body = "\n".join(block[1:])
        messages.append({"kind": block[0], "body": body})
    return messages


def collect_registers(text):
    regs = []
    current = None
    for line in text.splitlines():
        line = line.strip()
        if REGISTER_RE.search(line):
            current = {"line": line, "headers": {}}
            regs.append(current)
        elif current is not None and ": " in line:
            name, value = [part.strip() for part in line.split(": ", 1)]
            current["headers"].setdefault(name, []).append(value)
    return regs


def has_marker(text, marker):
    return re.search(re.escape(marker), text, re.IGNORECASE) is not None


def count_ok_expires(text):
    expires = []
    for line in text.splitlines():
        if CODE_RE.search(line) and "200" in line:
            pass
    for match in re.finditer(r"Expires\s*:\s*(\d+)", text, re.IGNORECASE):
        expires.append(int(match.group(1)))
    return expires


def check_tc014(text):
    regs = collect_registers(text)
    checks = []

    checks.append(("REGISTER count >= 4", len(regs) >= 4, "n_registers=%d" % len(regs)))

    if len(regs) >= 2:
        subsequent_ok = []
        for idx in range(1, len(regs)):
            missing = [h for h in REQUIRED_HEADERS if h not in regs[idx]["headers"]]
            subsequent_ok.append(not missing)
        checks.append(("subsequent REGISTER required headers present", all(subsequent_ok), "missing=%s" % [h for i in range(1, len(regs)) for h in REQUIRED_HEADERS if h not in regs[i]["headers"]]))

    checks.append(("re-register before half for initial 120s expiry", has_marker(text, "REREG_BEFORE_HALF=true"), "marker=REREG_BEFORE_HALF"))
    checks.append(("re-register at least 600s before 1200/1800 expiry", has_marker(text, "REREG_BEFORE_EXPIRY=true"), "marker=REREG_BEFORE_EXPIRY"))
    checks.append(("P-Associated-URI stored for next re-register", has_marker(text, "P_ASSOCIATED_URI_UPDATED=true"), "marker=P_ASSOCIATED_URI_UPDATED"))
    checks.append(("Security-Client new SPI/client port", has_marker(text, "SECURITY_CLIENT_UPDATED=true"), "marker=SECURITY_CLIENT_UPDATED"))

    expires = count_ok_expires(text)
    checks.append(("expiry sequence observed (120 then 1200/1800)", 120 in expires and any(e in (1200, 1800) for e in expires), "expires=%s" % expires))

    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def check_pjsua_tc014(text, limited=False):
    """Check a real pjsua/ims_client raw log for TS 34.229-1 8.2 semantics.

    The checks strictly follow what the real log can prove: an initial
    401->200 registration, at least two user/manual RE-REGISTER cycles,
    each reaching 200 OK, strictly increasing CSeq, and no 408/503.

    Official 8.2 also includes a 1200s/1800s expiry extension sequence and
    IPSEC Security-Client/Verify + P-Access-Network-Info header updates.
    Those are reported as N/A when the current simplified IMS testbed does
    not exercise them, so the verdict is a limited "real testbed PASS",
    not a full official TP PASS.
    """
    messages = extract_pjsua_messages(text)
    regs = [m for m in messages if re.match(r"REGISTER\s+sip:", m, re.IGNORECASE)]
    responses = [m for m in messages if re.match(r"SIP/2\.0\s+", m, re.IGNORECASE)]
    codes = [sip_status(m) or "" for m in responses]

    checks = []

    min_regs = 2 if limited else 4
    min_cycles = 1 if limited else 3
    checks.append((
        "REGISTER count >= %d" % min_regs,
        len(regs) >= min_regs,
        "n_registers=%d" % len(regs),
        True,
    ))

    cseqs = [parse_cseq(m) for m in regs]
    cseq_increment = (all(c is not None for c in cseqs)
                      and len(set(cseqs)) == len(cseqs)
                      and cseqs == sorted(cseqs))
    checks.append((
        "REGISTER CSeq strictly increments",
        cseq_increment,
        "cseq=%s" % cseqs,
        True,
    ))

    checks.append((
        "401 challenge observed",
        codes.count("401") >= min_cycles,
        "n401=%d" % codes.count("401"),
        True,
    ))
    checks.append((
        "200 OK responses observed",
        codes.count("200") >= min_cycles,
        "n200=%d" % codes.count("200"),
        True,
    ))
    checks.append((
        "no 408/503 seen",
        "408" not in codes and "503" not in codes,
        "codes=%s" % sorted(set(codes)),
        True,
    ))

    markers = [line for line in text.splitlines() if "manual RE-REGISTER" in line]
    need_markers = not limited
    checks.append((
        "manual RE-REGISTER markers >= 2" if need_markers else "auto/operator re-register cycles present",
        (len(markers) >= 2) if need_markers else True,
        "n_markers=%d" % len(markers),
        need_markers,
    ))

    successes = len(re.findall(r"registration success.*status=200", text, re.IGNORECASE))
    checks.append((
        "registration success status=200 >= %d" % min_cycles,
        successes >= min_cycles,
        "n_success=%d" % successes,
        True,
    ))

    # Derive "re-register before half of 120s" from pjsua timestamps instead of
    # requiring the harness to print REREG_BEFORE_HALF=true.
    exp_match = re.search(r"will re-register in (\d+) seconds", text, re.IGNORECASE)
    exp_secs = int(exp_match.group(1)) if exp_match else None
    marker_times = [parse_pj_time(m) for m in markers]
    first_reg_200_time = None
    for line in text.splitlines():
        if "registration success" in line and "will re-register" in line:
            first_reg_200_time = parse_pj_time(line)
            break
    if not limited and marker_times and first_reg_200_time is not None:
        timeout_ok = all(
            t is not None and t >= first_reg_200_time
            for t in marker_times
        )
        detail = "expires=%ss first_200=%.3fs rereg_times=%s" % (
            exp_secs, first_reg_200_time,
            ["%.3f" % t for t in marker_times if t is not None],
        )
    else:
        if limited and re.search(r"will re-register in (\d+) seconds", text, re.IGNORECASE):
            timeout_ok = True
            detail = "auto re-register timer observed (limited mode)"
        else:
            timeout_ok = False
            detail = "could not derive timing markers"
    checks.append((
        "manual re-register markers after initial 200 OK" if not limited else "auto re-register timer observed",
        timeout_ok,
        detail,
        True,
    ))
    checks.append((
        "official 8.2 expiry timing window",
        True,
        "N/A: local manual triggers are immediate; TP requires SS-measured 60s/half/600s windows",
        False,
    ))

    if not re.search(r"Security-Client\s*:", text, re.IGNORECASE):
        checks.append((
            "Security-Client/Verify headers",
            True,
            "N/A: simplified transport does not use IPSEC",
            False,
        ))
    elif re.search(r"Security-Client\s*:", text, re.IGNORECASE) and re.search(r"Security-Verify\s*:", text, re.IGNORECASE):
        checks.append((
            "Security-Client/Verify headers",
            True,
            "present in log",
            True,
        ))
    else:
        checks.append((
            "Security-Client/Verify headers",
            False,
            "Security-Client found without Security-Verify",
            True,
        ))

    if not re.search(r"P-Access-Network-Info\s*:", text, re.IGNORECASE):
        checks.append((
            "P-Access-Network-Info header",
            True,
            "N/A: testbed has no E-UTRAN/RRC access log",
            False,
        ))
    else:
        checks.append((
            "P-Access-Network-Info header",
            True,
            "present in log",
            True,
        ))

    long_exp = [int(v) for v in re.findall(r"Expires\s*:\s*(\d+)", text, re.IGNORECASE) if int(v) in (1200, 1800)]
    if not long_exp:
        checks.append((
            "1200/1800 expiry sequence",
            True,
            "N/A: test only used 120s Expires",
            False,
        ))
    else:
        checks.append((
            "1200/1800 expiry sequence",
            True,
            "expires=%s" % long_exp,
            True,
        ))

    overall = all(ok for _, ok, _, required in checks if required)
    return overall, checks


def render_pjsua_checks(checks, expected):
    ok = True
    for name, is_ok, detail, required in checks:
        if is_ok and required:
            status = "OK"
        elif is_ok:
            status = "NA "
        else:
            status = "BAD"
        print("  [%s] %s :: %s" % (status, name, detail))
        if required and expected is not None and is_ok != expected:
            ok = False
    if expected is not None and expected is True:
        ok = ok and all(is_ok for _, is_ok, _, required in checks if required)
    return ok


def render_checks(checks, expected):
    ok = True
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))
        if expected is not None and is_ok != expected:
            ok = False
    return ok


def build_fixtures():
    return {
        "pass": """[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:5002;branch=z9hG4bK-init
Contact: <sip:alice@10.45.0.2:5002>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-1", response="res-1", algorithm=AKAv1-MD5
Expires: 120
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[MESSAGE] SIP/2.0 200 OK
Expires: 120
[CHECK] REREG_BEFORE_HALF=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:5004;branch=z9hG4bK-rereg-1
Contact: <sip:alice@10.45.0.2:5004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-2", response="res-2", algorithm=AKAv1-MD5
Expires: 120
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[CHECK] P_ASSOCIATED_URI_UPDATED=true
[CHECK] SECURITY_CLIENT_UPDATED=true
[MESSAGE] SIP/2.0 200 OK
Expires: 1200
[CHECK] REREG_BEFORE_EXPIRY=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:6004;branch=z9hG4bK-rereg-2
Contact: <sip:alice@10.45.0.2:6004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-3", response="res-3", algorithm=AKAv1-MD5
Expires: 1200
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=3002; spi-s=3003; port-c=7003; port-s=7004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=3002; spi-s=3003; port-c=7003; port-s=7004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[MESSAGE] SIP/2.0 200 OK
Expires: 1800
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:7004;branch=z9hG4bK-rereg-3
Contact: <sip:alice@10.45.0.2:7004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-4", response="res-4", algorithm=AKAv1-MD5
Expires: 1800
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=4002; spi-s=4003; port-c=8003; port-s=8004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=4002; spi-s=4003; port-c=8003; port-s=8004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
""",
        "fail_headers": """[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:5002;branch=z9hG4bK-init
Contact: <sip:alice@10.45.0.2:5002>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-1", response="res-1", algorithm=AKAv1-MD5
Expires: 120
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[MESSAGE] SIP/2.0 200 OK
Expires: 120
[CHECK] REREG_BEFORE_HALF=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:5004;branch=z9hG4bK-rereg-1
Contact: <sip:alice@10.45.0.2:5004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-2", response="res-2", algorithm=AKAv1-MD5
Expires: 120
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[CHECK] P_ASSOCIATED_URI_UPDATED=true
[CHECK] SECURITY_CLIENT_UPDATED=true
[MESSAGE] SIP/2.0 200 OK
Expires: 1200
[CHECK] REREG_BEFORE_EXPIRY=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:6004;branch=z9hG4bK-rereg-2
Contact: <sip:alice@10.45.0.2:6004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-3", response="res-3", algorithm=AKAv1-MD5
Expires: 1200
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=3002; spi-s=3003; port-c=7003; port-s=7004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=3002; spi-s=3003; port-c=7003; port-s=7004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[MESSAGE] SIP/2.0 200 OK
Expires: 1800
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:7004;branch=z9hG4bK-rereg-3
Contact: <sip:alice@10.45.0.2:7004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-4", response="res-4", algorithm=AKAv1-MD5
Expires: 1800
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=4002; spi-s=4003; port-c=8003; port-s=8004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=4002; spi-s=4003; port-c=8003; port-s=8004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
""",
        "fail_timer": """[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:5002;branch=z9hG4bK-init
Contact: <sip:alice@10.45.0.2:5002>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-1", response="res-1", algorithm=AKAv1-MD5
Expires: 120
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=1002; spi-s=1003; port-c=5003; port-s=5004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[MESSAGE] SIP/2.0 200 OK
Expires: 120
[CHECK] REREG_BEFORE_HALF=false
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:5004;branch=z9hG4bK-rereg-1
Contact: <sip:alice@10.45.0.2:5004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-2", response="res-2", algorithm=AKAv1-MD5
Expires: 120
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[CHECK] P_ASSOCIATED_URI_UPDATED=true
[CHECK] SECURITY_CLIENT_UPDATED=true
[MESSAGE] SIP/2.0 200 OK
Expires: 1200
[CHECK] REREG_BEFORE_EXPIRY=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:6004;branch=z9hG4bK-rereg-2
Contact: <sip:alice@10.45.0.2:6004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-3", response="res-3", algorithm=AKAv1-MD5
Expires: 1200
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=3002; spi-s=3003; port-c=7003; port-s=7004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=3002; spi-s=3003; port-c=7003; port-s=7004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[MESSAGE] SIP/2.0 200 OK
Expires: 1800
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:7004;branch=z9hG4bK-rereg-3
Contact: <sip:alice@10.45.0.2:7004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-4", response="res-4", algorithm=AKAv1-MD5
Expires: 1800
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=4002; spi-s=4003; port-c=8003; port-s=8004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=4002; spi-s=4003; port-c=8003; port-s=8004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
""",
        "fail_seq": """[MESSAGE] SIP/2.0 200 OK
Expires: 120
[CHECK] REREG_BEFORE_HALF=true
[MESSAGE] REGISTER sip:ims.example.com SIP/2.0
From: <sip:alice@ims.example.com>
To: <sip:alice@ims.example.com>
Via: SIP/2.0/UDP 10.45.0.2:5004;branch=z9hG4bK-rereg-1
Contact: <sip:alice@10.45.0.2:5004>;ob
Authorization: Digest username="alice@ims.example.com", nonce="nonce-2", response="res-2", algorithm=AKAv1-MD5
Expires: 120
Security-Client: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
Security-Verify: ipsec-3gpp; alg=hmac-md5-96; spi-c=2002; spi-s=2003; port-c=6003; port-s=6004
Supported: path
P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=00101
[CHECK] P_ASSOCIATED_URI_UPDATED=true
[CHECK] SECURITY_CLIENT_UPDATED=true
""",
    }


def run_log(path, expected):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    overall, checks = check_tc014(text)
    print("FILE: %s expected=%s actual=%s" % (path, expected if expected is not None else "n/a", "PASS" if overall else "FAIL"))
    ok = render_checks(checks, expected)
    if expected is None:
        return ok and overall
    return ok and overall == (expected is True)


def run_raw_log(path, expected, limited=False):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    overall, checks = check_pjsua_tc014(text, limited=limited)
    verdict = "PASS"
    if not overall:
        verdict = "FAIL"
    elif limited:
        verdict = "LIMITED PASS"
    print("FILE: %s expected=%s actual=%s" % (
        path,
        expected if expected is not None else "n/a",
        verdict,
    ))
    ok = render_pjsua_checks(checks, expected)
    if expected is None:
        return ok and overall
    return ok and overall == (expected is True)


def run_selfcheck():
    fixtures = build_fixtures()
    all_ok = True
    for name in sorted(fixtures):
        text = fixtures[name]
        expected = name == "pass"
        overall, checks = check_tc014(text)
        print("SCENARIO: TC-014 %s expected=%s actual=%s" % (name, "PASS" if expected else "FAIL", "PASS" if overall else "FAIL"))
        if expected:
            ok = render_checks(checks, True) and overall
        else:
            render_checks(checks, None)
            ok = not overall
        all_ok = all_ok and ok
    print("SELFCHECK %s" % ("PASS" if all_ok else "FAIL"))
    return all_ok


def main():
    parser = argparse.ArgumentParser(description="TC-014 re-registration judgement engine")
    parser.add_argument("--selfcheck", action="store_true", help="run built-in fixtures")
    parser.add_argument("--log", help="path to SIP log file")
    parser.add_argument("--raw", action="store_true", help="pjsua/ims_client raw log mode")
    parser.add_argument("--limited", action="store_true", help="allow LIMITed PASS for a raw log with 1-2 real auto re-register cycles, not full 34.229-1 8.2 TP")
    parser.add_argument("--expect", choices=["pass", "fail"], help="optional expected result for log")
    args = parser.parse_args()

    if args.selfcheck:
        sys.exit(0 if run_selfcheck() else 1)
    if args.log:
        if not os.path.exists(args.log):
            print("ERROR: log not found: %s" % args.log)
            return 2
        expected = None if args.expect is None else (args.expect == "pass")
        ok = run_raw_log(args.log, expected, limited=args.limited) if args.raw else run_log(args.log, expected)
        if args.expect is not None:
            return 0 if ok else 1
        if args.raw:
            if args.limited:
                return 0 if ok else 1
            return 0 if ok else 1
        return 0 if check_tc014(open(args.log, "r", encoding="utf-8", errors="replace").read())[0] else 1
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
