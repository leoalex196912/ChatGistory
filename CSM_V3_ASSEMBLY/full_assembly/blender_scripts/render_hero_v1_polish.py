"""
Final polish: drop light energies, slight exposure adjustment, re-render.
"""
import bpy, math, os
from mathutils import Vector

BLEND = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly.blend"
PNG   = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_FullAssembly_Hero.png"

bpy.ops.wm.open_mainfile(filepath=BLEND)

# Dial down lights for a moodier marketing look
for n, e in [('Key', 60), ('Fill', 20), ('Rim', 40), ('AmbientSun', 0.5)]:
    o = bpy.data.objects.get(n)
    if o and o.type == 'LIGHT':
        o.data.energy = e

# Slight negative exposure
scene = bpy.context.scene
scene.view_settings.exposure = -0.6
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'High Contrast'

# Darker background for punchier subject
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.10, 0.12, 0.16, 1.0)
    bg.inputs[1].default_value = 0.50

# Higher quality
scene.cycles.samples = 128
scene.render.filepath = PNG
bpy.ops.render.render(write_still=True)
print(f"[OK] RENDER: {PNG}  ({os.path.getsize(PNG)} bytes)")
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
