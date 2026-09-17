# TC-031 eCall over IMS

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`11.3.5 / 11.3.8`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 ID 已锚定到 36.523-1 11.3 家族；eCall/MSD/SLR/PSAP 环境缺失。

## 1. 目的 / 为什么

验证 UE 在 eCall Only 模式下能通过 IMS 承载自动 eCall，上传 MSD，并在 RACH 失败或 SRVCC 到 GERAN/MSD Update 场景下正确处理。

## 2. 官方骨架

- 正文行锚（36.523-1 正文/TP，2026-09-11 重新核对）：
  - 11.3.5 body 行 240601 / TP 行 240604 / .3.2 行 240685 / Main behaviour 行 240686
  - 11.3.8 body 行 240975 / TP 行 240977 / .3.2 行 241108 / Main behaviour 行 241142








- 官方 ID：36.523-1 11.3.5（eCall Only / EPS supports IMS voice / RACH failure→CS eCall）/ 11.3.8（SRVCC→GERAN / MSD Update / Success）
- 来源：`523-1v14.pdf`；映射见 `74-` 表
- 关联：TS 34.229-1 eCall IMS 流程；TS 26.267 eCall MSD


### 2.1 官方 TP 原文要点

- 11.3.5.1 TP：UE 处于 EMM-DEREGISTERED.eCALL-INACTIVE；请求自动 eCall 且第 1 次 E-UTRA RACH failure 时，UE 使用 CS domain（UTRA/GERAN）建立 eCall。
- 11.3.8.1 TP：UE 处于 eCall Only Mode，IMS eCall 进行中；收到 MobilityFromEUTRACommand（源文显示 UTRA Speech RAB 配置）后，UE 在 geran cell 发送 HANDOVER COMPLETE，随后还应按 TS 26.267 核 MSD Update。

已抽取 .1 TP 原文；需要 eCall Only mode、MSD、RACH failure 注入、PSAP/SLR 或一致性仪表。

