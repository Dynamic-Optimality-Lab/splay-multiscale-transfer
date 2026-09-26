"""Append-only run logger (§27): every execution record carries the full field set."""
from __future__ import annotations

import datetime
import hashlib
import json
import os


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_log(path: str, rec: dict) -> dict:
    required = ["experiment_id", "phase", "branch", "command", "scientific_status"]
    for k in required:
        if k not in rec:
            raise ValueError(f"log missing {k}")
    rec = dict(rec)
    rec.setdefault("utc", datetime.datetime.now(datetime.timezone.utc).isoformat())
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    lines = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


# WP-1 REPAIR STEP L1: static §27 provenance fields shared by phase runners.
def static_fields(root: str) -> dict:
    """Collect commit/pin/contract/firewall/dependency hashes (read-only).

    Unavailable values are recorded as explicit null-with-reason, never
    omitted silently and never fabricated.
    """
    import subprocess as _sp
    fields: dict = {
        "experiment_id": "SPLAY-AM-MST-v0.3",
        "parent_commits": {
            "v02": "38c1be6afd2ab2420aa094c68ce45ee6a26b3628",
            "v01": "6de1ca2a595e8895f54794f3a211fe6ee1a95a80",
        },
        "calculus_id": None,
        "constant_C": None,
        "stdout_hash": None,
        "stderr_hash": None,
        "stream_note": "console streams not captured; outputs hash-covered instead",
    }
    try:
        r = _sp.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                    cwd=root, timeout=60)
        fields["local_commit"] = r.stdout.strip() or "unavailable: empty rev-parse"
    except Exception as e:  # noqa: BLE001 - provenance must not fail the run
        fields["local_commit"] = "unavailable: %s" % type(e).__name__
    for key, rel in (("spec_sha", "IMPLEMENTATION_SPEC_v0.3.md"),
                     ("prereg_sha", "prereg/prereg_sha256.txt"),
                     ("literature_manifest_sha", "external/MANIFEST.json"),
                     ("gate_matrix_sha", "prereg/theorem_gate_matrix.yaml"),
                     ("dependency_hashes", "requirements-lock.txt")):
        p = os.path.join(root, rel)
        try:
            fields[key] = sha(open(p, "rb").read())
        except OSError:
            fields[key] = "unavailable: missing " + rel
    try:
        h1 = json.load(open(os.path.join(root, "parent", "V02_H1_FIREWALL.json"),
                            encoding="utf-8"))
        h2r = json.load(open(os.path.join(root, "parent", "V02_H2R_FIREWALL.json"),
                             encoding="utf-8"))
        fields["firewall_states"] = {
            "H1": h1.get("state"),
            "H2R": "%s/unlocks=%s" % (h2r.get("state"),
                                      h2r.get("unlocks", h2r.get("unlock_count"))),
            "n8": "PARTIALLY_REVEALED_CANARY_CONTAMINATED",
        }
    except OSError:
        fields["firewall_states"] = "unavailable: parent firewall records missing"
    return fields


# WP-1 REPAIR STEP L4: tee capture for stdout/stderr hashes (§27, F16).
class _Tee:
    """Write-through tee: prints to the original stream and a file."""

    def __init__(self, stream, path: str):
        self._stream = stream
        self._file = open(path, "w", encoding="utf-8")

    def write(self, data):
        self._stream.write(data)
        self._file.write(data)
        return len(data)

    def flush(self):
        self._stream.flush()
        self._file.flush()

    def close(self):
        try:
            self._file.close()
        except OSError:
            pass


class capture:
    """Context manager capturing stdout/stderr to files (pass-through).

    Usage: with capture(logdir, "phase01") as cap: ... run ...
    Afterwards cap.hashes() returns {stdout_hash, stderr_hash, stdout_path,
    stderr_path}. Original streams restored in finally (fail-closed).
    """

    def __init__(self, logdir: str, tag: str):
        self._logdir = logdir
        self._tag = tag
        self.stdout_path = os.path.join(logdir, tag + ".stdout")
        self.stderr_path = os.path.join(logdir, tag + ".stderr")

    def __enter__(self):
        import sys as _sys
        os.makedirs(self._logdir, exist_ok=True)
        self._old = (_sys.stdout, _sys.stderr)
        _sys.stdout = _Tee(_sys.stdout, self.stdout_path)
        _sys.stderr = _Tee(_sys.stderr, self.stderr_path)
        return self

    def __exit__(self, _exc_type, _exc, _tb):
        import sys as _sys
        for stream in (_sys.stdout, _sys.stderr):
            try:
                stream.flush()
            except Exception:  # noqa: BLE001 - restore must not fail
                pass
            if isinstance(stream, _Tee):
                stream.close()
        _sys.stdout, _sys.stderr = self._old
        return False

    def hashes(self) -> dict:
        """SHA-256 of the captured streams (read back from disk)."""
        out = {}
        for key, path in (("stdout_hash", self.stdout_path),
                          ("stderr_hash", self.stderr_path)):
            with open(path, "rb") as f:
                out[key] = sha(f.read())
        out["stdout_path"] = self.stdout_path
        out["stderr_path"] = self.stderr_path
        return out


# WP-1 REPAIR STEP L2: hash every file in output dirs (deterministic order).
def hash_outputs(root: str, rel_dirs: list) -> dict:
    """Map relpath -> SHA-256 for all files under the given artifact dirs."""
    out: dict = {}
    for rel in rel_dirs:
        base = os.path.join(root, rel)
        if not os.path.isdir(base):
            continue
        for dp, _, fns in os.walk(base):
            for fn in sorted(fns):
                p = os.path.join(dp, fn)
                out[os.path.relpath(p, root).replace(os.sep, "/")] = sha(
                    open(p, "rb").read())
    return out
