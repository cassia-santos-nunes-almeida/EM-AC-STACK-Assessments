"""
Q1-V3: T-Network Circuit — DC Resistive Circuit
Vs on the left, R1 → Node B → R2 → Node C on top rail,
R3 vertical from Node B to ground, Is current source on right.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Voltage source (left side)
    source = d.add(elm.SourceV().up().label('Vs', loc='left', ofst=(0, 0.6)))

    # Top rail: R1
    d += elm.Line().right().length(0.5).at(source.end)
    d += elm.Resistor().right().label('R₁')

    # Node B junction
    nodeB = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeB.center).delta(0.5, 0.5).label('B', color='red', fontsize=14))

    # R3 vertical to ground from Node B (stem of T)
    d.push()
    d += elm.Resistor().down().label('R₃', loc='right', ofst=(0, 0.6))
    d += elm.Line().down().length(0.5)
    d.pop()

    # R2 horizontal continues to Node C
    d += elm.Resistor().right().label('R₂')

    # Node C junction
    nodeC = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeC.center).delta(0.5, 0.5).label('C', color='red', fontsize=14))

    # Current source on the right
    d += elm.Line().right().length(1)
    d += elm.SourceI().down().reverse().label('Is', loc='right', ofst=(0, 0.6))

    # Bottom return rail
    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    d.save('q1_v3_t_network.svg')
