# -*- coding: utf-8 -*-
"""CSM V3 -- HMI Module 10 -- LED Strip Holder V1.0 Drawing Generator"""
import os, struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
STL_PATH = os.path.join(HERE, "CSM_V3_LedStripHolder_V1_0.stl")

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

triangles = parse_stl(STL_PATH)
all_pts = triangles.reshape(-1, 3)
xmin, ymin, zmin = all_pts.min(axis=0)
xmax, ymax, zmax = all_pts.max(axis=0)

fig = plt.figure(figsize=(16, 12), dpi=180)
fig.suptitle('CSM V3 -- HMI Module 10 -- LED Strip Holder V1.0',
             fontsize=16, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, 'Work-area lighting: 150 mm channel for 5 V LED strip, zip-ties to beam',
         ha='center', fontsize=10, color='#444', style='italic')

def setup_3d(ax, elev, azim, title):
    ax.add_collection3d(Poly3DCollection(triangles, facecolor='#f0e08c',
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
setup_3d(ax_iso, 28, -58, 'Isometric View')
ax_iso.set_box_aspect((150, 14, 14))
ax_iso.set_xlabel('X'); ax_iso.set_ylabel('Y'); ax_iso.set_zlabel('Z')

ax_top = fig.add_subplot(2, 3, 2, projection='3d')
setup_3d(ax_top, 89.9, -90, 'Top View (against beam) -- 2 zip-tie grooves')
ax_top.set_box_aspect((150, 14, 1))
ax_top.set_xlabel('X'); ax_top.set_ylabel('Y'); ax_top.set_zticks([])

ax_bot = fig.add_subplot(2, 3, 4, projection='3d')
setup_3d(ax_bot, -89.9, -90, 'Bottom View (LED side) -- strip channel')
ax_bot.set_box_aspect((150, 14, 1))
ax_bot.set_xlabel('X'); ax_bot.set_ylabel('Y'); ax_bot.set_zticks([])

ax_side = fig.add_subplot(2, 3, 5, projection='3d')
setup_3d(ax_side, 0, 0, 'End View -- 14 x 5 mm cross-section')
ax_side.set_box_aspect((1, 14, 6))
ax_side.set_ylabel('Y'); ax_side.set_zlabel('Z'); ax_side.set_xticks([])

ax_tb = fig.add_subplot(2, 3, 3)
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis('off')
ax_tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, facecolor='white',
                            edgecolor='black', lw=1.5))
rows = [
    ('PART',     'LED Strip Holder'),
    ('NUMBER',   'M10-P09'),
    ('VERSION',  'V1.0 (DRAFT)'),
    ('MODULE',   '10 -- HMI'),
    ('QTY',      '1'),
    ('MATERIAL', 'PETG (PA12 prod)'),
    ('INFILL',   '100%, 4 walls'),
    ('LAYER',    '0.2 mm'),
    ('MASS',     '~8.4 g'),
    ('PRINT',    'flat, ~25 min'),
]
y = 0.95
for k, v in rows:
    ax_tb.text(0.06, y, k, fontsize=8.5, fontweight='bold', color='#444')
    ax_tb.text(0.42, y, v, fontsize=8.5, color='#111')
    y -= 0.045
ax_tb.text(0.06, 0.50, 'DIMENSIONS (mm)', fontsize=10, fontweight='bold')
dims = [
    ('Holder',         '150 x 14 x 5'),
    ('LED channel',    '10 wide x 2.5 deep'),
    ('Channel face',   'BOTTOM (LED out)'),
    ('Zip-tie grooves','2x 4 x 1 at X=+/-60'),
    ('LED strip',      '5V, 10 x 2-3 mm'),
    ('Mounts to',      'beam underside'),
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
    '1. Print PETG flat (TOP face down -- clean',
    '   channel surface)',
    '2. Solder leads to LED strip first (easier',
    '   than working overhead)',
    '3. Peel adhesive, press strip up into',
    '   channel; LEDs face out / downward',
    '4. Position against beam underside',
    '   (clears Pi Carrier in center)',
    '5. Pass 2x 2.5 mm zip-ties UP through',
    '   grooves, OVER beam top, back down,',
    '   pull tight; grooves prevent X slide',
    '6. Wire 5 V leads up rear mast face into',
    '   beam cable channel; connect to:',
    '     - Pi GPIO pin 2/4 (+5V) + 6/14 (GND)',
    '     - or LM2596 buck #2 5V output',
    '',
    'WALL CHECK: all 6 OK, min 1.5 mm',
    '',
    'NO BOLTS NEEDED -- zip-tie only.',
    'Coexists with Touchscreen Frame and',
    'Expansion Plate (uses different mounts).',
]
yy = 0.91
for n in notes:
    ax_notes.text(0.02, yy, n, fontsize=7.2, color='#222', family='sans-serif')
    yy -= 0.034

fig.text(0.5, 0.02,
         'github.com/leoalex196912/ChatGistory  *  '
         'CSM_V3_ASSEMBLY/hmi/led_strip_holder/  *  '
         'Module 10 part 9 of 10',
         ha='center', fontsize=8, color='#888')

out_png = os.path.join(HERE, "CSM_V3_LedStripHolder_V1_0_views.png")
out_pdf = os.path.join(HERE, "CSM_V3_LedStripHolder_V1_0_views.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
