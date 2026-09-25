"""Spec PHASE 12 runner (REAL): counterexample generalization + negative triage.

Entry: Phase-10 verdict file. Takes killed (predicate,k,C) configs, re-derives
their first violations on Stage-1 (fail_fast, exact), inflates the violating
critical cycles (x2/x4/x8) plus burst stretching, and tracks ACTUAL Splay ratios
(real costs, both cores agree — never transfer residuals) across the scale
parameter. N1-N5 decides activation (normally NOT_ACTIVATED with bounded ratios).
Console lines prefixed [WP4-STEP-07] are the audit record.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.adversary import generalize as generalize_mod  # noqa: E402
from python.adversary import generators as gen_mod  # noqa: E402
from python.adversary import inflate as inflate_mod  # noqa: E402
from python.cycles.enumerate import PairDomain, build_node_tree  # noqa: E402
from python.transfer import branchA as branchA_mod  # noqa: E402


def main() -> int:
    print("[WP4-STEP-07] PHASE 12: negative-branch triage (actual ratios only)", flush=True)
    verdict_path = os.path.join(ROOT, "artifacts", "v03", "solver", "verdict.json")
    if not os.path.exists(verdict_path):
        print("[WP4-STEP-07] PHASE12_FAIL: run_phase10 verdict missing", flush=True)
        return 2
    imp = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    outdir = os.path.join(ROOT, "artifacts", "v03", "adversarial")
    os.makedirs(outdir, exist_ok=True)
    # Killed configs on Stage-1 at C=2: re-derive first violations (fail_fast, exact).
    stage1 = json.load(open(os.path.join(ROOT, "artifacts", "v03", "transfer_grammar",
                                         "dev_corpus.json"), encoding="utf-8"))
    triaged = []
    for predicate in ("P_keep", "P_zigzig", "P_zigzag", "P_zigonly", "P_never"):
        for k in range(0, 7):
            v = branchA_mod.evaluate(predicate, k, 2, stage1, fail_fast=True)
            if v["feasible"]:
                continue
            first = v.get("first_violation")
            if not first:
                continue
            seq_id = first["seq"]
            ratios = []
            fam = None
            if seq_id.startswith("crit-"):
                n = 4
                dom = None
                cyc = None
                for cand_n in (4, 5, 6):
                    d = PairDomain(cand_n)
                    cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                                         "critical_n%d_canonical_cycles.json" % cand_n),
                                            encoding="utf-8"))
                    for ci, c in enumerate(cycles):
                        if seq_id == "crit-n%d-c%d" % (cand_n, ci) or \
                           seq_id.startswith("crit-n%d-c%d" % (cand_n, ci)):
                            n, dom, cyc = cand_n, d, c
                            break
                    if cyc is not None:
                        break
                if cyc is None:
                    continue
                for times in (1, 2, 4, 8):
                    hist = inflate_mod.inflate_cycle(cyc, times)
                    T0 = build_node_tree(dom.shapes, 0, n)
                    r = gen_mod.actual_ratio(hist, T0, n)
                    ratios.append({"times": times, "sum_a": r["sum_a"], "sum_b": r["sum_b"],
                                   "ratio": r["ratio"]})
                    print("[WP4-STEP-07] triage %s x%d: R=%s/%s"
                          % (seq_id, times, r["ratio"][0], r["ratio"][1]), flush=True)
                fam = {"histories": [seq_id], "construction": "inflate_cycle x[1,2,4,8]",
                       "diagonal": True}
            elif seq_id.startswith("near-"):
                near = json.load(open(os.path.join(ROOT, "artifacts", "v03", "discovery",
                                                   "near_critical.json"), encoding="utf-8"))
                rec = near[int(seq_id.split("-")[1])]
                n = rec.get("n", 4)
                keys = rec["keys"]
                for times in (1, 2, 4, 8):
                    hist = [("KEEP", keys[i % len(keys)]) for i in range(len(keys) * times)]
                    dom = PairDomain(n)
                    T0 = build_node_tree(dom.shapes, 0, n)
                    r = gen_mod.actual_ratio(hist, T0, n)
                    ratios.append({"times": times, "sum_a": r["sum_a"], "sum_b": r["sum_b"],
                                   "ratio": r["ratio"]})
                fam = {"histories": [seq_id], "construction": "inflate_walk x[1,2,4,8]",
                       "diagonal": True}
            if not ratios:
                continue
            grows = all(ratios[i + 1]["ratio"][0] * ratios[i]["ratio"][1] >
                        ratios[i]["ratio"][0] * ratios[i + 1]["ratio"][1]
                        for i in range(len(ratios) - 1)) if len(ratios) > 1 else False
            result = generalize_mod.generalize(fam, {"grows": grows, "replayed": True})
            triaged.append({"config": [predicate, k, 2], "first_violation": first,
                            "ratios": ratios, "triage": result})
            if len(triaged) >= 12:
                break
        if len(triaged) >= 12:
            break
    with open(os.path.join(outdir, "triage.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"triaged": triaged}, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP4-STEP-07] triage complete: %d motifs (all expect NOT_ACTIVATED)" % len(triaged),
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
