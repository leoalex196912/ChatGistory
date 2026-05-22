# -*- coding: utf-8 -*-
"""
CSM V3 -- Full assembly + multi-angle render (Blender 5.x headless).

Imports all locked + new STLs at their canonical world-Z positions,
assigns color-coded materials, and renders the machine from 4 camera
angles to PNG files.

All world-coordinate constants come from machine_datums.py. There is
NO hardcoded world Z in this script.

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_hero_v2.py
"""

import bpy, math, sys, os
from mathutils import Vector

# Single source of truth for coordinates
sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

mm = 0.001   # mm -> Blender meters

# =============================================================================
# RESET SCENE
# =============================================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):  bpy.data.collections.remove(c)
for m in list(bpy.data.materials):    bpy.data.materials.remove(m)
for img in list(bpy.data.images):     bpy.data.images.remove(img)

# =============================================================================
# HELPERS
# =============================================================================
def make_mat(name, base=(0.7, 0.7, 0.72, 1.0), rough=0.4, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = base
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            return m
    return m

def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)

def import_stl(path):
    """Import STL using Blender 4.x/5.x operator name."""
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=path)
    else:
        bpy.ops.import_mesh.stl(filepath=path)

def add_stl(name, path, translate_mm=(0.0, 0.0, 0.0), rotate_z_deg=0.0):
    """Import an STL, scale mm->m, translate to position in mm, optionally
    rotate around Z. Returns the new object."""
    before = set(bpy.data.objects)
    if not os.path.exists(path):
        print(f"  [MISS] {name}: {path}")
        return None
    import_stl(path)
    new = list(set(bpy.data.objects) - before)
    if not new:
        print(f"  [FAIL] {name}: no object after import")
        return None
    obj = new[0]
    obj.name = name
    obj.scale = (mm, mm, mm)
    obj.location = (translate_mm[0]*mm, translate_mm[1]*mm, translate_mm[2]*mm)
    if rotate_z_deg:
        obj.rotation_euler = (0, 0, math.radians(rotate_z_deg))
    bpy.context.view_layer.update()
    return obj

def add_primitive_box(name, sx, sy, sz, x=0, y=0, z=0, mat=None, rotate_z_deg=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x*mm, y*mm, z*mm))
    o = bpy.context.active_object
    o.name = name
    o.scale = (sx*mm/2, sy*mm/2, sz*mm/2)
    bpy.ops.object.transform_apply(scale=True)
    if rotate_z_deg:
        o.rotation_euler = (0, 0, math.radians(rotate_z_deg))
    if mat:
        assign(o, mat)
    return o

def add_primitive_cone(name, r1, r2, h, x, y, z, mat):
    bpy.ops.mesh.primitive_cone_add(radius1=r1*mm, radius2=r2*mm, depth=h*mm,
                                    location=(x*mm, y*mm, z*mm))
    o = bpy.context.active_object
    o.name = name
    assign(o, mat)
    return o

# =============================================================================
# MATERIALS (color-coded for visibility)
# =============================================================================
print("Building materials...")
M = {}
M['wood']        = make_mat("Wood_Walnut",        (0.32, 0.16, 0.06, 1), 0.55)
M['ext_2020']    = make_mat("Aluminum_2020_BLK",  (0.10, 0.10, 0.11, 1), 0.45, 0.7)
M['alu_plate']   = make_mat("Aluminum_6061",      (0.82, 0.84, 0.87, 1), 0.28, 1.0)
M['cyl_petg']    = make_mat("Cylinder_PETG",      (0.85, 0.86, 0.88, 1), 0.32)
M['cam_anod']    = make_mat("CamRing_Anodized",   (0.08, 0.08, 0.10, 1), 0.25, 0.5)
M['cassette']    = make_mat("Cassette_PETG",      (0.65, 0.68, 0.72, 1), 0.35)
M['sinker']      = make_mat("Sinker_PETG",        (0.55, 0.58, 0.62, 1), 0.35)
M['retainer']    = make_mat("Retainer_PA12",      (0.92, 0.86, 0.68, 1), 0.50)
M['drive_hub']   = make_mat("DriveHub_PETG",      (0.60, 0.62, 0.66, 1), 0.30)
M['bearings']    = make_mat("Bearings_PETG",      (0.40, 0.42, 0.45, 1), 0.40)
M['motor_mount'] = make_mat("MotorMount_PETG",    (0.30, 0.32, 0.35, 1), 0.40)
M['motor']       = make_mat("Motor_Black",        (0.03, 0.03, 0.04, 1), 0.40, 0.1)
M['feeder']      = make_mat("Feeder_PA12",        (0.78, 0.72, 0.55, 1), 0.45)
M['yarn_r']      = make_mat("Yarn_Red",           (0.78, 0.10, 0.10, 1), 0.85)
M['yarn_b']      = make_mat("Yarn_Blue",          (0.08, 0.22, 0.78, 1), 0.85)
M['touchscreen'] = make_mat("Screen_Active",      (0.08, 0.15, 0.32, 1), 0.30)
M['ground']      = make_mat("Ground",             (0.55, 0.55, 0.58, 1), 0.70)

