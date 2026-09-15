# TC-026 SRVCC

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`13.4.3.1 / 13.4.3.2 / 13.4.3.3`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 ID 已锚定到 36.523-1 13.4.3 家族；真实 eNB/EPC/SS 或一致性仪表缺失。

## 1. 目的 / 为什么

验证 E-UTRA 语音会话切换至 UTRA/GSM CS 语音时，UE 正确执行 SRVCC 流程并保持语音业务连续。

## 2. 官方骨架

- 正文行锚（36.523-1 正文/TP，2026-09-11 重新核对）：
  - 13.4.3.1 body 行 254166 / TP 行 254167 / .3.2 行 254385 / Main behaviour 行 254445
  - 13.4.3.2 body 行 254762 / TP 行 254764 / .3.2 行 255041 / Main behaviour 行 255101
  - 13.4.3.3 body 行 255457 / TP 行 255458 / .3.2 行 255655 / Main behaviour 行 255687








- 官方 ID：36.523-1 13.4.3.1（E-UTRA voice to UTRA CS）/ 13.4.3.2（PS voice + data）/ 13.4.3.3（to GSM CS）
- 来源：`C:/11/523协议/523-1v14.pdf`；映射见 `74-` 协议完整性核查表
- 关联：TS 36.508 / 34.108 跨 RAT 测试前置；TS 23.401 SRVCC 架构


### 2.1 官方 TP 原文要点

- 13.4.3.1.1 TP：UE 处于 E-UTRA RRC_CONNECTED，IMS voice 进行中；收到 MobilityFromEUTRACommand，UTRA Speech RAB 组合已配置时，UE 在 utra cell 发送 HANDOVER TO UTRAN COMPLETE。
- 13.4.3.2.1 TP：UE 处于 E-UTRA RRC_CONNECTED，IMS voice 进行中；收到 MobilityFromEUTRACommand，UTRA PS RB+Speech 组合已配置时，UE 在 utra cell 发送 HANDOVER TO UTRAN COMPLETE。
- 13.4.3.3.1 TP：UE 处于 E-UTRA RRC_CONNECTED，IMS voice 进行中；收到 MobilityFromEUTRACommand，GERAN Speech RAB 组合已配置时，UE 在 geran cell 发送 HANDOVER COMPLETE。

官方 `.3 Test Procedure` 与 `.3.3 Specific message contents` 正文已按 ETSI TS 136 523-1 V14.3.0 抽取并锚定行号；真实 SS/仪表执行仍待完成。

### 2.2 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-026-031-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 源规范：ETSI TS 136 523-1 V14.3.0 (2018-02)。
- 行号方法：将 CRLF/CR 归一化后按 LF 切分；form-feed 页分隔符不另计一行。
- 覆盖官方小节：13.4.3.1、13.4.3.2、13.4.3.3
- 说明：以下保留 `.3.2` 原文行号和 `.3.3` 表来源；`P/F` 是官方 TP Verdict 文本，不代表本地已得到一致性 Verdict。
- 正式结论仍必须由 R&S / Anritsu / Keysight 或检测机构按官方 SS 流程执行。

#### TC-026 / 13.4.3.1

- body 行 254166 / TP 行 254167 / Conformance 行 254176 / Test description 行 254376 / Pre-test 行 254377 / Test procedure 行 254385 / Main behaviour 行 254445-254529 / .3.3 行 254562

**官方表清单**

- `Table 13.4.3.1.3.2-1: Time instances of cell power level and parameter changes` 行 254390-254439
- `Table 13.4.3.1.3.2-2: Main behaviour` 行 254445-254529
- `Table 13.4.3.1.3.2-3: Void` 行 254535-254535
- `Table 13.4.3.1.3.2-4: Void` 行 254536-254536
- `Table 13.4.3.1.3.2-5: Parallel behaviour` 行 254537-254560
- `Table 13.4.3.1.3.3-0: Conditions for specific message contents` 行 254563-254566；Derivation path: 未在表块内以单行给出
- `Table 13.4.3.1.3.3-1: ATTACH REQUEST (preamble)` 行 254568-254577；Derivation path: 36.508 table 4.7.2-4
- `Table 13.4.3.1.3.3-2: RRCConnectionReconfiguration (step 28, Table 13.4.3.1.3.2-2)` 行 254579-254580；Derivation path: 36.508 clause 4.6.1 table 4.6.1-8 with condition MEAS
- `Table 13.4.3.1.3.3-3: MeasConfig (step 28, Table 13.4.3.1.3.2-2)` 行 254586-254634；Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition UTRAN
- `Table 13.4.3.1.3.3-4: MeasurementReport (step 31, Table 13.4.3.1.3.2-2)` 行 254640-254670；Derivation path: 36.508, table 4.6.1-5
- `Table 13.4.3.1.3.3-5: MobilityFromEUTRACommand (step 32, Table 13.4.3.1.3.2-2)` 行 254672-254697；Derivation path: 36.508, Table 4.6.1-6
- `Table 13.4.3.1.3.3-6: HANDOVER TO UTRAN COMMAND (step 32, Table 13.4.3.1.3.3-5)` 行 254699-254700；Derivation path: 36.508, Table 4.7B.1-1, condition UTRA Speech
- `Table 13.4.3.1.3.3-7: UECapabilityEnquiry (step 31A, Table 13.4.3.1.3.2-2)` 行 254706-254722；Derivation path: 36.508 clause 4.6.1 table 4.6.1-22
- `Table 13.4.3.1.3.3-8: SECURITY MODE COMMAND (step 34, Table 13.4.3.1.3.2-2)` 行 254724-254727；Derivation path: 36.508, Table 4.7B.1-n
- `Table 13.4.3.1.3.3-9: Void` 行 254729-254729；Derivation path: 未在表块内以单行给出
- `Table 13.4.3.1.3.3-10: QuantityConfig-DEFAULT-RSCP (Table 13.4.3.1.3.3-3)` 行 254730-254737；Derivation path: 36.508, Table 4.6.6-3A
- `Table 13.4.3.1.3.3-11: ROUTING AREA UPDATE ACCEPT (step 2, Table 13.4.3.1.3.2-5)` 行 254739-254748；Derivation path: 36.508, Table 4.7B.2-2
- `Table 13.4.3.1.3.3-12: SECURITY MODE COMMAND (step 1A, Table 13.4.3.1.3.2-5)` 行 254751-254756；Derivation path: 36.508, Table 4.7B.1-n

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.4.3.1.3.3-0: Conditions for specific message contents

行 254563-254566

```text
254563 | Table 13.4.3.1.3.3-0: Conditions for specific message contents
254564 | in Table 13.4.3.1.3.3-3
254565 | Condition Explanation
254566 | Band > 64 If band > 64 is selected
```

##### Table 13.4.3.1.3.3-1: ATTACH REQUEST (preamble)

行 254568-254577

```text
254568 | Table 13.4.3.1.3.3-1: ATTACH REQUEST (preamble)
254569 | Derivation path: 36.508 table 4.7.2-4
254570 | Information Element Value/remark Comment Condition
254571 | MS network capability SRVCC from UTRAN
254572 | HSPA or E-UTRAN to
254573 | GERAN/UTRAN
254574 | supported
254576 | Mobile station classmark 2 Any allowed value
254577 | Supported Codecs Any allowed value
```

