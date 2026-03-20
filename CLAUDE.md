# Testing-Codes

<!-- BEGIN GLOBAL RULES -->

## 1. Project Identity

Owner: Cássia Almeida (she/her), Associate Professor, LUT University (Finland)
Languages: English (primary for technical work), Finnish (institutional), Portuguese (personal)
Expertise level: Senior — skip fundamentals unless asked. Precision over completeness.
Role context: Engineering educator building AI-integrated teaching tools, assessment systems, and interactive web applications for electromagnetic theory and circuit analysis students.

Active courses:
* BL30A0350 — Electromagnetism and Circuit Analysis (EM&AC)
* LES10A020 — Engineering Physics (EP, co-taught with Mikko Äijälä and Ayesha Sadiqa)

Reference textbooks:
* Ulaby — Fundamentals of Applied Electromagnetics
* Ida — Engineering Electromagnetics
* Nilsson & Riedel — Electric Circuits

Notation conflict (known): Cross-sectional area: A (Nilsson) vs. S (Ulaby). Flux linkage: λ (Nilsson) vs. Λ (Ulaby). Always use the convention of the course being worked on — ask if unclear.

## 2. Behavior Defaults

* Architecture-first: explain structure before writing code.
* Confirm intent before writing code for any non-trivial task.
* Flag risks, edge cases, and conflicts proactively — do not wait to be asked.
* Only modify explicitly requested parts. Leave everything else untouched.
* When multiple options exist, present them with tradeoffs — let Cássia decide.
* Never add new ideas to messages or documents. Never remove existing ones. Only adjust what is asked.

Tone: Professional, direct, warm, natural. No flattery. No filler.

Environment:
* OS: Windows / PowerShell
* Python: use python — not python3 (not on PATH)
* Claude Code active — use session teleport when needed; re-authenticate with /login if token expired

## 3. Self-Verification (applies to all tasks)

Before returning any output:
1. Goal analysis — State the explicit and implicit goals. What does success look like?
2. Assumption audit — List every inference made that was not directly stated in the input. For each: what was the basis, and what would change if the assumption is wrong?
3. Gap identification — What is missing, ambiguous, or likely to fall short?
4. End-to-end self-test — Test output against all stated goals and identified risks. Iterate until requirements are met and output is optimized. Do not return control until this is complete.
5. Pattern check — Before finalizing, check PATTERNS.md. If the output would trigger a known pattern, apply the documented fix automatically.

## 4. Session Protocols

### Session Open
At the start of every session, before any task work:
1. Read CLAUDE.md (this file) — confirm active constraints and project identity.
2. Read PATTERNS.md — load all accumulated corrections and rules. Treat every entry as a hard constraint, not a suggestion.
3. Read SESSION.md if present — resume from last known state.
4. Read `.claude/skill/context_evaluator/context.md` — stable architecture facts.
5. Confirm readiness: state which skills are relevant to today's work and flag any conflict between loaded files.

Do not begin task work until these steps are confirmed.
To trigger this protocol, say: **open session** or **load context**.

### Session Close
At the end of every session, before returning control:
1. Review the full session for recurring corrections or repeated assumptions — anything said more than once, or any mistake that appeared in more than one place.
2. For each pattern found:
   - Produce a concrete rule in plain language.
   - Add it to PATTERNS.md under the relevant category.
   - State: "Pattern detected: [X]. Rule added: [Y]."
3. Write SESSION.md:
   - What was completed (with file names and locations).
   - What is in progress (enough context to resume cold).
   - Open decisions or blockers.
   - Which PATTERNS.md entries were triggered today.
4. If any SKILL.md should be updated based on today's work, state the proposed change explicitly and ask for confirmation before writing.

To trigger this protocol, say: **close session** or **wrap up**.

## 5. Cross-Skill Rules

These apply to all skills. Skills do not repeat them.

### Writing and communication
* Never use: "flagging", "thanks for flagging" — use "thanks for the heads-up" or "thanks for pointing that out"
* Email sign-off: "Best regards," — never "Best,"
* Sign as: "Cássia" — never full name in sign-off
* Anti-AI banned words: "crucial", "vital", "leverage", "delve", "navigate", "landscape", "groundbreaking", "game-changer", "it's worth noting", "at the end of the day", "in conclusion"

### Code
* Confirm intent before writing non-trivial code
* Explain architectural choices when making decisions that affect structure
* Flag performance and edge cases proactively

