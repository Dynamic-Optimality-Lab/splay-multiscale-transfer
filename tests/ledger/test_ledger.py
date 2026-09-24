"""Ledger test suite (LED mechanics). Fast; exact arithmetic throughout."""
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.ledger import energy as energy_mod  # noqa: E402
from python.ledger import flow as flow_mod  # noqa: E402
from python.ledger import state as ledger_state  # noqa: E402
from python.ledger import support as support_mod  # noqa: E402
from python.ledger import update as update_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def mk(t="T", sup=("boundary", 1, 2, "LEFT"), m=Fraction(1), p="P"):
    """Valid credit factory for tests."""
    return ledger_state.make_credit(t, sup, ("S0", 1), m, p)


def test_support() -> None:
    check("LED support valid", (support_mod.check_support(("interval", 1, 4)) or True))
    for bad in [("state_id", 4), ("boundary", 1, 2, "UP"), ("interval", 1),
                ("boundary", 1, "H1_X", "LEFT"), ("key",), ("nope", 1), (), "x"]:
        try:
            support_mod.check_support(bad)
            check("LED support rejects %r" % (bad,), False)
        except (ValueError, TypeError):
            check("LED support rejects %r" % (bad,), True)


def test_state_canonical() -> None:
    c1, c2 = mk("A"), mk("B")
    l1 = ledger_state.add(ledger_state.add(ledger_state.empty(), c1), c2)
    l2 = ledger_state.add(ledger_state.add(ledger_state.empty(), c2), c1)
    check("LED canonical order-free", ledger_state.canonical(l1) == ledger_state.canonical(l2))
    check("LED count", ledger_state.count(l1) == 2)
    l3 = ledger_state.remove(l1, c1)
    check("LED remove", ledger_state.count(l3) == 1)
    try:
        ledger_state.remove(l3, c1)
        check("LED remove absent raises", False)
    except KeyError:
        check("LED remove absent raises", True)


def test_update_energy_flow() -> None:
    rule = {"rule_id": "TR-T", "template": "T1_scale_preserving_move", "branch": "RAW_BOUNDARY",
            "match": {"mode_is": "KEEP"},
            "consume": [{"type": "A"}], "produce": [dict(mk("A"))]}
    ev = {"mode": "KEEP", "side": "B", "splay_case": "LL"}
    out, tr = update_mod.update(ledger_state.add(ledger_state.empty(), mk("A")), ev, [rule])
    check("LED update applied", tr[0]["applied"] is True)
    out_a, _t = update_mod.update(ledger_state.add(ledger_state.empty(), mk("A")), ev, [rule])
    check("LED update deterministic",
          ledger_state.canonical(out) == ledger_state.canonical(out_a))
    check("LED update skips on no-match",
          update_mod.update(ledger_state.empty(), {"mode": "DELETE"}, [rule])[1][0]["applied"] is False)
    try:
        bad = dict(rule)
        bad["match"] = {"support_kind_is": "boundary"}
        update_mod.update(ledger_state.empty(), ev, [bad])
        check("LED credit-atom match rejected", False)
    except ValueError:
        check("LED credit-atom match rejected", True)
    check("LED energy exact", energy_mod.total(out, {"A": Fraction(3)}) == Fraction(3))
    check("LED lower bound", energy_mod.check_lower_bound(out, {"A": Fraction(3)}, Fraction(3)))
    check("LED flow clean", flow_mod.audit_flow(rule) == [])
    rule2 = dict(rule)
    rule2["produce"] = [dict(mk("A")), dict(mk("A"))]
    check("LED flow imbalance caught", flow_mod.audit_flow(rule2) != [])


if __name__ == "__main__":
    test_support()
    test_state_canonical()
    test_update_energy_flow()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
