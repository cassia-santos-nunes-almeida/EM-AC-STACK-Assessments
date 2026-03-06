"""
Q2-V2: RC Circuit — Capacitor Energy & KCL-Charge Conservation
Series: Vs → R → C → ground loop.
Node X at junction of R and C. Voltage polarity v_C across capacitor.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Voltage source (left side)
    source = d.add(elm.SourceV().up().label('Vs', loc='top', ofst=0.15))

    # Top rail: resistor
    d += elm.Line().right().length(0.5).at(source.end)
    d += elm.Resistor().right().label('R')

    # Node X junction
    nodeX = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeX.center).delta(0.5, 0.5).label('X', color='red', fontsize=14))

    # Capacitor vertical on right side
    d += elm.Line().right().length(1)
    cap = d.add(elm.Capacitor().down().label('C', loc='bottom', ofst=0.15))

    # Current arrow on top rail
    d.add(elm.CurrentLabelInline(direction='in').at(source.end).label('i(t)', fontsize=13))

    # Return path with ground
    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    d.save('q2_v2_capacitor_rc.svg')
