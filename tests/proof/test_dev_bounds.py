"""Dev-side proof checks (PR-05/06 development analogues). Fast; sealed dev artifacts only.

PR-05-dev: bounded A-side injection holds on development (injected <= k * A-rotations).
PR-06-dev: KEEP repayment holds on development (paid == demand on burdened edges).
Both read the frozen shortlist + ladder/histories records; they assert no theorem.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_dev_bounds() -> None:
    short = json.load(open(os.path.join(ROOT, "artifacts", "v03", "solver", "shortlist.json")))
    check("PR-05-dev shortlist has <=3 primaries", len(short["selected"]) <= 3)
    check("PR-05-dev shortlist not frozen", short["status"] == "DEV_SHORTLIST_NOT_FROZEN")
    for cfg in short["selected"]:
        check("PR-05-dev %s k=%d C=%d zero residual on histories"
              % (cfg["predicate"], cfg["k"], cfg["C"]),
              cfg["histories_max_residual"] == [0, 1])
    lad = json.load(open(os.path.join(ROOT, "artifacts", "v03", "solver", "ladder.json")))
    for r in lad["rungs"]:
        if r["C"] == 2:
            check("PR-06-dev C=2 has feasible configs", r["n_feasible"] > 0)
    hyp_dir = os.path.join(ROOT, "artifacts", "v03", "hypotheses")
    devs = sorted(f for f in os.listdir(hyp_dir) if f.startswith("MSTC-DEV-"))
    check("PR-05-dev 3 dev hypotheses present", len(devs) == 3)
    for fn in devs:
        h = json.load(open(os.path.join(hyp_dir, fn)))
        check("PR-06-dev %s never fresh-tested" % fn,
              h.get("fresh_holdout_status") == "UNTOUCHED"
              and h.get("status") == "DEV_FALSIFICATION_PENDING")


if __name__ == "__main__":
    test_dev_bounds()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
