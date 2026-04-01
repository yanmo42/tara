# TODO

Work plan for bringing TARA from seed to operational framework.

---

## Phase 1 — Schema foundations

The schemas work but have structural problems that will compound if left unfixed.

- [ ] **Schema composition via `$ref`**: The gear-coupled schema duplicates every base field instead of extending it. Refactor so `tara-gear-coupled.schema.json` uses `$ref` to inherit from `tara.schema.json` and adds only the mechanical extension fields. This also makes it possible for others to extend the base without copy-paste.

- [ ] **Add `validityWindow`**: Sandy Chaos's TransferBundle already has this. A TARA without an expiry is a TARA that pretends it stays fresh forever, which violates the drift discipline. Should be a duration or tick-count after which the consumer must treat the array as stale.

- [ ] **Structured arc identifiers**: `sourceArc` and `targetArc` are bare strings. At minimum they should carry a temporal band (fast/meso/slow or a numeric cadence) and a role if applicable. Consider whether this should be a sub-object or a naming convention with a regex pattern.

- [ ] **Richer `driftEstimate`**: Currently a single number, but drift is directional — some fields decay faster than others. Consider whether this should become an object with per-field or per-dimension estimates, or whether the single-number version is the right simplification at this stage.

- [ ] **`stateSummary` sub-schemas**: Currently `additionalProperties: true`, which is maximally permissive. Define optional domain-specific sub-schemas (e.g., a Sandy Chaos transfer payload, a Yggdrasil promotion payload) that can be validated when the context is known.

---

## Phase 2 — Cross-project alignment

TARA is the formal representation discipline underneath patterns that Sandy Chaos and Yggdrasil already use informally. Making the mapping explicit gives all three projects shared infrastructure.

### Sandy Chaos

- [ ] **Map TransferBundle → TARA**: Sandy Chaos note 13 defines a `TransferBundle { payload, source_domain, target_domain, latency, distortion, confidence, provenance, validity_window }`. Write the formal field mapping from TransferBundle to base TARA, identify any gaps, and produce an example TARA that represents a Nested Temporal Domain transfer (e.g., fast-observer → meso-observer).

- [ ] **Model the neighbor-layer codec as TARA lifecycle**: The four-stage codec (embed → extract → translate → reconstruct) maps to distinct phases of a TARA's life. Document this mapping. Consider whether the schema should carry a `lifecycleStage` field or whether that belongs in the consumer, not the record.

- [ ] **Diagonal coupling as TARA composition**: Sandy Chaos disallows direct diagonal coupling (e.g., slow-observer → fast-observed) and says it should be decomposed into admissible neighbor links. This is the TARA composition problem in concrete form. Use it as the first test case for composition rules.

### Yggdrasil

- [ ] **Model promotion as a TARA transfer**: Branch→spine promotion is a fast→slow transfer with compression, loss, and confidence judgment. Write example TARAs representing: (a) a branch experiment result being promoted to spine memory, (b) a branch result being declined (the TARA exists but was rejected by the reconstruction policy). This grounds the promotion concept in inspectable records.

- [ ] **Map durable traces to TARA provenance**: Yggdrasil's "durable trace" concept — the artifact that carries consequence forward — is the thing a TARA's `stateSummary` + `provenance` encodes. Make this explicit. A durable trace is a consumed TARA whose reconstruction was accepted.

- [ ] **Cadence discipline via gear ratios**: Yggdrasil's fast-edge / meso-layer / slow-spine cadence differentiation can be expressed as gear-coupled TARAs with explicit ratios. Write example gear-coupled TARAs for Yggdrasil's three cadence layers.

---

## Phase 3 — Open questions → working answers

These are the questions named in the README. They need to go from open questions to at least partially answered with notation and examples.

- [ ] **TARA composition rules**: Given TARA(A→B) and TARA(B→C), define TARA(A→C). Expected properties: confidence compounds (multiplies or worse), drift accumulates, lossNotes merge, reconstruction target narrows. Write this out formally with at least one worked example. Test whether composition is associative and under what conditions.

- [ ] **Retrodiction semantics**: Define what it means to run a TARA backward (target→source inference). Expected: confidence degrades faster than forward, entropy increase makes backward reconstruction lossy. The base schema may need a `directionality` field or this may be purely a consumer-side concern. Decide and document.

- [ ] **Frame-covariance / invariants**: Identify what quantities survive a change of frame (e.g., re-parameterizing the same transfer from the target's perspective instead of the source's). Candidates: the information capacity bound, the causal ordering, the loss profile. This connects to the RG framing — universality classes are the things that don't change under coarse-graining.

- [ ] **RG formalization**: Write a short note connecting TARA explicitly to renormalization group language. A fast→meso TARA is a coarse-graining step. The `stateSummary` contains the relevant operators. The `lossNotes` name the irrelevant operators that were integrated out. The gear ratio is the scale factor. This doesn't need to be a paper — it needs to be a precise enough analogy that a physicist can evaluate whether it holds.

---

## Phase 4 — Tooling

Light tooling to make the schemas usable, not a framework.

- [ ] **Schema validator**: A script that validates a JSON file against the base or gear-coupled schema. Python or Node, minimal dependencies. The old repo had one; rewrite it properly.

- [ ] **Composition calculator**: Given two TARA JSON files with matching target→source arcs, compute and emit the composed TARA with accumulated drift, compounded confidence, merged loss notes. This is useful both as a tool and as a forcing function for getting the composition rules right.

- [ ] **Drift decay estimator**: Given a TARA and an elapsed time/ticks, estimate the current effective confidence. Simple model first (exponential decay from `driftEstimate`), with room for more sophisticated models later.

---

## Not yet — parked ideas

These are worth remembering but not worth building yet.

- **Simulation framework**: A proper gear-coupling simulator with configurable ratios, phase noise, and information capacity measurement. The old repo had a toy version. Rebuild only when the schemas are stable enough that the simulator's output validates against them.

- **Visual inspector**: A small web tool that renders a TARA or a TARA chain as a diagram. Useful for communication, premature now.

- **TARA-native memory format for Yggdrasil**: Replace or augment Yggdrasil's memory files with TARA-structured records so every memory artifact is a consumed TARA with declared provenance and drift. This is architecturally clean but only worth doing once TARA and Yggdrasil are both more mature.
