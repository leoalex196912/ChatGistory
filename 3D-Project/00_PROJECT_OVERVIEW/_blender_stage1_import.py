"""
CSM V3 hero render -- Stage 1: clear scene, import STLs, position at datums.
All Z values per MACHINE_DATUMS.md R1 (cylinder local coords, Z=0 = cyl bottom).
"""
import bpy, os, math

# ---------- 1. RESET SCENE ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    bpy.data.collections.remove(c)
for m in list(bpy.data.materials):
    bpy.data.materials.remove(m)
for img in list(bpy.data.images):
    bpy.data.images.remove(img)

# ---------- 2. STL IMPORTS ----------
ROOT = r"C:\3D-Project\01_MECHANICAL"

STL_MAP = [
    # (filepath, object_name, translate_z_mm, rotate_z_deg, notes)
    (ROOT + r"\02_CASSETTE_HEAD\cylinder\CSM_V3_Cylinder_V3_0_FULL.stl",
     "Cylinder_V3_0", 0.0, 0.0, "cylinder Z=0..75"),
    (ROOT + r"\02_CASSETTE_HEAD\cam_ring\CSM_V3_CamRing_V6_5_FULL.stl",
     "CamRing_V6_5", 19.0, 0.0, "cam ring top at Z=49"),
    (ROOT + r"\02_CASSETTE_HEAD\cassette_base\CSM_V3_CassetteBase_V1_1_FULL.stl",
     "CassetteBase_V1_1", 49.0, 0.0, "cassette bottom at CAM_DATUM_Z"),
    (ROOT + r"\02_CASSETTE_HEAD\sinker_ring\CSM_V3_SinkerRing_V1_2_1_FULL.stl",
     "SinkerRing_V1_2_1", 75.0, 0.0, "sinker bottom at SINKER_Z"),
    (ROOT + r"\02_CASSETTE_HEAD\retainer_ring\CSM_V3_RetainerRing_V1_0_FULL.stl",
     "RetainerRing_V1_0", 83.0, 0.0, "retainer bottom at HOOK_PEAK_Z"),
    (ROOT + r"\06_DRIVE_SYSTEM\CSM_V3_DriveHub_V2_4_2.stl",
     "DriveHub_V2_4_2", -10.0, 0.0, "drive hub below cylinder"),
    (ROOT + r"\06_DRIVE_SYSTEM\CSM_V3_MotorMount_V1_3.stl",
     "MotorMount_V1_3", -120.0, 0.0, "motor mount way below"),
    (ROOT + r"\05_BEARINGS_SHAFT\CSM_V3_BearingHousings_PAIR_V2_5_1.stl",
     "BearingHousings_V2_5", -70.0, 0.0, "bearing pair on shaft"),
]

# Detect Blender STL import operator (renamed in 4.0)
def import_stl(path):
    if hasattr(bpy.ops.wm, "stl_import"):
        bpy.ops.wm.stl_import(filepath=path)
    else:
        bpy.ops.import_mesh.stl(filepath=path)

results = []
for path, name, dz, rz, note in STL_MAP:
    if not os.path.exists(path):
        results.append(f"MISSING: {name} -> {path}")
        continue
    before = set(bpy.data.objects)
    try:
        import_stl(path)
    except Exception as e:
        results.append(f"FAIL {name}: {e}")
        continue
    new = list(set(bpy.data.objects) - before)
    if not new:
        results.append(f"NO_OBJECT {name}")
        continue
    obj = new[0]
    obj.name = name
    # STLs are in mm; Blender scene unit default is meters. Scale to m.
    obj.scale = (0.001, 0.001, 0.001)
    obj.location = (0.0, 0.0, dz * 0.001)   # Z in meters
    if rz:
        obj.rotation_euler = (0, 0, math.radians(rz))
    bpy.context.view_layer.update()
    results.append(f"OK {name:25s} z={dz:+7.1f}mm  ({note})")

# Set scene unit system to mm display, meter internal
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
bpy.context.scene.unit_settings.scale_length = 1.0

print("\n".join(results))
print(f"\nObjects in scene: {len(bpy.data.objects)}")
for o in bpy.data.objects:
    bb = [o.matrix_world @ v.co if o.type == 'MESH' else None for v in []]
    print(f"  {o.name}  type={o.type}")
