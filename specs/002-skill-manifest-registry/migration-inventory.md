# Spec 002 — Legacy Skill Migration Baseline

**Status:** Source inventory completed from `main` on 2026-10-08; migration NOT started. Blob SHAs are baseline source fingerprints, not behavioral parity proof.

## Canonical mapping proposal (review before T024)

| Existing skill / path | SKILL name | Target location (proposed) | Source blob SHA | Workflow references |
|---|---|---|---|---|
| `skills/architecture-plan/SKILL.md` | `architecture-plan` | `skills/delivery/ppmax-architecture-plan/SKILL.md` | `72412306e582f29c0db21aaa4fa694d5a8624deb` | idea-to-first-users, pre-launch-audit |
| `skills/customer-research/SKILL.md` | `customer-research` | `skills/opportunity/ppmax-customer-research/SKILL.md` | `6b557c25e12f73b51acda4247962b04a1bc19406` | idea-to-mvp |
| `skills/distribution-plan/SKILL.md` | `distribution-plan` | `skills/go-to-market/ppmax-distribution-plan/SKILL.md` | `7f2b2a53f0e0a12a747ee0ce3055fb61b6ba5fa2` | idea-to-first-users |
| `skills/engineering-readiness/SKILL.md` | `engineering-readiness` | `skills/verification/ppmax-engineering-readiness/SKILL.md` | `abc4d8d006cb797912d87856116156a510035503` | idea-to-first-users, pre-launch-audit |
| `skills/icp-positioning/SKILL.md` | `icp-positioning` | `skills/product-strategy/ppmax-icp-positioning/SKILL.md` | `b2d9dab505be6cac4122b73468d7e2084cad9488` | idea-to-mvp |
| `skills/idea-pressure-test/SKILL.md` | `idea-pressure-test` | `skills/opportunity/ppmax-idea-pressure-test/SKILL.md` | `a350608fb2cb73fa942c799e0a15d420f9addc82` | idea-to-mvp |
| `skills/launch-readiness/SKILL.md` | `launch-readiness` | `skills/go-to-market/ppmax-launch-readiness/SKILL.md` | `3f6b0b028870e6206edfeb26c2bda46d856d47df` | idea-to-first-users, pre-launch-audit |
| `skills/market-landscape/SKILL.md` | `market-landscape` | `skills/opportunity/ppmax-market-landscape/SKILL.md` | `2a0c67810544c4783a843cb37974a4cf8fd1d30a` | idea-to-mvp |
| `skills/mvp-scope/SKILL.md` | `mvp-scope` | `skills/product-definition/ppmax-mvp-scope/SKILL.md` | `d0994011bbd9bdbc94d900b69b341a5a3d471b7c` | idea-to-mvp, idea-to-first-users |
| `skills/pricing-experiment/SKILL.md` | `pricing-experiment` | `skills/growth/ppmax-pricing-experiment/SKILL.md` | `1e14cd667cf5b813dc2b28187e11c7397a2aeac1` | idea-to-first-users |
| `skills/problem-validation/SKILL.md` | `problem-validation` | `skills/opportunity/ppmax-problem-validation/SKILL.md` | `8c4889c9b0a067b94fe6257e98608c4588f9c9b2` | idea-to-mvp |
| `skills/runtime-verification/SKILL.md` | `runtime-verification` | `skills/verification/ppmax-runtime-verification/SKILL.md` | `a3934d01aa674dee04ff38e10a45ba52c301d0a0` | idea-to-first-users, pre-launch-audit |
| `skills/ux-flow/SKILL.md` | `ux-flow` | `skills/product-definition/ppmax-ux-flow/SKILL.md` | `c488f8df579a962b0ee9e01226663d190854e90f` | idea-to-first-users, pre-launch-audit |

Every mapping retains the original slug; proposed primary cycles require semantic review against Product Model before migration. No files have been renamed.

## Baseline behavior and evidence boundaries

