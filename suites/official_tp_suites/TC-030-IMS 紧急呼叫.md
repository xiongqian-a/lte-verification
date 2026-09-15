# TC-030 IMS 紧急呼叫

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`36.523-1 + 34.229-1`
- 官方章节/TP：`11.2.1 + 紧急流程`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS | 20260911_RERUN_REPRODUCED`
<!-- OFFICIAL_TP_METADATA:END -->

> 状态：官方 ID 已锚定到 36.523-1 11.2.1；co1750 本地功能级 112/110/119/120 PASS；2026-09-11 已在 phase5 命名空间复跑 112 成功，官方一致性/紧急 PDN 仍受限。

## 1. 目的 / 为什么

验证 UE 能发起 IMS 紧急呼叫：以 emergency 建立 RRC/SERVICE REQUEST，必要时触发紧急 PDN（request type=emergency，不含 APN），并完成紧急承载激活。

## 2. 官方骨架

- 正文行锚（36.523-1 正文/TP，2026-09-11 重新核对）：
  - 11.2.1 body 行 235227 / TP 行 235231 / .3.2 行 235399 / Main behaviour 行 235400








- 官方 ID：36.523-1 11.2.1 Emergency bearer services；紧急呼叫侧 13.1.19 / 13.1.20
- 来源：`523-1v14.pdf`；映射见 `74-` 表
- 关联：TS 34.229-1 Annex C.32 IMS 呼叫释放（C.30 是去注册，不作为本用例建立流程）


### 2.1 官方 TP 原文要点

- 11.2.1.1 TP（1）：UE 在 EMM-REGISTERED/EMM-IDLE，发起出向 emergency call 时，UE 建立 RRC connection，RRC establishmentCause=emergency，并发送 SERVICE REQUEST。
- 11.2.1.1 TP（2）：UE 被触发请求 emergency bearer service 的 additional PDN 时，发送 PDN CONNECTIVITY REQUEST，request type=emergency，且不携带 APN。
- 11.2.1.1 TP（3）：UE 已发送 PDN CONNECTIVITY REQUEST 后，后续 emergency bearer activation / service request / emergency PDN disconnect 仍需按 .3 Test Procedure 继续核。

官方标题还含 Service request / Emergency PDN disconnect；当前本地 112/110/119/120 是功能级 PASS，不覆盖紧急 PDN 与 emergency registration。

### 2.2 官方 .3.2/.3.3 子例级原文抽取

- 抽取文件：`C:/标准例程/official_tp_suites/_substeps/TC-026-031-3.2-main-behaviour.md`
- 源文本：`C:\Users\co1750\Documents\Codex\2026-08-31\qin\_523_evidence\work\523-1v14.txt`
- 源规范：ETSI TS 136 523-1 V14.3.0 (2018-02)。
- 行号方法：将 CRLF/CR 归一化后按 LF 切分；form-feed 页分隔符不另计一行。
- 覆盖官方小节：11.2.1
- 说明：以下保留 `.3.2` 原文行号和 `.3.3` 表来源；`P/F` 是官方 TP Verdict 文本，不代表本地已得到一致性 Verdict。
- 正式结论仍必须由 R&S / Anritsu / Keysight 或检测机构按官方 SS 流程执行。

#### TC-030 / 11.2.1

- body 行 235227 / TP 行 235231 / Conformance 行 235276 / Test description 行 235385 / Pre-test 行 235386 / Test procedure 行 235399 / Main behaviour 行 235400-235467 / .3.3 行 235473

**官方表清单**

- `Table 11.2.1.3.2-1: Main behaviour` 行 235400-235467
- `Table 11.2.1.3.3-1: ATTACH ACCEPT (Preamble)` 行 235474-235482；Derivation path: 36.508 table 4.7.2-1

**`.3.3` Specific message contents 原文（逐行）**

##### Table 11.2.1.3.3-1: ATTACH ACCEPT (Preamble)

行 235474-235482

```text
235474 | Table 11.2.1.3.3-1: ATTACH ACCEPT (Preamble)
235475 | Derivation path: 36.508 table 4.7.2-1
235476 | Information Element Value/Remark Comment Condition
235477 | Emergency number list 2 numbers
235478 | TS 24.008, 10.5.3.13
235479 | The numbers shall
235480 | be different than
235481 | any of those
235482 | indicated in TS
```

**关键官方判据**

- 步骤 2A：`RRCConnectionRequest.establishmentCause=emergency`，TP Verdict `1 P`；步骤 2：`SERVICE REQUEST`，TP Verdict `1 P`（行 235409-235415）。
- 步骤 16：不应发送 `SERVICE REQUEST`，TP Verdict `4 F`；步骤 21：UE 发送 `DEACTIVATE EPS BEARER CONTEXT ACCEPT`，TP Verdict `5 P`（行 235431-235459）。
- 步骤 3-13 接 `36.508 4.5A.4.3-1` steps 5-15；步骤 13A IMS 呼叫释放接 `34.229-1 C.32`（行 235416-235425）。

**Main behaviour 原文（逐行）**

```text
235400 | Table 11.2.1.3.2-1: Main behaviour
235401 | St Procedure Message Sequence TP Verdict
235402 |   U – S Message
235403 | 1 Cause the UE to request connectivity to an
235404 | additional PDN for emergency bearer service
235405 | and an emergency call to one of the numbers
235406 | received in Attach Accept message (see Note
235407 | 1)
235408 | - - - -
235409 | 2A Check: Does the UE transmit an
235410 | RRCConnectionRequest message with
235411 | establishmentCause set to ‘emergency'?
235412 | --> RRCConnectionRequest 1 P
235413 | 2 Check: Does UE transmit a SERVICE
235414 | REQUEST message?
235415 | --> SERVICE REQUEST 1 P
235416 | 3-
235417 | 13
235418 | Steps 5 to 15 of the generic test procedure for
235419 | IMS Emergency call establishment in EUTRA:
235420 | in EUTRA: Normal Service (TS 36.508
235421 | subclause 4.5A.4.3-1).
235422 | - - 2,3 P
235423 | 13
235424 | A
235425 | Release IMS Call (see Note 4) - - - -
235426 | 14 The SS releases the RRC connection. - - - -
235427 | 15 Cause the UE to request connectivity to an
235428 | additional PDN for emergency bearer service
235429 | (see Note 1)
235430 | - - - -
235431 | 16 Check: Does UE transmit a SERVICE
235432 | REQUEST message?
235433 | --> SERVICE REQUEST 4 F
235434 | 17 The SS transmits a Paging message to the UE
235435 | using S-TMSI with CN domain indicator set to
235436 | ''PS”.
235437 | - - - -
235438 | 18 The UE transmits the SERVICE REQUEST
235439 | message
235440 | --> SERVICE REQUEST - -
235441 | 19 The SS establishes SRB2 and DRBs
235442 | associated with two default EPS bearer
235443 | context (a first PDN obtained during the attach
235444 | procedure and an additional PDN).( see Note
235445 | 2)
235446 | - - - -
235447 | 20 The SS transmits a DEACTIVATE EPS
235448 | BEARER CONTEXT REQUEST including the
235449 | EPS bearer identity of the default EPS bearer
235450 | to the additional PDN.
235451 | <-- DEACTIVATE EPS BEARER
235452 | CONTEXT REQUEST
235453 | - -
235454 | 21 Check: Does the UE transmit a DEACTIVATE
235455 | EPS BEARER CONTEXT ACCEPT?
235456 | (see Note 3)
235457 | --> DEACTIVATE EPS BEARER
235458 | CONTEXT ACCEPT
235459 | 5 P
235460 | Note 1: The request of connectivity to an additional PDN and the sending of data may be performed by MMI or AT
235461 | command. (e.g. AT command +cgdcont with <Emergency Indication> set to 1)
235462 | Note 2: After a correct SERVICE REQUEST is received then the SS performs the Radio Bearer Establishment
235463 | procedure. The UE transmission of the RRCConnectionReconfigurationComplete message indicates the
235464 | completion of the radio bearer establishment procedure and that the UE has changed EMM mode from
235465 | EMM-IDLE to EMM-CONNECTED.
235466 | Note 3: It can be confirmed that the additional default EPS bearer has been deactivated by UE.
235467 | Note 4: The IMS Call is released using the generic procedure in TS 34.229-1 [35] subclause C.32.
```

**当前证据状态**：`STANDARD_ALIGNED / L1_SKELETON`；未在真实 SS、eNB/EPC/UTRAN/GERAN/IMS 或一致性仪表上执行，因此不得写成官方一致性 `PASS`。


### 2.3 36.508 锚点（通用测试环境）

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/36508.txt`
- 36.508 `Table 4.5A.4.3-1: EUTRA/EPS signalling for IMS Emergency Call` 行 16909
- 来源规范：ETSI TS 136 508 V14.3.0 (2017-11)，3GPP TS 36.508 version 14.3.0 Release 14
- 核对脚本：`work/verify_ts36508_refs.py`

