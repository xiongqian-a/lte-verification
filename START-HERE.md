# 拿到仓库后怎么使用

> 适用对象：第一次拿到本仓库的同事、测试人员和复核人。
>
> 目标：在不猜测、不伪造证据的前提下，先跑通仓库本地基线，再决定是否进入
> L1 测试床或 L2 一致性仪表环境。

完整的一键运行、目录和文件职责、输入输出图谱、证据查看、结果口径、
fresh-DUT 证据隔离、私有仓库权限、离线交接和常见问题，统一见
[`docs/104-仓库完整使用说明书-20260918.md`](docs/104-仓库完整使用说明书-20260918.md)。

系统学习、关键案例复盘、标准到代码的思维模型，以及面试口述和追问回答，
见 [`docs/105-实习期LTE-IMS自研协议栈验证体系开发与学习总结-20260918.md`](docs/105-实习期LTE-IMS自研协议栈验证体系开发与学习总结-20260918.md)。

需要查“所有套件、runner、原始证据和服务器测试床分别放在哪里”，见
[`docs/102-服务器与本机路径总表-20260918.md`](docs/102-服务器与本机路径总表-20260918.md)。
需要按类别、信号流、进程和 TC 查服务器路径，见
[`docs/103-服务器文件路径逻辑总表-20260918.md`](docs/103-服务器文件路径逻辑总表-20260918.md)。
参考服务器账号根目录的完整目录与符号链接清单见
[`docs/102a-服务器完整目录清单-20260918.txt`](docs/102a-服务器完整目录清单-20260918.txt)。

## 0. 先记住结论边界

本仓库可以做三件不同的事：

| 层级 | 做什么 | 需要什么环境 | 能得到的结论 |
|---|---|---|---|
| L0 | 检查标准映射、套件文档、脚本和报告是否完整 | Git + Python 3.10+ | `STANDARD_ALIGNED` / `SELFCHECK_PASS` |
| L1 | 复跑已固化的本地日志、单测、抓包或模拟器证据 | Git + Python 3.10+；实时测试还要核心网/IMS/测试床 | `LOCAL_PASS` / `LIMITED_PASS` / `RESTRICTED` |
| L2 | 由合格 SS、一致性仪表或检测机构执行官方 TP | R&S、Anritsu、Keysight、实验室或等价合格环境 | `OFFICIAL_PASS` / `OFFICIAL_FAIL` |

必须遵守以下边界：

- `UNIFIED RUNNER RESULT: OK` 只表示仓库基线可复现，不是官方一致性 PASS。
- 本地日志 PASS 不是 `36.523-1` 或 `34.229-1` 官方一致性。
- Open5GS、srsRAN、OpenIMSCore、pjsua 只能提供 L1 证据，不能替代 L2 仪表。
- 缺核心网、IMS、SS、仪表或运营商输入时，结果应标为 `RESTRICTED` 或
  `NOT_EXECUTED`，不能改写为 PASS。

## 1. 准备环境

最低要求：

- Git
- Python 3.10 或更高版本

检查版本：

```sh
git --version
python --version
python3 --version
```

Windows 如果没有 Python，可以运行仓库自带的 bootstrap。Linux/macOS 会按当前
系统可用的包管理器尝试安装 Python；若自动安装条件不满足，脚本会给出明确错误，
不会继续用不兼容的解释器运行。

本仓库当前不要求安装第三方 Python 包，不需要先执行 `pip install`。

仓库还带有当前套件已经收到的标准原文包 `standards/official/`。它不是 3GPP
全部规范，只包含当前可以用于内部交接的原文；缺失依赖和版本差异记录在
`standards/README.md`。

## 2. 获取仓库

### 2.1 使用 HTTPS

```sh
git clone https://github.com/xiongqian-a/lte-verification.git
cd lte-verification
```

私有仓库使用 HTTPS 时，系统会要求 GitHub 凭据或凭据管理器授权。

### 2.2 使用 SSH

前提是 GitHub 账号或 Deploy Key 已经配置完成：

```sh
git clone git@github.com:xiongqian-a/lte-verification.git
cd lte-verification
```

### 2.3 记录本次复跑提交

同事复跑时先记录本次使用的提交，确保大家得到的是同一版结果：

```sh
git checkout <完整 commit hash>
git rev-parse HEAD
git status --short --branch
git remote -v
```

仓库路径和用户名不应影响运行。不要手工修改脚本中的绝对路径。

