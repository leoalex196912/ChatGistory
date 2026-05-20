"""
CSM V3 -- FULL ASSEMBLY HERO RENDER V1
=======================================
Headless Blender script that imports every locked/bought STL,
positions them at the correct world coordinates per MACHINE_DATUMS,
applies materials, sets up lighting + camera, renders PNG + saves .blend.

Run:
  blender --background --python render_hero_v1.py

All Z values per MACHINE_DATUMS (cylinder local coords, Z=0 = cyl bottom).
All units: scene works in mm; final scaled to m at the end (Blender prefers m).
"""

import bpy
import math
import os
from mathutils import Vector

# ============================================================================
# PATHS
# ============================================================================
REPO  = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo"
LOCK  = REPO + r"\3D-Project\01_MECHANICAL"
NEW   = REPO + r"\CSM_V3_ASSEMBLY"
OUT_PNG  = REPO + r"\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly_Hero.png"
OUT_BLEND = REPO + r"\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly.blend"

# ============================================================================
# 1. RESET SCENE
# ============================================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)
for m in list(bpy.data.materials):
    bpy.data.materials.remove(m)

# Scale: STLs are in mm. Blender prefers m. We'll import in mm and scale
# objects by 0.001 at the end. Simpler: leave at mm throughout, set scene
# unit scale to mm. Many Blender setups handle this fine.
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

# ============================================================================
# 2. STL CATALOG
# ============================================================================
# (filepath, object_name, world_loc_mm, rotation_euler_rad, material_key)

