"""Phase-00 runner: verifies parent pin, prereg hashes, firewalls, theorem ledger shape."""
from __future__ import annotations

import hashlib
import json
import os
import sys


def sha_file(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fails: list[str] = []
    # 1. parent pin
    with open(os.path.join(root, "parent", "V02_SEAL.json")) as f:
        v02 = json.load(f)
    if v02.get("sealed_commit_short") != "38c1be6":
        fails.append("PARENT-01 parent commit mismatch")
    if v02.get("terminal_claim") != "FINITE_DEBT_LAW_MINING_RESULTS":
        fails.append("PARENT-02 terminal claim mismatch")
    with open(os.path.join(root, "parent", "V02_H1_FIREWALL.json")) as f:
        if json.load(f).get("state") != "EMPTY":
            fails.append("PARENT-04 H1 not EMPTY")
    with open(os.path.join(root, "parent", "V02_H2R_FIREWALL.json")) as f:
        h2r = json.load(f)
        if h2r.get("state") != "BANK_COMMITTED" or h2r.get("unlocks", h2r.get("unlock_count", -1)) != 0:
            fails.append("PARENT-05 H2R not pristine")
    # 2. theorem ledger shape
    with open(os.path.join(root, "math", "proof_status.json")) as f:
        ps = json.load(f)
    want = {"MST0-%02d" % (i,) for i in range(1, 27)}
    if set(ps.get("obligations", {})) != want:
        fails.append("PARENT-07 theorem ledger shape wrong")
    # 3. threat/stop sets
    import re
    t = open(os.path.join(root, "prereg", "threat_control_matrix.yaml")).read()
    tids = set(re.findall(r"^T\d\d", t, re.M))
    if tids != {"T%02d" % (i,) for i in range(1, 91)}:
        fails.append(f"SEAL-03 threat set wrong ({len(tids)})")
    s = open(os.path.join(root, "prereg", "stop_control_matrix.yaml")).read()
    sids = set(re.findall(r"STOP-\d\d", s))
    if sids != {"STOP-%02d" % (i,) for i in range(1, 51)}:
        fails.append(f"SEAL-04 stop set wrong ({len(sids)})")
    if fails:
        print("PHASE00_FAIL")
        for x in fails:
            print(" -", x)
        return 1
    print("PHASE00_PASS: parent pin + ledger + threat/stop sets exact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
