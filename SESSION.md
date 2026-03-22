# SESSION.md — Current State

Overwritten at every session close. Read at every session open.
Last updated: 2026-03-22 · Session focus: W13 Q5 JSXGraph fix + JSXGraph lessons learned

## Completed This Session

* [x] Diagnosed W13 Q5 JSXGraph blank graph and non-functional table — root causes: `{@var@}` inside jsxgraph block, table outside IFRAME scope, missing change event dispatch
* [x] Fix round 1 (`ab10be2`): replaced `{@var@}` with `{#var#}` inside jsxgraph block
* [x] Fix rounds 2-4 (`a0ebf83`, `fd9189e`, `e859c08`, `5553800`): iterative fixes matching proven STACK patterns
* [x] Fix round 5 (`54bf594`): moved table HTML inside jsxgraph block, added `dispatchEvent(new Event('change'))` on all input writes
* [x] Fix round 6 (`a2ff85c`): complete rewrite using `stack_jxg.custom_bind` — the proper STACK pattern for complex state binding
* [x] Elevated W13 Q1/Q3/Q5 to higher Bloom's taxonomy with AI-resistant connecting parts (`8445308`)
* [x] Added JSXGraph UX enhancements and Bloom's depth to W13 (`7fd1b7c`)
* [x] Documented 5 new JSXGraph patterns in PATTERNS.md (P-STACK-16 through P-STACK-20)
* [x] All changes committed and pushed to `claude/open-session-7TDcM`

## In Progress

Task: W13 Q5 JSXGraph — awaiting user testing in Moodle
Last state: Code rewritten and pushed, not yet tested in live Moodle/STACK environment
Next step: User imports XML into STACK-enabled Moodle and verifies: (a) graph renders, (b) dragging points updates table, (c) values are submitted to STACK for grading
Relevant files: `weekly/week13/xml/` (Q5 file)

Task: Progressive hint unlocking
Last state: Not started — planned as next feature work
Next step: Research STACK `[[if test="..."]]` conditional blocks for attempt-gated hints; prototype on Week 10 Q1
Relevant files: `weekly/week10/xml/Q1_*.xml`, CLAUDE.md (§ Known Issues / Pending Work)

Task: Global CLAUDE.md migration
Last state: Audit complete, risk flags documented, awaiting decision
Next step: Decide whether to proceed with migration — 6 risk flags need resolution
Relevant files: All 3 CLAUDE.md files, `~/.claude/CLAUDE.md` (does not exist yet)

Task: Moodle sandbox import test
Last state: Blocked — no STACK-enabled Moodle instance available
Next step: Import weekly/week10-13 XML files into sandbox once access is obtained
Relevant files: `weekly/week10/xml/`, `weekly/week11/xml/`, `weekly/week12/xml/`, `weekly/week13/xml/`

## Open Decisions / Blockers

* [ ] **W13 Q5 JSXGraph testing** — Needs live Moodle/STACK test to confirm the fix works end-to-end
* [ ] **Global CLAUDE.md migration** — Proceed or defer? 6 risk flags identified
* [ ] **Moodle instance access needed** — Cannot validate XML imports without a STACK-enabled Moodle sandbox
* [ ] **Progressive hints for exams?** — Determine if attempt-gated hints are appropriate in exam context
* [ ] Q4 4th variant (RL with Thevenin reduction) — deferred
* [ ] Exam diagram migration to CircuiTikZ — lower priority

## Patterns Triggered This Session

| Pattern ID | Triggered? | Applied? |
|------------|-----------|----------|
| P-STACK-16 | Created this session | Applied in fix round 1 |
| P-STACK-17 | Created this session | Applied in fix round 5 |
| P-STACK-18 | Created this session | Applied in fix round 5 |
| P-STACK-19 | Created this session | Applied in fix round 6 |
| P-STACK-20 | Created this session | Applied in all fix rounds |

## PATTERNS.md Updates This Session

* **Added:** P-STACK-16 — Use `{#var#}` not `{@var@}` inside `[[jsxgraph]]` blocks
* **Added:** P-STACK-17 — JSXGraph runs in a sandbox IFRAME — no direct DOM access outside the block
* **Added:** P-STACK-18 — Dispatch `change` event when writing to STACK inputs manually
* **Added:** P-STACK-19 — Prefer `stack_jxg.custom_bind` for complex JSXGraph state
* **Added:** P-STACK-20 — Declare `input-ref-X` attributes on `[[jsxgraph]]` tag

## Skills Used This Session

* [ ] lut-lecture
* [ ] stack-xml-generator
* [ ] message-coach
* [ ] circuitikz-circuit-diagrams
* [x] context-evaluator
* [ ] other: ...

## Deferred: External Skill Repo Updates

These updates should be applied to the **my-claude-skill** GitHub repo when next open:

**CircuiTikZ skill** (`circuitikz-latex-circuit-diagrams`):
- circuit-patterns.md Pattern 6 switch bug: `opening switch`/`closing switch` were reversed. Fixed locally; sync to skill repo.
- Add compilation testing rule and `border=10pt` note to SKILL.md.
- Add switch semantics warning to circuitikz-guide.md.

**Context evaluator skill**: Consider adding JSXGraph integration notes to context.md.

## Notes for Next Session

- **Priority 1:** Test W13 Q5 in live Moodle/STACK — the JSXGraph rewrite needs real-environment validation.
- The 6 fix rounds for Q5 are documented in git history — if the current version still fails, check whether `stack_jxg` library is loaded (it should be automatic in `[[jsxgraph]]` blocks).
- JSXGraph lessons (P-STACK-16 through P-STACK-20) are now in PATTERNS.md — apply them to any future JSXGraph questions.
- Progressive hint unlocking is next feature task after Q5 is validated.
- Weeks 10-13 content is complete. Next content creation would be `weekly/week14/` or exam updates.
