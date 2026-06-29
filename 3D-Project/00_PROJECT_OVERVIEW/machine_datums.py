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
# Wood thickness 18 -> 12 mm (2026-06-27): user ordered 12 mm Baltic Birch.
# Uprights lengthened 188 -> 200 mm to compensate (cut tolerance absorbs
# the 0.3 mm needed to keep master datum at Z=230 exactly).
WOOD_BASE_W            = 500.0
WOOD_BASE_D            = 400.0
WOOD_BASE_T            =  12.0   # 12 mm Baltic Birch plywood (was 18)
WOOD_BASE_BOTTOM_Z     =   0.0
WOOD_BASE_TOP_Z        =  12.0   # = WOOD_BASE_T
TAKEDOWN_HOLE_D        = 100.0   # ICD Interface 11 (sock take-down column)

# 2020 aluminum uprights (precision frame, 4x at corners of upper deck)
# Practical cut length 200 mm; CAD-exact is 199.7 to land plate top exactly
# at Z=230. 0.3 mm is well within saw kerf / stack tolerance.
UPRIGHT_W              =  20.0
UPRIGHT_LEN            = 199.7   # cut to 200 mm in practice (was 188)
UPRIGHT_BOT_Z          =  12.0   # = WOOD_BASE_TOP_Z
UPRIGHT_TOP_Z          = 211.7   # = UPRIGHT_BOT_Z + UPRIGHT_LEN
UPRIGHT_X_POSITIONS    = (+150.0, -150.0)
UPRIGHT_Y_POSITIONS    = (+120.0, -120.0)

# Wood upper deck (sits on uprights)
UPPER_DECK_W           = 320.0   # X span
UPPER_DECK_D           = 260.0   # Y span
UPPER_DECK_T           =  12.0   # 12 mm Baltic Birch plywood (was 18)
UPPER_DECK_BOTTOM_Z    = 211.7   # = UPRIGHT_TOP_Z (was 206)
UPPER_DECK_TOP_Z       = 223.7   # = UPPER_DECK_BOTTOM_Z + UPPER_DECK_T

# Aluminum master-datum plate
ALU_PLATE_W            = 250.0
ALU_PLATE_D            = 250.0
ALU_PLATE_T            =   6.3    # 1/4" plate (was 6.0 mm — supplier stock)
ALU_PLATE_BOTTOM_Z     = 223.7    # = ALU_PLATE_TOP_Z - ALU_PLATE_T
ALU_PLATE_TOP_Z        = 230.0    # MASTER DATUM PLANE (ICD invariant B3, locked)
ALU_PLATE_MATERIAL     = "6061-T6 mill finish"

# Touchscreen mast (LEGACY -- pre Module-10 lock; do not import in new code)
# These values are kept for backward compatibility with older docs only.
# All NEW HMI code MUST reference the HMI_* block below (ICD R7 Module 10).
MAST_UPRIGHT_LEN       = 400.0
MAST_CENTER_X          =   0.0
MAST_CENTER_Y          = -180.0
MAST_X_OFFSETS         = (+30.0, -30.0)
MAST_TOP_CROSSBAR_LEN  =  60.0
MAST_TOP_Z             = 418.0

# ============================================================
# HMI MODULE 10  (ICD R7 -- locked 2026-06-28)
# Single source of truth for Module 10 (HMI) dimensions.
# Any HMI macro reads constants from this block.
# ============================================================

# Mast placement and stick
HMI_MAST_X_POSITIONS   = (+75.0, -75.0)   # left + right mast centers
HMI_MAST_SPACING_X     = 150.0
HMI_MAST_Y             = -210.0            # wood-base Y of mast feet
HMI_MAST_LEN           = 400.0             # 2020 stick length (cut from 500)

# 2020 extrusion + slip fit
HMI_EXT_W              = 20.0
HMI_EXT_CLEAR          = 0.4               # 0.2 mm per side, FDM slip fit
HMI_POCKET_W           = HMI_EXT_W + 2 * HMI_EXT_CLEAR     # 20.8

# Heat-set inserts (BOM B0DPQJ4W3Z, M5 brass, ~Ø6.4 x 8 mm)
HMI_INSERT_POCKET_D    = 6.2               # press fit (insert OD - 0.2)
HMI_INSERT_POCKET_H    = 8.5

