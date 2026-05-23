# -*- coding: utf-8 -*-
"""
CSM V3 -- KINEMATIC TRIAD VIEW (Priority C follow-up, pre-D)

Render family: KINEMATIC VALIDATION (not architectural).
  - SE overlays:        OFF
  - Wood frame:         hidden
  - Touchscreen mast:   hidden
  - Electronics:        hidden
  - Drive train:        hidden
  - Cassette outer body: ghosted (transparent) -- only visible where it
                         doesn't block the triad view

Purpose: visualize the feeder-exit / retainer-lip / hook-peak triad
that governs yarn capture consistency. Per ICD R5 Phase 1.5 readiness:
"0.5-1.5 mm changes can materially affect knitting reliability."

This view should answer:
  - Does the yarn naturally fall into hook capture?
  - Is the feeder too radial or too tangential?
  - Does the retainer lip stabilize or deflect yarn?
  - Is there risk of hook-lip interference under compliance?
  - Is the yarn path smooth or kinked?

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_kinematic_triad.py
"""
import bpy, math, sys, os
from mathutils import Vector

sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

mm = 0.001

# ============================================================
# RESET
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for m in list(bpy.data.materials):   bpy.data.materials.remove(m)

# ============================================================
# HELPERS
# ============================================================
def make_mat(name, base=(0.7,0.7,0.72,1.0), rough=0.4, metal=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = base
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            if "Alpha" in n.inputs:
                n.inputs["Alpha"].default_value = alpha
                if alpha < 1.0:
                    m.blend_method = 'BLEND'
            return m
    return m

def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)

def import_stl(path):
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=path)
    else:
        bpy.ops.import_mesh.stl(filepath=path)

def add_stl(name, path, t_mm=(0,0,0), rz_deg=0):
    if not os.path.exists(path):
        print(f"  [MISS] {name}")
        return None
    before = set(bpy.data.objects)
    import_stl(path)
    new = list(set(bpy.data.objects) - before)
    if not new: return None
    o = new[0]; o.name = name
    o.scale = (mm, mm, mm)
    o.location = (t_mm[0]*mm, t_mm[1]*mm, t_mm[2]*mm)
    if rz_deg: o.rotation_euler = (0,0,math.radians(rz_deg))
    bpy.context.view_layer.update()
    return o

def add_sphere(name, r, x=0, y=0, z=0, mat=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r*mm, location=(x*mm, y*mm, z*mm))
    o = bpy.context.active_object; o.name = name
    if mat: assign(o, mat)
    return o

def add_cyl(name, r, h, x=0, y=0, z=0, mat=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=r*mm, depth=h*mm,
                                        location=(x*mm, y*mm, z*mm))
    o = bpy.context.active_object; o.name = name
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    if mat: assign(o, mat)
    return o

def add_torus(name, R_major, R_minor, x=0, y=0, z=0, mat=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=R_major*mm,
                                     minor_radius=R_minor*mm,
                                     location=(x*mm, y*mm, z*mm))
    o = bpy.context.active_object; o.name = name
    if mat: assign(o, mat)
    return o

def add_bezier_curve(name, points_mm, thickness_mm=1.0, mat=None):
    """Create a Bezier curve through the given control points and give it a tube radius."""
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = thickness_mm * mm
    curve_data.bevel_resolution = 4
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(len(points_mm) - 1)
    for i, p in enumerate(points_mm):
        bp = spline.bezier_points[i]
        bp.co = (p[0]*mm, p[1]*mm, p[2]*mm)
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    if mat: assign(obj, mat)
    return obj

# ============================================================
# MATERIALS (kinematic palette: high contrast, semantic)
# ============================================================
M = {}
M['cylinder']   = make_mat("Cylinder",     (0.78, 0.80, 0.82, 1), 0.30)
M['sinker']     = make_mat("Sinker",       (0.40, 0.55, 0.70, 1), 0.35)
M['retainer']   = make_mat("Retainer",     (0.95, 0.85, 0.55, 0.65), 0.50, alpha=0.65)
M['cassette']   = make_mat("Cassette",     (0.50, 0.50, 0.55, 0.30), 0.40, alpha=0.30)
M['feeder']     = make_mat("Feeder",       (0.65, 0.55, 0.35, 0.75), 0.45, alpha=0.75)
M['nozzle']     = make_mat("YarnNozzle",   (0.95, 0.95, 0.60, 1), 0.30)
M['yarn']       = make_mat("YarnPath",     (0.92, 0.10, 0.10, 1), 0.85)
M['hook_pt']    = make_mat("HookPeak",     (1.00, 0.40, 0.00, 1), 0.30)
                                              # bright orange = critical point
