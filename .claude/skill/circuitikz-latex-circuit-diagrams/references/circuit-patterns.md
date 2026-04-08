# Circuit Patterns — Reusable CircuiTikZ Templates

Tested against CircuiTikZ v1.6.6 (TeX Live 2023). All patterns follow the project conventions in SKILL.md.

---

## 1. Series RLC (DC source, switch at t=0)

Classic second-order transient. Switch opens at t=0 (was closed for t<0).

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) to[V, v=$V_s$] (0,4)
        to[opening switch, l={\shortstack{$t{=}0$\\(opens)}}] (3,4)
        to[R, l=$R$, i=$i(t)$] (3,2)
        to[L, l=$L$, v=$v_L$] (6,2)
        to[C, l=$C$, v=$v_C$] (6,0) -- (0,0);
  \draw (3,4) -- (3,2);  % vertical wire
  \fill (0,0) circle (2pt);
  \fill (0,4) circle (2pt);
\end{circuitikz}
```

**Variant — horizontal layout:** place all components in a single loop using coordinates (0,0)→(0,3)→(3,3)→(6,3)→(6,0)→(0,0).

---

## 2. Parallel RLC (Current source)

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  % Source
  \draw (0,0) to[I, l=$I_s$, i=$i_s$] (0,3);
  % Top wire
  \draw (0,3) -- (6,3);
  % Bottom wire
  \draw (0,0) -- (6,0);
  % Parallel branches
  \draw (2,3) to[R, l=$R$, i>^=$i_R$] (2,0);
  \draw (4,3) to[L, l=$L$, i>^=$i_L$] (4,0);
  \draw (6,3) to[C, l=$C$, i>^=$i_C$, v=$v(t)$] (6,0);
  % Junctions
  \fill (0,0) circle (2pt); \fill (0,3) circle (2pt);
  \fill (2,0) circle (2pt); \fill (2,3) circle (2pt);
  \fill (4,0) circle (2pt); \fill (4,3) circle (2pt);
  \fill (6,0) circle (2pt); \fill (6,3) circle (2pt);
\end{circuitikz}
```

---

## 3. First-Order RC (DC source, switch closes at t=0)

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) to[V, v=$V_s$] (0,3)
        to[closing switch, l={\shortstack{$t{=}0$\\(closes)}}] (3,3)
        to[R, l=$R$, i=$i(t)$] (3,0)
        -- (0,0);
  \draw (3,3) -- (6,3) to[C, l=$C$, v=$v_C(t)$] (6,0) -- (3,0);
  \fill (3,3) circle (2pt);
  \fill (3,0) circle (2pt);
\end{circuitikz}
```

---

## 4. First-Order RL (DC source, switch opens at t=0)

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) to[V, v=$V_s$] (0,3)
        to[opening switch, l={\shortstack{$t{=}0$\\(opens)}}] (3,3)
        to[R, l=$R$, i=$i(t)$] (3,0)
        -- (0,0);
  \draw (3,3) -- (6,3) to[L, l=$L$, v=$v_L(t)$] (6,0) -- (3,0);
  \fill (3,3) circle (2pt);
  \fill (3,0) circle (2pt);
\end{circuitikz}
```

---

## 5. Voltage Divider

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) to[V, v=$V_s$] (0,4)
        to[R, l=$R_1$, i=$i$] (3,4)
        to[R, l=$R_2$, v=$v_o$] (3,0) -- (0,0);
  % Output terminals
  \draw (3,4) -- (5,4);
  \draw (3,0) -- (5,0);
  \draw (5,4) to[open, v^=$v_o$] (5,0);
  \fill (3,4) circle (2pt);
  \fill (3,0) circle (2pt);
\end{circuitikz}
```

---

## 6. Current Divider

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) to[I, l=$I_s$, i=$i_s$] (0,3) -- (4,3);
  \draw (0,0) -- (4,0);
  \draw (2,3) to[R, l=$R_1$, i>^=$i_1$] (2,0);
  \draw (4,3) to[R, l=$R_2$, i>^=$i_2$] (4,0);
  \fill (2,3) circle (2pt); \fill (2,0) circle (2pt);
  \fill (4,3) circle (2pt); \fill (4,0) circle (2pt);
\end{circuitikz}
```

