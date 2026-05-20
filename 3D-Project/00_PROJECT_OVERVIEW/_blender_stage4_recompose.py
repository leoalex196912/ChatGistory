"""
Stage 4: pull camera back to show full assembly, fix overexposure,
re-render. Also tweak materials to read more like Erlbacher reference.
"""
import bpy, math, os
from mathutils import Vector

# ----- camera -----
cam = bpy.data.objects.get("HeroCamera")
if cam is None:
    bpy.ops.object.camera_add(); cam = bpy.context.active_object; cam.name = "HeroCamera"
# Pull WAY back, raise, frame the whole machine
cam.location = (0.75, -0.95, 0.20)
cam.data.lens = 38   # wider lens
target = Vector((0.0, 0.0, -0.05))   # aim at upper half of frame stack
dirvec = target - cam.location
cam.rotation_euler = dirvec.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# ----- lights: dial down -----
for n, energy in [("AreaKey", 80), ("AreaFill", 35), ("KeyLight_Sun", 1.5)]:
    o = bpy.data.objects.get(n)
    if o and o.type == 'LIGHT':
        o.data.energy = energy

# Bump world background a touch darker so the scene reads punchier
world = bpy.context.scene.world
if world and world.use_nodes:
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.35, 0.38, 0.44, 1.0)
        bg.inputs[1].default_value = 0.50

# ----- materials: deepen wood, darken aluminum slightly -----
def tweak(name, base=None, rough=None, metal=None):
    m = bpy.data.materials.get(name)
    if not m or not m.use_nodes: return
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            if base is not None: n.inputs["Base Color"].default_value = base
            if rough is not None: n.inputs["Roughness"].default_value = rough
            if metal is not None: n.inputs["Metallic"].default_value = metal
            return

tweak("Hardwood_Walnut", base=(0.20,0.10,0.05,1), rough=0.55)
tweak("Aluminum6061",    base=(0.78,0.79,0.82,1), rough=0.30, metal=1.0)
tweak("PETG_LightGray",  base=(0.62,0.64,0.68,1), rough=0.32)
tweak("PETG_CamRing",    base=(0.42,0.45,0.50,1), rough=0.30)
tweak("PA12_Retainer",   base=(0.88,0.84,0.74,1), rough=0.55)
tweak("PETG_Sinker",     base=(0.55,0.58,0.62,1), rough=0.40)

# Stronger yarn colors
tweak("Yarn_Red",    base=(0.85,0.10,0.10,1))
tweak("Yarn_Blue",   base=(0.08,0.22,0.78,1))

# ----- a tablet on a side arm (for marketing flair) -----
def add_box(name, sx, sy, sz, x=0, y=0, z=0, mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x,y,z))
    o = bpy.context.active_object; o.name = name
    o.scale = (sx/2, sy/2, sz/2)
    bpy.ops.object.transform_apply(scale=True)
    if mat:
        if o.data.materials: o.data.materials[0] = mat
        else: o.data.materials.append(mat)
    return o

tablet = bpy.data.objects.get("Tablet_Screen")
if tablet is None:
    mat_screen = bpy.data.materials.new("ScreenGlow")
    mat_screen.use_nodes = True
    for n in mat_screen.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = (0.10,0.18,0.30,1)
            try: n.inputs["Emission"].default_value = (0.18,0.40,0.85,1)
            except Exception: pass
            try: n.inputs["Emission Strength"].default_value = 1.8
            except Exception: pass
    add_box("Tablet_Screen", 0.180, 0.005, 0.110, x=-0.18, y=0.16, z=0.10, mat=mat_screen)

# ----- render -----
scene = bpy.context.scene
scene.view_settings.exposure = -0.4
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
OUT = r"C:\3D-Project\00_PROJECT_OVERVIEW\renders\CSM_V3_Assembly_Hero.png"
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDER DONE:", OUT, os.path.getsize(OUT), "bytes")
