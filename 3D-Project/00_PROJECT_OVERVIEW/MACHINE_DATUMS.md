# MACHINE_DATUMS.md — CSM V3 Dimensional Reference

```
Revision:  R2
Date:      2026-05-20
Status:    Active — all macros must reference these constants
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

| Cylinder-local plane | Local Z (mm) | World Z (mm) |
|---|---:|---:|
| CYLINDER_Z0 | 0 | 181 |
| Cam track top engagement | 31 | 212 |
| CAM_DATUM_Z (= master datum plane) | 49 | 230 |
| CASSETTE_TOP_Z | 63 | 244 |
| SINKER_Z / CYLINDER_TOP_Z | 75 | 256 |
| HOOK_PEAK_Z | 83 | 264 |
| FEEDER_REFERENCE_Z | 90 | 271 |
| Retainer top | ~91 | ~272 |

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

```python
# ============================================================
# FRAME (world coordinates)
# ============================================================

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

## Bought-Parts Dimensions (NEW section)

Constants for purchased components used in assembly placement,
clearance checking, and Blender render geometry. Source: vendor
datasheets, BOM_V11.

```python
# ============================================================
# DRIVE COMPONENTS (purchased)
# ============================================================
SHAFT_D                 =  12.00     # FEYRINX h8 steel shaft
SHAFT_LENGTH            = 150.00     # approx -- final cut to fit
BEARING_6001_OD         =  28.00     # 6001-2RS bearing outer race
BEARING_6001_ID         =  12.00     # = SHAFT_D
BEARING_6001_W          =   8.00     # axial width

NEMA17_BODY_W           =  42.30     # 42×42×40 mm class
NEMA17_BODY_L           =  40.00
NEMA17_SHAFT_D          =   5.00
NEMA17_SHAFT_L          =  24.00
NEMA17_MOUNT_PCD        =  31.00     # 4× M3
NEMA17_BOSS_D           =  22.00     # round boss in front of body
NEMA17_BOSS_H           =   2.00

# Drive hub (FreeCAD macro V2.4.2)
DRIVE_HUB_BOSS_OD       =  18.00     # mates with cylinder D18.2 pocket
DRIVE_HUB_BOSS_H        =   3.00
DRIVE_HUB_FLANGE_OD     =  90.00
DRIVE_HUB_BOLT_PCD      =  70.00     # matches cylinder PCD 70 + 45° offset

# HTD 5M timing belt + pulleys
PULLEY_BIG_TEETH        =  60        # on drive shaft (cylinder side)
PULLEY_BIG_OD           =  97.50
PULLEY_BIG_BORE         =  12.00     # = SHAFT_D
PULLEY_BIG_W            =  16.00     # axial width including flange
PULLEY_SMALL_TEETH      =  16        # on NEMA 17 motor shaft
PULLEY_SMALL_OD         =  27.40
PULLEY_SMALL_BORE       =   5.00     # = NEMA17_SHAFT_D
PULLEY_SMALL_W          =  16.00
GEAR_RATIO              =  60.0 / 16.0   # = 3.75 (motor → cylinder)
BELT_WIDTH              =  15.00
BELT_THICKNESS          =   3.00

# Motor placement on wood base (back-right per ICD Interface 6 locked)
MOTOR_X                 =  90.0      # world X (motor side, +X axis)
MOTOR_Y                 = -100.0     # world Y (back, -Y axis)
MOTOR_BODY_BOTTOM_Z     =  18.0      # sits on wood base top

# ============================================================
# FEEDER MOTORS (purchased — for Phase 1 feeder modules)
# ============================================================
NEMA11_BODY_W           =  28.0      # 28×28×32 mm class
NEMA11_BODY_L           =  32.0
NEMA11_SHAFT_D          =   5.0      # standard variant; hollow optional
NEMA11_SHAFT_L          =  20.0
NEMA11_MOUNT_PCD        =  23.0      # 4× M2.5

# ============================================================
# ELECTRONICS (purchased)
# ============================================================
MEGA_W                  = 101.0      # Arduino Mega 2560 PCB
MEGA_D                  =  53.0
MEGA_H                  =  15.0      # incl. through-hole headers
TB6600_W                =  96.0      # stepper driver enclosure
TB6600_D                =  56.0
TB6600_H                =  33.0      # incl. heatsink fins
LRS50_W                 =  99.0      # Mean Well LRS-50-24 PSU
LRS50_D                 =  82.0
LRS50_H                 =  30.0

# ============================================================
# DISPLAY (purchased)
# ============================================================
TOUCH_W                 = 165.0      # 7" HDMI capacitive touchscreen
TOUCH_D                 = 100.0
TOUCH_H                 =  10.0      # active panel depth

# ============================================================
# HALL SENSOR + MAGNET (purchased)
# ============================================================
HALL_SENSOR_PART        = "SS49E"    # linear Hall, B09MSDC3GR
MAGNET_PART             = "B0F4KS6KV3"   # N52 D6×2.0 mm neodymium
MAGNET_POCKET_D         =   6.0
MAGNET_POCKET_H         =   2.2      # 2.0 mm magnet + 0.2 mm epoxy bed
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
| Feeder Modules | ✓ | ✓ | PA12 retained (cost) |
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

---

## Cross-References

- **Coordinate authority:** `MACHINE_COORDINATE_SYSTEM.md` (R1)
- **Interface control:** `INTERFACE_CONTROL.md` (R3 — in progress)
- **Service envelopes:** `SERVICE_ENVELOPES.md` (next deliverable)
- **Project overview:** `~/.claude/projects/C--3D-Project/memory/project_csm_v3_overview.md`
- **BOM:** `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`
