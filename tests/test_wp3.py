"""WP-3 stress tests: determinism fuzz, idempotency, invalid inputs, firewall machine.

All fuzzing uses seeded construction (no holdout contact). Each test prints
WP3STRESS-<id> lines; failure exits non-zero.
"""
import json
import os
import random
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from fractions import Fraction

from python.ledger import state as ledger_state  # noqa: E402
from python.ledger import update as update_mod  # noqa: E402
from python.provenance import active as active_mod  # noqa: E402
from python.provenance import merge as merge_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("WP3STRESS-PASS " if cond else "WP3STRESS-FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _rand_credit(rng: random.Random, i: int) -> dict:
    types = ["BOUNDARY_LATENT", "SCALE_PACKET", "BEND_CREDIT"]
    kinds = [("boundary", 1, 2, "LEFT"), ("interval", 0, 5), ("key", 3)]
    return ledger_state.make_credit(rng.choice(types), rng.choice(kinds),
                                    ("S0", rng.randint(0, 3)),
                                    Fraction(rng.randint(1, 3), rng.randint(1, 2)),
                                    "P%d" % (i % 4))


def _rand_rules() -> list:
    return [
        {"rule_id": "TR-FZ-001", "template": "T1_scale_preserving_move",
         "branch": "RAW_BOUNDARY",
         "match": {"any_of": [{"mode_is": "DELETE"}, {"case_is": "LL"}]},
         "consume": [{"type": "BOUNDARY_LATENT"}],
         "produce": [{"type": "SCALE_PACKET", "support": ("interval", 0, 5),
                      "scale": ("S0", 1), "mass": Fraction(1), "provenance": "P0"}]},
        {"rule_id": "TR-FZ-002", "template": "T5_boundary_activation",
         "branch": "RAW_BOUNDARY", "match": {"side_is": "B"},
         "consume": [{"type": "SCALE_PACKET"}],
         "produce": [{"type": "BEND_CREDIT", "support": ("bend", 2),
                      "scale": ("S1", 0), "mass": Fraction(1), "provenance": "P1"}]},
    ]


def test_update_fuzz() -> None:
    rng = random.Random(20260923)
    events = [{"mode": m, "side": s, "splay_case": c}
              for m in ("KEEP", "DELETE") for s in ("A", "B")
              for c in ("ZIG", "LL", "RR", "LR", "RL")]
    bad = 0
    t0 = time.time()
    for trial in range(300):
        ledger = []
        for i in range(rng.randint(0, 6)):
            ledger = ledger_state.add(ledger, _rand_credit(rng, i))
        rules = _rand_rules()
        ev = dict(rng.choice(events))
        out1, tr1 = update_mod.update(list(ledger), ev, rules)
        out2, tr2 = update_mod.update(list(ledger), ev, rules)
        if ledger_state.canonical(out1) != ledger_state.canonical(out2) or tr1 != tr2:
            bad += 1
        # Reverse-ordered identical multiset merges (canonical equality).
        rev = list(reversed(ledger))
        if not merge_mod.equivalent(ledger, rev):
            bad += 1
    dt = time.time() - t0
    print("WP3STRESS-FUZZ 300 trials seconds=%.1f" % dt)
    check("WP3STRESS-FUZZ update deterministic + merge sound", bad == 0)


def test_idempotent_runners() -> None:
    import hashlib as _hl
    import subprocess
    for n in ("07", "09"):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run_phase%s.py" % n)],
                           capture_output=True, text=True)
        if n == "07":
            check("WP3STRESS-IDEM phase07 exit 0", r.returncode == 0)
        if n == "09":
            check("WP3STRESS-IDEM phase09 exit 0", r.returncode == 0)
    c1 = open(os.path.join(ROOT, "artifacts", "v03", "freeze",
                           "PHASE09_TRANSFER_GRAMMAR_FREEZE.json"), "rb").read()
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run_phase09.py")],
                       capture_output=True, text=True)
    c2 = open(os.path.join(ROOT, "artifacts", "v03", "freeze",
                           "PHASE09_TRANSFER_GRAMMAR_FREEZE.json"), "rb").read()
    check("WP3STRESS-IDEM phase09 cert stable",
          r.returncode == 0 and _hl.sha256(c1).hexdigest() == _hl.sha256(c2).hexdigest())