##### Table 13.4.3.1.3.3-2: RRCConnectionReconfiguration (step 28, Table 13.4.3.1.3.2-2)

行 254579-254580

```text
254579 | Table 13.4.3.1.3.3-2: RRCConnectionReconfiguration (step 28, Table 13.4.3.1.3.2-2)
254580 | Derivation Path: 36.508 clause 4.6.1 table 4.6.1-8 with condition MEAS
```

##### Table 13.4.3.1.3.3-3: MeasConfig (step 28, Table 13.4.3.1.3.2-2)

行 254586-254634

```text
254586 | Table 13.4.3.1.3.3-3: MeasConfig (step 28, Table 13.4.3.1.3.2-2)
254587 | Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition UTRAN
254588 | Information Element Value/Remark Comment Condition
254589 | measurementConfiguration ::= SEQUENCE {
254590 |   measObjectToAddModifyList SEQUENCE (SIZE
254591 | (1..maxObjectId)) OF SEQUENCE {
254592 | 2 entries
254593 |     measObjectId[1] IdMeasObject-f8
254594 |     measObject[1] MeasObjectUTRA-
254595 | GENERIC(f8)
254597 |     measObjectId[2] IdMeasObject-f1
254598 |     measObject[2] MeasObjectEUTRA-
254599 | GENERIC(f1)
254601 |     measObject[2] MeasObjectEUTRA-
254602 | GENERIC(maxEARFCN)
254603 |  Band > 64
254604 |   }
254605 |   reportConfigToAddModifyList SEQUENCE (SIZE
254606 | (1..maxReportConfigId)) OF SEQUENCE {
254607 | 1 entry
254608 |     reportConfigId[1] IdReportConfigInterRAT-
254609 | B2-UTRA
254611 |     reportConfig[1] ReportConfigInterRAT-
254612 | B2-UTRA (-72, -76)
254614 |   }
254615 |   measIdToAddModifyList SEQUENCE (SIZE
254616 | (1..maxMeasId)) OF SEQUENCE {
254617 | 1 entry
254618 |     measId[1] 1
254619 |     measObjectId[1] IdMeasObject-f8
254620 |     reportConfigId[1] IdReportConfigInterRAT-
254621 | B2-UTRA
254623 |   }
254624 |   measObjectToAddModList-v9e0  ::= SEQUENCE
254625 | (SIZE (1..maxObjectId)) OF SEQUENCE {
254626 |   Band > 64
254627 |     measObjectEUTRA-v9e0[1] SEQUENCE {}
254628 |     measObjectEUTRA-v9e0[2] SEQUENCE {
254629 |     carrierFreq-v9e0 Same downlink EARFCN
254630 | as used for f1
254632 |     }
254633 |   }
254634 |  }
```

##### Table 13.4.3.1.3.3-4: MeasurementReport (step 31, Table 13.4.3.1.3.2-2)

行 254640-254670

```text
254640 | Table 13.4.3.1.3.3-4: MeasurementReport (step 31, Table 13.4.3.1.3.2-2)
254641 | Derivation Path: 36.508, table 4.6.1-5
254642 | Information Element Value/remark Comment Condition
254643 | MeasurementReport ::= SEQUENCE {
254644 |   criticalExtensions CHOICE {
254645 |     c1 CHOICE{
254646 |       measurementReport-r8 SEQUENCE {
254647 |         measResults SEQUENCE {
254648 |           measId 1
254649 |           measResultServCell SEQUENCE {
254650 |             rsrpResult (0..97)
254651 |             rsrqResult (0..34)
254652 |           }
254653 |           measResultNeighCells CHOICE {
254654 |             measResultListUTRA SEQUENCE (SIZE
254655 | (1..maxCellReport)) OF SEQUENCE {
254656 | 1 entry
254657 |               physCellId[1] PhysicalCellIdentity of
254658 | Cell 5
254660 |               cgi-Info[1] Not present
254661 |               measResult[1] SEQUENCE {
254662 |                 utra-RSCP (-5..91)
254663 |               }
254664 |             }
254665 |           }
254666 |         }
254667 |       }
254668 |     }
254669 |   }
254670 | }
```

##### Table 13.4.3.1.3.3-5: MobilityFromEUTRACommand (step 32, Table 13.4.3.1.3.2-2)

行 254672-254697

```text
254672 | Table 13.4.3.1.3.3-5: MobilityFromEUTRACommand (step 32, Table 13.4.3.1.3.2-2)
254673 | Derivation Path: 36.508, Table 4.6.1-6
254674 | Information Element Value/remark Comment Condition
254675 | MobilityFromEUTRACommand ::= SEQUENCE {
254676 |   criticalExtensions CHOICE {
254677 |     c1 CHOICE{
254678 |       mobilityFromEUTRACommand-r8 SEQUENCE {
254679 |         cs-FallbackIndicator False
254680 |         purpose CHOICE{
254681 |           handover SEQUENCE {
254682 |             targetRAT-Type Utra
254683 |             targetRAT-MessageContainer HANDOVER TO UTRAN
254684 | COMMAND(UTRA RRC
254685 | message)
254687 |             nas-SecurityParamFromEUTRA The 4 least significant
254688 | bits of the NAS downlink
254689 | COUNT value
254691 |             systemInformation Not present
254692 |           }
254693 |         }
254694 |       }
254695 |     }
254696 |   }
254697 | }
```

##### Table 13.4.3.1.3.3-6: HANDOVER TO UTRAN COMMAND (step 32, Table 13.4.3.1.3.3-5)

行 254699-254700

```text
254699 | Table 13.4.3.1.3.3-6: HANDOVER TO UTRAN COMMAND (step 32, Table 13.4.3.1.3.3-5)
254700 | Derivation Path: 36.508, Table 4.7B.1-1, condition UTRA Speech
```

##### Table 13.4.3.1.3.3-7: UECapabilityEnquiry (step 31A, Table 13.4.3.1.3.2-2)

行 254706-254722

```text
254706 | Table 13.4.3.1.3.3-7: UECapabilityEnquiry (step 31A, Table 13.4.3.1.3.2-2)
254707 | Derivation path: 36.508 clause 4.6.1 table 4.6.1-22
254708 | Information Element Value/Remark Comment Condition
254709 | UECapabilityEnquiry ::= SEQUENCE {
254710 |   criticalExtensions CHOICE {
254711 |     c1 CHOICE {
254712 |       ueCapabilityEnquiry-r8 SEQUENCE {
254713 |         ue-CapabilityRequest SEQUENCE (SIZE
254714 | (1..maxRAT-Capabilities)) OF SEQUENCE {
254715 | 2 entry
254716 |           RAT-Type[1] eutra
254717 |           RAT-Type[2] utra
254718 |         }
254719 |       }
254720 |     }
254721 |   }
254722 | }
```

##### Table 13.4.3.1.3.3-8: SECURITY MODE COMMAND (step 34, Table 13.4.3.1.3.2-2)

行 254724-254727

```text
254724 | Table 13.4.3.1.3.3-8: SECURITY MODE COMMAND (step 34, Table 13.4.3.1.3.2-2)
254725 | Derivation Path: 36.508, Table 4.7B.1-n
254726 | Information Element Condition Value/remark
254727 | Ciphering mode info  Not Present
```

##### Table 13.4.3.1.3.3-9: Void

