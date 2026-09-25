"""Adversary engine tests (determinism + interface contracts). Fast; small sizes."""
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.adversary import anneal as anneal_mod  # noqa: E402
from python.adversary import generators as gen_mod  # noqa: E402
from python.adversary import generalize as generalize_mod  # noqa: E402
from python.adversary import genetic as genetic_mod  # noqa: E402
from python.adversary import hillclimb as hillclimb_mod  # noqa: E402
from python.adversary import inflate as inflate_mod  # noqa: E402
from python.adversary import neighborhood as neighborhood_mod  # noqa: E402
from python.adversary import splice as splice_mod  # noqa: E402
from python.splay_ref.splay import build_balanced  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def const_obj(history):
    """Constant objective (tests determinism, not search quality)."""
    return 0


def test_determinism() -> None:
    h1 = gen_mod.build_history(random.Random(7), 8, "RANDOM_LEGAL", 16)
    h2 = gen_mod.build_history(random.Random(7), 8, "RANDOM_LEGAL", 16)
    check("ADV determinism generators", h1 == h2)
    r1 = hillclimb_mod.hillclimb(8, "RANDOM_LEGAL", 16, 10, 11, const_obj)
    r2 = hillclimb_mod.hillclimb(8, "RANDOM_LEGAL", 16, 10, 11, const_obj)
    check("ADV determinism hillclimb", r1["best"] == r2["best"])
    r1 = anneal_mod.anneal(8, "RANDOM_LEGAL", 16, 10, 12, const_obj)
    r2 = anneal_mod.anneal(8, "RANDOM_LEGAL", 16, 10, 12, const_obj)
    check("ADV determinism anneal", r1["best"] == r2["best"])
    r1 = genetic_mod.genetic(8, "RANDOM_LEGAL", 16, 3, 4, 13, const_obj)
    r2 = genetic_mod.genetic(8, "RANDOM_LEGAL", 16, 3, 4, 13, const_obj)
    check("ADV determinism genetic", r1["best"] == r2["best"])
    n1 = neighborhood_mod.neighborhood(h1, 8, 4, 14)
    n2 = neighborhood_mod.neighborhood(h1, 8, 4, 14)
    check("ADV determinism neighborhood", n1 == n2)


def test_interfaces() -> None:
    T0 = build_balanced([1, 2, 3, 4])
    r = gen_mod.actual_ratio([("KEEP", 2), ("DELETE", 1)], T0, 4)
    check("ADV actual ratio exact", r["sum_a"] >= r["sum_b"] >= 0 and r["ratio"][1] > 0)
    cyc = {"edges": [{"key": 1}, {"key": 2}]}
    check("ADV inflate cycle", inflate_mod.inflate_cycle(cyc, 3) == [("KEEP", 1), ("KEEP", 2)] * 3)
    check("ADV inflate burst", inflate_mod.inflate_burst([("DELETE", 1)], 3) == [("DELETE", 1)] * 3)
    check("ADV splice", splice_mod.splice([cyc], [3], 4) == [("KEEP", 1), ("KEEP", 2), ("DELETE", 3)])
    g = generalize_mod.generalize({"histories": [], "construction": "", "diagonal": False},
                                  {"grows": False, "replayed": True})
    check("ADV N1-N5 fail-closed", g["status"] == "NEGATIVE_FAMILY_NOT_ACTIVATED")


if __name__ == "__main__":
    test_determinism()
    test_interfaces()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
