# MACHINE_DATUMS.md — CSM V3 Dimensional Reference

```
Revision:  R5
Date:      2026-05-24
Status:    Active — all macros must reference these constants.
           R5 locks SLOT_DEPTH and SPRING_GROOVE_DEPTH to production
           values derived from physical Phase-1 testing. Cylinder
           bumped V3.0 → V3.1.
```

This is the **single source of truth for all dimensional constants**
used across the CSM V3 project: cylinder-local datum planes, key
interface diameters, bolt patterns, frame geometry, and bought-parts
dimensions.

**Coordinate convention authority** has moved to a sister document:
`MACHINE_COORDINATE_SYSTEM.md` (R1). That doc defines the world frame,
the cylinder-local frame, and the `CYL_BOTTOM_WORLD_Z = 181 mm`
transform. This document focuses on **what things measure**, not where
they sit in world space.

Every machine-component macro MUST:
1. Reference these values by name (e.g. `CAM_DATUM_Z`), never by raw number
2. Copy the relevant constants block verbatim into its parameter section
3. Update this document FIRST when any datum changes, then sync macros
4. Follow `MACHINE_COORDINATE_SYSTEM.md` for any world-coordinate placement

---

## Cylinder-Local Z Datum Planes

All Z values below are **cylinder-local** (Z=0 at cylinder bottom face,
where it sits on the drive hub boss). To convert to world Z, add
`CYL_BOTTOM_WORLD_Z = 181.0` (see `MACHINE_COORDINATE_SYSTEM.md`).

```python
# ============================================================
# CYLINDER-LOCAL DATUMS  (copy verbatim into every cassette macro)
# ============================================================
CYLINDER_Z0          =  0.0    # cylinder bottom (= drive hub boss top)
CAM_DATUM_Z          = 49.0    # cam ring top / cassette base bottom
CASSETTE_TOP_Z       = 63.0    # outer disc top of cassette base
SINKER_Z             = 75.0    # sinker register plane (assembly reference)
CYLINDER_TOP_Z       = 75.0    # cylinder top face (geometry reference)
                                # Same numerical value as SINKER_Z but
                                # semantically distinct. Future variants
                                # may decouple them — keep both names.
FEEDER_REFERENCE_Z   = 90.0    # nominal feeder finger height
                                # CHANGED from R1 (was 78). Raised to
                                # match retainer/sinker geometry. Final
                                # value validated in Phase 1.5
                                # (kinematic motion study).
HOOK_PEAK_Z          = 83.0    # needle hook position at peak cam lift
                                # (cylinder top Z=75 + 8mm cam lift)
                                # Equal to retainer ring bottom plane
                                # in world coords (264 mm). Kinematic
                                # boundary — affects retainer lip
                                # clearance, feeder approach angle,
                                # ribber timing, knock-over geometry.
```

### Cylinder-local visualization

```
              Z=91  ─── retainer ring top (geometry-derived)
              Z=90  ─── FEEDER REFERENCE  (validated in Phase 1.5)
              Z=83  ─── HOOK PEAK         (= retainer bottom = world 264)
                         (yarn caught here, just above cylinder top)
              Z=75  ─── SINKER PLANE / CYLINDER TOP
                         (sinker ring sits here, cylinder top face)
              Z=63  ─── CASSETTE BASE TOP (outer disc upper surface)
              Z=49  ─── CAM DATUM (cam ring top / cassette base bottom)
                         (= world Z 230 = aluminum plate top
                          = MASTER DATUM for the whole machine)
              Z=19..31 ── cam track engagement (butt zone)
              Z=0   ─── CYLINDER BOTTOM (drive hub interface)
```

### World-Z mapping (derived from local datums + CYL_BOTTOM_WORLD_Z = 181)

**Semantic note:** `CAM_DATUM_Z` (cylinder-local) and `ALU_PLATE_TOP_Z`
(world) are **physically coincident** at world Z = 230 mm in the
nominal assembly — but they are **not the same datum**. The cassette's
local frame ends at `CAM_DATUM_Z`; the machine's master datum is
`ALU_PLATE_TOP_Z`. Any future shim/spacer between cassette bottom and
plate top will offset these two without violating either definition.

