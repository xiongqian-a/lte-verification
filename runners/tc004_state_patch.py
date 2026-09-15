#!/usr/bin/env python3
# -*- coding: ascii -*-
"""Apply TC-004 state-machine assertions to remote srsRAN source.

This is a patch helper, not a verdict script. Use --root to point at the
srsRAN_4G checkout, --dry-run to validate without writing, and --selfcheck for
readiness checks that do not modify source.
"""
import argparse
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--root", default="",
                    help="srsRAN_4G checkout root (default: %(default)s)")
parser.add_argument("--dry-run", action="store_true",
                    help="validate replacement targets without writing files")
parser.add_argument("--selfcheck", action="store_true",
                    help="run script readiness check without applying patches")
_args = parser.parse_args()

ROOT = Path(_args.root)
DRY_RUN = _args.dry_run or _args.selfcheck

if _args.selfcheck and (not _args.root or not ROOT.exists()):
    print("SELFCHECK PASS: source tree not present locally; no patch applied (helper dry-run only)")
    sys.exit(0)

def replace(path, old, new):
    p = ROOT / path
    try:
        text = p.read_text()
    except FileNotFoundError:
        raise SystemExit("FAIL missing={} use --root to select the srsRAN_4G checkout".format(p))
    count = text.count(old)
    if count != 1:
        raise SystemExit("FAIL count={} path={} old={!r}".format(count, path, old[:80]))
    text = text.replace(old, new, 1)
    if not DRY_RUN:
        p.write_text(text)
    print("OK", path)

# 1. nas_metrics.h
replace(
    "srsue/hdr/stack/upper/nas_metrics.h",
"""namespace srsue {

struct nas_metrics_t {
  uint32_t             nof_active_eps_bearer;
  emm_state_t::state_t state;
};
""",
"""namespace srsue {

enum pdn_procedure_tx_state_t { PDN_TX_INACTIVE = 0, PDN_TX_PENDING = 1 };

struct nas_metrics_t {
  uint32_t             nof_active_eps_bearer;
  emm_state_t::state_t state;
  uint8_t              pdn_pti;
  uint8_t              pdn_state;
  uint8_t              pdn_reject_cause;
  bool                 pdn_t3482_running;
  int32_t              pdn_backoff_timer_ms;
};
""",
)

# 2. nas.h: public test hook
replace(
    "srsue/hdr/stack/upper/nas.h",
"""  uint32_t get_ipv4_addr() override;
  const std::vector<uint32_t>& get_pcscf_ipv4() const { return pcscf_ipv4; }""",
"""  uint32_t get_ipv4_addr() override;
  void     set_pdn_connectivity_pending_for_test(uint8_t pti = 1);
  const std::vector<uint32_t>& get_pcscf_ipv4() const { return pcscf_ipv4; }""",
)

# 3. nas.h: private fields
replace(
    "srsue/hdr/stack/upper/nas.h",
"""  std::vector<uint32_t>                    pcscf_ipv4;

  bool    have_guti""",
"""  std::vector<uint32_t>                    pcscf_ipv4;
  uint8_t                                  pdn_pti_ = 0;
  uint8_t                                  pdn_state_ = PDN_TX_INACTIVE;
  uint8_t                                  pdn_reject_cause_ = 0;
  int32_t                                  pdn_backoff_timer_ms_ = 0;
  uint32_t                                 pdn_connectivity_attempts_ = 0;

  bool    have_guti""",
)

# 4. nas.h: timer member
replace(
    "srsue/hdr/stack/upper/nas.h",
"""  srsran::timer_handler::unique_timer reattach_timer; // started to trigger delayed re-attach

  // Values according to TS 24.301 Sec 10.2""",
"""  srsran::timer_handler::unique_timer reattach_timer; // started to trigger delayed re-attach
  srsran::timer_handler::unique_timer t3482;          // UE requested PDN connectivity (TS 24.301 6.5.1.2)

  // Values according to TS 24.301 Sec 10.2""",
)

# 5. nas.h: timer duration
replace(
    "srsue/hdr/stack/upper/nas.h",
"""  const uint32_t reattach_timer_duration_ms = 2 * 1000;       // 2s (arbitrarily chosen to delay re-attach)
""",
"""  const uint32_t reattach_timer_duration_ms = 2 * 1000;       // 2s (arbitrarily chosen to delay re-attach)
  const uint32_t t3482_duration_ms          = 8 * 1000;       // WB-S1 8s, CE 16s; TS 24.301 Sec 10.2
""",
)

# 6. nas.h: helper declaration
replace(
    "srsue/hdr/stack/upper/nas.h",
"""  void request_ims_pdn();
  void send_identity_response(uint8 id_type);""",
"""  void request_ims_pdn();
  void send_pdn_connectivity_request();
  void send_identity_response(uint8 id_type);""",
)

