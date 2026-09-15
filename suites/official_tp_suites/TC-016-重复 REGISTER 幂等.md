# TC-016 重复 REGISTER 幂等

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`24.229（行为支撑）`
- 官方章节/TP：`5.1.1.2.1 / 5.1.1.4.1（行为级）`
- 映射等级：`behavior`
- 当前证据层级：`LOCAL_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：行为级验证；34.229-1 无独立官方 TC，按 24.229 注册语义与自研健壮性验收。
> 证据边界：`TS 24.229 V14.17.0 5.1.1.2.1` 行 3251 和 `5.1.1.4.1` 行 3468-3486 只支撑注册时序与 200 OK 状态处理，**不是**独立官方一致性 TC。

## 1. 目的 / 为什么

验证 UE 对同一 Call-ID、相同注册身份的重复 REGISTER 能稳定返回 200 OK，不重置注册状态、不产生 Expires:0、不崩溃。

## 2. 官方骨架

- 官方状态：34.229-1 无独立重复 REGISTER 幂等 TC
- 行为支撑：`TS 24.229 V14.17.0 5.1.1.2.1` 行 3251；上一注册未收到最终响应或超时前，不再发起新注册过程
- 状态处理支撑：`TS 24.229 V14.17.0 5.1.1.4.1` 行 3468-3486；收到 200 OK 后更新注册有效期并保存 Service-Route 等状态
- 不得表述为：官方重复 REGISTER 一致性 TC 或 34.229-1 Verdict

## 3. 前置条件

- UE 已完成 IMS 注册。

## 4. 验证流程

1. 向同一 UA 重放同 Call-ID REGISTER。
2. 确认每次后续 REGISTER 获得 200 OK。
3. 确认注册状态未因重复 REGISTER 被重置。

## 5. TP Verdict 判据

- 同一 Call-ID 重复 REGISTER 后 200 OK。
- 无 Expires:0 重置。
- 无崩溃/死循环。

## 6. 当前本地证据

本地证据：`work/tc016_duplicate_register.py --raw --log outputs/tc014_rereg_real_20260909b.log` → PASS。

## 7. 受限 / L2_REQUIRED

- 无官方独立一致性 ID；不作为 34.229-1 官方 PASS。
- 行 3251/3468-3486 是行为级支持，不替代官方 TP 的执行与判定。

## 8. 执行命令

```text
python work/tc016_duplicate_register.py
```
```text
python work/tc016_duplicate_register.py --selfcheck
```
