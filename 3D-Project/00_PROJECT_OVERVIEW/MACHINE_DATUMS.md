# MACHINE_DATUMS.md — CSM V3 Master Coordinate Reference

```
Revision:  R1
Date:      2026-05-17
Status:    Active — all macros must reference these constants
```

This is the **single source of truth** for all global machine coordinates,
key interface dimensions, and datum planes used across the CSM V3 project.

Every machine-component macro MUST:
1. Reference these values by name (e.g. `CAM_DATUM_Z`), never by raw number
2. Copy the constants block verbatim into the macro's parameter section
3. Update this document FIRST when any datum changes, then sync all macros

---

## Coordinate Convention

```
+Z      = upward along the cylinder axis (from cylinder bottom)
+R      = radial outward from the cylinder axis
theta 0° = machine front / Hall sensor reference (cylinder slot #0)
```

All linear units are millimeters (mm).
All angular units are degrees.

---

## Global Z Datum Planes

All Z values are measured in **cylinder local coordinates**, with `Z=0` at
the cylinder bottom face (where it sits on the drive hub boss).

```python
# ============================================================
# MACHINE DATUMS  (copy verbatim into every component macro)
# ============================================================
CYLINDER_Z0          =  0.0    # cylinder bottom
CAM_DATUM_Z          = 49.0    # cam ring top / cassette base bottom
CASSETTE_TOP_Z       = 63.0    # outer disc top of cassette base
SINKER_Z             = 75.0    # sinker register plane (assembly reference)
CYLINDER_TOP_Z       = 75.0    # cylinder top face (geometry reference)
                                # Same numerical value as SINKER_Z but
                                # semantically distinct. Future variants
                                # may decouple them — keep both names.
FEEDER_REFERENCE_Z   = 78.0    # nominal feeder finger height
HOOK_PEAK_Z          = 83.0    # needle hook position at peak cam lift
                                # (cylinder Z=75 + 8mm cam lift)
                                # Kinematic boundary — affects retainer
                                # lip clearance, feeder approach angle,
                                # ribber timing, knock-over geometry.
```

### Visualization

```
              Z=83  ─── needle HOOK PEAK (peak cam lift)
                         (yarn caught here, just above cylinder top)
              Z=78  ─── FEEDER REFERENCE (yarn entry plane)
              Z=75  ─── SINKER PLANE / CYLINDER TOP
                         (sinker ring sits here, cylinder top face)
              Z=63  ─── CASSETTE BASE TOP (outer disc upper surface)
              Z=49  ─── CAM DATUM (cam ring top / cassette base bottom)
                         (cam track engages butts at Z=19-31 below this)
              Z=0   ─── CYLINDER BOTTOM (drive hub interface)
```

---

## Key Interface Dimensions

### Cylindrical / Rotational Centerlines

All concentric on the cylinder Z axis.

| Feature | Diameter (mm) | Notes |
|---|---|---|
| Cylinder OD | 114.30 | Legare 4.5" standard |
| Cylinder ID (bore) | 88.00 | sock take-down passage |
| Slot bottom (radial) | 107.50 | OD - 2× slot_depth (3.0mm) |
| Cam Ring ID | 115.00 | 0.35mm/side clearance to cylinder OD |
| Cam Ring OD | 165.00 | locked per Cam Ring V6.5 |
| Cassette Base center hole | 117.00 | 1.35mm total clearance |
| Sinker Pedestal ID | 128.00 | annular pedestal inner edge |
| Sinker Pedestal OD | 150.00 | annular pedestal outer edge |
| Sinker register pocket | 135.30 | sinker OD 135 + 0.3 slip fit |
| Sinker Ring OD | 135.00 | mates with register pocket |
| Sinker Ring ID | 115.30 | 0.5mm/side clearance to cylinder OD |
| Cassette Base OD | 200.00 | structural foundation |

### Bolt Patterns (PCD = Pitch Circle Diameter)

