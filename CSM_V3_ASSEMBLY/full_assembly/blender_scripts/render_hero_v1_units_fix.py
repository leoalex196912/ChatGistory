"""
Reopen the .blend, scale mm -> m, reposition camera+lights in meters,
re-render.
"""
import bpy, math, os
from mathutils import Vector

BLEND = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly.blend"
PNG   = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly_Hero.png"

bpy.ops.wm.open_mainfile(filepath=BLEND)

# Scale every mesh object by 0.001 AND scale its location by 0.001
for o in bpy.data.objects:
    if o.type == 'MESH':
        o.scale = (o.scale[0] * 0.001, o.scale[1] * 0.001, o.scale[2] * 0.001)
        o.location = (o.location[0] * 0.001, o.location[1] * 0.001, o.location[2] * 0.001)
    # Lights: scale location too (so 3-point setup still works)
    elif o.type == 'LIGHT':
        o.location = (o.location[0] * 0.001, o.location[1] * 0.001, o.location[2] * 0.001)
        if o.data.type == 'AREA':
            o.data.size = o.data.size * 0.001
        if o.data.type != 'SUN':
            o.data.energy = o.data.energy * 0.000001   # area light energy scales with surface area too

# Bump light energies back up to compensate
for n, e in [('Key', 800), ('Fill', 250), ('Rim', 500), ('AmbientSun', 1.5)]:
    o = bpy.data.objects.get(n)
    if o and o.type == 'LIGHT':
        o.data.energy = e

# Camera in METERS now
cam = bpy.data.objects.get("HeroCamera")
cam.location = (0.85, -1.10, 0.25)
cam.data.lens = 28
target = Vector((-0.03, 0.0, -0.07))
direction = target - Vector(cam.location)
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Ground plane already at -310mm = -0.31m if we scaled it; verify
gnd = bpy.data.objects.get("Ground")
if gnd:
    print(f"Ground at {gnd.location}, scale {gnd.scale}")

# Render
scene = bpy.context.scene
scene.render.filepath = PNG
scene.cycles.samples = 96
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
bpy.ops.render.render(write_still=True)
print(f"[OK] RENDER: {PNG}  ({os.path.getsize(PNG)} bytes)")

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"[OK] saved .blend: {BLEND}")
