"""
Stage 7: PUNCHY colors, less light, Standard view transform.
"""
import bpy, math, os

scene = bpy.context.scene

# Switch to STANDARD view transform so colors aren't desaturated
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = -1.0   # darker overall

# Drop light energy dramatically
energy_map = {"Key": 80, "Fill": 25, "Rim": 50}
for n, e in energy_map.items():
    o = bpy.data.objects.get(n)
    if o and o.type=='LIGHT': o.data.energy = e

# Darker world background
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.08, 0.10, 0.14, 1.0)
    bg.inputs[1].default_value = 0.20

# Make sure colors are vivid (re-apply)
def repaint(mname, base, rough=0.4, metal=0.0):
    m = bpy.data.materials.get(mname)
    if not m or not m.use_nodes: return
    for n in m.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = base
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            return

repaint("M_Cylinder",   (0.95,0.95,0.96,1), 0.35)            # bright white PETG
repaint("M_CamRing",    (0.05,0.05,0.07,1), 0.20, 0.7)       # deep black metal
repaint("M_Cassette",   (0.98,0.45,0.05,1), 0.40)            # vivid orange
repaint("M_Sinker",     (0.05,0.40,0.85,1), 0.35)            # vivid blue
repaint("M_Retainer",   (0.95,0.85,0.45,1), 0.50)            # warm yellow PA12
repaint("M_DriveHub",   (0.70,0.72,0.76,1), 0.18, 1.0)       # aluminum
repaint("M_MotorMount", (0.10,0.75,0.25,1), 0.45)            # vivid green
repaint("M_Bearings",   (0.88,0.10,0.10,1), 0.40)            # vivid red
repaint("M_Wood",       (0.32,0.16,0.06,1), 0.55)            # walnut
repaint("M_AlPlate",    (0.78,0.80,0.83,1), 0.25, 1.0)
repaint("M_2020",       (0.10,0.10,0.12,1), 0.40, 0.6)
repaint("M_Motor",      (0.02,0.02,0.03,1), 0.45, 0.05)
repaint("M_Pulley",     (0.04,0.04,0.05,1), 0.50)
repaint("M_Belt",       (0.015,0.015,0.015,1), 0.80)
repaint("M_Shaft",      (0.80,0.82,0.85,1), 0.18, 1.0)
repaint("M_YarnR",      (0.92,0.08,0.08,1), 0.85)
repaint("M_YarnB",      (0.08,0.20,0.92,1), 0.85)
repaint("M_Ground",     (0.50,0.50,0.52,1), 0.70)

# Cycles settings
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.use_denoising = True

# Frame the user's 3D viewport on the assembly too
try:
    bpy.ops.object.select_all(action='SELECT')
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    with bpy.context.temp_override(area=area, region=region):
                        bpy.ops.view3d.view_selected()
                    # set shading to material preview so user sees colors
                    for space in area.spaces:
                        if space.type=='VIEW_3D':
                            space.shading.type = 'MATERIAL'
                    break
            break
    bpy.ops.object.select_all(action='DESELECT')
except Exception as e:
    print("viewport frame skipped:", e)

OUT = r"C:\3D-Project\00_PROJECT_OVERVIEW\renders\CSM_V3_Assembly_Hero.png"
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("PUNCH RENDER:", OUT, os.path.getsize(OUT))
