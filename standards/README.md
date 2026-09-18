# 标准原文交接包

> 用途：随本私有仓库一起交付当前验证套件已经收集到的 3GPP/ETSI 标准原文和
> 直接引用的 IETF RFC，
> 方便同事不依赖原工作目录、不重新寻找文件，直接核对 TC 文档中的条款和行锚。
>
> 边界：这里包含的是“当前套件已经收到并能合法用于内部交接的原文”，不是
> 3GPP 全部规范，也不自动构成原文再分发授权。

## 1. 使用原则

- 本目录只随私有内部仓库交付。不要公开仓库、公开标准 PDF/DOC/DOCX，或把
  标准原文转发到组织外部，除非已经确认再分发权限。
- 运行 `run_official_suite.py`、`--doctor` 和 `--colleague-replay` 不需要
  打开标准原文，也不修改原文。
- 人工复核 TC 条款、消息内容、TP 步骤和行号时，应优先使用本目录对应版本的
  原文，不要用其他 Release 的章节内容替代。
- `manifest.json` 记录每份文件的相对路径、大小和 SHA256。仓库不会在运行时
  自动替换缺失或哈希不一致的文件。
- 原始 PDF/DOC/DOCX 的行号会受提取工具、分页和换行归一化方式影响。TC 文档
  中的行号是在指定版本和指定提取口径下产生的；版本或提取工具变化时必须重新
  核对，不能直接沿用。

## 2. 快速校验

在仓库根目录执行：

```text
python -X utf8 runners/verify_standards_bundle.py
```

成功结果：

```text
STANDARDS BUNDLE: PASS
FILES: 45
TOTAL BYTES: 144416074
```

如果文件缺失、大小变化或 SHA256 不一致，脚本会列出具体文件并返回非零状态。
这表示当前 checkout 不能作为同一份标准原文快照使用，应先恢复正确文件，不能把
校验失败报告成通过。

重新生成 manifest 只应用于更新标准包以后，并且必须由维护人明确知道哪些文件
发生了版本变化：

```text
python -X utf8 runners/build_standards_manifest.py
python -X utf8 runners/verify_standards_bundle.py
```

## 3. 当前包含的文件

当前包为 **45 个文件、39 个规范目录、144416074 字节**。完整路径、版本、大小和
SHA256 以 `official/manifest.json` 为准。按用途分组如下：

| 分组 | 已纳入规范/版本 | 主要用途 |
|---|---|---|
| LTE/EPC 官方 TP 主骨架 | `36.523-1 V14.3.0`、`36.523-2 V14.3.0` | LTE/EPC TC 编号、Pre-test、Procedure、Expected Sequence 和 Verdict。 |
| IMS 官方 TP 主骨架 | `34.229-1 V14.7.0 / V14.8.0`、`34.229-2 V14.8.0` | IMS 注册、呼叫、媒体、hold、会议、REFER 和异常行为。 |
| IMS/SIP 协议 | `24.229 V14.17.0`、`24.147 V14.1.0`、`24.173 V14.3.0`、`24.237 V14.7.0`、`24.341 V14.0.0`、`24.605 V14.0.0`、`24.610 V14.0.0`、`24.628 V14.10.0`、`24.629 V14.0.0` | SIP UE 过程、MMTel、会议、Hold、REFER/3pcc 和恢复。 |
| NAS/核心网 | `22.101 V14.9.0`、`23.003 V14.7.0`、`23.060 V14.8.0`、`23.401 V14.11.0`、`24.008 V14.9.0`、`24.301 V18.6.0`、`29.228 V14.6.0` | EPS 架构、PDN/承载、ESM reject、cause、T3346 和 HSS/用户数据。 |
| 媒体/eCall | `26.093 V14.0.0`、`26.114 V14.12.0`、`26.193 V14.0.0`、`26.267 V14.0.0`、`26.450 V14.0.0`、`26.451 V14.0.0` | MTSI SDP/RTP/RTCP、AMR/EVS、DTX/VAD/SID 和 eCall 媒体。 |
| 安全 | `33.102 V14.1.0`、`33.203 V14.3.0`、`33.401 V14.6.0` | AKA、IMS AKA、无效 MAC/SQN/AUTS 和 EPS 安全。 |
| RAN/测试环境 | `34.108 V11.14.0 / V14.2.0`、`36.306 V14.12.0`、`36.323 V14.5.0`、`36.331 V14.18.0`、`36.508 V14.3.0 / V18.6.0`、`36.509 V14.0.0`、`44.018 V14.6.0` | 通用测试过程、能力、RRC、PDCP、测试配置、闭环控制和 GERAN 消息。 |
| GERAN 派生依赖 | `51.010-1 V14.10.0` | `TC-026`/`TC-031` 中 `40.1.1`、`40.2.4.33` 等派生路径的 Release 14 原文。 |
| IETF SIP 外部依赖 | `RFC 3261`、`RFC 3515` | SIP 事务/定时器以及 REFER/NOTIFY 直接来源；不是 3GPP 规范。 |