# =============================================================================
# IMPORT STLs
# =============================================================================
print("\nImporting frame (Layer 2 structural)...")

# Wood base (already at world Z=0..18)
ROOT_ASM = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
o = add_stl("WoodBase",
            os.path.join(ROOT_ASM, "frame", "wood_base", "CSM_V3_WoodBase_V1_1.stl"))
if o: assign(o, M['wood'])

# 4x 2020 uprights at corners of upper deck
for i, (ux, uy) in enumerate([(+150, +120), (+150, -120), (-150, +120), (-150, -120)]):
    o = add_stl(f"Upright_{i}",
                os.path.join(ROOT_ASM, "frame", "upright_2020", "CSM_V3_Upright2020_V1_1.stl"),
                translate_mm=(ux, uy, 0.0))
    if o: assign(o, M['ext_2020'])

# Wood upper deck (at world Z=206..224)
o = add_stl("WoodUpperDeck",
            os.path.join(ROOT_ASM, "frame", "wood_upper_deck", "CSM_V3_WoodUpperDeck_V1_0.stl"))
if o: assign(o, M['wood'])

# Aluminum master-datum plate (at world Z=224..230)
o = add_stl("MountPlate6061",
            os.path.join(ROOT_ASM, "frame", "mount_plate_6061", "CSM_V3_MountPlate6061_V1_1.stl"))
if o: assign(o, M['alu_plate'])

# Touchscreen mast (at (0, -180), Z=18..418)
o = add_stl("TouchscreenMast",
            os.path.join(ROOT_ASM, "frame", "touchscreen_mast", "CSM_V3_TouchscreenMast_V1_0.stl"))
if o: assign(o, M['ext_2020'])

# =============================================================================
# Cassette (Layer 1 precision core) -- locked STLs, translate cyl-local
# to world by adding CYL_BOTTOM_WORLD_Z = 181 to their Z position
# =============================================================================
print("\nImporting cassette (Layer 1 precision core)...")
ROOT_LOCK = r"C:\3D-Project\01_MECHANICAL"
WZ = MD.CYL_BOTTOM_WORLD_Z   # 181

# Each locked STL was built with cyl-local Z=0 at cylinder bottom.
# So translating by WZ puts cylinder bottom at world Z=181.
o = add_stl("Cylinder_V3_0",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "cylinder",
                         "CSM_V3_Cylinder_V3_0_FULL.stl"),
            translate_mm=(0, 0, WZ))
if o: assign(o, M['cyl_petg'])

# Cam Ring V6.5 -- macro positions it relative to its own origin.
# Earlier render had it at Z=19 (cyl-local). Test with that offset.
o = add_stl("CamRing_V6_5",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "cam_ring",
                         "CSM_V3_CamRing_V6_5_FULL.stl"),
            translate_mm=(0, 0, 19 + WZ))
if o: assign(o, M['cam_anod'])

# Cassette Base V1.1 -- bottom at cyl-local Z=49 -> world Z=230
o = add_stl("CassetteBase_V1_1",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "cassette_base",
                         "CSM_V3_CassetteBase_V1_1_FULL.stl"),
            translate_mm=(0, 0, 49 + WZ))
if o: assign(o, M['cassette'])

# Sinker Ring V1.2.1 -- at cyl-local Z=75 -> world Z=256
o = add_stl("SinkerRing_V1_2_1",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "sinker_ring",
                         "CSM_V3_SinkerRing_V1_2_1_FULL.stl"),
            translate_mm=(0, 0, 75 + WZ))
if o: assign(o, M['sinker'])

# Retainer Ring V1.0 -- at cyl-local Z=83 -> world Z=264
o = add_stl("RetainerRing_V1_0",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "retainer_ring",
                         "CSM_V3_RetainerRing_V1_0_FULL.stl"),
            translate_mm=(0, 0, 83 + WZ))
if o: assign(o, M['retainer'])

