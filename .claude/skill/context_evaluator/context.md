# Project Context — STACK Exam & Practice Question Builder

## Project Overview

This project produces **Moodle STACK assessment content** for an undergraduate Electromagnetism and Circuit Analysis course. Content is organized into two categories:

1. **Exams** — Midterm/final exams with randomized variants and AI-resistance features (e.g., `exams/midterm-week9/`)
2. **Weekly practice** — Topic-specific question sets for formative assessment (e.g., `weekly/week10/`)

All content is delivered through **Moodle** using the **STACK** question type plugin (Maxima CAS for auto-grading). Circuit diagrams are generated with **CircuiTikZ/TikZ** (LaTeX), compiled to SVG via `pdflatex` + `pdf2svg`.

**This is NOT a coding project.** It is an educational assessment design project. The "code" is Moodle STACK XML (containing embedded Maxima CAS code) and SVG circuit diagrams.

**Repository:** `https://github.com/cassia-santos-nunes-almeida/Testing-Codes`

## Tech Stack and Tools

| Tool | Purpose |
|------|---------|
| **Moodle LMS** | Exam delivery platform (quiz module) |
| **STACK plugin** | Auto-grading engine for mathematical questions (numerical, algebraic, MCQ) |
| **Maxima CAS** | Computer algebra system embedded in STACK for randomization and grading |
| **Moodle XML** | Import format for all questions (STACK, Essay, File Upload) |
| **CircuiTikZ/TikZ** | LaTeX packages for circuit diagrams (`.tex` → SVG via pdflatex + pdf2svg) |
| **SVG + PNG** | Circuit diagram formats — SVG as source, PNG exports for Moodle upload |
| **Git** | Version control for all exam artifacts |
| **CC0 License** | Public domain dedication — no restrictions on reuse |

## Architecture

```
Testing-Codes/
├── CLAUDE.md                          # Repo-level rules, conventions, lessons learned
├── .claude/skill/                     # Claude skill files (session context + diagram generator)
├── docs/                              # Human-readable documentation
│   ├── 00_prompt_evaluation.md        # Analysis of original exam prompt + corrections
│   └── 01_exam_overview.md            # Complete exam specification
├── shared/
│   ├── scripts/                       # Reusable utilities across all content
│   │   ├── render_circuitikz.py       # .tex → .svg compilation (pdflatex + pdf2svg)
│   │   ├── render_all.py              # Batch Schemdraw rendering (legacy)
│   │   └── embed_images_in_xml.py     # Base64 SVG embedding for exam questions
│   └── templates/
│       └── circuitikz_template.tex    # Starter template for new diagrams
├── exams/
│   └── midterm-week9/                 # Week 9 midterm (50 pts, 120 min, 15 variants)
│       ├── xml/                       # pool_q1-q4 + upload_questions.xml
│       └── diagrams/
│           ├── q1/ q2/ q3/ q4/        # Exported SVG + PNG per variant
│           └── scripts/               # Schemdraw .py source files (legacy)
├── weekly/
│   └── week10/                        # RLC 2nd-order + magnetic circuits practice
│       ├── xml/                       # Q1-Q5 STACK questions
│       └── diagrams/                  # CircuiTikZ .tex + .svg per question
└── LICENSE                            # CC0 1.0 Universal
```

### Adding new content

- **New exam:** create `exams/<exam-name>/{xml,diagrams/}`
- **New week:** create `weekly/<weekN>/{xml,diagrams/}`
- **Naming:** `pool_q<N>_<difficulty>.xml` for exams, `Q<N>_<TopicDescription>.xml` for weekly
- **Shared scripts** go in `shared/scripts/`

### Diagram Embedding Strategy

Two approaches depending on content type:

- **Exam questions:** Text placeholders like `[INSERT DIAGRAM: ...]` in the XML. Instructor uploads diagrams manually via Moodle's editor after import. Both SVG (source) and PNG (1200px, 150 DPI) available.
- **Weekly questions:** Base64 SVG embedded directly in XML via `shared/scripts/embed_images_in_xml.py`. Works for practice questions where Moodle sanitizer is less restrictive.

## Content Summary

### Midterm Week 9 (50 Points Total, 120 Minutes)

