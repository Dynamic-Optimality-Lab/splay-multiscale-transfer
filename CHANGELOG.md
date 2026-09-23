# CHANGELOG

## 2026-09-23 — WP-0 EXECUTION (Phase 0 finished, FOUNDATION_FROZEN claimed)
- Implemented WP-0 exactly: bootstrap/verify/check modules + 19 fail-closed phase stubs; WP0-STEP-00..11 console logs with ID comments; L3 (732,837 B) + L6 (628,208 B) PDFs frozen (SHA-256 verified, %PDF-checked); real 11-entry bootstrap manifest + 12-file read-only lock; STOP-05 read-only recompute; artifacts allowlist; header-anchored gate regex. Stress 27/27 green; full battery (freeze, phase00, foundation 47/47, stress, reproduce) all exit 0. One scoped item: L1/L2/L4/L5 bytes pending with tracked reasons and downstream-use blocks.

## 2026-09-23 — Review-response hardening VI (PA-native fallback edge case)
- All 27 translation records carry preregistered `MST_NATIVE_*` fallbacks; NOT_APPLICABLE activates fallback, post-WP-0 invention banned (new experiment/version required); L6-00 gate extended. Freeze 24 entries; PHASE00_PASS + 47/47 green.

## 2026-09-23 — Review-response hardening V (WP-2A/WP-2B barrier, count, enum)
- WP-2A translation-only subphase with hard target-join barrier (6 steps) + WP-2B corpus science gated on L6_TRANSLATION_FROZEN + MST0-03 REVIEWED; count de-hardcoded (yaml self-declares); FALSE removed from mapping statuses (refutation-record schema). Freeze 24 entries; PHASE00_PASS + 47/47 green.

## 2026-09-23 — Review-response hardening IV (L6 lifecycle + polish)
- `l6_translation` now freezes language + proposed definitions (27×UNRESOLVED_PRE_PROOF; WP-2 resolves, never invents); L6-00 gate; L6 version identity in manifest; nine-mode summary; candidate-at-C residual wording; WorkPlan-text-freeze date label. Freeze 24 entries; PHASE00_PASS + 47/47 green.

## 2026-09-23 — Review-response hardening III (populated prereg, 11 strata, consistency)
- `event_ontology`/`transfer_grammar`/`l6_translation` promoted stub → fully populated immutable contracts (YAML-validated); H3T 11 strata in WorkPlan (10k/size distributed); WP-1 MST0-10 prerequisite wording; conditional gate wording. Freeze 24 entries; PHASE00_PASS + 47/47 green.

## 2026-09-23 — Review-response hardening II (freeze-conflict, MST0-01 handoff, wording)
- WP-0 prereg permanently immutable; WP-3 emits `artifacts/v03/freeze/` certificates (prereg hash + impl/generator hashes), never rewrites prereg; `holdouts.yaml` H3T status frozen as preregistered. MST0-01 via WP-1 pre-consumption subgate (owner WP-1; entry needs FOUNDATION_FROZEN only). Conditional-obligation + multiplicity wording. Freeze 24 entries; PHASE00_PASS + 47/47 green.

## 2026-09-23 — Review-response hardening (10 findings, no architecture change)
- Added ratified `SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md` (discharges PRE_FREEZE_PARENT_PIN_REQUIRED; v0.3 text byte-identical); full-SHA parent contract (all seal hashes); first-consumer gate matrix (26×REVIEWED-required); review-record template+schema (human-owned review vs INDEPENDENT_COMPUTATIONAL_VERIFICATION); Phase-04 single owner (WP-2); nine mandatory adversarial modes; `solver_backends.yaml` freeze (synthesis blocked); quarantine stale policy (count=0); 13/13 schemas; WP-4 residual/cross-C wording. Freeze 24 entries; PHASE00_PASS + 47/47 green.

## 2026-09-23 — WP-0 foundation freeze
- Cloned `splay-multiscale-transfer` (was LICENSE-only, 1 commit); working tree verified fresh, zero stale scientific results carried over (`artifacts/v03/STALE_CLEARANCE.json`).
- Pinned parent `splay-bellman-debt@38c1be6` (`FINITE_DEBT_LAW_MINING_RESULTS`), ancestor `6de1ca2` (`FINITE_EXACT_BN_RESULTS`); verified H1 EMPTY / H2R BANK_COMMITTED(0) / n8 contaminated.
- Added `IMPLEMENTATION_SPEC_v0.3.md`, `WorkPlan.md` (7 WPs covering spec PHASE 00–19), `Path.md` tracker.
- Scaffolded §18 layout; froze prereg matrices (MST0-01…26, T01…T90, STOP-01…50); initialized `math/proof_status.json`.
- Implemented exact Splay + Pair-Access + rotation-trace core with independent second implementation; `run_phase00.py` + `test_foundation.py` green.