STLS = [
    # ---- LOCKED CASSETTE HEAD ----
    (LOCK + r"\02_CASSETTE_HEAD\cylinder\CSM_V3_Cylinder_V3_0_FULL.stl",
     "Cylinder",   (0, 0, 0),    (0, 0, 0), 'petg_white'),
    (LOCK + r"\02_CASSETTE_HEAD\cam_ring\CSM_V3_CamRing_V6_5_FULL.stl",
     "CamRing",    (0, 0, 19),   (0, 0, 0), 'anodized_black'),
    (LOCK + r"\02_CASSETTE_HEAD\cassette_base\CSM_V3_CassetteBase_V1_1_FULL.stl",
     "CassetteBase",(0, 0, 49),  (0, 0, 0), 'petg_orange'),
    (LOCK + r"\02_CASSETTE_HEAD\sinker_ring\CSM_V3_SinkerRing_V1_2_1_FULL.stl",
     "SinkerRing", (0, 0, 75),   (0, 0, 0), 'petg_blue'),
    (LOCK + r"\02_CASSETTE_HEAD\retainer_ring\CSM_V3_RetainerRing_V1_0_FULL.stl",
     "RetainerRing",(0, 0, 83),  (0, 0, 0), 'pa12_cream'),

    # ---- LOCKED DRIVE COMPONENTS ----
    (LOCK + r"\06_DRIVE_SYSTEM\CSM_V3_DriveHub_V2_4_2.stl",
     "DriveHub",   (0, 0, -10),  (0, 0, 0), 'aluminum'),
    (LOCK + r"\05_BEARINGS_SHAFT\CSM_V3_BearingHousings_PAIR_V2_5_1.stl",
     "BearingHousings", (0, 0, -90), (0, 0, 0), 'petg_red'),
    (LOCK + r"\06_DRIVE_SYSTEM\CSM_V3_MotorMount_V1_3.stl",
     "MotorMount", (0, 0, -130), (0, 0, 0), 'petg_green'),

    # ---- NEW: FRAME ----
    (NEW + r"\frame\wood_shelf_mid\CSM_V3_WoodShelfMid_V1_0.stl",
     "WoodShelfMid", (0, 0, 0),  (0, 0, 0), 'wood_walnut'),
    (NEW + r"\frame\wood_base\CSM_V3_WoodBase_V1_0.stl",
     "WoodBase",     (0, 0, 0),  (0, 0, 0), 'wood_walnut'),
    (NEW + r"\frame\mount_plate_6061\CSM_V3_MountPlate6061_V1_0.stl",
     "MountPlate",   (0, 0, 0),  (0, 0, 0), 'aluminum'),

    # 4 uprights at corners of wood. Upright builds from Z=-300 to Z=31.
    (NEW + r"\frame\upright_2020\CSM_V3_Upright2020_V1_0.stl",
     "Upright_NE", ( 230,  180, 0), (0, 0, 0), 'anodized_black'),
    (NEW + r"\frame\upright_2020\CSM_V3_Upright2020_V1_0.stl",
     "Upright_NW", (-230,  180, 0), (0, 0, 0), 'anodized_black'),
    (NEW + r"\frame\upright_2020\CSM_V3_Upright2020_V1_0.stl",
     "Upright_SE", ( 230, -180, 0), (0, 0, 0), 'anodized_black'),
    (NEW + r"\frame\upright_2020\CSM_V3_Upright2020_V1_0.stl",
     "Upright_SW", (-230, -180, 0), (0, 0, 0), 'anodized_black'),

    # ---- NEW: DRIVE TRAIN (BOUGHT) ----
    # Motor: body 40mm + boss 2 + shaft 24. Shaft pointing +Z (up).
    # We want motor shaft top at ~Z=-44 so 16T pulley center at Z=-60.
    # Motor body builds 0..40. Position with translate Z = -130 -> body at -130..-90, boss -90..-88, shaft -88..-64.
    # Shaft top at -64, so 16T pulley needs to be on that shaft from -68..-52.
    (NEW + r"\drive_bought\nema17_stepper\CSM_V3_NEMA17_V1_0.stl",
     "NEMA17", (90, 0, -130),  (0, 0, 0), 'motor_black'),

    # Pulley macros build from Z=0..WIDTH (16). For belt centerline at Z=-60
    # we want pulley Z=0 maps to Z=-68 (centerline at -68+16/2 = -60).
    (NEW + r"\drive_bought\pulley_htd_60t\CSM_V3_PulleyHTD60T_V1_0.stl",
     "Pulley_60T", (0, 0, -68), (0, 0, 0), 'pulley_black'),
    (NEW + r"\drive_bought\pulley_htd_16t\CSM_V3_PulleyHTD16T_V1_0.stl",
     "Pulley_16T", (90, 0, -68), (0, 0, 0), 'pulley_black'),

    # Belt centered on world XY plane; macro centers Z extent on 0.
    (NEW + r"\drive_bought\belt_htd_5m\CSM_V3_BeltHTD5M_V1_0.stl",
     "Belt", (0, 0, -60), (0, 0, 0), 'belt_black'),

    # ---- NEW: BEARINGS + SHAFT ----
    # Two 6001 bearings inside BearingHousings_PAIR (which is at Z=-90).
    # Bearings: width 8mm each. Place one at upper position Z=-78, one at -100.
    (NEW + r"\bearings_bought\bearing_6001_2rs\CSM_V3_Bearing6001_V1_0.stl",
     "Bearing_Top", (0, 0, -78),  (0, 0, 0), 'steel'),
    (NEW + r"\bearings_bought\bearing_6001_2rs\CSM_V3_Bearing6001_V1_0.stl",
     "Bearing_Bot", (0, 0, -110), (0, 0, 0), 'steel'),

    # Shaft 12x150 from Z=-160..-10 (set translate so macro's Z=0..150 maps to -160..-10)
    (NEW + r"\bearings_bought\shaft_12mm\CSM_V3_Shaft12mm_V1_0.stl",
     "DriveShaft", (0, 0, -160), (0, 0, 0), 'steel'),

    # ---- NEW: ELECTRONICS (on wood base) ----
    # Wood base top at Z=-282. All electronics sit at Z=-282 (their own height adds up).
    (NEW + r"\electronics\arduino_mega_2560\CSM_V3_ArduinoMega_V1_0.stl",
     "ArduinoMega", (-140, 80, -282), (0, 0, math.radians(0)), 'pcb_green'),
    (NEW + r"\electronics\tb6600_driver\CSM_V3_TB6600_V1_0.stl",
     "TB6600", (-100, -80, -282), (0, 0, 0), 'tb_blue'),
    (NEW + r"\electronics\lrs50_psu\CSM_V3_LRS50_V1_0.stl",
     "LRS50", (140, -80, -282), (0, 0, 0), 'psu_steel'),

    # ---- NEW: TOUCHSCREEN + ARM ----
    # Arm clamps to NE upright at z ~ 30 (top of upright)
    (NEW + r"\electronics\touchscreen_arm\CSM_V3_TouchscreenArm_V1_0.stl",
     "TouchscreenArm", (-235, 0, 0), (0, 0, math.radians(0)), 'petg_white'),

    # Touchscreen mounted at end of arm. Arm end ~ (-235 + 5 + 120*cos30, 0, 0 + 30 + 120*sin30)
    # = (-235 + 5 + 104, 0, 30 + 60) = (-126, 0, 90)
    (NEW + r"\electronics\touchscreen_7in\CSM_V3_Touchscreen7in_V1_0.stl",
     "Touchscreen", (-200, 0, 60), (math.radians(0), math.radians(-30), 0), 'screen_bezel'),
    (NEW + r"\electronics\touchscreen_7in\CSM_V3_Touchscreen7in_Screen_V1_0.stl",
     "TouchscreenGlow", (-200, 0, 60), (math.radians(0), math.radians(-30), 0), 'screen_glow'),

    # ---- NEW: YARN CONES (2) at top of machine ----
    (NEW + r"\decor\yarn_cone\CSM_V3_YarnCone_V1_0.stl",
     "Yarn_Red",  ( 90, 0, 95), (0, 0, 0), 'yarn_red'),
    (NEW + r"\decor\yarn_cone\CSM_V3_YarnCone_V1_0.stl",
     "Yarn_Blue", (-90, 0, 95), (0, 0, 0), 'yarn_blue'),
]

