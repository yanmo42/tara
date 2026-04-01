# TARA and Renormalization Group

A precise analogy connecting TARA to renormalization group (RG) language.

## The analogy

A fast→meso TARA is the computational analog of a coarse-graining step in statistical physics. The RG transformation integrates out fast degrees of freedom and produces an effective description at a coarser scale. A TARA does the same thing across temporal arcs.

## Field-by-field mapping

| RG concept                  | TARA field / concept                     |
|-----------------------------|------------------------------------------|
| Microscopic degrees of freedom | Source arc's full state                 |
| Coarse-grained description  | `stateSummary`                           |
| Relevant operators          | Fields retained in `stateSummary`        |
| Irrelevant operators        | `lossNotes` — what was integrated out    |
| Scale factor                | `gearRatio` — cadence ratio between arcs |
| Block-spin transformation   | The compression from source to summary   |
| Coupling constants          | `confidence`, `driftEstimate`            |
| RG flow                     | Composition chain of TARAs               |

## Relevant operators

In RG, relevant operators are those that survive coarse-graining and determine the long-distance (slow-scale) behavior. In TARA:

- `stateSummary` contains exactly the relevant operators — the compressed state that the target arc will use
- The source arc's job is to identify which aspects of its state are relevant to the target
- This is a judgment call, not a mechanical operation — which is why `confidence` is always < 1

## Irrelevant operators

In RG, irrelevant operators are integrated out during coarse-graining. They affect the microscopic behavior but not the macroscopic description. In TARA:

- `lossNotes` explicitly names the irrelevant operators — the degrees of freedom that were dropped
- Unlike physics RG, TARA keeps a record of what was dropped (you can't reconstruct it, but you know it's gone)
- This is better than standard RG, where the information about what was integrated out is typically implicit

## Scale factor

In RG, the scale factor describes how much the system has been coarsened. In TARA:

- `gearRatio` is the explicit scale factor — a `3:1` ratio means the target operates at 1/3 the cadence
- The ratio determines the information capacity: how many source-frame bits can pass per target-frame cycle
- In physics: the ratio between the lattice spacing before and after blocking

## RG flow and composition

A chain of TARAs (fast → meso → slow) is an RG flow:

```
fast state → [3:1 coarse-graining] → meso description → [7:1 coarse-graining] → slow description
```

Composition (see `docs/theory/composition.md`) corresponds to composing two RG steps. The composed scale factor is the product of the individual ratios (3:1 ∘ 7:1 = 21:1). Confidence degrades because each coarse-graining step loses information.

## Universality class

In RG, a universality class is the set of microscopic systems that flow to the same fixed point under coarse-graining. In TARA:

- A universality class is the set of source states that produce the same `stateSummary` under the same compression policy
- Two sources are in the same universality class if their TARAs are indistinguishable at the target's resolution
- The target cannot distinguish between sources in the same class — this is exactly what `lossNotes` warns about

## Fixed points

In RG, a fixed point is a description that is invariant under further coarse-graining. In TARA:

- A fixed point is a TARA that, if composed with a further coarse-graining step, produces the same `stateSummary`
- This would mean the description is already at the coarsest useful resolution — no further compression is possible without losing relevant information
- Fixed points are rare in practice but important conceptually: they represent the most compressed useful description

## Where the analogy holds

- **Coarse-graining is lossy**: both RG and TARA acknowledge that going to coarser scales loses information
- **Relevant vs irrelevant**: both distinguish between what survives and what's integrated out
- **Scale hierarchy**: both operate on a hierarchy of scales with explicit ratios
- **Composition**: both compose coarse-graining steps, with compound effects on the coupling constants
- **Universality**: both identify equivalence classes of fine-grained states that map to the same coarse description

## Where the analogy is approximate

- **Quantitative RG**: physics RG produces precise flow equations (beta functions). TARA composition rules are simpler — multiplicative confidence, additive drift. A full "beta function for TARAs" would describe how confidence and drift flow under repeated coarse-graining, which may be worth formalizing if TARA is used in systems with many scale levels.
- **Symmetry**: physics RG is deeply connected to symmetry groups. TARA has no explicit symmetry structure, though the frame-invariance analysis (see `docs/theory/invariants.md`) plays a related role.
- **Continuum limit**: physics RG often studies the continuum limit (infinite coarse-graining). TARA has finite chains with a small number of steps. The continuum analog would be a system with arbitrarily many temporal layers — possible but not yet needed.

## Testable claim

If this analogy holds, then TARA chains should exhibit RG-like behavior:

1. **Confidence should decay predictably** along a chain — if the first coarse-graining loses 15% confidence and the second loses 24%, the pattern should be consistent and predictable for similar transfers.
2. **Some information should be universally irrelevant** — certain types of loss notes (e.g., "fine-grain microstate omitted") should appear at every coarse-graining boundary, indicating robust irrelevant operators.
3. **Fixed-point behavior** should be observable — after enough coarse-graining, the summary should stabilize and further compression should not change it.

These are empirically testable once TARA is used in systems with enough data.
