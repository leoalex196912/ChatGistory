CSM V3 - V2.4 DETERMINISTIC PRELOAD DELIVERY
==============================================
Date: April 2026

CONTENTS:

1. 01_MECHANICAL/05_BEARINGS_SHAFT/freecad_macros/
   CSM_V3_BearingHousings_V2_4.FCMacro
   -> Run in FreeCAD to generate 4 STL files:
      - CSM_V3_BearingHousing_TOP_V2_4.stl
      - CSM_V3_BearingHousing_BOTTOM_V2_4.stl
      - CSM_V3_BearingHousings_PAIR_V2_4.stl (assembly view)
      - CSM_V3_SpacerTube_V2_4.stl (NEW for V2.4)

2. 04_PURCHASING/
   BOM_Reconciliation_V8.html
   -> Open in browser for complete shopping status

=========================================
V2.4 PHILOSOPHY SHIFT
=========================================
V2.3: Preload = manual collar tightening at Z=59mm
V2.4: Preload = geometric (built into spacer tube length)

V2.4 is how industrial machines work:
- CNC spindles
- Lonati knitting heads
- Precision gearboxes

The spacer tube on the shaft holds the bearing inner races at exactly
the right distance to compress the wave spring by 0.5mm. The result
is ~30N constant preload regardless of how tight the collars are.

Top collar role changes from "preload setter" to "retention only."

=========================================
V2.4 CHANGES FROM V2.3
=========================================
1. NEW PART: Spacer tube
   - 12.2mm ID (slip on 12mm shaft)
   - 18mm OD (clears bearing OD)
   - 29.40mm long (PRELOAD CRITICAL)
   - +/- 0.05mm tolerance

2. Wave spring pocket: 1.2mm -> 1.4mm (safety margin)

3. Block gap LOCKED at 11mm
   (6mm aluminum plate + 5mm assembly clearance)

4. Top collar: light clamp only (no longer creates preload)

=========================================
CRITICAL DIMENSION
=========================================
SPACER TUBE LENGTH: 29.40mm

If tubes are too long: insufficient preload, click/rattle
If tubes are too short: excessive preload, drag/heat

Tuning range with shims: 29.20 - 29.60mm
No reprint needed - just add 0.1mm shims to adjust.

=========================================
HARDWARE SHOPPING (~$25-30 total)
=========================================
Already own (from V2.3 plans):
- Loctite 603 Retaining Compound
- Koyo AS1226 thrust washers
- 6001-2RS bearings, 51101 thrust bearing
- Clamping shaft collars (12mm)

To order from McMaster-Carr (~$20):
- Wave spring: 12mm ID x 25mm OD x 0.45mm, 17-7PH stainless
- Spacer ring: 12mm ID x 18mm OD x 2mm, 18-8 stainless

To make/buy spacer tube:
- Option A: 3D print PETG (free, prototype only)
- Option B: Cut aluminum tube to 29.40mm (~$5-15, recommended)
- Option C: Ground steel tube (~$15-30, elite)

=========================================
SPACER TUBE PRINT NOTES (if using PETG)
=========================================
Settings:
- Layer height: 0.1mm (precision)
- Perimeters: 8 (rigidity)
- Infill: 100% (solid)
- Orientation: vertical (length axis = Z)
- Speed: 30mm/s (slower for accuracy)
- Supports: NONE

Verify length after print with calipers (NEIKO 01407A).
Should be 29.40mm +/- 0.05mm.
If off, adjust in slicer's Z-scaling and reprint.

=========================================
V2.4 ASSEMBLY (SIMPLIFIED)
=========================================
1. Print all 3 STLs
2. Apply Loctite 603 to bearing pockets, install bearings, cure 24h
3. Stack into bottom block:
   lower washers -> thrust bearing -> upper washers
   -> wave spring -> spacer ring
4. Install radial bearings in both blocks (Loctite, cure 24h)
5. Mount blocks on aluminum plate (verify 11mm BLOCK_GAP)
6. Install bottom shaft collar at Z=-2mm
7. Insert shaft through bottom block
8. SLIDE SPACER TUBE onto shaft (sits on bottom inner race)
9. Lower top block onto shaft (top bearing slides down onto spacer)
10. Install top shaft collar - LIGHTLY clamp (retention only)

Done. No preload tuning step needed.

=========================================
TEST PROTOCOL
=========================================
Test 1: Rotation - smooth, slight resistance OK
Test 2: Axial play - pull shaft, ZERO movement allowed
Test 3: Drag - if sticky, spacer too short (-0.1mm shim)
Test 4: Click - if click, spacer too long (shorten or shim)
Test 5: Runout - dial indicator <0.2mm TIR at shaft end

=========================================
TUNING (NO REPRINT NEEDED)
=========================================
Too loose (click/play): add 0.1mm shim BELOW lower washer
                        (raises spring, increases compression)
Too tight (drag): add 0.1mm shim ABOVE spacer ring
                  (lowers spring, decreases compression)

McMaster-Carr "metric round shim 12mm 18mm" pack of 10
in various thicknesses (0.1, 0.2, 0.3mm) ~$10 covers all
tuning needs forever.
