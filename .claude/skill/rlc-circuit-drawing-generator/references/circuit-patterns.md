# Circuit Topology Patterns — CircuiTikZ

Common circuit patterns and their CircuiTikZ implementations.

**Important**:
- **Preferred layout**: Vertical component arrangement on the right side
- **Sans-serif fonts**: `\sffamily` throughout, `[american voltages, american currents]` package options
- **Explicit markings**: Current arrows and voltage polarities on every circuit
- **Complex labels**: Use `\node` for `\dfrac` — don't put fractions in `l=` parameter

## Pattern 1: Simple Single-Component Circuit

A voltage source with one component (resistor, capacitor, or inductor).

```latex
\documentclass[border=10pt]{standalone}
\usepackage[american voltages, american currents]{circuitikz}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]

\draw (0,0) to[V, v=$V_s$] (0,4);
\draw (0,4) -- (4,4);
\draw (4,4) to[R, l_=$R$] (4,0);
\draw (4,0) -- (0,0);

\end{circuitikz}
\end{document}
```

## Pattern 2: Series RC Circuit

```latex
\draw (0,0) to[V, v=$V_s$] (0,4);
\draw (0,4) -- (4,4);
\draw (4,4) to[R, l_=$R$] (4,2)
            to[C, l_=$C$, v^=$v_C$] (4,0);
\draw (4,0) -- (0,0);
```

## Pattern 3: Series RLC Circuit

```latex
\draw (0,0) to[V, v=$V_s$] (0,4);
\draw (0,4) -- (6,4);
\draw (6,4) to[R, l_=$R$] (6,2.7)
            to[L, l_=$L$] (6,1.3)
            to[C, l_=$C$, v^=$v_C$] (6,0);
\draw (6,0) -- (0,0);
```

## Pattern 4: Parallel RLC Circuit

Three parallel branches with junction dots.

```latex
\draw (0,0) to[I, l=$I_s$] (0,4);
\draw (0,4) -- (2,4);

% Junction dots
\fill (2,4) circle (2pt);
\fill (5,4) circle (2pt);
\fill (8,4) circle (2pt);

% Branch 1: Resistor
\draw (2,4) to[R, l_=$R$] (2,0);

% Branch 2: Inductor
\draw (5,4) to[L, l_=$L$, i>_=$i_L$] (5,0);

% Branch 3: Capacitor
\draw (8,4) to[C, l_=$C$] (8,0);

% Rails
\draw (2,4) -- (5,4) -- (8,4);
\draw (0,0) -- (2,0) -- (5,0) -- (8,0);

% Voltage label
\draw (1,4) to[open, v^=$v(t)$] (1,0);
```

## Pattern 5: Circuit with Switch

Using native `opening switch` / `closing switch` elements.

```latex
\draw (0,0) to[V, v=$V_s$] (0,4);
\draw (0,4) -- (2,4)
      to[opening switch, l=$t{=}0$ (opens)] (4,4)
      -- (6,4);
\draw (6,4) to[R, l_=$R$] (6,2)
            to[L, l_=$L$] (6,0);
\draw (6,0) -- (0,0);
```

## Pattern 6: Multi-Switch Circuit

Name every switch with `\textit{}` labels.

```latex
% SW1: closed, opens at t=0
\draw (2,4) -- (3,4)
      to[closing switch, l={\shortstack{$t{=}0$\\(opens)}}] (5,4);
\node[font=\sffamily\small\itshape, below, yshift=-4pt] at (4,4) {SW1};

% SW2: open, closes at t=0
\draw (6,4)
      to[opening switch, l={\shortstack{$t{=}0$\\(closes)}}] (8,4);
\node[font=\sffamily\small\itshape, below, yshift=-4pt] at (7,4) {SW2};
```

## Pattern 7: Reluctance Circuit (Magnetic Circuit Analogy)

MMF source as voltage source, reluctances as resistors, flux as current.

```latex
\draw (0,0) to[V, v=$NI$ (MMF)] (0,4);
\draw (0,4) -- (7,4);
\draw (7,4) to[R, i>^=$\Phi$] (7,2);
\node[right, xshift=6pt] at (7,3) {$\mathcal{R}_{\mathrm{core}} = \dfrac{\ell_c}{\mu_r \mu_0 A_c}$};
\draw (7,2) to[R] (7,0);
\node[right, xshift=6pt] at (7,1) {$\mathcal{R}_{\mathrm{gap}} = \dfrac{\ell_g}{\mu_0 A_c}$};
\draw (7,0) -- (0,0);
```

## Pattern 8: Voltage Divider

```latex
\draw (0,0) to[V, v=$V_{in}$] (0,4);
\draw (0,4) -- (4,4);
\draw (4,4) to[R, l=$R_1$] (4,2);

% Output tap
\fill (4,2) circle (2pt);
\draw (4,2) -- (5.5,2) node[right]{$V_{out}$};

\draw (4,2) to[R, l=$R_2$] (4,0);
\draw (4,0) -- (0,0);
```

## Tips for Clean Layouts

1. **Coordinate-based drawing**: CircuiTikZ uses explicit (x,y) coordinates — plan your layout on paper first
2. **Consistent spacing**: Use integer or half-integer coordinates for alignment
3. **Junction dots**: Always add `\fill (x,y) circle (2pt)` at parallel branch junctions
4. **Node labels**: Use `\node[position]` for complex labels instead of `l=` parameter
5. **Switch naming**: Always label switches with `\textit{SW1}`, `\textit{SW2}`, etc.
6. **Voltage polarity**: Use `v=$v_C$` for inline labels, or `to[open, v^=$v(t)$]` for gap-based labels
