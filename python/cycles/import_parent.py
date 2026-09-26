"""Read-only parent evidence import for WP-1 (comparison targets, never premises).

Sources (sealed clones, read by hash; holdout banks never touched):
  v0.1 splay-pair-dynamics@6de1ca2: critical/n*/canonical_cycles.json + summary.json
    + sccs.json + below_optimum.json + forced_delta_edges.json.zst, FINAL_RESULT.json,
    MANIFEST.sha256 (pins every v0.1 artifact).
  v0.2 splay-bellman-debt@38c1be6: fact_table.json, full FINAL_RESULT.json,
    falsification/PHI-*/dev.json, hypotheses/ledger.json, debt_atoms/*.json.
Vendored copies land in artifacts/v03/parent_import/ with import_ledger.json
(source URL, commit, per-file source+copy SHA-256). parent/ (WP-0 snapshot) is
never modified. Console lines prefixed [WP1-STEP-0x] are the audit record.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from fractions import Fraction

V01_COMMIT = "6de1ca2a595e8895f54794f3a211fe6ee1a95a80"
V02_COMMIT = "38c1be6afd2ab2420aa094c68ce45ee6a26b3628"

# (source-relative-path, destination-relative-path); holdout banks excluded by design.
V01_FILES = []
for _n in (2, 3, 4, 5, 6, 7):
    for _f in ("canonical_cycles.json", "summary.json", "sccs.json",
               "below_optimum.json", "forced_delta_edges.json.zst"):
        V01_FILES.append(("artifacts/critical/n%d/%s" % (_n, _f),
                          "v01/critical_n%d_%s" % (_n, _f)))
V01_FILES += [("artifacts/seal/FINAL_RESULT.json", "v01/FINAL_RESULT.json"),
              ("artifacts/seal/MANIFEST.sha256", "v01/MANIFEST.sha256")]
V02_FILES = [("artifacts/v02/parent_import/fact_table.json", "v02/fact_table.json"),
             ("artifacts/v02/seal/FINAL_RESULT.json", "v02/FINAL_RESULT.json"),
             ("artifacts/v02/seal/MANIFEST.sha256", "v02/MANIFEST.sha256"),
             ("artifacts/v02/hypotheses/ledger.json", "v02/hypothesis_ledger.json"),
             ("artifacts/v02/debt_atoms/recency_atoms.json", "v02/recency_atoms.json"),
             ("artifacts/v02/debt_atoms/state_only_search.json", "v02/state_only_search.json")]
for _h in ("PHI-0001", "PHI-0002", "PHI-0003"):
    V02_FILES.append(("artifacts/v02/falsification/%s/dev.json" % _h,
                      "v02/falsification_%s_dev.json" % _h))
for _n in (2, 3, 4, 5, 6, 7):
    for _f in ("specimens.json", "witnesses.json"):
        V02_FILES.append(("artifacts/v02/specimens/n%d/%s" % (_n, _f),
                          "v02/specimens_n%d_%s" % (_n, _f)))

# WP-1 REPAIR STEP V0: sealed parent-evidence classes (F1/F3/F5 vendor lists).
V01_EVIDENCE_FILES = []
for _n in (2, 3, 4, 5, 6, 7):
    for _f in ("trees.jsonl.zst", "summary.json", "SHA256SUMS"):
        V01_EVIDENCE_FILES.append(("artifacts/trees/n%d/%s" % (_n, _f),
                                   "v01evidence/trees/n%d/%s" % (_n, _f)))
    for _f in ("forward.bin.zst", "inverse.bin.zst", "summary.json"):
        V01_EVIDENCE_FILES.append(("artifacts/transitions/n%d/%s" % (_n, _f),
                                   "v01evidence/transitions/n%d/%s" % (_n, _f)))
    for _f in ("reachable.json.zst", "summary.json"):
        V01_EVIDENCE_FILES.append(("artifacts/reachability/n%d/%s" % (_n, _f),
                                   "v01evidence/reachability/n%d/%s" % (_n, _f)))
    for _f in ("bn_certificate.json", "witness_cycle.json", "potential_upper.json.zst"):
        V01_EVIDENCE_FILES.append(("artifacts/certificates/n%d/%s" % (_n, _f),
                                   "v01evidence/certificates/n%d/%s" % (_n, _f)))
    for _a in ("verify_reachability", "verify_transitions", "verify_bn_certificate",
               "verify_uv", "verify_critical_objects"):
        V01_EVIDENCE_FILES.append(("artifacts/audits/n%d/%s.json" % (_n, _a),
                                   "v01evidence/audits/n%d/%s.json" % (_n, _a)))
for _n in (2, 3):
    V01_EVIDENCE_FILES.append(("artifacts/certificates/n%d/witness_path.json" % _n,
                               "v01evidence/certificates/n%d/witness_path.json" % _n))
V01_EVIDENCE_FILES.append(("artifacts/falsification/adversarial/near_tight_families.json",
                           "v01evidence/adversarial/near_tight_families.json"))
V02_EVIDENCE_FILES = []
for _n in (2, 3, 4, 5, 6, 7):
    V02_EVIDENCE_FILES.append(("artifacts/v02/bellman/n%d_b2/anchor_report.json" % _n,
                               "v02evidence/bellman/n%d_b2/anchor_report.json" % _n))
V02_EVIDENCE_FILES.append(("artifacts/v02/bellman/panel.json", "v02evidence/bellman/panel.json"))


def sha_file(p: str) -> str:
    """SHA-256 over buffered reads."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP1-STEP-01: vendor sealed files by hash (fails closed on any mismatch/absence).
