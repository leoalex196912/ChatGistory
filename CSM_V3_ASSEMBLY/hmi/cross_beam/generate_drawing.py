# -*- coding: utf-8 -*-
"""
CSM V3 -- HMI Module 10 -- Cross Beam Drawing Generator
=======================================================
Renders the Cross Beam V1.0 STL as a multi-view engineering drawing:
  - Isometric perspective view
  - Top view (X-Y plane)  -- shows mast pockets, Pi mount points
  - Front view (X-Z, -Y face) -- 6x accessory insert pockets
  - Side view (Y-Z, +X face) -- cable channel profile
Plus title block, dimensions, and assembly notes.

Output:
  CSM_V3_CrossBeam_V1_0_views.png
  CSM_V3_CrossBeam_V1_0_views.pdf

Run with FreeCAD's Python (has matplotlib + numpy):
  "C:/Program Files/FreeCAD 1.1/bin/python.exe" generate_drawing.py
"""
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
STL_PATH = os.path.join(HERE, "CSM_V3_CrossBeam_V1_1.stl")

# Beam parameters (V1.1, mirror the macro for dimension annotation)
BEAM_LEN_X   = 170.0
BEAM_W_Y     = 40.0
BEAM_H_Z     = 30.0
MAST_SPACING = 150.0
POCKET_W     = 20.8
POCKET_DEPTH = 12.0
MAST_BOLT_D  = 5.5
BOLT_CB_D    = 9.5
BOLT_CB_H    = 5.5
INSERT_D     = 6.2
INSERT_H     = 8.5
PI_PCD_X     = 58.0
PI_PCD_Y     = 49.0
CABLE_CH_W   = 8.0
CABLE_CH_D   = 4.0
FRONT_COUNT  = 6
FRONT_PITCH  = 22.0
SERVICE_X    = 50.0
SERVICE_Y    = 18.0

# ============================================================
# STL parser (auto-detect ASCII vs binary)
# ============================================================
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
                    tris.append(cur)
                    cur = []
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
print(f"  extent: X[{xmin:.1f}, {xmax:.1f}]  Y[{ymin:.1f}, {ymax:.1f}]  Z[{zmin:.1f}, {zmax:.1f}]")

# ============================================================
# Figure layout: 2x3 grid
# ============================================================
fig = plt.figure(figsize=(16, 12), dpi=180)
fig.suptitle('CSM V3 -- HMI Module 10 -- Cross Beam V1.1',
             fontsize=16, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, 'Horizontal cross-member joining mast tops  *  Carries Pi 4 + future accessories  *  '
                    'PETG, 100% infill, 4 walls',
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

# Beam is long in X (170) and short in Y/Z (30/25); aspect needs care
ax_iso = fig.add_subplot(2, 3, 1, projection='3d')
setup_3d(ax_iso, 22, -58, 'Isometric View')
ax_iso.set_box_aspect((BEAM_LEN_X, BEAM_W_Y, BEAM_H_Z))
ax_iso.set_xlabel('X', fontsize=8); ax_iso.set_ylabel('Y', fontsize=8); ax_iso.set_zlabel('Z', fontsize=8)

ax_top = fig.add_subplot(2, 3, 2, projection='3d')
setup_3d(ax_top, 89.9, -90, 'Top View (X-Y) -- mast pockets + Pi inserts')
ax_top.set_box_aspect((BEAM_LEN_X, BEAM_W_Y, 1))
ax_top.set_xlabel('X', fontsize=8); ax_top.set_ylabel('Y', fontsize=8); ax_top.set_zticks([])

ax_front = fig.add_subplot(2, 3, 4, projection='3d')
setup_3d(ax_front, 0, -90, 'Front View (-Y face) -- 6x accessory inserts')
ax_front.set_box_aspect((BEAM_LEN_X, 1, BEAM_H_Z))
ax_front.set_xlabel('X', fontsize=8); ax_front.set_zlabel('Z', fontsize=8); ax_front.set_yticks([])

ax_side = fig.add_subplot(2, 3, 5, projection='3d')
setup_3d(ax_side, 0, 0, 'Side View (+X face) -- end profile + cable channel')
ax_side.set_box_aspect((1, BEAM_W_Y, BEAM_H_Z))
ax_side.set_ylabel('Y', fontsize=8); ax_side.set_zlabel('Z', fontsize=8); ax_side.set_xticks([])

# === Title block (top-right) ===
ax_tb = fig.add_subplot(2, 3, 3)
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis('off')
ax_tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                            facecolor='white', edgecolor='black', lw=1.5))
rows = [
    ('PART',      'Cross Beam'),
    ('VERSION',   'V1.1'),
    ('MODULE',    '10 -- HMI'),
    ('QTY',       '1'),
    ('MATERIAL',  'PETG (PA12 prod)'),
    ('INFILL',    '100%, 4 walls'),
    ('LAYER',     '0.2 mm'),
    ('MASS',      '~202 g'),
    ('TIME',      '~8-10 h'),
    ('INSTALL',   'top of HMI masts (X=0)'),
]
y = 0.95
for k, v in rows:
    ax_tb.text(0.06, y, k, fontsize=8.5, fontweight='bold', color='#444')
    ax_tb.text(0.42, y, v, fontsize=8.5, color='#111')
    y -= 0.045

