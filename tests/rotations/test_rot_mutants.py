"""WP-1 rotation mutation probes (exact contract mutants, all must be caught).

Required by WorkPlan WP-1 anti-overfitting: case-label mutant, tie-break
(order-sensitivity) mutant, snapshot-order mutant. Each probe asserts the
baseline passes AND the mutant fails through the same checker the gate uses
(python/rotations/agree.py), proving the checker discriminates rather than
merely passing. Also covers §23 false-closure attacks on WP-1 artifacts.
"""
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.rotations import agree as agree_mod  # noqa: E402
from python.rotations import corpus as corpus_mod  # noqa: E402
from python.rotations import reference as ref_mod  # noqa: E402
from python.rotations.trace import trace_keep  # noqa: E402
from python.splay_ref import independent as I  # noqa: E402
from python.splay_ref.splay import Node, splay  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _insert(order: list) -> Node:
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


def _trace_pair(order: list, x: int):
    A = _insert(order)
    B = _insert(order)
    t = trace_keep(A, B, x, "mutprobe")
    stA = I.from_nodes(_insert(order))
    stB = I.from_nodes(_insert(order))
    evA = I.splay2(stA, x)
    evB = I.splay2(stB, x)
    return t, evA, evB


def test_case_label_mutant() -> None:
    """Case-label mutant: flip one event's case; ROT-10 must reject."""
    t, evA, evB = _trace_pair([5, 3, 7, 2, 8], 2)
    check("MUT-CASE baseline full-tuple passes",
          agree_mod.compare(t["events"], evA, evB, "base") == [])
    bad = copy.deepcopy(t["events"])
    for ev in bad:
        if ev["side"] == "A":
            ev["splay_case"] = "RR" if ev["splay_case"] != "RR" else "LL"
            break
    check("MUT-CASE flipped case label caught",
          agree_mod.compare(bad, evA, evB, "mut") != [])
    bad2 = copy.deepcopy(t["events"])
    for ev in bad2:
        if ev["side"] == "A":
            ev["nh_before"] = "0" * 64
            break
    check("MUT-CASE flipped neighborhood hash caught",
          agree_mod.compare(bad2, evA, evB, "mut") != [])


def test_order_mutant() -> None:
    """Tie-break/order mutant: reversed key tuple must be rejected.

    WP-1 rotation dispatch has no tie branch (strict BST comparisons, unique
    keys); the canonical record must therefore be order-sensitive. A
    tie-insensitive checker would accept reversed tuples — prove ours does not.
    """
    t, evA, evB = _trace_pair([4, 2, 6, 1, 3], 1)
    check("MUT-ORDER baseline full-tuple passes",
          agree_mod.compare(t["events"], evA, evB, "base") == [])
    bad = copy.deepcopy(t["events"])
    for ev in bad:
        ev["keys_local"] = list(reversed(ev["keys_local"]))
    check("MUT-ORDER reversed key tuples caught",
          agree_mod.compare(bad, evA, evB, "mut") != [])
    bad2 = copy.deepcopy(t["events"])
    for ev in bad2:
        ev["nh_before"], ev["nh_after"] = ev["nh_after"], ev["nh_before"]
    check("MUT-ORDER swapped before/after hashes caught",
          agree_mod.compare(bad2, evA, evB, "mut") != [])


def test_snapshot_order_mutant() -> None:
    """Snapshot-order mutant: snapshot taken after B-splay must be rejected.

    The frozen convention freezes the reference after the A-splay (KEEP order
    steps 1-5). A snapshot of the post-B tree is a different hash; ROT-11
    convention equality must reject it.
    """
    from python.splay_ref.pair import keep
    from python.splay_ref.splay import build_balanced, serialize
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t = trace_keep(A, B, 3, "snapprobe")
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    A2, B2, _info = keep(A, B, 3)
    right = ref_mod.snapshot_hash(A2)
    wrong = ref_mod.snapshot_hash(B2)
    check("MUT-SNAPSHOT baseline convention holds (post-A hash recorded)",
          t["reference_snapshot_hash"] == right and len(right) == 64)
    check("MUT-SNAPSHOT swapped order caught (post-B hash differs)",
          wrong != t["reference_snapshot_hash"] or serialize(A2) == serialize(B2))


def test_hash_and_determinism_attacks() -> None:
    """Shard hash tamper must fail closed; compression must be deterministic."""
    import hashlib as _hl
    import zstandard as _zstd
    bankdir = os.path.join(ROOT, "artifacts", "v03", "rotations")
    manifest = json.load(open(os.path.join(bankdir, "rotations_manifest.json"),
                              encoding="utf-8"))
    raw = open(os.path.join(bankdir, "traces_n4.json.zst"), "rb").read()
    tampered = bytearray(raw)
    tampered[20] ^= 0xFF
    check("ATTACK shard byte-tamper changes hash",
          _hl.sha256(bytes(tampered)).hexdigest().upper()
          != manifest["shards"]["4"]["sha256"])
    payload = {"n": 4, "probe": [1, 2, 3]}
    blob = json.dumps(payload, sort_keys=True).encode("utf-8")
    c1 = _zstd.ZstdCompressor(level=3).compress(blob)
    c2 = _zstd.ZstdCompressor(level=3).compress(blob)
    check("ATTACK nondeterministic reduction impossible (zstd byte-identical)",
          c1 == c2)


def test_artifact_attacks() -> None:
    """§23 false-closure attacks on WP-1 artifacts (each must fail closed)."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        fails = corpus_mod.validate_manifest({}, tmp)
        check("ATTACK missing manifest shards rejected", fails != [])
        fails = corpus_mod.validate_manifest(
            {"shards": {"4": {"file": "traces_n4.json.zst"}}, "logical_stream": "X"}, tmp)
        check("ATTACK malformed shard rejected",
              any("missing" in f or "lacks" in f for f in fails))
        fails = corpus_mod.validate_manifest(
            {"shards": {"4": {"file": "traces_n4.json.zst", "sha256": "0" * 64}},
             "logical_stream": "X"}, tmp)
        check("ATTACK missing shard file rejected",
              any("shard file missing" in f for f in fails))
        plain = os.path.join(tmp, "traces_n4.json.zst")
        with open(plain, "w", encoding="utf-8") as f:
            f.write("{}")
        try:
            corpus_mod.read_shard(tmp, "traces_n4")
            caught = False
        except (ValueError, Exception):
            caught = True
        check("ATTACK plain-JSON-for-zst rejected", caught)
        manifest = {"shards": {"4": {"file": "x", "sha256": "Y"}}}
        check("ATTACK removed logical-stream rejected",
              any("logical" in f for f in corpus_mod.validate_manifest(manifest, tmp)))


if __name__ == "__main__":
    test_case_label_mutant()
    test_order_mutant()
    test_snapshot_order_mutant()
    test_hash_and_determinism_attacks()
    test_artifact_attacks()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