# =============================================================================
# Drive train (Layer 2) -- locked STLs, positioned below cassette
# =============================================================================
print("\nImporting drive train (Layer 2)...")

# Drive Hub V2.4.2 -- top boss enters cylinder bottom at world Z=181
# Hub flange below. Earlier render placed at cyl-local Z=-10 (i.e. hub
# extends DOWN from cylinder by 10 mm).
o = add_stl("DriveHub_V2_4_2",
            os.path.join(ROOT_LOCK, "06_DRIVE_SYSTEM", "CSM_V3_DriveHub_V2_4_2.stl"),
            translate_mm=(0, 0, -10 + WZ))
if o: assign(o, M['drive_hub'])

# Bearing Housings V2.5 pair -- below drive hub. Earlier at cyl-local Z=-70.
o = add_stl("BearingHousings_V2_5",
            os.path.join(ROOT_LOCK, "05_BEARINGS_SHAFT",
                         "CSM_V3_BearingHousings_PAIR_V2_5_1.stl"),
            translate_mm=(0, 0, -70 + WZ))
if o: assign(o, M['bearings'])

# Motor Mount V1.3 -- below bearings. Earlier at cyl-local Z=-120.
o = add_stl("MotorMount_V1_3",
            os.path.join(ROOT_LOCK, "06_DRIVE_SYSTEM", "CSM_V3_MotorMount_V1_3.stl"),
            translate_mm=(0, 0, -120 + WZ))
if o: assign(o, M['motor_mount'])

# NEMA 17 motor (built in CSM_V3_ASSEMBLY/drive_bought)
o = add_stl("NEMA17_Motor",
            os.path.join(ROOT_ASM, "drive_bought", "nema17_stepper",
                         "CSM_V3_NEMA17_V1_0.stl"),
            translate_mm=(MD.MOTOR_X, MD.MOTOR_Y, MD.MOTOR_BODY_BOTTOM_Z))
if o: assign(o, M['motor'])

# =============================================================================
# Feeders (Layer 3) -- Phase 1: F1 (theta=0, +X) and F4 (theta=180, -X)
# =============================================================================
print("\nImporting Phase 1 feeders (F1, F4)...")

# Feeder STL was built with mount edge pointing -Y. To place at F1 (theta=0,
# pointing +X), rotate +90 around Z so mount edge points -X (toward
# cylinder axis). The feeder origin is centered between its 2 bolts.
# Need to translate radially so the bolt positions land on PCD 190.

# Distance from feeder origin to bolt-pair midpoint at PCD 190:
# feeder mount holes are at Y=-BASE_D/2+10 = -25 in feeder local frame.
# So feeder origin sits at radial distance = PCD/2 - 25 from cylinder axis.
# = 95 - 25 = wait, no -- if mount edge faces toward cylinder (-Y) and
# bolts are at Y=-25 in feeder local, then feeder origin is at radial
# distance = (mount bolt radial) + 25 = 95 + 25 = 120 mm from cylinder axis.
# After rotating to F1 (theta=0, +X direction), feeder origin sits at
# X=+120, Y=0. Cone post then goes up from that origin.

FEEDER_RADIAL_OFFSET = MD.PCD_FEEDER / 2.0 + 25.0    # 120 mm

# F1 at theta = 0 deg (+X axis = motor side)
o = add_stl("Feeder_F1",
            os.path.join(ROOT_ASM, "feeder_module", "CSM_V3_FeederModule_V1_0.stl"),
            translate_mm=(FEEDER_RADIAL_OFFSET, 0, 0),
            rotate_z_deg=-90.0)   # rotate so mount edge faces -X (toward cylinder)
if o: assign(o, M['feeder'])

# F4 at theta = 180 deg (-X axis = service side)
o = add_stl("Feeder_F4",
            os.path.join(ROOT_ASM, "feeder_module", "CSM_V3_FeederModule_V1_0.stl"),
            translate_mm=(-FEEDER_RADIAL_OFFSET, 0, 0),
            rotate_z_deg=+90.0)   # rotate so mount edge faces +X
if o: assign(o, M['feeder'])

# Yarn cones on feeder cone posts
# Cone post bottom at world Z = 250 (cyl-local 69), height 130 -> top at world Z=380
# Cone diameter ~70 mm at base, 40 at top, height 130
CONE_Z_CENTER = 250 + 130/2   # mid-height of cone (cone bottom 250)
add_primitive_cone("YarnCone_F1", r1=35, r2=20, h=130,
                   x=FEEDER_RADIAL_OFFSET, y=20, z=CONE_Z_CENTER,
                   mat=M['yarn_r'])
