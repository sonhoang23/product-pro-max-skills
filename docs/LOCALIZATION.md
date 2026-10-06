# Localization

## Strategy

English is the canonical source for skill logic.

Do not maintain a translated copy of every `SKILL.md` in the MVP. That creates logic drift and multiplies review cost.

Instead:

1. Keep canonical behavior in English.
2. Require skills to respond in the user's requested language.
3. Keep stable terminology mappings under `locales/`.
4. Translate user-facing documentation where it adds value.
5. Add source revision metadata if full-document translations expand later.

## Stable machine terms

Do not translate machine-facing enum values such as:

`pass`, `warn`, `fail`, `provided`, `observed`, `researched`, `measured`, `inferred`, `assumed`.

Translate labels shown to users, not contract semantics.
