# Product Pro Max Skills

<p align="center"><strong>From vibe to viable.</strong></p>

<p align="center">
  An open-source, evidence-driven product operating system for AI-native builders.
</p>

<p align="center">
  <a href="./PRODUCT-MODEL.md">Product Model</a> ·
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
- STOP, PIVOT, DEFER, BACKTRACK and other evidence-driven decisions are valid outcomes.

## Canonical Product Model

Shared lifecycle semantics have one machine-readable authority:

**[`model/product-model.json`](./model/product-model.json)**

The human-readable contract is **[`PRODUCT-MODEL.md`](./PRODUCT-MODEL.md)**.

README pages, schemas, workflows, examples, diagrams, and translations are derived views. They must not invent or redefine canonical lifecycle identifiers.

The lifecycle is organized as:

```text
PRODUCT LIFECYCLE
    ↓
CYCLES
    ↓
PHASES

TRACKS     cross-cut disciplines
LOOPS      repeat learning or operating motions
GATES      judge evidence/readiness
DECISIONS  choose what happens next
```

Canonical cycles:

| Cycle | Purpose |
| --- | --- |
| Opportunity | Explore problems and evidence worth pursuing |
| Product Strategy | Choose market, customer, positioning, and business direction |
| Product Definition | Turn strategy into bounded, measurable product intent |
| Delivery | Design, plan, build, and integrate |
| Verification | Establish runtime, quality, security, reliability, and usability evidence |
| Go-to-Market | Prepare and expose the product to intended users |
| Growth | Acquire, activate, monetize, retain, refer, and expand |
| Operations | Operate, support, optimize, and maintain |
| Learning & Evolution | Review evidence and revise strategy or portfolio choices |
| End of Life | Deprecate, migrate, and sunset safely |

The complete canonical phase IDs and relationships live in the Product Model, not in this README.

## Core operating primitive

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

For experimentation-heavy work:

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

## Gates and decisions

Gate results and decisions are intentionally different.

Canonical gate results:

- `pass`
- `warn`
- `fail`

Canonical decisions include:

- `continue`
- `research`
- `revise`
- `pivot`
- `repeat`
- `backtrack`
- `defer`
- `stop`
- `escalate`

A `warn` gate, for example, might lead to `continue`, `research`, or `revise` depending on context. See [Product Model](./PRODUCT-MODEL.md).

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

These stage labels are navigation shorthand for the current MVP skill set. Canonical lifecycle phase IDs live in `model/product-model.json`.

Three workflows currently compose those skills:

- `workflows/idea-to-mvp`
- `workflows/pre-launch-audit`
- `workflows/idea-to-first-users`

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
├── project.yaml       # cycle + phase + status
├── assumptions.yaml
├── evidence/
├── decisions/
├── artifacts/
└── passport.md
```

Canonical cycle, phase, and status values come from `model/product-model.json`.

Templates live in `templates/project-state/`.

## Quality bar

A skill is not accepted because its advice sounds smart. It must define scope, trigger, inputs, workflow, evidence rules, output contract, quality gate, stop conditions, anti-patterns and examples.

See:

- [Skill Contract](./SKILL-CONTRACT.md)
- [Evidence Model](./EVIDENCE-MODEL.md)
- [Quality Gates](./QUALITY-GATES.md)
- [Product Model](./PRODUCT-MODEL.md)

Repository validation checks structural skill requirements plus canonical Product Model drift in dependent schemas/templates.

## Repository structure

```text
skills/       Canonical distributable Agent Skills
workflows/    Composed product workflows
model/        Canonical shared product semantics
schemas/      Machine-readable contracts
templates/    Durable project-state templates
examples/     End-to-end examples
locales/      Stable terminology for localization
docs/         Architecture and guidance
scripts/      Dependency-free installation and validation
specs/        Spec Kit feature work and foundation backlog
.specify/     Spec Kit project workflow state/templates
.agents/      Repository-development skills and tooling
.github/      CI and contribution templates
```

`skills/` is product surface. `.agents/` is repository-development tooling; it is not automatically part of the distributable Product Pro Max skill catalog.

## Language

English is canonical for skill logic, shared product semantics, and machine identifiers. User-facing output should follow the user's preferred language.

Machine IDs such as `go-to-market`, `runtime-verification`, `pass`, and `pivot` are not translated when used as contract values.

## Status

**MVP / v0.1 foundation.**

The repository implements the first slice of the Product Model. Later foundation specs will add skill metadata/registry, compatibility policy, broader quality evaluation, repository governance, global discovery/documentation, and release lifecycle without redefining Product Model v1 implicitly.

## License

MIT.
