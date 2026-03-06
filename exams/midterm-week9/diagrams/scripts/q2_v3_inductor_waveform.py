"""
Q2-V3: Inductor with Piecewise Linear Current Waveform
Shows an inductor element and a piecewise linear i(t) waveform plot.
Uses matplotlib directly since this is a graph + component diagram.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import schemdraw
import schemdraw.elements as elm
from io import BytesIO
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 6))
gs = GridSpec(2, 1, height_ratios=[1, 3], hspace=0.3)

# Top: Inductor schematic using schemdraw
ax_circuit = fig.add_subplot(gs[0])
with schemdraw.Drawing(canvas=ax_circuit) as d:
    d.config(unit=3, fontsize=14, font='sans-serif')
    d += elm.Line().right().length(1)
    d += elm.Inductor().right().label('L')
    d += elm.Line().right().length(1)
    # Current arrow
    d.add(elm.CurrentLabelInline(direction='in').at(d.here).label('i(t)', fontsize=13))

ax_circuit.set_xlim(-0.5, 8)
ax_circuit.axis('off')
ax_circuit.set_title('Inductor with Piecewise Linear Current', fontsize=14, fontweight='bold')

# Bottom: Current waveform plot
ax_wave = fig.add_subplot(gs[1])

# Piecewise linear waveform (3 segments matching XML):
# Seg 1: 0→t1, ramp from 0 to Ipeak
# Seg 2: t1→t2, constant at Ipeak
# Seg 3: t2→t3, ramp from Ipeak down to 0
t = [0, 1, 2.5, 4]
i_vals = [0, 3, 3, 0]

ax_wave.plot(t, i_vals, 'b-', linewidth=2.5)
ax_wave.set_xlabel('t (ms)', fontsize=13)
ax_wave.set_ylabel('i(t)', fontsize=13)
ax_wave.set_xticks(t)
ax_wave.set_xticklabels(['0', 't₁', 't₂', 't₃'], fontsize=12)
ax_wave.set_yticks([0, 3])
ax_wave.set_yticklabels(['0', 'I_peak'], fontsize=12)
ax_wave.grid(True, alpha=0.3)
ax_wave.set_xlim(-0.2, 4.5)
ax_wave.set_ylim(-0.3, 3.8)

# Mark key point at t1 (end of Segment 1, where i = Ipeak)
ax_wave.plot(1, 3, 'ro', markersize=8, zorder=5)

# Energy formula box
textstr = r'$E = \frac{1}{2} L \cdot i(t)^2$'
props = dict(boxstyle='round', facecolor='#e8f5e9', edgecolor='green', alpha=0.8)
ax_wave.text(3.5, 3.2, textstr, fontsize=13, verticalalignment='top', bbox=props)

# Voltage relationship
textstr2 = r'$v_L = L \cdot \frac{di}{dt}$'
ax_wave.text(3.5, 2.2, textstr2, fontsize=13, verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('q2_v3_inductor_waveform.svg', format='svg', bbox_inches='tight')
plt.savefig('q2_v3_inductor_waveform.png', format='png', dpi=150, bbox_inches='tight')
plt.close()