The following is transcribed from each source `SKILL.md` frontmatter and Trigger section; complete behavioral authority remains the original file at its recorded blob SHA.

### architecture-plan

- **Purpose/description:** Create a proportionate software architecture plan from product constraints, risks and verification needs. Use before significant implementation or when architecture choices need explicit trade-offs.
- **Positive trigger:** Use after MVP scope and core flows are sufficiently defined.
- **Exclusion:** Do not introduce enterprise patterns, microservices or infrastructure without a constraint that justifies them.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `72412306e582f29c0db21aaa4fa694d5a8624deb`
- **Markdown link targets:** none detected

### customer-research

- **Purpose/description:** Plan or synthesize customer research into traceable observations, pains, workarounds and buying signals. Use for interviews, notes, support conversations or qualitative research before product decisions.
- **Positive trigger:** Use to design interviews or synthesize existing qualitative customer material.
- **Exclusion:** Do not use leading questions to seek confirmation of a preferred solution.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `6b557c25e12f73b51acda4247962b04a1bc19406`
- **Markdown link targets:** none detected

### distribution-plan

- **Purpose/description:** Create a concrete distribution plan from ICP behavior, reachable channels, message, asset, CTA and measurement. Use before or immediately after launch to acquire the first users intentionally.
- **Positive trigger:** Use when ICP and product promise are specific enough to identify where prospects already gather.
- **Exclusion:** Do not choose channels because they are popular with founders rather than used by the target segment.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `7f2b2a53f0e0a12a747ee0ce3055fb61b6ba5fa2`
- **Markdown link targets:** none detected

### engineering-readiness

- **Purpose/description:** Audit implementation readiness across security, testing, observability, data safety, migration, rollback and operational risk. Use before declaring a build production-ready.
- **Positive trigger:** Use during late implementation, before launch readiness, or when inheriting AI-generated code.
- **Exclusion:** Do not mark checks complete from plans alone when runtime or test evidence is required.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `abc4d8d006cb797912d87856116156a510035503`
- **Markdown link targets:** none detected

### icp-positioning

- **Purpose/description:** Define a narrow ideal customer profile and positioning from validated problem evidence. Use when a product needs a specific audience, value proposition and reason to choose it.
- **Positive trigger:** Use after initial problem/customer evidence exists and before broad MVP scope or launch messaging.
- **Exclusion:** Do not define an ICP using only broad firmographics such as “small businesses”.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `b2d9dab505be6cac4122b73468d7e2084cad9488`
- **Markdown link targets:** none detected

### idea-pressure-test

- **Purpose/description:** Stress-test a product idea before implementation by exposing assumptions, risks, alternatives and missing evidence. Use when a builder has an idea and is deciding whether it deserves deeper validation.
- **Positive trigger:** Use when a user presents a product idea, feature concept or venture and wants to know whether it deserves deeper validation.
- **Exclusion:** Do not use as a substitute for customer research, market research or runtime verification.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `a350608fb2cb73fa942c799e0a15d420f9addc82`
- **Markdown link targets:** none detected

### launch-readiness

- **Purpose/description:** Run a cross-functional launch gate over product, UX, engineering, analytics, onboarding, support, discoverability and rollback. Use immediately before exposing an MVP to target users.
- **Positive trigger:** Use after core MVP functionality exists and runtime verification has begun.
- **Exclusion:** Do not require enterprise polish for a small controlled beta; readiness must match launch scope.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `3f6b0b028870e6206edfeb26c2bda46d856d47df`
- **Markdown link targets:** none detected

### market-landscape

- **Purpose/description:** Map direct competitors, indirect competitors, substitutes, manual workarounds and do-nothing behavior for a product problem. Use when positioning, differentiation or market understanding is needed.
- **Positive trigger:** Use after a problem and customer segment are specific enough to define a market context.
- **Exclusion:** Do not treat a list of companies as a market analysis.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `2a0c67810544c4783a843cb37974a4cf8fd1d30a`
- **Markdown link targets:** none detected

