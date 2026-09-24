"""n=7 internal validation against frozen n4-6 motif predicates (WP-2B step 2).

Firewall: predicates arrive as a frozen catalog (hashes); this module never forms
new predicates on n=7 data. Reports match rate + burden alignment. Console tag
[WP2B-STEP-02].
"""
from __future__ import annotations

from python.cycles import motifs as motifs_mod


# WP2B-STEP-02: validate n7 edges against the frozen catalog (no new formation).
def validate(n7_edges: list, catalog: dict) -> dict:
    """Return {matched, total, unmatched_idx, burden_matched, burden_total}."""
    matched = 0
    unmatched = []
    burden_matched = 0
    burden_total = 0
    for i, rec in enumerate(n7_edges):
        k = motifs_mod.motif_key(motifs_mod.motif_of(rec))
        if k in catalog:
            matched += 1
            if rec["regret"][2] > 0:
                burden_matched += 1
        else:
            unmatched.append(i)
        if rec["regret"][2] > 0:
            burden_total += 1
    out = {"matched": matched, "total": len(n7_edges), "unmatched_idx": unmatched,
           "burden_matched": burden_matched, "burden_total": burden_total}
    print("[WP2B-STEP-02] n7 validation: %d/%d motifs known, burden %d/%d aligned"
          % (matched, len(n7_edges), burden_matched, burden_total), flush=True)
    return out
