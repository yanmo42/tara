# TODO — next steps brainstorm

Phases 1-4 are done. This is a loose capture of what to work on next.

---

## Immediate / high value

- **Battle-test the schemas with real data.** The examples are hand-authored. Try writing a TARA from an actual Sandy Chaos or Yggdrasil operation — a real raven return, a real promotion decision — and see what breaks or feels wrong.

- **Wire up the validator to CI or a git hook.** Right now it's a script you run manually. A pre-commit hook that validates all `examples/**/*.json` would catch regressions immediately.

- **Composition test with real TARAs.** The diagonal decomposition is synthetic. Try composing two real-world TARAs (e.g., a Huginn scout result → Muninn compression → spine decision) and check whether the composed output makes sense.

---

## Schema / spec loose ends

- **`validityWindow.duration` parsing** — currently a raw string (ISO 8601 or human-readable). Should we parse it in the tools? Or commit to ISO 8601 only and add a regex pattern?

- **Arc identifier collisions** — if two arcs have the same `id` but different `temporalBand`/`role`, that's a problem. Is the `id` meant to be globally unique? Worth deciding and documenting.

- **`reconstructionTarget` as a structured field?** Right now it's a free string, which is fine, but after writing a dozen examples you may find patterns. Could become an enum of intent types + a freeform description.

- **`provenance` is still wide open** — the base schema has `additionalProperties: true`. After seeing real provenance objects, it may be worth tightening.

---

## Cross-project integration

- **Sandy Chaos: actually emit TransferBundles as TARAs.** The mapping doc exists — can we make Sandy Chaos code output a valid TARA JSON alongside or instead of a TransferBundle? Even a proof-of-concept in one place would validate the mapping.

- **Yggdrasil: TARA for next promotion.** Next time you run `ygg promote`, write the TARA manually. See if the fields are obvious or if something is missing.

- **Sandy Chaos diagonal: run the toy benchmark.** Note 13 suggests comparing neighbor-only vs all-to-all coupling. The diagonal decomposition TARAs could anchor that experiment — each TARA represents one hypothesis about information available at each stage.

---

## Tooling

- **Drift estimator: better capacity math.** Currently uses a simple exponential. The gear coupling simulation in `temporal-arc-rd` has a more principled capacity formula (`log2(1/tolerance) * min(ratio)`). Hook that into the drift estimator for gear-coupled TARAs.

- **Compose tool: add `--validate` flag.** After composing, automatically run the validator on the output. One command instead of two.

- **Compose tool: handle arc mismatch gracefully.** Currently errors if IDs don't match — but what if the arcs match semantically (same band/role) but have different IDs? Worth thinking about.

- **Schema viewer / diff tool?** Something that shows what changed between two versions of the same TARA (emission vs. re-emission). Would help track how summaries evolve.

---

## Theory

- **Composition: gear fields aren't composed yet.** The rules cover base TARAs but `gearRatio`, `phaseAlignment`, `slippageTolerance` have no composition rule. What's the composed gear ratio for a chain — the product? The weakest link?

- **RG: write a beta function sketch.** The renormalization doc draws the analogy but stops short of equations. Even a rough `d(confidence)/d(coarsening_step) = -drift * confidence` would be a start.

- **Retrodiction: try it on a real example.** Take a completed TARA, pretend you're the source, try to infer back. What can you recover? What can't you? Write it up — the exercise will sharpen the semantics faster than theorizing.

---

## Parked ideas (moving closer?)

- **Simulation framework.** Schemas feel stable enough. Port the `temporal-arc-rd` simulator in — scope: emit valid TARAs from simulated gear-coupled worldlines, validate them, compose them. Would close the loop between the framework and measurable output.

- **Visual inspector.** Even a quick `graphviz` render of a TARA chain (boxes for arcs, arrows for transfers, labels for confidence/drift) would communicate the structure cheaply. Not a web app — just `dot` output from the compose tool.
