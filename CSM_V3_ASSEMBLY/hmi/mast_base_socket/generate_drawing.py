# -*- coding: utf-8 -*-
"""
CSM V3 — HMI Module 10 — Mast Base Socket Drawing Generator
============================================================
Renders the V1.1 STL as a multi-view engineering drawing:
  - Isometric perspective view (large)
  - Top view (X-Y plane)
  - Front view (X-Z plane, operator-facing)
  - Side view (Y-Z plane)
Plus dimensions, title block, and notes.

Output:
  CSM_V3_MastBaseSocket_V1_1_views.png
  CSM_V3_MastBaseSocket_V1_1_views.pdf

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
STL_PATH = os.path.join(HERE, "CSM_V3_MastBaseSocket_V1_1.stl")

# Bracket parameters (mirror the macro for dimension annotation)
SOCKET_OUTER_W = 34.0
SOCKET_OUTER_T = 34.0
SOCKET_H       = 50.0
SOCKET_BOT_T   =  5.0
POCKET_W       = 20.8
POCKET_T       = 20.8
WALL_T         = 6.6
FOOT_LEN       = 70.0
FOOT_W         = 50.0
FOOT_T         = 8.0
FOOT_BOLT_DX   = 25.0
FOOT_BOLT_DY   = 17.0
T_BOLT_Z1      = 12.0
T_BOLT_Z2      = 38.0
GUSSET_BASE    = 18.0
GUSSET_RISE    = 22.0
CABLE_CH_W     = 8.0
CABLE_CH_D     = 4.0
INSERT_POCKET_D = 6.2
EXP_INSERT_COUNT = 4
EXP_INSERT_PITCH = 10.0
EXP_INSERT_Z0_REL = 6.0

# ============================================================
# STL parser (auto-detect ASCII vs binary)
# ============================================================
def parse_stl(path):
    """Auto-detect ASCII or binary STL, return triangles array (N, 3, 3)."""
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

# Bracket extent for axis scaling
all_pts = triangles.reshape(-1, 3)
xmin, ymin, zmin = all_pts.min(axis=0)
xmax, ymax, zmax = all_pts.max(axis=0)
print(f"  extent: X[{xmin:.1f}, {xmax:.1f}]  Y[{ymin:.1f}, {ymax:.1f}]  Z[{zmin:.1f}, {zmax:.1f}]")

# ============================================================
# Figure layout: 2x2 grid + title block
# ============================================================
fig = plt.figure(figsize=(16, 12), dpi=180)
fig.suptitle('CSM V3 — HMI Module 10 — Mast Base Socket V1.1',
             fontsize=16, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, 'Full U-pocket bracket for 2020 V-slot extrusion  •  '
                    'Print 2 (left + right)  •  PETG, 100% infill, 4 walls',
         ha='center', fontsize=10, color='#444', style='italic')

# === Isometric perspective (large, top-left) ===
ax_iso = fig.add_subplot(2, 3, 1, projection='3d')
ax_iso.add_collection3d(Poly3DCollection(triangles,
                                          facecolor='#4a6a9a',
                                          edgecolor='#1a2a4a',
                                          linewidth=0.15, alpha=0.92))
ax_iso.set_xlim(xmin - 2, xmax + 2)
ax_iso.set_ylim(ymin - 2, ymax + 2)
ax_iso.set_zlim(zmin - 2, zmax + 2)
ax_iso.set_box_aspect((1, 1, 0.9))
ax_iso.view_init(elev=22, azim=-58)
ax_iso.set_proj_type('ortho')
ax_iso.set_title('Isometric View', fontweight='bold', pad=10)
ax_iso.set_xlabel('X', fontsize=8)
ax_iso.set_ylabel('Y', fontsize=8)
ax_iso.set_zlabel('Z', fontsize=8)
ax_iso.tick_params(labelsize=7)

# === Top view (X-Y plane, looking down +Z) ===
ax_top = fig.add_subplot(2, 3, 2, projection='3d')
ax_top.add_collection3d(Poly3DCollection(triangles,
                                          facecolor='#4a6a9a',
                                          edgecolor='#1a2a4a',
                                          linewidth=0.15, alpha=0.92))
ax_top.set_xlim(xmin - 2, xmax + 2)
ax_top.set_ylim(ymin - 2, ymax + 2)
ax_top.set_zlim(zmin - 2, zmax + 2)
ax_top.view_init(elev=89.9, azim=-90)
ax_top.set_proj_type('ortho')
ax_top.set_title('Top View (X-Y plane)', fontweight='bold', pad=10)
ax_top.set_xlabel('X', fontsize=8)
ax_top.set_ylabel('Y', fontsize=8)
ax_top.set_zticks([])
ax_top.tick_params(labelsize=7)

# === Front view (X-Z plane, looking in +Y, operator-facing FRONT face) ===
ax_front = fig.add_subplot(2, 3, 4, projection='3d')
ax_front.add_collection3d(Poly3DCollection(triangles,
                                            facecolor='#4a6a9a',
                                            edgecolor='#1a2a4a',
                                            linewidth=0.15, alpha=0.92))
ax_front.set_xlim(xmin - 2, xmax + 2)
ax_front.set_ylim(ymin - 2, ymax + 2)
ax_front.set_zlim(zmin - 2, zmax + 2)
ax_front.view_init(elev=0, azim=-90)
ax_front.set_proj_type('ortho')
ax_front.set_title('Front View (-Y face, operator side) — 4× insert pockets',
                    fontweight='bold', pad=10)
ax_front.set_xlabel('X', fontsize=8)
ax_front.set_ylabel('')
ax_front.set_zlabel('Z', fontsize=8)
ax_front.set_yticks([])
ax_front.tick_params(labelsize=7)

# === Side view (Y-Z plane, looking in +X) ===
ax_side = fig.add_subplot(2, 3, 5, projection='3d')
ax_side.add_collection3d(Poly3DCollection(triangles,
                                           facecolor='#4a6a9a',
                                           edgecolor='#1a2a4a',
                                           linewidth=0.15, alpha=0.92))
ax_side.set_xlim(xmin - 2, xmax + 2)
ax_side.set_ylim(ymin - 2, ymax + 2)
ax_side.set_zlim(zmin - 2, zmax + 2)
ax_side.view_init(elev=0, azim=0)
ax_side.set_proj_type('ortho')
ax_side.set_title('Side View (+X face) — gusset profile + cable channel',
                   fontweight='bold', pad=10)
ax_side.set_xlabel('')
ax_side.set_ylabel('Y', fontsize=8)
ax_side.set_zlabel('Z', fontsize=8)
ax_side.set_xticks([])
ax_side.tick_params(labelsize=7)

# === Title block + dimensions (right column) ===
ax_tb = fig.add_subplot(2, 3, 3)
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis('off')
ax_tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96,
                            facecolor='white', edgecolor='black', lw=1.5))
rows = [
    ('PART',      'Mast Base Socket'),
    ('VERSION',   'V1.1'),
    ('MODULE',    '10 — HMI'),
    ('QTY',       '2 (left + right)'),
    ('MATERIAL',  'PETG (PA12 prod)'),
    ('INFILL',    '100%, 4 walls'),
    ('LAYER',     '0.2 mm'),
    ('MASS',      '~82 g each'),
    ('TIME',      '~3-4 h each'),
    ('INSTALL',   '(X=±75, Y=-210)'),
]
y = 0.95
for k, v in rows:
    ax_tb.text(0.06, y, k, fontsize=8.5, fontweight='bold', color='#444')
    ax_tb.text(0.42, y, v, fontsize=8.5, color='#111')
    y -= 0.045

ax_tb.text(0.06, 0.50, 'DIMENSIONS (mm)', fontsize=10, fontweight='bold')
dims = [
    ('Socket outer', f'{SOCKET_OUTER_W} × {SOCKET_OUTER_T} × {SOCKET_H}'),
    ('Pocket inner', f'{POCKET_W:.1f} × {POCKET_T:.1f} (0.4 dia clear)'),
    ('Wall thickness', f'{WALL_T:.1f}'),
    ('Foot', f'{FOOT_LEN} × {FOOT_W} × {FOOT_T}'),
    ('Foot bolt grid', f'±{FOOT_BOLT_DX} × ±{FOOT_BOLT_DY}'),
    ('Lateral bolt Z', f'{T_BOLT_Z1} / {T_BOLT_Z2}'),
    ('Gusset (B×H×T)', f'{GUSSET_BASE} × {GUSSET_RISE} × 6'),
    ('Cable channel', f'{CABLE_CH_W} × {CABLE_CH_D} (rear)'),
    ('Insert pocket Ø', f'{INSERT_POCKET_D} × 8.5 deep'),
    ('Insert count/pitch', f'{EXP_INSERT_COUNT} × {EXP_INSERT_PITCH} (front)'),
]
yy = 0.46
for k, v in dims:
    ax_tb.text(0.06, yy, k, fontsize=7.5, color='#444', family='monospace')
    ax_tb.text(0.50, yy, v, fontsize=7.5, color='#111', family='monospace')
    yy -= 0.030

# === Notes panel (bottom-right) ===
ax_notes = fig.add_subplot(2, 3, 6)
ax_notes.set_xlim(0, 1); ax_notes.set_ylim(0, 1); ax_notes.axis('off')
ax_notes.text(0.02, 0.95, 'ASSEMBLY (per bracket)', fontsize=10, fontweight='bold')
notes = [
    '1. Print PETG foot-down, 100% infill, 4 walls, 0.2 mm',
    '2. Heat 4× M5 brass inserts (B0DPQJ4W3Z) into FRONT face',
    '   pockets with soldering iron at ~220 °C, ~30 s each',
    '3. Slide 2× M5 T-nuts into 2020 FRONT slot at desired Z',
    '4. Slide bracket pocket down over 2020 base',
    '5. M5 × 12 mm bolts through bracket FRONT into T-nuts',
    '6. Place bracket on wood base at (X=+75 OR -75, Y=-210)',
    '7. Mark + drill 4× Ø5.5 in wood under foot bolt positions',
    '8. M5 × 25 socket-head bolts through countersunk foot top',
    '9. Steel flat washer + M5 nyloc nut underneath wood base',
    '10. Verify 2020 stands vertical (square against plate)',
    '',
    'EXPANSION (future, via heat-set inserts):',
    '  - Camera mount, LED strip, status panel, sensors',
    '  - Repeatable install/remove with M5 screws',
    '',
    'STRESS NOTES:',
    '  - 50 mm socket engagement (V1.0 had 35 mm)',
    '  - Lateral bolts spaced 12/38 mm for vertical retention',
    '  - Gussets both X sides for foot-socket transition',
    '  - Foot-socket fillet attempted but skipped (OCC error)',
    '    Manual blend candidate if first-print shows cracks',
]
yy = 0.91
for n in notes:
    ax_notes.text(0.02, yy, n, fontsize=7.5, color='#222', family='sans-serif')
    yy -= 0.038

# === Footer ===
fig.text(0.5, 0.02,
         'github.com/leoalex196912/ChatGistory  •  '
         'CSM_V3_ASSEMBLY/hmi/mast_base_socket/  •  '
         'Module 10 part 1 of 10',
         ha='center', fontsize=8, color='#888')

# ============================================================
# Save
# ============================================================
out_png = os.path.join(HERE, "CSM_V3_MastBaseSocket_V1_1_views.png")
out_pdf = os.path.join(HERE, "CSM_V3_MastBaseSocket_V1_1_views.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
