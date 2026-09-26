"""Spec PHASE 01 runner (REAL): WP-1 read-only import + independent reverification.

Entry: FOUNDATION_FROZEN. Certified parent-fact consumption additionally waits on
the WP-1 pre-consumption subgate (MST0-01 REVIEWED); this runner only IMPORTS sealed
bytes and RECOMPUTES independently, comparing the two (verification, not premise use).
Steps: WP1-STEP-01 import, STEP-02 enumerate, STEP-03 counts/costs, STEP-05 replay,
STEP-06 failure table, STEP-07 subgate report. Rotation mechanics live in run_phase03.
Console lines prefixed [WP1-STEP-0x] are the audit record (see Path.md WP-1 log table).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.audit import status as obligation_status  # noqa: E402
from python.cycles import import_parent  # noqa: E402
from python.cycles.enumerate import PairDomain  # noqa: E402

V01_COMMIT = import_parent.V01_COMMIT
V02_COMMIT = import_parent.V02_COMMIT


def sha_file(p: str) -> str:
    """SHA-256 over buffered reads."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP1-STEP-01: verify source commits, vendor sealed files, write the import ledger.
def step_import(v01: str, v02: str, outdir: str, skip_if_sealed: bool = True) -> list[str]:
    fails: list[str] = []
    ledger_path = os.path.join(outdir, "import_ledger.json")
    if skip_if_sealed and os.path.exists(ledger_path):
        print("[WP1-STEP-01] import ledger exists; re-verifying vendored bytes", flush=True)
    for label, src, want in (("v0.1", v01, V01_COMMIT), ("v0.2", v02, V02_COMMIT)):
        try:
            got = subprocess.run(["git", "rev-parse", "HEAD"], cwd=src,
                                 capture_output=True, text=True, timeout=60)
            head = got.stdout.strip()
        except (subprocess.SubprocessError, OSError) as e:
            fails.append("IMPORT-00 %s rev-parse failed: %s" % (label, e))
            continue
        if head != want:
            fails.append("IMPORT-00 %s HEAD %s != sealed %s" % (label, head, want))
        else:
            print("[WP1-STEP-01] %s HEAD exact: %s" % (label, want), flush=True)
    if fails:
        return fails
    dest_v01 = os.path.join(outdir, "v01baseline")
    dest_v02 = os.path.join(outdir, "v02baseline")
    ledger, f1 = import_parent.vendor({"v01": v01}, dest_v01)
    fails += f1
    ledger2, f2 = import_parent.vendor({"v02": v02}, dest_v02)
    fails += f2
    if fails:
        return fails
    # Cross-check vendored v0.1 files against the sealed v0.1 MANIFEST.
    manifest = {}
    for ln in open(os.path.join(dest_v01, "v01", "MANIFEST.sha256"), encoding="utf-8"):
        parts = ln.strip().split()
        if len(parts) == 2:
            manifest[parts[1]] = parts[0].upper()
    checked = 0
    for entry in ledger:
        if not entry["dest"].startswith("v01/critical_n"):
            continue
        size, fname = entry["dest"].split("critical_n")[1].split("_", 1)
        mkey = next((k for k in manifest
                     if k.endswith("critical/n%s/%s" % (size, fname.replace(".zst", ".zst")))), None)
        if mkey is None or manifest[mkey] != entry["sha256"]:
            fails.append("IMPORT-02 v0.1 manifest mismatch for %s" % entry["dest"])
        else:
            checked += 1
    print("[WP1-STEP-01] v0.1 manifest cross-check: %d cycle files pinned" % checked, flush=True)
    with open(ledger_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"v01_commit": V01_COMMIT, "v02_commit": V02_COMMIT,
                   "v01_files": ledger, "v02_files": ledger2}, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP1-STEP-01] import ledger written (%d+%d files)" % (len(ledger), len(ledger2)), flush=True)
    return fails


