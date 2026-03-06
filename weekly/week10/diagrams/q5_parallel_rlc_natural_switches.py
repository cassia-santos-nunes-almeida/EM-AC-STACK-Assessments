"""Q5: Parallel RLC Natural Response — Four-switch circuit (Nilsson P8.11).

Topology: 4 SPST switches on the top rail divide the circuit into three sections.
t < 0: SW1, SW4 closed (left/right loops active); SW2, SW3 open (middle isolated).
       Left loop:  Is ∥ Ra ∥ L — inductor charges (short at DC).
       Right loop:  C in series with Rb + Vdc — capacitor charges to Vdc.
t = 0: SW1, SW4 open; SW2, SW3 close.
       → L ∥ R ∥ C source-free parallel RLC, v₀(t) across R.

Layout (left to right):
    Is  Ra  [SW1]  L  [SW2]  R(v₀)  [SW3]  C  [SW4]  Rb──Vdc
     |   |          |          |              |              |
     └───┴──────────┴──────────┴──────────────┴──────────────┘
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='weekly/week10/diagrams/q5_parallel_rlc_natural_switches.svg') as d:
    d.config(unit=3.0, fontsize=14, font='sans-serif')

    # ── LEFT SECTION: Is ∥ Ra ─────────────────────────────────

    Is = d.add(elm.SourceI().up().label('$I_s$', loc='left', ofst=0.25))
    bot_is = Is.start
    top_is = Is.end

    d += elm.Line().right().length(1.5).at(top_is)
    d += elm.Dot()
    top_ra = d.here

    d.push()
    d.add(elm.Resistor().down().at(top_ra)
          .label('$R_a$', loc='right', ofst=0.2))
    bot_ra = d.here
    d.pop()

    # ── SW1 (closed at t<0 → opens at t=0) ───────────────────

    d += elm.Line().right().length(0.5)
    d.add(elm.Switch().right()
          .label('$t{=}0$\n(opens)', loc='top', ofst=(0, 0.25)))

    # ── L branch ─────────────────────────────────────────────

    d += elm.Line().right().length(0.5)
    d += elm.Dot()
    top_L = d.here

    d.push()
    d.add(elm.Inductor2(loops=4).down().at(top_L)
          .label('$L$', loc='right', ofst=0.2))
    bot_L = d.here
    d.pop()

    # ── SW2 (open at t<0 → closes at t=0) ────────────────────

    d += elm.Line().right().length(0.5)
    d.add(elm.Switch().right()
          .label('$t{=}0$\n(closes)', loc='top', ofst=(0, 0.25)))

    # ── R branch (with v₀ polarity) ──────────────────────────

    d += elm.Line().right().length(0.5)
    d += elm.Dot()
    top_R = d.here

    d.push()
    R = d.add(elm.Resistor().down().at(top_R)
              .label('$R$', loc='right', ofst=0.2))
    bot_R = d.here  # capture before Label elements move d.here
    d.add(elm.Label().at(top_R).label('+', loc='left', ofst=0.35))
    d.add(elm.Label().at(R.center)
          .label('$v_o(t)$', loc='left', ofst=0.6))
    d.add(elm.Label().at(bot_R).label('\u2212', loc='left', ofst=0.35))
    d.pop()

    # ── SW3 (open at t<0 → closes at t=0) ────────────────────

    d += elm.Line().right().length(0.5)
    d.add(elm.Switch().right()
          .label('$t{=}0$\n(closes)', loc='top', ofst=(0, 0.25)))

    # ── C branch ─────────────────────────────────────────────

    d += elm.Line().right().length(0.5)
    d += elm.Dot()
    top_C = d.here

    d.push()
    d.add(elm.Capacitor().down().at(top_C)
          .label('$C$', loc='right', ofst=0.2))
    bot_C = d.here
    d.pop()

    # ── SW4 (closed at t<0 → opens at t=0) ───────────────────

    d += elm.Line().right().length(0.5)
    d.add(elm.Switch().right()
          .label('$t{=}0$\n(opens)', loc='top', ofst=(0, 0.25)))

    # ── Rb (horizontal on top rail — no line underneath) ─────

    d.add(elm.Resistor().right()
          .label('$R_b$', loc='top', ofst=0.15))

    # ── Vdc (vertical, + on top) ─────────────────────────────

    d.add(elm.SourceV().down()
          .label('$V_{dc}$', loc='right', ofst=0.2)
          .reverse())
    bot_Vdc = d.here

    # ── BOTTOM RAIL (continuous) ──────────────────────────────

    d += elm.Line().right().at(bot_is).tox(bot_ra)
    d += elm.Line().right().tox(bot_L)
    d += elm.Line().right().tox(bot_R)
    d += elm.Line().right().tox(bot_C)
    d += elm.Line().right().tox(bot_Vdc)
