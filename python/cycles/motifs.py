"""Canonical cross-n motif records (WP-2B step 2; n4-6 selection only).

A motif is a canonical predicate over relative order, orientations, scale
transitions, and heavy/lazy roles — never literal node labels or cycle IDs.
Motifs are FORMED on n=4..6 selection; n=7 only validates (validate_n7.py).
Console tag [WP2B-STEP-02].
"""
from __future__ import annotations


def motif_of(edge_rec: dict) -> dict:
    """Canonical motif signature for one stratified edge."""
    z = edge_rec["zig"]
    bp = edge_rec["b_path"]
    path_len = bp["length"]
    motif = {
        "zig_classes": {k: z[k] for k in ("ZIG", "LL", "RR", "LR", "RL")},
        "heavy_fraction_bucket": ("%d/%d" % (bp["heavy"], max(1, path_len - 1))
                                  if path_len > 1 else "singleton"),
        "light_positions": bp["light_positions"],
        "bend_delta_sign": ("up" if edge_rec["bends"]["created"] > edge_rec["bends"]["destroyed"]
                            else "down" if edge_rec["bends"]["destroyed"] > edge_rec["bends"]["created"]
                            else "flat"),
        "gap_delta_sign": ("up" if edge_rec["gap_sum"]["delta"] > 0
                           else "down" if edge_rec["gap_sum"]["delta"] < 0 else "flat"),
        "contracted_delta_sign": ("up" if edge_rec["contracted_sum"]["delta"] > 0
                                  else "down" if edge_rec["contracted_sum"]["delta"] < 0 else "flat"),
        "pairing_classes": sorted({p["class"] for p in edge_rec["pairings"]}),
        "max_intervals_per_rotation": edge_rec["max_intervals_per_rotation"],
        "s0_path_signature": edge_rec["s0_scale_path"],
        "positive_regret_c2": edge_rec["regret"][2] > 0,
    }
    return motif


def motif_key(motif: dict) -> str:
    """Deterministic canonical key (sorted serialization)."""
    import json
    return json.dumps(motif, sort_keys=True)


# WP2B-STEP-02: form the motif catalog on selection sizes only.
def form_catalog(stratified: dict[int, list]) -> dict:
    """Map motif key -> {motif, occurrences: [(n, cycle, edge)], burden_edges}."""
    catalog: dict = {}
    for n, edges in stratified.items():
        for rec in edges:
            m = motif_of(rec)
            k = motif_key(m)
            entry = catalog.setdefault(k, {"motif": m, "occurrences": [], "burden": 0})
            entry["occurrences"].append([n, rec["cycle"], rec["edge"]])
            if rec["regret"][2] > 0:
                entry["burden"] += 1
    print("[WP2B-STEP-02] catalog: %d motifs over %d edges"
          % (len(catalog), sum(len(v) for v in stratified.values())), flush=True)
    return catalog
