# Retrodiction Semantics

What it means to run a TARA backward — inferring source state from a target representation.

## Forward vs backward

A TARA is emitted forward: source → target. The source compresses its state, declares what was lost, estimates drift, and hands the result to the target.

Retrodiction asks: given the target's consumed TARA, what can be inferred about the source's state at emission time?

## Why retrodiction degrades

### 1. Loss is irreversible

`lossNotes` declare what was dropped during forward emission. Those degrees of freedom cannot be recovered by the target. A TARA that says "fine-grain microstate omitted" means the target cannot reconstruct the microstate — the information is gone.

In physics terms: the forward TARA is a coarse-graining that integrates out fast degrees of freedom. The inverse map is not unique — many microstates produce the same coarse-grained summary.

### 2. Drift makes backward inference harder

`driftEstimate` measures how fast the source is diverging from the snapshot. In the forward direction, this tells the target how quickly the TARA goes stale. In the backward direction, the problem is worse: the source has continued evolving since emission, so the target's model of the source is strictly older than the TARA itself.

Backward effective confidence degrades as:

```
backward_confidence ≈ confidence × exp(-driftEstimate × elapsed) × (1 - information_loss_fraction)
```

where `information_loss_fraction` is roughly `len(lossNotes) / total_fields` — a heuristic for how much was dropped.

### 3. Entropy increase

The second law constrains retrodiction. Forward emission compresses and loses information (entropy increases in the transfer channel). Running the transfer backward means trying to decrease entropy, which is physically possible only with additional information from outside the TARA.

The practical consequence: retrodiction from a consumed TARA is always underdetermined. The target can form hypotheses about the source's state, but those hypotheses have lower confidence than the forward reconstruction and more candidate states to choose from.

## Design decision

**`directionality` is a consumer-side concern, not a schema field.**

A TARA is always emitted forward. It is an artifact of the forward transfer. Retrodiction is an inference operation performed by a consumer on a consumed TARA — it uses the TARA's data but is not a property of the TARA itself.

Reasons:
1. The TARA should be immutable after emission. Adding a `directionality` field implies the TARA changes meaning depending on how it's used, which contradicts its role as a reference record.
2. Retrodiction quality depends on the consumer's model of the source, which the TARA doesn't control.
3. Keeping retrodiction in the consumer avoids complicating the schema with a concern that most uses don't need.

## When retrodiction is useful

- **Debugging**: given a consumed TARA, infer what the source was doing when it emitted the array. Useful for post-hoc analysis.
- **Causal inference**: determine whether a source event could have caused a target behavior by checking whether the TARA's `stateSummary` is consistent with the hypothesized source state.
- **Provenance verification**: confirm that a TARA's declared provenance is consistent with the source's known behavior at the declared `timeMarker`.

## Relationship to composition

Retrodiction interacts with composition: if TARA(A→B) and TARA(B→C) are composed into TARA(A→C), retrodiction from C to A requires inverting both hops. The compound retrodiction is worse than either individual retrodiction because losses accumulate at each boundary.
