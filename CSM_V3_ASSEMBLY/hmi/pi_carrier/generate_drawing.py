# -*- coding: utf-8 -*-
"""
CSM V3 -- HMI Module 10 -- Pi Carrier V1.0 Drawing Generator
=============================================================
Multi-view engineering drawing.
"""
import os, struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
STL_PATH = os.path.join(HERE, "CSM_V3_PiCarrier_V1_0.stl")

PLATE_W   = 90.0
PLATE_D   = 60.0
PLATE_T   = 8.0
BEAM_PCD_X = 58.0
BEAM_PCD_Y = 28.0
PI_PCD_X  = 58.0
PI_PCD_Y  = 49.0
M5_D      = 5.5
BOLT_CB_D = 9.5
BOLT_CB_H = 5.5
M2_5_D    = 2.0
M2_5_H    = 6.0
NOTCH_W   = 14.0
NOTCH_D   = 6.0

def parse_stl(path):
    with open(path, 'rb') as f:
        head = f.read(5)
    if head == b'solid':
        return parse_ascii_stl(path)
    return parse_binary_stl(path)

def parse_ascii_stl(path):
    tris, cur = [], []
    with open(path, 'r') as f:
        for line in f:
            s = line.strip().lower()
            if s.startswith('vertex '):
                p = s.split()
                cur.append((float(p[1]), float(p[2]), float(p[3])))
                if len(cur) == 3:
                    tris.append(cur); cur = []
    return np.array(tris, dtype=np.float32)

def parse_binary_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        tris = np.zeros((n, 3, 3), dtype=np.float32)
        for i in range(n):
            f.read(12)
            for j in range(3):
                tris[i, j] = struct.unpack('<3f', f.read(12))
            f.read(2)
    return tris

print(f"Loading STL: {STL_PATH}")
triangles = parse_stl(STL_PATH)
print(f"  {len(triangles)} triangles")

all_pts = triangles.reshape(-1, 3)
xmin, ymin, zmin = all_pts.min(axis=0)
xmax, ymax, zmax = all_pts.max(axis=0)

fig = plt.figure(figsize=(16, 12), dpi=180)
fig.suptitle('CSM V3 -- HMI Module 10 -- Pi Carrier V1.0',
             fontsize=16, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, 'Adapter plate: Cross Beam (58 x 28) -> Raspberry Pi 4 (58 x 49)',
         ha='center', fontsize=10, color='#444', style='italic')

def setup_3d(ax, elev, azim, title):
    ax.add_collection3d(Poly3DCollection(triangles,
                                          facecolor='#5a7aaa',
                                          edgecolor='#1a2a4a',
                                          linewidth=0.10, alpha=0.92))
    ax.set_xlim(xmin - 2, xmax + 2)
    ax.set_ylim(ymin - 2, ymax + 2)
    ax.set_zlim(zmin - 2, zmax + 2)
    ax.view_init(elev=elev, azim=azim)
    ax.set_proj_type('ortho')
    ax.set_title(title, fontweight='bold', pad=10)
    ax.tick_params(labelsize=7)

ax_iso = fig.add_subplot(2, 3, 1, projection='3d')
setup_3d(ax_iso, 25, -58, 'Isometric View')
ax_iso.set_box_aspect((PLATE_W, PLATE_D, PLATE_T * 4))
ax_iso.set_xlabel('X', fontsize=8); ax_iso.set_ylabel('Y', fontsize=8); ax_iso.set_zlabel('Z', fontsize=8)

ax_top = fig.add_subplot(2, 3, 2, projection='3d')
setup_3d(ax_top, 89.9, -90, 'Top View (mates beam bottom)')
ax_top.set_box_aspect((PLATE_W, PLATE_D, 1))
ax_top.set_xlabel('X', fontsize=8); ax_top.set_ylabel('Y', fontsize=8); ax_top.set_zticks([])

ax_bot = fig.add_subplot(2, 3, 4, projection='3d')
setup_3d(ax_bot, -89.9, -90, 'Bottom View (4x M5 CB + 4x M2.5 + notch)')
ax_bot.set_box_aspect((PLATE_W, PLATE_D, 1))
ax_bot.set_xlabel('X', fontsize=8); ax_bot.set_ylabel('Y', fontsize=8); ax_bot.set_zticks([])

