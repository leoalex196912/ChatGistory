# -*- coding: utf-8 -*-
"""CSM V3 -- HMI Module 10 -- Touchscreen Frame V1.2 Drawing Generator"""
import os, struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
STL_PATH = os.path.join(HERE, "CSM_V3_TouchscreenFrame_V1_2.stl")

def parse_stl(path):
    with open(path, 'rb') as f:
        head = f.read(5)
    if head == b'solid':
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
fig.suptitle('CSM V3 -- HMI Module 10 -- Touchscreen Frame V1.2 [RC1]',
             fontsize=16, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, 'Back plate for ELECROW RC070S 7" touchscreen (165 x 102 x 35 mm)',
         ha='center', fontsize=10, color='#444', style='italic')

def setup_3d(ax, elev, azim, title):
    ax.add_collection3d(Poly3DCollection(triangles, facecolor='#7090c0',
                                          edgecolor='#1a2a4a',
                                          linewidth=0.08, alpha=0.92))
    ax.set_xlim(xmin - 2, xmax + 2)
    ax.set_ylim(ymin - 2, ymax + 2)
    ax.set_zlim(zmin - 2, zmax + 2)
    ax.view_init(elev=elev, azim=azim)
    ax.set_proj_type('ortho')
    ax.set_title(title, fontweight='bold', pad=10)
    ax.tick_params(labelsize=7)

ax_iso = fig.add_subplot(2, 3, 1, projection='3d')
setup_3d(ax_iso, 22, -58, 'Isometric View')
ax_iso.set_box_aspect((180, 5, 130))
ax_iso.set_xlabel('X'); ax_iso.set_ylabel('Y'); ax_iso.set_zlabel('Z')

ax_front = fig.add_subplot(2, 3, 2, projection='3d')
setup_3d(ax_front, 0, -90, 'Front View (operator) -- 4 windows + 4 beam bolts')
ax_front.set_box_aspect((180, 1, 130))
ax_front.set_xlabel('X'); ax_front.set_zlabel('Z'); ax_front.set_yticks([])

ax_back = fig.add_subplot(2, 3, 4, projection='3d')
setup_3d(ax_back, 0, 90, 'Back View (screen side)')
ax_back.set_box_aspect((180, 1, 130))
ax_back.set_xlabel('X'); ax_back.set_zlabel('Z'); ax_back.set_yticks([])

ax_side = fig.add_subplot(2, 3, 5, projection='3d')
setup_3d(ax_side, 0, 0, 'Side View -- 5 mm thickness')
ax_side.set_box_aspect((1, 5, 130))
ax_side.set_ylabel('Y'); ax_side.set_zlabel('Z'); ax_side.set_xticks([])

ax_tb = fig.add_subplot(2, 3, 3)
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis('off')
ax_tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, facecolor='white',
                            edgecolor='black', lw=1.5))
rows = [
    ('PART',     'Touchscreen Frame'),
    ('NUMBER',   'M10-P05'),
    ('VERSION',  'V1.2 (RC1)'),
    ('MODULE',   '10 -- HMI'),
    ('QTY',      '1'),
    ('MATERIAL', 'PETG (PA12 prod)'),
    ('INFILL',   '100%, 4 walls'),
    ('LAYER',    '0.2 mm'),
    ('MASS',     '~123 g'),
    ('PRINT',    'flat, ~3.5 h'),
]
y = 0.95
for k, v in rows:
    ax_tb.text(0.06, y, k, fontsize=8.5, fontweight='bold', color='#444')
    ax_tb.text(0.42, y, v, fontsize=8.5, color='#111')
    y -= 0.045
ax_tb.text(0.06, 0.50, 'DIMENSIONS (mm)', fontsize=10, fontweight='bold')
dims = [
    ('Plate',          '180 x 5 x 130'),
    ('Tab band (top)', '18 mm'),
    ('Beam bolts',     '4x M5 at X=+/-33,+/-55'),
    ('Beam bolt Z',    '123 (from bottom)'),
    ('Screen windows', '4x 30 x 30 mm'),
    ('Window PCD',     '80 x 64 (ELECROW)'),
    ('PCD range',      'X 50-110, Y 34-94'),
    ('Cable cutout',   '30 x 10 (bottom)'),
    ('Screen size',    '164.9 x 102 x 34.7'),
]
yy = 0.46
for k, v in dims:
    ax_tb.text(0.06, yy, k, fontsize=7.4, color='#444', family='monospace')
    ax_tb.text(0.50, yy, v, fontsize=7.4, color='#111', family='monospace')
    yy -= 0.030

ax_notes = fig.add_subplot(2, 3, 6)
ax_notes.set_xlim(0, 1); ax_notes.set_ylim(0, 1); ax_notes.axis('off')
ax_notes.text(0.02, 0.95, 'ASSEMBLY', fontsize=10, fontweight='bold')
notes = [
    '1. Print PETG flat, 100% infill, 4 walls,',
    '   BACK face up (clean window edges)',
    '2. Thread 4x brass pillars (ELECROW kit)',
    '   INTO screen back at PCD 79.45 x 64.4 mm',
    '3. Hold screen behind frame; pass 4x M2.5',
    '   screws + ~10 mm fender washer through',
    '   the corner windows from FRONT face into',
    '   the pillars; snug',
    '4. HDMI + USB-C cables hide in pillar gap',
    '5. Route cables DOWN through bottom cutout',
    '6. Bolt 4x M5 x 12 socket-head from FRONT',
    '   into beam FRONT-face inserts at',
    '   X = +/-33, +/-55 (skip middle pair)',
    '7. Route HDMI + USB-C up rear mast face,',
    '   through beam cable channel, to Pi Carrier',
    '',
    'PCD COVERAGE (also fits):',
    '  * VESA-75 (75 x 75)',
    '  * Raspberry Pi displays (58 x 49)',
    '  * Generic 7" HDMI LCDs within range',
    '',
    'WALL CHECK: all 10 OK',
]
yy = 0.91
for n in notes:
    ax_notes.text(0.02, yy, n, fontsize=7.0, color='#222', family='sans-serif')
    yy -= 0.033

fig.text(0.5, 0.02,
         'github.com/leoalex196912/ChatGistory  *  '
         'CSM_V3_ASSEMBLY/hmi/touchscreen_frame/  *  '
         'Module 10 part 5 of 10',
         ha='center', fontsize=8, color='#888')

out_png = os.path.join(HERE, "CSM_V3_TouchscreenFrame_V1_2_views.png")
out_pdf = os.path.join(HERE, "CSM_V3_TouchscreenFrame_V1_2_views.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
