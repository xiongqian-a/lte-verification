# TC-028 SSAC 接入控制

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`13.5.1 / 13.5.1a`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 ID 已锚定；真实 SIB2 SSAC 注入/RRC 行为观测缺失。

## 1. 目的 / 为什么

验证 UE 收到 ssac-BarringForMMTEL-Voice-r9=0% 等 SSAC 配置后，在 back-off timer 内不建立 RRC 连接发起 MTSI MO 语音。

## 2. 官方骨架

- 正文行锚（36.523-1 正文/TP，2026-09-11 重新核对）：
  - 13.5.1 body 行 275624 / TP 行 275626 / .3.2 行 275716 / Main behaviour 行 275717
  - 13.5.1a body 行 275778 / TP 行 275780 / .3.2 行 275880 / Main behaviour 行 275881








- 官方 ID：36.523-1 13.5.1（RRC_IDLE） / 13.5.1a（Connected）
- 来源：`523-1v14.pdf`；映射见 `74-` 表
- 关联：TS 36.331 SIB2 SSAC IE；TS 24.301/24.229 对 MTSI MO 语音触发


### 2.1 官方 TP 原文要点

- 13.5.1.1 TP（Idle）：UE 在 RRC_IDLE 收到 SIB2 含 ssac-BarringForMMTEL-Voice-r9=0% accessibility；用户发起 MTSI MO voice call 时，UE 不建立 RRC connection。
- 13.5.1.1 TP（Ty 期）：同样 0% barring 且带 back-off Ty，用户之前已失败一次；Ty 运行期间再次发起 MTSI MO voice call，UE 仍不建立 RRC connection。
- 13.5.1a.1 TP（Connected）：UE 在 RRC_CONNECTED 收到 SIB2 含 0% SSAC；用户发起 MTSI MO voice call 时，UE 不发起 MTSI MO voice call；Ty 运行期间即使 barring 移除也不发起。

已抽取 .1 TP 原文；SIB2/SSAC IE 和 Ty 行为需要真实 RRC/SIB2 注入或一致性仪表。

### 2.2 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-026-031-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 源规范：ETSI TS 136 523-1 V14.3.0 (2018-02)。
- 行号方法：将 CRLF/CR 归一化后按 LF 切分；form-feed 页分隔符不另计一行。
- 覆盖官方小节：13.5.1、13.5.1a
- 说明：以下保留 `.3.2` 原文行号和 `.3.3` 表来源；`P/F` 是官方 TP Verdict 文本，不代表本地已得到一致性 Verdict。
- 正式结论仍必须由 R&S / Anritsu / Keysight 或检测机构按官方 SS 流程执行。

#### TC-028 / 13.5.1

- body 行 275624 / TP 行 275626 / Conformance 行 275644 / Test description 行 275704 / Pre-test 行 275705 / Test procedure 行 275716 / Main behaviour 行 275717-275752 / .3.3 行 275754

**官方表清单**

- `Table 13.5.1.3.2-1: Main behaviour` 行 275717-275752
- `Table 13.5.1.3.3-1: SystemInformationBlockType2 for Cell 1 (preamble and step 1, Table 13.5.1.3.2-1)` 行 275755-275764；Derivation path: 36.508, Table 4.4.3.3-1
- `Table 13.5.1.3.3-2: Paging (step3, Table 13.5.1.3.2-1)` 行 275766-275772；Derivation path: 36.508 Table 4.6.1-7

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.5.1.3.3-1: SystemInformationBlockType2 for Cell 1 (preamble and step 1, Table 13.5.1.3.2-1)

行 275755-275764

```text
275755 | Table 13.5.1.3.3-1: SystemInformationBlockType2 for Cell 1 (preamble and step 1, Table 13.5.1.3.2-1)
275756 | Derivation Path: 36.508, Table 4.4.3.3-1
275757 | Information Element Value/remark Comment Condition
275758 | SystemInformationBlockType2 ::= SEQUENCE {
275759 |   ssac-BarringForMMTEL-Voice-r9 SEQUENCE {
275760 |     ac-BarringFactor p00
275761 |     ac-BarringTime s64
275762 |     ac-BarringForSpecialAC '11111'B
275763 |   }
275764 | }
```

##### Table 13.5.1.3.3-2: Paging (step3, Table 13.5.1.3.2-1)

行 275766-275772

