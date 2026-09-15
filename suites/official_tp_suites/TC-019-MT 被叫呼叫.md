# TC-019 MT 被叫呼叫

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`34.229-1`
- 官方章节/TP：`12.13 / 12.13a`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方骨架已锚定到 34.229-1 12.13/12.13a；co1750 pjsua MT 日志字段级 PASS，真实 IMS 被叫端到端仍受限。

## 0. 三层格式执行卡

【用例ID】TC-019 MT 被叫呼叫
【来源】TS 34.229-1 V14.7.0 `MT MTSI Speech Call`（12.13 / 12.13a 家族）；TP 行 4864-4867，入口行 4839、4878；关联 TS 24.229 5.1.4.1 / 6.1.1 / 6.1.3，TS 26.114 5.2.1 / 6.2.2.1 / 6.2.5 / 7.3.1。
【测试目的】验证 UE 作为被叫能正确响应 IMS MT MTSI speech call：SIP 信令、SDP offer/answer、preconditions、媒体会话建立与释放。
【优先级】P0
【前置条件/SS 环境】
1. UE 已完成 IMS 注册。
2. 对端/SS 能向 UE 发起 MT INVITE 并携带 SDP offer。
3. 抓包/日志环境能记录 SIP 与媒体释放。
【测试步骤】
1. 对端向 UE 发送 INVITE（媒体 offer）。
2. UE 校验 SIP 头域与 SDP offer。
3. 如启用 preconditions，UE 先确认资源预留（183/UPDATE 流程），再回 200 OK/answer。
4. 媒体建立，通话正常。
5. UE/对端释放呼叫。
【预期判据】
- MT 呼叫 SIP 信令正确，INVITE/183/200/ACK/BYE 顺序合法。
- SDP offer/answer 合法且媒体方向/resource reservation 符合 24.229/26.114。
- 被叫 UE 不错误拒绝或错误建立媒体。
- 呼叫结束能正确释放。
【通过标准】官方 34.229-1 12.13 的 TP Verdict：SIP 信令、SIP header 与参数、SDP 内容交换、呼叫释放全部符合才判 P/F。
【失败处理】记录失败步骤、抓包文件、UE 日志，关联缺陷 ID；本地字段级 PASS 不等于官方 MT 呼叫一致性 Verdict。

## 1. 目的 / 为什么

验证 UE 作为被叫接收 MT MTSI speech call，正确响应 INVITE、完成 SDP/资源预留协商、建立媒体会话并最终释放。

## 2. 官方骨架

- 官方骨架：34.229-1 12.13 / 12.13a 家族（MT MTSI speech call，含带/不带 preconditions）
- 正文证据：`_extract/34229-1e70_ascii.txt` line 4839（MT MTSI speech call with preconditions）；TP line 4864-4867；line 4878 提到 clause 12.13.4
- 官方 TP 过程原文：`official_tp_suites/_substeps/TC-012-021-official-tp-blocks.json` / `.md`；本用例对应 `12.13.3-12.13.5`、`12.13a.3-12.13a.5`。逐行核对脚本：`work/verify_34229_call_tp.py`。
- Annex A 默认消息内容：`official_tp_suites/_substeps/TC-012-021-annexA-call-messages.json` / `.md`；MT 方向对应 A.2.9，呼叫内响应/释放对应 A.2.3、A.2.6、A.2.7、A.2.8、A.3.1。逐行核对脚本：`work/verify_34229_annexA.py`。
- 关联：TS 24.229 5.1.4.1 / 6.1.1 / 6.1.3；TS 26.114 5.2.1 / 6.2.2.1 / 6.2.5 / 7.3.1

### 0.1 官方行号证据

- line 4839：`MT MTSI Speech Call` 相关标题/入口。
- line 4864-4867：TP 判据要求验证 SIP 信令、SIP header 与参数内容、SDP 内容交换、呼叫释放。
- line 4878：提及 clause 12.13.4 等后续子节，继续用于 `.3.2` 展开。

## 3. 前置条件

- UE 完成 IMS 注册。
- 存在可发起 MT 呼叫对端。

## 4. 验证流程

1. 对端向 UE 发起 INVITE（媒体 offer）。
2. UE 校验 SIP 头域与 SDP offer。
3. UE 完成资源预留判定并返回 200 OK/answer。
4. UE 建立媒体，呼叫结束后正确释放。

## 5. TP Verdict 判据

- MT 呼叫 SIP 信令正确。
- SDP offer/answer 正确。
- preconditions 策略行为符合 24.229/26.114。
- 呼叫能释放。

## 6. 当前本地证据

本地证据：`work/tc019_mt_call.py` 输入 `outputs/tc-real-pjsua-20260910-174217/tc019-mt/b.log` → PASS（字段级）。

## 7. 受限 / L2_REQUIRED

- 真实 IMS/被叫呼叫台端到端缺失；官方 `.3.2` 子例未跑。

## 8. 执行命令

```text
python work/tc019_mt_call.py
```
