---
name: rlc-circuit-drawing-generator
description: Generates RLC circuit diagrams from text descriptions using Schemdraw. Use this skill when the user wants to create circuit drawings for educational purposes, particularly for AC/DC circuits with resistors, capacitors, inductors, and power sources.
---

# RLC Circuit Drawing Generator

This skill generates professional circuit diagrams from natural language descriptions using Python's Schemdraw library.

## When to Use This Skill

- User asks to draw or create a circuit diagram
- User describes a circuit with resistors, capacitors, inductors, or power sources
- User needs an educational circuit illustration
- User wants to visualize an RLC circuit topology

## Workflow

1. **Parse the circuit description** - Identify components, values, and topology
2. **Determine layout** - Series, parallel, or mixed arrangement
3. **Generate Schemdraw code** - Create Python script using library conventions
4. **Render to image** - Execute script to produce SVG output

## Input Format

Users can describe circuits in natural language:
- "Draw a series RLC circuit with R=100Ω, L=10mH, C=1μF powered by 12V DC"
- "Create an RC low-pass filter with a 10kΩ resistor and 100nF capacitor"
- "Show a parallel LC circuit with L=1mH and C=100pF"

## Layout Convention

**Preferred layout**: Vertical component arrangement on the right side.

```
    ┌───────────────────┐
    │                   │
   (+)                [R₁]
  (SRC)                 │
   (-)                [L₁]
    │                   │
    └────────⏚────────[C₁]
           (GND)        │
                        │
```

- **Power source**: Vertical on left side, positive terminal on top
- **Components**: Arranged vertically on the right side using `.down()`
- **Ground**: Reference point on the return path (bottom)
- **Labels**: Include component designators and values (R₁  10kΩ) - use explicit positioning with `ofst` to avoid overlap (see below)

## Label Positioning (CRITICAL)

Schemdraw's default label placement overlaps with element symbols on vertical components.
**Always use explicit `loc` and `ofst` parameters** for vertical elements.

The `ofst` parameter uses the **element's local coordinate frame**, not screen coordinates.
For vertical elements, `ofst=(0, y)` moves labels **perpendicular** to the element:

| Element direction | Goal | Code |
|---|---|---|
| `.down()` → label screen-RIGHT | `loc='right', ofst=(0, 0.6)` |
| `.down()` → label screen-LEFT  | `loc='left', ofst=(0, 0.6)` |
| `.up()` → label screen-LEFT    | `loc='left', ofst=(0, 0.6)` |
| `.up()` → label screen-RIGHT   | `loc='left', ofst=(0, -0.6)` |
| `.right()` → label above       | default (no `ofst` needed) |
| `.left()` → label above        | default (no `ofst` needed) |

**For the standard layout** (source UP on left, components DOWN on right):
```python
source = d.add(elm.SourceV().up().label('Vs', loc='left', ofst=(0, 0.6)))
d += elm.Resistor().down().label('R₁', loc='right', ofst=(0, 0.6))
d += elm.Capacitor().down().label('C₁', loc='right', ofst=(0, 0.6))
```

## Schemdraw Code Generation

Use the bundled references for syntax:
- `references/schemdraw-guide.md` - Component elements and methods
- `references/circuit-patterns.md` - Common topology templates

### Basic Structure (Vertical Layout - Preferred)

**Important**: The ground must be connected to the source negative terminal to form a complete circuit.

**Labeling**: Always use explicit `loc` and `ofst` for vertical elements (see Label Positioning section above).

```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=12)

    # Source: UP → label LEFT with ofst=(0, 0.6)
    source = d.add(elm.SourceV().up().label('V₁\n12V', loc='left', ofst=(0, 0.6)))

    # Top rail to the right
    d += elm.Line().right().length(5).at(source.end)

    # Components DOWN → label RIGHT with ofst=(0, 0.6)
    d += elm.Resistor().down().label('R₁  100Ω', loc='right', ofst=(0, 0.6))
    d += elm.Inductor().down().label('L₁  10mH', loc='right', ofst=(0, 0.6))
    d += elm.Capacitor().down().label('C₁  1μF', loc='right', ofst=(0, 0.6))

    # Return path with ground
    d += elm.Line().left().length(3)
    d += elm.Ground()

    # Connect back to source negative terminal
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    d.save('circuit.svg')
```

## Rendering

After generating the Schemdraw code, save it to a `.py` file and render:

```bash
python scripts/render_circuit.py circuit_code.py output.svg
```

Or run the generated Python directly if Schemdraw is installed.

## Components Reference

| Component | Element | Typical Values |
|-----------|---------|----------------|
| DC Source | `elm.SourceV()` | 1V - 24V |
| AC Source | `elm.SourceSin()` | 120V, 60Hz |
| Battery | `elm.Battery()` | 1.5V, 9V, 12V |
| Resistor | `elm.Resistor()` | Ω, kΩ, MΩ |
| Capacitor | `elm.Capacitor()` | pF, nF, μF |
| Inductor | `elm.Inductor()` | μH, mH, H |
| Ground | `elm.Ground()` | - |

## Output

- **Default format**: SVG (scalable, web-friendly)
- **Alternatives**: PNG, PDF (specify in render command)
- **Location**: Same directory as the Schemdraw script, or user-specified path

## Example Files

See `assets/examples/` for working templates:
- `simple-resistive.py` - Basic resistor circuit
- `rc-series.py` - RC series circuit
- `rl-series.py` - RL series circuit
- `rlc-series.py` - Full RLC series circuit
- `rlc-parallel.py` - Parallel RLC circuit
