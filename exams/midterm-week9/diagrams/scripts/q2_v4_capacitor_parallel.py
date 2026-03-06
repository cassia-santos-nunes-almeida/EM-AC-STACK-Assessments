"""
Q2-V4: Parallel Capacitors — Total Energy & KCL
V source with C1 and C2 in parallel. Node P at junction.
Current arrows i, i1, i2. KCL annotation.
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Voltage source (left side)
    source = d.add(elm.SourceV().up().label('V', loc='top', ofst=0.15))

    # Top rail
    d += elm.Line().right().length(1).at(source.end)

    # Node P junction
    nodeP = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeP.center).delta(0.5, 0.5).label('P', color='red', fontsize=14))

    # C1 branch (first parallel)
    d.push()
    c1 = d.add(elm.Capacitor().down().label('C₁', loc='bottom', ofst=0.15))
    c1_bot = d.here
    d.pop()

    # Continue right for C2 branch
    d += elm.Line().right().length(3)
    d += elm.Dot()

    # C2 branch (second parallel)
    c2 = d.add(elm.Capacitor().down().label('C₂', loc='bottom', ofst=0.15))
    c2_bot = d.here

    # Bottom rail connecting both capacitors
    d += elm.Line().left().at(c2_bot).tox(c1_bot)

    # Ground at center
    mid_x = (c1_bot[0] + c2_bot[0]) / 2
    d.add(elm.Ground().at((mid_x, c1_bot[1])))

    # Return to source
    d += elm.Line().left().at(c1_bot).tox(source.start)
    d += elm.Line().up().toy(source.start)

    # Current labels
    d.add(elm.CurrentLabelInline(direction='in').at(source.end).label('i', fontsize=13))

    d.save('q2_v4_capacitor_parallel.svg')
