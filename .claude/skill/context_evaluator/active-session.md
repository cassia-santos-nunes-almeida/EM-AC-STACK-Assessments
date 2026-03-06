# Active Session — STACK Exam & Practice Question Builder

## Current Milestone
**Repo reorganized with CLAUDE.md. Exam (15 variants) and Week 10 (Q1-Q5) content complete.** Repository restructured into `exams/` and `weekly/` directories with shared scripts. CLAUDE.md captures all technical conventions and lessons learned for session persistence.

## Completed Tasks

### Repo Reorganization (2026-03-06)
- [x] Reorganized repo into `exams/midterm-week9/`, `weekly/week10/`, `shared/scripts/`
- [x] Created `CLAUDE.md` with STACK XML conventions, Maxima patterns, schemdraw rules, and common mistakes
- [x] Updated all skill context files (context.md, active-session.md, decisions-log.md)
- [x] Moved shared utilities (render_all.py, embed_images_in_xml.py) to `shared/scripts/`

### Week 10 Practice Questions (2026-03-05 to 2026-03-06)
- [x] Q1 — Series RLC natural response (3 damping regimes, radio MCQ classification)
- [x] Q2 — Parallel RLC step response (3 damping regimes, with voltage polarity Gap fix)
- [x] Q3 — Toroid: Ampere's law, B-H curve, magnetic flux (physical + reluctance diagrams)
- [x] Q4 — Magnetic circuit: reluctance, sensitivity analysis (C-core physical + reluctance diagrams)
- [x] Q5 — Parallel RLC natural response with switches (P8.11 inspired, 3 damping regimes)
- [x] Base64 SVG embedding implemented for all weekly questions
- [x] Converted dropdown MCQs to radio buttons for damping regime classification

### Midterm Week 9 Exam (2026-02-22 to 2026-02-24)
- [x] Q1 Easy — 4 STACK variants (two-node, two-mesh, T-network, bridge)
- [x] Q2 Medium A — 4 STACK+Essay variants (inductor RL, capacitor RC, waveform, parallel)
- [x] Q3 Medium B — 4 STACK variants (complex resistor networks, Req numerical)
- [x] Q4 Difficult — 3 STACK variants (RC switch, RL switch, Thevenin RC)
- [x] Upload question, PNG exports, critical audit (answer leaks, tolerance bugs)
- [x] MCQ format fixed (Maxima list format), diagram placeholders finalized

## Immediate Next Steps (Prioritized)
1. **Moodle test import** — Import weekly/week10 XML files into sandbox, verify base64 SVGs render
2. **Moodle exam import** — Import exams/midterm-week9 XMLs, verify diagram placeholders work
3. **Add more weeks** — Create `weekly/week11/`, `weekly/week12/` etc. as course progresses
4. **Peer review** — Colleague review of exam difficulty equivalence and time-on-task
5. **Quiz assembly** — Configure Moodle quiz settings (random selection, timer, single attempt)

## Deferred Items
- Q4 4th variant (RL with Thevenin reduction) — instructor may request later
- Week 10 PNG exports (only SVGs generated; PNGs needed if SVG rendering fails in Moodle)

## Blockers / Open Questions
- **Moodle instance access needed** — Cannot validate XML imports without a STACK-enabled Moodle sandbox
- **Base64 SVG rendering** — Weekly questions use embedded base64; needs verification in target Moodle theme

## Last Updated
2026-03-06