# Foot/beam bolt counterbore for M5 socket-head cap screws
HMI_M5_THROUGH_D       = 5.5
HMI_BOLT_CB_D          = 9.5
HMI_BOLT_CB_H          = 5.5

# Lead-in chamfer at pocket entries
HMI_POCKET_CHAMFER     = 1.0

# === Mast Base Socket V1.3 ===
HMI_SOCKET_OUTER_W     = 34.0
HMI_SOCKET_OUTER_T     = 34.0
HMI_SOCKET_H           = 50.0              # mast engagement
HMI_SOCKET_BOT_T       = 5.0               # closed pocket floor
HMI_SOCKET_POCKET_R    = 1.5               # inner corner fillet
HMI_FOOT_LEN           = 70.0
HMI_FOOT_W             = 54.0
HMI_FOOT_T             = 10.0
HMI_FOOT_BOLT_DX       = 25.0
HMI_FOOT_BOLT_DY       = 19.0
HMI_GUSSET_BASE        = 25.0
HMI_GUSSET_RISE        = 30.0
HMI_GUSSET_T           = 6.0
HMI_FRONT_BOSS_W       = 14.0
HMI_FRONT_BOSS_T       = 4.0
HMI_DRAIN_D            = 3.0

# === Mast Base Socket V1.3 (continued) ===
HMI_RIB_T              = 3.0               # diagonal anti-creep rib thickness
HMI_RIB_H              = 6.0               # rib height above foot
HMI_RIB_OVERLAP        = 4.0               # rib end inside gusset footprint
HMI_T_BOLT_Z1          = 12.0              # lateral 2020 T-nut bolt, low
HMI_T_BOLT_Z2          = 38.0              # lateral 2020 T-nut bolt, high
HMI_EXP_INSERT_COUNT   = 4                 # FRONT-face accessory inserts (socket)
HMI_EXP_INSERT_PITCH   = 20.0
HMI_EXP_INSERT_Z0_REL  = 6.0               # first insert above foot top
HMI_FRONT_BOSS_Z0_REL  = 1.0               # boss starts 1 mm above foot
HMI_FRONT_BOSS_TOP_REL = 5.0               # boss ends N mm below socket top

# === Cross Beam V1.2 ===
HMI_BEAM_LEN_X         = 178.0
HMI_BEAM_W_Y           = 40.0
HMI_BEAM_H_Z           = 30.0
HMI_BEAM_POCKET_DEPTH  = 12.0
HMI_BEAM_END_MARGIN    = 15.0              # cable channel margin each end
HMI_PI_MOUNT_PCD_X     = 58.0              # beam-side Pi Carrier interface
HMI_PI_MOUNT_PCD_Y     = 28.0              # Pi Carrier adapts to Pi 4 58 x 49
HMI_SERVICE_OPEN_X     = 50.0
HMI_SERVICE_OPEN_Y     = 16.0
HMI_CABLE_CH_W         = 8.0
HMI_CABLE_CH_D         = 4.0
HMI_FRONT_INSERT_COUNT = 6                 # FRONT-face accessory inserts (beam)
HMI_FRONT_INSERT_PITCH = 22.0

# === Touchscreen Frame V1.0 (Part M10-P05) ===
# Back plate for ELECROW RC070S 7" touchscreen (Amazon B08FMNDDSL).
# Plate hangs below beam FRONT face; screen attaches via 4 brass pillars
# (included in ELECROW kit) -- M2.5 screws through plate slots into pillars.
HMI_FRAME_W                = 180.0
HMI_FRAME_H                = 130.0
HMI_FRAME_T                = 5.0
HMI_FRAME_TAB_HEIGHT       = 18.0    # band at top with beam-mount bolts
HMI_FRAME_BEAM_BOLT_Z      = 7.0     # bolt center distance from top edge
HMI_FRAME_CABLE_CUT_W      = 30.0    # bottom-edge cable cutout, X width
HMI_FRAME_CABLE_CUT_H      = 10.0    # bottom-edge cable cutout, Z up
HMI_TOUCH_W                = 164.9   # ELECROW RC070S, from official drawing 7inch-D_Size
HMI_TOUCH_H                = 102.0   # (was 165 x 100; corrected from drawing)
HMI_TOUCH_T                = 10.0    # LCD module thickness (front bezel)
HMI_TOUCH_DEPTH_TOTAL      = 34.73   # total depth incl. back PCB (per drawing)
HMI_TOUCH_TOP_MARGIN       = 1.0     # clearance between tab band and screen top
HMI_TOUCH_PCD_X_NOMINAL    = 80.0    # ELECROW mount PCD 79.45 (drawing) -> round 80
HMI_TOUCH_PCD_Y_NOMINAL    = 64.0    # ELECROW mount PCD 64.4 (drawing) -> round 64
HMI_TOUCH_WIN_W            = 30.0    # mount window X (PCD X range 50-110)
HMI_TOUCH_WIN_H            = 30.0    # mount window Z (PCD Y range 34-94)
HMI_M2_5_CLEAR_D           = 3.0     # M2.5 screw clearance hole

