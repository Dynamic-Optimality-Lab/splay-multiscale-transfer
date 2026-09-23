# CHANGELOG

## 2026-09-23 — WP-0 foundation freeze
- Cloned `splay-multiscale-transfer` (was LICENSE-only, 1 commit); working tree verified fresh, zero stale scientific results carried over (`artifacts/v03/STALE_CLEARANCE.json`).
- Pinned parent `splay-bellman-debt@38c1be6` (`FINITE_DEBT_LAW_MINING_RESULTS`), ancestor `6de1ca2` (`FINITE_EXACT_BN_RESULTS`); verified H1 EMPTY / H2R BANK_COMMITTED(0) / n8 contaminated.
- Added `IMPLEMENTATION_SPEC_v0.3.md`, `WorkPlan.md` (7 WPs covering spec PHASE 00–19), `Path.md` tracker.
- Scaffolded §18 layout; froze prereg matrices (MST0-01…26, T01…T90, STOP-01…50); initialized `math/proof_status.json`.
- Implemented exact Splay + Pair-Access + rotation-trace core with independent second implementation; `run_phase00.py` + `test_foundation.py` green.
