# TC-007 SPS / DRX

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`7.1.6.1 / 7.1.6.1a / 7.1.6.2 / 7.1.6.3 / 7.1.6.4 / 7.1.6.5`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 DRX/eDRX 一致性用例已锚定；SPS 无已核到的独立 LTE 一致性 TP，仅作行为补充；真实 RRC/SS/仪表执行仍缺。

## 1. 目的 / 为什么

验证 UE 按 RRC 配置执行长 DRX、短 DRX、DRX Command MAC CE 和 eDRX 行为；SPS 仅作为实现行为补充，不冒充官方 DRX 用例。

## 2. 官方骨架

- 官方 ID：36.523-1 7.1.6.1 DRX operation / Short cycle not configured / Parameters configured by RRC。
- 官方 ID：36.523-1 7.1.6.1a DRX operation / Short cycle not configured / Parameters configured by RRC / Enhanced Coverage / CE Mode A。
- 官方 ID：36.523-1 7.1.6.2 DRX Operation / Short cycle not configured / DRX command MAC control element reception。
- 官方 ID：36.523-1 7.1.6.3 DRX operation / Short cycle configured / Parameters configured by RRC。
- 官方 ID：36.523-1 7.1.6.4 DRX Operation / Short cycle configured / DRX command MAC control element reception。
- 官方 ID：36.523-1 7.1.6.5 eDRX operation / Long cycle configured / Parameters configured by RRC；其 .3.2 继承 7.1.6.1.3.2。
- 正文行锚：7.1.6.1 起 line 58776；7.1.6.1a 起 line 59184；7.1.6.2 起 line 59454；7.1.6.3 起 line 59727；7.1.6.4 起 line 59990；7.1.6.5 起 line 60271。

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 7.1.6.1: body 57770 / TP 57771 / Conformance 57812 / Test description 57898 / Pre-test 57899 / .3.2 57906 / Main behaviour 57923-58127 / .3.3 58133-58170
- 7.1.6.1a: body 58171 / TP 58173 / Conformance 58182 / Test description 58325 / Pre-test 58326 / .3.2 58333 / Main behaviour 58340-58385 / .3.3 58391-58435
- 7.1.6.2: body 58436 / TP 58438 / Conformance 58466 / Test description 58520 / Pre-test 58521 / .3.2 58528 / Main behaviour 58534-58660 / .3.3 58666-58703
- 7.1.6.3: body 58704 / TP 58705 / Conformance 58728 / Test description 58814 / Pre-test 58815 / .3.2 58822 / Main behaviour 58828-58919 / .3.3 58921-58961
- 7.1.6.4: body 58962 / TP 58964 / Conformance 58992 / Test description 59046 / Pre-test 59047 / .3.2 59058 / Main behaviour 59064-59190 / .3.3 59196-59236
- 7.1.6.5: body 59237 / TP 59238 / Conformance 59279 / Test description 59415 / Pre-test 59416 / .3.2 59427 / Main behaviour 57923-58127 / .3.3 59429-59475
  - .3.2 继承关系：`7.1.6.5.3.2` 继承 `7.1.6.1.3.2`

## 3. 前置条件

- UE 处于 Loopback Activated (state 4)；7.1.6.1a 使用 state 4-CE。
- SS/eNB 可下发包含 DRX/eDRX 参数的 RRCConnectionReconfiguration。
- 测试环境可按官方步骤在指定 PDCCH 子帧注入传输并观测 UE 行为。

## 4. 验证流程

1. 按 RRC 下发 DRX 参数，并验证长 DRX 的 OnDuration、drx-InactivityTimer、HARQ RTT 和重传定时行为。
2. 按 7.1.6.1a 验证 CE Mode A 下的 UL HARQ RTT 和 drx-ULRetransmissionTimer 行为。
3. 按 7.1.6.2/7.1.6.4 验证 DRX Command MAC CE 在短/长 DRX 配置下的处理。
4. 按 7.1.6.3 验证短 DRX cycle 和 drxShortCycleTimer 到期后的行为。
5. 按 7.1.6.5 复用 7.1.6.1.3.2 过程验证 eDRX 长周期。
6. SPS 仅记录实现行为，除非另行核到独立官方 TP，否则不挂官方一致性 ID。

## 5. TP Verdict 判据

- 每条官方用例按其 Main Behaviour 表的 TP Verdict 逐步骤判定 P/F。
- 7.1.6.5 必须引用 7.1.6.1.3.2 的步骤序列，不能写成无 TP。
- SPS 不重复挂用 DRX 官方 ID。
- 本地/静态证据不构成 36.523-1 官方一致性 PASS。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED（6 条官方 DRX/eDRX TP 已对齐；无本地执行脚本）。

## 7. 受限 / L2_REQUIRED

- 真实 RRC/eNB/SS 或一致性仪表缺失。
- SPS 独立官方 LTE 一致性用例尚未核到，继续保持行为补充。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
