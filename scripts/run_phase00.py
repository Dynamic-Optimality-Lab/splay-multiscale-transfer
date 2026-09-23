"""WP-0 Phase-00 gate orchestrator: runs WP0-STEP-01..10 in order, fail-closed.

Each check module prints its own [WP0-STEP-0x] console lines (the auditable record;
see Path.md WP-0 log table for file:line references). PHASE00_PASS reports that the
WP-0 *checks* pass; it is not itself the FOUNDATION_FROZEN seal claim (see Path.md).
WP-1 certified consumption additionally requires MST0-01 == REVIEWED (gate matrix).
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.audit import check_prereg  # noqa: E402
from python.audit import verify_parent  # noqa: E402


# WP0-STEP-00: orchestrator entry (prints the execution plan before running checks).
def main() -> int:
    print("[WP0-STEP-00] WP-0 Phase-00 gate: STEP-01 parent pin, STEP-02 amendment, "
          "STEP-03 bootstrap lock, STEP-04 literature, STEP-05 gates, STEP-06 L6 "
          "contract, STEP-07 matrices, STEP-08 solver record, STEP-09 freeze "
          "integrity, STEP-10 no early science")
    root = ROOT
    fails: list[str] = []
    # WP0-STEP-01/02: parent pin + amendment (verify_parent module).
    fails += verify_parent.check_parent_pin(root)
    fails += verify_parent.check_amendment(root)
    # WP0-STEP-03: bootstrap lock is verified by bootstrap_parent (run separately
    # so its lock enforcement stays an explicit transaction); re-check read-only here.
    from python.inherited import bootstrap_parent
    fails += bootstrap_parent.check_manifest(root)
    fails += bootstrap_parent.enforce_lock(root, enforce=False)
    # WP0-STEP-04: literature status (identities exact; pending bytes are warnings).
    lit_fails, _warnings = verify_parent.check_literature_status(root)
    fails += lit_fails
    # WP0-STEP-05..10: prereg integrity battery (check_prereg module).
    fails += check_prereg.check_theorem_gates(root)
    fails += check_prereg.check_l6_contract(root)
    fails += check_prereg.check_matrices(root)
    fails += check_prereg.check_solver_record(root)
    fails += check_prereg.check_freeze_integrity(root)
    fails += check_prereg.check_no_early_science(root)
    if fails:
        print("[WP0-STEP-00] PHASE00_FAIL (%d)" % len(fails))
        for x in fails:
            print(" -", x)
        return 1
    print("[WP0-STEP-00] PHASE00_PASS: full-SHA parent pin + amendment + lock + "
          "literature identities + gates + solver record + freeze integrity + no early science")
    print("[WP0-STEP-00] NOTE: WP-1 entry needs FOUNDATION_FROZEN only; certified consumption waits on")
    print("[WP0-STEP-00] the WP-1 pre-consumption subgate (MST0-01 == REVIEWED).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
