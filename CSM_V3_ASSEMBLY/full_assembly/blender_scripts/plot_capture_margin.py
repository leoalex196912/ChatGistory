#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plot capture_margin(theta) from metrics.csv files.

Designed to compare nominal vs failure-mode runs frame-for-frame.

Usage:
  py plot_capture_margin.py                # plots all anim_*/metrics.csv it finds

Output:
  capture_margin_plot.png in the renders/ folder.

Pure stdlib + matplotlib; works without Blender or FreeCAD.
"""
import csv, os, sys, glob

try:
    import matplotlib
    matplotlib.use('Agg')   # headless
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib not installed. Install with:  py -m pip install matplotlib")
    sys.exit(1)

RENDERS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace(
    "blender_scripts", "renders")
RENDERS_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"

csv_paths = sorted(glob.glob(os.path.join(RENDERS_DIR, "anim_*", "metrics.csv")))
if not csv_paths:
    print(f"No metrics.csv files found in {RENDERS_DIR}/anim_*/")
    sys.exit(1)

print(f"Found {len(csv_paths)} animation runs:")
for p in csv_paths: print(f"  {p}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Top panel: capture margin
# Bottom panel: needle Z

for csv_path in csv_paths:
    label = os.path.basename(os.path.dirname(csv_path)).replace("anim_", "")
    thetas, margins, needle_zs, in_capture = [], [], [], []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            thetas.append(float(row["theta_cyl_deg"]))
            margins.append(float(row["capture_margin_mm"]))
            needle_zs.append(float(row["needle_z_mm"]))
            in_capture.append(row["in_capture_window"] == "1")

    ax1.plot(thetas, margins, marker='o', markersize=4, label=label)
    ax2.plot(thetas, needle_zs, marker='.', markersize=3, label=label)

    # Shade capture windows
    for i in range(len(thetas)):
        if in_capture[i]:
            ax1.axvspan(thetas[i] - 5, thetas[i] + 5, alpha=0.05, color='green')

# Top panel decorations
ax1.axhline(0, color='gray', linewidth=0.8, linestyle='--')
ax1.set_ylabel("Capture margin (mm)\n+ = yarn above hook | - = below")
ax1.set_title("CSM V3  Phase 1.5  capture-margin vs cylinder phase")
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# Mark feeder positions
for ft, lbl in [(0, "F1 (+X)"), (180, "F4 (-X)")]:
    ax1.axvline(ft, color='red', alpha=0.4, linewidth=1.5)
    ax1.text(ft, ax1.get_ylim()[1]*0.9, lbl, ha='center', fontsize=9, color='red')

# Bottom panel decorations
ax2.axhline(264, color='red', alpha=0.5, linewidth=0.8, linestyle='--', label='HOOK_PEAK_Z (264)')
ax2.axhline(256, color='blue', alpha=0.5, linewidth=0.8, linestyle='--', label='CYLINDER_TOP_Z (256)')
ax2.axhline(270, color='orange', alpha=0.5, linewidth=0.8, linestyle='--', label='retainer lip (270)')
ax2.set_xlabel("Cylinder rotation theta_cyl (deg)")
ax2.set_ylabel("Needle Z (mm, world)")
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
ax2.set_xticks(range(0, 361, 30))

out = os.path.join(RENDERS_DIR, "capture_margin_plot.png")
plt.tight_layout()
plt.savefig(out, dpi=120)
print(f"\nSaved plot: {out}")
