# -*- coding: utf-8 -*-
"""
CSM V3 — Complete Machine Engineering Illustration
====================================================
Isometric cover-page drawing showing the entire 14-module machine
with correct proportions from machine_datums.py.

Output:
  CSM_V3_MACHINE_OVERVIEW.png  (high-DPI cover image)
  CSM_V3_MACHINE_OVERVIEW.pdf  (vector for print)

Run:
  "C:/Program Files/FreeCAD 1.1/bin/python.exe" generate_machine_overview.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import machine_datums as MD

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# Colors (engineering illustration palette)
WOOD       = '#c8a878'
WOOD_DARK  = '#8c6a3f'
ALU        = '#c8ccd2'
ALU_DARK   = '#6a6e74'
STEEL      = '#888c92'
PETG_BLUE  = '#4a6a9a'
PETG_DARK  = '#2a3a5a'
CYL_GRAY   = '#a8a8b0'
CYL_DARK   = '#4a4a52'
MOTOR_DK   = '#3a3a40'
BELT_BK    = '#1a1a1a'
HOOK_LAV   = '#9990c0'
SCREEN_BK  = '#1a1a1a'
SCREEN_PX  = '#2a4a8a'
PSU_GRAY   = '#909296'
PCB_BLUE   = '#1f4ea8'
PCB_GREEN  = '#0c6e3a'
RED        = '#c43838'
YARN_COLORS = ['#c44', '#4c4', '#44c', '#cc4', '#c4c', '#4cc']

# ============================================================
# Helpers — draw 3D primitives
# ============================================================
def cylinder_mesh(cx, cy, z0, r, h, n_theta=48):
    th = np.linspace(0, 2*np.pi, n_theta + 1)
    x_bot = cx + r * np.cos(th); y_bot = cy + r * np.sin(th); z_bot = np.full_like(th, z0)
    x_top = x_bot; y_top = y_bot; z_top = np.full_like(th, z0 + h)
    return x_bot, y_bot, z_bot, x_top, y_top, z_top

def draw_cylinder(ax, cx, cy, z0, r, h, face_color, edge_color='k', n=48,
                  alpha=1.0, lw=0.5):
    th = np.linspace(0, 2*np.pi, n + 1)
    # Side surface
    x = cx + r * np.cos(th); y = cy + r * np.sin(th)
    verts_side = []
    for i in range(n):
        verts_side.append([
            (x[i], y[i], z0), (x[i+1], y[i+1], z0),
            (x[i+1], y[i+1], z0 + h), (x[i], y[i], z0 + h)
        ])
    side = Poly3DCollection(verts_side, facecolors=face_color,
                            edgecolors=edge_color, linewidths=lw, alpha=alpha)
    ax.add_collection3d(side)
    # Top and bottom rings
    top = list(zip(x, y, np.full_like(x, z0 + h)))
    bot = list(zip(x, y, np.full_like(x, z0)))
    ring_top = Poly3DCollection([top], facecolors=face_color,
                                 edgecolors=edge_color, linewidths=lw, alpha=alpha)
    ring_bot = Poly3DCollection([bot], facecolors=face_color,
                                 edgecolors=edge_color, linewidths=lw, alpha=alpha)
    ax.add_collection3d(ring_top)
    ax.add_collection3d(ring_bot)

def draw_hollow_cyl(ax, cx, cy, z0, r_out, r_in, h, color, edge='k', alpha=1.0, n=48):
    draw_cylinder(ax, cx, cy, z0, r_out, h, color, edge, n=n, alpha=alpha)
    # Inner hole shadow (just visible as a darker ring on top)
    th = np.linspace(0, 2*np.pi, n + 1)
    x = cx + r_in * np.cos(th); y = cy + r_in * np.sin(th)
    inner_top = list(zip(x, y, np.full_like(x, z0 + h)))
    ax.add_collection3d(Poly3DCollection([inner_top], facecolors='#222',
                                          edgecolors=edge, linewidths=0.4, alpha=alpha))

def draw_box(ax, x0, y0, z0, w, d, h, face_color, edge_color='k', alpha=1.0, lw=0.5):
    """Box from (x0,y0,z0) extending +w,+d,+h."""
    x1, y1, z1 = x0 + w, y0 + d, z0 + h
    verts = [
        # bottom
        [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],
        # top
        [(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],
        # sides
        [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],
        [(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],
        [(x1,y1,z0),(x0,y1,z0),(x0,y1,z1),(x1,y1,z1)],
        [(x0,y1,z0),(x0,y0,z0),(x0,y0,z1),(x0,y1,z1)],
    ]
    ax.add_collection3d(Poly3DCollection(verts, facecolors=face_color,
                                          edgecolors=edge_color, linewidths=lw,
                                          alpha=alpha))

# ============================================================
# Setup figure (isometric orthographic projection)
# ============================================================
fig = plt.figure(figsize=(20, 14), dpi=180)
ax = fig.add_subplot(111, projection='3d')
ax.set_proj_type('ortho')
ax.view_init(elev=12, azim=-58)
ax.set_box_aspect((1.1, 1.1, 1.4))

# Hide axis grid + ticks for clean illustration
ax.set_axis_off()
ax.set_xlim(-260, 260)
ax.set_ylim(-260, 260)
ax.set_zlim(-50, 650)

# ============================================================
# DRAW MACHINE (bottom-up)
# ============================================================
# --- Wood base ---
draw_box(ax, -MD.WOOD_BASE_W/2, -MD.WOOD_BASE_D/2, MD.WOOD_BASE_BOTTOM_Z,
         MD.WOOD_BASE_W, MD.WOOD_BASE_D, MD.WOOD_BASE_T,
         WOOD, WOOD_DARK, lw=0.6)
# Take-down hole on top face (just a darker circle)
th = np.linspace(0, 2*np.pi, 49)
x_hole = (MD.TAKEDOWN_HOLE_D/2) * np.cos(th)
y_hole = (MD.TAKEDOWN_HOLE_D/2) * np.sin(th)
hole_top = list(zip(x_hole, y_hole, np.full_like(x_hole, MD.WOOD_BASE_TOP_Z + 0.1)))
ax.add_collection3d(Poly3DCollection([hole_top], facecolors='#3a2a1a',
                                       edgecolors=WOOD_DARK, linewidths=0.4))

# --- PSU on left side ---
psu_x, psu_y = -195, 0
draw_box(ax, psu_x - 110/2, psu_y - 199/2, MD.WOOD_BASE_TOP_Z,
         110, 199, 50, PSU_GRAY, ALU_DARK, lw=0.5)

# --- Mega 2560 on right side ---
draw_box(ax, 200 - 102/2, 75 - 54/2, MD.WOOD_BASE_TOP_Z + 8,
         102, 54, 12, PCB_BLUE, 'k', lw=0.4)

# --- TB6600 driver ---
draw_box(ax, 200 - 96/2, -47 - 56/2, MD.WOOD_BASE_TOP_Z,
         96, 56, 37, RED, '#660000', lw=0.5)

# --- 2x LM2596 bucks on back strip ---
for bx in (-50, 50):
    draw_box(ax, bx - 43/2, 160 - 21/2, MD.WOOD_BASE_TOP_Z + 4,
             43, 21, 10, PCB_GREEN, 'k', lw=0.4)

# --- 4 precision uprights ---
for sx in MD.UPRIGHT_X_POSITIONS:
    for sy in MD.UPRIGHT_Y_POSITIONS:
        draw_box(ax, sx - MD.UPRIGHT_W/2, sy - MD.UPRIGHT_W/2,
                 MD.UPRIGHT_BOT_Z, MD.UPRIGHT_W, MD.UPRIGHT_W, MD.UPRIGHT_LEN,
                 ALU, ALU_DARK, lw=0.5)

# --- Wood upper deck ---
draw_box(ax, -MD.UPPER_DECK_W/2, -MD.UPPER_DECK_D/2, MD.UPPER_DECK_BOTTOM_Z,
         MD.UPPER_DECK_W, MD.UPPER_DECK_D, MD.UPPER_DECK_T,
         WOOD, WOOD_DARK, lw=0.6)
# Center hole indication
x_uh = 85 * np.cos(th); y_uh = 85 * np.sin(th)
uh_top = list(zip(x_uh, y_uh, np.full_like(x_uh, MD.UPPER_DECK_TOP_Z + 0.1)))
ax.add_collection3d(Poly3DCollection([uh_top], facecolors='#2a1a0a',
                                       edgecolors=WOOD_DARK, linewidths=0.4))

# --- Aluminum master plate ---
draw_box(ax, -MD.ALU_PLATE_W/2, -MD.ALU_PLATE_W/2, MD.ALU_PLATE_BOTTOM_Z,
         MD.ALU_PLATE_W, MD.ALU_PLATE_W, MD.ALU_PLATE_T,
         ALU, ALU_DARK, lw=0.6)
# Center hole
x_ah = 85 * np.cos(th); y_ah = 85 * np.sin(th)
ah_top = list(zip(x_ah, y_ah, np.full_like(x_ah, MD.ALU_PLATE_TOP_Z + 0.1)))
ax.add_collection3d(Poly3DCollection([ah_top], facecolors='#1a1a1a',
                                       edgecolors='k', linewidths=0.4))

# --- Cassette stack starts at master datum Z=230 ---
Z = MD.ALU_PLATE_TOP_Z

# --- Cassette base + retainer ring (Ø200) ---
draw_hollow_cyl(ax, 0, 0, Z, 200/2, 88/2, 14, PETG_DARK, 'k', n=64)
Z += 14

# --- Drive hub flange under cassette base (in the take-down column / motor zone) ---
# Showing motor tower underneath
MOT_Z = MD.WOOD_BASE_TOP_Z
draw_hollow_cyl(ax, 85, -47, MOT_Z, 40/2, 0/2, 50, ALU_DARK, 'k', n=32)  # gearbox
draw_box(ax, 85 - 57/2, -47 - 57/2, MOT_Z + 50,
         57, 57, 56, MOTOR_DK, 'k', lw=0.5)  # motor body

# --- Sinker ring (Ø135) - thin ring above cassette base ---
draw_hollow_cyl(ax, 0, 0, Z, 135/2, 115/2, 4, PETG_BLUE, 'k', n=64)
Z += 4

# --- Cam Ring V6.5 (Ø165) — encircles cylinder ---
CYL_Z_BOT = Z   # cylinder bottom at world Z (~248)
draw_hollow_cyl(ax, 0, 0, Z, 165/2, 117/2, 20, PETG_BLUE, 'k', n=64, alpha=0.85)

# --- CYLINDER V3.1 — the heart of the machine ---
# Ø114.30 × 75 mm, 72 slots, spring groove at z=55 local
draw_hollow_cyl(ax, 0, 0, CYL_Z_BOT, MD.CYL_OD/2, MD.CYL_ID/2,
                MD.CYL_HEIGHT, CYL_GRAY, 'k', n=72, alpha=0.95)

# Add the 72 slot lines (vertical grooves on cylinder surface)
slot_n = 72
for i in range(slot_n):
    ang = 2*np.pi*i/slot_n
    sx = (MD.CYL_OD/2 + 0.05) * np.cos(ang)
    sy = (MD.CYL_OD/2 + 0.05) * np.sin(ang)
    # Only draw front-facing slots for clarity (z-buffer handles back)
    ax.plot([sx, sx], [sy, sy], [CYL_Z_BOT + 3, CYL_Z_BOT + MD.CYL_HEIGHT - 3],
            color=CYL_DARK, linewidth=0.4, alpha=0.7)

# Spring groove — horizontal band at z_local=55 (i.e., world Z = CYL_Z_BOT + 55)
SG_Z = CYL_Z_BOT + MD.SPRING_GROOVE_Z_CTR
draw_hollow_cyl(ax, 0, 0, SG_Z - MD.SPRING_GROOVE_W/2,
                MD.CYL_OD/2 + 0.1, MD.CYL_OD/2 - MD.SPRING_GROOVE_DEPTH,
                MD.SPRING_GROOVE_W, '#2a2a30', '#1a1a1a', n=72, alpha=0.9)

CYL_Z_TOP = CYL_Z_BOT + MD.CYL_HEIGHT

# --- Retainer ring (Ø200) on top of cylinder ---
draw_hollow_cyl(ax, 0, 0, CYL_Z_TOP + 4, 200/2, 88/2, 6,
                 PETG_BLUE, 'k', n=64, alpha=0.85)

# --- 6 feeder modules around cassette at PCD 190 ---
for i in range(6):
    ang = 2*np.pi*i/6
    fx = 95 * np.cos(ang) + 8*np.cos(ang)
    fy = 95 * np.sin(ang) + 8*np.sin(ang)
    # Base plate
    draw_box(ax, fx - 95/2, fy - 35, Z - 5,
             95, 70, 6, PETG_DARK, 'k', lw=0.4, alpha=0.85)
    # Vertical post (cone post)
    draw_cylinder(ax, fx + 8*np.cos(ang+np.pi/2), fy + 8*np.sin(ang+np.pi/2),
                  Z + 1, 7, 90, PETG_DARK, 'k', n=16, alpha=0.85)

# --- Take-down assembly visualization (hook hanging through Ø100) ---
TD_TOP = MD.WOOD_BASE_BOTTOM_Z + MD.WOOD_BASE_T - 5
draw_hollow_cyl(ax, 0, 0, TD_TOP, 75/2, 57/2, 6.5,
                HOOK_LAV, '#554a80', n=48, alpha=0.9)
# Cord descending through hole
ax.plot([0, 0], [0, 0], [TD_TOP, TD_TOP - 80], color='k', linewidth=0.8)

# --- Yarn cones above feeders (6 cones above the machine, smaller + higher) ---
for i in range(6):
    ang = 2*np.pi*i/6 + np.pi/6
    cx = 150 * np.cos(ang); cy = 150 * np.sin(ang)
    cone_z = 500
    # Tapered cone
    n_th = 24
    th_c = np.linspace(0, 2*np.pi, n_th + 1)
    x_bot_c = cx + 22 * np.cos(th_c); y_bot_c = cy + 22 * np.sin(th_c)
    x_top_c = cx + 9 * np.cos(th_c); y_top_c = cy + 9 * np.sin(th_c)
    side_v = []
    for k in range(n_th):
        side_v.append([
            (x_bot_c[k], y_bot_c[k], cone_z),
            (x_bot_c[k+1], y_bot_c[k+1], cone_z),
            (x_top_c[k+1], y_top_c[k+1], cone_z + 70),
            (x_top_c[k], y_top_c[k], cone_z + 70),
        ])
    ax.add_collection3d(Poly3DCollection(side_v,
                        facecolors=YARN_COLORS[i % len(YARN_COLORS)],
                        edgecolors='#222', linewidths=0.3, alpha=0.85))
    # yarn line going down toward feeder
    target_ang = 2*np.pi*i/6
    fx = 95 * np.cos(target_ang); fy = 95 * np.sin(target_ang)
    ax.plot([cx, fx], [cy, fy], [cone_z, Z + 40],
            color=YARN_COLORS[i % len(YARN_COLORS)], linewidth=0.5, alpha=0.55)

# --- HMI Module 10 — dual 2020 mast at (X=±75, Y=-210) ---
MAST_H = 400.0
for mx in (-75, +75):
    draw_box(ax, mx - 10, -210 - 10, MD.WOOD_BASE_TOP_Z,
             20, 20, MAST_H, ALU, ALU_DARK, lw=0.5)

# --- Touchscreen + Pi at top of mast ---
SCREEN_Z = MD.WOOD_BASE_TOP_Z + MAST_H - 20
draw_box(ax, -90, -220, SCREEN_Z, 180, 8, 110, SCREEN_BK, 'k', lw=0.5)
# Active pixel area
draw_box(ax, -77, -218, SCREEN_Z + 8, 154, 0.5, 90, SCREEN_PX, '#222', lw=0.3)

# --- Front operator panel (vertical at -Y edge of wood base) ---
draw_box(ax, -100, -MD.WOOD_BASE_D/2 - 3, MD.WOOD_BASE_TOP_Z,
         200, 3, 60, '#dadde0', 'k', lw=0.5)
# E-stop button (red dot)
es_x, es_z = 20, MD.WOOD_BASE_TOP_Z + 30
ax.scatter([es_x], [-MD.WOOD_BASE_D/2 - 8], [es_z], s=200, c=RED,
           edgecolors='k', linewidths=0.8, alpha=0.95, depthshade=False)

# ============================================================
# LABELS (in 2D figure coords for clean leader lines)
# ============================================================
fig.text(0.5, 0.96, 'CSM V3 — CIRCULAR SOCK MACHINE',
         ha='center', fontsize=22, fontweight='bold', color='#222')
fig.text(0.5, 0.93, 'Complete Machine Architecture — Engineering Overview',
         ha='center', fontsize=12, color='#555', style='italic')
fig.text(0.5, 0.91, '14 Modules • Layer 1 Precision • Layer 2 Structural • Layer 3 Automation',
         ha='center', fontsize=9, color='#666')

# Module callouts as figure text with leader lines is complex in 3D;
# use simple annotations along the right side
label_x = 0.78
label_y_start = 0.85
label_step = 0.034
modules = [
    ("Module 1",  "72-slot Knitting Cylinder V3.1"),
    ("Module 2",  "Cam Ring V6.5"),
    ("Module 3",  "Sinker Ring V1.2.1"),
    ("Module 4",  "Cassette Base + Retainer + 6× Spacers"),
    ("Module 5",  "6× Feeder Assembly (servo-driven, ceramic pigtails)"),
    ("Module 6",  "Drive — NEMA 23 + HG5 5:1 gearbox + HTD belt"),
    ("Module 7",  "Bearing & Shaft Stack — floating-top / fixed-bottom"),
    ("Module 8",  "Take-Down — Phase 1 hook / Phase 2 dual roller"),
    ("Module 9",  "Frame — wood base 500×400×12 + 4× 2020 + Ø250 plate"),
    ("Module 10", "HMI — dual 2020 mast + 7\" touchscreen + Pi 4"),
    ("Module 11", "Electronics — S-250-24 PSU + Mega + 2× LM2596 + TB6600"),
    ("Module 12", "Operator Panel — E-stop + AC inlet + fuse"),
    ("Module 13", "Ribber Disk — provisioned for Phase 2"),
    ("Module 14", "Yarn Path — 6 cones + ceramic pigtails"),
]
for i, (mid, name) in enumerate(modules):
    y = label_y_start - i * label_step
    fig.text(label_x, y, mid, fontsize=8.5, fontweight='bold',
             color=PCB_BLUE, family='monospace')
    fig.text(label_x + 0.06, y, name, fontsize=8.5, color='#222')

# Master datum callout
fig.text(0.03, 0.85, 'MASTER DATUM\nZ = 230 mm', fontsize=8.5,
         fontweight='bold', color='#c00000', family='monospace')
fig.text(0.03, 0.82, '(Top of aluminum plate,\nICD R7 invariant B3)',
         fontsize=7.5, color='#666', style='italic')

# Layer color key
fig.text(0.03, 0.74, 'LAYER KEY', fontsize=9, fontweight='bold')
fig.text(0.03, 0.715, 'Wood (Baltic Birch 12 mm)', fontsize=8, color=WOOD_DARK)
fig.text(0.03, 0.695, '6061-T6 Aluminum (plate + 2020)', fontsize=8, color=ALU_DARK)
fig.text(0.03, 0.675, 'PETG printed (Phase 1)', fontsize=8, color=PETG_BLUE)
fig.text(0.03, 0.655, 'Steel / motor', fontsize=8, color=MOTOR_DK)
fig.text(0.03, 0.635, 'Electronics PCB', fontsize=8, color=PCB_GREEN)

# Title block (bottom)
fig.text(0.5, 0.04, 'leoalex196912/ChatGistory  •  CSM_V3  •  '
                    '14 Modules  •  Layered Architecture',
         ha='center', fontsize=8, color='#888')
fig.text(0.5, 0.025, 'Master Datum Z=230 (aluminum plate top)  •  '
                     'Origin XY at machine center',
         ha='center', fontsize=7, color='#888', style='italic')

# Save
out_png = os.path.join(OUTDIR, 'CSM_V3_MACHINE_OVERVIEW.png')
out_pdf = os.path.join(OUTDIR, 'CSM_V3_MACHINE_OVERVIEW.pdf')
fig.savefig(out_png, dpi=200, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
