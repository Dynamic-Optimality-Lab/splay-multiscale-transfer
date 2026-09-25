# CHANGELOG

## 2026-09-23 — WP-4 EXECUTION (Phase 4 finished: Branch-A survives dev + Branch-B unfired + triage quiet + battery clean)
- Masks frozen (384 near-critical, 9.6k noncritical sel, 52k val, 120+120 histories); flow screen (worst k=1 at C=2); CEGIS(z3)+brute+ILP agree per rung (C=2: 30/42, C≥3: 42/42); histories screen (P_all-only survival, dominance-pruned, 0 fails fresh); shortlist 3 dev hypotheses (zero residuals, UNTOUCHED); Branch B NOT_ACTIVATED; triage 11 motifs NOT_ACTIVATED (ratios constant); battery 84/0 kills over 9 modes. 20 suites/runners green. WP-4 FINISHED.

## 2026-09-23 — WP-3 EXECUTION (Phase 3 finished: provenance + ledger + grammar + H3T + MST0-10)
- Provenance/ledger/transfer machinery (deterministic U_R, support arity, event/credit predicate separation, duplicate-ID guards, tag-independence, flow/energy exactness); leakage audit clean over 7 scopes (two-tier + carve-outs); H3T 70,000-episode bank (11 strata, streams verified, 539 exact independent replays, BANK_COMMITTED, 14.1 MB committed to git); prereg untouched (re-verified); freeze certs; Branch B BLOCKED; MST0-10 conditional ACCEPT discharged via 3 fixes and recorded schema-valid; MST0-11 UNPROVED-setup. 15 suites/runners green. WP-3 FINISHED.

## 2026-09-23 — WP-2 EXECUTION (Phase 2 finished: WP-2A frozen + WP-2B science + lemma verdicts)
- WP-2A: source extraction, 9+1 translation modules, 27-record mapping (all SAME with operationalizations), dual agreement, 5 mutants, MST0-03 proof, human ACCEPT, L6_TRANSLATION_FROZEN cert. WP-2B: 70-edge stratification, 19 motifs, n7 validation (burden aligned), D5 verified, lemma battery (MST0-05 PROVED rank-0; MST0-06 killed + v2 conditional; MST0-07 PROVED turn-destruction; MST0-08 split finite-PROVED/universal-OPEN), baseline shape, reports. Human ACCEPT ×4 (08 scoped finite). Full regression green. WP-2 FINISHED.

## 2026-09-23 — WP-2 EXECUTION (Phase 2 finished: WP-2A frozen + WP-2B science + lemma verdicts)
- WP-2A: source extraction, 9+1 translation modules, 27-record mapping (all SAME with operationalizations), dual agreement, 5 mutants, MST0-03 proof, human ACCEPT, L6_TRANSLATION_FROZEN cert. WP-2B: 70-edge stratification, 19 motifs, n7 validation (burden aligned), D5 verified, lemma battery (MST0-05 PROVED rank-0; MST0-06 killed + v2 conditional; MST0-07 PROVED turn-destruction; MST0-08 split finite-PROVED/universal-OPEN), baseline shape, reports. Human ACCEPT ×4 (08 scoped finite). Full regression green. WP-2 FINISHED.

## 2026-09-23 — WP-1 CLOSED (subgate REVIEWED by human ACCEPT, WP-1 finished)
- Human verdict ACCEPT recorded for MST0-01/02/04/16 as schema-validated `math/reviews/*.review.json` (proof hashes match packages); derived statuses REVIEWED:4/UNPROVED:22; `run_phase01` re-ran PHASE01_PASS with subgate cleared. Certified consumption + WP-2 theorem-facing use unblocked (within entry gates).
- Canonical enumeration + sealed import (52 files, manifest cross-check) + strict replay (19/19 cycles exact, all-KEEP closed) + forced derivatives edge-exact + specimen witnesses (15 exact) + failure table + 70-edge dual-core agreement + idempotent expansion + 4 proofs PROVED with review packages + WP-1 stress green. Gates PARENT_CHAIN_VERIFIED + ROTATION_TRACE_CERTIFIED emitted (mechanics scope). Full regression green (phase00/foundation/wp0stress/reproduce exit 0). Subgate then CLOSED by human ACCEPT (see entry above).

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
