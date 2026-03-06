"""Q1: Series RLC Natural Response — Circuit with switch opening at t=0."""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='diagrams/week10/q1_series_rlc_switch.svg') as d:
    d.config(unit=3.5, fontsize=14, font='sans-serif')

    # DC voltage source on the left (vertical, positive on top)
    source = d.add(elm.SourceV().up().label('$V_s$', loc='left', ofst=(0, 0.6)))

    # Top rail rightward
    d += elm.Line().right().length(2).at(source.end)

    # Switch (opens at t=0) — shown closed
    sw = d.add(elm.Switch().right().label('$t = 0$\n(opens)', loc='top', ofst=(0, 0.3)))

    # Continue top rail
    d += elm.Line().right().length(2)

    # Resistor going down
    R = d.add(elm.Resistor().down().label('$R$', loc='right', ofst=(0, 0.6)))

    # Inductor going down
    L = d.add(elm.Inductor().down().label('$L$', loc='right', ofst=(0, 0.6)))

    # Capacitor going down with voltage polarity
    C = d.add(elm.Capacitor().down().label('$C$', loc='right', ofst=(0, 0.6)))

    # Voltage polarity on capacitor
    d += elm.CurrentLabelInline(direction='in').at(C).label('$v_C$')

    # Bottom return path
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    # Current arrow in the loop (top rail)
    d += elm.CurrentLabelInline(direction='in').at(sw).label('$i(t)$')
