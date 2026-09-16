#!/usr/bin/env python3
"""TC-011 IMS IPsec registration harness (SS side + reference UE emulator).

Why this exists
---------------
TC-011 maps to 3GPP TS 34.229-1 clause 8.1, which executes the generic
procedure in Annex C.2.  The original local pjsua evidence only covered C.2
Steps 4-7 at field level.  Before this harness, Steps 6-11 (temporary IPsec SA,
Security-Client/Security-Verify, SUBSCRIBE/NOTIFY registration state) had not
been covered.  The official TP also requires two PIXIT rounds
(px_IMS_IpSecAlgorithm = HMAC-MD5-96 and HMAC-SHA-1-96).

This script implements the SS/P-CSCF side of Annex C.2 as a real UDP endpoint
that judges a UE message by message, plus a reference UE emulator used only to
self-test the harness.  It is an L1 local instrument:

  * real SIP messages over a real UDP socket,
  * step-level PASS/FAIL for C.2 Steps 4-11,
  * both PIXIT algorithms,
  * but NO kernel xfrm SA (needs CAP_NET_ADMIN) and NO official SS verdict.

The IPsec boundary is emulated at the port/SPI level: the UE opens a second
socket on the port it announced in Security-Client port-c, and the SS requires
the protected REGISTER/SUBSCRIBE to arrive from exactly that port.  That is the
same header and port discipline the official procedure checks; it is not proof
that ESP/ah was applied, and the verdict JSON says so explicitly.

Usage
-----
  # harness self-test: both PIXIT algorithms, C.2 Steps 4-11, evidence bundle
  python3 tc011_ipsec_ss_sim.py --selftest --out-dir /tmp/tc011-l1

  # point the SS side at a real DUT (passive): waits for the first REGISTER
  python3 tc011_ipsec_ss_sim.py --dut --bind 10.45.0.1 --port 5060 \
      --algorithm hmac-md5-96 --out-dir /tmp/tc011-dut
"""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import sys
import threading
import time
from xml.sax.saxutils import escape as xml_escape


LINE = "=" * 78
TIMEOUT_S = 12.0

HOME_DOMAIN = "ims.mnc001.mcc001.3gppnetwork.org"
IMPI = "001010123456780"
IMPU = f"sip:{IMPI}@{HOME_DOMAIN}"
REALM = HOME_DOMAIN

# TS 34.229-1 Annex A.1.1 / A.1.2 / A.1.3 / A.1.4 / A.1.6 defaults, reduced to
# the fields this harness actually judges.
ALGORITHMS = {
    "hmac-md5-96": "hmac-md5-96",
    "hmac-sha-1-96": "hmac-sha-1-96",
}

OTHER_ALGORITHM = {
    "hmac-md5-96": "hmac-sha-1-96",
    "hmac-sha-1-96": "hmac-md5-96",
}

SEC_AGREE = "sec-agree"
P_ACCESS_NETWORK_INFO = "3GPP-E-UTRAN-FDD; utran-cell-id-3gpp=001010000000001"
SERVICE_ROUTE_VALUE = (
    "<sip:orig@{ss_ip}:{ss_port_c};lr>, <sip:scscf.3gpp.org;lr>"
)
SUBSCRIBE_CONTACT_USER = "001010123456780"

OFFICIAL_STEPS = [
    (4, "UE -> SS", "initial unprotected REGISTER"),
    (5, "SS -> UE", "401 Unauthorized with AKAv1-MD5 challenge + Security-Server"),
    (6, "UE -> SS", "second REGISTER over temporary SA (+Security-Client/Verify)"),
    (7, "SS -> UE", "200 OK over the same temporary SA"),
    (8, "UE -> SS", "SUBSCRIBE reg event package over new SA"),
    (9, "SS -> UE", "200 OK for SUBSCRIBE"),
    (10, "SS -> UE", "NOTIFY with full registration state XML"),
    (11, "UE -> SS", "200 OK for NOTIFY"),
]


class Transcript:
    """Ordered record of every datagram plus the check outcomes."""

    def __init__(self, algorithm: str) -> None:
        self.algorithm = algorithm
        self.entries: list[dict] = []
        self.checks: list[dict] = []
        self.t0 = time.time()

    def message(self, direction: str, step: int, peer, payload: str) -> None:
        self.entries.append(
            {
                "t": round(time.time() - self.t0, 3),
                "direction": direction,
                "step": step,
                "peer": f"{peer[0]}:{peer[1]}" if peer else "",
                "bytes": len(payload),
                "payload": payload,
            }
        )

    def note(self, step: int, text: str) -> None:
        self.entries.append(
            {"t": round(time.time() - self.t0, 3), "direction": "NOTE", "step": step,
             "peer": "", "bytes": 0, "payload": text}
        )

    def check(self, step: int, name: str, ok: bool, detail: str = "") -> None:
        self.checks.append(
            {"step": step, "check": name, "ok": bool(ok), "detail": detail}
        )

    def render(self) -> str:
        out = [f"algorithm={self.algorithm}", LINE]
        for e in self.entries:
            if e["direction"] == "NOTE":
                out.append(f"[{e['t']:7.3f}] NOTE step={e['step']} {e['payload']}")
                continue
            out.append(
                f"[{e['t']:7.3f}] {e['direction']:10s} step={e['step']:<2d} "
                f"peer={e['peer']} bytes={e['bytes']}"
            )
            out.extend(
                ("    " + ln).rstrip()
                for ln in e["payload"].rstrip("\n").splitlines()
            )
        out.append(LINE)
        for c in self.checks:
            out.append(
                f"[{'OK ' if c['ok'] else 'BAD'}] step {c['step']}: "
                f"{c['check']} :: {c['detail']}"
            )
        return "\n".join(out) + "\n"

    def steps(self) -> dict:
        by_step: dict[int, list[dict]] = {}
        for c in self.checks:
            by_step.setdefault(c["step"], []).append(c)
        result = {}
        for step, direction, title in OFFICIAL_STEPS:
            checks = by_step.get(step, [])
            executed = bool(checks)
            ok = executed and all(c["ok"] for c in checks)
            result[str(step)] = {
                "direction": direction,
                "title": title,
                "executed": executed,
                "passed": ok,
                "checks": checks,
            }
        return result


def parse_headers_all(msg: str) -> dict[str, list[str]]:
    headers: dict[str, list[str]] = {}
    for line in msg.splitlines()[1:]:
        if not line.strip():
            break
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers.setdefault(name.strip().lower(), []).append(value.strip())
    return headers