M['hook_env']   = make_mat("HookSweep",    (1.00, 0.40, 0.00, 0.20), 0.40, alpha=0.20)
M['lip_marker'] = make_mat("LipUnderside", (0.00, 0.80, 0.50, 1), 0.30)
                                              # green = retainer lip plane

# ============================================================
# IMPORT MINIMAL GEOMETRY  (no frame, no electronics, no drive train)
# ============================================================
print("Loading kinematic geometry only...")
ROOT_LOCK = r"C:\3D-Project\01_MECHANICAL"
ROOT_ASM  = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
WZ = MD.CYL_BOTTOM_WORLD_Z

# Cylinder -- solid, in scene (we want to see the slot openings)
o = add_stl("Cylinder", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","cylinder","CSM_V3_Cylinder_V3_0_FULL.stl"),
            t_mm=(0,0,WZ))
if o: assign(o, M['cylinder'])

# Sinker ring
o = add_stl("SinkerRing", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","sinker_ring","CSM_V3_SinkerRing_V1_2_1_FULL.stl"),
            t_mm=(0,0,75+WZ))
if o: assign(o, M['sinker'])

# Retainer ring -- TRANSLUCENT so we can see the lip from above and below
o = add_stl("RetainerRing", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","retainer_ring","CSM_V3_RetainerRing_V1_0_FULL.stl"),
            t_mm=(0,0,83+WZ))
if o: assign(o, M['retainer'])

# Cassette base -- ghosted (very transparent), only for spatial reference
o = add_stl("CassetteBase", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","cassette_base","CSM_V3_CassetteBase_V1_1_FULL.stl"),
            t_mm=(0,0,49+WZ))
if o: assign(o, M['cassette'])

# Feeder F1 only (the one we're studying; F4 hidden because it's symmetric)
o = add_stl("Feeder_F1",
            os.path.join(ROOT_ASM,"feeder_module","CSM_V3_FeederModule_V1_1.stl"),
            t_mm=(MD.PCD_FEEDER/2 + 25.0, 0, 0), rz_deg=-90.0)
if o: assign(o, M['feeder'])

# ============================================================
# KINEMATIC ANNOTATIONS
# ============================================================
print("Adding kinematic annotations...")

# === HOOK PEAK POSITION ===
# Single needle hook at the +X side (Slot #0) at peak cam lift.
# Hook tip sits at:
#   - radius: cylinder OD/2 = 57.15 mm (just inside the slot wall)
#   - theta: 0° (Slot #0)
#   - world Z: HOOK_PEAK_WORLD_Z = 264
hook_x = MD.CYL_OD/2.0 - 1.0   # just inside slot opening
hook_y = 0.0
hook_z = MD.world_z(MD.HOOK_PEAK_Z)   # 264

add_sphere("HOOK_PEAK_pt", r=2.5, x=hook_x, y=hook_y, z=hook_z, mat=M['hook_pt'])

# Hook sweep envelope -- thin torus showing where ALL 72 hooks travel at peak lift
# (this is the circular path traced by all needle hooks at peak Z)
add_torus("Hook_Sweep_Envelope",
          R_major=MD.CYL_OD/2.0 - 1.0,
          R_minor=1.5,
          x=0, y=0, z=hook_z,
          mat=M['hook_env'])

# === RETAINER LIP UNDERSIDE PLANE ===
# Lip underside is 2 mm down from retainer top = (world 272 - 2) = 270
# Lip ID = 104 mm (effective loop aperture)
lip_underside_z = MD.world_z(MD.HOOK_PEAK_Z) + 6.0   # 264 + 6 = 270
# Render as a thin disc to highlight the lip plane
add_cyl("LipUnderside_marker",
        r=MD.RETAINER_LIP_ID/2.0, h=0.5,
        x=0, y=0, z=lip_underside_z,
        mat=M['lip_marker'])

# === FEEDER YARN EXIT POINT ===
# Feeder nozzle exits at FEEDER_REFERENCE_WORLD_Z = 271 at PCD 190/2 ish
feeder_exit_x = MD.PCD_FEEDER/2.0 + 5.0   # nozzle slightly outboard of PCD
feeder_exit_y = 0.0
feeder_exit_z = MD.world_z(MD.FEEDER_REFERENCE_Z)   # 271

