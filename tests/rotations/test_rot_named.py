"""WP-1 named rotation tests (ROT-01..12, exact normative meanings).

Normative source: spec §24 (rotation family). Exactly ONE check() binding per
ID (dictionary discipline, F13): each ID's full meaning is a single compound
predicate evaluated over all fixtures. Corpus-scale agreement lives in
run_phase03 (STEP-04) and test_foundation.
"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.splay_ref import independent as I  # noqa: E402
from python.splay_ref.splay import (Node, build_balanced, cost, depth,  # noqa: E402
                                    search_path, serialize, splay)

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


def test_rot01_final_tree() -> None:
    """ROT-01 final tree matches parent Splay: splayed key at root, trees agree."""
    ok = True
    for order, x in [([2, 1, 3], 1), ([1, 2, 3], 3), ([3, 2, 1], 1), ([3, 1, 2], 2)]:
        A = _insert(order)
        st = I.from_nodes(_insert(order))
        A2, _e1 = splay(A, x)
        I.splay2(st, x)
        ok = ok and A2.key == x and serialize(A2) == I.serialize2(st)
    check("ROT-01 final tree at root and agreed", ok)


def test_rot02_search_path() -> None:
    """ROT-02 search path exact: both cores walk the identical root-to-x path."""
    rng = random.Random("ROT-02")
    ok = True
    for trial in range(12):
        n = 9
        order = list(range(1, n + 1))
        rng.shuffle(order)
        A = _insert(order)
        st = I.from_nodes(_insert(order))
        x = rng.randint(1, n)
        ok = ok and search_path(A, x) == I.path2(st, x)
    check("ROT-02 search paths equal on 12 trials", ok)


def test_rot03_root() -> None:
    """ROT-03 ROOT case: splaying the root performs zero rotations."""
    A = _insert([2, 1, 3])
    st = I.from_nodes(_insert([2, 1, 3]))
    _A2, e1 = splay(A, 2)
    e2 = I.splay2(st, 2)
    check("ROT-03 ROOT zero rotations", e1 == [] and e2 == [])


# WP-1 REPAIR STEP T4: frozen per-case registry (literal IDs for the set gate).
CASE_TESTS = [
    # (rot_id, case, insertion order, x, orientation, depth_before, nkeys)
    ("ROT-04", "ZIG", [2, 1, 3], 1, "L", 1, 2),
    ("ROT-05", "LL", [3, 2, 1], 1, "L,L", 2, 3),
    ("ROT-06", "RR", [1, 2, 3], 3, "R,R", 2, 3),
    ("ROT-07", "LR", [3, 1, 2], 2, "R,L", 2, 3),
    ("ROT-08", "RL", [1, 3, 2], 2, "L,R", 2, 3),
]


def _case_holds(rot_id: str, case: str, order: list, x: int,
                orientation: str, depth_before: int, nkeys: int) -> bool:
    A = _insert(order)
    st = I.from_nodes(_insert(order))
    _A2, e1 = splay(A, x)
    e2 = I.splay2(st, x)
    first1, first2 = e1[0], e2[0]
    return (first1["case"] == case == first2["case"]
            and first1["orientation"] == orientation == first2["orientation"]
            and first1["depth_before"] == depth_before == first2["depth_before"]
            and len(first1["keys_local"]) == nkeys
            and first1["keys_local"] == first2["keys_local"]
            and first1["nh_before"] == first2["nh_before"]
            and first1["nh_after"] == first2["nh_after"]
            and len(first1["nh_before"]) == 64 and len(first1["nh_after"]) == 64)


def test_rot04_zig() -> None:
    """ROT-04 ZIG case (first-event semantics, both cores)."""
    check("ROT-04 ZIG case exact", _case_holds(*CASE_TESTS[0]))


def test_rot05_ll() -> None:
    """ROT-05 LL case (first-event semantics, both cores)."""
    check("ROT-05 LL case exact", _case_holds(*CASE_TESTS[1]))


def test_rot06_rr() -> None:
    """ROT-06 RR case (first-event semantics, both cores)."""
    check("ROT-06 RR case exact", _case_holds(*CASE_TESTS[2]))


def test_rot07_lr() -> None:
    """ROT-07 LR case (first-event semantics, both cores)."""
    check("ROT-07 LR case exact", _case_holds(*CASE_TESTS[3]))


def test_rot08_rl() -> None:
    """ROT-08 RL case (first-event semantics, both cores)."""
    check("ROT-08 RL case exact", _case_holds(*CASE_TESTS[4]))


def test_rot09_ordering() -> None:
    """ROT-09 canonical event ordering: indices 0..k-1, byte-identical reruns."""
    import json as _json
    A = _insert([5, 3, 7, 2, 8])
    _A2, e1 = splay(A, 2)
    A = _insert([5, 3, 7, 2, 8])
    _A2b, e1b = splay(A, 2)
    check("ROT-09 canonical ordering and byte-identical reruns",
          [e["index"] for e in e1] == list(range(len(e1)))
          and _json.dumps(e1, sort_keys=True) == _json.dumps(e1b, sort_keys=True))


def test_rot10_agreement() -> None:
    """ROT-10 independent core agreement: full tuple on samples (scale: unit)."""
    rng = random.Random("ROT-10")
    bad = 0
    for trial in range(10):
        order = list(range(1, 8))
        rng.shuffle(order)
        A = _insert(order)
        st = I.from_nodes(_insert(order))
        x = rng.randint(1, 7)
        _A2, e1 = splay(A, x)
        e2 = I.splay2(st, x)
        if e1 != e2 or serialize(_A2) != I.serialize2(st):
            bad += 1
    check("ROT-10 full-tuple agreement 10 samples", bad == 0)


def test_rot11_snapshot() -> None:
    """ROT-11 reference snapshot exact: KEEP_REF_SNAPSHOT-v1 deterministic 64-hex."""
    from python.rotations import reference as ref_mod
    from python.rotations.trace import trace_keep
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t1 = trace_keep(A, B, 3, "rot11-a")
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t2 = trace_keep(A, B, 3, "rot11-b")
    check("ROT-11 snapshot deterministic 64-hex under frozen convention",
          t1["reference_snapshot_hash"] == t2["reference_snapshot_hash"]
          and len(t1["reference_snapshot_hash"]) == 64
          and t1["convention"] == ref_mod.CONVENTION == "KEEP_REF_SNAPSHOT-v1")


def test_rot12_cost() -> None:
    """ROT-12 cost convention not redefined: depth+1 always, never rotation count."""
    A = _insert([3, 2, 1])
    base = cost(A, 1) == depth(A, 1) + 1 == 3
    _A2, ev = splay(_insert([3, 2, 1]), 1)
    # NOTE: one LL event performs two pointer rewirings; cost is 3. Neither the
    # event count (1) nor the rewiring count (2) equals cost (3): cost is
    # depth+1 by convention, rotations are charging units.
    rewirings = sum(1 if e["case"] == "ZIG" else 2 for e in ev)
    order = [3, 1, 5, 2, 4]
    cross = all(cost(_insert(order), x) == I.cost2(
        I.from_nodes(_insert(order)), x) for x in range(1, 6))
    check("ROT-12 cost equals depth+1, rotations are charging units, costs agree",
          base and len(ev) == 1 and rewirings == 2
          and cost(_insert([3, 2, 1]), 1) == 3 and cross)


def test_corpus_schema() -> None:
    """Corpus events validate against the ROT-EVENT-v0.3 schema (all shards)."""
    import json as _json
    import zstandard as _zstd
    from jsonschema import validate as _validate
    schema = _json.load(open(os.path.join(
        ROOT, "schemas", "rotation_event.schema.json"), encoding="utf-8"))
    bankdir = os.path.join(ROOT, "artifacts", "v03", "rotations")
    n_ev = 0
    for n in (2, 3, 4, 5, 6, 7):
        with open(os.path.join(bankdir, "traces_n%d.json.zst" % n), "rb") as f:
            payload = _json.loads(_zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))
        for tr in payload["traces"]:
            for ev in tr["events"]:
                _validate(instance=ev, schema=schema)
                n_ev += 1
    check("corpus schema-valid events %d" % n_ev, n_ev > 0)


def test_set_equality() -> None:
    """Dictionary gate: exactly one check() binding per ROT ID (fixtures in
    CASE_TESTS are the registry, not bindings)."""
    import re as _re
    from collections import Counter as _Counter
    src = open(__file__, encoding="utf-8").read()
    found = _re.findall(r"check\(\s*\"(ROT-0[1-9]|ROT-1[0-2]) ", src)
    counts = _Counter(found)
    check("ROT-01..12 each bound exactly once with normative meaning",
          all(counts.get("ROT-%02d" % i, 0) == 1 for i in range(1, 13)))
    rows = _re.findall(r"\(\"(ROT-0[4-8])\",", src)
    check("ROT-04..08 fixture registry complete",
          sorted(set(rows)) == ["ROT-%02d" % i for i in range(4, 9)])


if __name__ == "__main__":
    test_rot01_final_tree()
    test_rot02_search_path()
    test_rot03_root()
    test_rot04_zig()
    test_rot05_ll()
    test_rot06_rr()
    test_rot07_lr()
    test_rot08_rl()
    test_rot09_ordering()
    test_rot10_agreement()
    test_rot11_snapshot()
    test_rot12_cost()
    test_corpus_schema()
    test_set_equality()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
