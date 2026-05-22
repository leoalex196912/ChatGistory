# -*- coding: utf-8 -*-
"""
machine_datums.py -- CSM V3 importable constants module

THIS FILE IS THE PYTHON MIRROR OF MACHINE_DATUMS.md (R2 final).
Hand-edit the .md FIRST, then sync this file. Both are tracked in git
and reviewed together. The .md is the human-readable spec; this is
the machine-readable spec.

USAGE
-----
In any FreeCAD macro, Blender script, or assembly utility:

    import sys, os
    sys.path.insert(0, r"C:\\3D-Project\\00_PROJECT_OVERVIEW")
    import machine_datums as MD

    cyl_bottom_world = MD.CYL_BOTTOM_WORLD_Z   # 181.0
    world_z = MD.world_z(MD.CAM_DATUM_Z)       # 230.0

NEVER hardcode world-coordinate numbers in macros or assembly scripts.
Reference MD.<NAME> by name. This is the "no hardcoded world coords"
rule from architecture lock 2026-05-20.

AUTHORITY ORDER
---------------
1. MACHINE_COORDINATE_SYSTEM.md  -- defines axes, origin, transform
2. MACHINE_DATUMS.md             -- defines numerical values
3. machine_datums.py             -- THIS FILE (mirror of #2)
4. component macros              -- import from THIS FILE

If this file and MACHINE_DATUMS.md disagree, the .md wins. Update
this file to match.
"""

# ============================================================
# WORLD <-> CYLINDER-LOCAL TRANSFORM
# (See MACHINE_COORDINATE_SYSTEM.md R1 §4)
# ============================================================
CYL_BOTTOM_WORLD_Z = 181.0   # mm. world Z of cylinder local Z=0
                              # = ALU_PLATE_TOP_Z - CAM_DATUM_Z
                              # = 230 - 49 = 181

def world_z(local_z):
    """Convert cylinder-local Z to world Z."""
    return local_z + CYL_BOTTOM_WORLD_Z

def local_z(world_z_value):
    """Convert world Z to cylinder-local Z."""
    return world_z_value - CYL_BOTTOM_WORLD_Z

# ============================================================
# CYLINDER-LOCAL DATUMS  (from MACHINE_DATUMS.md R2)
# ============================================================
CYLINDER_Z0          =  0.0    # cylinder bottom (= drive hub boss top)
CAM_DATUM_Z          = 49.0    # cam ring top / cassette base bottom
CASSETTE_TOP_Z       = 63.0    # outer disc top of cassette base
SINKER_Z             = 75.0    # sinker register plane
CYLINDER_TOP_Z       = 75.0    # cylinder top face (semantically distinct from SINKER_Z)
FEEDER_REFERENCE_Z   = 90.0    # nominal feeder finger height (provisional, Phase 1.5 validates)
HOOK_PEAK_Z          = 83.0    # needle hook position at peak cam lift

# Derived (DO NOT EDIT DIRECTLY)
HOOK_LIFT            = HOOK_PEAK_Z - CYLINDER_TOP_Z      # 8.0 mm
CASSETTE_DISC_THICK  = CASSETTE_TOP_Z - CAM_DATUM_Z      # 14.0 mm
SINKER_TO_HOOK_GAP   = HOOK_PEAK_Z - SINKER_Z            # 8.0 mm
FEEDER_ABOVE_HOOK    = FEEDER_REFERENCE_Z - HOOK_PEAK_Z  # 7.0 mm

# ============================================================
# CASSETTE GEOMETRY (cylindrical centerlines)
# ============================================================
CYL_OD                  = 114.30
CYL_ID                  =  88.00
SLOT_BOTTOM_RADIUS_DIM  = 107.50   # OD - 2*slot_depth(3.0)
CAM_RING_ID             = 115.00
CAM_RING_OD             = 165.00
CASSETTE_CENTER_HOLE_D  = 117.00
SINKER_PEDESTAL_ID      = 128.00
SINKER_PEDESTAL_OD      = 150.00
SINKER_REG_POCKET_D     = 135.30
SINKER_RING_OD          = 135.00
SINKER_RING_ID          = 115.30
CASSETTE_BASE_OD        = 200.00
RETAINER_OD             = 200.00
RETAINER_THROUGH_BORE   = 118.00
RETAINER_LIP_ID         = 104.00

