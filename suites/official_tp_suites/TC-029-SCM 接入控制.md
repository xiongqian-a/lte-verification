# TC-029 SCM 接入控制

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`13.5.4`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 ID 已锚定；真实 SIB2 SCM skip/RRC 行为观测缺失。

## 1. 目的 / 为什么

验证 UE 收到 ac-BarringForMO-data=0% 与 ac-BarringSkipForMMTELVoice-r12 时，可跳过通用接入阻塞并发起 MTSI MO 语音。

## 2. 官方骨架

- 正文行锚（36.523-1 正文/TP，2026-09-11 重新核对）：
  - 13.5.4 body 行 276534 / TP 行 276536 / .3.2 行 276827 / Main behaviour 行 276828








- 官方 ID：36.523-1 13.5.4
- 来源：`523-1v14.pdf`；映射见 `74-` 表
- 关联：TS 36.331 SIB2 access barring skip IE；TS 24.229 MTSI 触发


### 2.1 官方 TP 原文要点

- 13.5.4.1 TP：UE 在 RRC_IDLE 收到 SIB2 含 ac-BarringForMO-data=0% accessibility 且含 ac-BarringSkipForMMTELVoice-r12；用户发起 MTSI MO voice call 时，UE 建立 RRC connection 并建立 MTSI voice call。

已抽取 .1 TP 原文；需要真实 SIB2 注入（MO-data blocked + MMTEL Voice skip）或一致性仪表。

### 2.2 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-026-031-3.2-main-behaviour.md`
- 源文本：`<legacy-workspace>\523-1v14.txt`
- 源规范：ETSI TS 136 523-1 V14.3.0 (2018-02)。
- 行号方法：将 CRLF/CR 归一化后按 LF 切分；form-feed 页分隔符不另计一行。
- 覆盖官方小节：13.5.4
- 说明：以下保留 `.3.2` 原文行号和 `.3.3` 表来源；`P/F` 是官方 TP Verdict 文本，不代表本地已得到一致性 Verdict。
- 正式结论仍必须由 R&S / Anritsu / Keysight 或检测机构按官方 SS 流程执行。

#### TC-029 / 13.5.4

- body 行 276534 / TP 行 276536 / Conformance 行 276547 / Test description 行 276815 / Pre-test 行 276816 / Test procedure 行 276827 / Main behaviour 行 276828-276861 / .3.3 行 276863

**官方表清单**

- `Table 13.5.4.3.2-1: Main behaviour` 行 276828-276861
- `Table 13.5.4.3.3-1: SystemInformationBlockType2 (preamble, Table 13.5.4.3.2-1)` 行 276864-276873；Derivation path: 36.508, Table 4.4.3.3-1
- `Table 13.5.4.3.3-2: SystemInformationBlockType2 for Cell 1 (step 3, Table 13.5.4.3.2-1)` 行 276875-276888；Derivation path: 36.508, Table 4.4.3.3-1

**`.3.3` Specific message contents 原文（逐行）**

##### Table 13.5.4.3.3-1: SystemInformationBlockType2 (preamble, Table 13.5.4.3.2-1)

行 276864-276873

```text
276864 | Table 13.5.4.3.3-1: SystemInformationBlockType2 (preamble, Table 13.5.4.3.2-1)
276865 | Derivation Path: 36.508, Table 4.4.3.3-1
276866 | Information Element Value/remark Comment Condition
276867 | SystemInformationBlockType2 ::= SEQUENCE {
276868 |   ac-BarringInfo SEQUENCE {
276869 |     ac-BarringForEmergency FALSE
276870 |     ac-BarringForMO-Signalling Not present
276871 |     ac-BarringForMO-Data  Not present
276872 |   }
276873 | }
```

##### Table 13.5.4.3.3-2: SystemInformationBlockType2 for Cell 1 (step 3, Table 13.5.4.3.2-1)

行 276875-276888

```text
276875 | Table 13.5.4.3.3-2: SystemInformationBlockType2 for Cell 1 (step 3, Table 13.5.4.3.2-1)
276876 | Derivation Path: 36.508, Table 4.4.3.3-1
276877 | Information Element Value/remark Comment Condition
276878 | SystemInformationBlockType2 ::= SEQUENCE {
276879 |   ac-BarringInfo SEQUENCE {
276880 |     ac-BarringForEmergency FALSE
276881 |     ac-BarringForMO-Data SEQUENCE {
276882 |       ac-BarringFactor p0
276883 |       ac-BarringTime s512
276884 |       ac-BarringForSpecialAC '11111'B
276885 |     }
276886 |   }
276887 |   ac-BarringSkipForMMTELVoice-r12 TRUE
276888 | }
```

