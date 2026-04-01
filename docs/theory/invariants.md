# Frame-Covariance and Invariants

What survives a change of frame — re-describing the same transfer from the target's perspective instead of the source's, or re-parameterizing time.

## Frame-invariant quantities

These quantities do not change under a legitimate change of description frame:

### 1. Causal ordering

The source emitted the TARA before the target consumed it. This ordering is absolute — it does not depend on which frame describes the transfer. Any re-parameterization that reverses this ordering is illegitimate.

In the schema: `timeMarker` records the emission time. The consumption time is not recorded in the TARA (it's the consumer's concern), but it must be later than `timeMarker`.

### 2. Loss profile

What was dropped is frame-independent. If the source omitted fine-grain microstate, that information is absent regardless of how the transfer is described. `lossNotes` is an invariant of the transfer.

In physics terms: the kernel of the coarse-graining map does not depend on the coordinate system.

### 3. Information capacity bound

The maximum information that can pass through the transfer channel is determined by the physical channel, not by the description. For gear-coupled TARAs, `informationCapacity` is derived from the ratio and slippage tolerance — these are properties of the coupling, not of the observer.

### 4. Trust class

The relationship between emitter and consumer (`self`, `neighbor`, `external`, `synthetic`) is a structural property of the system topology, not of the description frame.

## Frame-dependent quantities

These quantities change depending on who is describing the transfer:

### 1. confidence

Confidence depends on the consumer's reconstruction policy. The source declares a confidence based on its assessment of compression quality, but the target may apply different standards. A TARA with `confidence: 0.85` from the source's perspective might be treated as `confidence: 0.7` by a more skeptical consumer.

In the schema, `confidence` is the source's declared value. Consumer-adjusted confidence is the consumer's concern.

### 2. driftEstimate

Drift rate depends on which frame measures time. If the source and target operate at different cadences (as in gear-coupled TARAs), the drift measured in source ticks differs from the drift measured in target ticks.

For gear-coupled TARAs: `driftEstimate` is in source-frame units. To convert to target-frame: multiply by `gearRatio` (source-teeth / target-teeth).

### 3. stateSummary contents

The representation is constructed in the source's frame. The same physical state could be described differently from the target's perspective. The TARA carries the source's description — translation to the target's local variables is the codec's translate stage (see `docs/mappings/codec-lifecycle.md`).

### 4. reconstructionTarget

What the target is trying to recover is defined from the target's perspective, but the source's `reconstructionTarget` field declares the source's understanding of the target's need. These may differ.

## Universality classes

The connection to renormalization group language (see `docs/theory/renormalization.md`): the frame-invariant quantities define equivalence classes of transfers.

Two transfers are in the same universality class if they have:
- the same causal ordering
- the same loss profile (same degrees of freedom integrated out)
- the same information capacity bound

The frame-dependent quantities (confidence, drift, summary contents) are the "irrelevant operators" — they vary within a universality class but don't change the class identity.

## Practical implications

1. When comparing two TARAs: compare frame-invariant quantities first. If they differ in loss profile or information capacity, they represent fundamentally different transfers regardless of confidence values.

2. When re-describing a TARA from a different frame: preserve `lossNotes`, `trustClass`, and `informationCapacity`. Adjust `confidence`, `driftEstimate`, and `stateSummary` contents for the new frame.

3. When composing TARAs: the composed invariants follow directly from the individual invariants (losses union, capacity bottlenecks). The composed frame-dependent quantities require more care.
