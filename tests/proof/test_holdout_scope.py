"""WP-5 holdout-scope proof checks (PR analogues on fresh evidence, all exact).

PR-05-holdout: paid never exceeds injected on fresh episodes (conservation).
PR-06-holdout: PASS candidates show zero fresh residuals with null first violations.
PR-08-holdout: clean-room agreement holds on every checked episode.
PR-10-holdout: no finite premise — ceiling is finite-survival only, MST0-22/25 UNPROVED.
PR-11-holdout: frozen C values predate reveal and are record-bound integers.
PR-12-holdout: energy telescope sanity (0 <= paid <= injected; E bounded).
PR-14-holdout: no source-paper theorem imported as premise in frozen records.
"""
import json
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

FAILS: list = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _load(rel: str):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def test_scope() -> None:
    reveal = _load("artifacts/v03/holdouts/h3t_reveal.json")
    commit = _load("artifacts/v03/holdouts/candidate_set_commit.json")
    for res in reveal["results"]:
        paid = Fraction(*res["paid_total"])
        injected = Fraction(*res["injected_total"])
        check("PR-05-holdout %s paid<=injected on fresh" % res["calculus_id"],
              paid <= injected and injected >= 0)
        if res["verdict"] == "FRESH_H3T_PASS":
            check("PR-06-holdout %s zero fresh residuals" % res["calculus_id"],
                  res["max_residual"] == [0, 1] and res["first_violation"] is None)
    agreement = _load("artifacts/v03/cleanroom/agreement.json")
    check("PR-08-holdout clean-room agreement on all checks",
          agreement["disagreements"] == 0 and agreement["n_checks"] > 0)
    ceiling = _load("artifacts/v03/freeze/PHASE16_WP5_CEILING.json")
    check("PR-10-holdout ceiling is finite-survival only, never theorem",
          ceiling["ceiling"] in ("TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS",
                                 "FINITE_FALSIFICATION_NO_CEILING")
          and "theorem" not in ceiling["ceiling"].lower())
    for text_rel in ("math/theorem_MST22_constant_independence.md",
                     "math/theorem_MST25_holdout_scope.md"):
        text = open(os.path.join(ROOT, text_rel), encoding="utf-8").read()
        check("PR-10-holdout %s declares UNPROVED" % text_rel.split("/")[-1],
              "UNPROVED" in text)
    reveal_mtime = os.path.getmtime(os.path.join(
        ROOT, "artifacts", "v03", "holdouts", "h3t_reveal.json"))
    for m in commit["candidates"]:
        doc = _load("artifacts/v03/hypotheses/" + m["calculus_id"] + ".json")
        check("PR-11-holdout %s C record-bound integer" % m["calculus_id"],
              isinstance(doc["universal_constant_C"], int))
        check("PR-11-holdout %s frozen before reveal" % m["calculus_id"],
              os.path.getmtime(os.path.join(
                  ROOT, "artifacts", "v03", "hypotheses",
                  m["calculus_id"] + ".json")) < reveal_mtime)
        blob = json.dumps(doc, sort_keys=True)
        check("PR-14-holdout %s no imported source theorem" % m["calculus_id"],
              "QED" not in blob and "theorem_proved" not in blob
              and doc["proof_outline"][0]["status"] != "PROVED_UNIVERSAL")
    for res in reveal["results"]:
        paid = Fraction(*res["paid_total"])
        injected = Fraction(*res["injected_total"])
        check("PR-12-holdout %s energy telescope sanity" % res["calculus_id"],
              0 <= paid and paid <= injected)


if __name__ == "__main__":
    test_scope()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
