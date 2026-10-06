# Product Pro Max Skills

<p align="center"><strong>From vibe to viable.</strong></p>

<p align="center">
  An open-source, evidence-driven product system for AI-native builders.
</p>

<p align="center">
  <a href="./README.vi.md">Tiếng Việt</a> ·
  <a href="./CONTRIBUTING.md">Contributing</a> ·
  <a href="./CONSTITUTION.md">Constitution</a>
</p>

## Why

AI can turn an idea into deployed software in hours. That does not mean the software solves a real problem, is safe to operate, is usable, or can reach customers.

Product Pro Max Skills helps builders move from:

**Idea → Evidence → Decision → Product → Verification → Distribution → Users → Revenue → Learning**

instead of:

**Idea → Prompt → Code → Deploy**

The system is intentionally opinionated:

- evidence before confidence;
- verification before "done";
- users before features;
- distribution as part of the product;
- STOP, PIVOT and DEFER are valid outcomes.

## MVP

The MVP ships 13 composable Agent Skills:

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

Three workflows compose those skills:

- `workflows/idea-to-mvp`
- `workflows/pre-launch-audit`
- `workflows/idea-to-first-users`

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

A generated document is not progress by itself. Progress exists when the artifact changes a decision and the evidence behind that decision is visible.

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

**MVP / v0.1 foundation.** Useful > large.

## License

MIT.
