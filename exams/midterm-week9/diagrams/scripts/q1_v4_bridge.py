"""
Q1-V4: Wheatstone Bridge Circuit — DC Resistive Circuit
Diamond-shaped bridge with R1-R4 on arms and R5 as bridge element.
Vs on the left. Nodes: A (top), B (left-mid), C (right-mid), D (bottom).
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Voltage source on the far left
    source = d.add(elm.SourceV().up().label('Vs', loc='top', ofst=0.15))

    # Connect to top node A
    d += elm.Line().right().length(1).at(source.end)
    nodeA_pos = d.here

    # Upper-left arm: R1 from A down-left to B
    d.push()
    d += elm.Resistor().down().label('R₁', loc='top', ofst=0.15)
    nodeB = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeB.center).delta(-0.8, 0).label('B', color='red', fontsize=14))
    d.pop()

    # Upper-right arm: R2 from A to the right then down to C
    d += elm.Line().right().length(3)
    d += elm.Resistor().down().label('R₂', loc='bottom', ofst=0.15)
    nodeC = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeC.center).delta(0.8, 0).label('C', color='red', fontsize=14))

    # Bridge element R5: horizontal between B and C
    d.add(elm.Resistor().right().at(nodeB.center).tox(nodeC.center).label('R₅'))

    # Lower-left arm: R3 from B down to D
    d.add(elm.Resistor().down().at(nodeB.center).label('R₃', loc='top', ofst=0.15))
    nodeD_left = d.here

    # Lower-right arm: R4 from C down to D
    d.add(elm.Resistor().down().at(nodeC.center).label('R₄', loc='bottom', ofst=0.15))
    nodeD_right = d.here

    # Bottom rail connecting D nodes
    d += elm.Line().left().at(nodeD_right).tox(nodeD_left)

    # Ground at center bottom
    d.push()
    mid_x = (nodeD_left[0] + nodeD_right[0]) / 2
    d += elm.Ground().at((mid_x, nodeD_left[1]))
    d.pop()

    # Return to source
    d += elm.Line().left().at(nodeD_left).tox(source.start)
    d += elm.Line().up().toy(source.start)

    d.save('q1_v4_bridge.svg')