add_primitive_cone("YarnCone_F4", r1=35, r2=20, h=130,
                   x=-FEEDER_RADIAL_OFFSET, y=-20, z=CONE_Z_CENTER,
                   mat=M['yarn_b'])

# =============================================================================
# Touchscreen panel (mounted on mast crossbar)
# =============================================================================
print("\nAdding touchscreen panel...")
add_primitive_box("Touchscreen", MD.TOUCH_W, MD.TOUCH_H, MD.TOUCH_D,
                  x=MD.MAST_CENTER_X, y=MD.MAST_CENTER_Y + 20, z=MD.MAST_TOP_Z - 50,
                  mat=M['touchscreen'])

# =============================================================================
# Ground plane (for shadow context)
# =============================================================================
print("\nAdding ground plane...")
bpy.ops.mesh.primitive_plane_add(size=2.5, location=(0, 0, -0.005))
ground = bpy.context.active_object; ground.name = "Ground"
assign(ground, M['ground'])

# =============================================================================
# LIGHTING (3-point + sun rim)
# =============================================================================
print("\nSetting up lighting...")
def add_light(name, ltype, loc, energy, rot=(0, 0, 0), size=0.8, color=(1, 1, 1)):
    bpy.ops.object.light_add(type=ltype, location=loc)
    L = bpy.context.active_object; L.name = name
    L.data.energy = energy
    if hasattr(L.data, 'size'):
        L.data.size = size
    L.data.color = color
    L.rotation_euler = rot
    return L

# Sun (rim from upper-back-left)
add_light("Sun_Rim", 'SUN', loc=(-1.0, -1.2, 2.5), energy=2.5,
          rot=(math.radians(45), math.radians(-15), math.radians(40)),
          color=(1.0, 0.97, 0.92))

# Key area light (front-right)
add_light("AreaKey", 'AREA', loc=(0.7, 0.7, 0.7), energy=180,
          rot=(math.radians(-50), 0, math.radians(135)), size=0.7)

# Fill area light (left-down)
add_light("AreaFill", 'AREA', loc=(-0.9, 0.4, 0.4), energy=80,
          rot=(math.radians(70), 0, math.radians(-110)), size=1.0)

# World background
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.20, 0.24, 0.30, 1.0)
    bg.inputs[1].default_value = 0.30

# =============================================================================
# CAMERA + RENDER SETTINGS
# =============================================================================
scene = bpy.context.scene

# Try Cycles first (better quality), fall back to Eevee Next
try:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    try:
        scene.cycles.device = 'GPU'
    except Exception:
        pass
    print(f"Render engine: CYCLES @ {scene.cycles.samples} samples")
except Exception:
    for cand in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
        try:
            scene.render.engine = cand
            print(f"Render engine: {cand}")
            break
        except Exception:
            continue

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -0.5

# =============================================================================
# Multi-angle render
# =============================================================================
OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"
os.makedirs(OUT_DIR, exist_ok=True)

# Camera target: cassette head center (a bit above master datum)
CAM_TARGET = Vector((0, 0, 0.260))    # world Y = 260 mm = ~middle of cassette

cam_views = [
    ("hero_34",       (0.70,  -0.85,  0.35),  42),
    ("front",         (0.00,  -0.95,  0.30),  50),
    ("side_motor",    (1.10,   0.00,  0.30),  45),
    ("top_down",      (0.00,   0.00,  1.30),  55),
]

# Add camera
bpy.ops.object.camera_add(location=cam_views[0][1])
cam = bpy.context.active_object; cam.name = "HeroCam"
cam.data.lens = cam_views[0][2]
scene.camera = cam

for view_name, cam_loc, lens in cam_views:
    cam.location = cam_loc
    cam.data.lens = lens
    if view_name == "top_down":
        cam.rotation_euler = (0, 0, math.radians(90))
    else:
        dirvec = CAM_TARGET - Vector(cam_loc)
        cam.rotation_euler = dirvec.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.view_layer.update()
    out_path = os.path.join(OUT_DIR, f"CSM_V3_Assembly_{view_name}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print(f"  [{view_name}] {out_path}  ({sz/1024:.0f} KB)")

# Save the .blend file so user can open it directly
blend_path = os.path.join(OUT_DIR, "CSM_V3_Assembly.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")

print("\nDONE. 4 renders + 1 .blend file in:")
print(f"  {OUT_DIR}")
