CSM V3 - NEMA 23 MOTOR MOUNT V1.2 (STRUCTURAL UPGRADE)
========================================================
Date: April 2026

Macro: CSM_V3_MotorMount_V1_2.FCMacro

V1.2 STRUCTURAL CHANGES FROM V1.1:

ACCEPTED FROM REVIEW (with modifications):
  1. PLATE_T 8mm -> 10mm
     Industrial-safe thickness. ~3x flex resistance increase via cube-of-thickness rule.
  
  2. FOOT_T 8mm -> 10mm
     Provides 4.5mm of material below 5.5mm bolt head pockets (was 2.5mm).
     Eliminates bolt-head crushing risk. Heads still sit FLUSH.
  
  3. RIB_BASE 6mm: ribs embedded INTO plate (not line-contact)
     Stress flows through bulk material, not concentrated at single edge.
     Matches the 10mm plate thickness with 4mm of plate behind rib root.

REJECTED FROM REVIEW:
  - Reduce FOOT_SLOT_HEAD_H 5.5 -> 4.5mm.
    With 8mm foot, this would leave bolt head 1.5mm PROUD (worse than before).
    Better fix is to thicken foot, which we did.
  - Reviewer's V1.2 macro replacement.
    Their version lost SVG/PNG export and chamfer logic.
    My V1.2 keeps all V1.1 features and only modifies what needs fixing.

==========================================
COST vs BENEFIT
==========================================
Cost: +60g extra material, +30 minutes print time
Benefit:
  - 3x more flex resistance (10mm vs 8mm plate)
  - 80% more material below bolt heads (4.5 vs 2.5mm)
  - Stress no longer concentrated at single edge (rib embedding)
  - Production-grade rigidity for 1.5kg motor + belt tension load

==========================================
ALL V1.1 FEATURES PRESERVED
==========================================
- 6mm rib thickness (cube-of-thickness rule applied)
- 11mm counterbores for M5 washer fit
- 60mm Y rail spacing (matches 420x320 base layout)
- 30mm slot length (belt tension 82-112mm range)
- 4 slots (resists motor torque pivot)
- Motor bolt direction (heads on outside, threads INTO gearbox)
- Chamfer logic (bounding-box filter)
- SVG blueprint export
- PNG view export
- Console output with full assembly procedure
- Frame layout documentation

==========================================
FRAME LAYOUT (your 420x320x18mm base)
==========================================

Mount 2x 2020 aluminum extrusions ON TOP of wood base, parallel:

       420mm long (X axis)
   <-------------------------->
   +--------------------------+
   |                          |
   |      Rail 2 (Y=+30)      |  ^
   |   ====================   |  |
   |                          |  |
   |   [bracket span 100mm]   |  | 320mm wide
   |                          |  | (Y axis)
   |   ====================   |  |
   |      Rail 1 (Y=-30)      |  |
   |                          |  v
   +--------------------------+
   <- 18mm thick hardwood base ->

==========================================
HARDWARE NEEDED (ALL ALREADY OWNED)
==========================================
- 4x M5 SHCS ~16mm (motor face mounting)
- 4x M5 SHCS ~12mm + 4x M5 T-nuts (foot)
- 4-8x M5 washers (under SHCS heads, prevents PETG creep)
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
Print time:   ~3.5 hours (was 3 hours in V1.1)
Material:     ~210g PETG (was 150g in V1.1)

==========================================
ASSEMBLY SEQUENCE
==========================================
1. Print bracket V1.2
2. Cut 2x 2020 extrusions to length (~400mm each)
3. Mount extrusions to wood base at +/-30mm Y spacing
4. Slide T-nuts into rail top slots
5. Place bracket on rails, loose-tighten foot bolts (with washers)
6. Mount NEMA 23 + gearbox to plate via 4x M5 SHCS (with washers)
   Torque: 4-6 Nm
7. Install 20T HTD pulley on gearbox output shaft
8. Wrap HTD 5M belt around 20T motor pulley + 60T cassette pulley
9. Slide bracket AWAY from cassette to apply belt tension
10. Adjust tension: belt deflects ~5mm at midpoint with 1kg force
11. Tighten foot bolts to lock bracket position (3-4 Nm)

==========================================
VALIDATION TESTS (after install)
==========================================
1. Verify 20T pulley installed on gearbox output (set screw to keyway)
2. Verify belt routes correctly around both pulleys
3. Belt deflection test: 5mm midpoint deflection with 1kg force
4. Power motor briefly - smooth rotation, no squeal
5. Run 30 RPM for 10 minutes - check for vibration, heat, click
6. Check bracket for visible flex under load (none expected with 10mm)

==========================================
WHY THIS COMPLETES THE DRIVE SYSTEM
==========================================
- Motor + gearbox properly mounted with rigid bracket
- Belt geometry verified at correct center distance
- Cassette can spin under motor power
- First chance to test V2.4 preload under DYNAMIC load
- If any clicks or vibration appear, indicates issues with:
  * V2.4 spacer tube length (preload wrong)
  * Belt tension (too tight/loose)
  * Drive hub clamp not gripping shaft

This V1.2 should be print-it-once and forget about it.
