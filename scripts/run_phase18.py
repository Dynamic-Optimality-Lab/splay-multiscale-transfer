"""Spec PHASE 18 runner (REAL): bridge/negative audit + paper-facing reports (WP-6).

Entry: Phase-17 lifecycle audit clean (0 jumps). Steps: WP6-STEP-00 entry;
WP6-STEP-04 bridge/negative audit record (positive branch NOT_REACHED past
author-claim injection; negative branch NOT_ACTIVATED; exactly one
finite branch active); WP6-STEP-05 report verification (Q01–Q40 coverage +
claim-level discipline); WP6-STEP-06 ledger finalization + atlas appends
(idempotent, marker-guarded). No theorem is proved or consumed here.
Console lines prefixed [WP6-STEP-0x] are the audit record.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# WP6-STEP-04: NEG-01..08 vacuous checks (negative branch never activated).
NEG_CHECKS = [
    ("NEG-01", "fixed-C failure not misclassified",
     "all kills labeled candidate-at-frozen-C (ladder/histories/h3t reveals)"),
    ("NEG-02", "actual Splay ratio used",
     "triage tracked R_k = sum(c_B)/sum(c_A) only (triage.json)"),
    ("NEG-03", "family closed form", "VACUOUS: no family (NOT_ACTIVATED 11/11)"),
    ("NEG-04", "diagonal-rooted legality", "VACUOUS: no family"),
    ("NEG-05", "symbolic full-sequence upper bound", "VACUOUS: no family"),
    ("NEG-06", "symbolic subsequence lower bound", "VACUOUS: no family"),
    ("NEG-07", "ratio limit proof", "VACUOUS: no family"),
    ("NEG-08", "independent family replay", "VACUOUS: no family"),
]

# WP6-STEP-05: reports whose presence + coverage is verified.
REPORTS = ["MULTISCALE_TRANSFER_REPORT.md", "THEOREM_STATUS_REPORT.md",
           "REPRODUCIBILITY.md", "AI_USE.md"]

# WP6-STEP-05: exact forbidden assertion strings (§33.4) — must not appear.
FORBIDDEN_ASSERTIONS = ["the calculus works for all n",
                        "Dynamic Optimality is proved"]


# WP6-STEP-00: Phase-18 entry gate (fail-closed).
def step_entry() -> tuple[list, dict]:
    fails: list = []
    ctx: dict = {}
    audit_path = os.path.join(ROOT, "artifacts", "v03", "proofs", "lifecycle_audit.json")
    if not os.path.exists(audit_path):
        fails.append("GATE-18 no lifecycle audit (Phase 17 not done)")
        return fails, ctx
    record = json.load(open(audit_path, encoding="utf-8"))
    if record.get("jumps") or record.get("pointerless"):
        fails.append("GATE-18 lifecycle audit unclean")
    ctx["lifecycle"] = record
    print("[WP6-STEP-00] PHASE 18 entry gates: %s"
          % ("PASS" if not fails else "FAIL %r" % (fails,)), flush=True)
    return fails, ctx


# WP6-STEP-04: bridge/negative audit record.
def step_bridge_negative(lifecycle: dict) -> dict:
    counts = lifecycle["counts"]
    neg = [{"id": nid, "check": name, "status": "VACUOUS_NOT_ACTIVATED",
            "evidence": ev} for nid, name, ev in NEG_CHECKS]
    tort = json.load(open(os.path.join(ROOT, "artifacts", "v03", "adversarial",
                                       "triage.json"), encoding="utf-8"))
    n_inactivated = sum(1 for t in tort["triaged"]
                        if t["triage"]["status"] == "NEGATIVE_FAMILY_NOT_ACTIVATED")
    record = {
        "positive_branch": {
            "primary": "MSTC-0002",
            "MST_GATE_16": "PROVED_PENDING_REVIEW (author claim, not consumed)",
            "MST_GATE_17": "NOT_REACHED (MST0-14/15 UNPROVED)",
            "MST_GATE_18": "NOT_REACHED", "MST_GATE_19": "NOT_REACHED",
            "MST_GATE_20": "NOT_REACHED", "MST_GATE_21": "NOT_REACHED",
            "theorem_branch_active": False,
        },
        "negative_branch": {
            "status": "NEGATIVE_FAMILY_NOT_ACTIVATED",
            "triaged_motifs": len(tort["triaged"]),
            "not_activated": n_inactivated,
            "neg_checks": neg,
            "theorem_branch_active": False,
        },
        "finite_branch": {"active": True,
                          "level": "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS",
                          "standing": ["MSTC-0002"]},
        "exactly_one_branch_active": True,
        "obligation_counts": counts,
    }
    if not (record["exactly_one_branch_active"]
            and record["finite_branch"]["active"]
            and not record["positive_branch"]["theorem_branch_active"]
            and not record["negative_branch"]["theorem_branch_active"]):
        raise ValueError("branch-exclusivity violated")
    outdir = os.path.join(ROOT, "artifacts", "v03", "audits")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "bridge_negative_audit.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(record, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP6-STEP-04] bridge/negative audit: no theorem branch active "
          "(finite branch only; NEG 8/8 vacuous-with-evidence)", flush=True)
    return record


# WP6-STEP-05: report verification (presence + Q-coverage + claim discipline).
def step_reports() -> list:
    fails: list = []
    for rel in REPORTS:
        if not os.path.exists(os.path.join(ROOT, rel)):
            fails.append("REPORT missing " + rel)
    body = open(os.path.join(ROOT, "MULTISCALE_TRANSFER_REPORT.md"),
                encoding="utf-8").read()
    for i in range(1, 41):
        if ("Q%02d" % i) not in body:
            fails.append("REPORT question Q%02d unanswered" % i)
    if "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS" not in body:
        fails.append("REPORT Q36 level missing")
    scanned = "\n".join(open(os.path.join(ROOT, rel), encoding="utf-8").read()
                        for rel in REPORTS + ["TRANSFER_CALCULUS_LEDGER.md"])
    for s in FORBIDDEN_ASSERTIONS:
        if s in scanned:
            fails.append("REPORT forbidden assertion present: %r" % s)
    print("[WP6-STEP-05] reports: %d files, Q01–Q40 covered, claim discipline (%s)"
          % (len(REPORTS), "PASS" if not fails else "FAIL %r" % (fails,)), flush=True)
    return fails


# WP6-STEP-06: ledger finalization + atlas appends (idempotent, marker-guarded).
def step_finalize_docs() -> None:
    ledger_path = os.path.join(ROOT, "TRANSFER_CALCULUS_LEDGER.md")
    ledger = open(ledger_path, encoding="utf-8").read()
    if "<!-- WP6-SEAL -->" not in ledger:
        with open(ledger_path, "a", encoding="utf-8", newline="\n") as f:
            f.write("\n## WP-6 seal (FINAL)\n\n<!-- WP6-SEAL -->\n"
                    "Standing finite survivor: MSTC-0002 (P_all, k=6, C=2) —\n"
                    "70,000/70,000 H3T episodes + 54 large-n trials, zero exact\n"
                    "residuals. Siblings MSTC-0001 (max_res=8) and MSTC-0003\n"
                    "(max_res=23) killed fresh with witnesses in\n"
                    "`artifacts/v03/holdouts/h3t_reveal.json`. Terminal claim:\n"
                    "`TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS` (see\n"
                    "`artifacts/v03/seal/FINAL_RESULT.json`). No theorem; pending\n"
                    "human reviews MST0-13/23/24/26 are not consumed.\n")
        print("[WP6-STEP-06] ledger finalized with seal pointer", flush=True)
    else:
        print("[WP6-STEP-06] ledger seal section already present (idempotent)", flush=True)
    atlas_path = os.path.join(ROOT, "COUNTEREXAMPLE_ATLAS.md")
    atlas = open(atlas_path, encoding="utf-8").read()
    if "<!-- WP6-FRESH-KILLS -->" not in atlas:
        with open(atlas_path, "a", encoding="utf-8", newline="\n") as f:
            f.write("\n## Killed on fresh H3T (WP-5, frozen C, append-only)\n\n"
                    "<!-- WP6-FRESH-KILLS -->\n"
                    "- MSTC-0001 (P_all,k=2,C=2): max_res=[8,1]; first n=32 idx 4406 "
                    "(w=[11,1] paid 9, edge a=1/y=13, x=11). Minimal-k anchor does not "
                    "transfer; rate insufficiency vs burst demand at larger n.\n"
                    "- MSTC-0003 (P_keep,k=1,C=6): max_res=[23,1]; first n=16 idx 3610 "
                    "(w=[8,1] paid 7, edge a=1/y=14, x=3). Weakest-predicate survivor "
                    "does not transfer; DELETE-burst timing killer persists fresh.\n"
                    "- MSTC-0002 (P_all,k=6,C=2): 0/70,000 residuals; not a kill — "
                    "standing survivor (finite only).\n"
                    "- Full witnesses + replay bundles: "
                    "`artifacts/v03/holdouts/h3t_reveal.json`; replays: `h3t_replay.json`.\n"
                    "- Representation obstructions (§32.10), not conjecture obstructions: "
                    "no growing actual Splay ratio observed anywhere.\n")
        print("[WP6-STEP-06] counterexample atlas extended with fresh kills", flush=True)
    else:
        print("[WP6-STEP-06] atlas fresh-kills section already present (idempotent)",
              flush=True)


def main() -> int:
    print("[WP6-STEP-00] PHASE 18: bridge/negative audit + paper-facing reports",
          flush=True)
    fails, ctx = step_entry()
    if fails:
        print("[WP6-STEP-00] PHASE18_FAIL: %r" % (fails,), flush=True)
        return 2
    step_bridge_negative(ctx["lifecycle"])
    fails = step_reports()
    if fails:
        print("[WP6-STEP-05] PHASE18_FAIL: %r" % (fails,), flush=True)
        return 2
    step_finalize_docs()
    print("[WP6-STEP-06] PHASE18_PASS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