# === Expansion Plate V1.0 (Part M10-P10) ===
# Generic accessory plate that bolts to 4 of the 6 cross-beam FRONT-face
# M5 heat-set inserts.  Carries a grid of M3 holes for mounting any
# downstream accessory (sensor PCB, LED driver, label maker, etc.)
HMI_EXP_PLATE_W       = 110.0   # plate X (along beam)
HMI_EXP_PLATE_H       = 70.0    # plate Z (vertical)
HMI_EXP_PLATE_T       = 4.0     # plate thickness (Y)
HMI_EXP_M3_CLEAR_D    = 3.5     # M3 clearance for accessory mounting
HMI_EXP_GRID_PITCH_X  = 20.0    # X spacing of M3 grid
HMI_EXP_GRID_PITCH_Z  = 20.0    # Z spacing of M3 grid
HMI_EXP_GRID_COLS     = 5       # 5 columns of M3 (X = -40 .. +40)
HMI_EXP_GRID_ROWS     = 3       # 3 rows of M3
HMI_EXP_BEAM_BOLT_Z   = 7.0     # M5 bolt center distance from top edge
                                  # (7 leaves 3.5 mm clear to top M3 row;
                                  # 10 only left 0.5 mm)
HMI_EXP_CORNER_R      = 3.0     # plate corner fillet

# === LED Strip Holder V1.0 (Part M10-P09) ===
# Long thin channel that zip-ties to the cross beam underside, carrying a
# 5 V LED strip (10 x 2-3 mm) pointing down for cassette work-area lighting.
HMI_LED_HOLDER_L         = 150.0  # X length (less than beam 178 mm)
HMI_LED_HOLDER_W         = 14.0   # Y width
HMI_LED_HOLDER_H         = 5.0    # Z thickness
HMI_LED_STRIP_W          = 10.0   # LED strip cavity width
HMI_LED_STRIP_H          = 2.5    # LED strip cavity depth (into bottom face)
HMI_LED_TIE_GROOVE_W     = 4.0    # zip-tie groove width (X)
HMI_LED_TIE_GROOVE_D     = 1.0    # zip-tie groove depth (Z, into top face)
HMI_LED_TIE_X            = 60.0   # zip-tie groove X offset from center

# === Display Tilt Lock V1.0 (Part M10-P06)  -- 2 parts: Base + Arm ===
# Two-plate friction-tilt assembly between Cross Beam and Touchscreen Frame.
# BASE bolts to beam FRONT face; ARM bolts to frame TOP TAB; the two pivot
# around a horizontal X-axis hinge with a single M5 lock thumb screw whose
# travel is constrained by an arc slot.
HMI_TILT_PLATE_W        = 180.0   # both plates share same X
HMI_TILT_PLATE_H        = 70.0    # both plates share same Z
HMI_TILT_PLATE_T        = 5.0     # both plates same Y thickness
HMI_TILT_BEAM_BOLT_Z    = 28.0    # M5 beam-mount holes Z (relative to center)
HMI_TILT_FRAME_BOLT_Z   = 22.0    # M5 frame-mount inserts Z
HMI_TILT_PIVOT_Z        = -25.0   # M5 pivot Z (below center)
HMI_TILT_LOCK_Z         = 0.0     # M5 lock-screw nominal Z (center)
# V1.1: TRUE arc slot centered on the pivot.  The lock bolt traverses an arc
# at constant radius from the pivot, eliminating side-loading of the screw.
HMI_TILT_SLOT_R         = 25.0    # arc center radius (pivot -> lock nominal)
HMI_TILT_SLOT_HALF_W    = 3.0     # slot perpendicular half-width (M5 + clearance)
HMI_TILT_ANGLE_HALF_DEG = 20.0    # +/- angular range from vertical-up
                                    # (40 deg total tilt range)
