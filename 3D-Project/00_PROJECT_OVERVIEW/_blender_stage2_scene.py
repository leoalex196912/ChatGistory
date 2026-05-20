"""
CSM V3 hero render -- Stage 2: build frame + drive train primitives,
assign materials, add lighting and camera. All units in METERS
(Blender internal), so values are mm * 0.001.
"""
import bpy, math
from mathutils import Vector

mm = 0.001  # mm -> m

# -------------- helpers --------------
def add_box(name, sx, sy, sz, x=0, y=0, z=0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
    o = bpy.context.active_object
    o.scale = (sx/2, sy/2, sz/2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.name = name
    return o

def add_cyl(name, r, h, x=0, y=0, z=0, axis='Z'):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, location=(x, y, z))
    o = bpy.context.active_object
    if axis == 'Y':
        o.rotation_euler = (math.radians(90), 0, 0)
    elif axis == 'X':
        o.rotation_euler = (0, math.radians(90), 0)
    o.name = name
    return o

def make_mat(name, base=(0.7,0.7,0.72,1), rough=0.5, metal=0.0, alpha=1.0, emission=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None:
        # in newer Blender it's named differently sometimes
        for n in nt.nodes:
            if n.type == 'BSDF_PRINCIPLED':
                bsdf = n; break
    bsdf.inputs["Base Color"].default_value = base
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = alpha
        if alpha < 1.0:
            m.blend_method = 'BLEND'
    if emission is not None and "Emission" in bsdf.inputs:
        bsdf.inputs["Emission"].default_value = emission
    return m

def assign(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# -------------- materials --------------
mat_petg     = make_mat("PETG_LightGray", base=(0.78,0.79,0.82,1), rough=0.32, metal=0.0)
mat_petg_warm= make_mat("PETG_Warm",      base=(0.85,0.78,0.70,1), rough=0.40, metal=0.0)
mat_aluminum = make_mat("Aluminum6061",   base=(0.85,0.86,0.88,1), rough=0.35, metal=1.0)
mat_alumblk  = make_mat("Anodized2020",   base=(0.10,0.10,0.11,1), rough=0.50, metal=0.85)
mat_wood     = make_mat("Hardwood_Walnut",base=(0.32,0.18,0.10,1), rough=0.55, metal=0.0)
mat_motor    = make_mat("MotorBlack",     base=(0.05,0.05,0.06,1), rough=0.45, metal=0.10)
mat_pulley   = make_mat("PulleyBlack",    base=(0.08,0.08,0.09,1), rough=0.55, metal=0.0)
mat_belt     = make_mat("Belt",           base=(0.04,0.04,0.04,1), rough=0.70, metal=0.0)
mat_shaft    = make_mat("Steel",          base=(0.78,0.80,0.83,1), rough=0.25, metal=1.0)
mat_yarn_r   = make_mat("Yarn_Red",       base=(0.78,0.12,0.10,1), rough=0.85)
mat_yarn_b   = make_mat("Yarn_Blue",      base=(0.10,0.30,0.72,1), rough=0.85)
mat_yarn_y   = make_mat("Yarn_Yellow",    base=(0.92,0.78,0.18,1), rough=0.85)
mat_brass    = make_mat("Brass",          base=(0.85,0.65,0.30,1), rough=0.30, metal=1.0)

# -------------- apply materials to STLs --------------
petg_objs = ["Cylinder_V3_0","CamRing_V6_5","CassetteBase_V1_1","SinkerRing_V1_2_1",
             "RetainerRing_V1_0","DriveHub_V2_4_2","MotorMount_V1_3","BearingHousings_V2_5"]
for n in petg_objs:
    o = bpy.data.objects.get(n)
    if o:
        assign(o, mat_petg)

# Tint sub-components for visual differentiation
if bpy.data.objects.get("CamRing_V6_5"):
    assign(bpy.data.objects["CamRing_V6_5"], make_mat("PETG_CamRing", base=(0.55,0.58,0.62,1), rough=0.35))
if bpy.data.objects.get("RetainerRing_V1_0"):
    assign(bpy.data.objects["RetainerRing_V1_0"], make_mat("PA12_Retainer", base=(0.88,0.86,0.80,1), rough=0.55))
if bpy.data.objects.get("SinkerRing_V1_2_1"):
    assign(bpy.data.objects["SinkerRing_V1_2_1"], make_mat("PETG_Sinker", base=(0.72,0.74,0.76,1), rough=0.40))

# -------------- frame --------------
# Wood mid-shelf 500x400x18, top at Z=49mm = 0.049m
SHELF_W, SHELF_D, SHELF_T = 0.500, 0.400, 0.018
mid_top_z = 0.049
mid_shelf = add_box("WoodMidShelf", SHELF_W, SHELF_D, SHELF_T,
                    z=mid_top_z - SHELF_T/2)
assign(mid_shelf, mat_wood)

# Wood base 500x400x18, top at Z = -0.300m
base_top_z = -0.300
wood_base = add_box("WoodBase", SHELF_W, SHELF_D, SHELF_T,
                    z=base_top_z - SHELF_T/2)
assign(wood_base, mat_wood)

# Aluminum plate 150x150x6, top at Z=49mm = under cassette
PLATE_W, PLATE_T = 0.150, 0.006
al_plate = add_box("AluminumPlate", PLATE_W, PLATE_W, PLATE_T,
                   z=mid_top_z + 0.001 - PLATE_T/2)  # sits visually just below cassette
assign(al_plate, mat_aluminum)

# 2020 uprights at corners
EXT = 0.020
upright_h = mid_top_z - SHELF_T - base_top_z
for sx, sy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
    x = sx * (SHELF_W/2 - EXT/2 - 0.005)
    y = sy * (SHELF_D/2 - EXT/2 - 0.005)
    z = base_top_z + upright_h/2
    up = add_box(f"Upright_{sx}_{sy}", EXT, EXT, upright_h, x=x, y=y, z=z)
    assign(up, mat_alumblk)

# -------------- drive train --------------
# 12mm steel shaft, runs vertical through bearings, motor below, drive hub above
SHAFT_D = 0.012
shaft_z_top = -0.010 - 0.005   # just below drive hub
shaft_z_bot = -0.230           # down to near base
shaft_h = shaft_z_top - shaft_z_bot
shaft = add_cyl("DriveShaft", SHAFT_D/2, shaft_h, z=(shaft_z_top+shaft_z_bot)/2)
assign(shaft, mat_shaft)

# NEMA 17 stepper: 42x42x40 block + shaft stub, mounted on side
MOTOR_W = 0.042; MOTOR_L = 0.040
motor_x = 0.075   # offset to side so belt has reach
motor_z = -0.160
motor = add_box("NEMA17_Motor", MOTOR_W, MOTOR_W, MOTOR_L, x=motor_x, y=0, z=motor_z)
assign(motor, mat_motor)

# Motor pulley (16T HTD 5M) -- small pulley on motor shaft
m_pulley_z = motor_z + MOTOR_L/2 + 0.012
m_pulley = add_cyl("MotorPulley_16T", 0.014, 0.012, x=motor_x, z=m_pulley_z)
assign(m_pulley, mat_pulley)

# Cylinder-side pulley (60T HTD 5M) on the drive shaft above bearings
c_pulley_z = -0.060
c_pulley = add_cyl("CylinderPulley_60T", 0.050, 0.014, z=c_pulley_z)
assign(c_pulley, mat_pulley)

# Belt -- approximate as a torus-like loop. Use a thin extruded path.
# Simpler: two cylinders representing belt wrap, plus two side connectors.
# We'll just use a thin elongated box for visual.
# Distance between pulley centers:
dx = motor_x
dy = 0
belt_y_offset = 0
belt_thickness = 0.003
belt_width = 0.009
# Top strand of belt
belt_top = add_box("Belt_Top", math.sqrt(dx*dx+dy*dy)+0.020, belt_width, belt_thickness,
                   x=motor_x/2, y=0.045, z=c_pulley_z)
assign(belt_top, mat_belt)
belt_bot = add_box("Belt_Bot", math.sqrt(dx*dx+dy*dy)+0.020, belt_width, belt_thickness,
                   x=motor_x/2, y=-0.045, z=c_pulley_z)
assign(belt_bot, mat_belt)

# -------------- decorative yarn cones --------------
# Two cones above the cassette base, suggesting feeding ports.
def add_cone(name, r1, r2, h, x, y, z, mat):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=h, location=(x,y,z))
    o = bpy.context.active_object; o.name = name
    assign(o, mat); return o

cone_z = 0.130
add_cone("Yarn_Cone_Red",    0.030, 0.020, 0.085,  0.085, 0.0, cone_z, mat_yarn_r)
add_cone("Yarn_Cone_Blue",   0.030, 0.020, 0.085, -0.085, 0.0, cone_z, mat_yarn_b)

# -------------- lighting --------------
# Sun (rim)
bpy.ops.object.light_add(type='SUN', location=(-1.5, -1.0, 2.5))
sun = bpy.context.active_object
sun.data.energy = 2.5
sun.data.angle = math.radians(8)
sun.rotation_euler = (math.radians(50), math.radians(-15), math.radians(35))
sun.name = "KeyLight_Sun"

# Area key (front)
bpy.ops.object.light_add(type='AREA', location=(0.6, -0.8, 0.6))
key = bpy.context.active_object
key.data.energy = 200
key.data.size = 0.8
key.rotation_euler = (math.radians(60), 0, math.radians(35))
key.name = "AreaKey"

# Fill from right
bpy.ops.object.light_add(type='AREA', location=(-0.9, 0.3, 0.3))
fill = bpy.context.active_object
fill.data.energy = 80
fill.data.size = 1.0
fill.rotation_euler = (math.radians(75), 0, math.radians(-110))
fill.name = "AreaFill"

# World background
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.88, 0.90, 0.94, 1.0)
    bg.inputs[1].default_value = 0.35

# -------------- camera --------------
bpy.ops.object.camera_add(location=(0.55, -0.55, 0.18))
cam = bpy.context.active_object
cam.name = "HeroCamera"
cam.data.lens = 55
# Aim at the cassette head (Z~0.06m)
target = Vector((0.0, 0.0, 0.05))
dirvec = target - cam.location
rot_quat = dirvec.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam

# -------------- render settings --------------
scene = bpy.context.scene
# Use Eevee (Blender 3.x) or Eevee Next (Blender 4.2+)
target_engine = None
for cand in ['BLENDER_EEVEE_NEXT','BLENDER_EEVEE']:
    try:
        scene.render.engine = cand
        target_engine = cand; break
    except Exception:
        continue

scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
# Eevee quality
try:
    scene.eevee.taa_render_samples = 64
    scene.eevee.use_bloom = True
    scene.eevee.use_ssr = True
    scene.eevee.use_gtao = True
except Exception:
    pass
# View transform for crisp marketing look
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'

print("Stage 2 done.")
print("Objects:", len(bpy.data.objects))
print("Engine: ", scene.render.engine)
for o in bpy.data.objects:
    print(f"  {o.type:8s} {o.name}")
