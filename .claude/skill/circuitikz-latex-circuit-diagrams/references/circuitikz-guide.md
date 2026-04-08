# CircuiTikZ Component Reference

Tested against CircuiTikZ v1.6.6 (TeX Live 2023). American style conventions.

---

## Package Setup

```latex
\usepackage[american voltages, american currents]{circuitikz}
```

Key options: `american voltages` gives +/- signs (not arrows), `american currents` gives conventional flow arrows.

---

## Passive Components

| Component | Syntax | Notes |
|-----------|--------|-------|
| Resistor (zigzag) | `to[R, l=$R$]` | American style default |
| Resistor (box/European) | `to[R, european]` | Or set globally |
| Inductor | `to[L, l=$L$]` | American coil symbol |
| Capacitor | `to[C, l=$C$]` | Two parallel lines |
| Polar capacitor | `to[eC, l=$C$]` | Electrolytic, curved plate |
| Variable resistor | `to[vR, l=$R$]` | Arrow through resistor |
| Potentiometer | `to[pR, l=$R$]` | Three-terminal |
| Fuse | `to[fuse, l=$F$]` | |

---

## Sources

| Component | Syntax | Notes |
|-----------|--------|-------|
| DC voltage | `to[V, v=$V_s$]` | Circle with +/- |
| AC voltage | `to[sinusoidal voltage source, v=$V_s$]` | Circle with sine wave |
| DC current | `to[I, l=$I_s$]` | Circle with arrow |
| Battery | `to[battery1, v=$9\,\text{V}$]` | Single cell |
| Controlled voltage | `to[cV, v=$\alpha v_x$]` | Diamond shape |
| Controlled current | `to[cI, l=$\beta i_x$]` | Diamond shape |
| American controlled voltage | `to[american controlled voltage source]` | Explicit diamond |

---

## Switches

| Component | Syntax | Meaning at t=0 |
|-----------|--------|----------------|
| Opening switch | `to[opening switch]` | Was closed, now opens |
| Closing switch | `to[closing switch]` | Was open, now closes |
| Normal open | `to[nos]` | Open contact |
| Normal closed | `to[ncs]` | Closed contact |

**Convention:** The element name describes the *action*, not the state before t=0.

Multi-line switch label:
```latex
to[opening switch, l={\shortstack{$t{=}0$\\(opens)}}]
```

---

## Labels and Annotations

### Component Labels

| Syntax | Position |
|--------|----------|
| `l=$R$` | Default side (above/right for horizontal, right for vertical) |
| `l_=$R$` | Opposite side |

### Voltage Labels

| Syntax | Polarity |
|--------|----------|
| `v=$v_C$` | + at start node, - at end node |
| `v^=$v_C$` | Reversed: + at end, - at start |
| `v_=$v_C$` | Opposite side placement |

### Current Arrows

| Syntax | Direction |
|--------|-----------|
| `i=$i$` | Along component, default direction |
| `i>=$i$` | Explicit rightward/downward |
| `i<=$i$` | Explicit leftward/upward |
| `i>^=$i$` | Arrow with label on opposite side |

---

## Wires and Connections

| Element | Syntax |
|---------|--------|
| Plain wire | `to[short]` or `--` |
| Wire with current | `to[short, i=$i$]` |
| Open circuit | `to[open, v^=$v$]` |
| Short circuit | `to[short]` |
| Junction dot | `\fill (x,y) circle (2pt);` |
| Ground | `\node[ground] at (x,y) {};` |
| Chassis ground | `\node[cground] at (x,y) {};` |

---

## Semiconductors

| Component | Syntax |
|-----------|--------|
| Diode | `to[D, l=$D$]` |
| Zener | `to[zD]` |
| LED | `to[leDo]` |
| NPN BJT | `node[npn](Q1){}` |
| PNP BJT | `node[pnp](Q1){}` |
| N-MOSFET | `node[nmos](M1){}` |
| P-MOSFET | `node[pmos](M1){}` |
| Op-amp | `node[op amp](OA){}` |

Transistors and op-amps use `node` syntax with anchors (`.B`, `.C`, `.E` for BJT; `.+`, `.-`, `.out` for op-amp).

---

## Complex Labels Workaround

CircuiTikZ's `l=` chokes on `\dfrac`. Use a separate `\node`:

```latex
\draw (6,4) to[R] (6,2);
\node[right, xshift=6pt] at (6,3) {$\mathcal{R} = \dfrac{\ell}{\mu_r \mu_0 A}$};
```

This also works for any multi-line or complex math that breaks inside `l=`.

## Equals Signs Inside Labels

If a label value contains `=`, the key-value parser breaks. **Wrap in braces**:

```latex
% WRONG
to[V, v=$V = IR$]

% CORRECT
to[V, v={$V = IR$}]
```

Applies to `l=`, `v=`, `i=` parameters. Rule: if the label has `=`, brace it.

---

## Coordinate and Layout Tips

1. **Grid-based:** Use integer or half-integer coordinates for alignment.
2. **Vertical source:** Place voltage source on the left, positive terminal on top.
3. **Adequate spacing:** Leave at least 2 units between parallel vertical branches so labels don't overlap.
4. **Named coordinates:** Use `coordinate(name)` for reuse:
   ```latex
   \draw (0,3) to[R, l=$R$] (3,3) coordinate(A);
   \draw (A) to[L, l=$L$] (A |- 0,0);
   ```
5. **Relative positioning:** `++(dx,dy)` moves from current position, `+(dx,dy)` is relative but doesn't update position.

---

## Color and Style

```latex
% Colored component
\draw[red] (0,0) to[R, l=$R$, color=red] (3,0);

% Thick wire
\draw[line width=1.5pt] (0,0) -- (3,0);

% Dashed wire
\draw[dashed] (0,0) -- (3,0);

% Annotation arrow
\draw[->, thick, blue] (2,1) -- (2,2) node[above]{$\vec{B}$};
```

---

## Units in Labels

Use `\,` thin space before unit text:

```latex
l=$R = 100\,\Omega$
l=$C = 10\,\mu\text{F}$
l=$L = 5\,\text{mH}$
v=$V_s = 12\,\text{V}$
```

---

## Version Notes

- **v1.6.x:** `eC` for electrolytic capacitor is stable. `sinusoidal voltage source` is the canonical AC source name.
- **v1.4+:** `opening switch` / `closing switch` are available. Older versions use `open` / `close`.
- **v1.0+:** `american voltages` / `american currents` package options available.

If you encounter unknown component errors, check `\pgfcircversion` in your TeX installation.