HMI_TILT_CORNER_R       = 3.0     # plate corner fillet

# === Rear Cable Cover V1.0 (Part M10-P07) ===
# Cosmetic strip that adheres to the beam REAR face, covering the cable
# channel and hiding the HDMI / USB-C / fan-power wire runs.
# Mounting: 3M VHB foam tape on the -Y face (beam-side).  Simple, removable,
# does not require any features on the beam (which is frozen at V1.2 RC1).
HMI_RCC_LEN          = 170.0   # X length (just inside beam X)
HMI_RCC_H            = 20.0    # Z height (wider than 8 mm channel for coverage)
HMI_RCC_T            = 3.0     # Y thickness
HMI_RCC_CORNER_R     = 4.0     # corner fillet (visible from rear)
HMI_RCC_CHAMFER      = 0.6     # bevel on visible edges

# === Cable Clamp V1.0 (Part M10-P08) ===
# Saddle plate that bolts to a 2020 mast slot with one M5 T-nut, holding a
# cable bundle against the mast face via 4 corner zip-tie holes.
HMI_CABLE_CLAMP_W       = 30.0    # plate X (along mast face)
HMI_CABLE_CLAMP_H       = 30.0    # plate Z (vertical)
HMI_CABLE_CLAMP_T       = 8.0     # plate thickness (Y, away from mast)
HMI_CABLE_CLAMP_TIE_D   = 3.0     # zip-tie pass-through hole diameter
HMI_CABLE_CLAMP_TIE_X   = 10.0    # zip-tie hole X offset from center
HMI_CABLE_CLAMP_TIE_Z   = 10.0    # zip-tie hole Z offset from center
HMI_CABLE_CLAMP_CORNER_R = 3.0    # plate corner fillet

# === Pi Fan Cover V1.0 (Part M10-P04) ===
# Flat plate hanging below the Pi 4 (opposite side from Pi Carrier).
# Carries a 30 x 30 x 10 mm 5V fan that blows air toward Pi components.
# Mounts via M2.5 x 25 mm screws stacked through Cover + brass standoff +
# Pi PCB + Pi Carrier insert (replaces the M2.5 x 6 mm screw from Pi Carrier).
HMI_PI_FAN_COVER_W      = 80.0     # plate X (inside Pi 88)
HMI_PI_FAN_COVER_D      = 60.0     # plate Y (matches Pi 58 + margin)
HMI_PI_FAN_COVER_T      = 3.0      # plate thickness
HMI_PI_FAN_OPENING_D    = 24.0     # round air intake (better airflow than 22)
HMI_PI_FAN_BODY_W       = 30.0     # standard 30 x 30 x 10 mm fan
HMI_PI_FAN_BODY_H       = 10.0
HMI_PI_FAN_MOUNT_PCD    = 24.0     # standard 30 mm fan screw spacing
HMI_PI_FAN_M3_CLEAR_D   = 3.7      # M3 clearance (bumped from 3.5 for fan PCD tolerance)
HMI_PI_FAN_STANDOFF_H   = 11.0     # user-supplied M2.5 brass standoff height
                                    # (Pi PCB to Fan Cover; clears 10 mm fan)
HMI_PI_FAN_VOLTAGE      = 5.0      # supplied from Pi GPIO header
HMI_PI_FAN_AIRFLOW      = "TOWARD_PI"  # arrow on fan should point at Pi PCB
HMI_PI_FAN_RIB_W        = 2.0      # stiffening rib width (perpendicular)
HMI_PI_FAN_RIB_H        = 1.5      # stiffening rib height (above top face)
# V1.2 -- slotted grille (replaces single round D24 intake)
HMI_PI_FAN_GRILLE_SLOTS    = 5     # number of parallel slots
HMI_PI_FAN_GRILLE_SLOT_W   = 3.5   # slot width (X)
HMI_PI_FAN_GRILLE_SLOT_H   = 22.0  # slot length (Y)
HMI_PI_FAN_GRILLE_WALL     = 1.6   # wall between slots (>= 4 perimeters at 0.4 mm)
# V1.2 -- additional features
HMI_PI_FAN_CORNER_R        = 3.0   # plate corner fillet radius
HMI_PI_FAN_CABLE_NOTCH_W   = 4.0   # cable exit notch width (X)
HMI_PI_FAN_CABLE_NOTCH_L   = 8.0   # cable exit notch length (X, away from fan)
HMI_PI_FAN_CABLE_NOTCH_D   = 2.0   # cable exit notch depth (Z, into plate top)
HMI_PI_HEATSINK_H_NOMINAL  = 6.0   # typical low-profile Pi 4 heatsink (set to
                                    # 8 for tall heatsinks or 0 for bare PCB)
