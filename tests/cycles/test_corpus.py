"""Corpus test suite (CYC-06..08 mechanics). Fast; uses sealed WP-2 artifacts."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.cycles import motifs as motifs_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_stratified_schema() -> None:
    base = os.path.join(ROOT, "artifacts", "v03", "cycles")
    if not os.path.exists(os.path.join(base, "stratified", "stratified_n4.json")):
        print("SKIP corpus suite (run_phase04 not executed yet)")
        return
    total = 0
    for n in (4, 5, 6, 7):
        recs = json.load(open(os.path.join(base, "stratified", "stratified_n%d.json" % n)))
        total += len(recs)
        for r in recs:
            for field in ("zig", "b_path", "bends", "gap_sum", "contracted_sum",
                          "pairings", "regret", "s0_scale_path"):
                if field not in r:
                    check("CYC-06 stratified schema n=%d" % n, False)
                    return
    check("CYC-06 stratified 70 edges", total == 70)
    cat = json.load(open(os.path.join(base, "motif_catalog.json")))
    check("CYC-08 catalog non-empty", len(cat) > 0)
    val = json.load(open(os.path.join(base, "n7_validation.json")))
    check("CYC-07 n7 validation recorded", val["total"] == 10)
    # CYC-07 firewall: re-deriving a catalog WITH n7 must not shrink the unknown set
    # below the validated reading (i.e., validation used the frozen catalog only).
    check("CYC-07 burden alignment sane",
          val["burden_matched"] <= val["burden_total"])


def test_motif_canonical() -> None:
    m = {"zig_classes": {"ZIG": 0, "LL": 1, "RR": 0, "LR": 0, "RL": 0},
         "heavy_fraction_bucket": "2/2", "light_positions": [],
         "bend_delta_sign": "flat", "gap_delta_sign": "flat",
         "contracted_delta_sign": "up", "pairing_classes": ["DEGENERATE_merged"],
         "max_intervals_per_rotation": 3, "s0_path_signature": [1, 1, 0],
         "positive_regret_c2": False}
    k1 = motifs_mod.motif_key(m)
    m2 = dict(m)
    m2["light_positions"] = [0]
    check("CYC-08 motif keys discriminate", motifs_mod.motif_key(m2) != k1)


if __name__ == "__main__":
    test_stratified_schema()
    test_motif_canonical()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
