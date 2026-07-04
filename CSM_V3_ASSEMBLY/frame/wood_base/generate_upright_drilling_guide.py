# -*- coding: utf-8 -*-
"""
Wood base -- upright drilling template.
Shows the 4 M5 clearance holes for the 2020 upright bottom mounts,
with all measurements a hand-driller needs.

Prints as PNG + PDF into the wood_base folder.
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
import matplotlib.patheffects as pe

HERE = os.path.dirname(os.path.abspath(__file__))

# Wood base dimensions
W, D, T = 500.0, 400.0, 12.7   # X, Y, Z (measured 12.7 mm)
# Upright hole positions (relative to base CENTER)
UP_XS = (+150.0, -150.0)
UP_YS = (+120.0, -120.0)
HOLE_D = 5.5  # M5 clearance
# Take-down center hole for context
TD_D = 100.0

# Distances from EDGES (this is what you actually measure)
EDGE_X = W/2.0 - abs(UP_XS[0])   # 100 mm
EDGE_Y = D/2.0 - abs(UP_YS[0])   # 80 mm
HOLE_SP_X = 2 * abs(UP_XS[0])    # 300 mm between holes in X
HOLE_SP_Y = 2 * abs(UP_YS[0])    # 240 mm between holes in Y

# Convert to origin-at-corner coords so measurements read from
# the edge (which is how you actually hand-measure)
def to_corner(x, y):
    return x + W/2.0, y + D/2.0

fig, ax = plt.subplots(figsize=(14, 11), dpi=180)

# Wood base outline (as viewed from the TOP face)
ax.add_patch(Rectangle((0, 0), W, D,
                        facecolor='#e6d3a5', edgecolor='black', lw=2.5))
# Wood-grain hatch
for gy in range(0, int(D)+1, 12):
    ax.plot([0, W], [gy, gy], color='#c4a679', lw=0.4, alpha=0.5)

# Center reference cross
ax.plot([W/2, W/2], [0, D], 'k--', lw=0.5, alpha=0.5)
ax.plot([0, W], [D/2, D/2], 'k--', lw=0.5, alpha=0.5)
ax.text(W/2 + 4, D/2 + 4, 'CENTER  (0, 0)', fontsize=8, color='#555',
        style='italic')

# Take-down center hole
cx, cy = to_corner(0, 0)
ax.add_patch(Circle((cx, cy), TD_D/2.0, facecolor='#fff', edgecolor='black', lw=1.5))
ax.text(cx, cy, f'Ø{TD_D:.0f}\n(pre-cut)', ha='center', va='center',
        fontsize=8, color='#333', style='italic')

# The 4 UPRIGHT MOUNT HOLES -- highlighted
hole_positions = []
for sx in UP_XS:
    for sy in UP_YS:
        hx, hy = to_corner(sx, sy)
        hole_positions.append((hx, hy, sx, sy))

for hx, hy, sx, sy in hole_positions:
    # Big red circle to show the hole clearly
    ax.add_patch(Circle((hx, hy), HOLE_D * 2.5, facecolor='none',
                         edgecolor='red', lw=1.5, linestyle=':', alpha=0.6))
    # Actual hole size (to scale)
    ax.add_patch(Circle((hx, hy), HOLE_D/2.0, facecolor='red',
                         edgecolor='#600', lw=1.5))
    # Position label
    label = f'({sx:+.0f}, {sy:+.0f})'
    label_dy = 22 if sy > 0 else -22
    ax.text(hx, hy + label_dy, label, ha='center', va='center',
            fontsize=10, color='#a00', fontweight='bold')

# Dimension helpers
def dim_h(ax, x1, x2, y, label, offset=0, color='blue'):
    """Horizontal dimension line."""
    ax.annotate('', xy=(x1, y), xytext=(x2, y),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.2))
    ax.text((x1+x2)/2, y + 6 + offset, label, ha='center', va='bottom',
            fontsize=11, color=color, fontweight='bold',
            path_effects=[pe.withStroke(linewidth=3, foreground='white')])

def dim_v(ax, y1, y2, x, label, offset=0, color='blue'):
    """Vertical dimension line."""
    ax.annotate('', xy=(x, y1), xytext=(x, y2),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.2))
    ax.text(x + 8 + offset, (y1+y2)/2, label, ha='left', va='center',
            fontsize=11, color=color, fontweight='bold', rotation=90,
            path_effects=[pe.withStroke(linewidth=3, foreground='white')])

# ---- Edge dimensions (what you actually measure with a ruler) ----
# X: from LEFT edge to nearest hole
hole_left_x = W/2.0 - abs(UP_XS[0])
dim_h(ax, 0, hole_left_x, 30, f'{EDGE_X:.0f} mm (from edge)', color='#0060c0')
dim_h(ax, hole_left_x + HOLE_D, W - hole_left_x - HOLE_D,
      30, f'{HOLE_SP_X:.0f} mm (between holes)', color='#0060c0')
dim_h(ax, W - hole_left_x, W, 30, f'{EDGE_X:.0f}', color='#0060c0')

# Y: from BOTTOM edge to nearest hole
hole_bot_y = D/2.0 - abs(UP_YS[0])
dim_v(ax, 0, hole_bot_y, 30, f'{EDGE_Y:.0f} mm', color='#c04000')
dim_v(ax, hole_bot_y + HOLE_D, D - hole_bot_y - HOLE_D,
      30, f'{HOLE_SP_Y:.0f} mm (between holes)', color='#c04000')
dim_v(ax, D - hole_bot_y, D, 30, f'{EDGE_Y:.0f}', color='#c04000')

# Overall dimensions on the outside
dim_h(ax, 0, W, -20, f'{W:.0f} mm  (full width)', color='#333')
dim_v(ax, 0, D, -25, f'{D:.0f} mm  (full depth)', color='#333')

# Title block
title_text = (
    "CSM V3 -- WOOD BASE  |  Upright hole drilling template\n"
    "500 x 400 x 12.7 mm Baltic Birch plywood, top face shown\n"
    f"4 x M5 clearance holes at (±150, ±120) mm from center -- drill through, both sides"
)
fig.suptitle(title_text, fontsize=13, fontweight='bold', y=0.97)

# Side/info panel
info_text = (
    "DRILL SPEC\n"
    "  Bit:      Ø5.5 mm  (M5 clearance)\n"
    "  Depth:    THROUGH (12.7 mm plywood)\n"
    "  Fastener: M5 x 25 SHCS from below + Loctite 242\n"
    "            (self-taps into 2020 end bore)\n\n"
    "HAND-DRILL PROCEDURE\n"
    "  1. Place wood base TOP FACE UP\n"
    "  2. Measure and mark 4 hole positions:\n"
    "       100 mm from each X-edge (left & right)\n"
    "       80 mm from each Y-edge (front & back)\n"
    "     -> 4 crosses at the 4 corners of a\n"
    "        300 x 240 mm rectangle centered on\n"
    "        the take-down hole.\n"
    "  3. Center-punch each mark to keep the bit\n"
    "     from wandering when you start the hole.\n"
    "  4. Place scrap plywood UNDER the wood base\n"
    "     to prevent tear-out on the exit face.\n"
    "  5. Drill straight down at each mark with a\n"
    "     Ø5.5 mm bit (14/64\" or 7/32\" imperial).\n"
    "  6. Break the top edges lightly with a\n"
    "     countersink or larger bit for clean look.\n\n"
    "TOLERANCE\n"
    "  Position: +/- 1 mm  (the 2020's end bore\n"
    "           has 1-2 mm clearance)\n"
    "  Diameter: 5.5 to 6.0 mm is fine\n"
    "  Squareness: keep the bit vertical -- a slanted\n"
    "           hole will tilt the whole upright"
)
ax.text(W + 40, D - 10, info_text, fontsize=9, va='top', ha='left',
        family='monospace', color='#222',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#f7f5ee',
                  edgecolor='#888', lw=1))

# Legend for hole colors
legend_text = (
    "LEGEND\n"
    "  Red circle:   NEW hole to drill (Ø5.5 mm)\n"
    "  Red dotted:   Drilling target area (not to scale)\n"
    "  White circle: Existing pre-cut hole (Ø100 take-down)\n"
    "  Dashed cross: Center reference axes"
)
ax.text(W + 40, 100, legend_text, fontsize=9, va='top', ha='left',
        family='monospace', color='#222',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#eef', edgecolor='#66a', lw=1))

# Axis setup
ax.set_xlim(-50, W + 340)
ax.set_ylim(-60, D + 40)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

fig.text(0.5, 0.01,
         'github.com/leoalex196912/ChatGistory  *  '
         'CSM_V3_ASSEMBLY/frame/wood_base/  *  '
         '2026-06-29',
         ha='center', fontsize=8, color='#888')

out_png = os.path.join(HERE, "CSM_V3_WoodBase_upright_drilling_guide.png")
out_pdf = os.path.join(HERE, "CSM_V3_WoodBase_upright_drilling_guide.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
