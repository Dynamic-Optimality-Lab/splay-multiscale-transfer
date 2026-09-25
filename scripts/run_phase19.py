"""Spec PHASE 19 runner (REAL): seal, reproduce, package, release (WP-6).

Entry: Phase-18 outputs (bridge/negative audit, 4 verified reports, ledger +
atlas finalization) + clean lifecycle. Steps: WP6-STEP-00 entry;
WP6-STEP-07 FINAL_RESULT from artifacts only (exactly one terminal level);
WP6-STEP-08 freeze roll-forward for living trackers (protected entries must be
byte-stable or fail closed) + audits + manifest; WP6-STEP-09 deterministic
archive + rebuild comparison; WP6-STEP-10 fresh-checkout reproduction (must exit
0). Failed artifacts are retained; deletion is a seal failure (STOP-48).
Console lines prefixed [WP6-STEP-0x] are the audit record.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.seal import finalize as seal_mod  # noqa: E402

TIMINGS: dict = {}


# WP6-STEP-00: Phase-19 entry gate (fail-closed).
def step_entry() -> tuple[list, dict]:
    fails: list = []
    ctx: dict = {}
    for rel in ("artifacts/v03/audits/bridge_negative_audit.json",
                "MULTISCALE_TRANSFER_REPORT.md", "THEOREM_STATUS_REPORT.md",
                "REPRODUCIBILITY.md", "AI_USE.md",
                "artifacts/v03/proofs/lifecycle_audit.json"):
        if not os.path.exists(os.path.join(ROOT, rel)):
            fails.append("GATE-19 missing %s (Phase 17/18 not done)" % rel)
    if fails:
        print("[WP6-STEP-00] PHASE 19 entry gates: FAIL %r" % (fails,), flush=True)
        return fails, ctx
    print("[WP6-STEP-00] PHASE 19 entry gates: PASS", flush=True)
    return fails, ctx


# WP6-STEP-07: FINAL_RESULT from artifacts only.
def step_final() -> dict:
    t0 = time.perf_counter()
    result = seal_mod.build_final_result(ROOT)
    out = os.path.join(ROOT, "artifacts", "v03", "seal", "FINAL_RESULT.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, sort_keys=True, indent=2)
        f.write("\n")
    regen = seal_mod.build_final_result(ROOT)
    if regen != result:
        raise ValueError("FINAL_RESULT not reproducible from artifacts")
    TIMINGS["step07_final_s"] = round(time.perf_counter() - t0, 2)
    print("[WP6-STEP-07] FINAL_RESULT sealed + regeneration-identical", flush=True)
    return result


# WP6-STEP-08: freeze roll-forward (living trackers only) + audits + manifest.
def step_freeze_audits_manifest() -> dict:
    t0 = time.perf_counter()
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    try:
        import freeze_prereg
        recomputed = freeze_prereg.normative_hashes(ROOT)
    finally:
        sys.path.pop(0)
    freeze_path = os.path.join(ROOT, "prereg", "prereg_sha256.txt")
    committed = open(freeze_path, encoding="utf-8").read().replace("\r\n", "\n")
    old = dict((ln.split("  ./")[1], ln.split("  ./")[0])
               for ln in committed.splitlines() if "  ./" in ln)
    new = dict((ln.split("  ./")[1], ln.split("  ./")[0]) for ln in recomputed)
    # NOTE: WorkPlan.md/Path.md are living trackers (PIN amendment §3); every
    # other normative entry must be byte-stable or the seal fails closed.
    allowed = {"Path.md", "WorkPlan.md"}
    drift = {k for k in set(old) | set(new) if old.get(k) != new.get(k)}
    if drift - allowed:
        raise ValueError("STOP-05 protected normative drift: %r" % sorted(drift - allowed))
    with open(freeze_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sorted(recomputed)) + "\n")
    print("[WP6-STEP-08] freeze rolled forward (drift only in %r; %d entries stable)"
          % (sorted(drift), len(new) - len(drift)), flush=True)
    audits = {}
    audits["threats"] = seal_mod.audit_threats(ROOT)
    audits["stops"] = seal_mod.audit_stops(ROOT)
    audits["invariants"] = seal_mod.audit_invariants(ROOT)
    audits["tests"] = seal_mod.audit_tests(ROOT)
    audits["arithmetic"] = seal_mod.audit_arithmetic(ROOT)
    # NOTE: wall timings stay console-only (TIMINGS printed at PASS); persisting
    # them would make re-runs non-byte-identical. The §26.7 record carries
    # sizes/attempted-work, and states the no-failure fact.
    audits["resources"] = seal_mod.build_resource_record(ROOT, {})
    adir = os.path.join(ROOT, "artifacts", "v03", "audits")
    for name, record in audits.items():
        with open(os.path.join(adir, name + "_audit.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(record, f, sort_keys=True, indent=2)
            f.write("\n")
    manifest_sha, lines = seal_mod.build_manifest(ROOT)
    audits["manifest"] = {"sha256": manifest_sha, "n_files": len(lines),
                          "scope": "all seal-input files (seal/ envelope excluded; "
                                   "FINAL_RESULT+MANIFEST ride inside the archive)"}
    TIMINGS["step08_audits_manifest_s"] = round(time.perf_counter() - t0, 2)
    return audits


# WP6-STEP-09: deterministic archive + pure rebuild comparison.
def step_archive() -> dict:
    t0 = time.perf_counter()
    digest, nbytes, members = seal_mod.build_archive(ROOT)
    with open(os.path.join(ROOT, "artifacts", "v03", "seal",
                           seal_mod.ARCHIVE_NAME), "rb") as f:
        blob1 = f.read()
    blob2 = seal_mod.archive_bytes(ROOT, members)
    if blob1 != blob2:
        raise ValueError("archive rebuild differs (nondeterminism)")
    TIMINGS["step09_archive_s"] = round(time.perf_counter() - t0, 2)
    print("[WP6-STEP-09] archive rebuild byte-identical (determinism proved)", flush=True)
    return {"sha256": digest, "bytes": nbytes, "rebuild_identical": True,
            "n_members": len(members)}


# WP6-STEP-10: fresh-checkout reproduction (must exit 0).
def step_reproduce() -> None:
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts",
                                                     "reproduce_all_v0.3.py")],
                       capture_output=True, text=True, cwd=ROOT)
    print("[WP6-STEP-10] reproduce_all exit=%d" % r.returncode, flush=True)
    tail = (r.stdout or "").splitlines()[-4:]
    for ln in tail:
        print("[WP6-STEP-10] " + ln, flush=True)
    if r.returncode != 0:
        raise ValueError("reproduction FAILED (exit %d)" % r.returncode)
    TIMINGS["step10_reproduce_s"] = round(time.perf_counter() - t0, 2)


def main() -> int:
    print("[WP6-STEP-00] PHASE 19: seal, reproduce, package, release", flush=True)
    fails, _ctx = step_entry()
    if fails:
        print("[WP6-STEP-00] PHASE19_FAIL: %r" % (fails,), flush=True)
        return 2
    step_final()
    step_freeze_audits_manifest()
    step_archive()
    step_reproduce()
    # NOTE: timings print to console only (audit record); writing them to a file
    # would make re-runs non-byte-identical. The §26.7 resource record carries
    # sizes/attempted-work, not wall clocks.
    print("[WP6-STEP-10] PHASE19_PASS: sealed + reproduced (timings=%s)" % (TIMINGS,),
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
