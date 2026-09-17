# TC-027 aSRVCC

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`13.4.3.7 / 13.4.3.10`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 ID 已锚定；当前仅标准判据，真实 aSRVCC/SS 注入缺失。

## 1. 目的 / 为什么

验证接入转移 aSRVCC（MO/MT call）在 E-UTRA voice to UTRA CS voice 切换及 SRVCC HO completed/cancelled/Forked 子例下行为正确。

## 2. 官方骨架

- 正文行锚（36.523-1 正文/TP，2026-09-11 重新核对）：
  - 13.4.3.7 body 行 257651 / TP 行 257652 / .3.2 行 257860 / Main behaviour 行 257924
  - 13.4.3.10 body 行 259691 / TP 行 259692 / .3.2 行 259903 / Main behaviour 行 259967








- 官方 ID：36.523-1 13.4.3.7（aSRVCC / MO call） / 13.4.3.10（aSRVCC / MT call）
- 来源：`523-1v14.pdf`；映射见 `74-` 表


### 2.1 官方 TP 原文要点

- 13.4.3.7.1 TP（MO aSRVCC）：UE 在 E-UTRA RRC_CONNECTED，IMS MO speech call 处于 alerting；收到 MobilityFromEUTRACommand 后，UE 在 UTRA cell 发送 HANDOVER TO UTRAN COMPLETE。
- 13.4.3.7.1 TP（MO 后续）：UE 进入 UTRA CELL_DCH，MO call alerting 阶段 SRVCC 完成后，收到 CONNECT 时发送 CONNECT ACKNOWLEDGE。
- 13.4.3.10.1 TP（MT aSRVCC）：UE 在 E-UTRA RRC_CONNECTED，IMS MT speech call 处于 alerting；收到 MobilityFromEUTRACommand 后，UE 在 UTRA cell 发送 HANDOVER TO UTRAN COMPLETE。

已抽取 .1 TP 原文；MO/MT alerting 与后续 CONNECT 子例需真实 eNB/EPC/UTRAN + IMS 呼叫台注入。

