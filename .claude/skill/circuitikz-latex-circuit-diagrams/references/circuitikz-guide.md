# CircuiTikZ Reference Guide

Quick reference for generating circuit diagrams with CircuiTikZ (LaTeX).

## System Dependencies

```bash
apt-get install -y texlive-latex-base texlive-pictures texlive-latex-recommended texlive-latex-extra pdf2svg
```

## Basic .tex Structure

```latex
\documentclass[border=10pt]{standalone}
\usepackage[american voltages, american currents]{circuitikz}
\usepackage{amsmath}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  % Drawing commands here
\end{circuitikz}
\end{document}
```

## Compilation

```bash
python shared/scripts/render_circuitikz.py input.tex [output.svg]
python shared/scripts/render_circuitikz.py --all directory/
```

## Power Sources

| Component | Syntax | Description |
|-----------|--------|-------------|
| DC Voltage | `to[V, v=$V_s$]` | Circle with + and - |
| AC Voltage | `to[sinusoidal voltage source, v=$V_s$]` | Circle with sine wave |
| Current | `to[I, l=$I_s$]` | Circle with arrow |
| Battery | `to[battery1, v=$9V$]` | Long/short line pair |

## Passive Components

| Component | Syntax | Description |
|-----------|--------|-------------|
| Resistor | `to[R, l=$R$]` | Zigzag (American) |
| Capacitor | `to[C, l=$C$]` | Two parallel plates |
| Polar Capacitor | `to[eC, l=$C$]` | With polarity |
| Inductor | `to[L, l=$L$]` | Coil loops |
| Inductor (European) | `to[cute inductor, l=$L$]` | Filled rectangle |

## Switches

| Component | Syntax | Description |
|-----------|--------|-------------|
| Opening switch | `to[opening switch, l=$t{=}0$]` | Switch shown opening |
| Closing switch | `to[closing switch, l=$t{=}0$]` | Switch shown closing |
| Normal open | `to[nos]` | Normally open switch |
| Normal closed | `to[ncs]` | Normally closed switch |

## Drawing Paths

### Components along a path
```latex
\draw (0,0) to[R, l=$R$] (4,0);     % Horizontal resistor
\draw (4,4) to[C, l_=$C$] (4,0);    % Vertical capacitor (label left)
```

### Wire
```latex
\draw (0,4) -- (4,4);               % Simple wire connection
```

### Junction dot
```latex
\fill (4,4) circle (2pt);           % Filled dot at junction
```

## Label Positioning

- `l=$R$` — label above/right (default position)
- `l_=$R$` — label below/left (opposite side)
- `v=$v_C$` — voltage label (+ at start, - at end)
- `v^=$v_C$` — voltage label (reversed polarity)
- `i=$i$` — current arrow along component
- `i>^=$\Phi$` — current arrow with explicit direction

## Complex Labels (IMPORTANT)

`\dfrac` inside `l=` causes "Extra \endgroup" errors. Use `\node` instead:

```latex
\draw (6,4) to[R] (6,2);
\node[right, xshift=6pt] at (6,3) {$\mathcal{R} = \dfrac{\ell}{\mu_r \mu_0 A}$};
```

## Multi-line Labels

Use `\shortstack` for multi-line component labels:

```latex
to[opening switch, l={\shortstack{$t{=}0$\\(closes)}}]
```

## Open Circuit (Voltage Label Across Gap)

```latex
\draw (1,4) to[open, v^=$v(t)$] (1,0);
```

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

## Project Conventions

- **Sans-serif**: `\renewcommand{\familydefault}{\sfdefault}` + `every node/.style={font=\sffamily}`
- **American style**: `[american voltages, american currents]`
- **Line width**: `line width=0.8pt`
- **Border**: `\documentclass[border=10pt]{standalone}`
- **Switch names**: Always label with `\textit{SW1}`, `\textit{SW2}`, etc.
- **Flux arrows**: `red!70!black` color for magnetic flux
- **Core material**: `gray!40` fill for ferromagnetic cores

## Complete Example

```latex
\documentclass[border=10pt]{standalone}
\usepackage[american voltages, american currents]{circuitikz}
\usepackage{amsmath}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]

% Voltage source
\draw (0,0) to[V, v=$V_s$] (0,4);

% Top rail with switch
\draw (0,4) -- (2,4)
      to[opening switch, l=$t{=}0$ (opens)] (4,4)
      -- (6,4);

% Series R-L-C
\draw (6,4) to[R, l_=$R$] (6,2.7)
            to[L, l_=$L$] (6,1.3)
            to[C, l_=$C$, v^=$v_C$] (6,0);

% Bottom return
\draw (6,0) -- (0,0);

% Current arrow
\draw[->, >=stealth, thick] (4.3,4.3) -- (5.5,4.3) node[midway, above]{$i(t)$};

\end{circuitikz}
\end{document}
```
