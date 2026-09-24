"""Fail-closed sealed-bank firewall. Discovery modules must call
guard_read() before touching any bank; it raises unless the bank state
machine permits the (phase, calculus-frozen) context."""
from __future__ import annotations

import json
import os

STATES = {"EMPTY", "BANK_COMMITTED", "TRANSFER_CALCULUS_FROZEN", "UNLOCKED_ONCE"}


def load_state(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def guard_read(state_path: str, calculus_frozen: bool, purpose: str) -> dict:
    st = load_state(state_path)
    state = st.get("state")
    if state in ("EMPTY", "BANK_COMMITTED") and not calculus_frozen:
        raise PermissionError(f"HOLDOUT_EARLY_READ blocked ({purpose}): {state}")
    if state == "UNLOCKED_ONCE" and st.get("unlock_count", 1) >= 1 and not st.get("reveal_record"):
        raise PermissionError("fresh bank second unlock blocked (STOP-30)")
    return st


def transition_commit(state_path: str, commitment: dict) -> dict:
    st = {"state": "BANK_COMMITTED", "commitment": commitment, "unlock_count": 0}
    os.makedirs(os.path.dirname(state_path) or ".", exist_ok=True)
    with open(state_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(st, sort_keys=True, indent=2) + "\n")
    return st
