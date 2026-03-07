"""Q5: Parallel RLC Natural Response — Four-switch circuit (Nilsson P8.11).

Topology: 4 SPST switches on the top rail divide the circuit into three sections.
t < 0: SW1, SW4 closed (left/right loops active); SW2, SW3 open (middle isolated).
       Left loop:  Is || Ra || L — inductor charges (short at DC).
       Right loop:  C in series with Rb + Vdc — capacitor charges to Vdc.
t = 0: SW1, SW4 open; SW2, SW3 close.
       -> L || R || C source-free parallel RLC, v_o(t) across R.

Layout (left to right):
    Is  Ra  [SW1]  L  [SW2]  R(vo)  [SW3]  C  [SW4]  Rb--Vdc
     |   |          |          |              |              |
     +---+----------+----------+--------------+--------------+

Rendering approach:
  - Schemdraw: all passive components, wires, dots
  - Matplotlib: switches (manual drawing for open/closed distinction)
  - Matplotlib: v_o(t) polarity labels (+, -, v_o(t))
"""
import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Helper: draw SPST switch with matplotlib ─────────────────
def draw_switch(ax, left_pt, right_pt, closed, label_text, name=None):
    """Draw a SPST switch manually on the matplotlib axes.

    left_pt, right_pt: (x, y) tuples for the two contacts.
    closed: True = arm touches contact (SW1/SW4 at t<0).
    label_text: annotation above the switch, e.g. 't = 0\n(opens)'.
    name: optional switch name label (e.g. 'SW1') drawn below the switch.
    """
    x1, y1 = float(left_pt[0]), float(left_pt[1])
    x2, y2 = float(right_pt[0]), float(right_pt[1])
    mid_x = (x1 + x2) / 2
    gap = x2 - x1

    # Left contact: filled dot
    ax.plot(x1, y1, 'ko', markersize=5, zorder=10)
    # Right contact: open circle
    ax.plot(x2, y2, 'o', color='black', markersize=5,
            markerfacecolor='white', markeredgewidth=1.5, zorder=10)

    if closed:
        # Arm: straight line from left to right (touching)
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, zorder=9)
    else:
        # Arm: angled up from left, not reaching right contact
        arm_x = x1 + gap * 0.8
        arm_y = y1 + gap * 0.4
        ax.plot([x1, arm_x], [y1, arm_y], 'k-', linewidth=1.5, zorder=9)

    # Label above
    ax.text(mid_x, y1 + gap * 0.8, label_text,
            ha='center', va='bottom', fontsize=11, fontfamily='sans-serif')

    # Switch name below
    if name:
        ax.text(mid_x, y1 - gap * 0.3, name, ha='center', va='top',
                fontsize=10, fontfamily='sans-serif', fontstyle='italic')


# ── Build circuit with schemdraw ─────────────────────────────
SW_GAP = 1.2   # horizontal gap reserved for each switch
WIRE = 0.3     # short wire segments flanking each switch

d = schemdraw.Drawing()
d.config(unit=3.0, fontsize=14, font='sans-serif')

# ── Is (current source, arrow up) ────────────────────────────
Is = d.add(elm.SourceI().up().label('$I_s$', loc='top', ofst=0.15))
bot_is = Is.start
top_is = Is.end

# Top rail to Ra
d += elm.Line().right().length(1.5).at(top_is)
d += elm.Dot()
top_ra = d.here

# Ra (vertical down, parallel to Is)
d.push()
d.add(elm.Resistor().down().at(top_ra)
      .label('$R_a$', loc='bottom', ofst=0.15))
bot_ra = d.here
d.pop()

# ── SW1 gap (closed -> opens at t=0) ─────────────────────────
d += elm.Line().right().length(WIRE)
sw1_left = d.here
sw1_right = (sw1_left[0] + SW_GAP, sw1_left[1])
d += elm.Line().right().length(WIRE).at(sw1_right)
d += elm.Dot()
top_L = d.here

