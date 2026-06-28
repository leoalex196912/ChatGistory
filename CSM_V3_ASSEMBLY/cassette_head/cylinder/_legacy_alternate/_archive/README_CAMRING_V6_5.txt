CSM V3 - CAM RING V6.5 (FINAL - production test ready)
=========================================================
Date: April 2026

==========================================
EVOLUTION SUMMARY
==========================================

V6   - WRONG (radial cam, no vertical lift)            [DISCARD]
V6.1 - CORRECTED (axial Z profile, real lift)          [Superseded]
V6.2 - REFINED (tolerance, 720 steps, gentler slope)   [Superseded]
V6.3 - SMOOTHSTEP cam easing + 8mm lift                [Superseded]
V6.4 - TOP LIP for contact control (knit zone only)    [Superseded]
V6.5 - SMOOTHSTEP-BLENDED lip transitions              [USE THIS - FINAL]

==========================================
*** MANDATORY POST-PRINT FINISHING ***
==========================================

V6.5 has BOTH bottom contact (cam profile) AND intermittent top contact
(lip in knit zone). This creates a pinch condition that is sensitive
to surface friction and misalignment.

Skipping the finishing steps below WILL cause:
  - Stick/slip behavior at layer lines
  - Inconsistent needle motion
  - Possible binding under print tolerance
  - Wear after first hours of operation

THIS IS NOT OPTIONAL. Do all 4 steps before assembly:

1. SAND BOTTOM CAM SURFACE (the rising/falling Z surface)
   - 400-grit sandpaper first - remove print artifacts and stair-stepping
   - 1000-grit second - smooth finish
   - Wipe with isopropyl alcohol after each step
   - Inspect under good light: no visible layer lines

2. SAND TOP LIP SURFACE (in knit zone, 270-325deg)
   - Same protocol as bottom
   - Pay extra attention to lip blend zones (270-273 and 322-325deg)
   - These are where contact loss is most likely

3. APPLY PTFE LUBRICANT (B003UTX0R8 - already in inventory)
   - Apply lightly to BOTH cam track surfaces (bottom AND lip)
   - Distribute evenly with cotton swab
   - Wipe excess - thin film, not pooled

4. VERIFY SURFACE QUALITY
   - Run finger lightly along cam track
   - Should feel smooth, no catch points
   - If any catches: re-sand that area

RE-LUBRICATE every 50 hours of operation.

==========================================
PRINT INSTRUCTIONS
==========================================

CRITICAL settings (especially print orientation):

  Material:       PETG (DRY filament essential)
  Layer height:   0.16mm (NOT 0.2mm) - smoother cam surface
  Perimeters:     5
  Top/bottom:     6 layers
  Infill:         40-50% Cubic
  
  ORIENTATION:    *** Ring lying FLAT (axis Z perpendicular to bed) ***
                  This puts cam surfaces parallel to layer lines
                  Ensures smooth riding surface for needle butts
                  
  Supports:       NONE
  Outer wall speed: 20-25 mm/s (slow for surface quality)
  Inner wall speed: 40-50 mm/s
  Infill speed:   80-120 mm/s
  Cooling fan:    100% after layer 3
  Monotonic top:  ON (PrusaSlicer/OrcaSlicer)
  Ironing:        OFF

Time estimates:
  Test slice (75deg): ~1-1.5 hours, ~35g PETG
  Full ring:          ~5-7 hours, ~180-200g PETG

==========================================
V6.5 CHANGES FROM V6.4
==========================================

NEW: Smoothstep blending of top lip transitions
  LIP_BLEND_ANGLE = 3.0 deg

What this does:
  V6.4: lip dropped/rose 0.8mm INSTANTLY at zone boundaries
  V6.5: lip ramps in/out smoothly over 3deg using smoothstep

Why this matters:
  Hard 0.8mm step in ceiling height could cause:
    - Secondary impact at zone boundary
    - Audible "click" during operation
    - Inconsistent transition behavior
  
  Smooth blending eliminates this:
    - Lip = 0 at theta = 270
    - Lip ramps to 0.8mm by theta = 273
    - Lip = 0.8mm full from 273 to 322
    - Lip ramps to 0 over 322-325
    - Lip = 0 at theta >= 325

==========================================
DESIGN DECISIONS NOT IMPLEMENTED (V7+ candidates)
==========================================

These were considered but deferred to keep V6.5 simple:

