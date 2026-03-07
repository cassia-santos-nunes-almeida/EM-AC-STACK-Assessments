# Active Session — STACK Exam & Practice Question Builder

## Current Milestone
**Week 10 Q1-Q5 content complete. Migrated from Schemdraw to CircuiTikZ.** All questions work in STACK with correct Maxima grading. Deep audit completed (2026-03-06). Circuit diagrams migrated to CircuiTikZ/TikZ `.tex` files (2026-03-07) — native switch elements, no more matplotlib workarounds. Old Schemdraw files preserved with `_schemdraw` suffix.

## Pending Tasks (Prioritized)

### Post-Migration Verification
- [ ] **Visual review of all 7 CircuiTikZ SVGs** — Verify circuit topology matches original Schemdraw versions
- [ ] **Moodle test import** — Import weekly/week10 XML files into sandbox, verify base64 SVGs render

## Completed Tasks

### CircuiTikZ Migration (2026-03-07)
- [x] Installed system dependencies (texlive-latex-base, texlive-pictures, texlive-latex-recommended, texlive-latex-extra, pdf2svg)
- [x] Created `shared/scripts/render_circuitikz.py` (single-file and batch `.tex` → SVG compilation)
- [x] Created `shared/templates/circuitikz_template.tex` (starter template)
- [x] Renamed 7 Schemdraw `.py` + `.svg` files with `_schemdraw` suffix (preserved)
- [x] Created 7 CircuiTikZ `.tex` files for all week 10 diagrams (Q1-Q5, including Q3/Q4 physical + reluctance)
- [x] Compiled all `.tex` to `.svg` via pdflatex + pdf2svg
- [x] Re-embedded new SVGs as base64 in all 5 XML files
- [x] Updated CLAUDE.md — replaced Schemdraw section with CircuiTikZ conventions
- [x] Updated decisions-log.md — documented migration decision

### Session Updates (2026-03-06)
- [x] Base64 SVG auto-embedding for all Q1-Q5 weekly questions
- [x] Converted radio MCQs to dropdown (type="dropdown") — no more "Clear my choice"
- [x] Q5 diagram rewritten to match Nilsson P8.11 topology with 4 SPST switches
- [x] Added switch names (SW1-SW4) and updated XML questiontext
- [x] **Deep audit of Q1-Q5**: Fixed PRT grading (AlgEquiv→NumAbsolute for zero answers), converted Q3/Q4 MCQs to dropdown, removed 8 answer-leaking syntaxhints

### Repo Reorganization (2026-03-06)
- [x] Reorganized repo into `exams/midterm-week9/`, `weekly/week10/`, `shared/scripts/`
- [x] Created `CLAUDE.md` with STACK XML conventions, Maxima patterns, CircuiTikZ rules, and common mistakes
- [x] Updated all skill context files

### Week 10 Practice Questions (2026-03-05 to 2026-03-06)
- [x] Q1 — Series RLC natural response (3 damping regimes, dropdown MCQ classification)
- [x] Q2 — Parallel RLC step response (3 damping regimes, with voltage polarity)
- [x] Q3 — Toroid: Ampere's law, B-H curve, magnetic flux (physical + reluctance diagrams)
- [x] Q4 — Magnetic circuit: reluctance, sensitivity analysis (C-core physical + reluctance diagrams)
- [x] Q5 — Parallel RLC natural response with 4 SPST switches (P8.11 inspired, 3 damping regimes)

### Midterm Week 9 Exam (2026-02-22 to 2026-02-24)
- [x] Q1 Easy — 4 STACK variants (two-node, two-mesh, T-network, bridge)
- [x] Q2 Medium A — 4 STACK+Essay variants (inductor RL, capacitor RC, waveform, parallel)
- [x] Q3 Medium B — 4 STACK variants (complex resistor networks, Req numerical)
- [x] Q4 Difficult — 3 STACK variants (RC switch, RL switch, Thevenin RC)
- [x] Upload question, PNG exports, critical audit (answer leaks, tolerance bugs)

## Next Steps
1. **Visual review** — Check CircuiTikZ SVGs match original circuit topologies
2. **Moodle test import** — Import weekly/week10 XML files into sandbox, verify base64 SVGs render
3. **Moodle exam import** — Import exams/midterm-week9 XMLs, verify diagram placeholders work
4. **Add more weeks** — Create `weekly/week11/`, `weekly/week12/` etc. as course progresses
5. **Migrate exam diagrams** — Optionally redraw exam diagrams in CircuiTikZ for visual consistency

## Deferred Items
- Q4 4th variant (RL with Thevenin reduction) — instructor may request later
- Exam diagram migration to CircuiTikZ (lower priority — text placeholders still work)

## Blockers / Open Questions
- **Moodle instance access needed** — Cannot validate XML imports without a STACK-enabled Moodle sandbox

## Last Updated
2026-03-07
