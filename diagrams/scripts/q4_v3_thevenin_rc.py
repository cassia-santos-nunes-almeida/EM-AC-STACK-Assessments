"""
Q4-V3: Thevenin Equivalent with RC Circuit
Left: Original circuit (Vs, R1, R2 voltage divider + switch + C).
Right: Thevenin equivalent (Vth, Rth, C).
Shows both circuits side by side.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Original circuit
ax1.set_title('Original Circuit', fontsize=14, fontweight='bold')
with schemdraw.Drawing(canvas=ax1) as d:
    d.config(unit=3, fontsize=13, font='sans-serif')

    source = d.add(elm.SourceV().up().label('Vs', loc='left', ofst=(0, 0.6)))
    d += elm.Line().right().length(0.5).at(source.end)
    d += elm.Resistor().right().label('R₁')

    nodeA = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeA.center).delta(0.5, 0.5).label('A', color='red', fontsize=13))

    # R2 to ground
    d.push()
    d += elm.Resistor().down().label('R₂', loc='right', ofst=(0, 0.6))
    d += elm.Line().down().length(0.5)
    d.pop()

    # Switch then C
    sw = d.add(elm.Switch().right().label('S'))
    d += elm.Line().right().length(0.5)
    cap = d.add(elm.Capacitor().down().label('C', loc='right', ofst=(0, 0.6)))

    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

ax1.axis('off')

# Thevenin equivalent
ax2.set_title('Thévenin Equivalent', fontsize=14, fontweight='bold')
with schemdraw.Drawing(canvas=ax2) as d:
    d.config(unit=3, fontsize=13, font='sans-serif')

    source = d.add(elm.SourceV().up().label('Vth', loc='left', ofst=(0, 0.6)))
    d += elm.Line().right().length(0.5).at(source.end)
    d += elm.Resistor().right().label('Rth')
    d += elm.Line().right().length(0.5)
    cap = d.add(elm.Capacitor().down().label('C', loc='right', ofst=(0, 0.6)))

    d.add(elm.CurrentLabelInline(direction='in').at(source.end).label('i(t)', fontsize=12))

    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

ax2.axis('off')

plt.tight_layout()
plt.savefig('q4_v3_thevenin_rc.svg', format='svg', bbox_inches='tight')
plt.savefig('q4_v3_thevenin_rc.png', format='png', dpi=150, bbox_inches='tight')
plt.close()