def parse_headers(msg: str) -> dict[str, str]:
    return {name: values[0] for name, values in parse_headers_all(msg).items()}


def start_line(msg: str) -> str:
    return msg.splitlines()[0].strip() if msg.strip() else ""


def join_header_values(values: list[str]) -> str:
    return ", ".join(v for v in values if v)


def split_security_entries(value: str) -> list[str]:
    """Split a comma-separated Security-Client/Server/Verify field."""
    entries: list[str] = []
    current: list[str] = []
    quoted = False
    escaped = False
    for ch in value:
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if ch == "\\":
            current.append(ch)
            escaped = True
            continue
        if ch == '"':
            quoted = not quoted
            current.append(ch)
            continue
        if ch == "," and not quoted:
            entry = "".join(current).strip()
            if entry:
                entries.append(entry)
            current = []
            continue
        current.append(ch)
    entry = "".join(current).strip()
    if entry:
        entries.append(entry)
    return entries


def parse_security(header_value: str) -> dict[str, str]:
    """Parse a Security-Client / Security-Server ipsec-3gpp header."""
    params: dict[str, str] = {}
    for part in re.split(r"[;\s]+", header_value):
        if "=" in part:
            key, value = part.split("=", 1)
            params[key.strip().lower()] = value.strip().strip('"')
    return params


def parse_security_entries(header_value: str) -> list[dict[str, str]]:
    return [parse_security(entry) for entry in split_security_entries(header_value)]


def get_uri(value: str) -> str:
    first = value.find("<")
    last = value.rfind(">")
    if first != -1 and last > first:
        return value[first + 1:last]
    return value.split(";", 1)[0].strip()


def uri_hostport(uri: str) -> str:
    match = re.search(r"@([^;>]+)", uri)
    return match.group(1) if match else ""


def uri_port(uri: str) -> int:
    hostport = uri_hostport(uri)
    if ":" not in hostport:
        return 0
    try:
        return int(hostport.rsplit(":", 1)[1])
    except ValueError:
        return 0


def header_has_token(value: str, token: str) -> bool:
    tokens = [part.strip().lower() for part in value.split(",")]
    return token.lower() in tokens


def to_tag(value: str) -> str:
    match = re.search(r"(?:^|;)tag=([^;\s>]+)", value, re.IGNORECASE)
    return match.group(1) if match else ""


def cseq_method(value: str) -> str:
    parts = value.split()
    return parts[-1].upper() if parts else ""


def p_associated_uris(value: str) -> list[str]:
    return [uri for uri in re.findall(r"<([^>]+)>", value) if uri]


def build_notify_body(contact_uri: str, associated_uris: list[str]) -> str:
    rows = []
    for index, uri in enumerate(associated_uris, start=1):
        event = "created" if uri.lower().startswith("tel:") else "registered"
        rows.append(
            f'  <registration aor="{uri}" id="reg-{index}" state="active">\n'
            f'    <contact id="c{index}" state="active" event="{event}">\n'
            f"      <uri>{xml_escape(contact_uri)}</uri>\n"
            "    </contact>\n"
            "  </registration>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<reginfo xmlns="urn:ietf:params:xml:ns:reginfo" version="0" state="full">\n'
        + "\n".join(rows)
        + "\n</reginfo>\n"
    )


def notify_aors(body: str) -> list[str]:
    return re.findall(r'<registration\s+[^>]*aor="([^"]+)"', body)


def response_200_from_request(request: str, headers: list[str], body: str = "") -> str:
    return build_ss_response("", "200 OK", headers, body)


