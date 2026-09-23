"""Phase-00 runner: verifies full parent pin (v0.3.1 amendment), prereg hashes,
firewalls, theorem-gate shape, and solver-freeze record.

NOTE: PHASE00_PASS means the WP-0 *checks* pass. It is not itself the
FOUNDATION_FROZEN seal claim (see Path.md); WP-1 certified consumption additionally
requires MST0-01 == REVIEWED per the gate matrix.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys


def sha_file(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


FULL_PARENT = "38c1be6afd2ab2420aa094c68ce45ee6a26b3628"


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fails: list[str] = []
    # 1. parent pin: full SHA, not short
    with open(os.path.join(root, "parent", "V02_SEAL.json")) as f:
        v02 = json.load(f)
    if v02.get("sealed_commit") != FULL_PARENT:
        fails.append("PARENT-01 full parent commit mismatch (short SHA never suffices)")
    if v02.get("terminal_claim") != "FINITE_DEBT_LAW_MINING_RESULTS":
        fails.append("PARENT-02 terminal claim mismatch")
    with open(os.path.join(root, "prereg", "parent_contract.yaml")) as f:
        pc = f.read()
    for token in [FULL_PARENT, "C5B1C60ADE7090C3B32000A3FF94FC376D65DF4ECAF16AA2AD227DC775995140",
                  "5C4BA61B1409A1E92263912173B749AD6BDE0CBBEB174E2CA285FEABA64BB17F",
                  "87AEA34C5BCB940EB32D3B7B6DF4199CEAEE6F44BC28E2F93612C95B6789DAF5"]:
        if token not in pc:
            fails.append(f"PARENT-01b parent_contract missing {token[:16]}...")
    with open(os.path.join(root, "parent", "V02_H1_FIREWALL.json")) as f:
        if json.load(f).get("state") != "EMPTY":
            fails.append("PARENT-04 H1 not EMPTY")
    with open(os.path.join(root, "parent", "V02_H2R_FIREWALL.json")) as f:
        h2r = json.load(f)
        if h2r.get("state") != "BANK_COMMITTED" or h2r.get("unlocks", h2r.get("unlock_count", -1)) != 0:
            fails.append("PARENT-05 H2R not pristine")
    # 2. v0.3.1 pin amendment present, pins full commit + v0.3 byte hash
    pin = os.path.join(root, "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md")
    if not os.path.exists(pin):
        fails.append("PIN-01 v0.3.1 amendment missing")
    else:
        txt = open(pin, encoding="utf-8").read()
        if FULL_PARENT not in txt:
            fails.append("PIN-01 amendment lacks full parent commit")
        if "PRE_FREEZE_PARENT_PIN_REQUIRED" not in txt:
            fails.append("PIN-01 amendment does not discharge PRE_FREEZE condition")
        actual_spec = sha_file(os.path.join(root, "IMPLEMENTATION_SPEC_v0.3.md"))
        if actual_spec not in txt:
            fails.append("PIN-02 amendment v0.3 byte-hash does not match file (silent edit?)")
    # 3. theorem ledger + gate matrix shape (26 obligations, first-consumer fields)
    with open(os.path.join(root, "math", "proof_status.json")) as f:
        ps = json.load(f)
    want = {"MST0-%02d" % (i,) for i in range(1, 27)}
    if set(ps.get("obligations", {})) != want:
        fails.append("PARENT-07 theorem ledger shape wrong")
    gm = open(os.path.join(root, "prereg", "theorem_gate_matrix.yaml")).read()
    for oid in sorted(want):
        if oid not in gm:
            fails.append(f"GATE-01 matrix missing {oid}")
            break
    else:
        if gm.count("first_consumer:") != 26 or gm.count("required_status_before_consumption: REVIEWED") != 26:
            fails.append("GATE-01 matrix lacks first-consumer/REVIEWED fields")
        m1 = re.search(r"MST0-01:\n(?:.*\n){1,2}.*first_consumer: (\S+)", gm)
        if not m1 or m1.group(1) != "WP-1":
            fails.append("GATE-01 MST0-01 first consumer must be WP-1")
    # 3b. L6 translation contract completeness (language + proposed definitions frozen)
    try:
        import yaml as _yaml
    except ImportError:
        fails.append("L6-00 pyyaml unavailable for contract check")
    else:
        with open(os.path.join(root, "prereg", "l6_translation_v0.3.yaml"), encoding="utf-8") as f:
            l6 = _yaml.safe_load(f)
        objs = l6.get("objects", {})
        expected = l6.get("declared_top_level_objects")
        if expected is None or len(objs) != expected:
            fails.append(f"L6-00 preregistered object set changed (found {len(objs)}, declared {expected})")
        for name, rec in objs.items():
            for field in ("source_identity", "proposed_pair_access_definition",
                          "fallback_pa_native_object", "fallback_pa_native_definition",
                          "mapping_status", "obligation"):
                if field not in rec:
                    fails.append(f"L6-00 {name} missing {field}")
                    break
            if rec.get("mapping_status") != "UNRESOLVED_PRE_PROOF":
                fails.append(f"L6-00 {name} must start UNRESOLVED_PRE_PROOF")
        for rule in ("fallback_activation_rule", "no_invention_rule"):
            if rule not in l6:
                fails.append(f"L6-00 missing {rule}")
        if "UNRESOLVED_PRE_PROOF" not in l6.get("status_vocabulary", []):
            fails.append("L6-00 status vocabulary lacks UNRESOLVED_PRE_PROOF")
    # 4. threat/stop sets exact
    t = open(os.path.join(root, "prereg", "threat_control_matrix.yaml")).read()
    tids = set(re.findall(r"^T\d\d", t, re.M))
    if tids != {"T%02d" % (i,) for i in range(1, 91)}:
        fails.append(f"SEAL-03 threat set wrong ({len(tids)})")
    s = open(os.path.join(root, "prereg", "stop_control_matrix.yaml")).read()
    sids = set(re.findall(r"STOP-\d\d", s))
    if sids != {"STOP-%02d" % (i,) for i in range(1, 51)}:
        fails.append(f"SEAL-04 stop set wrong ({len(sids)})")
    # 5. solver freeze record exists; synthesis blocked until a backend is frozen
    sb = os.path.join(root, "prereg", "solver_backends.yaml")
    if not os.path.exists(sb):
        fails.append("SOLV-01 solver_backends.yaml missing (freeze must precede synthesis)")
    elif "synthesis_authorized: false" not in open(sb).read():
        fails.append("SOLV-01 solver freeze record malformed")
    # 6. prereg_sha256 covers the amendment + solver record
    pz = open(os.path.join(root, "prereg", "prereg_sha256.txt")).read()
    if "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md" not in pz:
        fails.append("PIN-03 prereg_sha256 omits the v0.3.1 amendment")
    if "solver_backends.yaml" not in pz:
        fails.append("SOLV-02 prereg_sha256 omits solver_backends.yaml")
    if fails:
        print("PHASE00_FAIL")
        for x in fails:
            print(" -", x)
        return 1
    print("PHASE00_PASS: full-SHA parent pin + amendment + gates + solver record exact")
    print("NOTE: WP-1 entry needs FOUNDATION_FROZEN only; certified consumption waits on")
    print("the WP-1 pre-consumption subgate (MST0-01 == REVIEWED).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
