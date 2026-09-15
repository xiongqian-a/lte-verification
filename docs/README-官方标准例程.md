# 官方标准例程目录

> 定版日期：2026-09-15
> 目标：把当前 34 条功能 TC 的“验收标准”钉到 3GPP 官方 TP 骨架上，最大化后续第三方入网时与官方/运营商判例对齐的概率。

## 重要口径

1. 本目录不是最终一致性执行记录。
2. `LOCAL_PASS` 只代表研发/功能/字段行为符合预期，不等同 `36.523-1`、`34.229-1` 官方一致性 Verdict。
3. 一致性结论必须由一致性测试仪/检测机构按官方 TP 判 `P/F`。
4. 受限、缺失、部分条目不会伪造结果，统一标 `RESTRICTED` / `L2_REQUIRED`。

## 三层实现说明

本目录按三层落地，三层不能互相替代：

### 第 1 层：官方 TP 骨架

把功能 TC 对到具名官方规范/章节，写出目的、官方骨架、前置条件、验证流程、TP Verdict 判据和受限点。

现状：`official_tp_suites/` 已覆盖全部 34 条 TC 的标准套件文档；其中 32 条已有官方正文行号锚，28 条达到 `exact_line_ref`。TC-016/018 属于行为级或实现级验证，TC-034 依赖外部 YD/T 和运营商清单；这些差异已在文档和 `official_tp_registry.json` 中如实标记，不伪造独立官方 TC 或最终一致性 PASS。机器可读版见 `official_tp_library.json`，由 `work/build_official_library.py` 从套件文档与注册表生成。

### 第 2 层：可执行测试框架

把官方 TP 派生出的字段/行为判据做成本地脚本或测试台执行器，用于产出研发行为证据。

现状：`work/run_tc_selfchecks.py` 与 `work/run_tc_evidence.py` 可复跑；`work/run_official_suite_checks.py` 可检查套件文档是否齐备；`C:\标准例程\run_official_suite.py` 可一键串起生成库、完整性检查、自检、证据复跑和报告输出。

### 第 3 层：真实一致性执行环境

用一致性测试仪/检测机构按官方 TP 判 P/F。

现状：缺失。本地没有一致性仪表，也没有真实 eNB/EPC/IMS SS/eCall 等全套依赖，因此不能输出官方一致性 Verdict。

## 文件说明

| 文件 | 作用 |
|---|---|
| `official_tp_registry.json` | 功能 TC -> 官方规范/章节 -> 当前证据等级 -> 阻塞点 |
| `official_tp_library.json` | 从套件文档生成的机器可读用例库（preconditions / steps / verdicts / evidence） |
| `official_tp_suites/` | 每个 TC 的官方 TP 骨架、前置条件、步骤、判据、本地证据 |
| `run_official_suite.py` | 统一 runner：生成库 -> 完整性检查 -> 自检 -> 证据复跑 -> 报告 |
| `report_factory.py` | 生成官方风格 markdown 报告表，不代表一致性 Verdict |
| `THREE_LAYER_STATUS.md` | 每个 TC 的三层实现状态表 |
| `SUITE_RUNNERS.md` | 本地可执行命令与真实环境阻塞点对照 |
| `92-验证例程详细进度总表-20260915.md` | 逐 TC 详细总表：目的、官方依据、流程、正文行锚、当前证据和 L2 受限项 |
| `89-最终交付与汇报口径-20260915.md` | 面向管理汇报的最终交付结论、证据边界、剩余依赖和送审路线 |
| `90-明日汇报一页版-20260915.md` | 面向明日管理汇报的一页版结论、数字、边界和下一步 |
| `91-最终冻结清单与复核日志-20260915.md` | 冻结范围、实测命令、关键哈希、快照同步和交付边界 |
| `34.229-1版本裁定与证据边界-20260915.md` | 说明为什么 Release 14 IMS 正文主锚使用 V14.7.0，以及 V14.8.0 为什么不能重锚 |

## 当前覆盖

全量 34 条 TC 均已生成 `official_tp_suites/TC-xxx.md`。映射与证据等级见 `official_tp_registry.json` 和 `official_tp_audit.md`。

模块① 36.523-1：TC-001~010。
模块② IMS/SIP：TC-011~021（34.229-1 / 24.229 为主）。
模块③ 媒体：TC-022~025（34.229-1 SDP/媒体 TP + 26.114/26.093/26.193/26.450/26.451）。
模块④/⑤/⑥ 语音连续/接入控制/紧急：TC-026~031（36.523-1 13.4.3 / 13.5 / 11.2 / 11.3）。
模块⑦ 错误码/定时器：TC-032~033（34.229-1 / 24.229）。
模块⑧ 中国入网：TC-034（RESTRICTED，缺具体 YD/T 与运营商清单）。

## 如何使用

本文中的相对路径 `work/...` 指本地脚本目录
`C:\Users\co1750\Documents\Codex\2026-09-02\i\work`。执行相对命令前，先进入工作区：

```text
cd C:\Users\co1750\Documents\Codex\2026-09-02\i
```

1. 先看 `official_tp_registry.json` 找 TC 的当前证据等级和阻塞点。
2. 打开对应 `official_tp_suites/TC-xxx.md`，读官方骨架与验证流程。
3. 本地能跑的功能证据通过 `work/run_tc_selfchecks.py` 和 `work/run_tc_evidence.py` 复跑。
4. 缺真实环境/仪表/运营商标，不升级为最终 PASS。

可快速检查套件文档完整性：

```text
python work/run_official_suite_checks.py
```

一键复跑全链路：

```text
python C:\标准例程\run_official_suite.py
```

生成官方风格报告表：

```text
python C:\标准例程\report_factory.py
```

生成冻结哈希清单并校验归档快照：

```text
python work\build_final_manifest.py
python work\build_final_manifest.py --verify C:\11\523协议\standard-suite-20260915
```

## 下一步建议

- 以 `89-最终交付与汇报口径-20260915.md` 作为管理汇报入口。
- 明日汇报可直接使用 `90-明日汇报一页版-20260915.md`。
- 冻结和归档复核以 `91-最终冻结清单与复核日志-20260915.md` 与 `FINAL_MANIFEST.sha256` 为准。
- 本地能跑的 L0/L1 证据继续用 `run_official_suite.py` 回归，不把本地 PASS 升级为官方结论。
- 需要真实 eNB/EPC/IMS/SS/仪表的 TC 按 `official_tp_registry.json` 中 `blocker` 项接入 L2。
- TC-034 需要具体 YD/T 编号和运营商 VoLTE 入库清单后才能继续。
