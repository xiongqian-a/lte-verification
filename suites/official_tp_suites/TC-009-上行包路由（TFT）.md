# TC-009 上行包路由（TFT）

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`10.9.1`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 骨架已锚定；多承载 + UL TFT 端到端环境缺失，当前为标准判据待执行。

## 1. 目的 / 为什么

验证 UE 在多 EPS 承载场景下按 TFT 优先级路由上行 IP 包，命中专用承载走专用承载，未命中则按默认承载/丢弃规则处理。

## 2. 官方骨架

- 官方 ID：36.523-1 10.9.1 UE routing of uplinks packets
- 关联：TS 23.060 15.3.2.0；TS 24.008 TFT IE 定义

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`<legacy-workspace>\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 10.9.1: body 232864 / TP 232865 / Conformance 232908 / Test description 233215 / Pre-test 233216 / .3.2 233228 / Main behaviour 233447-233538 / .3.3 233544-234169

## 3. 前置条件

- UE 已建立默认承载 + 两个专用承载。
- 各承载配置 UL TFT/默认过滤器。

## 4. 验证流程

1. 构造命中专用承载 UL TFT 的 IP 包，验证按评估顺序走专用承载。
2. 构造未命中专用承载且默认承载无过滤器的包，验证走默认承载。
3. 构造仅命中默认承载过滤器的包，验证走默认承载。
4. 构造不满足任何过滤器的包，验证丢弃。

## 5. TP Verdict 判据

- TFT 过滤优先级正确。
- 无错路由；全部不匹配时丢弃。
- 真实多承载/过滤器验证缺失时不得给官方 PASS。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED。

## 7. 受限 / L2_REQUIRED

- 真实多承载 + UL TFT 下发 EPC 缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
