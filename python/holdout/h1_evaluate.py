"""WP-5 Phase-15 H1 legacy state-pair evaluation (frozen-calculus-only imports).

H1 is a state-pair bank (EMPTY at freeze). The frozen WP-5 candidates are causal
history ledgers: injection is charged per A-side rotation and repayment per KEEP
edge, so evaluation requires replayable histories. Per spec S14.2, H1 cannot
validate causal provenance requiring history absent from H1. This module records
that routing verdict truthfully: FRESH_H1_NOT_APPLICABLE with preserved
justification, zero episodes read, firewall left EMPTY. No PASS/FAIL is claimed
for an incompatible bank. Console tag [WP5-STEP-03].
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.holdout import firewall as firewall_mod  # noqa: E402


# WP5-STEP-03: route the frozen causal candidates against H1 (schema check only).
def evaluate(frozen_ids: list, h1_firewall_path: str, calculus_frozen: bool) -> dict:
    """Return the H1 reveal record (NOT_APPLICABLE for causal ledgers)."""
    if not calculus_frozen:
        raise PermissionError("H1 evaluation requires TRANSFER_CALCULUS_FROZEN")
    st = firewall_mod.load_state(h1_firewall_path)
    if st.get("state") != "EMPTY":
        raise ValueError("H1 firewall no longer EMPTY; refusing to mislabel")
    print("[WP5-STEP-03] H1 routing: %d causal candidates require histories; "
          "H1 is EMPTY state-pair storage -> NOT_APPLICABLE" % len(frozen_ids), flush=True)
    return {"bank_id": "HOLDOUT-H1-v0.1",
            "candidates": list(frozen_ids),
            "n_episodes": 0,
            "verdict": "FRESH_H1_NOT_APPLICABLE",
            "reason": ("causal history ledgers require replayable histories; "
                       "H1 stores pair states only and is EMPTY"),
            "firewall_after": "EMPTY",
            "fresh_claim": False}