ax_side = fig.add_subplot(2, 3, 5, projection='3d')
setup_3d(ax_side, 0, 0, 'Side View (+X) -- counterbore depth')
ax_side.set_box_aspect((1, PLATE_D, PLATE_T * 2))
ax_side.set_ylabel('Y', fontsize=8); ax_side.set_zlabel('Z', fontsize=8); ax_side.set_xticks([])

ax_tb = fig.add_subplot(2, 3, 3)
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis('off')
ax_tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                            facecolor='white', edgecolor='black', lw=1.5))
rows = [
    ('PART',     'Pi Carrier'),
    ('NUMBER',   'M10-P03'),
    ('VERSION',  'V1.0 (RC1)'),
    ('MODULE',   '10 -- HMI'),
    ('QTY',      '1'),
    ('MATERIAL', 'PETG (PA12 prod)'),
    ('INFILL',   '100%, 4 walls'),
    ('LAYER',    '0.2 mm'),
    ('MASS',     '~52 g'),
    ('PRINT',    'flat, ~2 h'),
]
y = 0.95
for k, v in rows:
    ax_tb.text(0.06, y, k, fontsize=8.5, fontweight='bold', color='#444')
    ax_tb.text(0.42, y, v, fontsize=8.5, color='#111')
    y -= 0.045

ax_tb.text(0.06, 0.50, 'DIMENSIONS (mm)', fontsize=10, fontweight='bold')
dims = [
    ('Plate',         f'{PLATE_W} x {PLATE_D} x {PLATE_T}'),
    ('Beam PCD',      f'{BEAM_PCD_X} x {BEAM_PCD_Y} (4x M5)'),
    ('Beam bolt CB',  f'{BOLT_CB_D} x {BOLT_CB_H} on bottom'),
    ('Pi 4 PCD',      f'{PI_PCD_X} x {PI_PCD_Y} (4x M2.5)'),
    ('Pi pilot',      f'D{M2_5_D} x {M2_5_H} (self-tap)'),
    ('Cable notch',   f'{NOTCH_W} x {NOTCH_D} on -Y edge'),
]
yy = 0.46
for k, v in dims:
    ax_tb.text(0.06, yy, k, fontsize=7.5, color='#444', family='monospace')
    ax_tb.text(0.52, yy, v, fontsize=7.5, color='#111', family='monospace')
    yy -= 0.030

ax_notes = fig.add_subplot(2, 3, 6)
ax_notes.set_xlim(0, 1); ax_notes.set_ylim(0, 1); ax_notes.axis('off')
ax_notes.text(0.02, 0.95, 'ASSEMBLY', fontsize=10, fontweight='bold')
notes = [
    '1. Print PETG flat on bed, BOTTOM face down',
    '   100% infill, 4 walls, 0.2 mm layers',
    '2. Heat / press 4x M2.5 standoffs (~10 mm) into',
    '   pilot holes on BOTTOM face (Pi PCD 58 x 49)',
    '3. Mount Raspberry Pi 4 to standoff bottoms',
    '   with M2.5 x 6 mm screws through Pi mount holes',
    '4. Position Pi+carrier assembly below Cross Beam',
    '   bottom face; align with beam Pi inserts',
    '5. M5 x 16 socket-head bolts go UP from carrier',
    '   BOTTOM counterbores into beam BOTTOM inserts',
    '6. Tighten gently -- snug, do not crush plate',
    '',
    'INTERFACE CONTRACT (locked):',
    '  Beam PCD 58 x 28 -- HMI_PI_MOUNT_PCD_*',
    '  Pi 4 PCD 58 x 49 -- HMI_PI4_PCD_*',
    '',
    'WALL CHECK (all OK):',
    '  edge to beam bolt  11.25 mm',
    '  edge to Pi hole     4.50 mm',
    '  beam to Pi hole     4.75 mm',
    '  cover over CB       2.50 mm',
]
yy = 0.91
for n in notes:
    ax_notes.text(0.02, yy, n, fontsize=7.3, color='#222', family='sans-serif')
    yy -= 0.038

fig.text(0.5, 0.02,
         'github.com/leoalex196912/ChatGistory  *  '
         'CSM_V3_ASSEMBLY/hmi/pi_carrier/  *  '
         'Module 10 part 3 of 10',
         ha='center', fontsize=8, color='#888')

out_png = os.path.join(HERE, "CSM_V3_PiCarrier_V1_0_views.png")
out_pdf = os.path.join(HERE, "CSM_V3_PiCarrier_V1_0_views.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