def bind_udp(bind_ip: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((bind_ip, port))
    sock.settimeout(TIMEOUT_S)
    return sock


class SecurityError(RuntimeError):
    pass


def build_ss_response(algorithm: str, status: str, headers: list[str],
                      body: str = "") -> str:
    lines = [f"SIP/2.0 {status}"]
    lines.extend(headers)
    lines.append(f"Content-Length: {len(body.encode('utf-8'))}")
    return "\r\n".join(lines) + "\r\n\r\n" + body


class SsSide:
    """SS/P-CSCF side of TS 34.229-1 Annex C.2, judging a UE."""

    def __init__(self, sock: socket.socket, algorithm: str, transcript: Transcript,
                 ss_port_c: int, ss_port_s: int) -> None:
        self.sock = sock
        self.algorithm = algorithm
        self.tx = transcript
        self.ss_port_c = ss_port_c
        self.ss_port_s = ss_port_s
        self.spi_c = 2000
        self.spi_s = 2001
        self.call_id = ""
        self.auth_nonce = "ss-nonce-0001"
        self.ue_initial = None
        self.ue_sa = None
        self.sa_port_c = 0
        self.security_server_value = ""
        self.initial_headers: dict[str, str] = {}
        self.initial_headers_all: dict[str, list[str]] = {}
        self.second_headers: dict[str, str] = {}
        self.second_headers_all: dict[str, list[str]] = {}
        self.second_contact_uri = ""
        self.subscribe_headers: dict[str, str] = {}
        self.subscribe_headers_all: dict[str, list[str]] = {}
        self.subscribe_call_id = ""
        self.subscribe_from = ""
        self.subscribe_to = ""
        self.subscribe_cseq = ""
        self.service_route_value = SERVICE_ROUTE_VALUE.format(
            ss_ip=self.sock.getsockname()[0],
            ss_port_c=self.ss_port_c,
        )
        self.p_associated_value = f"<{IMPU}>, <tel:{IMPI}>"

    def recv(self, step: int, direction: str = "UE -> SS"):
        data, peer = self.sock.recvfrom(65535)
        payload = data.decode("utf-8", errors="replace")
        self.tx.message(direction, step, peer, payload)
        return payload, peer

    def send(self, payload: str, peer, step: int, direction: str = "SS -> UE") -> None:
        self.sock.sendto(payload.encode("utf-8"), peer)
        self.tx.message(direction, step, peer, payload)

    def run(self) -> None:
        self.step4_initial_register()
        self.step5_challenge()
        self.step6_protected_register()
        self.step7_register_ok()
        self.step8_subscribe()
        self.step9_subscribe_ok()
        self.step10_notify()
        self.step11_notify_ok()

    # -- C.2 Step 4 -------------------------------------------------------
    def step4_initial_register(self) -> None:
        msg, peer = self.recv(4)
        self.ue_initial = peer
        first = start_line(msg)
        headers = parse_headers(msg)
        headers_all = parse_headers_all(msg)
        self.initial_headers = headers
        self.initial_headers_all = headers_all
        self.tx.check(4, "request line is REGISTER", first.upper().startswith("REGISTER"),
                      first)
        self.tx.check(
            4, "Request-URI is the home domain",
            HOME_DOMAIN in first,
            first,
        )
        self.tx.check(
            4, "initial REGISTER is unprotected (no Authorization)",
            "authorization" not in headers,
            f"authorization_present={'authorization' in headers}",
        )
        self.tx.check(
            4, "From and To carry the same public user identity",
            IMPU in headers.get("from", "") and IMPU in headers.get("to", ""),
            f"From={headers.get('from', '')!r} To={headers.get('to', '')!r}",
        )
        contact = headers.get("contact", "")
        self.tx.check(4, "Contact present", bool(contact), contact)
        self.tx.check(
            4, "initial Contact uses an unprotected UE port",
            uri_port(get_uri(contact)) == peer[1],
            f"contact_port={uri_port(get_uri(contact))} source_port={peer[1]}",
        )
        self.tx.check(
            4, "Contact advertises MTSI ICSI and instance ID",
            "icsi.mmtel" in contact and "+sip.instance" in contact,
            contact,
        )
        self.tx.check(
            4, "Expires is the official 600000 seconds",
            headers.get("expires", "") == "600000",
            headers.get("expires", ""),
        )
        self.tx.check(
            4, "Supported contains path",
            header_has_token(headers.get("supported", ""), "path"),
            headers.get("supported", ""),
        )
        self.tx.check(
            4, "Via has rport and a z9hG4bK branch",
            "rport" in headers.get("via", "").lower()
            and "branch=z9hG4bK" in headers.get("via", ""),
            headers.get("via", ""),
        )
        self.tx.check(
            4, "Route is not present in initial REGISTER",
            "route" not in headers,
            f"route_present={'route' in headers}",
        )
        self.tx.check(
            4, "Require contains sec-agree",
            header_has_token(headers.get("require", ""), SEC_AGREE),
            headers.get("require", ""),
        )
        self.tx.check(
            4, "Proxy-Require contains sec-agree",
            header_has_token(headers.get("proxy-require", ""), SEC_AGREE),
            headers.get("proxy-require", ""),
        )
        self.tx.check(
            4, "Max-Forwards is a non-zero value",
            headers.get("max-forwards", "").isdigit()
            and int(headers.get("max-forwards", "0")) > 0,
            headers.get("max-forwards", ""),
        )
        self.tx.check(
            4, "P-Access-Network-Info identifies E-UTRAN",
            "3GPP-E-UTRAN" in headers.get("p-access-network-info", ""),
            headers.get("p-access-network-info", ""),
        )
        sec = headers.get("security-client", "")
        self.tx.check(4, "Security-Client present", bool(sec), sec)
        if sec:
            entries = parse_security_entries(sec)
            params = entries[0] if entries else {}
            self.sa_port_c = int(params.get("port-c", "0") or 0)
            self.tx.check(
                4, "Security-Client announces the negotiated algorithm",
                params.get("alg", "").lower() == self.algorithm,
                f"alg={params.get('alg')!r} expected={self.algorithm!r}",
            )
            self.tx.check(
                4, "Security-Client uses ipsec-3gpp/ESP transport/null cipher",
                sec.lower().startswith("ipsec-3gpp")
                and params.get("protocol", "").lower() == "esp"
                and params.get("mode", "").lower() == "trans"
                and params.get("encrypt-algorithm", "").lower() == "null",
                sec,
            )
            self.tx.check(4, "Security-Client carries spi-c/spi-s/port-c/port-s",
                          all(k in params for k in ("spi-c", "spi-s", "port-c", "port-s")),
                          json.dumps(params, sort_keys=True))
            self.tx.check(
                4, "Security-Client has exactly one mechanism entry",
                len(entries) == 1,
                f"entries={len(entries)}",
            )
        self.call_id = headers.get("call-id", "")
        self.tx.check(4, "Call-ID captured for the dialog", bool(self.call_id),
                      self.call_id)

    # -- C.2 Step 5 -------------------------------------------------------
    def step5_challenge(self) -> None:
        www = (
            f'Digest realm="{REALM}", nonce="{self.auth_nonce}", '
            'algorithm=AKAv1-MD5, qop="auth", opaque="ss-opaque-0001", '
            'ck="84a711db79eebc337b09c8768dfb2ba2", '
            'ik="37e25fda40185767116d30c1b5c0b64a"'
        )
        selected = (
            f"ipsec-3gpp; alg={self.algorithm}; protocol=esp; mode=trans; "
            f"encrypt-algorithm=null; spi-c={self.spi_c}; spi-s={self.spi_s}; "
            f"port-c={self.ss_port_c}; port-s={self.ss_port_s}; q=0.9"
        )
        alternate = (
            f"ipsec-3gpp; alg={OTHER_ALGORITHM[self.algorithm]}; protocol=esp; "
            f"mode=trans; encrypt-algorithm=null; spi-c={self.spi_c + 100}; "
            f"spi-s={self.spi_s + 100}; port-c={self.ss_port_c}; "
            f"port-s={self.ss_port_s}; q=0.7"
        )
        self.security_server_value = f"{selected}, {alternate}"
        initial_to = self.initial_headers.get("to", f"<{IMPU}>")
        if "tag=" not in initial_to:
            initial_to = f"{initial_to};tag=ss-reg-to-1"
        headers = [
            f"Via: {join_header_values(self.initial_headers_all.get('via', []))}",
            f"From: {self.initial_headers.get('from', f'<{IMPU}>')}",
            f"To: {initial_to}",
            f"Call-ID: {self.initial_headers.get('call-id', self.call_id)}",
            f"CSeq: {self.initial_headers.get('cseq', '1 REGISTER')}",
            f"WWW-Authenticate: {www}",
            f"Security-Server: {self.security_server_value}",
        ]
        msg = build_ss_response(self.algorithm, "401 Unauthorized", headers)
        self.send(msg, self.ue_initial, 5)
        self.tx.check(5, "SS sends 401 with AKAv1-MD5 challenge",
                      "algorithm=AKAv1-MD5" in msg, "WWW-Authenticate present")
        self.tx.check(
            5, "401 copies Via/From/To/Call-ID/CSeq from initial REGISTER",
            all(
                marker in msg
                for marker in (
                    f"Call-ID: {self.initial_headers.get('call-id', self.call_id)}",
                    f"CSeq: {self.initial_headers.get('cseq', '1 REGISTER')}",
                )
            ),
            "transaction fields copied",
        )
        self.tx.check(
            5, "Security-Server offers selected algorithm with q=0.9",
            parse_security_entries(self.security_server_value)[0].get("q") == "0.9"
            and parse_security_entries(self.security_server_value)[0].get("alg")
            == self.algorithm,
            self.security_server_value,
        )
        self.tx.check(
            5, "Security-Server offers alternate algorithm with q=0.7",
            len(parse_security_entries(self.security_server_value)) == 2
            and parse_security_entries(self.security_server_value)[1].get("q") == "0.7"
            and parse_security_entries(self.security_server_value)[1].get("alg")
            == OTHER_ALGORITHM[self.algorithm],
            self.security_server_value,
        )

    # -- C.2 Step 6 -------------------------------------------------------
    def step6_protected_register(self) -> None:
        msg, peer = self.recv(6)
        first = start_line(msg)
        headers = parse_headers(msg)
        headers_all = parse_headers_all(msg)
        self.second_headers = headers
        self.second_headers_all = headers_all
        self.ue_sa = peer
        self.tx.check(6, "second REGISTER is a REGISTER request",
                      first.upper().startswith("REGISTER"), first)
        self.tx.check(6, "same Call-ID reused",
                      headers.get("call-id", "") == self.call_id,
                      f"first={self.call_id!r} second={headers.get('call-id')!r}")
        self.tx.check(
            6, "second REGISTER arrives on the announced temporary SA port",
            self.sa_port_c != 0 and peer[1] == self.sa_port_c,
            f"src_port={peer[1]} announced_port-c={self.sa_port_c}",
        )
        contact = headers.get("contact", "")
        self.second_contact_uri = get_uri(contact)
        self.tx.check(
            6, "second REGISTER Contact uses the protected UE port",
            uri_port(self.second_contact_uri) == self.sa_port_c,
            f"contact={self.second_contact_uri!r} port-c={self.sa_port_c}",
        )
        self.tx.check(
            6, "second REGISTER Via uses the protected UE port",
            f":{self.sa_port_c}" in headers.get("via", ""),
            headers.get("via", ""),
        )
        self.tx.check(
            6, "second REGISTER still has Require: sec-agree",
            header_has_token(headers.get("require", ""), SEC_AGREE),
            headers.get("require", ""),
        )
        self.tx.check(
            6, "second REGISTER still has Proxy-Require: sec-agree",
            header_has_token(headers.get("proxy-require", ""), SEC_AGREE),
            headers.get("proxy-require", ""),
        )
        self.tx.check(
            6, "second REGISTER has no Route header",
            "route" not in headers,
            f"route_present={'route' in headers}",
        )
        self.tx.check(
            6, "second REGISTER Max-Forwards is non-zero",
            headers.get("max-forwards", "").isdigit()
            and int(headers.get("max-forwards", "0")) > 0,
            headers.get("max-forwards", ""),
        )
        self.tx.check(
            6, "second REGISTER P-Access-Network-Info identifies E-UTRAN",
            "3GPP-E-UTRAN" in headers.get("p-access-network-info", ""),
            headers.get("p-access-network-info", ""),
        )
        auth = headers.get("authorization", "")
        self.tx.check(6, "Authorization present", bool(auth), auth[:120])
        self.tx.check(
            6, "Authorization response is non-empty",
            bool(re.search(r'response="([^"]+)"', auth)),
            auth[:120],
        )
        self.tx.check(
            6, "Authorization contains the complete AKA Digest tuple",
            all(
                key in auth.lower()
                for key in (
                    'username="', 'realm="', 'nonce="', 'uri="', 'response="',
                    "algorithm=akav1-md5", "qop=auth", "cnonce=", "nc=00000001",
                )
            ),
            auth[:240],
        )
        self.tx.check(
            6, "Authorization nonce/opaque are server values",
            self.auth_nonce in auth and 'opaque="ss-opaque-0001"' in auth,
            auth[:240],
        )
        self.tx.check(
            6, "second REGISTER Contact advertises MTSI ICSI and instance ID",
            "icsi.mmtel" in contact and "+sip.instance" in contact,
            contact,
        )
        client = headers.get("security-client", "")
        self.tx.check(6, "Security-Client present on protected REGISTER",
                      bool(client), client)
        self.tx.check(
            6, "Security-Client is unchanged from the initial REGISTER",
            client == self.initial_headers.get("security-client", ""),
            client,
        )
        verify = headers.get("security-verify", "")
        self.tx.check(6, "Security-Verify present on protected REGISTER",
                      bool(verify), verify)
        if verify:
            ventries = parse_security_entries(verify)
            vparams = ventries[0] if ventries else {}
            self.tx.check(
                6, "Security-Verify echoes the complete Security-Server",
                verify == self.security_server_value,
                verify,
            )
            self.tx.check(
                6, "Security-Verify selected entry echoes SS spi-c/spi-s/port-c/port-s",
                (vparams.get("spi-c") == str(self.spi_c)
                 and vparams.get("spi-s") == str(self.spi_s)
                 and vparams.get("port-c") == str(self.ss_port_c)
                 and vparams.get("port-s") == str(self.ss_port_s)),
                json.dumps(vparams, sort_keys=True),
            )
            self.tx.check(
                6, "Security-Verify carries both PIXIT algorithm candidates",
                len(ventries) == 2
                and ventries[0].get("alg", "").lower() == self.algorithm
                and ventries[1].get("alg", "").lower()
                == OTHER_ALGORITHM[self.algorithm],
                json.dumps(ventries, sort_keys=True),
            )

    # -- C.2 Step 7 -------------------------------------------------------
    def step7_register_ok(self) -> None:
        body = ""
        to_value = self.second_headers.get("to", f"<{IMPU}>")
        if "tag=" not in to_value:
            to_value = f"{to_value};tag=ss-reg-to-1"
        headers = [
            f"Via: {join_header_values(self.second_headers_all.get('via', []))}",
            f"From: {self.second_headers.get('from', f'<{IMPU}>')}",
            f"To: {to_value}",
            f"Call-ID: {self.second_headers.get('call-id', self.call_id)}",
            f"CSeq: {self.second_headers.get('cseq', '2 REGISTER')}",
            f"Contact: {self.second_headers.get('contact', '')};expires=600000",
            f"P-Associated-URI: {self.p_associated_value}",
            f"Service-Route: {self.service_route_value}",
            "Expires: 600000",
        ]
        msg = build_ss_response(self.algorithm, "200 OK", headers, body)
        self.send(msg, self.ue_sa, 7)
        self.tx.check(7, "200 OK sent to the temporary SA port",
                      self.ue_sa[1] == self.sa_port_c,
                      f"dst_port={self.ue_sa[1]}")
        self.tx.check(7, "200 OK carries P-Associated-URI",
                      "P-Associated-URI:" in msg, f"<{IMPU}>")
        self.tx.check(7, "200 OK carries Service-Route",
                      "Service-Route:" in msg, "orig route present")
        self.tx.check(
            7, "200 OK copies the second REGISTER transaction fields",
            all(
                marker in msg
                for marker in (
                    f"Call-ID: {self.second_headers.get('call-id', self.call_id)}",
                    f"CSeq: {self.second_headers.get('cseq', '2 REGISTER')}",
                )
            ),
            "transaction fields copied",
        )
        self.tx.check(
            7, "200 OK Contact matches the registered protected contact",
            self.second_contact_uri in msg,
            self.second_contact_uri,
        )

    # -- C.2 Step 8 -------------------------------------------------------
    def step8_subscribe(self) -> None:
        msg, peer = self.recv(8)
        first = start_line(msg)
        headers = parse_headers(msg)
        headers_all = parse_headers_all(msg)
        self.subscribe_headers = headers
        self.subscribe_headers_all = headers_all
        self.subscribe_call_id = headers.get("call-id", "")
        self.subscribe_from = headers.get("from", "")
        self.subscribe_to = headers.get("to", "")
        self.subscribe_cseq = headers.get("cseq", "")
        self.tx.check(8, "SUBSCRIBE request received", first.upper().startswith("SUBSCRIBE"),
                      first)
        self.tx.check(
            8, "SUBSCRIBE Request-URI is exactly the public user identity",
            first == f"SUBSCRIBE {IMPU} SIP/2.0",
            first,
        )
        self.tx.check(8, "SUBSCRIBE arrives on the new SA port",
                      peer[1] == self.sa_port_c,
                      f"src_port={peer[1]} expected={self.sa_port_c}")
        self.tx.check(
            8, "SUBSCRIBE Contact uses the protected UE port",
            uri_port(get_uri(headers.get("contact", ""))) == self.sa_port_c,
            headers.get("contact", ""),
        )
        self.tx.check(
            8, "SUBSCRIBE Via uses the protected UE port",
            f":{self.sa_port_c}" in headers.get("via", ""),
            headers.get("via", ""),
        )
        self.tx.check(
            8, "SUBSCRIBE follows the stored Service-Route",
            headers.get("route", "") == self.service_route_value,
            f"route={headers.get('route', '')!r} expected={self.service_route_value!r}",
        )
        self.tx.check(
            8, "SUBSCRIBE From has a tag and To is untagged",
            bool(to_tag(self.subscribe_from)) and not to_tag(self.subscribe_to),
            f"From={self.subscribe_from!r} To={self.subscribe_to!r}",
        )
        self.tx.check(
            8, "SUBSCRIBE carries the echoed Security-Verify value",
            headers.get("security-verify", "") == self.security_server_value,
            headers.get("security-verify", ""),
        )
        self.tx.check(
            8, "SUBSCRIBE Require contains sec-agree",
            header_has_token(headers.get("require", ""), SEC_AGREE),
            headers.get("require", ""),
        )
        self.tx.check(
            8, "SUBSCRIBE Proxy-Require contains sec-agree",
            header_has_token(headers.get("proxy-require", ""), SEC_AGREE),
            headers.get("proxy-require", ""),
        )
        self.tx.check(
            8, "SUBSCRIBE Expires is 600000",
            headers.get("expires", "") == "600000",
            headers.get("expires", ""),
        )
        self.tx.check(
            8, "SUBSCRIBE Max-Forwards is non-zero",
            headers.get("max-forwards", "").isdigit()
            and int(headers.get("max-forwards", "0")) > 0,
            headers.get("max-forwards", ""),
        )
        self.tx.check(
            8, "SUBSCRIBE P-Access-Network-Info identifies E-UTRAN",
            "3GPP-E-UTRAN" in headers.get("p-access-network-info", ""),
            headers.get("p-access-network-info", ""),
        )
        self.tx.check(8, "SUBSCRIBE targets the registration event package",
                      headers.get("event", "").lower().startswith("reg"),
                      headers.get("event", ""))
        self.tx.check(
            8, "SUBSCRIBE Accept allows application/reginfo+xml",
            "application/reginfo+xml" in headers.get("accept", ""),
            headers.get("accept", ""),
        )
        self.tx.check(8, "SUBSCRIBE uses the default public user identity",
                      IMPU in self.subscribe_from and IMPU in self.subscribe_to, first)

    # -- C.2 Step 9 -------------------------------------------------------
    def step9_subscribe_ok(self) -> None:
        to_value = self.subscribe_to
        if "tag=" not in to_value:
            to_value = f"{to_value};tag=ss-sub-to-1"
        headers = [
            f"Via: {join_header_values(self.subscribe_headers_all.get('via', []))}",
            f"From: {self.subscribe_from}",
            f"To: {to_value}",
            f"Call-ID: {self.subscribe_call_id}",
            f"CSeq: {self.subscribe_cseq}",
            "Contact: <sip:scscf.3gpp.org>",
            "Expires: 600000",
            f"Record-Route: <sip:{self.sock.getsockname()[0]}:{self.ss_port_c};lr>",
        ]
        msg = build_ss_response(self.algorithm, "200 OK", headers)
        self.send(msg, self.ue_sa, 9)
        self.tx.check(9, "SS accepts SUBSCRIBE with 200 OK", True, "200 OK")
        self.tx.check(
            9, "SUBSCRIBE 200 OK keeps Call-ID and CSeq",
            f"Call-ID: {self.subscribe_call_id}" in msg
            and f"CSeq: {self.subscribe_cseq}" in msg,
            "response correlation",
        )
        self.tx.check(
            9, "SUBSCRIBE 200 OK adds the server To-tag",
            to_tag(to_value) == "ss-sub-to-1",
            to_value,
        )
        self.tx.check(
            9, "SUBSCRIBE 200 OK carries Contact/Expires/Record-Route",
            all(
                header in msg
                for header in (
                    "Contact: <sip:scscf.3gpp.org>",
                    "Expires: 600000",
                    "Record-Route:",
                )
            ),
            "required response headers",
        )

    # -- C.2 Step 10 ------------------------------------------------------
    def step10_notify(self) -> None:
        subscribe_to_tag = "ss-sub-to-1"
        from_value = self.subscribe_to
        if "tag=" not in from_value:
            from_value = f"{from_value};tag={subscribe_to_tag}"
        notify_uri = self.second_contact_uri
        notify_body = build_notify_body(
            self.second_contact_uri,
            p_associated_uris(self.p_associated_value),
        )
        headers = [
            f"Via: SIP/2.0/UDP {self.sock.getsockname()[0]}:{self.ss_port_c};branch=z9hG4bK-ss-ntf",
            "Via: SIP/2.0/UDP scscf.3gpp.org;branch=z9hG4bK-ss-ntf-2",
            f"From: {from_value}",
            f"To: {self.subscribe_from}",
            f"Call-ID: {self.subscribe_call_id}",
            "CSeq: 1 NOTIFY",
            "Contact: <sip:scscf.3gpp.org>",
            "Event: reg",
            "Max-Forwards: 69",
            "Subscription-State: active;expires=600000",
            "Content-Type: application/reginfo+xml",
        ]
        head = "\r\n".join(
            [f"NOTIFY {notify_uri} SIP/2.0"]
            + headers
            + [f"Content-Length: {len(notify_body.encode('utf-8'))}"]
        )
        msg = head + "\r\n\r\n" + notify_body
        self.send(msg, self.ue_sa, 10)
        self.tx.check(10, "NOTIFY carries full registration state XML",
                      "application/reginfo+xml" in msg and 'state="full"' in msg,
                      "reginfo body present")
        self.tx.check(10, "NOTIFY Subscription-State is active",
                      "Subscription-State: active" in msg, "active")
        self.tx.check(
            10, "NOTIFY swaps SUBSCRIBE dialog tags correctly",
            f"From: {from_value}" in msg and f"To: {self.subscribe_from}" in msg,
            f"From={from_value!r} To={self.subscribe_from!r}",
        )
        self.tx.check(
            10, "NOTIFY Call-ID/CSeq correlate to SUBSCRIBE",
            f"Call-ID: {self.subscribe_call_id}" in msg
            and "CSeq: 1 NOTIFY" in msg,
            "dialog correlation",
        )
        self.tx.check(
            10, "NOTIFY Request-URI is the registered protected contact",
            msg.startswith(f"NOTIFY {self.second_contact_uri} SIP/2.0"),
            self.second_contact_uri,
        )
        self.tx.check(
            10, "NOTIFY reginfo aors match P-Associated-URI",
            set(notify_aors(notify_body)) == set(p_associated_uris(self.p_associated_value)),
            f"aors={notify_aors(notify_body)!r}",
        )

    # -- C.2 Step 11 ------------------------------------------------------
    def step11_notify_ok(self) -> None:
        msg, _peer = self.recv(11)
        first = start_line(msg)
        headers = parse_headers(msg)
        self.tx.check(11, "UE answers NOTIFY with 200 OK",
                      first.upper().startswith("SIP/2.0 200"), first)
        self.tx.check(11, "NOTIFY 200 OK keeps the Call-ID",
                      headers.get("call-id", "") == self.subscribe_call_id,
                      headers.get("call-id", ""))
        self.tx.check(
            11, "NOTIFY 200 OK keeps the CSeq method",
            cseq_method(headers.get("cseq", "")) == "NOTIFY",
            headers.get("cseq", ""),
        )
        self.tx.check(
            11, "NOTIFY 200 OK keeps the top Via",
            "z9hG4bK-ss-ntf" in headers.get("via", ""),
            headers.get("via", ""),
        )


def reference_ue(ss_addr, algorithm: str, transcript: Transcript,
                 client_port: int, sa_port: int) -> None:
    """Reference UE emulator: only used to self-test the SS harness."""
    try:
        _reference_ue_inner(ss_addr, algorithm, transcript, client_port, sa_port)
    except SecurityError as exc:
        transcript.note(0, f"reference UE aborted: {exc}")


def _reference_ue_inner(ss_addr, algorithm, tx: Transcript, client_port: int,
                        sa_port: int) -> None:
    plain = bind_udp("127.0.0.1", client_port)
    sa = bind_udp("127.0.0.1", sa_port)
    call_id = "tc011-l1-call-0001"
    subscribe_call_id = "tc011-l1-sub-call-0001"
    contact_base = (
        f'sip:{IMPI}@127.0.0.1:{{port}};+sip.instance='
        f'"<urn:gsma:imei:123456789012345>";'
        f'+g.3gpp.icsi-ref="urn%3Aurn-7%3A3gpp-service.ims.icsi.mmtel"'
    )
    sec_client = (
        f"ipsec-3gpp; alg={algorithm}; protocol=esp; mode=trans; "
        f"encrypt-algorithm=null; spi-c=1000; spi-s=1001; "
        f"port-c={sa_port}; port-s={sa_port + 1}"
    )

    def send(sock, peer, payload, step):
        sock.sendto(payload.encode("utf-8"), peer)
        tx.message("UE -> SS", step, sock.getsockname(), payload)

    def recv(sock, step):
        data, peer = sock.recvfrom(65535)
        payload = data.decode("utf-8", errors="replace")
        tx.message("SS -> UE", step, peer, payload)
        return payload

    # Step 4: initial unprotected REGISTER from the normal client port.
    body = ""
    head = "\r\n".join([
        f"REGISTER sip:{HOME_DOMAIN} SIP/2.0",
        f"Via: SIP/2.0/UDP 127.0.0.1:{client_port};rport;branch=z9hG4bK-ue-1",
        f"From: <{IMPU}>;tag=ue-tag-1",
        f"To: <{IMPU}>",
        f"Call-ID: {call_id}",
        "CSeq: 1 REGISTER",
        f"Contact: <{contact_base.format(port=client_port)}>",
        "Expires: 600000",
        "Supported: path, gruu, outbound",
        f"Require: {SEC_AGREE}",
        f"Proxy-Require: {SEC_AGREE}",
        "Max-Forwards: 70",
        f"P-Access-Network-Info: {P_ACCESS_NETWORK_INFO}",
        f"Security-Client: {sec_client}",
        f"Content-Length: {len(body)}",
    ])
    send(plain, ss_addr, head + "\r\n\r\n" + body, 4)

    challenge = recv(plain, 5)
    headers = parse_headers(challenge)
    server = headers.get("security-server", "")
    if not server:
        raise SecurityError("no Security-Server in 401")
    server_entries = parse_security_entries(server)
    if len(server_entries) != 2:
        raise SecurityError(f"expected two Security-Server entries, got {len(server_entries)}")
    server_entries.sort(key=lambda item: float(item.get("q", "0")), reverse=True)
    sp = server_entries[0]
    if sp.get("alg", "").lower() != algorithm:
        raise SecurityError(
            f"SS selected {sp.get('alg')!r}, expected PIXIT algorithm {algorithm!r}"
        )

    # Step 6: protected REGISTER from the announced temporary SA port.
    auth = (
        f'Digest username="{IMPI}", realm="{REALM}", '
        f'nonce="{headers.get("www-authenticate", "").split("nonce=")[-1].split(",")[0].strip().strip(chr(34))}", '
        f'uri="sip:{HOME_DOMAIN}", response="d0f1e2a3b4c5d6e7", '
        "algorithm=AKAv1-MD5, cnonce=\"ue-cnonce-1\", qop=auth, nc=00000001, "
        'opaque="ss-opaque-0001"'
    )
    head = "\r\n".join([
        f"REGISTER sip:{HOME_DOMAIN} SIP/2.0",
        f"Via: SIP/2.0/UDP 127.0.0.1:{sa_port};rport;branch=z9hG4bK-ue-2",
        f"From: <{IMPU}>;tag=ue-tag-1",
        f"To: <{IMPU}>",
        f"Call-ID: {call_id}",
        "CSeq: 2 REGISTER",
        f"Contact: <{contact_base.format(port=sa_port)}>",
        "Expires: 600000",
        "Supported: path, gruu, outbound",
        f"Require: {SEC_AGREE}",
        f"Proxy-Require: {SEC_AGREE}",
        f"Authorization: {auth}",
        f"Security-Client: {sec_client}",
        f"Security-Verify: {server}",
        "Max-Forwards: 70",
        f"P-Access-Network-Info: {P_ACCESS_NETWORK_INFO}",
        "Content-Length: 0",
    ])
    send(sa, ss_addr, head + "\r\n\r\n", 6)
    ok = recv(sa, 7)
    if "200" not in start_line(ok):
        raise SecurityError(f"registration failed: {start_line(ok)}")
    ok_headers = parse_headers(ok)
    service_route = ok_headers.get("service-route", "")
    associated_uris = p_associated_uris(ok_headers.get("p-associated-uri", ""))
    if not service_route:
        raise SecurityError("200 OK REGISTER did not store Service-Route")
    if not associated_uris:
        raise SecurityError("200 OK REGISTER did not provide P-Associated-URI")

    # Step 8: SUBSCRIBE over the new SA.
    subscribe_from = f"<{IMPU}>;tag=ue-sub-tag-1"
    subscribe_to = f"<{IMPU}>"
    head = "\r\n".join([
        f"SUBSCRIBE {IMPU} SIP/2.0",
        f"Via: SIP/2.0/UDP 127.0.0.1:{sa_port};rport;branch=z9hG4bK-ue-3",
        f"Route: {service_route}",
        f"From: {subscribe_from}",
        f"To: {subscribe_to}",
        f"Call-ID: {subscribe_call_id}",
        "CSeq: 3 SUBSCRIBE",
        f"Contact: <{contact_base.format(port=sa_port)}>",
        f"Security-Verify: {server}",
        f"Require: {SEC_AGREE}",
        f"Proxy-Require: {SEC_AGREE}",
        "Max-Forwards: 70",
        f"P-Access-Network-Info: {P_ACCESS_NETWORK_INFO}",
        "Event: reg",
        "Accept: application/reginfo+xml",
        "Expires: 600000",
        "Content-Length: 0",
    ])
    send(sa, ss_addr, head + "\r\n\r\n", 8)
    sub_ok = recv(sa, 9)
    if "200" not in start_line(sub_ok):
        raise SecurityError(f"SUBSCRIBE rejected: {start_line(sub_ok)}")
    sub_ok_headers = parse_headers(sub_ok)
    if sub_ok_headers.get("call-id", "") != subscribe_call_id:
        raise SecurityError("SUBSCRIBE 200 OK Call-ID mismatch")
    if cseq_method(sub_ok_headers.get("cseq", "")) != "SUBSCRIBE":
        raise SecurityError("SUBSCRIBE 200 OK CSeq mismatch")
    subscribe_to_tag = to_tag(sub_ok_headers.get("to", ""))
    if not subscribe_to_tag:
        raise SecurityError("SUBSCRIBE 200 OK did not add a To-tag")

    # Steps 10-11: accept the NOTIFY.
    notify = recv(sa, 10)
    nh = parse_headers(notify)
    nh_all = parse_headers_all(notify)
    if nh.get("call-id", "") != subscribe_call_id:
        raise SecurityError("NOTIFY Call-ID mismatch")
    if cseq_method(nh.get("cseq", "")) != "NOTIFY":
        raise SecurityError("NOTIFY CSeq mismatch")
    if to_tag(nh.get("from", "")) != subscribe_to_tag:
        raise SecurityError("NOTIFY From-tag does not match SUBSCRIBE To-tag")
    if to_tag(nh.get("to", "")) != to_tag(subscribe_from):
        raise SecurityError("NOTIFY To-tag does not match SUBSCRIBE From-tag")
    notify_body = notify.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in notify else ""
    if set(notify_aors(notify_body)) != set(associated_uris):
        raise SecurityError("NOTIFY reginfo aors do not match P-Associated-URI")
    response_headers = [
        "SIP/2.0 200 OK",
    ]
    for value in nh_all.get("via", []):
        response_headers.append(f"Via: {value}")
    response_headers.extend([
        f"From: {nh.get('from', '')}",
        f"To: {nh.get('to', '')}",
        f"Call-ID: {nh.get('call-id', '')}",
        f"CSeq: {nh.get('cseq', '')}",
        "Content-Length: 0",
    ])
    head = "\r\n".join(response_headers)
    send(sa, ss_addr, head + "\r\n\r\n", 11)
    plain.close()
    sa.close()


def pick_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def run_one(algorithm: str, bind_ip: str, bind_port: int, out_dir: str,
            selftest: bool) -> dict:
    tx = Transcript(algorithm)
    sock = bind_udp(bind_ip, bind_port)
    ss_port_c = bind_port
    ss_port_s = ss_port_c + 1
    ss = SsSide(sock, algorithm, tx, ss_port_c, ss_port_s)
    error = None

    if selftest:
        client_port = pick_port()
        sa_port = pick_port()
        tx.note(0, f"selftest/reference UE: client_port={client_port} sa_port={sa_port}")
        ue = threading.Thread(
            target=reference_ue,
            args=((bind_ip, bind_port), algorithm, tx, client_port, sa_port),
            daemon=True,
        )
        ue.start()

    try:
        ss.run()
    except socket.timeout:
        error = "timeout waiting for UE message"
        tx.note(0, error)
    except Exception as exc:  # noqa: BLE001 - report any harness failure
        error = f"{type(exc).__name__}: {exc}"
        tx.note(0, error)
    finally:
        sock.close()

    steps = tx.steps()
    executed = sum(1 for s in steps.values() if s["executed"])
    passed = sum(1 for s in steps.values() if s["passed"])
    all_pass = passed == len(OFFICIAL_STEPS)

    os.makedirs(out_dir, exist_ok=True)
    tag = algorithm.replace("/", "_")
    transcript_path = os.path.join(out_dir, f"tc011-l1-{tag}-transcript.txt")
    verdict_path = os.path.join(out_dir, f"tc011-l1-{tag}-verdict.json")

    with open(transcript_path, "w", encoding="utf-8") as fh:
        fh.write(tx.render())

    verdict = {
        "tc_id": "TC-011",
        "official_spec": "3GPP TS 34.229-1 clause 8.1 + Annex C.2",
        "layer": "L1_LOCAL_SIMULATED",
        "official_verdict": None,
        "dut": "reference_ue_emulator" if selftest else "external",
        "pixit": {"px_IMS_IpSecAlgorithm": algorithm},
        "algorithm": algorithm,
        "bind": f"{bind_ip}:{bind_port}",
        "started_epoch": int(tx.t0),
        "steps": steps,
        "summary": {
            "official_steps": len(OFFICIAL_STEPS),
            "executed": executed,
            "passed": passed,
            "local_l1_verdict": "PASS" if all_pass else "FAIL",
        },
        "ipsec_realization": "port_pair_emulation_no_kernel_xfrm",
        "error": error,
        "artifacts": {
            "transcript": transcript_path,
            "verdict": verdict_path,
        },
        "notes": [
            "Real SIP messages over a real UDP socket; per-message checks follow "
            "TS 34.229-1 Annex C.2 Steps 4-11.",
            "IPsec is emulated at the Security-Client/Security-Verify port and SPI "
            "level. No kernel xfrm state/policy is created, so this is not proof "
            "that ESP/AH protected the SIP exchange.",
            "This is not a 36.523-1 / 34.229-1 conformance verdict. Only a "
            "qualified SS or accredited laboratory can produce that.",
        ],
    }
    with open(verdict_path, "w", encoding="utf-8") as fh:
        json.dump(verdict, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return verdict


def cmd_selftest(bind_ip: str, out_dir: str) -> int:
    results = []
    for algorithm in ALGORITHMS:
        verdict = run_one(algorithm, bind_ip, pick_port(), out_dir, selftest=True)
        results.append(verdict)
        print(LINE)
        print(f"PIXIT round: px_IMS_IpSecAlgorithm = {algorithm}")
        for step, info in verdict["steps"].items():
            mark = "OK " if info["passed"] else ("---" if not info["executed"] else "BAD")
            print(f"  [{mark}] C.2 step {step:<2s} {info['direction']:9s} {info['title']}")
            for check in info["checks"]:
                print(f"         {'ok ' if check['ok'] else 'BAD'} {check['check']}"
                      f" :: {check['detail']}")
        print(f"  local L1 verdict: {verdict['summary']['local_l1_verdict']}"
              f" ({verdict['summary']['passed']}/{verdict['summary']['official_steps']})")

    summary = {
        "tc_id": "TC-011",
        "layer": "L1_LOCAL_SIMULATED",
        "official_verdict": None,
        "rounds": [
            {
                "algorithm": r["algorithm"],
                "executed": r["summary"]["executed"],
                "passed": r["summary"]["passed"],
                "verdict": r["summary"]["local_l1_verdict"],
                "verdict_json": os.path.basename(r["artifacts"]["verdict"]),
            }
            for r in results
        ],
        "all_rounds_pass": all(
            r["summary"]["local_l1_verdict"] == "PASS" for r in results
        ),
        "ipsec_realization": "port_pair_emulation_no_kernel_xfrm",
    }
    summary_path = os.path.join(out_dir, "tc011-l1-selftest-summary.json")
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(LINE)
    print(f"summary: {summary_path}")
    print(f"all PIXIT rounds pass: {summary['all_rounds_pass']}")
    return 0 if summary["all_rounds_pass"] else 1


def cmd_dut(bind_ip: str, port: int, algorithm: str, out_dir: str) -> int:
    verdict = run_one(algorithm, bind_ip, port, out_dir, selftest=False)
    print(LINE)
    for step, info in verdict["steps"].items():
        mark = "OK " if info["passed"] else ("---" if not info["executed"] else "BAD")
        print(f"[{mark}] C.2 step {step:<2s} {info['direction']:9s} {info['title']}")
        for check in info["checks"]:
            print(f"       {'ok ' if check['ok'] else 'BAD'} {check['check']}"
                  f" :: {check['detail']}")
    print(f"local L1 verdict: {verdict['summary']['local_l1_verdict']}")
    if verdict["error"]:
        print(f"error: {verdict['error']}")
    return 0 if verdict["summary"]["local_l1_verdict"] == "PASS" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--selftest",
        "--selfcheck",
        dest="selftest",
        action="store_true",
        help="run the SS harness against the reference UE emulator",
    )
    mode.add_argument("--dut", action="store_true",
                      help="run the SS harness against an external UE/DUT")
    parser.add_argument("--algorithm", choices=sorted(ALGORITHMS),
                        default="hmac-md5-96")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--out-dir", default="outputs/tc011-l1-selfcheck")
    args = parser.parse_args()

    if args.selftest:
        rc = cmd_selftest(args.bind, args.out_dir)
        print("SELFCHECK PASS" if rc == 0 else "SELFCHECK FAIL")
        return rc
    port = args.port or pick_port()
    return cmd_dut(args.bind, port, args.algorithm, args.out_dir)


if __name__ == "__main__":
    sys.exit(main())