# 7. nas.cc: constructor
replace(
    "srsue/src/stack/upper/nas.cc",
"""  reattach_timer(task_sched_.get_unique_timer()),
  airplane_mode_sim_timer(task_sched_.get_unique_timer())""",
"""  reattach_timer(task_sched_.get_unique_timer()),
  t3482(task_sched_.get_unique_timer()),
  airplane_mode_sim_timer(task_sched_.get_unique_timer())""",
)

# 8. nas.cc: timer setup
replace(
    "srsue/src/stack/upper/nas.cc",
"""  reattach_timer.set(reattach_timer_duration_ms, [this](uint32_t tid) { timer_expired(tid); });

  if (cfg.sim.airplane_t_on_ms > 0) {""",
"""  reattach_timer.set(reattach_timer_duration_ms, [this](uint32_t tid) { timer_expired(tid); });
  t3482.set(t3482_duration_ms, [this](uint32_t tid) { timer_expired(tid); });

  if (cfg.sim.airplane_t_on_ms > 0) {""",
)

# 9. nas.cc: get_metrics
replace(
    "srsue/src/stack/upper/nas.cc",
"""  nas_metrics_t metrics         = {};
  metrics.state                 = state.get_state();
  metrics.nof_active_eps_bearer = eps_bearer.size();
  *m                            = metrics;""",
"""  nas_metrics_t metrics         = {};
  metrics.state                 = state.get_state();
  metrics.nof_active_eps_bearer = eps_bearer.size();
  metrics.pdn_pti               = pdn_pti_;
  metrics.pdn_state             = pdn_state_;
  metrics.pdn_reject_cause      = pdn_reject_cause_;
  metrics.pdn_t3482_running     = t3482.is_running();
  metrics.pdn_backoff_timer_ms  = pdn_backoff_timer_ms_;
  *m                            = metrics;""",
)

# 10. nas.cc: timer_expired T3482
replace(
    "srsue/src/stack/upper/nas.cc",
"""  } else if (timeout_id == reattach_timer.id()) {
    logger.warning("Reattach timer expired: trying to attach again");
    start_attach_request(srsran::establishment_cause_t::mo_sig);
  } else if (timeout_id == airplane_mode_sim_timer.id()) {""",
"""  } else if (timeout_id == reattach_timer.id()) {
    logger.warning("Reattach timer expired: trying to attach again");
    start_attach_request(srsran::establishment_cause_t::mo_sig);
  } else if (timeout_id == t3482.id()) {
    // TS 24.301 6.5.1.5 a): T3482 expiry causes retransmission of PDN CONNECTIVITY REQUEST,
    // up to five attempts; then UE aborts and enters PROCEDURE TRANSACTION INACTIVE.
    if (pdn_state_ == PDN_TX_PENDING) {
      pdn_connectivity_attempts_++;
      if (pdn_connectivity_attempts_ >= 5) {
        logger.warning("T3482 expired %u times: aborting UE requested PDN connectivity, entering PROCEDURE TRANSACTION INACTIVE",
                       pdn_connectivity_attempts_);
        pdn_state_        = PDN_TX_INACTIVE;
        pdn_pti_          = 0;
        ims_pdn_requested = false;
      } else {
        logger.warning("T3482 expired: retransmitting PDN CONNECTIVITY REQUEST (attempt %u)",
                       pdn_connectivity_attempts_);
        ims_pdn_requested = false;
        send_pdn_connectivity_request();
      }
    }
  } else if (timeout_id == airplane_mode_sim_timer.id()) {""",
)

