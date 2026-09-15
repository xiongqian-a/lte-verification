#!/usr/bin/env python3
"""TC-032 SIP error-code handling judgement engine.

Anchors:
  503 MO call -> TS 34.229-1 TC 10.1 / 12.2 (503 Service Unavailable with
  Retry-After; UE shall not auto retry inside Retry-After).
  504 MO call -> TS 34.229-1 TC 12.2a (504 Server Time-out with
  application/3gpp-ims+xml restoration body; UE shall initiate initial
  registration).
  401/403/488 are implementation-level per TS 24.229 / 26.114, not attached to
  the 503/504 official TCs.
"""

import argparse
import re
import sys


INVITE_RE = re.compile(r"INVITE\s+sip:|Request msg INVITE/", re.IGNORECASE)
REGISTER_RE = re.compile(r"REGISTER\s+sip:|Request msg REGISTER/", re.IGNORECASE)
ACK_RE = re.compile(r"ACK\s+sip:|Request msg ACK/", re.IGNORECASE)
BYE_RE = re.compile(r"BYE\s+sip:|Request msg BYE/", re.IGNORECASE)
STATUS_RE = re.compile(r"SIP/2\.0\s+(\d{3})|Response msg\s+(\d{3})/|\[(\d{3})\]", re.IGNORECASE)
RETRY_AFTER_RE = re.compile(r"Retry-After:\s*(\d+)", re.IGNORECASE)


def split_lines(text):
    return text.splitlines()


def status_lines(lines, code):
    out = []
    for line in lines:
        match = STATUS_RE.search(line)
        if match:
            found = next((group for group in match.groups() if group is not None), None)
            if found == code:
                out.append(line)
    return out


def has(line, needle):
    return needle.lower() in line.lower()


