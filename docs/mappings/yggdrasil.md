# Yggdrasil → TARA Mapping

Maps Yggdrasil's promotion mechanics, durable traces, and cadence layers to TARA.

## 1. Promotion as TARA transfer

Branch→spine promotion (`ygg promote`) is a fast→slow transfer with compression, loss, and confidence judgment.

### Mapping

| Yggdrasil concept     | TARA field              | Notes                                                     |
|-----------------------|------------------------|-----------------------------------------------------------|
| branch ID             | `sourceArc.id`          | The branch that produced the result                        |
| spine memory          | `targetArc.id`          | The canonical memory surface receiving the promotion       |
| branch output         | `stateSummary`          | Compressed branch result using yggdrasil-promotion payload |
| promotion disposition | `stateSummary.disposition` | `no-promote`, `log-daily`, `promote-durable`, `escalate-hitl` |
| promotion evidence    | `stateSummary.promotionEvidence` | Why this disposition was chosen                   |
| staleness             | `driftEstimate`         | How stale the branch result is at promotion time           |
| review cadence        | `validityWindow`        | When this promotion record itself becomes stale            |

### Promotion dispositions as TARA patterns

- **`promote-durable`**: High confidence, clear reconstruction target. The spine accepts the TARA and incorporates it into canonical memory. See `examples/yggdrasil-promotion.json`.

- **`no-promote`**: The TARA exists but was rejected by reconstruction policy. Low confidence or the reconstruction target doesn't justify spine-level storage. See `examples/yggdrasil-declined.json`.

- **`log-daily`**: Medium confidence. The TARA is consumed at the meso layer (daily notes) but not promoted to the slow spine.

- **`escalate-hitl`**: The TARA's confidence or consequence level requires human judgment before the spine accepts it. The `trustClass` shifts to `"external"` because the decision is delegated outside the automated system.

## 2. Durable traces as consumed TARAs

Yggdrasil's "durable trace" — any artifact that preserves continuity across time — is a consumed TARA whose reconstruction was accepted.

The relationship:

```
durable trace = TARA where:
  - disposition == "promote-durable"
  - reconstruction was performed by the spine
  - the result was incorporated into canonical memory
  - provenance records the acceptance
```

The `provenance` field carries the acceptance record: who accepted it, when, and under what policy. This makes durable traces inspectable and auditable.

A branch result that was `no-promote` also has a TARA — it just wasn't accepted. The record still exists, with `lossNotes` explaining why the transfer was declined.

## 3. Cadence discipline via gear ratios

Yggdrasil's three cadence layers map to gear-coupled TARAs:

| Layer       | Cadence                    | Approx Hz | Role   |
|-------------|----------------------------|-----------|--------|
| Fast edge   | Discord pings, raven returns | ~10/hr   | scout  |
| Meso        | Branch execution, daily ops  | ~1/hr    | router |
| Slow spine  | Weekly review, canonical memory | ~0.14/hr | policy |

### Gear ratios

- Fast→Meso: approximately **10:1** (10 fast events per meso cycle)
- Meso→Slow: approximately **7:1** (7 meso cycles per weekly slow cycle)
- Fast→Slow (composed): approximately **70:1**

See `examples/yggdrasil-gear-coupled.json` for a meso→slow gear-coupled TARA representing a weekly Winter Pass promotion.

## 4. RAVENS as TARA pattern

The RAVENS architecture (Huginn/Muninn) maps cleanly:

- **Huginn** (outward scouting) operates at the fast edge — explores, searches, hypothesizes
- **Muninn** (memory/return) operates at the meso layer — compresses signal, classifies disposition
- **Spine** makes the slow policy decision — accepts or rejects the promotion

Each handoff (Huginn→Muninn, Muninn→Spine) is a TARA transfer. The full chain is a composition of two TARAs with compound confidence degradation.
