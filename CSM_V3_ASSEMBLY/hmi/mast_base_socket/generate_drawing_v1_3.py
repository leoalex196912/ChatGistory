# -*- coding: utf-8 -*-
"""
CSM V3 -- HMI Module 10 -- Mast Base Socket V1.3 Drawing Generator
==================================================================
Multi-view engineering drawing for the V1.3 STL.

Output:
  CSM_V3_MastBaseSocket_V1_3_views.png
  CSM_V3_MastBaseSocket_V1_3_views.pdf

Run with FreeCAD's Python:
  "C:/Program Files/FreeCAD 1.1/bin/python.exe" generate_drawing_v1_2.py
"""
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
STL_PATH = os.path.join(HERE, "CSM_V3_MastBaseSocket_V1_3.stl")

# V1.3 parameters
SOCKET_OUTER = 34.0
SOCKET_H     = 50.0
POCKET_W     = 20.8
POCKET_R     = 1.5
WALL_T       = 6.6
FOOT_LEN     = 70.0
FOOT_W       = 54.0
FOOT_T       = 10.0
BOLT_CB_D    = 9.5
BOLT_CB_H    = 5.5
GUSSET_B     = 25.0
GUSSET_R     = 30.0
RIB_T        = 3.0
RIB_H        = 6.0
CABLE_CH_W   = 8.0
CABLE_CH_D   = 4.0
INSERT_D     = 6.2
INSERT_H     = 8.5
EXP_COUNT    = 4
EXP_PITCH    = 20.0

def parse_stl(path):
    with open(path, 'rb') as f:
        head = f.read(5)
    if head == b'solid':
        return parse_ascii_stl(path)
    return parse_binary_stl(path)

def parse_ascii_stl(path):
    tris = []
    cur = []
    with open(path, 'r') as f:
        for line in f:
            s = line.strip().lower()
            if s.startswith('vertex '):
                parts = s.split()
                cur.append((float(parts[1]), float(parts[2]), float(parts[3])))
                if len(cur) == 3:
                    tris.append(cur); cur = []
    return np.array(tris, dtype=np.float32)

def parse_binary_stl(path):
    with open(path, 'rb') as f:
        f.read(80)
        n_tri = struct.unpack('<I', f.read(4))[0]
        tris = np.zeros((n_tri, 3, 3), dtype=np.float32)
        for i in range(n_tri):
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
fig.suptitle('CSM V3 -- HMI Module 10 -- Mast Base Socket V1.3',
             fontsize=16, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, 'FREEZE candidate: lead-in chamfer, drain hole, 4 diagonal ribs, '
                    'FRONT boss for inserts, wall-check verified',
         ha='center', fontsize=10, color='#444', style='italic')

def setup_3d(ax, elev, azim, title):
    ax.add_collection3d(Poly3DCollection(triangles,
                                          facecolor='#4a6a9a',
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
setup_3d(ax_iso, 22, -58, 'Isometric View')
ax_iso.set_box_aspect((1, 1, 1))
ax_iso.set_xlabel('X', fontsize=8); ax_iso.set_ylabel('Y', fontsize=8); ax_iso.set_zlabel('Z', fontsize=8)

ax_top = fig.add_subplot(2, 3, 2, projection='3d')
setup_3d(ax_top, 89.9, -90, 'Top View (X-Y) -- ribs + bolt counterbores')
ax_top.set_xlabel('X', fontsize=8); ax_top.set_ylabel('Y', fontsize=8); ax_top.set_zticks([])

ax_front = fig.add_subplot(2, 3, 4, projection='3d')
setup_3d(ax_front, 0, -90, 'Front View (-Y) -- 4x insert pockets @ 20 mm')
ax_front.set_xlabel('X', fontsize=8); ax_front.set_zlabel('Z', fontsize=8); ax_front.set_yticks([])

ax_side = fig.add_subplot(2, 3, 5, projection='3d')
setup_3d(ax_side, 0, 0, 'Side View (+X) -- larger gusset + rib + cable channel')
ax_side.set_ylabel('Y', fontsize=8); ax_side.set_zlabel('Z', fontsize=8); ax_side.set_xticks([])

# Title block
ax_tb = fig.add_subplot(2, 3, 3)
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis('off')
ax_tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                            facecolor='white', edgecolor='black', lw=1.5))
rows = [
    ('PART',      'Mast Base Socket'),
    ('VERSION',   'V1.3'),
    ('MODULE',    '10 -- HMI'),
    ('QTY',       '2 (left + right)'),
    ('MATERIAL',  'PETG (PA12 prod)'),
    ('INFILL',    '100%, 4 walls'),
    ('LAYER',     '0.2 mm'),
    ('MASS',      '~101 g each'),
    ('TIME',      '~4 h each'),
    ('INSTALL',   '(X=+/-75, Y=-210)'),
]
y = 0.95
for k, v in rows:
    ax_tb.text(0.06, y, k, fontsize=8.5, fontweight='bold', color='#444')
    ax_tb.text(0.42, y, v, fontsize=8.5, color='#111')
    y -= 0.045

