"""Parent-seal verification for WP-0 (v0.3.1 PIN amendment scope).

Reads only; never edits parent artifacts. Console output lines prefixed
[WP0-STEP-0x] are the auditable execution record (see Path.md WP-0 log table).
"""
from __future__ import annotations

import hashlib
import json
import os

FULL_PARENT = "38c1be6afd2ab2420aa094c68ce45ee6a26b3628"
TERMINAL_CLAIM = "FINITE_DEBT_LAW_MINING_RESULTS"


def sha_file(p: str) -> str:
    """SHA-256 over buffered reads (see Path.md WP-0 section 14 for why)."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP0-STEP-01: verify the full parent commit pin (short SHAs never suffice).
def check_parent_pin(root: str) -> list[str]:
    fails: list[str] = []
    with open(os.path.join(root, "parent", "V02_SEAL.json"), encoding="utf-8") as f:
        v02 = json.load(f)
    if v02.get("sealed_commit") != FULL_PARENT:
        fails.append("PARENT-01 full parent commit mismatch (short SHA never suffices)")
    else:
        print("[WP0-STEP-01] parent commit exact: %s" % FULL_PARENT)
    if v02.get("terminal_claim") != TERMINAL_CLAIM:
        fails.append("PARENT-02 terminal claim mismatch")
    else:
        print("[WP0-STEP-01] terminal claim exact: %s" % TERMINAL_CLAIM)
    with open(os.path.join(root, "prereg", "parent_contract.yaml"), encoding="utf-8") as f:
        pc = f.read()
    for token in (FULL_PARENT,
                  "C5B1C60ADE7090C3B32000A3FF94FC376D65DF4ECAF16AA2AD227DC775995140",
                  "5C4BA61B1409A1E92263912173B749AD6BDE0CBBEB174E2CA285FEABA64BB17F",
                  "87AEA34C5BCB940EB32D3B7B6DF4199CEAEE6F44BC28E2F93612C95B6789DAF5"):
        if token not in pc:
            fails.append("PARENT-01b parent_contract missing %s..." % token[:16])
    if not any(x.startswith("PARENT-01b") for x in fails):
        print("[WP0-STEP-01] parent_contract carries full commit + seal hashes")
    for name, want_state, label in (("V02_H1_FIREWALL.json", "EMPTY", "PARENT-04"),
                                    ("V02_H2R_FIREWALL.json", "BANK_COMMITTED", "PARENT-05")):
        with open(os.path.join(root, "parent", name), encoding="utf-8") as f:
            st = json.load(f)
        # H1 has unlock:null; H2R has unlocks/unlock_count 0.
        if want_state == "EMPTY":
            ok = st.get("state") == "EMPTY"
        else:
            ok = st.get("state") == "BANK_COMMITTED" and st.get("unlocks", st.get("unlock_count", -1)) == 0
        if not ok:
            fails.append("%s %s firewall not pristine" % (label, name))
        else:
            print("[WP0-STEP-01] %s firewall pristine: %s" % (label, st.get("state")))
    return fails


# WP0-STEP-02: verify the v0.3.1 pin amendment discharges PRE_FREEZE.
def check_amendment(root: str) -> list[str]:
    fails: list[str] = []
    pin = os.path.join(root, "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md")
    if not os.path.exists(pin):
        print("[WP0-STEP-02] MISSING v0.3.1 amendment")
        return ["PIN-01 v0.3.1 amendment missing"]
    txt = open(pin, encoding="utf-8").read()
    if FULL_PARENT not in txt:
        fails.append("PIN-01 amendment lacks full parent commit")
    if "PRE_FREEZE_PARENT_PIN_REQUIRED" not in txt:
        fails.append("PIN-01 amendment does not discharge PRE_FREEZE condition")
    actual_spec = sha_file(os.path.join(root, "IMPLEMENTATION_SPEC_v0.3.md"))
    if actual_spec not in txt:
        fails.append("PIN-02 amendment v0.3 byte-hash does not match file (silent edit?)")
    if not fails:
        print("[WP0-STEP-02] amendment present; full commit + v0.3 byte-hash verified")
    return fails


# WP0-STEP-03: verify the parent bootstrap lock (read-only + manifest present).
def check_bootstrap_lock(root: str) -> list[str]:
    fails: list[str] = []
    parent = os.path.join(root, "parent")
    required = ["V01_SEAL.json", "V02_SEAL.json", "V01_FINAL_RESULT.json",
                "V02_FINAL_RESULT.json", "V02_H1_FIREWALL.json",
                "V02_H2R_FIREWALL.json", "import_ledger.json",
                "BOOTSTRAP_MANIFEST.sha256"]
    missing = [n for n in required if not os.path.exists(os.path.join(parent, n))]
    if missing:
        fails.append("BOOTSTRAP-01 parent files missing: %s" % ",".join(missing))
    else:
        print("[WP0-STEP-03] all %d bootstrap files present" % len(required))
    locked, unlocked = 0, []
    for n in required:
        p = os.path.join(parent, n)
        if not os.path.exists(p):
            continue
        try:
            ro = bool(os.stat(p).st_file_attributes & 0x1)
        except AttributeError:
            ro = not os.access(p, os.W_OK)
        if ro:
            locked += 1
        else:
            unlocked.append(n)
    if unlocked:
        fails.append("BOOTSTRAP-02 parent files not read-only locked: %s" % ",".join(unlocked))
    else:
        print("[WP0-STEP-03] parent/ read-only lock intact (%d files)" % locked)
    return fails


# WP0-STEP-04: literature status — identities exact for all 8; bytes tracked.
def check_literature_status(root: str) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warnings: list[str] = []
    with open(os.path.join(root, "external", "MANIFEST.json"), encoding="utf-8") as f:
        man = json.load(f)
    ids = {s.get("id") for s in man.get("sources", [])}
    if ids != {"L0a", "L0b", "L1", "L2", "L3", "L4", "L5", "L6"}:
        fails.append("LIT-01 manifest source set wrong: %s" % sorted(ids))
        return fails, warnings
    print("[WP0-STEP-04] manifest identities exact for L0a/L0b/L1-L6")
    for s in man["sources"]:
        b = s.get("bytes", {})
        if b.get("status") in ("FROZEN", "PINNED_VIA_PARENT_SEAL"):
            if b.get("status") == "FROZEN":
                p = os.path.join(root, "external", "papers", b.get("file", ""))
                if not os.path.exists(p):
                    fails.append("LIT-02 %s frozen file missing" % s["id"])
                else:
                    got = sha_file(p)
                    if got != b.get("sha256", ""):
                        fails.append("LIT-02 %s byte hash mismatch" % s["id"])
                    else:
                        print("[WP0-STEP-04] %s bytes frozen: %s" % (s["id"], got[:16]))
        else:
            warnings.append("LIT-PENDING %s: %s" % (s["id"], b.get("reason", "unspecified")))
    for w in warnings:
        print("[WP0-STEP-04] WARNING %s (use blocked downstream)" % w)
    return fails, warnings
