# Decisions Log — STACK Exam Builder

## Format
Each entry: `[date] — Decision` followed by reasoning and rejected alternatives.

---

### 2026-02-22 — Evaluate and correct the original exam prompt before building anything
**Reason:** The original prompt had 10 identifiable issues (time budget, STACK limitations, accessibility, etc.) that would have propagated into the final product if not addressed upfront. Front-loading this analysis saved rework.
**Alternatives rejected:** Building questions first and fixing issues later — higher rework cost and risk of structural problems baked into XML.

---

### 2026-02-22 — Use 60% STACK auto-graded / 40% Essay manual-graded split
**Reason:** STACK cannot grade justification, physical interpretation, or debugging explanations. Forcing these into STACK would either make them trivially auto-gradeable (defeating the purpose) or create frustrating Maxima syntax requirements for students.
**Alternatives rejected:** 100% STACK (loses pedagogical depth), 100% manual (defeats the purpose of STACK), 80/20 split (too few essay subparts for meaningful assessment of understanding).

---

### 2026-02-22 — Exclude dependent sources from Q1 (Easy), reserve for Q4 (Difficult) only
**Reason:** Students reported difficulty with dependent sources. Including them in the Easy question would misrepresent its difficulty level and create unfair assessment.
**Alternatives rejected:** Including dependent sources in Q1 with reduced complexity — still too confusing for an "Easy" classification.

---

### 2026-02-22 — Consolidate file upload into a single question at the end
**Reason:** Per-question uploads (4 separate photo + upload cycles) would consume ~20 minutes of exam time. A single consolidated upload saves ~10 minutes and reduces student stress.
**Alternatives rejected:** Per-question uploads (too time-consuming), no upload requirement (removes key AI-resistance feature).

---

### 2026-02-22 — Guarantee a debug/compare subpart in every Q2 variant
**Reason:** The original prompt said "at least one debug per attempt" but random selection from a pool could theoretically skip debug questions. Embedding debug/compare in every Q2 variant guarantees exposure regardless of which variant a student receives.
**Alternatives rejected:** Relying on pool-level probability (not guaranteed), adding debug to all questions (over-saturates the exam with one question type).

---

### 2026-02-22 — Keep fields questions conceptual only (no Lorentz force calculations)
**Reason:** Week 5 coverage was conceptual. Calculation-based fields questions would test content not adequately taught, creating an unfair assessment.
**Alternatives rejected:** Including quantitative fields problems — unfair given the course coverage depth.

---

### 2026-02-22 — Use 4+4+4+3 = 15 variant pool structure
**Reason:** Instructor requirement for sufficient randomization. Q4 has 3 variants instead of 4 because the difficulty level requires more complex circuit design, and quality was prioritized over quantity.
**Alternatives rejected:** Fewer variants (insufficient randomization), more variants (quality would suffer given the complexity of full STACK implementation).

---

### 2026-02-22 — Minimize algebraic STACK inputs; prefer numerical
**Reason:** Students (especially international students) find Maxima algebraic syntax error-prone and frustrating. Numerical inputs with appropriate tolerances test the same skills without syntax barriers.
**Alternatives rejected:** Full algebraic input (high syntax error rate), multiple-choice only (too easy to guess).

---

