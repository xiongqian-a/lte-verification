# TC-011 L1 IPsec / SUBSCRIBE / NOTIFY 证据

> 生成日期：2026-09-16
>
> 结论级别：`L1_LOCAL_SIMULATED PASS`
>
> 官方一致性结论：`NO_OFFICIAL_VERDICT`

## 1. 目的

补齐 TC-011 之前遗留的本地执行缺口：

- Annex C.2 Steps 4-11；
- 临时 IPsec 安全关联的端口、SPI 和 Security Header 行为；
- `Security-Client` / `Security-Verify`；
- `SUBSCRIBE` / `NOTIFY` registration event package；
- `px_IMS_IpSecAlgorithm = HMAC-MD5-96`；
- `px_IMS_IpSecAlgorithm = HMAC-SHA-1-96`。

## 2. 标准来源

- 主 TP：`3GPP TS 34.229-1` Clause 8.1 Initial registration。
- 通用流程：`TS 34.229-1` Annex C.2 Steps 4-11。
- 默认消息：`TS 34.229-1` Annex A.1.1-A.1.6。
- Release 14 正文锚点：`34229-1e70-word.txt` L3875-L4151；Annex C.2 L32380-L32448；Annex A L21415-L23238。
- 版本边界：`TS 34.229-1 V14.8.0` 将 5-22 和 Annex A-J 标为 Void，因此 Release 14 正文主锚使用 V14.7.0。

本地核对命令均通过：

```text
python work/verify_34229_reg_auth_err_tp.py
python work/verify_34229_annexA.py
python work/verify_34229_version_boundary.py
```

## 3. 执行命令

```text
python -X utf8 runners/tc011_ipsec_ss_sim.py --selftest --out-dir evidence/local/tc011-l1-20260916
```

统一 runner 兼容入口：

```text
python -X utf8 runners/tc011_ipsec_ss_sim.py --selfcheck
```

## 4. 结果

| PIXIT 轮次 | 算法 | 已执行 C.2 步骤 | 通过 | 本地判定 |
|---|---|---:|---:|---|
| Round 1 | `hmac-md5-96` | 8 | 8 | PASS |
| Round 2 | `hmac-sha-1-96` | 8 | 8 | PASS |

机器可读摘要：

```json
{
  "tc_id": "TC-011",
  "layer": "L1_LOCAL_SIMULATED",
  "official_verdict": null,
  "all_rounds_pass": true,
  "ipsec_realization": "port_pair_emulation_no_kernel_xfrm"
}
```

## 5. 已验证的官方检查点

| C.2 Step | 方向 | 检查内容 | 结果 |
|---:|---|---|---|
| 4 | UE -> SS | 初始未保护 REGISTER、home domain、IMPU、Contact、Expires、Supported、PANI | PASS |
| 5 | SS -> UE | 401、AKAv1-MD5 challenge、Security-Server 与候选算法 | PASS |
| 6 | UE -> SS | 二次 REGISTER、受保护端口、Authorization、Security-Client、Security-Verify、SPI/端口回显 | PASS |
| 7 | SS -> UE | 200 OK 返回受保护端口、P-Associated-URI、Service-Route、Contact | PASS |
| 8 | UE -> SS | `SUBSCRIBE reg`、默认 IMPU、Service-Route、受保护端口、reginfo Accept | PASS |
| 9 | SS -> UE | SUBSCRIBE 200 OK、Call-ID/CSeq/To-tag | PASS |
| 10 | SS -> UE | NOTIFY、完整 reginfo XML、AOR、Subscription-State | PASS |
| 11 | UE -> SS | NOTIFY 200 OK、对话和事务字段 | PASS |

## 6. 证据文件

- `evidence/local/tc011-l1-20260916/tc011-l1-selftest-summary.json`
- `evidence/local/tc011-l1-20260916/tc011-l1-hmac-md5-96-verdict.json`
- `evidence/local/tc011-l1-20260916/tc011-l1-hmac-md5-96-transcript.txt`
- `evidence/local/tc011-l1-20260916/tc011-l1-hmac-sha-1-96-verdict.json`
- `evidence/local/tc011-l1-20260916/tc011-l1-hmac-sha-1-96-transcript.txt`

## 7. 边界与限制

- 本证据是本地参考 UE/SS 行为仿真，不是产品 DUT 日志。
- IPsec 当前在端口、SPI 和 Security Header 层仿真，不创建 Linux `xfrm state/policy`，不发送或校验真实 ESP/AH 数据包。
- 未在真实 eNB/EPC、真实 USIM/ISIM、IMS System Simulator 或一致性仪表上执行。
- 本地 `PASS` 只表示实现行为符合本检查器的官方 TP 派生断言；不表示 36.523-1、34.229-1 官方一致性通过。
- 官方 `PASS/FAIL` 仍必须由合格 SS 或检测机构按官方 TP 给出。
