# TC-010 TAU / Service Request / Paging

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`9.2.3.1.1 / 9.3.1.1 / 9.3.2.1`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 骨架已锚定；真实 RAN/EPC 触发缺失，当前为标准判据待执行。

## 1. 目的 / 为什么

验证 UE 在 TAI list 改变时发 TAU；在 EMM-IDLE 有用户数据时以 mo-Data 建立 RRC 并发 SERVICE REQUEST；匹配 S-TMSI 寻呼时响应并建 RRC，不匹配则不建。

## 2. 官方骨架

- 官方 ID：36.523-1 9.2.3.1.1 / 9.3.1.1 / 9.3.2.1
  - 9.2.3.1.1 body 行 210479 / TP 行 210480 / .3 行 210543 / Pre-test 行 210544 / Table 210559
  - 9.3.1.1 body 行 228923 / TP 行 228924 / .3 行 228999 / Pre-test 行 229000 / Table 229015
  - 9.3.2.1 body 行 230703 / TP 行 230704 / .3 行 230811 / Pre-test 行 230812 / Table 230825
- 关联：TS 24.301 5.3.1.1 / 5.5.3.1 / 5.5.3.2.x / 5.6.x；TS 36.331 5.3.2.3 / 5.3.3.2-5.3.3.4；TS 33.401 7.2.6.2

### 2.1 36.508 锚点（通用测试环境）

- 源文本：`<standards-extract>/36508.txt`
- TAU（9.2.3.1.1）：523 正文行 210557 要求 UE 处于 `TS 36.508` `State 2`；行 210586/210601 走 `TS 36.508 subclause 6.4.2.4` Paging/NAS 测试流程；行 210638/210680 引用 `Table 4.7.2-27: TRACKING AREA UPDATE REQUEST` 行 28903；行 210649/210692 引用 `Table 4.7.2-24: TRACKING AREA UPDATE ACCEPT` 行 28658
- Service Request（9.3.1.1）：523 正文行 229029/230854 引用 `TS 36.508 4.5.3.3-1` 的 Generic Radio Bearer establishment；对应 `Table 4.5.3.3-1: Generic Radio Bearer establishment procedure (state 2 to state 3)` 行 15750；行 229050 引用 `Table 4.6.1-16: RRCConnectionRequest` 行 20856
- Paging（9.3.2.1）：523 正文行 230861 引用 `Table 4.6.1-16` 行 20856；行 230881 引用 `Table 4.6.1-7: Paging` 行 19862
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.2 36.509 锚点（Test Loop 相关）

- 源文本：`<standards-extract>/36509.txt`（TS 36.509 V14.0.0）
- `5.4.4 UE test loop mode B operation` 行 1700；
- `5.4.4.2 Reception of IP PDUs when UE is in E-UTRA or NB-IoT mode` 行 1702-1703；下行 `PDCP SDU (=IP PDU)` 提交给 `UL TFT handling SAP` 行 1735，对应 523 正文 9.3.1.1 的 Loopback Activated 前置。
- `5.4.4.10 Establishment of the RRC/RR connection in E-UTRA, NB-IoT, UTRA, GSM/GPRS and CDMA2000 mode` 行 1827-1833：RRC/RR 连接与 EPS bearer 建立后，若 `TEST_LOOP_MODE_B_ACTIVE=TRUE`，按 5.4.4 系列执行。
- 说明：36.509 是 UE 测试环路能力/Test Loop mode B 的运行规则，用于理解 523 服务和 Service Request 的测试状态；它不是真实 RAN/MME 端到端判据。

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`<local-user>\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 9.2.3.1.1: body 206884 / TP 206885 / Conformance 206910 / Test description 206947 / Pre-test 206948 / .3.2 206961 / Main behaviour 206962-207032 / .3.3 207038-207122
- 9.3.1.1: body 225035 / TP 225036 / Conformance 225044 / Test description 225110 / Pre-test 225111 / .3.2 225124 / Main behaviour 225125-225147 / .3.3 225149-225169
- 9.3.2.1: body 226784 / TP 226785 / Conformance 226802 / Test description 226890 / Pre-test 226891 / .3.2 226902 / Main behaviour 226903-226935 / .3.3 226937-226978

## 3. 前置条件

- EMM-REGISTERED，UE 有用户数据待发或寻呼触发。
- RAN/MME 可调度 TAU/SR/Paging。

## 4. 验证流程

1. TAU：UE 进入新 TAI 时发 TRACKING AREA UPDATE REQUEST 且带 Last visited registered TAI；TAI list 内不发起 TAU。
2. Service Request：UE EMM-IDLE、有用户数据，RRC cause=mo-Data，发 SERVICE REQUEST。
3. Paging：收到 S-TMSI 匹配寻呼时建立 RRC 并发 SERVICE REQUEST；不匹配 ue-Identity 不建连接。

## 5. TP Verdict 判据

- TAU 请求/接受字段正确。
- Service Request 的 establishment cause 为 mo-Data。
- Paging 匹配/不匹配行为符合预期。
- 真实 RAN/MME 端到端缺失时不得给官方 PASS。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED。

## 7. 受限 / L2_REQUIRED

- 真实 RAN/MME 调度与寻呼环境缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
