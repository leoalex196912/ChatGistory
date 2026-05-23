# -*- coding: utf-8 -*-
"""
CSM V3 -- Phase 1.5 KINEMATIC PHASE SNAPSHOTS  (Priority D, deliverable 1)

Renders the machine at 6 angular positions of cylinder rotation,
showing the tracked needle (Slot #0) progressing through its cam cycle
and the active yarn (F1, motor side) coupling to it at peak lift.

Phases captured (cylinder rotates CCW from +Z; theta_cyl is the angle
Slot #0 has rotated from its initial +X position):
   theta = 0 deg   -- Slot #0 at +X (F1 capture moment, peak cam lift)
   theta = 60 deg  -- Slot #0 past F1, descending, loop pulled
   theta = 120 deg -- Slot #0 mid-rotation, at low (Z=75)
   theta = 180 deg -- Slot #0 at -X (F4 capture if feeder active, peak)
   theta = 240 deg -- Slot #0 past F4, descending
   theta = 300 deg -- Slot #0 approaching F1 again

This is the NOMINAL motion baseline. Failure-mode variants (feeder lag,
hook outrun, slack, snag, retainer interference) will reuse this script
with adjusted parameters.

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_phase_snapshots.py
"""
import bpy, math, sys, os
from mathutils import Vector

sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

mm = 0.001

# ============================================================
# KINEMATIC MODEL (NOMINAL)
# ============================================================
# Cam lift function: Z_needle(theta) for Slot #0.
# Cam peak is centered at theta = 0 (F1 position, +X).
# Lift profile is a cosine "bump" with a 60-degree-wide engagement zone
# centered on each feeder, peaking at HOOK_PEAK_Z, returning to
# CYLINDER_TOP_Z elsewhere.

def needle_Z(theta_cyl_deg, feeder_thetas=(0.0, 180.0), bump_width_deg=60.0):
    """Z position of needle in Slot #0 at cylinder rotation angle theta_cyl."""
    Z_low  = MD.world_z(MD.CYLINDER_TOP_Z)   # 256
    Z_high = MD.world_z(MD.HOOK_PEAK_Z)      # 264
    # For each feeder, compute angular distance from Slot #0 to that feeder
    # (Slot #0 has moved CCW by theta_cyl, so its current machine-frame
    # angular position is theta_cyl. The feeder is fixed at its angle.)
    distances = []
    for f in feeder_thetas:
        d = (theta_cyl_deg - f) % 360.0
        if d > 180: d = 360 - d   # shortest angular distance
        distances.append(d)
    dmin = min(distances)
    # Inside the bump: smoothly lift
    if dmin <= bump_width_deg / 2.0:
        # Cosine bump
        x = dmin / (bump_width_deg / 2.0)   # 0..1
        bump = 0.5 * (1.0 + math.cos(math.pi * x))   # 1 at center, 0 at edge
        return Z_low + (Z_high - Z_low) * bump
    return Z_low

def slot0_position(theta_cyl_deg):
    """World XY of Slot #0 as cylinder rotates CCW by theta_cyl from +X."""
    # Slot is at cylinder OD/2 - 1 mm (just inside the slot wall, hook tip)
    r = MD.CYL_OD/2.0 - 1.0   # 56.15
    rad = math.radians(theta_cyl_deg)
    return (r * math.cos(rad), r * math.sin(rad))

def yarn_capture_point(theta_cyl_deg, feeder_thetas=(0.0, 180.0)):
    """Return the world XYZ where yarn is being captured at this phase.
    If Slot #0 is near a feeder, yarn is captured at the hook position.
    Otherwise yarn is at the feeder nozzle (idle)."""
    # Identify which feeder (if any) Slot #0 is engaging with
    for f in feeder_thetas:
        d = (theta_cyl_deg - f) % 360.0
        if d > 180: d = 360 - d
        if d <= 30.0:   # within capture range
            # Yarn end is at the hook (slot #0 position)
            x, y = slot0_position(theta_cyl_deg)
            z = needle_Z(theta_cyl_deg, feeder_thetas=feeder_thetas)
            return ("captured", f, x, y, z)
    # Not in capture range -- yarn parked at feeder nozzle of the LAST
    # feeder Slot #0 swept past
    last_feeder = None
    last_dist = 360
    for f in feeder_thetas:
        # angular distance from feeder TO slot0 (in direction of rotation)
        d = (theta_cyl_deg - f) % 360.0
        if 0 < d < last_dist:
            last_dist = d
            last_feeder = f
    if last_feeder is None:
        last_feeder = feeder_thetas[0]
    f_rad = math.radians(last_feeder)
    feed_r = MD.PCD_FEEDER/2 + 5.0
    return ("idle_at_feeder", last_feeder,
            feed_r * math.cos(f_rad),
            feed_r * math.sin(f_rad),
            MD.world_z(MD.FEEDER_REFERENCE_Z))


