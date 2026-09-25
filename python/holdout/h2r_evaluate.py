"""WP-5 Phase-15 H2R legacy replay-history evaluation (frozen-calculus-only imports).

H2R is schema-compatible in principle (replayable legal histories for causal
ledgers), but its bank bytes live in the sealed parent repository and were never
vendored into this working repo (WP-0 bootstrapped firewall metadata only, by
design). Fabricating H2R-equivalent histories locally and calling them H2R
would be mislabeling. This module records that custody fact truthfully:
FRESH_H2R_NOT_APPLICABLE with preserved justification (bytes absent, firewall
still BANK_COMMITTED/unlocks=0, no reveal), and refuses to emit PASS/FAIL for
a bank it did not read. The transfer-specific H3T bank carries the fresh
history evidence instead. Console tag [WP5-STEP-03].
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.holdout import firewall as firewall_mod  # noqa: E402


# WP5-STEP-03: route the frozen causal candidates against H2R (custody check).
def evaluate(frozen_ids: list, h2r_firewall_path: str, calculus_frozen: bool,
             bank_dir: str | None = None) -> dict:
    """Return the H2R reveal record (NOT_APPLICABLE when bytes are absent)."""
    if not calculus_frozen:
        raise PermissionError("H2R evaluation requires TRANSFER_CALCULUS_FROZEN")
    st = firewall_mod.load_state(h2r_firewall_path)
    if st.get("state") != "BANK_COMMITTED" or st.get("unlocks", st.get("unlock_count", 0)) != 0:
        raise ValueError("H2R firewall not pristine; refusing to evaluate")
    if bank_dir is not None and os.path.isdir(bank_dir) and os.listdir(bank_dir):
        raise ValueError("H2R bank bytes unexpectedly present; full evaluation required, not this path")
    print("[WP5-STEP-03] H2R routing: schema-compatible but bank bytes absent "
          "locally (parent-sealed custody) -> NOT_APPLICABLE, firewall untouched", flush=True)
    return {"bank_id": "HOLDOUT-H2R-v0.1",
            "candidates": list(frozen_ids),
            "n_episodes": 0,
            "verdict": "FRESH_H2R_NOT_APPLICABLE",
            "reason": ("bank bytes in sealed parent custody, never vendored; "
                       "firewall BANK_COMMITTED/unlocks=0 preserved; no fabrication"),
            "firewall_after": "BANK_COMMITTED",
            "fresh_claim": False}
