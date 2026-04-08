---
name: circuitikz-circuit-diagrams
version: 2.1.0
description: >
  Use when: drawing circuit diagrams, creating circuit schematics,
  CircuiTikZ, TikZ, LaTeX circuit, "draw a circuit", "create a diagram",
  RLC circuit visualization, magnetic core diagram, toroid cross-section,
  reluctance circuit, switch topology, circuit with components.
---

# CircuiTikZ LaTeX Circuit Diagrams

This skill generates professional circuit diagrams from natural language descriptions using CircuiTikZ (LaTeX) for circuit schematics and TikZ for physical/geometric diagrams (e.g., magnetic core cross-sections).

**Target version:** CircuiTikZ v1.6.x (TeX Live 2023). Check with `\pgfcircversion` if unsure.

## When to Use This Skill

- User asks to draw or create a circuit diagram
- User describes a circuit with resistors, capacitors, inductors, switches, or power sources
- User needs an educational circuit illustration
- User wants to visualize a circuit topology (series, parallel, mixed)
- User needs a magnetic circuit or physical core diagram

## Workflow

### Step 0 — Install pdf2svg (once per session)

```bash
apt-get install -y pdf2svg
```

This is not pre-installed in the container. Takes ~10 seconds. pdflatex and texlive packages are already available.

### Step 1 — Parse the circuit description

Identify components, values, topology, and any switching actions.

### Step 2 — Determine layout

Plan coordinate grid. Vertical source on the left (positive terminal on top) is the default. Check `references/circuit-patterns.md` for reusable topologies.

### Step 3 — Generate the .tex file

Create the LaTeX source in `/home/claude/`. Use the conventions below and consult `references/circuitikz-guide.md` for component syntax.

### Step 4 — Compile to SVG

```bash
SKILL_DIR=/mnt/skills/user/circuitikz-circuit-diagrams
python "$SKILL_DIR/scripts/render_circuitikz.py" diagram.tex
```

Or compile manually:

```bash
cd /home/claude
pdflatex -interaction=nonstopmode -halt-on-error diagram.tex
pdf2svg diagram.pdf diagram.svg
```

### Step 5 — Deliver to user

```bash
cp /home/claude/diagram.svg /mnt/user-data/outputs/diagram.svg
```

Then call `present_files` with the output path. **This step is mandatory** — without it, the user never receives the file.

Optionally also deliver the `.tex` source so the user can edit it later.

## Input Format

Users can describe circuits in natural language:
- "Draw a series RLC circuit with R=100 ohm, L=10mH, C=1uF powered by 12V DC"
- "Create a parallel RLC with a switch that opens at t=0"
- "Show a toroidal core with N turns and an air gap"

## .tex File Structure

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

For physical/geometric diagrams (toroid cross-sections, C-cores), use `\usepackage{tikz}` instead.

## Layout Conventions

- **Vertical layout preferred**: Power source on left (vertical, positive terminal on top), components arranged vertically on right side
- **Sans-serif fonts**: `\sffamily` throughout, `\renewcommand{\familydefault}{\sfdefault}`
- **American style**: `[american voltages, american currents]`
- **Line width**: `line width=0.8pt`
- **Border**: `\documentclass[border=10pt]{standalone}` — without border, labels get clipped at SVG edges
- **Explicit markings**: Current arrows and voltage polarity markings on every circuit
- **High-contrast**: Black lines on white background
- **Adequate spacing**: Leave at least 2 coordinate units between parallel vertical branches so labels don't overlap

## Key CircuiTikZ Components

| Component | Syntax |
|-----------|--------|
| Resistor | `to[R, l=$R$]` |
| Inductor | `to[L, l=$L$]` |
| Capacitor | `to[C, l=$C$]` |
| Polar Capacitor | `to[eC, l=$C$]` |
| DC Voltage source | `to[V, v=$V_s$]` |
| AC Voltage source | `to[sinusoidal voltage source, v=$V_s$]` |
| Current source | `to[I, l=$I_s$]` |
| Battery | `to[battery1, v=$9V$]` |
| SPST switch (opening) | `to[opening switch, l=$t{=}0$]` |
| SPST switch (closing) | `to[closing switch, l=$t{=}0$]` |
| Normal open | `to[nos]` |
| Normal closed | `to[ncs]` |
| Voltage label | `v=$v_C$` or `v^=$v_o(t)$` |
| Current arrow | `i>^=$\Phi$` |
| Junction dot | `\fill (x,y) circle (2pt);` |
| Open circuit voltage | `to[open, v^=$v(t)$]` |

## Switch Conventions

- **Element name = action at t=0**: `opening switch` = was closed, now opening (breaking contact). `closing switch` = was open, now closing (making contact). Don't confuse the element name with the state *before* t=0.
- **Name every switch**: Label with `\textit{SW1}`, `\textit{SW2}`, etc. using a `\node` below the switch element.
- **Label the action**: Show `t{=}0` and `(opens)` or `(closes)` above each switch.
- Use `\shortstack` for multi-line switch labels.

## Complex Math Labels (Important)

CircuiTikZ's `l=` parameter doesn't handle `\dfrac` well — causes "Extra \endgroup" errors. For labels with fractions, use separate `\node` elements:

