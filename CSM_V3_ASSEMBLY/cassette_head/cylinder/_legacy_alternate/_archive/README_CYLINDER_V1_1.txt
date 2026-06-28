CSM V3 - CYLINDER V1.1 (with cylinder spring groove)
======================================================
Date: April 2026

CHANGES FROM V1.0:
  Added circumferential spring groove around cylinder OD:
    - Width: 3.0mm axial (for 0.110" / 2.79mm wire + 0.21mm clearance)
    - Depth: 1.5mm radial (spring half-recessed)
    - Position: Z=19.0 to Z=22.0mm
                (centered at 20.5mm, 1mm below slot bottom)

  Spring engages needle butts at their resting position.
  When cam lifts needle, butt rises through spring zone.
  Spring stretches, providing return force when cam releases.

SPRING SPEC (FlyDesigns Common Thickness):
  Wire: 0.110 inch / 2.79mm steel wire
  Function: Wraps around cylinder OD
  Order 3 from FlyDesigns ($18 + shipping)
  Request OPEN/STRAIGHT shipment for sizing flexibility

CRITICAL DIMENSIONS (LOCKED):
  Cylinder OD:        114.3mm (Legare 4.5" standard)
  Cylinder ID:        88.0mm
  Height:             75mm
  Slot count:         72
  Slot W x D:         1.22 x 1.90mm rectangular
  Slot length:        52mm axial (Z=23 to Z=75)
  Slot top chamfer:   0.4mm lead-in
  Wall between slots: 3.77mm (excellent for PETG)
  Butt cavity:        8.5 x 4.0mm at Z=19-23
  Hub pocket:         D18.20 x 3mm + 0.5mm chamfer
  Bolt pattern:       4x M5 @ PCD 70mm
  Spring groove:      W3.0 x D1.5mm at Z=19-22

OUTPUTS:
  1. Full 72-slot cylinder (CSM_V3_Cylinder_V1_1_FULL.stl)
  2. 30 deg test wedge (CSM_V3_Cylinder_V1_1_TESTWEDGE.stl)
     - Tests 3 slot widths: 1.20 / 1.22 / 1.25mm
     - Includes spring groove for full validation
  3. Top + side blueprint (Cylinder_V1_1_Blueprint.svg)

==========================================
TEST WEDGE STRATEGY (PRINT FIRST!)
==========================================

The test wedge validates BOTH:
  1. Slot fit (3 slot widths to test)
  2. Spring groove fit (when springs arrive)

PHASE 1 - Print test wedge (don't wait for springs)
  Print: CSM_V3_Cylinder_V1_1_TESTWEDGE.stl
  Time: 30-45 minutes
  Material: ~12g PETG
  
  Test now:
    - Insert needle in each slot pair (1.20/1.22/1.25 mm)
    - Verify slide motion is smooth
    - Pick winning slot width
    - Measure groove with caliper (should be ~2.9mm wide after PETG shrink)

PHASE 2 - When springs arrive
  Test:
    - Try fitting a length of spring wire into the groove
    - Should sit in groove with ~half wire diameter exposed
    - If too tight: file groove slightly OR adjust SPRING_GROOVE_W
    - If too loose: re-print with reduced groove width

PHASE 3 - Full cylinder
  Once both slot AND groove are validated:
    - Edit SLOT_WIDTH if needed (1.22 default)
    - Edit SPRING_GROOVE_W if needed (3.0 default)
    - Regenerate full cylinder STL
    - Print full cylinder (4-6 hours, ~120g PETG)

==========================================
PRINT SETTINGS (PETG)
==========================================
  Material:      PETG (DRY filament)
  Layer height:  0.2mm
  Perimeters:    5
  Top/bottom:    6 solid layers
  Infill:        40% Gyroid or Cubic
  Orientation:   Cylinder UPRIGHT (axis Z)
  Supports:      NONE (slots and groove are vertical/horizontal)
  Speed:         40mm/s walls, 120mm/s infill
  Cooling:       Fan ON
  Bed adhesion:  Brim or skirt

==========================================
ASSEMBLY ORDER (with spring)
==========================================
1. Apply Loctite 603 to M5 bolt threads
2. Place cylinder onto Drive Hub V1.3 (boss enters pocket)
3. Insert 4 M5 bolts through cylinder counterbores into hub
4. Tighten cross-pattern to ~5 Nm
5. Wait 24h for Loctite cure
6. Insert all 72 needles from TOP of cylinder
7. Wrap cylinder spring around the OD groove:
   - Open/straight spring goes around cylinder
   - Twist ends together to close loop
   - Spring should sit in groove, ~half exposed
   - Should provide light radial pressure on needle butts
8. Verify all 72 needles slide freely with spring engaged
9. Spin cylinder by hand - should rotate smoothly

==========================================
HARDWARE STATUS
==========================================

ALREADY HAVE:
  - PETG filament
  - 4x M5 bolts (via screw assortment kit B0FFSNFK3Y)
  - Loctite 603 (B0074NALBO)
  - 100x Legare 12g needles (FlyDesigns)

TO ORDER:
  - 3x Cylinder Springs Common Thickness (FlyDesigns, $18 + ship)
    * Order with note: "Please ship OPEN/STRAIGHT for sizing"

==========================================
NEXT STEPS AFTER CYLINDER
==========================================

Phase 1 (this delivery): Cylinder V1.1
Phase 2 (next): Sinker Ring V1.0 (72 sinkers + 6 yarn windows + taper)
Phase 3 (next): Cam Ring V6 (V5 with bore change to ID 115mm)
Phase 4 (next): Retainer Ring V1.0 (PA12, 6 yarn cutouts)
Phase 5 (next): Cassette Base V1.0 (200mm OD, 6 feeder mount pads)
Phase 6 (later): Feeder Module V1.0 (mechanical + servo-ready)
Phase 7 (later): Yarn Mast V1.0 (2-cone start, expandable to 6)

ESTIMATED PROJECT TIMELINE:
  Phase 1: Done (cylinder design)
  Phase 2-5: ~2-3 weeks design + print
  Phase 6-7: ~2-4 weeks (after spring arrives)
  Total to first knit: 6-8 weeks