### 2.2 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-026-031-3.2-main-behaviour.md`
- 源文本：`<local-user>\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 源规范：ETSI TS 136 523-1 V14.3.0 (2018-02)。
- 行号方法：将 CRLF/CR 归一化后按 LF 切分；form-feed 页分隔符不另计一行。
- 覆盖官方小节：11.3.5、11.3.8
- 说明：以下保留 `.3.2` 原文行号和 `.3.3` 表来源；`P/F` 是官方 TP Verdict 文本，不代表本地已得到一致性 Verdict。
- 正式结论仍必须由 R&S / Anritsu / Keysight 或检测机构按官方 SS 流程执行。

#### TC-031 / 11.3.5

- body 行 240601 / TP 行 240604 / Conformance 行 240613 / Test description 行 240646 / Pre-test 行 240647 / Test procedure 行 240685 / Main behaviour 行 240686-240820 / .3.3 行 240835

**官方表清单**

- `Table 11.3.5.3.2-1: Main behaviour` 行 240686-240820
- `Table 11.3.5.3.2-2: Parallel behaviour` 行 240822-240833
- `Table 11.3.5.3.3-1: Message SystemInformationBlockType1 (Preamble)` 行 240836-240837；Derivation path: 36.508 table 4.4.3.2-3 Condition eCalloverIMS
- `Table 11.3.5.3.3-2: RRC CONNECTION REQUEST (Step 4a2, Table 11.3.5.3.2-1)` 行 240839-240842；Derivation path: TS 34.108 clause 9.1.1
- `Table 11.3.5.3.3-3: CM SERVICE REQUEST (Steps 4a5 and 5b4, Table 11.3.5.3.2-1)` 行 240844-240848；Derivation path: TS 24.008 Table 9.2.11
- `Table 11.3.5.3.3-4: CHANNEL REQUEST (Step 5b2, Table 11.3.5.3.2-1)` 行 240851-240854；Derivation path: TS 44.018 Table 9.1.8.1

**`.3.3` Specific message contents 原文（逐行）**

##### Table 11.3.5.3.3-1: Message SystemInformationBlockType1 (Preamble)

行 240836-240837

```text
240836 | Table 11.3.5.3.3-1: Message SystemInformationBlockType1 (Preamble)
240837 | Derivation path: 36.508 table 4.4.3.2-3 Condition eCalloverIMS
```

##### Table 11.3.5.3.3-2: RRC CONNECTION REQUEST (Step 4a2, Table 11.3.5.3.2-1)

行 240839-240842

```text
240839 | Table 11.3.5.3.3-2: RRC CONNECTION REQUEST (Step 4a2, Table 11.3.5.3.2-1)
240840 | Derivation Path: TS 34.108 clause 9.1.1
240841 | Information Element Value/remark Comment Condition
240842 | Establishment cause Emergency Call
```

##### Table 11.3.5.3.3-3: CM SERVICE REQUEST (Steps 4a5 and 5b4, Table 11.3.5.3.2-1)

行 240844-240848

```text
240844 | Table 11.3.5.3.3-3: CM SERVICE REQUEST (Steps 4a5 and 5b4, Table 11.3.5.3.2-1)
240845 | Derivation Path: TS 24.008 Table 9.2.11
240846 | Information Element Value/remark Comment Condition
240847 | CM service type 0010 Emergency call
240848 | establishment
```

##### Table 11.3.5.3.3-4: CHANNEL REQUEST (Step 5b2, Table 11.3.5.3.2-1)

行 240851-240854

```text
240851 | Table 11.3.5.3.3-4: CHANNEL REQUEST (Step 5b2, Table 11.3.5.3.2-1)
240852 | Derivation Path: TS 44.018 Table 9.1.8.1
240853 | Information Element Value/remark Comment Condition
240854 | Establishment cause 101 Emergency call
```

**关键官方判据**

- 步骤 4a2/4a5/4a10：UTRA `RRC CONNECTION REQUEST`（Emergency Call）、`CM SERVICE REQUEST`、`EMERGENCY SETUP`，各 TP Verdict `1 P`（行 240701-240735）。
- 步骤 5b2/5b4/5b9：GERAN `CHANNEL REQUEST`、`CM SERVICE REQUEST`、`EMERGENCY SETUP`，各 TP Verdict `1 P`（行 240762-240793）。
- 并行表 `Table 11.3.5.3.2-2`：T300 期间重复 RACH，SS 不响应（行 240822-240833）。

**Main behaviour 原文（逐行）**

```text
240686 | Table 11.3.5.3.2-1: Main behaviour
240687 | St Procedure Message Sequence TP Verdict
240688 |   U - S Message
240689 | 1 The UE is switched on. - - - -
240690 | 2 An Automatic eCall is initiated. (Note 1) - - - -
240691 | 3 Check: Does the UE transmit preamble on
240692 | PRACH?
240693 | --> PRACH Preamble - -
240694 | - EXCEPTION: In parallel to the events
240695 | described in step 3 the steps specified in Table
240696 | 11.3.5.3.2-2 should take place.
240697 | - - - -
240698 | 4a1 IF (px_RATComb_Tested = EUTRA_UTRA
240699 | AND pc_CS_Em_Call_in_UTRA)
240700 | - - - -
240701 | 4a2 Check: Does the UE transmit an RRC
240702 | CONNECTION REQUEST message on Cell 5
240703 | with Establishment cause: Emergency Call?
240704 | --> RRC CONNECTION REQUEST 1 P
240705 | 4a3 The SS transmits an RRC CONNECTION
240706 | SETUP message.
240707 | <-- RRC CONNECTION SETUP - -
240708 | 4a4 The UE transmits an RRC CONNECTION
240709 | SETUP COMPLETE message.
240710 | --> RRC CONNECTION SETUP
240711 | COMPLETE
240712 | - -
240713 | 4a5 Check: Does the UE transmit a CM SERVICE
240714 | REQUEST with CM service type IE indicating
240715 | “Emergency call establishment”?
240716 | --> CM SERVICE REQUEST 1 P
240717 | 4a6 The SS transmits an AUTHENTICATION
240718 | REQUEST.
240719 | <-- AUTHENTICATION REQUEST - -
240720 | 4a7 The UE transmits AUTHENTICATION
240721 | RESPONSE.
240722 | --> AUTHENTICATION RESPONSE - -
240723 | 4a8 The SS transmits a SECURITY MODE
240724 | COMMAND message for the CS domain.
240725 | <-- SECURITY MODE COMMAND - -
240726 | 4a9 The UE transmits a SECURITY MODE
240727 | COMPLETE message.
240728 | --> SECURITY MODE COMPLETE - -
240729 | 4a1
240730 | 0
240731 | Check: Does the UE transmit an
240732 | EMERGENCY SETUP message with
240733 | Emergency Service Category IE bit 7 set to 1
240734 | and all other bits are set to 0?
240735 | --> EMERGENCY SETUP 1 P
240736 | 4a1
240737 | 1-
240738 | 4a1
240739 | 6
240740 | Steps 11 to 16 of the generic test procedure in
240741 | TS 34.108 sub clause 7.2.3.2.3 are performed
240742 | on Cell 5.
240743 | NOTE: the CS call setup is completed.
240744 | - - - -
240745 | 4a1
240746 | 7
240747 | The SS transmits DISCONNECT. <-- DISCONNECT - -
240748 | 4a1
240749 | 8
240750 | The UE transmits RELEASE. --> RELEASE - -
240751 | 4a1
240752 | 9
240753 | The SS transmits RELEASE COMPLETE. <-- RELEASE COMPLETE - -
240754 | 4a2
240755 | 0
240756 | The SS transmits an RRCConnectionRelease
240757 | message.
240758 | <-- RRCConnectionRelease - -
240759 | 5b1 IF (px_RATComb_Tested = EUTRA_GERAN
240760 | AND pc_CS_Em_Call_in_GERAN)
240761 | - - - -
240762 | 5b2 Check: Does the UE transmit a CHANNEL
240763 | REQUEST message on Cell 24 with
240764 | Establishment cause: Emergency call?
240765 | --> CHANNEL REQUEST 1 P
240766 | 5b3 The SS transmits an IMMEDIATE
240767 | ASSIGNMENT message.
240768 | <-- IMMEDIATE ASSIGNMENT - -
240769 | 5b4 Check: Does the UE transmit a CM SERVICE
240770 | REQUEST with CM service type IE indicating
240771 | “Emergency call establishment”?
240772 | --> CM SERVICE REQUEST 1 P
240773 | 5b5 The SS transmits an AUTHENTICATION
240774 | REQUEST message
240775 | <-- AUTHENTICATION REQUEST - -
240776 | 5b6 The UE transmits an AUTHENTICATION
240777 | RESPONSE message.
240778 | --> AUTHENTICATION RESPONSE - -
240779 | 5b7 The SS transmits a CIPHERING MODE
240780 | COMMAND.
240781 | <-- CIPHERING MODE COMMAND - -
240782 | 5b8 The UE transmits a CIPHERING MODE
240783 | COMPLETE.
240784 | --> CIPHERING MODE COMPLETE - -
240789 | 5b9 Check: Does the UE transmit an
240790 | EMERGENCY SETUP message with
240791 | Emergency Service Category IE bit 7 set to 1
240792 | and all other bits are set to 0?
240793 | --> EMERGENCY SETUP 1 P
240794 | 5b1
240795 | 0-
240796 | 5b1
240797 | 6
240798 | Steps 11 to 17 of the generic test procedure in
240799 | TS 51.010-1 subclause 10.2.3 are performed
240800 | on Cell 24.
240801 | NOTE: the CS call setup is completed.
240802 | - - - -
240803 | 5b1
240804 | 7
240805 | Traffic channel is kept active for at least 5
240806 | seconds.
240807 | - - - -
240808 | 5b1
240809 | 8
240810 | The SS transmits DISCONNECT. <-- DISCONNECT - -
240811 | 5b1
240812 | 9
240813 | The UE transmits RELEASE. --> RELEASE - -
240814 | 5b2
240815 | 0
240816 | The SS transmits RELEASE COMPLETE. <-- RELEASE COMPLETE - -
240817 | 5b2
240818 | 1
240819 | The SS transmits CHANNEL RELEASE <-- CHANNEL RELEASE - -
240820 | Note 1: The request to originate an automatic eCall may be performed by MMI or AT command.
```

**Table 11.3.5.3.2-2: Parallel behaviour 原文（逐行）**

```text
240822 | Table 11.3.5.3.2-2: Parallel behaviour
240823 | St Procedure Message Sequence TP Verdict
240824 |   U - S Message
240826 | -
240827 | EXCEPTION: The steps 1 and 2 below are
240828 | repeated for the duration of T300.
240829 | - - - -
240830 | 1 The UE attempts to perform RACH procedure
240831 | on Cell A.
240832 | - - - -
240833 | 2 The SS does not respond. - - - -
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。