```latex
\draw (6,4) to[R] (6,2);
\node[right, xshift=6pt] at (6,3) {$\mathcal{R} = \dfrac{\ell}{\mu_r \mu_0 A}$};
```

## Equals Signs Inside Labels (Common Gotcha)

If a label value contains `=`, CircuiTikZ's key-value parser breaks. **Wrap the entire value in braces**:

```latex
% WRONG — parser sees two = signs and chokes
to[V, v=$\mathcal{F} = NI$]

% CORRECT — braces protect the content
to[V, v={$\mathcal{F} = NI$}]
```

This applies to `l=`, `v=`, and `i=` parameters. Safe rule: if the label contains `=`, always brace it.

## Multi-line Labels

Use `\shortstack` for multi-line component labels:

```latex
to[opening switch, l={\shortstack{$t{=}0$\\(opens)}}]
```

## Label Positioning

- `l=$R$` — label above/right (default position)
- `l_=$R$` — label below/left (opposite side)
- `v=$v_C$` — voltage label (+ at start, - at end)
- `v^=$v_C$` — voltage label (reversed polarity)
- `i=$i$` — current arrow along component
- `i>^=$\Phi$` — current arrow with explicit direction

## Physical/Geometric Diagrams (TikZ)

For non-circuit diagrams (toroid cross-sections, C-cores):

```latex
\documentclass[border=10pt]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}
\begin{tikzpicture}[every node/.style={font=\sffamily}, >=stealth]
  \fill[gray!40, draw=black] ...  % Core material
  \draw[->, red!70!black, thick] ...  % Flux arrows
\end{tikzpicture}
\end{document}
```

- **Flux arrows**: `red!70!black` color for magnetic flux
- **Core material**: `gray!40` fill for ferromagnetic cores

## Compilation

```bash
SKILL_DIR=/mnt/skills/user/circuitikz-circuit-diagrams

# Single file
python "$SKILL_DIR/scripts/render_circuitikz.py" diagram.tex [output.svg]

# Batch (all .tex in a directory)
python "$SKILL_DIR/scripts/render_circuitikz.py" --all directory/
```

**System dependencies:** `texlive-latex-base`, `texlive-pictures`, `texlive-latex-recommended`, `texlive-latex-extra`, `pdf2svg`

Install on Debian/Ubuntu:
```bash
apt-get install -y texlive-latex-base texlive-pictures texlive-latex-recommended texlive-latex-extra pdf2svg
```

## Output and Delivery

- **Format**: SVG (compiled from PDF via pdf2svg)
- **Working directory**: `/home/claude/` for .tex and intermediate files
- **Output directory**: Copy final `.svg` (and optionally `.tex`) to `/mnt/user-data/outputs/`
- **Present to user**: Always call `present_files` with the output path(s)

## Diagram Types

| Type | Tool | Notes |
|------|------|-------|
| Circuit schematics | CircuiTikZ (`.tex`) | Use circuit-patterns.md templates |
| Magnetic core cross-sections | TikZ (`.tex`) | Use `\usepackage{tikz}` instead of circuitikz |
| Physical/geometric drawings | TikZ (`.tex`) | Toroid windings, field lines, etc. |
| Flowcharts / decision trees | TikZ (`.tex`) | Rounded rectangles, diamonds, arrows |

## Multi-Switch Topologies

When a circuit has multiple switches (e.g., 4-switch source-free RLC):

**Diagram rules:**
- **Name every switch** (SW1, SW2, ...) with an italic `\textit{}` label below each switch element.
- **Label the action** above each switch: `t{=}0` `(opens)` or `(closes)`.
- Use CircuiTikZ's native `opening switch` / `closing switch` elements.
- **Leave enough horizontal space** between adjacent vertical components so polarity/voltage labels don't overlap.

**Design pattern (4-switch source-free RLC):**
- SW1, SW4 closed at `t < 0` → connect energy sources to L and C for DC charging.
- SW2, SW3 open at `t < 0` → isolate the middle RLC section.
- At `t = 0`, all switches change state → sources disconnect, forming a source-free parallel RLC.

## Tips for Clean Layouts

1. **Coordinate-based drawing**: Plan layout on paper first, use explicit (x,y) coordinates
2. **Consistent spacing**: Use integer or half-integer coordinates for alignment
3. **Junction dots**: Always add `\fill (x,y) circle (2pt)` at parallel branch junctions
4. **Node labels**: Use `\node[position]` for complex labels instead of `l=` parameter
5. **Adequate spacing**: Leave enough horizontal space between adjacent vertical components so voltage/polarity labels don't overlap
6. **Test compilation**: Always compile `.tex` to SVG and visually inspect before delivering

## Reference Files

- `references/circuitikz-guide.md` — Component syntax, labels, semiconductors, styling
- `references/circuit-patterns.md` — 10 reusable topology templates (series/parallel RLC, dividers, Thevenin/Norton, transformers, magnetic circuits)
- `scripts/render_circuitikz.py` — Compilation script (.tex to .svg) with auto-install and batch mode
- `templates/circuitikz_template.tex` — Starter template for new diagrams