# ── L branch (vertical inductor) ─────────────────────────────
d.push()
d.add(elm.Inductor2(loops=4).down().at(top_L)
      .label('$L$', loc='bottom', ofst=0.15))
bot_L = d.here
d.pop()

# ── SW2 gap (open -> closes at t=0) ──────────────────────────
d += elm.Line().right().length(1.0)  # extra space so v_o(t) label doesn't crowd L
sw2_left = d.here
sw2_right = (sw2_left[0] + SW_GAP, sw2_left[1])
d += elm.Line().right().length(WIRE).at(sw2_right)
d += elm.Dot()
top_R = d.here

# ── R branch (vertical resistor) — polarity added via matplotlib
d.push()
R = d.add(elm.Resistor().down().at(top_R)
          .label('$R$', loc='bottom', ofst=0.15))
bot_R = d.here
d.pop()

# ── SW3 gap (open -> closes at t=0) ──────────────────────────
d += elm.Line().right().length(WIRE)
sw3_left = d.here
sw3_right = (sw3_left[0] + SW_GAP, sw3_left[1])
d += elm.Line().right().length(WIRE).at(sw3_right)
d += elm.Dot()
top_C = d.here

# ── C branch (vertical capacitor) ────────────────────────────
d.push()
d.add(elm.Capacitor().down().at(top_C)
      .label('$C$', loc='bottom', ofst=0.15))
bot_C = d.here
d.pop()

# ── SW4 gap (closed -> opens at t=0) ─────────────────────────
d += elm.Line().right().length(WIRE)
sw4_left = d.here
sw4_right = (sw4_left[0] + SW_GAP, sw4_left[1])
d += elm.Line().right().at(sw4_right).length(0)  # anchor point, no visible wire

# ── Rb (horizontal resistor directly on top rail) ────────────
d.add(elm.Resistor().right()
      .label('$R_b$', loc='top', ofst=0.15))

# ── Vdc (vertical, + on top) ─────────────────────────────────
d.add(elm.SourceV().down()
      .label('$V_{dc}$', loc='bottom', ofst=0.15)
      .reverse())
bot_Vdc = d.here

# ── Bottom rail (continuous) ─────────────────────────────────
d += elm.Line().right().at(bot_is).tox(bot_ra)
d += elm.Line().right().tox(bot_L)
d += elm.Line().right().tox(bot_R)
d += elm.Line().right().tox(bot_C)
d += elm.Line().right().tox(bot_Vdc)

# ── Render schemdraw, then annotate with matplotlib ──────────
d.draw()
fig = d.fig.fig    # matplotlib Figure
ax = d.fig.ax      # matplotlib Axes

# Draw the 4 switches
draw_switch(ax, sw1_left, sw1_right, closed=True,  label_text='t = 0\n(opens)',  name='SW1')
draw_switch(ax, sw2_left, sw2_right, closed=False, label_text='t = 0\n(closes)', name='SW2')
draw_switch(ax, sw3_left, sw3_right, closed=False, label_text='t = 0\n(closes)', name='SW3')
draw_switch(ax, sw4_left, sw4_right, closed=True,  label_text='t = 0\n(opens)',  name='SW4')

# v_o(t) polarity labels (to the left of R)
rx = float(top_R[0])
ry_top = float(top_R[1])
ry_bot = float(bot_R[1])
ry_mid = (ry_top + ry_bot) / 2

ax.text(rx - 0.4, ry_top - 0.3, '+', fontsize=14, fontfamily='sans-serif',
        ha='center', va='center')
ax.text(rx - 0.6, ry_mid, '$v_o(t)$', fontsize=13, fontfamily='sans-serif',
        ha='center', va='center')
ax.text(rx - 0.4, ry_bot + 0.3, '\u2212', fontsize=14, fontfamily='sans-serif',
        ha='center', va='center')

# Save SVG
fig.savefig('weekly/week10/diagrams/q5_parallel_rlc_natural_switches.svg',
            format='svg', bbox_inches='tight')
plt.close(fig)
