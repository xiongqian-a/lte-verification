# TC-xxx 用例名称

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`<specification>`
- 官方章节/TP：`<clause and official TP title>`
- 映射等级：`exact_line_ref | partial | behavior | none`
- 当前证据层级：`LOCAL_PASS | LIMITED_PASS | SELFCHECK_PASS | STANDARD_ALIGNED | RESTRICTED`
<!-- OFFICIAL_TP_METADATA:END -->

## 0. 执行卡

【用例ID】TC-xxx / <official specification and clause>

【来源】<specification, version, clause/subclause, line anchors, related specifications>

【测试目的】<what conformance or implementation behavior is being verified>

【优先级】P0 / P1 / P2

【前置条件/SS环境】
1. <UE state and configuration>
2. <network, SS, IMS, core-network, or instrument state>
3. <subscriber, UICC, APN, identity, or parameter configuration>
4. <evidence prerequisites>

【测试步骤】
1. <trigger or initialization>
2. <message or behavior under test>
3. <expected UE/network response>
4. <completion or cleanup>

【预期判据（逐消息检查）】
- <message 1 field, state, timer, or sequence criterion>
- <message 2 field, state, timer, or sequence criterion>
- <negative condition or timeout criterion>

【通过标准】<official TP verdict rule; state explicitly whether this is LOCAL or L2>

【失败处理】<capture logs, packets, failed step, actual/expected difference, defect linkage>

## 1. 目的 / 为什么

<Why this TC exists and what risk it controls.>

## 2. 官方骨架

- 主来源：<specification and clause>
- 正文锚点：<extracted file and line numbers>
- 关联规范：<cross references>
- 官方 TP：<test purpose, method, expected sequence, requirements>
- 官方消息内容：<Annex, table, or .3.3 reference>

## 3. 前置条件

- <Pre-test condition 1>
- <Pre-test condition 2>
- <Current local or L2 environment condition>

## 4. 验证流程

1. <Preconditions and trigger>
2. <Step-by-step procedure aligned to the official expected sequence>
3. <Message and state checks>
4. <Completion and cleanup>

## 5. TP Verdict 判据

- <Official checkpoint 1>
- <Official checkpoint 2>
- <Allowed variants, timers, tolerances, or fallback behavior>
- <What must not happen>

## 6. 当前本地证据

```text
<command>
输入：<artifact path>
结果：<LOCAL_PASS / LIMITED_PASS / EXPECTED_FAIL / NOT_EXECUTED>
观察：<facts actually observed>
限制：<coverage gaps>
```

## 7. 受限 / L2_REQUIRED

- <Missing eNB, EPC, IMS, SS, instrument, operator, or lab dependency>
- <Official subclause or variant not yet executed>
- <Explicit statement that local PASS is not an official verdict>

## 8. 执行命令

```text
<single-case command>
python runners/run_tc_evidence.py
python -X utf8 run_official_suite.py
```

## 9. 官方证据回填（仅在 L2 执行后填写）

```text
来源类型：<qualified SS / accredited laboratory>
厂商/产品：<manufacturer and product>
证据包：<bundle path or identifier>
官方章节：<official clause>
TP Verdict：<P / F / INCONCLUSIVE>
原始 artifact 与 SHA256：<artifact and hash>
```
