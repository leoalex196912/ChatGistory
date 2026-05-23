# -*- coding: utf-8 -*-
"""
CSM V3 -- MACHINE DIAGRAM SET (5 specialized views)

This is the upgrade from "single hero render" to a coherent engineering
diagram set. Each view answers a different question about the machine:

  D1  Full machine isometric  -- "What does the machine look like?"
  D2  Side section (elevation) -- "How does it stack vertically?"
  D3  Triad detail             -- "How is yarn captured?" (link to
                                   existing render_kinematic_triad.py;
                                   reproduced here for completeness)
  D4  Top architecture plan    -- "Where are the PCDs / feeders / θ=0°?"
  D5  Layer separation         -- "Precision / Structural / Automation?"

Designed AFTER the architecture is BOM-aligned + interfaces locked.
This is the first time the machine is coherent enough that diagrams
will not need to be re-drawn next week.

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_diagram_set.py
"""
import bpy, math, sys, os
from mathutils import Vector

sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

mm = 0.001

# ============================================================
# RESET + HELPERS
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for m in list(bpy.data.materials):   bpy.data.materials.remove(m)

def mk(name, base=(0.7,0.7,0.72,1.0), rough=0.4, metal=0.0, alpha=1.0, emit=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = base
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            if "Alpha" in n.inputs:
                n.inputs["Alpha"].default_value = alpha
                if alpha < 1.0: m.blend_method = 'BLEND'
            if emit is not None and "Emission" in n.inputs:
                n.inputs["Emission"].default_value = emit
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

def box(name, sx, sy, sz, x=0, y=0, z=0, mat=None, rz=0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x*mm,y*mm,z*mm))
    o = bpy.context.active_object; o.name = name
    o.scale = (sx*mm/2, sy*mm/2, sz*mm/2)
    bpy.ops.object.transform_apply(scale=True)
    if rz: o.rotation_euler = (0,0,math.radians(rz))
    if mat: assign(o, mat)
    return o

def cyl(name, r, h, x=0, y=0, z=0, mat=None, axis='Z'):
    bpy.ops.mesh.primitive_cylinder_add(radius=r*mm, depth=h*mm,
                                        location=(x*mm,y*mm,z*mm))
    o = bpy.context.active_object; o.name = name
    if axis=='Y': o.rotation_euler = (math.radians(90),0,0)
    elif axis=='X': o.rotation_euler = (0,math.radians(90),0)
    if mat: assign(o, mat)
    return o

def torus(name, R, r, x=0, y=0, z=0, mat=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=R*mm, minor_radius=r*mm,
                                     location=(x*mm,y*mm,z*mm))
    o = bpy.context.active_object; o.name = name
    if mat: assign(o, mat)
    return o

# ============================================================
# MATERIALS
# ============================================================
M = {
    # Layer 1 (Precision Core) -- warm tones
    'L1_cyl':       mk("L1_Cyl",       (0.92, 0.87, 0.72, 1), 0.30),
    'L1_cam':       mk("L1_Cam",       (0.85, 0.60, 0.25, 1), 0.30, 0.4),
    'L1_cassette':  mk("L1_Cass",      (0.95, 0.82, 0.55, 1), 0.35),
    'L1_sinker':    mk("L1_Sink",      (0.88, 0.75, 0.40, 1), 0.35),
    'L1_retainer':  mk("L1_Ret",       (0.95, 0.65, 0.30, 1), 0.45),

    # Layer 2 (Structural Frame) -- cool / metallic
    'L2_wood':      mk("L2_Wood",      (0.32, 0.18, 0.08, 1), 0.55),
    'L2_alu':       mk("L2_Alu",       (0.78, 0.82, 0.86, 1), 0.25, 1.0),
    'L2_ext':       mk("L2_Ext",       (0.10, 0.10, 0.12, 1), 0.45, 0.7),
    'L2_hub':       mk("L2_Hub",       (0.75, 0.78, 0.82, 1), 0.20, 1.0),
    'L2_bearings':  mk("L2_Brg",       (0.40, 0.45, 0.55, 1), 0.40),
    'L2_mount':     mk("L2_Mnt",       (0.30, 0.40, 0.50, 1), 0.40),

    # Layer 3 (Automation) -- accent colors
    'L3_motor':     mk("L3_Motor",     (0.05, 0.05, 0.06, 1), 0.40, 0.10),
    'L3_gearbox':   mk("L3_Gear",      (0.20, 0.20, 0.22, 1), 0.40, 0.50),
    'L3_pulley':    mk("L3_Pul",       (0.10, 0.10, 0.12, 1), 0.55),
    'L3_belt':      mk("L3_Belt",      (0.02, 0.02, 0.02, 1), 0.80),
    'L3_feeder':    mk("L3_Feed",      (0.85, 0.75, 0.45, 1), 0.45),
    'L3_yarn_r':    mk("L3_YarnR",     (0.85, 0.12, 0.10, 1), 0.85),
    'L3_yarn_b':    mk("L3_YarnB",     (0.10, 0.25, 0.85, 1), 0.85),
    'L3_screen':    mk("L3_Screen",    (0.10, 0.20, 0.45, 1), 0.20),
    'L3_pcb':       mk("L3_PCB",       (0.05, 0.35, 0.12, 1), 0.50),

    # Annotation
    'PCD_marker':   mk("PCD",          (1.00, 0.25, 0.15, 1), 0.30),
    'theta0_arrow': mk("Theta0",       (1.00, 0.45, 0.00, 1), 0.30),
    'feeder_label': mk("FlblBg",       (0.95, 0.95, 0.20, 1), 0.40),
    'ground':       mk("Ground",       (0.93, 0.93, 0.95, 1), 0.65),
}