```text
275766 | Table 13.5.1.3.3-2: Paging (step3, Table 13.5.1.3.2-1)
275767 | Derivation Path: 36.508 Table 4.6.1-7
275768 | Information Element Value/remark Comment Condition
275769 | Paging ::= SEQUENCE {
275770 |   pagingRecordList Not present
275771 |   systemInfoModification TRUE
275772 | }
```

**关键官方判据**

- 步骤 2：UE 在 10 s 内不应发送 `RRCConnectionRequest`，TP Verdict `1 F`（行 275721-275724）。
- 步骤 6：更新 SIB2 后 10 s 内仍不应发送 `RRCConnectionRequest`，TP Verdict `2 F`；步骤 7 等待 Ty（行 275735-275752）。

**Main behaviour 原文（逐行）**

```text
275717 | Table 13.5.1.3.2-1: Main behaviour
275718 | St Procedure Message Sequence TP Verdict
275719 |   U - S Message
275720 | 1 Make the UE attempt an MTSI MO Speech call - - - -
275721 | 2 Check: Does the UE transmit a
275722 | RRCConnectionRequest message  within 10
275723 | s?.
275724 | --> RRCConnectionRequest 1 F
275725 | 3 SS changes SIB2 according to TS 36.508,
275726 | table 4.4.3.3-1 and transmits a Paging
275727 | message including systemInfoModification.
275728 | The systemInfoValueTag in the
275729 | SystemInformationBlockType1 is increased.
275730 | <-- Paging - -
275731 | 4 Wait for 15 s (Note 1) to allow the new system
275732 | information to take effect.
275733 | - - - -
275734 | 5 Make the UE attempt an MTSI MO Speech call - - - -
275735 | 6 Check: Does the UE transmit an
275736 | RRCConnectionRequest message with in 10s?
275737 | --> RRCConnectionRequest 2 F
275738 | 7 Wait for 49 s (Note 2) to make the timer Ty
275739 | expire.
275740 |   - -
275741 | 8-
275742 | 21
275743 | Steps 1 to 14 of the generic test procedure for
275744 | MTSI MO Speech call establishment in
275745 | EUTRA: Normal Service (TS 36.508 4.5A.6.3-
275746 | 1).
275747 | - - - -
275748 | Note 1: The wait time of 15 s in step 3 is to allow for the network to page the system information change during the
275749 | next modification period, and update the system information at the subsequent modification period. UE
275750 | should acquire the updated system information within 100ms of the start of modification period.
275751 | Note 2: The UE starts timer Ty in step2. Maximum time of timer Ty is 83.2 sec ((0.7 + 0.6 * 1) * s64). At the end of
275752 | step 7, 35 sec elapses from step 2. Therefore 49 sec (84s - 35s) is enough to wait timer Ty expiry.
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。

#### TC-028 / 13.5.1a

- body 行 275778 / TP 行 275780 / Conformance 行 275808 / Test description 行 275871 / Pre-test 行 275872 / Test procedure 行 275880 / Main behaviour 行 275881-275931 / .3.3 行 275937

**官方表清单**

- `Table 13.5.1a.3.2-1: Main behaviour` 行 275881-275931
- `Table 13.5.1a.3.3-1: SystemInformationBlockType2 for Cell 1 (preamble,)` 行 275938-275947；Derivation path: 36.508, Table 4.4.3.3-1
- `Table 13.5.1a.3.3-2: Void` 行 275949-275949；Derivation path: 未在表块内以单行给出

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.5.1a.3.3-1: SystemInformationBlockType2 for Cell 1 (preamble,)

行 275938-275947

```text
275938 | Table 13.5.1a.3.3-1: SystemInformationBlockType2 for Cell 1 (preamble,)
275939 | Derivation Path: 36.508, Table 4.4.3.3-1
275940 | Information Element Value/remark Comment Condition
275941 | SystemInformationBlockType2 ::= SEQUENCE {
275942 |   ssac-BarringForMMTEL-Voice-r9 SEQUENCE {
275943 |     ac-BarringFactor p00
275944 |     ac-BarringTime s64
275945 |     ac-BarringForSpecialAC '11111'B
275946 |   }
275947 | }
```

##### Table 13.5.1a.3.3-2: Void

行 275949-275949

```text
275949 | Table 13.5.1a.3.3-2: Void
```

**关键官方判据**

- 步骤 6：UE 不应发送 `INVITE`，TP Verdict `1 F`（行 275886-275888）。
- 步骤 6B：Ty 运行期间 UE 仍不应发送 `INVITE`，TP Verdict `2 F`；步骤 9 Ty 到期后应发送 `INVITE`，TP Verdict `3 P`（行 275903-275913）。
- SIB2：`ssac-BarringForMMTEL-Voice-r9`、`ac-BarringFactor p00`、`ac-BarringTime s64`、`ac-BarringForSpecialAC '11111'B`（行 275938-275947）。

**Main behaviour 原文（逐行）**

```text
275881 | Table 13.5.1a.3.2-1: Main behaviour
275882 | St Procedure Message Sequence TP Verdict
275883 |   U - S Message
275884 | 1-4 Void - - - -
275885 | 5 Make the UE attempt a MTSI MO Speech call - - - -
275886 | 6 Check: Does the UE transmit an INVITE
275887 | message with in 10s?
275888 | --> INVITE 1 F
275889 | 6A
275890 | A
275891 | SS changes SIB2 according to TS 36.508,
275892 | table 4.4.3.3-1 and transmits a Paging
275893 | message including systemInfoModification.
275894 | The systemInfoValueTag in the
275895 | SystemInformationBlockType1 is increased.
275896 | <-- Paging - -
275897 | 6A
275898 | B
275899 | Wait for 15 s (Note 1) to allow the new system
275900 | information to take effect.
275901 | - - - -
275902 | 6A Make the UE attempt a MTSI MO Speech call - - - -
275903 | 6B Check: Does the UE transmit an INVITE
275904 | message during back-off timer Ty is running
275905 | and within 10s?
275906 | --> INVITE 2 F
275907 | 7 Wait for 49 s (Note 2) to make the timer Ty
275908 | expire.
275910 | 8 Make the UE attempt a MTSI MO Speech call
275911 | 9 Check: Does the UE transmit an INVITE
275912 | message within 10 s?
275913 | /barb2right  INVITE 3 P
275914 | 10-
275915 | 12
275916 | Steps 3 to 4 of the generic procedure for MTSI
275917 | MO speech call establishment (TS 34.229-1
275918 | C.21)
275920 | 13-
275921 | 15
275922 | Steps 12 to 14 of the generic procedure for
275923 | MTSI MO speech call establishment (TS
275924 | 36.508 table 4.5A.6.3-1).
275926 | Note 1: The wait time of 15 s in step 3 is to allow for the network to page the system information change during the
275927 | next modification period, and update the system information at the subsequent modification period. UE
275928 | should acquire the updated system information within 100ms of the start of modification period.
275929 | Note 2: The UE starts timer Ty in step 6. Maximum time of timer Ty is 83.2 sec ((0.7 + 0.6 * 1) * s64). At the end of
275930 | step 6B, 20 sec elapses from the beginning of step 6. Therefore 64 sec (84s - 20s) is enough to wait timer
275931 | Ty expiry.
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。


