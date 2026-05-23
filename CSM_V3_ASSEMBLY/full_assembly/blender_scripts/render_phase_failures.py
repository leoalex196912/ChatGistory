# -*- coding: utf-8 -*-
"""
CSM V3 -- Phase 1.5 D-2 FAILURE MODE TAXONOMY (8 scenarios)

Structured around four failure classes, each corresponding to a
fundamentally different physical mechanism:

  CLASS A -- TIMING failures (phase relationship errors)
    A1 Feeder lag         feeder phase +10 deg from nominal
    A2 Hook outrun        narrower cam bump (faster effective transit)
    A3 Belt oscillation   sinusoidal phase jitter (resonance / windup)

  CLASS B -- TENSION failures (material state instability)
    B1 Slack loop         delayed take-down -> yarn drops below hook plane
    B2 Over-tension       excessive downward pull -> straightened yarn

  CLASS C -- GEOMETRIC interference (spatial violation)
    C1 Retainer interference   needle_Z exceeds allowed peak (overlift)
    C2 Feeder intrusion        nozzle moved radially inward into hook zone

  CLASS D -- CAPTURE failures (loss of loop ownership)
    D1 Missed capture     yarn endpoint above hook sweep (no contact)
    D2 Double-feed        two yarn states simultaneously accessible

Each render is captured at the most-informative cylinder phase for
that scenario (typically near the F1 capture moment, theta_cyl ~ 0).

The point is NOT pretty pictures -- it is to derive safe operating
envelopes from observed behavior:
   - minimum capture margin
   - allowable feeder lag
   - allowable backlash
   - allowable belt elasticity
   - allowable tension variance

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_phase_failures.py
"""
import bpy, math, sys, os
from mathutils import Vector

sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

mm = 0.001

# ============================================================
# RESET + HELPERS (same shape as phase_snapshots)
# ============================================================
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
    'cyl_ghost':   mk("CylGhost",   (0.85,0.86,0.88,0.50), 0.30, alpha=0.50),
    'retainer':    mk("Ret",        (0.95,0.85,0.55,0.55), 0.50, alpha=0.55),
    'sinker':      mk("Sink",       (0.50,0.55,0.60,1),    0.40),
    'cassette':    mk("Cass",       (0.55,0.55,0.60,0.40), 0.40, alpha=0.40),
    'cam':         mk("Cam",        (0.10,0.10,0.12,1),    0.25, 0.5),
    'feeder':      mk("Feeder",     (0.80,0.72,0.45,0.85), 0.45, alpha=0.85),
    'cone_r':      mk("ConeR",      (0.78,0.10,0.10,1),    0.85),
    'cone_b':      mk("ConeB",      (0.10,0.25,0.85,1),    0.85),
    'needle':      mk("Needle",     (1.00,0.10,0.05,1),    0.40, emit=1.5),
    'yarn':        mk("Yarn",       (0.98,0.18,0.10,1),    0.50, emit=0.8),
    'yarn_idle':   mk("YarnIdle",   (0.30,0.45,0.95,1),    0.50, emit=0.4),
    # Failure indicators
    'fail_red':    mk("FailRed",    (1.00,0.05,0.05,1),    0.30, emit=3.0),
    'fail_yellow': mk("FailYell",   (1.00,0.95,0.10,1),    0.30, emit=2.5),
    'fail_orange': mk("FailOrng",   (1.00,0.50,0.05,1),    0.30, emit=2.0),
    'ground':      mk("Ground",     (0.10,0.12,0.16,1),    0.70),
}

# ============================================================
# LOAD GEOMETRY
# ============================================================
print("Loading geometry...")
L = r"C:\3D-Project\01_MECHANICAL"
A = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
WZ = MD.CYL_BOTTOM_WORLD_Z

imp("Cylinder", os.path.join(L,"02_CASSETTE_HEAD","cylinder","CSM_V3_Cylinder_V3_0_FULL.stl"), t_mm=(0,0,WZ),     mat=M['cyl_ghost'])
imp("CamRing",  os.path.join(L,"02_CASSETTE_HEAD","cam_ring","CSM_V3_CamRing_V6_5_FULL.stl"),  t_mm=(0,0,19+WZ),  mat=M['cam'])
imp("Cassette", os.path.join(L,"02_CASSETTE_HEAD","cassette_base","CSM_V3_CassetteBase_V1_1_FULL.stl"), t_mm=(0,0,49+WZ), mat=M['cassette'])
imp("Sinker",   os.path.join(L,"02_CASSETTE_HEAD","sinker_ring","CSM_V3_SinkerRing_V1_2_1_FULL.stl"),   t_mm=(0,0,75+WZ), mat=M['sinker'])
imp("Retainer", os.path.join(L,"02_CASSETTE_HEAD","retainer_ring","CSM_V3_RetainerRing_V1_0_FULL.stl"), t_mm=(0,0,83+WZ), mat=M['retainer'])

