# Sandy Chaos → TARA Field Mapping

Maps the TransferBundle from Sandy Chaos note 13 (Nested Temporal Domains) to TARA.

## Field mapping

| TransferBundle       | TARA field             | Notes                                                        |
|----------------------|------------------------|--------------------------------------------------------------|
| `source_domain`      | `sourceArc`            | Domain index D_{r,k} maps to structured arc with band + role |
| `target_domain`      | `targetArc`            | Same — structured arc carries temporalBand and role           |
| `payload`            | `stateSummary`         | Compressed representation of source-domain state              |
| `confidence`         | `confidence`           | Direct 1:1 mapping, same semantics                            |
| `distortion`         | `lossNotes`            | Distortion is one entry in the loss record; TARA is richer    |
| `latency`            | `driftEstimate`        | Latency contributes to staleness; TARA separates rate from window |
| `provenance`         | `provenance`           | Direct 1:1 mapping                                            |
| `validity_window`    | `validityWindow`       | Direct 1:1 mapping                                            |

## Gaps

### TransferBundle has, TARA adds
- `reconstructionTarget` — TransferBundle has no explicit statement of what the target is trying to recover. TARA requires this. For Sandy Chaos transfers, this should be the operational question the target domain needs answered.
- `trustClass` — TransferBundle does not declare the relationship between emitter and consumer. For same-system transfers this is typically `"self"` or `"neighbor"`.
- `driftEstimate` — TransferBundle's `latency` is a point-in-time measurement. TARA's `driftEstimate` is a rate that predicts future staleness.

### TransferBundle has, TARA absorbs differently
- `distortion` as a scalar becomes one entry in `lossNotes` (which is a list of declared losses). If a numeric distortion value is needed, it can go in `stateSummary` or in the domain sub-schema.
- `latency` as a scalar is absorbed into `driftEstimate` (rate) + `validityWindow` (expiry). The exact latency at emission can be recorded in `provenance`.

## Domain index → structured arc

Sandy Chaos's domain index `D_{r,k}` maps naturally to the structured arc identifier:

```
D_{observer, fast}  →  { "id": "fast-observer", "temporalBand": "fast", "role": "observer" }
D_{observed, meso}  →  { "id": "meso-observed", "temporalBand": "meso", "role": "observed" }
D_{chaser, slow}    →  { "id": "slow-chaser",   "temporalBand": "slow", "role": "chaser" }
```

## Example

See `examples/sandy-chaos-transfer.json` — a fast-observer → meso-observer temporal coupling transfer.
