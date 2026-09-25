"""Solver backend tests (TR-03/04 mechanics). Fast; z3 + exact flow + certificates."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.solver import certify as certify_mod  # noqa: E402
from python.solver import encode_sat as sat_mod  # noqa: E402
from python.solver import flow as flow_mod  # noqa: E402
from python.solver import ilp as ilp_mod  # noqa: E402
from python.solver import smt as smt_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_sat_smt() -> None:
    s, pvars = sat_mod.new_solver()
    m = sat_mod.solve(s, pvars)
    check("TR-03 SAT proposes a predicate", m is not None and m["predicate"] in sat_mod.PREDICATES)
    for p in sat_mod.PREDICATES:
        sat_mod.block_predicate(s, pvars, p)
    check("TR-04 SAT UNSAT after full blocking", sat_mod.solve(s, pvars) is None)
    s2, los = smt_mod.new_solver()
    prop = smt_mod.propose(s2, los, set())
    check("TR-03 SMT proposes k>=0", prop is not None and prop[1] >= 0)


def test_flow() -> None:
    cap = {"s": {"a": 3, "b": 2}, "a": {"t": 2}, "b": {"t": 3}, "t": {}}
    check("TR-04 max-flow exact", flow_mod.max_flow(cap, "s", "t") == 4)
    bal = flow_mod.cycle_balance([{"side": "A", "rotations": 4, "regret_w": 0},
                                  {"side": "B", "rotations": 1, "regret_w": 6}], 1, 2)
    check("TR-04 required-k arithmetic", bal["required_k"] == 2 and not bal["feasible_at_k"])
    bal2 = flow_mod.cycle_balance([{"side": "A", "rotations": 4, "regret_w": 0},
                                   {"side": "B", "rotations": 1, "regret_w": 6}], 2, 2)
    check("TR-04 feasible at k=requirement", bal2["feasible_at_k"])
    bal0 = flow_mod.cycle_balance([{"side": "A", "rotations": 4, "regret_w": 0},
                                   {"side": "B", "rotations": 1, "regret_w": 0}], 0, 2)
    check("TR-04 zero demand feasible", bal0["feasible_at_k"] and bal0["required_k"] == 0)


def test_ilp_certify() -> None:
    calls = []
    k, log = ilp_mod.minimize_k("P", 2, lambda p, kk, c: (calls.append(kk) or kk >= 3, "t"))
    check("TR-04 ILP minimal k", k == 3 and len(log) == 4)
    check("TR-03 cert agreement gate",
          certify_mod.check_agreement(True, True, "t") == [])
    check("TR-03 cert disagreement caught",
          certify_mod.check_agreement(True, False, "t") != [])


if __name__ == "__main__":
    test_sat_smt()
    test_flow()
    test_ilp_certify()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