行 254729-254729

```text
254729 | Table 13.4.3.1.3.3-9: Void
```

##### Table 13.4.3.1.3.3-10: QuantityConfig-DEFAULT-RSCP (Table 13.4.3.1.3.3-3)

行 254730-254737

```text
254730 | Table 13.4.3.1.3.3-10: QuantityConfig-DEFAULT-RSCP (Table 13.4.3.1.3.3-3)
254731 | Derivation Path: 36.508, Table 4.6.6-3A
254732 | Information Element Value/remark Comment Condition
254733 |   quantityConfigUTRA SEQUENCE {
254734 |     measQuantityUTRA-FDD cpich-RSCP
254735 |     measQuantityUTRA-TDD pccpch-RSCP
254736 |     filterCoefficient Not present DEFAULT fc4
254737 |   }
```

##### Table 13.4.3.1.3.3-11: ROUTING AREA UPDATE ACCEPT (step 2, Table 13.4.3.1.3.2-5)

行 254739-254748

```text
254739 | Table 13.4.3.1.3.3-11: ROUTING AREA UPDATE ACCEPT (step 2, Table 13.4.3.1.3.2-5)
254740 | Derivation path: 36.508, Table 4.7B.2-2
254741 | Information Element Value/Remark Comment Condition
254742 | PDP context status 0 NSAPI(0) -
254743 | NSAPI(15) is set
254744 | to 0, which means
254745 | that the SM state
254746 | of all PDP
254747 | contexts is PDP-
254748 | INACTIVE
```

##### Table 13.4.3.1.3.3-12: SECURITY MODE COMMAND (step 1A, Table 13.4.3.1.3.2-5)

行 254751-254756

```text
254751 | Table 13.4.3.1.3.3-12: SECURITY MODE COMMAND (step 1A, Table 13.4.3.1.3.2-5)
254752 | Derivation Path: 36.508, Table 4.7B.1-n
254753 | Information Element Condition Value/remark
254754 | Ciphering mode info  StartRestart
254755 | Integrity protection mode info  modify
254756 | CN Domain Identity  ps-domain
```

**关键官方判据**

- 步骤 33：UE 在 UTRA Cell 5 发送 `HANDOVER TO UTRAN COMPLETE`，TP Verdict `1 P`（行 254490-254494）。
- 并行表 `Table 13.4.3.1.3.2-5`：UE 发送 `ROUTING AREA UPDATE REQUEST`，TP Verdict `P`（行 254537-254560）。

**Main behaviour 原文（逐行）**

```text
254445 | Table 13.4.3.1.3.2-2: Main behaviour
254446 | St Procedure Message Sequence TP Verdict
254447 |   U - S Message
254448 | 1 The SS configures UTRA cell 5 to reference
254449 | configuration according 36.508 table 4.8.3-1,
254450 | condition UTRA Speech.
254451 | - - - -
254452 | 2-25 Steps 1 to 24 of the generic test procedure  for
254453 | IMS MT speech call (TS 36.508 4.5A.7.3-1).
254454 | - - - -
254455 | 26-
254456 | 27
254457 | Void - - - -
254458 | 28 The SS transmits an
254459 | RRCConnectionReconfiguration message on
254460 | Cell 1 to setup inter RAT measurement and
254461 | reporting for event B2.
254462 | <-- RRCConnectionReconfiguration - -
254463 | 29 The UE transmits an
254464 | RRCConnectionReconfigurationComplete
254465 | message on Cell 1.
254466 | --> RRCConnectionReconfigurationC
254467 | omplete
254468 | - -
254469 | 30 The SS changes the power level for Cell 1 and
254470 | Cell 5 according to the row "T1" in table
254471 | 13.4.3.1.3.2-1
254472 | - - - -
254473 | 31 The UE transmits a MeasurementReport
254474 | message on Cell 1 to report event B2 for Cell
254475 | 5.
254476 | --> MeasurementReport - -
254477 | 31A The SS transmits a UECapabilityEnquiry
254478 | message to request UE radio access capability
254479 | information for E-UTRA and UTRA.
254480 | <-- UECapabilityEnquiry - -
254481 | 31B The UE transmits a UECapabilityInformation
254482 | message on Cell 1.
254483 | NOTE:  The start-CS values received, should
254484 | be used to configure ciphering on cell 5.
254485 | --> UECapabilityInformation - -
254486 | 32 The SS transmits a
254487 | MobilityFromEUTRACommand message on
254488 | Cell 1.
254489 | <-- MobilityFromEUTRACommand - -
254490 | 33 Check: Does the UE transmit a HANDOVER
254491 | TO UTRAN COMPLETE message on cell 5?
254492 | --> HANDOVER TO UTRAN
254493 | COMPLETE
254494 | 1 P
254495 | - EXCEPTION: In parallel to the events
254496 | described in step 34 to 39 the steps specified
254497 | in table 13.4.3.1.3.2-5 takes place.
254498 | - - - -
254499 | 34 The SS transmits a SECURITY MODE
254500 | COMMAND message for the CS domain.
254501 | <-- SECURITY MODE COMMAND - -
254502 | 35 The UE transmits a SECURITY MODE
254503 | COMPLETE message.
254504 | --> SECURITY MODE COMPLETE - -
254505 | 36 The SS transmits an UTRAN MOBILITY
254506 | INFORMATION message to notify CN
254507 | information.
254508 | <-- UTRAN MOBILITY
254509 | INFORMATION
254510 | - -
254511 | 37 The UE transmits an UTRAN MOBILITY
254512 | INFORMATION CONFIRM message.
254513 | --> UTRAN MOBILITY
254514 | INFORMATION CONFIRM
254515 | - -
254516 | 38 The SS transmits a TMSI REALLOCATION
254517 | COMMAND message.
254518 | <-- TMSI REALLOCATION
254519 | COMMAND
254520 | - -
254521 | 39 The UE transmits a TMSI REALLOCATION
254522 | COMPLETE message.
254523 | --> TMSI REALLOCATION
254524 | COMPLETE
254525 | - -
254526 | 40 SS adjusts cell levels according to row T2 of
254527 | table 13.4.3.1.3.2-1.
254528 | - - - -
254529 | - The UE is in end state UTRA CS call (U5). - - - -
```

**Table 13.4.3.1.3.2-5: Parallel behaviour 原文（逐行）**

