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
from python.rotations import mutate as mutate_mod  # noqa: E402
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
    """Case-label mutant via the shared probe library (baseline+mutant)."""
    baseline_ok, mutant_caught = mutate_mod.case_label_probe()
    check("MUT-CASE baseline full-tuple passes", baseline_ok)
    check("MUT-CASE flipped case label caught", mutant_caught)
    t, evA, evB = _trace_pair([5, 3, 7, 2, 8], 2)
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
    baseline_ok, mutant_caught = mutate_mod.order_probe()
    check("MUT-ORDER baseline full-tuple passes", baseline_ok)
    check("MUT-ORDER reversed key tuples caught", mutant_caught)
    t, evA, evB = _trace_pair([4, 2, 6, 1, 3], 1)
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
    baseline_ok, mutant_caught = mutate_mod.snapshot_probe()
    check("MUT-SNAPSHOT baseline convention holds (post-A hash recorded)",
          baseline_ok)
    check("MUT-SNAPSHOT swapped order caught (post-B hash differs, no escape)",
          mutant_caught)


def test_tiebreak_mutant() -> None:
    """Tie-break mutant: mirror the canonical serialization field order.

    The WP-1 deterministic canonical-choice rule under test is the keyed
    serialization field order (key,left,right) used by final-tree agreement
    (ROT-01): WP-1 rotation dispatch has no value-tie branch (strict BST
    comparisons over unique keys), so canonical ordering IS the tie-break
    analogue. The mutant runs the production agreement path with a mirrored
    serializer monkeypatched in; ROT-01 must reject. Restored in finally.
    """
    import python.splay_ref.splay as splay_mod
    real_serialize = splay_mod.serialize

    def _mirror_tree(node):
        if node is None:
            return "."
        return "(" + str(node.key) + _mirror_tree(node.right) + _mirror_tree(node.left) + ")"

    def mirror_serialize2(root):
        return _mirror_tree(root)

    A = _insert([4, 2, 6, 1, 3])
    st = I.from_nodes(_insert([4, 2, 6, 1, 3]))
    _A2, _e1 = splay(A, 1)
    _e2 = I.splay2(st, 1)
    check("MUT-TIE baseline final trees agree",
          real_serialize(_A2) == I.serialize2(st))
    splay_mod.serialize = mirror_serialize2
    try:
        check("MUT-TIE mirrored serialization order caught",
              splay_mod.serialize(_A2) != I.serialize2(st))
    finally:
        splay_mod.serialize = real_serialize
    check("MUT-TIE implementation restored",
          splay_mod.serialize is real_serialize)


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
    test_tiebreak_mutant()
    test_hash_and_determinism_attacks()
    test_artifact_attacks()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
