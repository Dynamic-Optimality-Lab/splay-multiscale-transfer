# SPLAY-AM-MST v0.3.1 — Ratified Parent-Pin Amendment / Normative Freeze

**Status:** `RATIFIED` — this amendment closes the `PRE_FREEZE_PARENT_PIN_REQUIRED` condition
stated in `IMPLEMENTATION_SPEC_v0.3.md`.
**Date ratified:** 2026-09-23
**Amends:** `IMPLEMENTATION_SPEC_v0.3.md` (byte-identity preserved, see §4 — this file
adds the pin; it does not edit the v0.3 text).

## 1. Why this amendment exists

The v0.3 specification as issued declares `PRE_FREEZE_PARENT_PIN_REQUIRED`: its normative
freeze occurs only after the final sealed v0.2 commit, `FINAL_RESULT`, manifest, archive,
and normative hashes are pinned, and its parent-commit field reads
`TO_BE_PINNED_FROM_V0.2_WP6_FINAL_SEAL`. The v0.2 experiment has since sealed at WP-6.
This amendment records that pin Verbatim from sealed artifacts (never from prose) and
thereby ratifies the v0.3 normative stack. No Phase-01+ scientific execution predates it.

## 2. Ratified parent identity (all values read from sealed parent artifacts)

- Parent experiment: `SPLAY-AM-BD-v0.2`, repo
  `https://github.com/Dynamic-Optimality-Lab/splay-bellman-debt`
- Sealed full commit: `38c1be6afd2ab2420aa094c68ce45ee6a26b3628` (short `38c1be6`);
  verified clean tree at this commit on 2026-09-23.
- Terminal claim: `FINITE_DEBT_LAW_MINING_RESULTS`
  (`artifacts/v02/seal/FINAL_RESULT.json`).
- `FINAL_RESULT.json` SHA-256:
  `C5B1C60ADE7090C3B32000A3FF94FC376D65DF4ECAF16AA2AD227DC775995140`
- Seal manifest (`artifacts/v02/seal/MANIFEST.sha256`) SHA-256:
  `5C4BA61B1409A1E92263912173B749AD6BDE0CBBEB174E2CA285FEABA64BB17F`
- Archive `SPLAY-AM-BD-v0.2.tar.zst` SHA-256:
  `87AEA34C5BCB940EB32D3B7B6DF4199CEAEE6F44BC28E2F93612C95B6789DAF5`
  (matches the recorded `.tar.zst.sha256` sidecar).
- Route audit (`artifacts/v02/seal/route_audit.json`) SHA-256:
  `2CAD2F65432583846743ACF4FE54C1CE8373D325ED73D256ADE7B8643F52489E`
- Normative parent spec set (authoritative, as recorded in sealed `FINAL_RESULT`):
  `v0.2: 7F7B4EE0107AF2A02B8E264B83708392E61955F67C5A8F9871D22978090FC473`,
  `v0.2.1-SA01: EA69C3569F82B1B4AD942A13D4615540EA24FEBE82837D6A303949BFF1D6CC83`,
  `v0.2.2-SA02: 86669C307563C3BAD386B5F2A8884D227A1ACBC8634E1F9DF5F835C83DB9CB70`.
- H1 firewall: `EMPTY`, `unlock_record: null`,
  bank commitment `c9d9be2652412f6100c667ba1598d982e241868a0751ac5357499d55c0613bff`.
- H2R firewall: `BANK_COMMITTED`, `unlock_count: 0`
  (commitment `artifacts/v02/holdouts/H2R/commitment.json` SHA-256
  `3656B37270EFD1D3279D44A219D19EA558D61C3CEC32B836F16F5F1CF1718EBE`,
  firewall record SHA-256 `AC39287E217DD3079AA74A746ADB0C5E6C281ABBA6EF08A770BCB145759C9670`).
- n8: `PARTIALLY_REVEALED_CANARY_CONTAMINATED` (never fresh).
- Secondary ancestor: `SPLAY-AM-PD-v0.1`, sealed commit
  `6de1ca2a595e8895f54794f3a211fe6ee1a95a80`, terminal claim
  `FINITE_EXACT_BN_RESULTS` (via parent `parent/PARENT_SEAL.json`, separate repo history).
- Parent chain aides observed in sealed history:
  `b444f6a` (WP-1), `08dc1a7` (WP-2), `19245ab` (WP-3), `f131b14`/`1821865` (WP-4),
  `29de3df` (WP-5).

## 3. What is frozen by this amendment

The normative v0.3 stack is exactly:

1. `IMPLEMENTATION_SPEC_v0.3.md` (§4 byte-identity),
2. this amendment (`SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md`),
3. `WorkPlan.md`, `Path.md` (living trackers — versioned by commit history, not frozen text),
4. `prereg/` contents hashed in `prereg/prereg_sha256.txt` (which includes this amendment).

## 4. v0.3 text byte-identity (no silent post-hash edits)

`IMPLEMENTATION_SPEC_v0.3.md` SHA-256:
`462676E186C6282F493D13C13A4A7A63179943CFC7E9AB10ABFBE0019BD1E12F`
(120,420 bytes). Any future normative change requires a new versioned amendment
(`v0.3.2`, …); the v0.3 file itself is never edited in place.

## 5. Effect

With this pin recorded, the `PRE_FREEZE_PARENT_PIN_REQUIRED` condition is discharged:
WP-0 may claim `FOUNDATION_FROZEN` once its remaining gate checks pass, and downstream
gates (notably `MST0-01 → REVIEWED` before WP-1 certified consumption) operate on the
pinned identity above. Any `PARENT_SEAL_MISMATCH` against §2 values blocks execution.