### 2.2 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-026-031-3.2-main-behaviour.md`
- 源文本：`<local-user>\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 源规范：ETSI TS 136 523-1 V14.3.0 (2018-02)。
- 行号方法：将 CRLF/CR 归一化后按 LF 切分；form-feed 页分隔符不另计一行。
- 覆盖官方小节：13.4.3.7、13.4.3.10
- 说明：以下保留 `.3.2` 原文行号和 `.3.3` 表来源；`P/F` 是官方 TP Verdict 文本，不代表本地已得到一致性 Verdict。
- 正式结论仍必须由 R&S / Anritsu / Keysight 或检测机构按官方 SS 流程执行。

#### TC-027 / 13.4.3.7

- body 行 257651 / TP 行 257652 / Conformance 行 257672 / Test description 行 257851 / Pre-test 行 257852 / Test procedure 行 257860 / Main behaviour 行 257924-258033 / .3.3 行 258070

**官方表清单**

- `Table 13.4.3.7.3.2-1: Time instances of cell power level and parameter changes` 行 257869-257918
- `Table 13.4.3.7.3.2-2: Main behaviour` 行 257924-258033
- `Table 13.4.3.7.3.2-3: Parallel behaviour` 行 258035-258042
- `Table 13.4.3.7.3.2-4: Parallel behaviour` 行 258044-258068
- `Table 13.4.3.7.3.3-0: Conditions for specific message contents` 行 258071-258074；Derivation path: 未在表块内以单行给出
- `Table 13.4.3.7.3.3-1: ATTACH REQUEST (preamble)` 行 258076-258085；Derivation path: 36.508 Table 4.7.2-4
- `Table 13.4.3.7.3.3-2: RRCConnectionReconfiguration (step 16, Table 13.4.3.7.3.2-2)` 行 258087-258088；Derivation path: 36.508, Table 4.6.1-8, condition MEAS
- `Table 13.4.3.7.3.3-3: MeasConfig (Table 13.4.3.7.3.3-2)` 行 258094-258136；Derivation path: 36.508, Table 4.6.6-1, condition UTRAN
- `Table 13.4.3.7.3.3-4: MeasObjectUTRA-f8 (Table 13.4.3.7.3.3-3)` 行 258138-258172；Derivation path: 36.508, Table 4.6.6-3
- `Table 13.4.3.7.3.3-5: MeasurementReport (step 19, Table 13.4.3.7.3.2-2)` 行 258174-258218；Derivation path: 36.508, Table 4.6.1-5
- `Table 13.4.3.7.3.3-6: UECapabilityEnquiry (step 20, Table 13.4.3.7.3.2-2)` 行 258224-258240；Derivation path: 36.508, Table 4.6.1-22
- `Table 13.4.3.7.3.3-7: MobilityFromEUTRACommand (step 22, Table 13.4.3.7.3.2-2)` 行 258242-258267；Derivation path: 36.508, Table 4.6.1-6
- `Table 13.4.3.7.3.3-8: HANDOVER TO UTRAN COMMAND (Table 13.4.3.7.3.3-7)` 行 258269-258270；Derivation path: 36.508, Table 4.7B.1-1, condition UTRA Speech
- `Table 13.4.3.7.3.3-9: SECURITY MODE COMMAND (step 24, Table 13.4.3.7.3.2-2)` 行 258272-258275；Derivation path: 36.508, Table 4.7B.1-n
- `Table 13.4.3.7.3.3-10: CONNECT (step 30, Table 13.4.3.7.3.2-2)` 行 258277-258290；Derivation path: TS 24.008 Table 9.59
- `Table 13.4.3.7.3.3-11: CONNECT ACKNOWLEDGE (step 31, Table 13.4.3.7.3.2-2)` 行 258292-258301；Derivation path: TS 24.008 Table 9.60
- `Table 13.4.3.7.3.3-12: ROUTING AREA UPDATE ACCEPT (step 4, Table 13.4.3.7.3.2-4)` 行 258303-258312；Derivation path: 36.508, Table 4.7B.2-2

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.4.3.7.3.3-0: Conditions for specific message contents

行 258071-258074

```text
258071 | Table 13.4.3.7.3.3-0: Conditions for specific message contents
258072 | in Table 13.4.3.7.3.3-3
258073 | Condition Explanation
258074 | Band > 64 If band > 64 is selected
```

##### Table 13.4.3.7.3.3-1: ATTACH REQUEST (preamble)

行 258076-258085

```text
258076 | Table 13.4.3.7.3.3-1: ATTACH REQUEST (preamble)
258077 | Derivation path: 36.508 Table 4.7.2-4
258078 | Information Element Value/remark Comment Condition
258079 | MS network capability SRVCC from UTRAN
258080 | HSPA or E-UTRAN to
258081 | GERAN/UTRAN
258082 | supported
258084 | Mobile station classmark 2 Any allowed value
258085 | Supported Codecs Any allowed value
```

##### Table 13.4.3.7.3.3-2: RRCConnectionReconfiguration (step 16, Table 13.4.3.7.3.2-2)

行 258087-258088

```text
258087 | Table 13.4.3.7.3.3-2: RRCConnectionReconfiguration (step 16, Table 13.4.3.7.3.2-2)
258088 | Derivation Path: 36.508, Table 4.6.1-8, condition MEAS
```

##### Table 13.4.3.7.3.3-3: MeasConfig (Table 13.4.3.7.3.3-2)

行 258094-258136

```text
258094 | Table 13.4.3.7.3.3-3: MeasConfig (Table 13.4.3.7.3.3-2)
258095 | Derivation Path: 36.508, Table 4.6.6-1, condition UTRAN
258096 | Information Element Value/remark Comment Condition
258097 | MeasConfig ::= SEQUENCE {
258098 |   measObjectToAddModList SEQUENCE (SIZE
258099 | (1..maxObjectId)) OF SEQUENCE {
258100 | 2 entries
258101 |     measObjectId[1] IdMeasObject-f1
258102 |     measObject[1] MeasObjectEUTRA-
258103 | GENERIC(f1)
258105 |     measObject[1] MeasObjectEUTRA-
258106 | GENERIC(maxEARFCN)
258107 |  Band > 64
258108 |     measObjectId[2] IdMeasObject-f8
258109 |     measObject[2] MeasObjectUTRA-f8
258110 |   }
258111 |   reportConfigToAddModList SEQUENCE (SIZE
258112 | (1..maxReportConfigId)) OF SEQUENCE {
258113 | 1 entry
258114 |     reportConfigId[1] IdReportConfig-B2-UTRA
258115 |     reportConfig[1] ReportConfigInterRAT-
258116 | B2-UTRA (-72, -76)
258118 |   }
258119 |   measIdToAddModList SEQUENCE (SIZE
258120 | (1..maxMeasId)) OF SEQUENCE {
258121 | 1 entry
258122 |     measId[1] 1
258123 |     measObjectId[1] IdMeasObject-f8
258124 |     reportConfigId[1] IdReportConfig-B2-UTRA
258125 |   }
258126 |   measObjectToAddModList-v9e0  ::= SEQUENCE
258127 | (SIZE (1..maxObjectId)) OF SEQUENCE {
258128 |   Band > 64
258129 |     measObjectEUTRA-v9e0[1] SEQUENCE {
258130 |     carrierFreq-v9e0 Same downlink EARFCN
258131 | as used for f1
258133 |     }
258134 |     measObjectEUTRA-v9e0[2] SEQUENCE {}
258135 |   }
258136 | }
```

##### Table 13.4.3.7.3.3-4: MeasObjectUTRA-f8 (Table 13.4.3.7.3.3-3)

行 258138-258172

```text
258138 | Table 13.4.3.7.3.3-4: MeasObjectUTRA-f8 (Table 13.4.3.7.3.3-3)
258139 | Derivation Path: 36.508, Table 4.6.6-3
258140 | Information Element Value/remark Comment Condition
258141 | MeasObjectUTRA ::= SEQUENCE {
258142 |   carrierFreq Same downlink ARFCN
258143 | as used for Cell 5
258145 |   cellsToAddModList CHOICE {
258146 |     cellsToAddModListUTRA-FDD SEQUENCE (SIZE
258147 | (1..maxCellMeas)) OF SEQUENCE {
258148 | 1 entry  UTRA-FDD
258149 |       cellIndex[1] 1
258150 |       physCellId[1] PhysicalCellIdentity of
258151 | Cell 5
258153 |     }
258154 |     cellsToAddModListUTRA-TDD SEQUENCE (SIZE
258155 | (1..maxCellMeas)) OF SEQUENCE {
258156 |   UTRA-TDD
258157 |       cellIndex[1] 1
258158 |       physCellId[1] PhysicalCellIdentity of
258159 | Cell 5
258161 |     }
258162 |   }
258163 |   csg-allowedReportingCells-v930 Not present
258164 | }
258170 | Condition Explanation
258171 | UTRA-FDD UTRA FDD cell environment
258172 | UTRA-TDD UTRA TDD cell environment
```

##### Table 13.4.3.7.3.3-5: MeasurementReport (step 19, Table 13.4.3.7.3.2-2)

行 258174-258218

```text
258174 | Table 13.4.3.7.3.3-5: MeasurementReport (step 19, Table 13.4.3.7.3.2-2)
258175 | Derivation Path: 36.508, Table 4.6.1-5
258176 | Information Element Value/remark Comment Condition
258177 | MeasurementReport ::= SEQUENCE {
258178 |   criticalExtensions CHOICE {
258179 |     c1 CHOICE {
258180 |       measurementReport-r8 SEQUENCE {
258181 |         measResults SEQUENCE {
258182 |           measId 1
258183 |           measResultPCell SEQUENCE {
258184 |             rsrpResult (0..97)
258185 |             rsrqResult (0..34)
258186 |           }
258187 |           measResultNeighCells CHOICE {
258188 |             measResultListUTRA SEQUENCE (SIZE
258189 | (1..maxCellReport)) OF SEQUENCE {
258190 | 1 entry
258191 |               physCellId[1] CHOICE {
258192 |                 fdd PhysicalCellIdentity of
258193 | Cell 5
258194 |  UTRA-FDD
258195 |                 tdd PhysicalCellIdentity of
258196 | Cell 5
258197 |  UTRA-TDD
258198 |               }
258199 |               cgi-Info[1] Not present
258200 |               measResult[1] SEQUENCE {
258201 |                 utra-RSCP (-5..91)
258202 |                 utra-EcN0 Not present
258203 |                 additionalSI-Info-r9 Not present
258204 |               }
258205 |             }
258206 |           }
258207 |           measResultForECID-r9 Not present
258208 |           locationInfo-r10 Not present
258209 |           measResultServFreqList-r10 Not present
258210 |         }
258211 |       }
258212 |     }
258213 |   }
258214 | }
258216 | Condition Explanation
258217 | UTRA-FDD UTRA FDD cell environment
258218 | UTRA-TDD UTRA TDD cell environment
```

##### Table 13.4.3.7.3.3-6: UECapabilityEnquiry (step 20, Table 13.4.3.7.3.2-2)

行 258224-258240

```text
258224 | Table 13.4.3.7.3.3-6: UECapabilityEnquiry (step 20, Table 13.4.3.7.3.2-2)
258225 | Derivation Path: 36.508, Table 4.6.1-22
258226 | Information Element Value/remark Comment Condition
258227 | UECapabilityEnquiry ::= SEQUENCE {
258228 |   criticalExtensions CHOICE {
258229 |     c1 CHOICE {
258230 |       ueCapabilityEnquiry-r8 SEQUENCE {
258231 |         ue-CapabilityRequest (SIZE (1..maxRAT-
258232 | Capabilities)) OF SEQUENCE {
258233 | 2 entries
258234 |           RAT-Type[1] eutra
258235 |           RAT-Type[2] utra
258236 |         }
258237 |       }
258238 |     }
258239 |   }
258240 | }
```

##### Table 13.4.3.7.3.3-7: MobilityFromEUTRACommand (step 22, Table 13.4.3.7.3.2-2)

行 258242-258267

```text
258242 | Table 13.4.3.7.3.3-7: MobilityFromEUTRACommand (step 22, Table 13.4.3.7.3.2-2)
258243 | Derivation Path: 36.508, Table 4.6.1-6
258244 | Information Element Value/remark Comment Condition
258245 | MobilityFromEUTRACommand ::= SEQUENCE {
258246 |   criticalExtensions CHOICE {
258247 |     c1 CHOICE {
258248 |       mobilityFromEUTRACommand-r8 SEQUENCE {
258249 |         cs-FallbackIndicator False
258250 |         purpose CHOICE {
258251 |           handover SEQUENCE {
258252 |             targetRAT-Type utra
258253 |             targetRAT-MessageContainer HANDOVER TO UTRAN
258254 | COMMAND(UTRA RRC
258255 | message)
258257 |             nas-SecurityParamFromEUTRA The 4 least significant
258258 | bits of the NAS downlink
258259 | COUNT value
258261 |             systemInformation Not present
258262 |           }
258263 |         }
258264 |       }
258265 |     }
258266 |   }
258267 | }
```

##### Table 13.4.3.7.3.3-8: HANDOVER TO UTRAN COMMAND (Table 13.4.3.7.3.3-7)

行 258269-258270

```text
258269 | Table 13.4.3.7.3.3-8: HANDOVER TO UTRAN COMMAND (Table 13.4.3.7.3.3-7)
258270 | Derivation Path: 36.508, Table 4.7B.1-1, condition UTRA Speech
```

##### Table 13.4.3.7.3.3-9: SECURITY MODE COMMAND (step 24, Table 13.4.3.7.3.2-2)

行 258272-258275

```text
258272 | Table 13.4.3.7.3.3-9: SECURITY MODE COMMAND (step 24, Table 13.4.3.7.3.2-2)
258273 | Derivation Path: 36.508, Table 4.7B.1-n
258274 | Information Element Value/remark Comment Condition
258275 | Ciphering mode info Not present
```

##### Table 13.4.3.7.3.3-10: CONNECT (step 30, Table 13.4.3.7.3.2-2)

行 258277-258290

```text
258277 | Table 13.4.3.7.3.3-10: CONNECT (step 30, Table 13.4.3.7.3.2-2)
258278 | Derivation Path: TS 24.008 Table 9.59
258279 | Information Element Value/remark Comment Condition
258280 | Transaction identifier
258281 |   TI flag '0'B The message is
258282 | sent from the side
258283 | that originates the
258289 | TI
258290 |   TIO '000'B TI value 0
```

##### Table 13.4.3.7.3.3-11: CONNECT ACKNOWLEDGE (step 31, Table 13.4.3.7.3.2-2)

行 258292-258301

```text
258292 | Table 13.4.3.7.3.3-11: CONNECT ACKNOWLEDGE (step 31, Table 13.4.3.7.3.2-2)
258293 | Derivation Path: TS 24.008 Table 9.60
258294 | Information Element Value/remark Comment Condition
258295 | Transaction identifier
258296 |   TI flag '1'B The message is
258297 | sent to the side
258298 | that originates the
258299 | TI
258301 |   TIO '000'B TI value 0
```

##### Table 13.4.3.7.3.3-12: ROUTING AREA UPDATE ACCEPT (step 4, Table 13.4.3.7.3.2-4)

行 258303-258312

```text
258303 | Table 13.4.3.7.3.3-12: ROUTING AREA UPDATE ACCEPT (step 4, Table 13.4.3.7.3.2-4)
258304 | Derivation path: 36.508, Table 4.7B.2-2
258305 | Information Element Value/Remark Comment Condition
258306 | PDP context status 0 NSAPI(0) -
258307 | NSAPI(15) is set
258308 | to 0, which means
258309 | that the SM state
258310 | of all PDP
258311 | contexts is PDP-
258312 | INACTIVE
```

**关键官方判据**

- 步骤 23：UE 在 UTRA Cell 5 发送 `HANDOVER TO UTRAN COMPLETE`，TP Verdict `1 P`（行 257984-257988）。
- 步骤 31：UE 发送 `CONNECT ACKNOWLEDGE`，TP Verdict `2 P`（行 258024-258026）。
- 并行表包含 alerting phase 和 PS 域 RAU（行 258035-258068）。

**Main behaviour 原文（逐行）**

```text
257924 | Table 13.4.3.7.3.2-2: Main behaviour
257925 | St Procedure Message Sequence TP Verdict
257926 |   U - S Message
257927 | 1 The SS configures UTRA Cell 5 to reference
257928 | configuration according 36.508 Table 4.8.3-1,
257929 | condition UTRA Speech.
257930 | - - - -
257931 | 2-13 Steps 1 to 12 of the generic test procedure for
257932 | IMS MO speech call (TS 36.508 4.5A.6.3-1).
257933 | - - - -
257934 | - EXCEPTION: In parallel to the events
257935 | described in steps 14 to 15 the steps specified
257936 | in Table 13.4.3.7.3.2-3 should take place.
257937 | - - - -
257938 | 14 The UE transmits an
257939 | RRCConnectionReconfigurationComplete
257940 | message on Cell 1 to confirm the
257941 | establishment of the new data radio bearer,
257942 | associated with the dedicated EPS bearer.
257943 | --> RRCConnectionReconfigurationC
257944 | omplete
257945 | - -
257946 | 15 The UE transmits an ACTIVATE DEDICATED
257947 | EPS BEARER CONTEXT ACCEPT message
257948 | on Cell 1.
257949 | --> ACTIVATE DEDICATED EPS
257950 | BEARER CONTEXT ACCEPT
257951 | - -
257952 | 16 The SS transmits an
257953 | RRCConnectionReconfiguration message on
257954 | Cell 1 to setup inter-RAT measurement and
257955 | reporting for event B2.
257956 | <-- RRCConnectionReconfiguration - -
257957 | 17 The UE transmits an
257958 | RRCConnectionReconfigurationComplete
257959 | message on Cell 1.
257960 | --> RRCConnectionReconfigurationC
257961 | omplete
257962 | - -
257963 | 18 The SS changes the power level for Cell 1 and
257964 | Cell 5 according to the row "T1" in Table
257965 | 13.4.3.7.3.2-1.
257966 | - - - -
257967 | 19 The UE transmits a MeasurementReport
257968 | message on Cell 1 to report event B2 for Cell
257969 | 5.
257970 | --> MeasurementReport - -
257971 | 20 The SS transmits a UECapabilityEnquiry
257972 | message on Cell 1 to request UE radio access
257973 | capability information for E-UTRA and UTRA.
257974 | <-- UECapabilityEnquiry - -
257975 | 21 The UE transmits a UECapabilityInformation
257976 | message on Cell 1.
257977 | NOTE: The start-CS values received, should
257978 | be used to configure ciphering on Cell 5.
257979 | --> UECapabilityInformation - -
257980 | 22 The SS transmits a
257981 | MobilityFromEUTRACommand message on
257982 | Cell 1.
257983 | <-- MobilityFromEUTRACommand - -
257984 | 23 Check: Does the UE transmit a HANDOVER
257985 | TO UTRAN COMPLETE message on Cell 5?
257986 | --> HANDOVER TO UTRAN
257987 | COMPLETE
257988 | 1 P
257989 | - EXCEPTION: In parallel to the events
257990 | described in step 24 to 29 the steps specified
257991 | in Table 13.4.3.7.3.2-4 takes place.
257992 | - - - -
257993 | 24 The SS transmits a SECURITY MODE
257994 | COMMAND message for the CS domain on
257995 | Cell 5.
257996 | <-- SECURITY MODE COMMAND - -
257997 | 25 The UE transmits a SECURITY MODE
257998 | COMPLETE message on Cell 5.
257999 | --> SECURITY MODE COMPLETE - -
258000 | 26 The SS transmits an UTRAN MOBILITY
258001 | INFORMATION message on Cell 5 to notify
258002 | CN information.
258003 | <-- UTRAN MOBILITY
258004 | INFORMATION
258005 | - -
258006 | 27 The UE transmits an UTRAN MOBILITY
258007 | INFORMATION CONFIRM message on Cell 5.
258008 | --> UTRAN MOBILITY
258009 | INFORMATION CONFIRM
258010 | - -
258011 | 28 The SS transmits a TMSI REALLOCATION
258012 | COMMAND message on Cell 5.
258013 | <-- TMSI REALLOCATION
258014 | COMMAND
258015 | - -
258016 | 29 The UE transmits a TMSI REALLOCATION
258017 | COMPLETE message on Cell 5.
258018 | --> TMSI REALLOCATION
258019 | COMPLETE
258020 | - -
258021 | 30 The SS transmits a CONNECT message  on
258022 | Cell 5.
258023 | <-- CONNECT - -
258024 | 31 Check: Does the UE transmit a CONNECT
258025 | ACKNOWLEDGE message on Cell 5?
258026 | --> CONNECT ACKNOWLEDGE 2 P
258027 | 40 SS adjusts cell levels according to row T2 of - - - -
258032 | table 13.4.3.7.3.2-1.
258033 | - The UE is in end state UTRA CS call (U5). - - - -
```

**Table 13.4.3.7.3.2-3: Parallel behaviour 原文（逐行）**

```text
258035 | Table 13.4.3.7.3.2-3: Parallel behaviour
258036 | St Procedure Message Sequence TP Verdict
258037 |   U - S Message
258038 | 1-7 Steps 5-11 expected sequence defined in
258039 | annex C.21 of TS 34.229-1 [35].
258040 | NOTE: IMS MO speech call is in alerting
258041 | phase.
258042 | - - - -
```

**Table 13.4.3.7.3.2-4: Parallel behaviour 原文（逐行）**

```text
258044 | Table 13.4.3.7.3.2-4: Parallel behaviour
258045 | St Procedure Message Sequence TP Verdict
258046 |   U - S Message
258047 | 1 The UE transmits a ROUTING AREA UPDATE
258048 | REQUEST message on Cell 5.
258049 | --> ROUTING AREA UPDATE
258050 | REQUEST
258051 | - -
258052 | 2 The SS transmits a SECURITY MODE
258053 | COMMAND message for the PS domain on
258054 | Cell 5.
258055 | <-- SECURITY MODE COMMAND - -
258056 | 3 The UE transmits a SECURITY MODE
258057 | COMPLETE message on Cell 5.
258058 | --> SECURITY MODE COMPLETE - -
258059 | 4 The SS transmits a ROUTING AREA UPDATE
258060 | ACCEPT message on Cell 5.
258061 | <-- ROUTING AREA UPDATE
258062 | ACCEPT
258063 | - -
258064 | 5 The UE transmits a ROUTING AREA UPDATE
258065 | COMPLETE message on Cell 5.
258066 | --> ROUTING AREA UPDATE
258067 | COMPLETE
258068 | - -
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。

