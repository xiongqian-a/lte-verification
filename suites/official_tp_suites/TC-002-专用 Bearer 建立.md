# TC-002 专用 Bearer 建立

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`10.2.1`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 已锚定；当前只能进行 UE 侧 NAS 注入/字段证据，真实 EPC 触发受限。

## 1. 目的 / 为什么

验证 UE 在默认承载已激活后，收到网络下发的 ACTIVATE DEDICATED EPS BEARER CONTEXT REQUEST 时能正确返回 ACCEPT，并建立与 TFT/EBI 绑定的专用承载。

## 2. 官方骨架

- 官方 ID：36.523-1 10.2.1 Dedicated EPS bearer context activation / Success
- 关联：TS 24.301 ESM 专用承载激活；TS 24.008 TFT/ESM cause 定义

### 2.1 36.508 锚点（通用测试环境）

- 源文本：`<legacy-workspace>/_extract/36508.txt`
- 523 正文行 231749 引用 `36.508 table 4.7.3-3 and table 4.6.1-8 with condition AM-DRB-ADD(2)`；对应 `Table 4.7.3-3: ACTIVATE DEDICATED EPS BEARER CONTEXT REQUEST` 行 29100、`Table 4.6.1-8: RRCConnectionReconfiguration` 行 19886
- 523 正文行 231787 引用 `36.508 table 4.7.3-1`；对应 `Table 4.7.3-1: ACTIVATE DEDICATED EPS BEARER CONTEXT ACCEPT` 行 29018
- 523 正文行 231802 引用 `36.508 table 6.6.2-5`；对应 `Table 6.6.2-5: Reference packet filter #4` 行 43510
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`<legacy-workspace>\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 10.2.1: body 227717 / TP 227718 / Conformance 227728 / Test description 227747 / Pre-test 227748 / .3.2 227760 / Main behaviour 227761-227801 / .3.3 227807-227884

## 3. 前置条件

- EMM-REGISTERED，UE 已建立默认 EPS 承载。
- SS/EPC 可下发 ACTIVATE DEDICATED EPS BEARER CONTEXT REQUEST。
- 本地测试台可注入 NAS 专用承载激活消息。

## 4. 验证流程

1. SS 向 UE 发送 ACTIVATE DEDICATED EPS BEARER CONTEXT REQUEST（含关联默认承载 EBI、TFT、QoS）。
2. UE 校验 EBI/TFT/QoS 参数。
3. UE 回 ACTIVATE DEDICATED EPS BEARER CONTEXT ACCEPT，含正确 EPS Bearer Identity。
4. 判定 TFT 被 UE 接受并在后续上行包路由中启用。

## 5. TP Verdict 判据

- UE 正确返回 ACCEPT 且 EBI 匹配。
- ACCEPT 中不出现非法 EBI/ESM cause。
- TYPE 为 dedicated，且与默认承载关联正确。
- 本地单测 PASS 不代表 EPC 端到端专用承载已触发。

## 6. 当前本地证据

本地证据：`18-TC002-TC003-专用承载回调证据报告-20260902.md`；`run_tc_evidence.py`。

## 7. 受限 / L2_REQUIRED

- 当前环境 srsEPC 仅默认承载，无法端到端触发专用承载；需真实 EPC/SS。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