### 2.4 检查标准包

```sh
python -X utf8 runners/verify_standards_bundle.py
```

通过标志：

```text
STANDARDS BUNDLE: PASS
FILES: 45
TOTAL BYTES: 144416074
```

失败通常表示文件缺失、大小变化或 SHA256 不一致。不要忽略失败后继续把同一
checkout 当成固定标准快照。

## 3. 第一次运行

### 3.1 Windows 一键运行

在仓库根目录执行：

```powershell
.\bootstrap.cmd
```

如果本机已经有 Python 3.10+，也可以直接执行：

```powershell
python -X utf8 run_official_suite.py
```

### 3.2 Linux/macOS 一键运行

```sh
chmod +x bootstrap.sh
./bootstrap.sh
```

如果本机已经有 Python 3.10+：

```sh
python3 -X utf8 run_official_suite.py
```

### 3.3 成功标志

命令最后必须出现：

```text
UNIFIED RUNNER RESULT: OK
Generated reports: <仓库路径>/generated
```

随后检查仓库是否仍干净：

```sh
git status --short
git diff --exit-code
```

正常结果是：

- `git status --short` 没有输出
- `git diff --exit-code` 返回码为 0
- 没有把本地结果写成 `OFFICIAL_PASS`

再执行一次专门的便携性检查：

```sh
python -X utf8 runners/verify_portable_install.py
python -X utf8 runners/verify_portable_install.py --full
```

静态检查必须输出 `PORTABLE INSTALL: PASS (STATIC)`；完整检查必须输出
`PORTABLE INSTALL: PASS (FULL)` 和
`UNIFIED RUNNER: PASS FROM UNRELATED CWD`。

如果只想检查标准、脚本和报告，不重放历史证据，可以执行：

```sh
python -X utf8 run_official_suite.py --skip-evidence
```

### 3.4 先检查本机缺少什么

```sh
python -X utf8 runners/environment_doctor.py
```

或：

```powershell
.\bootstrap.cmd --doctor
```

重点看 `GOLDEN_REPLAY_READY`、`FRESH_DUT_ENV_MISSING` 和
`OFFICIAL_SS_REQUIRED`。缺少 Docker、Open5GS、srsRAN、pjsua、抓包或媒体工具，
不会阻止已提交证据的复跑，但会阻止新的实时端到端执行。

## 4. 一键 runner 实际做了什么

默认 runner 会按顺序执行：

1. 检查关键入口、执行位、CI 覆盖和机器绝对路径。
2. 从 registry 和套件文档生成机器可读官方 TP 库。
3. 重建验证架构页面。
4. 校验 34 条套件元数据。
5. 重建详细进度表。
6. 检查 34 条套件文档必需章节。
7. 执行判定脚本的正控和负控自检。
8. 复跑仓库中已固化的本地证据。
9. 检查 TC-026 到 TC-031 的官方边界保护。
10. 生成官方步骤和 TP Verdict 的证据 Schema。
11. 读取可选 L2 证据清单；没有合格证据时保持 `NOT_EXECUTED`。
12. 校验 L2 adapter 的语义，防止本地证据被误升级成官方判定。
13. 生成官方风格状态报告，但明确标注它不是官方证书。

主要输出目录：

```text
generated/84-本地证据复跑矩阵-20260914.md
generated/85-验证例程全量自检状态-20260914.md
generated/86-TC026-031-证据Schema与L1适配器-20260914.md
generated/92-验证例程详细进度总表-20260915.md
generated/official_report.md
```

每份报告都要看结论边界，不要只看标题里的 PASS。

## 5. 结果词怎么读

| 结果 | 含义 |
|---|---|
| `LOCAL_PASS` | 本地日志、抓包或单测满足脚本判据，仅代表本地实现证据 |
| `LIMITED_PASS` | 核心本地行为已通过，但仍有变体、字段或真实环境未覆盖 |
| `SELFCHECK_PASS` | 判定脚本本身可用，正控和负控按预期触发 |
| `STANDARD_ALIGNED` | 官方章节、步骤和判据已对齐，但完整官方流程尚未执行 |
| `RESTRICTED` | 缺标准、网络、仪表、运营商数据或测试权限，不能判 PASS/FAIL |
| `NOT_EXECUTED` | 当前没有该官方章节的合格证据 |
| `OFFICIAL_PASS` / `OFFICIAL_FAIL` | 只能由合格 SS、仪表或检测机构生成 |

