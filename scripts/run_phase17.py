"""Spec PHASE 17 runner (REAL): universal rotation-level proof records (WP-6).

Entry: WP-5 ceiling TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS (standing finite
survivor MSTC-0002 promoted as the single primary; at most one at a time).
Steps: WP6-STEP-00 entry gates; WP6-STEP-01 universal-record presence audit
(proofs + BLOCKED markers + NOT_APPLICABLE justifications; stubs superseded);
WP6-STEP-02 MST0-13 machine evidence (injection bound on fresh samples);
WP6-STEP-03 lifecycle audit + per-obligation bundles. Author claims at most
PROVED; REVIEWED is minted only by human ACCEPT (requested, never fabricated).
Console lines prefixed [WP6-STEP-0x] are the audit record.
"""
from __future__ import annotations

import json
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import zstandard as zstd  # noqa: E402

from python.audit import lifecycle as lifecycle_mod  # noqa: E402
from python.holdout import h3t_evaluate as h3t_mod  # noqa: E402

# WP6-STEP-00: the single promoted primary (Phase 17 promotes at most one).
PRIMARY = "MSTC-0002"

# WP6-STEP-01: required records per obligation outcome class.
REQUIRED_DOCS = [
    "math/theorem_MST13_delete_injection.md",
    "math/theorem_MST14_keep_repayment.md",
    "math/theorem_MST15_integrability.md",
    "math/theorem_MST17_pair_access.md",
    "math/theorem_MST18_telescoping.md",
    "math/theorem_MST19_bridge.md",
    "math/theorem_MST20_negative_guard.md",
    "math/theorem_MST21_negative_family.md",
    "math/theorem_MST23_finite_integrability_guard.md",
    "math/theorem_MST24_branch_scope.md",
    "math/theorem_MST26_literature_scope.md",
]
REQUIRED_MARKERS = ["MST0-17", "MST0-18", "MST0-19"]
REQUIRED_JUSTIFICATIONS = ["MST0-12", "MST0-20", "MST0-21"]
SUPERSEDED_STUBS_GONE = [
    "math/theorem_MST13_stub.md", "math/theorem_MST14_stub.md",
    "math/theorem_MST15_stub.md", "math/theorem_MST17_stub.md",
    "math/theorem_MST18_stub.md", "math/theorem_MST19_stub.md",
    "math/theorem_MST20_stub.md", "math/theorem_MST21_stub.md",
    "math/theorem_MST23_stub.md", "math/theorem_MST24_stub.md",
    "math/theorem_MST26_stub.md",
]


# WP6-STEP-00: Phase-17 entry gate (fail-closed).
def step_entry() -> tuple[list, dict]:
    fails: list = []
    ctx: dict = {}
    ceiling_path = os.path.join(ROOT, "artifacts", "v03", "freeze",
                                "PHASE16_WP5_CEILING.json")
    if not os.path.exists(ceiling_path):
        fails.append("GATE-17 no WP-5 ceiling (Phase 16 not done)")
        return fails, ctx
    ceiling = json.load(open(ceiling_path, encoding="utf-8"))
    if ceiling.get("ceiling") != "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS":
        fails.append("GATE-17 no finite survivor to promote (ceiling=%r)"
                     % ceiling.get("ceiling"))
    if PRIMARY not in ceiling.get("standing", []):
        fails.append("GATE-17 primary %s not standing" % PRIMARY)
    ctx["ceiling"] = ceiling
    print("[WP6-STEP-00] PHASE 17 entry gates: %s (primary=%s)"
          % ("PASS" if not fails else "FAIL %r" % (fails,), PRIMARY), flush=True)
    return fails, ctx


# WP6-STEP-01: universal-record presence audit (fail-closed on any gap).
def step_records() -> list:
    fails: list = []
    for rel in REQUIRED_DOCS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            fails.append("RECORD missing " + rel)
            continue
        text = open(p, encoding="utf-8").read()
        if "**Status:**" not in text:
            fails.append("RECORD no Status line " + rel)
    for oid in REQUIRED_MARKERS:
        p = os.path.join(ROOT, "math", "reviews", oid + ".BLOCKED")
        if not os.path.exists(p):
            fails.append("RECORD missing BLOCKED marker " + oid)
            continue
        rec = json.load(open(p, encoding="utf-8"))
        if not rec.get("blocked_by"):
            fails.append("RECORD empty blocked_by " + oid)
    for oid in REQUIRED_JUSTIFICATIONS:
        p = os.path.join(ROOT, "math", "reviews", oid + ".not_applicable.json")
        if not os.path.exists(p):
            fails.append("RECORD missing justification " + oid)
            continue
        rec = json.load(open(p, encoding="utf-8"))
        if not (rec.get("reason") and rec.get("evidence")):
            fails.append("RECORD unjustified " + oid)
    for rel in SUPERSEDED_STUBS_GONE:
        if os.path.exists(os.path.join(ROOT, rel)):
            fails.append("RECORD superseded stub still present " + rel)
    print("[WP6-STEP-01] universal records: %d docs + %d markers + %d justifications (%s)"
          % (len(REQUIRED_DOCS), len(REQUIRED_MARKERS), len(REQUIRED_JUSTIFICATIONS),
             "PASS" if not fails else "FAIL %r" % (fails,)), flush=True)
    return fails


