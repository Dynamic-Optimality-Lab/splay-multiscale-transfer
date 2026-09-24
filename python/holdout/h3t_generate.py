"""HOLDOUT-H3T-v0.3 generator (PHASE 08): 70,000 transfer-level episodes.

Deterministic (seeded), target-blind (structural predicates only: rotation cases,
pairing classes, nesting depth — never target values, and no transfer candidates
exist yet). Every episode starts diagonal (A=B=T0, inherited
convention). Per episode: seed, n, init shape, [(mode,key)] history, stratum,
length, totals, final tree hashes, episode hash. Sharded per size as .json.zst.
Console lines prefixed [WP3-STEP-04] are the audit record.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles.enumerate import PairDomain, build_node_tree  # noqa: E402
from python.splay_ref.splay import Node, cost, serialize, splay  # noqa: E402

MASTER_SEED = 20260923
SIZES = [10, 12, 16, 24, 32, 48, 64]
PER_SIZE = 10000
LENGTH_MENU = (24, 48, 96)
STRATA = ["RANDOM_LEGAL", "DELETE_BURST_THEN_KEEP", "ALTERNATING_KEEP_DELETE",
          "SPINE_VS_BALANCED", "OPPOSITE_SPINE", "ZIGZIG_ENRICHED",
          "ZIGZAG_ENRICHED", "BOUNDARY_PAIRING_ENRICHED",
          "NESTED_INTERVAL_ENRICHED", "MIRROR_PAIRED", "MOTIF_BLIND_RANDOM_WALK"]
STRATUM_COUNTS = {"RANDOM_LEGAL": 2000, "DELETE_BURST_THEN_KEEP": 800,
                  "ALTERNATING_KEEP_DELETE": 800, "SPINE_VS_BALANCED": 800,
                  "OPPOSITE_SPINE": 800, "ZIGZIG_ENRICHED": 800,
                  "ZIGZAG_ENRICHED": 800, "BOUNDARY_PAIRING_ENRICHED": 800,
                  "NESTED_INTERVAL_ENRICHED": 800, "MIRROR_PAIRED": 800,
                  "MOTIF_BLIND_RANDOM_WALK": 800}
MAX_RETRIES = 12


def _rng(size: int, stratum: str, idx: int) -> random.Random:
    """Deterministic per-episode RNG (master seed + coordinates, string-seeded)."""
    return random.Random("%d:%d:%s:%d" % (MASTER_SEED, size, stratum, idx))


def _init_tree(rng: random.Random, n: int, stratum: str) -> Node:
    """Diagonal-start initial tree by stratum (balanced / spine / random)."""
    from python.splay_ref.splay import build_balanced, build_spine
    keys = list(range(1, n + 1))
    if stratum in ("SPINE_VS_BALANCED", "OPPOSITE_SPINE"):
        return build_spine(keys, left=True)
    if stratum == "RANDOM_LEGAL" and rng.random() < 0.5:
        order = keys[:]
        rng.shuffle(order)
        root = None
        for k in order:
            node = Node(k)
            if root is None:
                root = node
                continue
            cur = root
            while True:
                if k < cur.key:
                    if cur.left is None:
                        cur.left = node
                        node.parent = cur
                        break
                    cur = cur.left
                else:
                    if cur.right is None:
                        cur.right = node
                        node.parent = cur
                        break
                    cur = cur.right
        return root
    return build_balanced(keys)


def _sim(history: list, T0: Node, n: int) -> dict:
    """Simulate a history from a diagonal start; structural tallies only."""
    from python.splay_ref.splay import serialize as _ser

    def fresh():
        return _rebuild(T0)

    A, B = fresh(), fresh()
    sum_a = sum_y = 0
    zigzig = zigzag = rots = 0
    nests: list[int] = []
    Alb = _ser(T0)
    for mode, x in history:
        if mode == "DELETE":
            a = cost(A, x)
            sum_a += a
            A, ev = splay(A, x)
            rots += len(ev)
        else:
            a, y = cost(A, x), cost(B, x)
            sum_a += a
            sum_y += y
            A, evA = splay(A, x)
            B, evB = splay(B, x)
            for e in evB:
                rots += 1
                if e["case"] in ("LL", "RR"):
                    zigzig += 1
                elif e["case"] in ("LR", "RL"):
                    zigzag += 1
    return {"sum_a": sum_a, "sum_y": sum_y, "zigzig": zigzig, "zigzag": zigzag,
            "rots": rots, "final_A": _ser(A), "final_B": _ser(B), "init": Alb}


def _rebuild(T0: Node) -> Node:
    """Fresh deep copy of a pointer tree."""
    if T0 is None:
        return None
    n = Node(T0.key)
    n.left = _rebuild(T0.left)
    if n.left is not None:
        n.left.parent = n
    n.right = _rebuild(T0.right)
    if n.right is not None:
        n.right.parent = n
    return n


def _boundary_count(history: list, T0: Node, n: int) -> int:
    """Boundary-pairing count via translated heap views (structural only)."""
    from python.cycles import stratify as strat_mod
    from python.l6_translation import rank as rank_mod
    A, B = _rebuild(T0), _rebuild(T0)
    total = 0
    for mode, x in history:
        if mode == "DELETE":
            A, _e = splay(A, x)
            continue
        A1, _e = splay(A, x)
        rank = rank_mod.all_ranks(A1)
        steps = strat_mod.stepwise_b_splay(strat_mod._snapshot(B), x)
        B, _e2 = splay(B, x)
        A = A1
        for s in steps[1:]:
            if s["case"] not in ("LL", "RR") or len(s["nodes"]) != 3:
                continue
            tree = strat_mod._parse_serialized(s["tree"])
            v = strat_mod.translated_view(A1, tree)
            owner = {}
            for b, rec0 in v["view"].items():
                for k in rec0["members"]:
                    owner[k] = b
            triple = sorted({owner[k] for k in s["nodes"] if k in owner})
            if len(triple) == 3:
                from python.l6_translation import pairing as pairing_mod
                from python.l6_translation import contracted as contracted_mod
                dec = pairing_mod.decompose_zigzig(triple, rank)
                contracted_of = {b: contracted_mod.contracted(v["gaps"][b]) for b in v["gaps"]}
                for pr in dec:
                    cls = pairing_mod.classify_pairing(pr, False, contracted_of, (0, 0))
                    if cls in ("IMPORTANT", "UNIMPORTANT"):
                        total += 1
    return total


def _nest_depth(history: list, T0: Node, n: int) -> int:
    """Max heap-component nesting depth over KEEP snapshots (structural only)."""
    from python.cycles import stratify as strat_mod
    from python.l6_translation import heap as heap_mod
    from python.l6_translation import heavy as heavy_mod
    from python.l6_translation import rank as rank_mod
    A, B = _rebuild(T0), _rebuild(T0)
    best = 0
    for mode, x in history:
        if mode == "DELETE":
            A, _e = splay(A, x)
            continue
        A1, _e = splay(A, x)
        rank = rank_mod.all_ranks(A1)
        Bs = _rebuild(B)
        heavy = heavy_mod.heavy_edges(Bs, rank)
        comps = heavy_mod.components(Bs, heavy)
        dep = heap_mod.depths(Bs)
        comp_rank = {c: rank[heavy_mod.bottom_most(c, dep)] for c in comps}
        view = heap_mod.heap_view(Bs, comps, comp_rank)
        depth: dict = {}
        def comp_depth(b):
            if b in depth:
                return depth[b]
            hp = view[b]["heap_parent"]
            depth[b] = 1 if hp is None else comp_depth(hp) + 1
            return depth[b]
        for b in view:
            best = max(best, comp_depth(b))
        B, _e2 = splay(B, x)
        A = A1
    return best


# WP3-STEP-04: build one episode history for (size, stratum, idx).
def build_history(rng: random.Random, n: int, stratum: str, length: int) -> list:
    """Deterministic history builder per stratum (modes+keys only)."""
    hist = []
    if stratum == "DELETE_BURST_THEN_KEEP":
        nb = length * 2 // 5
        hist = [["DELETE", rng.randint(1, n)] for _ in range(nb)]
        hist += [["KEEP", rng.randint(1, n)] for _ in range(length - nb)]
    elif stratum == "ALTERNATING_KEEP_DELETE":
        hist = [[("KEEP" if (i % 2 == 0) else "DELETE"), rng.randint(1, n)]
                for i in range(length)]
    elif stratum in ("SPINE_VS_BALANCED", "OPPOSITE_SPINE"):
        # Diagonal spine start; DELETE-heavy prefix separates A/B structurally.
        hist = [[("DELETE" if rng.random() < 0.6 else "KEEP"), rng.randint(1, n)]
                for _ in range(length)]
    elif stratum == "MIRROR_PAIRED":
        half = length // 2
        first = [[("KEEP" if rng.random() < 0.7 else "DELETE"), rng.randint(1, n)]
                 for _ in range(half)]
        hist = first + [[m, n + 1 - x] for m, x in first[:length - half]]
    else:
        hist = [[("KEEP" if rng.random() < 0.7 else "DELETE"), rng.randint(1, n)]
                for _ in range(length)]
    return hist


def _enriched(rng: random.Random, n: int, stratum: str, length: int, T0: Node) -> list:
    """Rejection-sampled enriched histories (structural predicates only)."""
    best, best_score = None, -1
    for _ in range(MAX_RETRIES):
        hist = [[("KEEP" if rng.random() < 0.7 else "DELETE"), rng.randint(1, n)]
                for _ in range(length)]
        sim = _sim(hist, T0, n)
        if stratum == "ZIGZIG_ENRICHED":
            score = sim["zigzig"] / max(1, sim["rots"])
            ok = score >= 0.35
        elif stratum == "ZIGZAG_ENRICHED":
            score = sim["zigzag"] / max(1, sim["rots"])
            ok = score >= 0.15
        elif stratum == "BOUNDARY_PAIRING_ENRICHED":
            score = _boundary_count(hist, T0, n)
            ok = score >= 2
        elif stratum == "NESTED_INTERVAL_ENRICHED":
            score = _nest_depth(hist, T0, n)
            ok = score >= 3
        else:
            return hist
        if ok:
            return hist
        if score > best_score:
            best, best_score = hist, score
    return best


# WP3-STEP-04: generate one size shard (deterministic).
def generate_size(n: int, per_size: int, outdir: str) -> dict:
    """Generate per_size episodes for n (stratum counts scale proportionally)."""
    episodes = []
    counts: dict[str, int] = {}
    lengths: dict[int, int] = {}
    idx = 0
    size_idx = SIZES.index(n)
    scale = per_size / float(sum(STRATUM_COUNTS.values()))
    for stratum in STRATA:
        target = max(1, int(round(STRATUM_COUNTS[stratum] * scale)))
        for k in range(target):
            rng = _rng(n, stratum, idx)
            length = LENGTH_MENU[(size_idx + idx) % len(LENGTH_MENU)]
            T0 = _init_tree(rng, n, stratum)
            if stratum in ("ZIGZIG_ENRICHED", "ZIGZAG_ENRICHED",
                           "BOUNDARY_PAIRING_ENRICHED", "NESTED_INTERVAL_ENRICHED"):
                hist = _enriched(rng, n, stratum, length, T0)
            else:
                hist = build_history(rng, n, stratum, length)
            sim = _sim(hist, T0, n)
            ep_hash = hashlib.sha256(json.dumps(
                {"n": n, "stratum": stratum, "init": sim["init"],
                 "history": hist, "totals": [sim["sum_a"], sim["sum_y"]],
                 "final": [sim["final_A"], sim["final_B"]]}, sort_keys=True
            ).encode("utf-8")).hexdigest().upper()
            episodes.append({"n": n, "stratum": stratum, "idx": idx,
                             "init_shape": sim["init"], "history": hist,
                             "length": len(hist), "sum_a": sim["sum_a"],
                             "sum_y": sim["sum_y"], "final_A": sim["final_A"],
                             "final_B": sim["final_B"], "episode_hash": ep_hash})
            counts[stratum] = counts.get(stratum, 0) + 1
            lengths[len(hist)] = lengths.get(len(hist), 0) + 1
            idx += 1
    blob = json.dumps(episodes, sort_keys=True).encode("utf-8")
    import zstandard as zstd
    shard = zstd.ZstdCompressor(level=9).compress(blob)
    path = os.path.join(outdir, "n%d.json.zst" % n)
    with open(path, "wb") as f:
        f.write(shard)
    stream = hashlib.sha256("".join(sorted(e["episode_hash"] for e in episodes))
                            .encode("utf-8")).hexdigest().upper()
    print("[WP3-STEP-04] n=%d episodes=%d bytes=%d stream=%s..."
          % (n, len(episodes), len(shard), stream[:16]), flush=True)
    return {"count": len(episodes), "bytes": len(shard), "stream": stream,
            "strata": counts, "lengths": {str(k): v for k, v in sorted(lengths.items())}}
