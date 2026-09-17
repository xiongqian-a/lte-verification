# TC-003 专用 Bearer 释放

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`10.4.1`
- 映射等级：`exact_line_ref`
- 当前证据层级：`STANDARD_ALIGNED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 已锚定；当前只能做 UE 侧 NAS 注入覆盖，真实 EPC 触发受限。

## 1. 目的 / 为什么

验证 UE 收到 DEACTIVATE EPS BEARER CONTEXT REQUEST 后能按官方 4 个子例正确返回 ACCEPT，删除对应 EBI/PDN 承载关联。

## 2. 官方骨架

- 官方 ID：36.523-1 10.4.1 EPS bearer context deactivation / Success
- 官方子例：删除单个承载、删除默认承载关联 PDN 全部承载、删除不存在承载仍回 ACCEPT/EBI、EMM-IDLE 转 CONNECTED 时按 SS 显式激活承载同步

### 2.1 36.508 锚点（通用测试环境）

- 源文本：`<legacy-workspace>/_extract/36508.txt`
- 523 正文行 232225 引用 `TS 36.508[18] clause 4.4.3.1` 的 System information combination 3；通用 SIB 结构见 36.508 `Table 4.4.3.3-1: SystemInformationBlockType2` 行 10026（SIB 表族入口）
- 523 正文行 232268 引用 `TS 36.508 subclause 4.5A.1`；对应 `Table 4.5A.1-1: Procedure for IP address allocation in the U-plane` 行 16410
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`<repo>/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`<legacy-workspace>\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 10.4.1: body 228159 / TP 228160 / Conformance 228193 / Test description 228274 / Pre-test 228275 / .3.2 228288 / Main behaviour 228289-228677 / .3.3 228679-229058

## 3. 前置条件

- EMM-REGISTERED，PDN/承载上下文已建立。
- SS 可对指定 EBI 下发 DEACTIVATE EPS BEARER CONTEXT REQUEST。
- 本地测试台可注入去激活消息并捕获 ACCEPT。

## 4. 验证流程

1. 按子例 1：SS 请求删除单个专用承载 EBI。
2. 按子例 2：SS 请求删除默认承载，UE 应删除该 PDN 全部承载并回 ACCEPT。
3. 按子例 3：SS 请求删除 UE 当前不存在承载，UE 仍回 ACCEPT，EBI 与请求一致。
4. 按子例 4：EMM-IDLE/EMM-CONNECTED 转换场景按 SS 显式激活的承载同步状态。

## 5. TP Verdict 判据

- UE 对合法去激活请求回 DEACTIVATE EPS BEARER CONTEXT ACCEPT。
- 删除默认承载场景下，该 PDN 的全部 EPS Bearer 被删除。
- 不存在承载场景下不崩溃，EBI 原样回显。
- 真实 EPC 端到端触发缺失时，不得给出官方一致性 PASS。

## 6. 当前本地证据

本地证据：NAS 注入回调/字段断言，见 `18-` 与 `run_tc_evidence.py`。

## 7. 受限 / L2_REQUIRED

- 真实 EPC 的专用承载释放触发缺失。

## 8. 执行命令

```text
python work/run_tc_evidence.py
```
