CSM V3 - NEMA 23 MOTOR MOUNT V1.0
====================================
Date: April 2026

Macro: CSM_V3_MotorMount_V1_0.FCMacro

VERSIONING:
This is V1.0 - the FIRST motor mount design.
Independent version counter per project policy.
Future iterations will be V1.1, V1.2, etc.

PURPOSE:
L-bracket holding NEMA 23 + 5:1 gearbox to 2020 frame.
Belt tension via sliding foot in extrusion channel.

GEOMETRY:
- Motor face plate: 100x100x8mm with NEMA 23 mount pattern
- Foot: 100x50x8mm with 4x slotted M5 holes
- 3x triangular reinforcement ribs at L-corner
- Bounding box: 108 x 100 x 100mm

BELT GEOMETRY (verified):
- 60T HTD 5M cassette pulley (PD 95.49mm)
- 20T HTD 5M motor pulley (PD 31.83mm)
- Belt: 405mm length, 9mm wide
- Calculated nominal center distance: 97.3mm
- Slot adjustment range: 30mm = center distance 82-112mm

HARDWARE - ALL ALREADY OWNED:
- 4x M5 SHCS ~16mm (motor face mounting)
- 4x M5 SHCS ~12mm (foot to T-nut)
- 4x M5 T-nuts for 2020 extrusion
All from existing B0FFSNFK3Y assortment + B0GG4N5GR4 T-nuts.

NO NEW ORDERS REQUIRED.

PRINT SETTINGS:
- PETG, 0.2mm layer, 5 perimeters
- 50% Gyroid infill
- Orient FOOT FACE DOWN on bed
- Supports may be needed under ribs (60deg threshold)
- Estimated print time: 3 hours
- Estimated material: ~150g PETG

INTEGRATION WITH FRAME:
- Bracket bolts to 2020 extrusion via T-nuts
- Slots align with belt tension direction (axis between motor and cassette)
- Slide whole bracket to adjust tension, retighten bolts

VALIDATION TESTS (after install):
1. Verify 20T pulley installed on gearbox output (set screw)
2. Verify belt routes correctly around both pulleys
3. Belt deflection test: 5mm midpoint deflection with 1kg force = correct tension
4. Power motor briefly - smooth rotation, no squeal
5. Run 30 RPM for 10 minutes - check for vibration, heat, click

THIS PART COMPLETES THE DRIVE SYSTEM.
After this, you can test the full motor -> belt -> cassette chain.

NEXT CAD WORK (after this is printed/tested):
- Cassette base V1.0 (if you want to start cassette parts)
- Cylinder R3+ (waiting on needle measurements)
- Yarn guide arm (Phase 4)