```text
254537 | Table 13.4.3.1.3.2-5: Parallel behaviour
254538 | St Procedure Message Sequence TP Verdict
254539 |   U - S Message
254540 | 1 Check: Does the UE transmit a ROUTING
254541 | AREA UPDATE REQUEST message?
254542 | --> ROUTING AREA UPDATE
254543 | REQUEST
254544 | - P
254545 | 1A The SS transmits a SECURITY MODE
254546 | COMMAND message for the PS domain.
254547 | <-- SECURITY MODE COMMAND - -
254548 | 1B The UE transmits a SECURITY MODE
254549 | COMPLETE message.
254550 | --> SECURITY MODE COMPLETE - -
254551 | 2 The SS transmits a ROUTING AREA UPDATE
254552 | ACCEPT message.
254553 | <-- ROUTING AREA UPDATE
254554 | ACCEPT
254555 | - -
254556 | 3 The UE transmits a ROUTING AREA UPDATE
254557 | COMPLETE message.
254558 | --> ROUTING AREA UPDATE
254559 | COMPLETE
254560 | - -
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。

#### TC-026 / 13.4.3.2

- body 行 254762 / TP 行 254764 / Conformance 行 254773 / Test description 行 255032 / Pre-test 行 255033 / Test procedure 行 255041 / Main behaviour 行 255101-255185 / .3.3 行 255285

**官方表清单**

- `Table 13.4.3.2.3.2-1: Time instances of cell power level and parameter changes` 行 255046-255095
- `Table 13.4.3.2.3.2-2: Main behaviour` 行 255101-255185
- `Table 13.4.3.2.3.2-3: Void` 行 255191-255191
- `Table 13.4.3.2.3.2-4: Void` 行 255192-255192
- `Table 13.4.3.2.3.2-5: Parallel behaviour` 行 255193-255236
- `Table 13.4.3.2.3.2-6: Parallel behaviour` 行 255238-255279
- `Table 13.4.3.2.3.3-0: Conditions for specific message contents` 行 255286-255289；Derivation path: 未在表块内以单行给出
- `Table 13.4.3.2.3.3-1: ATTACH REQUEST (preamble)` 行 255291-255300；Derivation path: 36.508 table 4.7.2-4
- `Table 13.4.3.2.3.3-2: RRCConnectionReconfiguration (step 28, Table 13.4.3.2.3.2-2)` 行 255302-255303；Derivation path: 36.508 clause 4.6.1 table 4.6.1-8 with condition MEAS
- `Table 13.4.3.2.3.3-3: MeasConfig (step 28, Table 13.4.3.2.3.2-2)` 行 255305-255353；Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition UTRAN
- `Table 13.4.3.2.3.3-4: MeasurementReport (step 31, Table 13.4.3.2.3.2-2)` 行 255359-255389；Derivation path: 36.508, table 4.6.1-5
- `Table 13.4.3.2.3.3-5: MobilityFromEUTRACommand (step 32, Table 13.4.3.2.3.2-2)` 行 255391-255416；Derivation path: 36.508, Table 4.6.1-6
- `Table 13.4.3.2.3.3-6: HANDOVER TO UTRAN COMMAND (step 32, Table 13.4.3.2.3.3-5)` 行 255418-255420；Derivation path: 36.508, Table 4.7B.1-1, condition UTRA Speech + Packet RAB Setup after Speech RAB Setup in CELL_DCH
- `Table 13.4.3.2.3.3-7: UECapabilityEnquiry (step 32A, Table 13.4.3.2.3.2-2)` 行 255426-255442；Derivation path: 36.508 clause 4.6.1 table 4.6.1-22
- `Table 13.4.3.2.3.3-8: SECURITY MODE COMMAND (step 34, Table 13.4.3.2.3.2-2)` 行 255444-255447；Derivation path: 36.508, Table 4.7B.1-n
- `Table 13.4.3.2.3.3-9: Void` 行 255449-255449；Derivation path: 未在表块内以单行给出
- `Table 13.4.3.2.3.3-10: Void` 行 255450-255450；Derivation path: 未在表块内以单行给出
- `Table 13.4.3.2.3.3-11: ROUTING AREA UPDATE ACCEPT (step 2, Table 13.4.3.2.3.2-5)` 行 255451-255455；Derivation path: 36.508, Table 4.7B.2-2

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.4.3.2.3.3-0: Conditions for specific message contents

行 255286-255289

```text
255286 | Table 13.4.3.2.3.3-0: Conditions for specific message contents
255287 | in Table 13.4.3.2.3.3-3
255288 | Condition Explanation
255289 | Band > 64 If band > 64 is selected
```

##### Table 13.4.3.2.3.3-1: ATTACH REQUEST (preamble)

行 255291-255300

```text
255291 | Table 13.4.3.2.3.3-1: ATTACH REQUEST (preamble)
255292 | Derivation path: 36.508 table 4.7.2-4
255293 | Information Element Value/remark Comment Condition
255294 | MS network capability SRVCC from UTRAN
255295 | HSPA or E-UTRAN to
255296 | GERAN/UTRAN
255297 | supported
255299 | Mobile station classmark 2 Any allowed value
255300 | Supported Codecs Any allowed value
```

##### Table 13.4.3.2.3.3-2: RRCConnectionReconfiguration (step 28, Table 13.4.3.2.3.2-2)

行 255302-255303

```text
255302 | Table 13.4.3.2.3.3-2: RRCConnectionReconfiguration (step 28, Table 13.4.3.2.3.2-2)
255303 | Derivation Path: 36.508 clause 4.6.1 table 4.6.1-8 with condition MEAS
```

##### Table 13.4.3.2.3.3-3: MeasConfig (step 28, Table 13.4.3.2.3.2-2)

行 255305-255353

```text
255305 | Table 13.4.3.2.3.3-3: MeasConfig (step 28, Table 13.4.3.2.3.2-2)
255306 | Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition UTRAN
255307 | Information Element Value/Remark Comment Condition
255308 | measurementConfiguration ::= SEQUENCE {
255309 |   measObjectToAddModifyList SEQUENCE (SIZE
255310 | (1..maxObjectId)) OF SEQUENCE {
255311 | 2 entries
255312 |     measObjectId[1] IdMeasObject-f8
255313 |     measObject[1] MeasObjectUTRA-
255314 | GENERIC(f8)
255316 |     measObjectId[2] IdMeasObject-f1
255317 |     measObject[2] MeasObjectEUTRA-
255318 | GENERIC(f1)
255320 |     measObject[2] MeasObjectEUTRA-
255321 | GENERIC(maxEARFCN)
255322 |  Band > 64
255323 |   }
255324 |   reportConfigToAddModifyList SEQUENCE (SIZE
255325 | (1..maxReportConfigId)) OF SEQUENCE {
255326 | 1 entry
255327 |     reportConfigId[1] IdReportConfigInterRAT-
255328 | B2-UTRA
255330 |     reportConfig[1] ReportConfigInterRAT-
255331 | B2-UTRA (-72, -76)
255333 |   }
255334 |   measIdToAddModifyList SEQUENCE (SIZE
255335 | (1..maxMeasId)) OF SEQUENCE {
255336 | 1 entry
255337 |     measId[1] 1
255338 |     measObjectId[1] IdMeasObject-f8
255339 |     reportConfigId[1] IdReportConfigInterRAT-
255340 | B2-UTRA
255342 |   }
255343 |   measObjectToAddModList-v9e0  ::= SEQUENCE
255344 | (SIZE (1..maxObjectId)) OF SEQUENCE {
255345 |   Band > 64
255346 |     measObjectEUTRA-v9e0[1] SEQUENCE {}
255347 |     measObjectEUTRA-v9e0[2] SEQUENCE {
255348 |     carrierFreq-v9e0 Same downlink EARFCN
255349 | as used for f1
255351 |     }
255352 |   }
255353 | }
```

##### Table 13.4.3.2.3.3-4: MeasurementReport (step 31, Table 13.4.3.2.3.2-2)

行 255359-255389

```text
255359 | Table 13.4.3.2.3.3-4: MeasurementReport (step 31, Table 13.4.3.2.3.2-2)
255360 | Derivation Path: 36.508, table 4.6.1-5
255361 | Information Element Value/remark Comment Condition
255362 | MeasurementReport ::= SEQUENCE {
255363 |   criticalExtensions CHOICE {
255364 |     c1 CHOICE{
255365 |       measurementReport-r8 SEQUENCE {
255366 |         measResults SEQUENCE {
255367 |           measId 1
255368 |           measResultServCell SEQUENCE {
255369 |             rsrpResult (0..97)
255370 |             rsrqResult (0..34)
255371 |           }
255372 |           measResultNeighCells CHOICE {
255373 |             measResultListUTRA SEQUENCE (SIZE
255374 | (1..maxCellReport)) OF SEQUENCE {
255375 | 1 entry
255376 |               physCellId[1] PhysicalCellIdentity of
255377 | Cell 5
255379 |               cgi-Info[1] Not present
255380 |               measResult[1] SEQUENCE {
255381 |                 utra-RSCP (-5..91)
255382 |               }
255383 |             }
255384 |           }
255385 |         }
255386 |       }
255387 |     }
255388 |   }
255389 | }
```

##### Table 13.4.3.2.3.3-5: MobilityFromEUTRACommand (step 32, Table 13.4.3.2.3.2-2)

行 255391-255416

```text
255391 | Table 13.4.3.2.3.3-5: MobilityFromEUTRACommand (step 32, Table 13.4.3.2.3.2-2)
255392 | Derivation Path: 36.508, Table 4.6.1-6
255393 | Information Element Value/remark Comment Condition
255394 | MobilityFromEUTRACommand ::= SEQUENCE {
255395 |   criticalExtensions CHOICE {
255396 |     c1 CHOICE{
255397 |       mobilityFromEUTRACommand-r8 SEQUENCE {
255398 |         cs-FallbackIndicator False
255399 |         purpose CHOICE{
255400 |           handover SEQUENCE {
255401 |             targetRAT-Type Utra
255402 |             targetRAT-MessageContainer HANDOVER TO UTRAN
255403 | COMMAND(UTRA RRC
255404 | message)
255406 |             nas-SecurityParamFromEUTRA The 4 least significant
255407 | bits of the NAS downlink
255408 | COUNT value
255410 |             systemInformation Not present
255411 |           }
255412 |         }
255413 |       }
255414 |     }
255415 |   }
255416 | }
```

##### Table 13.4.3.2.3.3-6: HANDOVER TO UTRAN COMMAND (step 32, Table 13.4.3.2.3.3-5)

行 255418-255420

```text
255418 | Table 13.4.3.2.3.3-6: HANDOVER TO UTRAN COMMAND (step 32, Table 13.4.3.2.3.3-5)
255419 | Derivation Path: 36.508, Table 4.7B.1-1, condition UTRA Speech + Packet RAB Setup after Speech RAB Setup in
255420 | CELL_DCH
```

##### Table 13.4.3.2.3.3-7: UECapabilityEnquiry (step 32A, Table 13.4.3.2.3.2-2)

行 255426-255442

```text
255426 | Table 13.4.3.2.3.3-7: UECapabilityEnquiry (step 32A, Table 13.4.3.2.3.2-2)
255427 | Derivation path: 36.508 clause 4.6.1 table 4.6.1-22
255428 | Information Element Value/Remark Comment Condition
255429 | UECapabilityEnquiry ::= SEQUENCE {
255430 |   criticalExtensions CHOICE {
255431 |     c1 CHOICE {
255432 |       ueCapabilityEnquiry-r8 SEQUENCE {
255433 |         ue-CapabilityRequest SEQUENCE (SIZE
255434 | (1..maxRAT-Capabilities)) OF SEQUENCE {
255435 | 2 entry
255436 |           RAT-Type[1] eutra
255437 |           RAT-Type[2] utra
255438 |         }
255439 |       }
255440 |     }
255441 |   }
255442 | }
```

##### Table 13.4.3.2.3.3-8: SECURITY MODE COMMAND (step 34, Table 13.4.3.2.3.2-2)

行 255444-255447

```text
255444 | Table 13.4.3.2.3.3-8: SECURITY MODE COMMAND (step 34, Table 13.4.3.2.3.2-2)
255445 | Derivation Path: 36.508, Table 4.7B.1-n
255446 | Information Element Condition Value/remark
255447 | Ciphering mode info  Not Present
```

##### Table 13.4.3.2.3.3-9: Void

行 255449-255449

```text
255449 | Table 13.4.3.2.3.3-9: Void
```

##### Table 13.4.3.2.3.3-10: Void

行 255450-255450

```text
255450 | Table 13.4.3.2.3.3-10: Void
```

##### Table 13.4.3.2.3.3-11: ROUTING AREA UPDATE ACCEPT (step 2, Table 13.4.3.2.3.2-5)

行 255451-255455

```text
255451 | Table 13.4.3.2.3.3-11: ROUTING AREA UPDATE ACCEPT (step 2, Table 13.4.3.2.3.2-5)
255452 | Derivation path: 36.508, Table 4.7B.2-2
255453 | Information Element Value/Remark Comment Condition
255454 | Update result 0 ‘ follow-on proceed’
255455 | PDP context status ‘0010000000000000’B NSAPI 5
```

**关键官方判据**

- 步骤 33：UE 在 UTRA Cell 5 发送 `HANDOVER TO UTRAN COMPLETE`，TP Verdict `1 P`（行 255146-255150）。
- 并行表 `Table 13.4.3.2.3.2-5/6`：PS 域 RAU，后续可选 IMS/媒体释放或 de-registration（行 255193-255279）。

**Main behaviour 原文（逐行）**

```text
255101 | Table 13.4.3.2.3.2-2: Main behaviour
255102 | St Procedure Message Sequence TP Verdict
255103 |   U - S Message
255104 | 1 The SS configures UTRA cell 5 to reference
255105 | configuration according TS 36.508 Table 4.8.3-
255106 | 1, condition UTRA PS RB + Speech.
255107 | - - - -
255108 | 2-25 Steps 1 to 24 of the generic test procedure for
255109 | IMS MT speech call (TS 36.508, 4.5A.7.3-1).
255110 | - - - -
255111 | 26-
255112 | 27
255113 | Void
255114 | 28 The SS transmits an
255115 | RRCConnectionReconfiguration message on
255116 | Cell 1 to setup inter RAT measurement and
255117 | reporting for event B2.
255118 | <-- RRCConnectionReconfiguration - -
255119 | 29 The UE transmits an
255120 | RRCConnectionReconfigurationComplete
255121 | message on Cell 1.
255122 | --> RRCConnectionReconfigurationC
255123 | omplete
255124 | - -
255125 | 30 The SS changes the power level for Cell 1 and
255126 | Cell 5 according to the row "T1" in table
255127 | 13.4.3.2.3.2-1
255128 | - - - -
255129 | 31 The UE transmits a MeasurementReport
255130 | message on Cell 1 to report event B2 for Cell
255131 | 5.
255132 | --> MeasurementReport - -
255133 | 32 The SS transmits a
255134 | MobilityFromEUTRACommand message on
255135 | Cell 1.
255136 | <-- MobilityFromEUTRACommand - -
255137 | 32A The SS transmits a UECapabilityEnquiry
255138 | message to request UE radio access capability
255139 | information for E-UTRA and UTRA.
255140 | <-- UECapabilityEnquiry - -
255141 | 32B The UE transmits a UECapabilityInformation
255142 | message on Cell 1.
255143 | NOTE:  The start-CS values received, should
255144 | be used to configure ciphering on Cell 5.
255145 | --> UECapabilityInformation - -
255146 | 33 Check: Does the UE transmit a HANDOVER
255147 | TO UTRAN COMPLETE message on Cell 5?
255148 | --> HANDOVER TO UTRAN
255149 | COMPLETE
255150 | 1 P
255151 | - EXCEPTION: In parallel to the events
255152 | described in step 34 to 39 the steps specified
255153 | in Table 13.4.3.2.3.2-5 take place.
255154 | - - - -
255155 | 34 The SS transmits a SECURITY MODE
255156 | COMMAND message for the CS domain.
255157 | <-- SECURITY MODE COMMAND - -
255158 | 35 The UE transmits a SECURITY MODE
255159 | COMPLETE message.
255160 | --> SECURITY MODE COMPLETE - -
255161 | 36 The SS transmits an UTRAN MOBILITY
255162 | INFORMATION message to notify CN
255163 | information.
255164 | <-- UTRAN MOBILITY
255165 | INFORMATION
255166 | - -
255167 | 37 The UE transmits an UTRAN MOBILITY
255168 | INFORMATION CONFIRM message.
255169 | --> UTRAN MOBILITY
255170 | INFORMATION CONFIRM
255171 | - -
255172 | 38 The SS transmits a TMSI REALLOCATION
255173 | COMMAND message.
255174 | <-- TMSI REALLOCATION
255175 | COMMAND
255176 | - -
255177 | 39 The UE transmits a TMSI REALLOCATION
255178 | COMPLETE message.
255179 | --> TMSI REALLOCATION
255180 | COMPLETE
255181 | - -
255182 | 40 SS adjusts cell levels according to row T2 of
255183 | Table 13.4.3.2.3.2-1.
255184 | - - - -
255185 | - The UE is in end state UTRA CS call (U5). - - - -
```

**Table 13.4.3.2.3.2-5: Parallel behaviour 原文（逐行）**

```text
255193 | Table 13.4.3.2.3.2-5: Parallel behaviour
255194 | St Procedure Message Sequence TP Verdict
255195 |   U - S Message
255196 | - EXCEPTION: In parallel to the events
255197 | described in Step 1 to 3 the steps specified in
255198 | Table 13.4.3.2.3.2-6 take place.
255199 | - - - -
255200 | 1 Check: Does the UE transmit a ROUTING
255201 | AREA UPDATE REQUEST message?
255202 | --> ROUTING AREA UPDATE
255203 | REQUEST
255204 | - P
255205 | 1A The SS transmits a SECURITY MODE
255206 | COMMAND message for the PS domain.
255207 | <-- SECURITY MODE COMMAND - -
255208 | 1B The UE transmits a SECURITY MODE
255209 | COMPLETE message.
255210 | --> SECURITY MODE COMPLETE - -
255211 | 2 The SS transmits a ROUTING AREA UPDATE
255212 | ACCEPT message.
255213 | <-- ROUTING AREA UPDATE
255214 | ACCEPT
255215 | - -
255216 | 3 The UE transmits a ROUTING AREA UPDATE
255217 | COMPLETE message.
255218 | --> ROUTING AREA UPDATE
255219 | COMPLETE
255220 | - -
255221 | - EXCEPTION: Step 4a1-4a2 describe
255222 | behaviour that depends on the UE
255223 | implementation; the "lower case letter"
255224 | identifies a step sequence that take place if the
255225 | UE performs a certain action.
255226 | - - - -
255227 | 4a1 The UE transmits DEACTIVATE PDP
255228 | CONTEXT REQUEST message
255229 | --> DEACTIVATE PDP CONTEXT
255230 | REQUEST
255231 | - -
255232 | 4a2 The SS transmits DEACTIVATE PDP
255233 | CONTEXT ACCEPT message
255234 | <-- DEACTIVATE PDP CONTEXT
255235 | ACCEPT
255236 | - -
```

**Table 13.4.3.2.3.2-6: Parallel behaviour 原文（逐行）**

```text
255238 | Table 13.4.3.2.3.2-6: Parallel behaviour
255239 | St Procedure Message Sequence TP Verdict
255240 |   U – S Message
255241 | - EXCEPTION: Steps 7a1 – 7b1 describe
255242 | behaviour that depends on the UE
255243 | implementation; the "lower case letter"
255244 | identifies a step sequence that take place if the
255245 | UE performs a certain action.
255246 | - - - -
255247 | - EXCEPTION: Step 7a1a1 describe behaviour
255248 | that depends on the UE implementation; the
255249 | "lower case letter" identifies a step sequence
255250 | that take place if the UE performs a certain
255251 | action.
255252 | - - - -
255253 | 1-4 Void - - - -
255254 | 1A
255255 | a1-
255256 | 1A
255257 | a4
255258 | Void - - - -
255259 | 5-6 Void - - - -
255260 | 7a1
255261 | a1
255262 | IF the UE wants to remove SRVCC media in
255263 | the next 10 sec THEN the generic procedure
255264 | defined in Annex C.24 of TS 34.229-1 [35]
255265 | take place.
255266 | - - - -
255267 | 7a2 Generic procedure defined in Annex C.36 of
255268 | TS 34.229-1 [35]. IMS session release.
255269 | - - - -
255270 | 7a3 Depending on the UE implementation, the
255271 | generic test procedure for mobile initiated IMS
255272 | SIP de-registration defined in Annex C.30 of
255273 | TS 34.229-1 [35] take place.
255274 | - - - -
255275 | 7b1 Depending on the UE implementation, the
255276 | generic test procedure for mobile initiated IMS
255277 | SIP de-registration defined in Annex C.30 of
255278 | TS 34.229-1 [35] take place.
255279 | - - - -
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。

