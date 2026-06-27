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

import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# FreeCAD Part for STEP export (only available when run via FreeCAD's Python)
try:
    import FreeCAD
    import Part
    HAS_FREECAD = True
except ImportError:
    HAS_FREECAD = False
    print("WARNING: FreeCAD not available; STEP export will be skipped.")

# machine_datums for STEP geometry
sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
try:
    import machine_datums as MD
except ImportError:
    MD = None
    print("WARNING: machine_datums not importable; STEP export will be skipped.")

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

# Frame parts have their drawings in their own folders (not lumped here)
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(OUTDIR)))
FRAME_DIRS = {
    'wood_base':       os.path.join(_REPO_ROOT, 'CSM_V3_ASSEMBLY', 'frame', 'wood_base'),
    'wood_upper_deck': os.path.join(_REPO_ROOT, 'CSM_V3_ASSEMBLY', 'frame', 'wood_upper_deck'),
    'mount_plate':     os.path.join(_REPO_ROOT, 'CSM_V3_ASSEMBLY', 'frame', 'mount_plate_6061'),
}

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
# Drawing 5: HARDWARE ORDER SHEET (single-page printable A4)
# ============================================================
def draw_hardware_order_sheet():
    """A4 portrait, optimized for printing and taking to hardware store."""
    # A4 portrait = 210 x 297 mm = 8.27 x 11.69 in
    fig = plt.figure(figsize=(8.27, 11.69), dpi=200)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis('off')

    # ===== HEADER =====
    ax.add_patch(Rectangle((4, 134), 92, 4, facecolor='#1f4ea8', edgecolor='none'))
    ax.text(50, 136, 'CSM V3 — HARDWARE ORDER SHEET',
            fontsize=14, ha='center', va='center', color='white', fontweight='bold')
    ax.text(50, 132, 'Wood Base V1.1 Electrical Mounting   •   Rev V1.0   •   2026-06-04',
            fontsize=8, ha='center', color='#444')

    # Customer/date row
    ax.add_patch(Rectangle((4, 126), 92, 5, facecolor='#f4f4f4', edgecolor='#ccc', lw=0.5))
    ax.text(7, 128.5, 'NAME:', fontsize=8, fontweight='bold', va='center')
    ax.plot([16, 50], [127.5, 127.5], color='#666', lw=0.5)
    ax.text(54, 128.5, 'ORDER DATE:', fontsize=8, fontweight='bold', va='center')
    ax.plot([70, 96], [127.5, 127.5], color='#666', lw=0.5)

    # ===== SECTION 1: BOLTS =====
    y = 122
    ax.add_patch(Rectangle((4, y - 1), 92, 3, facecolor='#1f4ea8', edgecolor='none'))
    ax.text(6, y + 0.5, '1. BOLTS  (machine screws, partial thread OK, pan or socket head)',
            fontsize=10, color='white', fontweight='bold', va='center')
    y -= 5

    # Column headers
    headers = [('☐', 4), ('QTY', 8), ('SIZE', 16), ('USE', 40), ('NOTES', 75)]
    for h, x in headers:
        ax.text(x, y, h, fontsize=7, fontweight='bold', color='#444')
    y -= 1.5
    ax.plot([4, 96], [y, y], color='#aaa', lw=0.4)
    y -= 2

    bolts = [
        ('4', 'M5 × 35 mm', 'NEMA 23 motor flange',         'Use w/ lock washer + threadlock'),
        ('4', 'M4 × 30 mm', 'PSU chassis',                   'Pan-head; rubber washer optional'),
        ('4', 'M3 × 30 mm', 'Arduino Mega (with standoffs)', '10 mm standoff under PCB'),
        ('2', 'M3 × 25 mm', 'TB6600 stepper driver flange',  'Through 4 mm flange tabs'),
        ('6', 'M3 × 22 mm', 'Bucks (×4) + Terminal (×2)',    'Or VHB pad on Bucks → skip 4 of these'),
    ]
    for qty, size, use, notes in bolts:
        ax.add_patch(Rectangle((5, y - 0.8), 1.8, 1.8, facecolor='white',
                               edgecolor='black', lw=0.8))
        ax.text(8, y, qty, fontsize=9, ha='right', va='center', fontweight='bold',
                color='#0050a0', family='monospace')
        ax.text(16, y, size, fontsize=8.5, va='center', family='monospace',
                fontweight='bold')
        ax.text(40, y, use, fontsize=8, va='center', color='#222')
        ax.text(75, y, notes, fontsize=7, va='center', color='#666', style='italic')
        y -= 3

    # Bolt subtotal
    ax.plot([4, 96], [y + 0.5, y + 0.5], color='#888', lw=0.4, linestyle=':')
    y -= 1.5
    ax.text(8, y, 'Subtotal: 20 bolts (or 16 if using VHB on Bucks)',
            fontsize=8, fontweight='bold', color='#444')
    y -= 4

    # ===== SECTION 2: WASHERS =====
    ax.add_patch(Rectangle((4, y - 1), 92, 3, facecolor='#1f4ea8', edgecolor='none'))
    ax.text(6, y + 0.5, '2. WASHERS', fontsize=10, color='white',
            fontweight='bold', va='center')
    y -= 5

    washers = [
        ('8',  'M5 flat washer',  'Under motor bolt head AND nut',  ''),
        ('4',  'M5 lock washer',  'Under motor nut (anti-vibration)', 'MANDATORY — motor vibrates'),
        ('8',  'M4 flat washer',  'PSU top + bottom',               ''),
        ('24', 'M3 flat washer',  'All M3 bolts, both sides',       'Pack of 50 is fine'),
    ]
    for qty, size, use, notes in washers:
        ax.add_patch(Rectangle((5, y - 0.8), 1.8, 1.8, facecolor='white',
                               edgecolor='black', lw=0.8))
        ax.text(8, y, qty, fontsize=9, ha='right', va='center', fontweight='bold',
                color='#0050a0', family='monospace')
        ax.text(16, y, size, fontsize=8.5, va='center', family='monospace',
                fontweight='bold')
        ax.text(40, y, use, fontsize=8, va='center', color='#222')
        ax.text(75, y, notes, fontsize=7, va='center', color='#a00', style='italic')
        y -= 3

    y -= 1

    # ===== SECTION 3: NUTS =====
    ax.add_patch(Rectangle((4, y - 1), 92, 3, facecolor='#1f4ea8', edgecolor='none'))
    ax.text(6, y + 0.5, '3. NUTS', fontsize=10, color='white', fontweight='bold', va='center')
    y -= 5

    nuts = [
        ('4',  'M5 hex nut', 'Motor underside',  ''),
        ('4',  'M4 hex nut', 'PSU underside',    ''),
        ('12', 'M3 hex nut', 'All M3 bolts',     'Nyloc nut OK — extra security'),
    ]
    for qty, size, use, notes in nuts:
        ax.add_patch(Rectangle((5, y - 0.8), 1.8, 1.8, facecolor='white',
                               edgecolor='black', lw=0.8))
        ax.text(8, y, qty, fontsize=9, ha='right', va='center', fontweight='bold',
                color='#0050a0', family='monospace')
        ax.text(16, y, size, fontsize=8.5, va='center', family='monospace',
                fontweight='bold')
        ax.text(40, y, use, fontsize=8, va='center', color='#222')
        ax.text(75, y, notes, fontsize=7, va='center', color='#666', style='italic')
        y -= 3

    y -= 1

    # ===== SECTION 4: STANDOFFS =====
    ax.add_patch(Rectangle((4, y - 1), 92, 3, facecolor='#1f4ea8', edgecolor='none'))
    ax.text(6, y + 0.5, '4. NYLON STANDOFFS (M3 female-female, threaded)',
            fontsize=10, color='white', fontweight='bold', va='center')
    y -= 5

    standoffs = [
        ('4', 'M3 × 10 mm nylon standoff', 'Under Arduino Mega', 'PCB airflow'),
        ('4', 'M3 ×  5 mm nylon standoff', 'Under each Buck',    'Optional if using VHB tape'),
    ]
    for qty, size, use, notes in standoffs:
        ax.add_patch(Rectangle((5, y - 0.8), 1.8, 1.8, facecolor='white',
                               edgecolor='black', lw=0.8))
        ax.text(8, y, qty, fontsize=9, ha='right', va='center', fontweight='bold',
                color='#0050a0', family='monospace')
        ax.text(16, y, size, fontsize=8.5, va='center', family='monospace',
                fontweight='bold')
        ax.text(40, y, use, fontsize=8, va='center', color='#222')
        ax.text(75, y, notes, fontsize=7, va='center', color='#666', style='italic')
        y -= 3

    y -= 1

    # ===== SECTION 5: CONSUMABLES =====
    ax.add_patch(Rectangle((4, y - 1), 92, 3, facecolor='#1f4ea8', edgecolor='none'))
    ax.text(6, y + 0.5, '5. CONSUMABLES', fontsize=10, color='white',
            fontweight='bold', va='center')
    y -= 5

    cons = [
        ('1', 'Loctite 243 (blue)', 'Threadlock for M5 motor bolts',  'Small bottle is plenty'),
        ('1', '3M VHB tape (optional)', 'Alt mounting for Bucks',      '20×20 mm pads, qty 8'),
        ('1', 'Pack ferrules 0.5-2.5 mm²', 'Wire ends into screw terms','Crimper required'),
        ('1', 'Pack heat shrink 3-8 mm', 'Wire terminations',          'Black + red mixed'),
    ]
    for qty, size, use, notes in cons:
        ax.add_patch(Rectangle((5, y - 0.8), 1.8, 1.8, facecolor='white',
                               edgecolor='black', lw=0.8))
        ax.text(8, y, qty, fontsize=9, ha='right', va='center', fontweight='bold',
                color='#0050a0', family='monospace')
        ax.text(16, y, size, fontsize=8.5, va='center', family='monospace',
                fontweight='bold')
        ax.text(40, y, use, fontsize=8, va='center', color='#222')
        ax.text(75, y, notes, fontsize=7, va='center', color='#666', style='italic')
        y -= 3

    y -= 1

    # ===== SECTION 6: DRILL BITS =====
    ax.add_patch(Rectangle((4, y - 1), 92, 3, facecolor='#0a6e3a', edgecolor='none'))
    ax.text(6, y + 0.5, '6. DRILL BITS (verify you have these before starting)',
            fontsize=10, color='white', fontweight='bold', va='center')
    y -= 5

    bits = [
        ('1', 'Ø 2.0 mm HSS', 'Pilot drill for ALL positions',  'Prevents wandering'),
        ('1', 'Ø 3.2 mm HSS', 'M3 clearance (10 holes)',         'Mega, Bucks, Terminal'),
        ('1', 'Ø 3.5 mm HSS', 'M3 clearance for TB6600 (2 holes)', 'TB6600 flange'),
        ('1', 'Ø 4.5 mm HSS', 'M4 clearance for PSU (4 holes)',  'PSU chassis'),
        ('1', 'Ø 5.5 mm HSS', 'M5 clearance for motor (4 holes)','NEMA 23 flange'),
        ('1', 'Ø 100 mm hole saw OR jigsaw', 'Take-down (1 hole)','Center on datum'),
        ('1', 'Ø 8 mm HSS (optional)', 'Counterbore PSU + motor nuts', 'Recess nut into wood'),
    ]
    for qty, size, use, notes in bits:
        ax.add_patch(Rectangle((5, y - 0.8), 1.8, 1.8, facecolor='white',
                               edgecolor='black', lw=0.8))
        ax.text(8, y, qty, fontsize=9, ha='right', va='center', fontweight='bold',
                color='#0a6e3a', family='monospace')
        ax.text(16, y, size, fontsize=8.5, va='center', family='monospace',
                fontweight='bold')
        ax.text(40, y, use, fontsize=8, va='center', color='#222')
        ax.text(75, y, notes, fontsize=7, va='center', color='#666', style='italic')
        y -= 3

    # ===== FOOTER =====
    ax.add_patch(Rectangle((4, y - 3.5), 92, 3, facecolor='#fff3b0',
                           edgecolor='#a89030', lw=0.8))
    ax.text(50, y - 2, 'TIP: A 100-piece M3 + M4 bolt/nut/washer assortment '
                       'kit usually covers everything except M5 motor bolts.',
            fontsize=8, ha='center', va='center', color='#5a4020', style='italic')
    y -= 6

    ax.text(50, y, 'NOTES:', fontsize=8, fontweight='bold', va='top')
    # Note lines for handwriting
    for i in range(3):
        ax.plot([4, 96], [y - 2 - i * 2, y - 2 - i * 2], color='#aaa', lw=0.3)

    # ===== Footer banner =====
    ax.add_patch(Rectangle((4, 1), 92, 3, facecolor='#222', edgecolor='none'))
    ax.text(50, 2.5, 'github.com/leoalex196912/ChatGistory  •  '
                     'CSM_V3_ASSEMBLY/electronics/drawings/  •  '
                     'See drilling_guide.pdf for hole coords',
            fontsize=7, ha='center', va='center', color='white')

    out_png = os.path.join(OUTDIR, 'hardware_order_sheet.png')
    out_pdf = os.path.join(OUTDIR, 'hardware_order_sheet.pdf')
    fig.savefig(out_png, dpi=200, facecolor='white')
    fig.savefig(out_pdf, facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

# ============================================================
# Helper: minimal DXF writer (for wood shop / CNC input)
# ============================================================
def _dxf_header():
    return ("0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n"
            "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n"
            "0\nLAYER\n2\nOUTLINE\n70\n0\n62\n7\n6\nCONTINUOUS\n"
            "0\nLAYER\n2\nHOLES\n70\n0\n62\n1\n6\nCONTINUOUS\n"
            "0\nLAYER\n2\nTEXT\n70\n0\n62\n3\n6\nCONTINUOUS\n"
            "0\nENDTAB\n0\nENDSEC\n"
            "0\nSECTION\n2\nENTITIES\n")

def _dxf_footer():
    return "0\nENDSEC\n0\nEOF\n"

def _dxf_line(x1, y1, x2, y2, layer='OUTLINE'):
    return (f"0\nLINE\n8\n{layer}\n"
            f"10\n{x1}\n20\n{y1}\n30\n0\n"
            f"11\n{x2}\n21\n{y2}\n31\n0\n")

def _dxf_circle(cx, cy, r, layer='HOLES'):
    return (f"0\nCIRCLE\n8\n{layer}\n"
            f"10\n{cx}\n20\n{cy}\n30\n0\n40\n{r}\n")

def _dxf_text(x, y, text, height=4.0, layer='TEXT'):
    return (f"0\nTEXT\n8\n{layer}\n"
            f"10\n{x}\n20\n{y}\n30\n0\n40\n{height}\n1\n{text}\n")

def _dxf_rect(cx, cy, w, h, layer='OUTLINE'):
    x0, y0 = cx - w/2, cy - h/2
    x1, y1 = cx + w/2, cy + h/2
    return (_dxf_line(x0, y0, x1, y0, layer) +
            _dxf_line(x1, y0, x1, y1, layer) +
            _dxf_line(x1, y1, x0, y1, layer) +
            _dxf_line(x0, y1, x0, y0, layer))

def write_dxf(filepath, entities):
    """entities = list of strings (each from _dxf_line/_circle/etc.)"""
    with open(filepath, 'w') as f:
        f.write(_dxf_header())
        for e in entities:
            f.write(e)
        f.write(_dxf_footer())

# ============================================================
# Helper for the procedure / checklist sheets
# ============================================================
def _checkbox_step(ax, x, y, n, text, fs=8, box_size=2.0, color='#222'):
    """Draws a checkbox + step number + step text."""
    ax.add_patch(Rectangle((x, y - box_size/2), box_size, box_size,
                           facecolor='white', edgecolor='black', lw=0.8))
    ax.text(x + box_size + 1.5, y, f'{n}.', fontsize=fs, va='center',
            fontweight='bold', color='#0050a0', family='monospace')
    ax.text(x + box_size + 4.5, y, text, fontsize=fs, va='center', color=color)

def _section_band(ax, x, y, w, h, label, color='#1f4ea8', fontsize=10):
    """Section header band with text inside."""
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor='none'))
    ax.text(x + 2, y + h/2, label, fontsize=fontsize, color='white',
            fontweight='bold', va='center')

