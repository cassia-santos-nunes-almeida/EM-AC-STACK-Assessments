"""
Q2-V1: RL Circuit with Switch — Inductor Energy & KVL-Faraday
Series: Vs → Switch S → R → L → ground loop.
Current arrow i(t) on top rail, voltage polarity v_L across inductor.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Voltage source (left side)
    source = d.add(elm.SourceV().up().label('Vs', loc='top', ofst=0.15))

    # Top rail: switch then resistor
    d += elm.Line().right().length(0.5).at(source.end)
    sw = d.add(elm.Switch().right().label('S'))
    d += elm.Resistor().right().label('R')

    # Continue to inductor (vertical on right)
    d += elm.Line().right().length(0.5)
    ind = d.add(elm.Inductor().down().label('L', loc='bottom', ofst=0.15))

    # Current arrow on top rail
    d.add(elm.CurrentLabelInline(direction='in').at(sw.center).label('i(t)', fontsize=13))

    # Return path with ground
    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    d.save('q2_v1_inductor_rl.svg')
