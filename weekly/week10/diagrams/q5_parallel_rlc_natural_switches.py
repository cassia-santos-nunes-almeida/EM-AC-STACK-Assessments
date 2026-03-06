"""Q5: Parallel RLC Natural Response — Two-switch circuit (Nilsson P8.11 style).

Layout matches the reference diagram:
  - Is || Ra on far left (both vertical, parallel)
  - SPDT switch 1 (a/b) at t=0  with iL arrow
  - L horizontal on top wire
  - R vertical from junction to bottom rail, with v_o(t) across it
  - Wire from junction to SPDT switch 2 (c/d)
  - C, Rb, Vdc vertical series branch on far right
  - Bottom rail connects all ground nodes
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='weekly/week10/diagrams/q5_parallel_rlc_natural_switches.svg') as d:
    d.config(unit=3.0, fontsize=14, font='sans-serif')

    # ──────────────────────────────────────────────
    # LEFT SECTION: Is ∥ Ra  (vertical, parallel)
    # ──────────────────────────────────────────────

    # Current source Is (vertical, arrow pointing up)
    Is = d.add(elm.SourceI().up().label('$I_s$', loc='left', ofst=0.25))
    bot_left = Is.start   # bottom rail (left)
    top_left = Is.end     # top rail (left)

    # Short wire right on top rail to Ra junction
    d += elm.Line().right().length(1.5).at(top_left)
    d += elm.Dot()
    ra_top = d.here

    # Ra (vertical, down) — parallel with Is
    d.push()
    d.add(elm.Resistor().down().at(ra_top).label('$R_a$', loc='left', ofst=0.25))
    ra_bot = d.here
    d.pop()

    # Bottom rail: Is start → Ra bottom
    d += elm.Line().right().at(bot_left).tox(ra_bot)
    d += elm.Dot().at(ra_bot)

    # ──────────────────────────────────────────────
    # SWITCH 1 (SPDT): a = top throw, b = bottom throw
    # Common on left (from Ra), throws on right
    # ──────────────────────────────────────────────
    d += elm.Line().right().length(0.6).at(ra_top)
    sw1_common = d.here

    sw1 = d.add(elm.SwitchSpdt2().right().at(sw1_common))

    # 'a' = upper throw (sw1.b), 'b' = lower throw (sw1.c)
    d.add(elm.Label().at(sw1.absanchors['b']).label('a', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw1.absanchors['c']).label('b', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw1.absanchors['a']).label('$t=0$', loc='bottom', ofst=0.4))

    # iL label near 'b' throw
    d.add(elm.Label().at(sw1.absanchors['c']).label('$i_L$', loc='right', ofst=0.85))

    # ──────────────────────────────────────────────
    # INDUCTOR L (horizontal, on top wire)
    # ──────────────────────────────────────────────
    d += elm.Line().right().length(0.5).at(sw1.absanchors['b'])
    L_elem = d.add(elm.Inductor2(loops=4).right().label('$L$', loc='top', ofst=0.15))
    d += elm.Line().right().length(0.5)
    d += elm.Dot()
    junction = d.here

    # ──────────────────────────────────────────────
    # RESISTOR R (vertical, from junction down to bottom rail)
    # ──────────────────────────────────────────────
    d.push()

    # + polarity at top
    d.add(elm.Label().at(junction).label('+', loc='left', ofst=0.3))

    R_elem = d.add(elm.Resistor().down().at(junction))

    # vo(t) label to the left of R
    d.add(elm.Label().at(R_elem.center).label('$v_o(t)$', loc='left', ofst=0.55))

    R_bot = d.here
    d += elm.Dot()

    # − polarity at bottom
    d.add(elm.Label().at(R_bot).label('\u2212', loc='left', ofst=0.3))

    d.pop()

    # ──────────────────────────────────────────────
    # HORIZONTAL WIRE from junction to SWITCH 2
    # Label R above this wire segment
    # ──────────────────────────────────────────────
    wire_to_sw2 = d.add(elm.Line().right().length(2.0).at(junction).label('$R$', loc='top', ofst=0.15))
    sw2_common = d.here

    # ──────────────────────────────────────────────
    # SWITCH 2 (SPDT): c = top throw, d = bottom throw
    # ──────────────────────────────────────────────
    sw2 = d.add(elm.SwitchSpdt2().right().at(sw2_common))

    d.add(elm.Label().at(sw2.absanchors['b']).label('c', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw2.absanchors['c']).label('d', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw2.absanchors['a']).label('$t=0$', loc='bottom', ofst=0.4))

    # ──────────────────────────────────────────────
    # RIGHT BRANCH: C → Rb → Vdc (vertical series, same height as left)
    # ──────────────────────────────────────────────
    # Wire from upper throw 'c' to C
    d += elm.Line().right().length(0.5).at(sw2.absanchors['b'])
    d += elm.Dot()
    c_top = d.here

    # Capacitor C (vertical, down) — use shorter length
    C_elem = d.add(elm.Capacitor().down().at(c_top).length(1.5).label('$C$', loc='right', ofst=0.15))

    # Rb (vertical, down)
    Rb_elem = d.add(elm.Resistor().down().length(1.5).label('$R_b$', loc='right', ofst=0.15))

    # Vdc (voltage source, + on top, vertical, down)
    Vdc_elem = d.add(elm.SourceV().down().length(1.5).label('$V_{dc}$', loc='right', ofst=0.15).reverse())
    vdc_bot = d.here

    # ──────────────────────────────────────────────
    # BOTTOM RAIL — connect all ground nodes at Vdc bottom level
    # ──────────────────────────────────────────────
    bot_y = vdc_bot  # reference point for bottom rail

    # Wire down from R_bot to bottom rail level
    d += elm.Line().down().at(R_bot).toy(bot_y)
    R_ground = d.here
    d += elm.Dot()

    # Horizontal: Vdc bottom → R ground
    d += elm.Line().left().at(vdc_bot).tox(R_ground)

    # Horizontal: R ground → Ra bottom x-position
    d += elm.Line().left().at(R_ground).tox(ra_bot)
    left_ground = d.here
    d += elm.Dot()

    # Vertical wire: Ra bottom → bottom rail
    d += elm.Line().down().at(ra_bot).toy(left_ground)

    # Vertical wire: Is bottom → bottom rail
    d += elm.Line().down().at(bot_left).toy(left_ground)

    # Horizontal: left ground → Is bottom
    d += elm.Line().left().at(left_ground).tox(bot_left)