FRO = MD.PCD_FEEDER/2 + 25.0
feeder_F1 = imp("Feeder_F1", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"), t_mm=(FRO,0,0), rz_deg=-90, mat=M['feeder'])
imp("Feeder_F4", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"), t_mm=(-FRO,0,0), rz_deg=+90, mat=M['feeder'])
imp("YarnCone_F1", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"), t_mm=(FRO,20,250), mat=M['cone_r'])
imp("YarnCone_F4", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"), t_mm=(-FRO,-20,250), mat=M['cone_b'])

# Tracked needle marker
bpy.ops.mesh.primitive_cone_add(radius1=0.0015, radius2=0.0, depth=0.020,
                                location=(0.057, 0, 0.264))
needle_obj = bpy.context.active_object; needle_obj.name = "TrackedNeedle"
assign(needle_obj, M['needle'])

# Failure marker (sphere repositioned per scenario)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.005, location=(0,0,0.32))
fail_mark = bpy.context.active_object; fail_mark.name = "FailureMarker"
assign(fail_mark, M['fail_red'])

# Ground
bpy.ops.mesh.primitive_plane_add(size=1.5, location=(0,0,-0.005))
g = bpy.context.active_object; g.name = "Ground"
assign(g, M['ground'])

# Lighting
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
    bg.inputs[0].default_value = (0.08,0.10,0.14,1.0)
    bg.inputs[1].default_value = 0.30

# Render settings
scene = bpy.context.scene
try:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    try: scene.cycles.device = 'GPU'
    except Exception: pass
except Exception:
    for cand in ['BLENDER_EEVEE_NEXT','BLENDER_EEVEE']:
        try: scene.render.engine = cand; break
        except Exception: continue
scene.render.resolution_x = 1280
scene.render.resolution_y = 800
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -0.5

OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"

# Camera
bpy.ops.object.camera_add(location=(0.25, -0.25, 0.40))
cam = bpy.context.active_object; cam.name = "FailureCam"
cam.data.lens = 60
target = Vector((0,0,0.27))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z','Y').to_euler()
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
# NOMINAL constants (yarn waypoints + cam profile)
# ============================================================
NOMINAL_HOOK_X = MD.CYL_OD/2 - 1.0          # 56.15
NOMINAL_HOOK_Z = MD.world_z(MD.HOOK_PEAK_Z) # 264
FEED_NOZZLE_R = MD.PCD_FEEDER/2 + 5.0       # 100
FEED_NOZZLE_Z = MD.world_z(MD.FEEDER_REFERENCE_Z)   # 271
F1_CONE_X = FRO; F1_CONE_Y = 20; F1_CONE_Z = 330

def nominal_yarn_pts(needle_xyz, feeder_theta_deg=0.0):
    fr = math.radians(feeder_theta_deg)
    fx = FEED_NOZZLE_R * math.cos(fr)
    fy = FEED_NOZZLE_R * math.sin(fr)
    cx = FRO * math.cos(fr)
    cy_off = 20.0 if feeder_theta_deg == 0 else -20.0
    return [
        (cx, cy_off, F1_CONE_Z),
        (cx, cy_off, 280.0),
        (fx + 5*math.cos(fr), fy + 5*math.sin(fr), FEED_NOZZLE_Z + 8),
        (fx, fy, FEED_NOZZLE_Z),
        (needle_xyz[0] + 8*math.cos(fr), needle_xyz[1] + 8*math.sin(fr), needle_xyz[2] + 4),
        needle_xyz,
    ]

# ============================================================
# SCENARIO RENDER FUNCTION
# ============================================================
def render_scenario(scenario_id, label, needle_xyz, yarn_pts, fail_marker_xyz=None,
                    fail_mat=None, extra_yarn=None):
    """Render one failure scenario.
       needle_xyz: (x,y,z) of needle hook tip in mm
       yarn_pts: list of (x,y,z) mm for the yarn Bezier curve
       fail_marker_xyz: optional (x,y,z) for a failure indicator sphere
       fail_mat: material for the failure marker
       extra_yarn: optional second yarn curve points (for D2)
    """
    # Position needle (cone tip at needle_xyz, offset -10mm so tip ends at xyz)
    needle_obj.location = (needle_xyz[0]*mm, needle_xyz[1]*mm,
                            needle_xyz[2]*mm - 0.010)

    # Update primary yarn
    make_yarn("YarnPrimary", yarn_pts, thickness_mm=1.2, mat=M['yarn'])

    # Optional secondary yarn (D2)
    if extra_yarn is not None:
        make_yarn("YarnSecondary", extra_yarn, thickness_mm=1.2, mat=M['yarn_idle'])
    else:
        old = bpy.data.objects.get("YarnSecondary")
        if old: bpy.data.objects.remove(old, do_unlink=True)

    # Position + color failure marker (or hide if None)
    if fail_marker_xyz is not None:
        fail_mark.location = (fail_marker_xyz[0]*mm, fail_marker_xyz[1]*mm,
                              fail_marker_xyz[2]*mm)
        fail_mark.hide_render = False
        if fail_mat is not None:
            assign(fail_mark, fail_mat)
    else:
        fail_mark.hide_render = True

    # Render
    out_path = os.path.join(OUT_DIR, f"CSM_V3_Phase15_Failure_{scenario_id}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print(f"  [{scenario_id}] {label}  -> {os.path.basename(out_path)} ({sz/1024:.0f} KB)")

# ============================================================
# CLASS A -- TIMING FAILURES
# ============================================================

# A1 -- Feeder lag (+10 deg): yarn hasn't reached hook yet at peak cam
# Needle is at peak (HOOK_PEAK_Z) at theta_cyl=0, but feeder is delayed
# by 10 deg, so its nozzle is at theta=+10 -- yarn still hanging at nozzle
print("\nA1 Feeder lag (+10 deg)")
needle_pos = (NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z)
lag_angle = 10.0
# Feeder F1 is now at θ=lag_angle. Yarn endpoint is at the lagged nozzle (still presenting)
lag_rad = math.radians(lag_angle)
lag_fx = FEED_NOZZLE_R * math.cos(lag_rad)
lag_fy = FEED_NOZZLE_R * math.sin(lag_rad)
lag_yarn = [
    (F1_CONE_X * math.cos(lag_rad), 20*math.cos(lag_rad), F1_CONE_Z),
    (F1_CONE_X * math.cos(lag_rad), 20*math.cos(lag_rad), 280),
    (lag_fx + 5, lag_fy + 1, FEED_NOZZLE_Z + 8),
    (lag_fx, lag_fy, FEED_NOZZLE_Z),
    # Yarn doesn't reach the hook -- ends 15 mm away
    (lag_fx - 8, lag_fy - 1.4, FEED_NOZZLE_Z - 4),
]
# Failure marker between feeder and hook (showing the GAP)
gap_marker = ((NOMINAL_HOOK_X + lag_fx) / 2, 4, NOMINAL_HOOK_Z + 2)
render_scenario("A1_feeder_lag", "feeder phase +10 deg, capture gap",
                needle_pos, lag_yarn, fail_marker_xyz=gap_marker,
                fail_mat=M['fail_red'])

# A2 -- Hook outrun (narrower bump): needle has already descended past peak
# At theta_cyl = 15 (well past nominal peak), needle should still be elevated
# but with narrower bump it's already back at Z_low
print("\nA2 Hook outrun (narrow cam bump)")
outrun_theta = 15.0
# Slot #0 position at theta=15
or_rad = math.radians(outrun_theta)
n_x = (MD.CYL_OD/2 - 1.0) * math.cos(or_rad)
n_y = (MD.CYL_OD/2 - 1.0) * math.sin(or_rad)
# Narrow bump => needle already low at theta=15
n_z = MD.world_z(MD.CYLINDER_TOP_Z)  # 256, descended
# Yarn arrived too late -- still at hook plane (z=264) but no needle there
late_yarn = nominal_yarn_pts((NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z), feeder_theta_deg=0)
render_scenario("A2_hook_outrun", "narrow cam bump, needle descended before yarn arrived",
                (n_x, n_y, n_z), late_yarn,
                fail_marker_xyz=(NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z + 2),
                fail_mat=M['fail_orange'])

# A3 -- Belt torsional oscillation: phase jitter +/- 5 deg
# At nominal theta=0, actual theta = +4 deg due to torsional windup
print("\nA3 Belt torsional oscillation")
jitter_theta = 4.0
j_rad = math.radians(jitter_theta)
n_x = (MD.CYL_OD/2 - 1.0) * math.cos(j_rad)
n_y = (MD.CYL_OD/2 - 1.0) * math.sin(j_rad)
# Cam profile: 4 deg off peak -> Z slightly reduced
# cos(pi * 4/30) ~ 0.93 (within 30 deg half-bump)
n_z_low = MD.world_z(MD.CYLINDER_TOP_Z)
n_z_high = MD.world_z(MD.HOOK_PEAK_Z)
n_z = n_z_low + (n_z_high - n_z_low) * 0.5 * (1 + math.cos(math.pi * jitter_theta / 30.0))
# Yarn still at nominal hook position (timing reference)
osc_yarn = nominal_yarn_pts((NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z), feeder_theta_deg=0)
render_scenario("A3_belt_oscillation", "belt windup +4 deg phase shift",
                (n_x, n_y, n_z), osc_yarn,
                fail_marker_xyz=(n_x, n_y + 4, n_z + 2),
                fail_mat=M['fail_yellow'])

# ============================================================
# CLASS B -- TENSION FAILURES
# ============================================================

# B1 -- Slack loop: take-down delayed, yarn drops BELOW hook plane
# after capture (so loop balloons inside the cylinder bore)
print("\nB1 Slack loop formation")
slack_needle = (NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z)
# Yarn proceeds through hook but then drops too low (slack ballooning down)
slack_yarn = nominal_yarn_pts(slack_needle, feeder_theta_deg=0)
# Extend: yarn continues from hook, ballooning down INSIDE cylinder bore
slack_yarn.append((NOMINAL_HOOK_X - 20, 0, NOMINAL_HOOK_Z - 30))   # droops down
slack_yarn.append((0, 0, NOMINAL_HOOK_Z - 50))                       # at cylinder bore
slack_yarn.append((0, 0, MD.world_z(MD.CYLINDER_Z0) + 50))           # mid-cylinder bore
render_scenario("B1_slack_loop", "delayed take-down, yarn balloons in bore",
                slack_needle, slack_yarn,
                fail_marker_xyz=(0, 0, NOMINAL_HOOK_Z - 30),
                fail_mat=M['fail_yellow'])

# B2 -- Over-tension: yarn from feeder is pulled too tight to take-down
# Path is straightened, hook load is high
print("\nB2 Over-tension")
tight_needle = (NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z)
# Yarn goes straight from feeder, through hook, then straight DOWN
tight_yarn = [
    (F1_CONE_X, 20, F1_CONE_Z),
    (F1_CONE_X, 20, 280),
    (FEED_NOZZLE_R + 5, 0, FEED_NOZZLE_Z + 8),
    (FEED_NOZZLE_R, 0, FEED_NOZZLE_Z),
    (NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z),
    # Tight straight pull DOWN inside cylinder
    (NOMINAL_HOOK_X - 5, 0, NOMINAL_HOOK_Z - 30),
    (0, 0, MD.world_z(MD.CYLINDER_Z0)),
]
render_scenario("B2_over_tension", "excessive take-down pull, yarn straightened",
                tight_needle, tight_yarn,
                fail_marker_xyz=(NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z),
                fail_mat=M['fail_orange'])

# ============================================================
# CLASS C -- GEOMETRIC INTERFERENCE
# ============================================================

# C1 -- Retainer interference: needle Z exceeds allowable peak,
# hook collides with retainer lip underside (at Z=270)
print("\nC1 Retainer interference")
retainer_lip_z = MD.world_z(MD.HOOK_PEAK_Z) + 6.0   # 270
overlift_needle = (NOMINAL_HOOK_X, 0, retainer_lip_z + 1)   # 1mm INTO lip
overlift_yarn = nominal_yarn_pts(overlift_needle, feeder_theta_deg=0)
render_scenario("C1_retainer_interference", "needle overlift collides with retainer lip",
                overlift_needle, overlift_yarn,
                fail_marker_xyz=(NOMINAL_HOOK_X, 0, retainer_lip_z + 1),
                fail_mat=M['fail_red'])

# C2 -- Feeder intrusion: feeder nozzle radially inward into hook zone
# Show with a "shifted" yarn path: nozzle at radius 50 (inside cylinder OD=57)
print("\nC2 Feeder intrusion")
intrusion_needle = (NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z)
# Feeder nozzle pretending to be at radius 50 (inside cylinder OD!)
INTRUSION_R = 50.0
intrusion_yarn = [
    (F1_CONE_X, 20, F1_CONE_Z),
    (F1_CONE_X, 20, 280),
    (INTRUSION_R + 10, 0, FEED_NOZZLE_Z + 4),
    (INTRUSION_R, 0, FEED_NOZZLE_Z),     # nozzle is INSIDE cylinder OD!
    (NOMINAL_HOOK_X - 5, 0, NOMINAL_HOOK_Z),
    intrusion_needle,
]
render_scenario("C2_feeder_intrusion", "nozzle moved inward into hook zone",
                intrusion_needle, intrusion_yarn,
                fail_marker_xyz=(INTRUSION_R, 0, FEED_NOZZLE_Z),
                fail_mat=M['fail_red'])

# ============================================================
# CLASS D -- CAPTURE FAILURES
# ============================================================

# D1 -- Missed capture: yarn endpoint stays ABOVE hook sweep envelope
# Needle reaches peak but yarn doesn't dip low enough to be caught
print("\nD1 Missed capture")
missed_needle = (NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z)
# Yarn floats above the hook plane by 8mm -- never contacts needle
missed_yarn = [
    (F1_CONE_X, 20, F1_CONE_Z),
    (F1_CONE_X, 20, 280),
    (FEED_NOZZLE_R + 5, 0, FEED_NOZZLE_Z + 8),
    (FEED_NOZZLE_R, 0, FEED_NOZZLE_Z),
    (NOMINAL_HOOK_X + 12, 2, NOMINAL_HOOK_Z + 12),  # too high, missing hook
    (NOMINAL_HOOK_X + 8, -2, NOMINAL_HOOK_Z + 10),
]
render_scenario("D1_missed_capture", "yarn endpoint above hook sweep, missed catch",
                missed_needle, missed_yarn,
                fail_marker_xyz=(NOMINAL_HOOK_X + 5, 0, NOMINAL_HOOK_Z + 11),
                fail_mat=M['fail_red'])

# D2 -- Double-feed: two yarn states simultaneously near hook
# F1 yarn captured + leftover F4 yarn from previous revolution also present
print("\nD2 Double-feed")
df_needle = (NOMINAL_HOOK_X, 0, NOMINAL_HOOK_Z)
primary_yarn = nominal_yarn_pts(df_needle, feeder_theta_deg=0)
# Secondary "stray" yarn from F4 still draped near hook (shouldn't be)
secondary_yarn = [
    (-FRO, -20, F1_CONE_Z),
    (-FRO, -20, 280),
    (-FEED_NOZZLE_R, 0, FEED_NOZZLE_Z),
    # Stray F4 yarn loops back toward F1's hook (impossible but illustrates fault)
    (-20, 0, NOMINAL_HOOK_Z + 5),
    (NOMINAL_HOOK_X - 3, -2, NOMINAL_HOOK_Z + 2),
]
render_scenario("D2_double_feed", "two yarn states accessible -- jam precursor",
                df_needle, primary_yarn,
                fail_marker_xyz=(NOMINAL_HOOK_X - 2, -1, NOMINAL_HOOK_Z + 3),
                fail_mat=M['fail_yellow'],
                extra_yarn=secondary_yarn)

# Save final .blend
blend_path = os.path.join(OUT_DIR, "CSM_V3_Phase15_Failures.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")
print("\nDONE -- 8 failure-mode scenarios.")
print("\nNext step: derive safe operating envelopes from these failures:")
print("  - allowable feeder lag (A1)            <  ?  deg")
print("  - minimum cam bump width  (A2)         >  ?  deg")
print("  - allowable belt phase jitter (A3)     <  ?  deg")
print("  - allowable take-down lag (B1)         <  ?  ms")
print("  - allowable tension peak (B2)          <  ?  N")
print("  - retainer lip vertical clearance (C1) >  ?  mm")
print("  - feeder nozzle inboard limit (C2)     >  ?  mm")
print("  - hook-yarn vertical capture margin    >  ?  mm")
print("These numerical tolerances go into DYNAMIC_BEHAVIOR_AND_COMPLIANCE.md.")