def check_503(text):
    lines = split_lines(text)
    invites = [i for i, line in enumerate(lines) if INVITE_RE.search(line)]
    status_503 = status_lines(lines, "503")
    retry_after_values = [int(m.group(1)) for line in lines for m in [RETRY_AFTER_RE.search(line)] if m]
    has_ack = any(ACK_RE.search(line) for line in lines)
    has_bye = any(BYE_RE.search(line) for line in lines)
    has_200 = bool(status_lines(lines, "200"))

    checks = [
        ("INVITE sent", bool(invites), "invite_lines=%d" % len(invites)),
        ("503 response observed", bool(status_503), "503_lines=%d" % len(status_503)),
        ("Retry-After present", bool(retry_after_values), "retry_after=%s" % (retry_after_values or [])),
        ("ACK to error response", has_ack, "ack=%s" % has_ack),
        (
            "retry INVITE after Retry-After observed",
            len(invites) >= 2 and has_200,
            "invites=%d has_200=%s" % (len(invites), has_200),
        ),
        ("graceful release/BYE", has_bye, "bye=%s" % has_bye),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def check_504(text):
    lines = split_lines(text)
    invite_present = any(INVITE_RE.search(line) for line in lines)
    register_present = any(REGISTER_RE.search(line) for line in lines)
    has_504 = bool(status_lines(lines, "504"))
    has_p_asserted_identity = any(has(line, "P-Asserted-Identity") for line in lines)
    has_ims_xml = any(has(line, "application/3gpp-ims+xml") for line in lines)
    has_restoration = any(has(line, "<type>") and has(line, "restoration") for line in lines)
    has_initial_registration = any(has(line, "<action>") and has(line, "initial-registration") for line in lines)
    last_504 = None
    for idx, line in enumerate(lines):
        if STATUS_RE.search(line) and "504" in line:
            last_504 = idx
    register_after_504 = (
        last_504 is not None
        and any(REGISTER_RE.search(line) and idx > last_504 for idx, line in enumerate(lines))
    )

    checks = [
        ("INVITE present", invite_present, "invite=%s" % invite_present),
        ("504 response observed", has_504, "504=%s" % has_504),
        ("P-Asserted-Identity present", has_p_asserted_identity, "pai=%s" % has_p_asserted_identity),
        ("Content-Type 3gpp-ims+xml", has_ims_xml, "ims_xml=%s" % has_ims_xml),
        ("alternative-service type=restoration", has_restoration, "restoration=%s" % has_restoration),
        ("action=initial-registration", has_initial_registration, "action=%s" % has_initial_registration),
        ("initial REGISTER after 504", register_after_504, "register_after=%s" % register_after_504),
        ("REGISTER traffic present", register_present, "register=%s" % register_present),
    ]
    overall = all(ok for _, ok, _ in checks)
    return overall, checks


def render_checks(checks):
    for name, is_ok, detail in checks:
        print("  [%s ] %s :: %s" % ("OK" if is_ok else "BAD", name, detail))


def run_selfcheck():
    failed = False

    pass_503 = (
        "[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0\n"
        "Route: <sip:pcscf.ims.example.com;lr>\n"
        "[MESSAGE] SIP/2.0 503 Service Unavailable\n"
        "Retry-After: 20\n"
        "[MESSAGE] ACK sip:bob@ims.example.com SIP/2.0\n"
        "[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0\n"
        "[MESSAGE] SIP/2.0 200 OK\n"
        "[MESSAGE] BYE sip:bob@ims.example.com SIP/2.0\n"
    )
    ok, checks = check_503(pass_503)
    print("SCENARIO: TC-032 503 pass expected=PASS actual=%s" % ("PASS" if ok else "FAIL"))
    render_checks(checks)
    failed = failed or not ok

    fail_503 = pass_503.replace("Retry-After: 20\n", "")
    ok, checks = check_503(fail_503)
    print("SCENARIO: TC-032 503 fail expected=FAIL actual=%s" % ("PASS" if ok else "FAIL"))
    render_checks(checks)
    failed = failed or ok

    pass_504 = (
        "[MESSAGE] INVITE sip:bob@ims.example.com SIP/2.0\n"
        "Route: <sip:pcscf.ims.example.com;lr>\n"
        "[MESSAGE] SIP/2.0 504 Server Time-out\n"
        "P-Asserted-Identity: <sip:scscf.ims.example.com>\n"
        "Content-Type: application/3gpp-ims+xml\n"
        "<ims-3gpp version=\"1\">\n"
        "<alternative-service>\n"
        "<type>restoration</type>\n"
        "<action>initial-registration</action>\n"
        "</alternative-service>\n"
        "</ims-3gpp>\n"
        "[MESSAGE] ACK sip:bob@ims.example.com SIP/2.0\n"
        "[MESSAGE] REGISTER sip:ims.example.com SIP/2.0\n"
    )
    ok, checks = check_504(pass_504)
    print("SCENARIO: TC-032 504 pass expected=PASS actual=%s" % ("PASS" if ok else "FAIL"))
    render_checks(checks)
    failed = failed or not ok

    if failed:
        print("SELFCHECK FAIL")
        return 1
    print("SELFCHECK PASS")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selfcheck", action="store_true")
    parser.add_argument("--log503")
    parser.add_argument("--log504")
    parser.add_argument("--expect", choices=["pass", "fail"])
    args = parser.parse_args()

    if args.selfcheck:
        return run_selfcheck()
    if not args.log503 and not args.log504:
        parser.error("provide --log503 and/or --log504")

    checks = []
    overall = True
    if args.log503:
        with open(args.log503, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        ok503, checks503 = check_503(text)
        print("--- 503 checks (%s) ---" % args.log503)
        render_checks(checks503)
        overall = overall and ok503
        checks.append(("503 flow", ok503, "ok=%s" % ok503))

    if args.log504:
        with open(args.log504, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        ok504, checks504 = check_504(text)
        print("--- 504 checks (%s) ---" % args.log504)
        render_checks(checks504)
        overall = overall and ok504
        checks.append(("504 flow", ok504, "ok=%s" % ok504))

    print("RESULT: %s" % ("PASS" if overall else "FAIL"))
    expected_bool = (args.expect == "pass") if args.expect else None
    if expected_bool is None:
        return 0 if overall else 1
    return 0 if overall == expected_bool else 1


if __name__ == "__main__":
    sys.exit(main())
