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
from python.rotations import reference as ref_mod  # noqa: E402
from python.rotations.trace import trace_keep  # noqa: E402
from python.splay_ref import independent as I  # noqa: E402
from python.splay_ref.splay import build_balanced, search_path  # noqa: E402


# WP1-STEP-04: dual-core agreement on every imported corpus edge + convention checks.
def step_rotation_verification(imp: str, sizes: list[int]) -> tuple[list[str], dict]:
    fails: list[str] = []
    checked = 0
    corpus: dict[int, list] = {n: [] for n in sizes}
    for n in sizes:
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        for cid, cyc in enumerate(cycles):
            for i, e in enumerate(cyc["edges"]):
                a_id, b_id = dom.unpid(e["source"])
                A = build_node_tree_outer(dom, a_id, n)
                B = build_node_tree_outer(dom, b_id, n)
                pathA = search_path(A, e["key"])
                pathB = search_path(B, e["key"])
                t1 = trace_keep(A, B, e["key"], "agree-%d-%d-%d" % (n, cid, i))
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
                    fails.append("ROT-02 n=%d c=%d e=%d search-path mismatch" % (n, cid, i))
                # ROT-12 component: cross-core cost equality (convention held).
                if a2 != t1["a"] or y2 != t1["y"]:
                    fails.append("ROT-12 n=%d c=%d e=%d cost mismatch" % (n, cid, i))
                # ROT-10 full tuple via the shared checker (single source).
                for desc in agree_mod.compare(t1["events"], evA, evB,
                                              "n=%d c=%d e=%d" % (n, cid, i)):
                    fails.append("ROT-10 " + desc)
                if I.serialize2(stA) != t1["A1"] or I.serialize2(stB) != t1["B1"]:
                    fails.append("ROT-01 n=%d c=%d e=%d final-tree mismatch" % (n, cid, i))
                if len(t1["reference_snapshot_hash"]) != 64:
                    fails.append("ROT-11 n=%d c=%d e=%d snapshot malformed" % (n, cid, i))
                corpus[n].append({"n": n, "cycle": cid, "edge_index": i,
                                  "key": e["key"], "mode": "KEEP",
                                  "source": e["source"], "a": t1["a"], "y": t1["y"],
                                  "convention": t1["convention"],
                                  "reference_snapshot_hash": t1["reference_snapshot_hash"],
                                  "A_path": pathA, "B_path": pathB,
                                  "A1": t1["A1"], "B1": t1["B1"],
                                  "events": t1["events"]})
                checked += 1
    print("[WP1-STEP-04] dual-core agreement on %d corpus edges (paths+costs+full-tuple+trees)" % checked,
          flush=True)
    # Reference determinism: same KEEP twice gives identical snapshot + event stream.
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t1 = trace_keep(A, B, 3, "det-a")
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t2 = trace_keep(A, B, 3, "det-b")
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


# WP1-STEP-05: expand all imported cycles (prerequisite mechanics for WP-2 science).
def step_expand(imp: str, outdir: str, sizes: list[int], b_map: dict) -> tuple[list[str], dict]:
    fails: list[str] = []
    os.makedirs(outdir, exist_ok=True)
    shards = {}
    for n in sizes:
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        p, q = b_map[n]
        expanded = []
        table = []
        for cid, cyc in enumerate(cycles):
            ex = expand_mod.expand_cycle(dom, n, cid, cyc)
            if not ex["closed"]:
                fails.append("EXPAND-01 n=%d cycle=%d did not close" % (n, cid))
            expanded.append(ex)
            table.append(circ_mod.circulate(ex, p, q))
        payload = {"n": n, "b": [p, q], "cycles": expanded, "circulation": table}
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
    import time as _time
    import tracemalloc as _tracemalloc
    _tracemalloc.start()
    _t0 = _time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="4,5,6,7")
    args = ap.parse_args()
    print("[WP1-STEP-00] PHASE 03: rotation verification + expansion mechanics", flush=True)
    imp = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    if not os.path.exists(os.path.join(imp, "replay.json")):
        print("[WP1-STEP-00] PHASE03_FAIL: run_phase01 outputs missing", flush=True)
        return 1
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
    exit_code = 1 if fails else 0
    # WP1-STEP-00: §27 execution record (append-only; fullest honest field set).
    rec = log_mod.static_fields(ROOT)
    rec.update({
        "phase": "03", "branch": "WP-1", "command": sys.argv,
        "scientific_status": "ROTATION_TRACE_CERTIFIED" if not fails else "PHASE03_FAIL",
        "input_hashes": log_mod.hash_outputs(ROOT, ["artifacts/v03/parent_import"]),
        "output_hashes": log_mod.hash_outputs(ROOT, ["artifacts/v03/cycles/expanded",
                                                     "artifacts/v03/rotations"]),
        "wall_s": round(_time.perf_counter() - _t0, 2),
        "allocator_peak_bytes": _tracemalloc.get_traced_memory()[1],
        "exit_code": exit_code,
    })
    _tracemalloc.stop()
    # WP-1 REPAIR STEP L3: append the §27 execution record (fail-closed fields).
    log_mod.write_log(os.path.join(ROOT, "artifacts", "v03", "logs", "phase03_wp1.jsonl"), rec)
    print("[WP1-STEP-00] §27 record appended (phase03_wp1.jsonl)", flush=True)
    if fails:
        print("[WP1-STEP-00] PHASE03_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP1-STEP-00] ROTATION_TRACE_CERTIFIED (mechanics scope; MST0-02/04 reviews pending human)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