### 2.3 36.508 锚点（通用测试环境）

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/36508.txt`
- 36.508 `Table 4.5A.6.3-1: EUTRA/EPS signalling for IMS MO speech call` 行 17476
- 36.508 `Table 4.4.3.3-1: SystemInformationBlockType2` 行 10026
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

## 3. 前置条件

- UE 支持 SSAC。
- eNB 可按 0% access probability 配置 SIB2。

## 4. 验证流程

1. eNB 下发 SIB2，SSAC 0%。
2. 用户发起 MTSI MO 语音。
3. UE 因 SSAC 不建立 RRC 连接；back-off timer Ty 运行期间继续禁止。

## 5. TP Verdict 判据

- UE 不建 RRC 连接。
- 无非法接入。
- Ty 到期后行为符合后续触发。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED。

## 7. 受限 / L2_REQUIRED

- 真实 SIB2 SSAC/RRC 行为观测缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```

## 9. L1 测试骨架

- 阶段：`L1_SKELETON`，不代表 `PASS`，不判官方一致性。
- 待补真实环境依赖：SIB2 ssac-BarringForMMTEL-Voice-r9=0% + back-off Ty + 真实 RRC/eNB。
- 本骨架作用：预留 L1 可执行入口，先保证套件文档包含官方 TP 原文要点、待注入消息、预期行为和环境依赖。
- L1 runner：`python work/l1_skeleton_026_031.py`
- 判定规则：脚本只检查文档/骨架存在性和环境缺口登记，不输出一致性 Verdict。
