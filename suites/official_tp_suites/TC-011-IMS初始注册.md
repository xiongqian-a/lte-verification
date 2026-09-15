# TC-011 IMS 初始注册

<!-- OFFICIAL_TP_METADATA:START -->
## 0. 元数据

- 官方主规范：`34.229-1`
- 官方章节/TP：`8.1 Initial registration`
- 映射等级：`exact_line_ref`
- 当前证据层级：`LOCAL_PASS`
<!-- OFFICIAL_TP_METADATA:END -->

## 0. 执行卡

【用例ID】TC-011 / 34.229-1 8.1 Initial registration

【来源】3GPP TS 34.229-1，Clause 8.1 Initial registration（`8.1.1`-`8.1.5`）；关联 `TS 24.229` 5.1.1.2 / 5.1.1.5.1 / Annex C.2，`TS 36.508` 4.5A.6.3-1。本地正文锚点：`_extract/34229-1e70-word.txt` L3875-L4151；`_extract/34229-1e70_ascii.txt` L3253-L3502；Annex C.2 见 Word 导出 L32380-L32448。

【测试目的】按 34.229-1 8.1 验证 UE 能完成 IMS 初始注册：发送未保护 REGISTER，响应 401 AKA 挑战，二次 REGISTER 完成鉴权，收到 200 OK，并订阅注册事件包。

【优先级】P0

【前置条件/SS环境】
1. UE 已激活用于 SIP 信令的 IP-CAN/PDN（IMS APN），已发现 P-CSCF。
2. UICC 含 ISIM+USIM，或仅 USIM（按 24.229 C.2 派生临时身份）。
3. SS/P-CSCF 配置正确 IMS AKA 共享密钥/OPc，能对 IMPI 执行 AKAv1-MD5。
4. 正式一致性要求按 `36.508` 4.5A.6.3-1 前置；当前本地测试台只提供真实 pjsua/自有客户端注册日志。

【测试步骤】
1. 完成 Annex C.2 Step 1 的 E-UTRA EPS bearer 或 UTRA PDP context 激活（BEARER activation）。
2. 按 Annex C.2 Step 3 可选完成 DHCP P-CSCF discovery；未执行时保持预配置 P-CSCF。
3. UE 发送初始未保护 `REGISTER`（Annex C.2 Step 4；Annex A.1.1 condition A1）。
4. SS/P-CSCF 回 `401 Unauthorized`，带有效 AKAv1-MD5 challenge 和网络支持的安全机制（Annex C.2 Step 5）。
5. UE 完成安全协商，建立临时 SA 集合，并通过该 SA 发送第二个 `REGISTER`，带 AKAv1-MD5 credentials（Annex C.2 Step 6）。
6. SS 通过同一临时 SA 集合回 `200 OK`（Annex C.2 Step 7）。
7. UE 通过新建 SA 发送 reg 事件包 `SUBSCRIBE`，SS 回 `200 OK`（Annex C.2 Steps 8-9）。
8. SS 发完整注册状态 XML 的 `NOTIFY`，UE 回 `200 OK`（Annex C.2 Steps 10-11）。
9. 如执行条件要求，按 `px_IMS_IpSecAlgorithm` 再跑一轮，分别覆盖 HMAC-MD5-96 与 HMAC-SHA-1-96。