| Physical interface plane | Cylinder-local Z | World Z | Notes |
|---|---:|---:|---|
| CYLINDER_Z0 (cylinder bottom face) | 0 | 181 | drive hub boss interface |
| Cam track top engagement | 31 | 212 | upper limit of butt travel |
| **CAM_DATUM_Z** (cam ring top = cassette base bottom) | 49 | 230 | local datum, coincident with master datum below |
| **ALU_PLATE_TOP_Z** (machine master datum plane) | — | **230** | world reference, cassette mounts here |
| CASSETTE_TOP_Z (outer disc top) | 63 | 244 | cassette base outer-disc top face |
| SINKER_Z / CYLINDER_TOP_Z | 75 | 256 | numerically equal, semantically distinct |
| HOOK_PEAK_Z | 83 | 264 | = retainer bottom plane |
| FEEDER_REFERENCE_Z | 90 | 271 | provisional; Phase 1.5 validates |
| Retainer top (macro-derived, RR_THICK = 8 mm) | 91 | 272 | per Retainer Ring V1.0 geometry |

`RETAINER_ASSEMBLY_OFFSET_Z = 0` in nominal assembly. Any future Z
shim between retainer and cassette is recorded by raising this value
in the assembly script — not by editing the retainer macro.

---

## Derived Values (DO NOT EDIT DIRECTLY)

These values are **computed** from the primary constants above. If
the primary value changes, the derived value updates automatically.
Hard-coding a derived value as a literal in a macro is a bug.

```python
# ============================================================
# DERIVED VALUES -- computed from primary constants. Read-only.
# ============================================================

# --- Cassette / cylinder kinematics ---
HOOK_LIFT             = HOOK_PEAK_Z - CYLINDER_TOP_Z      # = 8.0 mm  (cam stroke)
CASSETTE_DISC_THICK   = CASSETTE_TOP_Z - CAM_DATUM_Z      # = 14.0 mm (cassette outer disc)
SINKER_TO_HOOK_GAP    = HOOK_PEAK_Z - SINKER_Z            # = 8.0 mm  (yarn catch window)
FEEDER_ABOVE_HOOK     = FEEDER_REFERENCE_Z - HOOK_PEAK_Z  # = 7.0 mm  (yarn drop distance, provisional)

# --- Frame Z stack ---
UPRIGHT_BOT_Z         = WOOD_BASE_TOP_Z                    # = 18.0
UPRIGHT_TOP_Z         = UPRIGHT_BOT_Z + UPRIGHT_LEN        # = 206.0
UPPER_DECK_BOTTOM_Z   = UPRIGHT_TOP_Z                      # = 206.0
UPPER_DECK_TOP_Z      = UPPER_DECK_BOTTOM_Z + UPPER_DECK_T # = 224.0
ALU_PLATE_BOTTOM_Z    = UPPER_DECK_TOP_Z                   # = 224.0
ALU_PLATE_TOP_Z       = ALU_PLATE_BOTTOM_Z + ALU_PLATE_T   # = 230.0 (master datum)
CYL_BOTTOM_WORLD_Z    = ALU_PLATE_TOP_Z - CAM_DATUM_Z      # = 181.0 (= the transform constant)

# --- Service envelope SE5 derived geometry ---
BELT_TENSION_X_RANGE  = (MOTOR_X - BELT_TENSION_TRAVEL, MOTOR_X)   # = (60, 90)
                       # motor shall be free to translate in this X range
                       # for belt tension + removal (see SERVICE_ENVELOPES.md)
```

Build-time invariant: `CYL_BOTTOM_WORLD_Z` from the derived block
MUST equal the constant defined in `MACHINE_COORDINATE_SYSTEM.md`
(181.0). If frame Z stack ever changes such that the two diverge,
either the frame Z stack is wrong or the coordinate system constant
is wrong — fix the cause, not the symptom.

---

## Angular Phase Reference (θ = 0°)

```
═══════════════════════════════════════════════════════════════
θ = 0° MACHINE PHASE REFERENCE
═══════════════════════════════════════════════════════════════
  - Cylinder slot #0 aligned with +X axis (motor side)
  - Hall sensor index magnet at PCD 95 on bottom face,
    at angular position 0° (Cylinder V3.0 geometry)
  - Hall sensor index pulse occurs once per cylinder revolution
    when slot #0 crosses the sensor
  - All feeder timing, future pattern control, ribber sync, and
    heel/toe sequencing reference this phase origin
  - Rotation direction: CCW looking from +Z (standard knitting)
```

This is **foundational** for Phase 1.5 kinematic validation and all
subsequent automation. Changing θ = 0° alignment is a breaking
architectural change requiring an ICD revision bump.

