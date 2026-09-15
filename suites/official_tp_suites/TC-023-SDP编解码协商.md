# TC-023 SDP 编解码协商

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`34.229-1 + 26.114`
- 官方章节/TP：`12.12/12.13 SDP TP`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 已锚定到 `34.229-1 12.12/12.13` SDP 部分 + `26.114`。本地真实 pjsua SDP 字段 PASS，官方完整性判据未完全运行。

## 0. 三层格式执行卡

【用例ID】TC-023 SDP 编解码协商
【来源】TS 34.229-1 V14.7.0 MO/MT 语音呼叫 TP 中的 SDP Specific Message Contents：line 4732-4805（MO without preconditions）、line 4838-4877（MT with preconditions）；对应 TS 24.229 6.1.1/6.1.2/6.1.3（line 4672-4697、4754-4756、4849-4853）与 TS 26.114 SDP/RTCP 要求（line 4698-4708、4854-4862）。
【测试目的】验证 UE 发起的 SDP offer 与收到的 SDP answer 符合 IMS MTSI 规范，能正确协商音频编解码、带宽、媒体方向、preconditions、RTCP 参数。
【优先级】P0
【前置条件/SS 环境】
1. UE 已完成 IMS 注册。
2. UE 可发起 MO 呼叫或响应 MT 呼叫。
3. 抓包/日志能捕获 SIP INVITE/183/200 中的 SDP。
【测试步骤】
1. 捕获 INVITE 中 SDP offer。
2. 校验 session/media 级字段：`o=` / `c=` / `t=` / `m=audio`、`b=AS` / `b=RS` / `b=RR`、`a=rtpmap`（AMR/8000、AMR-WB/16000、telephone-event 等）、`a=fmtp`，以及媒体安全 `a=3ge2ae` / `a=crypto`（如支持）。
3. 捕获 183/200 OK 中 SDP answer。
4. 校验 answer 选择 UE offer 中的编码与 RTP profile。
5. 校验媒体方向 `sendrecv / sendonly / inactive` 与 preconditions 扩展。
6. 呼叫建立后核对实际 RTP 使用协商 payload type。
【预期判据】
- SDP 至少一个音频媒体；不出现无音频的异常 offer/answer。
- AMR `mode-set / mode-change-period / mode-change-neighbor / crc / robust-sorting / interleaving` 不出现（官方对呼叫建立默认的约束）。
- `max-red` 在允许范围；RS/RR 带宽符合 26.114 上限要求。
- 支持 precondition 时包含对应扩展；不支持时不包含。
- answer 合法，RTP 使用协商参数。
【通过标准】官方 34.229-1 12.12/12.13 TP Verdict：SDP 消息内容与字段符合官方 Specific Message Contents 才判 P/F。
【失败处理】记录失败步骤、抓包文件、UE 日志，关联缺陷 ID；当前字段级 PASS 只作研发行为支撑。

## 1. 目的 / 为什么

验证 UE 发起的 SDP offer 与收到的 SDP answer 符合 IMS MTSI 规范，能正确协商音频编解码、带宽、媒体方向、preconditions、RTCP 参数。

## 2. 官方骨架

- 主来源：`34.229-1` MO/MT 语音呼叫 TP 中的 SDP Specific Message Contents；`26.114` 6.2 SDP 要求。
- 正文行号证据：`_extract/34229-1e70_ascii.txt` line 4732-4805（MO without preconditions，SDP Specific Message Contents 见 line 4777-4802）；line 4838-4877（MT with preconditions，SDP Specific Message Content 见 line 4876-4877）。
- 对应 `24.229` 6.1.1/6.1.2/6.1.3 的 SDP 判据内联在 line 4672-4697、line 4754-4756、line 4849-4853；`26.114` 的 SDP/RTCP 要求内联在 line 4698-4708、line 4854-4862。

### 0.1 官方行号证据

- line 4732-4805：MO Voice Call Successful without preconditions 的 SDP Specific Message Contents。
- line 4777-4802：具体 `c=IN`、`b=AS`、`m=audio RTP/AVP`、`b=RS/RR`、`a=rtpmap` 等字段。
- line 4838-4877：MT Speech Call with preconditions 的 TP 与 SDP 引用。
- line 4672-4697 / 4754-4756 / 4849-4853：24.229 SDP/precondition 内联判据。
- line 4698-4708 / 4854-4862：26.114 的带宽/RTCP 上限内联要求。

## 3. 前置条件

- UE 已完成 IMS 注册。
- UE 可发起 MO 呼叫或响应 MT 呼叫。

## 4. 验证流程

1. 捕获 INVITE 中 SDP offer。
2. 校验 session/media 级字段：
   - `o=` / `c=` / `t=` / `m=audio`
   - `b=AS`、`b=RS`、`b=RR`
   - `a=rtpmap`（AMR/8000、AMR-WB/16000、telephone-event 等）
   - `a=fmtp`（按 codec 能力），禁用不允许参数
   - 媒体安全 `a=3ge2ae` / `a=crypto`（如支持）
3. 捕获 183/200 OK 中 SDP answer。
4. 校验 answer 选择 UE offer 中的编码与 RTP profile。
5. 校验预协商/媒体方向 `sendrecv / sendonly / inactive`。
6. 呼叫建立后核对实际 RTP 使用协商 payload type。

## 5. TP Verdict 判据（关键项）

- SDP 至少一个音频媒体；不出现无音频的异常 offer/answer。
- AMR `mode-set / mode-change-period / mode-change-neighbor / crc / robust-sorting / interleaving` 不出现（官方对呼叫建立默认的约束）。
- `max-red` 在允许范围；RS/RR 带宽符合 26.114 上限要求（RS<=4000bps、RR<=3000bps，见 line 4705-4708）。
- 支持 precondition 时包含对应扩展；不支持时不包含。
- answer 合法，且 RTP 使用协商参数。

## 6. 当前本地证据

```text
python work/tc023_sdp_negotiation.py
输入：outputs/tc12-tc13-calls-raw.log
结果：PASS（字段级）
```

## 7. 受限 / L2_REQUIRED

- 当前只校验字段级，不覆盖官方全部 `.3.2` 变体、媒体面加密/ECN 等条件。
- 完整官方判据需 `34.229-1` 具体 TP 正文 + `26.114` 对应版本与一致性仪表。

## 8. 执行命令

```text
python work/tc023_sdp_negotiation.py
```