【预期判据（逐消息检查）】
- 第一个 REGISTER：Request-URI 为 home domain，From/To 含公共用户标识，Contact 含 IP/FQDN 与端口，Supported 含 path，可选 gruu/outbound。
- 401：WWW-Authenticate 含 AKAv1-MD5 challenge；Security-Server 存在。
- 第二个 REGISTER：在 Security-Client/Server 所宣告端口间建立临时 SA，使用 SS 返回且 UE 支持的首选机制和算法，以 RAND 派生的 IK 作为完整性共享密钥；Authorization 含 username/realm/uri/nonce/response，并带 Security-Client 和 Security-Verify。
- 第二个 REGISTER 和之后的 SUBSCRIBE 必须通过临时/新建 SA 发送；200 OK 必须通过 UE 发送 REGISTER 的同一临时 SA 集合返回。
- 200 OK：Contact 的 expires、P-Associated-URI、Service-Route 均须被 UE 正确存储；P-Associated-URI 含已注册 IMPU。
- SUBSCRIBE：使用默认公共用户标识，按存储的 Service-Route 路由；200 OK 后 UE 维护 reg 事件包订阅。
- NOTIFY：携带已注册公共用户身份的完整注册状态 XML；UE 必须以 `200 OK` 响应。
- 若 Contact host 或 Via sent-by 使用 FQDN，SS 须确认其解析到 SA 绑定的 IP 地址。

【通过标准】以上字段检查和流程步骤全部通过，UE 进入已注册状态；本地字段级 PASS 不等同官方 SS Verdict。

【失败处理】记录失败步骤、抓包文件、UE 日志与字段偏离，关联缺陷 ID；官方一致性按 34.229-1 8.1 + 36.508 前置条件判 P/F。

## 官方 TP 原文摘录（34.229-1 8.1）

来源行号说明：本文件中的 `34229-1e70-word.txt` 主锚点和 `34229-1e70_ascii.txt` 交叉检索均使用 Python `str.splitlines()` 1-based 口径。

- 测试目的（ASCII L3254；Word L3877）：`Test to verify that the UE can correctly register to IMS services when equipped with UICC that contains either both ISIM and USIM applications or only USIM application but not ISIM.`
- Pre-test conditions（ASCII L3488-L3489；Word L4120-L4121）：
  `UE contains either ISIM and USIM applications or only USIM application on UICC. UE is not registered to IMS services.`
  `SS is configured with the IMSI within the USIM application, the home domain name, public and private user identities together with the shared secret key of IMS AKA algorithm ... SS is listening to SIP default port 5060 for both UDP and TCP protocols. SS is able to perform AKAv1-MD5 authentication algorithm ...`
- Test purpose（ASCII 对应 8.1.3；Word L4104-L4117）：列出 13 项 UE 行为，包括身份派生/ISIM 读取、初始 REGISTER 组成、401 后 AKAv1-MD5 认证、ipsec-3gpp 机制、两对 SA、200 OK 后存储身份、reg 事件订阅、NOTIFY 处理及回 200 OK。
- Test procedure / Expected sequence（ASCII L3490-L3502；Word L4118-L4139）：
  `Execute the generic test procedure in Annex C.2 up to the last step.`
  `Steps defined in C.2.`
  `Step 3: SS shall check that ... the UE sends another REGISTER request as follows: the UE sets up the temporary set of security associations between the ports announced in Security-Client header (UE) in the REGISTER request and Security-Server header (SS) in the 401 Unauthorized response; ... the UE sends the second REGISTER over the temporary set of security associations;`
  `Step 5: SS shall check that ... the UE sends a SUBSCRIBE request for registration event package over the newly established set of security associations.`
- `8.1.5 Test requirements`（Word L4140-L4151）：核对 ISIM 参数读取、临时 SA 建立、RAND 派生 IK、通过临时 SA 发送二次 REGISTER、通过新 SA 发送 SUBSCRIBE，以及 FQDN 反向解析要求。
- 完整官方 TP 区块机器可读证据：`official_tp_suites/_substeps/TC-011-015-032-official-tp-blocks.json` / `.md`，本用例对应 `8.1 Initial registration`，源文件 `34229-1e70-word.txt` 行 3875-4151；逐行核对脚本：`work/verify_34229_reg_auth_err_tp.py`。
- 具体消息内容：8.1 的 Expected Sequence 直接引用 Annex C.2，且 C.2 明确 `The default message contents in annex A are used`。因此本用例的逐消息骨架取 C.2 的准确步骤表，字段细节再引用 Annex A 默认消息，不把本地日志字段冒充 Annex A 终核结果。
- Annex A 默认消息内容（本用例的 `.3.3` 等价物）：`official_tp_suites/_substeps/TC-011-014-annexA-message-contents.json` / `.md`；含 `A.1.1 REGISTER`（行 21415-22020，含 A1/A2/A17 条件词表）、`A.1.2 401`（22021-22255）、`A.1.3 200 OK`（22256-22497）、`A.1.4 SUBSCRIBE`（22498-22771）、`A.1.5 200 OK`（22772-22918）、`A.1.6 NOTIFY`（22919-23238）。逐行核对脚本：`work/verify_34229_annexA.py`。

