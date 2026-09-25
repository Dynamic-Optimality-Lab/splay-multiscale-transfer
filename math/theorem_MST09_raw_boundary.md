# Theorem MST09 — raw boundary-damage law: CONJECTURE RECORD (development evidence)

**Status:** UNPROVED — finite development survival, explicitly not a theorem. No review
verdict is requested in WP-4. First consumer WP-6 requires REVIEWED before any
theorem-facing use.
**Domain:** the frozen development corpus (critical cycles n4-6 ×3, near-critical
selection, generated selection histories) at the stated diagnostic constants.

## Conjecture (to be proved in WP-6 or refuted by fresh evidence)
A nonnegative raw-boundary ledger (LATENT/ACTIVE boundary credits, T7 injection ≤ k
per A-rotation, T5 activation by frozen predicate, T6 repayment) with
(P_all, k≥2) at C=2 satisfies bounded injection and exact KEEP repayment on the
development corpus with zero exact residuals.

## Finite evidence (exact, all engines agree)
- Stage-1 grid (critical + near-critical cycles): C=2: 30/42 feasible (P_all/P_keep,
k≥1); CEGIS/z3 + brute force + ILP minimal-k coincide; engine == independent replay
on every config (CERT-01 clean).
- Histories screen (120 generated selection histories, burden max w=8 at C=2):
(P_all,k≥2,C=2) feasible with zero residuals; all other predicates dead at every k;
C=3,4 survivors (P_all,k≥2); C=6,8 survivors (P_all/P_keep/P_zigzig,k≥1); C≥12
vacuous (no burden — recorded as inconclusive, never as passes).
- Flow screen: worst required_k=1 at C=2 (n5-c0), 0 elsewhere — necessary condition
consistent with the minimal feasible k=1..2 found by search.
- Dominance (proved in-record): P_all fires on a superset of every predicate's events
and k=6 injects a superset of credit, so (P_all,6) residuals are pointwise ≤ any
(p,k≤6); one config per rung decides death.

## Minimal obstruction witnesses (killed families)
- All non-P_all predicates dead on histories at C=2..8 ∀k≤6 (first violations in
`solver/histories_screen.json`, e.g. P_keep pays nothing during DELETE bursts because
it never activates there — timing, not magnitude, is the killer).
- P_all k=1 dead on histories at C=2..4 (insufficient injection rate vs burst demand).
- Diagnostic C=2 (the parent-geometry microscope) is the binding rung; larger rungs
either vacuous (cycles C≥3, histories C≥12) or easier.

## Scope limits
Finite survival only. Fresh banks (H2R/H3T), clean-room reimplementation, large-n
adversarial falsification, and arbitrary-n proof all outstanding (WP-5/WP-6).
A fresh-holdout violation kills the corresponding candidate without touching the rest.

## WP-5/WP-6 outcome addendum (2026-09-25; original conjecture above unchanged)

Fresh H3T (70,000 episodes, every episode exact): MSTC-0001 (P_all,k=2,C=2) killed
(max_res=8; first n=32 idx 4406, w=11 paid 9 res 2); MSTC-0003 (P_keep,k=1,C=6)
killed (max_res=23; first n=16 idx 3610, w=8 paid 7 res 1); MSTC-0002
(P_all,k=6,C=2) survives (max_res=0, 70k/70k) plus 54 large-n trials with 0 kills
(witnesses clean-room replayed in `artifacts/v03/holdouts/h3t_reveal.json` /
`h3t_replay.json`). Status stays UNPROVED: the survivor has finite survival only
(§32.7), and arbitrary-n repayment (MST0-14) is not proved. The dev-stage
"minimal-k anchor" reading did not transfer; headroom (k=6) did at C=2.