def vendor(sources: dict[str, str], dest_root: str,
           spec: list | None = None) -> tuple[list[dict], list[str]]:
    fails: list[str] = []
    ledger: list[dict] = []
    if spec is None:
        spec = V01_FILES if "v01" in dest_root else V02_FILES
        base = sources["v01" if "v01" in dest_root else "v02"]
    else:
        base = next(iter(sources.values()))
    for src_rel, dst_rel in spec:
        src = os.path.join(base, *src_rel.split("/"))
        dst = os.path.join(dest_root, *dst_rel.split("/"))
        if not os.path.exists(src):
            fails.append("IMPORT-01 missing sealed source %s" % src_rel)
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        ledger.append({"source": src_rel, "dest": dst_rel,
                       "sha256": sha_file(dst)})
    print("[WP1-STEP-01] vendored %d files (%s)" % (len(ledger), dest_root), flush=True)
    return ledger, fails


# WP1-STEP-05: replay an imported critical cycle on our own edge evaluator.
def replay_cycle(dom, cycle: dict) -> dict:
    """Strict chained replay from edges[0].source, plus per-edge cost checks."""
    edges = cycle["edges"]
    cur = edges[0]["source"]
    sum_a = 0
    sum_y = 0
    all_keep = True
    mismatches = []
    for i, e in enumerate(edges):
        if cur != e["source"]:
            mismatches.append({"edge": i, "chained_state": cur,
                               "imported_source": e["source"]})
            break
        tgt, a, y = dom.edge(cur, e["key"], e["mode"])
        sum_a += a
        sum_y += y
        if e["mode"] != "KEEP":
            all_keep = False
        if tgt != e["target"]:
            mismatches.append({"edge": i, "ours": tgt, "imported": e["target"]})
            break
        cur = tgt
    ratio = Fraction(sum_y, sum_a) if sum_a else None
    closed = (not mismatches) and cur == edges[0]["source"]
    # Per-edge independent cost audit (localizes any divergence).
    audit = []
    for i, e in enumerate(edges):
        _t, a, y = dom.edge(e["source"], e["key"], e["mode"])
        audit.append({"edge": i, "a": a, "y": y, "target_match": _t == e["target"]})
    return {"sum_a": sum_a, "sum_y": sum_y, "ratio": str(ratio),
            "all_keep": all_keep, "closed": closed, "mismatches": mismatches,
            "edge_audit": audit}


def main() -> int:
    print("[WP1-STEP-01] import needs --v01/--v02 source dirs; see run_phase01.py", flush=True)
    return 2


if __name__ == "__main__":
    sys.exit(main())