# V1.3 -- M3 fan screw counterbore (heads flush on bottom face, away from wires)
HMI_PI_FAN_M3_CB_D         = 6.0   # M3 pan-head counterbore diameter
HMI_PI_FAN_M3_CB_H         = 1.5   # counterbore depth (into bottom face)
# V1.3 -- orientation-tolerant cable channels (replaces single corner notch)
HMI_PI_FAN_CABLE_CH_W      = 4.0   # channel width (Y dimension if X-aligned)
HMI_PI_FAN_CABLE_CH_L      = 6.0   # channel length from fan body edge
HMI_PI_FAN_CABLE_CH_D      = 1.5   # depth into plate top

# === Pi Carrier V1.0 (Part M10-P03) ===
# Adapter plate between beam (58 x 28 PCD inserts) and Pi 4 (58 x 49 PCD).
# Hangs from beam bottom face via M5 socket-head bolts going UP into beam
# inserts.  Pi 4 mounts BELOW plate via M2.5 standoffs into self-tap pilots.
HMI_PI_CARRIER_W       = 90.0              # X (along beam direction)
HMI_PI_CARRIER_D       = 60.0              # Y (front-back of machine)
HMI_PI_CARRIER_T       = 8.0               # plate thickness
HMI_PI4_PCD_X          = 58.0              # Pi 4 mount holes, X spread
HMI_PI4_PCD_Y          = 49.0              # Pi 4 mount holes, Y spread
HMI_M2_5_PILOT_D       = 2.0               # M2.5 self-tap pilot hole
HMI_M2_5_PILOT_H       = 6.0
HMI_PI_CABLE_NOTCH_W   = 14.0              # cable cutout, X width
HMI_PI_CABLE_NOTCH_D   = 6.0               # cable cutout, Y depth

# === Boolean / overcut helpers (FDM print engineering convention) ===
# Small offsets used in cuts to avoid coincident faces from Boolean ops.
# Centralized so they read as engineering intent, not magic numbers.
HMI_BOOLEAN_OVERCUT    = 0.1               # extend cut volume past target face
HMI_CUT_EXTRA          = 2.0               # extra length on through-cuts
HMI_CUT_START_OFFSET   = 0.05              # start cut just below target face

# ============================================================
# BOUGHT-PARTS DIMENSIONS (from BOM V12 -- physical inventory)
# Source of truth: 04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html
# ============================================================

# --- Drive shaft + bearings ---
SHAFT_D                = 12.00   # FEYRINX 12mm h8 (B08HX2LG53)
SHAFT_LENGTH           = 300.00  # actually-purchased shaft length
BEARING_6001_OD        = 28.00   # 6001-2RS (eBay 10pk)
BEARING_6001_ID        = 12.00
BEARING_6001_W         =  8.00
BEARING_51101_OD       = 26.00   # 51101 thrust bearings (B0G25X5L23)
BEARING_51101_ID       = 12.00
BEARING_51101_W        =  9.00
BEARING_608_OD         = 22.00   # 608-2RS skate (B0FH6QH8VQ)
BEARING_608_ID         =  8.00
BEARING_608_W          =  7.00
SHAFT_COLLAR_D         = 12.00   # 12mm clamping collars (B0DMMB1FHF)

# --- DRIVE MOTOR: NEMA 23 + 5:1 PLANETARY GEARBOX (23HS22-2804S-HG5) ---
# Source: StepperOnline direct  --  $95
# Bipolar 2.8 A holding ~2.8 N.m before gearbox, ~14 N.m at gearbox output
NEMA23_BODY_W          = 57.00     # NEMA 23 frame, 57x57 square
NEMA23_BODY_L          = 56.00     # 23HS22 = 56 mm body length
NEMA23_SHAFT_D         =  8.00     # input shaft (into gearbox, but motor side has shaft)
NEMA23_MOUNT_PCD_SQ    = 47.14     # 4x M5 square hole pattern (centre to centre)
NEMA23_MOUNT_HOLE_D    =  5.50     # M5 clearance
NEMA23_BOSS_D          = 38.10     # round register boss
NEMA23_BOSS_H          =  1.60
NEMA23_CURRENT_A       =  2.80
NEMA23_HOLDING_NM      =  2.80

