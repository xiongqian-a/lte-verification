# TC-018 畸形 REGISTER 容错

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`无独立官方 TC`
- 官方章节/TP：`自研健壮性（无官方 TP）`
- 映射等级：`behavior`
- 当前证据层级：`LOCAL_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：无独立官方 TC，按自研健壮性验收；不编造官方一致性 ID。
> 证据边界：当前已核的 `24.229` 正文没有独立“畸形 REGISTER”一致性判据，因此本用例不声明官方 TP 行锚。

## 1. 目的 / 为什么

验证 IMS 客户端收到畸形/异常 REGISTER 响应时不崩溃，并可按协议字段容忍或正确失败。

## 2. 官方骨架

- 官方状态：无独立 34.229-1 畸形 REGISTER TC
- 支撑来源：无；本用例只验证实现不崩溃、能给出受控错误或忽略异常输入，并保持后续请求可处理
- 不得表述为：RFC 3261 / 24.229 已定出本用例的官方 P/F 判据

## 3. 前置条件

- 本地可构造畸形 REGISTER 响应/消息。

## 4. 验证流程

1. 向解析器/客户端注入畸形头字段、缺失必填字段或异常响应。
2. 确认无崩溃、无非法状态跳转。

## 5. TP Verdict 判据

- 无崩溃。
- 错误处理路径稳定。
- 不冒充官方一致性 PASS。

## 6. 当前本地证据

本地证据：`work/tc018_malformed_register.py` → PASS。

## 7. 受限 / L2_REQUIRED

- 非官方一致性 TC。

## 8. 执行命令

```text
python work/tc018_malformed_register.py
```
