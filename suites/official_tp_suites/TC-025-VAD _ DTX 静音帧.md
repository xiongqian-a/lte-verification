# TC-025 VAD / DTX 静音帧

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`26.114 / 26.093 / 26.193 / 26.450 / 26.451`
- 官方章节/TP：`VAD/DTX`
- 映射等级：`partial`
- 当前证据层级：`LIMITED_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：标准来源已补齐；2026-09-14 真实长静音抓包经 bandwidth-efficient AMR ToC 复判，观测到 SID cadence 为 1000 帧，且 `NO_DATA` 被 RTP 实际传输 10 次。本地行为为 `PARTIAL`、标准断言为 `FAIL`，整体仍只能记 `LIMITED_PASS`，完整 SCR 与官方一致性仍受限。

## 1. 目的 / 为什么

验证 UE 在静音期按所选语音编解码产生/处理 DTX 静音帧（AMR/AMR-WB 的 SID、EVS DTX/SAD），且初始 SDP 的 dtx 参数符合 26.114 限制。

## 2. 官方骨架

- 来源：TS 26.114（MTSI SDP 控制）、TS 26.093 / 26.193（AMR/AMR-WB SCR）、TS 26.450 / 26.451（EVS DTX/SAD）
- 已抽取文本：`outputs/ts_26_extract/26093-e00.txt`、`26193-e00.txt`、`26450-e00.txt`、`26451-e00.txt`；`work/tc025-26114-pages37-42.txt`

### 2.1 26.093 / 26.193 / 26.450 / 26.451 原文行锚

来源文件行号基于 Python `splitlines()` 口径；只摘实际出现的正文，不扩展成官方一致性 Verdict。

| 规范 | 行号 | 原文要点 |
|---|---|---|
| 26.093 (AMR SCR) | 239-240 | 语音 burst 结束后，通常前七帧为 `SPEECH_GOOD` hangover；第八帧为 `SID_FIRST`，且 `SID_FIRST` 不包含语音数据。 |
| 26.093 (AMR SCR) | 243-244 | 少于 24 帧时可用上一 `SID_UPDATE`；`SID_FIRST` 之后每 8 帧生成一次 `SID_UPDATE`，首个 `SID_UPDATE` 在 `SID_FIRST` 后第三帧发送。 |
| 26.093 (AMR SCR) | 224 / 228 | `NO_DATA` 表示 Information Bit 与 Codec Mode 无有效内容，不应在接入网传输。 |
| 26.193 (AMR-WB SCR) | 203-204 | AMR-WB 同样在 hangover 后以 `SID_FIRST` 标记 talkspurt 结束，`SID_FIRST` 不含数据。 |
| 26.193 (AMR-WB SCR) | 207-208 | AMR-WB 的 `SID_UPDATE` 生成规则与 AMR 相同：每 8 帧一次，首个在 `SID_FIRST` 后第三帧。 |
| 26.193 (AMR-WB SCR) | 192 | AMR-WB `NO_DATA` 的说明与 AMR 一致。 |
| 26.450 (EVS DTX) | 118-119 | DTX 是 EVS 针对语音不活动降低平均速率的机制，用于降低 UE 能耗和改善网络容量。 |
| 26.450 (EVS DTX) | 124-127 | 默认 DTX 需要 TX 侧 SAD、噪声估计用于传输参数、RX 侧 CNG 生成舒适噪声。 |
| 26.451 (EVS VAD/SAD) | 67 | EVS 的 VAD 更准确称为 Signal Activity Detection（SAD）。 |
| 26.451 (EVS VAD/SAD) | 108 | SAD 输出布尔标志；1 表示活动信号，0 表示不活动信号（静音/背景噪声）。 |

2026-09-14 的长静音抓包经带宽高效 AMR ToC 复判后，得到 `ft=2` speech=218、`ft=15` `NO_DATA`=10、`ft=8` SID=4。SID 的 `sid_delta_ts=160000,160000`、`sid_delta_frames=1000,1000`，而 AMR 8 帧 cadence 预期为 `8 * 20 ms * 8000 Hz = 1280` RTP ticks。更关键的是，TS 26.093 行 229 明确 `NO_DATA` 不含有效信息且不应在接入网传输，本次抓包却实际发出了 10 个 `NO_DATA`。因此只能记为 `LIMITED_PASS`、`LOCAL_BEHAVIOR=PARTIAL`、`STANDARD_ASSERTION=FAIL`；J3-J5 的完整 `SID_FIRST/SID_UPDATE` 时序不能判定通过。

## 3. 前置条件

- UE 使用支持 VAD/DTX 的语音编解码。
- 具备媒体抓包或 codec 级静音帧观测能力。

## 4. 验证流程

1. J1：检查 SDP 初始 offer 是否含 dtx/dtx-recv（EVS 初始不得含）。
2. J2：确认实际编解码（AMR/AMR-WB/EVS），按对应标准判据。
3. J3/J4/J5：AMR 静音期应存在 hangover→SID_FIRST→SID_UPDATE 的 SCR 时序。
4. J6：EVS 上行 DTX 仅在网络命令后开启；下行始终处理。

## 5. TP Verdict 判据

- 存在真实语音帧/silence/DTX 证据。
- AMR no-data/DTX 帧只能给本地功能级 `LIMITED_PASS`；发现 SID 时必须继续校验 26.093 的 SID_UPDATE 8 帧 cadence。
- `NO_DATA` 不应在接入网传输；本次抓包实际发出 10 个 `NO_DATA`，因此标准断言必须记 `FAIL`。
- 当前 SID cadence 为 `160000` ticks / `1000` 帧，不符合 `1280` ticks / `8` 帧规则，因此不得断言完整 J3-J5 PASS。
- EVS 初始 offer 不得由终端引入 dtx。
- 最终一致性结论仍由仪表判 P/F。

## 6. 当前本地证据

本地证据：`work/tc025_vad_dtx.py --amr-stats "C:\标准例程\verification-evidence\tc025-longsilence-20260914\amr-stats.txt"` → `LIMITED_PASS`、`LOCAL_BEHAVIOR=PARTIAL`、`STANDARD_ASSERTION=FAIL`。

判定器自检同时包含合规正控（1280 ticks / 8 帧、`NO_DATA=0`，必须得到 `STANDARD_ASSERTION=PASS`）和真实违例负控（1000 帧、`NO_DATA=10`，必须得到 `STANDARD_ASSERTION=FAIL`）；自检 PASS 只证明判定器方向性正确，不是产品一致性 PASS。

证据摘要：

- 服务器目录：`/home/co1750/verification-evidence/tc025-vad-20260914-longsilence`
- 本地证据：`C:\标准例程\verification-evidence\tc025-longsilence-20260914\`
- 抓包：`call.pcap`，SHA-256 `776762EA6037FF1F3ED017CF90A4E3271A3A695781103AB9957BC6EFBCB3DC63`
- 统计：`amr-stats.txt`，SHA-256 `146D8F38697274B8F3492BB5EAB31F3ED5B25F160841C461BC58BB6D6DC62244`
- 时间线：`amr-timeline.txt`，SHA-256 `9169F1B282A3A98ABEF03F50946AF368B8F7598C9BBFF85F84998BCF9C0028BF`
- 媒体计数：`rtp_pt96_pkts=232`、speech `ft=2 count=218`、`ft=15 count=10`、`ft=8 count=4`
- SID 间隔：`sid_delta_ts=160000,160000`、`sid_delta_frames=1000,1000`；预期 AMR 8 帧 cadence 为 `1280` ticks
- `NO_DATA` 传输约束：`no_data_transmitted=10`，预期 `0`
- 会话日志：双方 AMR/8000、`VAD re-enabled`、`Call 0 state changed to CONFIRMED`

## 7. 受限 / L2_REQUIRED

- SID 已观测但 cadence 为 1000 帧，不符合 8 帧规则；`NO_DATA` 被实际传输 10 次，不能给出完整 SCR PASS。
- 完整 `SID_FIRST/SID_UPDATE` 时序、RX comfort-noise generation 和官方一致性 Verdict 仍为 `RESTRICTED/L2_PENDING`。
- 正式结论仍需能输出合规 SID/CN 的产品 codec 或一致性测试仪/检测机构。

## 8. 执行命令

```text
python work/tc025_vad_dtx.py --amr-stats "C:\标准例程\verification-evidence\tc025-longsilence-20260914\amr-stats.txt"
```
