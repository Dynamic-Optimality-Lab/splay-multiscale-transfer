"""Fresh-checkout reproduction entry point (WP-6 completes; WP-0 provides phase-00 step)."""
import subprocess
import sys

STEPS = [["python", "scripts/run_phase00.py"], ["python", "tests/test_foundation.py"]]

if __name__ == "__main__":
    for s in STEPS:
        r = subprocess.run(s)
        if r.returncode != 0:
            sys.exit(r.returncode)
    print("REPRODUCE_ALL (WP-0 scope): PASS")
