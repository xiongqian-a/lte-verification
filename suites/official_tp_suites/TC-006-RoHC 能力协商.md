# TC-006 RoHC 能力协商

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`8.2.1.8`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 已锚定到 36.523-1 8.2.1.8；真实 RRC/eNB/SS 或一致性仪表执行仍缺，不输出官方 P/F。

## 1. 目的 / 为什么

验证 UE 在 RRC_CONNECTED 且收到包含 headerCompression=rohc 的 RRCConnectionReconfiguration 后，发送 RRCConnectionReconfigurationComplete，并完成对应的专用承载 NAS 过程。

## 2. 官方骨架

- 官方 ID：36.523-1 8.2.1.8 RRC connection reconfiguration / Radio bearer establishment / Success / Dedicated bearer / ROHC configured。
- 正文行锚：title/TP 在 `523-1v14.txt` line 101264-101266；`.3.2` line 101351-101374；`.3.3` line 101376-101450。
- 关键判据：headerCompression 设为 rohc；profiles 中 profile0x0001 / profile0x0002 置为 TRUE；UE 回 RRCConnectionReconfigurationComplete。
- 关联：TS 36.331 5.3.5.3 / 5.3.10.3；TS 36.323 5.5.1 / 5.5.2；TS 36.306 4.3.1.1。

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`<legacy-workspace>\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 8.2.1.8: body 99541 / TP 99543 / Conformance 99552 / Test description 99614 / Pre-test 99615 / .3.2 99626 / Main behaviour 99627-99649 / .3.3 99651-99724

## 3. 前置条件

- UE 处于 Generic RB Established (state 3)，见 36.508。
- SS/eNB 可发送包含 RoHC 配置的 RRCConnectionReconfiguration。
- 测试环境具备真实 RRC 重配置和专用承载激活日志。

## 4. 验证流程

1. SS 发送 RRCConnectionReconfiguration 以建立数据无线承载，消息使用 headerCompression=rohc。
2. 检查 UE 发送 RRCConnectionReconfigurationComplete。
3. UE 发送 ULInformationTransfer，其中包含 ACTIVATE DEDICATED EPS BEARER CONTEXT ACCEPT。
4. 按 36.508 6.4.2.3 通用过程检查 UE 仍处于 E-UTRA RRC_CONNECTED。

## 5. TP Verdict 判据

- UE 发出的 RRCConnectionReconfigurationComplete 为官方步骤 2 的 TP Verdict=P。
- ACTIVATE DEDICATED EPS BEARER CONTEXT ACCEPT 与专用承载配置匹配。
- RoHC 配置字段与官方 `.3.3` 表一致，且 UE 不因配置失败而离开 RRC_CONNECTED。
- 本地/静态证据不构成 36.523-1 官方一致性 PASS。

## 6. 当前本地证据

当前证据等级：STANDARD_ALIGNED（官方 TP/.3.2/.3.3 已对齐；无本地执行脚本）。

## 7. 受限 / L2_REQUIRED

- 真实 RRC/eNB/SS 或一致性仪表缺失。
- 必须由合格 SS 执行官方步骤并给出 TP Verdict，不能由静态字段检查替代。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