| Pattern | PCD (mm) | Count | Fastener | Angular offset (deg) | Purpose |
|---|---|---|---|---|---|
| Cam ring bolts | 155.0 | 6 | M5 | 30, 90, 150, 210, 270, 330 | Cassette base ↔ Cam Ring |
| Cam ring pins | 145.0 | 6 | D4 dowels | 0, 60, 120, 180, 240, 300 | Cam Ring rotational registration |
| Feeder mounts | 190.0 | 6 | M4 | 0, 60, 120, 180, 240, 300 | Feeder modules (shared by Retainer Ring) |
| Frame mounts | 180.0 | 4 | M5 | 45, 135, 225, 315 | Cassette base ↔ wood mid-shelf (via Al plate) |
| Ribber mounts | 140.0 | 6 | M4 | 0, 60, 120, 180, 240, 300 | Phase 2 (provisioned, unused in Phase 1) |
| Cylinder ↔ Drive Hub | 70.0 | 4 | M5 (heat-set inserts) | 45, 135, 225, 315 | Cylinder bottom ring ↔ Drive Hub V2.4.2 |
| Hall index magnet | 95.0 | 1 | D6 magnet | 0 | Aligned with Slot #0 (master index) |

### Cassette Base / Frame Mounting

```
Aluminum plate footprint:  150 × 150 × 6 mm (6061 aluminum)
Wood mid-shelf:            500 × 400 × 18 mm  (hardwood)
Wood base:                 500 × 400 × 18 mm  (hardwood)
2020 frame uprights:       20 × 20mm extrusions, 4× at corners
```

---

## Materials by Component

| Component | Prototype | Production |
|---|---|---|
| Cylinder | PETG | PA12-CF or 6061 aluminum |
| Cam Ring | PETG | 6061 anodized aluminum |
| Sinker Ring | PETG | PA12 nylon |
| **Retainer Ring** | **PA12 nylon** (Phase 1) | PA12 nylon |
| Cassette Base | PETG | PA12 or 6061 aluminum |
| Drive Hub | PETG | machined aluminum |
| Motor Mount | PETG | unchanged |
| Bearing Housings | PETG | unchanged |
| Feeder Modules | PETG | PETG or PA12 |
| Yarn Mast | PETG | 2020 aluminum extrusion |

The Retainer Ring is the **only Phase 1 prototype where PA12 is recommended
upfront** because it's a sliding-wear surface (yarn loops scrape against it).

---

## Drive System (separate coordinate reference)

The drive components live BELOW the cylinder. Their reference frame is
the 12mm shaft. Mating to the cylinder happens via the Drive Hub V2.4.2
boss (D18 × 3mm) into the cylinder's bottom hub pocket.

```
SHAFT_D              = 12.00   (FEYRINX h8)
BEARING_OD           = 28.00   (6001-2RS)
BEARING_W            =  8.00
DRIVE_HUB_BOSS_OD    = 18.00   (mates with cylinder D18.2 pocket)
DRIVE_HUB_BOSS_H     =  3.00
DRIVE_HUB_FLANGE_OD  = 90.00
DRIVE_HUB_BOLT_PCD   = 70.00   (matches cylinder PCD 70 + 45° offset)
PULLEY_TEETH         = 60     (HTD 5M, drives cylinder)
MOTOR_PULLEY_TEETH   = 16
GEAR_RATIO           = 60/16 = 3.75
```

---

## Revision History

| Rev | Date | Author | Changes |
|---|---|---|---|
| R1 | 2026-05-17 | leoalex196912 | Initial document. Captures all locked datums + interfaces from existing committed macros (Cylinder V3.0, Cam Ring V6.5, Sinker Ring V1.2.1, Cassette Base V1.1, Drive Hub V2.4.2, Bearing Housings V2.5). |

---

## Cross-References

- **Interface Control:** see `INTERFACE_CONTROL.md` (sister document — every
  PCD, every dowel, every register diameter with mating-part traceability)
- **Project Overview:** `~/.claude/projects/C--3D-Project/memory/project_csm_v3_overview.md`
- **BOM:** `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`