# ============================================================
# SCENE BUILD (called once)
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
    'cyl_ghost':   mk("CylGhost",   (0.85,0.86,0.88,0.50), 0.30, alpha=0.50),
    'retainer':    mk("Ret",        (0.95,0.85,0.55,0.65), 0.50, alpha=0.65),
    'sinker':      mk("Sink",       (0.50,0.55,0.60,1),    0.40),
    'cassette':    mk("Cass",       (0.55,0.55,0.60,0.45), 0.40, alpha=0.45),
    'cam':         mk("Cam",        (0.10,0.10,0.12,1),    0.25, 0.5),
    'feeder':      mk("Feeder",     (0.80,0.72,0.45,0.85), 0.45, alpha=0.85),
    'cone_r':      mk("ConeR",      (0.78,0.10,0.10,1),    0.85),
    'cone_b':      mk("ConeB",      (0.10,0.25,0.85,1),    0.85),
    'needle':      mk("Needle",     (1.00,0.10,0.05,1),    0.40, emit=2.0),
    'yarn':        mk("Yarn",       (0.98,0.18,0.10,1),    0.50, emit=0.8),
    'slot0':       mk("Slot0Mark",  (1.00,0.95,0.10,1),    0.30, emit=0.5),
    'phase_label_bg': mk("LabelBG", (0.05,0.05,0.08,0.95), 0.40, alpha=0.95),
    'ground':      mk("Ground",     (0.18,0.20,0.24,1),    0.65),
}

# Load minimum geometry needed
print("Loading geometry...")
L = r"C:\3D-Project\01_MECHANICAL"
A = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
WZ = MD.CYL_BOTTOM_WORLD_Z

