# Architecture

## Canonical primitives

Product Pro Max has five core primitives:

```text
Skill → Artifact → Evidence → Gate → Decision
```

### Skill

A narrow agent capability with an explicit trigger, workflow and output contract.

### Artifact

A durable output such as a validation brief, scope decision, architecture decision or runtime report.

### Evidence

Traceable support for a claim, including provenance and evidence class.

### Gate

A rule that decides whether a workflow may continue.

### Decision

A recorded outcome: continue, research, revise, pivot, defer or stop.

## Workflows

A workflow composes existing skills. Workflow files should orchestrate; they should not duplicate skill logic.

## Project state

Chat sessions are replaceable. Product state is not.

The recommended `.product-pro-max/` directory persists assumptions, evidence, decisions, artifacts, lifecycle status and a product passport.

## Agent compatibility

Canonical skills remain under `skills/<name>/SKILL.md`. Installation tooling copies those canonical skills into a target Agent Skills directory. Platform-specific adapters should transform installation layout, not duplicate skill logic.

## MVP exclusions

The MVP intentionally excludes hosted dashboards, marketplaces, autonomous long-running orchestration, framework-specific engineering packs and proprietary skill formats.
