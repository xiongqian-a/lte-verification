# TC-021 三方 / REFER 会议

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`34.229-1`
- 官方章节/TP：`15.17 / 15.18 / 15.19 / 15.21`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方骨架已锚定到 `34.229-1 15.17 / 15.18 / 15.19 / 15.21` 家族，本地双 UA REFER + conference join 字段级 PASS。真实 MMTel/IMS 端到端仍缺。

## 0. 三层格式执行卡

【用例ID】TC-021 三方 / REFER 会议
【来源】TS 34.229-1 V14.7.0 `15.17 Creating a conference`、`15.18 Inviting user by REFER to the user`、`15.19 Inviting user via conference focus`、`15.21 Joining after being invited`；抽取文本行 17459-17547 / 17512-17516 / 19833；关联 TS 24.173 V14.3.0 `6.10 Conference (CONF)`（行 478-479）与 `6.11 ECT`（行 480-481），REFER 细节以 RFC 3515、TS 24.147、TS 24.605 为准。
【测试目的】验证 UE 能创建/加入 IMS MTSI 语音会议，并可通过 REFER / conference focus 邀请用户，conference event package 状态正确。
【优先级】P0
【前置条件/SS 环境】
1. UE 已完成 IMS 注册。
2. UE 已建立至少一路 MTSI 语音呼叫，或具备 conference focus 地址。
3. 远端/SS 支持 REFER、202 Accepted、NOTIFY 与 conference event package。
【测试步骤】
1. 创建 conference：UE 用 Conference Factory URI 发 INVITE，或使用已邀会议 URI。
2. 主动邀请：UE 向被邀请用户发 REFER（Refer-To 指向 conference URI），或向 conference focus 发 REFER（Refer-To 指向第三方 URI）。
3. 远端回 202 Accepted，随后 NOTIFY 指示 transfer/join 状态。
4. UE 收到 conference event package NOTIFY，确认成员状态。
5. 会议媒体呼叫建立/成员加入成功。
【预期判据】
- REFER 的 Refer-To/Referred-By 正确。
- 202 Accepted 与 NOTIFY 状态符合 RFC 3515 + 24.147。
- conference URI 可解析并能加入媒体会话。
- 不误终呼、`<dialog>` 状态错误、BYE 误发。
【通过标准】官方 34.229-1 15.17-15.21 的 TP Verdict 判 P/F；当前字段级 PASS 只作研发行为支撑。
【失败处理】记录失败步骤、抓包文件、UE 日志，关联缺陷 ID。

## 1. 目的 / 为什么

验证 UE 能创建/加入 IMS MTSI 语音会议：可发起 conference，或用 REFER 邀请用户，或用 REFER 到 conference focus 将第三方拉入。

## 2. 官方骨架

- 来源：`34.229-1` 15.17 Creating a conference、15.18 Inviting user by REFER to the user、15.19 Inviting user via conference focus、15.21 Joining after being invited。
- 文本抽取记录：`_extract/34229-1e70_ascii.txt`，新 MTSI TC 记录行 19833、19906、19913，通用接口行 17512-17516，WLAN 序列行 17459-17547。
- 官方 TP 过程原文：`official_tp_suites/_substeps/TC-012-021-official-tp-blocks.json` / `.md`；本用例对应 `15.17.3-15.17.5`、`15.18.3-15.18.5`、`15.19.3-15.19.5`、`15.21.3-15.21.5`。逐行核对脚本：`work/verify_34229_call_tp.py`。
- Annex A 默认消息内容：`official_tp_suites/_substeps/TC-012-021-annexA-call-messages.json` / `.md`；REFER/会议方向对应 A.2.7、A.2.8、A.2.10、A.2.11、A.2.12、A.3.1、A.3.3、A.5.3。逐行核对脚本：`work/verify_34229_annexA.py`。
- 关联：`24.147`，`24.173`，`24.628`。

### 2.1 24.173 锚点

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/24173.txt`（TS 24.173 V14.3.0）
- CONF 官方语义入口：`6.10 Conference (CONF)` 行 478-479，正文明确 “The CONF service is specified in 3GPP TS 24.605 [4].”
- ECT 官方语义入口：`6.11 Explicit Communication Transfer (ECT)` 行 480-481，正文明确 “The ECT service is specified in 3GPP TS 24.629 [10].”
- 补充业务总则：`4.3 Overview of supplementary services part` 行 384-389，说明补充业务用 SIP 作为使能协议。
- 结论：`24.173` 给出 MMTel 会议/ECT 的服务归属与参考规范；REFER 细节以 `RFC 3515`、`24.147`、`24.605`、`34.229-1 15.17-15.21` 为准。

### 0.1 官方行号证据

- `_extract/34229-1e70_ascii.txt` line 17459-17547：15.x 家族通用行为/子例引用。
- `_extract/34229-1e70_ascii.txt` line 17512-17516：15.x 通用接口相关引用。
- `_extract/34229-1e70_ascii.txt` line 19833：新 MTSI TC 记录，用于继续核对 15.17-15.21。
- `_extract/24173.txt` line 478-481：`6.10 Conference (CONF)` 与 `6.11 ECT` 的服务归属。

## 3. 前置条件

- UE 已完成 IMS 注册。
- UE 已建立至少一路 MTSI 语音呼叫，或具备 conference focus 地址。
- 远端/SS 支持 REFER / conference event package。

## 4. 验证流程（按用户要求覆盖 REFER 会议）

1. 创建 conference：UE 用 Conference Factory URI 发 INVITE 创建会议，或使用已邀会议。
2. 主动邀请：UE 向被邀请用户发 REFER，Refer-To 指向 conference URI；或向 conference focus 发 REFER，Refer-To 指向第三方 URI。
3. 远端回 202 Accepted，随后 NOTIFY 指示 transfer 状态。
4. UE 收到 conference event package NOTIFY 后，确认成员状态。
5. 会议媒体呼叫建立/成员加入成功。

## 5. TP Verdict 判据

- REFER 的 Refer-To/Referred-By 正确。
- 202 Accepted 与 NOTIFY 状态按 RFC 3515 + 24.147。
- conference URI 可被解析并加入媒体会话。
- 不出现误终呼、<dialog> 状态错误、BYE 误发。

## 6. 当前本地证据

```text
python work/tc021_conference_refer.py
输入：outputs/tc-real-pjsua-20260910-174217/tc021-refer/a.log
结果：PASS（字段级）
补充：co1750 双 UA REFER + FreeSWITCH 2-member conference join 日志字段级 PASS
```

## 7. 受限 / L2_REQUIRED

- 当前不是真实 MMTel conference server / IMS AS 端到端。
- 官方 15.17/15.18/15.19/15.21 的 `.3.2` 子例和 SS P/F 未跑。
- `24.173` 文档已核到 `6.10/6.11`，但会议/ECT 具体信令行为仍需按 `24.605/24.629` 继续对齐。

## 8. 执行命令

```text
python work/tc021_conference_refer.py
```
