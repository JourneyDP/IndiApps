# IndiApps Foundation Plan (DRAFT for Col's acceptance)

Drafted 24 Nov 2026 from a planning conversation with Col. Updated the same day with Col's rulings (D13 to D22) and the first draft of the charter and core schema v0.1. Nothing here has been built into the Platform. Labels: **[Col]** stated by Col this session. **[Claude-decided]** Col delegated the choice to Claude; Col has not yet confirmed it. **[Inferred]** Claude's reasoning. Standards named below are from Claude's own knowledge and were not searched or verified this session.

Companion docs: `core/CHARTER.md`, `core/indiapps-core-v0.1.schema.json`, `core/validate_pack.py`, `conformance/cases-v0.1.json`.

## 1. Intent [Col]

- IndiApps defines a **generic, universal schema and framework** for very small to medium businesses. It is a **mandatory foundation** for sub-solutions.
- Sub-solutions (IndiApps-Experiences, IndiApps-Plumber) customise it only by **encoding their ontology and workflows**, never by changing the core.
- IndiApps and IndiApps-Experiences are developed in the OpenHands and IndilumeApp environment, deployed to Google GCP.
- **OpenHands replaces Antigravity 2.0 in the IndilumeApp framework.** Runtime otherwise follows the current IndilumeApp specification. Col says OpenHands gives the same SDLC functionality.
- **The Google ecosystem is primary. Gemini is the likely model and GEAP is required.**
- **GitHub is the repository: `https://github.com/JourneyDP/IndiApps.git`.**
- First proof: **both sub-solutions in parallel**, to keep the core generic.
- Col is interested in **AI populating a new pack initially**, by scraping or referring to existing solutions.

## 2. Core concepts Col described [Col]

1. **Resource.** Anything of value: time, kg of raw material, intellectual property, a right to use public land. Units and quantities are configurable and are not fixed on the resource.
2. **Acquisition and change of resources.** Dug up, cooked, combined, manufactured, purchased, grown, sub-assembled, converted, time given for payment or exchange.
3. **Consumption of resources.** By time, depreciation, sub-manufacture, selling, shrinkage, half-life, converting, giving away.
4. **Workflow.** Strings resources together to produce outputs: product, sub-assembly, service experience, an occurrence of governance, new processes, new discoveries.
5. **Transaction.** A point in time where a workflow node consumed, committed or produced a resource, started a branch, or spawned a new workflow (inside or outside the owning organisation).
6. **Information files** (formerly "master files"). Customers, suppliers, compliance bodies, the primary organisation, competitors. Information may be static, occasionally changing, changing on a schedule, or changing unpredictably as a result of a workflow.
7. **Log and audit.** Believed to be already embedded in the IndilumeApp framework.
8. **Communication** within and between workflows, humans and agents. Synchronous and asynchronous.

## 3. Design decisions

