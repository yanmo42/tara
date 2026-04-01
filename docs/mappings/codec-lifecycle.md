# Neighbor-Layer Codec as TARA Lifecycle

Maps Sandy Chaos's four-stage neighbor-layer codec (note 13, section 5) to the lifecycle of a TARA.

## The four stages

### 1. Embed → TARA emission

The source arc constructs the TARA: compresses local state into `stateSummary`, declares what was lost in `lossNotes`, estimates drift, sets confidence.

This is the codec's **embed** operation — writing a constrained representation into a form the neighbor layer can receive.

The TARA record is the artifact produced by this stage.

### 2. Extract → TARA reception

The target arc receives and parses the TARA. At this point the record is syntactically available but not yet interpreted in the target's local frame.

This is the codec's **extract** operation — recovering a usable representation from the neighbor-layer signal.

The validator tool (`tools/validate.py`) operates at this stage: it confirms the TARA is structurally well-formed.

### 3. Translate → reconstruction attempt

The target arc maps the TARA's `stateSummary` into its own local variables and control terms. The `reconstructionTarget` field declares what the target is trying to recover. The `lossNotes` constrain what the target knows it cannot recover.

This is the codec's **translate** operation — converting the received representation into locally meaningful quantities.

### 4. Reconstruct → bounded local model

The target arc forms a bounded model of the source domain's state. The result is constrained by `confidence`, `driftEstimate`, and `lossNotes`. The model is useful for the target's decisions but is explicitly not the source's full state.

This is the codec's **reconstruct** operation — forming a bounded local model of the neighboring domain.

## Design decision

`lifecycleStage` belongs in the consumer/processor, not in the TARA record itself.

A TARA is the artifact at stage boundaries — it is emitted (stage 1) and consumed (stages 2-4). It does not track its own lifecycle. A consumer that wants to record which stage it has reached should do so in its own state, not by mutating the TARA.

This keeps the TARA immutable after emission, which preserves its value as a reference record.

## Relationship to TARA fields

| Codec stage   | Primary TARA fields used                          |
|---------------|--------------------------------------------------|
| Embed         | All fields written by emitter                     |
| Extract       | Schema validation, structural parsing             |
| Translate     | `stateSummary`, `reconstructionTarget`, `lossNotes` |
| Reconstruct   | `confidence`, `driftEstimate`, `validityWindow`    |
