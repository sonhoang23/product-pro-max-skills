# Product Pro Max Skills

<p align="center"><strong>From vibe to viable.</strong></p>

<p align="center">
  An open-source, evidence-driven product operating system for AI-native builders.
</p>

<p align="center">
  <a href="./README.vi.md">Tiếng Việt</a> ·
  <a href="./CONTRIBUTING.md">Contributing</a> ·
  <a href="./CONSTITUTION.md">Constitution</a>
</p>

## Why

AI can turn an idea into deployed software in hours. That does not mean the software solves a real problem, is safe to operate, is usable, can reach customers, retain them, or become a viable business.

Product Pro Max Skills helps builders move from:

**Idea → Evidence → Decision → Product → Verification → Distribution → Users → Revenue → Learning**

instead of:

**Idea → Prompt → Code → Deploy**

The system is intentionally opinionated:

- evidence before confidence;
- verification before "done";
- users before features;
- distribution is part of the product;
- learning continues after launch;
- STOP, PIVOT, DEFER and BACKTRACK are valid outcomes.

## Product operating model

Product Pro Max is not designed as a linear checklist and not as a loose collection of prompts.

It is a product operating system organized around five structural layers:

```text
PRODUCT LIFECYCLE
    ↓
CYCLES
    ↓
PHASES
    ↓
LOOPS
    ↓
GATES / DECISIONS
```

Cross-cutting **tracks** allow product, engineering, UX, research, data, marketing, growth, sales, revenue and operations work to progress in parallel.

The goal is to make the full path from idea to viable product explicit, evidence-driven and reversible where uncertainty remains.

## Product lifecycle

The full lifecycle is broader than software delivery:

```text
IDEA
 ↓
DISCOVER
 ↓
VALIDATE
 ↓
STRATEGIZE
 ↓
DEFINE
 ↓
DESIGN
 ↓
PLAN
 ↓
BUILD
 ↓
VERIFY
 ↓
LAUNCH
 ↓
ACQUIRE
 ↓
ACTIVATE
 ↓
MONETIZE
 ↓
RETAIN
 ↓
EXPAND
 ↓
OPERATE
 ↓
LEARN
 ↓
SCALE / PIVOT / MAINTAIN / SUNSET
```

A project does not need to execute every phase. The lifecycle is a map, not a mandatory waterfall.

### Lifecycle cycles

| Cycle | Purpose |
| --- | --- |
| Opportunity | Explore ideas, problems and evidence worth pursuing |
| Product Strategy | Decide market, customer, positioning, business model and strategic constraints |
| Product Definition | Define scope, requirements, experience and measurement |
| Delivery | Design technically, plan implementation and build |
| Verification | Verify product behavior, runtime reality, security, reliability and usability |
| Go-to-Market | Prepare launch, distribution and controlled exposure |
| Growth | Acquire, activate, monetize, retain, refer and expand |
| Operations | Operate, support, monitor, optimize and maintain the product |
| Learning & Evolution | Review evidence, revise strategy and decide the next product bet |
| End-of-Life | Deprecate, migrate or sunset safely when appropriate |

Cycles group related phases around a larger product objective.

## Phases

A phase represents a meaningful state of product work, not merely a document to generate.

Examples include:

```text
Discovery
Validation
Positioning
Business Model
Scope
Requirements
Experience Design
Measurement Design
Technical Design
Implementation Planning
Build
Integration
Product QA
Runtime Verification
Security & Reliability
UX Validation
Launch Preparation
Distribution
Acquisition
Activation
Engagement
Monetization
Retention
Referral
Expansion
Product Operations
Optimization
Maintenance
Evidence Review
Strategy Review
Portfolio Decision
Deprecation
Migration
Sunset
```

Each phase may use one or more skills, produce artifacts, collect evidence and end in a gate.

## Core model

Every useful step should move through the same primitives:

```text
SKILL
  ↓
ARTIFACT
  ↓
EVIDENCE
  ↓
GATE
  ↓
DECISION
```

A generated document is not progress by itself. Progress exists when an artifact changes a decision and the evidence behind that decision is visible.

For experimentation-heavy work, the model can extend to:

```text
ASSUMPTION
   ↓
HYPOTHESIS
   ↓
EXPERIMENT
   ↓
EXPOSURE
   ↓
MEASUREMENT
   ↓
EVIDENCE
   ↓
GATE
   ↓
DECISION
```

## Loops

Product development is not linear. Loops turn evidence into repeated learning.

The operating model currently recognizes these high-level loops:

| Loop | Core motion |
| --- | --- |
| Evidence Loop | Assumption → Research → Evidence → Decision → New assumption |
| Discovery Loop | Problem → Research → Hypothesis → Prototype → Feedback |
| Delivery Loop | Define → Design → Plan → Build → Verify → Fix |
| Experiment Loop | Observation → Hypothesis → Experiment → Measurement → Decision |
| Growth Loop | Acquire → Activate → Retain → Monetize → Refer |
| GTM Loop | ICP → Message → Channel → Exposure → Response → Revision |
| Revenue Loop | Value → Offer → Pricing → Purchase → Usage → Expansion |
| Reliability Loop | Observe → Detect → Respond → Recover → Prevent |
| Strategy Loop | Product evidence → Market evidence → Revenue evidence → Strategic bet |

