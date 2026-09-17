# 套件运行入口与真实环境阻塞点对照

> 本文件只列当前可执行命令和真实环境映射，不是最终一致性执行记录。
>
> 相对路径 `work/...` 指
> `<legacy-workspace>\work`。执行前先进入
> `<legacy-workspace>`。

## 本地复跑命令

```text
# 一键全链路：生成机器可读库 + 完整性检查 + 自检 + 证据复跑 + 报告
python <repo>\run_official_suite.py

# 一键复跑所有判定脚本自检
python work/run_tc_selfchecks.py

# 一键复跑已固化的本地真实证据
python work/run_tc_evidence.py

# 核对 TS 36.523-1 TC-026~031 的 36.523-1 行号锚点
python work/verify_523_line_refs.py

# 核对 TS 36.508 通用测试环境表格行号锚点（4.5A.4.3-1 / 4.5A.6.3-1 / 4.5A.7.3-1 / 4.5A.26.3-1 / 4.4.3.3-1 / 4.8.3-1）
python work/verify_ts36508_refs.py

# 核对 34.229-1 V14.7/V14.8 版本边界，确认 Release 14 正文为何使用 V14.7.0
python work/verify_34229_version_boundary.py

# 从 36.523-1 官方步骤表生成 TC-026~031 的证据 Schema
python work/build_tc026_031_evidence_schema.py

# 评估可选的真实 SS/仪表证据；无 manifest 时保持 NOT_EXECUTED
python work/run_l1_evidence_adapter_026_031.py

# 验证 TC-026~031 适配器的官方/本地状态语义
python work/verify_l1_evidence_adapter_026_031.py

# 检查 <repo> 的官方 TP 套件文档是否齐备
python work/run_official_suite_checks.py

# 从套件文档重新生成机器可读 official_tp_library.json
python work/build_official_library.py

# 生成官方风格 markdown 报告（非一致性 Verdict）
python <repo>\report_factory.py

# 从注册表、机器可读用例库和本地证据 JSON 重新生成逐 TC 详细进度表
python work/gen_detailed_progress.py
```

详细进度表输出：

- `<repo>\92-验证例程详细进度总表-20260915.md`
- `<repo>\进度总表-最详细版-20260914.md`（兼容旧路径，内容同步）

## 已生成套件文档的 TC（全量 34）

所有 34 条 TC 均已有 `<repo>\official_tp_suites\TC-xxx.md`。每个文件都包含：目的、官方骨架、前置条件、验证流程、TP Verdict 判据、当前本地证据、受限/L2_REQUIRED、执行命令。

以下表格按“当前有本地执行入口”的 TC 列出可复跑入口；无入口的 TC 表示当前只到标准判据层（STANDARD_ALIGNED / RESTRICTED）。

