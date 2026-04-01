# tara

**Temporal-Arc Reference Arrays** — a bounded representation discipline for moving structured state across temporal layers.

## Core idea

Many systems talk as if past, present, future, or multi-cadence layers can directly access each other's full state. In practice, what moves across a temporal boundary is always some compressed, partial, stale, or purpose-shaped representation.

A **TARA** makes that explicit:

> a bounded structured record describing what one temporal arc can hand to another — with declared confidence, drift, compression, and reconstruction limits.

The R/D split reads as **Reference / Dynamical**:
- **Reference**: what is retained, indexed, and handed forward
- **Dynamical**: the source keeps evolving, so the reference is always at risk of drift

## Discipline rule

> No raw cross-arc state access. Only bounded reference arrays with declared reconstruction limits.

This blocks: magic omniscience, metaphor drift, hidden uncertainty, and post-hoc reinterpretation without cost.

## Mechanical operationalization: worldline gears

A deeper framing treats worldlines as **computational gears** operating at different cadences:

- **Gear ratios** (3:1, 7:3, …) determine transfer characteristics between cadences
- **Phase alignment** determines when transfer can happen
- **Slippage tolerance** sets a measurable failure threshold
- **Steganographic encoding** embeds information in timing/phase relationships

This makes TARA testable, implementable, and auditable rather than just conceptual.

## Contents

- `schemas/` — JSON Schema definitions for base TARA and gear-coupled TARA
- `examples/` — hand-authored and simulated reference array instances
- `docs/` — vision and architecture notes

## Use cases

- agent continuity snapshots
- planner/resume packets
- temporal simulation checkpoints
- observer/chaser delayed-state models
- multiscale control systems
- memory pipelines
