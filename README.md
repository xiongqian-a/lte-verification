# LTE/IMS Official-TP-Aligned Verification Suite

This repository is the reproducible baseline for the project's LTE/EPC and
IMS verification cases. It combines:

- a machine-readable registry that maps the internal `TC-001` to `TC-034`
  identifiers to named 3GPP/ETSI specifications and clauses;
- 34 standard-suite documents containing purpose, preconditions, procedure,
  TP-style verdict criteria, evidence status, and known blockers;
- executable local checkers and evidence replay;
- an L2 evidence adapter for qualified System Simulator or laboratory results;
- generated progress, audit, and official-style reports.

## Chinese Quick Start

For a step-by-step Chinese guide that starts with a fresh checkout and covers
one-command execution, single-case execution, evidence interpretation,
environment differences, and colleague replay verification, see
[`START-HERE.md`](START-HERE.md).

For the complete colleague usage and missing-environment guide, see
[`docs/101-同事使用与离线环境说明书-20260918.md`](docs/101-同事使用与离线环境说明书-20260918.md).

For the server and local path inventory, including the difference between
tracked evidence files, replay checks, and the 34 functional TCs, see
[`docs/102-服务器与本机路径总表-20260918.md`](docs/102-服务器与本机路径总表-20260918.md).
The complete directory and symlink inventory for the two reference server
account roots is in
[`docs/102a-服务器完整目录清单-20260918.txt`](docs/102a-服务器完整目录清单-20260918.txt).

## Important Scope Statement

This repository is an **official-TP-aligned executable baseline**. It is not a
36.523-1 or 34.229-1 conformance execution record and does not prove any of the
following:

- official 3GPP conformance;
- pjsua or any new protocol-stack compliance;
- commercial-network acceptance;
- third-party lab approval.

An official verdict can only be produced by a qualified System Simulator or an
accredited conformance laboratory using the applicable official test procedure.
Local checker results remain implementation evidence and must not be relabeled
as `OFFICIAL_PASS`.

## Colleague Quick Start

For a colleague who only needs to pull the repository, run the verification
baseline, and compare the result with this snapshot, no project path edit,
`pip install`, core-network setup, or IMS setup is required. The machine needs
Git and read access to the repository; the bootstrap scripts handle the Python
launch and invoke the unified runner.

Requirements:

- Python 3.10 or later;
- Git;
- no third-party Python packages are required.

The repository also carries the private, authorized standards bundle under
`standards/official/`. It contains the source documents currently available to
the suite, not every 3GPP specification. The current manifest covers 45 source
files, including every 3GPP/ETSI specification directly referenced by the
existing suite and registry, plus RFC 3261 and RFC 3515. The bundle is
integrity-checked before the unified runner proceeds.

Windows PowerShell (clone, bootstrap, and run):

```powershell
git clone https://github.com/xiongqian-a/lte-verification.git
cd lte-verification
.\bootstrap.cmd --doctor
.\bootstrap.cmd --verify-standards
.\bootstrap.cmd
```

`--doctor` reports whether this machine can replay the committed golden evidence
or has enough tooling for a fresh DUT run. `--verify-standards` checks every
bundled source document against `standards/official/manifest.json`.

To generate the colleague replay acceptance report in the same one-command
flow:

```powershell
.\bootstrap.cmd --colleague-replay
```

`bootstrap.cmd` invokes the PowerShell bootstrap with an execution-policy
override, so it also works on systems where local `.ps1` files are blocked.
It refreshes the current process PATH and searches the standard per-user and
machine Python install directories after provisioning Python, so no new shell
is required. If the execution policy already allows local scripts,
`.\bootstrap.ps1` is equivalent.

Windows, macOS, or Linux with an existing Python 3.10+ installation:

```text
git clone https://github.com/xiongqian-a/lte-verification.git
cd lte-verification
python -X utf8 run_official_suite.py
```

macOS or Linux (bootstrap is optional when Python 3.10+ is already installed):

```sh
git clone https://github.com/xiongqian-a/lte-verification.git
cd lte-verification
./bootstrap.sh
```

`bootstrap.ps1` and `bootstrap.sh` only provision Python when it is missing,
then invoke the unified runner. They do not install or pretend to provide an
eNB, EPC, IMS core, System Simulator, conformance instrument, test subscriber,
or operator acceptance environment.

Optional: skip replay of the included evidence logs.

```text
python -X utf8 run_official_suite.py --skip-evidence
```

Successful completion ends with:

```text
UNIFIED RUNNER RESULT: OK
```