#### TC-031 / 11.3.8

- body 行 240975 / TP 行 240977 / Conformance 行 240986 / Test description 行 241082 / Pre-test 行 241083 / Test procedure 行 241108 / Main behaviour 行 241142-241207 / .3.3 行 241209

**官方表清单**

- `Table 11.3.8.3.2-1: Time instances of cell power level and parameter changes` 行 241113-241136
- `Table 11.3.8.3.2-2: Main behaviour` 行 241142-241207
- `Table 11.3.8.3.3-1: Message SystemInformationBlockType1 (Preamble)` 行 241210-241211；Derivation path: 36.508 table 4.4.3.2-3 Condition eCalloverIMS
- `Table 11.3.8.3.3-2: ATTACH REQUEST (preamble)` 行 241213-241222；Derivation path: 36.508 Table 4.7.2-4
- `Table 11.3.8.3.3-3: RRCConnectionReconfiguration (step 27, Table 11.3.8.3.2-2)` 行 241228-241229；Derivation path: 36.508, Table 4.6.1-8, condition MEAS
- `Table 11.3.8.3.3-4: MeasConfig (Table 11.3.8.3.3-3)` 行 241231-241266；Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition GERAN
- `Table 11.3.8.3.3-5: MeasurementReport (step 30, Table 11.3.8.3.2-2)` 行 241272-241305；Derivation path: 36.508, table 4.6.1-5
- `Table 11.3.8.3.3-6: MobilityFromEUTRACommand (step 31, Table 11.3.8.3.2-2)` 行 241307-241333；Derivation path: 36.508, Table 4.6.1-6
- `Table 11.3.8.3.3-7: HANDOVER COMMAND (Table 11.3.8.3.3-6)` 行 241339-241372；Derivation path: 51.010, Table 40.2.4.33
- `Table 11.3.8.3.3-10: ROUTING AREA UPDATE ACCEPT (step 51, Table 11.3.8.3.2-2)` 行 241375-241391；Derivation path: 36.508, Table 4.7B.2-2