当前 manifest 中保留多个版本是有意的：`34.229-1 V14.7.0` 是现有 IMS 行锚主版本，
`V14.8.0` 用于差异核对；`36.508 V14.3.0` 是当前测试配置主版本，`V18.6.0` 只作
后续差异参考；`34.108` 的两个版本服务于不同历史锚点。不要跨版本直接复用行号。

## 4. 当前尚未纳入的标准依赖

在仓库现有 `suites/` 和 `registry/` 的直接引用范围内，已经被引用的 3GPP/ETSI
TS 和两份 RFC 都已纳入当前标准包。仍不能宣称“包含 3GPP 全部规范”：

| 依赖 | 影响 |
|---|---|
| YD/T 和运营商企标 | TC-034 送测和入库映射。 |
| 3GPP 未直接被本套件引用的其他规范 | 如果后续新增 TC 或审计引用范围扩大，必须继续补原文并重新核会话，不能拿相近规范替代。 |

缺失项的 TC 状态必须保持 `RESTRICTED`、`NOT_EXECUTED`、`PARTIAL` 或
`L2_REQUIRED`，不能因为已经有一份相近标准就把判据说成完整。

## 4.1 原文件路径和本机路径无关

标准包使用仓库相对路径。`manifest.json` 的 `path` 字段始终从仓库根目录开始，
例如 `standards/official/36.523-1/...`。校验脚本通过
`Path(__file__).resolve().parent.parent` 找到仓库根目录，因此：

- Windows 放在 `C:\任意目录\lte-verification` 可以运行；
- Linux 放在 `/opt/lte-verification` 或同事自己的 home 目录可以运行；
- clone 目录名不叫 `lte-verification` 也可以运行；
- 不需要修改 `manifest.json`、TC 文档或脚本中的绝对路径。

如果校验失败，应恢复文件或重新 clone，不要手工改 manifest 的哈希来“消除”失败。

## 5. 缺少服务器软件时怎么办

标准原文包与运行环境是两件事：

| 目标 | 最低依赖 | 是否需要 IMS/EPC/eNB/仪表 |
|---|---|---|
| 核对标准原文和 TC 映射 | Git、Python 3.10+、本目录原文 | 不需要 |
| 复现仓库已保存的黄金日志 | Git、Python 3.10+ | 不需要 |
| 重新生成新的 DUT 端到端日志 | 目标 DUT、构建环境、实时 eNB/EPC/IMS、媒体和抓包工具 | 需要 |
| 得到 36.523-1/34.229-1 官方 Verdict | 合格 SS、仪表或检测机构 | 必须 |

先运行：

```text
python -X utf8 runners/environment_doctor.py
```

如果服务器没有 IMS、EPC、eNB 或 pjsua，`--doctor` 会明确显示相应能力缺失。
仓库不会自动安装或伪造这些系统。缺少这些软件时仍可完成标准核对和历史证据
复跑，但不能把它们写成一次新的端到端执行。

具体处理原则：

| 缺失项 | 只做交接/标准核对 | 要重新跑 L1 fresh-DUT |
|---|---|---|
| Python | 运行 `bootstrap.cmd` 或 `bootstrap.sh`，由启动器尝试准备 Python 3.10+。 | 同样先补齐 Python。 |
| Git | 安装 Git，或使用完整 Git bundle/含 `.git` 的压缩包。 | 强烈建议安装 Git，以便记录 DUT 和新证据对应的提交。 |
| pjsua | 不影响 L0；本地黄金证据仍可复跑。 | 安装 PJSIP/pjsua，或使用仓库对应测试环境已有的客户端。 |
| Open5GS、EPC、eNB/srsRAN | 不影响标准校验和黄金证据复跑。 | 必须准备真实测试床；不同发行版、内核和 SDR 的安装方式不同，仓库不提供伪一键部署。 |
| IMS/OpenIMSCore | 不影响 L0；只缺真实 DUT/SS 证据。 | 需要可用 IMS 测试床、ISIM、鉴权参数和网络地址。 |
| R&S/Anritsu/Keysight/实验室 | 仍可完成 L0/L1 文档和本地证据复核。 | 这是产生 `OFFICIAL_PASS/FAIL` 的唯一合法来源。 |

对于 Linux 服务器，可以让管理员按发行版安装基础工具；例如 Debian/Ubuntu 常见
包名包括 `git`、`python3`、`tshark`、`ffmpeg`。Open5GS、srsRAN、IMS 不应通过
猜命令安装：它们需要匹配的内核、网卡、SDR、PLMN、SIM 和配置，错误安装比缺环境
更容易制造不可信结果。