# ============================================================
# COMPLETE ASSEMBLY LOAD  (BOM-aligned, V1.4 motor mount, V1.1 feeders)
# ============================================================
print("Loading full BOM-aligned assembly...")
A = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
L = r"C:\3D-Project\01_MECHANICAL"
WZ = MD.CYL_BOTTOM_WORLD_Z

# Frame (Layer 2)
imp("WoodBase",      os.path.join(A,"frame","wood_base","CSM_V3_WoodBase_V1_1.stl"), mat=M['L2_wood'])
for i,(ux,uy) in enumerate([(+150,+120),(+150,-120),(-150,+120),(-150,-120)]):
    imp(f"Upright_{i}", os.path.join(A,"frame","upright_2020","CSM_V3_Upright2020_V1_1.stl"),
        t_mm=(ux,uy,0), mat=M['L2_ext'])
imp("UpperDeck",     os.path.join(A,"frame","wood_upper_deck","CSM_V3_WoodUpperDeck_V1_0.stl"), mat=M['L2_wood'])
imp("MountPlate",    os.path.join(A,"frame","mount_plate_6061","CSM_V3_MountPlate6061_V1_1.stl"), mat=M['L2_alu'])
imp("Mast",          os.path.join(A,"frame","touchscreen_mast","CSM_V3_TouchscreenMast_V1_0.stl"), mat=M['L2_ext'])

# Cassette (Layer 1)
imp("Cylinder",  os.path.join(L,"02_CASSETTE_HEAD","cylinder","CSM_V3_Cylinder_V3_0_FULL.stl"),    t_mm=(0,0,WZ), mat=M['L1_cyl'])
imp("CamRing",   os.path.join(L,"02_CASSETTE_HEAD","cam_ring","CSM_V3_CamRing_V6_5_FULL.stl"),     t_mm=(0,0,19+WZ), mat=M['L1_cam'])
imp("Cassette",  os.path.join(L,"02_CASSETTE_HEAD","cassette_base","CSM_V3_CassetteBase_V1_1_FULL.stl"), t_mm=(0,0,49+WZ), mat=M['L1_cassette'])
imp("Sinker",    os.path.join(L,"02_CASSETTE_HEAD","sinker_ring","CSM_V3_SinkerRing_V1_2_1_FULL.stl"),   t_mm=(0,0,75+WZ), mat=M['L1_sinker'])
imp("Retainer",  os.path.join(L,"02_CASSETTE_HEAD","retainer_ring","CSM_V3_RetainerRing_V1_0_FULL.stl"), t_mm=(0,0,83+WZ), mat=M['L1_retainer'])

# Drive train (Layer 2 -- frame, and Layer 3 -- automation)
imp("DriveHub",  os.path.join(L,"06_DRIVE_SYSTEM","CSM_V3_DriveHub_V2_4_2.stl"),                       t_mm=(0,0,-10+WZ), mat=M['L2_hub'])
imp("Bearings",  os.path.join(L,"05_BEARINGS_SHAFT","CSM_V3_BearingHousings_PAIR_V2_5_1.stl"),         t_mm=(0,0,-70+WZ), mat=M['L2_bearings'])
imp("MotorMount", os.path.join(A,"drive_bought","motor_mount_v1_4","CSM_V3_MotorMount_V1_4.stl"),       mat=M['L2_mount'])

