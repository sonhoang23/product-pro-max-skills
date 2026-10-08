# Quickstart / Verification Plan (future implementation)

**Current state**: Planning only. Commands below are proposed interface targets; do **not** treat them as available until related tasks are implemented.

1. Inspect approved local HTML showcase and token roles. Default is Signal Lime + Signal Path/Wordmark. The approved concept is not a substitute for production visual QA.
2. Implement and check `design-system/tokens.json` and `scripts/verify_design_system.py`:

   ```bash
   python scripts/verify_design_system.py --check-tokens
   ```

3. Generate standalone CSS snapshots / brand SVG variants with the planned deterministic exporter:

   ```bash
   python scripts/export_design_tokens.py --check
   python scripts/export_design_tokens.py --surface diagram --theme light --output /tmp/diagram-style.css
   ```

4. Adapt one **copy** of the Spec 002 relationship diagram using existing `diagram-design-vi`; verify semantic inventory against pre-migration HTML and links against Atlas/ledger.
5. Verify static invariants (against actual checkout):

   ```bash
   python scripts/verify-diagram-atlas.py
   python scripts/verify-diagram-layout.py
   python .agents/skills/diagram-design-vi/scripts/self_check.py <pilot-html>
   ```

   Check the actual supported `self_check.py` CLI before invoking; this line is a target form, not a confirmed argument contract.

6. Verify browser/visual: Light + Dark + accent preview; 390px and desktop widths; 200% zoom; accessible names/keyboard focus; reduced-motion; offline `file://`; GitHub README `picture` output. Record screenshots and any failures.
7. Re-run all validators after Atlas/registry link changes. Report static/browser/GitHub reviews separately and keep rollback copy until passed.
8. After implementation and verification, promote *implemented* design guidance to project docs; preserve Product Model/Skill Registry unchanged.

**Acceptance**: See SC-001–SC-007 in `spec.md`, risk coverage in `plan.md`, and task IDs in `tasks.md`. Do not tick implementation tasks from this planning work.
