# Theorem MST06 — zig-zig pairing decomposition: FALSE_AS_STATED + v2 conditional

**Status:** natural universal form FALSE_AS_STATED (witnesses preserved below);
replacement MST06v2 (conditional decomposition) PROVED (author claims; human review
pending — see `math/reviews/MST0-06.REVIEW-PACKAGE.md`).
**Domain:** every B zig-zig under the translated heap/pairing ontology.

## The kill (natural form)
Claim: every B zig-zig admits the three-consecutive-heap-children pairing
decomposition. Refuted as stated: on exhaustive small domains the rotation triple
systematically degenerates — R1 bottoms merged in 2,301/5,157 slots (44.6%), R2 host
components with <3 heap-children in 5,152/5,157 (99.9% at n≤6). Smallest witness
class: critical-corpus zig-zigs (85/115 DEGENERATE_merged), e.g. n=4 cycle 0 edge 0
(single LL, one heap component). The degeneracy is structural, not a bug: MST0-05
forces B paths all-heavy, so rotation triples typically live inside one component.
A universal pairing-transfer law cannot rest on triples that usually do not exist.

## Replacement MST06v2 (conditional, PROVED)
Claim: whenever a host component offers three consecutive heap-children around the
rotation site, the zig-zig decomposes into exactly two pairings with well-defined
GOOD/BAD/IMPORTANT/UNIMPORTANT classes. Proof: constructive (`decompose_zigzig` +
`classify_pairing` are total on valid triples; classes partition by definition).
Measured applicability: R2 triples engage in 692/1,491 zig-zigs at n=64 (46%) with
genuine GOOD=145/BAD=127 splits; IMPORTANT boundary pairings occur on corpus (30).
The v2 form is what WP-4 may consume, and only where triples exist.

## Scope limits
Neither form bounds transfer or proves repayment. The kill redirects Branch-A hopes
away from universal pairing transfer; it does not touch Pair Access itself.
