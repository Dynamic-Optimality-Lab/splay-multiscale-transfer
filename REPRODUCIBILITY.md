# REPRODUCIBILITY.md — SPLAY-AM-MST-v0.3 fresh-checkout reverification

## One-unlock semantics (read first)

Fresh banks were consumed exactly once in WP-5. A fresh checkout therefore
reproduces the seal by **verification, not by re-unlock**: re-running
`run_phase14.py` / `run_phase15.py` must FAIL fail-closed (one-freeze /
one-unlock refused); the checked-in reveal records, firewall states, and
hashes are the reproduced evidence. Re-running them would be a seal violation,
not a reproduction.

## Commands (repository root, Python 3.13.7, `pip install -r requirements-lock.txt`)

```text
python scripts/reproduce_all_v0.3.py
```

which executes, in order: Phase-00 gate (parent pin, freeze integrity,
allowlist), foundation suite, firewall + HLD suites, WP-5 suites (agreement,
holdout, scope), lifecycle audit re-derivation, manifest verification, archive
hash verification, clean-room spot replays, large-n spot trials, seal suite
(SEAL-01…12), proof suite (PR-01…14 + NEG analogues), mutation suite. Expected:
every step exit 0; terminal line `REPRODUCE_ALL: PASS`.

## What is recomputed vs reverified

- Recomputed: parent/ledger hashes, H3T shard streams + logical hash (14.1 MB),
  candidate-set hash, obligation derivation, lifecycle audit, injection-bound
  samples, clean-room replays, large-n spot trials, FINAL_RESULT regeneration
  (byte-identical), archive-design determinism (manifest + sidecar).
- Reverified (single-consumption evidence, hash-checked not re-shot): H3T
  reveal records + firewall UNLOCKED_ONCE/1, H1/H2R routing records, WP-4
  solver certificates (replay logs replayed, not re-solved).

## Determinism

Sorting is canonical everywhere; JSON written `sort_keys` + LF; archive built
with normalized metadata (uid/gid 0, mtime 0, sorted names) and fixed zstd
parameters. Rebuilds are byte-identical (SEAL-10).

## Environment

Python 3.13.7 (frozen in `requirements-lock.txt`); stdlib + `zstandard`,
`jsonschema`, `sympy`, `pyyaml`, `z3-solver 5.1.0.0` (discovery CEGIS proposer
only; verdicts required independent replay). No GPU, no network, no randomness
outside frozen seeds. Wall/peak resource notes: §26.7 record in
`artifacts/v03/audits/resource_record.json` (no resource failure occurred in
any WP; largest inputs: H3T bank 14.1 MB, masks 5.6 MB).
