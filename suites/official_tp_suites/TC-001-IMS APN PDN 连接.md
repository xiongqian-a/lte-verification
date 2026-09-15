# TC-001 IMS APN PDN 连接

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`10.5.1`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS | 20260914_NAS_TEST_RERUN`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 骨架已锚定；真实 PDN 报文为字段级证据，端到端一致性仍缺真实 eNB/EPC。

## 1. 目的 / 为什么

验证 UE 在 EMM-REGISTERED + EMM-IDLE、有上行信令或附加 PDN 请求时，能通过 RRC/SERVICE REQUEST 触发 PDN CONNECTIVITY REQUEST，并在默认/专用承载激活后返回 ACCEPT，确保 IMS 业务使用指定 APN 的 PDN。

## 2. 官方骨架

- 官方 ID：36.523-1 10.5.1 UE requested PDN connectivity accepted by the network
- 关联：TS 24.301 EPS Mobility/ESM 状态机；TS 24.229 IMS APN 与 P-CSCF 发现约束

### 2.1 36.508 锚点（通用测试环境）

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/36508.txt`
- 523 正文行 233465 引用 `TS 36.508 subclause 4.5A.1` 的 IP 地址分配流程；对应 `Table 4.5A.1-1: Procedure for IP address allocation in the U-plane` 行 16410
- 523 正文行 233497 引用 `36.508 table 4.6.1-16`；对应 `Table 4.6.1-16: RRCConnectionRequest` 行 20856
- 523 正文行 233513 引用 `TS 36.508 Table 4.7.3-20`；对应 `Table 4.7.3-20: PDN CONNECTIVITY REQUEST` 行 30198
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 10.5.1: body 229255 / TP 229256 / Conformance 229285 / Test description 229443 / Pre-test 229444 / .3.2 229450 / Main behaviour 229451-229517 / .3.3 229530-229651
  - Parallel `Table 10.5.1.3.2-2: Parallel behaviour` 229519-229528

## 3. 前置条件

- EMM-REGISTERED，UE 处于 EMM-IDLE，存在上行信令待发。
- UE 可被触发请求附加 PDN（IMS APN）。
- 本地测试台具备真实 PDN CONNECTIVITY REQUEST / ACTIVATE DEFAULT/DEDICATED BEARER 日志。

## 4. 验证流程

1. UE 建立 RRC，RRC establishmentCause=mo-Data，发送 SERVICE REQUEST。
2. UE 发送 PDN CONNECTIVITY REQUEST，Request Type=initial request，携带目标 APN。
3. 收到 RRCConnectionReconfiguration 且其中含 PTI 匹配的 ACTIVATE DEFAULT EPS BEARER CONTEXT REQUEST 与关联 ACTIVATE DEDICATED EPS BEARER CONTEXT REQUEST。
4. UE 对默认承载/专用承载回 ACTIVATE ... ACCEPT。

## 5. TP Verdict 判据

- PDN CONNECTIVITY REQUEST 中包含 APN 且 Request Type 正确。
- 收到激活请求时 EPS Bearer Identity / PTI 匹配。
- UE 不丢失 IMS PDN 与默认承载关联；不出现非法 ACCEPT/REJECT。
- 当前真实报文为研发证据，不等同 36.523-1 一致性 PASS。

## 6. 当前本地证据

本地证据：`15-TC001-IMS-PDN真实报文证据报告-20260901.md`；`run_tc_evidence.py` 覆盖 TC-001 字段断言。

## 7. 受限 / L2_REQUIRED

- 未在真实 eNB/EPC/一致性 SS 上执行端到端。
- 本地证据仅证明 UE 侧/测试台报文行为符合预期。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