---

## Cassette Geometry (cylindrical / rotational centerlines)

All concentric on the cylinder Z axis (world X=Y=0).

| Feature | Diameter (mm) | Notes |
|---|---:|---|
| Cylinder OD | 114.30 | Legare 4.5" standard (LOCKED ICD invariant #1) |
| Cylinder ID (bore) | 88.00 | sock take-down passage |
| Slot bottom (radial) | 107.50 | OD − 2 × slot_depth (3.0 mm) |
| Cam Ring ID | 115.00 | 0.35 mm/side clearance to cylinder OD |
| Cam Ring OD | 165.00 | locked per Cam Ring V6.5 |
| Cassette Base center hole | 117.00 | 1.35 mm total clearance |
| Sinker Pedestal ID | 128.00 | annular pedestal inner edge |
| Sinker Pedestal OD | 150.00 | annular pedestal outer edge |
| Sinker register pocket | 135.30 | sinker OD 135 + 0.3 slip fit |
| Sinker Ring OD | 135.00 | mates with register pocket |
| Sinker Ring ID | 115.30 | 0.5 mm/side clearance to cylinder OD |
| Cassette Base OD | 200.00 | structural foundation |
| Retainer Ring OD | 200.00 | matches cassette base OD |
| Retainer Ring through-bore | 118.00 | cylinder OD 114.3 + 1.85 mm radial clearance |
| Retainer loop-control lip ID | 104.00 | effective loop aperture |

---

## Bolt Patterns (PCD = Pitch Circle Diameter)

