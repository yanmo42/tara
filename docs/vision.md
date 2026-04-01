# Vision

## One sentence

Build a disciplined reference-array model for representing what can move lawfully across temporal arcs.

## Problem

Systems operating across time — multiscale simulations, agent memory pipelines, observer/chaser models, distributed control — routinely pretend that one temporal layer can directly access another's full state. That pretense hides compression loss, latency, uncertainty, and reconstruction error.

## Proposal

Instead of raw cross-arc access, define explicit arrays that record:
- what is preserved
- what is compressed
- what is lost
- how stale the representation is
- what reconstruction claim is being made

## Design stance

- adjacent or bounded transfer by default
- explicit drift and error handling
- no hidden omniscience
- useful both as documentation and as executable contract

## Mechanical operationalization

The gear-coupling framing adds a concrete engineering layer: worldlines as gears with ratios, phase alignment requirements, slippage tolerances, and information capacity limits. This transforms TARA from an abstract pattern into something measurable and buildable.
