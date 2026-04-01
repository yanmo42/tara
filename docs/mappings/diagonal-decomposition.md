# Diagonal Coupling as TARA Composition

Sandy Chaos note 13 (section 4.3) disallows direct diagonal coupling. A slow-observer affecting a fast-observed domain must be decomposed into admissible neighbor links:

```
D_{observer,slow} → D_{observer,meso} → D_{observed,meso} → D_{observed,fast}
```

This three-hop chain is the first concrete test case for TARA composition.

## The three TARAs

### Step 1: slow-observer → meso-observer (temporal coupling, downward)

A slow governance signal compressed for the meso layer.

- Transfer type: same-role, adjacent-band (temporal coupling)
- Direction: slow → meso (fast-ward)
- What moves: policy context, governance constraints, continuity priorities
- What's lost: long-term strategic nuance, multi-epoch patterns

See `examples/diagonal-decomposition/step1.json`

### Step 2: meso-observer → meso-observed (polarity coupling)

The meso observer's compressed model crosses the observer/observed boundary.

- Transfer type: opposite-role, same-band (polarity coupling)
- Direction: observer → observed
- What moves: observer's model of what it expects, measurement priorities
- What's lost: observer's internal uncertainty, alternative interpretations

See `examples/diagonal-decomposition/step2.json`

### Step 3: meso-observed → fast-observed (temporal coupling, downward)

The meso-observed domain passes actionable constraints to the fast layer.

- Transfer type: same-role, adjacent-band (temporal coupling)
- Direction: meso → fast (fast-ward)
- What moves: boundary conditions, priority signals, constraint summaries
- What's lost: meso-level context, routing rationale, alternative routes

See `examples/diagonal-decomposition/step3.json`

## Composition result

Composing all three yields TARA(slow-observer → fast-observed):

- `confidence` = 0.85 * 0.76 * 0.88 ≈ 0.569
- `driftEstimate` = 0.06 + 0.12 + 0.20 = 0.38
- `lossNotes` = union of all three steps (9 entries)
- `validityWindow` = min(500, 200, 50) = 50 ticks
- `reconstructionTarget` narrowed at each hop

The confidence degradation (0.85 → 0.569) and drift accumulation (0.06 → 0.38) are why Sandy Chaos disallows the diagonal shortcut — the compound loss is substantial, and pretending it's a single clean transfer hides this cost.

## Implications for composition rules

This test case confirms:
1. Confidence compounds multiplicatively (each hop degrades trust)
2. Drift accumulates additively (each hop adds staleness)
3. Loss notes merge (information is lost at every boundary)
4. Validity window takes the minimum (the shortest-lived hop constrains the chain)
5. The reconstruction target narrows at each step
