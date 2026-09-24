"""Spec PHASE 02 runner (REAL): WP-2A translation-only subphase.

Entry: ROTATION_TRACE_CERTIFIED + MST0-02/MST0-04 REVIEWED (both hold).
WP-2A steps: extract source sites, agreement on corpus snapshots, mutant controls,
MST0-03 proof presence, mapping-doc hash. The freeze certificate is written ONLY by
--finalize after the MST0-03 human ACCEPT (WP-2B stays blocked until then).
Target-blind: this runner never reads regret/criticality/Bellman/holdout fields.
Console lines prefixed [WP2A-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles.enumerate import PairDomain, build_node_tree  # noqa: E402
from python.l6_translation import mapping_check as mc  # noqa: E402


def sha_file(p: str) -> str:
    """SHA-256 over buffered reads."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP2A-STEP-02: agreement on corpus snapshots (reference=A1, subject=B pre-splay).
def step_agreement(sizes: list[int], per_n: int) -> list[str]:
    fails: list[str] = []
    pairs = []
    for n in sizes:
        dom = PairDomain(n)
        base = os.path.join(ROOT, "artifacts", "v03", "parent_import",
                            "v01baseline", "v01", "critical_n%d_canonical_cycles.json" % n)
        cycles = json.load(open(base, encoding="utf-8"))
        for cyc in cycles[:max(1, per_n // max(1, len(cycles)))]:
            for e in cyc["edges"][:2]:
                a_id, b_id = dom.unpid(e["source"])
                A = build_node_tree(dom.shapes, a_id, n)
                B = build_node_tree(dom.shapes, b_id, n)
                pairs.append((A, B))
                if len(pairs) >= per_n:
                    break
            if len(pairs) >= per_n:
                break
    print("[WP2A-STEP-02] corpus snapshot pairs built: %d (reference=A1, subject=B)" % len(pairs), flush=True)
    fails += mc.check_agreement(pairs)
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--finalize", action="store_true")
    ap.add_argument("--per-n", type=int, default=24)
    args = ap.parse_args()
    print("[WP2A-STEP-00] PHASE 02 (WP-2A translation-only; no target data)", flush=True)
    fails: list[str] = []
    # WP2A-STEP-01: source-site extraction record must exist from frozen bytes.
    sites = os.path.join(ROOT, "artifacts", "v03", "translation", "l6_source_sites.json")
    if not os.path.exists(sites):
        fails.append("L6-02 extraction record missing (run extract.py)")
    else:
        print("[WP2A-STEP-01] source sites recorded (frozen L6 bytes)", flush=True)
    # WP2A-STEP-02/03: agreement + mutants.
    fails += step_agreement([4, 5, 6, 7], args.per_n)
    fails += mc.run_mutants()
    # WP2A-STEP-04: MST0-03 proof + package presence (verdict tracked separately).
    for f in ("math/theorem_MST03_l6_translation.md",
              "math/reviews/MST0-03.REVIEW-PACKAGE.md",
              "math/L6_PAIR_ACCESS_MAPPING.md"):
        if not os.path.exists(os.path.join(ROOT, f)):
            fails.append("L6-02 missing %s" % f)
    if not fails:
        print("[WP2A-STEP-04] MST0-03 proof + package present; mapping doc populated", flush=True)
    mapping_hash = sha_file(os.path.join(ROOT, "math", "L6_PAIR_ACCESS_MAPPING.md"))
    print("[WP2A-STEP-05] mapping doc sha=%s..." % mapping_hash[:16], flush=True)
    if args.finalize:
        rev = os.path.join(ROOT, "math", "reviews", "MST0-03.review.json")
        if not os.path.exists(rev):
            fails.append("FINALIZE-01 MST0-03.review.json missing (human verdict first)")
        else:
            v = json.load(open(rev, encoding="utf-8"))
            if v.get("verdict") != "ACCEPT":
                fails.append("FINALIZE-01 verdict is not ACCEPT")
            else:
                cert = {"mapping_sha256": mapping_hash,
                        "prereg_yaml": "l6_translation_v0.3.yaml",
                        "review": "math/reviews/MST0-03.review.json",
                        "status": "L6_TRANSLATION_FROZEN"}
                out = os.path.join(ROOT, "artifacts", "v03", "freeze",
                                   "PHASE02_L6_MAPPING_FREEZE.json")
                with open(out, "w", encoding="utf-8", newline="\n") as f:
                    json.dump(cert, f, sort_keys=True, indent=2)
                    f.write("\n")
                print("[WP2A-STEP-05] L6_TRANSLATION_FROZEN certified", flush=True)
    if fails:
        print("[WP2A-STEP-00] PHASE02_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP2A-STEP-00] PHASE02_PASS (proof present; freeze cert iff --finalize with ACCEPT)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