**`.3.3` Specific message contents 原文（逐行）**

##### Table 11.3.8.3.3-1: Message SystemInformationBlockType1 (Preamble)

行 241210-241211

```text
241210 | Table 11.3.8.3.3-1: Message SystemInformationBlockType1 (Preamble)
241211 | Derivation path: 36.508 table 4.4.3.2-3 Condition eCalloverIMS
```

##### Table 11.3.8.3.3-2: ATTACH REQUEST (preamble)

行 241213-241222

```text
241213 | Table 11.3.8.3.3-2: ATTACH REQUEST (preamble)
241214 | Derivation path: 36.508 Table 4.7.2-4
241215 | Information Element Value/remark Comment Condition
241216 | MS network capability SRVCC from UTRAN
241217 | HSPA or E-UTRAN to
241218 | GERAN/UTRAN
241219 | supported
241221 | Mobile station classmark 2 Any allowed value
241222 | Supported Codecs Any allowed value
```

##### Table 11.3.8.3.3-3: RRCConnectionReconfiguration (step 27, Table 11.3.8.3.2-2)

行 241228-241229

```text
241228 | Table 11.3.8.3.3-3: RRCConnectionReconfiguration (step 27, Table 11.3.8.3.2-2)
241229 | Derivation Path: 36.508, Table 4.6.1-8, condition MEAS
```

