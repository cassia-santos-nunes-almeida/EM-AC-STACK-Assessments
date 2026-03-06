# Active Session — STACK Exam & Practice Question Builder

## Current Milestone
**Week 10 Q1-Q5 content functional and audited. Q5 diagram needs topology fix to match Nilsson P8.11.** All questions work in STACK with correct Maxima grading. Deep audit completed (2026-03-06): fixed PRT grading issues (AlgEquiv→NumAbsolute for zero answers), converted Q3/Q4 MCQs from algebraic to dropdown, removed 8 answer-leaking syntaxhints. The Q5 circuit diagram (`q5_parallel_rlc_natural_switches.py/svg`) does not match the textbook reference — needs complete Schemdraw rewrite. After fixing, the SVG must be re-embedded as base64 in the XML.

## Pending Tasks (Prioritized)

### Q5 Diagram Fix (CRITICAL — blocks Moodle deployment)
- [ ] **Rewrite `weekly/week10/diagrams/q5_parallel_rlc_natural_switches.py`** — Current layout has L horizontal and R labeled on a horizontal wire. Must match Nilsson Figure P8.11 topology where L and R are both VERTICAL between top/bottom rails. User to provide reference image for exact topology.
- [ ] **Regenerate SVG** — Run the rewritten .py script
- [ ] **Re-embed base64 SVG in XML** — Update `weekly/week10/xml/Q5_ParallelRLC_NaturalResponse_Switches.xml`

**Key issue:** The exact component arrangement (which components are vertical vs horizontal, switch positions, Rb placement) needs to match the Nilsson P8.11 figure. Two previous rewrite attempts didn't match — user has the reference image.

**Files involved:**
- `weekly/week10/diagrams/q5_parallel_rlc_natural_switches.py` (Schemdraw source)
- `weekly/week10/diagrams/q5_parallel_rlc_natural_switches.svg` (generated output)
- `weekly/week10/xml/Q5_ParallelRLC_NaturalResponse_Switches.xml` (contains base64-embedded SVG)

**Circuit components (Nilsson P8.11):**
- Is (current source, 5A), Ra (250Ω), L (160 mH), R (50Ω) with vo(t), C (25μF), Rb (75Ω), Vdc (100V)
- Two SPDT switches: sw1 (a/b) and sw2 (c/d), operating synchronously at t=0
- Before t=0: sw1=a (L connected to Is/Ra), sw2=d (C connected to Rb/Vdc)
- After t=0: sw1=b, sw2=c → L, R, C in parallel (natural response)

## Completed Tasks

### Session Updates (2026-03-06)
- [x] Base64 SVG auto-embedding for all Q1-Q5 weekly questions
- [x] Converted radio MCQs to dropdown (type="dropdown") — no more "Clear my choice"
- [x] Two attempts at Q5 diagram rewrite (still doesn't match reference)
- [x] **Deep audit of Q1-Q5**: Fixed PRT grading (AlgEquiv→NumAbsolute for zero answers in Q1 prt2, Q5 prt8), converted Q3/Q4 MCQs from algebraic→dropdown with Maxima list format, removed 8 answer-leaking syntaxhints (Q1 ans7/ans8, Q3 ans2, Q4 ans2/ans3/ans6, Q5 ans3/ans4 hints). Physics/math verified correct across all 5 questions. No SigFigsStrict used. 5% NumRelative properly applied.

### Repo Reorganization (2026-03-06)
- [x] Reorganized repo into `exams/midterm-week9/`, `weekly/week10/`, `shared/scripts/`
- [x] Created `CLAUDE.md` with STACK XML conventions, Maxima patterns, schemdraw rules, and common mistakes
- [x] Updated all skill context files (context.md, active-session.md, decisions-log.md)
- [x] Moved shared utilities (render_all.py, embed_images_in_xml.py) to `shared/scripts/`

### Week 10 Practice Questions (2026-03-05 to 2026-03-06)
- [x] Q1 — Series RLC natural response (3 damping regimes, dropdown MCQ classification)
- [x] Q2 — Parallel RLC step response (3 damping regimes, with voltage polarity Gap fix)
- [x] Q3 — Toroid: Ampere's law, B-H curve, magnetic flux (physical + reluctance diagrams)
- [x] Q4 — Magnetic circuit: reluctance, sensitivity analysis (C-core physical + reluctance diagrams)
- [x] Q5 — Parallel RLC natural response with switches (P8.11 inspired, 3 damping regimes) — XML/Maxima complete, diagram pending
- [x] Base64 SVG embedding implemented for all weekly questions
- [x] Converted MCQs from radio to dropdown for damping regime classification

### Midterm Week 9 Exam (2026-02-22 to 2026-02-24)
- [x] Q1 Easy — 4 STACK variants (two-node, two-mesh, T-network, bridge)
- [x] Q2 Medium A — 4 STACK+Essay variants (inductor RL, capacitor RC, waveform, parallel)
- [x] Q3 Medium B — 4 STACK variants (complex resistor networks, Req numerical)
- [x] Q4 Difficult — 3 STACK variants (RC switch, RL switch, Thevenin RC)
- [x] Upload question, PNG exports, critical audit (answer leaks, tolerance bugs)
- [x] MCQ format fixed (Maxima list format), diagram placeholders finalized

## Next Steps After Q5 Fix
1. **Moodle test import** — Import weekly/week10 XML files into sandbox, verify base64 SVGs render
2. **Moodle exam import** — Import exams/midterm-week9 XMLs, verify diagram placeholders work
3. **Add more weeks** — Create `weekly/week11/`, `weekly/week12/` etc. as course progresses
4. **Peer review** — Colleague review of exam difficulty equivalence and time-on-task
5. **Quiz assembly** — Configure Moodle quiz settings (random selection, timer, single attempt)

## Deferred Items
- Q4 4th variant (RL with Thevenin reduction) — instructor may request later
- Week 10 PNG exports (only SVGs generated; PNGs needed if SVG rendering fails in Moodle)

## Blockers / Open Questions
- **Q5 diagram topology** — User needs to provide reference image (Nilsson P8.11) so the Schemdraw script can be rewritten to match the exact layout
- **Moodle instance access needed** — Cannot validate XML imports without a STACK-enabled Moodle sandbox

## Last Updated
2026-03-06
