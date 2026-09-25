"""Fresh-checkout reproduction entry point (WP-6 scope).

Runs every fast verification gate in dependency order. Under one-unlock
semantics this verifies (never re-unlocks): Phase-14/15 re-runs are NOT
included (their entry gates must refuse — asserted by tests, not re-shot
here). Expected terminal line: REPRODUCE_ALL: PASS.
"""
import subprocess
import sys

STEPS = [
    ["python", "scripts/run_phase00.py"],
    ["python", "tests/test_foundation.py"],
    ["python", "tests/holdout/test_firewall.py"],
    ["python", "tests/holdout/test_wp5_holdout.py"],
    ["python", "tests/test_wp5.py"],
    ["python", "tests/proof/test_holdout_scope.py"],
    ["python", "tests/proof/test_pr.py"],
    ["python", "tests/seal/test_seal.py"],
    ["python", "tests/mutation/test_seal_mutants.py"],
]

if __name__ == "__main__":
    for s in STEPS:
        print("REPRODUCE_STEP: %s" % " ".join(s), flush=True)
        r = subprocess.run(s)
        if r.returncode != 0:
            print("REPRODUCE_ALL: FAIL at %s (exit %d)" % (" ".join(s), r.returncode))
            sys.exit(r.returncode)
    print("REPRODUCE_ALL: PASS")
