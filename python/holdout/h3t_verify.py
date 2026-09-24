"""HOLDOUT-H3T-v0.3 independent verifier (PHASE 08): streamed hashes + sampled replay.

Full policy: re-read every shard, recompute per-size stream hashes and the
logical-stream hash (cryptographic full coverage). Sampled policy: replay a
stratified sample per size with the INDEPENDENT dict-state core, comparing final
trees + totals against the recorded values (exact agreement required).
Console lines prefixed [WP3-STEP-05] are the audit record.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.splay_ref import independent as I  # noqa: E402


def _parse_keyed(ss: str, pos: list):
    if ss[pos[0]] == ".":
        pos[0] += 1
        return None
    assert ss[pos[0]] == "("
    pos[0] += 1
    key = 0
    while ss[pos[0]].isdigit():
        key = key * 10 + int(ss[pos[0]])
        pos[0] += 1
    left = _parse_keyed(ss, pos)
    right = _parse_keyed(ss, pos)
    assert ss[pos[0]] == ")"
    pos[0] += 1
    return (left, key, right)


def _to_dict_state(tree: tuple | None) -> dict:
    """Keyed-tuple tree to independent dict-state (separate construction path)."""
    nodes: dict[int, list] = {}

    def rec(t, parent):
        if t is None:
            return None
        left, key, right = t
        nodes[key] = [None, None, parent]
        nodes[key][0] = rec(left, key)
        nodes[key][1] = rec(right, key)
        return key

    return {"nodes": nodes, "root": rec(tree, None)}


def _load_shard(bankdir: str, n: int) -> list:
    import zstandard as zstd
    with open(os.path.join(bankdir, "n%d.json.zst" % n), "rb") as f:
        return json.loads(zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))


# WP3-STEP-05: full streamed hash verification (every shard, every episode).
def verify_hashes(bankdir: str, commitment: dict) -> list[str]:
    """Recompute per-size streams + logical hash; compare to commitment."""
    fails: list[str] = []
    streams = {}
    for n in commitment["sizes"]:
        eps = _load_shard(bankdir, int(n))
        if len(eps) != commitment["sizes"][n]["count"]:
            fails.append("H3T-HASH n=%s count %d != %d" % (n, len(eps), commitment["sizes"][n]["count"]))
            continue
        stream = hashlib.sha256("".join(sorted(e["episode_hash"] for e in eps))
                                .encode("utf-8")).hexdigest().upper()
        streams[n] = stream
        if stream != commitment["sizes"][n]["stream"]:
            fails.append("H3T-HASH n=%s stream mismatch" % n)
        else:
            print("[WP3-STEP-05] n=%s stream verified (%d episodes)" % (n, len(eps)), flush=True)
    logical = hashlib.sha256("".join(sorted(streams.values())).encode("utf-8")).hexdigest().upper()
    if logical != commitment.get("logical_stream"):
        fails.append("H3T-HASH logical stream mismatch")
    else:
        print("[WP3-STEP-05] logical stream verified: %s..." % logical[:16], flush=True)
    return fails


# WP3-STEP-05: sampled exact replay with the independent core.
def verify_sample(bankdir: str, per_size: int, seed: int = 707) -> list[str]:
    """Replay a deterministic stratified sample per size; exact agreement required."""
    import random
    fails: list[str] = []
    rng = random.Random(seed)
    checked = 0
    for fn in sorted(os.listdir(bankdir)):
        if not (fn.startswith("n") and fn.endswith(".json.zst")):
            continue
        n = int(fn[1:-len(".json.zst")])
        eps = _load_shard(bankdir, n)
        by_stratum: dict[str, list] = {}
        for e in eps:
            by_stratum.setdefault(e["stratum"], []).append(e)
        for stratum, group in sorted(by_stratum.items()):
            k = max(1, per_size // len(by_stratum))
            for e in rng.sample(group, min(k, len(group))):
                A = _to_dict_state(_parse_keyed(e["init_shape"], [0]))
                B = _to_dict_state(_parse_keyed(e["init_shape"], [0]))
                sum_a = sum_y = 0
                for mode, x in e["history"]:
                    if mode == "DELETE":
                        sum_a += I.cost2(A, x)
                        I.splay2(A, x)
                    else:
                        sum_a += I.cost2(A, x)
                        sum_y += I.cost2(B, x)
                        I.splay2(A, x)
                        I.splay2(B, x)
                if sum_a != e["sum_a"] or sum_y != e["sum_y"]:
                    fails.append("H3T-REPLAY n=%d %s totals mismatch" % (n, e["episode_hash"][:8]))
                elif I.serialize2(A) != e["final_A"] or I.serialize2(B) != e["final_B"]:
                    fails.append("H3T-REPLAY n=%d %s final trees mismatch" % (n, e["episode_hash"][:8]))
                else:
                    checked += 1
    print("[WP3-STEP-05] sampled replay: %d episodes exact" % checked, flush=True)
    return fails
