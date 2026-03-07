"""Q4: C-Core Electromagnet — Physical drawing with air gap and coil."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(7, 6))
ax.set_xlim(-1, 8)
ax.set_ylim(-1.5, 7)
ax.set_aspect('equal')
ax.axis('off')

# C-core dimensions
core_w = 0.8        # core leg width
outer_w = 6.0       # outer width
outer_h = 5.5       # outer height
gap = 0.5           # air gap size

# Core pieces (C-shape = top bar + left leg + right leg; bottom bar with gap)
core_color = '#B0B0B0'
lw = 1.5

# Top horizontal bar
top_bar = patches.FancyBboxPatch((0, outer_h - core_w), outer_w, core_w,
                                  boxstyle='square,pad=0', facecolor=core_color,
                                  edgecolor='black', linewidth=lw, zorder=2)
ax.add_patch(top_bar)

# Left vertical leg
left_leg = patches.FancyBboxPatch((0, gap), core_w, outer_h - core_w - gap,
                                   boxstyle='square,pad=0', facecolor=core_color,
                                   edgecolor='black', linewidth=lw, zorder=2)
ax.add_patch(left_leg)

# Right vertical leg
right_leg = patches.FancyBboxPatch((outer_w - core_w, gap), core_w, outer_h - core_w - gap,
                                    boxstyle='square,pad=0', facecolor=core_color,
                                    edgecolor='black', linewidth=lw, zorder=2)
ax.add_patch(right_leg)

# Bottom bar — left half (up to gap)
bot_left = patches.FancyBboxPatch((0, 0), outer_w / 2 - gap / 2, core_w * 0.6,
                                   boxstyle='square,pad=0', facecolor=core_color,
                                   edgecolor='black', linewidth=lw, zorder=2)
ax.add_patch(bot_left)

# Bottom bar — right half (after gap)
bot_right = patches.FancyBboxPatch((outer_w / 2 + gap / 2, 0),
                                    outer_w / 2 - gap / 2, core_w * 0.6,
                                    boxstyle='square,pad=0', facecolor=core_color,
                                    edgecolor='black', linewidth=lw, zorder=2)
ax.add_patch(bot_right)

# Air gap hatching
gap_x_start = outer_w / 2 - gap / 2
gap_x_end = outer_w / 2 + gap / 2
for y_h in np.linspace(0.05, core_w * 0.55, 6):
    ax.plot([gap_x_start, gap_x_end], [y_h, y_h + 0.1], 'k-', linewidth=0.5, zorder=3)

# Coil on left leg (shown as hatched rectangle)
coil_x = core_w
coil_y = 1.5
coil_w = 1.0
coil_h = 2.5
coil_rect = patches.FancyBboxPatch((coil_x, coil_y), coil_w, coil_h,
                                    boxstyle='square,pad=0',
                                    facecolor='#FFE0B0', edgecolor='black',
                                    linewidth=1.2, zorder=3)
ax.add_patch(coil_rect)

# Diagonal lines inside coil to indicate winding
for i in range(8):
    y_line = coil_y + (i + 0.5) * coil_h / 8
    ax.plot([coil_x + 0.1, coil_x + coil_w - 0.1],
            [y_line - 0.1, y_line + 0.1], 'k-', linewidth=0.7, zorder=4)

ax.text(coil_x + coil_w / 2, coil_y + coil_h + 0.25, '$N$ turns',
        fontsize=13, ha='center', va='bottom', fontstyle='italic',
        fontfamily='sans-serif')

# Current arrow
ax.annotate('$I$', xy=(coil_x + coil_w + 0.2, coil_y + coil_h),
            xytext=(coil_x + coil_w + 1.0, coil_y + coil_h + 0.8),
            fontsize=14, ha='center', va='center',
            fontfamily='sans-serif',
            arrowprops=dict(arrowstyle='->', lw=1.2))

# Flux arrows (going clockwise around the core)
# Top bar: left to right
ax.annotate('', xy=(4.0, outer_h - core_w / 2), xytext=(2.0, outer_h - core_w / 2),
            arrowprops=dict(arrowstyle='->', color='#CC0000', lw=2.0), zorder=5)

# Right leg: top to bottom
ax.annotate('', xy=(outer_w - core_w / 2, 2.0), xytext=(outer_w - core_w / 2, 3.5),
            arrowprops=dict(arrowstyle='->', color='#CC0000', lw=2.0), zorder=5)

# Bottom bar: right to left (right side)
ax.annotate('', xy=(outer_w / 2 + gap / 2 + 0.3, core_w * 0.3),
            xytext=(outer_w - core_w - 0.2, core_w * 0.3),
            arrowprops=dict(arrowstyle='->', color='#CC0000', lw=2.0), zorder=5)

# Bottom bar: right to left (left side, through gap)
ax.annotate('', xy=(1.0, core_w * 0.3),
            xytext=(outer_w / 2 - gap / 2 - 0.3, core_w * 0.3),
            arrowprops=dict(arrowstyle='->', color='#CC0000', lw=2.0), zorder=5)

# Left leg: bottom to top
ax.annotate('', xy=(core_w / 2, 3.5), xytext=(core_w / 2, 2.0),
            arrowprops=dict(arrowstyle='->', color='#CC0000', lw=2.0), zorder=5)

# Phi label
ax.text(3.0, outer_h - core_w / 2 + 0.35, '$\\Phi$', fontsize=15,
        color='#CC0000', ha='center', va='bottom', fontfamily='sans-serif')

# Dimension labels
# Core path length
ax.annotate('', xy=(-0.5, 0), xytext=(-0.5, outer_h),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.0))
ax.text(-0.8, outer_h / 2, '$\\ell_c$', fontsize=14, ha='right', va='center',
        fontfamily='sans-serif', rotation=90)

# Air gap length
ax.annotate('', xy=(outer_w / 2 - gap / 2, -0.5), xytext=(outer_w / 2 + gap / 2, -0.5),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.0))
ax.text(outer_w / 2, -0.9, '$\\ell_g$', fontsize=14, ha='center', va='top',
        fontfamily='sans-serif')

# Cross-section label
ax.annotate('$A_c$', xy=(outer_w - core_w / 2, outer_h - core_w),
            xytext=(outer_w + 0.5, outer_h - core_w - 0.5),
            fontsize=14, ha='left', va='top',
            fontfamily='sans-serif',
            arrowprops=dict(arrowstyle='->', lw=1.0))

# Permeability label on core
ax.text(outer_w / 2, outer_h - core_w / 2, '$\\mu_r \\mu_0$',
        fontsize=12, ha='center', va='center',
        fontfamily='sans-serif',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8),
        zorder=6)

plt.tight_layout()
plt.savefig('diagrams/week10/q4_ccore_physical.svg', format='svg', bbox_inches='tight')
plt.close()