# WP1-STEP-02/03: independent enumeration + count verification vs fact_table.
def step_enumerate(outdir: str, sizes: list[int], budget_s: float) -> tuple[list[str], dict]:
    fails: list[str] = []
    fact = json.load(open(os.path.join(outdir, "v02baseline", "v02", "fact_table.json"),
                          encoding="utf-8"))
    claims = {row["n"]: row for row in fact}
    results: dict = {}
    for n in sizes:
        t0 = time.time()
        dom = PairDomain(n)
        reached = dom.reachable(progress_every=50000 if n >= 7 else 0)
        dt = time.time() - t0
        results[str(n)] = {"trees": dom.C, "reachable": len(reached), "seconds": round(dt, 1)}
        print("[WP1-STEP-02] n=%d trees=%d reachable=%d seconds=%.1f"
              % (n, dom.C, len(reached), dt), flush=True)
        if dt > budget_s:
            fails.append("RESOURCE n=%d exceeded budget %.0fs (%.0fs)" % (n, budget_s, dt))
            break
        want = claims[n]["R"]
        if len(reached) != want:
            fails.append("COUNT-01 n=%d recomputed %d != parent %d" % (n, len(reached), want))
        else:
            print("[WP1-STEP-03] n=%d reachable count exact: %d" % (n, want), flush=True)
    with open(os.path.join(outdir, "enumeration.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(results, f, sort_keys=True, indent=2)
        f.write("\n")
    return fails, results


# WP1-STEP-05: replay every imported critical cycle; ratios + closure + all-KEEP.
def step_replay(outdir: str, sizes: list[int]) -> list[str]:
    fails: list[str] = []
    fact = json.load(open(os.path.join(outdir, "v02baseline", "v02", "fact_table.json"),
                          encoding="utf-8"))
    claims = {row["n"]: (int(row["b"][0]), int(row["b"][1])) for row in fact}
    report: dict = {}
    for n in sizes:
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(outdir, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        p, q = claims[n]
        ok_count = 0
        rows = []
        for cid, cyc in enumerate(cycles):
            rep = import_parent.replay_cycle(dom, cyc)
            ratio_ok = Fraction(rep["sum_y"], rep["sum_a"]) == Fraction(p, q)
            row_ok = rep["closed"] and rep["all_keep"] and ratio_ok and not rep["mismatches"]
            if row_ok:
                ok_count += 1
            else:
                fails.append("REPLAY-01 n=%d cycle=%d closed=%s all_keep=%s ratio=%s mism=%d"
                             % (n, cid, rep["closed"], rep["all_keep"], rep["ratio"],
                                len(rep["mismatches"])))
            rows.append({"cycle": cid, "sum_a": rep["sum_a"], "sum_y": rep["sum_y"],
                         "ratio": rep["ratio"], "all_keep": rep["all_keep"],
                         "closed": rep["closed"], "mismatch_count": len(rep["mismatches"])})
        report[str(n)] = {"cycles": len(cycles), "replayed_ok": ok_count,
                          "claimed_b": [p, q], "rows": rows}
        # CYC-04: forced-derivative records match parent (edge-exact + KEEP-only).
        import zstandard as zstd
        forced = json.loads(zstd.ZstdDecompressor().decompress(
            open(os.path.join(outdir, "v01baseline", "v01",
                              "critical_n%d_forced_delta_edges.json.zst" % n),
                 "rb").read()))
        fbad, fkeep = 0, 0
        for fe in forced:
            tgt, a, y = dom.edge(fe["source_pair_id"], fe["key"], fe["mode"])
            if tgt != fe["target_pair_id"] or a != fe["a"] or y != fe["y"]:
                fbad += 1
            if fe["mode"] == "KEEP":
                fkeep += 1
        if fbad:
            fails.append("CYC-04 n=%d forced-edge mismatches: %d/%d"
                         % (n, fbad, len(forced)))
        else:
            print("[WP1-STEP-05] n=%d forced derivatives exact: %d/%d edges, KEEP=%d"
                  % (n, len(forced) - fbad, len(forced), fkeep), flush=True)
        report[str(n)]["forced"] = {"count": len(forced), "mismatches": fbad,
                                    "keep": fkeep}
        print("[WP1-STEP-05] n=%d replayed %d/%d cycles ratio=%d/%d all-KEEP closed"
              % (n, ok_count, len(cycles), p, q), flush=True)
    with open(os.path.join(outdir, "replay.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, sort_keys=True, indent=2)
        f.write("\n")
    return fails


# WP1-STEP-06: parent failure-mechanism table (evidence labels with pointers).
def step_failures(outdir: str) -> list[str]:
    fails: list[str] = []
    base = os.path.join(outdir, "v02baseline", "v02")
    phis = {}
    for h in ("PHI-0001", "PHI-0002", "PHI-0003"):
        phis[h] = json.load(open(os.path.join(base, "falsification_%s_dev.json" % h),
                                 encoding="utf-8"))
    ledger = json.load(open(os.path.join(base, "hypothesis_ledger.json"), encoding="utf-8"))
    atoms = json.load(open(os.path.join(base, "recency_atoms.json"), encoding="utf-8"))
    table = {
        "GLOBAL_TOO_EASY_TO_CREATE": {"evidence": "PHI-0001 rejected by DELETE blowup",
                                      "pointer": "falsification_PHI-0001_dev.json"},
        "LOCAL_TOO_WEAK_TO_REPAY": {"evidence": "PHI-0002/PHI-0003 rejected by KEEP underpayment",
                                    "pointer": "falsification_PHI-0002/0003_dev.json"},
        "PURE_DIFFERENCE_LOSES_ABSOLUTE_SHAPE": {"evidence": "parent claim, imported as context",
                                                "pointer": "v02/FINAL_RESULT.json"},
        "RECENCY_V_BLIND": {"evidence": "parent claim, imported as context",
                            "pointer": "v02/FINAL_RESULT.json"},
        "RECENCY_SCALAR_UNDERPAYS_KEEP": {"evidence": "D5 near-miss family in recency_atoms.json",
                                          "pointer": "recency_atoms.json",
                                          "d5_keys": sorted(k for k in
                                                            (atoms.get("atoms", atoms) if isinstance(atoms, dict) else {})
                                                            .keys() if "D5" in k)},
        "FEATURE_DERIVATIVE_INCONSISTENT": {"evidence": "parent claim, imported as context",
                                            "pointer": "v01/FINAL_RESULT.json"},
        "NO_BEHAVIORAL_COMPRESSION_FINITE": {"evidence": "parent claim, imported as context",
                                             "pointer": "v02/FINAL_RESULT.json"},
    }
    for h in ("PHI-0001", "PHI-0002", "PHI-0003"):
        if phis[h].get("verdict") != "REJECTED":
            fails.append("FAILURE-01 %s not REJECTED in parent ledger" % h)
    if not fails:
        print("[WP1-STEP-06] failure table: 3/3 PHI REJECTED confirmed; 7 labels with pointers", flush=True)
    with open(os.path.join(outdir, "failure_table.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"labels": table, "hypotheses": ledger}, f, sort_keys=True, indent=2)
        f.write("\n")
    # D5/atom verdicts mechanically extracted (all families INCONSISTENT per parent).
    verdicts = atoms.get("verdicts", {})
    if not verdicts or any("INCONSISTENT" not in str(v) for v in verdicts.values()):
        fails.append("FAILURE-02 atom verdicts differ from parent claims")
    else:
        print("[WP1-STEP-06] atom families inconsistent: %s"
              % ",".join(sorted(verdicts)), flush=True)
    return fails


# WP1-STEP-06b: spot-check Bellman specimen witnesses as target-only context.
def step_specimens(outdir: str, sizes: list[int]) -> list[str]:
    fails: list[str] = []
    base = os.path.join(outdir, "v02baseline", "v02")
    checked = 0
    contextual = 0
    for n in sizes:
        dom = PairDomain(n)
        wit = json.load(open(os.path.join(base, "specimens_n%d_witnesses.json" % n),
                             encoding="utf-8"))
        for name, w in wit.items():
            if not isinstance(w, dict) or w.get("source") is None or w.get("target") is None:
                contextual += 1
                continue
            tgt, a, y = dom.edge(int(w["source"]), w["key"], w["mode"])
            if tgt != int(w["target"]) or a != w["a"] or y != w["y"]:
                fails.append("SPECIMEN-01 n=%d %s mismatch" % (n, name))
            else:
                checked += 1
    if not fails:
        print("[WP1-STEP-06] specimen witnesses: %d replayed exact, %d context-only (n=2 aggregates)"
              % (checked, contextual), flush=True)
    return fails


def main() -> int:
    import time as _time
    import tracemalloc as _tracemalloc
    from python.audit import log as log_mod
    _tracemalloc.start()
    _t0 = _time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--v01", required=True)
    ap.add_argument("--v02", required=True)
    ap.add_argument("--sizes", default="2,3,4,5,6,7")
    ap.add_argument("--budget-s", type=float, default=1200.0)
    args = ap.parse_args()
    print("[WP1-STEP-00] PHASE 01: import, enumerate, verify counts, replay cycles, "
          "failure table, subgate report", flush=True)
    outdir = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    os.makedirs(outdir, exist_ok=True)
    sizes = [int(s) for s in args.sizes.split(",")]
    fails: list[str] = []
    fails += step_import(args.v01, args.v02, outdir)
    if not fails:
        f2, _enum = step_enumerate(outdir, sizes, args.budget_s)
        fails += f2
    if not fails:
        fails += step_replay(outdir, [n for n in sizes if n >= 4])
    if not fails:
        fails += step_failures(outdir)
    if not fails:
        fails += step_specimens(outdir, sizes)
    statuses = obligation_status.main(ROOT)
    if statuses.get("MST0-01", {}).get("status") != "REVIEWED":
        print("[WP1-STEP-07] subgate: MST0-01 not REVIEWED; certified consumption stays blocked", flush=True)
    exit_code = 1 if fails else 0
    # WP1-STEP-00: §27 execution record (append-only; fullest honest field set).
    rec = log_mod.static_fields(ROOT)
    rec.update({
        "phase": "01", "branch": "WP-1", "command": sys.argv,
        "scientific_status": "PARENT_CHAIN_VERIFIED" if not fails else "PHASE01_FAIL",
        "clone_args": {"v01": args.v01, "v02": args.v02},
        "input_hashes": {"v01_sealed_commit": V01_COMMIT, "v02_sealed_commit": V02_COMMIT},
        "output_hashes": log_mod.hash_outputs(ROOT, ["artifacts/v03/parent_import"]),
        "wall_s": round(_time.perf_counter() - _t0, 2),
        "allocator_peak_bytes": _tracemalloc.get_traced_memory()[1],
        "exit_code": exit_code,
    })
    _tracemalloc.stop()
    # WP-1 REPAIR STEP L3: append the §27 execution record (fail-closed fields).
    log_mod.write_log(os.path.join(ROOT, "artifacts", "v03", "logs", "phase01_wp1.jsonl"), rec)
    print("[WP1-STEP-00] §27 record appended (phase01_wp1.jsonl)", flush=True)
    if fails:
        print("[WP1-STEP-00] PHASE01_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP1-STEP-00] PHASE01_PASS: import sealed, counts exact, cycles replay, failures tabled", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