---

## 7. Op-Amp Inverting Amplifier

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) node[left]{$v_{in}$}
        to[R, l=$R_1$, o-] (3,0)
        -- (3,0) node[op amp, anchor=-](OA){}
        (OA.out) node[right]{$v_{out}$};
  \draw (3,0) -- ++(0,1.5) to[R, l=$R_f$] (OA.out |- 0,1.5) -- (OA.out);
  \draw (OA.+) -- ++(0,-0.5) node[ground]{};
\end{circuitikz}
```

**Note:** Op-amp patterns need careful anchor management. Test-compile before extending.

---

## 8. Mutual Inductance / Ideal Transformer

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  % Primary
  \draw (0,0) to[V, v=$V_1$] (0,3)
        to[R, l=$R_1$, i=$i_1$] (3,3)
        to[L, l=$L_1$] (3,0) -- (0,0);
  % Coupling dots
  \node at (3.3,2.7) {$\bullet$};
  \node at (4.7,2.7) {$\bullet$};
  % Core lines
  \draw[thick] (3.8,0.3) -- (3.8,2.9);
  \draw[thick] (4.2,0.3) -- (4.2,2.9);
  % Secondary
  \draw (5,3) to[L, l=$L_2$] (5,0);
  \draw (5,3) to[short, i=$i_2$] (7,3) to[R, l=$R_L$, v=$v_o$] (7,0) -- (5,0);
  % M label
  \node at (4,3.5) {$M$};
\end{circuitikz}
```

---

## 9. Magnetic Circuit (Reluctance Model)

Uses the circuit analogy: MMF source, reluctance elements, flux "current."

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  % MMF source (modeled as voltage source)
  \draw (0,0) to[V, v={$\mathcal{F} = NI$}] (0,3)
        -- (3,3);
  % Reluctances (modeled as resistors)
  \draw (3,3) to[R, i>^=$\Phi$] (3,0) -- (0,0);
  \node[right, xshift=6pt] at (3,1.5) {$\mathcal{R}_{\text{core}} = \dfrac{\ell}{\mu_r \mu_0 A}$};
  % Air gap reluctance
  \draw (3,3) -- (6,3) to[R] (6,0) -- (3,0);
  \node[right, xshift=6pt] at (6,1.5) {$\mathcal{R}_{\text{gap}} = \dfrac{g}{\mu_0 A}$};
  \fill (3,3) circle (2pt);
  \fill (3,0) circle (2pt);
\end{circuitikz}
```

**Note:** This uses the `\dfrac`-in-a-`\node` workaround documented in SKILL.md.

---

## 10. Thevenin / Norton Equivalent

### Thevenin

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) to[V, v=$V_{Th}$] (0,3)
        to[R, l=$R_{Th}$, i=$i$] (3,3)
        -- (4,3);
  \draw (0,0) -- (4,0);
  \draw (4,3) to[open, v^=$v_{ab}$] (4,0);
  \node[right] at (4,3) {$a$};
  \node[right] at (4,0) {$b$};
\end{circuitikz}
```

### Norton

```latex
\begin{circuitikz}[line width=0.8pt, every node/.style={font=\sffamily}]
  \draw (0,0) to[I, l=$I_N$, i=$i_N$] (0,3) -- (4,3);
  \draw (0,0) -- (4,0);
  \draw (2,3) to[R, l=$R_N$] (2,0);
  \draw (4,3) to[open, v^=$v_{ab}$] (4,0);
  \fill (2,3) circle (2pt); \fill (2,0) circle (2pt);
  \node[right] at (4,3) {$a$};
  \node[right] at (4,0) {$b$};
\end{circuitikz}
```

---

## Tips for Extending Patterns

- **Adding ground:** `\node[ground] at (x,y) {};` or `\draw (x,y) node[ground]{};`
- **Adding labels to wires:** `\draw (a) to[short, i=$i$] (b);`
- **Controlled sources:** `to[cV, v=$\alpha v_x$]` (voltage), `to[cI, l=$\beta i_x$]` (current)
- **Dependent sources (diamond shape):** use `american controlled voltage source` for proper diamond symbol
- **Three-phase:** repeat single-phase patterns with Y-offset; label phases A, B, C
