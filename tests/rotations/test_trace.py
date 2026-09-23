"""Rotation-trace suite (ROT reference/block/circulation checks). Fast; corpus-free."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.rotations import blocks as blocks_mod  # noqa: E402
from python.rotations import reference as ref_mod  # noqa: E402
from python.rotations.trace import trace_delete, trace_keep  # noqa: E402
from python.splay_ref.splay import build_balanced  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_reference_convention() -> None:
    check("ROT-11 convention pinned", ref_mod.CONVENTION == "KEEP_REF_SNAPSHOT-v1")
    d = ref_mod.describe()
    check("ROT-11 convention record has 5 ordered steps", len(d["order"]) == 5)
    A = build_balanced([1, 2, 3])
    B = build_balanced([1, 2, 3])
    t = trace_keep(A, B, 2, "rot-unit")
    check("ROT-11 snapshot recorded", t["reference_snapshot_hash"] == ref_mod.snapshot_hash(A))
    check("ROT-11 edge carries convention", t["convention"] == ref_mod.CONVENTION)


def test_blocks() -> None:
    hists = [[], [{"mode": "KEEP", "x": 1}], [{"mode": "DELETE", "x": 1}],
             [{"mode": "DELETE", "x": 1}, {"mode": "KEEP", "x": 1}, {"mode": "DELETE", "x": 2}],
             [{"mode": "KEEP", "x": 1}, {"mode": "KEEP", "x": 2}, {"mode": "KEEP", "x": 3}]]
    for h in hists:
        check("BLOCK-01 coverage len=%d" % len(h),
              blocks_mod.check_coverage(h, blocks_mod.partition(h)))
    h = hists[3]
    kinds = [b["kind"] for b in blocks_mod.partition(h)]
    check("BLOCK-01 alternation", kinds == ["DELETE_BLOCK", "KEEP_BLOCK", "DELETE_BLOCK"])


def test_circulation_smoke() -> None:
    from python.cycles.circulation import circulate
    fake = {"cycle_index": 0, "closed": True,
            "edges": [{"a": 2, "y": 3, "events": [{"splay_case": "LL"}, {"splay_case": "ZIG"}]},
                      {"a": 2, "y": 3, "events": [{"splay_case": "RL"}]}]}
    c = circulate(fake, 3, 2)
    check("CYC-06 slack arithmetic", (c["scaled_slack_num"], c["scaled_slack_den"]) == (0, 1))
    check("CYC-06 flow counts", c["flow_counts"]["zigzig"] == 1 and c["flow_counts"]["zigzag"] == 1)


if __name__ == "__main__":
    test_reference_convention()
    test_blocks()
    test_circulation_smoke()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
