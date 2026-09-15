#!/usr/bin/env python3
"""Minimal AF_PACKET loopback RTP capture helper for TC-025 evidence.

Run this inside an unprivileged user+network namespace on the server:
  unshare -Urn python3 tc025_rtp_capture.py --out call.pcap --text rtp.txt

It writes a pcap file and a human-readable RTP packet summary. AF_PACKET works
without sudo after unshare gives the process CAP_NET_RAW inside its own netns.
"""

import argparse
import os
import socket
import struct
import sys
import time


def parse_rtp_packet(data):
    """Return parsed loopback IPv4/UDP/RTP fields, or None if not RTP."""
    if len(data) < 14:
        return None
    eth_type = struct.unpack("!H", data[12:14])[0]
    if eth_type != 0x0800:
        return None
    ip = data[14:]
    if len(ip) < 20 or (ip[0] >> 4) != 4:
        return None
    ihl = (ip[0] & 0x0F) * 4
    if ihl < 20 or len(ip) < ihl:
        return None
    if ip[9] != 17:
        return None
    src = socket.inet_ntoa(ip[12:16])
    dst = socket.inet_ntoa(ip[16:20])
    udp = ip[ihl:]
    if len(udp) < 8:
        return None
    sport, dport, ulen, _ = struct.unpack("!HHHH", udp[0:8])
    if ulen < 8 or len(udp) < ulen:
        return None
    payload = udp[8:ulen]
    if len(payload) < 12:
        return None
    vpx = payload[0]
    if (vpx >> 6) != 2:
        return None
    marker = payload[1] >> 7
    pt = payload[1] & 0x7F
    seq, ts, ssrc = struct.unpack("!HII", payload[2:12])
    csrc_len = (vpx & 0x0F) * 4
    if len(payload) < 12 + csrc_len:
        return None
    rtp_payload = payload[12 + csrc_len:]
    return {
        "src": src,
        "sport": sport,
        "dst": dst,
        "dport": dport,
        "pt": pt,
        "seq": seq,
        "ts": ts,
        "ssrc": ssrc,
        "payload": rtp_payload,
    }


def _selfcheck_packet():
    rtp_payload = bytes.fromhex("f0000102")
    rtp = struct.pack("!BBHII", 0x80, 96, 7, 160, 0x12345678) + rtp_payload
    udp = struct.pack("!HHHH", 5000, 5002, 8 + len(rtp), 0) + rtp
    ip = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0, 20 + len(udp), 1, 0, 64, 17, 0,
        socket.inet_aton("127.0.0.1"), socket.inet_aton("127.0.0.2"),
    ) + udp
    eth = b"\x00" * 12 + struct.pack("!H", 0x0800)
    return eth + ip


def run_selfcheck():
    parsed = parse_rtp_packet(_selfcheck_packet())
    checks = [
        ("Ethernet/IPv4/UDP/RTP frame parsed", parsed is not None),
        ("RTP payload type parsed", parsed is not None and parsed["pt"] == 96),
        ("RTP sequence parsed", parsed is not None and parsed["seq"] == 7),
        ("RTP timestamp parsed", parsed is not None and parsed["ts"] == 160),
        ("payload bytes preserved", parsed is not None and parsed["payload"] == bytes.fromhex("f0000102")),
    ]
    for name, ok in checks:
        print("  [%s ] %s" % ("OK" if ok else "BAD", name))
    ok = all(v for _, v in checks)
    print("SELFCHECK %s: RTP capture parser has no raw-socket dependency" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="call.pcap")
    ap.add_argument("--text", default="rtp.txt")
    ap.add_argument("--duration", type=float, default=0.0)
    ap.add_argument("--selfcheck", action="store_true")
    args = ap.parse_args()
    if args.selfcheck:
        return run_selfcheck()

    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    sock.bind(("lo", 0))
    sock.settimeout(1.0)
    start = time.time()
    pcap = open(args.out, "wb")
    txt = open(args.text, "w", encoding="utf-8")
    pcap.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))

    pkt_index = 0
    print("capture_start", flush=True)
    while True:
        try:
            data, _ = sock.recvfrom(65535)
        except socket.timeout:
            if args.duration and time.time() - start >= args.duration:
                break
            continue
        parsed = parse_rtp_packet(data)
        if parsed is None:
            continue
        src = parsed["src"]
        sport = parsed["sport"]
        dst = parsed["dst"]
        dport = parsed["dport"]
        pt = parsed["pt"]
        seq = parsed["seq"]
        ts = parsed["ts"]
        rtp_payload = parsed["payload"]
        pkt_index += 1
        now = time.time() - start
        txt.write(
            "%09.6f pkt=%d src=%s:%d dst=%s:%d pt=%d seq=%d ts=%d plen=%d bytes=%s\n"
            % (now, pkt_index, src, sport, dst, dport, pt, seq, ts, len(rtp_payload),
               rtp_payload[:16].hex())
        )
        pcap.write(struct.pack("<IIII", int(now * 1_000_000), 0, len(data), len(data)))
        pcap.write(data)
        if args.duration and now >= args.duration:
            break
    pcap.close()
    txt.close()
    print("capture_done pkts=%d" % pkt_index, flush=True)


if __name__ == "__main__":
    sys.exit(main())