##### Table 11.3.8.3.3-4: MeasConfig (Table 11.3.8.3.3-3)

行 241231-241266

```text
241231 | Table 11.3.8.3.3-4: MeasConfig (Table 11.3.8.3.3-3)
241232 | Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition GERAN
241233 | Information Element Value/Remark Comment Condition
241234 | measurementConfiguration ::= SEQUENCE {
241235 |   measObjectToAddModifyList SEQUENCE (SIZE
241236 | (1..maxObjectId)) OF SEQUENCE {
241237 | 2 entries
241238 |     measObjectId[1] IdMeasObject-f11
241239 |     measObject[1] MeasObjectGERAN-
241240 | GENERIC(f11)
241242 |     measObjectId[2] IdMeasObject-f1
241243 |     measObject[2] MeasObjectEUTRA-
241244 | GENERIC(f1)
241246 |   }
241247 |   reportConfigToAddModifyList SEQUENCE (SIZE
241248 | (1..maxReportConfigId)) OF SEQUENCE {
241249 | 1 entry
241250 |     reportConfigId[1] IdReportConfigInterRAT-
241251 | B2-GERAN
241253 |     reportConfig[1] ReportConfigInterRAT-
241254 | B2-GERAN (-69, -75)
241256 |   }
241257 |   measIdToAddModifyList SEQUENCE (SIZE
241258 | (1..maxMeasId)) OF SEQUENCE {
241259 | 1 entry
241260 |     measId[1] 1
241261 |     measObjectId[1] IdMeasObject-f11
241262 |     reportConfigId[1] IdReportConfigInterRAT-
241263 | B2-GERAN
241265 |   }
241266 | }
```

##### Table 11.3.8.3.3-5: MeasurementReport (step 30, Table 11.3.8.3.2-2)

行 241272-241305

```text
241272 | Table 11.3.8.3.3-5: MeasurementReport (step 30, Table 11.3.8.3.2-2)
241273 | Derivation Path: 36.508, table 4.6.1-5
241274 | Information Element Value/remark Comment Condition
241275 | MeasurementReport ::= SEQUENCE {
241276 |   criticalExtensions CHOICE {
241277 |     c1 CHOICE{
241278 |       measurementReport-r8 SEQUENCE {
241279 |         measResults SEQUENCE {
241280 |           measId 1
241281 |           measResultServCell SEQUENCE {
241282 |             rsrpResult (0..97)
241283 |             rsrqResult (0..34)
241284 |           }
241285 |           measResultNeighCells CHOICE {
241286 |             measResultListGERAN SEQUENCE (SIZE
241287 | (1..maxCellReport)) OF SEQUENCE {
241288 | 1 entry
241289 |               physCellId PhysicalCellIdentity of
241290 | Cell 24
241292 |               cgi-Info[1] Not present
241293 |               measResult[1] SEQUENCE {
241294 |                 rssi The value of rssi is
241295 | present but contents not
241296 | checked
241298 |               }
241299 |             }
241300 |           }
241301 |         }
241302 |       }
241303 |     }
241304 |   }
241305 | }
```

##### Table 11.3.8.3.3-6: MobilityFromEUTRACommand (step 31, Table 11.3.8.3.2-2)

行 241307-241333

