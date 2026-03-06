"""Q2: Parallel RLC Step Response — Current source with R, L, C in parallel."""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='diagrams/week10/q2_parallel_rlc_step.svg') as d:
    d.config(unit=3.5, fontsize=14, font='sans-serif')

    # DC current source on the left (vertical, arrow pointing up)
    source = d.add(elm.SourceI().up().label('$I_s$', loc='top', ofst=0.15))

    # Top rail rightward
    d += elm.Line().right().length(1.5).at(source.end)
    d += elm.Dot()

    # Save junction for parallel branches
    junction_top = d.here

    # Branch 1: Resistor (leftmost parallel branch)
    d.push()
    R = d.add(elm.Resistor().down().label('$R$', loc='bottom', ofst=0.15))
    junction_bot_R = d.here
    d.pop()

    # Line to next branch
    d += elm.Line().right().length(2.5)
    d += elm.Dot()
    d.push()

    # Branch 2: Inductor (middle parallel branch)
    L = d.add(elm.Inductor().down().label('$L$', loc='bottom', ofst=0.15))
    # Current arrow on inductor
    d += elm.CurrentLabelInline(direction='in').at(L).label('$i_L$')
    junction_bot_L = d.here
    d.pop()

    # Line to next branch
    d += elm.Line().right().length(2.5)
    d += elm.Dot()

    # Branch 3: Capacitor (rightmost parallel branch)
    C = d.add(elm.Capacitor().down().label('$C$', loc='bottom', ofst=0.15))
    junction_bot_C = d.here

    # Bottom rail: connect all branch bottoms
    d += elm.Line().left().at(junction_bot_C).tox(junction_bot_R)

    # Voltage label across parallel combination (on top rail)
    d += elm.Line().left().at(junction_bot_R).tox(source.start)
    d += elm.Line().up().toy(source.start)

    # Voltage polarity: v(t) between source and R branch
    # Invisible spacer to offset Gap from the current source
    spacer = d.add(elm.Line().right().at(source.end).length(0.75).color('white').zorder(-1))
    d += elm.Gap().down().at(spacer.end).label(['+', '$v(t)$', '−'], loc='bottom', ofst=0.15)
