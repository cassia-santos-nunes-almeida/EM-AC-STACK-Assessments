# SESSION.md — Current State

Overwritten at every session close. Read at every session open.
Last updated: 2026-04-08 · Session focus: Midterm 2 planning + Q1-Q5 XML authoring

## Completed This Session

* [x] **Prompt refinement** — Improved the second midterm exam brief from rough notes to a structured working brief with all parameters confirmed
* [x] **AI-resistance research** — Consensus, ERIC, ASEE PEER, web searches. Key findings: AI 49% on EM, 56% on crucial images, 45.7% on MCQ-MA
* [x] **Exam blueprint design** — 5 questions (2M+3H), 50 pts, 180+30 min, 4 variants each, per-question companion uploads
* [x] **Q1 — Magnetic Circuit + Faraday Induction (Medium, 9 pts)**
  - Generator: `exams/midterm2-week18/scripts/generate_q1.py`
  - XML: `exams/midterm2-week18/xml/pool_q1_medium.xml` (1949 lines, 4 variants + essay)
  - 4 topology variants: E-core, C-core, toroid, rectangular core
  - MCQ-MA debug task, essay qualitative analysis
  - 16 PRTs validated (P-STACK-08), P-STACK-32 verified
* [x] **Q2 — RLC Transient + Waveform Debug (Medium, 9 pts)**
  - Generator: `exams/midterm2-week18/scripts/generate_q2.py`
  - XML: `exams/midterm2-week18/xml/pool_q2_medium.xml` (1730 lines, 4 variants + essay)
  - 4 topology variants: series underdamped, parallel overdamped, series critically damped, parallel underdamped
  - MCQ-MA waveform debug, essay parameter sensitivity
  - 20 PRTs validated, P-STACK-32 verified
* [x] **Q3 — Coupled Circuits + Transformer Design (High, 10 pts)**
  - Generator: `exams/midterm2-week18/scripts/generate_q3.py`
  - XML: `exams/midterm2-week18/xml/pool_q3_high.xml` (1557 lines, 4 variants + essay)
  - 4 variants: aiding/opposing dots, different core types
  - Dot convention MCQ (interim — upgrade to drag-and-drop when diagrams ready)
  - Energy calculation with sign from dot convention
  - 16 PRTs validated, P-STACK-32 verified
* [x] **Q4 — TL Transient + Bounce Diagram (High, 10 pts)**
  - Generator: `exams/midterm2-week18/scripts/generate_q4.py`
  - XML: `exams/midterm2-week18/xml/pool_q4_high.xml` (1634 lines, 4 variants + essay)
  - 4 variants: R_L > Z0, R_L < Z0, short circuit, open circuit
  - QWT design essay
  - 24 PRTs validated, P-STACK-32 verified
* [x] **Q5 — EM Wave Propagation + Link Budget (High, 12 pts)**
  - Generator: `exams/midterm2-week18/scripts/generate_q5.py`
  - XML: `exams/midterm2-week18/xml/pool_q5_high.xml` (1732 lines, 4 variants + essay)
  - 4 scenarios: GPR, Wi-Fi through wall, IoT through soil, satellite through roof
  - V3 fixed: replaced VLF submarine (Friis near-field violation P-STACK-27) with 433 MHz IoT
  - MCQ-MA with AI-trap (frequency change affects α and FSPL differently)
  - 24 PRTs validated, P-STACK-32 verified
* [x] **Integration validation**
  - 20 STACK variants + 5 companion essays = 25 questions total
  - 100 PRTs, all chains terminate at -1 (P-STACK-08 HARD-GATE)
  - 50 points total, 8602 lines XML
  - P-STACK-03/06/10/23/32 all pass
* [x] **Settings fix** — Added wildcard Write/Edit/Bash permissions to `.claude/settings.json` for background agent compatibility
* [x] **Memory saved** — `project_midterm2_blueprint.md` with confirmed decisions
* [x] **Plan saved** — `.claude/plans/enumerated-cuddling-rabbit.md`

## Next Session — Remaining Work

**Priority 1: Diagrams (CircuiTikZ/TikZ)**
- 20 variant diagrams needed across Q1-Q5
- Q1: 4 core topology diagrams (E-core, C-core, toroid, rectangular)
- Q2: 4 circuit diagrams + 4 "wrong waveform" TikZ plots
- Q3: 4 physical winding diagrams (for dot convention)
- Q4: 4 TL system diagrams
- Q5: 4 multi-segment signal path diagrams
- Compile via pdflatex + dvisvgm, embed as `<file>` elements

**Priority 2: JSXGraph for Q4**
- Adapt W13 Q5 bounce diagram pattern for Q4 interactive
- 4 variants with different load types

**Priority 3: Q3 drag-and-drop upgrade**
- Convert part (a) from dropdown MCQ to Moodle drag-and-drop onto image
- Requires compiled winding diagrams with drop zone coordinates

**Priority 4: Moodle import + testing**
- Import all 5 XMLs to test Moodle instance
- Verify STACK grading, essay rendering, companion uploads
- Test file upload (P-STACK-25: "Allow attachments" setting)

**Priority 5: Instructor solve-through**
- Time budget validation (~160 min working target)
- Verify answer key correctness against Ulaby/Nilsson

**Priority 6: Save handover to Notion**
- Local handover at `exams/midterm2-week18/HANDOVER_2026-04-08.md` — needs to be posted to Notion
- Reconnect Notion MCP server first, then create the page
- Alternatively: copy-paste manually into Notion

## Open Decisions / Blockers

* [ ] Diagram style: match existing weekly question style or new exam style?
* [ ] Q5 all variants are quasi-conductor — acceptable or need one low-loss/good-conductor?
* [ ] Test background agent Write permissions with new settings before next large authoring session

## Patterns Triggered This Session

| Pattern ID | What happened | Action |
|------------|--------------|--------|
| P-STACK-08 | All 100 PRTs traced across 20 variants | All chains terminate at -1 |
| P-STACK-09 | All 20 variants computed and verified | No degenerate cases |
| P-STACK-23 | All MCQ/checkbox options use random_permutation() | Applied in all generators |
| P-STACK-27 | V3 of Q5 had near-field Friis violation (VLF, λ=30km, R=100m) | Replaced with 433 MHz IoT scenario |
| P-STACK-32 | Multiple syntaxhint values initially matched answers | Fixed iteratively for all 5 questions |
| P-EXEC-01 | 5 questions decomposed into phases before execution | Executed with task tracking |

## Skills Used This Session

* [x] context-evaluator (session open/close)
* [x] stack-xml-generator (exam question XML authoring via Python generators)
* [ ] circuitikz-circuit-diagrams (deferred to next session for diagram compilation)
* [ ] stack-question-validator (automated validation via Python scripts instead)

## Compilation Notes (carried forward)

- `pdflatex` at `/c/Users/z116447/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex`
- `dvisvgm` available: `dvisvgm --pdf input.pdf -o output.svg --no-fonts`
- Python at `/c/Users/z116447/AppData/Local/Programs/Python/Python313/python.exe`
- CircuiTikZ + `every node/.style={font=\sffamily}` causes infinite recursion — use `circuitikz` as top environment