Loops can cross multiple phases and multiple cycles.

## Tracks

A product can have several disciplines moving at the same time.

Product Pro Max models these as cross-cutting tracks such as:

```text
Product
Engineering
UX
Research
Data
Marketing
Growth
Sales
Revenue
Operations
Security
Support
```

For example, a Launch cycle may involve:

```text
Product Track      → launch scope
Engineering Track  → production readiness
Data Track         → analytics verification
Marketing Track    → messaging and campaign preparation
Growth Track       → acquisition experiments
Support Track      → support readiness
```

A launch gate can then combine evidence across all relevant tracks.

## Nested lifecycles

The product itself is not the only thing with a lifecycle.

Features, experiments, campaigns, pricing changes and other product bets can run their own smaller lifecycle inside the main product lifecycle:

```text
PRODUCT
├── Product lifecycle
├── Feature lifecycle
├── Experiment lifecycle
├── Campaign lifecycle
└── Pricing-change lifecycle
```

A typical nested lifecycle may look like:

```text
Opportunity
→ Evidence
→ Decision to explore
→ Definition
→ Build
→ Verify
→ Release
→ Measure
→ Learn
→ Keep / Improve / Rollback / Remove
```

This allows long-running AI agents and product teams to reason about both the whole product and individual bets without losing context.

## Gates and decisions

A phase does not automatically advance to the next phase.

Workflows may produce decisions such as:

```text
PASS
WARN
FAIL
PIVOT
REPEAT
BACKTRACK
DEFER
STOP
ESCALATE
```

Example:

```text
Problem Validation
     │
     ├── PASS → Positioning
     ├── WARN → More customer research
     ├── FAIL → Stop
     └── PIVOT → Discovery
```

The lifecycle is therefore closer to an evidence-driven state machine than a checklist.

## Current foundation

The current v0.1 foundation ships 13 composable Agent Skills:

| Stage | Skill | Outcome |
| --- | --- | --- |
| Discover | `idea-pressure-test` | Expose assumptions, risks and unknowns before building |
| Validate | `problem-validation` | Decide whether the problem has enough evidence |
| Validate | `customer-research` | Turn customer conversations into traceable evidence |
| Validate | `market-landscape` | Map direct competitors, substitutes and do-nothing |
| Define | `icp-positioning` | Define a specific ICP and positioning |
| Define | `mvp-scope` | Cut scope to the smallest test of the critical hypothesis |
| Design | `ux-flow` | Cover happy, error, empty, loading and recovery paths |
| Build | `architecture-plan` | Make proportionate architecture decisions with trade-offs |
| Build | `engineering-readiness` | Check security, testing, observability, migration and rollback |
| Verify | `runtime-verification` | Separate implemented, tested and runtime-verified claims |
| Launch | `launch-readiness` | Produce PASS/WARN/BLOCK launch evidence |
| Launch | `distribution-plan` | Turn ICP into concrete channels, messages and experiments |
| Revenue | `pricing-experiment` | Test pricing hypotheses instead of guessing a price |

Three workflows currently compose those skills:

- `workflows/idea-to-mvp`
- `workflows/pre-launch-audit`
- `workflows/idea-to-first-users`

These are the starting implementation, not the final boundary of the Product Pro Max lifecycle.

## Install

The repository uses `SKILL.md` as the canonical skill format.

```bash
git clone https://github.com/sonhoang23/product-pro-max-skills.git
cd product-pro-max-skills
python scripts/install.py --target /path/to/project/.agents/skills --all
```

Install selected skills:

```bash
python scripts/install.py \
  --target /path/to/project/.agents/skills \
  --skills problem-validation,mvp-scope,runtime-verification
```

Preview without writing:

```bash
python scripts/install.py --target .agents/skills --all --dry-run
```

## Use

Ask naturally:

```text
I want to build an AI meeting notes SaaS. Pressure-test the idea before we write code.
```

Or invoke a skill explicitly:

```text
Use problem-validation. Separate evidence from assumptions and stop if the gate fails.
```

## Project state

For long-running projects, keep durable product state outside chat history:

```text
.product-pro-max/
├── project.yaml
├── assumptions.yaml
├── evidence/
├── decisions/
├── artifacts/
└── passport.md
```

Templates live in `templates/project-state/`.

## Quality bar

A skill is not accepted because its advice sounds smart. It must define scope, trigger, inputs, workflow, evidence rules, output contract, quality gate, stop conditions, anti-patterns and examples.

See `SKILL-CONTRACT.md`, `EVIDENCE-MODEL.md` and `QUALITY-GATES.md`.

## Repository structure

```text
skills/       Canonical Agent Skills
workflows/    Composed product lifecycle workflows
schemas/      Machine-readable contracts
templates/    Durable project-state templates
examples/     End-to-end examples
locales/      Stable terminology for localization
docs/         Architecture and localization guidance
scripts/      Dependency-free installer and validation
.github/      CI and contribution templates
```

## Language

English is canonical for skill logic. User-facing output should follow the user's preferred language. Vietnamese is supported from the first release.

## Status

**MVP / v0.1 foundation.**

The repository currently implements the first slice of the operating model. Future versions will deepen lifecycle coverage, add more phases, loops, tracks and composed workflows while preserving the same evidence-driven architecture.

## License

MIT.