| TC | 本地执行入口 | 当前结果 | L2 阻塞 |
|---|---|---|---|
| TC-001 | `run_tc_evidence.py` | PASS（字段级） | 真实 eNB/EPC 端到端 |
| TC-002 | `run_tc_evidence.py` | STANDARD_ALIGNED/单测注入 | 真实 EPC 触发 |
| TC-003 | `run_tc_evidence.py` | STANDARD_ALIGNED/单测注入 | 真实 EPC 触发 |
| TC-004 | `work/tc004_state_patch.py --selfcheck` | SELFCHECK PASS | 真实核心网注入 REJECT/Wait Timer |
| TC-005 | `python work/tc005_dual_pdn.py --ue ... --mme ... --smf ... --sgwc ... --ue-since ... --core-since ...` / `--selfcheck` | LIMITED_PASS：LOCAL_BEHAVIOR=PASS；internet EBI=5 + ims EBI=6，专用承载 EBI=7 linked 6 | IPv6/IPv4v6、method II P-CSCF discovery 逐字段、网络侧 additional PDN 释放/E1；官方 Verdict 需一致性 SS/仪表 |
| TC-006 | 无 | STANDARD_ALIGNED：36.523-1 8.2.1.8 已锚定 | 真实 RRC/eNB/SS 或一致性仪表 |
| TC-007 | 无 | STANDARD_ALIGNED：36.523-1 7.1.6.1/1a/2/3/4/5 已锚定 | 真实 RRC/eNB/SS 或一致性仪表；SPS 仅行为补充 |
| TC-008 | 无 | STANDARD_ALIGNED | 真实 eNB/EPC |
| TC-009 | 无 | STANDARD_ALIGNED | 真实多承载 + UL TFT |
| TC-010 | 无 | STANDARD_ALIGNED | 真实 RAN/EPC |
| TC-011 | `python runners/tc011_register_flow.py --selfcheck` / `--log evidence/external/tc12-tc13-calls-raw.log`；`python runners/tc011_ipsec_ss_sim.py --selftest --out-dir evidence/local/tc011-l1-20260916` | 基础 SIP：LIMITED_PASS；L1 仿真：`L1_LOCAL_SIMULATED` PASS（Annex C.2 Steps 4-11，HMAC-MD5-96 + HMAC-SHA-1-96 各 8/8）；OFFICIAL_VERDICT=INCONCLUSIVE | 真实内核 `xfrm`/ESP、真实 UE/SS、官方 SS Verdict |
| TC-012 | `python work/tc012_mo_call.py` | PASS（字段级） | 官方 SS/一致性仪表 |
| TC-013 | `python work/tc013_invalid_auth.py --selfcheck` | SELFCHECK PASS；真实 bad-key EXPECTED_FAIL | 真实 IMS/HSS 注入无效 AKA 挑战 |
| TC-014 | `python work/tc014_rereg.py --raw --log ...` | PASS/LIMITED_PASS | 1200/1800s 序列、IPSEC、PANI |
| TC-015 | `python work/tc015_restoration.py --log outputs/tc015-504-local-pty-20260910.log` | PASS（responder） | 真实 S-CSCF 504 端到端 |
| TC-016 | `python work/tc016_duplicate_register.py` | PASS | 无官方独立 TC |
| TC-017 | `python work/tc017_two_calls.py` | PASS | 官方 `.3.2` 子例 |
| TC-018 | `python work/tc018_malformed_register.py` | PASS | 无官方独立 TC |
| TC-019 | `python work/tc019_mt_call.py` | PASS（字段级） | 真实被叫/IMS 呼叫台 |
| TC-020 | `python work/tc020_hold_retrieve.py` | PASS（字段级） | 真实 MMTel/IMS |
| TC-021 | `python work/tc021_conference_refer.py` | PASS（字段级） | 真实 MMTel/IMS/一致性仪表 |
| TC-022 | `python work/tc022_audio_media.py` | PASS（字段级） | 官方媒体测量表/SS |
| TC-023 | `python work/tc023_sdp_negotiation.py` | PASS（字段级） | 官方 SDP `.3.2`/SS |
| TC-024 | `python work/tc024_long_stability.py` | PASS（131.221s） | 非强制独立一致性 TC |
| TC-025 | `python work/tc025_vad_dtx.py` / `--selfcheck` | LIMITED_PASS：LOCAL_BEHAVIOR=PARTIAL，STANDARD_ASSERTION=FAIL；合规正控 PASS / 真实违例负控 FAIL | 已观测 SID；SID cadence=1000 frames，NO_DATA=10；官方 SCR/一致性仍需真实媒体环境 |
| TC-026 | `build_tc026_031_evidence_schema.py` + adapter | SCHEMA_READY / ADAPTER_READY；无真实证据时 NOT_EXECUTED | 真实 eNB/EPC/SS |
| TC-027 | `build_tc026_031_evidence_schema.py` + adapter | SCHEMA_READY / ADAPTER_READY；无真实证据时 NOT_EXECUTED | 真实 aSRVCC/SS |
| TC-028 | `build_tc026_031_evidence_schema.py` + adapter | SCHEMA_READY / ADAPTER_READY；无真实证据时 NOT_EXECUTED | 真实 SIB2/RRC |
| TC-029 | `build_tc026_031_evidence_schema.py` + adapter | SCHEMA_READY / ADAPTER_READY；无真实证据时 NOT_EXECUTED | 真实 SIB2/RRC |
| TC-030 | `work/run_tc030_emergency_lab.sh` | 历史功能级 PASS；`151858` 因错误命名空间 INCONCLUSIVE；`155404` 在 phase5 命名空间复现功能级 PASS | 官方一致性 Verdict、紧急 PDN、emergency registration |
| TC-031 | `build_tc026_031_evidence_schema.py` + adapter | SCHEMA_READY / ADAPTER_READY；无真实证据时 NOT_EXECUTED | eCall/MSD/SLR/PSAP |
| TC-032 | `python work/tc032_error_codes.py` | PASS（responder） | 官方 `.3.2`/真实 IMS |
| TC-033 | `python work/tc033_timer_timeout.py` | PASS（本地黑盒） | 真实超时场景 |
| TC-034 | 无 | RESTRICTED | YD/T 编号/运营商清单 |

## 真实一致性环境缺口

- 36.523-1 模块①/④/⑤：真实 eNB/EPC/SS 或一致性测试仪（R&S / Anritsu / Keysight / 检测机构）。
- 34.229-1 IMS 用例：IMS System Simulator，不是 OpenIMSCore 模拟。
- TC-031：eCall/MSD/SLR/PSAP。
- TC-034：具体 YD/T 编号和运营商 VoLTE 入库清单。
- 官方终核文档：`36.508`（已提供并锚定） / `36.509` / `36.523-2` / `34.108` / `24.173`。

## TC-026~031 证据适配状态

- 官方步骤已解析为 `11` 个章节、`114` 个消息检查点、`22` 个 TP Verdict、`77` 个 Specific Message Contents 表。
- 当前没有 `official_tp_suites/_evidence/TC-026-031-evidence-manifest.json`。
- 当前适配结果：`OFFICIAL_PASS=0`、`OFFICIAL_FAIL=0`、`LOCAL_ONLY=0`、`NOT_EXECUTED=11`。
- 只有合格 SS/仪表/检测机构来源、完整 TP Verdict 和对应 artifact 齐备时，适配器才可能生成官方 P/F；本地日志不会自动升级为官方结论。

## 冻结清单与快照校验

```powershell
python <legacy-workspace>\work\build_final_manifest.py
python <legacy-workspace>\work\build_final_manifest.py --verify <standards-source>\standard-suite-20260915
```

该校验会检查相对路径、缺失文件、额外文件和 SHA256 差异；`__pycache__` 与 `FINAL_MANIFEST.sha256` 自身不参与清单。