#### TC-027 / 13.4.3.10

- body 行 259691 / TP 行 259692 / Conformance 行 259711 / Test description 行 259894 / Pre-test 行 259895 / Test procedure 行 259903 / Main behaviour 行 259967-260057 / .3.3 行 260089

**官方表清单**

- `Table 13.4.3.10.3.2-1: Time instances of cell power level and parameter changes` 行 259912-259961
- `Table 13.4.3.10.3.2-2: Main behaviour` 行 259967-260057
- `Table 13.4.3.10.3.2-3: Parallel behaviour` 行 260063-260087
- `Table 13.4.3.10.3.3-0: Conditions for specific message contents` 行 260090-260093；Derivation path: 未在表块内以单行给出
- `Table 13.4.3.10.3.3-1: ATTACH REQUEST (preamble)` 行 260095-260104；Derivation path: 36.508 Table 4.7.2-4
- `Table 13.4.3.10.3.3-2: RRCConnectionReconfiguration (step 24, Table 13.4.3.10.3.2-2)` 行 260106-260107；Derivation path: 36.508, Table 4.6.1-8, condition MEAS
- `Table 13.4.3.10.3.3-3: MeasConfig (Table 13.4.3.10.3.3-2)` 行 260113-260155；Derivation path: 36.508, Table 4.6.6-1, condition UTRAN
- `Table 13.4.3.10.3.3-4: MeasObjectUTRA-f8 (Table 13.4.3.10.3.3-3)` 行 260157-260191；Derivation path: 36.508, Table 4.6.6-3
- `Table 13.4.3.10.3.3-5: MeasurementReport (step 27, Table 13.4.3.10.3.2-2)` 行 260193-260237；Derivation path: 36.508, Table 4.6.1-5
- `Table 13.4.3.10.3.3-6: UECapabilityEnquiry (step 28, Table 13.4.3.10.3.2-2)` 行 260243-260259；Derivation path: 36.508, Table 4.6.1-22
- `Table 13.4.3.10.3.3-7: MobilityFromEUTRACommand (step 30, Table 13.4.3.10.3.2-2)` 行 260261-260286；Derivation path: 36.508, Table 4.6.1-6
- `Table 13.4.3.10.3.3-8: HANDOVER TO UTRAN COMMAND (Table 13.4.3.10.3.3-7)` 行 260288-260289；Derivation path: 36.508, Table 4.7B.1-1, condition UTRA Speech
- `Table 13.4.3.10.3.3-9: SECURITY MODE COMMAND (step 32 Table 13.4.3.10.3.2-2)` 行 260291-260294；Derivation path: 36.508, Table 4.7B.1-n
- `Table 13.4.3.10.3.3-10: CONNECT (step 39, Table 13.4.3.10.3.2-2)` 行 260296-260309；Derivation path: TS 24.008 Table 9.59a
- `Table 13.4.3.10.3.3-11: CONNECT ACKNOWLEDGE (step 40, Table 13.4.3.10.3.2-2)` 行 260311-260320；Derivation path: TS 24.008 Table 9.60
- `Table 13.4.3.10.3.3-12: ROUTING AREA UPDATE ACCEPT (step 4, Table 13.4.3.10.3.2-3)` 行 260322-260331；Derivation path: 36.508, Table 4.7B.2-2

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.4.3.10.3.3-0: Conditions for specific message contents

