CSM V3 - NEMA 23 MOTOR MOUNT V1.3 (DURABILITY REFINEMENT)
============================================================
Date: April 2026

Macro: CSM_V3_MotorMount_V1_3.FCMacro

V1.3 CHANGES FROM V1.2:

CHANGE 1: FOOT_SLOT_HEAD_H 5.5 -> 5.0mm
  Material below head pocket increases from 4.5mm to 5.0mm
  Bolt heads sit ~1mm proud of foot top (acceptable - top face has no
  mating part above it, and proud heads are easier to grip during
  tension adjustment).

CHANGE 2: NEW slot-end relief geometry
  Added 0.8mm chamfered relief at TWO critical Z heights per slot:
    1. Foot bottom face (Z = -10mm)
       - This is where T-nut bears against slot edge under load
       - Highest stress location during belt tension
       - Chamfer flares DOWNWARD (out of bottom face)
    2. Head pocket transition (Z = -5mm)
       - Geometry step from D5.5 through-hole to D11.0 head pocket
       - Bolt shank loads slot wall at this transition
       - Chamfer flares UPWARD (into head pocket)

  Both chamfers are at the SLOT END semicircles (where bolt presses).
  Reduces crack initiation under repeated tightening cycles.

  Implementation note: V1.3 introduces a new helper function
  add_slot_end_relief() that handles direction (up/down) explicitly.
  This is more reliable than makeFillet on complex fused geometry.

REJECTED FROM REVIEW (4 points):
  - L-corner fillet via makeFillet (filter too broad - would catch
    slot edges, counterbore edges, foot perimeter; makeFillet fragile)
  - Shift rib base another 2mm (diminishing returns)
  - CHAMFER_SIZE 1.0 -> 0.6mm (chamfers not in load path; no benefit)
  - "Rotate so ribs grow upward" (already correct with foot DOWN)

ALL V1.2 + V1.1 FEATURES PRESERVED:
  - 10mm plate/foot thickness
  - 6mm rib thickness with 6mm embedded base
  - 11mm counterbores for M5 washer fit
  - 60mm Y rail spacing (matches 420x320 base)
  - Chamfer logic, SVG export, PNG export, frame layout docs

==========================================
COST vs BENEFIT
==========================================
Cost: Negligible (~5g extra material, ~5 minutes print time)
Benefit:
  - Reduced crack initiation at slot ends under cyclic load
  - Longer service life under repeated belt tension adjustments
  - Smoother bolt shank engagement during tension cycles

==========================================
FRAME LAYOUT (your 420x320x18mm base)
==========================================

       420mm long (X axis)
   <-------------------------->
   +--------------------------+
   |                          |
   |      Rail 2 (Y=+30)      |  ^
   |   ====================   |  |
   |                          |  |
   |   [bracket span 100mm]   |  | 320mm
   |                          |  | wide
   |   ====================   |  | (Y axis)
   |      Rail 1 (Y=-30)      |  |
   |                          |  v
   +--------------------------+
   <- 18mm thick hardwood base ->

==========================================
HARDWARE NEEDED (ALL ALREADY OWNED)
==========================================
- 4x M5 SHCS ~16mm (motor face mounting)
- 4x M5 SHCS ~12mm + 4x M5 T-nuts (foot)
- 8x M5 washers (4 motor + 4 foot, prevents PETG creep)
All from B0FFSNFK3Y assortment + B0GG4N5GR4 T-nuts.
NO NEW ORDERS REQUIRED.

==========================================
PRINT SETTINGS
==========================================
Material:     PETG (DRY)
Layer:        0.2mm
Perimeters:   5
Top/bottom:   6 solid layers
Infill:       50% Gyroid
Orientation:  foot face DOWN on bed
Supports:     YES, under ribs (60deg overhang threshold)
Speed:        40mm/s walls, 100mm/s infill
Print time:   ~3.5 hours
Material:     ~210g PETG

VERIFICATION AFTER PRINT:
1. Check slot end relief is visible (subtle chamfer at slot ends)
2. Test M5 SHCS + washer fit in counterbores
3. Verify foot underside is smooth (sliding face)
4. Inspect ribs - no layer separation at L-corner

==========================================
ASSEMBLY SEQUENCE
==========================================
1. Print bracket V1.3
2. Cut 2x 2020 extrusions to length (~400mm each)
3. Mount extrusions to wood base at +/-30mm Y spacing
4. Slide 4x M5 T-nuts into rail top slots
5. Place bracket on rails, loose-tighten foot bolts (with washers)
6. Mount NEMA 23 + gearbox to plate via 4x M5 SHCS (with washers)
   Torque: 4-6 Nm
7. Install 20T HTD pulley on gearbox output shaft
8. Wrap HTD 5M belt around 20T motor pulley + 60T cassette pulley
9. Slide bracket AWAY from cassette to apply belt tension
10. Tension target: 5mm belt deflection at midpoint with 1kg force
11. Tighten foot bolts to lock bracket position (3-4 Nm)

==========================================
COMPLETE DRIVE SYSTEM STATUS
==========================================
With V1.3, the entire drive subsystem is design-locked:
- Cam ring V5
- Bearing housings V2.4 (top + bottom)
- Spacer tube V2.4
- Drive hub V1.3
- Motor mount V1.3 (THIS PART)

Ready to print and validate the full motor-to-cassette chain.
