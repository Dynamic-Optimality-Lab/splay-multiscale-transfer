"""Spec PHASE 04 runner (REAL): WP-2B critical-corpus science (targets joined).

Entry: WP-2A L6_TRANSLATION_FROZEN + MST0-03 REVIEWED (both hold).
Steps: WP2B-STEP-01 stratify all critical edges, WP2B-STEP-02 motif catalog (n4-6)
+ n7 validation, WP2B-STEP-03 D5 analysis. Outputs feed run_phase05/06.
Console lines prefixed [WP2B-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles import motifs as motifs_mod  # noqa: E402
from python.cycles import stratify as strat_mod  # noqa: E402
from python.cycles import validate_n7 as vn7_mod  # noqa: E402
from python.cycles.enumerate import PairDomain  # noqa: E402
from python.provenance import d5_analysis as d5_mod  # noqa: E402


def _require_freeze() -> list[str]:
    cert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE02_L6_MAPPING_FREEZE.json")
    if not os.path.exists(cert):
        return ["GATE-02 WP-2A freeze certificate missing (run_phase02 --finalize after ACCEPT)"]
    c = json.load(open(cert, encoding="utf-8"))
    if c.get("status") != "L6_TRANSLATION_FROZEN":
        return ["GATE-02 freeze certificate status is not L6_TRANSLATION_FROZEN"]
    rev = os.path.join(ROOT, "math", "reviews", "MST0-03.review.json")
    if not os.path.exists(rev) or json.load(open(rev, encoding="utf-8")).get("verdict") != "ACCEPT":
        return ["GATE-02 MST0-03.review.json ACCEPT missing"]
    print("[WP2B-STEP-00] WP-2B entry: L6_TRANSLATION_FROZEN + MST0-03 REVIEWED hold", flush=True)
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="4,5,6,7")
    args = ap.parse_args()
    print("[WP2B-STEP-00] PHASE 04: critical-corpus science (targets joined post-freeze)", flush=True)
    fails = _require_freeze()
    if fails:
        print("[WP2B-STEP-00] PHASE04_FAIL", flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 2
    imp = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    sizes = [int(s) for s in args.sizes.split(",")]
    outdir = os.path.join(ROOT, "artifacts", "v03", "cycles")
    os.makedirs(os.path.join(outdir, "stratified"), exist_ok=True)
    stratified: dict[int, list] = {}
    for n in sizes:
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        recs = []
        for cid, cyc in enumerate(cycles):
            for i, e in enumerate(cyc["edges"]):
                r = strat_mod.analyze_edge(dom, n, e["source"], e["key"])
                r["cycle"] = cid
                r["edge"] = i
                recs.append(r)
        stratified[n] = recs
        with open(os.path.join(outdir, "stratified", "stratified_n%d.json" % n),
                  "w", encoding="utf-8", newline="\n") as f:
            json.dump(recs, f, sort_keys=True, indent=1)
            f.write("\n")
        print("[WP2B-STEP-01] n=%d stratified %d edges" % (n, len(recs)), flush=True)
    # WP2B-STEP-02: motifs on n4-6, frozen catalog, n7 validation.
    catalog = motifs_mod.form_catalog({n: stratified[n] for n in sizes if n in (4, 5, 6)})
    with open(os.path.join(outdir, "motif_catalog.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(catalog, f, sort_keys=True, indent=1)
        f.write("\n")
    n7recs = [r for n in sizes if n == 7 for r in stratified.get(n, [])]
    validation = vn7_mod.validate(n7recs, catalog)
    with open(os.path.join(outdir, "n7_validation.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(validation, f, sort_keys=True, indent=2)
        f.write("\n")
    # WP2B-STEP-03: D5 analysis.
    counters, f3 = d5_mod.verify_counters(os.path.join(imp, "v02baseline"))
    fails += f3
    alle = [r for v in stratified.values() for r in v]
    separation = d5_mod.separate(alle)
    with open(os.path.join(outdir, "d5_analysis.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"counters": counters, "separation": separation}, f, sort_keys=True, indent=2)
        f.write("\n")
    if fails:
        print("[WP2B-STEP-00] PHASE04_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP2B-STEP-00] PHASE04_PASS: stratified %d edges, %d motifs, n7 checked, D5 tabled"
          % (len(alle), len(catalog)), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
