# Architecture

## Primitive objects

### 1. Temporal arc
A bounded interval or cadence context:
- fast / meso / slow
- tick N
- session epoch
- checkpoint interval

### 2. Reference array
A structured packet emitted by one arc for use by another. Contains compressed state, declared confidence, drift estimate, and reconstruction limits.

### 3. Reconstruction policy
A declared rule for how another arc may use the array. What it can infer, what it cannot, and what failure looks like.

## Minimal fields

| Field | Purpose |
|---|---|
| `sourceArc` | Which arc emitted the array |
| `targetArc` | Which arc will consume it |
| `timeMarker` | When it was emitted |
| `stateSummary` | Compressed state representation |
| `confidence` | How much to trust it (0–1) |
| `driftEstimate` | Expected staleness rate |
| `reconstructionTarget` | What the consumer is trying to recover |
| `lossNotes` | What was deliberately dropped |
| `provenance` | Where this came from |
| `trustClass` | `self` / `neighbor` / `external` / `synthetic` |

## Gear-coupling extension

When temporal arcs are modeled as gears:

| Field | Mechanical meaning |
|---|---|
| `gearRatio` | Cadence relationship (e.g. `3:1`) |
| `phaseAlignment` | Normalized phase match at transfer time (0–1) |
| `slippageTolerance` | Max allowable phase error before transfer fails |
| `informationCapacity` | Bits per gear cycle (derived from ratio and tolerance) |
| `mechanicalFailureModes` | Observed: slippage, backlash, tooth-skipping, resonance |

## Discipline rule

> No raw cross-arc state access. Only bounded reference arrays with declared reconstruction limits.

In gear terms:

> No direct state transfer. Only gear-coupled representations with explicit ratio, phase, and slip limits.

## Failure conditions

TARA fails if:
- arrays become decorative jargon with no enforcement
- drift and loss are declared but ignored downstream
- reconstruction claims grow stronger than the data supports
- the concept expands faster than examples and experiments justify

Mechanical failure is more specific and observable: slippage beyond tolerance, backlash in bidirectional transfer, tooth-skipping at specific cadences, resonance at harmonic ratios.
