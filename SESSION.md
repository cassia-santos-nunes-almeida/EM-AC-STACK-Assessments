# SESSION.md — Current State

Overwritten at every session close. Read at every session open.
Last updated: 2026-04-07 · Session focus: Quality improvements — validator, MCQ shuffle, coverage matrix

## Completed This Session

* [x] **Action 1 — Context migration completion**
  - Added STACK_XML_Generator browser tool to CLAUDE.md §7 Skill Index (URL: stack-xml-generator.vercel.app)
  - Updated PATTERNS.md reference from P-STACK-20 to P-STACK-23
  - Added catch-up decisions-log entries for sessions 6-9 (2026-03-10 to 2026-03-22)
  - Verified all 39 migration items, 19 duplications resolved, 13 orphaned items preserved
  - CLAUDE.md at 200 lines (target: ≤200)

* [x] **Action 2 — PRT chain validator** (`shared/validate_stack_xml.py`)
  - 9 checks: PRT chains, answer tests, MCQ shuffle, insertstars, CDATA, base64, names, exact arithmetic, handwritten companions
  - Self-test with inline known-good XML passes before every run
  - CLI: `--all`, `--exams-only`, single file, directory modes
  - Initial report: 49 FAIL, 167 WARN, 208 PASS across 21 files

* [x] **Action 3 — MCQ shuffle retroactive fix**
  - Applied `random_permutation()` to 31 MCQ inputs across 13 files (exams + weeks 10-12)
  - Handled conditional option list in Q3_CouplingCoefficient (per-branch wrapping)
  - Handled `is()` expression options in Q5_ParallelRLC (manual fix, regex missed it)
  - Final report: 0 Check 3 failures remaining
  - Commit: `30d2263`

* [x] **Action 4 — §8 Question Design Protocol in CLAUDE.md**
  - Pre-XML spec gate: 5 required items before any XML generation
  - Exam companion decision gate: ask once per session about handwritten notes

* [x] **Action 5 — Coverage matrix** (`docs/coverage-matrix.md`)
  - 3 tables: topic × week, Bloom's × week, difficulty × week
  - Gap analysis: no recall/synthesize questions, weeks 10-12 are 100% analyze, weeks 11-12 missing 2 questions each

## Manual Review Items

* [ ] **Exam Q1 V3/V4 PRT grading bug** — `pool_q1_easy.xml` variants 3 and 4 have `true` flag at position 2 in the option list but PRT `tans` is `1`. The PRT grades value 1 as correct, but the option list marks value 2 as correct. These disagree. Not introduced by this session — pre-existing. Needs manual Moodle testing to determine which is actually correct.

* [ ] **Q2 unit checking validation** — Q2 converted to STACK `units` type in prior session. Needs Moodle import + test before extending to other questions.

* [ ] **Pre-existing Check 4 failures (5)** — algebraic inputs missing `insertstars=1`:
  - exam Q3 (4 variants): `pool_q3_medium_b.xml` (algebraic inputs for transfer functions)
  - week13 Q5: `Q5_BounceDiagram_Transient.xml` ans6 (JSXGraph hidden input — `insertstars` not relevant for hidden inputs)

* [ ] **Pre-existing Check 5 failures (13)** — bare `<` outside CDATA in feedbackvariables:
  - `Q3_Toroid` (2), `Q4_MagneticCircuit` (5), `Q5_ParallelRLC_Switches` (1), week11 Q1 (1), week11 Q2 (1), week12 Q3 (1), week13 Q3 (1), week13 Q5 (1)
  - These work in practice (content is inside `<text>` CDATA at the outer level) but technically violate P-STACK-04 at the inner element level.

* [ ] **Moodle re-import needed** — all modified XML files need Moodle re-import (13 files from MCQ shuffle fix + 5 week 13 files from prior session)

## In Progress

Task: Weeks 10-12 audit fixes (deferred from prior session)
Known issues:
  - Week 10 Q4: `{@ans2@}` and `{@ans3@}` in specificfeedback (P-STACK-03)
  - Week 10 Q1: Float literal `1e-7` in questionvariables (P-STACK-06)
  - All weeks 10-12: Missing `<hint>` blocks (15 questions)
  - Check 4 and Check 5 failures listed above

Task: Progressive hint unlocking
Last state: Not started
Next step: Research STACK `[[if test="..."]]` conditional blocks

## Open Decisions / Blockers

* [ ] **Exam Q1 V3/V4 correct answer** — which is actually right, value 1 or value 2? Needs course content review.
* [ ] **Extend units checking** beyond Q2 pilot? Wait for Moodle test results.
* [ ] **Coverage gap: no Easy/Medium weekly questions** — intentional design or gap to fill?
* [ ] **Coverage gap: weeks 11-12 missing Q1/Q2 and Q3/Q4 respectively** — planned or skipped?

## Patterns Triggered This Session

| Pattern ID | Triggered? | Applied? |
|------------|-----------|----------|
| P-STACK-23 | MCQ shuffle check failures across weeks 10-12 and exams | Fixed — random_permutation() added to all 31 MCQ inputs |
| P-STACK-10 | 5 algebraic inputs missing insertstars=1 | Noted for manual review (not in scope) |
| P-STACK-04 | 13 bare `<` outside inner CDATA | Noted for manual review (not in scope) |

## Skills Used This Session

* [x] context-evaluator (session open/close)
* [ ] circuitikz-circuit-diagrams
* [ ] stack-xml-generator

## Recommended Focus for Session 2a (STACK_XML_Generator)

1. **Fix Check 4/5 pre-existing failures** — 5 insertstars, 13 CDATA wrapping
2. **Resolve exam Q1 V3/V4 PRT disagreement** — verify correct answer with course content
3. **Test Q2 unit checking in Moodle** — confirm units input works before extending
4. **Progressive hints** — research and implement for weekly questions
5. **Fill coverage gaps** — Easy/Medium tier questions for weeks 10-12, missing Q slots in weeks 11-12
