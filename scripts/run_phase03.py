"""Spec PHASE 03 runner (REAL): rotation-trace certification + expansion mechanics.

Requires run_phase01 outputs (import ledger, replay). Steps: WP1-STEP-04 rotation
verification (dual-core agreement on every imported corpus edge, reference-snapshot
determinism, block-partition exact-once coverage), WP1-STEP-05 expansion of all
imported critical cycles to A/B rotation traces + circulation tables (prerequisite
artifacts for WP-2-owned Phase 04 science). Emits ROTATION_TRACE_CERTIFIED
(mechanics scope; MST0-02/04 theorem reviews remain pending human verdicts).
Console lines prefixed [WP1-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.audit import log as log_mod  # noqa: E402
from python.cycles import expand as expand_mod  # noqa: E402
from python.cycles import circulation as circ_mod  # noqa: E402
from python.cycles.enumerate import PairDomain  # noqa: E402
from python.rotations import agree as agree_mod  # noqa: E402
from python.rotations import blocks as blocks_mod  # noqa: E402
from python.rotations import corpus as corpus_mod  # noqa: E402
from python.rotations import independent_trace as indep_trace_mod  # noqa: E402
from python.rotations import reference as ref_mod  # noqa: E402
from python.rotations import trace as trace_mod  # noqa: E402
from python.splay_ref import independent as I  # noqa: E402
from python.splay_ref.splay import build_balanced, search_path  # noqa: E402


# WP1-STEP-04: full-tuple dual-core agreement on every imported corpus edge.
def step_rotation_verification(imp: str, sizes: list[int]) -> tuple[list[str], dict]:
    fails: list[str] = []
    checked = 0
    seen_edge_ids: set = set()
    corpus: dict[int, list] = {n: [] for n in sizes}
    for n in sizes:
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        for cid, cyc in enumerate(cycles):
            for i, e in enumerate(cyc["edges"]):
                # WP-1 REPAIR STEP E1: canonical edge identity (§5.5, F8).
                edge_id = dom.edge_id(e["source"], "KEEP", e["key"])
                if edge_id in seen_edge_ids:
                    fails.append("EDGE-ID %s not unique" % edge_id)
                seen_edge_ids.add(edge_id)
                a_id, b_id = dom.unpid(e["source"])
                A = build_node_tree_outer(dom, a_id, n)
                B = build_node_tree_outer(dom, b_id, n)
                pathA = search_path(A, e["key"])
                pathB = search_path(B, e["key"])
                # WP-1 REPAIR STEP T6: every certified trace routes through the
                # trace-owned validator (fail-closed inside trace.py).
                try:
                    t1 = trace_mod.certify_keep(A, B, e["key"], edge_id)
                except ValueError as ex:
                    fails.append("TRACE-CERTIFY %s: %s" % (edge_id, ex))
                    continue
                # Independent core on structurally identical trees.
                A2 = build_node_tree_outer(dom, a_id, n)
                B2 = build_node_tree_outer(dom, b_id, n)
                stA, stB = I.from_nodes(A2), I.from_nodes(B2)
                pathA2 = I.path2(stA, e["key"])
                pathB2 = I.path2(stB, e["key"])
                a2, y2 = I.cost2(stA, e["key"]), I.cost2(stB, e["key"])
                evA, evB = I.splay2(stA, e["key"]), I.splay2(stB, e["key"])
                # ROT-02 (true meaning): search paths exact on both sides.
                if pathA != pathA2 or pathB != pathB2:
                    fails.append("ROT-02 %s search-path mismatch" % edge_id)
                # ROT-12 component: cross-core cost equality (convention held).
                if a2 != t1["a"] or y2 != t1["y"]:
                    fails.append("ROT-12 %s cost mismatch" % edge_id)
                # ROT-10 full tuple via the shared checker (single source).
                for desc in agree_mod.compare(t1["events"], evA, evB, edge_id):
                    fails.append("ROT-10 " + desc)
                if I.serialize2(stA) != t1["A1"] or I.serialize2(stB) != t1["B1"]:
                    fails.append("ROT-01 %s final-tree mismatch" % edge_id)
                if len(t1["reference_snapshot_hash"]) != 64:
                    fails.append("ROT-11 %s snapshot malformed" % edge_id)
                # WP-1 REPAIR STEP S5: independent serializer end-to-end bytes.
                stA3 = I.from_nodes(build_node_tree_outer(dom, a_id, n))
                stB3 = I.from_nodes(build_node_tree_outer(dom, b_id, n))
                a3, y3 = I.cost2(stA3, e["key"]), I.cost2(stB3, e["key"])
                t2 = indep_trace_mod.trace_keep_independent(
                    stA3, stB3, e["key"], edge_id, a3, y3, ref_mod.CONVENTION)
                for desc in indep_trace_mod.compare_canonical(t1, t2, edge_id):
                    fails.append("ROT-10-serializer " + desc)
                corpus[n].append({"edge_id": edge_id, "n": n, "cycle": cid,
                                  "edge_index": i, "key": e["key"], "mode": "KEEP",
                                  "source": e["source"], "a": t1["a"], "y": t1["y"],
                                  "convention": t1["convention"],
                                  "reference_snapshot_hash": t1["reference_snapshot_hash"],
                                  "A_path": pathA, "B_path": pathB,
                                  "A1": t1["A1"], "B1": t1["B1"],
                                  "events": t1["events"]})
                checked += 1
    print("[WP1-STEP-04] dual-core agreement on %d corpus edges (paths+costs+full-tuple+trees+serializer)" % checked,
          flush=True)
    # Reference determinism: same KEEP twice gives identical snapshot + event stream.
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t1 = trace_mod.trace_keep(A, B, 3, "det-a")
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t2 = trace_mod.trace_keep(A, B, 3, "det-b")
    if t1["reference_snapshot_hash"] != t2["reference_snapshot_hash"]:
        fails.append("ROT-11 reference snapshot not deterministic")
    elif [ev["splay_case"] for ev in t1["events"]] != [ev["splay_case"] for ev in t2["events"]]:
        fails.append("ROT-11 event stream not deterministic")
    else:
        print("[WP1-STEP-04] reference snapshot deterministic; convention %s"
              % ref_mod.CONVENTION, flush=True)
    # Block partition exact-once coverage on synthetic histories (incl. empty/edge cases).
    cases = [[], [{"mode": "KEEP", "x": 1}],
             [{"mode": "DELETE", "x": 1}, {"mode": "DELETE", "x": 2},
              {"mode": "KEEP", "x": 1}, {"mode": "KEEP", "x": 3},
              {"mode": "DELETE", "x": 2}, {"mode": "KEEP", "x": 1}]]
    for h in cases:
        bl = blocks_mod.partition(h)
        if not blocks_mod.check_coverage(h, bl):
            fails.append("BLOCK-01 partition coverage failed for %s" % h)
    # Determinism of partition itself.
    h = cases[2]
    if blocks_mod.partition(h) != blocks_mod.partition([dict(z) for z in h]):
        fails.append("BLOCK-02 partition not a pure function of history")
    else:
        print("[WP1-STEP-04] block partition exact-once on %d histories" % len(cases), flush=True)
    if not fails:
        print("[WP1-STEP-04] rotation core verified (dual-core agreement via foundation suite)", flush=True)
    return fails, corpus


def build_node_tree_outer(dom: PairDomain, idx: int, n: int):
    """Fresh pointer tree for tree_id (import here to keep runner dependency-light)."""
    from python.cycles.enumerate import build_node_tree
    return build_node_tree(dom.shapes, idx, n)


def sha_file(p: str) -> str:
    """SHA-256 over buffered reads."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP1-STEP-04b: persist the agreement corpus (sharded zst + manifest + bundle).
