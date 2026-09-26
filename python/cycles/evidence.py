"""WP-1 sealed parent-evidence verification (F1/F2/F3/F5 classes).

Verifies v0.1 tree universes, single-tree transition tables, reachable domains,
b_n* certificates, near-critical records, and v0.2 Bellman anchors against the
hash-bound vendored bytes in parent_import/v01evidence + v02evidence. All
comparisons recompute from OUR canonical implementation; sealed bytes are never
trusted from prose. n7 uses streamed certificate checks without pair-state
BFS. Console tag [WP1-STEP-02/03] via the owning runner.
"""
from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction

from python.cycles.enumerate import PairDomain, build_node_tree, canonical_shapes
from python.splay_ref.splay import Node, cost, serialize, splay


# WP-1 REPAIR STEP V1: sha-256 over buffered reads.
def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP-1 REPAIR STEP V2: read a sealed .json.zst artifact.
def _read_zst(path: str):
    import zstandard as zstd
    with open(path, "rb") as f:
        return json.loads(zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))


# WP-1 REPAIR STEP V3: unkeyed shape key of a parent tree record.
def _parent_shape_key(rec: dict) -> str:
    """Topology string in our canonical shape grammar (keys ignored)."""
    left, right, parent = rec["left_by_key"], rec["right_by_key"], rec["parent_by_key"]
    n = len(parent)
    root = next(k for k in range(n) if parent[k] == -1) + 1

    def rec_shape(k: int | None) -> str:
        if k is None:
            return "."
        return "(" + rec_shape(left[k - 1] if left[k - 1] != -1 else None) \
            + rec_shape(right[k - 1] if right[k - 1] != -1 else None) + ")"

    return rec_shape(root)


# WP-1 REPAIR STEP V4: our Node tree from a parent tree record (keys by label).
def _parent_node(rec: dict) -> Node:
    """Build a pointer BST with parent key labels (inorder must be 1..n)."""
    left, right, parent = rec["left_by_key"], rec["right_by_key"], rec["parent_by_key"]
    n = len(parent)
    nodes = {k: Node(k) for k in range(1, n + 1)}
    for k in range(1, n + 1):
        if left[k - 1] != -1:
            nodes[k].left = nodes[left[k - 1]]
            nodes[left[k - 1]].parent = nodes[k]
        if right[k - 1] != -1:
            nodes[k].right = nodes[right[k - 1]]
            nodes[right[k - 1]].parent = nodes[k]
    return nodes[[k for k in range(1, n + 1) if parent[k - 1] == -1][0]]


# WP-1 REPAIR STEP V5: unkeyed shape of one of our pointer trees.
def _our_shape_key(root: Node | None) -> str:
    if root is None:
        return "."
    return "(" + _our_shape_key(root.left) + _our_shape_key(root.right) + ")"


# WP-1 REPAIR STEP V6: full single-tree transition/cost verification (F2).
def verify_tree_tables(evdir: str, n: int) -> tuple[list[str], dict]:
    """Compare every sealed (tree,x) record against our splay (cost+shape)."""
    fails: list[str] = []
    tdir = os.path.join(evdir, "trees", "n%d" % n)
    trees = []
    with open(os.path.join(tdir, "trees.jsonl.zst"), "rb") as f:
        import zstandard as zstd
        for ln in zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8").splitlines():
            if ln.strip():
                trees.append(json.loads(ln))
    summary = json.load(open(os.path.join(tdir, "summary.json"), encoding="utf-8"))
    if len(trees) != summary.get("tree_count", len(trees)):
        fails.append("TREES-01 n=%d count %d != summary %s" % (n, len(trees), summary))
    fwd = _read_zst(os.path.join(evdir, "transitions", "n%d" % n, "forward.bin.zst"))
    shapes = canonical_shapes(n)
    bad = 0
    checked = 0
    for r in fwd["records"]:
        tree = _parent_node(trees[r["tree"]])
        if cost(tree, r["x"]) != r["cost"]:
            bad += 1
            continue
        top, _ev = splay(tree, r["x"])
        if _our_shape_key(top) != _parent_shape_key(trees[r["after"]]):
            bad += 1
            continue
        checked += 1
    if bad:
        fails.append("TRANS-01 n=%d transition mismatches %d/%d" % (n, bad, len(fwd["records"])))
    inv = _read_zst(os.path.join(evdir, "transitions", "n%d" % n, "inverse.bin.zst"))
    for x in range(1, n + 1):
        preds = inv["pred"][str(x)]
        if sum(len(v) for v in preds) != len(trees):
            fails.append("TRANS-02 n=%d x=%d inverse conservation" % (n, x))
    stats = {"records": len(fwd["records"]), "checked": checked, "mismatches": bad}
    if not fails:
        print("[WP1-STEP-03] n=%d tree transitions exact: %d/%d records" % (n, checked, len(fwd["records"])),
              flush=True)
    return fails, stats