imp("Cylinder",   os.path.join(L,"02_CASSETTE_HEAD","cylinder","CSM_V3_Cylinder_V3_0_FULL.stl"),    t_mm=(0,0,WZ),     mat=M['cyl_ghost'])
imp("CamRing",    os.path.join(L,"02_CASSETTE_HEAD","cam_ring","CSM_V3_CamRing_V6_5_FULL.stl"),     t_mm=(0,0,19+WZ),  mat=M['cam'])
imp("Cassette",   os.path.join(L,"02_CASSETTE_HEAD","cassette_base","CSM_V3_CassetteBase_V1_1_FULL.stl"), t_mm=(0,0,49+WZ), mat=M['cassette'])
imp("Sinker",     os.path.join(L,"02_CASSETTE_HEAD","sinker_ring","CSM_V3_SinkerRing_V1_2_1_FULL.stl"),   t_mm=(0,0,75+WZ), mat=M['sinker'])
imp("Retainer",   os.path.join(L,"02_CASSETTE_HEAD","retainer_ring","CSM_V3_RetainerRing_V1_0_FULL.stl"), t_mm=(0,0,83+WZ), mat=M['retainer'])
FRO = MD.PCD_FEEDER/2 + 25.0
imp("Feeder_F1",  os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"), t_mm=(FRO,0,0), rz_deg=-90, mat=M['feeder'])
imp("Feeder_F4",  os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"), t_mm=(-FRO,0,0), rz_deg=+90, mat=M['feeder'])
imp("YarnCone_F1", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"), t_mm=(FRO,20,250), mat=M['cone_r'])
imp("YarnCone_F4", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"), t_mm=(-FRO,-20,250), mat=M['cone_b'])

# Tracked needle marker (a small bright cylinder/cone in Slot #0)
# Will be repositioned each frame -- create once, move per phase
bpy.ops.mesh.primitive_cone_add(radius1=0.0015, radius2=0.0, depth=0.020,
                                location=(0.057, 0, 0.264))
needle_obj = bpy.context.active_object; needle_obj.name = "TrackedNeedle_S0"
assign(needle_obj, M['needle'])

# Slot#0 azimuthal marker (a small disc at the cassette top showing
# where Slot #0 currently is, viewed from above)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0035, location=(0.057, 0, 0.245))
slot0_marker = bpy.context.active_object; slot0_marker.name = "Slot0_Marker"
assign(slot0_marker, M['slot0'])

# Yarn segment (active yarn from F1 to current capture point)
# This will be a Bezier curve we re-create per frame.
def make_yarn_curve(name, pts_mm, thickness_mm=1.2, mat=None):
    # Remove old curve if it exists
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    cdata = bpy.data.curves.new(name=name, type='CURVE')
    cdata.dimensions = '3D'
    cdata.bevel_depth = thickness_mm * mm
    cdata.bevel_resolution = 3
    spline = cdata.splines.new('BEZIER')
    spline.bezier_points.add(len(pts_mm) - 1)
    for i,p in enumerate(pts_mm):
        bp = spline.bezier_points[i]
        bp.co = (p[0]*mm, p[1]*mm, p[2]*mm)
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    obj = bpy.data.objects.new(name, cdata)
    bpy.context.collection.objects.link(obj)
    if mat: assign(obj, mat)
    return obj

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
    bg.inputs[0].default_value = (0.10,0.12,0.16,1.0)
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

# Camera (single 3/4 view from above, framed on cassette top)
bpy.ops.object.camera_add(location=(0.25, -0.25, 0.40))
cam = bpy.context.active_object; cam.name = "PhaseCam"
cam.data.lens = 60
target = Vector((0,0,0.27))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z','Y').to_euler()
scene.camera = cam

# ============================================================
# PER-PHASE RENDER
# ============================================================
phases_deg = [0, 60, 120, 180, 240, 300]

print("\nRendering 6 phase snapshots...")
for phase in phases_deg:
    # 1. Compute needle position
    nx, ny = slot0_position(phase)
    nz = needle_Z(phase)

    # 2. Move the tracked needle
    needle_obj.location = (nx*mm, ny*mm, nz*mm - 0.010)   # cone tip ~ at hook position

    # 3. Move slot0 visual marker (at sinker plane height to show angular position)
    slot0_marker.location = (nx*mm * 0.95, ny*mm * 0.95, 0.256)

    # 4. Determine yarn state
    state, feeder, yx, yy, yz = yarn_capture_point(phase)

    # 5. Build yarn curve from active feeder cone -> nozzle -> needle/hook
    f_rad = math.radians(feeder)
    feed_r = MD.PCD_FEEDER/2 + 5.0
    feed_x = feed_r * math.cos(f_rad)
    feed_y = feed_r * math.sin(f_rad)
    feed_z = MD.world_z(MD.FEEDER_REFERENCE_Z)
    cone_x = (MD.PCD_FEEDER/2 + 25.0) * math.cos(f_rad)
    cone_y_offset = 20.0 if feeder == 0.0 else -20.0
    cone_top_z = 330.0

    if state == "captured":
        yarn_pts = [
            (cone_x, cone_y_offset, cone_top_z),
            (cone_x, cone_y_offset, 280.0),
            (feed_x + 5*math.cos(f_rad), feed_y + 5*math.sin(f_rad), feed_z + 8),
            (feed_x, feed_y, feed_z),
            (nx + 8*math.cos(f_rad), ny + 8*math.sin(f_rad), nz + 4),
            (nx, ny, nz),
        ]
    else:
        # Yarn parked at nozzle, draped slightly downward
        yarn_pts = [
            (cone_x, cone_y_offset, cone_top_z),
            (cone_x, cone_y_offset, 280.0),
            (feed_x + 5*math.cos(f_rad), feed_y + 5*math.sin(f_rad), feed_z + 8),
            (feed_x, feed_y, feed_z),
            (feed_x - 3*math.cos(f_rad), feed_y - 3*math.sin(f_rad), feed_z - 4),
        ]

    make_yarn_curve("YarnDynamic", yarn_pts, thickness_mm=1.2, mat=M['yarn'])

    # 6. Render
    out_path = os.path.join(OUT_DIR, f"CSM_V3_Phase15_theta_{phase:03d}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print(f"  theta={phase:3d}deg  Slot#0 at ({nx:+6.1f},{ny:+6.1f},{nz:.1f})  "
          f"state={state:18s}  -> {os.path.basename(out_path)} ({sz/1024:.0f}KB)")

# Save .blend
blend_path = os.path.join(OUT_DIR, "CSM_V3_Phase15_PhaseSnapshots.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")
print("\nDONE -- 6 phase snapshots, nominal motion baseline.")
print("\nNext: failure-mode variants (feeder lag, hook outrun, slack, snag)")
print("      can re-use this script with adjusted parameters in")
print("      yarn_capture_point() and needle_Z().")