# ============================================================
# BOLT PATTERNS (PCD = Pitch Circle Diameter, mm)
# All angular offsets are MACHINE FRAME angles (+X axis = 0 deg)
# See ANGULAR_REFERENCE_STANDARD.md R1
# ============================================================
PCD_CAM_BOLTS          = 155.0   # 6x M5, 30 deg offset
PCD_CAM_PINS           = 145.0   # 6x D4 dowels, 0 deg offset
PCD_FEEDER             = 190.0   # 6x M4, 0 deg offset (shared by retainer)
PCD_FRAME_MOUNT        = 180.0   # 4x M5, 45 deg offset
PCD_RIBBER             = 140.0   # 6x M4, 0 deg offset (Phase 2 provision)
PCD_CYL_TO_DRIVE_HUB   =  70.0   # 4x M5, 45 deg offset
PCD_HALL_MAGNET        =  95.0   # 1x D6 magnet, 0 deg

# ============================================================
# FRAME GEOMETRY (world coordinates)
# Origin: cylinder rotation axis projected to Z=0 (wood base bottom)
# See MACHINE_DATUMS.md R2 final
# ============================================================
FRAME_ORIGIN_XY        = (0.0, 0.0)

# Wood base
WOOD_BASE_W            = 500.0
WOOD_BASE_D            = 400.0
WOOD_BASE_T            =  18.0
WOOD_BASE_BOTTOM_Z     =   0.0
WOOD_BASE_TOP_Z        =  18.0
TAKEDOWN_HOLE_D        = 100.0   # ICD Interface 11 (sock take-down column)

# 2020 aluminum uprights (precision frame, 4x at corners of upper deck)
UPRIGHT_W              =  20.0
UPRIGHT_LEN            = 188.0
UPRIGHT_BOT_Z          =  18.0   # = WOOD_BASE_TOP_Z
UPRIGHT_TOP_Z          = 206.0   # = UPRIGHT_BOT_Z + UPRIGHT_LEN
UPRIGHT_X_POSITIONS    = (+150.0, -150.0)
UPRIGHT_Y_POSITIONS    = (+120.0, -120.0)

# Wood upper deck (sits on uprights)
UPPER_DECK_W           = 320.0   # X span
UPPER_DECK_D           = 260.0   # Y span
UPPER_DECK_T           =  18.0
UPPER_DECK_BOTTOM_Z    = 206.0
UPPER_DECK_TOP_Z       = 224.0

# Aluminum master-datum plate
ALU_PLATE_W            = 250.0
ALU_PLATE_D            = 250.0
ALU_PLATE_T            =   6.0
ALU_PLATE_BOTTOM_Z     = 224.0
ALU_PLATE_TOP_Z        = 230.0   # MASTER DATUM PLANE (ICD invariant B3)
ALU_PLATE_MATERIAL     = "6061-T6 mill finish"

# Touchscreen mast (dual 2020 + crossbar, REAR of wood base, -Y)
MAST_UPRIGHT_LEN       = 400.0
MAST_CENTER_X          =   0.0
MAST_CENTER_Y          = -180.0
MAST_X_OFFSETS         = (+30.0, -30.0)
MAST_TOP_CROSSBAR_LEN  =  60.0
MAST_TOP_Z             = 418.0   # = WOOD_BASE_TOP_Z + MAST_UPRIGHT_LEN

# ============================================================
# BOUGHT-PARTS DIMENSIONS (purchased components)
# ============================================================

# Drive shaft + bearings
SHAFT_D                = 12.00   # FEYRINX h8 steel
SHAFT_LENGTH           = 150.00  # provisional, final cut to fit
BEARING_6001_OD        = 28.00
BEARING_6001_ID        = 12.00
BEARING_6001_W         =  8.00

# NEMA 17 drive motor
NEMA17_BODY_W          = 42.30
NEMA17_BODY_L          = 40.00
NEMA17_SHAFT_D         =  5.00
NEMA17_SHAFT_L         = 24.00
NEMA17_MOUNT_PCD       = 31.00
NEMA17_BOSS_D          = 22.00
NEMA17_BOSS_H          =  2.00

# NEMA 11 feeder motor (Phase 1 feeders)
NEMA11_BODY_W          = 28.0
NEMA11_BODY_L          = 32.0
NEMA11_SHAFT_D         =  5.0
NEMA11_SHAFT_L         = 20.0
NEMA11_MOUNT_PCD       = 23.0

# Drive hub
DRIVE_HUB_BOSS_OD      = 18.00
DRIVE_HUB_BOSS_H       =  3.00
DRIVE_HUB_FLANGE_OD    = 90.00
DRIVE_HUB_BOLT_PCD     = 70.00

# HTD 5M timing belt + pulleys
PULLEY_BIG_TEETH       = 60
PULLEY_BIG_OD          = 97.50
PULLEY_BIG_BORE        = 12.00
PULLEY_BIG_W           = 16.00
PULLEY_SMALL_TEETH     = 16
PULLEY_SMALL_OD        = 27.40
PULLEY_SMALL_BORE      =  5.00
PULLEY_SMALL_W         = 16.00
GEAR_RATIO             = 60.0 / 16.0   # 3.75
BELT_WIDTH             = 15.00
BELT_THICKNESS         =  3.00

