# -*- coding: utf-8 -*-
"""
CSM V3 -- YARN PATH VISUALIZATION (Phase-1.5 precursor)

Renders the COMPLETE THREAD ROUTE through the machine, end-to-end:
  cone-top -> upper guide -> tensioner -> feeder nozzle -> hook capture
  -> loop formation -> sinker descent -> fabric column -> take-down exit

This is the static answer to: "How does thread actually move through
this machine?"  The Phase-1.5 kinematic study (Priority D) will then
animate this route through one full cylinder revolution.

Two yarn colors to make the routing clear:
  RED   = active yarn being knit at F1 (motor side, +X, theta=0)
  BLUE  = inactive yarn from F4 (service side, -X, theta=180) -- just
          shown reaching its feeder nozzle, not being knit in this view

Renders 3 views:
  Y1  3/4 perspective with both yarn paths fully drawn
  Y2  Section side showing the vertical journey (cone -> base hole)
  Y3  Top view showing the in-plane geometry (feeder exit -> hook)

Run via:
  & "C:\\Program Files\\Blender Foundation\\Blender 5.1\\blender.exe" ^
    --background --python render_yarn_path.py
"""
import bpy, math, sys, os
from mathutils import Vector

sys.path.insert(0, r"C:\3D-Project\00_PROJECT_OVERVIEW")
import machine_datums as MD

mm = 0.001

# ============================================================
# RESET + HELPERS
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
for m in list(bpy.data.materials):   bpy.data.materials.remove(m)

