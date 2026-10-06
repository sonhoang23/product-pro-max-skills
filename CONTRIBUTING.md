# Contributing

## Before proposing a skill

Open a Skill Proposal and answer:

- What problem does this solve?
- Who encounters it and when?
- Why is an existing skill insufficient?
- What decision or outcome improves?
- What evidence should the skill consume or produce?
- How can quality be evaluated?
- What are the stop conditions?

## Quality checklist

- [ ] narrow scope
- [ ] explicit trigger and non-trigger
- [ ] required/optional inputs
- [ ] ordered workflow
- [ ] evidence rules
- [ ] output contract
- [ ] quality gate
- [ ] stop conditions
- [ ] anti-patterns
- [ ] example
- [ ] no duplicated responsibility
- [ ] localization impact considered

Run:

```bash
python scripts/validate_repo.py
python scripts/install.py --target .tmp-skills --all --dry-run
```

English is canonical for skill logic. Documentation translations should not fork business logic.
