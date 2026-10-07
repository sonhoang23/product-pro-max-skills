# Quickstart: Updating the Product Model

1. Start with `model/product-model.json`; do not introduce canonical lifecycle IDs only in prose or a dependent schema.
2. Keep each phase under exactly one cycle.
3. Keep tracks and loops outside the sequential phase list.
4. Keep `pass|warn|fail` as gate results; next-action concepts belong to decisions.
5. Update dependent schemas/templates when the canonical model changes.
6. Promote human documentation only after machine contracts align.
7. Run:

```bash
python scripts/validate_repo.py
python scripts/install.py --target .tmp-skills --all --dry-run
```

A Product Model change is not complete while validation reports ontology drift.
