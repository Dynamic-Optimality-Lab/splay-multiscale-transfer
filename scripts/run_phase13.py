"""Spec PHASE 13 runner (REAL): adversarial battery + shortlist zero-violation gate.

Entry: solver shortlist (dev). Nine required search modes produce seeded families
(sizes <= 32, bounded lengths); every family history becomes rotation-level events
via the shared corpus builder; every shortlist candidate is evaluated EXACTLY at
its frozen C (full pass — zero residuals required to advance to WP-5 freezing);
actual Splay ratios tracked alongside (reported, never substituted). Heuristics
propose; exact evaluator disposes. Console lines prefixed [WP4-STEP-06/08].
"""
from __future__ import annotations

import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.adversary import anneal as anneal_mod  # noqa: E402
from python.adversary import generators as gen_mod  # noqa: E402
from python.adversary import genetic as genetic_mod  # noqa: E402
from python.adversary import hillclimb as hillclimb_mod  # noqa: E402
from python.adversary import neighborhood as neighborhood_mod  # noqa: E402
from python.adversary import splice as splice_mod  # noqa: E402
from python.cycles import discovery as disc_mod  # noqa: E402
from python.cycles.enumerate import node_shape_string  # noqa: E402
from python.solver import certify as certify_mod  # noqa: E402
from python.transfer import branchA as branchA_mod  # noqa: E402

MODES = ["uniform", "structured", "hillclimb", "annealing", "genetic",
         "neighborhood", "splicing", "inflation", "generalization"]
N = 16
LENGTH = 48
PER_MODE = 6
SEED0 = 424242


def _rec(n: int, kind: str, history: list, seed: int) -> dict:
    """Format an engine history as a corpus gen-record (init shape + history)."""
    rng = random.Random(seed)
    T0 = gen_mod.initial_tree(rng, n, kind)
    return {"n": n, "seed": seed, "init_shape": node_shape_string(T0), "history": history}


# WP4-STEP-06: build one family per required mode (seeded, deterministic).
def build_families() -> dict:
    """Nine-mode battery families (histories only; events built later)."""
    fams: dict[str, list] = {}
    rng = random.Random(SEED0)
    kinds = ["RANDOM_LEGAL", "SPINE_VS_BALANCED", "OPPOSITE_SPINE",
             "ALTERNATING_KEEP_DELETE", "DELETE_BURST_THEN_KEEP", "MIRROR_PAIRED"]
    fams["uniform"] = [gen_mod.build_history(random.Random(SEED0 + i), N, "RANDOM_LEGAL", LENGTH)
                       for i in range(PER_MODE)]
    fams["structured"] = [gen_mod.build_history(random.Random(SEED0 + 100 + i), N,
                                                kinds[i % len(kinds)], LENGTH)
                          for i in range(PER_MODE)]
    base = gen_mod.build_history(random.Random(SEED0 + 200), N, "RANDOM_LEGAL", LENGTH)
    fams["neighborhood"] = neighborhood_mod.neighborhood(base, N, PER_MODE, SEED0 + 201)
    crit = json.load(open(os.path.join(ROOT, "artifacts", "v03", "parent_import",
                                       "v01baseline", "v01",
                                       "critical_n4_canonical_cycles.json"),
                          encoding="utf-8"))
    fams["splicing"] = [splice_mod.splice(crit[:2], [1, N], N) for _ in range(2)]
    from python.adversary import inflate as inflate_mod
    fams["inflation"] = [inflate_mod.inflate_cycle(crit[0], t) for t in (2, 4)]
    fams["inflation"] += [inflate_mod.inflate_burst(base, 3)]
    fams["generalization"] = [inflate_mod.inflate_cycle(crit[1], t) for t in (3, 5)]
    return fams


