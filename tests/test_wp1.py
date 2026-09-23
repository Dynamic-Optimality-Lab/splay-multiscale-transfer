"""WP-1 stress tests: exhaustive agreement, tamper rejection, idempotency, perf.

Heavy checks stay out of the fast suites; this file runs the WP-1 battery.
Each test prints WP1STRESS-<id> lines; any failure exits non-zero.
"""
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles import import_parent  # noqa: E402
from python.cycles.enumerate import PairDomain, build_node_tree  # noqa: E402
from python.splay_ref import independent as I  # noqa: E402
from python.splay_ref.splay import cost, serialize, splay  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("WP1STRESS-PASS " if cond else "WP1STRESS-FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_exhaustive_n4_agreement() -> None:
    dom = PairDomain(4)
    reached = dom.reachable()
    check("WP1STRESS-N4 count 196", len(reached) == 196)
    bad = 0
    t0 = time.time()
    for pid in sorted(reached):
        a_id, b_id = dom.unpid(pid)
        for x in range(1, 5):
            for mode in ("KEEP", "DELETE"):
                tgt, a, y = dom.edge(pid, x, mode)
                A = build_node_tree(dom.shapes, a_id, 4)
                B = build_node_tree(dom.shapes, b_id, 4)
                stA, stB = I.from_nodes(A), I.from_nodes(B)
                if I.cost2(stA, x) != a or (I.cost2(stB, x) != y if mode == "KEEP" else False):
                    bad += 1
                    continue
                evA = I.splay2(stA, x)
                A2, ev1 = splay(A, x)
                if [e["case"] for e in ev1] != [e["case"] for e in evA]:
                    bad += 1
                    continue
                if mode == "KEEP":
                    evB = I.splay2(stB, x)
                    B2, ev2 = splay(B, x)
                    if [e["case"] for e in ev2] != [e["case"] for e in evB]:
                        bad += 1
                    elif I.serialize2(stB) != serialize(B2):
                        bad += 1
                if I.serialize2(stA) != serialize(A2):
                    bad += 1
    dt = time.time() - t0
    print("WP1STRESS-N4 exhaustive edges=%d seconds=%.1f" % (len(reached) * 8, dt))
    check("WP1STRESS-N4 zero dual-core divergences", bad == 0)


def test_tampered_cycle_rejected() -> None:
    dom = PairDomain(4)
    base = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    if not os.path.exists(os.path.join(base, "v01baseline")):
        print("WP1STRESS-SKIP tamper test (import not executed yet)")
        return
    cyc = json.load(open(os.path.join(base, "v01baseline", "v01",
                                      "critical_n4_canonical_cycles.json")))[0]
    rep = import_parent.replay_cycle(dom, cyc)
    check("WP1STRESS-TAMPER genuine cycle clean", not rep["mismatches"] and rep["closed"])
    bad = json.loads(json.dumps(cyc))
    bad["edges"][0]["target"] = (bad["edges"][0]["target"] + 1) % 196
    rep2 = import_parent.replay_cycle(dom, bad)
    check("WP1STRESS-TAMPER corrupted target caught", bool(rep2["mismatches"]) or not rep2["closed"])
    bad2 = json.loads(json.dumps(cyc))
    bad2["edges"][0]["key"] = 5 - bad2["edges"][0]["key"] if bad2["edges"][0]["key"] != 2 else 3
    rep3 = import_parent.replay_cycle(dom, bad2)
    check("WP1STRESS-TAMPER corrupted key caught",
          bool(rep3["mismatches"]) or not rep3["closed"] or rep3["ratio"] != rep["ratio"])


def test_expand_idempotent() -> None:
    import hashlib
    from python.cycles import circulation as circ_mod
    from python.cycles import expand as expand_mod
    dom = PairDomain(4)
    base = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    if not os.path.exists(os.path.join(base, "v01baseline")):
        print("WP1STRESS-SKIP expand test (import not executed yet)")
        return
    cyc = json.load(open(os.path.join(base, "v01baseline", "v01",
                                      "critical_n4_canonical_cycles.json")))[0]
    h = lambda ex: hashlib.sha256(json.dumps(ex, sort_keys=True).encode()).hexdigest()
    e1 = expand_mod.expand_cycle(dom, 4, 0, cyc)
    e2 = expand_mod.expand_cycle(dom, 4, 0, cyc)
    check("WP1STRESS-IDEM expansion deterministic", h(e1) == h(e2) and e1["closed"])
    c = circ_mod.circulate(e1, 3, 2)
    check("WP1STRESS-IDEM critical slack zero", (c["scaled_slack_num"], c["scaled_slack_den"]) == (0, 1))


if __name__ == "__main__":
    test_exhaustive_n4_agreement()
    test_tampered_cycle_rejected()
    test_expand_idempotent()
    print("WP1STRESS-FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