#### TC-026 / 13.4.3.3

- body 行 255457 / TP 行 255458 / Conformance 行 255467 / Test description 行 255642 / Pre-test 行 255643 / Test procedure 行 255655 / Main behaviour 行 255687-255740 / .3.3 行 255747

**官方表清单**

- `Table 13.4.3.3.3.2-1: Time instances of cell power level and parameter changes` 行 255660-255685
- `Table 13.4.3.3.3.2-2: Main behaviour` 行 255687-255740
- `Table 13.4.3.3.3.2-4: Void` 行 255746-255746
- `Table 13.4.3.3.3.3-1: ATTACH REQUEST (preamble)` 行 255748-255757；Derivation path: 36.508 table 4.7.2-4
- `Table 13.4.3.3.3.3-2: RRCConnectionReconfiguration (step 27, Table 13.4.3.3.3.2-2)` 行 255759-255760；Derivation path: 36.508 clause 4.6.1 table 4.6.1-8 with condition MEAS
- `Table 13.4.3.3.3.3-3: MeasConfig (step 27, Table 13.4.3.3.3.2-2)` 行 255762-255813；Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition GERAN
- `Table 13.4.3.3.3.3-4: MeasurementReport (step 30, Table 13.4.3.3.3.2-2)` 行 255819-255852；Derivation path: 36.508, table 4.6.1-5
- `Table 13.4.3.3.3.3-5: MobilityFromEUTRACommand (step 31, Table 13.4.3.3.3.2-2)` 行 255858-255893；Derivation path: 36.508, Table 4.6.1-6
- `Table 13.4.3.3.3.3-6: HANDOVER COMMAND (step 31, Table 13.4.3.3.3.2-2)` 行 255899-255932；Derivation path: 51.010, Table 40.2.4.33
- `Table 13.4.3.3.3.3-7: ROUTING AREA UPDATE ACCEPT (step 48, Table 13.4.3.3.3.2-2)` 行 255935-255944；Derivation path: 36.508, Table 4.7B.2-2

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.4.3.3.3.3-1: ATTACH REQUEST (preamble)

