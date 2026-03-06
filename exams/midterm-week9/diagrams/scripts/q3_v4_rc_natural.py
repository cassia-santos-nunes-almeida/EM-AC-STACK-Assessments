"""
Q3-V4: RC Natural Response — Complex Resistor Network
Capacitor C with initial condition v_C(0) = V0.
C → R1 → Node A (R3 to ground) → R2 → Node B (R4 to ground).
No external source (natural/free response).
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Capacitor on the left (vertical, with initial condition)
    cap = d.add(elm.Capacitor().up().label('C', loc='top', ofst=0.15))

    # Top rail: R1
    d += elm.Line().right().length(0.5).at(cap.end)
    d += elm.Resistor().right().label('R₁')

    # Node A junction
    nodeA = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeA.center).delta(0.5, 0.5).label('A', color='red', fontsize=14))

    # R3 vertical to ground from Node A
    d.push()
    d += elm.Resistor().down().label('R₃', loc='bottom', ofst=0.15)
    d += elm.Line().down().length(0.5)
    d.pop()

    # R2 horizontal to Node B
    d += elm.Resistor().right().label('R₂')

    # Node B junction
    nodeB = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeB.center).delta(0.5, 0.5).label('B', color='red', fontsize=14))

    # R4 vertical to ground from Node B
    d += elm.Line().right().length(0.5)
    d += elm.Resistor().down().label('R₄', loc='bottom', ofst=0.15)
    d += elm.Line().down().length(0.5)

    # Bottom return rail
    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(cap.start)
    d += elm.Line().up().toy(cap.start)

    # Current arrow
    d.add(elm.CurrentLabelInline(direction='in').at(cap.end).label('i(t)', fontsize=13))

    # Initial condition annotation
    d.add(elm.Annotate().at(cap.center).delta(-1.5, 0).label('v_C(0) = V₀', fontsize=12, color='blue'))

    d.save('q3_v4_rc_natural.svg')