| Pattern | PCD (mm) | Count | Fastener | Angular offset (deg) | Purpose |
|---|---:|---:|---|---|---|
| Cam ring bolts | 155.0 | 6 | M5 | 30, 90, 150, 210, 270, 330 | Cassette base ↔ Cam Ring (ICD invariant #2) |
| Cam ring pins | 145.0 | 6 | D4 dowels | 0, 60, 120, 180, 240, 300 | Cam Ring rotational registration (ICD invariant #3) |
| Feeder mounts | 190.0 | 6 | M4 | 0, 60, 120, 180, 240, 300 | Feeder modules + retainer ring (ICD invariant #4) |
| Frame mounts | 180.0 | 4 | M5 | 45, 135, 225, 315 | Cassette base ↔ aluminum plate (ICD invariant #5) |
| Ribber mounts | 140.0 | 6 | M4 | 0, 60, 120, 180, 240, 300 | Phase 2 (provisioned, unused in Phase 1) |
| Cylinder ↔ Drive Hub | 70.0 | 4 | M5 (heat-set inserts) | 45, 135, 225, 315 | Cylinder bottom ring ↔ Drive Hub V2.4.2 |
| Hall index magnet | 95.0 | 1 | D6 magnet | 0 | Aligned with Slot #0 (= +X axis, motor side) |

---

## Frame Geometry (NEW for R2 — three-layer architecture)

The structural frame is now **isolated** from the precision knitting
core. Frame dimensions are world coordinates (Z = 0 at wood base
bottom = rubber-feet contact plane).

**XY origin:** all frame coordinates below are measured from the
**cylinder rotation axis** projected onto Z = 0 (i.e. `FRAME_ORIGIN_XY
= (0.0, 0.0)`). The wood base is centered on the cylinder axis;
corner positions are at (±W/2, ±D/2). This is **not** a "wood base
corner = origin" convention.

```python
# ============================================================
# FRAME (world coordinates -- origin at cylinder axis projected to Z=0)
# ============================================================
FRAME_ORIGIN_XY       = (0.0, 0.0)   # cylinder axis / machine centerline
                                      # all X, Y values below are signed
                                      # offsets from this point.


# Wood base (the only large wood piece)
WOOD_BASE_W           = 500.0     # X
WOOD_BASE_D           = 400.0     # Y
WOOD_BASE_T           =  18.0     # Z thickness
WOOD_BASE_BOTTOM_Z    =   0.0     # world (rubber feet contact)
WOOD_BASE_TOP_Z       =  18.0
TAKEDOWN_HOLE_D       = 100.0     # center through-hole for sock take-down

# 4× 2020 aluminum uprights (precision frame -- supports upper deck)
UPRIGHT_W             =  20.0     # cross-section width (20×20 mm)
UPRIGHT_LEN           = 188.0     # length
UPRIGHT_BOT_Z         =  18.0     # = wood base top
UPRIGHT_TOP_Z         = 206.0
UPRIGHT_X_POSITIONS   = (+150.0, -150.0)
UPRIGHT_Y_POSITIONS   = (+120.0, -120.0)
                                   # 4 uprights at corners ±150, ±120
                                   # — clustered around cassette
                                   # footprint, NOT the wood base corners

# Wood upper deck (sits on uprights)
UPPER_DECK_W          = 320.0     # X
UPPER_DECK_D          = 260.0     # Y
UPPER_DECK_T          =  18.0
UPPER_DECK_BOTTOM_Z   = 206.0     # = top of uprights
UPPER_DECK_TOP_Z      = 224.0

# Aluminum master-datum plate (sits on wood upper deck)
ALU_PLATE_W           = 250.0     # X
ALU_PLATE_D           = 250.0     # Y
ALU_PLATE_T           =   6.0
ALU_PLATE_BOTTOM_Z    = 224.0
ALU_PLATE_TOP_Z       = 230.0     # = world Z of cassette base bottom
                                   #   = world_z(CAM_DATUM_Z)
                                   #   = MASTER DATUM PLANE (ICD invariant #8)
ALU_PLATE_MATERIAL    = "6061-T6 mill finish"

# Touchscreen mast (dual 2020 + crossbar, isolated from precision frame)
MAST_UPRIGHT_LEN      = 400.0
MAST_CENTER_X         =   0.0
MAST_CENTER_Y         = -180.0    # at rear edge of wood base (Y=-200 minus margin)
MAST_X_OFFSETS        = (+30.0, -30.0)  # two parallel uprights at X = ±30 from mast center
MAST_TOP_CROSSBAR_LEN =  60.0
MAST_TOP_Z            = 418.0     # = WOOD_BASE_TOP_Z + MAST_UPRIGHT_LEN
```

---

## Bought-Parts Dimensions (R3 BOM-aligned)

Constants for purchased components used in assembly placement, clearance
checking, and Blender render geometry.

**Source of truth: `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`** (the
physical inventory). R3 corrects the R2 errors where the docs assumed
NEMA 17 drive motor + NEMA 11 feeder steppers — the actual purchases are
**NEMA 23 + 5:1 planetary gearbox** for drive and **MG90S metal-gear
servos** for feeders.

```python
# ============================================================
# DRIVE SHAFT + BEARINGS  (in inventory)
# ============================================================
SHAFT_D                 = 12.00      # FEYRINX 12 mm h8 (B08HX2LG53)
SHAFT_LENGTH            = 300.00     # actually-purchased
BEARING_6001_OD         = 28.00      # 6001-2RS radial (eBay 10pk)
BEARING_6001_ID         = 12.00
BEARING_6001_W          =  8.00
BEARING_51101_OD        = 26.00      # 51101 thrust (B0G25X5L23)
BEARING_51101_ID        = 12.00
BEARING_51101_W         =  9.00
BEARING_608_OD          = 22.00      # 608-2RS skate (B0FH6QH8VQ)
BEARING_608_ID          =  8.00
BEARING_608_W           =  7.00
SHAFT_COLLAR_D          = 12.00      # clamping collars (B0DMMB1FHF)

# ============================================================
# DRIVE MOTOR: NEMA 23 + 5:1 PLANETARY GEARBOX
# Part: StepperOnline 23HS22-2804S-HG5  ($95)
# Bipolar 2.8 A, 2.8 N.m holding before gearbox → ~14 N.m at output
# ============================================================
NEMA23_BODY_W           = 57.00      # NEMA 23 = 57×57 mm square frame
NEMA23_BODY_L           = 56.00      # 23HS22 = 56 mm body length
NEMA23_SHAFT_D          =  8.00      # input shaft (motor side)
NEMA23_MOUNT_PCD_SQ     = 47.14      # 4× M5 square hole pattern, centre-to-centre
NEMA23_MOUNT_HOLE_D     =  5.50      # M5 clearance
NEMA23_BOSS_D           = 38.10      # round register boss on output face
NEMA23_BOSS_H           =  1.60
NEMA23_CURRENT_A        =  2.80      # under TB6600 4 A rating (good)
NEMA23_HOLDING_NM       =  2.80

GEARBOX_RATIO           =  5.0       # HG5 planetary
GEARBOX_FLANGE_OD       = 60.00      # typical HG-series for NEMA 23
GEARBOX_LENGTH          = 50.00      # housing length
GEARBOX_OUTPUT_SHAFT_D  = 14.00      # output shaft (D-cut or keyed)
GEARBOX_OUTPUT_SHAFT_L  = 25.00
GEARBOX_MOUNT_PCD       = 70.00      # output-flange mount pattern (M5)

# Total drive assembly length = NEMA23_BODY_L + GEARBOX_LENGTH = 106 mm

# ============================================================
# HTD 5M PULLEYS + BELT  (kit B0C6Y1462P: 60T + 20T + 405 mm belt)
# ============================================================
PULLEY_BIG_TEETH        = 60         # mounts on GEARBOX output (14 mm bore)
PULLEY_BIG_OD           = 97.50      # pitch dia 95.493, OD ~97.5
PULLEY_BIG_BORE         = 14.00      # = GEARBOX_OUTPUT_SHAFT_D
PULLEY_BIG_W            = 16.00
PULLEY_SMALL_TEETH      = 20         # mounts on 12 mm DRIVE SHAFT  (NOT 16T as R2 had)
PULLEY_SMALL_OD         = 33.30      # pitch dia 31.831, OD ~33.3
PULLEY_SMALL_BORE       = 12.00      # = SHAFT_D
PULLEY_SMALL_W          = 16.00
BELT_WIDTH              = 15.00      # mm  -- TO VERIFY on receipt (kit
                                      # B0C6Y1462P ships 9 mm or 15 mm
                                      # variants; verify and update if 9)
BELT_THICKNESS          =  3.00
BELT_PITCH              =  5.00      # HTD 5M
BELT_PITCH_LENGTH       = 405.0      # mm  -- LOCKS center distance below
# Three drivetrain ratios chained:
GEAR_RATIO_GEARBOX      = GEARBOX_RATIO         # = 5:1   (HG5 planetary)
GEAR_RATIO_BELT         = 60.0 / 20.0           # = 3:1   (60T : 20T)
GEAR_RATIO_TOTAL        = GEAR_RATIO_GEARBOX * GEAR_RATIO_BELT   # = 15:1
# At motor 250 RPM input -> cylinder 16.67 RPM output.

# Belt-geometry derivation (HTD 5M, 405 mm pitch, 60T + 20T):
#   Lp = 2C + π·(D1+D2)/2 + (D1−D2)²/(4C)
#   D1 = 60·5/π = 95.493    (60T pitch diameter)
#   D2 = 20·5/π = 31.831    (20T pitch diameter)
#   Solve for C → 97.29 mm  (real solution)
BELT_CENTER_DISTANCE    = 97.29      # mm  -- LOCKED by belt geometry

# Drive motor placement on wood base (back-right per ICD R3 Interface 6).
# Motor position chosen so distance from drive shaft axis (0,0) to motor
# axis = BELT_CENTER_DISTANCE = 97.29 mm.
# R4 correction: was (90, -100) = 134.54 mm distance (would not fit belt).
MOTOR_X                 =  85.0      # world X (+X side = motor side)
MOTOR_Y                 = -47.0      # world Y (back-right quadrant)
                                      # sqrt(85² + 47²) = 97.13 mm ≈ 97.29
MOTOR_BODY_BOTTOM_Z     =  18.0      # = WOOD_BASE_TOP_Z
BELT_TENSION_TRAVEL     =  30.0      # mm motor X-travel slot for SE5
                                      # (allows ±5 mm center distance trim)

# ============================================================
# FEEDER ACTUATORS: MG90S METAL-GEAR SERVOS (NOT NEMA 11 steppers)
# 8× purchased: 6 for feeders F1..F6 + 2 spares
# 9 g micro servo, 4.8-6 V, 2.5-3.0 kg.cm, 180 deg PWM
# ============================================================
SERVO_MG90S_W           = 22.80      # body width
SERVO_MG90S_D           = 12.20      # body depth
SERVO_MG90S_H           = 28.50      # body height (incl. spline output)
SERVO_MG90S_MOUNT_W     = 32.00      # tab-to-tab including mounting tabs
SERVO_MG90S_MOUNT_HOLES_PITCH = 28.00    # 2× M2 mounting holes pitch
SERVO_MG90S_SHAFT_D     =  4.80      # spline output shaft
SERVO_MG90S_VOLTAGE     =  6.0       # via LM2596 buck converter from 24 V
SERVO_MG90S_TORQUE_KGCM =  3.0
SERVO_MG90S_BUCK_CONVERTER = "LM2596 (B008BHB4L8) 24V -> 6V"

# ============================================================
# DRIVE HUB (locked V2.4.2 -- unchanged, fits 12 mm shaft via collar)
# ============================================================
DRIVE_HUB_BOSS_OD       = 18.00      # mates with cylinder D18.2 pocket
DRIVE_HUB_BOSS_H        =  3.00
DRIVE_HUB_FLANGE_OD     = 90.00
DRIVE_HUB_BOLT_PCD      = 70.00      # matches cylinder PCD 70 + 45° offset

# ============================================================
# ELECTRONICS (Layer 3, sit on wood base)
# ============================================================
# Compute
MEGA_W,   MEGA_D,   MEGA_H   = 101.0, 53.0, 15.0    # Arduino Mega 2560 (B0046AMGW0) -- stepper control
RPI4_W,   RPI4_D,   RPI4_H   =  88.0, 58.0, 19.0    # Raspberry Pi 4 4GB (B07V5JTMV9) -- touchscreen UI

# Stepper driver
TB6600_W, TB6600_D, TB6600_H = 96.0, 56.0, 33.0     # B08SG7L54W, 4 A

# Power supply (replaces R2 LRS-50 -- actual purchase is S-250-24)
S250_24_W, S250_24_D, S250_24_H = 199.0, 98.0, 38.0  # Mean Well S-250-24 (B07Y7L664K) 24 V 10 A

# Servo power: 24 V from S-250 -> LM2596 buck -> 6 V to MG90S servos
LM2596_W, LM2596_D, LM2596_H = 43.0, 21.0, 13.0      # B008BHB4L8 buck module

# ============================================================
# TOUCHSCREEN DISPLAY (purchased)
# ============================================================
TOUCH_W                 = 165.0      # ELECROW 7" HDMI capacitive (B08FMNDDSL)
TOUCH_D                 = 100.0
TOUCH_H                 =  10.0

# ============================================================
# HALL SENSOR + INDEX MAGNET (purchased)
# ============================================================
HALL_SENSOR_PART        = "SS49E"    # linear Hall, B09MSDC3GR
MAGNET_PART             = "B0F4KS6KV3"   # N52 D6×2.0 mm neodymium
MAGNET_POCKET_D         =   6.0
MAGNET_POCKET_H         =   2.2      # 2.0 mm magnet + 0.2 mm epoxy bed

# ============================================================
# CYLINDER SPRINGS (V10 NEW, from FlyDesigns)
# ============================================================
SPRING_WIRE_D           =   2.79     # 0.110" music wire
SPRING_QTY_PURCHASED    =   3        # ordered open/straight for sizing flexibility
```

---

## Materials by Component (with progression flags)

Architecture is **frame-locked, polymer-flexible**: the geometry is
fixed; the material may evolve from PETG prototype → PA12 functional
→ 6061 production without re-architecting.

| Component | Phase 1 (PETG) | Phase 2 (PA12) | Phase 3 (6061 / steel) |
|---|---|---|---|
| Cylinder | ✓ | ✓ (PA12-CF preferred for wear) | machined 6061 |
| Cam Ring | ✓ | ✓ | anodized 6061 |
| Sinker Ring | ✓ | ✓ (recommended) | PA12 retained (low load) |
| **Retainer Ring** | ✓ **PA12 recommended from start** (sliding wear) | ✓ | PA12 retained |
| Cassette Base | ✓ | ✓ | 6061 (precision interface) |
| Drive Hub | ✓ | n/a | machined 6061 |
| Motor Mount | ✓ | ✓ | 6061 |
| Bearing Housings | ✓ | ✓ | 6061 |
| Feeder Modules | ✓ (housing for MG90S servo) | ✓ | PA12 retained (cost) |
| Wood Base | hardwood (walnut/maple) | unchanged | unchanged |
| Wood Upper Deck | hardwood | unchanged | unchanged |
| Aluminum Plate | **6061 from V1** (master datum, not a print) | unchanged | unchanged |
| 2020 Uprights | aluminum extrusion | unchanged | unchanged |
| Touchscreen Mast | aluminum extrusion | unchanged | unchanged |

Material flag in each macro:
```python
MATERIAL = "PETG"    # or "PA12" or "AL6061" / "STEEL"
# Tolerance settings vary by material (slot clearance, insert holes,
# root fillets). One macro source file, three material targets.
```

---

## Locked Versions As of R2

| Component | Version | Macro file |
|---|---|---|
| Cylinder | V3.0 | `02_CASSETTE_HEAD/cylinder/freecad_macros/CSM_V3_Cylinder_V3_0.FCMacro` |
| Cam Ring | V6.5 (FINAL) | `02_CASSETTE_HEAD/cam_ring/freecad_macros/CSM_V3_CamRing_V6_5.FCMacro` |
| Sinker Ring | V1.2.1 (LOCKED) | `02_CASSETTE_HEAD/sinker_ring/freecad_macros/CSM_V3_SinkerRing_V1_2_1.FCMacro` |
| Cassette Base | V1.1 | `02_CASSETTE_HEAD/cassette_base/freecad_macros/CSM_V3_CassetteBase_V1_1.FCMacro` |
| Drive Hub | V2.4.2 (Done) | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_DriveHub_V2_4_2.FCMacro` |
| Motor Mount | V1.3 (Done) | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_MotorMount_V1_3.FCMacro` |
| Bearing Housings | V2.5 (Done) | `05_BEARINGS_SHAFT/freecad_macros/CSM_V3_BearingHousings_V2_5.FCMacro` |
| Retainer Ring | V1.0 (LOCKED) | `02_CASSETTE_HEAD/retainer_ring/freecad_macros/CSM_V3_RetainerRing_V1_0.FCMacro` |
| Wood Base | V1.0 | `CSM_V3_ASSEMBLY/frame/wood_base/freecad_macros/CSM_V3_WoodBase_V1_0.FCMacro` (needs V1.1 for D100 hole) |
| Wood Upper Deck | **NOT YET** | to build at `CSM_V3_ASSEMBLY/frame/wood_upper_deck/` |
| Mount Plate (aluminum) | V1.0 (150×150) | needs V1.1 resize to 250×250 |
| 2020 Upright | V1.0 (267 mm) | needs V1.1 shorten to 188 mm + reposition |
| Touchscreen Mast | **NOT YET** | to build at `CSM_V3_ASSEMBLY/frame/touchscreen_mast/` |
| Feeder Module | **NOT YET** | to build at `CSM_V3_ASSEMBLY/feeder_module/` |
| Yarn Cone (decorative) | V1.0 (existing) | mount on feeder, not loose |
| Ribber (Phase 2) | provisioned only | future |

---

## Revision History

| Rev | Date | Author | Changes |
|---|---|---|---|
| R1 | 2026-05-17 | leoalex196912 | Initial datums document. Captured cylinder-local datums + interfaces from existing committed macros. |
| R2 | 2026-05-20 | leoalex196912 | (a) Demote coord-convention ownership to new `MACHINE_COORDINATE_SYSTEM.md`; (b) Add world-Z mapping for cassette datums; (c) FEEDER_REFERENCE_Z 78→90 (provisional, validated in Phase 1.5); (d) Three-layer frame architecture: wood base 500×400×18 with D100 center hole + 4× 2020 uprights (188 mm, at ±150 ±120) + wood upper deck 320×260×18 + aluminum plate 250×250×6 as master datum; (e) Delete wood mid-shelf 500×400 (was wrong, didn't match poster); (f) Add dual-upright touchscreen mast at (0, −180); (g) NEW bought-parts dimensions section (NEMA 11 for feeders, electronics, touchscreen, HTD pulleys/belt, Hall sensor); (h) Material progression flags per component; (i) Refresh locked versions table with new frame components. |
| R2 final | 2026-05-20 | leoalex196912 | Pre-lock refinements per architectural review: (1) Disambiguated CAM_DATUM_Z (local) vs ALU_PLATE_TOP_Z (world master datum) — they are coincident but not the same datum; (2) Clarified retainer top derivation from macro geometry (world Z 272) and added RETAINER_ASSEMBLY_OFFSET_Z placeholder for future shimming; (3) Explicit `FRAME_ORIGIN_XY = (0, 0)` statement in frame section; (4) Added `BELT_CENTER_DISTANCE = 134.5` mm + `BELT_TENSION_TRAVEL = 30` mm for service envelope SE5; (5) NEW "Derived Values" section separating primary constants from computed ones; (6) Elevated θ=0° angular phase reference to its own dedicated section. R2 now formally locked. |
| R3 | 2026-05-22 | leoalex196912 | **BOM ALIGNMENT.** Discovered R2 specified wrong actuators vs. the actual BOM V11 physical inventory. Corrections: (a) Drive motor: NEMA 17 → **NEMA 23 + 5:1 planetary gearbox (23HS22-2804S-HG5)**. Body 57×57×56 mm, M5 mount PCD 47.14, output shaft 14 mm via HG5 gearbox. (b) Feeder actuators: NEMA 11 steppers → **MG90S metal-gear servos** (8 purchased: 6 active + 2 spare). 9 g 180° PWM. (c) Pulley kit: HTD 5M 60T+16T → actual purchase is **60T+20T+405mm belt** (B0C6Y1462P). New belt reduction 3:1; total motor→cylinder reduction = 5×3 = **15:1**. (d) Big pulley bore: 12 mm → 14 mm (gearbox output). (e) PSU: LRS-50 → **Mean Well S-250-24** (199×98×38 mm). (f) Added Raspberry Pi 4 4GB constants (Pi handles UI, Mega handles steppers). (g) Added secondary bearings (51101 thrust, 608-2RS), shaft collars. (h) Added LM2596 buck converter constants (24V→6V for servos). (i) Added cylinder spring constants (FlyDesigns 0.110" wire, 3 purchased). Source of truth declared: `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`. |
| R4 | 2026-05-24 | leoalex196912 | **BELT GEOMETRY CORRECTION.** R3 had MOTOR_X=90, MOTOR_Y=-100 → distance √(8100+10000) = 134.54 mm from drive shaft axis. This is **impossible** for the purchased 405 mm pitch HTD 5M belt with 60T + 20T pulleys. Correct center distance derived from belt-length equation `Lp = 2C + π(D1+D2)/2 + (D1−D2)²/(4C)` with D1=95.493, D2=31.831, Lp=405 → **C = 97.29 mm**. Motor repositioned to (X=+85, Y=−47) giving distance 97.13 mm ≈ 97.29 mm. (b) Added `BELT_CENTER_DISTANCE = 97.29` constant. (c) Separated three drivetrain ratios as named constants: `GEAR_RATIO_GEARBOX = 5`, `GEAR_RATIO_BELT = 3`, `GEAR_RATIO_TOTAL = 15`. (d) Flagged `BELT_WIDTH = 15.00` as TO-VERIFY (BOM kit B0C6Y1462P ships 9 mm or 15 mm variants — verify on physical receipt). Canonical poster v2 (`CSM_V3_CANONICAL_POSTER_V2`) adopted concurrently. |
| R5 | 2026-05-24 | leoalex196912 | **SLOT_DEPTH + SPRING_GROOVE_DEPTH LOCKED TO PHYSICAL TEST RESULT.** Phase-1 WEDGE_B V2 (10-slot fine sweep 3.50–5.30 mm at 0.20 mm steps) printed + tested with 12g FlyDesigns needles. Result: **slot 7 (4.70 mm depth, 3.10 mm groove) = BEST retention**, slot 6 (4.50 mm) = acceptable tie, slot 8 (4.90 mm) = loose. Lock: `SLOT_DEPTH = 4.70` (was 3.00), `SPRING_GROOVE_DEPTH = 3.10` (was 1.30). Both preserve +0.20 mm spring preload on needle stem. Mechanical consequences: (a) spring is now RECESSED 0.31 mm below cylinder OD (was protruding 1.49 mm in V3.0) → no risk of cam ring interference (cam ID 115, cylinder OD 114.3, 0.35 mm/side clearance preserved); (b) wall remaining at slot bottom = 8.45 mm (plenty of structural material). Cylinder version bumped **V3.0 → V3.1**. V3.0 STLs archived in `01_MECHANICAL/02_CASSETTE_HEAD/cylinder/_archive/v3_0_locked_2026-05-19/`. ICD R6 locked-versions table updated inline (no ICD revision bump — architecture unchanged, only implementation version). |

---

## Cross-References

- **Coordinate authority:** `MACHINE_COORDINATE_SYSTEM.md` (R1)
- **Interface control:** `INTERFACE_CONTROL.md` (R3 — in progress)
- **Service envelopes:** `SERVICE_ENVELOPES.md` (next deliverable)
- **Project overview:** `~/.claude/projects/C--3D-Project/memory/project_csm_v3_overview.md`
- **BOM:** `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`
