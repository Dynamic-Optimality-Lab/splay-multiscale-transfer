# Theorem MST0-23 — finite transfer-grammar feasibility does not imply universal integrability

**Status:** PROVED — author guard-held record (human theorem review requested;
REVIEWED only on human ACCEPT). The claim proved is a process claim about this
seal, verified from artifacts: at no point was finite feasibility consumed as
universal integrability.

## Proof (audit of non-consumption)

1. WP-4 synthesis outputs were labeled dev-only (`DEV_FALSIFICATION_PENDING`,
   `DEV_SHORTLIST_NOT_FROZEN`, "never fresh-tested"); no integrability claim
   appears in any WP-4 record (`solver/verdict.json` gate language is
   candidate-at-C rejection only).
2. WP-5 froze candidates with proof outlines explicitly marking integrability
   UNPROVED; fresh survival was recorded as finite-sample survival
   (`fresh_claim: false` in every reveal record; §32.7).
3. WP-6 records MST0-15 UNPROVED and MST0-17/18 BLOCKED; FINAL_RESULT's terminal
   claim is the finite-survival level, citing no integrability theorem.
4. Machine check: the strings "integrability proved", "integrable for all n",
   and any universal energy-telescope equality appear in no theorem-facing
   record outside this guard document's negations (asserted by
   `tests/proof/test_pr.py` PR-08).

Therefore finite feasibility was never upgraded to universal integrability in
this seal. QED (process claim; human review requested via review package).