行 260090-260093

```text
260090 | Table 13.4.3.10.3.3-0: Conditions for specific message contents
260091 | in Table 13.4.3.10.3.3-3
260092 | Condition Explanation
260093 | Band > 64 If band > 64 is selected
```

##### Table 13.4.3.10.3.3-1: ATTACH REQUEST (preamble)

行 260095-260104

```text
260095 | Table 13.4.3.10.3.3-1: ATTACH REQUEST (preamble)
260096 | Derivation path: 36.508 Table 4.7.2-4
260097 | Information Element Value/remark Comment Condition
260098 | MS network capability SRVCC from UTRAN
260099 | HSPA or E-UTRAN to
260100 | GERAN/UTRAN
260101 | supported
260103 | Mobile station classmark 2 Any allowed value
260104 | Supported Codecs Any allowed value
```

##### Table 13.4.3.10.3.3-2: RRCConnectionReconfiguration (step 24, Table 13.4.3.10.3.2-2)

行 260106-260107

```text
260106 | Table 13.4.3.10.3.3-2: RRCConnectionReconfiguration (step 24, Table 13.4.3.10.3.2-2)
260107 | Derivation Path: 36.508, Table 4.6.1-8, condition MEAS
```

##### Table 13.4.3.10.3.3-3: MeasConfig (Table 13.4.3.10.3.3-2)

