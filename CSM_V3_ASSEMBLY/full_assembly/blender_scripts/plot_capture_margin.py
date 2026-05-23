#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plot capture_margin(theta) for all parameter sweeps in renders/anim_*/

Output:
  capture_margin_plot.png        -- 3 panels (A1 lag, B1 slack, D1 miss)
                                    each color-coded by parameter value
  delta_margin_plot.png          -- delta from nominal per sweep
                                    (shows divergence directly)
"""
import csv, os, sys, glob, re
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
except ImportError:
    print("matplotlib needed: py -m pip install matplotlib"); sys.exit(1)

RENDERS_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"

def load_csv(path):
    rows = []
    with open(path, "r") as f:
        for row in csv.DictReader(f):
            rows.append({
                "theta": float(row["theta_cyl_deg"]),
                "margin_z": float(row["capture_margin_mm"]),
                "needle_z": float(row["needle_z_mm"]),
                "offset_xy": float(row.get("capture_offset_xy_mm", 0.0) or 0.0),
                "dist_3d": float(row.get("capture_3d_distance_mm", 0.0) or 0.0),
                "in_capture": row["in_capture_window"] == "1",
            })
    return rows

# Group runs by scenario class
runs = {}     # {scenario: [(param, rows), ...]}
nominal_rows = None
for csv_path in sorted(glob.glob(os.path.join(RENDERS_DIR, "anim_*", "metrics.csv"))):
    name = os.path.basename(os.path.dirname(csv_path)).replace("anim_", "")
    rows = load_csv(csv_path)
    if name == "nominal":
        nominal_rows = rows
        continue
    # parse scenario + param (e.g. A1_lag_10 -> scenario=A1_lag, param=10)
    m = re.match(r"([A-Z]\d_\w+?)_(\d+(?:p\d+)?)$", name)
    if not m:
        print(f"WARN: cannot parse {name}"); continue
    scen, p_str = m.group(1), m.group(2).replace('p', '.')
    param = float(p_str)
    runs.setdefault(scen, []).append((param, rows))

for s in runs:
    runs[s].sort(key=lambda x: x[0])

# Build "nominal-equivalent" inside each scenario: the param=0 case
nominal_per_scen = {s: dict(runs[s])[0.0] if 0.0 in dict(runs[s]) else None
                    for s in runs}

# ============================================================
# Figure 1: 3-panel margin overlay
# ============================================================
scen_titles = {
    "A1_lag":   "A1 -- Feeder lag (deg)",
    "B1_slack": "B1 -- Slack (mm yarn below nominal)",
    "D1_miss":  "D1 -- Missed capture (mm yarn above nominal)",
}

fig, axes = plt.subplots(3, 1, figsize=(14, 11), sharex=True)
for ax, scen in zip(axes, ["A1_lag", "B1_slack", "D1_miss"]):
    pairs = runs.get(scen, [])
    if not pairs:
        ax.text(0.5, 0.5, f"no runs for {scen}", transform=ax.transAxes); continue
    params = [p for p,_ in pairs]
    cmap = cm.get_cmap('viridis')
    for i, (p, rows) in enumerate(pairs):
        thetas = [r["theta"] for r in rows]
        margins = [r["margin_z"] for r in rows]
        color = cmap(i / max(1, len(pairs) - 1))
        ax.plot(thetas, margins, color=color, marker='.', markersize=3,
                label=f"{p:g}", linewidth=1.5 if p == 0 else 1.0,
                alpha=0.4 if p == 0 else 0.85)
    ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
    ax.set_title(scen_titles.get(scen, scen))
    ax.set_ylabel("Capture margin Z (mm)")
    ax.grid(True, alpha=0.3)
    ax.legend(title="parameter", loc='upper right', fontsize=8, ncol=2)
    # Mark feeder positions
    for ft, lbl in [(0, "F1"), (180, "F4")]:
        ax.axvline(ft, color='red', alpha=0.25, linewidth=1)
        ax.text(ft, ax.get_ylim()[1]*0.85, lbl, ha='center', fontsize=8, color='red')

axes[-1].set_xlabel("Cylinder rotation theta_cyl (deg)")
axes[-1].set_xticks(range(0, 361, 30))

plt.suptitle("CSM V3 Phase 1.5 D-4b -- capture margin sweeps", fontsize=13)
plt.tight_layout()
out1 = os.path.join(RENDERS_DIR, "capture_margin_plot.png")
plt.savefig(out1, dpi=110)
plt.close()
print(f"Saved {out1}")

# ============================================================
# Figure 2: peak deviation per parameter -- the engineering envelope
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, scen in zip(axes, ["A1_lag", "B1_slack", "D1_miss"]):
    pairs = runs.get(scen, [])
    if not pairs: continue
    xs = [p for p,_ in pairs]
    # For each run, find the WORST-CASE margin during the capture window
    # (most negative = catastrophic; max absolute = unstable boundary)
    min_margins = []
    max_margins = []
    max_abs = []
    for p, rows in pairs:
        in_win = [r["margin_z"] for r in rows if r["in_capture"]]
        if in_win:
            min_margins.append(min(in_win))
            max_margins.append(max(in_win))
            max_abs.append(max(abs(r) for r in in_win))
        else:
            min_margins.append(float('nan')); max_margins.append(float('nan'))
            max_abs.append(float('nan'))
    ax.plot(xs, min_margins, 'o-', color='blue', label='min (yarn below)')
    ax.plot(xs, max_margins, 's-', color='red',  label='max (yarn above)')
    ax.plot(xs, max_abs,     'd--', color='black', label='max |margin|', alpha=0.6)
    ax.axhline(0, color='gray', linewidth=0.8)
    # Suggest threshold lines
    ax.axhline(2,  color='green', linestyle=':', alpha=0.4, label='+/- 2 mm (acceptable)')
    ax.axhline(-2, color='green', linestyle=':', alpha=0.4)
    ax.axhline(5,  color='orange', linestyle=':', alpha=0.4, label='+/- 5 mm (degraded)')
    ax.axhline(-5, color='orange', linestyle=':', alpha=0.4)
    ax.set_title(scen_titles.get(scen, scen))
    ax.set_xlabel("parameter value")
    ax.set_ylabel("worst-case margin Z (mm)")
    ax.legend(loc='best', fontsize=8)
    ax.grid(True, alpha=0.3)

plt.suptitle("CSM V3 Phase 1.5 D-4b -- operating envelope per failure mode", fontsize=13)
plt.tight_layout()
out2 = os.path.join(RENDERS_DIR, "operating_envelope_plot.png")
plt.savefig(out2, dpi=110)
plt.close()
print(f"Saved {out2}")

print("\nSweep summary table:")
print("-" * 70)
for scen in ["A1_lag", "B1_slack", "D1_miss"]:
    pairs = runs.get(scen, [])
    if not pairs: continue
    print(f"{scen}:")
    for p, rows in pairs:
        in_win = [r["margin_z"] for r in rows if r["in_capture"]]
        if in_win:
            print(f"  param={p:5g}   margin Z worst-case: "
                  f"[{min(in_win):+6.2f}, {max(in_win):+6.2f}]  "
                  f"max|m| = {max(abs(m) for m in in_win):5.2f} mm")