ax_tb.text(0.06, 0.50, 'DIMENSIONS (mm)', fontsize=10, fontweight='bold')
dims = [
    ('Socket outer', f'{SOCKET_OUTER} sq x {SOCKET_H}'),
    ('Pocket',       f'{POCKET_W} sq, R{POCKET_R} fillets'),
    ('Wall thick',   f'{WALL_T}'),
    ('Foot',         f'{FOOT_LEN} x {FOOT_W} x {FOOT_T}'),
    ('Foot bolt CB', f'{BOLT_CB_D} x {BOLT_CB_H}'),
    ('Gusset',       f'{GUSSET_B} x {GUSSET_R} x 6'),
    ('Anti-creep rib', f'2x {RIB_T} x {RIB_H}'),
    ('Cable channel', f'{CABLE_CH_W} x {CABLE_CH_D} rear'),
    ('Insert pocket', f'{INSERT_D} x {INSERT_H}'),
    ('Insert pitch', f'{EXP_COUNT} @ {EXP_PITCH}'),
]
yy = 0.46
for k, v in dims:
    ax_tb.text(0.06, yy, k, fontsize=7.5, color='#444', family='monospace')
    ax_tb.text(0.52, yy, v, fontsize=7.5, color='#111', family='monospace')
    yy -= 0.030

# Notes
ax_notes = fig.add_subplot(2, 3, 6)
ax_notes.set_xlim(0, 1); ax_notes.set_ylim(0, 1); ax_notes.axis('off')
ax_notes.text(0.02, 0.95, 'V1.3 IMPROVEMENTS', fontsize=10, fontweight='bold')
notes = [
    '1. R1.5 pocket inner fillets (printable + easier',
    '   2020 insertion + lower stress)',
    '2. Gussets enlarged 18x22 -> 25x30',
    '3. Foot thickness 8 -> 10 mm',
    '4. 2x anti-creep ribs (3 x 6) on foot top',
    '5. Foot bolt CSK -> counterbore (socket-head)',
    '6. Insert pitch 10 -> 20 mm (std patterns)',
    '7. cut_cylinder() helper in macro',
    '',
    'ASSEMBLY (per bracket):',
    '1. Print PETG foot-down, 100% infill, 4 walls',
    '2. Heat 4x M5 brass inserts into FRONT pockets',
    '3. 2x M5 T-nuts into 2020 FRONT slot',
    '4. Slide bracket pocket down over 2020 base',
    '5. M5 x 12 socket-heads through FRONT into T-nuts',
    '6. Bracket on wood at (X=+/-75, Y=-210)',
    '7. Drill 4x dia 5.5 through wood under bolt grid',
    '8. M5 x 30 socket-heads through foot CB into wood',
    '9. Washer + M5 nyloc nut under wood; tighten',
    '10. Verify 2020 stands square in both planes',
]
yy = 0.91
for n in notes:
    ax_notes.text(0.02, yy, n, fontsize=7.3, color='#222', family='sans-serif')
    yy -= 0.038

fig.text(0.5, 0.02,
         'github.com/leoalex196912/ChatGistory  *  '
         'CSM_V3_ASSEMBLY/hmi/mast_base_socket/  *  '
         'Module 10 part 1 of 10 (V1.3)',
         ha='center', fontsize=8, color='#888')

out_png = os.path.join(HERE, "CSM_V3_MastBaseSocket_V1_3_views.png")
out_pdf = os.path.join(HERE, "CSM_V3_MastBaseSocket_V1_3_views.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
