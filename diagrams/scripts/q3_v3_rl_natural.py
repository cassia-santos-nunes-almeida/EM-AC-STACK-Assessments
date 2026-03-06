"""
Q3-V3: RL Natural Response — Complex Resistor Network
Inductor L with initial condition i_L(0) = I0.
L → top rail → R4 to ground, R1 → Node A → R2 to ground, R3 to ground.
No external source (natural/free response).
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Inductor on the left (vertical, with initial condition)
    ind = d.add(elm.Inductor().up().label('L', loc='left', ofst=(0, 0.6)))

    # Top rail
    d += elm.Line().right().length(0.5).at(ind.end)

    # R4 vertical to ground (shunt)
    d += elm.Dot()
    d.push()
    d += elm.Resistor().down().label('R₄', loc='right', ofst=(0, 0.6))
    d += elm.Line().down().length(0.5)
    d.pop()

    # R1 horizontal to Node A
    d += elm.Resistor().right().label('R₁')

    # Node A junction
    nodeA = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeA.center).delta(0.5, 0.5).label('A', color='red', fontsize=14))

    # R2 vertical to ground from Node A
    d.push()
    d += elm.Resistor().down().label('R₂', loc='right', ofst=(0, 0.6))
    d += elm.Line().down().length(0.5)
    d.pop()

    # R3 continues right then to ground
    d += elm.Line().right().length(1)
    d += elm.Resistor().down().label('R₃', loc='right', ofst=(0, 0.6))
    d += elm.Line().down().length(0.5)

    # Bottom return rail
    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(ind.start)
    d += elm.Line().up().toy(ind.start)

    # Current arrow
    d.add(elm.CurrentLabelInline(direction='in').at(ind.end).label('i_L(t)', fontsize=13))

    # Initial condition annotation
    d.add(elm.Annotate().at(ind.center).delta(-1.5, 0).label('i_L(0) = I₀', fontsize=12, color='blue'))

    d.save('q3_v3_rl_natural.svg')
