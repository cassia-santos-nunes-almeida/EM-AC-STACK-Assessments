# SESSION.md — Current State

Overwritten at every session close. Read at every session open.
Last updated: 2026-03-22 · Session focus: JSXGraph Q5 fix + Week 13 audit + context file migration

## Completed This Session

* [x] Fixed Week 13 Q5 JSXGraph bounce diagram — 3 bugs (snap, table, grading)
  - Merged unmerged fix branch `claude/open-session-7TDcM` into main
  - Fixed `snapToGrid: true` → `snapSizeX: 1, snapSizeY: 0.25`
  - Reduced SNAP from 0.5 to 0.25
  - Added `stack_jxg.custom_bind` fallback guard for older STACK versions
* [x] Audited all 15 weekly questions (weeks 10-13) against PATTERNS.md rules
* [x] Fixed Week 13 Q1-Q4 issues:
  - Q1: Standardized 3 syntax hints (ans1, ans2, ans5)
  - Q2: Fixed float literal `1e-12` → `1/10^12` (P-STACK-06)
  - Q3: Added "Syntax hint:" prefix to 4 dropdown/radio/notes hints
  - Q4: Added missing syntax hint for dropdown ans5
* [x] Context file migration (Phases 1-3 per analysis.md):
  - CLAUDE.md: 465 → 178 lines (eliminated 19 duplications)
  - context.md: Updated tree, added weeks 11-13 summaries
  - circuitikz/SKILL.md: Absorbed multi-switch topology + diagram style
  - stack-xml-generator/SKILL.md: Added JSXGraph Integration section
  - Created `references/jsxgraph-conventions.md`
  - decisions-log.md: Added 3 catch-up entries
  - personal-preferences.md: Cleaned placeholder comment
* [x] Added P-STACK-21 and P-DIAG-08 to PATTERNS.md

## In Progress

Task: Week 13 Q5 — user reported a new problem (not yet described)
Last state: User mentioned finding a new issue during session close
Next step: Open next session, ask user to describe the new problem

Task: Weeks 10-12 audit fixes (deferred)
Last state: Issues identified but deferred per user request
Next step: Fix when working on those weeks
Known issues:
  - Week 10 Q4: `{@ans2@}` and `{@ans3@}` in specificfeedback (P-STACK-03)
  - Week 10 Q1: Float literal `1e-7` in questionvariables (P-STACK-06)
  - All weeks 10-12: Missing `<hint>` blocks (15 questions)

Task: Progressive hint unlocking
Last state: Not started
Next step: Research STACK `[[if test="..."]]` conditional blocks

## Open Decisions / Blockers

* [ ] **New Q5 problem** — user found another issue, not yet described
* [ ] **Progressive hints for exams?** — TBD

## Patterns Triggered This Session

| Pattern ID | Triggered? | Applied? |
|------------|-----------|----------|
| P-DIAG-08 | Created this session | N/A (new) |
| P-STACK-21 | Created this session | N/A (new) |
| P-STACK-06 | Triggered by Q2 float literal | Applied |
| P-STACK-11 | Triggered by missing syntax hints | Applied |
| P-EXEC-01 | Followed for migration decomposition | Applied |

## PATTERNS.md Updates This Session

* **Added:** P-STACK-21 — Use `snapSizeX`/`snapSizeY` instead of `snapToGrid`
* **Added:** P-DIAG-08 — Always merge fix branches before importing to Moodle

## Skills Used This Session

* [x] context-evaluator
* [ ] circuitikz-circuit-diagrams
* [x] stack-xml-generator (referenced for dedup)

## Notes for Next Session

- User found a NEW problem in Week 13 Q5 — investigate first
- Migration complete (analysis.md fully executed). Those files can be archived.
- Weeks 10-12 have known audit issues — tackle when in scope
- New CLAUDE.md (178 lines) + session-open now includes personal-preferences.md as step 5
