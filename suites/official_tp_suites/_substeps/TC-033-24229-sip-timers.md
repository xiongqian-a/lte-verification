# TC-033 SIP 定时器：TS 24.229 Table 7.7.1

来源：`3GPP TS 24.229` V14.17.0 (2022-12)，逐行抽取自 `C:\Users\co1750\Documents\Codex\2026-09-02\i\_extract\24229.txt`；行号口径 `Python str.splitlines()` 1-based。

该条款是 TC-033 的协议支撑证据，不把 TC-033 声称为独立 `34.229-1` 一致性用例。

## 7.7 SIP timers（行 10691-10813；used_by: TC-033）

关键官方标记：`Table 7.7.1: SIP timers`、`Timer A`、`Timer B`、`Timer C`、`Timer D`、`Timer E`、`Timer F`、`Timer G`、`Timer H`、`Timer I`、`Timer J`、`Timer K`、`Timer L`、`Timer M`、`Timer N`、`64*T1`

```text
10691: 7.7	SIP timers
10692: The timers T1, T2, T4 A, B, C, D, E, F, G, H and I (defined in RFC 3261 [26]), timers L and M (defined in RFC 6026 [163]), and timer N (defined in RFC 6665 [28]) need modification in some cases to accommodate the delays introduced by the air interface processing and transmission delays. Table 7.7.1 shows recommended values for IM CN subsystem.
10693: Table 7.7.1 lists in the first column, titled "SIP Timer" the timer names as defined in RFC 3261 [26] and RFC 6026 [163].
10694: The second column, titled "value to be applied between IM CN subsystem elements" lists the values recommended for network elements e.g. P-CSCF, S-CSCF, MGCF, when communicating with each other i.e. when no air interface leg is included. These values are identical to those recommended by RFC 3261 [26], RFC 6026 [163], and RFC 6665 [28].
10695: The third column, titled "value to be applied at the UE" lists the values recommended for the UE, when in normal operation the UE generates requests or responses containing a P-Access-Network-Info header field which included a value of "3GPP-GERAN","3GPP-UTRAN-FDD", "3GPP-UTRAN-TDD", "3GPP-E-UTRAN-FDD", "3GPP-E-UTRAN-TDD", "3GPP-E-UTRAN-ProSe-UNR", "3GPP2-1X", "3GPP2-1X-HRPD", "3GPP2-UMB", "IEEE-802.11", "IEEE-802.11a", "IEEE-802.11b", "IEEE-802.11g", "IEEE-802.11n", or "DVB-RCS2". These are modified when compared to RFC 3261 [26] and RFC 6026 [163] to accommodate the air interface delays. In all other cases, the UE should use the values specified in RFC 3261 [26] or RFC 6026 [163] as indicated in the second column of table 7.7.1.
10696: The fourth column, titled "value to be applied at the P-CSCF toward a UE" lists the values recommended for the P-CSCF when an air interface leg is traversed, and which are used on all SIP transactions on a specific security association where the security association was established using a REGISTER request containing a P-Access-Network-Info header field provided by the UE which included a value of "3GPP-GERAN","3GPP-UTRAN-FDD", "3GPP-UTRAN-TDD", "3GPP-E-UTRAN-FDD", "3GPP-E-UTRAN-TDD", "3GPP-E-UTRAN-ProSe-UNR", "3GPP2-1X", "3GPP2-1X-HRPD", "3GPP2-UMB", "IEEE-802.11", "IEEE-802.11a", "IEEE-802.11b", "IEEE-802.11g", "IEEE-802.11n", or "DVB-RCS2". These are modified when compared to RFC 3261 [26] and RFC 6026 [163]. In all other cases, the P-CSCF should use the values specified in RFC 3261 [26] and RFC 6026 [163] as indicated in the second column of table 7.7.1.
10697: The final column reflects the timer meaning as defined in RFC 3261 [26], RFC 6026 [163] or RFC 6665 [28].
10698: Table 7.7.1: SIP timers
10699: SIP Timer 
10700: Value to be applied between IM CN subsystem elements 
10701: Value to be applied at the UE
10702: Value to be applied at the P-CSCF toward a UE
10703: Meaning
10704: T1
10705: 500ms default
10706: (see NOTE)
10707: 2s default
10708: 2s default
10709: RTT estimate
10710: T2
10711: 4s
10712: (see NOTE)
10713: 16s
10714: 16s
10715: The maximum retransmit interval for non-INVITE requests and INVITE responses
10716: T4
10717: 5s
10718: (see NOTE)
10719: 17s
10720: 17s
10721: Maximum duration a message will remain in the network
10722: Timer A
10723: initially T1
10724: initially T1
10725: initially T1
10726: INVITE request retransmit interval, for UDP only 
10727: Timer B
10728: 64*T1
10729: 64*T1
10730: 64*T1
10731: INVITE transaction timeout timer
10732: Timer C
10733: > 3min
10734: > 3 min
10735: > 3 min
10736: proxy INVITE transaction timeout
10737: Timer D
10738: > 32s for UDP
10739: >128s
10740: >128s
10741: Wait time for response retransmits
10743: 0s for TCP/SCTP
10744:  0s for TCP/SCTP
10745: 0s for TCP/SCTP
10747: Timer E
10748: initially T1
10749: initially T1
10750: initially T1
10751: non-INVITE request retransmit interval, UDP only 
10752: Timer F
10753: 64*T1
10754: 64*T1
10755: 64*T1
10756: non-INVITE transaction timeout timer
10757: Timer G
10758: initially T1
10759: initially T1
10760: initially T1
10761: INVITE response retransmit interval 
10762: Timer H
10763: 64*T1
10764: 64*T1
10765: 64*T1
10766: Wait time for ACK receipt. 
10767: Timer I
10768: T4 for UDP
10769: T4 for UDP
10770: T4 for UDP
10771: Wait time for ACK retransmits 
10773: 0s for TCP/SCTP
10774: 0s for TCP/SCTP
10775: 0s for TCP/SCTP
10777: Timer J
10778: 64*T1 for UDP
10779: 64*T1 for UDP
10780: 64*T1 for UDP
10781: Wait time for non-INVITE request retransmits 
10783: 0s for TCP/SCTP
10784: 0s for TCP/SCTP
10785: 0s for TCP/SCTP
10787: Timer K
10788: T4 for UDP
10789: T4 for UDP
10790: T4 for UDP
10791: Wait time for response retransmits 
10793: 0s for TCP/SCTP
10794: 0s for TCP/SCTP 
10795: 0s for TCP/SCTP
10797: Timer L
10798: 64*T1
10799: 64*T1
10800: 64*T1
10801: Wait time for accepted INVITE
10802: request retransmits
10803: Timer M
10804: 64*T1
10805: 64*T1
10806: 64*T1
10807: Wait time for retransmission of  2xx to INVITE or additional 2xx from other branches of a forked INVITE
10808: Timer N
10809: 64*T1
10810: 64*T1
10811: 64*T1
10812: Wait time for receipt of a NOTIFY request upon sending SUBSCRIBE
10813: NOTE:	As a network option, SIP T1 Timer's value can be extended, along with the necessary modifications of T2 and T4 Timers' values, to take into account the specificities of the supported services when the MRFC and the controlling AS are under the control of the same operator and the controlling AS knows, based on local configuration, that the MRFC implements a longer value of SIP T1 Timer.
```

> 正式 P/F 仍由目标网络/测试台的定时器行为判定；本文件只固定 `24.229` V14.17.0 (2022-12) 表 7.7.1 的原文。
