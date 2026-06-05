# -*- coding: utf-8 -*-
"""
CSM V3 -- Wood Base Electrical Mounting Drawings Generator
============================================================
Produces engineering drawings for drilling the wood base electrical
mounts. Every dimension a machinist needs to drill the holes is shown.

Outputs:
  wood_base_top.png/.pdf       -- top view with full dimensioning
  drilling_guide.png/.pdf      -- pure drilling template with numbered
                                   holes and coordinate table
  operator_panel.png/.pdf      -- front operator panel detail
  components_card.png/.pdf     -- product reference card with ASINs

Run:
  "C:/Program Files/FreeCAD 1.1/bin/python.exe" generate_drawings.py
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np

# ============================================================
# WOOD BASE + INFRASTRUCTURE (from machine_datums.py)
# ============================================================
WB_W, WB_D, WB_T = 500, 400, 18
HOLE_D = 100
UP_X = [+150, -150]
UP_Y = [+120, -120]
UP_W = 20
MOTOR_X, MOTOR_Y = 85, -47

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# HARDWARE SPECS PER COMPONENT
# 'bolt': thread, length (mm), head, washer, nut, hardware notes
# All bolts go THROUGH the 18 mm wood base with washer + nut underneath.
# Drill diameter = clearance for the bolt thread.
# ============================================================
HW_PSU      = dict(bolt='M4 × 30', drill='Ø4.5',
                   hardware='M4 bolt 30 mm + washer top + M4 washer bottom + M4 nut',
                   notes='Pan-head bolt; rubber washer optional under head')
HW_MOTOR    = dict(bolt='M5 × 35', drill='Ø5.5',
                   hardware='M5 bolt 35 mm + washer top + M5 lock washer + M5 nut',
                   notes='Lock washer required — motor vibrates')
HW_TB6600   = dict(bolt='M3 × 25', drill='Ø3.5',
                   hardware='M3 bolt 25 mm + washer top + M3 washer bottom + M3 nut',
                   notes='Through TB6600 flange tabs (4 mm thick)')
HW_MEGA     = dict(bolt='M3 × 30', drill='Ø3.2',
                   hardware='M3 bolt 30 mm + nylon standoff 10 mm + M3 washer + M3 nut',
                   notes='Standoff between Mega PCB and wood for airflow')
HW_BUCK     = dict(bolt='M3 × 22', drill='Ø3.2',
                   hardware='M3 bolt 22 mm + nylon standoff 5 mm + M3 washer + M3 nut',
                   notes='OR substitute 3M VHB pad — no holes needed')
HW_TERMINAL = dict(bolt='M3 × 22', drill='Ø3.2',
                   hardware='M3 bolt 22 mm + washer top + M3 washer bottom + M3 nut',
                   notes='OR DIN-rail clip to wood base')
HW_TAKEDOWN = dict(bolt='—', drill='Ø100',
                   hardware='Through-hole only (hole saw or jigsaw)',
                   notes='Sock fabric tube descends through this')

# ============================================================
# ALL COMPONENT POSITIONS + MOUNTING HOLES (single source of truth)
# ============================================================
COMPONENTS = {
    'PSU': dict(
        label='PSU Mean Well S-250-24',
        cx=-195, cy=0, w=110, d=199,
        color='#9aa1a8',
        hw=HW_PSU,
        holes=[(-47, -90, 4.5, 'M4'), (+47, -90, 4.5, 'M4'),
               (-47, +90, 4.5, 'M4'), (+47, +90, 4.5, 'M4')],
    ),
    'MOTOR': dict(
        label='NEMA 23 + HG5 gearbox',
        cx=85, cy=-47, w=57, d=57,
        color='#7a7e85',
        hw=HW_MOTOR,
        holes=[(round(47.14/2*np.cos(np.radians(a)), 2),
                round(47.14/2*np.sin(np.radians(a)), 2), 5.5, 'M5')
               for a in (45, 135, 225, 315)],
    ),
    'TB6600': dict(
        label='TB6600 stepper driver',
        cx=200, cy=-47, w=96, d=56,
        color='#c43838',
        hw=HW_TB6600,
        holes=[(-42, 0, 3.5, 'M3'), (+42, 0, 3.5, 'M3')],
    ),
    'MEGA': dict(
        label='Arduino Mega 2560',
        cx=200, cy=75, w=102, d=54,
        color='#1f4ea8',
        hw=HW_MEGA,
        holes=[(-47, -23, 3.2, 'M3'), (+47, -23, 3.2, 'M3'),
               (-47, +23, 3.2, 'M3'), (+47, +23, 3.2, 'M3')],
    ),
    'BUCK1': dict(
        label='LM2596 buck #1 (Mega+servo)',
        cx=-50, cy=160, w=43, d=21,
        color='#0f6b34',
        hw=HW_BUCK,
        holes=[(-18, -7, 3.2, 'M3'), (+18, +7, 3.2, 'M3')],
    ),
    'BUCK2': dict(
        label='LM2596 buck #2 (Pi)',
        cx=+50, cy=160, w=43, d=21,
        color='#0f6b34',
        hw=HW_BUCK,
        holes=[(-18, -7, 3.2, 'M3'), (+18, +7, 3.2, 'M3')],
    ),
    'TERMINAL': dict(
        label='24V distribution block',
        cx=0, cy=180, w=50, d=20,
        color='#e6dc4a',
        hw=HW_TERMINAL,
        holes=[(-22, 0, 3.2, 'M3'), (+22, 0, 3.2, 'M3')],
    ),
}

# Build flat numbered list of every drill hole on the wood base
# (uprights are 2020 extrusion, not drilled into base here)
def build_drill_list():
    holes = []
    n = 1
    # Take-down hole
    holes.append(dict(n=0, x=0, y=0, d=HOLE_D, m='Ø100',
                      bolt='—', component='TAKE-DOWN',
                      note='Sock fabric column'))
    for comp_id, comp in COMPONENTS.items():
        for (dx, dy, hd, ml) in comp['holes']:
            holes.append(dict(
                n=n,
                x=round(comp['cx'] + dx, 1),
                y=round(comp['cy'] + dy, 1),
                d=hd, m=ml,
                bolt=comp['hw']['bolt'],
                component=comp_id,
                note=comp['label'],
            ))
            n += 1
    return holes

DRILL_LIST = build_drill_list()

# ============================================================
# Style
# ============================================================
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 9,
    'axes.linewidth': 1.0,
    'lines.linewidth': 0.9,
})

WOOD_FILL    = '#D2B48C'
WOOD_EDGE    = '#5a4020'
DIM_COLOR    = '#222'
DIM_FAINT    = '#777'
HOLE_COLOR   = '#d40000'
RESERVED_FILL = '#ffd6d6'
RESERVED_EDGE = '#c00000'
ALUMINUM     = '#B8BCC4'

# ============================================================
# Dimension helpers
# ============================================================
def dim_h(ax, x1, x2, y, label, offset_y=18, color=DIM_COLOR, fontsize=8,
          ext_line=True):
    """Horizontal dimension below position y."""
    yo = y - offset_y
    ax.annotate('', xy=(x2, yo), xytext=(x1, yo),
                arrowprops=dict(arrowstyle='<|-|>', color=color, lw=0.9,
                                shrinkA=0, shrinkB=0, mutation_scale=8))
    if ext_line:
        ax.plot([x1, x1], [y - 2, yo - 4], color=color, lw=0.5)
        ax.plot([x2, x2], [y - 2, yo - 4], color=color, lw=0.5)
    ax.text((x1 + x2) / 2, yo + 2, label, ha='center', va='bottom',
            fontsize=fontsize, color=color,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none'))

def dim_v(ax, y1, y2, x, label, offset_x=18, color=DIM_COLOR, fontsize=8,
          ext_line=True):
    """Vertical dimension right of position x."""
    xo = x + offset_x
    ax.annotate('', xy=(xo, y2), xytext=(xo, y1),
                arrowprops=dict(arrowstyle='<|-|>', color=color, lw=0.9,
                                shrinkA=0, shrinkB=0, mutation_scale=8))
    if ext_line:
        ax.plot([x + 2, xo + 4], [y1, y1], color=color, lw=0.5)
        ax.plot([x + 2, xo + 4], [y2, y2], color=color, lw=0.5)
    ax.text(xo + 2, (y1 + y2) / 2, label, ha='left', va='center',
            fontsize=fontsize, color=color, rotation=90,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none'))

def draw_hole(ax, x, y, dia, n=None, label=None, fs=6, with_crosshair=True):
    r = dia / 2
    ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor=HOLE_COLOR, lw=1.2,
                        zorder=10))
    if with_crosshair:
        ax.plot([x - r * 1.8, x + r * 1.8], [y, y], color=HOLE_COLOR, lw=0.5, zorder=10)
        ax.plot([x, x], [y - r * 1.8, y + r * 1.8], color=HOLE_COLOR, lw=0.5, zorder=10)
    if n is not None:
        ax.text(x, y, str(n), fontsize=fs, ha='center', va='center',
                color=HOLE_COLOR, fontweight='bold', zorder=11)
    if label:
        ax.text(x + r + 1.5, y + r + 1.5, label, fontsize=fs, color=HOLE_COLOR)

# ============================================================
# Drawing 1: WOOD BASE TOP VIEW with full dimensioning
# ============================================================
def draw_wood_base_top():
    fig = plt.figure(figsize=(22, 16), dpi=150)
    gs = fig.add_gridspec(1, 2, width_ratios=[3.5, 1], wspace=0.02)
    ax = fig.add_subplot(gs[0])
    tb = fig.add_subplot(gs[1])

    ax.set_aspect('equal')
    ax.set_xlim(-340, 340)
    ax.set_ylim(-310, 280)
    ax.set_facecolor('white')
    ax.grid(True, linestyle=':', linewidth=0.3, color='#cccccc', zorder=0)
    ax.set_axisbelow(True)
    ax.set_xticks(np.arange(-300, 301, 50))
    ax.set_yticks(np.arange(-250, 251, 50))

    # Center crosshair (datum)
    ax.axhline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.6, zorder=1)
    ax.axvline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.6, zorder=1)
    ax.plot(0, 0, marker='+', color='#000', markersize=18, mew=1.5, zorder=3)
    ax.text(8, -10, 'DATUM (0, 0)', fontsize=7, color='#444')
    ax.text(310, 4, '+X →', fontsize=9, color='#444', ha='right')
    ax.text(4, 270, '+Y ↑', fontsize=9, color='#444', va='top')

    # Wood base
    ax.add_patch(Rectangle((-WB_W / 2, -WB_D / 2), WB_W, WB_D,
                           facecolor=WOOD_FILL, edgecolor=WOOD_EDGE, lw=2.5, zorder=1))
    for gy in np.linspace(-WB_D / 2 + 20, WB_D / 2 - 20, 14):
        ax.plot([-WB_W / 2 + 6, WB_W / 2 - 6], [gy, gy], color='#a8865a',
                lw=0.3, alpha=0.4, zorder=1.5)

    # Take-down reserved column
    ax.add_patch(Circle((0, 0), HOLE_D / 2 + 8, facecolor=RESERVED_FILL,
                        edgecolor='none', alpha=0.4, zorder=2))
    ax.add_patch(Circle((0, 0), HOLE_D / 2, facecolor='white', edgecolor=RESERVED_EDGE,
                        lw=1.8, linestyle='--', zorder=3))
    ax.text(0, 0, 'Ø100', fontsize=10, ha='center', va='center',
            color=RESERVED_EDGE, fontweight='bold')
    ax.text(0, -10, 'TAKE-DOWN', fontsize=7, ha='center',
            color=RESERVED_EDGE)

    # Uprights (visual only — NOT drilled into base here)
    for sx in UP_X:
        for sy in UP_Y:
            ax.add_patch(Rectangle((sx - UP_W / 2, sy - UP_W / 2), UP_W, UP_W,
                                   facecolor=ALUMINUM, edgecolor='black',
                                   lw=1.0, zorder=4))
            ax.plot(sx, sy, '+', color='black', markersize=10, mew=1.2, zorder=5)
            ax.text(sx + 13, sy + 13, f'({sx:+d}, {sy:+d})', fontsize=6, color='#222')

    # Components as simple labeled rectangles (no fake-PCB clutter — drilling focus)
    n_counter = 1
    hole_label_positions = {}  # for callouts
    for cid, c in COMPONENTS.items():
        x0 = c['cx'] - c['w'] / 2
        y0 = c['cy'] - c['d'] / 2
        ax.add_patch(Rectangle((x0, y0), c['w'], c['d'],
                               facecolor=c['color'], edgecolor='black',
                               lw=1.0, alpha=0.55, zorder=5))
        # Center crosshair on component
        ax.plot(c['cx'], c['cy'], '+', color='black', markersize=10, mew=1.0, zorder=6)
        # Component label
        ax.text(c['cx'], c['cy'] + 8, cid, fontsize=10, ha='center',
                fontweight='bold', color='#111', zorder=7)
        ax.text(c['cx'], c['cy'] - 4, f'({c["cx"]:+d}, {c["cy"]:+d})',
                fontsize=7, ha='center', color='#333', zorder=7)
        ax.text(c['cx'], c['cy'] - 12, f'{c["w"]:.0f}×{c["d"]:.0f}',
                fontsize=7, ha='center', color='#555', zorder=7)
        # Mounting holes
        for (dx, dy, hd, ml) in c['holes']:
            hx, hy = c['cx'] + dx, c['cy'] + dy
            draw_hole(ax, hx, hy, hd, n=n_counter, fs=6)
            hole_label_positions[n_counter] = (hx, hy, hd, ml)
            n_counter += 1

    # ===== OVERALL WOOD BASE DIMENSIONS =====
    dim_h(ax, -WB_W / 2, WB_W / 2, -WB_D / 2, '500 mm  (overall width)', offset_y=24)
    dim_v(ax, -WB_D / 2, WB_D / 2, WB_W / 2, '400 mm  (overall depth)', offset_x=24)
    # Half widths to show centering
    dim_h(ax, -WB_W / 2, 0, WB_D / 2 + 8, '250', offset_y=-10, color=DIM_FAINT, fontsize=7)
    dim_h(ax, 0, WB_W / 2, WB_D / 2 + 8, '250', offset_y=-10, color=DIM_FAINT, fontsize=7)
    dim_v(ax, -WB_D / 2, 0, -WB_W / 2 - 8, '200', offset_x=-26, color=DIM_FAINT, fontsize=7)
    dim_v(ax, 0, WB_D / 2, -WB_W / 2 - 8, '200', offset_x=-26, color=DIM_FAINT, fontsize=7)

    # ===== UPRIGHT POSITIONS =====
    dim_h(ax, UP_X[1], UP_X[0], UP_Y[1] - 8, '300 (upright pitch)', offset_y=12,
          color='#0050a0', fontsize=8)
    dim_v(ax, UP_Y[1], UP_Y[0], UP_X[0] + 8, '240 (upright pitch)', offset_x=10,
          color='#0050a0', fontsize=8)

    # ===== COMPONENT CENTER X positions from datum =====
    # PSU
    dim_h(ax, -195, 0, COMPONENTS['PSU']['cy'] - COMPONENTS['PSU']['d']/2 - 6,
          '195  (PSU ctr X)', offset_y=8, color='#0050a0', fontsize=7)
    # TB6600 + Mega + Pi all at +200
    dim_h(ax, 0, 200, -150, '200  (Right components X)', offset_y=8,
          color='#0050a0', fontsize=7)
    # Bucks at ±50
    dim_h(ax, -50, 0, 160 + COMPONENTS['BUCK1']['d']/2 + 8,
          '50', offset_y=-3, color='#0050a0', fontsize=7)
    dim_h(ax, 0, 50, 160 + COMPONENTS['BUCK2']['d']/2 + 8,
          '50', offset_y=-3, color='#0050a0', fontsize=7)
    # Terminal block at X=0 - no dim needed (on Y axis)
    # Motor at X=85
    dim_h(ax, 0, 85, MOTOR_Y - 35, '85  (motor X)', offset_y=8,
          color='#0050a0', fontsize=7)

    # ===== COMPONENT CENTER Y positions from datum =====
    dim_v(ax, 0, 75, COMPONENTS['MEGA']['cx'] + COMPONENTS['MEGA']['w']/2 + 6,
          '75 (Mega Y)', offset_x=8, color='#0050a0', fontsize=7)
    dim_v(ax, -47, 0, COMPONENTS['TB6600']['cx'] + COMPONENTS['TB6600']['w']/2 + 6,
          '-47 (TB6600 Y)', offset_x=8, color='#0050a0', fontsize=7)
    dim_v(ax, 0, 160, -150, '160 (Bucks Y)', offset_x=-20,
          color='#0050a0', fontsize=7)
    dim_v(ax, 0, 180, -180, '180 (Term Y)', offset_x=-26,
          color='#0050a0', fontsize=7)
    dim_v(ax, -47, 0, MOTOR_X + 30, '47 (motor Y)', offset_x=8,
          color='#0050a0', fontsize=7)

    # ===== EDGE-TO-COMPONENT distances =====
    # Distance from -X wood edge to PSU left edge
    psu_x_left = -195 - 110/2  # = -250
    dim_h(ax, -WB_W/2, psu_x_left + 110, -WB_D/2 + 30,
          '0 mm (PSU flush)', offset_y=8, color='#666', fontsize=6)

    # ===== PSU mounting hole pattern detail =====
    # Hole-to-hole spacings on PSU
    psu = COMPONENTS['PSU']
    h1 = (psu['cx'] - 47, psu['cy'] - 90)
    h2 = (psu['cx'] + 47, psu['cy'] - 90)
    h3 = (psu['cx'] - 47, psu['cy'] + 90)
    h4 = (psu['cx'] + 47, psu['cy'] + 90)
    dim_h(ax, h1[0], h2[0], h1[1] - 4, '94', offset_y=12, color='#888', fontsize=6)
    dim_v(ax, h1[1], h3[1], h1[0] - 4, '180', offset_x=-22, color='#888', fontsize=6)

    # ===== MEGA mounting hole pattern detail =====
    mega = COMPONENTS['MEGA']
    mh1 = (mega['cx'] - 47, mega['cy'] - 23)
    mh2 = (mega['cx'] + 47, mega['cy'] - 23)
    mh3 = (mega['cx'] - 47, mega['cy'] + 23)
    dim_h(ax, mh1[0], mh2[0], mh1[1] - 6, '94', offset_y=10, color='#888', fontsize=6)
    dim_v(ax, mh1[1], mh3[1], mh1[0] - 6, '46', offset_x=-22, color='#888', fontsize=6)

    # ===== TB6600 mounting holes detail =====
    tb_ = COMPONENTS['TB6600']
    dim_h(ax, tb_['cx'] - 42, tb_['cx'] + 42, tb_['cy'] - tb_['d']/2 - 6,
          '84 (TB6600 flange pitch)', offset_y=8, color='#888', fontsize=6)

    # Motor PCD callout
    ax.add_patch(Circle((MOTOR_X, MOTOR_Y), 47.14/2, facecolor='none',
                        edgecolor='#888', lw=0.6, linestyle=':', zorder=8))
    ax.text(MOTOR_X + 30, MOTOR_Y + 25, 'PCD\nØ47.14', fontsize=6, color='#444',
            ha='left', va='center')

    # ===== Front operator panel marker =====
    ax.add_patch(Rectangle((-100, -200 - 3), 200, 6,
                           facecolor='#888', edgecolor='black', lw=1.0,
                           hatch='///', zorder=6))
    ax.text(0, -218, 'FRONT OPERATOR PANEL → see Sheet 3',
            fontsize=8, ha='center', color='#222', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc='#fff3b0', ec='#888', lw=0.8))

    ax.set_xlabel('X (mm) — origin at center of wood base', fontsize=9)
    ax.set_ylabel('Y (mm) — origin at center', fontsize=9)
    ax.set_title('CSM V3  —  WOOD BASE V1.1  —  DRILLING LAYOUT (TOP VIEW)\n'
                 'Sheet 1 of 4   |   Holes numbered — see Sheet 2 for coordinate table',
                 fontsize=12, fontweight='bold', pad=14)

    # ============== TITLE BLOCK ==============
    tb.set_xlim(0, 1); tb.set_ylim(0, 1); tb.axis('off')
    tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                           facecolor='white', edgecolor='black', lw=1.5))

    rows = [
        ('PROJECT',    'CSM V3 — Circular Sock Machine'),
        ('DRAWING',    'Wood Base V1.1 — Drilling'),
        ('SCALE',      '1 : 5  (full at A3 print)'),
        ('UNITS',      'Millimeters'),
        ('REV',        'V1.1'),
        ('DATE',       '2026-06-04'),
        ('SHEET',      '1 of 4'),
        ('TOLERANCE',  '±1.0 mm  (hole positions)'),
        ('MATERIAL',   'Hardwood walnut, 18 mm'),
        ('DATUM',      'X = 0, Y = 0  at wood center'),
    ]
    y = 0.965
    for k, v in rows:
        tb.text(0.06, y, k, fontsize=8, fontweight='bold', color='#444')
        tb.text(0.42, y, v, fontsize=8, color='#111')
        y -= 0.038

    tb.text(0.06, 0.55, 'DIMENSIONS', fontsize=9, fontweight='bold')
    tb.text(0.06, 0.52, 'Black: from wood edges', fontsize=7, color='#222')
    tb.text(0.06, 0.49, 'Blue:  component centers from datum', fontsize=7, color='#0050a0')
    tb.text(0.06, 0.46, 'Gray:  hole-to-hole pitches', fontsize=7, color='#777')
    tb.text(0.06, 0.43, 'Red:   drill hole + number', fontsize=7, color=HOLE_COLOR)

    tb.text(0.06, 0.38, 'HOLES & BOLTS', fontsize=9, fontweight='bold')
    n_total = sum(len(c['holes']) for c in COMPONENTS.values()) + 1
    tb.text(0.06, 0.355, 'Component   #  Drill  Bolt', fontsize=6.5,
            family='monospace', color='#444', fontweight='bold')
    rows_drill = [
        ('Take-down', '1', 'Ø100', '—'),
        ('PSU',       '4', 'Ø4.5', 'M4×30'),
        ('Motor',     '4', 'Ø5.5', 'M5×35'),
        ('TB6600',    '2', 'Ø3.5', 'M3×25'),
        ('Mega',      '4', 'Ø3.2', 'M3×30'),
        ('Bucks×2',   '4', 'Ø3.2', 'M3×22'),
        ('Terminal',  '2', 'Ø3.2', 'M3×22'),
    ]
    yy = 0.335
    for comp, n, drill, bolt in rows_drill:
        tb.text(0.06, yy, f'{comp:<10s} {n:>2s}  {drill:>5s}  {bolt:>5s}',
                fontsize=6.5, family='monospace')
        yy -= 0.018
    tb.text(0.06, yy, '─────────────────────────', fontsize=6.5, family='monospace')
    yy -= 0.018
    tb.text(0.06, yy, f'TOTAL: {n_total} holes',
            fontsize=7, family='monospace', fontweight='bold')

    # Bolt total summary
    yy -= 0.025
    tb.text(0.06, yy, 'BOLT TOTALS', fontsize=8, fontweight='bold')
    yy -= 0.018
    tb.text(0.06, yy, '4× M5 × 35     (motor)', fontsize=6.5, family='monospace')
    yy -= 0.016
    tb.text(0.06, yy, '4× M4 × 30     (PSU)', fontsize=6.5, family='monospace')
    yy -= 0.016
    tb.text(0.06, yy, '4× M3 × 30     (Mega)', fontsize=6.5, family='monospace')
    yy -= 0.016
    tb.text(0.06, yy, '2× M3 × 25     (TB6600)', fontsize=6.5, family='monospace')
    yy -= 0.016
    tb.text(0.06, yy, '6× M3 × 22     (Buck+Term)', fontsize=6.5, family='monospace')
    yy -= 0.020
    tb.text(0.06, yy, '+ washers + nuts + standoffs', fontsize=6, color='#666', style='italic')
    yy -= 0.014
    tb.text(0.06, yy, '   See Sheet 2 hardware list', fontsize=6, color='#666', style='italic')

    plt.tight_layout()
    out_png = os.path.join(OUTDIR, 'wood_base_top.png')
    out_pdf = os.path.join(OUTDIR, 'wood_base_top.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

# ============================================================
# Drawing 2: DRILLING GUIDE — numbered holes + coordinate table
# ============================================================
def draw_drilling_guide():
    fig = plt.figure(figsize=(22, 16), dpi=150)
    gs = fig.add_gridspec(1, 2, width_ratios=[2.4, 1.2], wspace=0.04)
    ax = fig.add_subplot(gs[0])
    tab_ax = fig.add_subplot(gs[1])

    ax.set_aspect('equal')
    ax.set_xlim(-310, 310)
    ax.set_ylim(-260, 260)
    ax.set_facecolor('white')
    ax.grid(True, linestyle=':', linewidth=0.3, color='#bbbbbb', zorder=0)
    ax.set_xticks(np.arange(-300, 301, 25))
    ax.set_yticks(np.arange(-250, 251, 25))
    ax.tick_params(labelsize=7)

    # Datum crosshair
    ax.axhline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.7, zorder=1)
    ax.axvline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.7, zorder=1)
    ax.plot(0, 0, '+', color='#000', markersize=18, mew=1.5, zorder=3)

    # Wood base outline (no fill, drilling-template style)
    ax.add_patch(Rectangle((-WB_W / 2, -WB_D / 2), WB_W, WB_D,
                           facecolor='none', edgecolor='black', lw=2.0))

    # Take-down hole
    ax.add_patch(Circle((0, 0), HOLE_D / 2, facecolor='none',
                        edgecolor=RESERVED_EDGE, lw=1.8, linestyle='--'))
    ax.text(0, -5, 'Ø100', fontsize=8, ha='center', va='center',
            color=RESERVED_EDGE, fontweight='bold')

    # Upright positions (light reference)
    for sx in UP_X:
        for sy in UP_Y:
            ax.add_patch(Rectangle((sx - UP_W / 2, sy - UP_W / 2), UP_W, UP_W,
                                   facecolor='none', edgecolor=ALUMINUM,
                                   lw=0.6, linestyle=':'))

    # Component bounding boxes (thin outlines only — drilling template)
    for cid, c in COMPONENTS.items():
        x0 = c['cx'] - c['w'] / 2
        y0 = c['cy'] - c['d'] / 2
        ax.add_patch(Rectangle((x0, y0), c['w'], c['d'],
                               facecolor='none', edgecolor=c['color'],
                               lw=0.8, linestyle='--', alpha=0.6))
        ax.text(c['cx'], c['cy'] + c['d']/2 + 4, cid, fontsize=7,
                ha='center', color=c['color'], fontweight='bold')

    # All drill holes with numbers
    for h in DRILL_LIST:
        if h['n'] == 0:  # take-down already drawn
            continue
        draw_hole(ax, h['x'], h['y'], h['d'], n=h['n'], fs=7)

    # Edge ruler — overall dimensions
    dim_h(ax, -WB_W/2, WB_W/2, -WB_D/2, '500.0', offset_y=20, fontsize=9)
    dim_v(ax, -WB_D/2, WB_D/2, WB_W/2, '400.0', offset_x=20, fontsize=9)

    ax.set_xlabel('X (mm) — origin at center', fontsize=8)
    ax.set_ylabel('Y (mm) — origin at center', fontsize=8)
    ax.set_title('CSM V3  —  WOOD BASE V1.1  —  DRILLING TEMPLATE\n'
                 'Sheet 2 of 4   |   Hole coordinates in adjacent table',
                 fontsize=12, fontweight='bold', pad=14)

    # =========== COORDINATE TABLE ===========
    tab_ax.axis('off')
    tab_ax.set_xlim(0, 1); tab_ax.set_ylim(0, 1)

    headers = ['#', 'X', 'Y', 'Drill', 'Thread', 'Bolt', 'Component']
    col_x = [0.04, 0.10, 0.18, 0.27, 0.36, 0.45, 0.61]

    # Title
    tab_ax.text(0.5, 0.985, 'DRILL HOLE & HARDWARE TABLE',
                fontsize=11, ha='center', fontweight='bold')
    tab_ax.text(0.5, 0.965, 'Origin at wood base center  •  +X right, +Y back',
                fontsize=7, ha='center', color='#666', style='italic')

    # Header row
    y = 0.94
    tab_ax.add_patch(Rectangle((0.02, y - 0.012), 0.96, 0.024,
                               facecolor='#333', edgecolor='none'))
    for h_text, xc in zip(headers, col_x):
        tab_ax.text(xc, y, h_text, fontsize=8, color='white', fontweight='bold')

    # Data rows
    y -= 0.024
    for i, h in enumerate(DRILL_LIST):
        if i % 2 == 0:
            tab_ax.add_patch(Rectangle((0.02, y - 0.010), 0.96, 0.021,
                                       facecolor='#f4f4f4', edgecolor='none'))
        n_txt = '—' if h['n'] == 0 else str(h['n'])
        row_vals = [n_txt, f"{h['x']:+.1f}", f"{h['y']:+.1f}",
                    f"Ø{h['d']:.1f}", h['m'], h.get('bolt', '—'), h['component']]
        for v, xc in zip(row_vals, col_x):
            tab_ax.text(xc, y, v, fontsize=7, family='monospace', color='#111')
        y -= 0.022

    # Drill bit summary
    y -= 0.008
    tab_ax.plot([0.04, 0.96], [y, y], color='black', lw=0.8)
    y -= 0.020
    tab_ax.text(0.04, y, 'DRILL BIT SUMMARY (count × diameter)',
                fontsize=9, fontweight='bold')
    y -= 0.020
    counts = {}
    for h in DRILL_LIST:
        counts[h['d']] = counts.get(h['d'], 0) + 1
    bit_lines = [
        ('1 × Ø100 mm',       'Hole saw or jigsaw (take-down)'),
        (f"{counts.get(5.5, 0)} × Ø5.5 mm",  'Standard HSS bit (M5 clearance)'),
        (f"{counts.get(4.5, 0)} × Ø4.5 mm",  'Standard HSS bit (M4 clearance)'),
        (f"{counts.get(3.5, 0)} × Ø3.5 mm",  'Standard HSS bit (M3 for thicker flange)'),
        (f"{counts.get(3.2, 0)} × Ø3.2 mm",  'Standard HSS bit (M3 clearance, PCB-style)'),
    ]
    for cnt, note in bit_lines:
        tab_ax.text(0.04, y, cnt, fontsize=7.5, family='monospace', fontweight='bold')
        tab_ax.text(0.22, y, note, fontsize=7, color='#444')
        y -= 0.017

    # HARDWARE SHOPPING LIST
    y -= 0.015
    tab_ax.text(0.04, y, 'HARDWARE SHOPPING LIST', fontsize=9, fontweight='bold')
    y -= 0.020
    hw_list = [
        ('M5 × 35 mm bolt',   4, 'NEMA 23 motor flange (lock washer required)'),
        ('M4 × 30 mm bolt',   4, 'PSU chassis'),
        ('M3 × 30 mm bolt',   4, 'Mega 2560 (with 10 mm standoffs)'),
        ('M3 × 25 mm bolt',   2, 'TB6600 flange'),
        ('M3 × 22 mm bolt',   6, 'Bucks (x4) + Terminal (x2)'),
        ('M5 lock washer',    4, 'Under motor nut'),
        ('M5 flat washer',    8, 'PSU + motor top side'),
        ('M4 flat washer',    8, 'PSU top + bottom side'),
        ('M3 flat washer',   24, 'All M3 holes, both sides'),
        ('M5 nut',            4, 'Motor underside'),
        ('M4 nut',            4, 'PSU underside'),
        ('M3 nut',           12, 'All M3 holes'),
        ('Nylon standoff 10 mm M3', 4, 'Under Mega'),
        ('Nylon standoff  5 mm M3', 4, 'Under Bucks (or skip + use VHB pad)'),
    ]
    for item, qty, note in hw_list:
        tab_ax.text(0.04, y, f'{qty:2d} ×', fontsize=7, family='monospace',
                    fontweight='bold', color='#0050a0')
        tab_ax.text(0.10, y, item, fontsize=7, family='monospace')
        tab_ax.text(0.42, y, note, fontsize=6.5, color='#666', style='italic')
        y -= 0.016

    # Instructions
    y -= 0.012
    tab_ax.text(0.04, y, 'DRILLING PROCEDURE', fontsize=9, fontweight='bold')
    y -= 0.018
    instr = [
        '1. Mark wood-base center (datum); draw +X and +Y axes lightly with pencil.',
        '2. Mark every hole position with center punch using the X/Y column values.',
        '3. Pilot-drill all positions with Ø2 mm bit first (prevents wandering).',
        '4. Final-drill each position to its listed Ø (clearance for bolt thread).',
        '5. Use hole saw for the Ø100 take-down opening (centered on datum).',
        '6. Counterbore PSU + Motor holes Ø8 × 2 mm from underside (recess nut).',
        '7. Tolerance ±1.0 mm; dry-fit component before tightening bolts.',
        '8. Apply blue threadlocker on M5 motor bolts (lock washer + threadlock).',
    ]
    for line in instr:
        tab_ax.text(0.04, y, line, fontsize=6.5, color='#222')
        y -= 0.016

    plt.tight_layout()
    out_png = os.path.join(OUTDIR, 'drilling_guide.png')
    out_pdf = os.path.join(OUTDIR, 'drilling_guide.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

# ============================================================
# Drawing 3: OPERATOR PANEL FRONT VIEW (unchanged from V1.0)
# ============================================================
def draw_operator_panel():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    ax.set_aspect('equal')
    ax.set_xlim(-140, 140)
    ax.set_ylim(-30, 110)
    ax.set_facecolor('white')
    ax.grid(True, linestyle=':', linewidth=0.3, color='#cccccc')

    PW, PH = 200, 60
    ax.add_patch(Rectangle((-PW / 2, 0), PW, PH, facecolor='#dadde0',
                           edgecolor='black', lw=2.0))
    ax.text(0, PH + 8, 'PANEL: 200 × 60 × 3 mm  (3 mm plywood OR 2 mm aluminum)',
            fontsize=9, ha='center', fontweight='bold')

    # IEC C14 (cutout 27 x 19 at -70, 30)
    iec_w, iec_h = 27, 19
    ax.add_patch(Rectangle((-70 - iec_w/2, 30 - iec_h/2), iec_w, iec_h,
                           facecolor='#1a1a1a', edgecolor='black', lw=1.0))
    for px, py in [(-3.5, -4), (3.5, -4), (0, 4)]:
        ax.add_patch(Circle((-70 + px, 30 + py), 1.8, facecolor='#444',
                            edgecolor='black', lw=0.4))
    ax.text(-70, 50, 'IEC C14', fontsize=8, ha='center', fontweight='bold')
    ax.text(-70, 46, '27 × 19 cutout', fontsize=6, ha='center', color='#666')
    ax.text(-70, 8, 'AC MAINS IN', fontsize=6, ha='center', fontweight='bold')

    # Fuse Ø12
    ax.add_patch(Circle((-25, 30), 6, facecolor='#3a3a3a', edgecolor='black', lw=1.2))
    ax.add_patch(Circle((-25, 30), 4, facecolor='#888', edgecolor='black', lw=0.5))
    ax.text(-25, 50, 'FUSE 2A T', fontsize=8, ha='center', fontweight='bold')
    ax.text(-25, 46, 'Ø12 cutout', fontsize=6, ha='center', color='#666')

    # E-stop Ø22
    ax.add_patch(Circle((20, 30), 11, facecolor='#1a1a1a', edgecolor='black', lw=1.2))
    ax.add_patch(Circle((20, 30), 15, facecolor='#d40000', edgecolor='#660000', lw=1.0))
    ax.text(20, 30, 'STOP', fontsize=10, ha='center', va='center',
            color='white', fontweight='bold')
    ax.text(20, 54, 'EMERGENCY STOP', fontsize=8, ha='center',
            color='#d40000', fontweight='bold')
    ax.text(20, 50, '22 mm mushroom', fontsize=6, ha='center', color='#666')

    # LEDs
    ax.add_patch(Circle((75, 35), 2.5, facecolor='#0c0', edgecolor='black', lw=0.6))
    ax.add_patch(Circle((75, 25), 2.5, facecolor='#f80', edgecolor='black', lw=0.6))
    ax.text(82, 35, 'POWER (green)', fontsize=7, va='center')
    ax.text(82, 25, 'FAULT (amber)', fontsize=7, va='center')
    ax.text(75, 50, 'STATUS', fontsize=8, ha='center', fontweight='bold')

    # Dimensions
    dim_h(ax, -PW/2, PW/2, 0, '200 mm', offset_y=14)
    dim_v(ax, 0, PH, PW/2, '60 mm', offset_x=14)
    dim_h(ax, -PW/2, -70, 0, '30 (to IEC ctr)', offset_y=28)
    dim_h(ax, -70, -25, 0, '45', offset_y=42)
    dim_h(ax, -25, 20, 0, '45', offset_y=42)
    dim_h(ax, 20, 75, 0, '55', offset_y=42)

    for bx in [-90, +90]:
        ax.add_patch(Rectangle((bx - 4, 4), 8, 8, facecolor='none',
                               edgecolor=HOLE_COLOR, lw=1.2, linestyle='--'))
        ax.text(bx, 0, f'L-bkt M4\nto wood', fontsize=6, ha='center', color=HOLE_COLOR)

    ax.set_xlabel('X (mm) — operator-facing', fontsize=9)
    ax.set_ylabel('Z (mm) — height above panel bottom', fontsize=9)
    ax.set_title('CSM V3 — FRONT OPERATOR PANEL  (Sheet 3 of 4)',
                 fontsize=12, fontweight='bold', pad=14)

    plt.tight_layout()
    out_png = os.path.join(OUTDIR, 'operator_panel.png')
    out_pdf = os.path.join(OUTDIR, 'operator_panel.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

# ============================================================
# Drawing 4: COMPONENTS REFERENCE CARD
# ============================================================
def draw_components_card():
    fig, ax = plt.subplots(figsize=(14, 18), dpi=150)
    ax.set_xlim(0, 100); ax.set_ylim(0, 140)
    ax.axis('off')
    ax.set_title('CSM V3 — ELECTRICAL COMPONENTS REFERENCE CARD  (Sheet 4 of 4)',
                 fontsize=14, fontweight='bold', pad=14)

    cards = [
        ('Mean Well S-250-24 PSU', 'B07Y7L664K',
         '24V DC, 10A (240W). AC input switchable 115/230V.',
         '199 × 110 × 50 mm | mass ~960 g | 4× M4 chassis',
         '#9aa1a8', 'https://www.amazon.com/dp/B07Y7L664K'),
        ('Arduino Mega 2560 REV3', 'B0046AMGW0',
         'Real-time controller. Mega <-> Pi via UART/USB 115200 baud.',
         '102 × 54 mm | 4× M3 PCB holes | USB-B port',
         '#1f4ea8', 'https://www.amazon.com/dp/B0046AMGW0'),
        ('Raspberry Pi 4 4GB Starter', 'B07V5JTMV9',
         'Touchscreen UI + pattern logic. Lives on touchscreen mast.',
         '85 × 56 mm | 4× M2.5 mounting | HDMI + USB-C',
         '#0c6e3a', 'https://www.amazon.com/dp/B07V5JTMV9'),
        ('TB6600 Stepper Driver 4A', 'B08SG7L54W',
         'Drives NEMA 23 (2.8A < 4A rating). Microstep + current via DIP.',
         '96 × 56 × 37 mm | 2× M3 flange | screw terminals',
         '#c43838', 'https://www.amazon.com/dp/B08SG7L54W'),
        ('RioRand LM2596 DC-DC Buck', 'B008BHB4L8',
         'Adjustable 24V -> 5V. TWO units: #1 Mega+servos, #2 Pi.',
         '43 × 21 mm | 2× M3 corner holes | adj trimpot',
         '#0f6b34', 'https://www.amazon.com/dp/B008BHB4L8'),
        ('NEMA 23 + 5:1 HG5 Gearbox', '(StepperOnline)',
         'Drive motor. Body 57×57×56 + 50 mm gearbox = 106 mm tower.',
         '57 × 57 footprint | 4× M5 PCD 47.14 flange | shaft Ø14',
         '#7a7e85', '(supplier StepperOnline 23HS22-2804S-HG5)'),
    ]

    y = 130
    for title, asin, desc, spec, color, link in cards:
        ax.add_patch(Rectangle((4, y - 16), 18, 14, facecolor=color,
                               edgecolor='black', lw=1.0))
        ax.text(13, y - 9, asin if asin.startswith('B') else 'STEP',
                fontsize=7, ha='center', va='center', color='white', fontweight='bold')
        ax.text(26, y - 2, title, fontsize=12, fontweight='bold', color='#111')
        ax.text(26, y - 6, f'ASIN: {asin}', fontsize=8.5, color='#666', family='monospace')
        ax.text(26, y - 10, desc, fontsize=8.5, color='#222')
        ax.text(26, y - 14, spec, fontsize=8, color='#444', family='monospace')
        ax.text(26, y - 17.5, link, fontsize=7, color='#0050a0', style='italic')
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
if __name__ == '__main__':
    print("=" * 70)
    print("CSM V3 -- Generating drilling drawings (V1.1)")
    print("=" * 70)
    print()
    print(f"Total drill holes to be marked: {len(DRILL_LIST)}")
    print()
    print("Sheet 1: Wood Base Top View (with dimensions)")
    draw_wood_base_top()
    print()
    print("Sheet 2: Drilling Template (numbered holes + coordinate table)")
    draw_drilling_guide()
    print()
    print("Sheet 3: Front Operator Panel")
    draw_operator_panel()
    print()
    print("Sheet 4: Components Reference Card")
    draw_components_card()
    print()
    print("=" * 70)
    print("Done. PDFs are vector (print to A3 or A2 for accurate scale).")
    print("=" * 70)