# WP6-STEP-02: MST0-13 machine evidence (supporting only, never the proof).
def _load_shard(bankdir: str, n: int) -> list:
    with open(os.path.join(bankdir, "n%d.json.zst" % n), "rb") as f:
        return json.loads(zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))


def step_injection_evidence() -> dict:
    bankdir = os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_bank")
    commit = json.load(open(os.path.join(ROOT, "artifacts", "v03", "holdouts",
                                         "candidate_set_commit.json"), encoding="utf-8"))
    rows: list = []
    for m in commit["candidates"]:
        doc = json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                          m["calculus_id"] + ".json"), encoding="utf-8"))
        pred = doc["active_predicate"]
        k = doc["injection_rules"][0]["k"]
        c_const = doc["universal_constant_C"]
        for n in (10, 24, 64):
            eps = sorted(_load_shard(bankdir, n), key=lambda e: e["idx"])
            for ep in (eps[0], eps[len(eps) // 2]):
                rots, _sa, _sy = h3t_mod.episode_rotations(ep)
                r_a = sum(1 for r in rots if r["side"] == "A")
                r = h3t_mod.simulate(pred, k, c_const, rots)
                holds = r["injected"] <= k * r_a
                rows.append({"calculus_id": m["calculus_id"], "size": n,
                             "idx": ep["idx"], "r_a": r_a,
                             "injected": [r["injected"].numerator,
                                          r["injected"].denominator],
                             "bound": [k * r_a, 1], "holds": bool(holds)})
                if not holds:
                    raise ValueError("injection bound violated on %s n=%d"
                                     % (m["calculus_id"], n))
    out = {"rows": rows, "n_checks": len(rows), "violations": 0,
           "note": "supporting evidence for MST0-13 Lemma 2; the proof is the doc"}
    with open(os.path.join(ROOT, "artifacts", "v03", "proofs",
                           "MST13_injection_bound.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(out, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP6-STEP-02] MST0-13 machine evidence: %d checks, bound holds" % len(rows),
          flush=True)
    return out


# WP6-STEP-03: lifecycle audit + per-obligation bundles.
def step_lifecycle() -> dict:
    from python.audit import status as status_mod
    record = lifecycle_mod.audit(ROOT)
    with open(os.path.join(ROOT, "artifacts", "v03", "proofs",
                           "lifecycle_audit.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(record, f, sort_keys=True, indent=2)
        f.write("\n")
    # NOTE: refresh the live derived view (recomputed, never frozen) and prove
    # it coincides with the audit (two writers, one truth).
    live = status_mod.main(ROOT)
    if live != record["statuses"]:
        raise ValueError("derived obligation view differs from lifecycle audit")
    bdir = os.path.join(ROOT, "artifacts", "v03", "proofs", "bundles")
    os.makedirs(bdir, exist_ok=True)
    for oid, bundle in sorted(record["bundles"].items()):
        with open(os.path.join(bdir, oid + ".json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(bundle, f, sort_keys=True, indent=2)
            f.write("\n")
    print("[WP6-STEP-03] lifecycle audit sealed: %s; %d bundles"
          % (record["counts"], len(record["bundles"])), flush=True)
    return record


def main() -> int:
    print("[WP6-STEP-00] PHASE 17: universal rotation-level proof records", flush=True)
    fails, ctx = step_entry()
    if fails:
        print("[WP6-STEP-00] PHASE17_FAIL: %r" % (fails,), flush=True)
        return 2
    fails = step_records()
    if fails:
        print("[WP6-STEP-01] PHASE17_FAIL: %r" % (fails,), flush=True)
        return 2
    step_injection_evidence()
    record = step_lifecycle()
    print("[WP6-STEP-03] PHASE17_PASS: counts=%s (PROVED author-claims await human review)"
          % (record["counts"],), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