行 260113-260155

```text
260113 | Table 13.4.3.10.3.3-3: MeasConfig (Table 13.4.3.10.3.3-2)
260114 | Derivation Path: 36.508, Table 4.6.6-1, condition UTRAN
260115 | Information Element Value/remark Comment Condition
260116 | MeasConfig ::= SEQUENCE {
260117 |   measObjectToAddModList SEQUENCE (SIZE
260118 | (1..maxObjectId)) OF SEQUENCE {
260119 | 2 entries
260120 |     measObjectId[1] IdMeasObject-f1
260121 |     measObject[1] MeasObjectEUTRA-
260122 | GENERIC(f1)
260124 |     measObject[1] MeasObjectEUTRA-
260125 | GENERIC(maxEARFCN)
260126 |  Band > 64
260127 |     measObjectId[2] IdMeasObject-f8
260128 |     measObject[2] MeasObjectUTRA-f8
260129 |   }
260130 |   reportConfigToAddModList SEQUENCE (SIZE
260131 | (1..maxReportConfigId)) OF SEQUENCE {
260132 | 1 entry
260133 |     reportConfigId[1] IdReportConfig-B2-UTRA
260134 |     reportConfig[1] ReportConfigInterRAT-
260135 | B2-UTRA (-72, -76)
260137 |   }
260138 |   measIdToAddModList SEQUENCE (SIZE
260139 | (1..maxMeasId)) OF SEQUENCE {
260140 | 1 entry
260141 |     measId[1] 1
260142 |     measObjectId[1] IdMeasObject-f8
260143 |     reportConfigId[1] IdReportConfig-B2-UTRA
260144 |   }
260145 |   measObjectToAddModList-v9e0  ::= SEQUENCE
260146 | (SIZE (1..maxObjectId)) OF SEQUENCE {
260147 |   Band > 64
260148 |     measObjectEUTRA-v9e0[1] SEQUENCE {
260149 |     carrierFreq-v9e0 Same downlink EARFCN
260150 | as used for f1
260152 |     }
260153 |     measObjectEUTRA-v9e0[2] SEQUENCE {}
260154 |   }
260155 | }
```

