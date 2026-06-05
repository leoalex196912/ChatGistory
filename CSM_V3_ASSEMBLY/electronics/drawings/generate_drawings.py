# -*- coding: utf-8 -*-
"""
CSM V3 -- Wood Base Electrical Mounting Drawings Generator
============================================================
Produces engineering-style drawings of the wood base with all electronics
positioned for drilling. Components are rendered with realistic visual
features (vents, terminals, PCB markings, USB ports, etc.) -- not just
colored rectangles.

Outputs:
  wood_base_top.png  / .pdf       -- top view drilling diagram
  operator_panel.png / .pdf       -- front operator panel detail
  components_card.png / .pdf      -- product reference card with ASINs

Run with FreeCAD's Python (which bundles matplotlib):
  "C:/Program Files/FreeCAD 1.1/bin/python.exe" generate_drawings.py
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch, Wedge
from matplotlib.lines import Line2D
import matplotlib.transforms as mtransforms
import numpy as np

# ============================================================
# DIMENSIONS (mm) -- locked from machine_datums.py
# ============================================================
WB_W, WB_D, WB_T = 500, 400, 18
HOLE_D = 100
UP_X = [+150, -150]
UP_Y = [+120, -120]
UP_W = 20
MOTOR_X, MOTOR_Y = 85, -47

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# Drawing style
# ============================================================
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 9,
    'axes.linewidth': 1.0,
    'lines.linewidth': 1.0,
})

# Engineering color palette
WOOD_FILL    = '#D2B48C'    # tan walnut
WOOD_EDGE    = '#5a4020'
DIM_COLOR    = '#222'
HOLE_COLOR   = '#d40000'
RESERVED_FILL = '#ffd6d6'
RESERVED_EDGE = '#c00000'
ALUMINUM     = '#B8BCC4'
ALUMINUM_DK  = '#7a7e85'

# Component visual signatures
PSU_BODY     = '#9aa1a8'
PSU_VENT     = '#4a4d52'
PSU_LABEL_BG = '#f5e7a8'
MEGA_PCB     = '#1f4ea8'
PI_PCB       = '#0c6e3a'
TB6600_BODY  = '#c43838'
TB6600_FIN   = '#7a2222'
BUCK_PCB     = '#0f6b34'
TERMINAL_BLK = '#e6dc4a'
PANEL_FILL   = '#dadde0'
ESTOP_RED    = '#d40000'
ESTOP_BLACK  = '#1a1a1a'
IEC_BODY     = '#1a1a1a'
FUSE_BODY    = '#3a3a3a'

# ============================================================
# Helpers: dimension lines, callouts
# ============================================================
def dim_h(ax, x1, x2, y, label, offset_y=18, color=DIM_COLOR, fontsize=8):
    """Horizontal dimension line below position y."""
    yo = y - offset_y
    ax.annotate('', xy=(x2, yo), xytext=(x1, yo),
                arrowprops=dict(arrowstyle='<|-|>', color=color, lw=1.0,
                                shrinkA=0, shrinkB=0))
    ax.plot([x1, x1], [y - 2, yo - 4], color=color, lw=0.6)
    ax.plot([x2, x2], [y - 2, yo - 4], color=color, lw=0.6)
    ax.text((x1 + x2) / 2, yo - 2, label, ha='center', va='top',
            fontsize=fontsize, color=color,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none'))

def dim_v(ax, y1, y2, x, label, offset_x=18, color=DIM_COLOR, fontsize=8):
    """Vertical dimension line to the right of position x."""
    xo = x + offset_x
    ax.annotate('', xy=(xo, y2), xytext=(xo, y1),
                arrowprops=dict(arrowstyle='<|-|>', color=color, lw=1.0,
                                shrinkA=0, shrinkB=0))
    ax.plot([x + 2, xo + 4], [y1, y1], color=color, lw=0.6)
    ax.plot([x + 2, xo + 4], [y2, y2], color=color, lw=0.6)
    ax.text(xo + 2, (y1 + y2) / 2, label, ha='left', va='center',
            fontsize=fontsize, color=color, rotation=90,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none'))

def callout(ax, x, y, text, dx=40, dy=40, color=DIM_COLOR, fontsize=8):
    """Leader line with text box."""
    tx, ty = x + dx, y + dy
    ax.annotate(text, xy=(x, y), xytext=(tx, ty),
                fontsize=fontsize, color=color, ha='left',
                arrowprops=dict(arrowstyle='-', color=color, lw=0.8),
                bbox=dict(boxstyle='round,pad=0.4', fc='#fffbe0', ec=color, lw=0.8))

def draw_hole(ax, x, y, dia, label=None, fs=7):
    """Drill hole marker with diameter."""
    r = dia / 2
    ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor=HOLE_COLOR, lw=1.2))
    ax.plot([x - r * 1.6, x + r * 1.6], [y, y], color=HOLE_COLOR, lw=0.5)
    ax.plot([x, x], [y - r * 1.6, y + r * 1.6], color=HOLE_COLOR, lw=0.5)
    if label:
        ax.text(x + r + 1.5, y + r + 1.5, label, fontsize=fs, color=HOLE_COLOR)

# ============================================================
# Component renderers (each draws a visually distinctive component)
# ============================================================

def draw_psu(ax, cx, cy):
    """Mean Well S-250-24 (199 x 110 x 50). Long axis along Y."""
    w, h = 110, 199
    x0, y0 = cx - w / 2, cy - h / 2
    # Body (silver with subtle gradient effect via two rects)
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=PSU_BODY,
                           edgecolor=ALUMINUM_DK, lw=1.2))
    # Ventilation slots on top (long slots in X direction)
    for vy in np.linspace(y0 + 25, y0 + h - 25, 9):
        ax.add_patch(Rectangle((x0 + 12, vy - 1), w - 24, 2,
                               facecolor=PSU_VENT, edgecolor='none'))
    # Terminal block on +Y end (the back/inboard end)
    ax.add_patch(Rectangle((x0 + 10, y0 + h - 22), w - 20, 16,
                           facecolor='#1a1a1a', edgecolor='#000', lw=0.8))
    # Terminal screws (10 positions)
    for i, tx in enumerate(np.linspace(x0 + 18, x0 + w - 18, 10)):
        ax.add_patch(Circle((tx, y0 + h - 14), 1.3, facecolor='#999', edgecolor='#000', lw=0.5))
    # Voltage selector switch
    ax.add_patch(Rectangle((x0 + w - 25, y0 + 10), 15, 8,
                           facecolor='#c00', edgecolor='black', lw=0.5))
    ax.text(x0 + w - 17.5, y0 + 14, '115/230', fontsize=4.5, ha='center', va='center', color='white')
    # Label
    ax.add_patch(FancyBboxPatch((x0 + 8, y0 + 35), w - 16, 40,
                                boxstyle='round,pad=0.1',
                                facecolor=PSU_LABEL_BG, edgecolor='#a89030', lw=0.5))
    ax.text(cx, y0 + 65, 'MEAN WELL', fontsize=8, ha='center', fontweight='bold', color='#222')
    ax.text(cx, y0 + 55, 'S-250-24', fontsize=10, ha='center', fontweight='bold', color='#111')
    ax.text(cx, y0 + 45, '24V  10A  240W', fontsize=6, ha='center', color='#444')
    ax.text(cx, y0 + 38, 'B07Y7L664K', fontsize=5, ha='center', color='#666', style='italic')
    # Mounting holes (4x M4 chassis pattern, approximate)
    holes = [(cx - 47, cy - 90), (cx + 47, cy - 90),
             (cx - 47, cy + 90), (cx + 47, cy + 90)]
    for hx, hy in holes:
        draw_hole(ax, hx, hy, 4.5, label='M4', fs=6)
    return holes

def draw_tb6600(ax, cx, cy):
    """TB6600 Stepper Driver (~96 x 56 x 37)."""
    w, h = 96, 56
    x0, y0 = cx - w / 2, cy - h / 2
    # Red metal case
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=TB6600_BODY,
                           edgecolor='#660000', lw=1.2))
    # Heatsink fins on one side
    for fx in np.linspace(x0 + 8, x0 + 30, 6):
        ax.add_patch(Rectangle((fx, y0 + 8), 1.5, h - 16,
                               facecolor=TB6600_FIN, edgecolor='none'))
    # Screw terminals (left side: power+motor; right: signal)
    for i, ty in enumerate(np.linspace(y0 + 8, y0 + h - 8, 6)):
        ax.add_patch(Rectangle((x0 + w - 14, ty - 2), 10, 4,
                               facecolor='#1a1a1a', edgecolor='#000', lw=0.4))
        ax.add_patch(Circle((x0 + w - 9, ty), 1, facecolor='#aaa', edgecolor='#000', lw=0.3))
    # DIP switches
    ax.add_patch(Rectangle((x0 + 38, y0 + 20), 18, 12,
                           facecolor='#1a1a1a', edgecolor='black', lw=0.5))
    for i in range(6):
        ax.add_patch(Rectangle((x0 + 39 + i * 2.8, y0 + 22), 2, 8,
                               facecolor='white', edgecolor='black', lw=0.3))
    # Label
    ax.text(cx, y0 - 6, 'TB6600 (B08SG7L54W)', fontsize=7, ha='center', color='#444')
    ax.text(cx + 5, y0 + h / 2, 'TB6600', fontsize=9, ha='center', fontweight='bold', color='white')
    # Mounting flange holes (2x, on the long sides)
    holes = [(cx - 42, cy), (cx + 42, cy)]
    for hx, hy in holes:
        draw_hole(ax, hx, hy, 3.5, label='M3', fs=6)
    return holes

def draw_mega(ax, cx, cy):
    """Arduino Mega 2560 REV3 (102 x 54). Blue PCB with USB jack."""
    w, h = 102, 54
    x0, y0 = cx - w / 2, cy - h / 2
    # Blue PCB
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0',
                                facecolor=MEGA_PCB, edgecolor='#0c2860', lw=1.0))
    # USB-B port on +X end (right side)
    ax.add_patch(Rectangle((x0 + w - 4, y0 + h / 2 - 8), 12, 16,
                           facecolor=ALUMINUM, edgecolor=ALUMINUM_DK, lw=0.8))
    # Barrel jack
    ax.add_patch(Circle((x0 + w - 4, y0 + 12), 4, facecolor='#1a1a1a', edgecolor='#000'))
    # ATmega chip
    ax.add_patch(Rectangle((x0 + 50, y0 + 20), 18, 18,
                           facecolor='#1a1a1a', edgecolor='black', lw=0.5))
    ax.text(x0 + 59, y0 + 29, 'ATmega\n2560', fontsize=4.5, ha='center', va='center', color='white')
    # Pin headers (top and bottom rows)
    for row_y in [y0 + h - 2, y0 + 2]:
        for px in np.linspace(x0 + 6, x0 + w - 16, 30):
            ax.add_patch(Rectangle((px - 0.4, row_y - 0.8), 0.8, 1.6,
                                   facecolor='#1a1a1a', edgecolor='none'))
    # Reset button
    ax.add_patch(Rectangle((x0 + 4, y0 + 6), 4, 4, facecolor='#888', edgecolor='black', lw=0.3))
    # Label
    ax.text(cx, y0 - 6, 'Arduino Mega 2560 (B0046AMGW0)', fontsize=7, ha='center', color='#444')
    ax.text(x0 + 25, y0 + h / 2, 'MEGA\n2560', fontsize=7, ha='center', va='center',
            fontweight='bold', color='white')
    # Mounting holes (4x M3)
    holes = [(x0 + 4, y0 + 4), (x0 + 4, y0 + h - 4),
             (x0 + w - 4, y0 + 4), (x0 + w - 4, y0 + h - 4)]
    for hx, hy in holes:
        draw_hole(ax, hx, hy, 3.2, label='M3', fs=5)
    return holes

def draw_buck(ax, cx, cy, label_main, label_use):
    """LM2596 buck (~43 x 21 mm). Green PCB with big inductor."""
    w, h = 43, 21
    x0, y0 = cx - w / 2, cy - h / 2
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=BUCK_PCB,
                           edgecolor='#053820', lw=1.0))
    # Big inductor (the visible toroid)
    ax.add_patch(Circle((x0 + 10, y0 + h / 2), 6, facecolor='#3a2a1a', edgecolor='black', lw=0.5))
    ax.add_patch(Circle((x0 + 10, y0 + h / 2), 3, facecolor='#5a4030', edgecolor='black', lw=0.3))
    # LM2596 chip (small SMD)
    ax.add_patch(Rectangle((x0 + 20, y0 + 8), 8, 5,
                           facecolor='#1a1a1a', edgecolor='black', lw=0.3))
    # Trim pot
    ax.add_patch(Circle((x0 + 32, y0 + 14), 3, facecolor='#aaa', edgecolor='black', lw=0.4))
    # Output capacitor (cylinder)
    ax.add_patch(Circle((x0 + 38, y0 + 7), 3, facecolor='#000080', edgecolor='black', lw=0.4))
    # Label
    ax.text(cx, y0 - 4, label_main, fontsize=6.5, ha='center', color='#222', fontweight='bold')
    ax.text(cx, y0 + h + 2, label_use, fontsize=6, ha='center', color='#666', style='italic')
    # Mounting holes (2x diagonal)
    holes = [(x0 + 3, y0 + 3), (x0 + w - 3, y0 + h - 3)]
    for hx, hy in holes:
        draw_hole(ax, hx, hy, 3.2, fs=4)
    return holes

def draw_terminal_block(ax, cx, cy):
    """24V distribution terminal block (50 x 20)."""
    w, h = 50, 20
    x0, y0 = cx - w / 2, cy - h / 2
    ax.add_patch(Rectangle((x0, y0), w, h, facecolor=TERMINAL_BLK,
                           edgecolor='#7a6b00', lw=1.0))
    # 4 terminal positions
    for i in range(4):
        tx = x0 + 8 + i * 11
        ax.add_patch(Rectangle((tx, y0 + 4), 8, 12,
                               facecolor='#3a3a3a', edgecolor='black', lw=0.4))
        ax.add_patch(Circle((tx + 4, y0 + 10), 1.5, facecolor='#aaa', edgecolor='black', lw=0.3))
    ax.text(cx, y0 - 4, '24V Distribution (WAGO 221)', fontsize=6.5, ha='center', color='#222')
    holes = [(x0 + 3, cy), (x0 + w - 3, cy)]
    for hx, hy in holes:
        draw_hole(ax, hx, hy, 3.2, fs=4)
    return holes

def draw_motor(ax, cx, cy):
    """NEMA 23 + HG5 gearbox (top view, square)."""
    # Outer = motor body 57x57
    w = 57
    x0, y0 = cx - w / 2, cy - w / 2
    ax.add_patch(Rectangle((x0, y0), w, w, facecolor=ALUMINUM_DK,
                           edgecolor='black', lw=1.5))
    # Center shaft
    ax.add_patch(Circle((cx, cy), 7, facecolor='#222', edgecolor='black', lw=1.0))
    # Corner mount holes (visible from above on gearbox flange)
    for sx in [-22, 22]:
        for sy in [-22, 22]:
            ax.add_patch(Circle((cx + sx, cy + sy), 2.5, facecolor='white', edgecolor='black', lw=0.5))
    # Inner gearbox circle visible
    ax.add_patch(Circle((cx, cy), 17, facecolor='none', edgecolor='#333', lw=0.5, linestyle='--'))
    ax.text(cx, cy - w / 2 - 6, 'NEMA 23 + HG5 gearbox', fontsize=6.5, ha='center', color='#222', fontweight='bold')
    ax.text(cx, cy - w / 2 - 12, '(StepperOnline 23HS22-2804S-HG5)', fontsize=5.5, ha='center', color='#666', style='italic')
    # Drill holes through wood for M5 mounts (gearbox flange PCD ~47.14)
    holes = []
    for ang_deg in [45, 135, 225, 315]:
        ang = np.radians(ang_deg)
        hx = cx + 47.14 / 2 * np.cos(ang)
        hy = cy + 47.14 / 2 * np.sin(ang)
        draw_hole(ax, hx, hy, 5.5, fs=4)
        holes.append((hx, hy))
    return holes

# ============================================================
# Drawing 1: Wood Base TOP view with drilling positions
# ============================================================
def draw_wood_base_top():
    fig = plt.figure(figsize=(20, 14), dpi=150)
    # Main drawing area + title block on right
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.02)
    ax = fig.add_subplot(gs[0])
    tb = fig.add_subplot(gs[1])

    ax.set_aspect('equal')
    ax.set_xlim(-330, 330)
    ax.set_ylim(-280, 280)
    ax.set_facecolor('white')

    # Grid (very subtle)
    ax.grid(True, which='both', linestyle=':', linewidth=0.3, color='#cccccc', zorder=0)
    ax.set_axisbelow(True)
    ax.set_xticks(np.arange(-300, 301, 50))
    ax.set_yticks(np.arange(-250, 251, 50))

    # Coordinate axes (centerline crosshair)
    ax.axhline(0, color='#999', lw=0.5, linestyle='-.', alpha=0.6)
    ax.axvline(0, color='#999', lw=0.5, linestyle='-.', alpha=0.6)
    ax.text(310, 4, '+X (motor side)', fontsize=8, color='#666', ha='right')
    ax.text(4, 260, '+Y (back)', fontsize=8, color='#666', va='top')

    # Wood base
    ax.add_patch(Rectangle((-WB_W / 2, -WB_D / 2), WB_W, WB_D,
                           facecolor=WOOD_FILL, edgecolor=WOOD_EDGE, lw=2.5, zorder=1))

    # Wood-grain hint
    for gy in np.linspace(-WB_D / 2 + 20, WB_D / 2 - 20, 18):
        ax.plot([-WB_W / 2 + 6, WB_W / 2 - 6], [gy, gy], color='#a8865a', lw=0.3, alpha=0.5, zorder=1.5)

    # Take-down reserved column (transparent pink halo)
    ax.add_patch(Circle((0, 0), HOLE_D / 2 + 8, facecolor=RESERVED_FILL, edgecolor='none', alpha=0.4, zorder=2))
    # Take-down through-hole
    ax.add_patch(Circle((0, 0), HOLE_D / 2, facecolor='white', edgecolor=RESERVED_EDGE,
                        lw=1.8, linestyle='--', zorder=3))
    ax.text(0, 0, 'Ø100\nTAKE-DOWN', fontsize=8, ha='center', va='center', color=RESERVED_EDGE, fontweight='bold')

    # Uprights (4x 2020 posts)
    for sx in UP_X:
        for sy in UP_Y:
            ax.add_patch(Rectangle((sx - UP_W / 2, sy - UP_W / 2), UP_W, UP_W,
                                   facecolor=ALUMINUM, edgecolor='black', lw=1.0, zorder=4))
            ax.plot(sx, sy, 'x', color='black', markersize=8, mew=1.5, zorder=5)
            ax.text(sx + 14, sy + 14, f'({sx:+d}, {sy:+d})', fontsize=6, color='#222')

    # --- Components ---
    psu_holes    = draw_psu(ax, -195, 0)
    tb_holes     = draw_tb6600(ax, +200, -47)
    mega_holes   = draw_mega(ax, +200, +75)
    buck1_holes  = draw_buck(ax, -50, +160, 'LM2596 #1', 'Mega + Servos 5V')
    buck2_holes  = draw_buck(ax, +50, +160, 'LM2596 #2', 'Pi 4 isolated 5V')
    term_holes   = draw_terminal_block(ax, 0, +180)
    motor_holes  = draw_motor(ax, MOTOR_X, MOTOR_Y)

    # --- Overall dimensions (outside the wood) ---
    dim_h(ax, -WB_W / 2, WB_W / 2, -WB_D / 2, '500 mm  (WOOD_BASE_W)', offset_y=30)
    dim_v(ax, -WB_D / 2, WB_D / 2, WB_W / 2, '400 mm  (WOOD_BASE_D)', offset_x=30)
    # Upright spacing
    dim_h(ax, UP_X[1], UP_X[0], -WB_D / 2 + 60, '300 mm (upright pitch X)', offset_y=12)
    dim_v(ax, UP_Y[1], UP_Y[0], -WB_W / 2 + 60, '240 mm (upright pitch Y)', offset_x=10)

    # --- Component position callouts ---
    callout(ax, -195, 0, 'PSU center\n(X = −195, Y = 0)', dx=-110, dy=-150)
    callout(ax, 200, -47, 'TB6600 center\n(X = +200, Y = −47)\nnear motor', dx=70, dy=-80)
    callout(ax, 200, 75, 'Arduino Mega 2560\n(X = +200, Y = +75)\non 10 mm M3 standoffs', dx=80, dy=50)
    callout(ax, -50, 160, 'LM2596 buck #1\n(X = −50, Y = +160)', dx=-120, dy=40)
    callout(ax, 50, 160, 'LM2596 buck #2\n(X = +50, Y = +160)', dx=70, dy=40)
    callout(ax, 0, 180, '24V distribution\nterminal block\n(X = 0, Y = +180)', dx=-150, dy=80)
    callout(ax, MOTOR_X, MOTOR_Y, 'NEMA 23 + HG5\n(X = +85, Y = −47)', dx=-180, dy=-60)

    # --- Front operator panel indicator (along Y = -200 edge) ---
    ax.add_patch(Rectangle((-100, -200 - 3), 200, 6,
                           facecolor='#888', edgecolor='black', lw=1.0, hatch='///'))
    ax.text(0, -218, 'FRONT OPERATOR PANEL  (vertical 200 × 60 × 3 mm — see separate drawing)',
            fontsize=8, ha='center', color='#222', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#fff3b0', ec='#888', lw=0.8))

    ax.set_xlabel('X (mm)  — origin at center of wood base', fontsize=9)
    ax.set_ylabel('Y (mm)  — origin at center', fontsize=9)
    ax.set_title('CSM V3 — WOOD BASE V1.1 — ELECTRICAL DRILLING DRAWING (TOP VIEW)',
                 fontsize=13, fontweight='bold', pad=18)

    # ================ TITLE BLOCK ================
    tb.set_xlim(0, 1); tb.set_ylim(0, 1)
    tb.axis('off')
    # Border
    tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, facecolor='white', edgecolor='black', lw=1.5))

    rows = [
        ('PROJECT',        'CSM V3 — Circular Sock Machine'),
        ('DRAWING',        'Wood Base V1.1 — Electrical Drilling'),
        ('SCALE',          '1 : 5  (full at print)'),
        ('UNITS',          'Millimeters'),
        ('REV',            'V1.0'),
        ('DATE',           '2026-06-04'),
        ('SHEET',          '1 of 3'),
        ('TOLERANCE',      'Hole positions ±1.0 mm'),
        ('MATERIAL',       'Hardwood (walnut), 18 mm'),
    ]
    y = 0.92
    for k, v in rows:
        tb.text(0.06, y, k, fontsize=8, fontweight='bold', color='#444')
        tb.text(0.45, y, v, fontsize=8, color='#111')
        y -= 0.045

    # Legend
    tb.text(0.06, 0.50, 'LEGEND', fontsize=9, fontweight='bold')
    leg_items = [
        ('●', HOLE_COLOR,    'Drill hole (label = thread)'),
        ('▣', ALUMINUM,      '2020 upright location'),
        ('○', RESERVED_EDGE, 'Take-down reserved Ø100'),
        ('▭', PSU_BODY,      'PSU Mean Well S-250-24'),
        ('▭', TB6600_BODY,   'TB6600 stepper driver'),
        ('▭', MEGA_PCB,      'Arduino Mega 2560'),
        ('▭', BUCK_PCB,      'LM2596 buck converter'),
        ('▭', TERMINAL_BLK,  '24V distribution block'),
    ]
    yy = 0.46
    for sym, color, name in leg_items:
        tb.text(0.08, yy, sym, fontsize=12, color=color, ha='center')
        tb.text(0.15, yy, name, fontsize=7.5, color='#222', va='center')
        yy -= 0.034

    # Drill list summary
    tb.text(0.06, 0.18, 'DRILL SUMMARY', fontsize=9, fontweight='bold')
    drill_summary = [
        '4 × Ø4.5 M4   (PSU chassis)',
        '4 × Ø5.5 M5   (Motor flange)',
        '2 × Ø3.5 M3   (TB6600)',
        '4 × Ø3.2 M3   (Mega)',
        '4 × Ø3.2 M3   (Buck × 2)',
        '2 × Ø3.2 M3   (Terminal)',
        '1 × Ø100      (Take-down)',
    ]
    yy = 0.14
    for line in drill_summary:
        tb.text(0.06, yy, line, fontsize=7, family='monospace', color='#222')
        yy -= 0.028

    plt.tight_layout()
    out_png = os.path.join(OUTDIR, 'wood_base_top.png')
    out_pdf = os.path.join(OUTDIR, 'wood_base_top.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

# ============================================================
# Drawing 2: Operator panel front view
# ============================================================
def draw_operator_panel():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    ax.set_aspect('equal')
    ax.set_xlim(-140, 140)
    ax.set_ylim(-30, 110)
    ax.set_facecolor('white')
    ax.grid(True, linestyle=':', linewidth=0.3, color='#cccccc')

    # Panel outline (200 wide x 60 tall, viewed from front)
    PW, PH = 200, 60
    ax.add_patch(Rectangle((-PW / 2, 0), PW, PH, facecolor=PANEL_FILL,
                           edgecolor='black', lw=2.0))
    ax.text(0, PH + 8, 'PANEL: 200 × 60 × 3 mm  (3 mm plywood OR 2 mm aluminum)',
            fontsize=9, ha='center', fontweight='bold', color='#222')

    # IEC C14 inlet (27 × 19 cutout at X=-70, Z=30)
    iec_w, iec_h = 27, 19
    ax.add_patch(Rectangle((-70 - iec_w / 2, 30 - iec_h / 2), iec_w, iec_h,
                           facecolor=IEC_BODY, edgecolor='black', lw=1.0))
    # IEC pin holes
    for px, py in [(-3.5, -4), (3.5, -4), (0, 4)]:
        ax.add_patch(Circle((-70 + px, 30 + py), 1.8, facecolor='#444', edgecolor='black', lw=0.4))
    ax.text(-70, 50, 'IEC C14', fontsize=8, ha='center', color='#222', fontweight='bold')
    ax.text(-70, 46, '27 × 19 cutout', fontsize=6, ha='center', color='#666')
    ax.text(-70, 8, 'AC MAINS IN', fontsize=6, ha='center', color='#222', fontweight='bold')

    # Fuse holder (Ø12 at X=-25, Z=30)
    ax.add_patch(Circle((-25, 30), 6, facecolor=FUSE_BODY, edgecolor='black', lw=1.2))
    ax.add_patch(Circle((-25, 30), 4, facecolor='#888', edgecolor='black', lw=0.5))
    ax.text(-25, 50, 'FUSE 2A T', fontsize=8, ha='center', color='#222', fontweight='bold')
    ax.text(-25, 46, 'Ø12 cutout', fontsize=6, ha='center', color='#666')
    ax.text(-25, 8, 'T2AL250V', fontsize=6, ha='center', color='#666')

    # E-stop (Ø22 at X=+20, Z=30) — big red mushroom front view
    estop_outer = 22
    estop_inner = 18
    ax.add_patch(Circle((20, 30), estop_outer / 2, facecolor=ESTOP_BLACK,
                        edgecolor='black', lw=1.2))
    ax.add_patch(Circle((20, 30), estop_inner / 2 + 6, facecolor=ESTOP_RED,
                        edgecolor='#660000', lw=1.0))
    ax.text(20, 30, 'STOP', fontsize=10, ha='center', va='center', color='white', fontweight='bold')
    ax.text(20, 54, 'EMERGENCY STOP', fontsize=8, ha='center', color=ESTOP_RED, fontweight='bold')
    ax.text(20, 50, '22mm mushroom', fontsize=6, ha='center', color='#666')
    ax.text(20, 46, 'NC+NC latching, 10A 250V', fontsize=6, ha='center', color='#666')
    ax.text(20, 6, 'Push to stop / twist to release', fontsize=6, ha='center', color='#888', style='italic')

    # Status LEDs (Ø5 at X=+75, Z=25 and 35)
    ax.add_patch(Circle((75, 35), 2.5, facecolor='#0c0', edgecolor='black', lw=0.6))
    ax.add_patch(Circle((75, 25), 2.5, facecolor='#f80', edgecolor='black', lw=0.6))
    ax.text(82, 35, 'POWER (green)', fontsize=7, va='center', color='#222')
    ax.text(82, 25, 'FAULT (amber)', fontsize=7, va='center', color='#222')
    ax.text(75, 50, 'STATUS', fontsize=8, ha='center', color='#222', fontweight='bold')
    ax.text(75, 46, '2 × Ø5 cutouts', fontsize=6, ha='center', color='#666')

    # Dimensions
    dim_h(ax, -PW / 2, PW / 2, 0, '200 mm', offset_y=14)
    dim_v(ax, 0, PH, PW / 2, '60 mm', offset_x=14)
    dim_h(ax, -PW / 2, -70, 0, '30 mm (to IEC ctr)', offset_y=28)
    dim_h(ax, -70, -25, 0, '45 mm', offset_y=42)
    dim_h(ax, -25, 20, 0, '45 mm', offset_y=42)
    dim_h(ax, 20, 75, 0, '55 mm', offset_y=42)

    # L-bracket mount points
    for bx in [-90, +90]:
        ax.add_patch(Rectangle((bx - 4, 4), 8, 8, facecolor='none', edgecolor=HOLE_COLOR, lw=1.2, linestyle='--'))
        ax.text(bx, 0, f'L-bkt M4\nto wood base', fontsize=6, ha='center', color=HOLE_COLOR)

    ax.set_xlabel('X (mm) — operator-facing', fontsize=9)
    ax.set_ylabel('Z (mm) — height above panel bottom', fontsize=9)
    ax.set_title('CSM V3 — FRONT OPERATOR PANEL — V1.0  (Sheet 2 of 3)', fontsize=12, fontweight='bold', pad=14)

    plt.tight_layout()
    out_png = os.path.join(OUTDIR, 'operator_panel.png')
    out_pdf = os.path.join(OUTDIR, 'operator_panel.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

# ============================================================
# Drawing 3: Components reference card with BOM links
# ============================================================
def draw_components_card():
    fig, ax = plt.subplots(figsize=(14, 18), dpi=150)
    ax.set_xlim(0, 100); ax.set_ylim(0, 140)
    ax.axis('off')
    ax.set_title('CSM V3 — ELECTRICAL COMPONENTS REFERENCE CARD  (Sheet 3 of 3)',
                 fontsize=14, fontweight='bold', pad=14)

    # Each card: title, sketch, dims, ASIN, BOM line
    cards = [
        ('Mean Well S-250-24 PSU',  'B07Y7L664K',
         '24V DC, 10A (240W), AC input switchable 115/230V',
         '199 × 110 × 50 mm | mass ~960 g | 4× M4 chassis',
         '#9aa1a8', 'https://www.amazon.com/dp/B07Y7L664K'),
        ('Arduino Mega 2560 REV3',  'B0046AMGW0',
         'Real-time controller. Mega <-> Pi via UART/USB 115200 baud.',
         '102 × 54 mm | 4× M3 mounting | USB-B port',
         '#1f4ea8', 'https://www.amazon.com/dp/B0046AMGW0'),
        ('Raspberry Pi 4 4GB Starter', 'B07V5JTMV9',
         'Touchscreen UI + pattern logic. Higher CPU layer. Lives on touchscreen mast, NOT wood base.',
         '85 × 56 mm | 4× M2.5 mounting | HDMI + USB-C',
         '#0c6e3a', 'https://www.amazon.com/dp/B07V5JTMV9'),
        ('TB6600 Stepper Driver 4A', 'B08SG7L54W',
         'Drives NEMA 23 (2.8A < 4A rating). Microstep + current via DIP.',
         '96 × 56 × 37 mm | 2× M3 flange | screw terminals',
         '#c43838', 'https://www.amazon.com/dp/B08SG7L54W'),
        ('RioRand LM2596 DC-DC Buck', 'B008BHB4L8',
         'Adjustable 24V -> 5V. TWO units required: #1 for Mega+servos, #2 for Pi (isolated rail).',
         '43 × 21 mm | 2× M3 corner holes | adj trimpot',
         '#0f6b34', 'https://www.amazon.com/dp/B008BHB4L8'),
        ('NEMA 23 + 5:1 HG5 Gearbox', '(StepperOnline)',
         'Drive motor. Body 57×57×56 + 50 mm gearbox = 106 mm tower.',
         '57 × 57 footprint | M5 PCD 47.14 flange holes | shaft 14 mm',
         '#7a7e85', '(supplier StepperOnline 23HS22-2804S-HG5)'),
    ]

    y = 130
    for title, asin, desc, spec, color, link in cards:
        # Sketch box
        ax.add_patch(Rectangle((4, y - 16), 18, 14, facecolor=color, edgecolor='black', lw=1.0))
        ax.text(13, y - 9, asin if asin.startswith('B') else 'STEP',
                fontsize=7, ha='center', va='center', color='white', fontweight='bold')
        # Title
        ax.text(26, y - 2, title, fontsize=12, fontweight='bold', color='#111')
        # ASIN line
        ax.text(26, y - 6, f'ASIN: {asin}', fontsize=8.5, color='#666', family='monospace')
        # Description
        ax.text(26, y - 10, desc, fontsize=8.5, color='#222', wrap=True)
        # Spec
        ax.text(26, y - 14, spec, fontsize=8, color='#444', family='monospace')
        # Link
        ax.text(26, y - 17.5, link, fontsize=7, color='#0050a0', style='italic')
        # Separator
        ax.plot([4, 96], [y - 20, y - 20], color='#ccc', lw=0.5)
        y -= 22

    plt.tight_layout()
    out_png = os.path.join(OUTDIR, 'components_card.png')
    out_pdf = os.path.join(OUTDIR, 'components_card.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("=" * 70)
    print("CSM V3 -- Generating electrical mounting drawings")
    print("=" * 70)
    print()
    print("Sheet 1: Wood Base Top View")
    draw_wood_base_top()
    print()
    print("Sheet 2: Front Operator Panel")
    draw_operator_panel()
    print()
    print("Sheet 3: Components Reference Card")
    draw_components_card()
    print()
    print("=" * 70)
    print("Done. PDFs are vector (print to A3 or larger for accurate scale).")
    print("PNGs are 200 DPI raster (use for screen viewing).")
    print("=" * 70)