def step_write_corpus(corpus: dict) -> dict:
    outdir = os.path.join(ROOT, "artifacts", "v03", "rotations")
    os.makedirs(outdir, exist_ok=True)
    shards = {}
    for n in sorted(corpus):
        payload = {"n": n, "convention": ref_mod.CONVENTION, "traces": corpus[n]}
        rec = corpus_mod.write_shard(outdir, "traces_n%d" % n, payload)
        rec["traces"] = len(corpus[n])
        shards[str(n)] = rec
    manifest = {"shards": shards, "logical_stream": corpus_mod.logical_stream(shards),
                "convention": ref_mod.CONVENTION,
                "n_traces": sum(len(v) for v in corpus.values())}
    with open(os.path.join(outdir, "rotations_manifest.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, sort_keys=True, indent=2)
        f.write("\n")
    # WP-1 REPAIR STEP C4: rotations manifest + MST02 bundle sealed to hashes.
    print("[WP-1][REPAIR STEP C4] rotations manifest logical=%s..."
          % manifest["logical_stream"][:16], flush=True)
    proof_path = os.path.join(ROOT, "math", "theorem_MST02_rotation_refinement.md")
    bundle = {"obligation": "MST0-02",
              "theorem_doc": "math/theorem_MST02_rotation_refinement.md",
              "theorem_sha256": sha_file(proof_path),
              "review_record": "math/reviews/MST0-02.review.json",
              "corpus_manifest": "artifacts/v03/rotations/rotations_manifest.json",
              "corpus_manifest_sha256": sha_file(os.path.join(
                  outdir, "rotations_manifest.json")),
              "gate": "ROTATION_TRACE_CERTIFIED (mechanics scope)"}
    with open(os.path.join(outdir, "MST02_proof_bundle.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(bundle, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP1-STEP-04] corpus persisted: %d traces, logical=%s..."
          % (manifest["n_traces"], manifest["logical_stream"][:16]), flush=True)
    return manifest


# WP-1 REPAIR STEP E4: one expansion task (parallel-safe, fresh domain).
def _expand_task(task: tuple) -> tuple:
    """Expand a single cycle; return (canonical_key, expanded, table)."""
    n, cid, cyc, p, q = task
    dom = PairDomain(n)
    ex = expand_mod.expand_cycle(dom, n, cid, cyc)
    table = circ_mod.circulate(ex, p, q)
    return (expand_mod.canonical_key(n, cyc, cid), ex, table)


# WP-1 REPAIR STEP E5: mutant gate — probes must pass before certification.
def step_mutant_gate() -> list[str]:
    """Run the WP-1 rotation mutants; any escape blocks certification (§21)."""
    from python.rotations import mutate as mutate_mod
    fails: list[str] = []
    for name, fn in (("case-label", mutate_mod.case_label_probe),
                     ("canonical-ordering", mutate_mod.order_probe),
                     ("snapshot-order", mutate_mod.snapshot_probe)):
        try:
            baseline_ok, mutant_caught = fn()
        except Exception as e:  # noqa: BLE001 - probe crash blocks certification
            fails.append("MUTANT-GATE %s probe crashed: %s" % (name, type(e).__name__))
            continue
        if not baseline_ok:
            fails.append("MUTANT-GATE %s baseline failed" % name)
        if not mutant_caught:
            fails.append("MUTANT-GATE %s mutant escaped" % name)
    if not fails:
        print("[WP1-STEP-04] mutant gate: 3/3 probes (baseline pass, mutant caught)",
              flush=True)
    return fails


# WP1-STEP-05: expand all imported cycles (prerequisite mechanics for WP-2 science).
def step_expand(imp: str, outdir: str, sizes: list[int], b_map: dict) -> tuple[list[str], dict]:
    fails: list[str] = []
    os.makedirs(outdir, exist_ok=True)
    from concurrent.futures import ThreadPoolExecutor
    tasks = []
    for n in sizes:
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        p, q = b_map[n]
        for cid, cyc in enumerate(cycles):
            tasks.append((n, cid, cyc, p, q))
    # WP-1 REPAIR STEP E6: parallel over cycles with sorted reduce (§9.4 order).
    with ThreadPoolExecutor(max_workers=8) as pool:
        done = list(pool.map(_expand_task, tasks))
    done.sort(key=lambda t: t[0])
    by_n: dict[int, list] = {n: [] for n in sizes}
    for key, ex, table in done:
        if not ex["closed"]:
            fails.append("EXPAND-01 n=%d cycle=%d did not close" % (ex["n"], ex["cycle_index"]))
        by_n[ex["n"]].append((ex, table))
    shards = {}
    for n in sizes:
        p, q = b_map[n]
        expanded = [ex for ex, _t in by_n[n]]
        table = [_t for _ex, _t in by_n[n]]
        payload = {"n": n, "b": [p, q], "cycles": expanded, "circulation": table,
                   "order": "canonical [n, source_state_id, cycle_length, key_word_lex]"}
        blob = json.dumps(payload, sort_keys=True)
        plain_path = os.path.join(outdir, "expanded_n%d.json" % n)
        with open(plain_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(blob + "\n")
        # NOTE: digest covers the exact landed bytes (trailing newline
        # included); hashing the pre-newline string would mismatch the file.
        digest = sha_file(plain_path)
        rec = corpus_mod.write_shard(outdir, "expanded_n%d" % n, payload)
        rec["json"] = "expanded_n%d.json" % n
        rec["cycles"] = len(expanded)
        rec["sha256_json"] = digest
        shards[str(n)] = rec
        print("[WP1-STEP-05] n=%d expanded %d cycles sha=%s..."
              % (n, len(expanded), digest[:16]), flush=True)
    manifest = {"shards": shards, "logical_stream": corpus_mod.logical_stream(shards)}
    with open(os.path.join(outdir, "expanded_manifest.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, sort_keys=True, indent=2)
        f.write("\n")
    # WP-1 REPAIR STEP C4: expansion manifest sealed to shard hashes.
    print("[WP-1][REPAIR STEP C4] expanded manifest logical=%s..."
          % manifest["logical_stream"][:16], flush=True)
    print("[WP1-STEP-05] expansion manifest: logical=%s..."
          % manifest["logical_stream"][:16], flush=True)
    return fails, manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="2,3,4,5,6,7")
    args = ap.parse_args()
    logdir = os.path.join(ROOT, "artifacts", "v03", "logs")
    # WP-1 REPAIR STEP L5: capture both streams, hash after close (§27).
    with log_mod.capture(logdir, "phase03") as cap:
        exit_code, rec = _run(args)
    streams = cap.hashes()
    rec["stdout_hash"] = streams["stdout_hash"]
    rec["stderr_hash"] = streams["stderr_hash"]
    # WP-1 REPAIR STEP L3: append the §27 execution record (fail-closed fields).
    log_mod.write_log(os.path.join(ROOT, "artifacts", "v03", "logs", "phase03_wp1.jsonl"), rec)
    print("[WP1-STEP-00] §27 record appended (phase03_wp1.jsonl)", flush=True)
    if exit_code:
        print("[WP1-STEP-00] PHASE03_FAIL (see record)", flush=True)
        return 1
    print("[WP1-STEP-00] ROTATION_TRACE_CERTIFIED (mechanics scope; MST0-02/04 reviews pending human)", flush=True)
    return 0


def _run(args) -> tuple[int, dict]:
    import time as _time
    import tracemalloc as _tracemalloc
    _tracemalloc.start()
    _t0 = _time.perf_counter()
    print("[WP1-STEP-00] PHASE 03: rotation verification + expansion mechanics", flush=True)
    imp = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    rec = log_mod.static_fields(ROOT)
    rec.update({
        "phase": "03", "branch": "WP-1", "command": sys.argv,
        "stdout_hash": None, "stderr_hash": None,
        "allocator_peak_bytes": None,
    })
    if not os.path.exists(os.path.join(imp, "replay.json")):
        print("[WP1-STEP-00] PHASE03_FAIL: run_phase01 outputs missing", flush=True)
        rec.update({"scientific_status": "PHASE03_FAIL",
                    "input_hashes": {}, "output_hashes": {},
                    "wall_s": round(_time.perf_counter() - _t0, 2),
                    "exit_code": 1})
        _tracemalloc.stop()
        return 1, rec
    sizes = [int(s) for s in args.sizes.split(",")]
    fails: list[str] = []
    fails_ver, corpus = step_rotation_verification(imp, sizes)
    fails += fails_ver
    fact = json.load(open(os.path.join(imp, "v02baseline", "v02", "fact_table.json"),
                          encoding="utf-8"))
    b_map = {row["n"]: (int(row["b"][0]), int(row["b"][1])) for row in fact}
    fails_exp, manifest = step_expand(imp, os.path.join(ROOT, "artifacts", "v03", "cycles", "expanded"),
                                      sizes, b_map)
    fails += fails_exp
    corpus_manifest = step_write_corpus(corpus) if not fails else {}
    # WP-1 REPAIR STEP E7: §21 order — mutants run BEFORE certification status.
    fails += step_mutant_gate()
    exit_code = 1 if fails else 0
    # WP1-STEP-00: §27 execution record (append-only; fullest honest field set).
    rec.update({
        "scientific_status": "ROTATION_TRACE_CERTIFIED" if not fails else "PHASE03_FAIL",
        "input_hashes": log_mod.hash_outputs(ROOT, ["artifacts/v03/parent_import"]),
        "output_hashes": log_mod.hash_outputs(ROOT, ["artifacts/v03/cycles/expanded",
                                                     "artifacts/v03/rotations"]),
        "wall_s": round(_time.perf_counter() - _t0, 2),
        "allocator_peak_bytes": _tracemalloc.get_traced_memory()[1],
        "exit_code": exit_code,
    })
    _tracemalloc.stop()
    for x in fails:
        print(" -", x, flush=True)
    return exit_code, rec


if __name__ == "__main__":
    sys.exit(main())
