# SESSION.md — Current State

Overwritten at every session close. Read at every session open.
Last updated: 2026-04-08 · Session focus: W14-16 question enhancement (storytelling, deep learning, diagrams)

## Completed This Session

* [x] **W14-16 Question Enhancement (all 6 questions)**
  - Storytelling narratives: EMC shielding (Q1), autonomous vehicle radar (Q2), IoT antenna review (Q3), industrial sensor (Q4), 5G campus deployment (Q5), EV wireless charging (Q6)
  - 14 new auto-graded parts: 8 conceptual MCQs + 4 numerical + 2 hybrid
  - Follow-through grading (P-STACK-26) on cascading new parts (Q1 prt6, Q3 prt9, Q5 prt7)
  - All PATTERNS.md constraints verified (P-STACK-08/09 HARD-GATE passed for all 6 questions)
  - Points: 8 → 10 per question (48 → 60 total)

* [x] **Teaching Diagrams (6 TikZ diagrams)**
  - Created `.tex` + `.svg` in `weekly/week14_16/diagrams/`
  - Compiled via `pdflatex` + `dvisvgm --pdf` (pdf2svg not available, dvisvgm works)
  - Embedded in XML via `@@PLUGINFILE@@` + base64 `<file>` elements
  - Answer-leaking "Key insight" boxes removed after review (P-STACK-31 added)

* [x] **Hint System Overhaul**
  - 18 progressive hints rewritten (formula reminders → learning scaffolds)
  - Format hints added to all numerical/algebraic inputs
  - Syntaxhint values standardized to safe non-answer examples (P-STACK-32 added)
  - Standard example vocabulary defined by unit type (metres=0.234, ohms=42.0, ratio=0.29, etc.)

* [x] **New PATTERNS.md entries**
  - P-STACK-31: Diagram annotations must not reveal question answers
  - P-STACK-32: Syntaxhint/format hint values must not match any variant answer

* [x] **Memory saved**
  - `feedback_question_enhancement_spec.md` — reusable spec for enhancing any STACK question
  - `project_course_structure.md` — full 4-module course structure, learning outcomes, student demographics

* [x] **Committed and pushed**: `b0c20f8` on main (18 files, +1977 lines)

## Manual Review Items (carried forward)

* [ ] **Exam Q1 V3/V4 PRT grading bug** — pre-existing, needs Moodle testing
* [ ] **Q2 unit checking validation** — needs Moodle import + test
* [ ] **Pre-existing Check 4 failures (5)** — algebraic inputs missing insertstars=1
* [ ] **Pre-existing Check 5 failures (13)** — bare `<` outside CDATA in feedbackvariables
* [ ] **Moodle re-import needed** — all modified W14-16 XML files (diagrams included)

## Next Session — Planned Work

**Priority 1: Second mid-term exam**
  - Scope: likely covers Modules 3-4 (Weeks 10-16: magnetics, induction, coupled circuits, transmission lines, waves, antennas, link budgets)
  - Design decisions needed: number of pools, difficulty tiers, time allocation, essay vs STACK split
  - Apply Question Design Protocol (CLAUDE.md §8): spec gate → error model → PRT tree → parameters → coverage
  - Apply enhancement spec from memory (storytelling, conceptual parts, hints)

**Priority 2: First final exam planning**
  - Scope: full course (Modules 1-4, Weeks 2-16)
  - Start with coverage matrix: which topics are already assessed (midterm 1 + weekly), which need final exam coverage
  - Design decisions: comprehensive vs focused, cumulative weight

## In Progress (carried forward)

Task: Weeks 10-12 audit fixes (deferred from prior sessions)
Known issues:
  - Week 10 Q4: `{@ans2@}` and `{@ans3@}` in specificfeedback (P-STACK-03)
  - Week 10 Q1: Float literal `1e-7` in questionvariables (P-STACK-06)
  - All weeks 10-12: Missing `<hint>` blocks (15 questions)

Task: Progressive hint unlocking
Last state: Not started
Next step: Research STACK `[[if test="..."]]` conditional blocks

## Open Decisions / Blockers (carried forward)

* [ ] **Exam Q1 V3/V4 correct answer** — needs course content review
* [ ] **Extend units checking** beyond Q2 pilot?
* [ ] **Coverage gaps: weeks 11-12** — missing Q slots
* [ ] **Second midterm scope and structure** — needs Cássia's input
* [ ] **Final exam format** — comprehensive or focused? Essay weight?

## Patterns Triggered This Session

| Pattern ID | What happened | Action |
|------------|--------------|--------|
| P-STACK-12 | Diagram annotations + syntaxhint values leaked answers | Fixed: removed insight boxes, standardized examples |
| P-STACK-23 | All new MCQs checked for random_permutation() | Applied to all 10 new MCQ options |
| P-STACK-26 | Cascading answers in new parts (Q1 f←d, Q3 i←e, Q5 g←c) | Follow-through grading implemented |
| P-STACK-08 | All 49 PRTs (35 existing + 14 new) traced | All chains terminate at -1 |
| P-STACK-09 | All variants verified for 6 questions (29 total) | No degenerate cases |
| **NEW** P-STACK-31 | Diagram "Key insight" boxes revealed MCQ answers | **Rule added** — diagrams must not state conclusions |
| **NEW** P-STACK-32 | Syntaxhint values matched variant answers exactly | **Rule added** — standardize safe examples by unit type |

## Skills Used This Session

* [x] context-evaluator (session open/close)
* [x] stack-xml-generator (question enhancement)
* [ ] stack-question-validator (manual validation performed — formal validator not invoked)
* [x] circuitikz-circuit-diagrams (Q6 equivalent circuit)

## Compilation Notes

- `pdflatex` available at `/c/Users/z116447/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`
- `pdf2svg` NOT in PATH (user says it should be — check next session)
- `dvisvgm` available and works as alternative: `dvisvgm --pdf input.pdf -o output.svg --no-fonts`
- Python at `/c/Users/z116447/AppData/Local/Programs/Python/Python313/python.exe` (not `python` in bash PATH)
- CircuiTikZ + `every node/.style={font=\sffamily}` causes infinite recursion — use `circuitikz` as top environment, not nested inside `tikzpicture`
