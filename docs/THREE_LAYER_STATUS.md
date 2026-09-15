# 三层实现状态表

> 定版日期：2026-09-15
> 三层定义：
> - L0 官方 TP 骨架：官方规范/章节、目的、验证流程、TP 判据是否已经落到标准例程；
> - L1 可执行测试框架：是否已有脚本/测试台执行器可产出字段或行为证据；
> - L2 真实一致性执行环境：是否已由一致性测试仪/检测机构按官方 TP 判 P/F。
>
> 机器可读库：`official_tp_library.json`；统一 runner：`run_official_suite.py`。
>
> 版本边界：Release 14 IMS 正文主锚使用 `TS 34.229-1 V14.7.0`。V14.8.0 已把测试要求指向 Release 15，并将 `5 to 22` 与 Annex A-J 标为 Void；裁定见 `34.229-1版本裁定与证据边界-20260915.md`。

## 状态值

- `Y`：已有且可复跑/已执行；
- `partial`：部分覆盖，仍有变体或环境缺口；
- `no`：未做；
- `RESTRICTED`：缺外部依赖，不能输出最终一致性结论。

## 全量状态

| TC | L0 官方 TP 骨架 | L1 可执行测试框架 | L2 真实一致性环境 |
|---|---|---|---|
| TC-001 | Y：official_tp_suites/TC-001 | run_tc_evidence 汇总 | RESTRICTED：真实 eNB/EPC 缺 |
| TC-002 | Y：official_tp_suites/TC-002 | 单测注入/字段证据 | RESTRICTED：真实 EPC 触发缺 |
| TC-003 | Y：official_tp_suites/TC-003 | 单测注入/字段证据 | RESTRICTED：真实 EPC 触发缺 |
| TC-004 | Y：official_tp_suites/TC-004 | tc004 本地单测 helper | RESTRICTED：真实核心网注入 REJECT/Wait Timer 缺 |
| TC-005 | Y：official_tp_suites/TC-005 | Y：`tc005_dual_pdn.py`；LOCAL_BEHAVIOR=PASS / LIMITED_PASS（internet EBI=5 + ims EBI=6，专用承载 EBI=7 linked 6） | RESTRICTED：IPv6/IPv4v6、method II P-CSCF discovery 逐字段、网络侧释放/E1；官方 Verdict 需 SS/仪表 |
| TC-006 | Y：36.523-1 8.2.1.8，`.3.2/.3.3` 已入套件 | no | RESTRICTED：真实 RRC/eNB/SS 或一致性仪表 |
| TC-007 | Y：36.523-1 7.1.6.1/1a/2/3/4/5，`.3.2/.3.3` 已入套件 | no | RESTRICTED：真实 RRC/eNB/SS 或一致性仪表；SPS 仅行为补充 |
| TC-008 | Y：official_tp_suites/TC-008 | no | RESTRICTED：真实 eNB/EPC |
| TC-009 | Y：official_tp_suites/TC-009 | no | RESTRICTED：真实多承载 + UL TFT |
| TC-010 | Y：official_tp_suites/TC-010 | no | RESTRICTED：真实 RAN/EPC |
| TC-011 | Y：套件文档已生成 | Y：tc011_register_flow | RESTRICTED：官方 SS `.3.2` 未跑 |
| TC-012 | Y：套件文档已生成 | Y：tc012_mo_call | RESTRICTED：官方 SS/一致性仪表 |
| TC-013 | Y：套件文档已生成 | Y：tc013_invalid_auth 自检；真实 bad-key EXPECTED_FAIL | RESTRICTED：真实 IMS/HSS 注入无效挑战 |
| TC-014 | Y：套件文档已生成 | Y：tc014_rereg / LIMITED_PASS | RESTRICTED：1200/1800s 序列、IPSEC、PANI |
| TC-015 | Y：套件文档已生成 | Y：tc015_restoration 本地 responder PASS | RESTRICTED：真实 S-CSCF 504 端到端 |
| TC-016 | Y：official_tp_suites/TC-016（行为级） | Y：tc016_duplicate_register | 无官方独立一致性 TC |
| TC-017 | Y：official_tp_suites/TC-017 | Y：tc017_two_calls | RESTRICTED：官方子例完整执行 |
| TC-018 | Y：official_tp_suites/TC-018（行为级） | Y：tc018_malformed_register | 无官方独立一致性 TC |
| TC-019 | Y：official_tp_suites/TC-019 | Y：tc019_mt_call | RESTRICTED：真实被叫/IMS 呼叫台 |
| TC-020 | Y：套件文档已生成 | Y：tc020_hold_retrieve | RESTRICTED：真实 MMTel/IMS 端到端 |
| TC-021 | Y：套件文档已生成 | Y：tc021_conference_refer / conference_join | RESTRICTED：真实 MMTel/IMS/一致性仪表 |
| TC-022 | Y：套件文档已生成 | Y：tc022_audio_media | RESTRICTED：官方媒体测量表/SS |
| TC-023 | Y：套件文档已生成 | Y：tc023_sdp_negotiation | RESTRICTED：官方 SDP `.3.2` 子例/SS |
| TC-024 | Y：official_tp_suites/TC-024 | Y：tc024_long_stability（长稳 PASS） | RESTRICTED：非强制独立一致性 TC |
| TC-025 | Y：official_tp_suites/TC-025 | Y：tc025_vad_dtx（LIMITED_PASS；LOCAL_BEHAVIOR=PARTIAL；STANDARD_ASSERTION=FAIL；合规正控 PASS / 真实违例负控 FAIL 自检通过） | RESTRICTED：已观测 SID、SID cadence=1000 frames、NO_DATA=10；真实 SID/CN 周期、官方 SCR 与一致性 Verdict 仍需仪表环境 |
| TC-026 | Y：official_tp_suites/TC-026 + 11-section evidence schema | SCHEMA_READY / ADAPTER_READY；当前 2/2 章节 NOT_EXECUTED | RESTRICTED：真实 eNB/EPC/SS |
| TC-027 | Y：official_tp_suites/TC-027 + 11-section evidence schema | SCHEMA_READY / ADAPTER_READY；当前 2/2 章节 NOT_EXECUTED | RESTRICTED：真实 aSRVCC/SS |
| TC-028 | Y：official_tp_suites/TC-028 + 11-section evidence schema | SCHEMA_READY / ADAPTER_READY；当前 2/2 章节 NOT_EXECUTED | RESTRICTED：真实 SIB2/RRC |
| TC-029 | Y：official_tp_suites/TC-029 + 11-section evidence schema | SCHEMA_READY / ADAPTER_READY；当前 1/1 章节 NOT_EXECUTED | RESTRICTED：真实 SIB2/RRC |
| TC-030 | Y：official_tp_suites/TC-030，`36.523-1 11.2.1` 正文/TP/.3.2/.3.3 已锚定 | Y：历史 112/110/119/120 功能级 PASS；`151858` 因错误命名空间 INCONCLUSIVE；`155404` 在 phase5 命名空间复现功能级 PASS（REGISTER 401->200、INVITE 100->200、ACK、CONFIRMED、RTP、BYE 200） | RESTRICTED：官方一致性 Verdict、紧急 PDN、emergency registration |
| TC-031 | Y：official_tp_suites/TC-031 + 11-section evidence schema | SCHEMA_READY / ADAPTER_READY；当前 2/2 章节 NOT_EXECUTED | RESTRICTED：eCall/MSD/SLR/PSAP 缺 |
| TC-032 | Y：套件文档已生成 | Y：tc032_error_codes | RESTRICTED：官方 `.3.2` 子例/真实 IMS |
| TC-033 | Y：套件文档已生成 | Y：tc033_timer_timeout | RESTRICTED：无独立官方 TC，真实超时场景缺 |
| TC-034 | Y：official_tp_suites/TC-034（RESTRICTED） | no | RESTRICTED：缺 YD/T 编号和运营商清单 |

## 改进优先级

- `36.508` V14.3.0 已提供并锚定 TC-026~031 的通用测试环境表格；`verify_ts36508_refs.py` 会检查这些锚点。
- `TC-026~031` 已具备官方步骤 Schema 与 L1/L2 证据适配器；当前 `11/11 NOT_EXECUTED`，因为缺真实 SS/仪表日志。

1. L0 全量 34 条套件文档已生成并通过完整性检查；当前 28 条为 `exact_line_ref`，其余按行为级、规范支撑或外部依赖如实标注。
2. TC-031 的 `36.508 4.5A.27` 已按 V18.6.0 正文终核；继续补齐 TC-034 的 YD/T 编号与运营商清单。
3. L1 继续核实现有脚本的断言与官方 `.3.2` 子例映射；TC-024/025/033/016/018 保持各自的非独立一致性 TC 口径。
4. L2 按 `official_tp_registry.json` 的 `blocker` 接入合格 SS/仪表/检测机构证据，不把本地 PASS 升级成官方一致性结论。
