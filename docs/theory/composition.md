# TARA Composition Rules

Given TARA(A→B) and TARA(B→C), define TARA(A→C).

## Prerequisites

Composition requires that the `targetArc` of the first TARA matches the `sourceArc` of the second. When using structured arc identifiers, the `id` fields must match. The temporal band and role may differ (polarity coupling changes role, temporal coupling changes band).

## Field-by-field composition

### confidence — multiplicative

```
confidence(A→C) = confidence(A→B) × confidence(B→C)
```

Trust compounds. If A trusts its representation at 0.85 and B trusts its at 0.76, the end-to-end trust is 0.85 × 0.76 = 0.646. This is a conservative bound — the true composed confidence cannot be higher than either individual confidence, and in practice is worse due to compounding reconstruction error.

### driftEstimate — additive

```
driftEstimate(A→C) = driftEstimate(A→B) + driftEstimate(B→C)
```

When both are structured objects:
- `overall` fields add
- `perField` maps merge, summing shared keys
- `decayModel` takes the faster-decaying model (exponential > linear > step)

When mixed (one number, one object), the number is treated as the `overall` of a minimal object.

### lossNotes — union

```
lossNotes(A→C) = lossNotes(A→B) ∪ lossNotes(B→C)
```

Concatenate and deduplicate. Everything lost at any boundary stays lost. Order is preserved (A→B losses first, then B→C losses).

### reconstructionTarget — narrowing

```
reconstructionTarget(A→C) = narrower of the two targets
```

The composed reconstruction target should describe what C is actually trying to recover, which is constrained by both what B could provide and what C needs. In practice, the second TARA's `reconstructionTarget` is usually the right one, qualified by the first's limitations.

### validityWindow — minimum

```
validityWindow(A→C) = min(validityWindow(A→B), validityWindow(B→C))
```

The chain expires when its weakest link expires. When both have tick counts, take the minimum. When both have durations, take the shorter. When mixed, preserve both forms using the minimums.

### stateSummary — second TARA's

```
stateSummary(A→C) = stateSummary(B→C)
```

The intermediate state (A→B's summary) was consumed by B to produce B→C. The composed TARA carries what C actually receives, which is B→C's summary.

### sourceArc / targetArc

```
sourceArc(A→C) = sourceArc(A→B)
targetArc(A→C) = targetArc(B→C)
```

### timeMarker

```
timeMarker(A→C) = timeMarker(B→C)
```

The composed TARA's timestamp is the latest emission, since that's when the final transfer was constructed.

### provenance — chain

```
provenance(A→C) = {
  emitter: "composed",
  method: "tara-composition",
  chain: [provenance(A→B), provenance(B→C)]
}
```

### trustClass — weakest

```
trustClass(A→C) = weakest(trustClass(A→B), trustClass(B→C))
```

Trust class ordering: `self` > `neighbor` > `external` > `synthetic`. The composed trust class is the weakest in the chain.

### lossNotes for composition itself

The composition process itself introduces a loss: the intermediate representation (what B saw) is not preserved in the composed TARA. Add: `"intermediate representation at [B.id] consumed and not preserved"`.

## Associativity

Composition is associative for:
- **confidence**: multiplication is associative
- **driftEstimate**: addition is associative
- **lossNotes**: set union is associative
- **validityWindow**: min is associative
- **trustClass**: min over an ordered set is associative

Composition is approximately associative for:
- **reconstructionTarget**: narrowing is associative if the narrowing operation is consistent, but natural-language targets may produce different phrasings depending on grouping
- **stateSummary**: always takes the final TARA's summary, so grouping doesn't affect the result
- **provenance**: chain nesting differs ((A,B),C vs A,(B,C)) but carries the same information

## Worked example

See `docs/mappings/diagonal-decomposition.md` and `examples/diagonal-decomposition/` for a three-hop composition:

```
TARA(slow-observer → meso-observer) ∘ TARA(meso-observer → meso-observed) ∘ TARA(meso-observed → fast-observed)
```

Result:
- confidence: 0.85 × 0.76 × 0.88 = 0.569
- driftEstimate: 0.06 + 0.12 + 0.20 = 0.38
- lossNotes: 9 entries (3 from each hop)
- validityWindow: min(500, 200, 50) = 50 ticks
- trustClass: self (all hops are self)