重点：`LIMITED_PASS` 不是完整 PASS；`RESTRICTED` 不是 FAIL；`NOT_EXECUTED`
不是 PASS，也不是 FAIL。

## 6. 单条 TC 怎么跑

每条 TC 的标准入口都在：

```text
suites/official_tp_suites/TC-xxx-*.md
```

阅读顺序：

1. 看元数据和标准来源。
2. 看测试目的和官方骨架。
3. 看前置条件与测试环境。
4. 看官方步骤和 Expected Sequence。
5. 看 TP Verdict、字段判据和允许变体。
6. 看当前证据和明确的 blocker。
7. 执行文档中“本地执行命令”一节的脚本。
8. 检查退出码、脚本输出和对应原始日志。

不要只看脚本最后打印的 `PASS`。必须同时确认：

- checker 有正控和负控
- 输入日志或抓包来源可追溯
- checker 判据能在套件文档中找到对应标准条款
- 受限项没有被静默升级成官方 PASS

### TC-011 示例

查看套件：

```sh
python -X utf8 -c "from pathlib import Path; print(Path('suites/official_tp_suites/TC-011-IMS初始注册.md').read_text(encoding='utf-8'))"
```

或直接用编辑器打开：

```text
suites/official_tp_suites/TC-011-IMS初始注册.md
```

运行基础注册判定脚本自检：

```sh
python -X utf8 runners/tc011_register_flow.py --selfcheck
```

使用仓库内固化日志复跑：

```sh
python -X utf8 runners/tc011_register_flow.py --log evidence/external/tc12-tc13-calls-raw.log
```

运行 TC-011 的 L1 IPsec、SUBSCRIBE 和 NOTIFY 仿真自检：

```sh
python -X utf8 runners/tc011_ipsec_ss_sim.py --selftest --out-dir evidence/local/tc011-l1-20260916
```

这些命令对应的是 L1 本地/仿真证据。TC-011 仍不能给出官方 SS Verdict；
真实 IPsec SA、真实 UE/SS 和正式一致性结论仍需合格环境。

## 7. 同事拉取后如何复跑并确认结果

同事拿到仓库后，不需要配置服务器、核心网、项目路径或 Python 依赖。只要本机有
Git 和仓库读取权限，按下面的命令复跑即可。一条命令会先准备 Python（如果本机
缺失），然后直接生成同事复跑报告。

### Windows PowerShell

```powershell
.\bootstrap.cmd --colleague-replay
```

### Linux/macOS

```sh
chmod +x bootstrap.sh
./bootstrap.sh --colleague-replay
```

如果本机已经有 Python 3.10+，也可以直接运行下面的等价命令。

### Windows PowerShell（已装 Python）

```powershell
$commit = git rev-parse HEAD
python -X utf8 runners/colleague_replay_verification.py `
  --expected-commit $commit `
  --out-dir outputs/colleague-replay
```

### Linux/macOS（已装 Python）

```sh
COMMIT=$(git rev-parse HEAD)
python3 -X utf8 runners/colleague_replay_verification.py \
  --expected-commit "$COMMIT" \
  --out-dir outputs/colleague-replay
```

成功输出必须包含：

```text
COLLEAGUE REPLAY: PASS
TC011_INVARIANTS: PASS
OFFICIAL_VERDICT: null
```

这里的 `PASS` 表示“同事复跑成功、固定提交匹配、仓库内部一致性检查通过”，
仍然不是官方一致性结论。

复跑报告会写入：

```text
outputs/colleague-replay/
```

这条路径会复跑仓库中已经提交的本地日志、抓包和 checker。它不会重新连接
eNB/EPC/IMS，也不会生成一份新的现场日志。因此同事得到的是“与你这版仓库
一致的复现结果”，不是“同事重新做了一遍端到端测试”。

复跑结果建议按以下格式反馈：

```text
仓库可复现性：PASS / FAIL
标准映射一致性：PASS / PARTIAL / FAIL
本地证据可信度：PASS / PARTIAL / FAIL
官方一致性：NO_OFFICIAL_VERDICT
复跑提交：
操作系统和 Python 版本：
执行命令：
报告路径：
发现的问题：
不能复现或不能核对的项目：
```

## 8. 核心网、IMS 和仪表怎么使用

### 8.1 只跑本地基线

不需要 eNB、EPC、IMS、HSS、SS 或仪表：

```sh
python -X utf8 run_official_suite.py
```

它会复跑仓库中已经固化的证据，不会连接外部测试台。