# ============================================================
# Drawing 6: ASSEMBLY PROCEDURE SHEET (2-page A4 PDF, 2 PNG files)
# ============================================================
def _header(ax, title, subtitle, banner_color='#1f4ea8',
            fields=(('BUILDER:', 18, 50), ('DATE:', 60, 96))):
    """Standard header for printable sheets."""
    ax.add_patch(Rectangle((4, 134), 92, 4, facecolor=banner_color, edgecolor='none'))
    ax.text(50, 136, title, fontsize=14, ha='center', va='center',
            color='white', fontweight='bold')
    ax.text(50, 132, subtitle, fontsize=8, ha='center', color='#444')
    ax.add_patch(Rectangle((4, 126), 92, 5, facecolor='#f4f4f4',
                           edgecolor='#ccc', lw=0.5))
    x_cursor = 7
    for (lab, end_x, line_end) in fields:
        ax.text(x_cursor, 128.5, lab, fontsize=8, fontweight='bold', va='center')
        ax.plot([end_x, line_end], [127.5, 127.5], color='#666', lw=0.5)
        x_cursor = line_end + 2

def _footer(ax, label, page=None, total=None):
    ax.add_patch(Rectangle((4, 1), 92, 3, facecolor='#222', edgecolor='none'))
    page_txt = f'  •  Page {page} of {total}' if page else ''
    ax.text(50, 2.5,
            f'github.com/leoalex196912/ChatGistory  •  CSM V3 — {label}{page_txt}',
            fontsize=7, ha='center', va='center', color='white')

