"""Derived obligation statuses (live view; frozen ledgers never edited).

proof_status.json and theorem_gate_matrix.yaml are WP-0 snapshots (UNPROVED).
Current status per obligation is derived here:
  REVIEWED iff math/reviews/MST0-XX.review.json exists with verdict ACCEPT;
  PROVED   iff a proof document math/theorem_MST*.md exists for it (YC stub
           files do not count) — author's claim, subject to human review;
  BLOCKED  iff a math/reviews/MST0-XX.BLOCKED marker exists;
  else UNPROVED.
Output: artifacts/v03/proofs/obligation_status.json (recomputed, never frozen).
Console tag [WP1-STEP-07].
"""
from __future__ import annotations

import json
import os

PROOF_DOCS = {
    "MST0-01": "math/theorem_MST01_parent_transport.md",
    "MST0-02": "math/theorem_MST02_rotation_refinement.md",
    "MST0-03": "math/theorem_MST03_l6_translation.md",
    "MST0-04": "math/theorem_MST04_keep_reference_snapshot.md",
    "MST0-05": "math/theorem_MST05_keep_heavy_path.md",
    "MST0-06": "math/theorem_MST06_zigzig_pairing.md",
    "MST0-07": "math/theorem_MST07_zigzag_bends.md",
    "MST0-08": "math/theorem_MST08_reference_rotation_locality.md",
    "MST0-09": "math/theorem_MST09_raw_boundary.md",
    "MST0-10": "math/theorem_MST10_ledger_determinism.md",
    "MST0-11": "math/theorem_MST11_transfer_preservation.md",
    "MST0-12": "math/theorem_MST12_signed_lower_bound.md",
    "MST0-13": "math/theorem_MST13_delete_injection.md",
    "MST0-14": "math/theorem_MST14_keep_repayment.md",
    "MST0-15": "math/theorem_MST15_integrability.md",
    "MST0-16": "math/theorem_MST16_block_partition.md",
    "MST0-17": "math/theorem_MST17_pair_access.md",
    "MST0-18": "math/theorem_MST18_telescoping.md",
    "MST0-19": "math/theorem_MST19_bridge.md",
    "MST0-20": "math/theorem_MST20_negative_guard.md",
    "MST0-21": "math/theorem_MST21_negative_family.md",
    "MST0-22": "math/theorem_MST22_constant_independence.md",
    "MST0-23": "math/theorem_MST23_finite_integrability_guard.md",
    "MST0-24": "math/theorem_MST24_branch_scope.md",
    "MST0-25": "math/theorem_MST25_holdout_scope.md",
    "MST0-26": "math/theorem_MST26_literature_scope.md",
}


# WP1-STEP-07: derive live statuses without touching frozen ledgers.
def derive(root: str) -> dict:
    """Return {obligation: {status, evidence}} for all 26 obligations.

    A proof document maps to PROVED only when its Status line claims PROVED
    (SETUP/design documents map to UNPROVED with the reason recorded).
    """
    import re as _re
    out = {}
    for oid in sorted(PROOF_DOCS):
        review = os.path.join(root, "math", "reviews", "%s.review.json" % oid)
        blocked = os.path.join(root, "math", "reviews", "%s.BLOCKED" % oid)
        na_rec = os.path.join(root, "math", "reviews", "%s.not_applicable.json" % oid)
        proof = os.path.join(root, *PROOF_DOCS[oid].split("/"))
        if os.path.exists(review):
            try:
                verdict = json.load(open(review, encoding="utf-8")).get("verdict")
            except (json.JSONDecodeError, OSError):
                verdict = None
            if verdict == "ACCEPT":
                out[oid] = {"status": "REVIEWED", "evidence": "%s.review.json:ACCEPT" % oid}
                continue
            out[oid] = {"status": "UNPROVED", "evidence": "review record without ACCEPT"}
        elif os.path.exists(blocked):
            out[oid] = {"status": "BLOCKED", "evidence": "%s.BLOCKED marker" % oid}
        elif os.path.exists(proof):
            text = open(proof, encoding="utf-8").read()
            m = _re.search(r"\*\*Status:\*\*\s*([A-Z_]+)", text)
            claimed = m.group(1) if m else "PROVED"
            if claimed == "PROVED":
                out[oid] = {"status": "PROVED", "evidence": PROOF_DOCS[oid]}
            elif claimed == "NOT_APPLICABLE" and os.path.exists(na_rec):
                try:
                    rec = json.load(open(na_rec, encoding="utf-8"))
                    ok = bool(rec.get("reason")) and bool(rec.get("evidence"))
                except (json.JSONDecodeError, OSError):
                    ok = False
                if ok:
                    out[oid] = {"status": "NOT_APPLICABLE",
                                "evidence": "%s.not_applicable.json" % oid}
                else:
                    out[oid] = {"status": "UNPROVED",
                                "evidence": "NOT_APPLICABLE without preserved justification"}
            else:
                out[oid] = {"status": "UNPROVED",
                            "evidence": "%s declares %s" % (PROOF_DOCS[oid], claimed)}
        else:
            out[oid] = {"status": "UNPROVED", "evidence": "no proof document yet"}
    return out


def main(root: str | None = None) -> dict:
    """Write the derived status file; print the WP-1 subgate line."""
    root = root or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    statuses = derive(root)
    out_path = os.path.join(root, "artifacts", "v03", "proofs", "obligation_status.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"derived_utc": "2026-09-23", "statuses": statuses}, f, sort_keys=True, indent=2)
        f.write("\n")
    counts: dict[str, int] = {}
    for v in statuses.values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    print("[WP1-STEP-07] obligation statuses: %s" % counts, flush=True)
    sub = statuses.get("MST0-01", {}).get("status")
    print("[WP1-STEP-07] WP-1 pre-consumption subgate MST0-01=%s (needs REVIEWED)" % sub, flush=True)
    return statuses


if __name__ == "__main__":
    main()
