# artifacts/v03/freeze/ — Phase-freeze certificates (WP-3 and later)

Rule (STOP-05): WP-0 prereg files (`prereg/event_ontology_v0.3.yaml`,
`prereg/transfer_grammar_v0.3.yaml`, `prereg/holdouts.yaml`, and every file hashed in
`prereg/prereg_sha256.txt`) are permanently immutable after the WP-0 freeze.
Later phases NEVER edit them.

Instead, each freezing phase emits a certificate here, e.g.
`PHASE09_TRANSFER_GRAMMAR_FREEZE.json`, with at minimum:

- `preregistered_ontology_hash` / `preregistered_grammar_hash` (from `prereg_sha256.txt`)
- `implementation_hash` (frozen `python/` modules), `generator_hash` (H3T generator)
- `freeze_timestamp_utc`, `status` (e.g. `TRANSFER_GRAMMAR_FROZEN`)
- `h3t_commitment_hash` (points at `artifacts/v03/holdouts/h3t_commitment.json`,
  whose firewall state — not `holdouts.yaml` — carries `BANK_COMMITTED`)

WP-3 certifies/instantiates the frozen preregistration; it does not rewrite it.
`holdouts.yaml` keeps `H3T.status_at_prereg = TO_BE_GENERATED_AND_QUARANTINED` forever:
preregistered rule vs. observed execution state stay separated.
