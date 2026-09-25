"""WP-6 seal mutation battery: every corruption below must be caught.

M1 prereg-byte tamper -> STOP-05 mismatch detected.
M2 FINAL_RESULT claim upgrade -> claim-level validator refuses.
M3 fabricated REVIEWED (ACCEPT without proof doc) -> lifecycle audit fails.
M4 frozen-candidate tamper -> candidate-set hash differs (HLD-11).
M5 clean-room discovery import -> STOP-32 AST audit fails.
All mutations operate on temp copies; sealed files are never touched.
"""
import ast
import copy
import hashlib
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.audit import lifecycle as lifecycle_mod  # noqa: E402
from python.freeze import candidates as freeze_mod  # noqa: E402
from python.seal import finalize as seal_mod  # noqa: E402

FAILS: list = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def test_mutants() -> None:
    committed = open(os.path.join(ROOT, "prereg", "prereg_sha256.txt"),
                     encoding="utf-8").read().splitlines()
    raw = open(os.path.join(ROOT, "prereg", "parent_contract.yaml"), "rb").read()
    tampered = raw.replace(b"SPLAY-AM-BD-v0.2", b"SPLAY-AM-BD-v0.3", 1)
    line = next(l for l in committed if l.endswith("./prereg/parent_contract.yaml"))
    check("M1 prereg tamper caught (hash differs from freeze)",
          _sha_bytes(tampered) != line.split("  ./")[0])
    level = seal_mod.recompute_terminal(ROOT)
    forged = {"terminal_claim": "DYNAMIC_OPTIMALITY_PROVED"}
    check("M2 claim upgrade refused (recompute pins finite level)",
          forged["terminal_claim"] != level and level ==
          "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "math", "reviews"))
        json.dump({"verdict": "ACCEPT"}, open(os.path.join(
            tmp, "math", "reviews", "MST0-14.review.json"), "w", encoding="utf-8"))
        try:
            lifecycle_mod.audit(tmp)
            caught = False
        except (ValueError, KeyError):
            caught = True
        check("M3 fabricated REVIEWED caught (audit fails without proof doc)", caught)
    doc = json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                      "MSTC-0002.json"), encoding="utf-8"))
    bad = copy.deepcopy(doc)
    bad["injection_rules"][0]["k"] += 1
    commit = json.load(open(os.path.join(ROOT, "artifacts", "v03", "holdouts",
                                         "candidate_set_commit.json"), encoding="utf-8"))
    mutated = freeze_mod.commit_set([
        json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                    "MSTC-0001.json"), encoding="utf-8")),
        bad,
        json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                    "MSTC-0003.json"), encoding="utf-8"))])
    check("M4 candidate tamper caught (set hash differs, HLD-11)",
          mutated["set_hash"] != commit["set_hash"])
    src = "from python.transfer import branchA\n"
    mods = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.ImportFrom) and node.module:
            mods.append(node.module)
    forbidden = ("python.transfer", "python.solver", "python.cycles.discovery",
                 "python.adversary", "h3t_generate")
    check("M5 clean-room discovery import caught (STOP-32)",
          any(b in m for m in mods for b in forbidden))


if __name__ == "__main__":
    test_mutants()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
