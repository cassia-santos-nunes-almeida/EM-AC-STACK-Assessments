"""
Q1-V2: Two-Mesh Circuit — DC Resistive Circuit
Two voltage sources (left and right), four resistors forming two meshes.
R2 is shared between meshes (center vertical element).
"""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    d.config(unit=3, fontsize=14, font='sans-serif')

    # Left voltage source
    vs1 = d.add(elm.SourceV().up().label('Vs₁', loc='top', ofst=0.15))

    # Top rail left mesh: R1
    d += elm.Line().right().length(0.5).at(vs1.end)
    d += elm.Resistor().right().label('R₁')

    # Center node (top)
    center_top = d.add(elm.Dot())

    # R2 shared vertical element (center)
    d.push()
    d += elm.Resistor().down().label('R₂', loc='bottom', ofst=0.15)
    center_bot = d.add(elm.Dot())
    d.pop()

    # Top rail right mesh: R3
    d += elm.Resistor().right().label('R₃')
    d += elm.Line().right().length(0.5)

    # Right voltage source
    vs2 = d.add(elm.SourceV().down().label('Vs₂', loc='bottom', ofst=0.15))

    # Bottom rail right mesh: connect to center bottom
    d += elm.Line().left().length(0.5)
    d += elm.Resistor().left().label('R₄')

    # Bottom rail continues left to Vs1
    d += elm.Line().left().at(center_bot.center).length(0.5)
    d += elm.Ground()
    d += elm.Line().left().tox(vs1.start)
    d += elm.Line().up().toy(vs1.start)

    # Mesh current labels
    d.add(elm.CurrentLabelInline(direction='in').at(vs1.center).label('i₁', fontsize=13))
    d.add(elm.CurrentLabelInline(direction='in').at(vs2.center).label('i₂', fontsize=13))

    d.save('q1_v2_two_mesh.svg')
