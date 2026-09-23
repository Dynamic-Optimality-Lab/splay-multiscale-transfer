"""WP-0 stress tests: determinism, idempotency, fail-closed mutations, invalid inputs.

All mutation probes run against temp-dir fixtures (copies), never the real tree.
Each test prints STRESS-<id> lines; any failure exits non-zero.
"""
import copy
import json
import os
import random
import shutil
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.audit import check_prereg  # noqa: E402
from python.audit import verify_parent  # noqa: E402
from python.rotations.trace import trace_delete, trace_keep  # noqa: E402
from python.splay_ref import independent as I  # noqa: E402
from python.splay_ref.splay import build_balanced, cost, inorder, serialize, splay  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("STRESS-PASS " if cond else "STRESS-FAIL ") + name)
    if not cond:
        FAILS.append(name)


def fixture_root() -> str:
    """Temp copy of the repo files the checks read (mutable, disposable)."""
    tmp = tempfile.mkdtemp(prefix="wp0stress_")
    for rel in ["parent", "prereg", "math", "external",
                "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md",
                "IMPLEMENTATION_SPEC_v0.3.md"]:
        src = os.path.join(ROOT, rel)
        dst = os.path.join(tmp, rel)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    os.makedirs(os.path.join(tmp, "artifacts", "v03"), exist_ok=True)
    with open(os.path.join(tmp, "artifacts", "v03", "STALE_CLEARANCE.json"), "w") as f:
        f.write("{}")
    # Fixture must be mutable (copies inherit the parent/ read-only lock).
    import stat as _stat
    for dirpath, _dn, fns in os.walk(tmp):
        for fn in fns:
            os.chmod(os.path.join(dirpath, fn), _stat.S_IWRITE | _stat.S_IREAD)
    return tmp


def test_determinism() -> None:
    rng = random.Random(20260923)
    seqs = [[rng.randint(1, 9) for _ in range(40)] for _ in range(3)]
    for si, seq in enumerate(seqs):
        outs = []
        for _rep in range(2):
            r = build_balanced(list(range(1, 10)))
            st = I.build_balanced_dict(list(range(1, 10)))
            trace = []
            for x in seq:
                r, e1 = splay(r, x)
                e2 = I.splay2(st, x)
                trace.append(([e["case"] for e in e1], [e["case"] for e in e2], serialize(r)))
            outs.append(trace)
        check(f"STRESS-DET repeat identical seq{si}", outs[0] == outs[1])
        check(f"STRESS-DET dual-core agree seq{si}",
              all(a == b for a, b, _t in outs[0]))
    t0 = time.time()
    r = build_balanced(list(range(1, 65)))
    for x in [rng.randint(1, 64) for _ in range(200)]:
        r, _ = splay(r, x)
    dt = time.time() - t0
    print("STRESS-PERF 200 accesses n=64: %.2fs" % dt)
    check("STRESS-PERF under 30s", dt < 30)


def test_idempotency() -> None:
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import freeze_prereg
    sys.path.pop(0)
    a = freeze_prereg.normative_hashes(ROOT)
    b = freeze_prereg.normative_hashes(ROOT)
    check("STRESS-IDEM freeze deterministic", a == b)
    committed = open(os.path.join(ROOT, "prereg", "prereg_sha256.txt")).read()
    check("STRESS-IDEM freeze matches sealed file",
          "\n".join(sorted(a)) + "\n" == committed.replace("\r\n", "\n"))


