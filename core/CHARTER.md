# IndiApps Foundation Charter

**Version 0.1, DRAFT. Not yet accepted by Col.** Written 24 Nov 2026. Repository: `https://github.com/JourneyDP/IndiApps.git`.

Decision numbers (D1 to D23) refer to `IndiApps_Foundation_Plan_2026-11-24.md`, which records who made each decision. Several were made by Claude on Col's delegation and still await his confirmation.

## 1. Purpose

IndiApps defines one generic schema and framework for the workings of a very small to medium organisation. It is the mandatory foundation for every sub-solution. The first two sub-solutions are IndiApps-Experiences and IndiApps-Plumber.

## 2. The rule

1. Every sub-solution is a **pack**. A pack encodes its ontology (dimensions, units, resource types, information record types) and its workflows, using only the shapes in the core schema.
2. A pack **cannot change, remove or add to the core**. The schema rejects any field the core does not define.
3. If a pack cannot express something, that is a **gap in the core**. It is logged and fixed in the core for everyone. It is never patched inside the pack.
4. Each pack states the core version it extends (`extendsCore`).

## 3. What the core defines

| Concept | Meaning | Schema name |
|---|---|---|
| Resource type | Anything of value an organisation gets, holds, uses up or produces: time, material, intellectual property, a right of use, money. | `ResourceType` |
| Dimension and unit | What a resource can be counted in. A resource type lists its allowed dimensions. Every quantity carries its own unit. | `Dimension`, `Unit`, `Quantity`, `Conversion` |
| Consumption rule | Loss that happens without anyone acting: elapsed time, depreciation, shrinkage, half-life, expiry. | `ConsumptionRule` |
| Information record | What used to be called master files: customers, suppliers, compliance bodies, competitors, the organisation itself. Each type states how often it changes. | `InformationRecordType` |
| Workflow | Nodes that string resources together to produce an output. Nodes can branch and can spawn other workflows, inside or outside the organisation. | `WorkflowDefinition`, `Node`, `Flow` |
| Economic event | The point in time where a node produced, consumed, used, committed, released or transferred a resource, branched, or spawned. | `EconomicEvent` |
| Commitment | A reservation of a resource for a run. It has a lease that expires. | `Commitment` |
| Mandate | A human's pre-approval for an agent to act within limits. | `Mandate` |
| Message | Typed communication between workflows, humans and agents, synchronous or asynchronous, with a human-readable version. | `Message` |
| Boundary record | Evidence of work crossing to or from another organisation, through an adapter or natively. | `BoundaryRecord` |
| Provenance | Who proposed an element, from what source, with what confidence. | `Provenance` |
| Policies | The pack's money cap and any stricter approval triggers. | `Policies` |

**Log and audit** are not redefined. Runtime records travel as the payload of the existing IndilumeApp event envelope 2.0.0.

## 4. Rules the validator enforces

The JSON Schema checks shape. `core/validate_pack.py` adds these cross-reference rules:

- **R1** Ids are unique within a pack.
- **R2** Every unit belongs to a declared dimension.
- **R3** Every resource type, and every consumption rule, uses declared dimensions.
- **R4** A conversion between two dimensions must name the resource type it applies to (for example, hours of a plumber's time to dollars).
- **R5** Workflow nodes only point to nodes that exist.
- **R6** Workflow nodes only use declared resource types.
- **R7** A node may only count a resource in a unit whose dimension that resource type allows.
- **R8** Every pack sets a money cap per action, in a currency unit.

## 5. Authority

- Money above the pack's cap, **per action**, always needs a human each time (D16, D22). This is the one trigger no pack can remove.
- A pack may add stricter triggers (D16a, awaiting Col's confirmation).
- Below the cap, agents act under mandates. The owner grants them by default (D17). An agent may delegate a narrower mandate inside its own organisation, and the chain is recorded (D18). Mandates do not cross organisations.
- How this sits with the Platform's rule D-081 is deferred (D19). Until Col rules, D-081 stays in force for the Platform.

**Not yet enforced by code:** that a delegated mandate is narrower than its parent, and that a mandate has not expired. Both need the runtime, since they compare one record with another.

## 6. AI-drafted packs

AI may draft a pack from existing sources. Every AI-proposed element must carry its source and a confidence, and stays a proposal until a human accepts it (D9, D10). Scraped material needs a licensing and terms-of-use check before commercial use.

## 7. Build and runtime

- Build lane: OpenHands, replacing Antigravity 2.0 (D13).
- Google ecosystem is primary; Gemini is likely and GEAP is required (D15).
- Runtime follows the current IndilumeApp specification (D12).
- **Not verified:** that OpenHands can use Gemini through GEAP. Confirm before build work depends on it.

## 8. Repository layout (D20)

```
core/           CHARTER.md, indiapps-core-v0.1.schema.json, validate_pack.py
conformance/    cases-v0.1.json (30 cases), build_cases.py
packs/
  experiences/  pack.json
  plumber/      pack.json
docs/           IndiApps_Foundation_Plan_2026-11-24.md
```

Run the checks with `python core/validate_pack.py --cases conformance/cases-v0.1.json`. On 24 Nov 2026 all 30 cases passed in Claude's workspace (Python with the `jsonschema` package). Nothing has been run inside IndilumeApp or OpenHands.

## 9. What v0.1 does not yet cover

1. The two seed packs are small illustrations written by Claude. They are not based on real business data.
2. Resource instances, balances and information record contents have no schema yet; only their types do.
3. Mapping to the Platform's existing event type names and its `schemaRef` scheme.
4. The mapping table to REA / ValueFlows and CloudEvents (D1).
5. Stream anchoring across per-stream sequences (D2).
6. Pack versioning and migration when the core changes.