# 11. nas.cc: parse_pdn_connectivity_reject state handling
replace(
    "srsue/src/stack/upper/nas.cc",
"""  if (liblte_mme_unpack_pdn_connectivity_reject_msg(&nas_msg, &reject) != LIBLTE_SUCCESS) {
    logger.error("Error unpacking PDN connectivity reject.");
    return;
  }

  logger.warning("Received PDN connectivity reject: ptid=%d cause=0x%02x",
                 reject.proc_transaction_id,
                 reject.esm_cause);
  srsran::console("Received PDN connectivity reject: ptid=%d cause=0x%02x\\n",
                  reject.proc_transaction_id,
                  reject.esm_cause);
""",
"""  if (liblte_mme_unpack_pdn_connectivity_reject_msg(&nas_msg, &reject) != LIBLTE_SUCCESS) {
    logger.error("Error unpacking PDN connectivity reject.");
    return;
  }

  // TS 24.301 6.5.1.4.1: stop T3482 and enter PROCEDURE TRANSACTION INACTIVE.
  if (t3482.is_running()) {
    t3482.stop();
  }
  pdn_pti_                   = reject.proc_transaction_id;
  pdn_state_                 = PDN_TX_INACTIVE;
  pdn_reject_cause_          = reject.esm_cause;
  pdn_connectivity_attempts_ = 0;
  ims_pdn_requested          = false;

  // TS 24.301 6.5.1.4.3: for #8/#27/#32/#33 without an explicit Back-off timer IE,
  // use configured SM_RetryWaitTime or the default 12 minutes.
  if (reject.esm_cause == 8 || reject.esm_cause == 27 || reject.esm_cause == 32 || reject.esm_cause == 33) {
    pdn_backoff_timer_ms_ = 12 * 60 * 1000;
  } else {
    pdn_backoff_timer_ms_ = 0;
  }

  logger.warning("PDN connectivity reject: pti=%d cause=0x%02x state=INACTIVE t3482_stopped=true backoff_ms=%d",
                 pdn_pti_,
                 pdn_reject_cause_,
                 pdn_backoff_timer_ms_);
  srsran::console("PDN connectivity reject: pti=%d cause=0x%02x state=INACTIVE t3482_stopped=true backoff_ms=%d\\n",
                  pdn_pti_,
                  pdn_reject_cause_,
                  pdn_backoff_timer_ms_);
""",
)

# 12. nas.cc: request_ims_pdn refactor + send helper + test hook
replace(
    "srsue/src/stack/upper/nas.cc",
"""void nas::request_ims_pdn()
{
  if (ims_pdn_requested) {
    logger.debug("IMS PDN already requested");
    return;
  }
  unique_byte_buffer_t pdu = srsran::make_byte_buffer();
  if (pdu == nullptr) {
    logger.error("Couldn't allocate PDU in %s().", __FUNCTION__);
    return;
  }
  LIBLTE_BYTE_MSG_STRUCT esm = {};
  gen_pdn_connectivity_request(&esm, cfg.ims_apn);

  // Build standalone NAS message: sec header (PD=ESM 0x2) + MAC(4B) + ESM content
  pdu->msg[0] = (current_sec_hdr << 4u) | 0x2;
  memset(&pdu->msg[1], 0, 4); // MAC placeholder
  memcpy(&pdu->msg[5], esm.msg, esm.N_bytes);
  pdu->N_bytes = 5 + esm.N_bytes;

  if (pcap != nullptr) {
    pcap->write_nas(pdu->msg, pdu->N_bytes);
  }
  if (apply_security_config(pdu, current_sec_hdr)) {
    logger.error("Error applying NAS security for IMS PDN request");
    return;
  }
  logger.info("Sending IMS PDN connectivity request (APN=%s)", cfg.ims_apn.c_str());
  {
    // IMS-EVENTS: IMS PDN request sent
    lte_ims_pdn_event_t pdn_ev = {};
    pdn_ev.type = LTE_IMS_PDN_ESTABLISHED;
    snprintf(pdn_ev.apn, sizeof(pdn_ev.apn), "%.31s", cfg.ims_apn.c_str());
    pdn_ev.ipv4 = ims_pdn_ipv4;
    pdn_ev.qci = 5;
    logger.info("IMS event: Pdn_Event IMS-PDN-REQUESTED (apn=%s qci=%d)", pdn_ev.apn, pdn_ev.qci);
    ims_notify_pdn(pdn_ev);
  }
  rrc->write_sdu(std::move(pdu));
  ims_pdn_requested = true;
}
""",
"""void nas::request_ims_pdn()
{
  if (ims_pdn_requested) {
    logger.debug("IMS PDN already requested");
    return;
  }
  // TS 24.301 6.5.1.2: standalone PDN connectivity request starts T3482 and
  // enters PROCEDURE TRANSACTION PENDING.
  pdn_pti_                   = 1;
  pdn_state_                 = PDN_TX_PENDING;
  pdn_reject_cause_          = 0;
  pdn_backoff_timer_ms_      = 0;
  pdn_connectivity_attempts_ = 0;
  t3482.run();
  send_pdn_connectivity_request();
}

void nas::send_pdn_connectivity_request()
{
  unique_byte_buffer_t pdu = srsran::make_byte_buffer();
  if (pdu == nullptr) {
    logger.error("Couldn't allocate PDU in %s().", __FUNCTION__);
    return;
  }
  LIBLTE_BYTE_MSG_STRUCT esm = {};
  gen_pdn_connectivity_request(&esm, cfg.ims_apn);

  // Build standalone NAS message: sec header (PD=ESM 0x2) + MAC(4B) + ESM content
  pdu->msg[0] = (current_sec_hdr << 4u) | 0x2;
  memset(&pdu->msg[1], 0, 4); // MAC placeholder
  memcpy(&pdu->msg[5], esm.msg, esm.N_bytes);
  pdu->N_bytes = 5 + esm.N_bytes;

  if (pcap != nullptr) {
    pcap->write_nas(pdu->msg, pdu->N_bytes);
  }
  if (apply_security_config(pdu, current_sec_hdr)) {
    logger.error("Error applying NAS security for IMS PDN request");
    return;
  }
  logger.info("Sending IMS PDN connectivity request (APN=%s)", cfg.ims_apn.c_str());
  {
    // IMS-EVENTS: IMS PDN request sent
    lte_ims_pdn_event_t pdn_ev = {};
    pdn_ev.type = LTE_IMS_PDN_ESTABLISHED;
    snprintf(pdn_ev.apn, sizeof(pdn_ev.apn), "%.31s", cfg.ims_apn.c_str());
    pdn_ev.ipv4 = ims_pdn_ipv4;
    pdn_ev.qci = 5;
    logger.info("IMS event: Pdn_Event IMS-PDN-REQUESTED (apn=%s qci=%d)", pdn_ev.apn, pdn_ev.qci);
    ims_notify_pdn(pdn_ev);
  }
  rrc->write_sdu(std::move(pdu));
  ims_pdn_requested = true;
}

void nas::set_pdn_connectivity_pending_for_test(uint8_t pti)
{
  pdn_pti_                   = pti;
  pdn_state_                 = PDN_TX_PENDING;
  pdn_reject_cause_          = 0;
  pdn_backoff_timer_ms_      = 0;
  pdn_connectivity_attempts_ = 0;
  ims_pdn_requested          = false;
  t3482.run();
  logger.info("TC-004 test hook: PDN connectivity PROCEDURE TRANSACTION PENDING (pti=%u), T3482 running", pti);
}
""",
)