add_sphere("FEEDER_EXIT_pt", r=2.0, x=feeder_exit_x, y=feeder_exit_y, z=feeder_exit_z, mat=M['hook_pt'])

# === YARN PATH (Bezier from feeder exit -> hook capture) ===
# 4-point curve: exit -> arc over sinker -> down to hook plane -> hook tip
yarn_points = [
    (feeder_exit_x, feeder_exit_y, feeder_exit_z),                # feeder exit
    (feeder_exit_x * 0.8, feeder_exit_y, feeder_exit_z + 1),       # slight rise / handle
    (hook_x + 8, hook_y, hook_z + 4),                              # over sinker, dropping
    (hook_x, hook_y, hook_z),                                      # hook tip capture
]
add_bezier_curve("YarnPath_F1_to_Hook",
                 points_mm=yarn_points,
                 thickness_mm=1.0,
                 mat=M['yarn'])

# ============================================================
# LIGHTING (clinical, flat, even)
# ============================================================
def add_light(name, ltype, loc, energy, rot=(0,0,0), size=1.0):
    bpy.ops.object.light_add(type=ltype, location=loc)
    L = bpy.context.active_object; L.name = name
    L.data.energy = energy
    if hasattr(L.data, 'size'): L.data.size = size
    L.rotation_euler = rot
    return L

add_light("Sun", 'SUN', loc=(0.3, -0.3, 1.0), energy=0.8,
          rot=(math.radians(45), 0, math.radians(30)))
add_light("Fill", 'AREA', loc=(0.2, 0.3, 0.4), energy=20,
          rot=(math.radians(70), 0, math.radians(180)), size=0.5)
add_light("Back", 'AREA', loc=(-0.2, -0.3, 0.4), energy=10,
          rot=(math.radians(110), 0, 0), size=0.5)

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.20, 0.22, 0.26, 1.0)
    bg.inputs[1].default_value = 0.30

# ============================================================
# RENDER SETTINGS
# ============================================================
scene = bpy.context.scene
try:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    try: scene.cycles.device = 'GPU'
    except Exception: pass
except Exception:
    for cand in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
        try: scene.render.engine = cand; break
        except Exception: continue

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -1.0

OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# CAMERAS (multiple angles on the triad)
# ============================================================
# Frame target: the hook peak point + lip plane + feeder exit
TARGET = Vector((hook_x*mm * 0.5, 0, MD.world_z(MD.HOOK_PEAK_Z)*mm))

views = [
    # name             pos_m                              ortho?  scale_m
    ("K_triad_3q",     (0.30, -0.22, 0.40),               False, None),     # 3/4 close
    ("K_triad_side",   (0.50, 0.0, 0.265),                True,  0.35),     # ortho side, looking -X
    ("K_triad_front",  (0.0, -0.50, 0.265),               True,  0.35),     # ortho front
    ("K_triad_top",    (0.08, 0.0, 0.70),                 True,  0.40),     # ortho top down on F1
]

for name, pos, is_ortho, ortho_scale in views:
    bpy.ops.object.camera_add(location=pos)
    cam = bpy.context.active_object
    cam.name = name
    if is_ortho:
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = ortho_scale
    else:
        cam.data.lens = 60.0
    dirv = TARGET - Vector(pos)
    cam.rotation_euler = dirv.to_track_quat('-Z','Y').to_euler()
    scene.camera = cam

    out_path = os.path.join(OUT_DIR, f"CSM_V3_KinematicTriad_{name}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print(f"  [{name}] -> {out_path} ({sz/1024:.0f} KB)")

# Save .blend
blend_path = os.path.join(OUT_DIR, "CSM_V3_KinematicTriad.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")
print("\nDONE -- 4 kinematic triad views + 1 .blend.")
print("\nLEGEND:")
print("  ORANGE sphere  = hook peak point (Slot #0 at peak cam lift, world Z=264)")
print("  ORANGE torus   = full hook-sweep envelope at peak Z (where ALL 72 hooks travel)")
print("  GREEN disc     = retainer lip underside plane (world Z=270, ID 104 mm)")
print("  RED curve      = yarn path from feeder exit to hook capture")
print("  YELLOW sphere  = feeder F1 yarn exit point (world Z=271)")
print("  GHOSTED        = cassette base body (transparent so the triad is visible)")
