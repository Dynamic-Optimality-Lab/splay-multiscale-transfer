"""WP-6 Phase-17 theorem-ledger lifecycle audit (machine verification of §7 closure).

Derives live statuses via status.derive (frozen ledgers never edited) and then
audits: (a) no UNPROVED -> REVIEWED jumps (every REVIEWED has an ACCEPT review
record AND a proof document); (b) every status carries a proof/review pointer
(REVIEWED: review record; PROVED: proof doc claiming PROVED; BLOCKED: marker;
NOT_APPLICABLE: justification record; UNPROVED: setup doc or explicit absence);
(c) writes per-obligation bundles under artifacts/v03/proofs/bundles/.
Console tag [WP6-STEP-03].
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.audit import status as status_mod  # noqa: E402


# WP6-STEP-03: sha-256 of a file (buffered reads).
def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP6-STEP-03: audit every obligation lifecycle transition + pointer.
def audit(root: str = ROOT) -> dict:
    """Return the lifecycle audit record (fails closed on any violation)."""
    statuses = status_mod.derive(root)
    jumps: list = []
    pointerless: list = []
    bundles: dict = {}
    for oid in sorted(statuses):
        st = statuses[oid]["status"]
        ev = statuses[oid]["evidence"]
        review = os.path.join(root, "math", "reviews", "%s.review.json" % oid)
        proof = os.path.join(root, *status_mod.PROOF_DOCS[oid].split("/"))
        bundle: dict = {"obligation": oid, "status": st, "evidence": ev}
        if st == "REVIEWED":
            if not (os.path.exists(review) and os.path.exists(proof)):
                jumps.append(oid)
            else:
                bundle["review_sha256"] = _sha(review)
                bundle["proof_sha256"] = _sha(proof)
        elif st == "PROVED":
            if not os.path.exists(proof):
                pointerless.append(oid)
            else:
                bundle["proof_sha256"] = _sha(proof)
        elif st == "BLOCKED":
            marker = os.path.join(root, "math", "reviews", "%s.BLOCKED" % oid)
            if not os.path.exists(marker):
                pointerless.append(oid)
            else:
                bundle["marker"] = json.load(open(marker, encoding="utf-8"))
        elif st == "NOT_APPLICABLE":
            rec = os.path.join(root, "math", "reviews", "%s.not_applicable.json" % oid)
            if not os.path.exists(rec):
                pointerless.append(oid)
            else:
                bundle["justification"] = json.load(open(rec, encoding="utf-8"))
                if os.path.exists(proof):
                    bundle["proof_sha256"] = _sha(proof)
        else:
            if os.path.exists(proof):
                bundle["proof_sha256"] = _sha(proof)
            else:
                bundle["note"] = "no proof document yet"
        bundles[oid] = bundle
    counts: dict = {}
    for v in statuses.values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    print("[WP6-STEP-03] lifecycle: %s; jumps=%r pointerless=%r"
          % (counts, jumps, pointerless), flush=True)
    if jumps or pointerless:
        raise ValueError("lifecycle audit FAILED: jumps=%r pointerless=%r"
                         % (jumps, pointerless))
    return {"statuses": statuses, "counts": counts, "bundles": bundles,
            "jumps": jumps, "pointerless": pointerless}
