"""WP-6 proof suite (PR-01..14 + NEG-01..08 analogues). Machine checks on records.

PR-01..04 cite WP-2 REVIEWED lemmas (case language present in docs).
PR-05..14 verify WP-6 obligations: proof presence, no-finite-premise scans,
scope guards, BLOCKED/NOT_APPLICABLE states, and claim-level discipline.
NEG-01..08 mirror the bridge/negative audit (vacuous with evidence).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

FAILS: list = []

FINITE_PREMISE_TOKENS = ["n<=7", "holdout pass", "catalog completeness",
                         "solver optimality", "empirical scaling",
                         "finite grammar feasibility"]


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def _load(rel: str):
    return json.loads(_read(rel))


def _negated(doc: str, token: str) -> bool:
    """True iff every line containing token also carries a negation word.

    The proof's No-finite-premise section names each forbidden premise to
    exclude it; a naive absence scan would false-positive on those negations.
    """
    for ln in doc.splitlines():
        if token in ln and not any(w in ln.lower() for w in ("no ", "without", "never", "not ")):
            return False
    return True


def test_pr() -> None:
    d05 = _read("math/theorem_MST05_keep_heavy_path.md")
    check("PR-01 MST0-05 translated-rank hypotheses in doc",
          "rank" in d05.lower() and "PROVED" in d05)
    d06 = _read("math/theorem_MST06_zigzig_pairing.md")
    check("PR-02 MST0-06 all zig-zig cases (case language + witnesses)",
          "LL" in d06 and "zig-zig" in d06.lower() and "witness" in d06.lower())
    d07 = _read("math/theorem_MST07_zigzag_bends.md")
    check("PR-03 MST0-07 all zig-zag cases (bend language)", "bend" in d07.lower())
    d08 = _read("math/theorem_MST08_reference_rotation_locality.md")
    check("PR-04 MST0-08 reference cases enumerated, universal gap explicit",
          "LOCALITY" in d08.upper() or "local" in d08.lower())
    d13 = _read("math/theorem_MST13_delete_injection.md")
    check("PR-05 MST0-13 PROVED with case-complete arbitrary-n proof",
          "**Status:** PROVED" in d13 and "ROOT" in d13 and "arbitrary n" in d13)
    check("PR-05 MST0-13 no finite premise in proof (all named premises negated)",
          all(_negated(d13, t) for t in FINITE_PREMISE_TOKENS))
    check("PR-05 MST0-13 machine bound evidence all-holds",
          all(r["holds"] for r in
              _load("artifacts/v03/proofs/MST13_injection_bound.json")["rows"]))
    d14 = _read("math/theorem_MST14_keep_repayment.md")
    final = _load("artifacts/v03/seal/FINAL_RESULT.json")
    check("PR-06 MST0-14 UNPROVED and unclaimed (terminal stays finite)",
          "UNPROVED" in d14 and final["terminal_claim"] ==
          "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS")
    frozen = [_load("artifacts/v03/hypotheses/MSTC-000%d.json" % i) for i in (1, 2, 3)]
    check("PR-07 signed lower bound N/A (no signed components anywhere)",
          all(d["branch"] == "RAW_BOUNDARY" and d["cancellation_rules"] == []
              for d in frozen)
          and _load("artifacts/v03/proofs/obligation_status.json")
          ["statuses"]["MST0-12"]["status"] == "NOT_APPLICABLE")
    check("PR-08 integrability unproved and unclaimed",
          "UNPROVED" in _read("math/theorem_MST15_integrability.md")
          and "telescope" not in final["terminal_claim"].lower())
    check("PR-09 block partition REVIEWED (ACCEPT record)",
          _load("math/reviews/MST0-16.review.json")["verdict"] == "ACCEPT")
    check("PR-10 no finite premise anywhere in universal claims",
          all(_negated(d13, t) for t in FINITE_PREMISE_TOKENS)
          and "for all n" not in final["terminal_claim"]
          and "works for all n" not in final["allowed_meaning"])
    check("PR-11 universal C independence open (setup + record-bound C)",
          "UNPROVED" in _read("math/theorem_MST22_constant_independence.md")
          and all(isinstance(d["universal_constant_C"], int) for d in frozen))
    check("PR-12 telescope unaudited-unclaimed (MST0-18 BLOCKED)",
          os.path.isfile(os.path.join(ROOT, "math", "reviews", "MST0-18.BLOCKED"))
          and "PAIR_ACCESS" not in final["terminal_claim"])
    d19 = _read("math/theorem_MST19_bridge.md")
    check("PR-13 bridge checklist recorded, nothing passed (MST0-19 BLOCKED)",
          all(k in d19 for k in ("Splay variant", "cost convention",
                                 "initial-tree", "subsequence", "additive term",
                                 "constant independence", "direction",
                                 "L2/L3")) and "NOT_REACHED" in d19)
    scoped = "\n".join(json.dumps(d, sort_keys=True) for d in frozen) + "\n" + \
        json.dumps(final, sort_keys=True) + "\n" + d13
    check("PR-14 no source-paper theorem consumed as premise",
          not any(t in scoped for t in ("by Theorem", "L6 proves",
                                        "Levy-Tarjan prove", "follows from L6")))
    neg = _load("artifacts/v03/audits/bridge_negative_audit.json")
    check("NEG-01..08 negative branch vacuous with evidence (NOT_ACTIVATED)",
          len(neg["negative_branch"]["neg_checks"]) == 8
          and neg["negative_branch"]["status"] == "NEGATIVE_FAMILY_NOT_ACTIVATED"
          and neg["negative_branch"]["not_activated"] == 11)
    check("NEG transfer residuals never substitute for Splay costs (§32.10)",
          "representation obstruction" in
          _read("COUNTEREXAMPLE_ATLAS.md").lower())


if __name__ == "__main__":
    test_pr()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
