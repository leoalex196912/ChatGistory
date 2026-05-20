"""
CSM V3 hero render -- REFRAME PASS
Opens the saved .blend, repositions camera + key lights for a wider shot
that captures the entire machine, then re-renders.
"""
import bpy, math, os
from mathutils import Vector

BLEND = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly.blend"
PNG   = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly_Hero.png"

bpy.ops.wm.open_mainfile(filepath=BLEND)

# Compute scene bounding box of MESH objects (exclude ground)
mins = Vector(( 1e9,  1e9,  1e9))
maxs = Vector((-1e9, -1e9, -1e9))
for o in bpy.data.objects:
    if o.type != 'MESH' or o.name == 'Ground':
        continue
    # Apply world-space transform to vertices via bbox in world coords
    for corner in o.bound_box:
        wpt = o.matrix_world @ Vector(corner)
        mins = Vector((min(mins.x, wpt.x), min(mins.y, wpt.y), min(mins.z, wpt.z)))
        maxs = Vector((max(maxs.x, wpt.x), max(maxs.y, wpt.y), max(maxs.z, wpt.z)))

ctr = (mins + maxs) / 2
ext = maxs - mins
print(f"Scene bbox: min={mins}  max={maxs}")
print(f"Center: {ctr}, extent: {ext}")

# Hard-coded camera for a clear 3/4 view that shows everything.
# Higher Z so shelf doesn't occlude bottom electronics + base.
cam = bpy.data.objects.get("HeroCamera")
if cam is None:
    bpy.ops.object.camera_add(); cam = bpy.context.active_object; cam.name="HeroCamera"
cam.location = (900, -1200, 250)
cam.data.lens = 28      # wide enough to fit the whole machine
target = Vector((-30, 0, -60))   # aim at center of mass slightly left
direction = target - Vector(cam.location)
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

print(f"Camera at: {cam.location}")
print(f"Lens: {cam.data.lens}mm, looking at {ctr}")

# Boost key light slightly
for n in ['Key', 'Fill', 'Rim']:
    o = bpy.data.objects.get(n)
    if o:
        o.data.energy *= 1.2

# Render
scene = bpy.context.scene
scene.render.filepath = PNG
scene.cycles.samples = 96
bpy.ops.render.render(write_still=True)
print(f"[OK] RENDER: {PNG}  ({os.path.getsize(PNG)} bytes)")

# Save the reframed .blend
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"[OK] saved .blend: {BLEND}")
