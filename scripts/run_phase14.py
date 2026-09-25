"""Spec PHASE 14 runner (REAL): freeze theorem candidates + constant (WP-5 entry).

Entry: WP-4 dev shortlist (3 survivors, zero residuals at frozen C) +
TRANSFER_GRAMMAR_FROZEN cert + H3T BANK_COMMITTED/unlocks=0 + prereg STOP-05
clear + no prior reveal (one-unlock semantics). Steps: WP5-STEP-00 entry gates;
WP5-STEP-01 eligibility audit + frozen MSTC construction; WP5-STEP-02
candidate-set commitment + firewall transition to TRANSFER_CALCULUS_FROZEN.
No bank contents are read. Console lines prefixed [WP5-STEP-0x] are the audit
record.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.freeze import candidates as freeze_mod  # noqa: E402
from python.holdout import firewall as firewall_mod  # noqa: E402

# WP5-STEP-00: dev shortlist order maps onto frozen IDs (complexity order kept).
FROZEN_MAP = [
    ("MSTC-0001", "MSTC-DEV-0001"),
    ("MSTC-0002", "MSTC-DEV-0002"),
    ("MSTC-0003", "MSTC-DEV-0003"),
]


# WP5-STEP-00: entry-gate audit (fail-closed, exit non-zero on any failure).
def step_entry() -> tuple[list, dict]:
    fails: list = []
    ctx: dict = {}
    short_path = os.path.join(ROOT, "artifacts", "v03", "solver", "shortlist.json")
    if not os.path.exists(short_path):
        fails.append("GATE-14 shortlist missing")
        return fails, ctx
    short = json.load(open(short_path, encoding="utf-8"))
    sel = short.get("selected", [])
    if len(sel) != 3 or short.get("status") != "DEV_SHORTLIST_NOT_FROZEN":
        fails.append("GATE-14 shortlist not the 3-member dev shortlist")
    want = [("P_all", 2, 2), ("P_all", 6, 2), ("P_keep", 1, 6)]
    got = [(s.get("predicate"), s.get("k"), s.get("C")) for s in sel]
    if got != want:
        fails.append("GATE-14 shortlist triples differ from WP-4 record: %r" % (got,))
    ctx["shortlist"] = sel
    for name in ("PHASE09_TRANSFER_GRAMMAR_FREEZE", "PHASE09_EVENT_ONTOLOGY_FREEZE",
                 "PHASE02_L6_MAPPING_FREEZE"):
        if not os.path.exists(os.path.join(ROOT, "artifacts", "v03", "freeze", name + ".json")):
            fails.append("GATE-14 freeze cert missing: %s" % name)
    h3t = os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_state.json")
    st = firewall_mod.load_state(h3t)
    if st.get("state") != "BANK_COMMITTED" or st.get("unlock_count") != 0:
        fails.append("GATE-14 H3T not BANK_COMMITTED/0 (state=%r)" % st.get("state"))
    ctx["h3t_state"] = st
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    for fn in ("h1_reveal.json", "h2r_reveal.json", "h3t_reveal.json",
               "candidate_set_commit.json"):
        if os.path.exists(os.path.join(holdouts, fn)):
            fails.append("GATE-14 reveal/commit already exists pre-freeze: %s" % fn)
    for fn in ("MSTC-0001.json", "MSTC-0002.json", "MSTC-0003.json"):
        if os.path.exists(os.path.join(ROOT, "artifacts", "v03", "hypotheses", fn)):
            fails.append("GATE-14 frozen candidate already exists: %s" % fn)
    print("[WP5-STEP-00] PHASE 14 entry gates: %s"
          % ("PASS" if not fails else "FAIL %r" % (fails,)), flush=True)
    return fails, ctx


# WP5-STEP-01: eligibility audit + frozen construction from dev triples.
def step_freeze(shortlist: list) -> list:
    docs = []
    dev_by_triple = {(s["predicate"], s["k"], s["C"]): s for s in shortlist}
    for frozen_id, dev_id in FROZEN_MAP:
        dev_path = os.path.join(ROOT, "artifacts", "v03", "hypotheses", dev_id + ".json")
        dev = json.load(open(dev_path, encoding="utf-8"))
        key = (dev["predicate"], dev["k"], dev["C"])
        if key not in dev_by_triple:
            raise ValueError("dev %s triple %r not in WP-4 shortlist" % (dev_id, key))
        if dev.get("fresh_holdout_status") != "UNTOUCHED":
            raise ValueError("dev %s already touched; cannot promote" % dev_id)
        doc = freeze_mod.build_frozen(frozen_id, dev_id, dev["predicate"],
                                      dev["k"], dev["C"])
        freeze_mod.validate_eligibility(doc)
        out = os.path.join(ROOT, "artifacts", "v03", "hypotheses", frozen_id + ".json")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, sort_keys=True, indent=2)
            f.write("\n")
        print("[WP5-STEP-01] froze %s from %s (%s,k=%d,C=%d)" % (
            frozen_id, dev_id, dev["predicate"], dev["k"], dev["C"]), flush=True)
        docs.append(doc)
    return docs


# WP5-STEP-02: commitment + firewall transition (H3T) + metadata (H1/H2R).
def step_commit(docs: list) -> dict:
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    commit = freeze_mod.commit_set(docs)
    with open(os.path.join(holdouts, "candidate_set_commit.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(commit, f, sort_keys=True, indent=2)
        f.write("\n")
    h3t_path = os.path.join(holdouts, "h3t_state.json")
    st = firewall_mod.load_state(h3t_path)
    if st.get("state") != "BANK_COMMITTED":
        raise ValueError("H3T firewall moved under Phase 14 (read-before-freeze)")
    st["state"] = "TRANSFER_CALCULUS_FROZEN"
    st["candidate_set_hash"] = commit["set_hash"]
    st["candidate_ids"] = [m["calculus_id"] for m in commit["candidates"]]
    with open(h3t_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(st, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP5-STEP-02] H3T firewall BANK_COMMITTED -> TRANSFER_CALCULUS_FROZEN "
          "(set_hash=%s...)" % commit["set_hash"][:16], flush=True)
    for bank, fname in (("HOLDOUT-H1-v0.1", "h1_firewall_wp5.json"),
                        ("HOLDOUT-H2R-v0.1", "h2r_firewall_wp5.json")):
        meta = {"bank_id": bank, "candidate_set_hash": commit["set_hash"],
                "candidate_ids": [m["calculus_id"] for m in commit["candidates"]],
                "contents_revealed": False}
        with open(os.path.join(holdouts, fname), "w", encoding="utf-8", newline="\n") as f:
            json.dump(meta, f, sort_keys=True, indent=2)
            f.write("\n")
    print("[WP5-STEP-02] H1/H2R candidate-set metadata recorded without revealing contents",
          flush=True)
    return commit


def _sha(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


def main() -> int:
    print("[WP5-STEP-00] PHASE 14: freeze theorem candidates + constant", flush=True)
    fails, ctx = step_entry()
    if fails:
        print("[WP5-STEP-00] PHASE14_FAIL: %r" % (fails,), flush=True)
        return 2
    docs = step_freeze(ctx["shortlist"])
    commit = step_commit(docs)
    print("[WP5-STEP-02] PHASE14_PASS: TRANSFER_CALCULUS_FROZEN (%d candidates)"
          % len(docs), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