| Pool | Difficulty | Points | Time | Topic | Variants |
|------|-----------|--------|------|-------|----------|
| Q1 | Easy | 12 | ~20 min | DC Resistive (node-voltage, mesh-current) | 4 |
| Q2 | Medium A | 13 | ~30 min | Component physics, energy storage, fields, debug | 4 |
| Q3 | Medium B | 13 | ~30 min | Laplace transforms, first-order circuits | 4 |
| Q4 | Difficult | 12 | ~30 min | Complete transient analysis (pre-switch → s-domain → response) | 3 |
| Upload | — | 0 | ~10 min | Handwritten work photos (PDF/JPG/PNG, up to 4 files) | 1 |

Each question has 4 scaffolded subparts (A-D) mixing STACK auto-graded and Essay manual-graded components. Grading split: ~60% STACK auto-graded, ~40% instructor-graded essays.

### Weekly Week 10 — RLC 2nd-Order + Magnetic Circuits (5 Questions)

| Question | Topic | Parts | Points |
|----------|-------|-------|--------|
| Q1 | Series RLC natural response (3 damping regimes) | 8 | 8 |
| Q2 | Parallel RLC step response (3 damping regimes) | 8 | 8 |
| Q3 | Toroid: Ampere's law, B-H curve, flux | 8 | 8 |
| Q4 | Magnetic circuit: reluctance, sensitivity analysis | 8 | 8 |
| Q5 | Parallel RLC natural response with switches (3 damping regimes) | 8 | 8 |

## Key Constraints

### Technical
- STACK plugin must be installed on the Moodle instance.
- Maxima syntax required for all STACK question variables, PRTs, and feedback.
- Algebraic input kept minimal — students find Maxima syntax frustrating. Prefer numerical inputs.
- Numerical tolerances: ±0.01 to ±0.5 depending on question context.
- SVG/PNG diagrams must be manually uploaded via Moodle's editor after XML import (text placeholders mark where each goes).
- Variable randomization ranges must avoid degenerate cases (division by zero, negative R/L/C, unrealistic values).

### Pedagogical
- Content scope: Weeks 2-8 only. **RLC second-order transients are explicitly excluded.**
- Difficulty must be equivalent across variants within the same pool.
- Every Q2 variant must contain a debug or compare subpart (AI-resistance guarantee).
- Essay subparts kept to 2-4 sentences to manage instructor grading workload.
- Handwritten upload is mandatory for process verification.

### Accessibility
- Sans-serif fonts in SVG diagrams.
- High-contrast colors.
- Clear English (international student cohort — no idioms).
- Explicit current arrows and voltage polarities on all circuit diagrams.

## Quality Assurance

All STACK XML content must pass the **multi-tiered PRT validation** (documented in CLAUDE.md) before committing:
- **Tier 1 — Structural:** Node chains, orphan nodes, feedbackvariable definitions
- **Tier 2 — Grading:** NumAbsolute for zero, NumRelative fallback, score consistency
- **Tier 3 — XML/CAS:** CDATA wrapping, insertstars, exact arithmetic
- **Tier 4 — Pedagogical:** Syntax hints, progressive hints, diagram-text sync, no answer leaks

**Week 10 status:** All 5 questions (38 PRTs) passed full validation (2026-03-07).

## Never Suggest

- Including RLC second-order transient content in the Week 9 exam (explicitly excluded from exam scope).
- Removing the handwritten upload requirement (core AI-resistance feature for exams).
- Making all exam subparts STACK-only (essays are pedagogically necessary for justification and physical interpretation).
- Using dependent sources in Q1 Easy (students reported difficulty — reserved for Q4 only).
- Per-question file uploads (consolidated single upload saves ~10 min of exam time).
- Complex Maxima algebraic inputs for students (error-prone and frustrating).
- Reducing the exam pool to fewer than 15 variants (instructor requirement).
- Using `AlgEquiv` for numerical answers that could be 0 (use `NumAbsolute` instead).
- Using `type="radio"` for classification MCQs — shows "Clear my choice" clutter. Use `type="dropdown"` instead.
- Mixing Schemdraw and CircuiTikZ diagrams in the same content set (visual inconsistency).
- Skipping PRT validation before committing STACK XML.

## Last Updated
2026-03-07