### 2.4 34.108 锚点

- 源文本：`C:/Users/co1750/Documents/Codex/2026-09-02/i/_extract/34108.txt`（TS 34.108 V14.2.0）
- 34.108 `7.2.5 IMS Emergency Call setup` 行 53980-53982 与 `7.2.5.1.3 Procedure` 行 53991-54016：Normal Service 下 emergency 建立流程含 RRC establishmentCause=emergency、SERVICE REQUEST、ACTIVATE PDP CONTEXT REQUEST（Request Type=Emergency）等。
- 说明：34.108 是 UTRA/通用测试环境正文，不作为 E-UTRA 一致性 Verdict 替代；用于明确 IMS 紧急呼叫的通用 SS 流程来源。

## 3. 前置条件

- UE 支持 IMS 紧急服务，配置紧急号码。
- 本地测试台可发起 112/110/119/120 呼叫。

## 4. 验证流程

1. 用户拨紧急号码，UE 以 RRC emergency cause 建立连接。
2. 需要紧急 PDN 时发 PDN CONNECTIVITY REQUEST，request type=emergency，避免携带普通 APN。
3. 收到 ACTIVATE DEFAULT EPS BEARER（紧急）后回 ACCEPT。
4. 发起 IMS emergency INVITE 并保持呼叫。

