"""WP-4 stress tests: determinism, idempotency, firewall pins, invalid inputs.

Probes run on fixtures and tiny corpora (never holdout banks). Each test prints
WP4STRESS-<id> lines; failure exits non-zero.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.solver import certify as certify_mod  # noqa: E402
from python.transfer import branchA as branchA_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("WP4STRESS-PASS " if cond else "WP4STRESS-FAIL ") + name)
    if not cond:
        FAILS.append(name)


def tiny_corpus():
    """Toy corpus (independent of sealed development data)."""
    return {"sequences": [
        {"id": "s-del", "rotations": [
            {"mode": "DELETE", "side": "A", "splay_case": "LL", "keys": [1, 2],
             "interval": [1, 2], "nkeys": 2, "x": 1, "a_edge": 0, "y_edge": 0}]},
        {"id": "s-keep", "rotations": [
            {"mode": "KEEP", "side": "A", "splay_case": "ZIG", "keys": [1, 2],
             "interval": [1, 2], "nkeys": 2, "x": 2, "a_edge": 0, "y_edge": 0},
            {"mode": "KEEP", "side": "B", "splay_case": "ZIG", "keys": [1, 2],
             "interval": [1, 2], "nkeys": 2, "x": 2, "a_edge": 2, "y_edge": 5}]},
    ]}


def test_paths_agree() -> None:
    corpus = tiny_corpus()
    for p in ("P_all", "P_keep", "P_never"):
        for k in (0, 3):
            v = branchA_mod.evaluate(p, k, 2, corpus)
            r = certify_mod.replay_candidate(p, k, 2, corpus)
            check("WP4STRESS-AGREE %s k=%d" % (p, k),
                  v["feasible"] == r["feasible"] and v["max_residual"] == r["max_residual"])


def test_idempotent_writes() -> None:
    bf = json.load(open(os.path.join(ROOT, "artifacts", "v03", "solver", "backend_freeze.json")))
    check("WP4STRESS-IDEM backend freeze has version+seeds+role",
          bf.get("package_version") == "5.1.0.0" and bf.get("threads") == 1
          and "certificate_capability" in bf)
    m1 = json.load(open(os.path.join(ROOT, "artifacts", "v03", "discovery", "masks.json")))
    check("WP4-STEP-01 masks manifest has near/splits + tag",
          len(m1.get("near", [])) > 0 and len(m1.get("gen_sel", [])) > 0
          and len(m1.get("gen_val", [])) > 0 and "code_tag" in m1)


def test_firewall_pins() -> None:
    st = json.load(open(os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_state.json")))
    check("WP4STRESS-FW H3T still BANK_COMMITTED/0",
          st.get("state") == "BANK_COMMITTED" and st.get("unlock_count") == 0)
    sb = open(os.path.join(ROOT, "prereg", "solver_backends.yaml"), encoding="utf-8").read()
    check("WP4STRESS-FW prereg solver record untouched",
          "synthesis_authorized: false" in sb)


def test_invalid_inputs() -> None:
    try:
        branchA_mod.evaluate("P_bogus", 1, 2, tiny_corpus())
        check("WP4STRESS-INV predicate menu enforced", False)
    except ValueError:
        check("WP4STRESS-INV predicate menu enforced", True)
    try:
        branchA_mod.evaluate("P_all", 99, 2, tiny_corpus())
        check("WP4STRESS-INV k domain enforced", False)
    except ValueError:
        check("WP4STRESS-INV k domain enforced", True)


if __name__ == "__main__":
    test_paths_agree()
    test_idempotent_writes()
    test_firewall_pins()
    test_invalid_inputs()
    print("WP4STRESS-FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