# ============================================================================
# 3. MATERIALS
# ============================================================================
def make_mat(name, base, rough=0.4, metal=0.0, emission=None, emission_strength=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = (*base, 1.0)
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            if emission is not None and "Emission Color" in n.inputs:
                n.inputs["Emission Color"].default_value = (*emission, 1.0)
                n.inputs["Emission Strength"].default_value = emission_strength
            elif emission is not None and "Emission" in n.inputs:
                n.inputs["Emission"].default_value = (*emission, 1.0)
    return m

MATS = {
    'petg_white':     make_mat('PETG_White',     (0.92, 0.93, 0.95),     0.30),
    'petg_orange':    make_mat('PETG_Orange',    (0.95, 0.45, 0.10),     0.40),
    'petg_blue':      make_mat('PETG_Blue',      (0.08, 0.35, 0.80),     0.35),
    'petg_red':       make_mat('PETG_Red',       (0.85, 0.12, 0.10),     0.40),
    'petg_green':     make_mat('PETG_Green',     (0.12, 0.65, 0.25),     0.40),
    'pa12_cream':     make_mat('PA12_Cream',     (0.92, 0.86, 0.70),     0.55),
    'anodized_black': make_mat('Anodized_Black', (0.04, 0.04, 0.05),     0.30, 0.85),
    'aluminum':       make_mat('Aluminum_6061',  (0.78, 0.80, 0.84),     0.25, 1.00),
    'wood_walnut':    make_mat('Wood_Walnut',    (0.32, 0.16, 0.07),     0.55),
    'motor_black':    make_mat('Motor_Black',    (0.025, 0.025, 0.030),  0.45, 0.10),
    'pulley_black':   make_mat('Pulley_Black',   (0.04, 0.04, 0.05),     0.55),
    'belt_black':     make_mat('Belt_Black',     (0.020, 0.020, 0.020),  0.75),
    'steel':          make_mat('Steel_Bright',   (0.80, 0.82, 0.85),     0.20, 1.00),
    'pcb_green':      make_mat('PCB_Green',      (0.05, 0.35, 0.10),     0.55),
    'tb_blue':        make_mat('TB_Blue_Alum',   (0.20, 0.30, 0.55),     0.40, 0.50),
    'psu_steel':      make_mat('PSU_Steel',      (0.65, 0.65, 0.68),     0.45, 0.60),
    'screen_bezel':   make_mat('Screen_Bezel',   (0.02, 0.02, 0.02),     0.30),
    'screen_glow':    make_mat('Screen_Glow',    (0.10, 0.18, 0.30),     0.20, 0.0,
                               emission=(0.20, 0.45, 0.90), emission_strength=2.5),
    'yarn_red':       make_mat('Yarn_Red',       (0.82, 0.08, 0.10),     0.85),
    'yarn_blue':      make_mat('Yarn_Blue',      (0.05, 0.20, 0.85),     0.85),
}

# ============================================================================
# 4. IMPORT + POSITION
# ============================================================================
def import_stl(path):
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=path)
    else:
        bpy.ops.import_mesh.stl(filepath=path)