行 255748-255757

```text
255748 | Table 13.4.3.3.3.3-1: ATTACH REQUEST (preamble)
255749 | Derivation path: 36.508 table 4.7.2-4
255750 | Information Element Value/remark Comment Condition
255751 | MS network capability SRVCC from UTRAN
255752 | HSPA or E-UTRAN to
255753 | GERAN/UTRAN
255754 | supported
255756 | Mobile station classmark 2 Any allowed value
255757 | Supported Codecs Any allowed value
```

##### Table 13.4.3.3.3.3-2: RRCConnectionReconfiguration (step 27, Table 13.4.3.3.3.2-2)

行 255759-255760

```text
255759 | Table 13.4.3.3.3.3-2: RRCConnectionReconfiguration (step 27, Table 13.4.3.3.3.2-2)
255760 | Derivation Path: 36.508 clause 4.6.1 table 4.6.1-8 with condition MEAS
```

##### Table 13.4.3.3.3.3-3: MeasConfig (step 27, Table 13.4.3.3.3.2-2)

行 255762-255813

```text
255762 | Table 13.4.3.3.3.3-3: MeasConfig (step 27, Table 13.4.3.3.3.2-2)
255763 | Derivation path: 36.508 clause 4.6.6 table 4.6.6-1 with condition GERAN
255764 | Information Element Value/Remark Comment Condition
255765 | measurementConfiguration ::= SEQUENCE {
255766 |   measObjectToAddModifyList SEQUENCE (SIZE
255767 | (1..maxObjectId)) OF SEQUENCE {
255768 | 2 entries
255769 |     measObjectId[1] IdMeasObject-f11
255770 |     measObject[1] MeasObjectGERAN-
255771 | GENERIC(f11)
255773 |     measObjectId[2] IdMeasObject-f1
255774 |     measObject[2] MeasObjectEUTRA-
255775 | GENERIC(f1)
255777 |     measObject[2] MeasObjectEUTRA-
255778 | GENERIC(maxEARFCN)
255779 |  Band > 64
255780 |   }
255781 |   reportConfigToAddModifyList SEQUENCE (SIZE
255782 | (1..maxReportConfigId)) OF SEQUENCE {
255783 | 1 entry
255784 |     reportConfigId[1] IdReportConfigInterRAT-
255785 | B2-GERAN
255787 |     reportConfig[1] ReportConfigInterRAT-
255788 | B2-GERAN (-69, -75)
255790 |   }
255791 |   measIdToAddModifyList SEQUENCE (SIZE
255792 | (1..maxMeasId)) OF SEQUENCE {
255793 | 1 entry
255794 |     measId[1] 1
255795 |     measObjectId[1] IdMeasObject-f11
255796 |     reportConfigId[1] IdReportConfigInterRAT-
255797 | B2-GERAN
255799 |   }
255800 |   measObjectToAddModList-v9e0  ::= SEQUENCE
255801 | (SIZE (1..maxObjectId)) OF {
255802 | 2 entries  Band > 64
255803 |     measObjectEUTRA-v9e0[1] ::= SEQUENCE {}
255804 |     measObjectEUTRA-v9e0[1] ::= SEQUENCE {
255805 |       carrierFreq-v9e0 Same downlink EARFCN
255806 | as used for f1
255808 |     }
255809 |   }
255810 | }
255812 | Condition Explanation
255813 | Band > 64 If band > 64 is selected
```

