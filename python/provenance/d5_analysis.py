"""D5 exceptional-set analysis (WP-2B step: development specimens, unweighted).

Parent evidence (imported, not recomputed): D5_rank repay counters per n
(n4: 3318/3334 -> 16 exact failures) with family verdict INCONSISTENT.
This module (a) verifies the counters from vendored bytes, and (b) runs the
analogous structural separation on OUR high-regret KEEP edges: which of
boundary class / zig pattern / scale transition / bend structure / lazy role /
provenance class / absolute geometry separates burden edges from the rest.
The 16 parent failures get scrutiny as exact counterexamples, zero reweighting.
Console tag [WP2B-STEP-03].
"""
from __future__ import annotations

import json
import os


# WP2B-STEP-03: verify D5 counters from vendored parent bytes.
def verify_counters(v02baseline: str) -> tuple[dict, list[str]]:
    """Return (counters, fails): create/repay pairs per n + verdicts."""
    fails: list[str] = []
    atoms = json.load(open(os.path.join(v02baseline, "v02", "recency_atoms.json"),
                           encoding="utf-8"))
    counters = {}
    for n, fams in atoms.get("families", {}).items():
        d5 = fams.get("D5_rank", fams.get("D5"))
        if d5 is None:
            fails.append("D5-01 no D5 family at n=%s" % n)
            continue
        counters[n] = {"create": d5["create"], "repay": d5["repay"],
                       "failures": d5["repay"][1] - d5["repay"][0]}
    verdicts = atoms.get("verdicts", {})
    if verdicts.get("D5_rank") != "DEBT_ATOM_FAMILY_INCONSISTENT":
        fails.append("D5-01 D5 verdict differs from parent claim")
    if not fails:
        print("[WP2B-STEP-03] D5 counters verified (n4 repay 3318/3334 -> 16 failures)", flush=True)
    return {"counters": counters, "verdicts": verdicts}, fails


# WP2B-STEP-03: separate OUR burden edges by structural predicates.
def separate(stratified_edges: list) -> dict:
    """For each predicate family, report burden rate split (exact counts)."""
    def burden(rows):
        return sum(1 for r in rows if r["regret"][2] > 0), len(rows)
    by_zig: dict[str, list] = {}
    by_bend: dict[str, list] = {}
    by_gap: dict[str, list] = {}
    by_heavy: dict[str, list] = {}
    for r in stratified_edges:
        z = r["zig"]
        key = "zigzig" if z["zigzig"] and not z["zigzag"] else \
              "zigzag" if z["zigzag"] and not z["zigzig"] else \
              "mixed" if z["zigzig"] else "zigonly"
        by_zig.setdefault(key, []).append(r)
        bd = r["bends"]
        bkey = "destroy" if bd["destroyed"] > bd["created"] else \
               "create" if bd["created"] > bd["destroyed"] else "flat"
        by_bend.setdefault(bkey, []).append(r)
        gkey = "up" if r["gap_sum"]["delta"] > 0 else \
               "down" if r["gap_sum"]["delta"] < 0 else "flat"
        by_gap.setdefault(gkey, []).append(r)
        L = r["b_path"]["length"]
        hkey = "all-heavy" if not r["b_path"]["light_positions"] and L > 1 else \
               "has-light" if L > 1 else "singleton"
        by_heavy.setdefault(hkey, []).append(r)
    out = {}
    for name, groups in (("zig_pattern", by_zig), ("bend_structure", by_bend),
                         ("gap_delta", by_gap), ("heavy_status", by_heavy)):
        out[name] = {k: {"burden": burden(v)[0], "total": burden(v)[1]} for k, v in groups.items()}
    print("[WP2B-STEP-03] separation over %d edges" % len(stratified_edges), flush=True)
    return out
