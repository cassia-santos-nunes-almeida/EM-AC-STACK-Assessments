# Testing-Codes

## Project Overview

Educational assessment content for an undergraduate Electromagnetism & Circuit Analysis course. Two content types:

- **Exams** — Moodle STACK midterm/final exams with randomized variants and AI-resistance features
- **Weekly** — Practice questions for specific topics (RLC circuits, magnetic circuits, etc.)

All content is **Moodle STACK XML** (containing embedded Maxima CAS code) with **SVG circuit diagrams** generated via Python Schemdraw.

**Repository:** `https://github.com/cassia-santos-nunes-almeida/Testing-Codes`
**License:** CC0 1.0 Universal (public domain)

## Repository Structure

```
Testing-Codes/
├── CLAUDE.md                          # This file — repo-level rules and lessons learned
├── .claude/skill/
│   ├── context_evaluator/             # Project management context (session tracking, decisions)
│   └── rlc-circuit-drawing-generator/ # Circuit diagram generation skill + references
├── docs/                              # Human-readable documentation
│   ├── 00_prompt_evaluation.md        # Original exam brief analysis and corrections
│   └── 01_exam_overview.md            # Complete exam specification
├── shared/
│   └── scripts/                       # Reusable utilities across all content
│       ├── render_all.py              # Batch Schemdraw rendering
│       └── embed_images_in_xml.py     # Base64 SVG embedding for weekly questions
├── exams/
│   └── midterm-week9/                 # Week 9 midterm (50 pts, 120 min, 15 variants)
│       ├── xml/                       # pool_q1_easy.xml ... pool_q4_difficult.xml + upload
│       └── diagrams/
│           ├── q1/ q2/ q3/ q4/        # Exported SVG + PNG per variant
│           └── scripts/               # Schemdraw .py source files
└── weekly/
    └── week10/                        # RLC 2nd-order + magnetic circuits practice
        ├── xml/                       # Q1-Q5 STACK questions
        └── diagrams/                  # Schemdraw .py + .svg per question
```

### Adding New Content

- **New exam:** `exams/<exam-name>/{xml,diagrams/}`
- **New week:** `weekly/<weekN>/{xml,diagrams/}`
- **Naming:** `pool_q<N>_<difficulty>.xml` for exams, `Q<N>_<TopicDescription>.xml` for weekly
- **Shared scripts** go in `shared/scripts/`

## STACK XML Conventions (Mandatory)

### Syntax Hints

Every `[[input:ansN]]` MUST be followed by a visible syntax hint line immediately AFTER the input:

```html
[[input:ansN]]
<p><em>Syntax hint: Enter a number, e.g. <code>0.523</code> or <code>5.23e-1</code></em></p>
```

Type-specific hint text:

| Input type | Hint text |
|------------|-----------|
| MCQ / integer | `Enter a single integer, e.g. <code>2</code>` |
| Numerical | `Enter a number, e.g. <code>0.523</code> or <code>5.23e-1</code>` (adapt to expected magnitude) |
| Symbolic / algebraic | Show complete example with expected variables, e.g. `Write <code>lc/(mur*mu0*Ac)</code>` |
| Expression (function of t) | `Use <code>exp(...)</code>, <code>sin(...)</code>, <code>cos(...)</code>, and <code>t</code>.` |
| Notes / essay | Content hint about what to address |

### Progressive Hints

Every question MUST include 2-3 `<hint>` elements at the end of the `<question>` block:

1. **Hint 1:** Intuition / physical reasoning
2. **Hint 2:** Relevant formulas and approach
3. **Hint 3:** Worked step or partial derivation

### Grading (PRT) Rules

| Rule | Details |
|------|---------|
| Numerical answers | Use `NumRelative` with 5% tolerance. **Never** `AlgEquiv` alone for rounded values. |
| Answer is 0 | Use `NumAbsolute` with tolerance 0.01. `NumRelative` divides by zero. |
| Complex expressions (e.g. i(t)) | 2-node PRT: Node 0 = `AlgEquiv`; Node 1 fallback = evaluate at 2-3 test points with `NumRelative` (5%). |
| Complex-valued roots (s) | 2-node PRT: Node 0 = `AlgEquiv`; Node 1 = compare `realpart()`/`imagpart()` with `NumRelative` (2%). |
| `SigFigsStrict` | **Never** use as a scoring gate. Use `NumRelative` for full marks instead. |
| Specific feedback | **Never** use `{@ansN@}` — renders as CAS symbol. Use `[[feedback:prtN]]` only. |