### Annex C.2 官方步骤逐项映射

以下步骤表来自 `34229-1e70-word.txt` L32380-L32448；正文过程为 L32382-L32391，Expected sequence 为 L32392-L32445，默认消息说明为 L32447-L32448。

| C.2 Step | 方向 | 消息/动作 | 官方检查点 | 当前证据状态 |
|---:|---|---|---|---|
| 1 | 前置 | EPS bearer / PDP context activation | E-UTRA 按 Annex C.18，UTRA 按 Annex C.17 | `RESTRICTED`：需要真实 eNB/EPC 或等效 SS |
| 2 | 前置 | Void | 官方无动作 | `N/A` |
| 3 | 前置 | 可选 P-CSCF discovery | DHCP IPv6 按 C.3；DHCP IPv4 按 C.4 | `RESTRICTED`：需要 DHCP/P-CSCF 测试环境 |
| 4 | UE -> SS | `REGISTER` | UE 发起 IMS 初始注册，发送未保护 REGISTER | 本地有真实 `REGISTER` 原始日志 |
| 5 | SS -> UE | `401 Unauthorized` | 有效 AKAv1-MD5 challenge 和网络支持的安全机制 | 本地有 401，但未见完整 Security-Server/临时 SA 证据 |
| 6 | UE -> SS | `REGISTER` | 完成安全协商、建立临时 SA，并通过临时 SA 发送带 AKAv1-MD5 credentials 的二次 REGISTER | `RESTRICTED`：本地栈缺 Security-Client/Security-Verify 和临时 SA |
| 7 | SS -> UE | `200 OK` | 必须通过 UE 发送 REGISTER 的同一临时 SA 集合返回 | 本地有 200，但不是官方临时 SA Verdict |
| 8 | UE -> SS | `SUBSCRIBE` | UE 通过新建 SA 订阅 registration event package | `NOT_EXECUTED`：本地日志未覆盖 |
| 9 | SS -> UE | `200 OK` | SS 接受 SUBSCRIBE | `NOT_EXECUTED` |
| 10 | SS -> UE | `NOTIFY` | 包含已注册 IMPU 的完整 registration state XML | `NOT_EXECUTED` |
| 11 | UE -> SS | `200 OK` | UE 接受 NOTIFY | `NOT_EXECUTED` |

> 官方额外要求：本用例须跑两轮，分别配置 `px_IMS_IpSecAlgorithm` 为 HMAC-MD5-96 与 HMAC-SHA-1-96；当前本地证据未覆盖该 PIXIT 双轮要求。

> 状态：官方 TP 骨架已锚定，本地真实 `401 -> 200` 字段级 PASS。官方一致性仍需 SS/一致性仪表按 `34.229-1` 判 P/F。

## 1. 目的 / 为什么

验证 UE 在 LTE/EPC 承载和 P-CSCF 发现完成后，能正确完成 IMS 初始注册：发送初始未保护 REGISTER，响应 401 挑战，完成 AKA 鉴权，收到 200 OK，并订阅注册事件包。

## 2. 官方骨架