import_summary = []
for path, name, loc, rot, mat_key in STLS:
    if not os.path.exists(path):
        import_summary.append(f"MISSING: {name}  -> {path}")
        continue
    before = set(bpy.data.objects)
    try:
        import_stl(path)
    except Exception as ex:
        import_summary.append(f"FAIL {name}: {ex}")
        continue
    new_objs = list(set(bpy.data.objects) - before)
    if not new_objs:
        import_summary.append(f"NO_OBJECT for {name}")
        continue
    obj = new_objs[0]
    obj.name = name
    obj.location = loc
    obj.rotation_euler = rot
    # Assign material
    obj.data.materials.clear()
    obj.data.materials.append(MATS[mat_key])
    import_summary.append(f"OK {name:25s} @ ({loc[0]:+7.1f},{loc[1]:+7.1f},{loc[2]:+7.1f})  mat={mat_key}")

print("=" * 70)
print("IMPORT SUMMARY")
print("=" * 70)
for line in import_summary:
    print(line)
print(f"\nTotal objects: {len([o for o in bpy.data.objects if o.type=='MESH'])}")

# ============================================================================
# 5. LIGHTING
# ============================================================================
# Three-point in Cycles. Key from front-right, fill from left, rim from behind.
def add_light(name, type_, loc, energy, rot=(0,0,0), size=1.0, color=(1,1,1)):
    bpy.ops.object.light_add(type=type_, location=loc)
    l = bpy.context.active_object
    l.name = name
    l.data.energy = energy
    l.rotation_euler = rot
    l.data.color = color
    if type_ == 'AREA':
        l.data.size = size
    return l

# Key
add_light("Key", 'AREA', (650, -700, 350), 30000,
          rot=(math.radians(55), 0, math.radians(45)), size=400)
# Fill
add_light("Fill", 'AREA', (-700, -300, 250), 12000,
          rot=(math.radians(70), 0, math.radians(-100)), size=600)
# Rim
add_light("Rim", 'AREA', (0, 800, 500), 18000,
          rot=(math.radians(120), 0, math.radians(180)), size=400)

# Sun for soft ambient
bpy.ops.object.light_add(type='SUN', location=(0, 0, 2000))
sun = bpy.context.active_object; sun.name = "AmbientSun"
sun.data.energy = 0.6
sun.data.angle = math.radians(45)
sun.rotation_euler = (math.radians(45), math.radians(-15), 0)

# World
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.20, 0.22, 0.28, 1.0)
    bg.inputs[1].default_value = 0.30

# ============================================================================
# 6. CAMERA
# ============================================================================
bpy.ops.object.camera_add(location=(720, -800, 150))
cam = bpy.context.active_object
cam.name = "HeroCamera"
cam.data.lens = 50  # mm
target = Vector((0, 0, -60))
direction = target - Vector(cam.location)
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# ============================================================================
# 7. GROUND
# ============================================================================
bpy.ops.mesh.primitive_plane_add(size=3000, location=(0, 0, -310))
gnd = bpy.context.active_object
gnd.name = "Ground"
gmat = make_mat('Ground_Grey', (0.45, 0.45, 0.48), 0.65)
gnd.data.materials.append(gmat)

# ============================================================================
# 8. RENDER SETTINGS
# ============================================================================
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
try:
    scene.cycles.device = 'GPU'
    prefs = bpy.context.preferences.addons.get('cycles')
    if prefs:
        prefs.preferences.compute_device_type = 'CUDA'
except Exception:
    pass
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0.0

# ============================================================================
# 9. SAVE BLEND + RENDER
# ============================================================================
os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print(f"[OK] saved .blend: {OUT_BLEND}")

scene.render.filepath = OUT_PNG
bpy.ops.render.render(write_still=True)
print(f"[OK] rendered PNG: {OUT_PNG}  ({os.path.getsize(OUT_PNG)} bytes)")
