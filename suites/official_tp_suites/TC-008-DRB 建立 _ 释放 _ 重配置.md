# TC-008 DRB 建立 / 释放 / 重配置

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`8.2.1.3`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 骨架已锚定；真实 eNB/EPC 端到端缺失，当前为标准判据待执行。

## 1. 目的 / 为什么

验证 UE 在 RRC_CONNECTED 下收到含新 drb-Identity + dedicatedInfoNASList 的 RRCConnectionReconfiguration 后建立 DRB 并回 RRCConnectionReconfigurationComplete。

## 2. 官方骨架

- 官方 ID：36.523-1 8.2.1.3 RRC connection reconfiguration / Radio bearer establishment / Success / Dedicated bearer
- 关联：TS 36.331 5.3.5.3 / 5.3.10.3

### 2.1 36.508 锚点（通用测试环境）

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/36508.txt`
- 523 正文行 100575 引用 `TS 36.508 subclause 6.4.2.3` 的通用流程；对应 `Table 6.4.2.3-1: Test procedure sequence` 行 40682
- 523 正文行 100582 引用 `36.508 table 4.6.1-8, condition DRB(1,0)`；对应 `Table 4.6.1-8: RRCConnectionReconfiguration` 行 19886
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 8.2.1.3: body 98790 / TP 98792 / Conformance 98801 / Test description 98836 / Pre-test 98837 / .3.2 98844 / Main behaviour 98845-98868 / .3.3 98870-98898

## 3. 前置条件

- UE 在 E-UTRA RRC_CONNECTED。
- SS/eNB 可下发包含新 DRB 的重配置。

## 4. 验证流程

1. SS 发送 RRCConnectionReconfiguration，含新 drb-Identity 与 dedicatedInfoNASList。
2. UE 按 radioResourceConfigDedicated 建立 PDCP/RLC/逻辑信道。
3. UE 发送 RRCConnectionReconfigurationComplete。

## 5. TP Verdict 判据

- DRB Identity 与 EPS Bearer 映射正确。
- Complete 消息发送成功。
- 相关 PDCP/RLC/LCID 建立可观测。
- 真实 eNB 端到端缺失时不得给官方 PASS。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED。

## 7. 受限 / L2_REQUIRED

- 真实 eNB/EPC/SS 缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