### 2026-02-22 — SVG format for all circuit diagrams
**Reason:** SVGs are scalable (no pixelation at any zoom), accessible (text elements readable by screen readers), embeddable inline in STACK question HTML, and version-controllable in Git (they're text files).
**Alternatives rejected:** PNG/JPG (not scalable, not accessible), LaTeX TikZ (not directly embeddable in Moodle STACK question text), external image hosting (fragile, may break).

---

### 2026-02-22 — Sans-serif fonts and high-contrast colors in diagrams
**Reason:** Accessibility for students with dyslexia and visual impairments. High contrast ensures readability on various screens and when printed.
**Alternatives rejected:** Default serif fonts (less accessible), decorative styling (distracting from content).

---

### 2026-02-22 — Explicit reference directions (current arrows, voltage polarities) on all diagrams
**Reason:** Ambiguous reference directions are a common source of errors unrelated to circuit analysis skill. Explicit directions test analysis ability, not diagram interpretation guesswork.
**Alternatives rejected:** Leaving reference directions implicit (tests the wrong skill for this exam level).

---

### 2026-02-22 — Equal point distribution for Q1 Easy (12 pts) and Q4 Difficult (12 pts)
**Reason:** Instructor preference. Although it reduces score discrimination between strong and weak students, the scaffolded subparts within Q4 provide an internal difficulty gradient. The instructor's pedagogical judgment was respected.
**Alternatives rejected:** Weighting Q4 higher (rejected by instructor preference).

---

### 2026-02-22 — Time budget: 20 + 30 + 30 + 30 + 10 (upload) = 120 minutes
**Reason:** Based on analysis of subpart count and complexity. Q1 is shortest (simpler calculations), Q2-Q4 each get 30 minutes for more complex multi-step problems. Upload buffer is generous to reduce time pressure.
**Alternatives rejected:** Equal 25-min splits (doesn't reflect actual difficulty differences), 90-min exam (too rushed for this content depth).

---

### 2026-02-02 — CC0 public domain license
**Reason:** Maximum reusability. Other instructors can freely adapt questions without legal concerns. Aligns with open educational resources (OER) philosophy. (Decision predates the Claude-assisted work — made at repository creation.)
**Alternatives rejected:** MIT/Apache (unnecessary complexity for educational content), CC-BY (attribution requirement adds friction for exam reuse).

---

### 2026-02-22 — Variable randomization ranges designed to avoid degenerate cases
**Reason:** Random parameters must never produce division by zero, negative resistance/inductance/capacitance, or unrealistically large/small values. Ranges were chosen with constraints (e.g., R1 != R2 when division would occur).
**Alternatives rejected:** Wider ranges with runtime checks (more complex Maxima code, harder to debug).

---

### 2026-02-23 — Q1 SVG diagrams reworked for responsive design
**Reason:** Initial diagrams had fixed sizing that didn't render well across devices. Responsive SVG with viewBox attributes ensures proper display on desktop, tablet, and mobile.
**Alternatives rejected:** Fixed-width only (poor mobile experience), multiple resolution exports (maintenance burden).

---

### 2026-02-23 — Create Claude skill package for session continuity
**Reason:** The project involves substantial domain knowledge, design decisions, and pedagogical rationale that would be expensive to re-explain in every new Claude session. A structured skill package preserves this context.
**Alternatives rejected:** Re-explaining each session (time-consuming), single monolithic context file (hard to maintain and update).

---

### 2026-02-23 — Use STACK MCQ list format `[[value, bool, "text"]]` for all dropdowns
**Reason:** STACK 4.x requires dropdown/MCQ options to be defined as Maxima lists of `[value, correctness_flag, "display_text"]` triples in `questionvariables`. Bare integers or `<options>` XML elements don't work. Discovered through iterative Moodle import testing — Q1 was fixed first, then Q2 was converted to match.
**Alternatives rejected:** Bare integer answer with `<options>` XML element (does not render in STACK 4.x), radio buttons (not compatible with inline STACK input slots).

---

### 2026-02-23 — Use text placeholders for diagram references instead of embedding
**Reason:** After three failed embedding approaches (base64 data URIs stripped by Moodle security, `@@PLUGINFILE@@` references unreliable on import, inline SVG too large), the pragmatic solution is text placeholders like `[INSERT DIAGRAM: diagrams/q1/q1_v1_two_node.svg]`. The instructor manually uploads each diagram via Moodle's rich text editor after importing the XML.
**Alternatives rejected:** Base64 data URIs (stripped by Moodle's HTML sanitizer), `@@PLUGINFILE@@` with `<file>` elements (unreliable rendering after import), inline SVG in CDATA (bloated XML, rendering inconsistencies).

---

### 2026-02-23 — Generate PNG exports alongside SVGs for Moodle compatibility
**Reason:** Some Moodle themes and export paths (PDF, mobile app) don't render SVGs reliably. High-resolution PNG exports (1200px wide, 150 DPI) provide a universal fallback. Both formats are kept in the repository.
**Alternatives rejected:** SVG-only (rendering issues in some Moodle contexts), PNG-only (loses scalability and version-controllability of SVG source).

---

### 2026-02-23 — Change Q2 energy tolerance from NumAbsolute to NumRelative (5%)
**Reason:** Energy calculations with randomized parameters produce answers spanning several orders of magnitude. A fixed absolute tolerance (e.g., ±0.01) is too tight for large answers and too generous for small ones. A 5% relative tolerance (`NumRelative`) adapts to the answer magnitude.
**Alternatives rejected:** Wider absolute tolerance (still fails for extreme parameter combinations), tighter relative tolerance (penalizes rounding differences).

---

### 2026-02-23 — Remove all textarea placeholders that leak answers
**Reason:** Critical audit discovered that placeholder text in Essay textareas for Q1 (Part B equations), Q1 V4 (bridge balance hint), and Q4 (s-domain setup) gave away partial or full solutions. These were removed to maintain exam integrity.
**Alternatives rejected:** Keeping generic placeholders (even generic hints can narrow the solution space in a take-home exam).

---

### 2026-02-23 — Remove syntaxhint from Q3 ansB to prevent answer leakage
**Reason:** STACK's `syntaxhint` parameter for algebraic inputs was pre-filling the exact transfer function structure, effectively giving away the answer. Removed across all Q3 variants. Also added uppercase letters to `allowwords` so students can type `A`, `B`, `C`, `D` without case errors.
**Alternatives rejected:** Keeping a partial hint (any structural hint narrows the answer space too much for a take-home exam).

---

### 2026-02-24 — Redesign Q3 circuits with complex resistor networks (3-4 nodes, 3 meshes)
**Reason:** Original Q3 circuits were trivially simple (single-loop series R+L or R+C, 2 nodes, 1 mesh). For a Medium B question in an unsupervised exam, students could solve them instantly or get full solutions from AI. New circuits require genuine multi-step circuit analysis (Thevenin, series/parallel combinations, node analysis) before applying Laplace.
**Alternatives rejected:** Adding dependent sources (excluded from Q3 scope, reserved for Q4), adding second energy storage element (would make circuits second-order, violating the RLC exclusion constraint).

---

### 2026-02-24 — Change Q3 Part B from algebraic transfer function to numerical Req
**Reason:** With complex resistor networks, the transfer function expression becomes unwieldy for algebraic STACK input. Asking for the equivalent resistance (numerical) directly tests the circuit analysis skill and is practical for STACK grading. Part C then uses Req to compute tau.
**Alternatives rejected:** Keeping algebraic H(s) (messy expressions with substituted numerical values, error-prone Maxima syntax for students), asking for Vth+Rth separately (too many input fields for 4 points).

---

### 2026-02-24 — Strip all hints, version identifiers, and solution annotations from diagrams and questions
**Reason:** In an unsupervised open-everything exam, any hint narrows the solution space for AI tools. Removed: s-domain annotation boxes, "Find:" instructions, variant labels ("Q3-V1", "Q3-V2"), method hints ("3 nodes, 3 meshes"), placeholder text in textareas. Students must determine the analysis approach themselves.
**Alternatives rejected:** Keeping generic hints (even method-neutral hints like "use Thevenin" or "find tau" reduce AI resistance).

---

### 2026-03-05 — Use radio buttons (type="radio") instead of dropdown MCQs for classification
**Reason:** Dropdown MCQs in STACK use a complex Maxima list format and render inconsistently. Radio buttons are more natural for regime/method classification (3-4 options) and work reliably across STACK versions.
**Alternatives rejected:** Dropdown MCQ (rendering issues, verbose Maxima syntax), integer input with mapping (error-prone for students).

---

### 2026-03-05 — Use NumAbsolute (tolerance 0.01) when reference value is 0
**Reason:** `NumRelative` computes relative error as `|student - teacher| / |teacher|`, which divides by zero when the correct answer is 0. Discovered when testing Q5 Part (h) where v_o(infinity) = 0.
**Alternatives rejected:** `NumRelative` with any tolerance (mathematically undefined at 0), `AlgEquiv` (too strict for numerical contexts).

---

### 2026-03-06 — Switch back to dropdown (type="dropdown") for classification MCQs
**Reason:** Radio buttons show an unnecessary "Clear my choice" link in Moodle. The earlier dropdown rendering issues (2026-02-23) were caused by incorrect Maxima format, not the dropdown type itself. Now that the correct `[[value, bool, "text"]]` format is in place, dropdown works cleanly — simple click-and-choose with no clutter. Supersedes the 2026-03-05 decision to use radio.
**Alternatives rejected:** Radio buttons (shows "Clear my choice"), integer input (less user-friendly).

---

### 2026-03-06 — Use base64 SVG embedding for weekly practice questions
**Reason:** Weekly questions are lower-stakes than exams. Base64 SVG data URIs work in the Moodle question bank for practice/formative contexts where the HTML sanitizer is less restrictive. This avoids the manual diagram upload step required for exam questions.
**Alternatives rejected:** Text placeholders (unnecessary friction for practice questions), `@@PLUGINFILE@@` (unreliable on import).

---

### 2026-03-06 — Reorganize repo into exams/ and weekly/ subdirectories
**Reason:** The flat structure (all XMLs in `xml/`, all diagrams in `diagrams/`) mixed exam and weekly content, making it hard to add new content types. The new `exams/<name>/` and `weekly/<weekN>/` structure scales to any number of exams and weekly sets. Shared utilities moved to `shared/scripts/`.
**Alternatives rejected:** Keep flat structure with naming conventions only (doesn't scale), separate repos per content type (over-engineered).

---

### 2026-03-06 — Add CLAUDE.md for persistent technical context
**Reason:** Skill context files (context.md, active-session.md, decisions-log.md) require loading the skill to access. CLAUDE.md is automatically loaded by Claude Code, providing always-available technical guardrails (STACK conventions, common mistakes, Maxima patterns) without depending on skill activation.
**Alternatives rejected:** Relying only on skill context files (not loaded in Claude Code CLI), putting everything in CLAUDE.md (would duplicate project management that skills handle better).

---

### 2026-03-06 — Deep audit fixes: AlgEquiv→NumAbsolute for zero answers, MCQ dropdown conversion, syntaxhint leak removal
**Reason:** User reported "Fill in correct responses" marking some answers incorrect in STACK preview. Root cause analysis identified three categories of issues:
1. **Q3/Q4 MCQ inputs using `type="algebraic"` instead of `type="dropdown"`** — STACK's "Fill correct" behaves inconsistently with typed integer MCQs vs. dropdown MCQs. Converting to dropdown with Maxima list format `[[value, bool, "text"]]` aligns with Q1/Q2/Q5 convention and fixes preview behavior.
2. **AlgEquiv for zero-valued answers (Q1 prt2 i(0⁺)=0, Q5 prt8 v(∞)=0)** — Changed to NumAbsolute with tolerance 0.01 to avoid edge cases.
3. **8 syntaxhints leaking exact answers** — Removed or replaced with generic examples across Q1, Q3, Q4, Q5.
**Physics/math verified correct** across all 5 questions. No SigFigsStrict anywhere. 5% NumRelative properly applied on all non-zero numerical answers.
**Alternatives rejected:** Leaving algebraic MCQs (functional but inconsistent UX and "Fill correct" issues), keeping answer-leaking hints (undermines assessment integrity).

---

### 2026-03-07 — Migrate from Schemdraw to CircuiTikZ as sole diagram tool

**Reason:** Schemdraw (pure Python) lacked native SPST/SPDT switch elements with open/closed visual states, requiring a custom `draw_switch` matplotlib helper. CircuiTikZ provides native `opening switch`/`closing switch` elements, a much larger component library (European symbols, transformers, etc.), and eliminates the need for workarounds. The trade-off (LaTeX dependency + compilation step) is acceptable since all diagrams are pre-compiled to SVG for Moodle embedding.

**Migration approach:**
- Existing Schemdraw `.py` and `.svg` files renamed with `_schemdraw` suffix (preserved, not deleted)
- 7 new `.tex` files created for week 10 diagrams using CircuiTikZ/TikZ
- Compilation pipeline: `.tex` → `pdflatex` → PDF → `pdf2svg` → SVG
- New `shared/scripts/render_circuitikz.py` handles compilation (single file or batch)
- New `shared/templates/circuitikz_template.tex` provides starter template

**System dependencies added:** `texlive-latex-base`, `texlive-pictures`, `texlive-latex-recommended`, `texlive-latex-extra`, `pdf2svg`

**Supersedes:** 2026-02-22 decision noting "LaTeX TikZ (not directly embeddable in Moodle STACK question text)" as a rejected alternative — this is still true, but we now pre-compile to SVG instead of trying to embed TikZ directly.

**Alternatives rejected:** Keeping both tools (visual inconsistency, two pipelines to maintain, decision overhead), staying with Schemdraw only (continued need for workarounds on switches and limited component library).

---

### 2026-03-07 — Adopt multi-tiered PRT validation methodology as standard practice

**Reason:** Manual spot-checking of PRTs missed subtle issues in previous sessions (e.g., broken node chains, missing feedbackvariable definitions, un-wrapped `<` operators). A systematic 4-tier checklist (structural integrity → grading correctness → XML/CAS safety → pedagogical quality) caught all categories of issues during session 3 validation of 38 PRTs across 5 questions.

**Methodology tiers:**
1. **Structural:** Node chain completeness, orphan detection, feedbackvariable definitions
2. **Grading:** NumAbsolute for zero, NumRelative fallback on symbolic PRTs, score consistency
3. **XML/CAS Safety:** CDATA wrapping, insertstars, exact arithmetic
4. **Pedagogical:** Syntax hints, progressive hints, diagram-text sync, no answer leaks

**Alternatives rejected:** Ad-hoc checking (incomplete coverage), automated XML schema validation only (doesn't catch CAS-level issues like wrong answertest selection).

---

### 2026-03-07 — Plan progressive hint unlocking as next feature

**Reason:** Currently all hints are visible simultaneously, which reduces their pedagogical value — students skip straight to the most detailed hint. STACK supports `[[if test="..."]]` conditional blocks that can gate content on attempt number or PRT score, enabling a progressive reveal: Hint 1 (intuition) → Hint 2 (formulas, after 1 wrong attempt) → Hint 3 (worked step, after 2 wrong attempts).

**Scope:** Weekly questions first (Q1-Q5). Exam applicability TBD — progressive hints may conflict with exam time pressure.

**Alternatives rejected:** Removing hints entirely (reduces learning value), keeping all hints visible (current approach, but suboptimal for learning).

---

## Last Updated
2026-03-07