##### Table 13.4.3.3.3.3-4: MeasurementReport (step 30, Table 13.4.3.3.3.2-2)

行 255819-255852

```text
255819 | Table 13.4.3.3.3.3-4: MeasurementReport (step 30, Table 13.4.3.3.3.2-2)
255820 | Derivation Path: 36.508, table 4.6.1-5
255821 | Information Element Value/remark Comment Condition
255822 | MeasurementReport ::= SEQUENCE {
255823 |   criticalExtensions CHOICE {
255824 |     c1 CHOICE{
255825 |       measurementReport-r8 SEQUENCE {
255826 |         measResults SEQUENCE {
255827 |           measId 1
255828 |           measResultServCell SEQUENCE {
255829 |             rsrpResult (0..97)
255830 |             rsrqResult (0..34)
255831 |           }
255832 |           measResultNeighCells CHOICE {
255833 |             measResultListGERAN SEQUENCE (SIZE
255834 | (1..maxCellReport)) OF SEQUENCE {
255835 | 1 entry
255836 |               physCellId PhysicalCellIdentity of
255837 | Cell 24
255839 |               cgi-Info[1] Not present
255840 |               measResult[1] SEQUENCE {
255841 |                 rssi The value of rssi is
255842 | present but contents not
255843 | checked
255845 |               }
255846 |             }
255847 |           }
255848 |         }
255849 |       }
255850 |     }
255851 |   }
255852 | }
```

##### Table 13.4.3.3.3.3-5: MobilityFromEUTRACommand (step 31, Table 13.4.3.3.3.2-2)

行 255858-255893

```text
255858 | Table 13.4.3.3.3.3-5: MobilityFromEUTRACommand (step 31, Table 13.4.3.3.3.2-2)
255859 | Derivation Path: 36.508, Table 4.6.1-6
255860 | Information Element Value/remark Comment Condition
255861 | MobilityFromEUTRACommand ::= SEQUENCE {
255862 |   criticalExtensions CHOICE {
255863 |     c1 CHOICE{
255864 |       mobilityFromEUTRACommand-r8 SEQUENCE {
255865 |         cs-FallbackIndicator False
255866 |         purpose CHOICE{
255867 |           handover SEQUENCE {
255868 |             targetRAT-Type geran
255869 |             targetRAT-MessageContainer HANDOVER
255870 | COMMAND(GERAN
255871 | RRC message), see
255872 | Table 13.4.3.3.3.3-6
255874 |             nas-SecurityParamFromEUTRA The 4 least significant
255875 | bits of the NAS downlink
255876 | COUNT value
255878 |             systemInformation Not present
255879 |           }
255880 |         }
255881 |         nonCriticalExtension SEQUENCE {
255882 |           lateNonCriticalExtension Not present
255883 |           nonCriticalExtension SEQUENCE {
255884 |             bandIndicator Set according to the band
255885 | used for Cell 24
255887 |             nonCriticalExtension SEQUENCE {} Not present
255888 |           }
255889 |         }
255890 |       }
255891 |     }
255892 |   }
255893 | }
```

##### Table 13.4.3.3.3.3-6: HANDOVER COMMAND (step 31, Table 13.4.3.3.3.2-2)

行 255899-255932