def main() -> int:
    print("[WP4-STEP-00] PHASE 13: adversarial battery + zero-violation gate", flush=True)
    short_path = os.path.join(ROOT, "artifacts", "v03", "solver", "shortlist.json")
    if not os.path.exists(short_path):
        print("[WP4-STEP-00] PHASE13_FAIL: shortlist missing", flush=True)
        return 2
    shortlist = json.load(open(short_path, encoding="utf-8"))["selected"]
    if not shortlist:
        print("[WP4-STEP-00] PHASE13_FAIL: empty shortlist", flush=True)
        return 1
    print("[WP4-STEP-00] shortlist: %s" % [(c["predicate"], c["k"], c["C"]) for c in shortlist],
          flush=True)
    fams = build_families()
    # Search engines maximize shortlist residual (exact objective, seeded).
    imp = os.path.join(ROOT, "artifacts", "v03", "parent_import")

    def residual_of(history):
        rec = _rec(N, "RANDOM_LEGAL", history, 999)
        corpus = disc_mod.build_dev_corpus(imp, [], [rec])
        worst = 0
        for cfg in shortlist:
            v = branchA_mod.evaluate(cfg["predicate"], cfg["k"], cfg["C"], corpus,
                                     fail_fast=True)
            if v["max_residual"][0] > worst:
                worst = v["max_residual"][0]
        return worst

    hc = hillclimb_mod.hillclimb(N, "RANDOM_LEGAL", LENGTH, 40, SEED0 + 300, residual_of)
    an = anneal_mod.anneal(N, "RANDOM_LEGAL", LENGTH, 40, SEED0 + 400, residual_of)
    ge = genetic_mod.genetic(N, "RANDOM_LEGAL", LENGTH, 8, 8, SEED0 + 500, residual_of)
    fams["hillclimb"] = [hc["best"]]
    fams["annealing"] = [an["best"]]
    fams["genetic"] = [ge["best"]]
    print("[WP4-STEP-06] engines best residuals: hill=%s anneal=%s genetic=%s"
          % (hc["best_score"], an["best_score"], ge["best_score"]), flush=True)
    # Exact battery: every family x every shortlist config (full pass, zero required).
    outdir = os.path.join(ROOT, "artifacts", "v03", "adversarial")
    os.makedirs(outdir, exist_ok=True)
    kills = []
    rows = []
    for mode in MODES:
        for hi, history in enumerate(fams[mode]):
            seed = SEED0 + 1000 + hi
            T0 = gen_mod.initial_tree(random.Random(seed), N, mode)
            rec = {"n": N, "seed": seed, "init_shape": node_shape_string(T0),
                   "history": history}
            corpus = disc_mod.build_dev_corpus(imp, [], [rec])
            ratio = gen_mod.actual_ratio(history, T0, N)
            for cfg in shortlist:
                v = branchA_mod.evaluate(cfg["predicate"], cfg["k"], cfg["C"], corpus)
                r = certify_mod.replay_candidate(cfg["predicate"], cfg["k"], cfg["C"], corpus)
                if v["feasible"] != r["feasible"]:
                    kills.append({"kind": "CERT-01", "mode": mode, "hist": hi,
                                  "cfg": [cfg["predicate"], cfg["k"], cfg["C"]]})
                if not v["feasible"]:
                    kills.append({"kind": "RESIDUAL", "mode": mode, "hist": hi,
                                  "cfg": [cfg["predicate"], cfg["k"], cfg["C"]],
                                  "max_res": v["max_residual"],
                                  "first": v["first_violation"]})
                rows.append({"mode": mode, "hist": hi,
                             "cfg": [cfg["predicate"], cfg["k"], cfg["C"]],
                             "feasible": v["feasible"], "agree": v["feasible"] == r["feasible"],
                             "ratio": ratio["ratio"]})
    with open(os.path.join(outdir, "battery.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"rows": rows, "kills": kills}, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP4-STEP-08] battery: %d evaluations, %d kills" % (len(rows), len(kills)), flush=True)
    for k in kills[:8]:
        print("[WP4-STEP-08] kill: %s" % (k,), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
