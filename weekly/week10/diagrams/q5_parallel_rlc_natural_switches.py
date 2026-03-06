"""Q5: Parallel RLC Natural Response — Two-switch circuit (Nilsson P8.11).

Topology (matches Figure P8.11):
  - Is || Ra on far left (both vertical, parallel)
  - SPDT switch 1 (a/b) on top rail; at t=0 moves from a→b
  - L vertical branch (inductor) between top/bottom rails
  - R vertical branch (resistor) with v_o(t) between top/bottom rails
  - SPDT switch 2 (c/d) on top rail; at t=0 moves from d→c
  - C vertical branch (from sw2 upper throw 'c')
  - Rb horizontal + Vdc vertical (from sw2 lower throw 'd')
  - Bottom rail connects all ground nodes

Before t=0 (sw1=a, sw2=d): L charges from Is||Ra; C charges from Vdc via Rb; R isolated.
After  t=0 (sw1=b, sw2=c): L, R, C in parallel — source-free natural response.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='weekly/week10/diagrams/q5_parallel_rlc_natural_switches.svg') as d:
    d.config(unit=3.0, fontsize=14, font='sans-serif')

    # ── LEFT SECTION: Is ∥ Ra (vertical, parallel) ──────────────

    Is = d.add(elm.SourceI().up().label('$I_s$', loc='left', ofst=0.25))
    bot_left = Is.start   # bottom rail reference (left end)
    top_left = Is.end     # top rail reference (left end)

    d += elm.Line().right().length(1.5).at(top_left)
    d += elm.Dot()
    ra_top = d.here

    d.push()
    d.add(elm.Resistor().down().at(ra_top).label('$R_a$', loc='left', ofst=0.25))
    ra_bot = d.here
    d.pop()

    # Bottom wire: Is start → Ra bottom
    d += elm.Line().right().at(bot_left).tox(ra_bot)
    d += elm.Dot().at(ra_bot)

    # ── SWITCH 1 (SPDT) ─────────────────────────────────────────
    # Common on left (from Ra), throws on right.
    # 'a' = upper throw (schemdraw 'b' anchor)
    # 'b' = lower throw (schemdraw 'c' anchor)

    d += elm.Line().right().length(0.6).at(ra_top)
    sw1 = d.add(elm.SwitchSpdt2().right())

    d.add(elm.Label().at(sw1.absanchors['b']).label('a', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw1.absanchors['c']).label('b', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw1.absanchors['a']).label('$t=0$', loc='bottom', ofst=0.4))

    # ── L branch (VERTICAL — from upper throw 'a') ──────────────

    d += elm.Line().right().length(0.5).at(sw1.absanchors['b'])
    d += elm.Dot()
    L_top = d.here

    d.push()
    L_elem = d.add(elm.Inductor2(loops=4).down()
                    .label('$L$', loc='bottom', ofst=0.15))
    L_bot = d.here
    d.pop()

    # ── Top rail continues right to R branch ─────────────────────

    d += elm.Line().right().length(2.0)
    d += elm.Dot()
    R_top = d.here

    # ── R branch (VERTICAL — with v_o(t) polarity) ──────────────

    d.push()

    # Voltage polarity: + at top
    d.add(elm.Label().at(R_top).label('+', loc='left', ofst=0.3))

    R_elem = d.add(elm.Resistor().down().at(R_top)
                    .label('$R$', loc='bottom', ofst=0.15))

    # v_o(t) label to the left of R
    d.add(elm.Label().at(R_elem.center)
          .label('$v_o(t)$', loc='left', ofst=0.55))

    R_bot = d.here
    d += elm.Dot()

    # Voltage polarity: − at bottom
    d.add(elm.Label().at(R_bot).label('\u2212', loc='left', ofst=0.3))

    d.pop()

    # ── Top rail continues right to SWITCH 2 ────────────────────

    d += elm.Line().right().length(0.6)
    sw2 = d.add(elm.SwitchSpdt2().right())

    d.add(elm.Label().at(sw2.absanchors['b']).label('c', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw2.absanchors['c']).label('d', loc='right', ofst=0.3))
    d.add(elm.Label().at(sw2.absanchors['a']).label('$t=0$', loc='bottom', ofst=0.4))

    # ── C branch (VERTICAL — from upper throw 'c') ──────────────

    d += elm.Line().right().length(0.5).at(sw2.absanchors['b'])
    d += elm.Dot()
    C_top = d.here

    d.push()
    C_elem = d.add(elm.Capacitor().down()
                    .label('$C$', loc='bottom', ofst=0.15))
    C_bot = d.here
    d.pop()

    # ── Rb (HORIZONTAL) + Vdc (VERTICAL) from lower throw 'd' ───

    d += elm.Line().right().length(0.5).at(sw2.absanchors['c'])
    Rb_elem = d.add(elm.Resistor().right()
                     .label('$R_b$', loc='top', ofst=0.15))

    Vdc_elem = d.add(elm.SourceV().down()
                      .label('$V_{dc}$', loc='right', ofst=0.15)
                      .reverse())
    Vdc_bot = d.here

    # ── BOTTOM RAIL ──────────────────────────────────────────────
    # Extend all branch bottoms to the bottom rail level (ra_bot Y),
    # then connect horizontally.

    d += elm.Line().down().at(L_bot).toy(ra_bot)
    L_gnd = d.here

    d += elm.Line().down().at(R_bot).toy(ra_bot)
    R_gnd = d.here

    d += elm.Line().down().at(C_bot).toy(ra_bot)
    C_gnd = d.here

    d += elm.Line().down().at(Vdc_bot).toy(ra_bot)
    Vdc_gnd = d.here

    # Horizontal bottom rail: ra_bot → L → R → C → Vdc
    d += elm.Line().right().at(ra_bot).tox(L_gnd)
    d += elm.Line().right().at(L_gnd).tox(R_gnd)
    d += elm.Line().right().at(R_gnd).tox(C_gnd)
    d += elm.Line().right().at(C_gnd).tox(Vdc_gnd)
