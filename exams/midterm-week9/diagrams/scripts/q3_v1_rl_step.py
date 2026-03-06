"""
Q3-V1: RL Step Response — Complex Resistor Network
Vs*u(t) → R1 → Node A (R2 to ground) → R3 → Node B (L to ground).
3-4 nodes, multi-step analysis required.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Voltage source with step input
    source = d.add(elm.SourceV().up().label('Vs·u(t)', loc='top', ofst=0.15))

    # Top rail: R1
    d += elm.Line().right().length(0.5).at(source.end)
    d += elm.Resistor().right().label('R₁')

    # Node A junction
    nodeA = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeA.center).delta(0.5, 0.5).label('A', color='red', fontsize=14))

    # R2 vertical to ground from Node A
    d.push()
    d += elm.Resistor().down().label('R₂', loc='bottom', ofst=0.15)
    d += elm.Line().down().length(0.5)
    d.pop()

    # R3 horizontal to Node B
    d += elm.Resistor().right().label('R₃')

    # Node B junction
    nodeB = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeB.center).delta(0.5, 0.5).label('B', color='red', fontsize=14))

    # Inductor vertical to ground from Node B
    d += elm.Line().right().length(0.5)
    ind = d.add(elm.Inductor().down().label('L', loc='bottom', ofst=0.15))

    # Current arrow
    d.add(elm.CurrentLabelInline(direction='in').at(source.end).label('i(t)', fontsize=13))

    # Return path with ground
    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    d.save('q3_v1_rl_step.svg')
