"""
Q1-V1: Two Essential Nodes — DC Resistive Circuit
Vs on the left, R1 horizontal on top, Node A junction,
R2 and R3 vertical to ground, Is current source on the right.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Voltage source (left side, vertical)
    source = d.add(elm.SourceV().up().label('Vs', loc='left', ofst=(0, 0.6)))

    # Top rail from source to R1
    d += elm.Line().right().length(1).at(source.end)
    d += elm.Resistor().right().label('R₁')

    # Node A junction
    nodeA = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeA.center).delta(0.5, 0.5).label('A', color='red', fontsize=14))

    # R2 vertical to ground from Node A
    d.push()
    d += elm.Resistor().down().label('R₂', loc='right', ofst=(0, 0.6))
    d += elm.Line().down().length(0.5)
    d.pop()

    # Continue right to R3
    d += elm.Line().right().length(3)
    d += elm.Dot()

    # R3 vertical to ground
    d.push()
    d += elm.Resistor().down().label('R₃', loc='right', ofst=(0, 0.6))
    d += elm.Line().down().length(0.5)
    d.pop()

    # Continue right to current source
    d += elm.Line().right().length(1)
    d += elm.SourceI().down().reverse().label('Is', loc='right', ofst=(0, 0.6))

    # Bottom return rail
    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    d.save('q1_v1_two_node.svg')
