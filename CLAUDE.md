# Testing-Codes

## Project Overview

Educational assessment content for an undergraduate Electromagnetism & Circuit Analysis course. Two content types:

- **Exams** — Moodle STACK midterm/final exams with randomized variants and AI-resistance features
- **Weekly** — Practice questions for specific topics (RLC circuits, magnetic circuits, etc.)

All content is **Moodle STACK XML** (containing embedded Maxima CAS code) with **SVG circuit diagrams** generated via CircuiTikZ/TikZ (LaTeX).

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
│   ├── scripts/                       # Reusable utilities across all content
│   │   ├── render_circuitikz.py       # .tex → .svg compilation (pdflatex + pdf2svg)
│   │   ├── render_all.py              # Batch Schemdraw rendering (legacy)
│   │   └── embed_images_in_xml.py     # Base64 SVG embedding for exam questions
│   └── templates/
│       └── circuitikz_template.tex    # Starter template for new diagrams
├── exams/
│   └── midterm-week9/                 # Week 9 midterm (50 pts, 120 min, 15 variants)
│       ├── xml/                       # pool_q1_easy.xml ... pool_q4_difficult.xml + upload
│       └── diagrams/
│           ├── q1/ q2/ q3/ q4/        # Exported SVG + PNG per variant
│           └── scripts/               # Schemdraw .py source files (legacy)
└── weekly/
    └── week10/                        # RLC 2nd-order + magnetic circuits practice
        ├── xml/                       # Q1-Q5 STACK questions
        └── diagrams/                  # CircuiTikZ .tex + .svg per question
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
| Classification MCQs | `type="dropdown"` | Use dropdown select for regime/method classification (no "Clear my choice" clutter) |
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

## CircuiTikZ / TikZ Circuit Diagrams

All diagrams are authored as `.tex` files using **CircuiTikZ** (for circuit schematics) or plain **TikZ** (for physical/geometric drawings like magnetic core cross-sections). The `.tex` files are compiled to SVG via `pdflatex` + `pdf2svg`.

### Compilation Pipeline

```bash
# Single file
python shared/scripts/render_circuitikz.py diagram.tex [output.svg]

# Batch (all .tex in a directory)
python shared/scripts/render_circuitikz.py --all weekly/week10/diagrams/
```

**System dependencies:** `texlive-latex-base`, `texlive-pictures`, `texlive-latex-recommended`, `texlive-latex-extra`, `pdf2svg`

### .tex File Structure

```latex
\documentclass[border=10pt]{standalone}
\usepackage[american voltages, american currents]{circuitikz}
\usepackage{amsmath}
\renewcommand{\familydefault}{\sfdefault}  % sans-serif

\begin{document}
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  % Circuit drawing commands here
\end{circuitikz}
\end{document}
```

For physical/geometric diagrams (e.g., toroid cross-sections), use `\usepackage{tikz}` instead of `circuitikz`.

### Layout Rules

- **Vertical layout preferred:** Power source on left (vertical, positive on top), components arranged vertically on right
- **Sans-serif fonts** (`\sffamily`), **high-contrast** black on white
- **Explicit current arrows** and **voltage polarity markings** on every circuit
- SVG output uses `viewBox` (responsive sizing via `standalone` class)
- Use `[american voltages, american currents]` package options

### Key CircuiTikZ Components

| Component | Syntax |
|-----------|--------|
| Resistor | `to[R, l=$R$]` |
| Inductor | `to[L, l=$L$]` |
| Capacitor | `to[C, l=$C$]` |
| Voltage source | `to[V, v=$V_s$]` |
| Current source | `to[I, l=$I_s$]` |
| SPST switch (open) | `to[opening switch, l=$t{=}0$]` |
| SPST switch (closed) | `to[closing switch, l=$t{=}0$]` |
| Voltage label | `v=$v_C$` or `v^=$v_o(t)$` |
| Current arrow | `i>^=$\Phi$` |

### Complex Math Labels

CircuiTikZ's `l=` parameter doesn't handle `\dfrac` well. For labels with fractions, use separate `\node` elements:

```latex
\draw (6,4) to[R] (6,2);
\node[right, xshift=6pt] at (6,3) {$\mathcal{R} = \dfrac{\ell}{\mu_r \mu_0 A}$};
```

