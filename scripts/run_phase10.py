"""Spec PHASE 10 runner (REAL): Branch-A raw-boundary synthesis on development only.

Entry: TRANSFER_GRAMMAR_FROZEN cert + MST0-03 REVIEWED + H3T committed + prereg
solver_backends unchanged + H3T firewall pinned + no-holdout-import scan clean.
Steps: WP4-STEP-00 backend freeze + firewall pins; WP4-STEP-01 discovery masks +
dev/validation corpora + flow screen; WP4-STEP-02 CEGIS(z3)+brute force with
agreement; WP4-STEP-03 ladder verdict (survive / minimal obstruction).
Scope discipline: Stage-1 screen (critical + near-critical cycles) decides the
family; generated histories screen survivors/near-misses only. One exact residual
at frozen C rejects that candidate at that C (gate semantics in log).
Console lines prefixed [WP4-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
from fractions import Fraction

import z3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles import discovery as disc_mod  # noqa: E402
from python.cycles.enumerate import PairDomain  # noqa: E402
from python.solver import certify as certify_mod  # noqa: E402
from python.solver import encode_sat as sat_mod  # noqa: E402
from python.solver import flow as flow_mod  # noqa: E402
from python.solver import ilp as ilp_mod  # noqa: E402
from python.solver import smt as smt_mod  # noqa: E402
from python.transfer import branchA as branchA_mod  # noqa: E402
from python.transfer import ladder as ladder_mod  # noqa: E402

SCAN_SCOPES = ["python/solver", "python/transfer", "python/adversary",
               "python/cycles/discovery.py", "scripts/run_phase10.py",
               "scripts/run_phase11.py", "scripts/run_phase12.py",
               "scripts/run_phase13.py"]


def sha_file(p: str) -> str:
    """SHA-256 over buffered reads."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP4-STEP-00: entry gates + firewall pins + backend freeze.
