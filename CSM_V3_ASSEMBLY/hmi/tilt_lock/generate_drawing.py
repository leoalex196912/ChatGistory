# -*- coding: utf-8 -*-
"""CSM V3 -- HMI Module 10 -- Display Tilt Lock V1.0 Drawing Generator
Combined Base + Arm into single drawing."""
import os, struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_STL = os.path.join(HERE, "CSM_V3_TiltLock_V1_0_Base.stl")
ARM_STL  = os.path.join(HERE, "CSM_V3_TiltLock_V1_0_Arm.stl")

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

base_tris = parse_stl(BASE_STL)
arm_tris  = parse_stl(ARM_STL)
all_pts = np.vstack([base_tris.reshape(-1, 3), arm_tris.reshape(-1, 3)])
xmin, ymin, zmin = all_pts.min(axis=0)
xmax, ymax, zmax = all_pts.max(axis=0)

fig = plt.figure(figsize=(16, 12), dpi=180)
fig.suptitle('CSM V3 -- HMI Module 10 -- Display Tilt Lock V1.0',
             fontsize=16, fontweight='bold', y=0.97)
fig.text(0.5, 0.94, '2-piece friction tilt: BASE bolts to beam, ARM bolts to touchscreen frame',
         ha='center', fontsize=10, color='#444', style='italic')

def setup_3d(ax, elev, azim, title, tris, color):
    ax.add_collection3d(Poly3DCollection(tris, facecolor=color,
                                          edgecolor='#1a2a4a',
                                          linewidth=0.10, alpha=0.92))
    ax.set_xlim(xmin - 2, xmax + 2)
    ax.set_ylim(ymin - 2, ymax + 2)
    ax.set_zlim(zmin - 2, zmax + 2)
    ax.view_init(elev=elev, azim=azim)
    ax.set_proj_type('ortho')
    ax.set_title(title, fontweight='bold', pad=10)
    ax.tick_params(labelsize=7)

ax_base_iso = fig.add_subplot(2, 3, 1, projection='3d')
setup_3d(ax_base_iso, 22, -58, 'BASE Iso (mounts to beam)', base_tris, '#8aa6d0')
ax_base_iso.set_box_aspect((180, 5, 70))

ax_arm_iso = fig.add_subplot(2, 3, 4, projection='3d')
setup_3d(ax_arm_iso, 22, -58, 'ARM Iso (mounts to frame)', arm_tris, '#d09a86')
ax_arm_iso.set_box_aspect((180, 5, 70))

ax_base_front = fig.add_subplot(2, 3, 2, projection='3d')
setup_3d(ax_base_front, 0, -90, 'BASE Front -- pivot + lock inserts',
         base_tris, '#8aa6d0')
ax_base_front.set_box_aspect((180, 1, 70))
ax_base_front.set_xlabel('X'); ax_base_front.set_zlabel('Z'); ax_base_front.set_yticks([])

ax_arm_front = fig.add_subplot(2, 3, 5, projection='3d')
setup_3d(ax_arm_front, 0, -90, 'ARM Front -- frame inserts + lock arc-slot',
         arm_tris, '#d09a86')
ax_arm_front.set_box_aspect((180, 1, 70))
ax_arm_front.set_xlabel('X'); ax_arm_front.set_zlabel('Z'); ax_arm_front.set_yticks([])

ax_tb = fig.add_subplot(2, 3, 3)
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis('off')
ax_tb.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, facecolor='white',
                            edgecolor='black', lw=1.5))
rows = [
    ('PART',     'Display Tilt Lock'),
    ('NUMBER',   'M10-P06'),
    ('VERSION',  'V1.0 (DRAFT)'),
    ('MODULE',   '10 -- HMI'),
    ('QTY',      '1 Base + 1 Arm'),
    ('MATERIAL', 'PETG (PA12 prod)'),
    ('INFILL',   '100%, 4 walls'),
    ('LAYER',    '0.2 mm'),
    ('MASS',     '~79 g each'),
    ('PRINT',    'flat, ~1.5 h each'),
]
y = 0.95
for k, v in rows:
    ax_tb.text(0.06, y, k, fontsize=8.5, fontweight='bold', color='#444')
    ax_tb.text(0.42, y, v, fontsize=8.5, color='#111')
    y -= 0.045
ax_tb.text(0.06, 0.50, 'DIMENSIONS (mm)', fontsize=10, fontweight='bold')
dims = [
    ('Each plate',    '180 x 5 x 70'),
    ('Corner fillet', 'R3'),
    ('Beam bolts',    '4x M5 thru (Base)'),
    ('Frame inserts', '4x M5 heat-set (Arm)'),
    ('Pivot',         'M5 insert (Base)/thru (Arm)'),
    ('Lock screw',    'M5 insert (Base)'),
    ('Lock arc slot', '15 x 6 (Arm), 0-30 deg'),
    ('Tilt range',    '0 to +30 deg backward'),
]
yy = 0.46
for k, v in dims:
    ax_tb.text(0.06, yy, k, fontsize=7.2, color='#444', family='monospace')
    ax_tb.text(0.52, yy, v, fontsize=7.2, color='#111', family='monospace')
    yy -= 0.030

ax_notes = fig.add_subplot(2, 3, 6)
ax_notes.set_xlim(0, 1); ax_notes.set_ylim(0, 1); ax_notes.axis('off')
ax_notes.text(0.02, 0.95, 'ASSEMBLY', fontsize=10, fontweight='bold')
notes = [
    '1. Print both PETG 100%, 4 walls.',
    '   BASE: operator face down',
    '   ARM:  frame face down',
    '2. Heat 6x M5 inserts (B0DPQJ4W3Z):',
    '   BASE: pivot + lock (2)',
    '   ARM:  4 frame-mount inserts',
    '3. Bolt BASE to beam (4x M5 x 20)',
    '4. Stack ARM on BASE; M5 x 16 thumb',
    '   screw through ARM pivot into BASE',
    '5. M5 x 16 thumb screw through ARM',
    '   lock slot into BASE lock insert',
    '6. Bolt Touchscreen Frame to ARM',
    '   (frame existing M5 x 12 bolts)',
    '7. Adjust: loosen lock thumb screw,',
    '   tilt, retighten.  Friction holds.',
    '',
    'V1.1 PLAN: toothed indexing at 10 deg',
    '       increments (eliminates slip).',
    '',
    'WALL CHECK: all 7 OK, min 3.25 mm',
]
yy = 0.91
for n in notes:
    ax_notes.text(0.02, yy, n, fontsize=7.1, color='#222', family='sans-serif')
    yy -= 0.034

fig.text(0.5, 0.02,
         'github.com/leoalex196912/ChatGistory  *  '
         'CSM_V3_ASSEMBLY/hmi/tilt_lock/  *  '
         'Module 10 part 6 of 10',
         ha='center', fontsize=8, color='#888')

out_png = os.path.join(HERE, "CSM_V3_TiltLock_V1_0_views.png")
out_pdf = os.path.join(HERE, "CSM_V3_TiltLock_V1_0_views.pdf")
fig.savefig(out_png, dpi=180, bbox_inches='tight', facecolor='white')
fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"[OK] PNG: {out_png}")
print(f"[OK] PDF: {out_pdf}")