### Diagram Embedding

| Content type | Embedding method |
|--------------|-----------------|
| Weekly questions | Base64 SVG embedded directly in XML (`data:image/svg+xml;base64,...`) |
| Exam questions | Text placeholders `[INSERT DIAGRAM: ...]` — instructor uploads manually via Moodle editor |

### Circuits with Switches (Multi-Switch Topologies)

When a circuit has multiple switches (e.g., Nilsson P8.11 style):

**Diagram rules:**
- **Name every switch** (SW1, SW2, …) with an italic `\textit{}` label below each switch element.
- **Label the action** above each switch: `t{=}0` `(opens)` or `(closes)`.
- Use CircuiTikZ's native `opening switch` / `closing switch` elements — no manual drawing needed.
- **Leave enough horizontal space** between adjacent vertical components so that polarity/voltage labels don't visually overlap.

**XML questiontext rules:**
- **List every switch explicitly** in a bulleted `<ul>` with: switch name, location (between which components), state for `t < 0`, and state at `t = 0`.
- Example:
  ```html
  <ul>
    <li><strong>SW1</strong> (between \(R_a\) and \(L\)): <em>closed</em> for \(t &lt; 0\), <em>opens</em> at \(t = 0\).</li>
    ...
  </ul>
  ```
- Use consistent terminology: "change state" (not "flip" or "move to alternate positions") when describing what happens at `t = 0`.
- **Generalfeedback and hints** must also reference switch names (SW1, SW2, …), not abstract "switch 1 in position a" language.

**Design pattern (4-switch source-free RLC):**
- SW1, SW4 closed at `t < 0` → connect energy sources to L and C for DC charging.
- SW2, SW3 open at `t < 0` → isolate the middle RLC section.
- At `t = 0`, all switches change state → sources disconnect, L‖R‖C forms a source-free parallel RLC.

## Known Issues / Pending Work

- *(None at this time)*

## Common Mistakes to Avoid

These are hard-won lessons from previous sessions. **Do not repeat these errors:**

1. **Don't use `AlgEquiv` when reference value is 0** — `NumRelative` divides by zero. Use `NumAbsolute` with tolerance 0.01.
2. **Don't use `SigFigsStrict` as a scoring gate** — penalizes formatting, not understanding.
3. **Don't leak answers** via `syntaxhint` or textarea placeholder text. In unsupervised exams, even structural hints narrow the solution space.
4. **Verify parameter sets mathematically** before implementing. Check that `alpha` vs `omega0` produces the intended damping regime for every variant.
5. **Don't use `type="radio"` for classification MCQs** — radio buttons show an unnecessary "Clear my choice" link. Use `type="dropdown"` instead.
6. **Don't embed base64 in exam XMLs** — Moodle's HTML sanitizer strips data URIs. Use text placeholders for exams.
7. **Don't include dependent sources in Easy questions** — students find them confusing; reserve for Difficult (Q4) only.
8. **Test all parameter set variants** before committing. A single untested variant can produce wrong answers or degenerate cases.
9. **Don't use `{@ansN@}` in `<specificfeedback>`** — STACK renders these as CAS variable symbols, not student answers.
10. **Don't forget `insertstars=1`** on algebraic inputs — without it, `2t` is rejected instead of interpreted as `2*t`.
11. **Name every switch in multi-switch circuits** — unnamed switches force students to count from left to right, which is error-prone. Use SW1, SW2, … in both the diagram and the XML text.
12. **Don't use abstract switch position labels** (e.g., "position a", "position b") for SPST switches — these only make sense for SPDT (multi-throw) switches. For SPST, describe as "open" or "closed".
13. **Leave adequate spacing between adjacent vertical components** in horizontal-rail circuits — voltage/polarity labels (like `v_o(t)`) need clear visual separation from neighboring components.
15. **Don't use `\dfrac` inside CircuiTikZ `l=` labels** — it causes "Extra \endgroup" errors. Use a separate `\node` element for complex math labels instead.
14. **Keep diagram labels and XML text in sync** — if the diagram shows SW1–SW4, the questiontext, generalfeedback, and hints must all use the same names. Never mix naming conventions (e.g., "switch 1" in text vs. "SW1" in diagram).

## Last Updated

2026-03-07
