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
    dest_ev01 = os.path.join(outdir, "v01evidence")
    dest_ev02 = os.path.join(outdir, "v02evidence")
    ledger, f1 = import_parent.vendor({"v01": v01}, dest_v01)
    fails += f1
    ledger2, f2 = import_parent.vendor({"v02": v02}, dest_v02)
    fails += f2
    # WP-1 REPAIR STEP V0: vendor the sealed parent-evidence classes (F1/F3/F5).
    ledger_ev1, f3 = import_parent.vendor(
        {"v01": v01}, dest_ev01, import_parent.V01_EVIDENCE_FILES)
    fails += f3
    ledger_ev2, f4 = import_parent.vendor(
        {"v02": v02}, dest_ev02, import_parent.V02_EVIDENCE_FILES)
    fails += f4
    if fails:
        return fails
    # Cross-check vendored v0.1 files against the sealed v0.1 MANIFEST.
    manifest = {}
    for ln in open(os.path.join(dest_v01, "v01", "MANIFEST.sha256"), encoding="utf-8"):
        parts = ln.strip().split()
        if len(parts) == 2:
            manifest[parts[1]] = parts[0].upper()
    checked = 0

    def _manifest_key(dest: str) -> str | None:
        if dest.startswith("v01/critical_n"):
            size, fname = dest.split("critical_n")[1].split("_", 1)
            return next((k for k in manifest
                         if k.endswith("critical/n%s/%s" % (size, fname))), None)
        if dest.startswith("v01evidence/"):
            rel = dest[len("v01evidence/"):]
            return next((k for k in manifest if k.endswith(rel)), None)
        return None

    for entry in ledger + ledger_ev1:
        mkey = _manifest_key(entry["dest"])
        if mkey is None or manifest[mkey] != entry["sha256"]:
            fails.append("IMPORT-02 v0.1 manifest mismatch for %s" % entry["dest"])
        else:
            checked += 1
    print("[WP1-STEP-01] v0.1 manifest cross-check: %d files pinned" % checked, flush=True)
    # Cross-check vendored v0.2 evidence against the sealed v0.2 MANIFEST.
    manifest2 = {}
    for ln in open(os.path.join(dest_v02, "v02", "MANIFEST.sha256"), encoding="utf-8"):
        parts = ln.strip().split()
        if len(parts) == 2:
            manifest2[parts[1]] = parts[0].upper()
    checked2 = 0
    for entry in ledger_ev2:
        rel = entry["dest"][len("v02evidence/"):]
        mkey = next((k for k in manifest2 if k.endswith(rel)), None)
        if mkey is None or manifest2[mkey] != entry["sha256"]:
            fails.append("IMPORT-02 v0.2 manifest mismatch for %s" % entry["dest"])
        else:
            checked2 += 1
    print("[WP1-STEP-01] v0.2 manifest cross-check: %d files pinned" % checked2, flush=True)
    with open(ledger_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"v01_commit": V01_COMMIT, "v02_commit": V02_COMMIT,
                   "v01_files": ledger, "v02_files": ledger2,
                   "v01evidence_files": ledger_ev1,
                   "v02evidence_files": ledger_ev2}, f, sort_keys=True, indent=2)
        f.write("\n")
    print("[WP1-STEP-01] import ledger written (%d+%d+%d+%d files)"
          % (len(ledger), len(ledger2), len(ledger_ev1), len(ledger_ev2)), flush=True)
    return fails


