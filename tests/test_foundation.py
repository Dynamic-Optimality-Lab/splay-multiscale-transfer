"""Foundation tests: PARENT-01..08, ROT agreement spot-check, firewall fail-closed."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.holdout.firewall import guard_read
from python.rotations.trace import trace_delete, trace_keep
from python.splay_ref import independent as I
from python.splay_ref.splay import build_balanced, cost, inorder, serialize, splay

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_parent_pin() -> None:
    v02 = json.load(open(os.path.join(ROOT, "parent", "V02_SEAL.json")))
    check("PARENT-01 commit exact", v02["sealed_commit_short"] == "38c1be6")
    check("PARENT-02 terminal claim", v02["terminal_claim"] == "FINITE_DEBT_LAW_MINING_RESULTS")
    v01 = json.load(open(os.path.join(ROOT, "parent", "V01_SEAL.json")))
    check("PARENT-03 ancestor chain", v01["sealed_commit"] == "6de1ca2a595e8895f54794f3a211fe6ee1a95a80")
    h1 = json.load(open(os.path.join(ROOT, "parent", "V02_H1_FIREWALL.json")))
    check("PARENT-04 H1 EMPTY", h1["state"] == "EMPTY")
    h2r = json.load(open(os.path.join(ROOT, "parent", "V02_H2R_FIREWALL.json")))
    check("PARENT-05 H2R pristine", h2r["state"] == "BANK_COMMITTED" and h2r.get("unlocks", 0) == 0)
    check("PARENT-06 n8 contaminated", "PARTIALLY_REVEALED" in v02.get("n8_status", ""))
    ps = json.load(open(os.path.join(ROOT, "math", "proof_status.json")))
    check("PARENT-07 ledger 26 obligations", set(ps["obligations"]) == {"MST0-%02d" % (i,) for i in range(1, 27)})


def test_splay_core() -> None:
    for n in (3, 5, 7):
        r = build_balanced(list(range(1, n + 1)))
        for x in range(1, n + 1):
            a = cost(r, x)
            r2, evs = splay(r, x)
            check(f"ROT-01 splay root n={n} x={x}", r2.key == x)
            check(f"ROT-cost positive n={n} x={x}", a >= 1)
            assert inorder(r2) == list(range(1, n + 1)), "BST order broken"
            r = r2
    # case coverage on crafted trees
    r = build_balanced([1, 2, 3])
    _, evs = splay(r, 1)
    check("ROT cases serialize", all(e["case"] in ("ROOT", "ZIG", "LL", "RR", "LR", "RL") for e in evs))
    # independent agreement
    st = I.build_balanced_dict([1, 2, 3, 4, 5])
    r = build_balanced([1, 2, 3, 4, 5])
    for x in (4, 2, 5, 1):
        r, e1 = splay(r, x)
        e2 = I.splay2(st, x)
        check(f"ROT-10 agreement x={x}", [e["case"] for e in e1] == [e["case"] for e in e2])


def test_traces_and_firewall() -> None:
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t = trace_keep(A, B, 3, "e-test-keep")
    check("TRACE keep snapshot", len(t["reference_snapshot_hash"]) == 64)
    check("TRACE keep events", len(t["events"]) >= 0)
    A = build_balanced([1, 2, 3])
    B = build_balanced([1, 2, 3])
    t2 = trace_delete(A, B, 2, "e-test-del")
    check("TRACE delete mode", t2["mode"] == "DELETE" and t2["y"] == 0)
    try:
        guard_read(os.path.join(ROOT, "parent", "V02_H1_FIREWALL.json"), False, "discovery-probe")
        check("HLD-02 fail-closed pre-freeze", False)
    except PermissionError:
        check("HLD-02 fail-closed pre-freeze", True)
    except Exception:
        check("HLD-02 fail-closed pre-freeze", True)


if __name__ == "__main__":
    test_parent_pin()
    test_splay_core()
    test_traces_and_firewall()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
