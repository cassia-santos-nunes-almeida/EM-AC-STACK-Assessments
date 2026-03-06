"""Q3: Toroidal Core — Physical cross-section drawing with air gap and coil."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(7, 7))
ax.set_xlim(-4.5, 4.5)
ax.set_ylim(-4.5, 4.5)
ax.set_aspect('equal')
ax.axis('off')

# Toroid parameters
R_outer = 3.2
R_inner = 2.2
R_mid = (R_outer + R_inner) / 2
core_width = R_outer - R_inner

# Air gap angular extent (about 15 degrees centred at bottom)
gap_half_angle = 7.5  # degrees

# Draw ferromagnetic core as annular arc (excluding gap)
# Core section: from gap_half_angle to (360 - gap_half_angle)
core_start = -90 + gap_half_angle
core_extent = 360 - 2 * gap_half_angle

# Outer arc
theta_core = np.linspace(np.radians(core_start), np.radians(core_start + core_extent), 200)
x_outer = R_outer * np.cos(theta_core)
y_outer = R_outer * np.sin(theta_core)

# Inner arc (reversed)
x_inner = R_inner * np.cos(theta_core[::-1])
y_inner = R_inner * np.sin(theta_core[::-1])

# Fill core
core_x = np.concatenate([x_outer, x_inner])
core_y = np.concatenate([y_outer, y_inner])
ax.fill(core_x, core_y, color='#B0B0B0', edgecolor='black', linewidth=1.5, zorder=2)

# Draw air gap region (hatched)
theta_gap_left = np.linspace(np.radians(-90 - gap_half_angle), np.radians(-90 + gap_half_angle), 30)
x_gap_outer = R_outer * np.cos(theta_gap_left)
y_gap_outer = R_outer * np.sin(theta_gap_left)
x_gap_inner = R_inner * np.cos(theta_gap_left[::-1])
y_gap_inner = R_inner * np.sin(theta_gap_left[::-1])

gap_x = np.concatenate([x_gap_outer, x_gap_inner])
gap_y = np.concatenate([y_gap_outer, y_gap_inner])
ax.fill(gap_x, gap_y, color='white', edgecolor='black', linewidth=1.5, zorder=2)

# Hatching for air gap
for i in range(5):
    frac = (i + 1) / 6
    r = R_inner + frac * core_width
    x1 = r * np.cos(np.radians(-90 - gap_half_angle * 0.8))
    y1 = r * np.sin(np.radians(-90 - gap_half_angle * 0.8))
    x2 = r * np.cos(np.radians(-90 + gap_half_angle * 0.8))
    y2 = r * np.sin(np.radians(-90 + gap_half_angle * 0.8))
    ax.plot([x1, x2], [y1, y2], 'k-', linewidth=0.5, zorder=3)

# Draw coil windings on top portion as small rectangles
n_turns_shown = 14
wind_start = np.radians(30)
wind_end = np.radians(150)
wind_angles = np.linspace(wind_start, wind_end, n_turns_shown)

for angle in wind_angles:
    # Outer winding dot
    x_w = (R_outer + 0.2) * np.cos(angle)
    y_w = (R_outer + 0.2) * np.sin(angle)
    ax.plot(x_w, y_w, 'ko', markersize=4, zorder=4)

    # Inner winding cross
    x_w2 = (R_inner - 0.2) * np.cos(angle)
    y_w2 = (R_inner - 0.2) * np.sin(angle)
    size = 0.1
    ax.plot([x_w2 - size, x_w2 + size], [y_w2 - size, y_w2 + size], 'k-', linewidth=1.2, zorder=4)
    ax.plot([x_w2 - size, x_w2 + size], [y_w2 + size, y_w2 - size], 'k-', linewidth=1.2, zorder=4)

# Coil bracket / label
ax.annotate('$N$ turns', xy=(0, R_outer + 0.6), fontsize=13,
            ha='center', va='bottom', fontstyle='italic',
            fontfamily='sans-serif')

# B-field arrows inside core (clockwise)
arrow_angles = [0, 45, 135, 180, 225]
for angle_deg in arrow_angles:
    angle = np.radians(angle_deg)
    x_arr = R_mid * np.cos(angle)
    y_arr = R_mid * np.sin(angle)
    # Tangent direction (clockwise: negative tangent)
    dx = -np.sin(angle) * 0.35
    dy = np.cos(angle) * 0.35
    ax.annotate('', xy=(x_arr + dx, y_arr + dy), xytext=(x_arr - dx, y_arr - dy),
                arrowprops=dict(arrowstyle='->', color='#CC0000', lw=1.8),
                zorder=5)

# B label inside core
ax.text(R_mid * np.cos(np.radians(0)) + 0.5, R_mid * np.sin(np.radians(0)),
        '$\\mathbf{B}$', fontsize=15, color='#CC0000', ha='left', va='center',
        fontfamily='sans-serif', zorder=5)

# Labels for core section length
ax.annotate('', xy=(R_outer + 0.5, -1.0), xytext=(R_outer + 0.5, 1.0),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
ax.text(R_outer + 0.8, 0, '$\\ell_1$', fontsize=14, ha='left', va='center',
        fontfamily='sans-serif')

# Label for air gap length
ax.annotate('', xy=(0.6, -R_mid - 0.6), xytext=(-0.6, -R_mid - 0.6),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
ax.text(0, -R_mid - 1.0, '$\\ell_2$', fontsize=14, ha='center', va='top',
        fontfamily='sans-serif')

# Cross-section label
ax.annotate('$A$', xy=(R_outer * np.cos(np.radians(45)) + 0.15,
                         R_outer * np.sin(np.radians(45)) + 0.15),
            fontsize=14, ha='left', va='bottom',
            fontfamily='sans-serif',
            arrowprops=dict(arrowstyle='->', lw=1.0),
            xytext=(R_outer * np.cos(np.radians(45)) + 0.8,
                    R_outer * np.sin(np.radians(45)) + 0.8))

# Permeability labels
ax.text(-R_mid * np.cos(np.radians(45)), R_mid * np.sin(np.radians(45)) - 0.1,
        '$\\mu_r$', fontsize=13, ha='center', va='center',
        fontfamily='sans-serif',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8),
        zorder=6)

# Current I label with arrow at wire end
ax.annotate('$I$', xy=((R_outer + 0.2) * np.cos(wind_angles[0]),
                        (R_outer + 0.2) * np.sin(wind_angles[0])),
            xytext=((R_outer + 1.2) * np.cos(wind_angles[0]),
                    (R_outer + 1.2) * np.sin(wind_angles[0])),
            fontsize=14, ha='center', va='center',
            fontfamily='sans-serif',
            arrowprops=dict(arrowstyle='->', lw=1.2))

plt.tight_layout()
plt.savefig('diagrams/week10/q3_toroid_physical.svg', format='svg', bbox_inches='tight')
plt.close()