1. True overhang lip (radial inward projection)
   Status: Functionally equivalent to shorter ceiling for our geometry
   (butt is anchored to cylinder, can't escape radially)
   V7 candidate IF jump issues observed in testing

2. Kinematic coherence (lip phase tied to cam progress)
   Status: Two independent smoothstep functions could create brief
   transient at lip boundary. Reviewer says "next-order effect,
   likely negligible at our speeds."
   V7 candidate IF chatter/ticking observed at zone transitions

3. PA12 nylon material upgrade (vs PETG)
   Status: Better wear resistance but harder to print
   V7 candidate IF excessive wear observed after 50+ hours

4. 1440 angular segments (vs 720)
   Status: Below noise floor of PETG tolerance
   Computation cost too high for marginal benefit

==========================================
DIMENSIONS (V6.5 FINAL)
==========================================

Ring:
  OD:               165mm
  ID:               115mm (clears 114.3mm cylinder + 0.7mm)
  Height:           35mm
  Wall thickness:   25mm

Cam slot:
  Slot height:           6.0mm (outside knit zone)
                         5.2mm (inside knit zone, full lip)
                         5.2-6.0mm (lip blend zones)
  Slot depth:            3.0mm radial
  Z rest (bottom):       5mm
  Z peak (bottom):       13mm
  Lift amount:           8mm
  Z offset:              0.0mm (tuning parameter)

Top lip (V6.5):
  Max height:            0.8mm
  Zone start:            270deg
  Zone end:              325deg
  Blend angle:           3deg (smoothstep transitions)

Cam profile (smoothstep):
  Rest zone:    0-270deg + 325-360deg = 305deg total
  Rise zone:    270-300deg = 30deg (smoothstep)
  Peak zone:    300-305deg = 5deg
  Fall zone:    305-325deg = 20deg (smoothstep)
  Total knit zone: 55deg

Mounting (unchanged):
  6x M5 bolts at PCD 155mm
  6x 4mm pins at PCD 145mm (1 round + 5 slotted)

==========================================
TEST PROTOCOL
==========================================

Step 1: Print test slice (75deg, 260-335 covers all cam features)
  File: CSM_V3_CamRing_V6_5_TESTSLICE.stl

Step 2: COMPLETE MANDATORY FINISHING (above)
  - Sand bottom cam
  - Sand top lip
  - PTFE lubricate
  - Verify surface quality

Step 3: Mount near cylinder with at least one needle installed

Step 4: Slowly rotate cylinder, observe:
  - Smooth lift to ~8mm peak
  - No binding throughout knit zone (esp. at lip transitions)
  - No "click" or impact at zone boundaries
  - No jump or contact loss
  - All transitions smooth

Step 5: Decision:
  PASS -> print full ring
  Lift wrong -> adjust LIFT or Z_OFFSET, reprint slice
  Binding -> reduce TOP_LIP_HEIGHT to 0.5mm, reprint slice
  Chatter at lip transition -> increase LIP_BLEND_ANGLE to 5deg

==========================================
HARDWARE NEEDED
==========================================

Already have:
  - PETG filament (DRY!)
  - 6x M5 bolts (B0FFSNFK3Y assortment)
  - 6x 4mm dowel pins (B0FDWVGMQ9 / B0F5HFFVP7)
  - Loctite 603 (B0074NALBO)
  - PTFE lubricant (B003UTX0R8) *** MANDATORY USE ***
  - Sandpaper assortment (B07DTGP1QT) *** MANDATORY USE ***
  - Isopropyl alcohol 99% (B00DT52Y98)

Nothing new to order.

==========================================
ASSEMBLY
==========================================

1. Print full cam ring V6.5 (after test slice validates)
2. SAND bottom cam track (400 then 1000 grit)
3. SAND top lip surfaces in knit zone (400 then 1000 grit)
4. Wipe with IPA
5. Apply PTFE lubricant to all cam surfaces
6. Cassette base V1.0 must be done first
7. Apply Loctite 603 to M5 bolt threads
8. Insert 6 dowel pins into cassette base
9. Lower cam ring onto pins (round pin first locks orientation)
10. Tighten 6 M5 bolts in cross pattern
11. Cure Loctite 24h
12. Hand-rotate cylinder, verify smooth needle motion through full ring

==========================================
WHEN TO ADVANCE TO V7
==========================================

After 50+ hours of operation, inspect cam track for:

  Symptom              -> V7 path
  ------------------   ----------------------------
  Smooth wear pattern  -> No upgrade needed
  Localized galling    -> True overhang lip OR PA12
  Audible ticking      -> Kinematic coherence (phase lock)
  Excessive wear       -> PA12 nylon material
  Print artifacts      -> Better surface finish protocol

Don't preemptively upgrade. Test, observe, then decide.

==========================================
NEXT STEPS
==========================================

Cam ring design is COMPLETE.
Next phase: Sinker Ring V1.0 (most complex remaining knitting part)
Then: Retainer Ring V1.0 (PA12, 6 yarn cutouts)
Then: Cassette Base V1.0 (200mm OD, 6 feeder mounts)
Then: Feeder Module V1.0 (mechanical + servo)
Then: Yarn Mast V1.0