### Files and structure
* Check PATTERNS.md before starting any task in a known domain
* Session state lives in SESSION.md — write it at close, read it at open
* Never duplicate content between CLAUDE.md and a SKILL.md — reference by name

## 6. Skill Index

| Skill | Trigger | File |
|-------|---------|------|
| context-evaluator | STACK, Moodle, session management, context loading | .claude/skill/context_evaluator/SKILL.md |
| circuitikz-circuit-diagrams | circuit diagram, draw circuit, CircuiTikZ, LaTeX circuit | .claude/skill/circuitikz-latex-circuit-diagrams/SKILL.md |

<!-- END GLOBAL RULES -->

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
├── CLAUDE.md                          # This file — global rules + repo-specific conventions
├── PATTERNS.md                        # Accumulated corrections and rules (living memory)
├── SESSION.md                         # Current session state (overwritten each close)
├── .claude/skill/
│   ├── context_evaluator/             # Project management context (session tracking, decisions)
│   └── circuitikz-latex-circuit-diagrams/ # Circuit diagram generation skill + references
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
    ├── week10/                        # RLC 2nd-order + magnetic circuits practice
    │   ├── xml/                       # Q1-Q5 STACK questions
    │   └── diagrams/                  # CircuiTikZ .tex + .svg per question
    ├── week11/                        # Electromagnetic induction (Faraday's law, motional EMF, self-inductance)
    │   ├── xml/                       # Q1-Q2 (induction) + Q5 (self-inductance & energy)
    │   └── diagrams/                  # TikZ/CircuiTikZ .tex + .svg per question
    └── week12/                        # Coupled inductors & ideal transformers
        ├── xml/                       # Q3-Q4 (aiding + transformer) + Q5 (opposing + energy)
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
| Numerical (may contain π) | Add: `You may also use <code>%pi</code> for π, e.g. <code>0.2*%pi</code>.` |
| Symbolic / algebraic | Show complete example with expected variables, e.g. `Write <code>lc/(mur*mu0*Ac)</code>`. **Always** state how to type special symbols: `<code>mu0</code> for μ₀`, `<code>mur</code> for μᵣ`, `<code>%pi</code> for π`. |
| Expression (function of t) | `Use <code>exp(...)</code>, <code>sin(...)</code>, <code>cos(...)</code>, and <code>t</code>.` Include a complete example matching the expected form. |
| Complex roots (with j) | `For complex roots use <code>j</code> for the imaginary unit, e.g. <code>-2800+9600*j</code>` |
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
| Classification MCQs (short labels) | `type="dropdown"` | Compact for single-word/short-phrase options (e.g., "Overdamped"/"Underdamped"/"Critically damped") |
| Reasoning MCQs (long text) | `type="radio"` | Full option text always visible; dropdowns truncate long descriptions |
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

## PRT Validation Methodology (Multi-Tiered)

Before committing any STACK XML, validate **every PRT** using this checklist:

### Tier 1 — Structural Integrity
- [ ] **Node chain completeness:** Every `truenextnode` / `falsenextnode` points to an existing node name or `-1` (exit). No dangling references.
- [ ] **No orphan nodes:** Every node is reachable from node 0 (root) in each PRT.
- [ ] **Feedbackvariables defined:** All variables referenced in PRT node tests (`sans`, `tans`, or boolean flags) are defined either in the PRT's `<feedbackvariables>` or in `<questionvariables>`.

### Tier 2 — Grading Correctness
- [ ] **NumAbsolute for zero:** Any PRT where the expected answer is 0 uses `NumAbsolute` (tolerance 0.01), never `NumRelative`.
- [ ] **NumRelative fallback on symbolic PRTs:** Any `AlgEquiv` node that evaluates to a numerical value has a fallback node with `NumRelative` (5%) against `float()`.
- [ ] **Score consistency:** Typical pattern is 1.0 (exact/5%), 0.7 (close/15%), 0.3 (order-of-magnitude), 0.0 (wrong).
- [ ] **No `SigFigsStrict` as scoring gate.**
- [ ] **No `{@ansN@}` in specificfeedback** — use `[[feedback:prtN]]` only.

