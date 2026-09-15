# TC-004 IMS PDN 拒绝 / 重试

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`10.5.3 / 10.5.4`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS | 20260914_NAS_TEST_RERUN`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 已锚定；ESM cause、T3346/backoff 本地单测已固化，真实核心网注入 REJECT/Wait Timer 受限。

## 1. 目的 / 为什么

验证 UE 收到 PDN CONNECTIVITY REJECT 后进入 PROCEDURE TRANSACTION INACTIVE，并能在 RRC reject + Extended wait timer 时启用 T3346/backoff，到期后再发 PDN CONNECTIVITY REQUEST。

## 2. 官方骨架

- 官方 ID：36.523-1 10.5.3 / 10.5.4
  - 10.5.3 Test description 行 234231 / Pre-test 行 234232 / Table 234245
  - 10.5.4 Test description 行 234530 / Pre-test 行 234531 / Table 234558
- 关联：TS 24.301 ESM cause、T3482、T3346 back-off；TS 24.008 ESM cause 值域

### 2.2 TS 24.301 V18.6.0 原文行锚（`_extract/24301.txt`）

| 24.301 条款 | 行号 | 核心判定句 |
|---|---|---|
| 5.6.1.6 Abnormal cases in the UE | 13259 / 13497 | 收到 Extended wait time 后 abort service request、进入 `EMM-REGISTERED`、停止 `T3417/T3417ext`，条件满足则启动 `T3346`。 |
| 6.5.1.2 UE requested PDN connectivity procedure initiation | 15842 | UE 发 `PDN CONNECTIVITY REQUEST`、启动 `T3482`、进入 `PROCEDURE TRANSACTION PENDING`。 |
| 6.5.1.4 UE requested PDN connectivity procedure not accepted | 16118 | 网络回 `PDN CONNECTIVITY REJECT`，必含 PTI 和 ESM cause。 |
| 6.5.1.4.1 General | 16119 / 16178 | UE 收到 REJECT 后停止 `T3482`、进入 `PROCEDURE TRANSACTION INACTIVE`；cause 列表从 16123 起。 |
| 6.5.1.4.3 Handling of network rejection due to ESM cause other than #26 | 16368 | `#8/#27/#32/#33` 等 cause 的 back-off/重试规则；`#32 service option not supported` 在 16438-16458 有专用行为。 |
| ESM cause #32 编码 | 16131 / 30279 | `#32: service option not supported`；UE 请求的 service 不被 PLMN 支持时使用。 |

本地单测注入的 `0x20` 即 `#32 service option not supported`，对应 24.301 行 `16131` / `16178` / `16438-16458`。该映射已由 `outputs/38-模块1-TC004-24.301原文行号证据-20260903.md` 固化。

### 2.1 36.508 锚点（通用测试环境）

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/36508.txt`
- 10.5.3 正文引用：`TS 36.508 subclause 4.5A.1`（行 234297）、`Table 4.7.3-20 PDN CONNECTIVITY REQUEST`（行 234332/234372=30198）、`Table 4.7.3-19 PDN CONNECTIVITY REJECT`（行 234353=30166）、`Table 4.7.3-6` + `Table 4.6.1-8`（行 234403=29276/19886）
- 10.5.4 正文引用：`TS 36.508 subclause 4.5A.1`（行 234622=16410）、`Table 4.7.2-4 ATTACH REQUEST`（行 234643=27956）、`Table 4.7.2-1 ATTACH ACCEPT`（行 234651=27675）、`Table 4.6.1-16 RRCConnectionRequest`（行 234665=20856）、`Table 4.7.2-14A EXTENDED SERVICE REQUEST`（行 234678=28374）、`Table 4.6.1-15 RRCConnectionRelease`（行 234694=20820）、`Table 4.7.3-20`（行 234722=30198）
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 10.5.3: body 230182 / TP 230183 / Conformance 230192 / Test description 230253 / Pre-test 230254 / .3.2 230265 / Main behaviour 230266-230344 / .3.3 230350-230458
- 10.5.4: body 230459 / TP 230461 / Conformance 230480 / Test description 230547 / Pre-test 230548 / .3.2 230573 / Main behaviour 230574-230650 / .3.3 230656-230787

## 3. 前置条件

- UE 注册 EMM，尝试 IMS PDN。
- 测试台可注入 PDN CONNECTIVITY REJECT with PTI + ESM cause，或 RRC reject + Extended wait timer。
- 本地判据脚本覆盖 parse_pdn_connectivity_reject 与 backoff 状态机。

## 4. 验证流程

1. SS/核心网向 UE 发送 PDN CONNECTIVITY REJECT，携带 PTI 匹配与 ESM cause。
2. UE 中止对应过程，进入 PROCEDURE TRANSACTION INACTIVE。
3. 对低优先级 EXTENDED SERVICE REQUEST 被 RRC reject 且收到 Extended wait timer 的场景，UE 启动 T3346。
4. UE 在 T3346 到期前不发 PDN CONNECTIVITY REQUEST；到期后重发 initial request + APN。

## 5. TP Verdict 判据

- ESM cause 被正确解析并映射到重试/终止行为。
- T3346 未到期时无非法重试；到期后能发起重试。
- 不出现无限重试风暴或状态机卡死。
- 本地单测为研发证据，不代表真实核心网注入已跑。

## 6. 当前本地证据

本地证据：`32-`/`35-`/`37-`/`38-`/`40-` 文档与 `work/tc004_state_patch.py --selfcheck`。

## 7. 受限 / L2_REQUIRED

- 真实核心网注入 PDN REJECT / RRC reject + Wait Timer 缺失。

## 8. 执行命令

```text
python work/tc004_state_patch.py --selfcheck
```
```text
python work/run_tc_selfchecks.py
```
