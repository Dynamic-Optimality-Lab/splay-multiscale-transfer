# Counterexample atlas (WP-4 draft, append-only)

Every exact violation killed a candidate at a frozen C; representation failures are
distinguished from conjecture failures by actual-ratio tracking (never residuals).

## Killed on Stage-1 cycles (C=2, non-vacuous rung)
- All non-P_all/non-P_keep predicates dead ∀k≤6 (first violations in ladder rows).
- P_all/P_keep k=0 dead (zero injection cannot pay positive regret).
- Minimal obstruction: flow screen worst required_k=1 at C=2 (n5-c0) — consistent
  with minimal feasible k=1..2 found by search (necessary condition tight here).

## Killed on generated histories (C=2..8, burden max w=8..2)
- All non-P_all predicates dead ∀k≤6 at every burdened rung (timing, not magnitude:
  P_keep never activates during DELETE bursts, so credit is not ready at repayment).
- P_all k=1 dead at C=2..4 (injection rate insufficient vs burst demand); survives k≥2.
- Full per-config verdicts: `artifacts/v03/solver/histories_screen.json`.

## Negative triage (11 motifs, actual ratios)
- Inflated critical-cycle families: actual ratio CONSTANT (= cycle ratio) across
  x1/x2/x4/x8 — N3 fails everywhere → NEGATIVE_FAMILY_NOT_ACTIVATED (11/11).
- Transfer residuals do not predict actual-ratio growth: representation obstruction,
  not conjecture obstruction. Full tracks: `artifacts/v03/adversarial/triage.json`.

## Adversarial battery (84 evaluations, 0 kills)
- Nine modes (uniform/structured/hillclimb/annealing/genetic/neighborhood/splicing/
  inflation/generalization), shortlist (P_all,2,2), (P_all,6,2), (P_keep,1,6):
  zero exact residuals at frozen C; search engines best residual 0 everywhere.
- `artifacts/v03/adversarial/battery.json`.
