# Theorem MST0-19 — Levy–Tarjan bridge (convention checklist, audit NOT reached)

**Status:** BLOCKED — prerequisite MST0-18 is BLOCKED (see
`math/reviews/MST0-19.BLOCKED`). The bridge audit is recorded below as a
checklist with every item marked; no bridge conclusion is drawn. This record
must never be consumed.

## Convention checklist (audit status: NOT_REACHED — no Pair-Access lemma to bridge)

```text
Splay variant:            ordinary bottom-up Splay (frozen; matches L1 context, L2 premise use blocked: L2 bytes pending)
cost convention:          depth+1 (frozen; INV-004)
initial-tree convention:  diagonal starts for generated histories (frozen); arbitrary legal trees in bank episodes
subsequence definition:   Y <= X retained-subsequence semantics (inherited from parent Pair-Access contract)
additive term:            none exists (no telescope proved)
constant independence:    unproved (MST0-22 UNPROVED setup)
direction of implication: Pair Access -> approximate monotonicity -> dynamic optimality (route documented, not traversed)
exact L2/L3 version:      L2/L3 bytes PENDING (paywall/migrated endpoint); bridge-audit premise use remains blocked
```

## What unblocking requires

REVIEWED MST0-18 plus retrievable L2/L3 source bytes (or a documented
premise-free route), then the full audit above with PASS on every item before
any of `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED → APPROXIMATE_MONOTONICITY_PROVED →
DYNAMIC_OPTIMALITY_PROVED` may be claimed. L2/L3 premise use is additionally
blocked by the literature-byte freeze (downstream-use blocks recorded in WP-0).