# Planetary gearbox (HG5 = 5:1 ratio, attached to motor output)
GEARBOX_RATIO          =  5.0      # HG5
GEARBOX_FLANGE_OD      = 60.00     # typical for NEMA 23 + HG-series planetary
GEARBOX_LENGTH         = 50.00     # planetary gearbox housing length
GEARBOX_OUTPUT_SHAFT_D = 14.00     # output shaft diameter (gearbox)
GEARBOX_OUTPUT_SHAFT_L = 25.00     # output shaft length
GEARBOX_MOUNT_PCD      = 70.00     # output flange mount pattern (M5)

# Drive motor placement (Interface 6 -- physical position on wood base)
# Combined motor + gearbox total length = NEMA23_BODY_L + GEARBOX_LENGTH = 106 mm
#
# R4 CORRECTION: motor moved from (+90, -100) to (+85, -47) so that the
# belt center distance MATCHES the actual purchased 405 mm pitch belt.
# Old MOTOR_X=90, MOTOR_Y=-100 gave distance sqrt(90^2 + 100^2) = 134.54 mm,
# which is 37 mm too far for a 405 mm HTD 5M belt with 60T+20T pulleys.
# Correct center distance derived from belt-length equation: ~97.29 mm
#  (see BELT_CENTER_DISTANCE below for derivation).
MOTOR_X                =  85.0     # world X (+X side, motor side, Interface 6)
MOTOR_Y                = -47.0     # world Y (back-right quadrant per ICD I6)
MOTOR_BODY_BOTTOM_Z    =  18.0     # gearbox-side mounts on wood base top
BELT_TENSION_TRAVEL    =  30.0     # SE5 X-travel slot (allows ~+/- 5 mm
                                    # center distance variation around nominal)

# --- HTD 5M PULLEYS + BELT (from B0C6Y1462P kit: 60T + 20T + 405 mm belt) ---
PULLEY_BIG_TEETH       = 60
PULLEY_BIG_OD          = 97.50     # for HTD 5M @ 60 teeth: pitch dia 95.49, OD~97.5
PULLEY_BIG_BORE        = 14.00     # bored for gearbox output shaft (was 12)
PULLEY_BIG_W           = 16.00
PULLEY_SMALL_TEETH     = 20        # 20T (NOT 16T)
PULLEY_SMALL_OD        = 33.30     # for HTD 5M @ 20 teeth: pitch dia 31.83, OD~33.3
PULLEY_SMALL_BORE      = 12.00     # bored for 12 mm drive shaft (note inversion below)
PULLEY_SMALL_W         = 16.00
BELT_WIDTH             = 15.00     # mm  -- TO VERIFY on receipt (B0C6Y1462P
                                    #     kit variant ships 9 or 15 mm; this
                                    #     constant assumes 15 mm. Verify and
                                    #     fix if 9 mm before locking the
                                    #     motor-mount slot width.)
BELT_THICKNESS         =  3.00
BELT_PITCH_LENGTH      = 405.0     # mm  -- LOCKS center distance (see below)
BELT_PITCH             =   5.0     # HTD 5M

# Belt center distance derivation (HTD 5M, 405 mm pitch, 60T + 20T):
#   Lp = 2C + pi*(D1+D2)/2 + (D1-D2)^2/(4C)
#   D1 = 60*5/pi = 95.493     (60T pitch diameter)
#   D2 = 20*5/pi = 31.831     (20T pitch diameter)
#   Solving:  C = 97.29 mm   (real solution)
# Motor placement MOTOR_X/MOTOR_Y above is chosen to give this center distance.
BELT_CENTER_DISTANCE   = 97.29     # mm  -- LOCKED by belt geometry

