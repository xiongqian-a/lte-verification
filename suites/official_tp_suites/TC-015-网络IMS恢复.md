# TC-015 网络 / IMS 重启恢复

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`34.229-1 + 24.229 + 36.523-1`
- 官方章节/TP：`MO Call 504 Server Time-out restoration`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 504 restoration 骨架已锚定，本地 responder 证据 PASS。真实 S-CSCF 重启后 504 端到端未覆盖，标 `RESTRICTED`。

## 0. 三层格式执行卡

【用例ID】TC-015 网络 / IMS 重启恢复
【来源】TS 34.229-1 V14.7.0 `12.2a MO Call - 504 Server Time-out`，源文件 `34229-1e70-word.txt` 行 6119-6186；底层协议 TS 24.229 clause 5.1.2A.1.6；RAN/网络侧前置关联 TS 36.523-1 9.3.1。
【测试目的】验证 UE 在 IMS 服务器重启/不可用时收到带 restoration body 的 504 Server Time-out 后，能执行 initial registration 完成恢复。
【优先级】P0
【前置条件/SS 环境】
1. UE 已完成 IMS 注册（Annex C.2 到 last step）。
2. SS 配置 IMS AKA 共享密钥，并已完成 AKAv1-MD5 鉴权。
3. SS 能对 INVITE 回 504，且消息体为 `Content-Type: application/3gpp-ims+xml` 的 alternative-service，`type=restoration`，`action=initial-registration`；`P-Asserted-Identity` 等于注册时 Service-Route/Path 的 URI。
【测试步骤】
1. UE 按 TS 36.508 table 4.5A.6.3-1 / Annex C.21 发起 MTSI MO speech call。
2. SS 回 504 Server Time-out（Annex A.4.6；body 按 A.2.7）。
3. UE 回 ACK。
4. UE 按 Annex C.2 步骤 4-11 执行 initial registration（REGISTER）。
5. IMS/SS 完成注册并回 200 OK。
【预期判据】
- 504 的 P-Asserted-Identity 匹配注册身份。
- XML body 的 alternative-service 为 restoration / initial-registration。
- UE 收到 504 后执行 initial registration，不是忽略或继续原会话。
- 初始注册最终完成，无会话泄漏/崩溃。
【通过标准】官方 34.229-1 TP Verdict：只有 UE 在 504 后执行 initial registration 才判通过。
【失败处理】记录失败步骤、抓包文件、UE 日志，关联缺陷 ID；本地 responder 证据只作研发行为支撑。

## 1. 目的 / 为什么

验证 UE 在 IMS 网络重启/服务器不可用后，能根据 504 Server Time-out 与 `application/3gpp-ims+xml` alternative-service restoration 发起初始注册恢复。

## 2. 官方骨架

- 来源：`34.229-1` `12.2a` MO Call - 504 Server Time-out。
- 主文本抽取记录：`official_tp_suites/_substeps/TC-011-015-032-official-tp-blocks.json` / `.md`，源文件 `34229-1e70-word.txt` 行 6119-6186；逐行核对脚本 `work/verify_34229_reg_auth_err_tp.py`。`34229-1e70_ascii.txt` 行 4564-4599 仅作交叉检索。
- 关联：`24.229`，`36.523-1 9.3.1` 可用作 RAN/网络侧恢复的前置参考。

### 0.1 官方行号证据

- line 6119：官方标题 `12.2a MO Call - 504 Server Time-out`。
- line 6122-6135：Conformance requirement，504 含 P-Asserted-Identity（Service-Route/Path）且 `application/3gpp-ims+xml` alternative-service 为 restoration / initial-registration 时，UE 应执行 initial registration。
- line 6143-6146：步骤要点（TS 36.508 steps 1-8 → SS 回 504 → UE ACK → Annex C.2 steps 4-11 initial registration）。
- line 6186：Verdict 点：step 3 后 UE 必须执行 initial registration。

## 3. 前置条件

- UE 已完成 IMS 注册。
- SS/网络可对 INVITE 回 504，并在消息体携带：
  - `Content-Type: application/3gpp-ims+xml`
  - `<alternative-service><type>restoration</type><action>initial-registration</action></alternative-service>`
  - `P-Asserted-Identity` 等于注册时 Service-Route/Path 中 URI。

## 4. 验证流程

1. UE 发起 MTSI MO speech call，发送 INVITE。
2. SS 回 504 Server Time-out，带 restoration body。
3. UE 回 ACK（事务完成）。
4. UE 随后发起 initial registration（REGISTER）。
5. SS/IMS 完成注册并回 200 OK。

## 5. TP Verdict 判据

- 504 的 P-Asserted-Identity 匹配之前注册身份。
- XML body 为 `alternative-service` restoration，`action=initial-registration`。
- UE 收到后执行 initial registration，不是继续原会话或忽略。
- 注册过程最终成功，无泄漏会话/崩溃。

## 6. 当前本地证据

```text
python work/tc015_restoration.py --selfcheck
  SELFCHECK PASS

python work/tc015_restoration.py --log outputs/tc015-504-local-pty-20260910.log
  PASS
  观察到 INVITE、504、P-Asserted-Identity、3gpp-ims+xml、restoration、initial-registration、REGISTER after 504
```

## 7. 受限 / L2_REQUIRED

- 当前为本地注入/responder 证据，不是真实 S-CSCF 重启后 504 端到端。
- 需要真实 IMS 网络重启故障注入或一致性测试仪。

## 8. 执行命令

```text
python work/tc015_restoration.py
```
