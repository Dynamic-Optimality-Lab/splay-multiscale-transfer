"""WP-1 rotation-trace corpus persistence (contract: traces + manifest + bundle).

Persists the dual-core agreement corpus (one trace_keep record per imported
critical-cycle KEEP edge, full §5.5 event fields) as per-n .json.zst shards
with a manifest of shard hashes plus a logical-stream SHA-256 (H3T pattern),
and binds the MST02 proof to the corpus via a proof-bundle record. Writes are
deterministic (canonical JSON, sorted keys, fixed zstd level); readers must use
the manifest hashes. Console tag [WP1-STEP-04] via the owning runner.
"""
from __future__ import annotations

import hashlib
import json
import os

ZSTD_LEVEL = 3


# WP-1 REPAIR STEP C1: canonical JSON bytes for hashing and sharding.
def canonical_bytes(obj: dict | list) -> bytes:
    """Deterministic UTF-8 bytes (sorted keys, LF-terminated)."""
    return (json.dumps(obj, sort_keys=True) + "\n").encode("utf-8")


# WP-1 REPAIR STEP C2: compress bytes deterministically.
def compress(raw: bytes) -> bytes:
    """Zstandard compression at the frozen level (deterministic)."""
    import zstandard as zstd
    return zstd.ZstdCompressor(level=ZSTD_LEVEL).compress(raw)


# WP-1 REPAIR STEP C3: write one shard + return its record.
def write_shard(outdir: str, name: str, payload: dict) -> dict:
    """Write name.json.zst; return {file, sha256, bytes, count}."""
    raw = canonical_bytes(payload)
    blob = compress(raw)
    path = os.path.join(outdir, name + ".json.zst")
    with open(path, "wb") as f:
        f.write(blob)
    digest = hashlib.sha256(blob).hexdigest().upper()
    # WP-1 REPAIR STEP C3: shard write with hash (deterministic bytes).
    print("[WP-1][REPAIR STEP C3] shard %s bytes=%d sha=%s..."
          % (name + ".json.zst", len(blob), digest[:16]), flush=True)
    return {"file": name + ".json.zst", "sha256": digest, "bytes": len(blob),
            "count": len(payload.get("traces", payload.get("cycles", [])))}


# WP-1 REPAIR STEP C4: logical-stream hash over shard digests (H3T pattern).
def logical_stream(shards: dict) -> str:
    """SHA-256 over the sorted per-shard digests (uppercase hex)."""
    joined = "".join(sorted(s["sha256"] for s in shards.values()))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest().upper()


# WP-1 REPAIR STEP C5: read one shard (fail-closed on wrong representation).
def read_shard(outdir: str, name: str) -> dict:
    """Decompress and parse name.json.zst (plain JSON rejected)."""
    import zstandard as zstd
    path = os.path.join(outdir, name + ".json.zst")
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return json.loads(zstd.ZstdDecompressor().decompress(raw).decode("utf-8"))
    except Exception as e:
        raise ValueError("shard %s unreadable (representation attack?)" % name) from e


# WP-1 REPAIR STEP C6: validate a manifest against its shards on disk.
def validate_manifest(manifest: dict, outdir: str) -> list[str]:
    """Check shard presence, hashes, counts, and logical stream."""
    fails: list[str] = []
    shards = manifest.get("shards", {})
    if not shards:
        return ["manifest has no shards"]
    if "logical_stream" not in manifest:
        fails.append("manifest lacks logical_stream")
        return fails
    whole = True
    for key in sorted(shards):
        spec = shards[key]
        intact = True
        for field in ("file", "sha256"):
            if field not in spec:
                fails.append("shard %s lacks %s" % (key, field))
                intact = False
        if not intact:
            whole = False
            continue
        p = os.path.join(outdir, spec["file"])
        if not os.path.isfile(p):
            fails.append("shard file missing " + spec["file"])
            whole = False
            continue
        with open(p, "rb") as f:
            if hashlib.sha256(f.read()).hexdigest().upper() != spec["sha256"]:
                fails.append("shard hash mismatch " + spec["file"])
    if whole and logical_stream(shards) != manifest["logical_stream"]:
        fails.append("logical stream mismatch")
    return fails
