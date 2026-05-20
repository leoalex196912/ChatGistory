"""
Stage 6: actually-readable render.
- Distinct material colors per component (not all white)
- Switch to CYCLES for proper shading
- Frame the scene in the user's 3D viewport so they can orbit
- Tighter camera, ground plane for shadow contact
"""
import bpy, math, os
from mathutils import Vector

# ---------------- MATERIAL OVERHAUL ----------------
def get_or_make(name):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m

def set_pbr(m, base=(0.5,0.5,0.5,1), rough=0.4, metal=0.0, ior=1.45):
    for n in m.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = base
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            if "IOR" in n.inputs:
                n.inputs["IOR"].default_value = ior
            return n
    return None

# DISTINCT colors -- each part its own identity
M = {}
M['cylinder']    = get_or_make("M_Cylinder");      set_pbr(M['cylinder'],    (0.78,0.79,0.82,1), 0.30, 0.0)  # off-white PETG
M['camring']     = get_or_make("M_CamRing");       set_pbr(M['camring'],     (0.18,0.20,0.24,1), 0.25, 0.6)  # near-black anodized
M['cassette']    = get_or_make("M_Cassette");      set_pbr(M['cassette'],    (0.92,0.55,0.18,1), 0.40, 0.0)  # ORANGE PETG (visible)
M['sinker']      = get_or_make("M_Sinker");        set_pbr(M['sinker'],      (0.10,0.45,0.78,1), 0.35, 0.0)  # BLUE PETG
M['retainer']    = get_or_make("M_Retainer");      set_pbr(M['retainer'],    (0.95,0.92,0.78,1), 0.55, 0.0)  # cream PA12
M['drivehub']    = get_or_make("M_DriveHub");      set_pbr(M['drivehub'],    (0.72,0.74,0.78,1), 0.20, 1.0)  # aluminum
M['motormount']  = get_or_make("M_MotorMount");    set_pbr(M['motormount'],  (0.20,0.65,0.30,1), 0.45, 0.0)  # GREEN PETG
M['bearings']    = get_or_make("M_Bearings");      set_pbr(M['bearings'],    (0.80,0.20,0.20,1), 0.40, 0.0)  # RED PETG
M['wood']        = get_or_make("M_Wood");          set_pbr(M['wood'],        (0.42,0.22,0.10,1), 0.55, 0.0)  # walnut
M['aluplate']    = get_or_make("M_AlPlate");       set_pbr(M['aluplate'],    (0.82,0.84,0.87,1), 0.28, 1.0)  # aluminum
M['ext2020']     = get_or_make("M_2020");          set_pbr(M['ext2020'],     (0.18,0.18,0.20,1), 0.40, 0.8)  # anodized black
M['motor']       = get_or_make("M_Motor");         set_pbr(M['motor'],       (0.04,0.04,0.05,1), 0.45, 0.10) # black
M['pulley']      = get_or_make("M_Pulley");        set_pbr(M['pulley'],      (0.06,0.06,0.08,1), 0.55, 0.0)
M['belt']        = get_or_make("M_Belt");          set_pbr(M['belt'],        (0.025,0.025,0.025,1), 0.75, 0.0)
M['shaft']       = get_or_make("M_Shaft");         set_pbr(M['shaft'],       (0.78,0.80,0.84,1), 0.20, 1.0)
M['yarn_r']      = get_or_make("M_YarnR");         set_pbr(M['yarn_r'],      (0.90,0.10,0.10,1), 0.85)
M['yarn_b']      = get_or_make("M_YarnB");         set_pbr(M['yarn_b'],      (0.10,0.30,0.85,1), 0.85)
M['ground']      = get_or_make("M_Ground");        set_pbr(M['ground'],      (0.78,0.78,0.80,1), 0.65)

# assign single material (overwrite any existing)
def reassign(obj_name, mat):
    o = bpy.data.objects.get(obj_name)
    if not o: return
    o.data.materials.clear()
    o.data.materials.append(mat)