def _new_a4():
    fig = plt.figure(figsize=(8.27, 11.69), dpi=200)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis('off')
    return fig, ax

def draw_assembly_procedure():
    # ====================== PAGE 1 ======================
    fig1, ax = _new_a4()
    _header(ax, 'CSM V3 — ASSEMBLY PROCEDURE',
            'Wood Base V1.1 Electrical Mounting  •  Rev V1.0  •  '
            '~4-6 h  •  Page 1: Drilling + Mechanical')
    y = 122

    # === PHASE A: PREPARATION ===
    _section_band(ax, 4, y - 1, 92, 3, 'PHASE A — PREPARATION  (30 min)', color='#0a6e3a')
    y -= 5
    steps_A = [
        'Print drilling_guide.pdf at 1:1 scale. Verify with ruler that 50 mm marks measure 50 mm.',
        'Gather all hardware per hardware_order_sheet.pdf checklist.',
        'Stage tools: drill, drill bits (Ø2 / Ø3.2 / Ø3.5 / Ø4.5 / Ø5.5 / Ø100 saw), screwdrivers, wrenches, calipers.',
        'Wood-base orientation: long edge = X (500 mm), short edge = Y (400 mm). Mark "FRONT" arrow on -Y edge.',
        'Mark center of wood base (datum 0, 0). Draw faint +X and +Y axis lines with pencil.',
        'Tape the drilling_guide printout to the wood with axis lines aligned to the printed datum.',
    ]
    for i, s in enumerate(steps_A, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    # === PHASE B: DRILLING ===
    _section_band(ax, 4, y - 1, 92, 3, 'PHASE B — DRILLING  (1 h)', color='#0a6e3a')
    y -= 5
    steps_B = [
        'Center-punch ALL 21 hole positions through the paper template into the wood.',
        'Remove paper template. Pilot-drill every position with Ø 2.0 mm bit.',
        'Drill 10 × Ø 3.2 mm holes  (Mega ×4, Buck#1 ×2, Buck#2 ×2, Terminal ×2).',
        'Drill 2 × Ø 3.5 mm holes  (TB6600 flange).',
        'Drill 4 × Ø 4.5 mm holes  (PSU chassis).',
        'Drill 4 × Ø 5.5 mm holes  (NEMA 23 motor flange).',
        'Cut Ø 100 mm take-down opening with hole saw or jigsaw, centered on datum.',
        '(Optional) Counterbore PSU + Motor holes Ø 8 × 2 mm from UNDERSIDE to recess nuts.',
        'Vacuum dust. Verify hole positions with calipers — tolerance ±1 mm.',
    ]
    for i, s in enumerate(steps_B, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    # === PHASE C: MECHANICAL MOUNTING ===
    _section_band(ax, 4, y - 1, 92, 3, 'PHASE C — MECHANICAL MOUNTING  (1.5 h)', color='#0a6e3a')
    y -= 5
    steps_C = [
        'Dry-fit PSU at (-195, 0). Verify all 4 chassis screws align with Ø 4.5 holes.',
        'Bolt PSU: M4 × 30 + washer top, washer + nut bottom. Tighten cross-pattern.',
        'Set NEMA 23 + HG5 motor at (+85, -47), shaft pointing UP. Verify gearbox orientation.',
        'Bolt motor: M5 × 35 + washer + lock washer + nut. Apply Loctite 243 on threads.',
        'Mount TB6600 at (+200, -47). Bolt: M3 × 25 + washer + nut. Terminals face +X (edge).',
        'Install M3 × 10 mm nylon standoffs at the 4 Mega positions (+200, +75 area).',
        'Mount Arduino Mega on standoffs. Bolt: M3 × 30 + washer + nut. USB port faces +X.',
        'Mount LM2596 Buck #1 at (-50, +160) using M3 × 22 + 5 mm standoff (or 3M VHB).',
        'Mount LM2596 Buck #2 at (+50, +160) same method as Buck #1.',
        'Mount 24V terminal block at (0, +180). Use M3 × 22 OR DIN-rail clip.',
        'Build operator panel per operator_panel.pdf. L-bracket to FRONT (-Y) edge of wood base.',
    ]
    for i, s in enumerate(steps_C, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    _footer(ax, 'Assembly Procedure', page=1, total=2)
    out_png_p1 = os.path.join(OUTDIR, 'assembly_procedure_p1.png')
    fig1.savefig(out_png_p1, dpi=200, facecolor='white')

    # ====================== PAGE 2 ======================
    fig2, ax = _new_a4()
    _header(ax, 'CSM V3 — ASSEMBLY PROCEDURE',
            'Wood Base V1.1 Electrical Mounting  •  Rev V1.0  •  '
            '~4-6 h  •  Page 2: Wiring + Verify')
    y = 122

    # === PHASE D: WIRING ===
    _section_band(ax, 4, y - 1, 92, 3,
                  'PHASE D — WIRING  (2-3 h, see CSM_V3_WIRING_V1_0.md)',
                  color='#c43838')
    y -= 5
    steps_D = [
        'Wire mains FIRST with PSU DISCONNECTED from wall. 16 AWG brown/blue/g-y.',
        'Order: wall → E-stop → 2 A T-fuse → PSU L/N/PE terminals.',
        'Wire 24 V DC bus: PSU +V/-V → 24V terminal block. 14 AWG with ferrules.',
        'Branch 24 V to TB6600 power, Buck #1 IN, Buck #2 IN.',
        'BEFORE downstream loads: power bucks alone, adjust each to 5.10 V no-load.',
        'Wire 5 V #1 → Mega VIN + GND + 6× servo headers. Single-point GND.',
        'Wire 5 V #2 → Pi GPIO 5 V + GND (or USB-C wall wart for bench).',
        'Wire Mega → TB6600 step/dir/en (D5/D6/D7 with 220 Ω each).',
        'Wire NEMA 23 4-wire to TB6600 A+/A-/B+/B- (check motor color code).',
        'Wire E-stop second NC contact → Mega D2 with 10 kΩ pull-up.',
        'Cable-tie all wiring per ELECTRICAL_LAYOUT §2.6 (mains FRONT, 24V BACK).',
        'Label every wire bundle with tape: AC / 24V / 5V / SIG.',
    ]
    for i, s in enumerate(steps_D, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.5
    y -= 1

    # === SAFETY BANNER ===
    ax.add_patch(Rectangle((4, y - 4), 92, 3.5, facecolor='#ffd6d6',
                           edgecolor='#c00000', lw=1.0))
    ax.text(50, y - 2, '⚠ DO NOT CONNECT MAINS UNTIL BENCH-TEST PHASE 1 PASSES ⚠',
            fontsize=9, ha='center', va='center', color='#c00000', fontweight='bold')
    y -= 7

    # === PHASE E: VERIFY ===
    _section_band(ax, 4, y - 1, 92, 3, 'PHASE E — VERIFY BEFORE FIRST POWER  (15 min)',
                  color='#1f4ea8')
    y -= 5
    steps_E = [
        'Re-check every bolt is tight; no loose washers visible.',
        'Confirm all 4 motor bolts have lock washers + Loctite 243.',
        'Multimeter continuity: PE wire wall plug → PSU FG. Must be < 1 Ω.',
        'Multimeter resistance: PSU +V to -V terminals UNPOWERED. Should be high (>1 kΩ).',
        'No bare conductor exposed at any mains terminal. Cap unused terminals.',
        'Verify wire colors: brown=L, blue=N, green/yellow=PE, red=+, black=GND.',
        'PSU voltage selector SWITCH set to match your mains (115 OR 230 V).',
        'Photograph the finished assembly (top + 4 sides) for the record.',
        'Proceed to BENCH-TEST CHECKLIST (bench_test_checklist.pdf).',
    ]
    for i, s in enumerate(steps_E, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.5

    # Notes section
    y -= 1.5
    ax.text(4, y, 'NOTES / DEVIATIONS:', fontsize=8, fontweight='bold')
    y -= 2
    for i in range(3):
        ax.plot([4, 96], [y, y], color='#aaa', lw=0.3)
        y -= 2.2

    _footer(ax, 'Assembly Procedure', page=2, total=2)
    out_png_p2 = os.path.join(OUTDIR, 'assembly_procedure_p2.png')
    fig2.savefig(out_png_p2, dpi=200, facecolor='white')

    # Save combined PDF
    out_pdf = os.path.join(OUTDIR, 'assembly_procedure.pdf')
    with PdfPages(out_pdf) as pdf:
        pdf.savefig(fig1)
        pdf.savefig(fig2)
    plt.close(fig1)
    plt.close(fig2)
    print(f"  -> {out_png_p1}")
    print(f"  -> {out_png_p2}")
    print(f"  -> {out_pdf} (2 pages)")

# ============================================================
# Drawing 7: BENCH-TEST CHECKLIST (single-page printable A4)
# ============================================================
def draw_bench_test_checklist():
    # ====================== PAGE 1 ======================
    fig1, ax = _new_a4()
    _header(ax, 'CSM V3 — BENCH-TEST CHECKLIST',
            'Validate electronics BEFORE installing in machine  •  Rev V1.0  •  '
            '~1-2 h  •  Page 1: Pre-Test + Stages 1-3',
            banner_color='#c43838')
    y = 122

    # === PRE-TEST SAFETY ===
    _section_band(ax, 4, y - 1, 92, 3, 'PRE-TEST SAFETY (REQUIRED)', color='#c00000')
    y -= 5
    pre = [
        'Wall outlet behind a kill switch you can reach without touching the bench.',
        'Multimeter ready (DC voltage mode, set to 20 V or 200 V range).',
        'No food, drink, or wet items on bench. Dry hands. Insulated mat preferred.',
        'E-stop button accessible BEFORE energizing PSU.',
        'PSU voltage selector switch matches your wall voltage (115 OR 230 V).',
    ]
    for i, s in enumerate(pre, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5, color='#c00000')
        y -= 2.6
    y -= 1

    # === STAGE 1 ===
    _section_band(ax, 4, y - 1, 92, 3, 'STAGE 1 — PSU ONLY', color='#1f4ea8')
    y -= 5
    st1 = [
        'Wire mains: wall → E-stop → 2A fuse → PSU L/N/PE. NOTHING on PSU output.',
        'Press E-stop IN. Plug PSU into wall.',
        'Release E-stop. PSU green LED should illuminate.',
        ('Multimeter on PSU +V to -V terminals. Reading: ____ V  '
         '(expect 24.0 ± 0.2 V)'),
        'Adjust +V trimpot if needed; lock with paint marker once 24.0 V achieved.',
        'Press E-stop. PSU LED off within 1 s. Multimeter to 0 V within 2 s.',
        'PASS Stage 1: ☐ YES ☐ NO   (If NO: check mains wiring, do not proceed)',
    ]
    for i, s in enumerate(st1, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    # === STAGE 2 ===
    _section_band(ax, 4, y - 1, 92, 3, 'STAGE 2 — BUCKS + MEGA', color='#1f4ea8')
    y -= 5
    st2 = [
        'E-stop IN. Wire Buck #1 IN+/IN- to 24 V bus. Output disconnected.',
        'Release E-stop. Multimeter on Buck #1 output: ____ V  (adjust to 5.10 V)',
        'E-stop IN. Wire Buck #1 OUT+/OUT- to Mega VIN + GND.',
        'Release E-stop. Mega power LED (ON pin) should light.',
        'Connect USB to laptop. Mega should enumerate. Upload Blink sketch.',
        'LED 13 on Mega blinks at 1 Hz: ☐ verified',
        'Multimeter on Mega 5 V pin to GND: ____ V  (expect 4.95-5.10)',
        'Press E-stop. Mega LEDs off within 1 s.',
        'PASS Stage 2: ☐ YES ☐ NO',
    ]
    for i, s in enumerate(st2, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    # === STAGE 3 ===
    _section_band(ax, 4, y - 1, 92, 3, 'STAGE 3 — BUCKS #2 + Pi', color='#1f4ea8')
    y -= 5
    st3 = [
        'Repeat Stage 2 procedure for Buck #2. Adjust to 5.10 V no-load.',
        'Connect Pi 4 via Buck #2 OUT (or USB-C wall wart for bench test).',
        'Pi boots, touchscreen shows desktop within 60 s.',
        'Multimeter on Pi 5 V pin to GND under load: ____ V  (expect ≥ 5.00)',
        'PASS Stage 3: ☐ YES ☐ NO',
    ]
    for i, s in enumerate(st3, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    _footer(ax, 'Bench-Test Checklist', page=1, total=2)
    out_png_p1 = os.path.join(OUTDIR, 'bench_test_checklist_p1.png')
    fig1.savefig(out_png_p1, dpi=200, facecolor='white')

    # ====================== PAGE 2 ======================
    fig2, ax = _new_a4()
    _header(ax, 'CSM V3 — BENCH-TEST CHECKLIST',
            'Validate electronics BEFORE installing in machine  •  Rev V1.0  •  '
            '~1-2 h  •  Page 2: Stages 4-5 + Verdict',
            banner_color='#c43838')
    y = 122

    # === STAGE 4 ===
    _section_band(ax, 4, y - 1, 92, 3, 'STAGE 4 — TB6600 + NEMA 23', color='#1f4ea8')
    y -= 5
    st4 = [
        'E-stop IN. Wire TB6600 power (24 V), step/dir/en to Mega D5/D6/D7 via 220 Ω.',
        'Wire NEMA 23 4-wire to TB6600 A+/A-/B+/B-.',
        'Verify DIP switches: 8 microstep, 2.5 A current limit.',
        'Release E-stop. Upload slow-pulse sketch (1 step/100 ms).',
        'Motor rotates smoothly, no stutter or skipping: ☐ verified',
        'Listen for grinding or whine. Smooth hum is OK; harsh whine = wrong current.',
        'E-stop test: press during rotation. Motor stops within 200 ms.',
        'PASS Stage 4: ☐ YES ☐ NO',
    ]
    for i, s in enumerate(st4, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    # === STAGE 5 ===
    _section_band(ax, 4, y - 1, 92, 3, 'STAGE 5 — SERVOS (6× MG90S)', color='#1f4ea8')
    y -= 5
    st5 = [
        'E-stop IN. Wire ONE MG90S to Mega D9 + Buck #1 5 V rail.',
        'Release E-stop. Run sweep sketch (servo position 0-180-0).',
        'Servo motion clean, no jitter: ☐ verified',
        'Repeat for servos on D10, D11, D12, D44, D45. All 6 hold position.',
        'Combined load test: command all 6 servos to move. Multimeter on Buck #1 output.',
        'Voltage stays ≥ 4.95 V during combined motion: ____ V minimum observed',
        'PASS Stage 5: ☐ YES ☐ NO',
    ]
    for i, s in enumerate(st5, 1):
        _checkbox_step(ax, 5, y, i, s, fs=7.5)
        y -= 2.6
    y -= 1

    # === FINAL VERDICT ===
    ax.add_patch(Rectangle((4, y - 5), 92, 4.5, facecolor='#ffd', edgecolor='#aa9000', lw=1.2))
    ax.text(50, y - 1.5, 'FINAL VERDICT — Bench Test Complete',
            fontsize=10, ha='center', va='center', fontweight='bold', color='#553300')
    ax.text(8, y - 3.5,
            '☐ ALL 5 STAGES PASS  →  Electronics validated. Proceed to machine integration.',
            fontsize=8, va='center', color='#0a6e3a', fontweight='bold')
    ax.text(8, y - 4.5,
            '☐ ANY STAGE FAILED   →  Fix at the bench, NOT in the machine. Re-test.',
            fontsize=8, va='center', color='#c00000', fontweight='bold')
    y -= 7

    # Notes
    ax.text(4, y, 'NOTES / ANOMALIES:', fontsize=8, fontweight='bold')
    y -= 2.5
    for i in range(4):
        ax.plot([4, 96], [y, y], color='#aaa', lw=0.3)
        y -= 2.2

    _footer(ax, 'Bench-Test Checklist', page=2, total=2)
    out_png_p2 = os.path.join(OUTDIR, 'bench_test_checklist_p2.png')
    fig2.savefig(out_png_p2, dpi=200, facecolor='white')

    # Combined PDF
    out_pdf = os.path.join(OUTDIR, 'bench_test_checklist.pdf')
    with PdfPages(out_pdf) as pdf:
        pdf.savefig(fig1)
        pdf.savefig(fig2)
    plt.close(fig1)
    plt.close(fig2)
    print(f"  -> {out_png_p1}")
    print(f"  -> {out_png_p2}")
    print(f"  -> {out_pdf} (2 pages)")

# ============================================================
# WOOD UPPER DECK + ALUMINUM PLATE common dims
# ============================================================
UD_W, UD_D, UD_T = 320, 260, 18   # Wood upper deck
UD_CENTER_HOLE_D = 170
ALU_W, ALU_T = 250, 6.3            # Aluminum plate (square, 1/4" / 6.3 mm)
ALU_CENTER_HOLE_D = 170
PCD_FRAME_MOUNT = 180
PCD_OFFSET_DEG = 45

# ============================================================
# Drawing 8: WOOD UPPER DECK DRILLING SHEET (shop-ready)
# ============================================================
def draw_wood_upper_deck():
    fig = plt.figure(figsize=(20, 14), dpi=150)
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.02)
    ax = fig.add_subplot(gs[0])
    tb = fig.add_subplot(gs[1])

    ax.set_aspect('equal')
    ax.set_xlim(-220, 220)
    ax.set_ylim(-180, 180)
    ax.set_facecolor('white')
    ax.grid(True, linestyle=':', linewidth=0.3, color='#cccccc', zorder=0)
    ax.set_xticks(np.arange(-200, 201, 50))
    ax.set_yticks(np.arange(-150, 151, 50))

    # Datum
    ax.axhline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.6, zorder=1)
    ax.axvline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.6, zorder=1)
    ax.plot(0, 0, '+', color='#000', markersize=16, mew=1.5, zorder=3)
    ax.text(8, -8, 'DATUM (0, 0)', fontsize=7, color='#444')

    # Deck outline
    ax.add_patch(Rectangle((-UD_W/2, -UD_D/2), UD_W, UD_D,
                           facecolor=WOOD_FILL, edgecolor=WOOD_EDGE, lw=2.5, zorder=1))
    for gy in np.linspace(-UD_D/2 + 15, UD_D/2 - 15, 10):
        ax.plot([-UD_W/2 + 4, UD_W/2 - 4], [gy, gy], color='#a8865a',
                lw=0.3, alpha=0.4, zorder=1.5)

    # Center cam-ring hole
    ax.add_patch(Circle((0, 0), UD_CENTER_HOLE_D/2 + 4, facecolor='#ffeeee',
                        edgecolor='none', alpha=0.4, zorder=2))
    ax.add_patch(Circle((0, 0), UD_CENTER_HOLE_D/2, facecolor='white',
                        edgecolor=HOLE_COLOR, lw=1.8, linestyle='--', zorder=3))
    ax.text(0, 5, f'Ø{UD_CENTER_HOLE_D}', fontsize=11, ha='center', va='center',
            color=HOLE_COLOR, fontweight='bold')
    ax.text(0, -8, 'CAM RING + TAKE-DOWN', fontsize=7, ha='center', color=HOLE_COLOR)

    # 4× corner holes for uprights at (±150, ±120)
    n = 1
    for sx in (+150, -150):
        for sy in (+120, -120):
            draw_hole(ax, sx, sy, 5.5, n=n, fs=7)
            ax.text(sx + 10, sy + 10, f'({sx:+d}, {sy:+d})', fontsize=6, color='#222')
            n += 1

    # 4× PCD 180 holes at 45° offset
    pcd_holes = []
    for i in range(4):
        ang = np.radians(i * 90 + PCD_OFFSET_DEG)
        hx = (PCD_FRAME_MOUNT/2) * np.cos(ang)
        hy = (PCD_FRAME_MOUNT/2) * np.sin(ang)
        draw_hole(ax, hx, hy, 5.5, n=n, fs=7)
        ax.text(hx + 8, hy + 8, f'({hx:+.1f}, {hy:+.1f})', fontsize=6, color='#222')
        pcd_holes.append((hx, hy))
        n += 1

    # PCD reference circle (dotted)
    ax.add_patch(Circle((0, 0), PCD_FRAME_MOUNT/2, facecolor='none',
                        edgecolor='#888', lw=0.6, linestyle=':', zorder=2))
    ax.text(0, -PCD_FRAME_MOUNT/2 - 5, f'PCD Ø{PCD_FRAME_MOUNT}',
            fontsize=7, ha='center', color='#888')

    # Overall dimensions
    dim_h(ax, -UD_W/2, UD_W/2, -UD_D/2, '320 mm  (UPPER_DECK_W)', offset_y=20)
    dim_v(ax, -UD_D/2, UD_D/2, UD_W/2, '260 mm  (UPPER_DECK_D)', offset_x=20)
    # Half dimensions
    dim_h(ax, -UD_W/2, 0, UD_D/2 + 6, '160', offset_y=-10, color=DIM_FAINT, fontsize=6)
    dim_h(ax, 0, UD_W/2, UD_D/2 + 6, '160', offset_y=-10, color=DIM_FAINT, fontsize=6)
    dim_v(ax, -UD_D/2, 0, -UD_W/2 - 6, '130', offset_x=-22, color=DIM_FAINT, fontsize=6)
    dim_v(ax, 0, UD_D/2, -UD_W/2 - 6, '130', offset_x=-22, color=DIM_FAINT, fontsize=6)
    # Upright pitch
    dim_h(ax, -150, +150, +120 - 10, '300 (upright pitch)', offset_y=10,
          color='#0050a0', fontsize=7)
    dim_v(ax, -120, +120, +150 + 10, '240', offset_x=10, color='#0050a0', fontsize=7)

    ax.set_xlabel('X (mm) — origin at center', fontsize=9)
    ax.set_ylabel('Y (mm) — origin at center', fontsize=9)
    ax.set_title('CSM V3 — WOOD UPPER DECK V1.0 — DRILLING DRAWING\n'
                 'Sheet 8 of 8   |   320 × 260 × 18 mm hardwood',
                 fontsize=12, fontweight='bold', pad=14)

    # Title block
    tb.set_xlim(0, 1); tb.set_ylim(0, 1); tb.axis('off')
    tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                           facecolor='white', edgecolor='black', lw=1.5))
    rows = [
        ('PROJECT',   'CSM V3 — Circular Sock Machine'),
        ('PART',      'Wood Upper Deck V1.0'),
        ('SIZE',      '320 × 260 × 18 mm'),
        ('MATERIAL',  'Hardwood (walnut/maple/Baltic birch)'),
        ('FINISH',    'Sanded smooth, oiled or sealed'),
        ('TOLERANCE', '±1.0 mm (holes), ±2 mm (outline)'),
        ('REV',       'V1.0'),
        ('DATE',      '2026-06-05'),
        ('QTY',       '1 piece'),
    ]
    y = 0.96
    for k, v in rows:
        tb.text(0.06, y, k, fontsize=8, fontweight='bold', color='#444')
        tb.text(0.40, y, v, fontsize=8, color='#111')
        y -= 0.040

    tb.text(0.06, 0.55, 'HOLE LIST', fontsize=10, fontweight='bold')
    tb.text(0.06, 0.52, '#   X       Y      Drill   Use', fontsize=7,
            family='monospace', color='#444', fontweight='bold')
    holes_list = [
        ('1',  '+150', '-120',  'Ø5.5',  'upright SE'),
        ('2',  '+150', '+120',  'Ø5.5',  'upright NE'),
        ('3',  '-150', '-120',  'Ø5.5',  'upright SW'),
        ('4',  '-150', '+120',  'Ø5.5',  'upright NW'),
        ('5',  '+63.6', '+63.6', 'Ø5.5',  'plate NE (PCD180 @ 45°)'),
        ('6',  '-63.6', '+63.6', 'Ø5.5',  'plate NW (PCD180 @ 135°)'),
        ('7',  '-63.6', '-63.6', 'Ø5.5',  'plate SW (PCD180 @ 225°)'),
        ('8',  '+63.6', '-63.6', 'Ø5.5',  'plate SE (PCD180 @ 315°)'),
        ('—',  '0',    '0',     'Ø170',  'cam ring through-hole'),
    ]
    yy = 0.49
    for row in holes_list:
        tb.text(0.06, yy, f'{row[0]:<3s} {row[1]:>5s}  {row[2]:>5s}  {row[3]:>5s}  {row[4]}',
                fontsize=6.5, family='monospace')
        yy -= 0.026

    yy -= 0.01
    tb.plot([0.04, 0.96], [yy, yy], color='black', lw=0.6)
    yy -= 0.02
    tb.text(0.06, yy, 'TOTAL: 9 holes  (8× Ø5.5 + 1× Ø170)',
            fontsize=8, fontweight='bold')

    yy -= 0.05
    tb.text(0.06, yy, 'NOTES', fontsize=10, fontweight='bold')
    yy -= 0.025
    notes = [
        '• Hole tolerance ±1 mm acceptable',
        '• Cam-ring hole can be jigsawed if no Ø170 hole saw',
        '• Sand all edges before assembly',
        '• Bolt: M5 × 35 mm through wood into',
        '  T-nut (upright) or M5 insert (plate)',
        '• Dry-fit before any glue/finish',
    ]
    for n in notes:
        tb.text(0.06, yy, n, fontsize=7, color='#222')
        yy -= 0.022

    plt.tight_layout()
    out_png = os.path.join(FRAME_DIRS['wood_upper_deck'],
                           'CSM_V3_WoodUpperDeck_V1_0_drilling.png')
    out_pdf = os.path.join(FRAME_DIRS['wood_upper_deck'],
                           'CSM_V3_WoodUpperDeck_V1_0_drilling.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

    # DXF export
    entities = []
    # outline (rectangle)
    entities.append(_dxf_rect(0, 0, UD_W, UD_D))
    # center hole
    entities.append(_dxf_circle(0, 0, UD_CENTER_HOLE_D/2))
    # 4 corner holes
    for sx in (+150, -150):
        for sy in (+120, -120):
            entities.append(_dxf_circle(sx, sy, 5.5/2))
    # 4 PCD holes
    for i in range(4):
        ang = np.radians(i * 90 + PCD_OFFSET_DEG)
        hx = (PCD_FRAME_MOUNT/2) * np.cos(ang)
        hy = (PCD_FRAME_MOUNT/2) * np.sin(ang)
        entities.append(_dxf_circle(hx, hy, 5.5/2))
    # text labels
    entities.append(_dxf_text(-UD_W/2 + 10, UD_D/2 - 15,
                              'CSM V3 WOOD UPPER DECK V1.0'))
    entities.append(_dxf_text(-UD_W/2 + 10, UD_D/2 - 25,
                              'MATERIAL: Hardwood Plywood 18mm'))
    entities.append(_dxf_text(-UD_W/2 + 10, UD_D/2 - 35,
                              'SIZE: 320 x 260 mm'))
    entities.append(_dxf_text(-UD_W/2 + 10, UD_D/2 - 45,
                              'HOLES: 8x Dia 5.5 + 1x Dia 170'))
    out_dxf = os.path.join(FRAME_DIRS['wood_upper_deck'],
                           'CSM_V3_WoodUpperDeck_V1_0_320x260x18.dxf')
    write_dxf(out_dxf, entities)
    print(f"  -> {out_dxf} (CNC-ready)")

# ============================================================
# Drawing 9: ALUMINUM MASTER-DATUM PLATE DRILLING SHEET
# ============================================================
def draw_aluminum_plate():
    fig = plt.figure(figsize=(20, 14), dpi=150)
    gs = fig.add_gridspec(1, 2, width_ratios=[3, 1], wspace=0.02)
    ax = fig.add_subplot(gs[0])
    tb = fig.add_subplot(gs[1])

    ax.set_aspect('equal')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_facecolor('white')
    ax.grid(True, linestyle=':', linewidth=0.3, color='#cccccc', zorder=0)
    ax.set_xticks(np.arange(-150, 151, 50))
    ax.set_yticks(np.arange(-150, 151, 50))

    # Datum
    ax.axhline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.6, zorder=1)
    ax.axvline(0, color='#888', lw=0.5, linestyle='-.', alpha=0.6, zorder=1)
    ax.plot(0, 0, '+', color='#000', markersize=16, mew=1.5, zorder=3)
    ax.text(8, -8, 'DATUM (0, 0)', fontsize=7, color='#444')

    # Plate outline (aluminum gray with subtle brushed effect)
    ax.add_patch(Rectangle((-ALU_W/2, -ALU_W/2), ALU_W, ALU_W,
                           facecolor='#cfd2d6', edgecolor='#5a5d62', lw=2.5, zorder=1))
    # Brushed-aluminum texture lines
    for gy in np.linspace(-ALU_W/2 + 10, ALU_W/2 - 10, 30):
        ax.plot([-ALU_W/2 + 4, ALU_W/2 - 4], [gy, gy], color='#aaaeb3',
                lw=0.3, alpha=0.5, zorder=1.5)

    # Center cam-ring clearance hole
    ax.add_patch(Circle((0, 0), ALU_CENTER_HOLE_D/2 + 4, facecolor='#ffeeee',
                        edgecolor='none', alpha=0.4, zorder=2))
    ax.add_patch(Circle((0, 0), ALU_CENTER_HOLE_D/2, facecolor='white',
                        edgecolor=HOLE_COLOR, lw=1.8, linestyle='--', zorder=3))
    ax.text(0, 5, f'Ø{ALU_CENTER_HOLE_D}', fontsize=11, ha='center', va='center',
            color=HOLE_COLOR, fontweight='bold')
    ax.text(0, -8, 'CAM RING CLEARANCE', fontsize=7, ha='center', color=HOLE_COLOR)

    # 4× PCD 180 holes at 45° offset (M5 frame mount)
    n = 1
    for i in range(4):
        ang = np.radians(i * 90 + PCD_OFFSET_DEG)
        hx = (PCD_FRAME_MOUNT/2) * np.cos(ang)
        hy = (PCD_FRAME_MOUNT/2) * np.sin(ang)
        draw_hole(ax, hx, hy, 5.5, n=n, fs=7)
        ax.text(hx + 8, hy + 8, f'({hx:+.1f}, {hy:+.1f})', fontsize=6, color='#222')
        n += 1

    # PCD reference circle
    ax.add_patch(Circle((0, 0), PCD_FRAME_MOUNT/2, facecolor='none',
                        edgecolor='#888', lw=0.7, linestyle=':', zorder=2))
    ax.text(0, -PCD_FRAME_MOUNT/2 - 5, f'PCD Ø{PCD_FRAME_MOUNT}',
            fontsize=7, ha='center', color='#888')

    # Overall dimensions
    dim_h(ax, -ALU_W/2, ALU_W/2, -ALU_W/2, '250 mm  (ALU_PLATE_W)', offset_y=20)
    dim_v(ax, -ALU_W/2, ALU_W/2, ALU_W/2, '250 mm  (square)', offset_x=20)
    # Half
    dim_h(ax, -ALU_W/2, 0, ALU_W/2 + 6, '125', offset_y=-10, color=DIM_FAINT, fontsize=6)
    dim_h(ax, 0, ALU_W/2, ALU_W/2 + 6, '125', offset_y=-10, color=DIM_FAINT, fontsize=6)

    ax.set_xlabel('X (mm) — origin at center', fontsize=9)
    ax.set_ylabel('Y (mm) — origin at center', fontsize=9)
    ax.set_title('CSM V3 — ALUMINUM MASTER-DATUM PLATE V1.1 — DRILLING DRAWING\n'
                 '250 × 250 × 6.3 mm (1/4") 6061-T6  •  MASTER DATUM PLANE (top surface)',
                 fontsize=12, fontweight='bold', pad=14)

    # Title block
    tb.set_xlim(0, 1); tb.set_ylim(0, 1); tb.axis('off')
    tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                           facecolor='white', edgecolor='black', lw=1.5))
    rows = [
        ('PROJECT',   'CSM V3 — Circular Sock Machine'),
        ('PART',      'Aluminum Master Datum Plate V1.1'),
        ('SIZE',      '250 × 250 × 6.3 mm  (square, 1/4")'),
        ('MATERIAL',  '6061-T6 aluminum, mill finish'),
        ('FLATNESS',  '< 0.2 mm across full plate (CRITICAL)'),
        ('TOLERANCE', '±0.5 mm (holes), ±1 mm (outline)'),
        ('REV',       'V1.1'),
        ('DATE',      '2026-06-05'),
        ('QTY',       '1 piece'),
        ('STATUS',    'MASTER DATUM — top surface = Z=230'),
    ]
    y = 0.96
    for k, v in rows:
        tb.text(0.06, y, k, fontsize=8, fontweight='bold', color='#444')
        tb.text(0.40, y, v, fontsize=8, color='#111')
        y -= 0.038

    tb.text(0.06, 0.56, 'HOLE LIST', fontsize=10, fontweight='bold')
    tb.text(0.06, 0.53, '#   X         Y       Drill   Use', fontsize=7,
            family='monospace', color='#444', fontweight='bold')
    holes_list = [
        ('1', '+63.64',  '+63.64', 'Ø5.5', 'NE (PCD180 @ 45°)'),
        ('2', '-63.64',  '+63.64', 'Ø5.5', 'NW (PCD180 @ 135°)'),
        ('3', '-63.64',  '-63.64', 'Ø5.5', 'SW (PCD180 @ 225°)'),
        ('4', '+63.64',  '-63.64', 'Ø5.5', 'SE (PCD180 @ 315°)'),
        ('—', '0',       '0',      'Ø170', 'cam ring clearance'),
    ]
    yy = 0.50
    for row in holes_list:
        tb.text(0.06, yy, f'{row[0]:<3s} {row[1]:>7s}  {row[2]:>7s}  {row[3]:>5s}  {row[4]}',
                fontsize=6.5, family='monospace')
        yy -= 0.028

    yy -= 0.01
    tb.plot([0.04, 0.96], [yy, yy], color='black', lw=0.6)
    yy -= 0.02
    tb.text(0.06, yy, 'TOTAL: 5 holes  (4× Ø5.5 + 1× Ø170)',
            fontsize=8, fontweight='bold')

    yy -= 0.045
    tb.text(0.06, yy, 'CRITICAL NOTES', fontsize=10, fontweight='bold', color='#c00')
    yy -= 0.022
    notes = [
        '• FLATNESS < 0.2 mm — this is the master',
        '  datum for the entire cassette stack',
        '• Top surface must NOT be brushed/abraded',
        '  after machining (preserve flatness)',
        '• Center hole can be plunge-milled OR drilled',
        '  + reamed to Ø170 ±0.5',
        '• 4× M5 holes are clearance (no threading)',
        '• Optional: chamfer 0.5×45° all top edges',
        '• Anodizing OK but not required',
    ]
    for n in notes:
        tb.text(0.06, yy, n, fontsize=7, color='#222')
        yy -= 0.020

    plt.tight_layout()
    out_png = os.path.join(FRAME_DIRS['mount_plate'],
                           'CSM_V3_MountPlate6061_V1_1_drilling.png')
    out_pdf = os.path.join(FRAME_DIRS['mount_plate'],
                           'CSM_V3_MountPlate6061_V1_1_drilling.pdf')
    fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  -> {out_png}")
    print(f"  -> {out_pdf}")

    # DXF export
    entities = []
    entities.append(_dxf_rect(0, 0, ALU_W, ALU_W))
    entities.append(_dxf_circle(0, 0, ALU_CENTER_HOLE_D/2))
    for i in range(4):
        ang = np.radians(i * 90 + PCD_OFFSET_DEG)
        hx = (PCD_FRAME_MOUNT/2) * np.cos(ang)
        hy = (PCD_FRAME_MOUNT/2) * np.sin(ang)
        entities.append(_dxf_circle(hx, hy, 5.5/2))
    entities.append(_dxf_text(-ALU_W/2 + 10, ALU_W/2 - 15,
                              'CSM V3 ALU MASTER PLATE V1.1'))
    entities.append(_dxf_text(-ALU_W/2 + 10, ALU_W/2 - 25,
                              'MATERIAL: 6061-T6 Aluminum 6.3mm (1/4 inch)'))
    entities.append(_dxf_text(-ALU_W/2 + 10, ALU_W/2 - 35,
                              'SIZE: 250 x 250 mm  (square)'))
    entities.append(_dxf_text(-ALU_W/2 + 10, ALU_W/2 - 45,
                              'FLATNESS <0.2mm CRITICAL'))
    entities.append(_dxf_text(-ALU_W/2 + 10, ALU_W/2 - 55,
                              'HOLES: 4x Dia 5.5 + 1x Dia 170'))
    out_dxf = os.path.join(FRAME_DIRS['mount_plate'],
                           'CSM_V3_MountPlate6061_V1_1_250x250x6_3.dxf')
    write_dxf(out_dxf, entities)
    print(f"  -> {out_dxf} (CNC-ready)")

# ============================================================
# Also: write DXF for wood base (existing drawing has it as PNG only)
# ============================================================
def write_wood_base_dxf():
    entities = []
    entities.append(_dxf_rect(0, 0, WB_W, WB_D))
    entities.append(_dxf_circle(0, 0, HOLE_D/2))
    # All 21 electrical mount holes
    for h in DRILL_LIST:
        if h['n'] == 0:
            continue
        entities.append(_dxf_circle(h['x'], h['y'], h['d']/2))
    entities.append(_dxf_text(-WB_W/2 + 10, WB_D/2 - 15,
                              'CSM V3 WOOD BASE V1.1'))
    entities.append(_dxf_text(-WB_W/2 + 10, WB_D/2 - 25,
                              'MATERIAL: Hardwood Plywood 18mm'))
    entities.append(_dxf_text(-WB_W/2 + 10, WB_D/2 - 35,
                              'SIZE: 500 x 400 mm'))
    entities.append(_dxf_text(-WB_W/2 + 10, WB_D/2 - 45,
                              'HOLES: 21 electrical + 1x Dia 100 take-down'))
    out_dxf = os.path.join(FRAME_DIRS['wood_base'],
                           'CSM_V3_WoodBase_V1_1_500x400x18.dxf')
    write_dxf(out_dxf, entities)
    print(f"  -> {out_dxf} (CNC-ready)")

# ============================================================
# STEP file generation (3D solid models with thickness embedded)
# ============================================================
def _make_wood_base_solid():
    """500 × 400 × 18 slab with take-down hole + all 21 electronics holes."""
    t = MD.WOOD_BASE_T
    slab = Part.makeBox(MD.WOOD_BASE_W, MD.WOOD_BASE_D, t,
                        FreeCAD.Vector(-MD.WOOD_BASE_W/2, -MD.WOOD_BASE_D/2, 0))
    # Take-down hole
    td = Part.makeCylinder(MD.TAKEDOWN_HOLE_D/2.0, t + 2.0,
                            FreeCAD.Vector(0, 0, -1.0))
    shape = slab.cut(td)
    # All 21 electronics mounting holes
    for h in DRILL_LIST:
        if h['n'] == 0:
            continue
        eh = Part.makeCylinder(h['d']/2.0, t + 2.0,
                                FreeCAD.Vector(h['x'], h['y'], -1.0))
        shape = shape.cut(eh)
    return shape

def _make_wood_upper_deck_solid():
    """320 × 260 × 18 slab with Ø170 center + 4 upright + 4 PCD-180 holes."""
    t = MD.UPPER_DECK_T
    slab = Part.makeBox(UD_W, UD_D, t,
                        FreeCAD.Vector(-UD_W/2, -UD_D/2, 0))
    # Center hole
    center = Part.makeCylinder(UD_CENTER_HOLE_D/2.0, t + 2.0,
                                FreeCAD.Vector(0, 0, -1.0))
    shape = slab.cut(center)
    # 4× corner holes for uprights
    for sx in (+150, -150):
        for sy in (+120, -120):
            h = Part.makeCylinder(5.5/2.0, t + 2.0,
                                   FreeCAD.Vector(sx, sy, -1.0))
            shape = shape.cut(h)
    # 4× PCD 180 holes at 45°
    for i in range(4):
        ang = np.radians(i * 90 + PCD_OFFSET_DEG)
        hx = (PCD_FRAME_MOUNT/2.0) * np.cos(ang)
        hy = (PCD_FRAME_MOUNT/2.0) * np.sin(ang)
        h = Part.makeCylinder(5.5/2.0, t + 2.0,
                               FreeCAD.Vector(hx, hy, -1.0))
        shape = shape.cut(h)
    return shape

def _make_alu_plate_solid():
    """250 × 250 × 6 plate with Ø170 center + 4 PCD-180 holes."""
    t = MD.ALU_PLATE_T
    slab = Part.makeBox(ALU_W, ALU_W, t,
                        FreeCAD.Vector(-ALU_W/2, -ALU_W/2, 0))
    center = Part.makeCylinder(ALU_CENTER_HOLE_D/2.0, t + 2.0,
                                FreeCAD.Vector(0, 0, -1.0))
    shape = slab.cut(center)
    for i in range(4):
        ang = np.radians(i * 90 + PCD_OFFSET_DEG)
        hx = (PCD_FRAME_MOUNT/2.0) * np.cos(ang)
        hy = (PCD_FRAME_MOUNT/2.0) * np.sin(ang)
        h = Part.makeCylinder(5.5/2.0, t + 2.0,
                               FreeCAD.Vector(hx, hy, -1.0))
        shape = shape.cut(h)
    return shape

def generate_step_files():
    """Export STEP (3D) for the three CNC frame parts."""
    if not HAS_FREECAD or MD is None:
        print("STEP export skipped (FreeCAD or machine_datums missing).")
        return
    doc = FreeCAD.newDocument("FrameStepExport")
    parts = [
        ('WoodBase',       _make_wood_base_solid,
         FRAME_DIRS['wood_base'],
         f'CSM_V3_WoodBase_V1_1_500x400x{int(MD.WOOD_BASE_T)}.step'),
        ('WoodUpperDeck',  _make_wood_upper_deck_solid,
         FRAME_DIRS['wood_upper_deck'],
         f'CSM_V3_WoodUpperDeck_V1_0_320x260x{int(MD.UPPER_DECK_T)}.step'),
        ('AluPlate',       _make_alu_plate_solid,
         FRAME_DIRS['mount_plate'],
         f'CSM_V3_MountPlate6061_V1_1_250x250x{str(MD.ALU_PLATE_T).replace(".", "_")}.step'),
    ]
    for name, builder, folder, filename in parts:
        try:
            obj = doc.addObject("Part::Feature", name)
            obj.Shape = builder()
            out = os.path.join(folder, filename)
            Part.export([obj], out)
            print(f"  -> {out} (3D STEP, thickness embedded)")
        except Exception as e:
            print(f"  STEP FAILED for {name}: {e}")
    FreeCAD.closeDocument("FrameStepExport")

# ============================================================
if __name__ == '__main__':
    print("=" * 70)
    print("CSM V3 -- Generating drilling drawings (V1.2)")
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
    print("Sheet 5: Hardware Order Sheet (A4 printable)")
    draw_hardware_order_sheet()
    print()
    print("Sheet 6: Assembly Procedure (A4 printable)")
    draw_assembly_procedure()
    print()
    print("Sheet 7: Bench-Test Checklist (A4 printable)")
    draw_bench_test_checklist()
    print()
    print("Sheet 8: Wood Upper Deck Drilling (+DXF)")
    draw_wood_upper_deck()
    print()
    print("Sheet 9: Aluminum Master-Datum Plate Drilling (+DXF)")
    draw_aluminum_plate()
    print()
    print("Sheet 10: Wood Base DXF (companion to existing drawing)")
    write_wood_base_dxf()
    print()
    print("=" * 70)
    print("STEP FILES (3D solid models with thickness embedded)")
    print("=" * 70)
    generate_step_files()
    print()
    print("=" * 70)
    print("Done. PDFs are vector. DXFs are 2D CNC paths. STEPs are 3D solids.")
    print("Send shop:  *.step (verification + thickness) + *.dxf (cut path)")
    print("=" * 70)
