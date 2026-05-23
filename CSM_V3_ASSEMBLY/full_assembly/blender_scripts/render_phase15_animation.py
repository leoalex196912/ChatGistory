# -*- coding: utf-8 -*-
"""
CSM V3 -- Phase 1.5 D-4 BEHAVIORAL SIMULATOR (first pass, NOMINAL)

Not "rendering animation" -- this is the first behavioral simulator.
Three tracks computed per frame:

   1. MECHANICAL STATE (rigid-body):
      - cylinder angle theta_cyl
      - tracked needle (Slot #0) position (X, Y, Z)
      - hook engagement state

   2. YARN STATE (material):
      - yarn endpoint position
      - ownership (which feeder owns it)
      - capture state (captured / approaching / parked)

   3. ERROR STATE (system health):
      - capture margin (vertical distance yarn-to-hook at capture window)
      - phase from nearest feeder
      - whether failure-mode conditions are met

All three tracks are written to a CSV per frame so post-processing
(plot, analysis, comparison with failure variants) can derive numerical
tolerances without re-rendering.

DELIBERATELY exaggerated and slow -- interpretability > realism for D-4.

Output:
  PNG sequence at full_assembly/renders/anim_nominal/frame_NNNN.png
  CSV at        full_assembly/renders/anim_nominal/metrics.csv

ffmpeg post-step (run manually after this script):
  ffmpeg -framerate 12 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p
         -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" anim_nominal.mp4

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_phase15_animation.py
"""
import bpy, math, sys, os, csv
from mathutils import Vector

sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

mm = 0.001

# ============================================================
# KINEMATIC MODEL (same as D-1 baseline)
# ============================================================
FEEDER_THETAS = (0.0, 180.0)
CAM_BUMP_DEG  = 60.0   # 60-deg engagement zone per feeder

def needle_Z(theta_cyl):
    """Vertical position of Slot #0 needle hook tip."""
    Z_low  = MD.world_z(MD.CYLINDER_TOP_Z)
    Z_high = MD.world_z(MD.HOOK_PEAK_Z)
    distances = []
    for f in FEEDER_THETAS:
        d = (theta_cyl - f) % 360.0
        if d > 180: d = 360 - d
        distances.append(d)
    dmin = min(distances)
    if dmin <= CAM_BUMP_DEG / 2:
        x = dmin / (CAM_BUMP_DEG / 2)
        bump = 0.5 * (1.0 + math.cos(math.pi * x))
        return Z_low + (Z_high - Z_low) * bump
    return Z_low

def needle_XY(theta_cyl):
    r = MD.CYL_OD/2.0 - 1.0
    rad = math.radians(theta_cyl)
    return (r * math.cos(rad), r * math.sin(rad))

def yarn_state(theta_cyl):
    """Determine which feeder owns yarn + endpoint XYZ + capture flag."""
    for f in FEEDER_THETAS:
        d = (theta_cyl - f) % 360.0
        if d > 180: d = 360 - d
        if d <= 30.0:    # within capture window
            nx, ny = needle_XY(theta_cyl)
            return {
                'owner': f,
                'state': 'captured',
                'endpoint': (nx, ny, needle_Z(theta_cyl)),
                'angular_dist': d,
            }
    # Idle -- parked at last feeder swept past
    last_f = FEEDER_THETAS[0]
    last_d = 360
    for f in FEEDER_THETAS:
        d = (theta_cyl - f) % 360.0
        if 0 < d < last_d:
            last_d = d; last_f = f
    fr = math.radians(last_f)
    fr_x = (MD.PCD_FEEDER/2 + 5.0) * math.cos(fr)
    fr_y = (MD.PCD_FEEDER/2 + 5.0) * math.sin(fr)
    return {
        'owner': last_f,
        'state': 'idle_at_feeder',
        'endpoint': (fr_x, fr_y, MD.world_z(MD.FEEDER_REFERENCE_Z)),
        'angular_dist': last_d,
    }

def capture_margin_mm(theta_cyl):
    """Vertical distance (mm) between yarn endpoint and the needle hook.
    Positive = yarn ABOVE hook (waiting to be caught).
    Zero     = yarn AT hook plane (being caught).
    Negative = yarn BELOW hook (potentially missed or already pulled through).
    Only meaningful inside the capture window (dist <= 30 deg)."""
    nz = needle_Z(theta_cyl)
    ys = yarn_state(theta_cyl)
    yz = ys['endpoint'][2]
    return yz - nz

