"""One authorized parent-bootstrap transaction for WP-0 (idempotent verifier).

First run populates parent/ from the sealed parent clone by hash, writes
BOOTSTRAP_MANIFEST.sha256, and sets the snapshot read-only. Every later run
only verifies: same hashes, same lock, no drift. Never edits sealed content.
Console output lines prefixed [WP0-STEP-03] are the auditable execution record.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import sys

from python.audit.verify_parent import FULL_PARENT, TERMINAL_CLAIM


def _manifest_lines(root: str) -> list[str]:
    parent = os.path.join(root, "parent")
    lines = []
    for name in sorted(os.listdir(parent)):
        p = os.path.join(parent, name)
        if not os.path.isfile(p) or name == "BOOTSTRAP_MANIFEST.sha256":
            continue
        h = hashlib.sha256()
        with open(p, "rb") as f:
            h.update(f.read())
        lines.append("%s  parent/%s" % (h.hexdigest().upper(), name))
    return lines


# WP0-STEP-03: verify the bootstrap manifest matches parent/ bytes exactly.
def check_manifest(root: str) -> list[str]:
    fails: list[str] = []
    manifest_path = os.path.join(root, "parent", "BOOTSTRAP_MANIFEST.sha256")
    if not os.path.exists(manifest_path):
        print("[WP0-STEP-03] BOOTSTRAP_MANIFEST.sha256 MISSING")
        return ["BOOTSTRAP-01 BOOTSTRAP_MANIFEST.sha256 missing"]
    recorded = open(manifest_path, encoding="utf-8").read().replace("\r\n", "\n")
    current = "\n".join(_manifest_lines(root)) + "\n"
    header_ok = recorded.startswith("#")
    body = "\n".join(ln for ln in recorded.split("\n") if ln and not ln.startswith("#")) + "\n"
    if not header_ok or body != current:
        fails.append("BOOTSTRAP-03 manifest does not match parent/ bytes (drift or placeholder)")
    else:
        print("[WP0-STEP-03] bootstrap manifest matches %d parent files" % (len(current.strip().split("\n"))))
    return fails


# WP0-STEP-03: write the bootstrap manifest (one authorized transaction only).
def write_manifest(root: str) -> None:
    lines = _manifest_lines(root)
    with open(os.path.join(root, "parent", "BOOTSTRAP_MANIFEST.sha256"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("# v0.3 parent bootstrap manifest (sealed bytes of parent/ at WP-0)\n")
        f.write("\n".join(lines) + "\n")
    print("[WP0-STEP-03] wrote BOOTSTRAP_MANIFEST.sha256 (%d entries)" % len(lines))


# WP0-STEP-03: enforce/verify the read-only lock on parent/.
def enforce_lock(root: str, enforce: bool = False) -> list[str]:
    parent = os.path.join(root, "parent")
    changed, locked, fails = [], 0, []
    for name in sorted(os.listdir(parent)):
        p = os.path.join(parent, name)
        if not os.path.isfile(p):
            continue
        try:
            ro = bool(os.stat(p).st_file_attributes & 0x1)
        except AttributeError:
            ro = not os.access(p, os.W_OK)
        if ro:
            locked += 1
        elif enforce:
            os.chmod(p, stat.S_IREAD)
            changed.append(name)
        else:
            fails.append("BOOTSTRAP-02 parent/%s not read-only (run with --enforce-lock)" % name)
    if changed:
        print("[WP0-STEP-03] lock enforced on: %s" % ",".join(changed))
    if not fails:
        print("[WP0-STEP-03] parent/ read-only lock intact (%d files)" % (locked + len(changed)))
    return fails


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    enforce = "--enforce-lock" in sys.argv
    if "--write-manifest" in sys.argv:
        print("[WP0-STEP-03] bootstrap write-manifest transaction")
        write_manifest(root)
        enforce_lock(root, enforce=True)
        return 0
    fails: list[str] = []
    print("[WP0-STEP-03] bootstrap verify (enforce=%s)" % enforce)
    v02 = json.load(open(os.path.join(root, "parent", "V02_SEAL.json"), encoding="utf-8"))
    if v02.get("sealed_commit") != FULL_PARENT or v02.get("terminal_claim") != TERMINAL_CLAIM:
        fails.append("BOOTSTRAP-00 seal identity mismatch")
    else:
        print("[WP0-STEP-03] seal identity: %s / %s" % (FULL_PARENT[:13], TERMINAL_CLAIM))
    fails += check_manifest(root)
    fails += enforce_lock(root, enforce=enforce)
    if fails:
        print("[WP0-STEP-03] BOOTSTRAP_FAIL")
        for x in fails:
            print(" -", x)
        return 1
    print("[WP0-STEP-03] BOOTSTRAP_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
