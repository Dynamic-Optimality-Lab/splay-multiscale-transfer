# Theorem MST08 — reference-rotation locality: FINITE BOUNDS PROVED, arbitrary-n OPEN

**Status:** SPLIT. Finite exhaustive bounds (n≤6) PROVED below. The arbitrary-n
bounded-modification claim is UNPROVED (proof sketch + gap recorded); it blocks
WP-4 locality-dependent consumption until proved (no fabrication).
Human review pending — see `math/reviews/MST0-08.REVIEW-PACKAGE.md`.
**Domain:** single A reference-tree rotations; translated heavy/lazy structure on a
fixed subject.

## Finite theorem (PROVED by exhaustive enumeration)
Over ALL single rotations of ALL trees n=4,5,6 (42+168+660 rotations): heavy-edge
flips ≤ 2, gap-sum change ≤ 2, heap-children membership changes (interval creations)
≤ 3. Machine-checked (`lemma_measurements.json`, `step_locality`). Adversarial
hill-climbing (mutate-the-best, 120 steps each at n=8/16/32/64, seeded) never exceeds
2 flips either (`test_wp2.py` WP2STRESS-HILL). The constant-2 ceiling at every scale
tested, plus even-valued maxima throughout, suggests a true O(1) bound with possible
parity structure — recorded as a proof lead, not a claim.

## Arbitrary-n conjecture (UNPROVED)
One reference rotation changes the translated structure through O(1) primitive
modifications. Sketch: a rotation permutes exactly three subtrees (A,B,C) with
uniform ±1 depth shifts per subtree; heavy flips require min-rank equality toggles,
which the interval-uniqueness structure restricts to the rotated neighborhood.
GAP (explicit): rank shifts propagate to min-rank values of ancestor intervals, and
the sketch does not yet bound equality toggles along ancestor chains in full
generality — measured max stays 2 through n=6 plus hill-climb evidence at scale
(see WP-2 stress), but that is evidence, not proof.

## Interval-level finite evidence
Heap-children membership changes per rotation ≤ 3 (n≤6 exhaustive); ≤ 4 per rotation
on critical corpus. The source's "O(1) new lazy intervals per rotation" shape holds
finitely; universally it inherits the conjecture's status.

## Scope limits
Nothing here bounds DELETE injection or proves transfer. WP-4 may consume the FINITE
bounds as development evidence only; any universal locality premise stays blocked.
