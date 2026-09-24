# Theorem MST07 — zig-zag / bend destruction accounting

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-07.REVIEW-PACKAGE.md`).
**Domain:** every synchronous KEEP zig-zag (LR/RL), all n, under the translated
bend definition.

## Statement
Every KEEP zig-zag destroys at least one bend (the turn node of the rotation).

## Proof
Take LR (RL mirrors): g has left child p, p has right child x. Ranks: x is the KEEP
key, hence A1-root with rank 0 (global minimum; MST0-05 setup).
Before: x lies in the subtrees of p and g, so m(p) = m(g) = 0; m(x) = rank(x) = 0.
Edge (g,p) heavy (0==0); edge (p,x) heavy (0==0). p's other child subtree excludes x,
so its min-rank exceeds 0 (only x attains rank 0) and edge (p,left) is light. Thus p
has exactly one heavy child edge, on the opposite side from its heavy parent edge:
p IS a bend before the rotation.
After (x rotated to triple root, p its left child): p's subtree excludes x, so
m(p-after) > 0 = m(x-after); edge (x,p) is light; p lacks a heavy parent edge and is
no longer a bend. At least one bend (p) is destroyed. The argument is fully general
in n, shapes, and surrounding ranks.

## Finite confirmation
816/816 zig-zags destroy ≥1 bend (all KEEP edges n≤5 exhaustive + 6,000 n6 samples);
2/2 on critical corpus. Zero violations.

## Scope limits
Destruction only — no claim about bends created elsewhere in the same splay, and no
claim that bend destruction pays any particular regret class (that is MST0-14/WP-6).
Ribless assumptions are not used and would be invalid here.