The unified runner rebuilds derived data, checks all 34 suite documents,
executes the checker self-checks, replays included evidence, evaluates the
optional TC-026..031 L2 manifest, and writes reports under `generated/`.

The executable entry points resolve paths from their own location. A fresh
checkout can therefore live in any directory; no machine-specific path edit is
required. The run is deterministic with respect to the tracked artifacts: it
uses repository-relative paths and stable generated timestamps. Runtime
scratch files are written under the ignored `outputs/` directory.

For a deliberate fresh-checkout portability check, run:

```text
python -X utf8 runners/verify_portable_install.py
python -X utf8 runners/verify_portable_install.py --full
```

The static mode checks required entry points, executable flags, CI coverage,
and forbidden machine-specific paths. The full mode additionally runs the
unified suite from an unrelated working directory and verifies that tracked
generated artifacts do not change.

## Verification Architecture Explorer

Open [`verification-architecture.html`](verification-architecture.html) directly
in a browser. It is a self-contained page that presents the eight functional
modules, all 34 internal TCs, official-specification mappings, validation
procedure, verdict criteria, scripts, evidence paths, and current blockers.

The page does not claim a conformance result. Its status remains
`NO_OFFICIAL_VERDICT` until a qualified System Simulator or accredited
laboratory executes the applicable official test procedure.

Rebuild the page after changing the registry, TP library, or suite documents:

```text
python -X utf8 tools/build_verification_architecture.py
```

## Repository Layout

| Path | Purpose |
|---|---|
| `run_official_suite.py` | Cross-platform one-command entry point |
| `run.ps1` | Windows PowerShell wrapper for the same runner |
| `bootstrap.cmd` | Windows one-click bootstrap with execution-policy override |
| `standards/` | Private authorized standards-source handoff bundle and hash manifest |
| `registry/` | Machine-readable TC-to-official-TP registry and library |
| `suites/official_tp_suites/` | One Markdown suite document per internal TC |
| `suites/official_tp_suites/_substeps/` | Official procedure, Annex A, message, and verdict extracts |
| `suites/official_tp_suites/_evidence/` | L2 evidence schema and manifest template |
| `suites/official_tp_suites/_templates/TC-TEMPLATE.md` | Reusable template for a new standard suite document |
| `runners/` | Local checkers, evidence replay, report generation, and adapters |
| `evidence/local/` | Selected local reproduction evidence |
| `evidence/external/` | Selected testbed, pjsua, core-network, and packet-capture evidence |
| `generated/` | Reports produced by the unified runner |
| `docs/` | Progress, mapping, audit, freeze, and reporting documents |
| `config/` | Optional local configuration; no secrets may be committed |
| `tools/` | Optional extraction or instrument integration helpers |
| `verification-architecture.html` | Self-contained visual architecture and traceability explorer |
| `.github/workflows/verify.yml` | CI entry point that runs the unified verification |

## Result Vocabulary

The repository deliberately separates implementation evidence from conformance
verdicts.

| Result | Meaning |
|---|---|
| `LOCAL_PASS` | A local log, packet, or behavior matched the implemented checker criteria. This is development evidence only. |
| `LIMITED_PASS` | Core local behavior passed, but a required variant, environment, or official field was not covered. |
| `SELFCHECK_PASS` | The checker itself executed and its positive/negative fixture behaved as expected. It is not a product verdict. |
| `STANDARD_ALIGNED` | The official procedure and criteria have been mapped, but the complete official flow was not executed locally. |
| `RESTRICTED` | Required standards, network functions, instrumentation, operator data, or test access is missing. It is neither PASS nor FAIL. |
| `NOT_EXECUTED` | No qualified evidence has been supplied for that official section. |
| `OFFICIAL_PASS` / `OFFICIAL_FAIL` | Reserved for a qualified SS or accredited laboratory verdict. Local runners do not create these results. |

## What the One-Command Run Verifies

The default run validates:

- registry and suite metadata consistency;
- completeness of all 34 suite documents;
- all verdict-checker self-checks;
- replay of the included local evidence matrix;
- the TC-026..031 evidence schema and L2 adapter semantics;
- generation of the detailed progress and official-style reports.

The run does not turn missing infrastructure into PASS. When no qualified L2
manifest is present, TC-026..031 remain `NOT_EXECUTED`.

## Official and External Dependencies

The following are intentionally outside this repository:

- extracted standard text and temporary extraction directories;
- production credentials, tokens, keys, `.env` files, and SSH material;
- a qualified LTE/EPC System Simulator;
- an IMS System Simulator or accredited test laboratory;
- YD/T and operator acceptance specifications where not supplied.

The private repository includes the currently available, authorized 3GPP/ETSI
source documents that the suite already uses. It does not contain every
specification. The remaining dependencies are listed in
[`standards/README.md`](standards/README.md); affected cases remain
`RESTRICTED`, `PARTIAL`, or `NOT_EXECUTED`.

Tracked source documents use repository-relative paths or neutral placeholders.
Raw provenance under `evidence/` and runtime output under `outputs/` can still
contain original machine or server paths and are intentionally not rewritten.
The executable runners never depend on those paths.

## What One-Command Run Does Not Claim

The one-command run reproduces the repository's local verification baseline. It
does not provide the external equipment that a formal conformance campaign
needs. In particular, it cannot manufacture:

- an official `36.523-1` or `34.229-1` verdict;
- a real eNB/EPC/IMS end-to-end execution;
- a qualified SS/Anritsu/R&S/Keysight execution result;
- YD/T or operator acceptance evidence.

Those items remain `RESTRICTED`, `NOT_EXECUTED`, or `L2_PENDING` until qualified
evidence is supplied.

## Evidence and Publication Policy

- Prefer a **private/internal repository** for the first push.
- Never commit passwords, private keys, access tokens, `.env` files, or server
  credentials.
- Review raw packet captures and logs before public publication because they
  may contain internal addresses, subscriber identifiers, or operator data.
- Redact or exclude restricted evidence rather than fabricating replacement
  results.
- Keep the repository private unless the organization has explicitly confirmed
  redistribution rights for every bundled standard document and evidence file.
- Do not publish `standards/official/` outside the authorized organization.

## Key Reports

| Report | Purpose |
|---|---|
| `generated/84-本地证据复跑矩阵-20260914.md` | Replayed evidence matrix |
| `generated/85-验证例程全量自检状态-20260914.md` | Checker self-check result |
| `generated/86-TC026-031-证据Schema与L1适配器-20260914.md` | Official-section schema and L2 adapter status |
| `generated/92-验证例程详细进度总表-20260915.md` | Detailed TC-by-TC progress |
| `generated/official_report.md` | Official-style status report, not an official verdict |
| `docs/89-最终交付与汇报口径-20260915.md` | Delivery scope, limitations, and reporting language |
| `docs/91-最终冻结清单与复核日志-20260915.md` | Freeze record and verification log |
| `docs/THREE_LAYER_STATUS.md` | L0/L1/L2 implementation status by TC |
| `docs/93-TC011-L1-IPsec-SUBSCRIBE-NOTIFY-证据-20260916.md` | TC-011 local Annex C.2 Steps 4-11 evidence and boundaries |
| `docs/96-验证例程运行流程与模板说明-20260915.md` | End-to-end runner flow, templates, and result vocabulary |
| `docs/97-同事拉取复跑与结果验收流程-20260916.md` | Colleague handoff, fresh-checkout replay procedure, and result acceptance |
| `docs/98-仓库目录与文件说明-20260917.md` | Repository directories, files, evidence types, and handoff boundaries |
| `docs/99-全新克隆交接实测-20260917.md` | Measured clean-clone and colleague replay acceptance record |
| `docs/100-同事完整交接说明书-20260918.md` | Complete colleague handoff, standards bundle, environment doctor, fresh-DUT, and offline-transfer guide |
| `docs/101-同事使用与离线环境说明书-20260918.md` | Colleague usage, no-path-edit execution, standards coverage, and missing-environment guide |
| `docs/102-服务器与本机路径总表-20260918.md` | Server/local path inventory, evidence-count vocabulary, per-TC file/runner/evidence index, and handoff boundaries |
| `docs/102a-服务器完整目录清单-20260918.txt` | Complete directory and symlink inventory for the two reference server account roots |

## Adding or Changing a Case

1. Keep the internal `TC-xxx` identifier stable.
2. Add or update the official specification, clause, and line-level anchor.
3. Update the suite document and machine-readable registry.
4. Add or update an executable checker only when it has a real evidence source.
5. Preserve `RESTRICTED` or `NOT_EXECUTED` when qualified evidence is absent.
6. Run `python -X utf8 run_official_suite.py` before committing.

Start a new case from
`suites/official_tp_suites/_templates/TC-TEMPLATE.md`. The reusable template is
kept outside the top-level suite glob so it cannot be mistaken for a formal
`TC-xxx` case.
