"""WP-5 stress battery: agreement, firewall pins, menu/C domains, determinism.

Fast (synthetic episodes only; the 70k-bank evaluation lives in run_phase15 and
is checked here via its sealed reveal record, never re-run).
"""
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.audit import cleanroom as cleanroom_mod  # noqa: E402
from python.freeze import candidates as freeze_mod  # noqa: E402
from python.holdout import h3t_evaluate as h3t_mod  # noqa: E402
from python.splay_ref.splay import build_balanced, serialize  # noqa: E402
from python.transfer import branchA as branchA_mod  # noqa: E402

FAILS: list = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _synthetic(seed: int, n: int = 8, length: int = 32) -> dict:
    rng = random.Random("WP5-STRESS:%d" % seed)
    T0 = build_balanced(list(range(1, n + 1)))
    shape = serialize(T0)
    hist = [("KEEP" if rng.random() < 0.7 else "DELETE", rng.randint(1, n))
            for _ in range(length)]
    return {"n": n, "init_shape": shape, "history": hist}


def test_agreement() -> None:
    """Primary vs dev evaluator vs clean-room agree exactly (3 paths, 1 math)."""
    for seed in (1, 2, 3, 4):
        ep = _synthetic(seed)
        rots, _sa, _sy = h3t_mod.episode_rotations(ep)
        dev_seq = {"id": "stress-%d" % seed, "rotations": [
            {"mode": r["mode"], "side": r["side"], "splay_case": r["splay_case"],
             "keys": r["keys"], "interval": r["interval"], "nkeys": r["nkeys"],
             "x": r["x"], "a_edge": r["a_edge"], "y_edge": r["y_edge"],
             "w_num": 0, "w_den": 1} for r in rots]}
        for pred_name, pred, k, c in (
                ("P_all", {"any_of": [{"mode_is": "KEEP"}, {"mode_is": "DELETE"}]}, 2, 2),
                ("P_keep", {"mode_is": "KEEP"}, 1, 6)):
            prim = h3t_mod.simulate(pred, k, c, rots)
            dev_r = branchA_mod.evaluate(pred_name, k, c, [dev_seq])
            check("WP5-AGREE seed=%d %s primary==dev (res %s)" % (seed, pred_name, prim["max_res"]),
                  [prim["max_res"].numerator, prim["max_res"].denominator]
                  == [dev_r["max_residual"][0], dev_r["max_residual"][1]]
                  and prim["feasible"] == dev_r["feasible"])
            clean = cleanroom_mod.simulate_episode(
                ep["n"], ep["init_shape"], ep["history"], pred_name, k, c)
            check("WP5-AGREE seed=%d %s primary==cleanroom" % (seed, pred_name),
                  [prim["max_res"].numerator, prim["max_res"].denominator]
                  == list(clean["max_res"])
                  and prim["feasible"] == clean["feasible"])


def test_firewall_pins() -> None:
    st = json.load(open(os.path.join(
        ROOT, "artifacts", "v03", "holdouts", "h3t_state.json"), encoding="utf-8"))
    check("WP5-FIREWALL H3T UNLOCKED_ONCE/1",
          st.get("state") == "UNLOCKED_ONCE" and st.get("unlock_count") == 1)
    h1 = json.load(open(os.path.join(ROOT, "parent", "V02_H1_FIREWALL.json"),
                        encoding="utf-8"))
    check("WP5-FIREWALL H1 still EMPTY", h1.get("state") == "EMPTY")
    h2r = json.load(open(os.path.join(ROOT, "parent", "V02_H2R_FIREWALL.json"),
                         encoding="utf-8"))
    check("WP5-FIREWALL H2R still COMMITTED/0",
          h2r.get("state") == "BANK_COMMITTED"
          and h2r.get("unlocks", h2r.get("unlock_count")) == 0)
    commit = json.load(open(os.path.join(
        ROOT, "artifacts", "v03", "holdouts", "candidate_set_commit.json"),
        encoding="utf-8"))
    check("WP5-FREEZE 3 frozen members", len(commit["candidates"]) == 3)
    check("WP5-FREEZE firewall hash matches commitment",
          st.get("candidate_set_hash") == commit["set_hash"])


def test_domains() -> None:
    for bad in (("P_never", 1, 2), ("P_zigzig", 1, 2), ("P_all", 7, 2),
                ("P_all", 1, 1), ("P_all", -1, 2)):
        try:
            freeze_mod.build_frozen("MSTC-MUT", "MSTC-DEV-0001", *bad)
            check("WP5-DOMAIN refuses %r" % (bad,), False)
        except ValueError:
            check("WP5-DOMAIN refuses %r" % (bad,), True)
    try:
        h3t_mod.episode_rotations({"n": 3, "init_shape": "(2(1..)(3..))",
                                   "history": [("KEEP", 99)]})
        check("WP5-DOMAIN bad key raises", False)
    except KeyError:
        check("WP5-DOMAIN bad key raises", True)
    ep = _synthetic(9)
    rots, _sa, _sy = h3t_mod.episode_rotations(ep)
    pred = {"any_of": [{"mode_is": "KEEP"}, {"mode_is": "DELETE"}]}
    r1 = h3t_mod.simulate(pred, 2, 2, rots)
    r2 = h3t_mod.simulate(pred, 2, 2, rots)
    check("WP5-DETERMINISM repeated simulate agrees", r1 == r2)


if __name__ == "__main__":
    test_agreement()
    test_firewall_pins()
    test_domains()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