def mk(name, base=(0.7,0.7,0.72,1.0), rough=0.4, metal=0.0, alpha=1.0, emit_strength=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Base Color"].default_value = base
            n.inputs["Roughness"].default_value = rough
            n.inputs["Metallic"].default_value = metal
            if "Alpha" in n.inputs:
                n.inputs["Alpha"].default_value = alpha
                if alpha < 1.0: m.blend_method = 'BLEND'
            if emit_strength > 0 and "Emission Strength" in n.inputs:
                n.inputs["Emission Strength"].default_value = emit_strength
                n.inputs["Emission Color"].default_value = base
            return m
    return m

def assign(o, mat):
    o.data.materials.clear(); o.data.materials.append(mat)

def imp(name, path, t_mm=(0,0,0), rz_deg=0, mat=None):
    if not os.path.exists(path): return None
    before = set(bpy.data.objects)
    if hasattr(bpy.ops.wm,"stl_import"): bpy.ops.wm.stl_import(filepath=path)
    else: bpy.ops.import_mesh.stl(filepath=path)
    new = list(set(bpy.data.objects) - before)
    if not new: return None
    o = new[0]; o.name = name
    o.scale = (mm,mm,mm)
    o.location = (t_mm[0]*mm, t_mm[1]*mm, t_mm[2]*mm)
    if rz_deg: o.rotation_euler = (0,0,math.radians(rz_deg))
    if mat: assign(o, mat)
    bpy.context.view_layer.update()
    return o

def sphere(name, r, x=0, y=0, z=0, mat=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r*mm, location=(x*mm,y*mm,z*mm))
    o = bpy.context.active_object; o.name = name
    if mat: assign(o, mat)
    return o

def add_curve(name, pts_mm, thickness_mm=1.0, mat=None, resolution=12):
    """Continuous Bezier curve through pts (auto-handles). Tube radius = thickness."""
    cdata = bpy.data.curves.new(name=name, type='CURVE')
    cdata.dimensions = '3D'
    cdata.bevel_depth = thickness_mm * mm
    cdata.bevel_resolution = 4
    cdata.resolution_u = resolution
    spline = cdata.splines.new('BEZIER')
    spline.bezier_points.add(len(pts_mm) - 1)
    for i, p in enumerate(pts_mm):
        bp = spline.bezier_points[i]
        bp.co = (p[0]*mm, p[1]*mm, p[2]*mm)
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    obj = bpy.data.objects.new(name, cdata)
    bpy.context.collection.objects.link(obj)
    if mat: assign(obj, mat)
    return obj

# ============================================================
# MATERIALS
# ============================================================
M = {
    'cylinder':    mk("Cyl",      (0.85, 0.86, 0.88, 0.85), 0.30, alpha=0.85),
    'cam':         mk("Cam",      (0.10, 0.10, 0.12, 1),    0.25, 0.5),
    'cassette':    mk("Cass",     (0.62, 0.64, 0.68, 0.55), 0.35, alpha=0.55),
    'sinker':      mk("Sink",     (0.55, 0.58, 0.62, 1),    0.35),
    'retainer':    mk("Ret",      (0.95, 0.85, 0.55, 0.55), 0.50, alpha=0.55),
    'wood':        mk("Wood",     (0.32, 0.18, 0.08, 1),    0.55),
    'alu':         mk("Alu",      (0.78, 0.82, 0.86, 1),    0.25, 1.0),
    'ext':         mk("Ext",      (0.12, 0.12, 0.14, 1),    0.45, 0.7),
    'feeder':      mk("Feeder",   (0.85, 0.75, 0.45, 0.85), 0.45, alpha=0.85),
    'cone_r':      mk("ConeR",    (0.78, 0.10, 0.10, 1),    0.85),
    'cone_b':      mk("ConeB",    (0.10, 0.25, 0.85, 1),    0.85),

    # Yarn -- bright + emissive so it pops against the cassette
    'yarn_active': mk("YarnActive", (0.98, 0.18, 0.10, 1),  0.50, emit_strength=0.8),
    'yarn_idle':   mk("YarnIdle",   (0.30, 0.45, 0.95, 1),  0.50, emit_strength=0.4),
    'yarn_fabric': mk("YarnFabric", (0.85, 0.30, 0.20, 1),  0.70),

    # Waypoint markers
    'pt_cone':     mk("Pt_Cone",    (1.00, 0.30, 0.10, 1), 0.30),
    'pt_guide':    mk("Pt_Guide",   (1.00, 0.80, 0.10, 1), 0.30),
    'pt_tension':  mk("Pt_Tension", (1.00, 1.00, 0.10, 1), 0.30),
    'pt_nozzle':   mk("Pt_Nozzle",  (1.00, 0.45, 0.00, 1), 0.30),
    'pt_hook':     mk("Pt_Hook",    (1.00, 0.10, 0.00, 1), 0.30, emit_strength=1.0),
    'pt_loop':     mk("Pt_Loop",    (0.30, 1.00, 0.30, 1), 0.30, emit_strength=0.5),
    'pt_takedown': mk("Pt_Takedown",(0.10, 0.80, 0.50, 1), 0.30),

    'ground':      mk("Ground",   (0.18, 0.20, 0.24, 1),    0.65),
}

# ============================================================
# LOAD GEOMETRY (assembly but ghosted in places to see yarn through)
# ============================================================
print("Loading geometry...")
A = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY"
L = r"C:\3D-Project\01_MECHANICAL"
WZ = MD.CYL_BOTTOM_WORLD_Z

# Frame
imp("WoodBase",   os.path.join(A,"frame","wood_base","CSM_V3_WoodBase_V1_1.stl"), mat=M['wood'])
for i,(ux,uy) in enumerate([(+150,+120),(+150,-120),(-150,+120),(-150,-120)]):
    imp(f"Upright_{i}", os.path.join(A,"frame","upright_2020","CSM_V3_Upright2020_V1_1.stl"),
        t_mm=(ux,uy,0), mat=M['ext'])
imp("UpperDeck",  os.path.join(A,"frame","wood_upper_deck","CSM_V3_WoodUpperDeck_V1_0.stl"), mat=M['wood'])
imp("MountPlate", os.path.join(A,"frame","mount_plate_6061","CSM_V3_MountPlate6061_V1_1.stl"), mat=M['alu'])

# Cassette -- ghosted so we can see yarn passing through
imp("Cylinder",  os.path.join(L,"02_CASSETTE_HEAD","cylinder","CSM_V3_Cylinder_V3_0_FULL.stl"),    t_mm=(0,0,WZ), mat=M['cylinder'])
imp("CamRing",   os.path.join(L,"02_CASSETTE_HEAD","cam_ring","CSM_V3_CamRing_V6_5_FULL.stl"),     t_mm=(0,0,19+WZ), mat=M['cam'])
imp("Cassette",  os.path.join(L,"02_CASSETTE_HEAD","cassette_base","CSM_V3_CassetteBase_V1_1_FULL.stl"), t_mm=(0,0,49+WZ), mat=M['cassette'])
imp("Sinker",    os.path.join(L,"02_CASSETTE_HEAD","sinker_ring","CSM_V3_SinkerRing_V1_2_1_FULL.stl"),   t_mm=(0,0,75+WZ), mat=M['sinker'])
imp("Retainer",  os.path.join(L,"02_CASSETTE_HEAD","retainer_ring","CSM_V3_RetainerRing_V1_0_FULL.stl"), t_mm=(0,0,83+WZ), mat=M['retainer'])

# Feeders + cones
FRO = MD.PCD_FEEDER/2 + 25.0
imp("Feeder_F1", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"),
    t_mm=(FRO,0,0), rz_deg=-90, mat=M['feeder'])
imp("Feeder_F4", os.path.join(A,"feeder_module","CSM_V3_FeederModule_V1_1.stl"),
    t_mm=(-FRO,0,0), rz_deg=+90, mat=M['feeder'])
imp("YarnCone_F1", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"),
    t_mm=(FRO,20,250), mat=M['cone_r'])
imp("YarnCone_F4", os.path.join(A,"decor","yarn_cone","CSM_V3_YarnCone_V1_0.stl"),
    t_mm=(-FRO,-20,250), mat=M['cone_b'])

# ============================================================
# YARN PATH WAYPOINTS  (F1 = active, motor side, theta=0 deg)
# ============================================================
print("Computing yarn path...")

# Hook capture point (Slot #0 at peak cam lift, just inside cylinder OD)
HOOK_X = MD.CYL_OD/2 - 1.0   # 56.15 (just inside slot opening)
HOOK_Y = 0.0
HOOK_Z = MD.world_z(MD.HOOK_PEAK_Z)   # 264

# Feeder F1 nozzle exit (outboard of cassette)
FEED_X = MD.PCD_FEEDER/2 + 5.0   # 100 (outboard of PCD 190)
FEED_Y = 0.0
FEED_Z = MD.world_z(MD.FEEDER_REFERENCE_Z)   # 271

# Cone for F1: positioned at (FRO=120, 20, 250 base + ~50 top)
CONE_TOP_X = FRO
CONE_TOP_Y = 20.0
CONE_TOP_Z = 250 + 80   # 330 (top of cone -- yarn exits from top)

# Upper guide eye above the cone (yarn unwinds from cone top, through eye)
UPPER_GUIDE_X = FRO
UPPER_GUIDE_Y = 20.0
UPPER_GUIDE_Z = 380.0

# Tensioner zone (inside feeder body)
TENSION_X = FRO
TENSION_Y = -5.0
TENSION_Z = 280.0

# Hook loop formation point (just below hook peak, where loop pulls down)
LOOP_X = MD.CYL_OD/2 - 4.0   # 53.15 (pulled inside cylinder bore region)
LOOP_Y = 0.0
LOOP_Z = MD.world_z(MD.SINKER_Z)    # 256 (one cam stroke below hook peak)

# Fabric column descent (down through cylinder bore)
FABRIC_TOP_X = 0
FABRIC_TOP_Y = 0
FABRIC_TOP_Z = MD.world_z(MD.SINKER_Z) - 5    # 251
FABRIC_MID_Z = MD.world_z(MD.CYLINDER_Z0) + 40  # 221 (mid cylinder bore)
FABRIC_BOT_Z = MD.WOOD_BASE_TOP_Z + 5          # 23 (just above wood base hole)

# Take-down exit (through D100 hole in wood base)
TAKEDOWN_TOP_Z = MD.WOOD_BASE_TOP_Z   # 18
TAKEDOWN_BOT_Z = MD.WOOD_BASE_BOTTOM_Z - 30   # -30 (through hole, weight hangs below)

# ============================================================
# BUILD F1 YARN PATH (active yarn -- being knit)
# ============================================================
print("  F1 active yarn: cone -> guide -> tensioner -> nozzle -> hook -> loop -> fabric -> takedown")

f1_path = [
    (CONE_TOP_X,    CONE_TOP_Y,    CONE_TOP_Z),     # 1. yarn unwinds from cone top
    (UPPER_GUIDE_X, UPPER_GUIDE_Y, UPPER_GUIDE_Z),  # 2. upper guide eye
    (TENSION_X,     TENSION_Y,     TENSION_Z),     # 3. through tensioner
    (FEED_X + 5,    FEED_Y,        FEED_Z + 8),    # 4a. yarn entering feeder body
    (FEED_X,        FEED_Y,        FEED_Z),         # 4b. feeder nozzle exit (yarn presented)
    (HOOK_X + 8,    HOOK_Y,        HOOK_Z + 4),    # 5a. yarn descending toward hook
    (HOOK_X,        HOOK_Y,        HOOK_Z),         # 5b. hook capture point
    (LOOP_X,        LOOP_Y,        LOOP_Z),         # 6. loop formation / knock-over
]
add_curve("YarnPath_F1_active", f1_path, thickness_mm=1.2, mat=M['yarn_active'])

# Fabric column (knit fabric descends through cylinder bore)
fabric_path = [
    (LOOP_X,       LOOP_Y,       LOOP_Z),
    (FABRIC_TOP_X, FABRIC_TOP_Y, FABRIC_TOP_Z),
    (FABRIC_TOP_X, FABRIC_TOP_Y, FABRIC_MID_Z),
    (FABRIC_TOP_X, FABRIC_TOP_Y, FABRIC_BOT_Z),
    (FABRIC_TOP_X, FABRIC_TOP_Y, TAKEDOWN_TOP_Z),
    (FABRIC_TOP_X, FABRIC_TOP_Y, TAKEDOWN_BOT_Z),
]
add_curve("YarnPath_Fabric", fabric_path, thickness_mm=2.5, mat=M['yarn_fabric'])

# F4 idle yarn (cone -> guide -> tensioner -> nozzle, but NOT knit in this view)
F4_FRO = -FRO
f4_path = [
    (-FRO,             -20,  CONE_TOP_Z),
    (-FRO,             -20,  UPPER_GUIDE_Z),
    (-FRO,               5,  TENSION_Z),
    (-FEED_X - 5,        0,  FEED_Z + 8),
    (-FEED_X,            0,  FEED_Z),    # ends at nozzle exit, no further routing
]
add_curve("YarnPath_F4_idle", f4_path, thickness_mm=1.0, mat=M['yarn_idle'])

# ============================================================
# WAYPOINT MARKERS (semantic, color-coded)
# ============================================================
print("  Waypoint markers...")

sphere("Pt1_ConeTop",  r=2.5, x=CONE_TOP_X,    y=CONE_TOP_Y,    z=CONE_TOP_Z,    mat=M['pt_cone'])
sphere("Pt2_UpperGuide", r=2.0, x=UPPER_GUIDE_X, y=UPPER_GUIDE_Y, z=UPPER_GUIDE_Z, mat=M['pt_guide'])
sphere("Pt3_Tensioner", r=2.0, x=TENSION_X,    y=TENSION_Y,    z=TENSION_Z,    mat=M['pt_tension'])
sphere("Pt4_NozzleExit", r=2.5, x=FEED_X,       y=FEED_Y,       z=FEED_Z,       mat=M['pt_nozzle'])
sphere("Pt5_HookPeak",  r=3.0, x=HOOK_X,       y=HOOK_Y,       z=HOOK_Z,       mat=M['pt_hook'])
sphere("Pt6_LoopForm",  r=2.5, x=LOOP_X,       y=LOOP_Y,       z=LOOP_Z,       mat=M['pt_loop'])
sphere("Pt7_TakedownExit", r=3.0, x=0,         y=0,            z=TAKEDOWN_TOP_Z,
       mat=M['pt_takedown'])

# Ground
bpy.ops.mesh.primitive_plane_add(size=3.0, location=(0,0,-0.06))
g = bpy.context.active_object; g.name = "Ground"
assign(g, M['ground'])

# ============================================================
# LIGHTING (clean engineering)
# ============================================================
def light(name, ltype, loc, energy, rot=(0,0,0), size=0.8):
    bpy.ops.object.light_add(type=ltype, location=loc)
    L = bpy.context.active_object; L.name = name
    L.data.energy = energy
    if hasattr(L.data,'size'): L.data.size = size
    L.rotation_euler = rot

light("Sun",  'SUN',  loc=(-0.5,-0.7,2.5), energy=1.0,
      rot=(math.radians(45),math.radians(-15),math.radians(35)))
light("Key",  'AREA', loc=(0.7,-0.7,0.5),  energy=40,
      rot=(math.radians(-50),0,math.radians(135)), size=0.6)
light("Fill", 'AREA', loc=(-0.7,0.4,0.4),  energy=20,
      rot=(math.radians(70),0,math.radians(-110)), size=1.0)

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World"); bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.12, 0.14, 0.18, 1.0)
    bg.inputs[1].default_value = 0.25

# ============================================================
# RENDER SETTINGS
# ============================================================
scene = bpy.context.scene
try:
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    try: scene.cycles.device = 'GPU'
    except Exception: pass
except Exception:
    for cand in ['BLENDER_EEVEE_NEXT','BLENDER_EEVEE']:
        try: scene.render.engine = cand; break
        except Exception: continue
scene.render.resolution_x = 1920
scene.render.resolution_y = 1200
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -0.7

OUT_DIR = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"

def set_cam(name, pos, look_at, ortho=False, ortho_scale=1.0, lens=50):
    bpy.ops.object.camera_add(location=pos)
    cam = bpy.context.active_object; cam.name = name
    if ortho:
        cam.data.type = 'ORTHO'; cam.data.ortho_scale = ortho_scale
    else:
        cam.data.lens = lens
    dirv = Vector(look_at) - Vector(pos)
    cam.rotation_euler = dirv.to_track_quat('-Z','Y').to_euler()
    scene.camera = cam
    return cam

def render_to(name):
    out = os.path.join(OUT_DIR, f"CSM_V3_YarnPath_{name}.png")
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    sz = os.path.getsize(out) if os.path.exists(out) else 0
    print(f"  [{name}] {out} ({sz/1024:.0f} KB)")

# ============================================================
# 3 VIEWS
# ============================================================
print("\n[Y1] 3/4 perspective with full yarn paths")
set_cam("CamY1", pos=(0.55,-0.80,0.40), look_at=(0,0,0.20), lens=42)
render_to("Y1_full")

print("\n[Y2] Side section showing vertical journey")
set_cam("CamY2", pos=(1.5, 0.0, 0.20), look_at=(0,0,0.20),
        ortho=True, ortho_scale=0.55)
render_to("Y2_side")

print("\n[Y3] Top view, in-plane yarn geometry")
set_cam("CamY3", pos=(0,0,1.5), look_at=(0,0,0.265),
        ortho=True, ortho_scale=0.45)
render_to("Y3_top")

# Save .blend
blend_path = os.path.join(OUT_DIR, "CSM_V3_YarnPath.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print(f"\nSaved .blend: {blend_path}")
print("\nDONE -- 3 yarn-path views.")
print("\nLEGEND:")
print("  RED bright curve   = F1 ACTIVE yarn being knit (cone -> hook)")
print("  RED-darker curve   = fabric column (knit sock descending through bore)")
print("  BLUE curve         = F4 IDLE yarn (parked at nozzle, not knitting)")
print("  Color-coded spheres at each kinematic waypoint:")
print("    Pt1 cone-top    | Pt2 upper-guide  | Pt3 tensioner")
print("    Pt4 nozzle-exit | Pt5 HOOK-PEAK    | Pt6 loop-form")
print("    Pt7 take-down exit (through wood-base D100 hole)")