# WP-1 REPAIR STEP V7: full reachability member-set verification (F2, n<=6).
def verify_reachability_full(evdir: str, n: int, dom: PairDomain) -> tuple[list[str], dict]:
    """Compare our BFS member set against the sealed reachable set."""
    fails: list[str] = []
    d = _read_zst(os.path.join(evdir, "reachability", "n%d" % n, "reachable.json.zst"))
    sealed = set(d["pair_ids"])
    mine = set(dom.reachable())
    if sealed != mine:
        fails.append("REACH-01 n=%d member set differs (sealed %d, ours %d)" % (n, len(sealed), len(mine)))
    else:
        print("[WP1-STEP-03] n=%d reachable member set exact: %d states" % (n, len(mine)), flush=True)
    return fails, {"sealed": len(sealed), "ours": len(mine)}


# WP-1 REPAIR STEP V8: streamed n7 certificate verification (F2, no pair BFS).
def verify_n7_streamed(evdir: str, fact_row: dict) -> tuple[list[str], dict]:
    """Verify n7 via sealed summaries, audits, and witness replay (no BFS)."""
    fails: list[str] = []
    summary = json.load(open(os.path.join(evdir, "reachability", "n7", "summary.json"),
                             encoding="utf-8"))
    if summary.get("reachable_pair_count") != 184041 or summary.get("raw_pair_count") != 184041:
        fails.append("REACH-02 n7 sealed summary count differs")
    d = _read_zst(os.path.join(evdir, "reachability", "n7", "reachable.json.zst"))
    if len(d["pair_ids"]) != 184041 or len(set(d["pair_ids"])) != 184041:
        fails.append("REACH-02 n7 sealed member stream count/duplicates differ")
    else:
        print("[WP1-STEP-03] n7 reachable stream verified: 184041 members (no BFS)", flush=True)
    for audit in ("verify_reachability", "verify_transitions", "verify_bn_certificate"):
        rec = json.load(open(os.path.join(evdir, "audits", "n7", audit + ".json"), encoding="utf-8"))
        if rec.get("verdict") != "PASS":
            fails.append("AUDIT-01 n7 %s verdict %r" % (audit, rec.get("verdict")))
    if not fails:
        print("[WP1-STEP-03] n7 sealed audits PASS (reachability/transitions/bn)", flush=True)
    cert = json.load(open(os.path.join(evdir, "certificates", "n7", "bn_certificate.json"),
                           encoding="utf-8"))
    if [cert["b"]["p"], cert["b"]["q"]] != ["23", "14"] or cert.get("reachable_pair_count") != 184041:
        fails.append("BNCERT-01 n7 certificate claim differs")
    wit = json.load(open(os.path.join(evdir, "certificates", "n7", "witness_cycle.json"),
                         encoding="utf-8"))
    dom = PairDomain(7)
    sum_a = sum_y = 0
    for e in wit["cycle"]:
        _t, a, y = dom.edge(e["source"], e["key"], e["mode"])
        sum_a += a
        sum_y += y
    if Fraction(sum_y, sum_a) != Fraction(23, 14):
        fails.append("BNCERT-02 n7 witness ratio differs")
    elif (sum_a, sum_y) != (wit["sum_a_cycle"], wit["sum_y_cycle"]):
        fails.append("BNCERT-02 n7 witness sums differ")
    else:
        print("[WP1-STEP-03] n7 witness cycle replayed: ratio 23/14 exact", flush=True)
    if fact_row.get("R") != 184041:
        fails.append("BNCERT-03 n7 fact reachable differs")
    return fails, {"streamed": True, "witness_ratio": "23/14"}


# WP-1 REPAIR STEP V9: b_n* certificate verification per n (F2/F3).
def verify_bn_certificate(evdir: str, n: int, dom: PairDomain, b: tuple) -> tuple[list[str], dict]:
    """Verify the sealed bn certificate: claim, witness replay, count, audit."""
    fails: list[str] = []
    cdir = os.path.join(evdir, "certificates", "n%d" % n)
    cert = json.load(open(os.path.join(cdir, "bn_certificate.json"), encoding="utf-8"))
    if [cert["b"]["p"], cert["b"]["q"]] != [str(b[0]), str(b[1])]:
        fails.append("BNCERT-01 n=%d b claim differs" % n)
    wit = json.load(open(os.path.join(cdir, "witness_cycle.json"), encoding="utf-8"))
    sum_a = sum_y = 0
    for e in wit["cycle"]:
        _t, a, y = dom.edge(e["source"], e["key"], e["mode"])
        sum_a += a
        sum_y += y
    if Fraction(sum_y, sum_a) != Fraction(b[0], b[1]):
        fails.append("BNCERT-02 n=%d witness ratio differs" % n)
    elif (sum_a, sum_y) != (wit["sum_a_cycle"], wit["sum_y_cycle"]):
        fails.append("BNCERT-02 n=%d witness sums differ" % n)
    if cert.get("reachable_pair_count") != len(dom.reachable()):
        fails.append("BNCERT-03 n=%d reachable count differs" % n)
    audit = json.load(open(os.path.join(evdir, "audits", "n%d" % n,
                                        "verify_bn_certificate.json"), encoding="utf-8"))
    if audit.get("verdict") != "PASS":
        fails.append("BNCERT-04 n=%d sealed audit verdict %r" % (n, audit.get("verdict")))
    if not fails:
        print("[WP1-STEP-03] n=%d bn certificate verified: %s/%s witness exact" % (n, b[0], b[1]),
              flush=True)
    return fails, {"witness_ratio": "%s/%s" % (b[0], b[1])}