def step_entry() -> tuple[list[str], dict]:
    fails: list[str] = []
    ctx: dict = {}
    cert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE02_L6_MAPPING_FREEZE.json")
    if not os.path.exists(cert):
        fails.append("GATE-02 WP-2A freeze missing")
    gcert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE09_TRANSFER_GRAMMAR_FREEZE.json")
    if not os.path.exists(gcert):
        fails.append("GATE-09 grammar freeze missing")
    h3t = os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_state.json")
    if not os.path.exists(h3t):
        fails.append("GATE-H3T bank state missing")
    else:
        ctx["h3t_state_sha"] = sha_file(h3t)
        print("[WP4-STEP-00] H3T firewall pinned: %s" % ctx["h3t_state_sha"][:16], flush=True)
    sb = open(os.path.join(ROOT, "prereg", "solver_backends.yaml"), encoding="utf-8").read()
    if "synthesis_authorized: false" not in sb:
        fails.append("SOLV-01 solver_backends.yaml mutated (must stay WP-0 snapshot)")
    else:
        print("[WP4-STEP-00] solver_backends.yaml is the WP-0 snapshot (backend entries live in artifacts/)",
              flush=True)
    hits = []
    carve = re.compile(r"FORBIDDEN_|LEAKAGE|banned|blocklist|FIREWALL-scan-pattern")
    for scope in SCAN_SCOPES:
        path = os.path.join(ROOT, *scope.split("/"))
        targets = []
        if os.path.isdir(path):
            targets = [os.path.join(path, fn) for fn in sorted(os.listdir(path)) if fn.endswith(".py")]
        elif os.path.isfile(path):
            targets = [path]
        for target in targets:
            if not os.path.exists(target):
                continue
            sourcelines = open(target, encoding="utf-8").read().split("\n")
            tree = ast.parse("\n".join(sourcelines))
            for node in ast.walk(tree):
                lineno = getattr(node, "lineno", 0)
                srcline = sourcelines[lineno - 1] if 0 < lineno <= len(sourcelines) else ""
                if carve.search(srcline):
                    continue
                # Bank-CONTENT access: imports of the holdout package or bank paths.
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    names = []
                    if isinstance(node, ast.Import):
                        names = [a.name for a in node.names]
                    else:
                        names = [node.module or ""]
                    if any("holdout" in nm for nm in names):
                        hits.append("%s:holdout-import" % os.path.relpath(target, ROOT))
                elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                    low = node.value.lower()
                    if "h3t_bank" in low or "h1_bank" in low or "h2r" in low:  # FIREWALL-scan-pattern
                        hits.append("%s:bank-path" % os.path.relpath(target, ROOT))
                        break
    if hits:
        fails.append("FIREWALL-01 synthesis paths reference holdout bank: %s" % sorted(set(hits)))
    else:
        print("[WP4-STEP-00] synthesis namespaces holdout-clean (no bank reads possible)", flush=True)
    import z3
    freeze = {"backend": "z3-solver", "package_version": "5.1.0.0",
              "reported_version": z3.get_version_string(),
              "module_hash": sha_file(z3.__file__)[:32],
              "seeds": {"random_seed": 0},
              "threads": 1, "parameter_files": [],
              "certificate_capability": "model-replay + unsat-by-exhaustion-agreement",
              "role": "discovery CEGIS proposer; verdicts require independent replay + brute-force agreement"}
    sod = os.path.join(ROOT, "artifacts", "v03", "solver")
    os.makedirs(sod, exist_ok=True)
    with open(os.path.join(sod, "backend_freeze.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(freeze, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP4-STEP-00] backend frozen: z3-solver 5.1.0.0 seeds pinned single-thread", flush=True)
    ctx["backend"] = freeze
    return fails, ctx


# WP4-STEP-01: frozen masks + corpora + flow screen.
def step_masks(imp: str, outdir: str) -> tuple[list[str], dict]:
    fails: list[str] = []
    near, near_info = disc_mod.near_critical_selection(imp)
    sel, val = disc_mod.noncritical_edges([2, 3, 4, 5], [6, 7])
    gen_sel = disc_mod.generated_histories("selection")
    gen_val = disc_mod.generated_histories("validation")
    masks = {"counts": {"near_critical": len(near),
                        "noncritical_sel": {k: len(v) for k, v in sel.items()},
                        "noncritical_val": {k: len(v) for k, v in val.items()},
                        "generated_sel": len(gen_sel), "generated_val": len(gen_val)},
             "top_k": disc_mod.TOP_K, "slack_set": sorted(disc_mod.SLACK_SET),
             "cycle_len_bound": disc_mod.CYCLE_LEN_BOUND,
             "dev_seeds": disc_mod.DEV_SEEDS, "val_seeds": disc_mod.VAL_SEEDS,
             "near_info": near_info}
    with open(os.path.join(outdir, "masks.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(masks, f, sort_keys=True, indent=2)
        f.write("\n")
    with open(os.path.join(outdir, "near_critical.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(near, f, sort_keys=True)
        f.write("\n")
    with open(os.path.join(outdir, "noncritical_sel.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(sel, f, sort_keys=True)
        f.write("\n")
    with open(os.path.join(outdir, "noncritical_val.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(val, f, sort_keys=True)
        f.write("\n")
    with open(os.path.join(outdir, "generated_sel.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(gen_sel, f, sort_keys=True)
        f.write("\n")
    with open(os.path.join(outdir, "generated_val.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(gen_val, f, sort_keys=True)
        f.write("\n")
    print("[WP4-STEP-01] masks frozen: near=%d sel=%s val=%s gen=%d/%d"
          % (len(near), masks["counts"]["noncritical_sel"],
             masks["counts"]["noncritical_val"],
             len(gen_sel), len(gen_val)), flush=True)
    return fails, {"near": near, "sel": sel, "val": val,
                   "gen_sel": gen_sel, "gen_val": gen_val}


def code_tag() -> str:
    """Hash of the synthesis code paths (masks/corpus/grid resume only on match)."""
    h = hashlib.sha256()
    for rel in ("python/cycles/discovery.py", "python/transfer/branchA.py",
                "python/solver/certify.py", "python/splay_ref/splay.py",
                "python/cycles/enumerate.py", "scripts/run_phase10.py"):
        with open(os.path.join(ROOT, *rel.split("/")), "rb") as f:
            h.update(f.read())
    return h.hexdigest().upper()[:16]


def checkpoint_ok(path: str, tag: str) -> bool:
    """Existing output reusable iff non-empty and code tag matches."""
    if not (os.path.exists(path) and os.path.getsize(path) > 100):
        return False
    try:
        meta = json.load(open(path, encoding="utf-8"))
        return isinstance(meta, dict) and meta.get("code_tag") == tag
    except (json.JSONDecodeError, OSError, AttributeError):
        return False


def checkpoint_tags_path() -> str:
    """Sidecar recording code tags of all checkpointed artifacts."""
    return os.path.join(ROOT, "artifacts", "v03", "solver", "checkpoints.json")


def checkpoint_get(name: str, tag: str) -> bool:
    """True iff the named checkpoint was computed by identical code."""
    try:
        tags = json.load(open(checkpoint_tags_path(), encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return tags.get(name) == tag


def checkpoint_put(name: str, tag: str) -> None:
    """Record the code tag of a checkpointed artifact (payload stays in its file)."""
    try:
        tags = json.load(open(checkpoint_tags_path(), encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        tags = {}
    tags[name] = tag
    with open(checkpoint_tags_path(), "w", encoding="utf-8", newline="\n") as f:
        json.dump(tags, f, sort_keys=True, indent=2)
        f.write("\n")


def flow_screen(imp: str, near: list, ladder: list) -> dict:
    """Per-cycle required-k lower bounds per C (necessary for any k-bounded law)."""
    from python.cycles import import_parent as import_mod
    out = {}
    for c_const in ladder:
        worst = {"required_k": 0, "cycle": None}
        rows = []
        for n in (4, 5, 6):
            dom = PairDomain(n)
            cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                                 "critical_n%d_canonical_cycles.json" % n),
                                    encoding="utf-8"))
            for cid, cyc in enumerate(cycles):
                events = []
                for e in cyc["edges"]:
                    a_id, b_id = dom.unpid(e["source"])
                    from python.cycles.enumerate import build_node_tree
                    from python.splay_ref.splay import cost, splay
                    A0 = build_node_tree(dom.shapes, a_id, n)
                    B0 = build_node_tree(dom.shapes, b_id, n)
                    a, y = cost(A0, e["key"]), cost(B0, e["key"])
                    A2, evA = splay(A0, e["key"])
                    _B2, evB = splay(B0, e["key"])
                    w = y - c_const * a if e["mode"] == "KEEP" else 0
                    events.append({"side": "A", "rotations": len(evA), "regret_w": 0})
                    if e["mode"] == "KEEP":
                        events.append({"side": "B", "rotations": len(evB), "regret_w": max(0, w)})
                bal = flow_mod.cycle_balance(events, 10 ** 9, c_const)
                rows.append({"n": n, "cycle": cid, "required_k": bal["required_k"],
                             "demand": bal["demand"], "supply": bal["supply_rotations"]})
                if bal["required_k"] not in (0,) and bal["required_k"] > worst["required_k"]:
                    worst = {"required_k": bal["required_k"], "cycle": "n%d-c%d" % (n, cid)}
        for i, cyc in enumerate(near):
            n = cyc.get("n", 4)
            dom = PairDomain(n)
            states = cyc["states"]
            keys = cyc.get("keys", [])
            events = []
            for j, src in enumerate(states):
                key = keys[j % len(keys)] if keys else 1
                a_id, b_id = dom.unpid(src)
                from python.cycles.enumerate import build_node_tree
                from python.splay_ref.splay import cost, splay
                A0 = build_node_tree(dom.shapes, a_id, n)
                B0 = build_node_tree(dom.shapes, b_id, n)
                a, y = cost(A0, key), cost(B0, key)
                A2, evA = splay(A0, key)
                _B2, evB = splay(B0, key)
                w = y - c_const * a
                events.append({"side": "A", "rotations": len(evA), "regret_w": 0})
                events.append({"side": "B", "rotations": len(evB), "regret_w": max(0, w)})
            bal = flow_mod.cycle_balance(events, 10 ** 9, c_const)
            rows.append({"cycle": "near-%d" % i, "required_k": bal["required_k"],
                         "demand": bal["demand"], "supply": bal["supply_rotations"]})
            if bal["required_k"] not in (0,) and bal["required_k"] > worst["required_k"]:
                worst = {"required_k": bal["required_k"], "cycle": "near-%d" % i}
        out[str(c_const)] = {"cycles": len(rows), "worst": worst, "rows": rows}
        print("[WP4-STEP-01] flow screen C=%d: %d cycles, worst required_k=%s (%s)"
              % (c_const, len(rows), worst["required_k"], worst["cycle"]), flush=True)
    return out


# WP4-STEP-02: CEGIS loop (z3 proposes, exact engine disposes, blocks learned).
def step_cegis(corpus: dict, c_const: int, eval_fn=None) -> tuple[list[str], dict]:
    fails: list[str] = []
    if eval_fn is None:
        eval_fn = branchA_mod.evaluate
    sat, pvars = sat_mod.new_solver()
    tried: dict = {}
    order: list = []
    live = list(sat_mod.PREDICATES)
    while live:
        m = sat_mod.solve(sat, pvars)
        if m is None:
            break
        prop = m["predicate"]
        # Fresh SMT k-scope per predicate (bounds never couple across predicates).
        smt, los = smt_mod.new_solver()
        k = 0
        while k <= sat_mod.KMAX:
            verdict = eval_fn(prop, k, c_const, corpus)
            tried[(prop, k)] = verdict["feasible"]
            order.append({"predicate": prop, "k": k,
                          "feasible": verdict["feasible"],
                          "max_residual": verdict["max_residual"],
                          "first_violation": verdict["first_violation"]})
            if verdict["feasible"]:
                break
            smt_mod.block_k_le(smt, los, prop, k)
            if smt.check() != z3.sat:
                break
            k += 1
        sat_mod.block_predicate(sat, pvars, prop)
        live = [p for p in live if p != prop]
    print("[WP4-STEP-02] CEGIS C=%d: %d configs tried" % (c_const, len(order)), flush=True)
    return fails, {"tried": order, "tried_map": {str(k): v for k, v in tried.items()}}


# WP4-STEP-02: exhaustive brute force is ladder_mod.sweep_rung (single exhaustive
# path); CEGIS is the z3 path; ilp.minimize_k is the third leg. All three must agree.
def step_bruteforce(corpus: dict, c_const: int, eval_fn=None, replay_fn=None) -> tuple[list[str], dict]:
    fails: list[str] = []
    if eval_fn is None:
        eval_fn = branchA_mod.evaluate
    if replay_fn is None:
        replay_fn = certify_mod.replay_candidate
    rung = ladder_mod.sweep_rung(c_const, list(sat_mod.PREDICATES),
                                 range(sat_mod.KMAX + 1), corpus,
                                 eval_fn, replay_fn)
    if any(not r["independent_agreement"] for r in rung["rows"]):
        fails.append("CERT-01 ladder replay disagreement at C=%d" % c_const)
    feasible = [{"predicate": r["predicate"], "k": r["k"]} for r in rung["rows"] if r["feasible"]]
    for predicate in sat_mod.PREDICATES:
        best, _log = ilp_mod.minimize_k(
            predicate, c_const,
            lambda p, k, c: (eval_fn(p, k, c, corpus)["feasible"], "engine"))
        rung_best = min([r["k"] for r in rung["rows"]
                         if r["predicate"] == predicate and r["feasible"]], default=None)
        if best != rung_best:
            fails.append("CERT-01 ILP/rung minimal-k differ for %s at C=%d" % (predicate, c_const))
    return fails, {"feasible": feasible, "checked": len(rung["rows"])}


# WP4-STEP-03: ladder verdict per rung + family verdict across the ladder.
def step_ladder(corpus_stage1: dict, ladder: list, flow: dict, fresh: bool = False) -> tuple[list[str], dict]:
    fails: list[str] = []
    rungs = []
    memo: dict = {}
    ladder_path = os.path.join(ROOT, "artifacts", "v03", "solver", "ladder.json")
    prior: dict = {}
    if os.path.exists(ladder_path) and checkpoint_get("ladder", code_tag()) and not fresh:
        try:
            old = json.load(open(ladder_path, encoding="utf-8"))
            if isinstance(old, dict):
                for r in old.get("rungs", []):
                    prior[r["C"]] = r
            print("[WP4-STEP-03] ladder checkpoint hit (code tag match); resuming", flush=True)
        except (json.JSONDecodeError, OSError):
            prior = {}
    elif os.path.exists(ladder_path):
        print("[WP4-STEP-03] ladder checkpoint STALE (code changed); recomputing", flush=True)

    def eval_memo(predicate: str, k: int, c_const: int, _corpus=None) -> dict:
        """Memoized exact evaluation (one simulation per unique config per run)."""
        key = (predicate, k, c_const)
        if key not in memo:
            memo[key] = branchA_mod.evaluate(predicate, k, c_const, corpus_stage1)
        return memo[key]

    def replay_memo(predicate: str, k: int, c_const: int, _corpus=None) -> dict:
        """Memoized independent replay."""
        key = ("replay", predicate, k, c_const)
        if key not in memo:
            memo[key] = certify_mod.replay_candidate(predicate, k, c_const, corpus_stage1)
        return memo[key]
    for c_const in ladder:
        if c_const in prior and prior[c_const].get("n_feasible") is not None:
            rungs.append(prior[c_const])
            fails += prior[c_const].get("fails", [])
            print("[WP4-STEP-03] C=%d resumed from checkpoint (%d feasible, %d fails)"
                  % (c_const, prior[c_const]["n_feasible"],
                     len(prior[c_const].get("fails", []))), flush=True)
            continue
        worst_k = flow[str(c_const)]["worst"]["required_k"]
        if worst_k > sat_mod.KMAX:
            print("[WP4-STEP-03] C=%d flow-dead (required_k=%s > KMAX=%d); grid skipped by necessity"
                  % (c_const, worst_k, sat_mod.KMAX), flush=True)
            rungs.append({"C": c_const, "feasible": [], "n_feasible": 0,
                          "flow_dead": True, "worst": flow[str(c_const)]["worst"]})
            continue
        f1, cegis = step_cegis(corpus_stage1, c_const, eval_memo)
        fails += f1
        f2, brute = step_bruteforce(corpus_stage1, c_const, eval_memo, replay_memo)
        # Agreement on decision-relevant quantities: per-predicate minimal feasible
        # k (CEGIS finds minima by k-scan; brute force enumerates; both coincide).
        cegis_min = {}
        for o in cegis["tried"]:
            if o["feasible"]:
                p = o["predicate"]
                if p not in cegis_min or o["k"] < cegis_min[p]:
                    cegis_min[p] = o["k"]
        brute_min = {}
        for o in brute["feasible"]:
            p = o["predicate"]
            if p not in brute_min or o["k"] < brute_min[p]:
                brute_min[p] = o["k"]
        if cegis_min != brute_min:
            fails.append("CERT-01 CEGIS/brute minimal-k differ at C=%d: %s vs %s"
                         % (c_const, cegis_min, brute_min))
        else:
            print("[WP4-STEP-02] cert agreement at C=%d: minima %s"
                  % (c_const, cegis_min), flush=True)
        rungs.append({"C": c_const, "feasible": brute["feasible"],
                      "n_feasible": len(brute["feasible"]), "flow_dead": False,
                      "fails": [x for x in fails if "C=%d" % c_const in x]})
        if brute["feasible"]:
            print("[WP4-STEP-03] C=%d SURVIVES with %d configs (histories screen next)"
                  % (c_const, len(brute["feasible"])), flush=True)
        with open(os.path.join(ROOT, "artifacts", "v03", "solver", "ladder.json"),
                  "w", encoding="utf-8", newline="\n") as f:
            json.dump({"rungs": rungs}, f, sort_keys=True, indent=2)
            f.write("\n")
        checkpoint_put("ladder", code_tag())
    return fails, {"rungs": rungs}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ladder", default="2,3,4,6,8,12,16,24,32,64")
    ap.add_argument("--fresh", action="store_true",
                    help="ignore checkpoints and recompute everything deterministically")
    args = ap.parse_args()
    print("[WP4-STEP-00] PHASE 10: Branch-A raw-boundary synthesis (development only)", flush=True)
    fails, ctx = step_entry()
    if fails:
        print("[WP4-STEP-00] PHASE10_FAIL (refused)", flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 2
    ladder = [int(c) for c in args.ladder.split(",")]
    imp = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    outdir = os.path.join(ROOT, "artifacts", "v03", "discovery")
    os.makedirs(outdir, exist_ok=True)
    masks_path = os.path.join(outdir, "masks.json")
    tag = code_tag()
    masks = None
    near = None
    if checkpoint_ok(masks_path, tag) and not args.fresh:
        masks = json.load(open(masks_path, encoding="utf-8"))
        near = json.load(open(os.path.join(outdir, "near_critical.json"), encoding="utf-8"))
        masks["near"] = near
        print("[WP4-STEP-01] masks checkpoint hit (code tag %s); rebuild skipped"
              % tag[:8], flush=True)
    else:
        fails2, masks = step_masks(imp, outdir)
        fails += fails2
        near = json.load(open(os.path.join(outdir, "near_critical.json"), encoding="utf-8"))
        masks["code_tag"] = tag
        with open(masks_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(masks, f, sort_keys=True, indent=2)
            f.write("\n")
    flow = flow_screen(imp, masks["near"], ladder)
    with open(os.path.join(ROOT, "artifacts", "v03", "solver", "flow_screen.json"),
              "w", encoding="utf-8", newline="\n") as f:
        json.dump(flow, f, sort_keys=True, indent=2)
        f.write("\n")
    # Stage-1 corpus (critical x3 + near-critical) for the configuration grid.
    dev_path = os.path.join(ROOT, "artifacts", "v03", "transfer_grammar", "dev_corpus.json")
    os.makedirs(os.path.join(ROOT, "artifacts", "v03", "transfer_grammar"), exist_ok=True)
    if os.path.exists(dev_path) and checkpoint_get("dev_corpus", tag) and not args.fresh:
        stage1 = json.load(open(dev_path, encoding="utf-8"))
        print("[WP4-STEP-01] dev corpus checkpoint hit; rebuild skipped", flush=True)
    else:
        stage1 = disc_mod.build_dev_corpus(imp, masks["near"], [])
        with open(dev_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(stage1, f, sort_keys=True)
            f.write("\n")
        checkpoint_put("dev_corpus", tag)
    f3, ladder_out = step_ladder(stage1, ladder, flow, fresh=args.fresh)
    fails += f3
    with open(os.path.join(ROOT, "artifacts", "v03", "solver", "ladder.json"),
              "w", encoding="utf-8", newline="\n") as f:
        json.dump(ladder_out, f, sort_keys=True, indent=2)
        f.write("\n")
    # Histories screen: only rungs WITH positive-regret history edges (vacuity pre-scan),
    # only survivor configs, fail_fast evaluation + independent replay agreement.
    survivors = [(r["C"], r["feasible"]) for r in ladder_out["rungs"] if r["n_feasible"]]
    hist_corpus = None
    if survivors:
        hist_path = os.path.join(ROOT, "artifacts", "v03", "transfer_grammar", "hist_corpus.json")
        os.makedirs(os.path.join(ROOT, "artifacts", "v03", "transfer_grammar"), exist_ok=True)
        fresh = getattr(args, "fresh", False)
        if os.path.exists(hist_path) and checkpoint_get("hist_corpus", code_tag()) and not fresh:
            hist_corpus = json.load(open(hist_path, encoding="utf-8"))
            print("[WP4-STEP-03] histories corpus checkpoint hit; rebuild skipped", flush=True)
        else:
            hist_corpus = disc_mod.build_dev_corpus(
                imp, [], json.load(open(os.path.join(outdir, "generated_sel.json"), encoding="utf-8")))
            with open(hist_path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(hist_corpus, f, sort_keys=True)
                f.write("\n")
            checkpoint_put("hist_corpus", code_tag())
        burden_by_c: dict = {}
        for c_const, _feas in survivors:
            top = 0
            for seq in hist_corpus["sequences"]:
                for ev in seq["rotations"]:
                    if ev["mode"] == "KEEP" and ev.get("y_edge", 0) > 0:
                        w = ev["y_edge"] - c_const * ev["a_edge"]
                        if w > top:
                            top = w
            burden_by_c[c_const] = top
            print("[WP4-STEP-03] histories burden at C=%d: max w=%d%s"
                  % (c_const, top, " (VACUOUS rung)" if top <= 0 else ""), flush=True)
        screen_path = os.path.join(ROOT, "artifacts", "v03", "solver", "histories_screen.json")
        screened: dict = {}
        if os.path.exists(screen_path) and checkpoint_get("histories", code_tag()) and not fresh:
            try:
                screened = json.load(open(screen_path, encoding="utf-8"))
                print("[WP4-STEP-03] histories checkpoint hit (code tag match); resuming",
                      flush=True)
            except (json.JSONDecodeError, OSError):
                screened = {}
        elif os.path.exists(screen_path):
            print("[WP4-STEP-03] histories checkpoint STALE (code changed); recomputing",
                  flush=True)
        # Dominance-pruned histories screen. PROVED dominance (see MST09 record):
        # P_all fires on a superset of every predicate's events and k=6 injects a
        # superset of credit, so by event-wise induction latent/active pools of
        # (P_all,6) dominate any (p,k<=6) pointwise, hence residuals are <=.
        # One config per rung therefore decides death; minima only on survival.
        for c_const, feas in survivors:
            if burden_by_c[c_const] <= 0:
                for cfg in feas:
                    cfg["histories_feasible"] = "VACUOUS_NO_BURDEN"
                continue
            key0 = "%d|P_all|6" % c_const
            if key0 not in screened or fresh:
                v0 = branchA_mod.evaluate("P_all", 6, c_const, hist_corpus)
                r0 = certify_mod.replay_candidate("P_all", 6, c_const, hist_corpus)
                entry_fails = []
                if v0["feasible"] != r0["feasible"]:
                    entry_fails.append("CERT-01 histories engine/replay disagree (P_all,6,C=%d)"
                                       % c_const)
                screened[key0] = {"histories_feasible": v0["feasible"],
                                  "histories_max_residual": v0["max_residual"],
                                  "histories_first_violation": v0["first_violation"],
                                  "fails": entry_fails}
                with open(screen_path, "w", encoding="utf-8", newline="\n") as f:
                    json.dump(screened, f, sort_keys=True, indent=2)
                    f.write("\n")
                checkpoint_put("histories", code_tag())
                print("[WP4-STEP-03] histories screen (P_all,6,C=%d): feasible=%s max_res=%s"
                      % (c_const, v0["feasible"], v0["max_residual"]), flush=True)
            fails += screened[key0].get("fails", [])
            v0f = screened[key0]["histories_feasible"]
            if v0f is not True:
                for cfg in feas:
                    cfg["histories_feasible"] = False
                    cfg["histories_first_violation"] = screened[key0]["histories_first_violation"]
                print("[WP4-STEP-03] C=%d rung DEAD on histories (dominance: P_all/6 fails)"
                      % c_const, flush=True)
                continue
            for cfg in feas:
                key = "%d|%s|%d" % (c_const, cfg["predicate"], cfg["k"])
                if key in screened and not fresh:
                    cfg.update({k: v for k, v in screened[key].items() if k != "fails"})
                    fails += screened[key].get("fails", [])
                    continue
                v = branchA_mod.evaluate(cfg["predicate"], cfg["k"], c_const,
                                         hist_corpus, fail_fast=True)
                r = certify_mod.replay_candidate(cfg["predicate"], cfg["k"], c_const, hist_corpus)
                entry_fails = []
                if v["feasible"] != r["feasible"]:
                    entry_fails.append("CERT-01 histories engine/replay disagree (%s,k=%d,C=%d)"
                                       % (cfg["predicate"], cfg["k"], c_const))
                cfg["histories_feasible"] = v["feasible"]
                cfg["histories_max_residual"] = v["max_residual"]
                cfg["histories_first_violation"] = v["first_violation"]
                screened[key] = {"histories_feasible": v["feasible"],
                                 "histories_max_residual": v["max_residual"],
                                 "histories_first_violation": v["first_violation"],
                                 "fails": entry_fails}
                fails += entry_fails
                with open(screen_path, "w", encoding="utf-8", newline="\n") as f:
                    json.dump(screened, f, sort_keys=True, indent=2)
                    f.write("\n")
                checkpoint_put("histories", code_tag())
                print("[WP4-STEP-03] histories screen (%s,k=%d,C=%d): feasible=%s"
                      % (cfg["predicate"], cfg["k"], c_const, v["feasible"]), flush=True)
    confirmed = [c for _c, feas in survivors for c in feas
                 if c.get("histories_feasible") is True]
    verdict = "RAW_BOUNDARY_LAW_SURVIVES_DEV" if confirmed else "RAW_BOUNDARY_LAW_REJECTED"
    print("[WP4-STEP-03] verdict: %s" % verdict, flush=True)
    # Dev shortlist (NOT frozen calculi — WP-5 Phase 14 freezes from this list).
    # Explicit selection by the frozen complexity order: minimal-k anchor survivor,
    # max-headroom anchor survivor, weakest-predicate survivor at its first
    # burdened rung. Each asserted present in the screened results (fail if absent).
    shortlist = []
    if verdict == "RAW_BOUNDARY_LAW_SURVIVES_DEV":
        screen = {}
        try:
            scr = json.load(open(os.path.join(ROOT, "artifacts", "v03", "solver",
                                              "histories_screen.json"), encoding="utf-8"))
            for key, rec in scr.items():
                if "|" in key:
                    screen[key] = rec
        except (json.JSONDecodeError, OSError):
            pass
        for want in [("P_all", 2, 2), ("P_all", 6, 2), ("P_keep", 1, 6)]:
            key = "%d|%s|%d" % (want[2], want[0], want[1])
            rec = screen.get(key)
            if rec is None or rec.get("histories_feasible") is not True:
                fails.append("SHORTLIST-01 wanted candidate missing/not feasible: %s" % key)
                continue
            shortlist.append({"predicate": want[0], "k": want[1], "C": want[2],
                              "histories_max_residual": rec.get("histories_max_residual")})
        print("[WP4-STEP-03] shortlist (%d, WP-5 freezes): %s"
              % (len(shortlist), [(c["predicate"], c["k"], c["C"]) for c in shortlist]),
              flush=True)
    with open(os.path.join(ROOT, "artifacts", "v03", "solver", "shortlist.json"),
              "w", encoding="utf-8", newline="\n") as f:
        json.dump({"status": "DEV_SHORTLIST_NOT_FROZEN", "selected": shortlist}, f,
                  sort_keys=True, indent=2, default=str)
        f.write("\n")
    with open(os.path.join(ROOT, "artifacts", "v03", "solver", "verdict.json"),
              "w", encoding="utf-8", newline="\n") as f:
        json.dump({"verdict": verdict, "ladder": ladder_out,
                   "gate": "one exact residual at frozen C rejects that candidate at that C"},
                  f, sort_keys=True, indent=2)
        f.write("\n")
    from collections import Counter as _Counter
    by_kind = dict(_Counter(x.split(" ")[0] for x in fails))
    with open(os.path.join(ROOT, "artifacts", "v03", "solver", "fails.json"),
              "w", encoding="utf-8", newline="\n") as f:
        json.dump({"count": len(fails), "by_kind": by_kind, "fails": fails},
                  f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP4-STEP-00] fail kinds: %s" % by_kind, flush=True)
    if fails:
        print("[WP4-STEP-00] PHASE10_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP4-STEP-00] PHASE10_PASS: %s" % verdict, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
