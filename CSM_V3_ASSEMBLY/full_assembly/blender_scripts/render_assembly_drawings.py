# -*- coding: utf-8 -*-
"""
CSM V3 -- ARCHITECTURAL VALIDATION DRAWINGS (Priority C)

NOT a hero render. This is an engineering validation pass:
  - Orthographic views (no perspective distortion)
  - Service envelopes overlaid as semi-transparent volumes
  - Maintenance vectors (extraction arrows, swing arcs, tool cones)
  - Critical-triad zoom (feeder exit / retainer lip / hook peak)

The goal of these drawings is to expose hidden conflicts:
  - unreachable fasteners
  - cable interference paths
  - feeder swing collisions
  - cylinder lift obstructions
  - tool-access blind spots

Uses BOM-aligned geometry: FeederModule V1.1, Motor Mount V1.4.
The NEMA 23 + gearbox is rendered as a primitive solid sized to BOM dims
(no V1.0 STL yet for NEMA 23 -- placeholder box is dimensionally correct).

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_assembly_drawings.py
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

def add_stl(name, path, t_mm=(0.0,0.0,0.0), rz_deg=0.0):
    if not os.path.exists(path):
        print(f"  [MISS] {name}: {path}")
        return None
    before = set(bpy.data.objects)
    import_stl(path)
    new = list(set(bpy.data.objects) - before)
    if not new: return None
    obj = new[0]
    obj.name = name
    obj.scale = (mm, mm, mm)
    obj.location = (t_mm[0]*mm, t_mm[1]*mm, t_mm[2]*mm)
    if rz_deg:
        obj.rotation_euler = (0, 0, math.radians(rz_deg))
    bpy.context.view_layer.update()
    return obj

def add_box(name, sx, sy, sz, x=0, y=0, z=0, mat=None, rz_deg=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x*mm, y*mm, z*mm))
    o = bpy.context.active_object
    o.name = name
    o.scale = (sx*mm/2, sy*mm/2, sz*mm/2)
    bpy.ops.object.transform_apply(scale=True)
    if rz_deg:
        o.rotation_euler = (0, 0, math.radians(rz_deg))
    if mat: assign(o, mat)
    return o

def add_cyl(name, r, h, x=0, y=0, z=0, mat=None, axis='Z'):
    bpy.ops.mesh.primitive_cylinder_add(radius=r*mm, depth=h*mm,
                                        location=(x*mm, y*mm, z*mm))
    o = bpy.context.active_object
    o.name = name
    if axis == 'Y':
        o.rotation_euler = (math.radians(90), 0, 0)
    elif axis == 'X':
        o.rotation_euler = (0, math.radians(90), 0)
    if mat: assign(o, mat)
    return o

def add_arrow(name, tail_xyz_mm, head_xyz_mm, radius=2.5, mat=None):
    """Add an arrow from tail to head as a cylinder + cone."""
    tail = Vector(tail_xyz_mm) * mm
    head = Vector(head_xyz_mm) * mm
    dirv = head - tail
    length = dirv.length
    if length < 1e-6: return None
    # cylinder portion (shaft is 80% of length, cone is 20%)
    shaft_len = length * 0.8
    cone_len  = length * 0.2
    cone_r = radius * 2.5 * mm
    # Build at origin pointing +Z, then orient
    shaft_loc = tail + dirv * 0.4
    cone_loc  = tail + dirv * 0.9
    # Shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=radius*mm, depth=shaft_len,
                                        location=shaft_loc)
    sh = bpy.context.active_object; sh.name = f"{name}_shaft"
    quat = dirv.to_track_quat('Z', 'Y')
    sh.rotation_euler = quat.to_euler()
    # Cone
    bpy.ops.mesh.primitive_cone_add(radius1=cone_r, radius2=0,
                                    depth=cone_len, location=cone_loc)
    co = bpy.context.active_object; co.name = f"{name}_head"
    co.rotation_euler = quat.to_euler()
    if mat:
        assign(sh, mat); assign(co, mat)
    return sh, co

# ============================================================
# MATERIALS
# ============================================================
M = {}
M['wood']        = make_mat("Wood",            (0.32, 0.16, 0.06, 1), 0.55)
M['ext_2020']    = make_mat("Ext_2020",        (0.10, 0.10, 0.11, 1), 0.45, 0.7)
M['alu']         = make_mat("Aluminum",        (0.82, 0.84, 0.87, 1), 0.28, 1.0)
M['cyl']         = make_mat("Cylinder",        (0.85, 0.86, 0.88, 1), 0.32)
M['cam']         = make_mat("CamRing",         (0.08, 0.08, 0.10, 1), 0.25, 0.5)
M['cassette']    = make_mat("Cassette",        (0.65, 0.68, 0.72, 1), 0.35)
M['sinker']      = make_mat("Sinker",          (0.55, 0.58, 0.62, 1), 0.35)
M['retainer']    = make_mat("Retainer",        (0.92, 0.86, 0.68, 1), 0.50)
M['drive_hub']   = make_mat("DriveHub",        (0.78, 0.80, 0.83, 1), 0.20, 1.0)
M['bearings']    = make_mat("Bearings",        (0.40, 0.42, 0.45, 1), 0.40)
M['motor']       = make_mat("Motor",           (0.03, 0.03, 0.04, 1), 0.40, 0.1)
M['gearbox']     = make_mat("Gearbox",         (0.20, 0.20, 0.22, 1), 0.40, 0.5)
M['motor_mount'] = make_mat("MotorMount_V14",  (0.20, 0.40, 0.50, 1), 0.40)
M['feeder']      = make_mat("Feeder_V11",      (0.78, 0.72, 0.55, 1), 0.45)
M['yarn_r']      = make_mat("Yarn_R",          (0.78, 0.10, 0.10, 1), 0.85)
M['yarn_b']      = make_mat("Yarn_B",          (0.08, 0.22, 0.78, 1), 0.85)
M['screen']      = make_mat("Screen",          (0.05, 0.10, 0.18, 1), 0.20)

# Service envelopes -- semi-transparent
M['SE1_red']     = make_mat("SE1_lift",    (1.00, 0.20, 0.20, 0.30), 0.50, alpha=0.30)
M['SE3_blue']    = make_mat("SE3_feeder",  (0.20, 0.40, 1.00, 0.25), 0.50, alpha=0.25)
M['SE5_yellow']  = make_mat("SE5_belt",    (1.00, 0.90, 0.10, 0.30), 0.50, alpha=0.30)
M['takedown_g']  = make_mat("Takedown",    (0.20, 0.90, 0.40, 0.25), 0.50, alpha=0.25)

# Maintenance vector arrows
M['arrow_red']   = make_mat("Arrow_Lift",     (1.00, 0.10, 0.10, 1), 0.40)
M['arrow_blue']  = make_mat("Arrow_Feeder",   (0.10, 0.30, 1.00, 1), 0.40)
M['arrow_yellow']= make_mat("Arrow_Belt",     (1.00, 0.80, 0.10, 1), 0.40)
M['arrow_green'] = make_mat("Arrow_Takedown", (0.10, 0.80, 0.30, 1), 0.40)

# ============================================================
# IMPORT GEOMETRY (BOM-aligned)
# ============================================================
print("Importing geometry (BOM-aligned)...")
ROOT_ASM  = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
ROOT_LOCK = r"C:\3D-Project\01_MECHANICAL"
WZ = MD.CYL_BOTTOM_WORLD_Z

# Frame
o = add_stl("WoodBase", os.path.join(ROOT_ASM, "frame", "wood_base", "CSM_V3_WoodBase_V1_1.stl"))
if o: assign(o, M['wood'])
for i,(ux,uy) in enumerate([(+150,+120),(+150,-120),(-150,+120),(-150,-120)]):
    o = add_stl(f"Upright_{i}",
                os.path.join(ROOT_ASM,"frame","upright_2020","CSM_V3_Upright2020_V1_1.stl"),
                t_mm=(ux,uy,0))
    if o: assign(o, M['ext_2020'])
o = add_stl("UpperDeck", os.path.join(ROOT_ASM,"frame","wood_upper_deck","CSM_V3_WoodUpperDeck_V1_0.stl"))
if o: assign(o, M['wood'])
o = add_stl("MountPlate", os.path.join(ROOT_ASM,"frame","mount_plate_6061","CSM_V3_MountPlate6061_V1_1.stl"))
if o: assign(o, M['alu'])
o = add_stl("Mast", os.path.join(ROOT_ASM,"frame","touchscreen_mast","CSM_V3_TouchscreenMast_V1_0.stl"))
if o: assign(o, M['ext_2020'])

# Cassette
o = add_stl("Cylinder", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","cylinder","CSM_V3_Cylinder_V3_0_FULL.stl"),
            t_mm=(0,0,WZ))
if o: assign(o, M['cyl'])
o = add_stl("CamRing", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","cam_ring","CSM_V3_CamRing_V6_5_FULL.stl"),
            t_mm=(0,0,19+WZ))
if o: assign(o, M['cam'])
o = add_stl("Cassette", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","cassette_base","CSM_V3_CassetteBase_V1_1_FULL.stl"),
            t_mm=(0,0,49+WZ))
if o: assign(o, M['cassette'])
o = add_stl("Sinker", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","sinker_ring","CSM_V3_SinkerRing_V1_2_1_FULL.stl"),
            t_mm=(0,0,75+WZ))
if o: assign(o, M['sinker'])
o = add_stl("Retainer", os.path.join(ROOT_LOCK,"02_CASSETTE_HEAD","retainer_ring","CSM_V3_RetainerRing_V1_0_FULL.stl"),
            t_mm=(0,0,83+WZ))
if o: assign(o, M['retainer'])

# Drive train (locked + BOM-aligned)
o = add_stl("DriveHub", os.path.join(ROOT_LOCK,"06_DRIVE_SYSTEM","CSM_V3_DriveHub_V2_4_2.stl"),
            t_mm=(0,0,-10+WZ))
if o: assign(o, M['drive_hub'])
o = add_stl("Bearings", os.path.join(ROOT_LOCK,"05_BEARINGS_SHAFT","CSM_V3_BearingHousings_PAIR_V2_5_1.stl"),
            t_mm=(0,0,-70+WZ))
if o: assign(o, M['bearings'])

# Motor Mount V1.4 (BOM-aligned, replaces V1.3)
o = add_stl("MotorMount_V14",
            os.path.join(ROOT_ASM,"drive_bought","motor_mount_v1_4","CSM_V3_MotorMount_V1_4.stl"))
if o: assign(o, M['motor_mount'])

# NEMA 23 + Gearbox -- placeholder primitive (no STL yet) sized per BOM
# Body: 57x57x56 (NEMA 23 frame)
# Gearbox: cylindrical housing 60 OD x 50 mm below motor body
# Position: motor body bottom at gearbox-top Z = 70 + 50 = 120 (gearbox below motor)
# Wait -- per Motor Mount V1.4 design: gearbox flange bolts to bracket head at Z=70.
# Gearbox extends UPWARD from Z=70 to Z=70+50=120 (gearbox housing top = motor flange bottom).
# Motor body extends UPWARD from Z=120 to Z=120+56=176.
GEARBOX_Z_BOTTOM = 70.0
GEARBOX_Z_TOP    = GEARBOX_Z_BOTTOM + MD.GEARBOX_LENGTH   # 120
MOTOR_Z_BOTTOM   = GEARBOX_Z_TOP
MOTOR_Z_TOP      = MOTOR_Z_BOTTOM + MD.NEMA23_BODY_L      # 176

# Gearbox cylinder
add_cyl("Gearbox", MD.GEARBOX_FLANGE_OD/2.0, MD.GEARBOX_LENGTH,
        x=MD.MOTOR_X, y=MD.MOTOR_Y, z=(GEARBOX_Z_BOTTOM+GEARBOX_Z_TOP)/2.0,
        mat=M['gearbox'])
# Motor body box
add_box("NEMA23_Body", MD.NEMA23_BODY_W, MD.NEMA23_BODY_W, MD.NEMA23_BODY_L,
        x=MD.MOTOR_X, y=MD.MOTOR_Y, z=(MOTOR_Z_BOTTOM+MOTOR_Z_TOP)/2.0,
        mat=M['motor'])

# 60T pulley (BIG) on gearbox output shaft -- below the mount bracket head plate
# Gearbox output shaft exits DOWNWARD from gearbox housing bottom (Z=70).
# Pulley sits below the bracket head plate. Pulley centerline at Z=62.
# Drive pulley (20T) on drive shaft at same Z so belt is horizontal.
PULLEY_Z = 62.0
add_cyl("Pulley_60T_GearboxSide",
        MD.PULLEY_BIG_OD/2.0, MD.PULLEY_BIG_W,
        x=MD.MOTOR_X, y=MD.MOTOR_Y, z=PULLEY_Z,
        mat=M['gearbox'])
add_cyl("Pulley_20T_ShaftSide",
        MD.PULLEY_SMALL_OD/2.0, MD.PULLEY_SMALL_W,
        x=0, y=0, z=PULLEY_Z,
        mat=M['gearbox'])

# Feeders V1.1 (Phase 1: F1 + F4)
FEEDER_RADIAL_OFFSET = MD.PCD_FEEDER/2.0 + 25.0   # 120 mm
o = add_stl("Feeder_F1",
            os.path.join(ROOT_ASM,"feeder_module","CSM_V3_FeederModule_V1_1.stl"),
            t_mm=(FEEDER_RADIAL_OFFSET,0,0), rz_deg=-90.0)
if o: assign(o, M['feeder'])
o = add_stl("Feeder_F4",
            os.path.join(ROOT_ASM,"feeder_module","CSM_V3_FeederModule_V1_1.stl"),
            t_mm=(-FEEDER_RADIAL_OFFSET,0,0), rz_deg=+90.0)
if o: assign(o, M['feeder'])

# Yarn cones
o = add_stl("YarnCone_F1",
            os.path.join(ROOT_ASM,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"),
            t_mm=(FEEDER_RADIAL_OFFSET, 20, 250))
if o: assign(o, M['yarn_r'])
o = add_stl("YarnCone_F4",
            os.path.join(ROOT_ASM,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"),
            t_mm=(-FEEDER_RADIAL_OFFSET, -20, 250))
if o: assign(o, M['yarn_b'])

# ============================================================
# SERVICE ENVELOPES (semi-transparent volumes)
# ============================================================
print("Adding service envelopes...")

# SE1: Cylinder removal column -- vertical cylinder above retainer
SE1_R = 60.0
SE1_Z_LOW = 272.0
SE1_Z_HIGH = 430.0
add_cyl("SE1_LiftColumn", SE1_R, SE1_Z_HIGH - SE1_Z_LOW,
        x=0, y=0, z=(SE1_Z_LOW + SE1_Z_HIGH)/2.0,
        mat=M['SE1_red'])

# SE3: Feeder swing-out wedges (6 wedges around PCD 190)
# Visualize the 2 ACTIVE feeders (F1 + F4) -- simpler than 6
for theta_deg, name in [(0.0, "F1"), (180.0, "F4")]:
    th = math.radians(theta_deg)
    sx = (MD.PCD_FEEDER/2 + 25.0) * math.cos(th)
    sy = (MD.PCD_FEEDER/2 + 25.0) * math.sin(th)
    add_box(f"SE3_{name}_swing",
            sx=60, sy=60, sz=70,
            x=sx*1.2, y=sy*1.2, z=255,
            mat=M['SE3_blue'])

# SE5: Belt replacement zone -- motor X-travel slot + vertical pulley clearance
# Box from motor X-travel (60..120) at motor Y, between wood-base top and pulley height
add_box("SE5_BeltZone",
        sx=MD.BELT_TENSION_TRAVEL + 30, sy=80, sz=80,
        x=(60 + 120)/2.0, y=MD.MOTOR_Y, z=(18 + 80)/2.0,
        mat=M['SE5_yellow'])

# Take-down column (Interface 11)
add_cyl("TakedownColumn", 50, 200,
        x=0, y=0, z=85,
        mat=M['takedown_g'])

# ============================================================
# MAINTENANCE VECTORS (arrows showing extraction directions)
# ============================================================
print("Adding maintenance vectors...")

# SE1 -- cylinder extraction (straight up)
add_arrow("SE1_arrow",
          tail_xyz_mm=(0, 0, 272), head_xyz_mm=(0, 0, 380),
          radius=3.0, mat=M['arrow_red'])

# SE3 -- feeder swing-out (radial outward from each Phase 1 feeder)
for theta_deg in (0.0, 180.0):
    th = math.radians(theta_deg)
    r1 = MD.PCD_FEEDER/2.0   # tail at PCD 190
    r2 = MD.PCD_FEEDER/2.0 + 80.0   # head extends outward 80 mm
    add_arrow(f"SE3_arrow_{int(theta_deg)}",
              tail_xyz_mm=(r1*math.cos(th), r1*math.sin(th), 260),
              head_xyz_mm=(r2*math.cos(th), r2*math.sin(th), 260),
              radius=3.0, mat=M['arrow_blue'])

# SE5 -- belt removal (motor X-travel + lift vertical)
add_arrow("SE5_arrow_translate",
          tail_xyz_mm=(MD.MOTOR_X, MD.MOTOR_Y, 65),
          head_xyz_mm=(60.0, MD.MOTOR_Y, 65),
          radius=2.5, mat=M['arrow_yellow'])
add_arrow("SE5_arrow_lift",
          tail_xyz_mm=(MD.MOTOR_X, MD.MOTOR_Y, 65),
          head_xyz_mm=(MD.MOTOR_X, MD.MOTOR_Y, 145),
          radius=2.5, mat=M['arrow_yellow'])

# Take-down column -- sock exits downward
add_arrow("Takedown_arrow",
          tail_xyz_mm=(0, 0, 170), head_xyz_mm=(0, 0, -20),
          radius=3.0, mat=M['arrow_green'])

# ============================================================
# GROUND PLANE (subtle, just for orientation)
# ============================================================
bpy.ops.mesh.primitive_plane_add(size=2.5, location=(0,0,-0.001))
g = bpy.context.active_object; g.name = "Ground"
assign(g, make_mat("Ground", (0.85, 0.85, 0.88, 1), 0.6))

# ============================================================
# LIGHTING (uniform / clinical, not dramatic)
# ============================================================
def add_light(name, ltype, loc, energy, rot=(0,0,0), size=1.0):
    bpy.ops.object.light_add(type=ltype, location=loc)
    L = bpy.context.active_object; L.name = name
    L.data.energy = energy
    if hasattr(L.data, 'size'): L.data.size = size
    L.rotation_euler = rot
    return L

add_light("KeyLight",  'SUN',  loc=(0,-1,2), energy=2.0, rot=(math.radians(35), 0, math.radians(20)))
add_light("FillFront", 'AREA', loc=(0, 0.5, 0.4), energy=60, rot=(math.radians(70), 0, 0), size=1.5)
add_light("FillSide",  'AREA', loc=(0.5, 0, 0.4), energy=40, rot=(0, math.radians(70), 0), size=1.0)

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.92, 0.92, 0.94, 1.0)   # light gray
    bg.inputs[1].default_value = 0.55

# ============================================================
# RENDER SETTINGS (clinical, fast)
# ============================================================
scene = bpy.context.scene
try:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    try: scene.cycles.device = 'GPU'
    except Exception: pass
except Exception:
    for cand in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
        try: scene.render.engine = cand; break
        except Exception: continue

scene.render.resolution_x = 1920
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'

OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# ORTHOGRAPHIC CAMERAS
# ============================================================
# 5 views, all ORTHO (no perspective distortion).
# Cameras positioned far away to ensure ortho scale is set correctly.

def setup_ortho_camera(name, loc, look_at, ortho_scale_m):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.name = name
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = ortho_scale_m
    dirv = Vector(look_at) - Vector(loc)
    cam.rotation_euler = dirv.to_track_quat('-Z','Y').to_euler()
    return cam

views = [
    # name           camera_pos          look_at           ortho_scale_meters
    ("C_top",        (0.0, 0.0, 2.0),    (0.0, 0.0, 0.20), 0.7),
    ("C_front",      (0.0, -2.0, 0.22),  (0.0, 0.0, 0.22), 0.55),
    ("C_side",       (2.0, 0.0, 0.22),   (0.0, 0.0, 0.22), 0.55),
    ("C_iso",        (1.4, -1.4, 1.0),   (0.0, 0.0, 0.20), 0.75),
    # Detail close-up: feeder F1 exit / retainer lip / hook peak triad
    ("C_triad",      (0.30, -0.30, 0.30), (0.10, 0.0, 0.27), 0.20),
]

renders_done = []
for view_name, cam_loc, look_at, ortho_scale in views:
    cam = setup_ortho_camera(view_name, cam_loc, look_at, ortho_scale)
    scene.camera = cam
    out_path = os.path.join(OUT_DIR, f"CSM_V3_AssemblyDrawing_{view_name}.png")
    scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out_path) if os.path.exists(out_path) else 0
    print(f"  [{view_name}] -> {out_path}  ({sz/1024:.0f} KB)")
    renders_done.append((view_name, out_path))

# Save .blend
blend_path = os.path.join(OUT_DIR, "CSM_V3_AssemblyDrawing.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")
print(f"DONE. {len(renders_done)} orthographic drawings + 1 .blend.")
