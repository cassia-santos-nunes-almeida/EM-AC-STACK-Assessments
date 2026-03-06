"""Q5: Parallel RLC Natural Response — Two-switch circuit (based on Nilsson P8.11).

Full circuit with two SPDT switches. At t=0 switches flip, disconnecting sources
and leaving a parallel RLC natural response.

Pre-switch (t<0): Switch 1 at 'a', Switch 2 at 'd'.
  - Left: Is current source || Ra
  - Center: L and R in parallel
  - Right: Rb in series with Vdc, C in parallel

Post-switch (t>0): Switch 1 at 'b', Switch 2 at 'c'.
  - Isolated parallel RLC: L, R, C with initial conditions V0 and I0.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='diagrams/week10/q5_parallel_rlc_natural_switches.svg') as d:
    d.config(unit=3.5, fontsize=14, font='sans-serif')

    # ── Bottom rail (reference) ──
    # Start at bottom-left, build the circuit upward and to the right.

    # Left section: Current source (up) with Ra in parallel
    source = d.add(elm.SourceI().up().label('$I_s$', loc='top', ofst=0.15))
    top_left = source.end
    bot_left = source.start

    # Top rail: short line right from source top
    d += elm.Line().right().length(1.0).at(top_left)
    d += elm.Dot()
    junction_a_top = d.here

    # Ra resistor (parallel with source): down from junction back to bottom
    d.push()
    Ra = d.add(elm.Resistor().down().label('$R_a$', loc='bottom', ofst=0.15))
    junction_a_bot = d.here
    d.pop()

    # Bottom rail segment: source start to Ra bottom
    d += elm.Line().right().at(bot_left).tox(junction_a_bot)

    # ── Switch 1 (SPDT): positions a and b ──
    # Represent as a line from junction_a_top going right, with a switch element
    # Position 'a' = closed (t<0), position 'b' = open line going right
    d += elm.Line().right().length(0.5).at(junction_a_top)
    sw1_pivot = d.here

    # Switch 1: draw as an open switch going right (at t=0 it flips from a to b)
    sw1 = d.add(elm.Switch().right().length(2.0).label('$t=0$', loc='top', ofst=0.3))
    sw1_end = d.here

    # Label switch positions
    d += elm.Dot().at(sw1_pivot)
    d.add(elm.Label().at(sw1_pivot).label('a', loc='top', ofst=0.15))
    d.add(elm.Label().at(sw1_end).label('b', loc='top', ofst=0.15))

    # ── Center section: L and R in parallel ──
    d += elm.Line().right().length(0.5).at(sw1_end)
    d += elm.Dot()
    center_top_left = d.here

    # Branch 1: Inductor (left parallel branch)
    d.push()
    L = d.add(elm.Inductor().down().label('$L$', loc='top', ofst=0.15))
    center_bot_left = d.here
    d.pop()

    # Top rail to R branch
    d += elm.Line().right().length(2.5)
    d += elm.Dot()
    center_top_right = d.here

    # Branch 2: Resistor (right parallel branch)
    d.push()
    R = d.add(elm.Resistor().down().label('$R$', loc='bottom', ofst=0.15))
    center_bot_right = d.here
    d.pop()

    # Connect center bottom rail
    d += elm.Line().left().at(center_bot_right).tox(center_bot_left)
    d += elm.Dot().at(center_bot_left)
    d += elm.Dot().at(center_bot_right)

    # v_o(t) polarity — Gap between L and R branches (use spacer from center_top_left)
    spacer_v = d.add(elm.Line().right().at(center_top_left).length(1.25).color('white').zorder(-1))
    d += elm.Gap().down().at(spacer_v.end).label(['+', '$v_o(t)$', '−'], loc='bottom', ofst=0.15)

    # i_L current arrow on inductor
    d += elm.CurrentLabelInline(direction='in').at(L).label('$i_L$')

    # ── Switch 2 (SPDT): positions c and d ──
    d += elm.Line().right().length(0.5).at(center_top_right)
    sw2_pivot = d.here
    d += elm.Dot()

    sw2 = d.add(elm.Switch().right().length(2.0).label('$t=0$', loc='top', ofst=0.3))
    sw2_end = d.here

    # Label switch positions
    d.add(elm.Label().at(sw2_pivot).label('c', loc='top', ofst=0.15))
    d.add(elm.Label().at(sw2_end).label('d', loc='top', ofst=0.15))

    # ── Right section: Rb + Vdc in series (vertical right), C in parallel ──
    d += elm.Line().right().length(0.5).at(sw2_end)
    d += elm.Dot()
    right_top = d.here

    # Branch: Rb in series with Vdc (going down on right side)
    d.push()
    Rb = d.add(elm.Resistor().down().length(1.75).label('$R_b$', loc='bottom', ofst=0.15))
    Vdc = d.add(elm.SourceV().down().length(1.75).label('$V_{dc}$', loc='bottom', ofst=0.15).reverse())
    right_bot_vdc = d.here
    d.pop()

    # Branch: Capacitor (parallel, further right)
    d += elm.Line().right().length(2.5).at(right_top)
    d += elm.Dot()
    d.push()
    C = d.add(elm.Capacitor().down().label('$C$', loc='bottom', ofst=0.15))
    right_bot_c = d.here
    d.pop()

    # Connect right bottom rail
    d += elm.Line().left().at(right_bot_c).tox(right_bot_vdc)

    # ── Connect all bottom rails ──
    # Bottom: from right section back through center to left section
    d += elm.Line().left().at(right_bot_vdc).tox(center_bot_right)
    d += elm.Line().left().at(center_bot_left).tox(junction_a_bot)
