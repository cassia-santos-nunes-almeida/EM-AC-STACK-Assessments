"""
Q4-V1: RC Circuit with Switch Opening
Pre-switch (t<0): Vs → R1 → Node A, R2 and C in parallel to ground.
Post-switch (t>0): Switch opens, R2 disconnected. Vs → R1 → C.
Shows both circuit states side by side.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Pre-switch circuit (t < 0)
ax1.set_title('t < 0  (switch closed)', fontsize=14, fontweight='bold')
with schemdraw.Drawing(canvas=ax1) as d:
    d.config(unit=3, fontsize=13, font='sans-serif')

    source = d.add(elm.SourceV().up().label('Vs', loc='top', ofst=0.15))
    d += elm.Line().right().length(0.5).at(source.end)
    d += elm.Resistor().right().label('R₁')

    nodeA = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeA.center).delta(0.5, 0.5).label('A', color='red', fontsize=13))

    # R2 branch (with closed switch)
    d.push()
    d += elm.Switch().down().label('S', loc='bottom', ofst=0.15)
    d += elm.Resistor().down().label('R₂', loc='bottom', ofst=0.15)
    d += elm.Line().down().length(0.3)
    d.pop()

    # C branch in parallel
    d += elm.Line().right().length(2)
    d += elm.Capacitor().down().label('C', loc='bottom', ofst=0.15)
    d += elm.Line().down().length(0.3)

    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

ax1.axis('off')

# Post-switch circuit (t > 0)
ax2.set_title('t > 0  (switch opens)', fontsize=14, fontweight='bold')
with schemdraw.Drawing(canvas=ax2) as d:
    d.config(unit=3, fontsize=13, font='sans-serif')

    source = d.add(elm.SourceV().up().label('Vs', loc='top', ofst=0.15))
    d += elm.Line().right().length(0.5).at(source.end)
    d += elm.Resistor().right().label('R₁')

    nodeA = d.add(elm.Dot())
    d.add(elm.Annotate().at(nodeA.center).delta(0.5, 0.5).label('A', color='red', fontsize=13))

    # Capacitor (R2 disconnected)
    d += elm.Line().right().length(1)
    d += elm.Capacitor().down().label('C', loc='bottom', ofst=0.15)

    d.add(elm.CurrentLabelInline(direction='in').at(source.end).label('i(t)', fontsize=12))

    d += elm.Line().left().length(2)
    d += elm.Ground()
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

ax2.axis('off')

plt.tight_layout()
plt.savefig('q4_v1_rc_switch.svg', format='svg', bbox_inches='tight')
plt.savefig('q4_v1_rc_switch.png', format='png', dpi=150, bbox_inches='tight')
plt.close()