ax_tb.text(0.06, 0.50, 'DIMENSIONS (mm)', fontsize=10, fontweight='bold')
dims = [
    ('Beam L x W x H', f'{BEAM_LEN_X} x {BEAM_W_Y} x {BEAM_H_Z}'),
    ('Mast spacing',   f'{MAST_SPACING} (X=+/-75)'),
    ('Mast pockets',   f'{POCKET_W:.1f} sq x {POCKET_DEPTH} deep'),
    ('Mast bolt',      f'M5, CB {BOLT_CB_D} x {BOLT_CB_H} on TOP'),
    ('Pi mount PCD',   f'{PI_PCD_X} x {PI_PCD_Y} (Pi 4 std)'),
    ('Cable channel',  f'{CABLE_CH_W} x {CABLE_CH_D} (rear)'),
    ('Insert pocket',  f'{INSERT_D} dia x {INSERT_H} deep'),
    ('Front inserts',  f'{FRONT_COUNT} @ {FRONT_PITCH} pitch'),
    ('Service open',   f'{SERVICE_X} x {SERVICE_Y} top'),
]
yy = 0.46
for k, v in dims:
    ax_tb.text(0.06, yy, k, fontsize=7.5, color='#444', family='monospace')
    ax_tb.text(0.50, yy, v, fontsize=7.5, color='#111', family='monospace')
    yy -= 0.030

# === Notes panel (bottom-right) ===
ax_notes = fig.add_subplot(2, 3, 6)
ax_notes.set_xlim(0, 1); ax_notes.set_ylim(0, 1); ax_notes.axis('off')
ax_notes.text(0.02, 0.95, 'ASSEMBLY', fontsize=10, fontweight='bold')
notes = [
    'V1.1 changes from V1.0:',
    '  - Beam 30x25 -> 40x30 (fits Pi 4 PCD 49)',
    '  - Mast pockets 8 -> 12 mm (better torsion)',
    '  - Center service opening on TOP face',
    '  - Mast bolt CSK -> counterbore (socket-head)',
    '',
    'ASSEMBLY:',
    '1. Print PETG flat on bed, 100% infill,',
    '   4 walls, 0.2 mm layers',
    '2. Heat 4x M5 inserts into BOTTOM Pi mount',
    '3. Heat 6x M5 inserts into FRONT face',
    '4. Drop beam over both mast tops (12 mm engage)',
    '5. M5 x 30 socket-head through TOP counterbores',
    '   self-tap into 2020 center bore',
    '6. SD card / cables via center service opening',
    '7. Mount Pi Carrier V1.0 to BOTTOM inserts',
    '8. Route cables up REAR face cable channel',
    '',
    'EXPANSION (6x M5, FRONT face):',
    '  - Status LED, mic, motion sensor, OLED,',
    '    camera, future UI',
]
yy = 0.91
for n in notes:
    ax_notes.text(0.02, yy, n, fontsize=7.5, color='#222', family='sans-serif')
    yy -= 0.038

fig.text(0.5, 0.02,
         'github.com/leoalex196912/ChatGistory  *  '
         'CSM_V3_ASSEMBLY/hmi/cross_beam/  *  '
         'Module 10 part 2 of 10',
         ha='center', fontsize=8, color='#888')

out_png = os.path.join(HERE, "CSM_V3_CrossBeam_V1_1_views.png")
out_pdf = os.path.join(HERE, "CSM_V3_CrossBeam_V1_1_views.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
