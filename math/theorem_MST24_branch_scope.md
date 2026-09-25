# Theorem MST0-24 — raw-gap branch failure does not imply signed-transfer branch failure

**Status:** PROVED — author guard-held record (human theorem review requested;
REVIEWED only on human ACCEPT). The claim proved is a scope claim about this
seal, verified from artifacts: the raw-branch fresh failures were never read
as evidence against the signed branch.

## Proof (audit of non-consumption)

1. MSTC-0001/0003 fresh falsifications are recorded strictly as
   candidate-at-frozen-C rejections of RAW_BOUNDARY calculi
   (`artifacts/v03/holdouts/h3t_reveal.json` verdicts FRESH_H3T_FAIL with
   residual witnesses; §32.5 allowed form).
2. Branch B (SIGNED_MULTISCALE) was preregistered in WP-3 and never activated
   (no exact Branch-A rejection of the right form occurred: Branch A as a
   family still has a standing finite survivor; activation precondition
   absent — `artifacts/v03/solver/branch_b.json`). Its status is unchanged
   NOT_ACTIVATED, not REJECTED.
3. No record draws any inference from raw-branch residuals to signed-branch
   prospects in either direction (asserted by `tests/proof/test_pr.py` scope
   checks; §32.6/§32.10 honored).
4. MST0-12 stays NOT_APPLICABLE (no signed components exist to bound).

Therefore raw-branch failure was never consumed as signed-branch failure in
this seal. QED (scope claim; human review requested via review package).
