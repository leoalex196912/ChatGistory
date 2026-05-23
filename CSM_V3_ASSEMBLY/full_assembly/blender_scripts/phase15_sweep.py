#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSM V3 -- Phase 1.5 D-4b PARAMETER SWEEP (pure Python, no Blender)

The simulator math, extracted from render_phase15_animation.py and run
HEADLESSLY in pure Python. No Blender. No STL imports. Runs in seconds.

Generates metrics.csv per parameter combination in anim_<scenario>/ folders,
ready for plot_capture_margin.py to overlay.

Sweeps run:
  A1 Feeder lag    -- 0 (nominal), 2, 4, 6, 8, 10, 12, 15  degrees
  B1 Slack         -- 0, 2, 4, 6, 8, 12  mm below nominal yarn Z
  D1 Missed cap.   -- 0, 2, 4, 6, 8, 12, 20  mm above nominal yarn Z

This produces ~20 metrics.csv files. Plotting overlays them on the
capture_margin_plot.png to expose:
  - soft degradation threshold (where margin starts dropping)
  - unstable threshold (where margin oscillates around zero)
  - catastrophic threshold (where margin goes deeply negative or
                            yarn no longer enters capture window)
"""
import csv, os, math, sys

sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

# ============================================================
# KINEMATIC MODEL  (parameterized for sweeps)
# ============================================================
CAM_BUMP_DEG = 60.0

def needle_Z(theta_cyl, feeder_thetas=(0.0, 180.0), bump_width_deg=CAM_BUMP_DEG):
    Z_low  = MD.world_z(MD.CYLINDER_TOP_Z)
    Z_high = MD.world_z(MD.HOOK_PEAK_Z)
    distances = []
    for f in feeder_thetas:
        d = (theta_cyl - f) % 360.0
        if d > 180: d = 360 - d
        distances.append(d)
    dmin = min(distances)
    if dmin <= bump_width_deg / 2:
        x = dmin / (bump_width_deg / 2)
        bump = 0.5 * (1.0 + math.cos(math.pi * x))
        return Z_low + (Z_high - Z_low) * bump
    return Z_low

def needle_XY(theta_cyl):
    r = MD.CYL_OD/2.0 - 1.0
    rad = math.radians(theta_cyl)
    return (r * math.cos(rad), r * math.sin(rad))

def yarn_state(theta_cyl, feeder_thetas=(0.0, 180.0),
               slack_mm=0.0, miss_mm=0.0, bump_width_deg=CAM_BUMP_DEG,
               yarn_feeder_thetas=None):
    """Yarn endpoint subject to slack/miss offsets AND feeder lag.

    feeder_thetas         -- where the CAM peaks (mechanical reality, fixed)
    yarn_feeder_thetas    -- where the FEEDER actually delivers yarn
                             (may differ from cam if feeder is lagging)
    """
    if yarn_feeder_thetas is None:
        yarn_feeder_thetas = feeder_thetas
    # Yarn ownership and capture-zone check use the YARN feeder positions
    for f_yarn in yarn_feeder_thetas:
        d = (theta_cyl - f_yarn) % 360.0
        if d > 180: d = 360 - d
        if d <= 30.0:
            # Yarn endpoint is at THIS theta's needle position projected onto
            # the yarn's lagged feeder. So yarn x,y are at the cylinder
            # location where the lagged feeder is presenting -- which is
            # the hook position FOR THE SLOT CURRENTLY AT THAT FEEDER.
            # Yarn endpoint Z is the cam-driven height AT THE LAGGED FEEDER
            # ANGLE (not the current theta).
            yarn_z_at_lag = needle_Z(f_yarn, feeder_thetas, bump_width_deg)
            r = MD.CYL_OD/2.0 - 1.0
            f_rad = math.radians(f_yarn)
            yx = r * math.cos(f_rad)
            yy = r * math.sin(f_rad)
            yz = yarn_z_at_lag - slack_mm + miss_mm
            return {
                'owner': f_yarn, 'state': 'captured',
                'endpoint': (yx, yy, yz),
                'angular_dist': d,
            }
    # Idle
    last_f = feeder_thetas[0]; last_d = 360
    for f in feeder_thetas:
        d = (theta_cyl - f) % 360.0
        if 0 < d < last_d:
            last_d = d; last_f = f
    fr = math.radians(last_f)
    fr_x = (MD.PCD_FEEDER/2 + 5.0) * math.cos(fr)
    fr_y = (MD.PCD_FEEDER/2 + 5.0) * math.sin(fr)
    return {
        'owner': last_f, 'state': 'idle_at_feeder',
        'endpoint': (fr_x, fr_y, MD.world_z(MD.FEEDER_REFERENCE_Z)),
        'angular_dist': last_d,
    }

def capture_margin_mm(theta_cyl, **kwargs):
    nz = needle_Z(theta_cyl, kwargs.get('feeder_thetas', (0.0,180.0)),
                  kwargs.get('bump_width_deg', CAM_BUMP_DEG))
    ys = yarn_state(theta_cyl, **kwargs)
    return ys['endpoint'][2] - nz

# ============================================================
# SWEEP RUNNER
# ============================================================
N_FRAMES = 72   # 5 deg per frame for finer angular resolution

def run_sweep(scenario_id, param_values, param_to_kwargs, out_root):
    """Run a parameter sweep. For each param value, write metrics.csv."""
    print(f"\n=== Sweep {scenario_id} ===")
    for p in param_values:
        kwargs = param_to_kwargs(p)
        run_name = f"anim_{scenario_id}_{p:g}".replace('.', 'p')
        run_dir = os.path.join(out_root, run_name)
        os.makedirs(run_dir, exist_ok=True)
        csv_path = os.path.join(run_dir, "metrics.csv")
        with open(csv_path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow([
                "frame", "theta_cyl_deg",
                "needle_x_mm", "needle_y_mm", "needle_z_mm",
                "yarn_owner_deg", "yarn_state", "yarn_x_mm", "yarn_y_mm", "yarn_z_mm",
                "angular_dist_to_owner_deg",
                "capture_margin_mm",        # vertical (Z) error
                "capture_offset_xy_mm",     # lateral (XY) error
                "capture_3d_distance_mm",   # Euclidean total
                "in_capture_window",
            ])
            for i in range(N_FRAMES):
                theta = i * (360.0 / N_FRAMES)
                nx, ny = needle_XY(theta)
                nz = needle_Z(theta, kwargs.get('feeder_thetas', (0.0,180.0)),
                              kwargs.get('bump_width_deg', CAM_BUMP_DEG))
                ys = yarn_state(theta, **kwargs)
                yx, yy, yz = ys['endpoint']
                margin = yz - nz
                offset_xy = math.sqrt((yx - nx)**2 + (yy - ny)**2)
                dist_3d = math.sqrt(offset_xy**2 + margin**2)
                w.writerow([
                    i, f"{theta:.2f}",
                    f"{nx:.3f}", f"{ny:.3f}", f"{nz:.3f}",
                    f"{ys['owner']:.1f}", ys['state'],
                    f"{yx:.3f}", f"{yy:.3f}", f"{yz:.3f}",
                    f"{ys['angular_dist']:.2f}",
                    f"{margin:+.3f}",
                    f"{offset_xy:.3f}",
                    f"{dist_3d:.3f}",
                    "1" if ys['angular_dist'] <= 30 else "0",
                ])
        # Quick summary of this run
        with open(csv_path, "r") as fh:
            rdr = csv.DictReader(fh)
            rows_in = [r for r in rdr if r["in_capture_window"] == "1"]
        if rows_in:
            margins = [float(r["capture_margin_mm"]) for r in rows_in]
            offsets = [float(r["capture_offset_xy_mm"]) for r in rows_in]
            dists   = [float(r["capture_3d_distance_mm"]) for r in rows_in]
            print(f"  {scenario_id}={p:5g} -> {run_name}/  "
                  f"Z=[{min(margins):+.2f},{max(margins):+.2f}] "
                  f"XY=[{min(offsets):.2f},{max(offsets):.2f}] "
                  f"3D_max={max(dists):.2f} mm")
        else:
            print(f"  {scenario_id}={p:5g} -> {run_name}/  no in-window samples")

# ============================================================
# RUN SWEEPS
# ============================================================
OUT_ROOT = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"

# A1 -- Feeder LAG in degrees
# Cam stays nominal (peak at theta=0,180). YARN feeder is shifted by lag.
# This properly models "the feeder hasn't delivered yarn yet when the cam
# fired" -- a real-world phenomenon caused by mechanical compliance,
# servo timing error, or yarn-buffer drag.
run_sweep("A1_lag",
          param_values=[0, 2, 4, 6, 8, 10, 12, 15],
          param_to_kwargs=lambda p: {
              'feeder_thetas': (0.0, 180.0),                       # cam fixed
              'yarn_feeder_thetas': (0.0 + p, 180.0 + p),           # yarn lagged
          },
          out_root=OUT_ROOT)

# B1 -- Slack: yarn endpoint Z drops by slack_mm below nominal
run_sweep("B1_slack",
          param_values=[0, 2, 4, 6, 8, 12],
          param_to_kwargs=lambda p: {'slack_mm': p},
          out_root=OUT_ROOT)

# D1 -- Missed capture: yarn endpoint Z above nominal by miss_mm
run_sweep("D1_miss",
          param_values=[0, 2, 4, 6, 8, 12, 20],
          param_to_kwargs=lambda p: {'miss_mm': p},
          out_root=OUT_ROOT)

print("\n" + "=" * 70)
print("Sweeps complete. Run plot_capture_margin.py to visualize overlays.")
print("=" * 70)
