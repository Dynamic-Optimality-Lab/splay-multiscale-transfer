"""Active-predicate language (PHASE 07): finite structural predicate combinators.

Atoms evaluate (credit, event) pairs using ONLY declared local/aggregate structural
relations: mode/case/side equality, scale equality, support-kind equality, mass
thresholds. Only the ATOMS set below exists -- the constructor rejects unknown atom
names, so non-structural predicates cannot be expressed.
Named-predicate registry is append-only with new-ID discipline (WP-5 populates).
Console tag [WP3-STEP-01].
"""
from __future__ import annotations

from fractions import Fraction

ATOMS = {"mode_is", "case_is", "side_is", "scale_eq", "support_kind_is", "mass_gte"}
EVENT_ATOMS = {"mode_is", "case_is", "side_is"}
CREDIT_ATOMS = {"scale_eq", "support_kind_is", "mass_gte"}


def check_event_predicate(pred: dict) -> None:
    """Validate an update-time rule match: event atoms only.

    Credit atoms (support/scale/mass) are repayment-time predicates evaluated
    against actual ledger credits in WP-5+; they are forbidden in update-time
    rule matches (a match with no credit to evaluate against is meaningless).
    """
    check_predicate(pred)

    def walk(node: dict) -> None:
        op, arg = next(iter(node.items()))
        if op in ("all_of", "any_of"):
            for sub in arg:
                walk(sub)
        elif op == "not":
            walk(arg)
        elif op in CREDIT_ATOMS:
            raise ValueError("credit atom %r forbidden in update-time rule match" % op)
        elif op not in EVENT_ATOMS:
            raise ValueError("unknown atom %r" % (op,))

    walk(pred)


def check_predicate(pred: dict) -> None:
    """Validate a predicate tree (raises on unknown atoms or malformed nodes)."""
    if not isinstance(pred, dict) or len(pred) != 1:
        raise ValueError("predicate node must be a single-key dict")
    op, arg = next(iter(pred.items()))
    if op in ("all_of", "any_of"):
        if not (isinstance(arg, list) and arg):
            raise ValueError("combinator needs a non-empty list")
        for sub in arg:
            check_predicate(sub)
    elif op == "not":
        check_predicate(arg)
    elif op in ATOMS:
        if not isinstance(arg, (str, int, list)):
            raise ValueError("atom argument must be str/int/list")
    else:
        raise ValueError("unknown predicate operator %r (outside the structural atom language)" % (op,))


def evaluate(pred: dict, credit: dict, event: dict) -> bool:
    """Evaluate a validated predicate on (credit, event). Pure function."""
    check_predicate(pred)
    op, arg = next(iter(pred.items()))
    if op == "all_of":
        return all(evaluate(sub, credit, event) for sub in arg)
    if op == "any_of":
        return any(evaluate(sub, credit, event) for sub in arg)
    if op == "not":
        return not evaluate(arg, credit, event)
    if op == "mode_is":
        return event.get("mode") == arg
    if op == "case_is":
        return event.get("splay_case") == arg
    if op == "side_is":
        return event.get("side") == arg
    if op == "scale_eq":
        return list(credit.get("scale", [])) == list(arg)
    if op == "support_kind_is":
        sup = credit.get("support", ())
        return bool(sup) and sup[0] == arg
    if op == "mass_gte":
        return credit.get("mass", Fraction(0)) >= Fraction(arg)
    raise AssertionError("unreachable")


REGISTRY: dict[str, dict] = {}


def register(name: str, pred: dict) -> None:
    """Append-only named-predicate registration (re-registration forbidden)."""
    if name in REGISTRY:
        raise ValueError("predicate ID %r exists; edits require a new ID" % name)
    check_predicate(pred)
    REGISTRY[name] = pred
