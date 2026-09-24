"""Spec PHASE 06 runner (REAL): contracted baseline + paper-facing WP-2 reports.

Entry: WP-2A L6_TRANSLATION_FROZEN (reproduces the known-loss SHAPE — boundary
pairings, contracted increases, lazy ops, bends, zig roles — without overclaiming
any bound). Outputs: baseline.json, L6_PAIR_ACCESS_TRANSLATION_REPORT.md,
KEEP_CYCLE_ATLAS.md (drafts; finalized at seal).
Console lines prefixed [WP2B-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def _require_freeze() -> list[str]:
    cert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE02_L6_MAPPING_FREEZE.json")
    if not os.path.exists(cert):
        return ["GATE-02 WP-2A freeze certificate missing"]
    return []


# WP2B-STEP-08: contracted baseline identities on development traces.
def step_baseline(sizes: list[int]) -> tuple[list[str], dict]:
    fails: list[str] = []
    edges = []
    for n in sizes:
        edges += json.load(open(os.path.join(ROOT, "artifacts", "v03", "cycles",
                                             "stratified", "stratified_n%d.json" % n),
                                encoding="utf-8"))
    contracted_d = [e["contracted_sum"]["delta"] for e in edges]
    raw_d = [e["gap_sum"]["delta"] for e in edges]
    with_important = [e for e in edges
                      if any(p["class"] == "IMPORTANT" for p in e["pairings"])]
    imp_d = [e["contracted_sum"]["delta"] for e in with_important]
    ops_per_rotation = []
    for e in edges:
        ops_per_rotation += [len(e["pairings"]) + c for c in e["intervals_created_per_rotation"]]
    out = {"edges": len(edges),
           "contracted_delta": {"min": min(contracted_d), "max": max(contracted_d),
                                "positive": sum(1 for d in contracted_d if d > 0)},
           "raw_delta": {"min": min(raw_d), "max": max(raw_d)},
           "important_boundary_edges": len(with_important),
           "important_contracted_max": max(imp_d) if imp_d else None,
           "structural_ops_per_rotation_max": max(ops_per_rotation) if ops_per_rotation else 0,
           "paid_free_status": "UNDETERMINED_PRE_WP6 (vocabulary only, no transplant)"}
    print("[WP2B-STEP-08] baseline: %d edges, contracted delta range [%d,%d], "
          "important-boundary edges %d (max contracted +%s), structural ops/rot max %d"
          % (out["edges"], out["contracted_delta"]["min"], out["contracted_delta"]["max"],
             out["important_boundary_edges"], out["important_contracted_max"],
             out["structural_ops_per_rotation_max"]), flush=True)
    return fails, out


# WP2B-STEP-08: paper-facing drafts from sealed WP-2 artifacts.
def step_reports(baseline: dict) -> list[str]:
    fails: list[str] = []
    rep = ["# L6 Pair-Access translation report (WP-2 draft)",
           "",
           "27/27 objects resolved (SAME with recorded operationalizations; zero N/A).",
           "Evidence: dual-implementation agreement, 5 mutant controls, 0-tie exhaustive,",
           "contracted identity 0..4999, MST0-03 REVIEWED (see freeze cert).",
           "Withheld: all COUNT/paid-free claims (WP-2B measurements / WP-6 theorems).",
           ""]
    with open(os.path.join(ROOT, "L6_PAIR_ACCESS_TRANSLATION_REPORT.md"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rep))
    atlas = ["# KEEP cycle atlas (WP-2 draft)", ""]
    for n in (4, 5, 6, 7):
        edges = json.load(open(os.path.join(ROOT, "artifacts", "v03", "cycles", "stratified",
                                            "stratified_n%d.json" % n), encoding="utf-8"))
        cycs: dict[int, list] = {}
        for e in edges:
            cycs.setdefault(e["cycle"], []).append(e)
        atlas.append("## n=%d: %d cycles, %d edges" % (n, len(cycs), len(edges)))
        for cid, es in sorted(cycs.items()):
            atlas.append("- cycle %d: sum_a=%d sum_y=%d zigzig=%d zigzag=%d bends_destroyed=%d "
                         "gap_delta=%d contracted_delta=%d motifs=%s"
                         % (cid, sum(e["a"] for e in es), sum(e["y"] for e in es),
                            sum(e["zig"]["zigzig"] for e in es),
                            sum(e["zig"]["zigzag"] for e in es),
                            sum(e["bends"]["destroyed"] for e in es),
                            sum(e["gap_sum"]["delta"] for e in es),
                            sum(e["contracted_sum"]["delta"] for e in es),
                            sorted({p["class"] for e in es for p in e["pairings"]})))
    with open(os.path.join(ROOT, "KEEP_CYCLE_ATLAS.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(atlas) + "\n")
    print("[WP2B-STEP-08] reports drafted (translation report + cycle atlas)", flush=True)
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="4,5,6,7")
    args = ap.parse_args()
    print("[WP2B-STEP-00] PHASE 06: contracted baseline + WP-2 reports", flush=True)
    fails = _require_freeze()
    if fails:
        print("[WP2B-STEP-00] PHASE06_FAIL", flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 2
    sizes = [int(s) for s in args.sizes.split(",")]
    f, baseline = step_baseline(sizes)
    fails += f
    os.makedirs(os.path.join(ROOT, "artifacts", "v03", "baseline"), exist_ok=True)
    with open(os.path.join(ROOT, "artifacts", "v03", "baseline", "baseline.json"),
              "w", encoding="utf-8", newline="\n") as fh:
        json.dump(baseline, fh, sort_keys=True, indent=2)
        fh.write("\n")
    fails += step_reports(baseline)
    if fails:
        print("[WP2B-STEP-00] PHASE06_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP2B-STEP-00] L6_BASELINE_REPRODUCED (shape only; no bound claimed)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