```text
241307 | Table 11.3.8.3.3-6: MobilityFromEUTRACommand (step 31, Table 11.3.8.3.2-2)
241308 | Derivation Path: 36.508, Table 4.6.1-6
241309 | Information Element Value/remark Comment Condition
241310 | MobilityFromEUTRACommand ::= SEQUENCE {
241311 |   criticalExtensions CHOICE {
241312 |     c1 CHOICE{
241313 |       mobilityFromEUTRACommand-r8 SEQUENCE {
241314 |         cs-FallbackIndicator False
241315 |         purpose CHOICE{
241316 |           handover SEQUENCE {
241317 |             targetRAT-Type GERAN
241318 |             targetRAT-MessageContainer HANDOVER
241319 | COMMAND(GERAN RR
241320 | message) , see Table
241321 | 11.3.8.3.3-7
241323 |             nas-SecurityParamFromEUTRA The 4 least significant
241324 | bits of the NAS downlink
241325 | COUNT value
241327 |             systemInformation Not present
241328 |           }
241329 |         }
241330 |       }
241331 |     }
241332 |   }
241333 | }
```

##### Table 11.3.8.3.3-7: HANDOVER COMMAND (Table 11.3.8.3.3-6)

行 241339-241372

```text
241339 | Table 11.3.8.3.3-7: HANDOVER COMMAND (Table 11.3.8.3.3-6)
241340 | Derivation Path: 51.010, Table 40.2.4.33
241341 | Information Element Value/remark Comment Condition
241342 | Cell Description
241343 |   Network Colour Code 1
241344 |   Base Station Colour Code 5
241345 |   BCCH Carrier Number The BCCH Carrier
241346 | ARFCN as per table in
241347 | clause 40.1.1 of 51.010-
241348 | 1.
241350 | Description of the First Channel, after time
241351 |  Channel Description
241352 |   Channel Type and TDMA offset TCH/F + ACCH’s
241353 |    Timeslot Number Chosen arbitrarily, but not
241354 | Zero.
241356 |    Training Sequence Code Same as the BCCH
241357 |    Hopping channel Single RF channel
241358 |    ARFCN The first ARFCN in the
241359 | cell allocation as per
241360 | table in clause 40.2.1.1.1
241361 | of 51.010-1
241363 | Cipher Mode Setting 1001xxxy See TS 44.018
241364 | §9.1.15.10
241366 | xxx -
241367 | px_GSM_CipherAl
241368 | g
241370 | y -
241371 | px_GSM_Cipherin
241372 | gOnOff
```

##### Table 11.3.8.3.3-10: ROUTING AREA UPDATE ACCEPT (step 51, Table 11.3.8.3.2-2)

行 241375-241391

```text
241375 | Table 11.3.8.3.3-10: ROUTING AREA UPDATE ACCEPT (step 51, Table 11.3.8.3.2-2)
241376 | Derivation path: 36.508, Table 4.7B.2-2
241377 | Information Element Value/Remark Comment Condition
241378 | PDP context status 0 NSAPI(0) -
241379 | NSAPI(15) is set
241380 | to 0, which means
241381 | that the SM state
241382 | of all PDP
241383 | contexts is PDP-
241384 | INACTIVE
241391 | 12 E-UTRA radio bearer tests
```

**关键官方判据**

- 步骤 32：UE 在 Cell 24 发送 `HANDOVER COMPLETE`，TP Verdict `1 P`（行 241177-241179）。
- 步骤 33：`GPRS SUSPENSION REQUEST`；步骤 37：CS traffic channel 保持至少 5 秒用于 in-band MSD transfer（行 241180-241197）。
- 步骤 38-52 接 `36.508 6.4.3.8.1` steps 20-34（行 241199-241206）。

**Main behaviour 原文（逐行）**