## 5. TP Verdict 判据

- 紧急号码触发/紧急 PDN 发起字段正确。
- RRC cause=emergency。
- 呼叫建立/释放成功。

## 6. 当前本地证据

本地证据：`work/run_tc030_emergency_lab.sh` 功能级 PASS（112/110/119/120）。

### 6.1 2026-09-11 phase5 命名空间 fifo 复跑（REPRODUCED PASS）

- 复跑时间：2026-09-11 15:54:04（`tc030-emergency-112-20260911-155404`）。
- 服务器证据目录：`/home/co1750/verification-evidence/tc030-emergency-112-20260911-155404`。
- 环境：先前在默认主机命名空间看不到 `tun_srsue`/`srs_spgw_sgi` 与 SIP 端口；本次通过 `run-baseline20-20260831-175026/cmd.fifo` 在 phase5 命名空间内执行，确认 `tun_srsue=10.45.0.2/24`、`srs_spgw_sgi=10.45.0.1/24`、`10.45.0.1:5060/6060`、`127.0.0.1:8022` 均可见。
- `ims-client.log` 关键步骤：
  - REGISTER 401 Challenging the UE -> 200 OK（含 `P-Associated-URI`、`Service-Route`）。
  - INVITE `sip:112@ims.mnc001.mcc001.3gppnetwork.org` -> 100 trying -> 200 OK -> ACK -> `call state: CONFIRMED`。
  - 15 秒音频会话：RX 725 pkt / TX 751 pkt，`pkt loss=0 (0.0%)`，`discrd=0`，`dup=0`，`reord=0`。
  - 自动挂断后 BYE -> 200 OK，`call state: DISCONNECTED`。
- `scscf-key-lines.txt` / `scscf-emergency-lines.txt`：
  - `EMERGENCY-RULE-HIT from=10.45.0.1:5060 rm=INVITE rU=112 ru=sip:112@ims.mnc001.mcc001.3gppnetwork.org`
  - `EMERGENCY-ROUTE-REWRITE ru=sip:112@10.45.0.1:5081`
- `run-summary.txt`：`fs_reloadxml_rc=0`；`call_rc=124` 是 `timeout` 包装器在脚本侧等满 40s 的返回，日志已确认呼叫确认、媒体与 BYE 正常，不能据此判呼叫失败。
- 说明：该复跑是本地/模拟 IMS 功能级证据，不产出官方一致性 Verdict。

## 7. 受限 / L2_REQUIRED

- 官方一致性、紧急 PDN、emergency registration 仍受限。
- 本地已在 phase5 命名空间复跑 112 成功；后续如需功能级复跑，须继续通过该实例的 `cmd.fifo` 进入命名空间执行，而不是从默认命名空间直接调用。

## 8. 执行命令

```text
在本测试台所在环境内执行已验证的 emergency lab 脚本；服务器地址和凭据通过受控的本地配置提供，不写入仓库。
```

## 9. L1 测试骨架

- 阶段：`L1_SKELETON`，不代表 `PASS`，不判官方一致性。
- 待补真实环境依赖：真实紧急号码触发 + emergency RRC/SERVICE REQUEST + 紧急 PDN + IMS/eNB/EPC。
- 本骨架作用：预留 L1 可执行入口，先保证套件文档包含官方 TP 原文要点、待注入消息、预期行为和环境依赖。
- L1 runner：`python work/l1_skeleton_026_031.py`
- 判定规则：脚本只检查文档/骨架存在性和环境缺口登记，不输出一致性 Verdict。
