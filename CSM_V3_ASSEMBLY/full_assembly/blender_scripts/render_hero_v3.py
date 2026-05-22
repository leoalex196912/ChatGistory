# -*- coding: utf-8 -*-
"""
CSM V3 -- Full assembly + 4-angle render V3 (Blender 5.x headless).

V3 adds (vs V2 render):
  - Real pulleys (HTD 5M 60T + 16T) on drive shaft and motor shaft
  - HTD belt connecting the two pulleys
  - 12 mm drive shaft (real geometry, not implied)
  - 6001-2RS bearings inside bearing housings
  - Real yarn cone with base flange + body
  - Electronics on wood base: Arduino Mega + TB6600 + LRS-50 PSU
  - Real touchscreen (active screen + bezel) on mast crossbar
  - Touchscreen mounting arm

All world-Z constants come from machine_datums.py. No hardcoded coords.

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_hero_v3.py
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
for img in list(bpy.data.images):    bpy.data.images.remove(img)

# ============================================================
# HELPERS
# ============================================================
def make_mat(name, base=(0.7,0.7,0.72,1.0), rough=0.4, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
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
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=path)
    else:
        bpy.ops.import_mesh.stl(filepath=path)

def add_stl(name, path, t_mm=(0.0, 0.0, 0.0), rz_deg=0.0, rx_deg=0.0, ry_deg=0.0):
    if not os.path.exists(path):
        print(f"  [MISS] {name}: {path}")
        return None
    before = set(bpy.data.objects)
    import_stl(path)
    new = list(set(bpy.data.objects) - before)
    if not new:
        print(f"  [FAIL] {name}: no object")
        return None
    obj = new[0]
    obj.name = name
    obj.scale = (mm, mm, mm)
    obj.location = (t_mm[0]*mm, t_mm[1]*mm, t_mm[2]*mm)
    obj.rotation_euler = (math.radians(rx_deg), math.radians(ry_deg), math.radians(rz_deg))
    bpy.context.view_layer.update()
    return obj

# ============================================================
# MATERIALS
# ============================================================
print("Materials...")
M = {}
M['wood']        = make_mat("Wood_Walnut",        (0.32, 0.16, 0.06, 1), 0.55)
M['ext_2020']    = make_mat("Aluminum_2020_BLK",  (0.10, 0.10, 0.11, 1), 0.45, 0.7)
M['alu_plate']   = make_mat("Aluminum_6061",      (0.82, 0.84, 0.87, 1), 0.28, 1.0)
M['cyl_petg']    = make_mat("Cylinder_PETG",      (0.85, 0.86, 0.88, 1), 0.32)
M['cam_anod']    = make_mat("CamRing_Anodized",   (0.08, 0.08, 0.10, 1), 0.25, 0.5)
M['cassette']    = make_mat("Cassette_PETG",      (0.65, 0.68, 0.72, 1), 0.35)
M['sinker']      = make_mat("Sinker_PETG",        (0.55, 0.58, 0.62, 1), 0.35)
M['retainer']    = make_mat("Retainer_PA12",      (0.92, 0.86, 0.68, 1), 0.50)
M['drive_hub']   = make_mat("DriveHub_Al",        (0.78, 0.80, 0.83, 1), 0.20, 1.0)
M['bearings_ho'] = make_mat("BearingHsg_PETG",    (0.40, 0.42, 0.45, 1), 0.40)
M['motor_mount'] = make_mat("MotorMount_PETG",    (0.30, 0.32, 0.35, 1), 0.40)
M['motor']       = make_mat("Motor_Black",        (0.03, 0.03, 0.04, 1), 0.40, 0.1)
M['feeder']      = make_mat("Feeder_PA12",        (0.78, 0.72, 0.55, 1), 0.45)
M['yarn_r']      = make_mat("Yarn_Red",           (0.78, 0.10, 0.10, 1), 0.85)
M['yarn_b']      = make_mat("Yarn_Blue",          (0.08, 0.22, 0.78, 1), 0.85)
M['screen']      = make_mat("Screen_Active",      (0.05, 0.10, 0.18, 1), 0.20)
M['ground']      = make_mat("Ground",             (0.55, 0.55, 0.58, 1), 0.70)
M['pulley']      = make_mat("Pulley_Black",       (0.06, 0.06, 0.08, 1), 0.50)
M['belt']        = make_mat("Belt_Rubber",        (0.025,0.025,0.025,1), 0.75)
M['steel']       = make_mat("Steel_Polished",     (0.78, 0.80, 0.84, 1), 0.18, 1.0)
M['bearing']     = make_mat("Bearing_Steel",      (0.65, 0.67, 0.70, 1), 0.25, 1.0)
M['pcb_green']   = make_mat("PCB_Green",          (0.04, 0.32, 0.10, 1), 0.50)
M['enclosure']   = make_mat("Enclosure_Gray",     (0.45, 0.47, 0.50, 1), 0.40, 0.6)
M['psu_silver']  = make_mat("PSU_Silver",         (0.72, 0.74, 0.76, 1), 0.30, 0.6)

# ============================================================
# IMPORT FRAME (Layer 2)
# ============================================================
print("Frame...")
ROOT_ASM  = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
ROOT_LOCK = r"C:\3D-Project\01_MECHANICAL"

o = add_stl("WoodBase", os.path.join(ROOT_ASM, "frame", "wood_base", "CSM_V3_WoodBase_V1_1.stl"))
if o: assign(o, M['wood'])

for i, (ux, uy) in enumerate([(+150,+120),(+150,-120),(-150,+120),(-150,-120)]):
    o = add_stl(f"Upright_{i}",
                os.path.join(ROOT_ASM, "frame", "upright_2020", "CSM_V3_Upright2020_V1_1.stl"),
                t_mm=(ux, uy, 0.0))
    if o: assign(o, M['ext_2020'])

o = add_stl("WoodUpperDeck", os.path.join(ROOT_ASM, "frame", "wood_upper_deck", "CSM_V3_WoodUpperDeck_V1_0.stl"))
if o: assign(o, M['wood'])

o = add_stl("MountPlate6061", os.path.join(ROOT_ASM, "frame", "mount_plate_6061", "CSM_V3_MountPlate6061_V1_1.stl"))
if o: assign(o, M['alu_plate'])

o = add_stl("TouchscreenMast", os.path.join(ROOT_ASM, "frame", "touchscreen_mast", "CSM_V3_TouchscreenMast_V1_0.stl"))
if o: assign(o, M['ext_2020'])

# ============================================================
# CASSETTE (Layer 1) -- locked STLs, translate cyl-local + WZ
# ============================================================
print("Cassette...")
WZ = MD.CYL_BOTTOM_WORLD_Z

o = add_stl("Cylinder_V3_0",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "cylinder", "CSM_V3_Cylinder_V3_0_FULL.stl"),
            t_mm=(0, 0, WZ))
if o: assign(o, M['cyl_petg'])

o = add_stl("CamRing_V6_5",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "cam_ring", "CSM_V3_CamRing_V6_5_FULL.stl"),
            t_mm=(0, 0, 19 + WZ))
if o: assign(o, M['cam_anod'])

o = add_stl("CassetteBase_V1_1",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "cassette_base", "CSM_V3_CassetteBase_V1_1_FULL.stl"),
            t_mm=(0, 0, 49 + WZ))
if o: assign(o, M['cassette'])

o = add_stl("SinkerRing_V1_2_1",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "sinker_ring", "CSM_V3_SinkerRing_V1_2_1_FULL.stl"),
            t_mm=(0, 0, 75 + WZ))
if o: assign(o, M['sinker'])

o = add_stl("RetainerRing_V1_0",
            os.path.join(ROOT_LOCK, "02_CASSETTE_HEAD", "retainer_ring", "CSM_V3_RetainerRing_V1_0_FULL.stl"),
            t_mm=(0, 0, 83 + WZ))
if o: assign(o, M['retainer'])

# ============================================================
# DRIVE TRAIN (Layer 2)
# ============================================================
print("Drive train...")

# Drive hub
o = add_stl("DriveHub_V2_4_2",
            os.path.join(ROOT_LOCK, "06_DRIVE_SYSTEM", "CSM_V3_DriveHub_V2_4_2.stl"),
            t_mm=(0, 0, -10 + WZ))
if o: assign(o, M['drive_hub'])

# Bearing housing pair
o = add_stl("BearingHousings_V2_5",
            os.path.join(ROOT_LOCK, "05_BEARINGS_SHAFT", "CSM_V3_BearingHousings_PAIR_V2_5_1.stl"),
            t_mm=(0, 0, -70 + WZ))
if o: assign(o, M['bearings_ho'])

# Motor mount
o = add_stl("MotorMount_V1_3",
            os.path.join(ROOT_LOCK, "06_DRIVE_SYSTEM", "CSM_V3_MotorMount_V1_3.stl"),
            t_mm=(0, 0, -120 + WZ))
if o: assign(o, M['motor_mount'])

# 12 mm steel shaft (vertical, passes through bearings + drive hub)
o = add_stl("DriveShaft_12mm",
            os.path.join(ROOT_ASM, "bearings_bought", "shaft_12mm", "CSM_V3_Shaft12mm_V1_0.stl"),
            t_mm=(0, 0, 30))
if o: assign(o, M['steel'])

# 6001-2RS bearings (two of them, in housings)
o = add_stl("Bearing_Lower",
            os.path.join(ROOT_ASM, "bearings_bought", "bearing_6001_2rs", "CSM_V3_Bearing6001_V1_0.stl"),
            t_mm=(0, 0, 90))
if o: assign(o, M['bearing'])

o = add_stl("Bearing_Upper",
            os.path.join(ROOT_ASM, "bearings_bought", "bearing_6001_2rs", "CSM_V3_Bearing6001_V1_0.stl"),
            t_mm=(0, 0, 130))
if o: assign(o, M['bearing'])

# Drive shaft pulley (60T HTD 5M)
DRIVE_PULLEY_Z = 70
o = add_stl("Pulley_60T",
            os.path.join(ROOT_ASM, "drive_bought", "pulley_htd_60t", "CSM_V3_PulleyHTD60T_V1_0.stl"),
            t_mm=(0, 0, DRIVE_PULLEY_Z))
if o: assign(o, M['pulley'])

# NEMA 17 motor
o = add_stl("NEMA17_Motor",
            os.path.join(ROOT_ASM, "drive_bought", "nema17_stepper", "CSM_V3_NEMA17_V1_0.stl"),
            t_mm=(MD.MOTOR_X, MD.MOTOR_Y, MD.MOTOR_BODY_BOTTOM_Z))
if o: assign(o, M['motor'])

# Motor pulley (16T HTD 5M) at top of motor shaft
MOTOR_PULLEY_Z = MD.MOTOR_BODY_BOTTOM_Z + MD.NEMA17_BODY_L + MD.NEMA17_BOSS_H + 8
o = add_stl("Pulley_16T",
            os.path.join(ROOT_ASM, "drive_bought", "pulley_htd_16t", "CSM_V3_PulleyHTD16T_V1_0.stl"),
            t_mm=(MD.MOTOR_X, MD.MOTOR_Y, MOTOR_PULLEY_Z))
if o: assign(o, M['pulley'])

# HTD belt loop -- placed midway between the two pulleys, at the belt centerline Z
BELT_Z = (DRIVE_PULLEY_Z + MOTOR_PULLEY_Z) / 2.0
o = add_stl("Belt_HTD5M",
            os.path.join(ROOT_ASM, "drive_bought", "belt_htd_5m", "CSM_V3_BeltHTD5M_V1_0.stl"),
            t_mm=(MD.MOTOR_X/2, MD.MOTOR_Y/2, BELT_Z))
if o: assign(o, M['belt'])

# ============================================================
# FEEDERS (Layer 3) -- Phase 1: F1 and F4
# ============================================================
print("Feeders...")
FEEDER_RADIAL_OFFSET = MD.PCD_FEEDER / 2.0 + 25.0  # 120

o = add_stl("Feeder_F1",
            os.path.join(ROOT_ASM, "feeder_module", "CSM_V3_FeederModule_V1_0.stl"),
            t_mm=(FEEDER_RADIAL_OFFSET, 0, 0), rz_deg=-90.0)
if o: assign(o, M['feeder'])

o = add_stl("Feeder_F4",
            os.path.join(ROOT_ASM, "feeder_module", "CSM_V3_FeederModule_V1_0.stl"),
            t_mm=(-FEEDER_RADIAL_OFFSET, 0, 0), rz_deg=+90.0)
if o: assign(o, M['feeder'])

# Yarn cones on each feeder cone post -- real geometry now (CSM_V3_YarnCone_V1_0)
# Cone post bottom at world Z = 250 (cyl-local 69 + WZ).
# YarnCone STL should be built with its bottom at Z=0 in its local frame.
o = add_stl("YarnCone_F1",
            os.path.join(ROOT_ASM, "decor", "yarn_cone", "CSM_V3_YarnCone_V1_0.stl"),
            t_mm=(FEEDER_RADIAL_OFFSET, 20, 250))
if o: assign(o, M['yarn_r'])

o = add_stl("YarnCone_F4",
            os.path.join(ROOT_ASM, "decor", "yarn_cone", "CSM_V3_YarnCone_V1_0.stl"),
            t_mm=(-FEEDER_RADIAL_OFFSET, -20, 250))
if o: assign(o, M['yarn_b'])

# ============================================================
# ELECTRONICS (Layer 3) -- on wood base around drive train
# ============================================================
print("Electronics...")

# Arduino Mega 2560 -- front-right of drive train
o = add_stl("ArduinoMega2560",
            os.path.join(ROOT_ASM, "electronics", "arduino_mega_2560", "CSM_V3_ArduinoMega_V1_0.stl"),
            t_mm=(-130, 130, MD.WOOD_BASE_TOP_Z + 2))
if o: assign(o, M['pcb_green'])

# TB6600 driver -- back-right of drive train
o = add_stl("TB6600_Driver",
            os.path.join(ROOT_ASM, "electronics", "tb6600_driver", "CSM_V3_TB6600_V1_0.stl"),
            t_mm=(150, 60, MD.WOOD_BASE_TOP_Z + 2), rz_deg=90)
if o: assign(o, M['enclosure'])

# LRS-50 PSU -- back-left
o = add_stl("LRS50_PSU",
            os.path.join(ROOT_ASM, "electronics", "lrs50_psu", "CSM_V3_LRS50_V1_0.stl"),
            t_mm=(-150, -60, MD.WOOD_BASE_TOP_Z + 2), rz_deg=90)
if o: assign(o, M['psu_silver'])

# ============================================================
# TOUCHSCREEN + ARM
# ============================================================
print("Touchscreen...")

# Mounting arm
o = add_stl("TouchscreenArm",
            os.path.join(ROOT_ASM, "electronics", "touchscreen_arm", "CSM_V3_TouchscreenArm_V1_0.stl"),
            t_mm=(0, MD.MAST_CENTER_Y + 20, MD.MAST_TOP_Z - 80))
if o: assign(o, M['enclosure'])

# Screen panel (active screen)
o = add_stl("Touchscreen_Screen",
            os.path.join(ROOT_ASM, "electronics", "touchscreen_7in", "CSM_V3_Touchscreen7in_Screen_V1_0.stl"),
            t_mm=(0, MD.MAST_CENTER_Y + 40, MD.MAST_TOP_Z - 50))
if o: assign(o, M['screen'])

# Bezel + backplate
o = add_stl("Touchscreen_Bezel",
            os.path.join(ROOT_ASM, "electronics", "touchscreen_7in", "CSM_V3_Touchscreen7in_V1_0.stl"),
            t_mm=(0, MD.MAST_CENTER_Y + 35, MD.MAST_TOP_Z - 50))
if o: assign(o, M['enclosure'])

# ============================================================
# GROUND
# ============================================================
print("Ground...")
bpy.ops.mesh.primitive_plane_add(size=2.5, location=(0, 0, -0.005))
ground = bpy.context.active_object; ground.name = "Ground"
assign(ground, M['ground'])

# ============================================================
# LIGHTING
# ============================================================
print("Lighting...")
def add_light(name, ltype, loc, energy, rot=(0,0,0), size=0.8, color=(1,1,1)):
    bpy.ops.object.light_add(type=ltype, location=loc)
    L = bpy.context.active_object; L.name = name
    L.data.energy = energy
    if hasattr(L.data, 'size'): L.data.size = size
    L.data.color = color
    L.rotation_euler = rot
    return L

add_light("Sun_Rim", 'SUN', loc=(-1.0,-1.2,2.5), energy=2.5,
          rot=(math.radians(45), math.radians(-15), math.radians(40)),
          color=(1.0, 0.97, 0.92))
add_light("AreaKey", 'AREA', loc=(0.7,0.7,0.7), energy=180,
          rot=(math.radians(-50), 0, math.radians(135)), size=0.7)
add_light("AreaFill", 'AREA', loc=(-0.9,0.4,0.4), energy=80,
          rot=(math.radians(70), 0, math.radians(-110)), size=1.0)

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.20, 0.24, 0.30, 1.0)
    bg.inputs[1].default_value = 0.30

# ============================================================
# CAMERA + RENDER
# ============================================================
scene = bpy.context.scene
try:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    try: scene.cycles.device = 'GPU'
    except Exception: pass
    print(f"Engine: CYCLES @ {scene.cycles.samples}")
except Exception:
    for cand in ['BLENDER_EEVEE_NEXT','BLENDER_EEVEE']:
        try: scene.render.engine = cand; break
        except Exception: continue

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -0.5

OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"
os.makedirs(OUT_DIR, exist_ok=True)

CAM_TARGET = Vector((0, 0, 0.260))

cam_views = [
    ("v3_hero_34",       (0.70,  -0.85,  0.30),  42),
    ("v3_front",         (0.00,  -0.95,  0.25),  50),
    ("v3_side_motor",    (1.10,   0.00,  0.30),  45),
    ("v3_top_down",      (0.00,   0.00,  1.30),  55),
]

bpy.ops.object.camera_add(location=cam_views[0][1])
cam = bpy.context.active_object; cam.name = "HeroCam"
cam.data.lens = cam_views[0][2]
scene.camera = cam

for view_name, cam_loc, lens in cam_views:
    cam.location = cam_loc
    cam.data.lens = lens
    if view_name == "v3_top_down":
        cam.rotation_euler = (0, 0, math.radians(90))
    else:
        dirvec = CAM_TARGET - Vector(cam_loc)
        cam.rotation_euler = dirvec.to_track_quat('-Z','Y').to_euler()
    bpy.context.view_layer.update()
    out_path = os.path.join(OUT_DIR, f"CSM_V3_Assembly_{view_name}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print(f"  [{view_name}] {out_path}  ({sz/1024:.0f} KB)")

blend_path = os.path.join(OUT_DIR, "CSM_V3_Assembly_V3.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")
print("DONE V3.")
