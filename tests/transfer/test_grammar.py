"""Transfer-grammar test suite (TR mechanics). Fast; no synthesis."""
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.transfer import branches as branches_mod  # noqa: E402
from python.transfer import complexity as complexity_mod  # noqa: E402
from python.transfer import grammar as grammar_mod  # noqa: E402
from python.transfer import templates_T1_T10 as templates_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def prod(t="T"):
    """Minimal valid produce template."""
    return {"type": t, "support": ("key", 1), "scale": ("S0", 0),
            "mass": Fraction(1), "provenance": "A_ROTATION_CREATED"}


def test_templates() -> None:
    grammar, _h = grammar_mod.load()
    check("TR-01 ten templates preregistered", len(templates_mod.TEMPLATES) == 10)
    for i, template in enumerate(templates_mod.TEMPLATES):
        short = template.split("_")[0]
        branch = "SIGNED_MULTISCALE" if short == "T9" else "RAW_BOUNDARY"
        rule = templates_mod.make_rule("TR-T-%02d" % i, template, branch,
                                       {"mode_is": "KEEP"}, [{"type": "T"}], [prod()])
        if grammar_mod.validate_rule(rule, grammar) or complexity_mod.audit_rule(rule):
            check("TR-02 template %s clean" % short, False)
        else:
            check("TR-02 template %s clean" % short, True)
    try:
        templates_mod.make_rule("X", "T99_nope", "RAW_BOUNDARY", {"mode_is": "KEEP"})
        check("TR-02 unknown template rejected", False)
    except ValueError:
        check("TR-02 unknown template rejected", True)


def test_branches() -> None:
    check("TR-12 Branch A allows T1 unsigned", branches_mod.branch_allows("RAW_BOUNDARY", "T1", False))
    check("TR-12 Branch A rejects T9", not branches_mod.branch_allows("RAW_BOUNDARY", "T9", False))
    check("TR-12 Branch A rejects signed", not branches_mod.branch_allows("RAW_BOUNDARY", "T1", True))
    check("TR-12 Branch B allows T9", branches_mod.branch_allows("SIGNED_MULTISCALE", "T9", True))
    check("TR-12 Branch B blocked pre-rejection",
          branches_mod.activate_branch_B(None) == "BLOCKED")
    check("TR-12 Branch B blocked incomplete record",
          branches_mod.activate_branch_B({"grammar_version": "x"}) == "BLOCKED")


def test_complexity() -> None:
    wide = templates_mod.make_rule("TR-W", "T2_upward_scale_transfer", "RAW_BOUNDARY",
                                   {"mode_is": "KEEP"}, [], [prod("T%d" % i) for i in range(9)])
    check("TR-14 over-wide caught", complexity_mod.audit_rule(wide) != [])
    evil = templates_mod.make_rule("TR-E", "T1_scale_preserving_move", "RAW_BOUNDARY",
                                   {"mode_is": "KEEP"}, [{"type": "FUTURE_COINS"}], [prod()])
    check("TR-14 target input caught", complexity_mod.audit_rule(evil) != [])
    litkey = templates_mod.make_rule("TR-K", "T1_scale_preserving_move", "RAW_BOUNDARY",
                                     {"mode_is": "KEEP", "access_key": 4}, [], [prod()])
    check("TR-14 literal key caught", complexity_mod.audit_rule(litkey) != [])
    agg = templates_mod.make_rule("TR-A", "T3_downward_scale_split", "RAW_BOUNDARY",
                                  {"mode_is": "KEEP"}, [], [prod("T%d" % i) for i in range(9)])
    agg["aggregate_proof_ref"] = "math/theorem_MST15_integrability.md#aggregate"
    check("TR-14 aggregate proof excuses width", complexity_mod.audit_rule(agg) == [])


if __name__ == "__main__":
    test_templates()
    test_branches()
    test_complexity()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
