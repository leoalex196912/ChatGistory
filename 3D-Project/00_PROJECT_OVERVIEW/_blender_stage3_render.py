"""
CSM V3 hero render -- Stage 3: render to PNG.
"""
import bpy, os

OUT_DIR = r"C:\3D-Project\00_PROJECT_OVERVIEW\renders"
os.makedirs(OUT_DIR, exist_ok=True)

OUT_PATH = os.path.join(OUT_DIR, "CSM_V3_Assembly_Hero.png")

scene = bpy.context.scene
scene.render.filepath = OUT_PATH
scene.render.image_settings.file_format = 'PNG'

bpy.ops.render.render(write_still=True)

import os
sz = os.path.getsize(OUT_PATH) if os.path.exists(OUT_PATH) else 0
print(f"RENDER DONE: {OUT_PATH}  ({sz} bytes / {sz/1024:.1f} KB)")