##### Table 13.4.3.10.3.3-4: MeasObjectUTRA-f8 (Table 13.4.3.10.3.3-3)

行 260157-260191

```text
260157 | Table 13.4.3.10.3.3-4: MeasObjectUTRA-f8 (Table 13.4.3.10.3.3-3)
260158 | Derivation Path: 36.508, Table 4.6.6-3
260159 | Information Element Value/remark Comment Condition
260160 | MeasObjectUTRA ::= SEQUENCE {
260161 |   carrierFreq Same downlink ARFCN
260162 | as used for Cell 5
260164 |   cellsToAddModList CHOICE {
260165 |     cellsToAddModListUTRA-FDD SEQUENCE (SIZE
260166 | (1..maxCellMeas)) OF SEQUENCE {
260167 | 1 entry  UTRA-FDD
260168 |       cellIndex[1] 1
260169 |       physCellId[1] PhysicalCellIdentity of
260170 | Cell 5
260172 |     }
260173 |     cellsToAddModListUTRA-TDD SEQUENCE (SIZE
260174 | (1..maxCellMeas)) OF SEQUENCE {
260175 |   UTRA-TDD
260176 |       cellIndex[1] 1
260177 |       physCellId[1] PhysicalCellIdentity of
260178 | Cell 5
260180 |     }
260181 |   }
260182 |   csg-allowedReportingCells-v930 Not present
260183 | }
260189 | Condition Explanation
260190 | UTRA-FDD UTRA FDD cell environment
260191 | UTRA-TDD UTRA TDD cell environment
```

##### Table 13.4.3.10.3.3-5: MeasurementReport (step 27, Table 13.4.3.10.3.2-2)

行 260193-260237

```text
260193 | Table 13.4.3.10.3.3-5: MeasurementReport (step 27, Table 13.4.3.10.3.2-2)
260194 | Derivation Path: 36.508, Table 4.6.1-5
260195 | Information Element Value/remark Comment Condition
260196 | MeasurementReport ::= SEQUENCE {
260197 |   criticalExtensions CHOICE {
260198 |     c1 CHOICE {
260199 |       measurementReport-r8 SEQUENCE {
260200 |         measResults SEQUENCE {
260201 |           measId 1
260202 |           measResultPCell SEQUENCE {
260203 |             rsrpResult (0..97)
260204 |             rsrqResult (0..34)
260205 |           }
260206 |           measResultNeighCells CHOICE {
260207 |             measResultListUTRA SEQUENCE (SIZE
260208 | (1..maxCellReport)) OF SEQUENCE {
260209 | 1 entry
260210 |               physCellId[1] CHOICE {
260211 |                 fdd PhysicalCellIdentity of
260212 | Cell 5
260213 |  UTRA-FDD
260214 |                 tdd PhysicalCellIdentity of
260215 | Cell 5
260216 |  UTRA-TDD
260217 |               }
260218 |               cgi-Info[1] Not present
260219 |               measResult[1] SEQUENCE {
260220 |                 utra-RSCP (-5..91)
260221 |                 utra-EcN0 Not present
260222 |                 additionalSI-Info-r9 Not present
260223 |               }
260224 |             }
260225 |           }
260226 |           measResultForECID-r9 Not present
260227 |           locationInfo-r10 Not present
260228 |           measResultServFreqList-r10 Not present
260229 |         }
260230 |       }
260231 |     }
260232 |   }
260233 | }
260235 | Condition Explanation
260236 | UTRA-FDD UTRA FDD cell environment
260237 | UTRA-TDD UTRA TDD cell environment
```

##### Table 13.4.3.10.3.3-6: UECapabilityEnquiry (step 28, Table 13.4.3.10.3.2-2)

行 260243-260259

```text
260243 | Table 13.4.3.10.3.3-6: UECapabilityEnquiry (step 28, Table 13.4.3.10.3.2-2)
260244 | Derivation Path: 36.508, Table 4.6.1-22
260245 | Information Element Value/remark Comment Condition
260246 | UECapabilityEnquiry ::= SEQUENCE {
260247 |   criticalExtensions CHOICE {
260248 |     c1 CHOICE {
260249 |       ueCapabilityEnquiry-r8 SEQUENCE {
260250 |         ue-CapabilityRequest (SIZE (1..maxRAT-
260251 | Capabilities)) OF SEQUENCE {
260252 | 2 entries
260253 |           RAT-Type[1] eutra
260254 |           RAT-Type[2] utra
260255 |         }
260256 |       }
260257 |     }
260258 |   }
260259 | }
```

##### Table 13.4.3.10.3.3-7: MobilityFromEUTRACommand (step 30, Table 13.4.3.10.3.2-2)

行 260261-260286