**关键官方判据**

- 步骤 5：UE 发送 `RRCConnectionRequest`，TP Verdict `2 P`（行 276845-276847）。
- 步骤 6-18 接 `36.508 4.5A.6.3-1` steps 3-15；步骤 19 由 `36.508 6.4.2.3` 检查 UE 在 E-UTRA `RRC_CONNECTED`（行 276848-276857）。
- SIB2 条件：`ac-BarringForMO-Data p0/s512`、`ac-BarringSkipForMMTELVoice-r12 TRUE`（行 276875-276888）。

**Main behaviour 原文（逐行）**

```text
276828 | Table 13.5.4.3.2-1: Main behaviour
276829 | St Procedure Message Sequence TP Verdict
276830 |   U - S Message
276831 | 1 Void - - - -
276832 | 2 Void - - - -
276833 | 3 SS changes SIB2 according to table
276834 | 13.5.4.3.3-2 and transmits a Paging message
276835 | including systemInfoModification. The
276836 | systemInfoValueTag in the
276837 | SystemInformationBlockType1 is increased.
276838 | <-- Paging - -
276839 | 3A Wait for 13 s (Note 1) to allow the new system
276840 | information to take effect.
276841 | - - - -
276842 | 4 Make the UE attempt an MTSI MO Speech
276843 | call.
276844 | - - - -
276845 | 5 Check: Does the UE transmit an
276846 | RRCConnectionRequest message?
276847 | --> RRCConnectionRequest 2 P
276848 | 6-
276849 | 18
276850 | Steps 3 to 15 of the generic test procedure for
276851 | IMS MO Speech call establishment in EUTRA:
276852 | Normal Service (TS 36.508 4.5A.6.3-1).
276853 | - - - -
276854 | 19 Check: Does the test result of generic test
276855 | procedure in TS 36.508 subclause 6.4.2.3
276856 | indicate that the UE is in E-UTRA
276857 | RRC_CONNECTED state on Cell 1?
276858 | - - - -
276859 | Note 1: The wait time of 13 s in step 3A is to allow for the network to page the system information change during
276860 | the next modification period, and update the system information at the subsequent modification period. UE
276861 | should acquire the updated system information within 100ms of the start of modification period.
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。


### 2.3 36.508 锚点（通用测试环境）

- 源文本：`<legacy-workspace>/_extract/36508.txt`
- 36.508 `Table 4.4.3.3-1: SystemInformationBlockType2` 行 10026
- 36.508 `Table 4.5A.6.3-1: EUTRA/EPS signalling for IMS MO speech call` 行 17476
- 36.508 `Table 6.4.2.3-1: Test procedure sequence` 行 40682
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

## 3. 前置条件

- UE 支持 SCM 跳过 MMTEL Voice 接入阻塞。
- eNB 可配置 ac-BarringSkipForMMTELVoice-r12。

## 4. 验证流程

1. eNB 下发 SIB2，ac-BarringForMO-data=0% 且 MMTEL Voice skip 生效。
2. 用户发起 MTSI MO 语音。
3. UE 跳过阻塞并建立 RRC，发起语音呼叫。

## 5. TP Verdict 判据

- UE 建立 RRC 并发起 MTSI 语音。
- 未将通用 MO-data 阻塞误用于 MMTEL Voice。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED。

## 7. 受限 / L2_REQUIRED

- 真实 SIB2 SCM skip/RRC 行为观测缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```

## 9. L1 测试骨架

- 阶段：`L1_SKELETON`，不代表 `PASS`，不判官方一致性。
- 待补真实环境依赖：SIB2 ac-BarringForMO-data=0% + ac-BarringSkipForMMTELVoice-r12 + 真实 RRC/eNB。
- 本骨架作用：预留 L1 可执行入口，先保证套件文档包含官方 TP 原文要点、待注入消息、预期行为和环境依赖。
- L1 runner：`python work/l1_skeleton_026_031.py`
- 判定规则：脚本只检查文档/骨架存在性和环境缺口登记，不输出一致性 Verdict。