# NEMA 23 + Gearbox primitives (placeholder until STL built)
gbZ_bot = 70.0; gbZ_top = gbZ_bot + MD.GEARBOX_LENGTH
mZ_bot = gbZ_top;  mZ_top = mZ_bot + MD.NEMA23_BODY_L
cyl("Gearbox", MD.GEARBOX_FLANGE_OD/2, MD.GEARBOX_LENGTH,
    x=MD.MOTOR_X, y=MD.MOTOR_Y, z=(gbZ_bot+gbZ_top)/2, mat=M['L3_gearbox'])
box("NEMA23", MD.NEMA23_BODY_W, MD.NEMA23_BODY_W, MD.NEMA23_BODY_L,
    x=MD.MOTOR_X, y=MD.MOTOR_Y, z=(mZ_bot+mZ_top)/2, mat=M['L3_motor'])

# Pulleys + belt
pulley_z = 62.0
cyl("Pulley_60T", MD.PULLEY_BIG_OD/2, MD.PULLEY_BIG_W,
    x=MD.MOTOR_X, y=MD.MOTOR_Y, z=pulley_z, mat=M['L3_pulley'])
cyl("Pulley_20T", MD.PULLEY_SMALL_OD/2, MD.PULLEY_SMALL_W,
    x=0, y=0, z=pulley_z, mat=M['L3_pulley'])

# Feeders V1.1
FRO = MD.PCD_FEEDER/2 + 25.0
imp("Feeder_F1", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"),
    t_mm=(FRO,0,0), rz_deg=-90, mat=M['L3_feeder'])
imp("Feeder_F4", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"),
    t_mm=(-FRO,0,0), rz_deg=+90, mat=M['L3_feeder'])
imp("YarnCone_F1", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"),
    t_mm=(FRO,20,250), mat=M['L3_yarn_r'])
imp("YarnCone_F4", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"),
    t_mm=(-FRO,-20,250), mat=M['L3_yarn_b'])

# Electronics
imp("Mega",   os.path.join(A,"electronics","arduino_mega_2560","CSM_V3_ArduinoMega_V1_0.stl"),
    t_mm=(-130, 130, 20), mat=M['L3_pcb'])
imp("TB6600", os.path.join(A,"electronics","tb6600_driver","CSM_V3_TB6600_V1_0.stl"),
    t_mm=(150, 60, 20), rz_deg=90, mat=M['L2_mount'])
imp("LRS50",  os.path.join(A,"electronics","lrs50_psu","CSM_V3_LRS50_V1_0.stl"),
    t_mm=(-150, -60, 20), rz_deg=90, mat=M['L2_mount'])
imp("TouchArm", os.path.join(A,"electronics","touchscreen_arm","CSM_V3_TouchscreenArm_V1_0.stl"),
    t_mm=(0, MD.MAST_CENTER_Y+20, MD.MAST_TOP_Z-80), mat=M['L2_mount'])
imp("Screen", os.path.join(A,"electronics","touchscreen_7in","CSM_V3_Touchscreen7in_Screen_V1_0.stl"),
    t_mm=(0, MD.MAST_CENTER_Y+40, MD.MAST_TOP_Z-50), mat=M['L3_screen'])

# Ground
bpy.ops.mesh.primitive_plane_add(size=3.0, location=(0,0,-0.005))
ground = bpy.context.active_object; ground.name = "Ground"
assign(ground, M['ground'])

# ============================================================
# LIGHTING
# ============================================================
def light(name, ltype, loc, energy, rot=(0,0,0), size=0.8):
    bpy.ops.object.light_add(type=ltype, location=loc)
    L = bpy.context.active_object; L.name = name
    L.data.energy = energy
    if hasattr(L.data,'size'): L.data.size = size
    L.rotation_euler = rot
    return L

light("Sun", 'SUN', loc=(-0.5,-0.7,2.5), energy=1.2,
      rot=(math.radians(50), math.radians(-15), math.radians(35)))
light("Key", 'AREA', loc=(0.6,-0.7,0.6), energy=80,
      rot=(math.radians(-50),0,math.radians(135)), size=0.6)
light("Fill", 'AREA', loc=(-0.7,0.3,0.4), energy=30,
      rot=(math.radians(70),0,math.radians(-110)), size=1.0)

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.16, 0.18, 0.22, 1.0)
    bg.inputs[1].default_value = 0.30

# ============================================================
# RENDER SETTINGS
# ============================================================
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
scene.render.resolution_x = 1920
scene.render.resolution_y = 1200
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -0.5

OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"