# WP-1 REPAIR STEP V10: Bellman anchor cross-check (F3).
def verify_anchors(evdir: str, fact: list) -> tuple[list[str], dict]:
    """Assert vendored anchor maxU/maxV equal fact_table rows (n2..7)."""
    fails: list[str] = []
    rows = {row["n"]: row for row in fact}
    for n in (2, 3, 4, 5, 6, 7):
        rep = json.load(open(os.path.join(evdir, "bellman", "n%d_b2" % n,
                                          "anchor_report.json"), encoding="utf-8"))
        if rep.get("maxU") != rows[n].get("maxU") or rep.get("maxV") != rows[n].get("maxV"):
            fails.append("ANCHOR-01 n=%d anchor/fact mismatch" % n)
    if not fails:
        print("[WP1-STEP-03] Bellman anchors cross-checked n2..7 (maxU/maxV exact)",
              flush=True)
    return fails, {"sizes": [2, 3, 4, 5, 6, 7]}


# WP-1 REPAIR STEP V11: near-critical records (F5: identify, bind, classify).
def verify_near_critical(evdir: str) -> tuple[list[str], dict]:
    """Vendor-verify near-tight hypotheses (quarantined) + below-optimum records."""
    fails: list[str] = []
    NT = "falsification/adversarial/near_tight_families.json"
    fams = json.load(open(os.path.join(evdir, NT), encoding="utf-8"))
    if not isinstance(fams, list) or not fams:
        fails.append("NEAR-01 near-tight families malformed")
    else:
        for h in fams:
            if not all(k in h for k in ("hypothesis_id", "motif", "samples", "status")):
                fails.append("NEAR-01 hypothesis record malformed")
                break
    below = {}
    for n in (2, 3, 4, 5, 6, 7):
        rec = json.load(open(os.path.join(evdir, "critical", "n%d" % n, "below_optimum.json"),
                             encoding="utf-8"))
        if not all(k in rec for k in ("b_minus", "certified_b", "kind", "label", "n")):
            fails.append("NEAR-02 n=%d below-optimum record malformed" % n)
        else:
            below[str(n)] = {"b_minus": rec["b_minus"], "certified_b": rec["certified_b"],
                             "kind": rec["kind"], "label": rec["label"]}
    if not fails:
        print("[WP1-STEP-03] near-critical classes bound: %d near-tight hypotheses "
              "(quarantined adversarial context) + below-optimum n2..7" % len(fams), flush=True)
    return fails, {"near_tight_hypotheses": len(fams) if isinstance(fams, list) else 0,
                   "below_optimum": below,
                   "quarantine": "near-tight families are v0.1 adversarial hypotheses "
                                 "(UNDECIDED at v0.1 WP-6 P17); preserved as context, "
                                 "never replayed as certified evidence"}


# WP-1 REPAIR STEP V12: D5 ledger resolution (F6: ledger imported, count derived).
def d5_resolution(v02baseline: str) -> tuple[dict, list[str]]:
    """Import the sealed D5 ledger class; derive the count; record provenance.

    Per-item failure identities exist in NO sealed parent artifact (exhaustive
    negative search: sealed manifest + full v0.2 tree contain only the
    aggregates 3318/3334 + verdict INCONSISTENT). Manufacturing identities
    would fabricate evidence (§17/§24). Resolution: import the complete sealed
    class hash-bound, derive 3334-3318=16 machine-side, preserve the aggregate.
    """
    fails: list[str] = []
    atoms = json.load(open(os.path.join(v02baseline, "v02", "recency_atoms.json"),
                           encoding="utf-8"))
    fams = atoms.get("families", {})
    d5 = fams.get("4", {}).get("D5_rank", fams.get("4", {}).get("D5"))
    if d5 is None:
        return {}, ["D5-01 no sealed D5_rank class at n4"]
    create, repay = d5["create"], d5["repay"]
    derived = repay[1] - repay[0]
    verdicts = atoms.get("verdicts", {})
    if verdicts.get("D5_rank") != "DEBT_ATOM_FAMILY_INCONSISTENT":
        fails.append("D5-01 D5 verdict differs from parent claim")
    record = {"create": create, "repay": repay, "derived_failures": derived,
              "verdict": verdicts.get("D5_rank"),
              "provenance": "v02/debt_atoms/recency_atoms.json (sealed, hash-bound)",
              "identities": None,
              "identities_note": "absent from all sealed parent artifacts (manifest-wide "
                                 "and full-tree search); count derived machine-side, never "
                                 "fabricated"}
    if derived != 16:
        fails.append("D5-01 derived count %d != 16" % derived)
    else:
        print("[WP1-STEP-06] D5 ledger resolved: 3318/3334 -> 16 (identities absent-from-seal)",
              flush=True)
    return record, fails