# Drive motor placement (Interface 6, +X side, rear -Y)
MOTOR_X                =  90.0
MOTOR_Y                = -100.0
MOTOR_BODY_BOTTOM_Z    =  18.0
BELT_CENTER_DISTANCE   = 134.5   # sqrt(90^2 + 100^2) provisional
BELT_TENSION_TRAVEL    =  30.0   # SE5 X-travel slot

# Electronics (sit on wood base, Layer 3)
MEGA_W,  MEGA_D,  MEGA_H   = 101.0, 53.0, 15.0
TB6600_W, TB6600_D, TB6600_H = 96.0, 56.0, 33.0
LRS50_W, LRS50_D, LRS50_H  =  99.0, 82.0, 30.0

# Touchscreen
TOUCH_W, TOUCH_D, TOUCH_H  = 165.0, 100.0, 10.0

# Hall sensor + index magnet
HALL_SENSOR_PART       = "SS49E"
MAGNET_PART            = "B0F4KS6KV3"
MAGNET_POCKET_D        =   6.0
MAGNET_POCKET_H        =   2.2

# ============================================================
# CYLINDER (Cylinder V3.0 specifics)
# ============================================================
CYL_HEIGHT             = 75.0
SLOT_COUNT             = 72
SLOT_PITCH_DEG         = 360.0 / SLOT_COUNT   # 5.0
SLOT_WIDTH             =  1.22
SLOT_DEPTH             =  3.00
SPRING_GROOVE_DEPTH    =  1.30
SPRING_GROOVE_W        =  4.00
SPRING_GROOVE_Z_CTR    = 55.0

# ============================================================
# ANGULAR PHASE REFERENCE (theta = 0 deg)
# See ANGULAR_REFERENCE_STANDARD.md R1
# ============================================================
THETA_HALL_INDEX       =   0.0   # Hall index magnet at +X axis
THETA_SLOT_0           =   0.0   # Slot #0 aligned with +X at theta_cyl=0
THETA_OPERATOR_FRONT   =  90.0   # +Y axis (NOT 0)
THETA_SERVICE_SIDE     = 180.0   # -X axis
THETA_REAR             = 270.0   # -Y axis (touchscreen mast)

# Feeder positions (PCD 190, 6x M4, 0 deg offset)
FEEDER_POSITIONS = {
    "F1": (  0.0, True),    # +X motor side       -- Phase 1 ACTIVE
    "F2": ( 60.0, False),   # front-right         -- Phase 2
    "F3": (120.0, False),   # front-left          -- Phase 2
    "F4": (180.0, True),    # -X service side     -- Phase 1 ACTIVE
    "F5": (240.0, False),   # rear-left           -- Phase 2
    "F6": (300.0, False),   # rear-right          -- Phase 2
}
CYL_ROTATION_DIR       = "CCW from +Z"

# ============================================================
# SERVICE ENVELOPES (summary -- full spec in SERVICE_ENVELOPES.md)
# ============================================================
SE1_COLUMN_RADIUS      =  60.0   # cylinder removal column radius
SE1_COLUMN_Z_LOW       = 272.0
SE1_COLUMN_Z_HIGH      = 430.0

SE5_MOTOR_X_TRAVEL     =  30.0   # belt replacement motor slot
SE5_PULLEY_VERT_CLEAR  =  80.0

# ============================================================
# BUILD-TIME SELF-CHECK
# ============================================================
def _self_check():
    """Verify derived frame Z stack matches CYL_BOTTOM_WORLD_Z constant.
    Raises if frame architecture has drifted from the transform."""
    derived = ALU_PLATE_TOP_Z - CAM_DATUM_Z
    assert abs(derived - CYL_BOTTOM_WORLD_Z) < 0.001, (
        f"machine_datums.py drift: derived CYL_BOTTOM_WORLD_Z = {derived}, "
        f"but constant is {CYL_BOTTOM_WORLD_Z}. Fix the cause."
    )

_self_check()


if __name__ == "__main__":
    # Quick sanity print when run directly
    print(f"CSM V3 machine_datums.py loaded.")
    print(f"  CYL_BOTTOM_WORLD_Z = {CYL_BOTTOM_WORLD_Z}")
    print(f"  ALU_PLATE_TOP_Z    = {ALU_PLATE_TOP_Z} (master datum)")
    print(f"  HOOK_PEAK_WORLD_Z  = {world_z(HOOK_PEAK_Z)}")
    print(f"  Phase 1 feeders    = "
          f"{[k for k,(_,act) in FEEDER_POSITIONS.items() if act]}")
    print("  _self_check passed.")