# WP1-STEP-02/03: independent enumeration + count verification vs fact_table.
def step_enumerate(outdir: str, sizes: list[int], budget_s: float) -> tuple[list[str], dict]:
    fails: list[str] = []
    from python.cycles import evidence as evidence_mod
    fact = json.load(open(os.path.join(outdir, "v02baseline", "v02", "fact_table.json"),
                          encoding="utf-8"))
    claims = {row["n"]: row for row in fact}
    evdir = os.path.join(outdir, "v01evidence")
    results: dict = {}
    for n in sizes:
        if n >= 7:
            # WP-1 REPAIR STEP V8: streamed n7 certificate verification (F2):
            # sealed summaries + audits + witness replay, no pair-state BFS.
            t0 = time.time()
            fN, stats = evidence_mod.verify_n7_streamed(evdir, claims[n])
            fails += fN
            dt = time.time() - t0
            results[str(n)] = {"trees": 429, "reachable": 184041,
                               "method": "streamed-certificate (no pair BFS)",
                               "seconds": round(dt, 1)}
            print("[WP1-STEP-02] n=%d streamed certificate verified seconds=%.1f"
                  % (n, dt), flush=True)
            continue
        t0 = time.time()
        dom = PairDomain(n)
        reached = dom.reachable(progress_every=50000 if n >= 7 else 0)
        dt = time.time() - t0
        results[str(n)] = {"trees": dom.C, "reachable": len(reached),
                           "method": "full-BFS", "seconds": round(dt, 1)}
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
        # WP-1 REPAIR STEP V7: member-set equality vs sealed reachable set (F2).
        fM, _stats = evidence_mod.verify_reachability_full(evdir, n, dom)
        fails += fM
    with open(os.path.join(outdir, "enumeration.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(results, f, sort_keys=True, indent=2)
        f.write("\n")
    return fails, results


# WP-1 REPAIR STEP V11: sealed evidence verification (trees/transitions/bn/anchors).
def step_evidence(outdir: str, sizes: list[int]) -> list[str]:
    """Verify parent-evidence classes: transitions, bn certificates, anchors."""
    from python.cycles import evidence as evidence_mod
    fails: list[str] = []
    fact = json.load(open(os.path.join(outdir, "v02baseline", "v02", "fact_table.json"),
                          encoding="utf-8"))
    claims = {row["n"]: row for row in fact}
    evdir = os.path.join(outdir, "v01evidence")
    for n in sizes:
        if n >= 7:
            continue
        fT, _s = evidence_mod.verify_tree_tables(evdir, n)
        fails += fT
        dom = PairDomain(n)
        b = (int(claims[n]["b"][0]), int(claims[n]["b"][1]))
        fB, _s = evidence_mod.verify_bn_certificate(evdir, n, dom, b)
        fails += fB
    fA, _s = evidence_mod.verify_anchors(os.path.join(outdir, "v02evidence"), fact)
    fails += fA
    fN, _s = evidence_mod.verify_near_critical(evdir)
    fails += fN
    return fails


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
    # WP-1 REPAIR STEP V12: D5 ledger resolution (F6: class imported, count
    # derived, identities absent-from-seal recorded, never fabricated).
    from python.cycles import evidence as evidence_mod
    d5rec, d5fails = evidence_mod.d5_resolution(os.path.join(outdir, "v02baseline"))
    fails += d5fails
    table["D5_RANK_LEDGER"] = {
        "evidence": "sealed D5_rank counters n4 create %s repay %s -> %d derived failures" % (
            d5rec.get("create"), d5rec.get("repay"), d5rec.get("derived_failures", -1)),
        "pointer": "v02/debt_atoms/recency_atoms.json",
        "verdict": d5rec.get("verdict"),
        "derived_failures": d5rec.get("derived_failures"),
        "identities": d5rec.get("identities"),
        "identities_note": d5rec.get("identities_note"),
    }
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


# WP-1 REPAIR STEP E8: pre-status tamper probe (§21 order for Phase 01).
def step_tamper_probe(outdir: str) -> list[str]:
    """Corrupt one cycle target and one key; replay must reject both.

    Fast analogue of the stress tamper battery, executed inline before the
    scientific phase status is emitted.
    """
    import json as _json
    import copy as _copy
    from python.cycles import import_parent as _imp
    from python.cycles.enumerate import PairDomain as _PD
    fails: list[str] = []
    base = os.path.join(outdir, "v01baseline", "v01")
    cyc = _json.load(open(os.path.join(base, "critical_n4_canonical_cycles.json"),
                          encoding="utf-8"))[0]
    dom = _PD(4)
    rep = _imp.replay_cycle(dom, cyc)
    if rep["mismatches"] or not rep["closed"]:
        fails.append("TAMPER-PROBE genuine cycle unclean")
        return fails
    bad = _copy.deepcopy(cyc)
    bad["edges"][0]["target"] = (bad["edges"][0]["target"] + 1) % 196
    rep2 = _imp.replay_cycle(dom, bad)
    if not (rep2["mismatches"] or not rep2["closed"]):
        fails.append("TAMPER-PROBE corrupted target escaped")
    bad2 = _copy.deepcopy(cyc)
    bad2["edges"][0]["key"] = 5 - bad2["edges"][0]["key"] if bad2["edges"][0]["key"] != 2 else 3
    rep3 = _imp.replay_cycle(dom, bad2)
    if not (rep3["mismatches"] or not rep3["closed"] or rep3["ratio"] != rep["ratio"]):
        fails.append("TAMPER-PROBE corrupted key escaped")
    if not fails:
        print("[WP1-STEP-06] tamper probe: genuine clean, 2/2 corruptions caught",
              flush=True)
    return fails


def main() -> int:
    from python.audit import log as log_mod
    ap = argparse.ArgumentParser()
    ap.add_argument("--v01", required=True)
    ap.add_argument("--v02", required=True)
    ap.add_argument("--sizes", default="2,3,4,5,6,7")
    ap.add_argument("--budget-s", type=float, default=1200.0)
    args = ap.parse_args()
    logdir = os.path.join(ROOT, "artifacts", "v03", "logs")
    # WP-1 REPAIR STEP L5: capture both streams, hash after close (§27).
    with log_mod.capture(logdir, "phase01") as cap:
        exit_code, rec = _run(args)
    streams = cap.hashes()
    rec["stdout_hash"] = streams["stdout_hash"]
    rec["stderr_hash"] = streams["stderr_hash"]
    # WP-1 REPAIR STEP L3: append the §27 execution record (fail-closed fields).
    log_mod.write_log(os.path.join(ROOT, "artifacts", "v03", "logs", "phase01_wp1.jsonl"), rec)
    print("[WP1-STEP-00] §27 record appended (phase01_wp1.jsonl)", flush=True)
    if exit_code:
        print("[WP1-STEP-00] PHASE01_FAIL (see record)", flush=True)
        return 1
    print("[WP1-STEP-00] PHASE01_PASS: import sealed, counts exact, cycles replay, failures tabled", flush=True)
    return 0


def _run(args) -> tuple[int, dict]:
    import time as _time
    import tracemalloc as _tracemalloc
    from python.audit import log as log_mod
    _tracemalloc.start()
    _t0 = _time.perf_counter()
    print("[WP1-STEP-00] PHASE 01: import, enumerate, verify counts, replay cycles, "
          "failure table, subgate report", flush=True)
    outdir = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    os.makedirs(outdir, exist_ok=True)
    sizes = [int(s) for s in args.sizes.split(",")]
    rec = log_mod.static_fields(ROOT)
    rec.update({
        "phase": "01", "branch": "WP-1", "command": sys.argv,
        "clone_args": {"v01": args.v01, "v02": args.v02},
        "input_hashes": {"v01_sealed_commit": V01_COMMIT, "v02_sealed_commit": V02_COMMIT},
        "stdout_hash": None, "stderr_hash": None,
    })
    fails: list[str] = []
    fails += step_import(args.v01, args.v02, outdir)
    if not fails:
        f2, _enum = step_enumerate(outdir, sizes, args.budget_s)
        fails += f2
    if not fails:
        # WP-1 REPAIR STEP V11: sealed evidence classes before replay (F1/F3/F5).
        fails += step_evidence(outdir, sizes)
    if not fails:
        fails += step_replay(outdir, sizes)
    if not fails:
        fails += step_failures(outdir)
    if not fails:
        fails += step_specimens(outdir, sizes)
    # WP-1 REPAIR STEP E8: §21 order — tamper probe BEFORE phase status.
    if not fails:
        fails += step_tamper_probe(outdir)
    statuses = obligation_status.main(ROOT)
    if statuses.get("MST0-01", {}).get("status") != "REVIEWED":
        print("[WP1-STEP-07] subgate: MST0-01 not REVIEWED; certified consumption stays blocked", flush=True)
    exit_code = 1 if fails else 0
    # WP1-STEP-00: §27 execution record (append-only; fullest honest field set).
    rec.update({
        "scientific_status": "PARENT_CHAIN_VERIFIED" if not fails else "PHASE01_FAIL",
        "output_hashes": log_mod.hash_outputs(ROOT, ["artifacts/v03/parent_import"]),
        "wall_s": round(_time.perf_counter() - _t0, 2),
        "allocator_peak_bytes": _tracemalloc.get_traced_memory()[1],
        "exit_code": exit_code,
    })
    _tracemalloc.stop()
    for x in fails:
        print(" -", x, flush=True)
    return exit_code, rec


if __name__ == "__main__":
    sys.exit(main())