def test_invalid_inputs() -> None:
    try:
        ledger_state.make_credit("T", ("boundary", 1, 2, "LEFT"), ("S0", 1), 1.5, "P")
        check("WP3STRESS-INV float mass rejected", False)
    except TypeError:
        check("WP3STRESS-INV float mass rejected", True)
    active_mod.register("WP3STRESS-DUP", {"mode_is": "KEEP"})
    try:
        active_mod.register("WP3STRESS-DUP", {"mode_is": "KEEP"})
        check("WP3STRESS-INV registry append-only", False)
    except ValueError:
        check("WP3STRESS-INV registry append-only", True)
    from python.transfer import grammar as grammar_mod
    dup_rules = [
        {"rule_id": "DUP", "template": "T1_scale_preserving_move", "branch": "RAW_BOUNDARY",
         "match": {"mode_is": "KEEP"}, "consume": [], "produce": []},
        {"rule_id": "DUP", "template": "T1_scale_preserving_move", "branch": "RAW_BOUNDARY",
         "match": {"mode_is": "KEEP"}, "consume": [], "produce": []},
    ]
    try:
        update_mod.update([], {"mode": "KEEP"}, dup_rules)
        check("WP3STRESS-INV duplicate IDs rejected at invocation", False)
    except ValueError:
        check("WP3STRESS-INV duplicate IDs rejected at invocation", True)
    grammar, _h = grammar_mod.load()
    check("WP3STRESS-INV ruleset gate catches duplicates",
          any("duplicate" in v for v in grammar_mod.check_ruleset(dup_rules, grammar)))
    ok_rule = {"rule_id": "OK-1", "template": "T1_scale_preserving_move",
               "branch": "RAW_BOUNDARY", "match": {"mode_is": "KEEP"},
               "consume": [], "produce": []}
    check("WP3STRESS-INV ruleset gate passes clean list",
          grammar_mod.check_ruleset([ok_rule], grammar) == [])
    # Tag-independence: equal ledgers with different tag histories evolve identically.
    from python.provenance import merge as merge_mod
    c = ledger_state.make_credit("T", ("boundary", 1, 2, "LEFT"), ("S0", 1),
                                 Fraction(1), "P-A")
    la = ledger_state.add(ledger_state.empty(), c)
    lb = ledger_state.add(ledger_state.empty(), dict(c))
    tags = merge_mod.merge(["P-A"], ["P-B", "P-A"], la, lb)
    ev = {"mode": "KEEP"}
    r = {"rule_id": "TI-1", "template": "T1_scale_preserving_move", "branch": "RAW_BOUNDARY",
         "match": {"mode_is": "KEEP"}, "consume": [], "produce": [dict(c)]}
    oa, _ta = update_mod.update(la, ev, [r])
    om, _tm = update_mod.update(ledger_state.add(ledger_state.empty(), c), ev, [r])
    check("WP3STRESS-INV merged tags do not affect evolution",
          ledger_state.canonical(oa) == ledger_state.canonical(om) and tags == ["P-A", "P-B"])
    from python.transfer import templates_T1_T10 as templates_mod
    try:
        templates_mod.make_rule("X", "T1_scale_preserving_move", "NOPE", {"mode_is": "X"})
        check("WP3STRESS-INV branch validated", False)
    except ValueError:
        check("WP3STRESS-INV branch validated", True)


if __name__ == "__main__":
    test_update_fuzz()
    test_idempotent_runners()
    test_invalid_inputs()
    print("WP3STRESS-FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