### Tier 3 — XML/CAS Safety
- [ ] **CDATA wrapping:** All `<feedbackvariables>` blocks containing `<` comparison operators are wrapped in `<![CDATA[...]]>`.
- [ ] **Penalty settings:** Question-level and per-node penalty values are intentional (typically 0 for practice, >0 for exams).
- [ ] **`insertstars=1`** on all algebraic inputs.
- [ ] **Exact arithmetic:** No floating-point constants (`1e-7`) in expressions involving symbolic constants (`%pi`).

### Tier 4 — Pedagogical Quality
- [ ] **Syntax hints present** after every `[[input:ansN]]` with type-appropriate text.
- [ ] **Progressive hints** (2-3 `<hint>` elements) at the end of each `<question>` block.
- [ ] **Diagram-text sync:** Component names in diagrams match XML text exactly.
- [ ] **No answer leaks** via `syntaxhint`, placeholder text, or hint content.

## Known Issues / Pending Work

### Progressive Hint Unlocking (Next Step)
- **Goal:** Implement STACK's `[[if test="..."]]` conditional blocks to reveal hints progressively based on student attempt count or score, rather than showing all hints at once.
- **Approach:** Use `\{#attempts#\}` or PRT score variables to gate hint visibility.
- **Scope:** Apply to all weekly questions first (Q1-Q5), then evaluate for exam use.
- **Status:** Not yet started — planned for next session.

## Workflow Guidelines — Task Decomposition

**Always plan before building.** Before starting any question set, create a plan first (use the Plan agent or outline the structure). Then execute in small, parallelizable chunks.

### STACK Questions
- **1–2 questions per agent** — never generate a full question set in one task
- Separate concerns for complex questions:
  - Variable randomization & Maxima logic
  - Solution derivation & worked examples
  - PRT/feedback tree structure
  - Maxima grading code
- Validate each question independently before bundling into a quiz

### CircuiTikZ / TikZ Diagrams
- **1 diagram per agent** — each `.tex` file is an independent task
- Run all diagram agents in parallel
- Compile and visually inspect each before embedding

### General Principles
- Smaller tasks = faster completion, easier debugging, better parallelization
- If a single agent task takes >2 minutes, it should be split further
- Always maximize parallel agent execution for independent tasks
- Plan the full question set structure before generating any XML

## Visual Style & Diagram Resources — Must Read Before Building

Before creating any diagram or visual content, read these files:

| Resource | Path | When to Read |
|----------|------|-------------|
| **CircuiTikZ skill** | `.claude/skill/circuitikz-latex-circuit-diagrams/SKILL.md` | Before creating any circuit diagram — compilation pipeline, .tex structure, layout rules |
| **Circuit patterns** | `.claude/skill/circuitikz-latex-circuit-diagrams/references/circuit-patterns.md` | Before drawing circuits — 8 standard topology templates, switch naming, spacing tips |
| **Render script** | `shared/scripts/render_circuitikz.py` | For compiling .tex → SVG |
| **CircuiTikZ template** | `shared/templates/circuitikz_template.tex` | Starter template for new diagrams |

### Diagram Style Rules (CircuiTikZ / TikZ)
- **Sans-serif fonts** (`\sffamily`) — high contrast, black on white
- **Vertical layout preferred** — power source on left (positive on top), components on right
- **Explicit current arrows and voltage polarity** on every circuit
- **`[american voltages, american currents]`** package options always
- **`standalone` with `border=10pt`** — prevents label/arrow clipping
- **Name every switch** (SW1, SW2, …) with italic labels; element name = action at t=0
- **No `\dfrac` in `l=` labels** — use separate `\node` for complex math
- **Adequate spacing** between adjacent vertical components for polarity labels

### Diagram Types for Questions
| Type | Tool | Notes |
|------|------|-------|
| Circuit schematics | CircuiTikZ (`.tex`) | Use circuit-patterns.md templates |
| Magnetic core cross-sections | TikZ (`.tex`) | Use `\usepackage{tikz}` instead of circuitikz |
| Physical/geometric drawings | TikZ (`.tex`) | Toroid windings, field lines, etc. |
| Flowcharts / decision trees | TikZ (`.tex`) | Rounded rectangles, diamonds, arrows |
| Embedding in weekly XML | Base64 SVG | `data:image/svg+xml;base64,...` |
| Embedding in exam XML | Text placeholder | Instructor uploads manually via Moodle |

## Last Updated

2026-03-20 (session 5: integrated 3-file context system — CLAUDE.md, PATTERNS.md, SESSION.md)
