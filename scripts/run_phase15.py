"""Spec PHASE 15 runner (REAL): consume fresh holdouts exactly once (WP-5).

Entry: TRANSFER_CALCULUS_FROZEN (candidate-set commitment + matching H3T
firewall). Order (WorkPlan/Section-14.6): causal/history ledgers consume H2R
then H3T; H1 is state-pair storage and cannot validate causal provenance, so it
is routed NOT_APPLICABLE (never mislabeled PASS). H2R bank bytes live in sealed
parent custody and were never vendored, so H2R is routed NOT_APPLICABLE without
fabrication. H3T (the transfer-specific bank) is evaluated fully: every episode
exactly, canonical first/max violations, replay bundles. No candidate mutation
inside this phase (post-reveal edits mint new POST_HOLDOUT IDs). Console lines
prefixed [WP5-STEP-0x] are the audit record.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import zstandard as zstd  # noqa: E402

from python.audit import cleanroom as cleanroom_mod  # noqa: E402
from python.freeze import candidates as freeze_mod  # noqa: E402
from python.holdout import firewall as firewall_mod  # noqa: E402
from python.holdout import h1_evaluate as h1_mod  # noqa: E402
from python.holdout import h2r_evaluate as h2r_mod  # noqa: E402
from python.holdout import h3t_evaluate as h3t_mod  # noqa: E402

H3T_SIZES = [10, 12, 16, 24, 32, 48, 64]

# WP5-STEP-00: modules the fresh-evaluation path may never import.
FORBIDDEN_IMPORTS = ("python.transfer", "python/solver", "python.solver",
                     "python.cycles.discovery", "python/cycles/discovery",
                     "python.adversary", "python/adversary",
                     "h3t_generate", "python.holdout.h3t_generate")


# WP5-STEP-00: Phase-15 entry gate (fail-closed).
def step_entry() -> tuple[list, dict]:
    fails: list = []
    ctx: dict = {}
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    commit_path = os.path.join(holdouts, "candidate_set_commit.json")
    if not os.path.exists(commit_path):
        fails.append("GATE-15 no candidate-set commitment (Phase 14 not done)")
        return fails, ctx
    commit = json.load(open(commit_path, encoding="utf-8"))
    if commit.get("status") != "TRANSFER_CALCULUS_FROZEN":
        fails.append("GATE-15 commitment not FROZEN")
    st = firewall_mod.load_state(os.path.join(holdouts, "h3t_state.json"))
    if st.get("state") == "UNLOCKED_ONCE":
        fails.append("GATE-15 H3T already UNLOCKED_ONCE (STOP-30 second unlock refused)")
    elif st.get("state") != "TRANSFER_CALCULUS_FROZEN":
        fails.append("GATE-15 H3T firewall not FROZEN (state=%r)" % st.get("state"))
    elif st.get("candidate_set_hash") != commit.get("set_hash"):
        fails.append("GATE-15 H3T firewall hash differs from commitment (HLD-11)")
    for fn in ("h1_reveal.json", "h2r_reveal.json", "h3t_reveal.json"):
        if os.path.exists(os.path.join(holdouts, fn)):
            fails.append("GATE-15 reveal already exists: %s (one-unlock)" % fn)
    ctx["commit"] = commit
    print("[WP5-STEP-00] PHASE 15 entry gates: %s"
          % ("PASS" if not fails else "FAIL %r" % (fails,)), flush=True)
    return fails, ctx


# WP5-STEP-00: static import audit of the fresh-evaluation path.
def step_import_audit() -> list:
    fails: list = []
    for rel in ("python/holdout/h1_evaluate.py", "python/holdout/h2r_evaluate.py",
                "python/holdout/h3t_evaluate.py", "python/audit/cleanroom.py"):
        tree = ast.parse(open(os.path.join(ROOT, rel), encoding="utf-8").read())
        got: list = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                got += [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                got.append(node.module)
        bad = [g for g in got for b in FORBIDDEN_IMPORTS if b in g]
        if bad:
            fails.append("IMPORT-AUDIT %s imports discovery: %r" % (rel, bad))
    if "python." in "".join(
            _imports_of(os.path.join(ROOT, "python/audit/cleanroom.py"))):
        fails.append("IMPORT-AUDIT cleanroom imports python/ modules (STOP-32)")
    print("[WP5-STEP-00] fresh-path import audit: %s"
          % ("PASS" if not fails else "FAIL %r" % (fails,)), flush=True)
    return fails


def _imports_of(path: str) -> list:
    tree = ast.parse(open(path, encoding="utf-8").read())
    got: list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            got += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            got.append(node.module)
    return got


# WP5-STEP-03: H1/H2R routing (schema + custody checks, no bank reads).
def step_route(commit: dict) -> dict:
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    ids = [m["calculus_id"] for m in commit["candidates"]]
    h1 = h1_mod.evaluate(
        ids, os.path.join(ROOT, "parent", "V02_H1_FIREWALL.json"), True)
    with open(os.path.join(holdouts, "h1_reveal.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(h1, f, sort_keys=True, indent=2)
        f.write("\n")
    h2r = h2r_mod.evaluate(
        ids, os.path.join(ROOT, "parent", "V02_H2R_FIREWALL.json"), True, None)
    with open(os.path.join(holdouts, "h2r_reveal.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(h2r, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP5-STEP-03] routing recorded: H1=%s H2R=%s"
          % (h1["verdict"], h2r["verdict"]), flush=True)
    return {"h1": h1, "h2r": h2r}


# WP5-STEP-04: full H3T evaluation (every episode, shared rotation build).
def _load_shard(bankdir: str, n: int) -> list:
    with open(os.path.join(bankdir, "n%d.json.zst" % n), "rb") as f:
        return json.loads(zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))


def step_h3t(commit: dict) -> dict:
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    bankdir = os.path.join(holdouts, "h3t_bank")
    cands = []
    for m in commit["candidates"]:
        pred, k, c_const, _doc = freeze_mod.load_frozen(
            os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                         m["calculus_id"] + ".json"))
        cands.append({"id": m["calculus_id"], "predicate": pred, "k": k, "C": c_const,
                      "n_episodes": 0, "n_burdened": 0, "max_res": Fraction(0),
                      "first": None, "paid": Fraction(0), "injected": Fraction(0)})
    for n in H3T_SIZES:
        eps = _load_shard(bankdir, n)
        eps = sorted(eps, key=lambda e: e["idx"])
        print("[WP5-STEP-04] H3T n=%d: %d episodes" % (n, len(eps)), flush=True)
        for ep in eps:
            rots, _sa, _sy = h3t_mod.episode_rotations(ep)
            burdened = any(r.get("y_edge", 0) > 0 for r in rots)
            for c in cands:
                r = h3t_mod.simulate(c["predicate"], c["k"], c["C"], rots)
                c["n_episodes"] += 1
                c["paid"] += r["paid"]
                c["injected"] += r["injected"]
                if burdened:
                    c["n_burdened"] += 1
                if r["max_res"] > c["max_res"]:
                    c["max_res"] = r["max_res"]
                if r["first"] is not None and c["first"] is None:
                    c["first"] = {"size": n, "idx": ep["idx"],
                                  "episode_hash": ep["episode_hash"],
                                  **r["first"],
                                  "failure_class": "BURDEN_UNPAID",
                                  "ledger_size_after": r["ledger_final_size"],
                                  "event_trace": rots}
    results = []
    for c in cands:
        verdict = "FRESH_H3T_PASS" if c["max_res"] == 0 else "FRESH_H3T_FAIL"
        first = c["first"]
        if first is not None:
            first = dict(first)
            first["w"] = list(first["w"])
            first["res"] = list(first["res"])
        results.append({"calculus_id": c["id"], "verdict": verdict,
                        "n_episodes": c["n_episodes"],
                        "n_burdened_episodes": c["n_burdened"],
                        "max_residual": [c["max_res"].numerator, c["max_res"].denominator],
                        "first_violation": first,
                        "paid_total": [c["paid"].numerator, c["paid"].denominator],
                        "injected_total": [c["injected"].numerator, c["injected"].denominator],
                        "fresh_claim": False})
        print("[WP5-STEP-04] %s: %s (%d episodes, max_res=%s)"
              % (c["id"], verdict, c["n_episodes"], c["max_res"]), flush=True)
    reveal = {"bank_id": "HOLDOUT-H3T-v0.3", "results": results,
              "reveal_state": "UNLOCKED_ONCE", "fresh_claim": False,
              "note": "survival is finite-sample survival, never theorem status"}
    with open(os.path.join(holdouts, "h3t_reveal.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(reveal, f, sort_keys=True, indent=2)
        f.write("\n")
    st_path = os.path.join(holdouts, "h3t_state.json")
    st = firewall_mod.load_state(st_path)
    if st.get("state") != "TRANSFER_CALCULUS_FROZEN":
        raise ValueError("H3T firewall moved during Phase 15 (STOP-30)")
    digest = hashlib.sha256(json.dumps(reveal, sort_keys=True).encode("utf-8")).hexdigest().upper()
    st["state"] = "UNLOCKED_ONCE"
    st["unlock_count"] = 1
    st["reveal_record"] = "h3t_reveal.json"
    st["reveal_sha256"] = digest
    with open(st_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(st, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP5-STEP-04] H3T firewall TRANSFER_CALCULUS_FROZEN -> UNLOCKED_ONCE "
          "(reveal=%s...)" % digest[:16], flush=True)
    return reveal


# WP5-STEP-05: independent replay of every fresh counterexample (clean-room).
def step_replay(reveal: dict, commit: dict) -> dict:
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    bankdir = os.path.join(holdouts, "h3t_bank")
    by_id = {m["calculus_id"]: m for m in commit["candidates"]}
    replayed: list = []
    for res in reveal["results"]:
        cid = res["calculus_id"]
        doc = json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                          cid + ".json"), encoding="utf-8"))
        pred = doc["active_predicate"]
        pname = ("P_all" if pred == {"any_of": [{"mode_is": "KEEP"},
                                                {"mode_is": "DELETE"}]}
                 else "P_keep")
        k = doc["injection_rules"][0]["k"]
        c_const = doc["universal_constant_C"]
        targets = []
        if res["first_violation"] is not None:
            fv = res["first_violation"]
            targets.append((fv["size"], fv["idx"], "first-violation"))
        else:
            for n in H3T_SIZES:
                eps = _load_shard(bankdir, n)
                eps = sorted(eps, key=lambda e: e["idx"])
                step = max(1, len(eps) // 2)
                for ep in (eps[0], eps[step]):
                    targets.append((n, ep["idx"], "zero-violation sample"))
        for (n, idx, kind) in targets:
            eps = _load_shard(bankdir, n)
            ep = next(e for e in eps if e["idx"] == idx)
            clean = cleanroom_mod.simulate_episode(
                n, ep["init_shape"], [tuple(h) for h in ep["history"]],
                pname, k, c_const)
            rots, _sa, _sy = h3t_mod.episode_rotations(ep)
            prim = h3t_mod.simulate(pred, k, c_const, rots)
            # NOTE: primary returns Fractions, clean-room [num, den] lists.
            agree = (prim["max_res"] == Fraction(*clean["max_res"])
                     and prim["feasible"] == clean["feasible"])
            replayed.append({"calculus_id": cid, "size": n, "idx": idx,
                             "kind": kind, "agree": agree,
                             "primary_max_res": [prim["max_res"].numerator,
                                                 prim["max_res"].denominator],
                             "clean_max_res": list(clean["max_res"])})
            if not agree:
                raise ValueError("clean-room replay disagrees on %s n=%d idx=%d"
                                 % (cid, n, idx))
    print("[WP5-STEP-05] independent replay: %d checks, all agree" % len(replayed),
          flush=True)
    with open(os.path.join(holdouts, "h3t_replay.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump({"replayed": replayed}, f, sort_keys=True, indent=2)
        f.write("\n")
    return {"replayed": replayed}


# WP5-STEP-05: crash-recovery mode (completes an interrupted STEP-05 only).
def main_replay_only() -> int:
    """Resume only the independent-replay step after an interrupted Phase-15 run.

    Requires the reveal         + UNLOCKED_ONCE firewall to already exist with
    matching hashes; writes only h3t_replay.json. No firewall change, no new
    reveal, no second unlock, no candidate contact beyond replay reads.
    """
    import hashlib as _hashlib
    print("[WP5-STEP-05] PHASE 15 replay-only recovery (no unlock, no reveal rewrite)",
          flush=True)
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    commit = json.load(open(os.path.join(holdouts, "candidate_set_commit.json"),
                            encoding="utf-8"))
    reveal = json.load(open(os.path.join(holdouts, "h3t_reveal.json"), encoding="utf-8"))
    st = firewall_mod.load_state(os.path.join(holdouts, "h3t_state.json"))
    digest = _hashlib.sha256(json.dumps(reveal, sort_keys=True).encode("utf-8")).hexdigest().upper()
    if st.get("state") != "UNLOCKED_ONCE" or st.get("reveal_sha256") != digest:
        print("[WP5-STEP-05] REPLAY-ONLY REFUSED: firewall/reveal mismatch", flush=True)
        return 2
    if os.path.exists(os.path.join(holdouts, "h3t_replay.json")):
        print("[WP5-STEP-05] REPLAY-ONLY REFUSED: replay record already exists", flush=True)
        return 2
    fails = step_import_audit()
    if fails:
        print("[WP5-STEP-05] PHASE15_FAIL: %r" % (fails,), flush=True)
        return 2
    step_replay(reveal, commit)
    print("[WP5-STEP-05] PHASE15_PASS (replay completed): fresh holdouts consumed once",
          flush=True)
    return 0


def main(argv=None) -> int:
    import argparse as _argparse
    ap = _argparse.ArgumentParser()
    ap.add_argument("--replay-only", action="store_true",
                    help="complete interrupted STEP-05 only (no unlock)")
    args = ap.parse_args(argv)
    if args.replay_only:
        return main_replay_only()
    print("[WP5-STEP-00] PHASE 15: consume fresh holdouts exactly once", flush=True)
    fails, ctx = step_entry()
    if fails:
        print("[WP5-STEP-00] PHASE15_FAIL: %r" % (fails,), flush=True)
        return 2
    fails = step_import_audit()
    if fails:
        print("[WP5-STEP-00] PHASE15_FAIL: %r" % (fails,), flush=True)
        return 2
    step_route(ctx["commit"])
    reveal = step_h3t(ctx["commit"])
    step_replay(reveal, ctx["commit"])
    print("[WP5-STEP-05] PHASE15_PASS: fresh holdouts consumed once", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
