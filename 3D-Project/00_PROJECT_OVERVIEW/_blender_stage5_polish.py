"""
Stage 5 polish: tighter framing, stronger contrast, hero light on cassette head.
"""
import bpy, math, os
from mathutils import Vector

cam = bpy.data.objects["HeroCamera"]
cam.location = (0.55, -0.72, 0.10)
cam.data.lens = 42
target = Vector((0.0, 0.0, -0.04))
cam.rotation_euler = (target - cam.location).to_track_quat('-Z','Y').to_euler()

# Stronger contrast: brighten key, dim fill more, add hero spot on cassette head
def relight(name, e):
    o = bpy.data.objects.get(name)
    if o and o.type=='LIGHT': o.data.energy = e
relight("AreaKey", 140)
relight("AreaFill", 25)
relight("KeyLight_Sun", 1.2)

# Hero spot lighting the cassette head
hero = bpy.data.objects.get("HeroSpot")
if hero is None:
    bpy.ops.object.light_add(type='SPOT', location=(0.25, -0.35, 0.30))
    hero = bpy.context.active_object; hero.name = "HeroSpot"
hero.data.energy = 400
hero.data.spot_size = math.radians(45)
hero.data.spot_blend = 0.6
hero.data.color = (1.0, 0.96, 0.90)
t = Vector((0,0,0.07)) - hero.location
hero.rotation_euler = t.to_track_quat('-Z','Y').to_euler()

# Sharpen material contrast on the assembly
def tweak(name, base=None, rough=None, metal=None):
    m = bpy.data.materials.get(name)
    if not m or not m.use_nodes: return
    for n in m.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':
            if base is not None: n.inputs["Base Color"].default_value=base
            if rough is not None: n.inputs["Roughness"].default_value=rough
            if metal is not None: n.inputs["Metallic"].default_value=metal

tweak("PETG_LightGray",  base=(0.52,0.55,0.60,1), rough=0.30)     # cylinder/cassette
tweak("PETG_CamRing",    base=(0.30,0.34,0.40,1), rough=0.25)     # cam ring darker steel
tweak("PA12_Retainer",   base=(0.90,0.85,0.72,1), rough=0.45)     # retainer warm beige
tweak("PETG_Sinker",     base=(0.42,0.45,0.50,1), rough=0.35)     # sinker mid gray
tweak("Hardwood_Walnut", base=(0.16,0.08,0.04,1), rough=0.50)     # darker walnut
tweak("Aluminum6061",    base=(0.82,0.84,0.87,1), rough=0.28, metal=1.0)
tweak("MotorBlack",      base=(0.025,0.025,0.030,1), rough=0.45)
tweak("Anodized2020",    base=(0.12,0.12,0.13,1), rough=0.45, metal=0.7)
tweak("Yarn_Red",        base=(0.78,0.08,0.08,1), rough=0.80)
tweak("Yarn_Blue",       base=(0.06,0.18,0.65,1), rough=0.80)

# Drive hub: make it stand out as machined aluminum (it WILL be aluminum in production)
mat_dh = bpy.data.materials.get("PETG_LightGray")  # was reusing this
# Create a distinct material and assign to drive hub
mat_drivehub = bpy.data.materials.new("DriveHub_AluminumPrototype")
mat_drivehub.use_nodes = True
for n in mat_drivehub.node_tree.nodes:
    if n.type=='BSDF_PRINCIPLED':
        n.inputs["Base Color"].default_value=(0.62,0.65,0.70,1)
        n.inputs["Roughness"].default_value=0.32
        n.inputs["Metallic"].default_value=0.0
dh = bpy.data.objects.get("DriveHub_V2_4_2")
if dh:
    if dh.data.materials: dh.data.materials[0]=mat_drivehub
    else: dh.data.materials.append(mat_drivehub)

# Exposure & contrast
scene = bpy.context.scene
scene.view_settings.exposure = -0.2
scene.view_settings.look = 'High Contrast'

# Bigger world contribution
world = scene.world
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.18, 0.22, 0.28, 1.0)
    bg.inputs[1].default_value = 0.40

# Output
OUT = r"C:\3D-Project\00_PROJECT_OVERVIEW\renders\CSM_V3_Assembly_Hero.png"
scene.render.filepath = OUT
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
try:
    scene.eevee.taa_render_samples = 128
except Exception: pass
bpy.ops.render.render(write_still=True)
print("POLISH RENDER:", OUT, os.path.getsize(OUT), "bytes")