### 8.2 运行 L1 实时测试

如果要重新产生日志或抓包，必须由外部环境提供：

- eNB 或 srsRAN
- EPC 或 Open5GS
- IMS/OpenIMSCore 或等价 L1 IMS
- pjsua 或目标 UE 测试程序
- 测试 SIM/ISIM、APN/DNN、鉴权参数和网络地址

仓库不会自动启动这些服务，也不会把它们伪装成官方 SS。实时测试通常需要
目标机器的日志路径、接口地址和测试参数。具体参数以每条 TC 套件文档的第 8 节
为准。

### 8.3 进入 L2 官方测试

L2 必须使用合格 SS、仪表或检测机构。L2 结果应通过 L2 evidence manifest
接入，不能从 L1 日志自动升级。没有实际 Verdict 时，适配器保持
`NOT_EXECUTED`、`INCONCLUSIVE` 或 `RESTRICTED`。

## 9. 环境不一致时怎么办

先记录环境指纹：

```sh
git rev-parse HEAD
git status --short
python --version
python3 --version
```

Linux 再记录：

```sh
uname -a
cat /etc/os-release
```

Windows 再记录：

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
```

判断规则：

- L0 和 L1 复跑只要 Python 3.10+，在 Windows、Linux、macOS 上应得到相同结果。
- 如果 `git diff --exit-code` 失败，说明不同环境破坏了可复现性，应修脚本，
  不应修改报告掩盖差异。
- 如果运行实时 L1，优先使用统一 Linux 测试床，不要在多台个人电脑上各自重建
  一套核心网。
- L2 不接受“差不多”的环境。必须使用合格仪表或检测机构。

## 10. 常见故障

### Python 版本低于 3.10

表现：

```text
Python 3.10 or later is required
```

处理：安装 Python 3.10+，重新打开终端后重试。

### 私有仓库认证失败

表现：

```text
Authentication failed
Repository not found
Permission denied (publickey)
```

处理：

- HTTPS：重新登录 GitHub 或配置凭据管理器。
- SSH：确认公钥已加入 GitHub，或 Deploy Key 已启用。
- 只读复核不要申请写权限。

### runner 输出 `FAIL`

先保留完整日志，再执行：

```sh
git status --short
git diff --exit-code
python -X utf8 run_official_suite.py
```

不要手工修改 generated 文件后重新提交来“修绿”。先定位是哪个阶段失败。

### 没有核心网或仪表

这不应阻止 L0 和已固化 L1 证据复跑，但会阻止真实的端到端执行。相关结果应保持
`RESTRICTED`、`NOT_EXECUTED` 或 `L2_REQUIRED`。

## 11. 最小交付检查清单

同事复跑完成前至少确认：

- [ ] checkout 的完整 commit 已记录。
- [ ] `git status --short` 没有未解释的改动。
- [ ] `run_official_suite.py` 返回 `UNIFIED RUNNER RESULT: OK`。
- [ ] `git diff --exit-code` 通过。
- [ ] 34 条套件元数据完整。
- [ ] checker 自检全部通过。
- [ ] 本地证据复跑结果和受限状态已记录。
- [ ] 没有错误出现 `OFFICIAL_PASS`。
- [ ] 所有缺环境的项目仍标为 `RESTRICTED` 或 `NOT_EXECUTED`。
- [ ] 复跑验证报告、原始日志和命令已保存。

## 12. 发给同事的最短说明

把下面内容直接发给同事即可：

```text
仓库：https://github.com/xiongqian-a/lte-verification
适用环境：本机有 Git，能读取该仓库
第一步：git clone https://github.com/xiongqian-a/lte-verification.git
第二步：cd lte-verification
第三步（Windows）：.\bootstrap.cmd --colleague-replay
第三步（Linux/macOS）：chmod +x bootstrap.sh && ./bootstrap.sh --colleague-replay
第四步：python -X utf8 runners/verify_portable_install.py --full
通过标记：UNIFIED RUNNER RESULT: OK、PORTABLE INSTALL: PASS (FULL)、
          COLLEAGUE REPLAY: PASS、TC011_INVARIANTS: PASS、
          OFFICIAL_VERDICT: null
结果位置：outputs/colleague-replay/
边界：本流程复跑仓库已提交证据，不会自动产生新的 eNB/EPC/IMS 现场日志；
      本地 PASS 不等于官方一致性，L2 必须接合格 SS/仪表/检测机构
```
