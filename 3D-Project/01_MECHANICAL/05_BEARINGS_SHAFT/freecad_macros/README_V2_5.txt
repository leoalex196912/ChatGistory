CSM V3 - BEARING HOUSINGS V2.5 (REAL CATALOG SPRING)
=======================================================
Date: April 2026

Macro: CSM_V3_BearingHousings_V2_5.FCMacro

V2.5 PHILOSOPHY SHIFT:
V2.4 used a theoretical custom wave spring (12 ID x 25 OD x 0.45mm) that
turned out to NOT be a real catalog part. V2.5 uses Smalley CM25-L1, a
real off-the-shelf wave spring with verified specs.

This is mechanically SUPERIOR to V2.4:
- V2.4 (snap-flat 0.45mm): 0.1mm tube tolerance = 20-50% preload swing
- V2.5 (CM25-L1 + tube):    0.1mm tube tolerance = ~3% preload swing
V2.5 is 5-15x more tolerant of manufacturing variations.

V2.5 CHANGES FROM V2.4:
1. Spring spec: theoretical -> Smalley CM25-L1 (real catalog part)
   - Bore: 25mm | Shaft clear: 19mm
   - Free height: 6.63mm | Work height: 2.06mm (50N max)
   - Spring rate: 10.94 N/mm | Material: 17-7 stainless | 3 turns
   - Source: smalley.com (free samples available!)

2. Spring pocket: D26.3 x 1.4mm -> D25.7 x 5.5mm
   Accommodates the much taller CM25-L1 spring.
   0.5mm lead-in chamfer at top edge for assembly.

3. Spacer washer: 12 ID x 18 OD x 2mm -> 19 ID x 28 OD x 1.6mm
   Source: McMaster-Carr (search "metric flat washer 19mm ID 28mm OD")
   OR call McMaster at 630-833-0300 for exact part match.

4. Spacer pocket: D26.3 x 2.0mm -> D28.10 x 1.6mm
   Now matches bearing pocket diameter (cleaner stack).

5. Spacer tube length: 29.40mm -> 22.9mm
   New length accounts for deeper spring pocket and new compression target.

6. Preload target: 30N -> 35N
   - Compression: 3.20mm
   - Operating height: 3.43mm
   - Margin to 50N max: 1.37mm (70% of max load)
   - Better damping, sustainable long-term

7. Tolerance: +/- 0.05mm -> +/- 0.1mm
   Spring is forgiving, so tube precision relaxed.

UNCHANGED FROM V2.4:
- Block dimensions (top 60x60x20, bottom 80x80x35)
- Top block geometry (single radial bearing pocket)
- Floor 3mm, washer pockets, thrust bearing pocket
- Loctite 603 + slip fit for radial bearings
- All M5 mount holes, countersinks, outer chamfers
- Block gap 11mm (6mm Al plate + 5mm clearance)

==========================================
HARDWARE TO ORDER (V2.5)
==========================================

1. Smalley CM25-L1 Wave Springs x 2  (~$15-20 total)
   Source: https://www.smalley.com/wave-spring/cm25-l1
   Best path: Request FREE SAMPLES from Smalley first
              (they often provide free samples for prototyping)
   Alternative: Rotor Precision Canada (rotoprecision.ca)

2. Spacer Washers x 2 (~$5-15)
   Spec: 19mm ID x 28mm OD x 1.6mm thick, 18-8 stainless
   Source: McMaster-Carr (mcmaster.com/products/stainless-steel-flat-washers)
   Search the metric washer catalog or call 630-833-0300
   Sold in packs (typically 25 per pack)

3. (Optional) Aluminum tube for spacer
   Spec: 18mm OD x 12mm ID
   Cut to 22.9mm length
   Source: Amazon "18mm OD 12mm ID aluminum tube"

4. Wood base 420 x 320 x 18mm
   Source: Home Depot or local lumber yard
   Hardwood preferred (oak, maple, or birch plywood)

==========================================
ASSEMBLY ORDER (V2.5)
==========================================
1. Print all 3 STLs (top block, bottom block, spacer tube 22.9mm)
2. Apply Loctite 603, install bearings, cure 24h
3. Stack into bottom block:
   - 2x AS1226 washers (lower)
   - 51101 thrust bearing
   - 2x AS1226 washers (upper)
   - CM25-L1 spring
   - McMaster spacer washer (28x19x1.6mm)
4. Install bottom radial bearing (Loctite, cure 24h)
5. Install top radial bearing in top block (Loctite, cure 24h)
6. Mount blocks on aluminum plate (verify 11mm BLOCK_GAP)
7. Install bottom shaft collar at Z=-2mm (hard stop)
8. Insert shaft through bottom block
9. Slide spacer tube (22.9mm) onto shaft above bottom radial inner race
10. Lower top block onto shaft (top bearing slides down onto spacer)
11. Install top shaft collar - LIGHTLY clamp (retention only)

==========================================
TEST PROTOCOL
==========================================
Test 1: Rotation - smooth, slight resistance OK
Test 2: Axial play - pull shaft, ZERO movement allowed
Test 3: Drag - if too sticky, spacer too short (lengthen 0.2-0.3mm)
Test 4: Click - if click on rotation, spacer too long (shorten 0.2-0.3mm)
Test 5: Dial indicator - shaft runout <0.2mm TIR at shaft end

==========================================
FORCE PATH (V2.5)
==========================================
Top block (rigid)
 -> top bearing inner race
   -> spacer tube (22.9mm rigid)
     -> bottom radial bearing inner race
       -> spacer washer (McMaster 19x28x1.6)
         -> CM25-L1 spring (compressed 3.20mm = ~35N)
           -> upper washers
             -> thrust bearing (preloaded)
               -> lower washers
                 -> PETG floor (rigid)

Result: preload set by SPRING COMPRESSION, controlled by spacer length.

==========================================
PRINT SETTINGS
==========================================
Blocks: PETG, 0.2mm layer, 5 perimeters, 40-50% Gyroid infill
        Pocket opening UP, no supports
Spacer tube: PETG, 0.1mm layer, 8 perimeters, 100% infill
             Vertical orientation, slow speed (30mm/s)