reassign("Cylinder_V3_0",         M['cylinder'])
reassign("CamRing_V6_5",          M['camring'])
reassign("CassetteBase_V1_1",     M['cassette'])
reassign("SinkerRing_V1_2_1",     M['sinker'])
reassign("RetainerRing_V1_0",     M['retainer'])
reassign("DriveHub_V2_4_2",       M['drivehub'])
reassign("MotorMount_V1_3",       M['motormount'])
reassign("BearingHousings_V2_5",  M['bearings'])
reassign("WoodMidShelf",          M['wood'])
reassign("WoodBase",              M['wood'])
reassign("AluminumPlate",         M['aluplate'])
for s in ['1_1','1_-1','-1_1','-1_-1']:
    reassign(f"Upright_{s}",      M['ext2020'])
reassign("NEMA17_Motor",          M['motor'])
reassign("MotorPulley_16T",       M['pulley'])
reassign("CylinderPulley_60T",    M['pulley'])
reassign("Belt_Top",              M['belt'])
reassign("Belt_Bot",              M['belt'])
reassign("DriveShaft",            M['shaft'])
reassign("Yarn_Cone_Red",         M['yarn_r'])
reassign("Yarn_Cone_Blue",        M['yarn_b'])

# Ground plane far below for shadow catch
ground = bpy.data.objects.get("Ground")
if ground is None:
    bpy.ops.mesh.primitive_plane_add(size=2.5, location=(0,0,-0.320))
    ground = bpy.context.active_object; ground.name = "Ground"
reassign("Ground", M['ground'])

# ---------------- LIGHTING (Cycles-friendly) ----------------
for n in ['AreaKey','AreaFill','KeyLight_Sun','HeroSpot']:
    o = bpy.data.objects.get(n)
    if o: bpy.data.objects.remove(o, do_unlink=True)

# Key
bpy.ops.object.light_add(type='AREA', location=(0.55,-0.75,0.45))
key = bpy.context.active_object; key.name="Key"
key.data.energy = 350; key.data.size = 0.6
key.rotation_euler = (math.radians(55), 0, math.radians(35))

# Fill
bpy.ops.object.light_add(type='AREA', location=(-0.75,-0.20,0.30))
fill = bpy.context.active_object; fill.name="Fill"
fill.data.energy = 90; fill.data.size = 1.0
fill.rotation_euler = (math.radians(70), 0, math.radians(-90))

# Rim
bpy.ops.object.light_add(type='AREA', location=(0.0,0.85,0.55))
rim = bpy.context.active_object; rim.name="Rim"
rim.data.energy = 200; rim.data.size = 0.8
rim.rotation_euler = (math.radians(110), 0, math.radians(180))

# World
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs[0].default_value = (0.20, 0.24, 0.30, 1.0)
bg.inputs[1].default_value = 0.30

# ---------------- CAMERA ----------------
cam = bpy.data.objects.get("HeroCamera")
cam.location = (0.62, -0.78, 0.06)
cam.data.lens = 45
target = Vector((0.0, 0.0, -0.04))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z','Y').to_euler()
bpy.context.scene.camera = cam

# ---------------- RENDER ENGINE: CYCLES ----------------
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
try:
    scene.cycles.device = 'GPU'
except Exception: pass
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'
scene.view_settings.exposure = 0.2

# ---------------- FRAME VIEWPORT ----------------
# So the user's open Blender window orbits around the assembly
try:
    bpy.ops.object.select_all(action='SELECT')
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    with bpy.context.temp_override(area=area, region=region):
                        bpy.ops.view3d.view_selected()
                    break
            break
    bpy.ops.object.select_all(action='DESELECT')
except Exception as e:
    print("viewport frame skipped:", e)

# ---------------- RENDER ----------------
OUT = r"C:\3D-Project\00_PROJECT_OVERVIEW\renders\CSM_V3_Assembly_Hero.png"
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("CYCLES RENDER:", OUT, os.path.getsize(OUT), "bytes")