| # | Decision | Status | Reason |
|---|---|---|---|
| D1 | Use REA / ValueFlows as the **vocabulary** (resource, event, agent, commitment, process). Do not adopt them as the runtime design. Publish a mapping to them, and to CloudEvents for the event envelope. | [Claude-decided] after Col asked what to recommend given agentic speeds | Those standards predate agent-speed, machine-to-machine transactions. |
| D2 | **Per-stream ordering** with idempotency keys, anchored together periodically. Do not rely on a single global hash chain and sequence. | [Inferred] | The profile notes `accept_event` scans all events for duplicates and will slow as the log grows. |
| D3 | **Commitments are reservations with a lease and expiry**, with optimistic concurrency. | [Inferred] | Agents will race for the same resource. |
| D4 | **Authority travels with every event.** Each external-effect event records the mandate that authorised it. | [Inferred] | D-081 (human approval for every outward action) cannot work at agent speed. |
| D5 | **Authority model: tiered by risk, using mandates.** Low-risk actions run automatically. Other actions need a human-approved mandate (class of action, caps, counterparties, expiry). High-risk actions always need a human each time (see D16). | [Claude-decided]; how it sits with D-081 is deferred (D19) | Keeps speed where safe and keeps a human where it matters. |
| D6 | **Units: dimensional model.** A resource type declares the dimensions it can be counted in (mass, time, count, right-of-use, currency). Every event records its own value and unit. Each pack declares its unit sets and conversions. | [Claude-decided] | Configurable per organisation, and lets a validator reject packs that mix incompatible units. |
| D7 | **Decay, depreciation, half-life, shrinkage:** declarative rules on the resource type. The engine writes ordinary consume events tagged with the causing rule, written lazily (when the resource is next touched, or at period close). Balances are computed on read in between. | [Claude-decided] | Keeps the log small at high event rates and stays auditable. |
| D8 | **Communication is typed first.** Each message carries a schema and a purpose (request, offer, commit, notify). Natural-language text is an attachment. The core defines meaning, not transport. | [Inferred] | Needed for agent-to-agent work. |
| D9 | **Pack format:** one declarative format holding ontology, workflows, units and policies. Authoring route: AI drafts from sources, a human accepts (the Scoping Tool's propose-then-accept pattern). A UI can come later on the same format. | [Claude-decided] | One format serves developers, AI and, later, business owners. |
| D10 | **Every AI-drafted element carries its source, a confidence and its origin tag.** Scraped material is treated as draft only, subject to a licensing and terms-of-use check before commercial use. | [Inferred] | Provenance and legal risk. |
| D11 | **Cross-organisation work: adapters first.** The core models the boundary and keeps evidence for foreign systems (email, accounting, supplier portals). When the counterparty is also an IndiApps organisation, the same boundary record is shared natively. | [Col] chose adapters, noting it may also be a native IndiApps organisation | |
| D12 | **Runtime:** local-first Mac event log plus GCP backend, as in the current IndilumeApp spec. Schema and event format stay runtime-neutral. | [Col]: "as per the current indilumeapp specification" | |
| D13 | **OpenHands replaces Antigravity 2.0 in the IndilumeApp framework** as the build lane. Docs: https://docs.openhands.dev/overview/introduction. Repos: https://github.com/orgs/OpenHands/repositories. Wherever the Platform profile (30 Oct 2026) says "Antigravity 2.0", read "OpenHands". The profile itself has not been edited. | [Col], 24 Nov 2026 | |
| D14 | **GitHub is the repository** and the source of truth for the shared core and packs. | [Col], 24 Nov 2026 | |
| D15 | **Google ecosystem is primary. Gemini is the likely model; GEAP is required.** The build lane and the runtime model path go through GEAP. | [Col], 24 Nov 2026 | |
| D16 | **High risk = money above a limit.** A payment, purchase or commitment above a cap set by the organisation always needs a human each time. This is the core's only mandatory per-action trigger. | [Col], 24 Nov 2026 | |
| D16a | A pack or organisation **may add stricter triggers** (for example irreversible lodgements or personal data) but can never remove the money cap. | [Claude-decided]; an addition to Col's answer, for Col to confirm | Col selected only money; some sub-solutions will handle children's or customers' data. |
| D17 | **Who grants mandates:** the organisation's owner by default. An organisation may widen this to roles using the existing IndilumeApp roles and levels, and no one can grant more authority than they hold. | [Claude-decided] | One simple default for very small businesses, with room for larger ones. |
| D18 | **Delegation:** an agent may pass on a narrower slice of its mandate (lower cap, shorter expiry) to another agent or spawned workflow inside the same organisation. The chain is recorded on every event. A mandate never crosses to another organisation; the other organisation grants its own. | [Claude-decided] | Workflows that spawn workflows need it; narrowing keeps it auditable. |
| D19 | **Scope against D-081: decide later.** The schema supports both per-action approval and mandates. Rule on it when the first pack runs. | [Col], 24 Nov 2026 | |
| D20 | **One GitHub repo (monorepo)** holding `core/`, `packs/experiences/`, `packs/plumber/` and `conformance/` while the core is at v0.x. Split packs into their own repos once the core reaches v1.0. | [Claude-decided]; Col said "guided by Claude" | Both packs are being built in parallel against a moving core, so core and pack changes need to land together. |
| D21 | **The repo is `IndiApps`, at `https://github.com/JourneyDP/IndiApps.git`.** | [Col], 24 Nov 2026 | |
| D22 | **The money cap applies per action.** | [Col], 24 Nov 2026 | |
| D23 | **The OpenHands change stays recorded in this project only for now.** No register delta. | [Col], 24 Nov 2026 | |

## 4. Core entities

Now defined in `core/indiapps-core-v0.1.schema.json` (draft): Pack, Dimension, Unit, Conversion, ResourceType (with consumption rules), InformationRecordType, WorkflowDefinition and Node, Policies, EconomicEvent, Commitment, Mandate, Message, BoundaryRecord, Provenance. Names remain provisional until Col accepts v0.1.

## 5. Plan

| Phase | What | Output | State |
|---|---|---|---|
| 0 | Col accepts or amends this plan and the points in section 6 | Accepted plan | Open |
| 1 | Write the **foundation charter** and **core schema v0.1**, with valid and invalid conformance cases. Map to the existing event envelope 2.0.0 and the workflow definition shape. | Charter and schema in the IndiApps project and in GitHub | **Drafted 24 Nov 2026 in the project. Not in GitHub. Not accepted by Col.** |
| 2 | Create **IndiApps-Experiences** and **IndiApps-Plumber** in claude.ai (Col does this; Claude cannot create projects). Seed each with the charter, schema, glossary, Platform profile and this plan, plus an "extends IndiApps core vX, cannot override it" doc. | Two seeded projects | Open |
| 3 | Hand-write a small pack for each sub-solution against the core. Record every place the core had to bend. | Two packs and a gap list | Tiny illustrative seed packs exist as conformance cases only |
| 4 | Revise the core from the gap list. Define the pack format and validator. | Core v0.2, pack format | Open |
| 5 | Build the **AI pack-drafting pipeline** with provenance, confidence and human acceptance. | Draft-from-sources tool | Open |
| 6 | Implement the runtime pieces in the Platform via the OpenHands build lane: reservation leases, mandates, lazy decay, typed messages. | Work orders | Open |

Source of truth for shared files: **GitHub**, one repo (D14, D20, D21). Claude Projects do not share documents or chat history with each other, so each project gets a copy of the core from GitHub.

## 6. Conflicts and open points (not verified or not resolved)

1. **OpenHands with Gemini through GEAP is not verified.** The OpenHands organisation page (read 24 Nov 2026, page 1 of 2) shows it maintains a fork of LiteLLM, an LLM gateway whose description lists VertexAI among providers. Gemini, Google and GEAP are not named on the pages read. Since GEAP is required (D15), confirm this route works before any build work depends on it.
2. **OpenHands: what else was checked.** Introduction page and organisation repo list only. Components: Agent Canvas (browser client), a Python Software Agent SDK (MIT), Agent Server, an automation service (MIT), OpenHands Cloud and Enterprise (other licences). The docs say the CLI is no longer actively maintained and the local GUI is deprecated. **Not verified:** that it matches Antigravity 2.0's functions in the SDLC (Col's statement), which component and deployment IndilumeApp will use, GitHub integration, and its fit with the register and work-order process.
3. **Python-only (SR-9).** The profile says Python is mandatory unless a work order says otherwise. Not confirmed whether it still holds under OpenHands. (The OpenHands SDK is itself Python.)
4. **GitHub repo state.** On 24 Nov 2026 a `git ls-remote` on the repo URL returned no branches and no error, which suggests the repo exists and is empty. Claude's session had no API or push access to it, so this is not confirmed and nothing has been pushed.
5. **D-081** stays in force for the Platform until Col rules (D19).
6. **Money cap default value** is not set. The schema requires each pack to state one.
7. **D16a** (packs may add stricter approval triggers) awaits Col's confirmation.
8. **Standards claims** (REA, ValueFlows, ISA-95, CloudEvents, MCP, A2A and others) are from Claude's knowledge and not checked against current sources.
9. The third resource doc, `resources/01-ipaas-event-driven-workflow-automation.md`, was not read for this plan.
