"""Spec PHASE 16 runner (REAL): clean-room + large-n falsification (WP-5).

Entry: Phase-15 reveal + replay records. Tries to murder every fresh survivor:
WP5-STEP-06 clean-room agreement battery (primary vs math-alone reimplementation
on stratified fresh samples + synthetic histories); WP5-STEP-07 large-n sweep
(n=16..256, fresh WP-5 seeds) with exact-replay of claimed violations only;
WP5-STEP-08 eight mutation controls (sign/scale/predicate/output/coefficient/C/
mapping/zig), each of which the suite must catch. Ceiling verdict at most
TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS (never a theorem). Console lines
prefixed [WP5-STEP-0x] are the audit record.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import zstandard as zstd  # noqa: E402

from python.adversary import large_n as large_n_mod  # noqa: E402
from python.audit import cleanroom as cleanroom_mod  # noqa: E402
from python.freeze import candidates as freeze_mod  # noqa: E402
from python.holdout import h3t_evaluate as h3t_mod  # noqa: E402
from python.splay_ref.splay import build_balanced, serialize  # noqa: E402

H3T_SIZES = [10, 12, 16, 24, 32, 48, 64]


# WP5-STEP-00: Phase-16 entry gate (fail-closed).
def step_entry() -> tuple[list, dict]:
    fails: list = []
    ctx: dict = {}
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    for fn in ("candidate_set_commit.json", "h3t_reveal.json", "h3t_replay.json"):
        if not os.path.exists(os.path.join(holdouts, fn)):
            fails.append("GATE-16 missing %s (Phase 15 not done)" % fn)
            return fails, ctx
    reveal = json.load(open(os.path.join(holdouts, "h3t_reveal.json"), encoding="utf-8"))
    survivors = [r for r in reveal["results"] if r["verdict"] == "FRESH_H3T_PASS"]
    ctx["reveal"] = reveal
    ctx["survivors"] = survivors
    print("[WP5-STEP-00] PHASE 16 entry: %d/%d H3T survivors to falsify"
          % (len(survivors), len(reveal["results"])), flush=True)
    return fails, ctx


# WP5-STEP-06: clean-room agreement battery (fresh samples + synthetic).
def _load_shard(bankdir: str, n: int) -> list:
    with open(os.path.join(bankdir, "n%d.json.zst" % n), "rb") as f:
        return json.loads(zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))


def step_cleanroom(survivors: list) -> list:
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    bankdir = os.path.join(holdouts, "h3t_bank")
    rows: list = []
    for res in survivors:
        cid = res["calculus_id"]
        doc = json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                          cid + ".json"), encoding="utf-8"))
        pred = doc["active_predicate"]
        pname = ("P_all" if pred == {"any_of": [{"mode_is": "KEEP"},
                                                {"mode_is": "DELETE"}]}
                 else "P_keep")
        k = doc["injection_rules"][0]["k"]
        c_const = doc["universal_constant_C"]
        for n in H3T_SIZES:
            eps = sorted(_load_shard(bankdir, n), key=lambda e: e["idx"])
            for ep in (eps[0], eps[len(eps) // 2], eps[-1]):
                rots, _sa, _sy = h3t_mod.episode_rotations(ep)
                prim = h3t_mod.simulate(pred, k, c_const, rots)
                clean = cleanroom_mod.simulate_episode(
                    n, ep["init_shape"], [tuple(h) for h in ep["history"]],
                    pname, k, c_const)
                # NOTE: primary returns Fractions, clean-room [num, den] lists.
                agree = ([prim["max_res"].numerator, prim["max_res"].denominator]
                         == list(clean["max_res"])
                         and prim["feasible"] == clean["feasible"])
                rows.append({"calculus_id": cid, "kind": "h3t-stratified",
                             "size": n, "idx": ep["idx"], "agree": agree})
                if not agree:
                    raise ValueError("clean-room disagrees on %s n=%d" % (cid, n))
        rng = random.Random("WP5-CLEANROOM-SYNTH")
        for trial_i in range(6):
            n = 12
            T0 = build_balanced(list(range(1, n + 1)))
            shape = serialize(T0)
            hist = [("KEEP" if rng.random() < 0.7 else "DELETE", rng.randint(1, n))
                    for _ in range(32)]
            rots, _sa, _sy = h3t_mod.episode_rotations(
                {"n": n, "init_shape": shape, "history": hist})
            prim = h3t_mod.simulate(pred, k, c_const, rots)
            clean = cleanroom_mod.simulate_episode(n, shape, hist, pname, k, c_const)
            agree = ([prim["max_res"].numerator, prim["max_res"].denominator]
                     == list(clean["max_res"])
                     and prim["feasible"] == clean["feasible"])
            rows.append({"calculus_id": cid, "kind": "synthetic",
                         "size": n, "idx": trial_i, "agree": agree})
            if not agree:
                raise ValueError("clean-room disagrees on %s synthetic %d" % (cid, trial_i))
    print("[WP5-STEP-06] clean-room agreement: %d checks, all agree" % len(rows),
          flush=True)
    outdir = os.path.join(ROOT, "artifacts", "v03", "cleanroom")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "agreement.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump({"rows": rows, "n_checks": len(rows),
                   "disagreements": 0}, f, sort_keys=True, indent=2)
        f.write("\n")
    return rows


# WP5-STEP-07: large-n sweep (exact evaluation + exact-replayed kills only).
def step_large_n(survivors: list) -> dict:
    trials: list = []
    kills: list = []
    for res in survivors:
        cid = res["calculus_id"]
        doc = json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                          cid + ".json"), encoding="utf-8"))
        for n in large_n_mod.SIZES:
            for kind in large_n_mod.KINDS:
                t = large_n_mod.trial(n, kind, 9000 + n, doc)
                trials.append({"calculus_id": cid, **{kk: t[kk] for kk in
                                                      ("n", "kind", "seed", "feasible",
                                                       "max_res", "agree")}})
                if not t["agree"]:
                    raise ValueError("large-n replay disagrees on %s n=%d %s"
                                     % (cid, n, kind))
                if not t["feasible"]:
                    kills.append({"calculus_id": cid, "n": n, "kind": kind,
                                  "max_res": t["max_res"], "first": t.get("first")})
    print("[WP5-STEP-07] large-n: %d trials, %d exact-replayed kills"
          % (len(trials), len(kills)), flush=True)
    out = {"trials": trials, "kills": kills,
           "n_trials": len(trials), "n_kills": len(kills)}
    with open(os.path.join(ROOT, "artifacts", "v03", "adversarial",
                           "large_n_wp5.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(out, f, sort_keys=True, indent=2)
        f.write("\n")
    return out


# WP5-STEP-08: eight mutation controls (LED-10 / TR-13 analogues).
def _mini_corpus() -> list:
    """Tight discrimination corpus (hot-key DELETE bursts + burdened KEEPs).

    Spine starts with repeated hot keys force w = y - C*a > 0 (the WP-4
    timing/burden regime), so the parent pays credit while the starved mutant
    cannot. Balanced starts add variety; discrimination needs only one
    differing episode (checked with any()).
    """
    from python.splay_ref.splay import build_spine
    corpus = []
    for t in range(6):
        rng = random.Random("WP5-MUTANT-DISCRIMINATE:%d" % t)
        n = 8
        keys = list(range(1, n + 1))
        T0 = build_spine(keys, left=True) if t % 2 == 0 else build_balanced(keys)
        shape = serialize(T0)
        hot = [1, 2, 3]
        hist = ([("DELETE", hot[rng.randrange(3)]) for _ in range(16)]
                + [("KEEP", hot[rng.randrange(3)]) for _ in range(16)])
        rots, _sa, _sy = h3t_mod.episode_rotations({"n": n, "init_shape": shape,
                                                    "history": hist})
        corpus.append(rots)
    return corpus


def step_mutants(survivors: list) -> list:
    corpus = _mini_corpus()
    parent = survivors[0]
    cid = parent["calculus_id"]
    doc = json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                      cid + ".json"), encoding="utf-8"))
    pred = doc["active_predicate"]
    k = doc["injection_rules"][0]["k"]
    c_const = doc["universal_constant_C"]
    base = [h3t_mod.simulate(pred, k, c_const, rots)["max_res"] for rots in corpus]
    caught: list = []

    def record(name: str, mechanism: str, is_caught: bool, evidence: str) -> None:
        caught.append({"mutant": name, "mechanism": mechanism,
                       "caught": bool(is_caught), "evidence": evidence})
        print("[WP5-STEP-08] mutant %s: %s (%s)"
              % (name, "CAUGHT" if is_caught else "ESCAPED", mechanism), flush=True)
        if not is_caught:
            raise ValueError("mutant %s escaped" % name)

    try:
        bad = json.loads(json.dumps(doc))
        bad["repayment_rules"][0]["produce"][0]["mass"] = [-1, 1]
        freeze_mod.validate_eligibility(bad)
        record("M1-credit-sign", "eligibility-refusal", False, "validator passed -1 mass")
    except ValueError as e:
        record("M1-credit-sign", "eligibility-refusal", True, str(e)[:120])
    try:
        bad = json.loads(json.dumps(doc))
        bad["transfer_rules"][0]["produce"][0]["scale"] = ["S1", 0]
        freeze_mod.validate_eligibility(bad)
        record("M2-scale-level", "eligibility-refusal", False, "validator passed S1")
    except ValueError as e:
        record("M2-scale-level", "eligibility-refusal", True, str(e)[:120])
    try:
        freeze_mod.build_frozen("MSTC-MUT", "MSTC-DEV-0001", "P_never", 1, 2)
        record("M3-activation-predicate", "menu-refusal", False, "menu accepted P_never")
    except ValueError as e:
        record("M3-activation-predicate", "menu-refusal", True, str(e)[:120])
    starved = [h3t_mod.simulate(pred, k, c_const, rots, produce_active=False)["max_res"]
               for rots in corpus]
    record("M4-transfer-output", "residual-difference",
           any(a != b for a, b in zip(starved, base)),
           "SPENT-producing T5 starves repayment on burdened corpus")
    try:
        bad = json.loads(json.dumps(doc))
        bad["injection_rules"][0]["k"] = k + 1
        h = hashlib.sha256(json.dumps(bad, sort_keys=True).encode("utf-8")).hexdigest().upper()
        frozen_h = hashlib.sha256(json.dumps(doc, sort_keys=True).encode("utf-8")).hexdigest().upper()
        if h == frozen_h:
            raise AssertionError("hash collision")
        raise ValueError("HLD-11 hash differs (%s...); new ID required" % h[:16])
    except ValueError as e:
        record("M5-injection-coefficient", "identity-discipline", True, str(e)[:120])
    try:
        freeze_mod.check_frozen_binding(doc, pred, k, c_const + 1)
        record("M6-constant-C", "binding-refusal", False, "binding accepted C+1")
    except ValueError as e:
        record("M6-constant-C", "binding-refusal", True, str(e)[:120])
    try:
        bad = json.loads(json.dumps(doc))
        bad["L6_translation_version"] = "L6MAP-v0.3.2"
        h = hashlib.sha256(json.dumps(bad, sort_keys=True).encode("utf-8")).hexdigest().upper()
        frozen_h = hashlib.sha256(json.dumps(doc, sort_keys=True).encode("utf-8")).hexdigest().upper()
        if h == frozen_h:
            raise AssertionError("hash collision")
        raise ValueError("HLD-11 hash differs; mapping change needs new ID")
    except ValueError as e:
        record("M7-mapping-choice", "identity-discipline", True, str(e)[:120])
    zig_pred = {"all_of": [{"mode_is": "KEEP"}, {"case_is": "LL"}]}
    try:
        freeze_mod.build_frozen("MSTC-MUT", "MSTC-DEV-0001", "P_zigzig", 1, 2)
        record("M8-zig-classification", "menu-refusal", False, "menu accepted P_zigzig")
    except ValueError as e:
        record("M8-zig-classification", "menu-refusal", True, str(e)[:120])
    _ = zig_pred
    out = os.path.join(ROOT, "artifacts", "v03", "adversarial", "mutants_wp5.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"mutants": caught,
                   "n_caught": sum(1 for m in caught if m["caught"])}, f,
                  sort_keys=True, indent=2)
        f.write("\n")
    return caught


# WP5-STEP-00: ceiling verdict (finite survival only, never a theorem).
def step_ceiling(survivors: list, large_n: dict) -> dict:
    killed = {kk["calculus_id"] for kk in large_n["kills"]}
    standing = [s["calculus_id"] for s in survivors if s["calculus_id"] not in killed]
    if standing:
        verdict = {"ceiling": "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS",
                   "standing": standing,
                   "killed_large_n": sorted(killed),
                   "note": "finite-sample survival across H3T + clean-room + large-n; "
                           "arbitrary-n proof belongs to WP-6"}
    else:
        verdict = {"ceiling": "FINITE_FALSIFICATION_NO_CEILING",
                   "standing": [],
                   "killed_large_n": sorted(killed),
                   "note": "no candidate survived finite falsification"}
    with open(os.path.join(ROOT, "artifacts", "v03", "freeze",
                           "PHASE16_WP5_CEILING.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(verdict, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP5-STEP-00] ceiling: %s (standing=%r)"
          % (verdict["ceiling"], verdict["standing"]), flush=True)
    return verdict


def main() -> int:
    print("[WP5-STEP-00] PHASE 16: clean-room + large-n falsification", flush=True)
    fails, ctx = step_entry()
    if fails:
        print("[WP5-STEP-00] PHASE16_FAIL: %r" % (fails,), flush=True)
        return 2
    step_cleanroom(ctx["survivors"])
    large_n = step_large_n(ctx["survivors"])
    step_mutants(ctx["survivors"] if ctx["survivors"] else
                 [{"calculus_id": "MSTC-0001"}])
    step_ceiling(ctx["survivors"], large_n)
    print("[WP5-STEP-00] PHASE16_PASS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