# Pulley assignment:
#   60T mounts on GEARBOX output (14 mm bore)
#   20T mounts on 12 mm DRIVE SHAFT
# Three separate reductions chain together:
#   gearbox  =  5:1   (HG5 planetary)
#   belt     =  3:1   (60T : 20T)
#   total    = 15:1   (motor input -> cylinder output)
GEAR_RATIO_GEARBOX     = GEARBOX_RATIO            # 5.0   (defined earlier)
GEAR_RATIO_BELT        = 60.0 / 20.0              # 3.0   (60T : 20T)
GEAR_RATIO_TOTAL       = GEAR_RATIO_GEARBOX * GEAR_RATIO_BELT   # 15.0
# At 250 RPM motor input -> 16.67 RPM cylinder output.

# --- FEEDER MOTORS: MG90S METAL-GEAR SERVOS (NOT stepper motors) ---
# 8x purchased: 6 for feeders F1..F6 + 2 spares
# 9 g micro servo, 4.8-6 V, 2.5-3.0 kg.cm torque, 180 deg PWM
SERVO_MG90S_W          = 22.80    # body width
SERVO_MG90S_D          = 12.20    # body depth
SERVO_MG90S_H          = 28.50    # body height (incl. spline output)
SERVO_MG90S_MOUNT_W    = 32.00    # tab-to-tab including mounting tabs
SERVO_MG90S_MOUNT_HOLES_PITCH = 28.00    # 2x M2 mounting holes pitch
SERVO_MG90S_SHAFT_D    =  4.80    # spline output shaft
SERVO_MG90S_VOLTAGE    =  6.0
SERVO_MG90S_TORQUE_KGCM = 3.0
SERVO_MG90S_BUCK_CONVERTER = "LM2596 (B008BHB4L8) 24V -> 6V"

# --- DRIVE HUB (unchanged -- same 18 mm boss, but now mates to 14 mm shaft via collar) ---
DRIVE_HUB_BOSS_OD      = 18.00
DRIVE_HUB_BOSS_H       =  3.00
DRIVE_HUB_FLANGE_OD    = 90.00
DRIVE_HUB_BOLT_PCD     = 70.00

# --- ELECTRONICS (sit on wood base, Layer 3) ---
# Compute
MEGA_W,  MEGA_D,  MEGA_H   = 101.0, 53.0, 15.0    # Arduino Mega 2560 (B0046AMGW0)
RPI4_W,  RPI4_D,  RPI4_H   =  88.0, 58.0, 19.0    # Raspberry Pi 4 4GB (B07V5JTMV9)
                                                    # Pi handles touchscreen UI; Mega handles steppers

# Stepper driver
TB6600_W, TB6600_D, TB6600_H = 96.0, 56.0, 33.0   # B08SG7L54W

# Power supply (replaces LRS50 in earlier docs)
S250_24_W, S250_24_D, S250_24_H = 199.0, 98.0, 38.0    # Mean Well S-250-24 (B07Y7L664K)

# Touchscreen
TOUCH_W, TOUCH_D, TOUCH_H  = 165.0, 100.0, 10.0   # ELECROW 7" HDMI (B08FMNDDSL)

# --- HALL + INDEX ---
HALL_SENSOR_PART       = "SS49E"
MAGNET_PART            = "B0F4KS6KV3"
MAGNET_POCKET_D        =   6.0
MAGNET_POCKET_H        =   2.2

# --- CYLINDER SPRINGS (V10 NEW, from FlyDesigns) ---
SPRING_WIRE_D          =   2.79   # 0.110 inch music wire
SPRING_QTY_PURCHASED   =   3

# --- ALUMINUM PLATE (purchased B0D9S2KH4V, size TBD-verify) ---
ALU_PLATE_PURCHASED_T  =   6.30   # 1/4 inch nominal = 6.35; ordered 6.3
# (W and D values come from ALU_PLATE_W and ALU_PLATE_D in frame block above)

# ============================================================
# CYLINDER (Cylinder V3.0 specifics)
# ============================================================
CYL_HEIGHT             = 75.0
SLOT_COUNT             = 72
SLOT_PITCH_DEG         = 360.0 / SLOT_COUNT   # 5.0
SLOT_WIDTH             =  1.22
SLOT_DEPTH             =  4.70   # V3.1 LOCKED 2026-05-24 (was 3.00 in V3.0)
                                  # Physical WEDGE_B V2 test result: slot 7 = best
SPRING_GROOVE_DEPTH    =  3.10   # V3.1 LOCKED (was 1.30 in V3.0)
                                  # Coupled to SLOT_DEPTH for +0.20 mm preload
                                  # Spring recessed 0.31 mm below OD (no cam ring interference)
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