### Input Configuration

| Setting | Value | Reason |
|---------|-------|--------|
| `insertstars` | `1` | Required for algebraic expression inputs (e.g. `2*exp(-3*t)`) |
| Classification MCQs | `type="radio"` | Use radio buttons, NOT dropdown MCQs, for regime/method selection |
| MCQ option format | `[[value, bool, "text"]]` | STACK 4.x Maxima list format in `questionvariables` |

## Maxima CAS Patterns

### Parameter Randomization

```maxima
/* Use rand_with_step for constrained random values */
R1: rand_with_step(2, 8, 2);    /* 2, 4, 6, or 8 */

/* CRITICAL: Verify parameter sets produce the intended damping regime */
/* alpha vs omega0 determines: overdamped, underdamped, or critically damped */
```

### RLC Circuit Formulas

| Circuit | alpha | omega0 | dv/dt(0+) or di/dt(0+) |
|---------|-------|--------|-------------------------|
| Parallel RLC | `1/(2*R*C)` | `1/sqrt(L*C)` | `dv/dt(0+) = -(1/C)*(V0/R + I0)` from KCL |
| Series RLC | `R/(2*L)` | `1/sqrt(L*C)` | `di/dt(0+) = (1/L)*(V0 - R*I0)` |

### Key Patterns

- **Natural response:** No forced term. `v_final = 0` (all exponentials decay to zero).
- **Step response:** Has forced term. `v_final = V_source * (voltage divider)`.
- **Pre-switch DC analysis:** Inductor = short circuit, capacitor = open circuit.
- **Damping classification:**
  - `alpha > omega0` → overdamped (two real roots)
  - `alpha < omega0` → underdamped (complex conjugate roots)
  - `alpha = omega0` → critically damped (repeated root)

## Schemdraw Circuit Diagrams

### Layout Rules

- **Vertical layout preferred:** Power source on left (vertical, positive on top), components arranged vertically on right using `.down()`
- **Sans-serif fonts** (Arial/Helvetica), **high-contrast** black on white
- **Explicit current arrows** and **voltage polarity markings** on every circuit
- Responsive sizing via `viewBox` attribute (no fixed width/height)
- Labels: `loc='bottom'` with `ofst=0.15` for vertical-down elements

### Voltage Polarity Labels

Use the **Gap/spacer technique** for voltage polarity labels that don't overlap components:

```python
# Create a gap element, then annotate + and - labels on it
gap = d.add(elm.Line().down().at(node).length(0))  # zero-length spacer
gap.label('+', loc='top', ofst=0.15)
gap.label('-', loc='bottom', ofst=0.15)
```

### Diagram Embedding

| Content type | Embedding method |
|--------------|-----------------|
| Weekly questions | Base64 SVG embedded directly in XML via `shared/scripts/embed_images_in_xml.py` |
| Exam questions | Text placeholders `[INSERT DIAGRAM: ...]` — instructor uploads manually via Moodle editor |

## Common Mistakes to Avoid

These are hard-won lessons from previous sessions. **Do not repeat these errors:**

1. **Don't use `AlgEquiv` when reference value is 0** — `NumRelative` divides by zero. Use `NumAbsolute` with tolerance 0.01.
2. **Don't use `SigFigsStrict` as a scoring gate** — penalizes formatting, not understanding.
3. **Don't leak answers** via `syntaxhint` or textarea placeholder text. In unsupervised exams, even structural hints narrow the solution space.
4. **Verify parameter sets mathematically** before implementing. Check that `alpha` vs `omega0` produces the intended damping regime for every variant.
5. **Don't use dropdown MCQs** for classification questions — use `type="radio"` radio buttons.
6. **Don't embed base64 in exam XMLs** — Moodle's HTML sanitizer strips data URIs. Use text placeholders for exams.
7. **Don't include dependent sources in Easy questions** — students find them confusing; reserve for Difficult (Q4) only.
8. **Test all parameter set variants** before committing. A single untested variant can produce wrong answers or degenerate cases.
9. **Don't use `{@ansN@}` in `<specificfeedback>`** — STACK renders these as CAS variable symbols, not student answers.
10. **Don't forget `insertstars=1`** on algebraic inputs — without it, `2t` is rejected instead of interpreted as `2*t`.

## Last Updated

2026-03-06
