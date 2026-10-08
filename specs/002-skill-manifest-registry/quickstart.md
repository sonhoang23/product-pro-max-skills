# Quickstart — Planned validation

**Not executed.** After implementation, use the project's pinned Python and safe YAML parser toolchain.

1. Inventory all distributable skill directories; check sibling `manifest.yaml` and matching `SKILL.md` identity.
2. Run the future registry generator twice and assert byte-identical JSON.
3. Run the future read-only checker on valid data: exit code zero and no mutation.
4. Inject separate failing fixtures: missing manifest; bad ID; duplicate slug; wrong cycle/path; invalid phase/cycle, track, skill/workflow relation; edited derived registry. Require nonzero exit and source-specific diagnostic.
5. Verify `.agents/` exclusion and that `skill-creator-vi` generates contract-conformant metadata.
6. Review migration links and compare original versus renamed skill behavior, triggers, evidence rules, outputs and responsibilities.
7. Record exact commands, versions, commit, output logs, fixture results and inventory counts. Do not claim runtime PASS from this plan.