```text
260261 | Table 13.4.3.10.3.3-7: MobilityFromEUTRACommand (step 30, Table 13.4.3.10.3.2-2)
260262 | Derivation Path: 36.508, Table 4.6.1-6
260263 | Information Element Value/remark Comment Condition
260264 | MobilityFromEUTRACommand ::= SEQUENCE {
260265 |   criticalExtensions CHOICE {
260266 |     c1 CHOICE {
260267 |       mobilityFromEUTRACommand-r8 SEQUENCE {
260268 |         cs-FallbackIndicator False
260269 |         purpose CHOICE {
260270 |           handover SEQUENCE {
260271 |             targetRAT-Type utra
260272 |             targetRAT-MessageContainer HANDOVER TO UTRAN
260273 | COMMAND(UTRA RRC
260274 | message)
260276 |             nas-SecurityParamFromEUTRA The 4 least significant
260277 | bits of the NAS downlink
260278 | COUNT value
260280 |             systemInformation Not present
260281 |           }
260282 |         }
260283 |       }
260284 |     }
260285 |   }
260286 | }
```

##### Table 13.4.3.10.3.3-8: HANDOVER TO UTRAN COMMAND (Table 13.4.3.10.3.3-7)

行 260288-260289

```text
260288 | Table 13.4.3.10.3.3-8: HANDOVER TO UTRAN COMMAND (Table 13.4.3.10.3.3-7)
260289 | Derivation Path: 36.508, Table 4.7B.1-1, condition UTRA Speech
```

##### Table 13.4.3.10.3.3-9: SECURITY MODE COMMAND (step 32 Table 13.4.3.10.3.2-2)

行 260291-260294

```text
260291 | Table 13.4.3.10.3.3-9: SECURITY MODE COMMAND (step 32 Table 13.4.3.10.3.2-2)
260292 | Derivation Path: 36.508, Table 4.7B.1-n
260293 | Information Element Value/remark Comment Condition
260294 | Ciphering mode info Not present
```

##### Table 13.4.3.10.3.3-10: CONNECT (step 39, Table 13.4.3.10.3.2-2)

行 260296-260309

```text
260296 | Table 13.4.3.10.3.3-10: CONNECT (step 39, Table 13.4.3.10.3.2-2)
260297 | Derivation Path: TS 24.008 Table 9.59a
260298 | Information Element Value/remark Comment Condition
260299 | Transaction identifier
260300 |   TI flag '1'B The message is
260301 | sent to the side
260302 | that originates the
260308 | TI
260309 |   TIO '000'B TI value 0
```

##### Table 13.4.3.10.3.3-11: CONNECT ACKNOWLEDGE (step 40, Table 13.4.3.10.3.2-2)

行 260311-260320

```text
260311 | Table 13.4.3.10.3.3-11: CONNECT ACKNOWLEDGE (step 40, Table 13.4.3.10.3.2-2)
260312 | Derivation Path: TS 24.008 Table 9.60
260313 | Information Element Value/remark Comment Condition
260314 | Transaction identifier
260315 |   TI flag '0'B The message is
260316 | sent from the side
260317 | that originates the
260318 | TI
260320 |   TIO '000'B TI value 0
```

##### Table 13.4.3.10.3.3-12: ROUTING AREA UPDATE ACCEPT (step 4, Table 13.4.3.10.3.2-3)

行 260322-260331

```text
260322 | Table 13.4.3.10.3.3-12: ROUTING AREA UPDATE ACCEPT (step 4, Table 13.4.3.10.3.2-3)
260323 | Derivation path: 36.508, Table 4.7B.2-2
260324 | Information Element Value/Remark Comment Condition
260325 | PDP context status 0 NSAPI(0) -
260326 | NSAPI(15) is set
260327 | to 0, which means
260328 | that the SM state
260329 | of all PDP
260330 | contexts is PDP-
260331 | INACTIVE
```

**关键官方判据**

- 步骤 31：UE 在 UTRA Cell 5 发送 `HANDOVER TO UTRAN COMPLETE`，TP Verdict `1 P`（行 260009-260013）。
- 步骤 39：UE 发送 `CONNECT`，TP Verdict `2 P`；步骤 40 SS 发送 `CONNECT ACKNOWLEDGE`（行 260047-260052）。
- 并行表 `Table 13.4.3.10.3.2-3`：PS 域 RAU（行 260063-260087）。

**Main behaviour 原文（逐行）**

