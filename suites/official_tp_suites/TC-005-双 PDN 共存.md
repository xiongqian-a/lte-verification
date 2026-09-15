# TC-005 双 PDN 共存

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1`
- 官方章节/TP：`9.2.1.1.28a`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LIMITED_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 TP 已锚定；co1750 本地 srsRAN 4G + 补丁版 Open5GS 已跑出 internet + ims 双 PDN 行为证据，结果为 `LOCAL_BEHAVIOR=PASS / LIMITED_PASS`。官方一致性 Verdict 仍需一致性 SS/仪表。

## 1. 目的 / 为什么

验证 UE 能携带 IMS 第二 PDN 完成 attach，并使用 method II P-CSCF discovery 与 IPv4v6 PDN type；两 PDN 独立共存。

## 2. 官方骨架

- 官方 ID：36.523-1 9.2.1.1.28a Attach / Success / IMS / Second PDN
- 关联：TS 24.229 L.2.2.1 / L.3.1.2；TS 23.401 5.3.1.1

### 2.1 36.508 锚点（通用测试环境）

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/36508.txt`
- 523 正文行 202150 引用 UE registration `TS 36.508 subclause 4.5.2.3-1`；对应 `Table 4.5.2.3-1: UE registration procedure (state 1 to state 2)` 行 14039
- 523 正文行 202155/202156、202198 引用 additional PDN 建立/释放 `4.5A.16.3-1` / `4.5A.18.3`；对应 `Table 4.5A.16.3-1: Establishment of additional PDN connectivity` 行 18387、`Table 4.5A.18.3-1: Release of additional PDN connectivity` 行 18630
- 523 正文行 202176/202177 引用 `TS 36.508 subclause 4.5A.1`；对应 `Table 4.5A.1-1: Procedure for IP address allocation in the U-plane` 行 16410
- 523 正文行 202203 引用 `TS 36.508 Table 6.4.3A.2-1`；对应 `Table 6.4.3A.2-1: Reference end states` 行 42808
- 523 正文行 202216 引用 `TS 36.508 Table 4.7.3-20`；对应 `Table 4.7.3-20: PDN CONNECTIVITY REQUEST` 行 30198
- 523 正文行 202308 引用 `36.508 table 4.7.2-3`；对应 `Table 4.7.2-3: ATTACH REJECT` 行 27931
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.3 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-001-010-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 行号方法：CRLF/CR 归一化后按 LF 切分；以下仅建立官方 TP 骨架和可追溯性，不等于官方一致性 Verdict。

已核对的官方边界：

- 9.2.1.1.28a: body 198590 / TP 198591 / Conformance 198612 / Test description 198664 / Pre-test 198665 / .3.2 198677 / Main behaviour 198678-198739 / .3.3 198749-198763

## 3. 前置条件

- UE 关机，支持 method II P-CSCF discovery。
- UE 支持会话语音，开机后可接电话并执行首次 IMS 注册。
- UE 具备 IPv4+IPv6 能力。

## 4. 验证流程

1. UE 开机后发 PDN CONNECTIVITY REQUEST，携带 method II P-CSCF discovery 请求。
2. PDN type 为 IPv4v6。
3. UE 执行首次 IMS 注册。
4. 验证第二 PDN 建立后不影响已建 IMS PDN，承载/地址/事件独立。

## 5. TP Verdict 判据

- 第二 PDN Connreq 中的 P-CSCF discovery 容器存在且为 method II。
- PDN type = IPv4v6。
- 两 PDN 独立承载 ID/地址/生命周期。
- 端到端未跑时，不得宣称 9.2.1.1.28a PASS。

## 6. 当前本地证据

2026-09-14 在 co1750 测试床完成 `srsRAN 4G + 补丁版 Open5GS MME/SMF+SGW-C+UPF` 运行。最终成功窗口观察到：

- `internet`：IPv4 `10.45.0.2`，默认承载 `EBI=5`
- `ims`：IPv4 `10.46.0.2`，第二个默认承载 `EBI=6`
- IMS 专用承载：`EBI=7`，`linked_bearer_id=6`
- MME：`Number of MME-Sessions is now 2`
- SGW-C：完成 `Create Bearer Response`
- UE：发送第二个默认承载 `EBI=6` Accept，并接受绑定到 `EBI=6` 的 `EBI=7`

判定输出：

```text
[WARN] IPv4 dual-PDN behavior observed; IPv6/dual-stack assignment is RESTRICTED
OFFICIAL_VERDICT: RESTRICTED (requires SS/consistency instrument)
LOCAL_BEHAVIOR: PASS
RESULT: LIMITED_PASS
```

详细证据与哈希：`outputs/87-TC005-双PDN本地证据-20260914.md`；归档：`outputs/TC005-双PDN本地证据-20260914-archive.tgz`。

## 7. 受限 / L2_REQUIRED

- IPv4v6 / IPv6：UE 请求了 IPv4v6，但 SMF 只分配 IPv4；IPv6 subnet 未配置。
- method II P-CSCF discovery：当前日志证明 `APN=ims`、第二 PDN 和承载行为，但未完成官方容器的逐字段检查。
- additional PDN 网络侧释放与 E1 结束态：未按 `36.508 4.5A.18.3` 和 `Table 6.4.3A.2-1` 全步骤执行。
- 官方一致性 Verdict：必须由合格 SS/仪表或检测机构执行，本文件不将本地 PASS 升级为 `36.523-1 9.2.1.1.28a PASS`。

## 8. 执行命令

```text
python work/tc005_dual_pdn.py \
  --ue outputs/TC005-dual-pdn-20260914/evidence-20260914-184930/log/ue.log \
  --mme outputs/TC005-dual-pdn-20260914/evidence-20260914-184930/log/mme.log \
  --smf outputs/TC005-dual-pdn-20260914/evidence-20260914-184930/log/smf.log \
  --sgwc outputs/TC005-dual-pdn-20260914/evidence-20260914-184930/log/sgwc.log \
  --ue-since 2026-09-14T10:47:29 \
  --core-since "09/14 18:47"

python work/tc005_dual_pdn.py --selfcheck
```
