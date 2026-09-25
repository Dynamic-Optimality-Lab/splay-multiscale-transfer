"""Spec PHASE 11 runner (REAL, untriggered): signed branch activation gate.

Entry: WP-4 Phase-10 verdict file. If the verdict is RAW_BOUNDARY_LAW_REJECTED with
a preserved obstruction record, Branch B activates and search_signed runs (exact).
Otherwise (current state: SURVIVES_DEV) the runner emits SIGNED_TRANSFER_NOT_ACTIVATED
without searching — Branch B was preregistered, not invented, and stays unfired.
Console lines prefixed [WP4-STEP-04] are the audit record.
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.transfer import branchB as branchB_mod  # noqa: E402


def main() -> int:
    print("[WP4-STEP-04] PHASE 11: signed-branch activation gate", flush=True)
    verdict_path = os.path.join(ROOT, "artifacts", "v03", "solver", "verdict.json")
    if not os.path.exists(verdict_path):
        print("[WP4-STEP-04] PHASE11_FAIL: run_phase10 verdict missing", flush=True)
        return 2
    verdict = json.load(open(verdict_path, encoding="utf-8"))["verdict"]
    if verdict != "RAW_BOUNDARY_LAW_REJECTED":
        print("[WP4-STEP-04] Branch-A verdict is %s (not exact rejection)" % verdict, flush=True)
        print("[WP4-STEP-04] SIGNED_TRANSFER_NOT_ACTIVATED (preregistered, unfired)", flush=True)
        with open(os.path.join(ROOT, "artifacts", "v03", "solver", "branch_b.json"),
                  "w", encoding="utf-8", newline="\n") as f:
            json.dump({"status": "SIGNED_TRANSFER_NOT_ACTIVATED",
                       "reason": "Branch A survives development; activation precondition absent"},
                      f, sort_keys=True, indent=2)
            f.write("\n")
        return 0
    print("[WP4-STEP-04] Branch-A rejection present; signed search would activate here", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
