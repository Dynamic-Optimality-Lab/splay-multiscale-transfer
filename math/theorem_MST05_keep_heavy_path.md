# Theorem MST05 — KEEP heavy-path characterization (translated rank)

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-05.REVIEW-PACKAGE.md`).
**Domain:** every synchronous KEEP edge, all n, under `KEEP_REF_SNAPSHOT-v1` and the
translated min-rank-equality heavy rule.

## Statement
Every edge of the B access path is heavy after the A splay.

## Proof
Let x be the KEEP key. The A splay puts x at the root of A1, so rank(x) = 0, the
global minimum. For any node v on the B access path to x, x lies in v's B-subtree,
hence m(v) = 0 (m = subtree min-rank). The same holds for v's B-parent u on the
path. The heavy rule marks (u,v) heavy iff m(u) == m(v); here 0 == 0. Therefore
every B-path edge is heavy. The argument uses only the SAME-transplanted rank
(depth-in-reference) and rule; no tie case arises (both sides attain 0, which IS
the heavy condition, not a tie between children).

## Finite confirmation
27,876/27,876 B-path edges heavy (all KEEP edges n≤5 exhaustive + 6,000 n6 samples);
13,022/13,022 more on generated histories (n16/32/64); 140/140 on critical corpus.
Zero light edges anywhere measured.

## Scope limits
Applies to the B access path of KEEP edges under the frozen reference convention.
Says nothing about off-path edges, DELETE analysis, or transfer bounds.