```text
241142 | Table 11.3.8.3.2-2: Main behaviour
241143 | St Procedure Message Sequence TP Verdict
241144 |   U - S Message
241145 | 1 The UE is switched on. - - - -
241146 | 2 Wait 60s for the UE to camp on Cell 1 as an
241147 | acceptable cell.
241148 | - - - -
241149 | 3 A manual NG eCall is initiated. (See Note 1).  - - - -
241150 | 4-26 Steps 3 to 25 of the generic Test Procedure for
241151 | eCall over IMS establishment in EUTRA: eCall
241152 | only mode (TS 36.508 4.5A.27).
241153 | - - - -
241154 | 27 The SS transmits an
241155 | RRCConnectionReconfiguration message on
241156 | Cell 1 to setup inter-RAT measurement and
241157 | reporting for event B2.
241158 | <-- RRCConnectionReconfiguration - -
241159 | 28 The UE transmits an
241160 | RRCConnectionReconfigurationComplete
241161 | message on Cell 1.
241162 | --> RRCConnectionReconfigurationC
241163 | omplete
241164 | - -
241165 | 29 The SS changes the power level for Cell 1 and
241166 | Cell 24 according to the row "T1" in Table
241167 | 11.3.8.3.2-1.
241168 | - - - -
241169 | 30 The UE transmits a MeasurementReport
241170 | message on Cell 1 to report event B2 for Cell
241171 | 24.
241172 | --> MeasurementReport - -
241173 | 31 The SS transmits a
241174 | MobilityFromEUTRACommand message on
241175 | Cell 1.
241176 | <-- MobilityFromEUTRACommand - -
241177 | 32 Check: Does the UE transmit a HANDOVER
241178 | COMPLETE message on cell 24?
241179 | --> HANDOVER COMPLETE 1 P
241180 | 33 The UE transmits a GPRS SUSPENSION
241181 | REQUEST message
241182 | --> GPRS SUSPENSION REQUEST - -
241183 | 34 The SS transmits a TMSI REALLOCATION
241184 | COMMAND message.
241185 | <-- TMSI REALLOCATION
241186 | COMMAND
241187 | - -
241188 | 35 The UE transmits a TMSI REALLOCATION
241189 | COMPLETE message.
241190 | --> TMSI REALLOCATION
241191 | COMPLETE
241192 | - -
241193 | 36 SS adjusts cell levels according to row T2 of
241194 | table 11.3.8.3.2-1.
241195 | - - - -
241196 | 37 The CS traffic channel is kept alive by UE for
241197 | at least 5 seconds for In-band MSD transfer
241198 | - - - -
241199 | 38-
241200 | 52
241201 | Steps 20 to 34 of the generic test procedure
241202 | described in TS 36.508 subclause 6.4.3.8.1
241203 | are performed on Cell 24.
241204 | NOTE: Call is released and UE performs a
241205 | RAU procedure.
241206 | - - - -
241207 | Note 1: The request to originate a manual eCall may be performed by MMI or AT command.
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。


### 2.3 36.508 锚点（通用测试环境）

- 旧版 Normal Service 锚点：
  - 源文本：`<standards-extract>/36508.txt`
  - 36.508 `Table 4.5A.26.3-1: EUTRA/EPS signalling for eCall over IMS` 行 19224。
  - 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14。
- eCall Only 正文终核：
  - 源文本：`<standards-extract>/36508-v180600.txt`。
  - 来源规范：ETSI TS 136 508 V18.6.0 (2024-10)，3GPP TS 36.508 version 18.6.0 Release 18。
  - PDF SHA-256：`BD1F0FF368BBDBAAF1EA39E49C68F34F155A0B39A346453A2E2BE5CD5F3A7DBF`。
  - 提取文本 SHA-256：`E7027023DEA7E6537FB17A059C3F2CEAFDA9270B6224D3C0AD14DDC93438DCAB`。
  - `4.5A.27 Generic Test Procedure for eCall over IMS establishment in EUTRA: eCall Only Support`：行 22184-22185。
  - `4.5A.27.1 Initial conditions`：行 22186-22191；UE 初始状态为 `Switched OFF (State 1)`。
  - `4.5A.27.3 Procedure` 与 `Table 4.5A.27.3-1`：行 22194-22300。
  - `Table 4.5A.27.3-2: Parallel behaviour`：行 22302-22319；其中紧急注册引用 `34.229-1 Annex C.20`，NG eCall 建立引用 `34.229-1 Annex C.47`。
  - `4.5A.27.4 Specific message contents`：行 22322-22370。
- `4.5A.27` 已核前置与消息约束：
  - UE 开机后驻留服务小区，并保持 `EMM-DEREGISTERED.eCALL-INACTIVE`（行 22203-22205）。
  - UE 发起 eCall 后发送 `RRCConnectionRequest`，`establishmentCause=emergency`（行 22209-22213）。
  - UE 发送 `PDN CONNECTIVITY REQUEST`，`Request type='0100'B`，APN 不出现或为任意值（行 22234-22236、22324-22328）。
  - SS 建立额外默认承载：EPS bearer context #2、QCI 5，APN 为 IR.88 建议的 SOS APN（行 22238-22246、22330-22347）。
  - SS 建立关联专用承载：EPS bearer context #4、QCI 1，`Linked EPS bearer identity=Default EBId-2`，TFT 按参考专用承载 #1（行 22270-22279、22349-22369）。
  - 并行行为包含 IP 地址分配、IMS emergency registration，以及 `34.229-1 Annex C.47` 的 NG eCall 建立（行 22302-22319）。
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.4 34.108 锚点

- 源文本：`<standards-extract>/34108.txt`（TS 34.108 V14.2.0）
- 34.108 `7.2.5 IMS Emergency Call setup` 行 53980-53982，给出 Normal Service 下移动始发 IMS 紧急呼叫通用流程；52190-5258 给出 UTRA/GERAN 测试系统配置入口，`Configuration 6/7` 与 E-UTRA-UTRA/EUTRA-UTRA-GERAN 测试相关。
- 523 正文 eCall CS 回退对 34.108 的引用：
  - 行 244608：`Steps 11 to 16 of the generic test procedure in TS 34.108 subclause 7.2.3.2.3 are performed on Cell 5.`
  - 行 244899：`Steps 11 to 16 of the generic test procedure in TS 34.108 sub clause 7.2.3.2.3 are performed on Cell 5.`
  - 行 244723 与 244999：`Derivation Path: TS 34.108 clause 9.1.1`（RRC CONNECTION REQUEST）。

## 3. 前置条件

- SS：按 36.508 `4.5A.27.1` 配置基本单小区默认参数；支持 emergency RRC、紧急 PDN、IMS emergency registration 与 NG eCall。
- UE：处于 `Switched OFF (State 1)`；支持 eCall Only；存在 MSD 能力和 MMI/AT eCall 触发源。
- UE 开机后需驻留服务小区，并进入且保持 `EMM-DEREGISTERED.eCALL-INACTIVE`。
- IMS/PSAP/SLR：具备 IMS emergency registration、`34.229-1 Annex C.47` NG eCall 建立、MSD 传输与 PSAP 接入能力。
- 11.3.8 SRVCC：具备 GERAN 目标小区、`MobilityFromEUTRACommand`、CS traffic channel 与 in-band MSD Update 条件。
- 正式判定：必须由合格 SS/一致性仪表或检测机构按官方 TP Verdict 执行；本地无该环境时保持受限。

## 4. 验证流程

1. 触发自动 eCall。
2. 验证 IMS eCall 建立及 MSD 传输。
3. RACH failure 场景验证回退 CS eCall。
4. SRVCC 到 GERAN 后验证 MSD Update。

## 5. TP Verdict 判据

- eCall 建立成功。
- MSD 数据正确。
- 回退/更新场景行为符合官方 TP。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED。

## 7. 受限 / L2_REQUIRED

- eCall/MSD/SLR/PSAP 或一致性仪表缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```

## 9. L1 测试骨架

- 阶段：`L1_SKELETON`，不代表 `PASS`，不判官方一致性。
- 待补真实环境依赖：eCall Only mode + MSD + RACH failure injection + PSAP/SLR + SS/仪表。
- 本骨架作用：预留 L1 可执行入口，先保证套件文档包含官方 TP 原文要点、待注入消息、预期行为和环境依赖。
- L1 runner：`python work/l1_skeleton_026_031.py`
- 判定规则：脚本只检查文档/骨架存在性和环境缺口登记，不输出一致性 Verdict。