- 主来源：`34.229-1` 8.1 Initial registration，正式子节为 `8.1.1 Definition`、`8.1.2 Conformance requirement`、`8.1.3 Test purpose`、`8.1.4 Method of test`、`8.1.5 Test requirements`。
- 文本抽取记录：`_extract/34229-1e70-word.txt` L3875-L4151；Annex C.2 在 L32380-L32448。`_extract/34229-1e70_ascii.txt` 仅用于交叉检索。
- 关联：`TS 24.229` 5.1.1.2 初始注册客户端行为，Annex C.2 通用注册流程。
- E-UTRA 接入前置：`36.508` table 4.5A.6.3-1（正式 SS 侧执行时需要，当前本地测试台不具备）。

## 3. 前置条件

- UE 已激活用于 SIP 信令的 IP-CAN/PDP/PDN（IMS APN）。
- UE 已通过 DHCP 或预配置发现 P-CSCF。
- UICC 含 ISIM+USIM，或 USIM 并按 `24.229` C.2 派生临时身份。
- SS 配置正确 IMS AKA 共享密钥/OPc，能对 IMPI 执行 AKAv1-MD5。
- 本地测试台条件下：已有真实 pjsua/自有客户端注册日志。

## 4. 验证流程

1. 完成 Annex C.2 前置：EPS bearer/PDP context；可选 P-CSCF discovery。
2. UE 发送未保护 `REGISTER`（Annex A.1.1 条件 A1）。
3. SS/P-CSCF 回 `401 Unauthorized`，带有效 AKAv1-MD5 challenge 和 Security-Server。
4. UE 建立临时 SA 集合，发送第二个 `REGISTER`：
   - `From` / `To` 为公共用户标识；
   - `Contact` 包含 UE IP/FQDN 与端口；
   - `Authorization` 含 username/realm/uri/nonce/response；
   - 使用 IMS 安全时包含 `Security-Client`，收到 `Security-Server` 后包含 `Security-Verify`。
5. SS 通过同一临时 SA 回 `200 OK`，带 `P-Associated-URI`、`Service-Route`、`Contact`、`Expires`。
6. UE 通过新建 SA 发送 `SUBSCRIBE`（reg event package），SS 回 `200 OK`。
7. SS 发送注册状态 `NOTIFY`，UE 回 `200 OK`。

## 5. TP Verdict 判据（关键项）

- 初始 REGISTER 未保护，`Expires` 默认 600000s，`Supported: path/gruu/outbound` 按能力出现。
- 401 后安全参数和临时 SA 生成正确，第二个 REGISTER 必须通过 C.2 指定的临时 SA 发送，不能把普通明文 SIP 通道计为通过。
- 200 OK 必须通过同一临时 SA 返回；UE 绑定 `P-Associated-URI` 与 `Service-Route`。
- SUBSCRIBE 使用默认公共用户标识，并通过新建 SA 发送。
- NOTIFY 必须包含完整 registration state XML，UE 返回 200 OK。
- 不出现 408/503/超时或崩溃。

## 6. 当前本地证据

```text
python work/tc011_register_flow.py
输入：outputs/co1750-20260904/ims_register_test.log
结果：PASS（字段级）
观察：REGISTER -> 401 -> REGISTER -> 200 OK
限制：当前真实日志只覆盖 C.2 Steps 4-7 的字段子集，未证明临时 SA、Security-Client/Verify、Steps 8-11 或 PIXIT 双算法
```

## 7. 受限 / L2_REQUIRED

- 未在官方 SS + 无线接口 + 真实 USIM/ISIM 上按 34.229-1 8.1 + 36.508 前置条件执行。
- 本地日志缺 C.2 Step 6 的临时 SA 和 Security-Client/Security-Verify 证据，缺 Steps 8-11 的 SUBSCRIBE/NOTIFY 证据。
- 未完成 HMAC-MD5-96 / HMAC-SHA-1-96 两轮 PIXIT 配置。
- 本地测试台为 IMS 模拟/简化流程，缺少正式 SS Verdict。

## 8. 执行命令

```text
python work/tc011_register_flow.py
python work/run_tc_evidence.py
```
