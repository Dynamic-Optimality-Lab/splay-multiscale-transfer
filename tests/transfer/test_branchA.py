"""Transfer candidate tests (TR synthesis mechanics). Fast; fixtures + tiny corpora."""
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.solver import certify as certify_mod  # noqa: E402
from python.transfer import branchA as branchA_mod  # noqa: E402
from python.transfer import ladder as ladder_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def tiny_corpus():
    """Two-sequence toy corpus (independent of sealed development data)."""
    return {"sequences": [
        {"id": "t-del", "rotations": [
            {"mode": "DELETE", "side": "A", "splay_case": "LL", "keys": [1, 2],
             "interval": [1, 2], "nkeys": 2, "x": 1, "a_edge": 0, "y_edge": 0}]},
        {"id": "t-keep", "rotations": [
            {"mode": "KEEP", "side": "A", "splay_case": "ZIG", "keys": [1, 2],
             "interval": [1, 2], "nkeys": 2, "x": 2, "a_edge": 0, "y_edge": 0},
            {"mode": "KEEP", "side": "B", "splay_case": "ZIG", "keys": [1, 2],
             "interval": [1, 2], "nkeys": 2, "x": 2, "a_edge": 1, "y_edge": 3}]},
    ]}


def test_candidate_semantics() -> None:
    corpus = tiny_corpus()
    # w = 3 - 2*1 = 1 at C=2; k=1 injects 1 per A-rotation (2 A-rotations here).
    v = branchA_mod.evaluate("P_all", 1, 2, corpus)
    r = certify_mod.replay_candidate("P_all", 1, 2, corpus)
    check("TR-05 engine feasible toy", v["feasible"])
    check("TR-05 replay agrees toy", v["feasible"] == r["feasible"]
          and v["max_residual"] == r["max_residual"])
    v0 = branchA_mod.evaluate("P_never", 6, 2, corpus)
    check("TR-06 no-activation fails with burden", not v0["feasible"])
    check("TR-06 residual exact", v0["max_residual"] == [1, 1])
    # Monotonicity in k on the toy (larger k never increases residuals).
    res = [branchA_mod.evaluate("P_all", k, 2, corpus)["max_residual"] for k in range(4)]
    check("TR-06 monotone in k", all(res[i] >= res[i + 1] for i in range(3)))
    # fail_fast preserves verdict + first witness.
    vf = branchA_mod.evaluate("P_never", 6, 2, corpus, fail_fast=True)
    check("TR-06 fail_fast same verdict", vf["feasible"] == v0["feasible"]
          and vf["first_violation"] == v0["first_violation"])


def test_ladder_format() -> None:
    check("TR-08 ladder has 10 rungs", ladder_mod.LADDER == (2, 3, 4, 6, 8, 12, 16, 24, 32, 64))


if __name__ == "__main__":
    test_candidate_semantics()
    test_ladder_format()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