def set_camera(name, pos, look_at, ortho=False, ortho_scale=1.0, lens=50):
    bpy.ops.object.camera_add(location=pos)
    cam = bpy.context.active_object; cam.name = name
    if ortho:
        cam.data.type = 'ORTHO'
        cam.data.ortho_scale = ortho_scale
    else:
        cam.data.lens = lens
    dirv = Vector(look_at) - Vector(pos)
    cam.rotation_euler = dirv.to_track_quat('-Z','Y').to_euler()
    scene.camera = cam
    return cam

def render_to(name):
    out = os.path.join(OUT_DIR, f"CSM_V3_Diagram_{name}.png")
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out) if os.path.exists(out) else 0
    print(f"  [{name}] {out} ({sz/1024:.0f} KB)")
    return out

# ============================================================
# D1 -- Full machine isometric
# ============================================================
print("\n[D1] Full machine isometric")
set_camera("CamD1", pos=(0.65,-0.80,0.35), look_at=(0,0,0.20), lens=42)
render_to("D1_isometric")

# ============================================================
# D2 -- Side elevation (section view)
# Camera from +X looking -X, ortho so vertical stack is clear
# ============================================================
print("\n[D2] Side elevation")
set_camera("CamD2", pos=(1.5, 0.0, 0.22), look_at=(0,0,0.22),
           ortho=True, ortho_scale=0.55)
render_to("D2_side_section")

# ============================================================
# D3 -- Triad detail (close-up of cassette top + feeder F1)
# ============================================================
print("\n[D3] Triad detail")
set_camera("CamD3", pos=(0.30,-0.22,0.32), look_at=(0.05,0,0.27), lens=70)
render_to("D3_triad")

# ============================================================
# D4 -- Top architecture plan (with PCD overlays)
# ============================================================
print("\n[D4] Top architecture plan")

# Add PCD ring overlays (thin tori at master datum height)
plan_z_overlay = MD.ALU_PLATE_TOP_Z + 1.0   # 231 -- just above master plate
torus("PCD_180", 180/2, 0.8, z=plan_z_overlay, mat=M['PCD_marker'])
torus("PCD_190", 190/2, 0.8, z=plan_z_overlay, mat=M['feeder_label'])
torus("PCD_155", 155/2, 0.8, z=plan_z_overlay, mat=M['PCD_marker'])

# θ=0° arrow (along +X axis at master datum)
bpy.ops.mesh.primitive_cylinder_add(radius=0.003, depth=0.08,
                                    location=(0.060, 0, plan_z_overlay*mm))
arr = bpy.context.active_object; arr.name = "Theta0_arrow"
arr.rotation_euler = (0, math.radians(90), 0)
assign(arr, M['theta0_arrow'])
bpy.ops.mesh.primitive_cone_add(radius1=0.006, radius2=0.0, depth=0.012,
                                location=(0.106, 0, plan_z_overlay*mm))
ah = bpy.context.active_object; ah.name = "Theta0_head"
ah.rotation_euler = (0, math.radians(90), 0)
assign(ah, M['theta0_arrow'])

set_camera("CamD4", pos=(0,0,1.5), look_at=(0,0,0.22),
           ortho=True, ortho_scale=0.55)
render_to("D4_top_plan")

# Remove overlays before D5
for n in ["PCD_180","PCD_190","PCD_155","Theta0_arrow","Theta0_head"]:
    o = bpy.data.objects.get(n)
    if o: bpy.data.objects.remove(o, do_unlink=True)

# ============================================================
# D5 -- Layer separation (exploded vertically)
# Move Layer 1 UP by +0.15m, Layer 3 DOWN by -0.10m
# ============================================================
print("\n[D5] Layer separation (exploded)")

L1_objects = ["Cylinder","CamRing","Cassette","Sinker","Retainer"]
L3_objects = ["NEMA23","Gearbox","Pulley_60T","Pulley_20T","Feeder_F1","Feeder_F4",
              "YarnCone_F1","YarnCone_F4","Mega","TB6600","LRS50","TouchArm","Screen"]

# Move Layer 1 up
for n in L1_objects:
    o = bpy.data.objects.get(n)
    if o: o.location.z += 0.15

# Move Layer 3 down
for n in L3_objects:
    o = bpy.data.objects.get(n)
    if o: o.location.z -= 0.10

set_camera("CamD5", pos=(0.75, -0.60, 0.40), look_at=(0,0,0.25), lens=42)
render_to("D5_layer_separation")

# Save final .blend (still in exploded state -- caller can ctrl-Z)
blend_path = os.path.join(OUT_DIR, "CSM_V3_DiagramSet.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")
print("\nDONE -- 5 diagram-set views.")
