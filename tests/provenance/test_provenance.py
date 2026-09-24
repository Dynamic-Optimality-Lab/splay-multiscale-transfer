"""Provenance test suite (LED/PROV mechanics). Fast; seeded development traces only."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.ledger import state as ledger_state  # noqa: E402
from python.provenance import active as active_mod  # noqa: E402
from python.provenance import descendants as desc_mod  # noqa: E402
from python.provenance import merge as merge_mod  # noqa: E402
from python.provenance import sources as sources_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_sources() -> None:
    ev_a = {"mode": "DELETE", "side": "A", "splay_case": "LL",
            "keys_local": [1, 2], "affected_interval": [1, 2]}
    ev_b = {"mode": "KEEP", "side": "B", "splay_case": "RR", "keys_local": [2, 3, 4]}
    check("PROV sources A emits 2", len(sources_mod.source_candidates(ev_a)) == 2)
    check("PROV sources B emits 0", sources_mod.source_candidates(ev_b) == [])
    check("PROV triggers B zigzig", sources_mod.b_transfer_triggers(ev_b)[0]["provenance_class"] == "B_ZIGZIG_TRANSFERRED")
    check("PROV triggers A none", sources_mod.b_transfer_triggers(ev_a) == [])
    try:
        sources_mod.source_candidates({"mode": "KEEP", "side": "A", "future_key": 9})
        check("PROV lookahead rejected", False)
    except ValueError:
        check("PROV lookahead rejected", True)


def test_descendants_merge() -> None:
    src = {"provenance_class": "A_ROTATION_CREATED",
           "structural_ref": {"interval": [1, 4], "keys_local": [2, 3], "case": "LL"}}
    d = desc_mod.descendants(src, orientation="LEFT")
    check("PROV descendants bounded at 5", len(d) == 5)
    try:
        desc_mod.descendants(src, orientation="UP")
        check("PROV orientation validated", False)
    except ValueError:
        check("PROV orientation validated", True)
    from fractions import Fraction
    c = ledger_state.make_credit("T", ("boundary", 1, 2, "LEFT"), ("S0", 1), Fraction(1), "P")
    l1 = ledger_state.add(ledger_state.empty(), c)
    check("PROV merge equal", merge_mod.merge(["a"], ["b"], l1, list(l1)) == ["a", "b"])
    c2 = ledger_state.make_credit("T", ("boundary", 1, 3, "LEFT"), ("S0", 1), Fraction(1), "P")
    try:
        merge_mod.merge(["a"], ["b"], l1, ledger_state.add(ledger_state.empty(), c2))
        check("PROV merge divergent refused", False)
    except ValueError:
        check("PROV merge divergent refused", True)


def test_active() -> None:
    from fractions import Fraction
    pred = {"all_of": [{"mode_is": "DELETE"}, {"not": {"case_is": "ZIG"}}]}
    c = {"type": "T", "support": ("key", 1), "scale": ("S0", 1),
         "mass": Fraction(2), "provenance": "P"}
    check("PROV active true", active_mod.evaluate(pred, c, {"mode": "DELETE", "splay_case": "LL"}))
    check("PROV active false", not active_mod.evaluate(pred, c, {"mode": "KEEP", "splay_case": "LL"}))
    try:
        active_mod.check_predicate({"mass_gt_tomorrow": 1})
        check("PROV unknown atom rejected", False)
    except ValueError:
        check("PROV unknown atom rejected", True)
    try:
        active_mod.register("P1", pred)
        active_mod.register("P1", pred)
        check("PROV registry append-only", False)
    except ValueError:
        check("PROV registry append-only", True)


if __name__ == "__main__":
    test_sources()
    test_descendants_merge()
    test_active()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