### mvp-scope

- **Purpose/description:** Reduce a product idea to the smallest coherent MVP that tests the critical product hypothesis. Use when deciding what to build now, later or explicitly not at all.
- **Positive trigger:** Use after a problem/ICP hypothesis is clear enough to define the product test.
- **Exclusion:** Do not use MVP as shorthand for low quality or a miniature full roadmap.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `d0994011bbd9bdbc94d900b69b341a5a3d471b7c`
- **Markdown link targets:** none detected

### pricing-experiment

- **Purpose/description:** Turn pricing into a falsifiable hypothesis about value metric, package, segment and willingness to pay. Use before choosing or changing a monetization model.
- **Positive trigger:** Use when a target segment and meaningful product outcome are defined.
- **Exclusion:** Do not present a precise price as validated without willingness-to-pay or transaction evidence.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `1e14cd667cf5b813dc2b28187e11c7397a2aeac1`
- **Markdown link targets:** none detected

### problem-validation

- **Purpose/description:** Evaluate whether a customer problem has enough real evidence to justify product investment. Use before committing MVP scope or when a team is unsure whether observed pain is real, frequent and consequential.
- **Positive trigger:** Use after an idea has a reasonably specific problem hypothesis and before major solution commitment.
- **Exclusion:** Do not fabricate interviews, demand, metrics or willingness-to-pay evidence.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `8c4889c9b0a067b94fe6257e98608c4588f9c9b2`
- **Markdown link targets:** none detected

### runtime-verification

- **Purpose/description:** Verify a running product and distinguish implementation claims from test, runtime, browser and production evidence. Use after implementation or whenever an agent claims something works.
- **Positive trigger:** Use after code changes, before task completion, before launch, or when a runtime issue needs evidence.
- **Exclusion:** Do not claim commands, tests, browser flows or production checks were executed unless they actually were.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `a3934d01aa674dee04ff38e10a45ba52c301d0a0`
- **Markdown link targets:** none detected

### ux-flow

- **Purpose/description:** Design or audit an end-to-end product flow including success, error, empty, loading, permission and recovery states. Use before UI implementation or when an existing flow feels incomplete.
- **Positive trigger:** Use when a concrete user goal and MVP scope exist.
- **Exclusion:** Do not turn the skill into visual styling or brand design unless explicitly requested.
- **Evidence/output safeguards:** Evidence rules, Output contract, Quality gate, Stop conditions sections present; exact text preserved only in source blob `c488f8df579a962b0ee9e01226663d190854e90f`
- **Markdown link targets:** none detected

## Workflow baseline

| Workflow file | Ordered skill references |
|---|---|
| `workflows/idea-to-mvp/workflow.yaml` | `idea-pressure-test` → `problem-validation` → `customer-research` → `market-landscape` → `icp-positioning` → `mvp-scope` |
| `workflows/idea-to-first-users/workflow.yaml` | `mvp-scope` → `ux-flow` → `architecture-plan` → `engineering-readiness` → `runtime-verification` → `launch-readiness` → `distribution-plan` → `pricing-experiment` |
| `workflows/pre-launch-audit/workflow.yaml` | `ux-flow` → `architecture-plan` → `engineering-readiness` → `runtime-verification` → `launch-readiness` |

All three workflow YAMLs use legacy unprefixed `skill:` references. Update these only in T026 after confirming mapping, preserving order and gate transitions. README/docs and other textual references remain to be audited in T027.

## Migration acceptance evidence required later

- T023: formally review exact mapping and collisions; target paths above are proposals.
- T024–T025: compare before/after skill behavior, triggers, negative triggers, Required/Optional inputs, Evidence rules, Output contract, Quality gate and Stop conditions, not merely file names.
- T026–T028: verify workflow links and gate transitions, then record parity results with exact source/target hashes; currently **NOT VERIFIED**.
