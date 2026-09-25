# Theorem MST0-17 — universal block inequalities imply constant-factor Pair Access

**Status:** BLOCKED — prerequisites MST0-13 (PROVED, awaiting human review),
MST0-14 (UNPROVED), MST0-15 (UNPROVED) are not all REVIEWED. See
`math/reviews/MST0-17.BLOCKED`. No proof is attempted while blocked; this
record must never be consumed (BLOCKED forbids consumption).

## Blocked-by

- MST0-13 bounded DELETE injection: author-claim PROVED, review pending.
- MST0-14 synchronous KEEP repayment: UNPROVED (sibling fresh falsifications).
- MST0-15 integrability: UNPROVED.

## What unblocking requires

REVIEWED verdicts on MST0-13/14/15, then a block-composition proof of
`Splay(Y,T) + E_m − E_0 <= C·Splay(X,T) + A(n)` with `A(n) = 0` preferred
(bounded `O(n)` only if bridge-compatible and audited), universal C
independent of n/length/tree/holdout/panel (MST0-22, PR-11), covering every
legal paired execution exactly once per the REVIEWED block partition
(MST0-16). None of this is claimed in the current seal.
