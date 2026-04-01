# tara

**Temporal-Arc Reference Arrays** — a relational representation discipline for moving structured state across temporal frames.

## What this is

A TARA is not an object that lives inside a temporal frame. It is a relation *between* two frames — a structured record of what one temporal arc can lawfully hand to another, with declared confidence, drift, compression, and reconstruction limits.

The word "array" signals inspectability and structure. The harder point is the relational one: a TARA has no meaning without both a source and a target. It is defined by the gap between them.

This matters because most systems that operate across time pretend that one temporal layer can directly access another's full state. In practice what moves across a temporal boundary is always compressed, partial, stale, or purpose-shaped. TARA makes that unavoidable fact explicit and enforceable.

## Physics grounding

TARAs are intended to be implementable on any architecture. The way to ensure that is to keep the primitives in contact with first-principles physics rather than tying them to implementation specifics.

Three principles anchor the framework:

**Causality.** Information can only flow forward along the causal cone. A TARA can only be consumed after it was emitted. The discipline rule is a causality constraint, not just an engineering preference.

**Bounded information.** Any physical representation has a finite information content. Compression and loss are not optional features — they are the cost of crossing a temporal boundary. The `lossNotes` and `driftEstimate` fields exist to make this cost declared rather than hidden.

**Coarse-graining.** Moving from a fast arc to a slower one is the computational analog of renormalization group flow: fast degrees of freedom are integrated out and an effective description at the coarser scale is what survives. A TARA is the transfer record at that boundary. This gives the multi-scale hierarchy (fast → meso → slow) a well-understood physical interpretation.

## The R/D split

**Reference**: what is retained, indexed, and handed forward — stable enough to be consulted.

**Dynamical**: the source system keeps evolving after emission, so the reference is always at risk of drift. The two tensions live in every array simultaneously.

## Discipline rule

> No raw cross-arc state access. Only bounded reference arrays with declared reconstruction limits.

This is a causality and information-theoretic constraint. It blocks: magic omniscience, metaphor drift, hidden uncertainty, and post-hoc reinterpretation without declared cost.

## Worldline gears (mechanical operationalization)

A deeper framing treats worldlines as **computational gears** operating at different cadences. This is an analogy, not a claim about literal mechanics — but it is a productive one because it maps to measurable quantities:

- **Gear ratio** — the cadence ratio between two arcs (e.g. 3:1), which is the computational analog of a proper-time rate ratio between clocks
- **Phase alignment** — when in the source cycle a transfer is attempted; determines synchronization quality
- **Slippage tolerance** — maximum allowable phase error before the coupling is considered failed; a measurable threshold, not a vague limit
- **Information capacity** — bits per gear cycle, derivable from ratio and tolerance

Mechanical failure modes (slippage, backlash, tooth-skipping, resonance) become observable diagnostics rather than vague warnings.

## Open questions

**Composition.** If a fast→meso TARA and a meso→slow TARA exist, can they compose into a fast→slow TARA? Almost certainly yes, but with accumulated drift and loss at each boundary. The composition rules are not yet defined.

**Retrodiction.** TARAs flow forward. Running one backward — inferring source state from a target representation — is possible but degrades faster than forward prediction, consistent with entropy increase. The framework does not yet address this direction explicitly.

**Frame-covariance.** A TARA's contents are true relative to its source frame at emission time. By the time the target consumes it, the source has moved on. How much of a TARA is frame-invariant, and how much is observer-relative? This question becomes sharper as the framework is applied to relativistic or highly asynchronous systems.

## Contents

- `schemas/` — JSON Schema definitions for base TARA and gear-coupled TARA
- `examples/` — hand-authored reference array instances
- `docs/` — vision and architecture notes

## Use cases

- agent continuity and memory snapshots
- planner/resume packets across session boundaries
- temporal simulation checkpoints
- observer/chaser delayed-state models
- multiscale control systems
- any system where "the other layer knows the full state" is a hidden assumption worth removing