def test_mutations_fail_closed() -> None:
    tmp = fixture_root()
    try:
        # Tampered seal must fail PARENT-01.
        p = os.path.join(tmp, "parent", "V02_SEAL.json")
        d = json.load(open(p))
        d["sealed_commit"] = "0" * 40
        json.dump(d, open(p, "w"))
        f = verify_parent.check_parent_pin(tmp)
        check("STRESS-MUT tampered seal fails", any("PARENT-01" in x for x in f))
        # Restored seal passes (proves the check discriminates, not blanket-fails).
        shutil.copy2(os.path.join(ROOT, "parent", "V02_SEAL.json"), p)
        check("STRESS-MUT restored seal passes", verify_parent.check_parent_pin(tmp) == [])
        # Missing gate obligation fails.
        g = os.path.join(tmp, "prereg", "theorem_gate_matrix.yaml")
        txt = open(g).read().replace("MST0-26:", "MST0-XX:")
        open(g, "w").write(txt)
        check("STRESS-MUT dropped obligation fails",
              any("GATE-01" in x for x in check_prereg.check_theorem_gates(tmp)))
        # Resolved-early L6 status fails (must start UNRESOLVED).
        l6 = os.path.join(tmp, "prereg", "l6_translation_v0.3.yaml")
        txt = open(l6).read().replace("mapping_status: UNRESOLVED_PRE_PROOF",
                                      "mapping_status: SAME_proved_equivalent", 1)
        open(l6, "w").write(txt)
        check("STRESS-MUT pre-resolved mapping fails",
              any("L6-00" in x for x in check_prereg.check_l6_contract(tmp)))
        # Early science file fails the allowlist.
        os.makedirs(os.path.join(tmp, "artifacts", "v03", "hypotheses"))
        open(os.path.join(tmp, "artifacts", "v03", "hypotheses", "MSTC-0001.json"), "w").write("{}")
        check("STRESS-MUT early science fails",
              any("EARLY-SCIENCE" in x for x in check_prereg.check_no_early_science(tmp)))
        # Missing fallback field fails (object-level mutation, not the schema line).
        l6b = os.path.join(tmp, "prereg", "l6_translation_v0.3.yaml")
        shutil.copy2(os.path.join(ROOT, "prereg", "l6_translation_v0.3.yaml"), l6b)
        txt = open(l6b).read().replace("fallback_pa_native_object: MST_NATIVE_DEPTH_RANK",
                                       "fallback_pa_native_object_MISSING: MST_NATIVE_DEPTH_RANK", 1)
        open(l6b, "w").write(txt)
        check("STRESS-MUT dropped fallback fails",
              any("L6-00" in x for x in check_prereg.check_l6_contract(tmp)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_invalid_inputs() -> None:
    r = build_balanced([1, 2, 3])
    try:
        splay(r, 99)
        check("STRESS-INV missing key raises", False)
    except KeyError:
        check("STRESS-INV missing key raises", True)
    try:
        cost(r, 99)
        check("STRESS-INV cost missing key raises", False)
    except KeyError:
        check("STRESS-INV cost missing key raises", True)
    a = build_balanced([1, 2, 3])
    b = build_balanced([1, 2, 3])
    t = trace_keep(a, b, 2, "e-stress")
    check("STRESS-INV trace snapshot 64hex",
          len(t["reference_snapshot_hash"]) == 64)
    check("STRESS-INV inorder preserved", inorder(a) == [1, 2, 3])
    a2 = build_balanced([1, 2, 3])
    b2 = build_balanced([1, 2, 3])
    t2 = trace_delete(a2, b2, 1, "e-stress-del")
    check("STRESS-INV delete y=0", t2["y"] == 0 and t2["mode"] == "DELETE")


def test_stubs_fail_closed() -> None:
    import subprocess
    for n in (2, 9, 19):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run_phase%02d.py" % n)],
                           capture_output=True, text=True)
        check("STRESS-STUB phase%02d exit 2" % n, r.returncode == 2)
        check("STRESS-STUB phase%02d says NOT_AUTHORIZED" % n, "NOT_AUTHORIZED" in r.stdout)
    # Real runner 01 refuses without required source args (argparse exit 2).
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run_phase01.py")],
                       capture_output=True, text=True)
    check("STRESS-STUB phase01 real runner refuses arg-less", r.returncode != 0)
    # Real runner 03 is idempotent: re-run succeeds and reproduces byte-identical outputs.
    import hashlib as _hl
    before = {}
    expdir = os.path.join(ROOT, "artifacts", "v03", "cycles", "expanded")
    for fn in sorted(os.listdir(expdir)):
        before[fn] = _hl.sha256(open(os.path.join(expdir, fn), "rb").read()).hexdigest()
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run_phase03.py")],
                       capture_output=True, text=True)
    after = {fn: _hl.sha256(open(os.path.join(expdir, fn), "rb").read()).hexdigest()
             for fn in sorted(os.listdir(expdir))}
    check("STRESS-STUB phase03 re-run exit 0", r.returncode == 0)
    check("STRESS-STUB phase03 outputs idempotent", before == after)


if __name__ == "__main__":
    test_determinism()
    test_idempotency()
    test_mutations_fail_closed()
    test_invalid_inputs()
    test_stubs_fail_closed()
    print("STRESS-FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