```text
255899 | Table 13.4.3.3.3.3-6: HANDOVER COMMAND (step 31, Table 13.4.3.3.3.2-2)
255900 | Derivation Path: 51.010, Table 40.2.4.33
255901 | Information Element Value/remark Comment Condition
255902 | Cell Description
255903 |   Network Colour Code 1
255904 |   Base Station Colour Code 5
255905 |   BCCH Carrier Number The BCCH Carrier
255906 | ARFCN as per table in
255907 | clause 40.1.1 of 51.010-
255908 | 1.
255910 | Description of the First Channel, after time
255911 |  Channel Description
255912 |   Channel Type and TDMA offset TCH/F + ACCH’s
255913 |    Timeslot Number Chosen arbitrarily, but not
255914 | Zero.
255916 |    Training Sequence Code Same as the BCCH
255917 |    Hopping channel Single RF channel
255918 |    ARFCN The first ARFCN in the
255919 | cell allocation as per
255920 | table in clause 40.2.1.1.1
255921 | of 51.010-1
255923 | Cipher Mode Setting 1001xxxy See TS 44.018
255924 | §9.1.15.10
255926 | xxx -
255927 | px_GSM_CipherAl
255928 | g
255930 | y -
255931 | px_GSM_Cipherin
255932 | gOnOff
```

##### Table 13.4.3.3.3.3-7: ROUTING AREA UPDATE ACCEPT (step 48, Table 13.4.3.3.3.2-2)

行 255935-255944

```text
255935 | Table 13.4.3.3.3.3-7: ROUTING AREA UPDATE ACCEPT (step 48, Table 13.4.3.3.3.2-2)
255936 | Derivation path: 36.508, Table 4.7B.2-2
255937 | Information Element Value/Remark Comment Condition
255938 | PDP context status 0 NSAPI(0) -
255939 | NSAPI(15) is set
255940 | to 0, which means
255941 | that the SM state
255942 | of all PDP
255943 | contexts is PDP-
255944 | INACTIVE
```

**关键官方判据**

- 步骤 32：UE 在 GERAN Cell 24 发送 `HANDOVER COMPLETE`，TP Verdict `1 P`（行 255716-255718）。
- 步骤 33：`GPRS SUSPENSION REQUEST`；步骤 36-50 接 `36.508 6.4.3.8.1` steps 20-34（行 255719-255740）。

**Main behaviour 原文（逐行）**

```text
255687 | Table 13.4.3.3.3.2-2: Main behaviour
255688 | St Procedure Message Sequence TP Verdict
255689 |   U - S Message
255690 | 1-26 Steps 1 to 26 of the generic test procedure  for
255691 | IMS MT speech call (TS 36.508 4.5A.7.3-1).
255692 | - - - -
255693 | 27 The SS transmits an
255694 | RRCConnectionReconfiguration message on
255695 | Cell 1 to setup inter RAT measurement and
255696 | reporting for event B2.
255697 | <-- RRCConnectionReconfiguration - -
255698 | 28 The UE transmits an
255699 | RRCConnectionReconfigurationComplete
255700 | message on Cell 1.
255701 | --> RRCConnectionReconfigurationC
255702 | omplete
255703 | - -
255704 | 29 The SS changes the power level for Cell 1 and
255705 | Cell 5 according to the row "T1" in table
255706 | 13.4.3.3.3.2-1
255707 | - - - -
255708 | 30 The UE transmits a MeasurementReport
255709 | message on Cell 1 to report event B2 for Cell
255710 | 24.
255711 | --> MeasurementReport - -
255712 | 31 The SS transmits a
255713 | MobilityFromEUTRACommand message on
255714 | Cell 1.
255715 | <-- MobilityFromEUTRACommand - -
255716 | 32 Check: Does the UE transmit a HANDOVER
255717 | COMPLETE message on Cell 24?
255718 | --> HANDOVER COMPLETE 1 P
255719 | 33 The UE transmits a GPRS SUSPENSION
255720 | REQUEST message
255721 | --> GPRS SUSPENSION REQUEST - -
255722 | 34 The SS transmits a TMSI REALLOCATION
255723 | COMMAND message.
255724 | <-- TMSI REALLOCATION
255725 | COMMAND
255726 | - -
255727 | 35 The UE transmits a TMSI REALLOCATION
255728 | COMPLETE message.
255729 | --> TMSI REALLOCATION
255730 | COMPLETE
255731 | - -
255732 | 35A SS adjusts cell levels according to row T2 of
255733 | table 13.4.3.3.3.2-1.
255734 | - - - -
255735 | 36-
255736 | 50
255737 | Steps 20 to 34 of the generic test procedure
255738 | described in TS36.508 subclause 6.4.3.8.1 are
255739 | performed on Cell 24.
255740 | - - - -
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。


### 2.3 36.508 锚点（通用测试环境）

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/36508.txt`
- 36.508 `Table 4.5A.7.3-1: EUTRA/EPS signalling for IMS MT speech call` 行 17622
- 36.508 `Table 4.8.3-1: UTRA reference radio parameters and combinations` 行 35964
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.4 34.108 / 36.523-2 锚点

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/34108.txt`（TS 34.108 V14.2.0）
- UTRA/GERAN 测试系统配置入口：行 5246-5258，其中 `Configuration 6` 用于 interRAT E-UTRA-UTRA 测试，UTRA SIB scheduling 引用 `36.508 clause 4.4.4.2`；`Configuration 7` 用于 EUTRA-UTRA-GERAN 测试，引用 `36.508 clause 4.4.4.3`。
- 523 正文对 UTRA cell 功率表的 34.108 引用：SRVCC 13.4.3.1 附近行 260754（`TS 34.108 Table 6.1.4`）、aSRVCC 13.4.3.7/13.4.3.10 附近行 263774 与 265053（`TS 34.108 Table 6.1.4 / Table 6.1.9`）。
- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/3652302.txt`（TS 36.523-2 V14.3.0）
- 36.523-2 是 E-UTRA/EPC UE 一致性测试的 ICS proforma；正式送测应由 Annex A 判定能力/适用性（行 343-409 描述了 Table 4-1 的 Clause/ICS/IXIT 列含义）。当前不把 36.523-2 条目硬挂为 TC-026 的替代官方 ID。

## 3. 前置条件

- UE 支持 SRVCC，处于 E-UTRA RRC_CONNECTED，IMS 语音通话进行中。
- 存在可切换 UTRA/GSM 网络。

## 4. 验证流程

1. UE 收到 MobilityFromEUTRACommand（SRVCC 切换命令）。
2. UE 在目标 UTRA/GSM 小区完成接入。
3. 验证语音 RAB/CS 域建立及媒体连续。

## 5. TP Verdict 判据

- 切换命令处理正确，完成消息发送。
- 语音会话在切换后保持。
- 无掉话/错误回落。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED（官方判据已锚，未执行）。

## 7. 受限 / L2_REQUIRED

- 真实 eNB/EPC/UTRAN/GERAN/SS 或一致性仪表缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```

## 9. L1 测试骨架

- 阶段：`L1_SKELETON`，不代表 `PASS`，不判官方一致性。
- 待补真实环境依赖：真实 eNB/EPC + UTRA/GERAN CS voice + SS/一致性仪表。
- 本骨架作用：预留 L1 可执行入口，先保证套件文档包含官方 TP 原文要点、待注入消息、预期行为和环境依赖。
- L1 runner：`python work/l1_skeleton_026_031.py`
- 判定规则：脚本只检查文档/骨架存在性和环境缺口登记，不输出一致性 Verdict。