# ============================================================
# SCENE BUILD
# ============================================================
print("Resetting scene...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for m in list(bpy.data.materials):   bpy.data.materials.remove(m)

def mk(name, base=(0.7,0.7,0.72,1), rough=0.4, metal=0.0, alpha=1.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = base
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            if "Alpha" in n.inputs:
                n.inputs["Alpha"].default_value = alpha
                if alpha < 1.0: m.blend_method = 'BLEND'
            if emit > 0:
                if "Emission Strength" in n.inputs:
                    n.inputs["Emission Strength"].default_value = emit
                if "Emission Color" in n.inputs:
                    n.inputs["Emission Color"].default_value = base
            return m
    return m

def assign(o, mat):
    o.data.materials.clear(); o.data.materials.append(mat)

def imp(name, path, t_mm=(0,0,0), rz_deg=0, mat=None):
    if not os.path.exists(path): return None
    before = set(bpy.data.objects)
    if hasattr(bpy.ops.wm,"stl_import"): bpy.ops.wm.stl_import(filepath=path)
    else: bpy.ops.import_mesh.stl(filepath=path)
    new = list(set(bpy.data.objects) - before)
    if not new: return None
    o = new[0]; o.name = name
    o.scale = (mm,mm,mm)
    o.location = (t_mm[0]*mm, t_mm[1]*mm, t_mm[2]*mm)
    if rz_deg: o.rotation_euler = (0,0,math.radians(rz_deg))
    if mat: assign(o, mat)
    bpy.context.view_layer.update()
    return o

# Materials
M = {
    'cyl_ghost':  mk("Cyl",     (0.85,0.86,0.88,0.50), 0.30, alpha=0.50),
    'retainer':   mk("Ret",     (0.95,0.85,0.55,0.55), 0.50, alpha=0.55),
    'sinker':     mk("Sink",    (0.50,0.55,0.60,1),    0.40),
    'cassette':   mk("Cass",    (0.55,0.55,0.60,0.40), 0.40, alpha=0.40),
    'cam':        mk("Cam",     (0.10,0.10,0.12,1),    0.25, 0.5),
    'feeder':     mk("Feeder",  (0.80,0.72,0.45,0.85), 0.45, alpha=0.85),
    'cone_r':     mk("ConeR",   (0.78,0.10,0.10,1),    0.85),
    'cone_b':     mk("ConeB",   (0.10,0.25,0.85,1),    0.85),
    'needle':     mk("Needle",  (1.00,0.10,0.05,1),    0.40, emit=1.5),
    'yarn_active':mk("Yarn",    (0.98,0.18,0.10,1),    0.50, emit=0.8),
    'yarn_idle':  mk("YarnI",   (0.30,0.45,0.95,1),    0.50, emit=0.4),
    'slot0':      mk("Slot0",   (1.00,0.95,0.10,1),    0.30, emit=0.5),
    'ground':     mk("Ground",  (0.08,0.10,0.14,1),    0.65),
}

print("Loading geometry...")
L = r"C:\3D-Project\01_MECHANICAL"
A = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
WZ = MD.CYL_BOTTOM_WORLD_Z

imp("Cylinder", os.path.join(L,"02_CASSETTE_HEAD","cylinder","CSM_V3_Cylinder_V3_0_FULL.stl"),    t_mm=(0,0,WZ),   mat=M['cyl_ghost'])
imp("CamRing",  os.path.join(L,"02_CASSETTE_HEAD","cam_ring","CSM_V3_CamRing_V6_5_FULL.stl"),     t_mm=(0,0,19+WZ),mat=M['cam'])
imp("Cassette", os.path.join(L,"02_CASSETTE_HEAD","cassette_base","CSM_V3_CassetteBase_V1_1_FULL.stl"), t_mm=(0,0,49+WZ), mat=M['cassette'])
imp("Sinker",   os.path.join(L,"02_CASSETTE_HEAD","sinker_ring","CSM_V3_SinkerRing_V1_2_1_FULL.stl"),   t_mm=(0,0,75+WZ), mat=M['sinker'])
imp("Retainer", os.path.join(L,"02_CASSETTE_HEAD","retainer_ring","CSM_V3_RetainerRing_V1_0_FULL.stl"), t_mm=(0,0,83+WZ), mat=M['retainer'])
FRO = MD.PCD_FEEDER/2 + 25.0
imp("Feeder_F1", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"), t_mm=(FRO,0,0),  rz_deg=-90, mat=M['feeder'])
imp("Feeder_F4", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"), t_mm=(-FRO,0,0), rz_deg=+90, mat=M['feeder'])
imp("YarnCone_F1", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"), t_mm=(FRO,20,250),   mat=M['cone_r'])
imp("YarnCone_F4", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"), t_mm=(-FRO,-20,250), mat=M['cone_b'])

# Tracked needle marker (Slot #0)
bpy.ops.mesh.primitive_cone_add(radius1=0.0015, radius2=0.0, depth=0.020,
                                location=(0.057, 0, 0.264))
needle_obj = bpy.context.active_object; needle_obj.name = "TrackedNeedle"
assign(needle_obj, M['needle'])

# Slot #0 sphere marker (visible-from-top marker)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.004, location=(0.057, 0, 0.245))
slot0_marker = bpy.context.active_object; slot0_marker.name = "Slot0Marker"
assign(slot0_marker, M['slot0'])

# Ground
bpy.ops.mesh.primitive_plane_add(size=1.5, location=(0,0,-0.005))
g = bpy.context.active_object; g.name = "Ground"
assign(g, M['ground'])

# Lighting (interpretability lighting -- bright, even, no drama)
def light(name, ltype, loc, energy, rot=(0,0,0), size=0.8):
    bpy.ops.object.light_add(type=ltype, location=loc)
    L = bpy.context.active_object; L.name = name
    L.data.energy = energy
    if hasattr(L.data,'size'): L.data.size = size
    L.rotation_euler = rot

light("Sun", 'SUN', loc=(-0.3,-0.5,1.5), energy=1.5,
      rot=(math.radians(50),math.radians(-15),math.radians(30)))
light("Key", 'AREA', loc=(0.5,-0.5,0.5), energy=40,
      rot=(math.radians(-50),0,math.radians(135)), size=0.5)

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.06,0.08,0.12,1.0)
    bg.inputs[1].default_value = 0.30

# Render settings -- FAST settings for animation
scene = bpy.context.scene
try:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 16          # low for speed
    scene.cycles.use_denoising = True
    try: scene.cycles.device = 'GPU'
    except Exception: pass
except Exception:
    for cand in ['BLENDER_EEVEE_NEXT','BLENDER_EEVEE']:
        try: scene.render.engine = cand; break
        except Exception: continue
scene.render.resolution_x = 960
scene.render.resolution_y = 600
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -0.5

# Output folder
OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\anim_nominal"
os.makedirs(OUT_DIR, exist_ok=True)

# Camera (fixed throughout animation)
bpy.ops.object.camera_add(location=(0.25, -0.25, 0.40))
cam = bpy.context.active_object; cam.name = "AnimCam"
cam.data.lens = 60
cam.rotation_euler = (Vector((0,0,0.27)) - cam.location).to_track_quat('-Z','Y').to_euler()
scene.camera = cam

# Yarn curve management
def make_yarn(name, pts_mm, thickness_mm=1.2, mat=None):
    old = bpy.data.objects.get(name)
    if old: bpy.data.objects.remove(old, do_unlink=True)
    cdata = bpy.data.curves.new(name=name, type='CURVE')
    cdata.dimensions = '3D'
    cdata.bevel_depth = thickness_mm * mm
    cdata.bevel_resolution = 3
    sp = cdata.splines.new('BEZIER')
    sp.bezier_points.add(len(pts_mm) - 1)
    for i,p in enumerate(pts_mm):
        bp = sp.bezier_points[i]
        bp.co = (p[0]*mm, p[1]*mm, p[2]*mm)
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    obj = bpy.data.objects.new(name, cdata)
    bpy.context.collection.objects.link(obj)
    if mat: assign(obj, mat)
    return obj

# ============================================================
# ANIMATION LOOP
# ============================================================
N_FRAMES = 36                 # 10 deg per frame, one full revolution
THETA_PER_FRAME = 360.0 / N_FRAMES

# CSV metrics
csv_path = os.path.join(OUT_DIR, "metrics.csv")
csv_file = open(csv_path, "w", newline="")
writer = csv.writer(csv_file)
writer.writerow([
    "frame", "theta_cyl_deg",
    "needle_x_mm", "needle_y_mm", "needle_z_mm",
    "yarn_owner_deg", "yarn_state", "yarn_x_mm", "yarn_y_mm", "yarn_z_mm",
    "angular_dist_to_owner_deg",
    "capture_margin_mm",
    "in_capture_window",
])

print(f"\nRendering {N_FRAMES} frames (one cylinder revolution)...")
for i in range(N_FRAMES):
    theta = i * THETA_PER_FRAME

    # === MECHANICAL TRACK ===
    nx, ny = needle_XY(theta)
    nz = needle_Z(theta)
    needle_obj.location = (nx*mm, ny*mm, nz*mm - 0.010)
    slot0_marker.location = (nx*mm * 0.95, ny*mm * 0.95, 0.256)

    # === YARN TRACK ===
    ys = yarn_state(theta)
    yx, yy, yz = ys['endpoint']
    state = ys['state']
    owner = ys['owner']
    ang_dist = ys['angular_dist']

    # Yarn path from active feeder to endpoint
    fr = math.radians(owner)
    cone_x = FRO * math.cos(fr)
    cone_y_off = 20.0 if owner == 0.0 else -20.0
    feed_x = (MD.PCD_FEEDER/2 + 5.0) * math.cos(fr)
    feed_y = (MD.PCD_FEEDER/2 + 5.0) * math.sin(fr)
    feed_z = MD.world_z(MD.FEEDER_REFERENCE_Z)
    if state == 'captured':
        yarn_pts = [
            (cone_x, cone_y_off, 330),
            (cone_x, cone_y_off, 280),
            (feed_x + 5*math.cos(fr), feed_y + 5*math.sin(fr), feed_z + 8),
            (feed_x, feed_y, feed_z),
            (yx + 8*math.cos(fr), yy + 8*math.sin(fr), yz + 4),
            (yx, yy, yz),
        ]
    else:
        yarn_pts = [
            (cone_x, cone_y_off, 330),
            (cone_x, cone_y_off, 280),
            (feed_x + 5*math.cos(fr), feed_y + 5*math.sin(fr), feed_z + 8),
            (feed_x, feed_y, feed_z),
            (feed_x - 3*math.cos(fr), feed_y - 3*math.sin(fr), feed_z - 4),
        ]
    yarn_mat = M['yarn_active'] if state == 'captured' else M['yarn_idle']
    make_yarn("YarnDynamic", yarn_pts, thickness_mm=1.2, mat=yarn_mat)

    # === ERROR TRACK ===
    margin = capture_margin_mm(theta)
    in_capture = ang_dist <= 30.0

    # === RENDER ===
    out_path = os.path.join(OUT_DIR, f"frame_{i:04d}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)

    # === LOG CSV ===
    writer.writerow([
        i, f"{theta:.2f}",
        f"{nx:.3f}", f"{ny:.3f}", f"{nz:.3f}",
        f"{owner:.1f}", state,
        f"{yx:.3f}", f"{yy:.3f}", f"{yz:.3f}",
        f"{ang_dist:.2f}",
        f"{margin:.3f}",
        "1" if in_capture else "0",
    ])

    if i % 6 == 0 or i == N_FRAMES - 1:
        print(f"  frame {i:3d}  theta={theta:6.1f}deg  needle Z={nz:6.2f}  "
              f"state={state:18s}  margin={margin:+6.2f}mm")

csv_file.close()
print(f"\nMetrics CSV: {csv_path}")

# Save .blend (final state)
blend_path = os.path.join(OUT_DIR, "CSM_V3_Phase15_Animation_Nominal.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"Saved .blend:  {blend_path}")

print(f"\nDONE -- {N_FRAMES} frames + metrics.csv + .blend in {OUT_DIR}")
print("\nNext steps:")
print(" 1. Assemble video:")
print(f"    cd {OUT_DIR}")
print('    ffmpeg -framerate 12 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p '
      '-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" anim_nominal.mp4')
print(" 2. Plot capture_margin vs theta:")
print("    python -m matplotlib (use metrics.csv columns theta_cyl_deg + capture_margin_mm)")
print(" 3. Re-run with failure parameters (lag, jitter, etc.) for comparison")