```text
259967 | Table 13.4.3.10.3.2-2: Main behaviour
259968 | St Procedure Message Sequence TP Verdict
259969 |   U - S Message
259970 | 1 The SS configures UTRA Cell 5 to reference
259971 | configuration according 36.508 Table 4.8.3-1,
259972 | condition UTRA Speech.
259973 | - - - -
259974 | 2-23 Steps 1 to 22 of the generic test procedure for
259975 | IMS MT speech call (TS 36.508 4.5A.7.3-1).
259976 | - - - -
259977 | 24 The SS transmits an
259978 | RRCConnectionReconfiguration message on
259979 | Cell 1 to setup inter-RAT measurement and
259980 | reporting for event B2.
259981 | <-- RRCConnectionReconfiguration - -
259982 | 25 The UE transmits an
259983 | RRCConnectionReconfigurationComplete
259984 | message on Cell 1.
259985 | --> RRCConnectionReconfigurationC
259986 | omplete
259987 | - -
259988 | 26 The SS changes the power level for Cell 1 and
259989 | Cell 5 according to the row "T1" in Table
259990 | 13.4.3.10.3.2-1
259991 | - - - -
259992 | 27 The UE transmits a MeasurementReport
259993 | message on Cell 1 to report event B2 for Cell
259994 | 5.
259995 | --> MeasurementReport - -
259996 | 28 The SS transmits a UECapabilityEnquiry
259997 | message on Cell 1 to request UE radio access
259998 | capability information for E-UTRA and UTRA.
259999 | <-- UECapabilityEnquiry - -
260000 | 29 The UE transmits a UECapabilityInformation
260001 | message on Cell 1.
260002 | NOTE: The start-CS values received, should
260003 | be used to configure ciphering on Cell 5.
260004 | --> UECapabilityInformation - -
260005 | 30 The SS transmits a
260006 | MobilityFromEUTRACommand message on
260007 | Cell 1.
260008 | <-- MobilityFromEUTRACommand - -
260009 | 31 Check: Does the UE transmit a HANDOVER
260010 | TO UTRAN COMPLETE message on Cell 5?
260011 | --> HANDOVER TO UTRAN
260012 | COMPLETE
260013 | 1 P
260014 | - EXCEPTION: In parallel to the events
260015 | described in step 32 to 37 the steps specified
260016 | in Table 13.4.3.10.3.2-3 takes place.
260017 | - - - -
260018 | 32 The SS transmits a SECURITY MODE
260019 | COMMAND message for the CS domain on
260020 | Cell 5.
260021 | <-- SECURITY MODE COMMAND - -
260022 | 33 The UE transmits a SECURITY MODE
260023 | COMPLETE message on Cell 5.
260024 | --> SECURITY MODE COMPLETE - -
260025 | 34 The SS transmits an UTRAN MOBILITY
260026 | INFORMATION message on Cell 5 to notify
260027 | CN information.
260028 | <-- UTRAN MOBILITY
260029 | INFORMATION
260030 | - -
260031 | 35 The UE transmits an UTRAN MOBILITY
260032 | INFORMATION CONFIRM message on Cell 5.
260033 | --> UTRAN MOBILITY
260034 | INFORMATION CONFIRM
260035 | - -
260036 | 36 The SS transmits a TMSI REALLOCATION
260037 | COMMAND message on Cell 5.
260038 | <-- TMSI REALLOCATION
260039 | COMMAND
260040 | - -
260041 | 37 The UE transmits a TMSI REALLOCATION
260042 | COMPLETE message on Cell 5.
260043 | --> TMSI REALLOCATION
260044 | COMPLETE
260045 | - -
260046 | 38 Cause the UE to answer an MT call. (NOTE 1) - - - -
260047 | 39 Check: Does the UE transmit a CONNECT
260048 | message on Cell 5?
260049 | --> CONNECT 2 P
260050 | 40 The SS transmits a CONNECT
260051 | ACKNOWLEDGE message on Cell 5.
260052 | <-- CONNECT ACKNOWLEDGE - -
260053 | 41 SS adjusts cell levels according to row T2 of
260054 | table 13.4.3.10.3.2-1.
260055 | - - - -
260056 | - The UE is in end state UTRA CS call (U5). - - - -
260057 | NOTE 1: The request may be triggered by MMI or by AT command A.
```

**Table 13.4.3.10.3.2-3: Parallel behaviour 原文（逐行）**

```text
260063 | Table 13.4.3.10.3.2-3: Parallel behaviour
260064 | St Procedure Message Sequence TP Verdict
260065 |   U - S Message
260066 | 1 The UE transmits a ROUTING AREA UPDATE
260067 | REQUEST message on Cell 5.
260068 | --> ROUTING AREA UPDATE
260069 | REQUEST
260070 | - -
260071 | 2 The SS transmits a SECURITY MODE
260072 | COMMAND message for the PS domain on
260073 | Cell 5.
260074 | <-- SECURITY MODE COMMAND - -
260075 | 3 The UE transmits a SECURITY MODE
260076 | COMPLETE message on Cell 5.
260077 | --> SECURITY MODE COMPLETE - -
260078 | 4 The SS transmits a ROUTING AREA UPDATE
260079 | ACCEPT message on Cell 5.
260080 | <-- ROUTING AREA UPDATE
260081 | ACCEPT
260082 | - -
260083 | 5 The UE transmits a ROUTING AREA UPDATE
260084 | COMPLETE message on Cell 5.
260085 | --> ROUTING AREA UPDATE
260086 | COMPLETE
260087 | - -
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。


### 2.3 36.508 锚点（通用测试环境）

- 源文本：`<standards-extract>/36508.txt`
- 36.508 `Table 4.5A.6.3-1: EUTRA/EPS signalling for IMS MO speech call` 行 17476
- 36.508 `Table 4.5A.7.3-1: EUTRA/EPS signalling for IMS MT speech call` 行 17622
- 36.508 `Table 4.8.3-1: UTRA reference radio parameters and combinations` 行 35964
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.4 34.108 / 36.523-2 锚点

- 源文本：`<standards-extract>/34108.txt`（TS 34.108 V14.2.0）
- UTRA/GERAN 测试系统配置入口：行 5246-5258，`Configuration 6` 用于 interRAT E-UTRA-UTRA 测试，`Configuration 7` 用于 EUTRA-UTRA-GERAN 测试。
- 523 正文对 UTRA cell 功率表的 34.108 引用：aSRVCC 13.4.3.7 附近行 263774、13.4.3.10 附近行 265053（`TS 34.108 Table 6.1.4 / Table 6.1.9`）。
- 源文本：`<standards-extract>/3652302.txt`（TS 36.523-2 V14.3.0）
- 36.523-2 ICS proforma 用于正式送测时的适用性声明；当前不把其中条目硬挂为 TC-027 的官方 ID。

## 3. 前置条件

- UE 支持 aSRVCC。
- 网络支持接入转移与 IMS 语音。

## 4. 验证流程

1. 建立 MO 或 MT MTSI 语音呼叫。
2. 触发 aSRVCC 接入转移。
3. 验证 SRVCC HO completed/cancelled/Forked 变体行为。

## 5. TP Verdict 判据

- 接入转移完成、呼叫保持。
- 取消/Forked 子例状态正确。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED。

## 7. 受限 / L2_REQUIRED

- 真实 aSRVCC/SS 注入缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```

## 9. L1 测试骨架

- 阶段：`L1_SKELETON`，不代表 `PASS`，不判官方一致性。
- 待补真实环境依赖：真实 eNB/EPC + aSRVCC HSS/IMS + SS/一致性仪表。
- 本骨架作用：预留 L1 可执行入口，先保证套件文档包含官方 TP 原文要点、待注入消息、预期行为和环境依赖。
- L1 runner：`python work/l1_skeleton_026_031.py`
- 判定规则：脚本只检查文档/骨架存在性和环境缺口登记，不输出一致性 Verdict。
