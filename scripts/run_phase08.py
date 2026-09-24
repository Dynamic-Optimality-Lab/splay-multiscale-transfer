"""Spec PHASE 08 runner (REAL): generate + quarantine HOLDOUT-H3T-v0.3.

Entry: WP-2 gates. Fail-closed BEFORE generation: refuses if any transfer-synthesis
artifacts exist (hypotheses/, solver outputs, frozen calculi — synthesis must not
predate the bank), if the bank state is anything but EMPTY/missing, or if WP-2A
freeze + MST0-03 ACCEPT are absent. Steps: WP3-STEP-04 generate 70k episodes,
WP3-STEP-05 verify (full streamed hashes + sampled independent replay), commit
(h3t_commitment.json + firewall state EMPTY -> BANK_COMMITTED).
Console lines prefixed [WP3-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.holdout import firewall as firewall_mod  # noqa: E402
from python.holdout import h3t_generate as gen_mod  # noqa: E402
from python.holdout import h3t_verify as verify_mod  # noqa: E402


def _entry() -> list[str]:
    fails: list[str] = []
    cert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE02_L6_MAPPING_FREEZE.json")
    if not os.path.exists(cert):
        fails.append("GATE-02 WP-2A freeze missing")
    rev = os.path.join(ROOT, "math", "reviews", "MST0-03.review.json")
    if not os.path.exists(rev):
        fails.append("GATE-02 MST0-03.review.json missing")
    art = os.path.join(ROOT, "artifacts", "v03")
    for forbidden in ("hypotheses", "solver", "transfer_grammar"):
        p = os.path.join(art, forbidden)
        if os.path.isdir(p) and any(os.scandir(p)):
            fails.append("PRE-SYNTHESIS %s/ non-empty: bank must predate synthesis" % forbidden)
    state_path = os.path.join(art, "holdouts", "h3t_state.json")
    if os.path.exists(state_path):
        st = firewall_mod.load_state(state_path)
        if st.get("state") != "EMPTY":
            fails.append("H3T-STATE bank already %s (no regeneration)" % st.get("state"))
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="10,12,16,24,32,48,64")
    ap.add_argument("--per-size", type=int, default=10000)
    ap.add_argument("--sample-per-size", type=int, default=77)
    args = ap.parse_args()
    print("[WP3-STEP-00] PHASE 08: H3T generation + quarantine (pre-synthesis)", flush=True)
    fails = _entry()
    if fails:
        print("[WP3-STEP-00] PHASE08_FAIL (refused)", flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 2
    bankdir = os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_bank")
    os.makedirs(bankdir, exist_ok=True)
    holdouts = os.path.join(ROOT, "artifacts", "v03", "holdouts")
    os.makedirs(holdouts, exist_ok=True)
    sizes = [int(s) for s in args.sizes.split(",")]
    commitment: dict = {"seed_policy": "master=%d per-episode (size,stratum,idx)" % gen_mod.MASTER_SEED,
                        "generator": "python/holdout/h3t_generate.py", "sizes": {}}
    with open(os.path.join(ROOT, "python", "holdout", "h3t_generate.py"), "rb") as f:
        commitment["generator_sha256"] = hashlib.sha256(f.read()).hexdigest().upper()
    print("[WP3-STEP-04] generator sha=%s..." % commitment["generator_sha256"][:16], flush=True)
    for n in sizes:
        frag = gen_mod.generate_size(n, args.per_size, bankdir)
        commitment["sizes"][str(n)] = frag
    total = sum(v["count"] for v in commitment["sizes"].values())
    logical = hashlib.sha256("".join(sorted(v["stream"] for v in commitment["sizes"].values()))
                             .encode("utf-8")).hexdigest().upper()
    commitment["total_episodes"] = total
    commitment["logical_stream"] = logical
    with open(os.path.join(ROOT, "python", "holdout", "h3t_verify.py"), "rb") as f:
        commitment["replay_verifier_sha256"] = hashlib.sha256(f.read()).hexdigest().upper()
    with open(os.path.join(holdouts, "h3t_commitment.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(commitment, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP3-STEP-04] bank committed: %d episodes logical=%s..." % (total, logical[:16]), flush=True)
    fails += verify_mod.verify_hashes(bankdir, commitment)
    fails += verify_mod.verify_sample(bankdir, args.sample_per_size)
    if fails:
        print("[WP3-STEP-00] PHASE08_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    firewall_mod.transition_commit(os.path.join(holdouts, "h3t_state.json"),
                                   {"logical_stream": logical, "total": total})
    print("[WP3-STEP-05] firewall: EMPTY -> BANK_COMMITTED (unlock_count=0)", flush=True)
    print("[WP3-STEP-00] H3T_BANK_COMMITTED (%d episodes, fresh, quarantined)" % total, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