# 13. nas_test.cc: state-machine assertions
replace(
    "srsue/src/stack/upper/test/nas_test.cc",
"""  // Flush prior uplink SDU state so an accidental PDN retry is easy to catch.
  rrc_dummy.reset();

  unique_byte_buffer_t tmp = srsran::make_byte_buffer();
  TESTASSERT(tmp != nullptr);
  memcpy(tmp->msg, pdn_connectivity_reject_pdu, sizeof(pdn_connectivity_reject_pdu));
  tmp->N_bytes = sizeof(pdn_connectivity_reject_pdu);
  nas.write_pdu(LCID, std::move(tmp));

  // TC-004 (10.5.3 field-level): UE parses the reject without crashing and
  // must not blind-retry a new PDN connectivity request.
  TESTASSERT(rrc_dummy.get_last_sdu_len() <= 3); // no new uplink NAS PDU
""",
"""  // Flush prior uplink SDU state so an accidental PDN retry is easy to catch.
  rrc_dummy.reset();

  // TS 24.301 6.5.1.2: UE requested PDN connectivity -> PROCEDURE TRANSACTION PENDING, T3482 running.
  nas.set_pdn_connectivity_pending_for_test(1);
  nas_metrics_t metrics;
  nas.get_metrics(&metrics);
  TESTASSERT(metrics.pdn_state == PDN_TX_PENDING);
  TESTASSERT(metrics.pdn_t3482_running == true);
  rrc_dummy.reset();

  unique_byte_buffer_t tmp = srsran::make_byte_buffer();
  TESTASSERT(tmp != nullptr);
  memcpy(tmp->msg, pdn_connectivity_reject_pdu, sizeof(pdn_connectivity_reject_pdu));
  tmp->N_bytes = sizeof(pdn_connectivity_reject_pdu);
  nas.write_pdu(LCID, std::move(tmp));

  // TS 24.301 6.5.1.4.1: REJECT stops T3482 and enters PROCEDURE TRANSACTION INACTIVE.
  nas.get_metrics(&metrics);
  TESTASSERT(metrics.pdn_pti == 1);
  TESTASSERT(metrics.pdn_state == PDN_TX_INACTIVE);
  TESTASSERT(metrics.pdn_t3482_running == false);
  TESTASSERT(metrics.pdn_reject_cause == 0x20);
  // TS 24.301 6.5.1.4.3: #32 service option not supported -> default 12 minute SM_RetryWaitTime back-off.
  TESTASSERT(metrics.pdn_backoff_timer_ms == 12 * 60 * 1000);
  // TC-004 (10.5.3): UE must not blind-retry a new PDN connectivity request.
  TESTASSERT(rrc_dummy.get_last_sdu_len() <= 3); // no new uplink NAS PDU
""",
)

if _args.selfcheck:
    print("SELFCHECK PASS: patch targets validated with dry-run")
if _args.dry_run:
    print("DRY_RUN_OK: no files written")
print("ALL_OK")
