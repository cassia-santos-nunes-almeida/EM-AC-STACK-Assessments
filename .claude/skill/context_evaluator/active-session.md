# Active Session — STACK Exam & Practice Question Builder

## Current Milestone
**Week 10 Q1-Q5 content complete. CircuiTikZ migration done. Full PRT validation passed.** All 5 questions validated across 38 PRTs — node chains, feedbackvariables, CDATA wrapping, scoring, and pedagogical quality all confirmed correct. Session 3 closed (2026-03-07).

## Pending Tasks (Prioritized)

### Progressive Hint Unlocking (Next Session)
- [ ] **Research STACK conditional blocks** — Investigate `[[if test="..."]]` syntax for attempt-gated hints
- [ ] **Prototype on Q1** — Implement progressive hint reveal based on attempt count or PRT score
- [ ] **Roll out to Q2-Q5** — Apply pattern to remaining weekly questions
- [ ] **Evaluate for exams** — Determine if progressive hints are appropriate for exam context

### Post-Migration Verification
- [ ] **Visual review of all 7 CircuiTikZ SVGs** — Verify circuit topology matches original Schemdraw versions
- [ ] **Moodle test import** — Import weekly/week10 XML files into sandbox, verify base64 SVGs render

## Completed Tasks

### Session 3: PRT Validation & Session Close (2026-03-07)
- [x] Multi-tiered PRT validation of all 5 questions (38 PRTs total) — all passed
- [x] Validated: node chain integrity, orphan detection, feedbackvariable definitions
- [x] Validated: CDATA wrapping for `<` operators in all feedbackvariables blocks
- [x] Validated: score consistency (1.0/0.7/0.3/0.0 pattern), penalty settings
- [x] Validated: NumAbsolute for zero-valued answers (Q1 prt2, Q5 prt8)
- [x] Validated: NumRelative fallback nodes on symbolic PRTs (Q1 prt7/prt8, Q2 prt7/prt8, Q5 prt7/prt8)
- [x] Updated CLAUDE.md — added PRT Validation Methodology section, 6 new lessons learned (#21-#26), fixed numbering (#14/#15 swap), added progressive hint unlocking roadmap
- [x] Updated all context files for session close

### Session 2: CircuiTikZ Migration (2026-03-07)
- [x] Installed system dependencies (texlive-latex-base, texlive-pictures, texlive-latex-recommended, texlive-latex-extra, pdf2svg)
- [x] Created `shared/scripts/render_circuitikz.py` (single-file and batch `.tex` → SVG compilation)
- [x] Created `shared/templates/circuitikz_template.tex` (starter template)
- [x] Renamed 7 Schemdraw `.py` + `.svg` files with `_schemdraw` suffix (preserved)
- [x] Created 7 CircuiTikZ `.tex` files for all week 10 diagrams (Q1-Q5, including Q3/Q4 physical + reluctance)
- [x] Compiled all `.tex` to `.svg` via pdflatex + pdf2svg
- [x] Re-embedded new SVGs as base64 in all 5 XML files
- [x] Updated CLAUDE.md — replaced Schemdraw section with CircuiTikZ conventions
- [x] Updated decisions-log.md — documented migration decision

### Session 1: Deep Audit & Fixes (2026-03-06)
- [x] Base64 SVG auto-embedding for all Q1-Q5 weekly questions
- [x] Converted radio MCQs to dropdown (type="dropdown") — no more "Clear my choice"
- [x] Q5 diagram rewritten to match Nilsson P8.11 topology with 4 SPST switches
- [x] Added switch names (SW1-SW4) and updated XML questiontext
- [x] **Deep audit of Q1-Q5**: Fixed PRT grading (AlgEquiv→NumAbsolute for zero answers), converted Q3/Q4 MCQs to dropdown, removed 8 answer-leaking syntaxhints
- [x] Repo reorganization into `exams/midterm-week9/`, `weekly/week10/`, `shared/scripts/`
- [x] Created `CLAUDE.md` with STACK XML conventions, Maxima patterns, CircuiTikZ rules

### Initial Content Creation (2026-03-05 to 2026-03-06)
- [x] Q1 — Series RLC natural response (3 damping regimes, dropdown MCQ classification)
- [x] Q2 — Parallel RLC step response (3 damping regimes, with voltage polarity)
- [x] Q3 — Toroid: Ampere's law, B-H curve, magnetic flux (physical + reluctance diagrams)
- [x] Q4 — Magnetic circuit: reluctance, sensitivity analysis (C-core physical + reluctance diagrams)
- [x] Q5 — Parallel RLC natural response with 4 SPST switches (P8.11 inspired, 3 damping regimes)

### Midterm Week 9 Exam (2026-02-22 to 2026-02-24)
- [x] Q1-Q4 STACK variants + Upload question, PNG exports, critical audit

## Next Steps (Ordered)
1. **Progressive hint unlocking** — Research and implement STACK conditional hint reveal
2. **Visual review** — Check CircuiTikZ SVGs match original circuit topologies
3. **Moodle test import** — Import weekly/week10 XML files into sandbox
4. **Add more weeks** — Create `weekly/week11/`, `weekly/week12/` as course progresses
5. **Migrate exam diagrams** — Optionally redraw exam diagrams in CircuiTikZ

## External Skill Updates Needed (my-claude-skill GitHub)

The following updates should be applied to the **my-claude-skill** repository next time it's open. These reflect lessons learned across sessions 1-3.

### CircuiTikZ Diagram Skill (`circuitikz-latex-circuit-diagrams`)

1. **SKILL.md — Add compilation testing rule:** Add a note under Workflow: "Always compile `.tex` → SVG and visually inspect before base64-encoding into XML. LaTeX errors produce no output and a broken base64 renders as nothing in Moodle." (lesson #25)
2. **SKILL.md — Add `standalone` border note:** Mention `border=10pt` is mandatory to prevent label/arrow clipping at SVG edges (lesson #26).
3. **circuit-patterns.md — Pattern 6 switch bug FIXED locally:** The original had `closing switch` for "opens" and `opening switch` for "closes" — reversed. Fixed in this repo's copy. **Sync this fix to the skill repo.**
4. **circuit-patterns.md — Add tip about testing before embedding:** Add to "Tips for Clean Layouts": "Always compile and visually inspect SVGs before embedding as base64 in XML."
5. **circuitikz-guide.md — Add switch semantics warning:** In the Switches table, add a note: "Element name = action at t=0, not prior state. `opening switch` = was closed, now breaking. `closing switch` = was open, now making."
6. **assets/examples/ — Consider adding CircuiTikZ examples:** Current examples are legacy Schemdraw `.py` files. Add `.tex` equivalents for at least 2-3 patterns (series RLC, parallel RLC, multi-switch).

### Context Evaluator Skill (`contex-evaluator`)

1. **SKILL.md — Add PRT validation reference:** Under "Session Rules > Do", add: "Before committing any STACK XML, run the multi-tiered PRT validation checklist (documented in CLAUDE.md). Validate all 4 tiers: structural, grading, XML/CAS safety, pedagogical."
2. **SKILL.md — Fix SVG naming convention:** Current text says `q{N}_v{M}_{description}.svg` but weekly questions use `q{N}_{description}.svg` (no variant suffix). Clarify: exams use variant suffix, weekly questions don't.
3. **SKILL.md — Add progressive hint unlocking:** Under "MANDATORY — Conceptual hints", add: "Future: investigate STACK `[[if test="..."]]` conditional blocks for attempt-gated progressive hint reveal."
4. **SKILL.md — Add CDATA rule:** Under grading robustness, add: "All PRT `<feedbackvariables>` blocks containing `<` comparison operators MUST be wrapped in `<![CDATA[...]]>`."
5. **SKILL.md — Fix skill name typo:** The `name` field says `contex-evaluator` (missing 't'). Should be `context-evaluator`.

## Deferred Items
- Q4 4th variant (RL with Thevenin reduction) — instructor may request later
- Exam diagram migration to CircuiTikZ (lower priority — text placeholders still work)

## Blockers / Open Questions
- **Moodle instance access needed** — Cannot validate XML imports without a STACK-enabled Moodle sandbox

## Last Updated
2026-03-07
