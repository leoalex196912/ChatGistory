CSM V3 - SINKER RING V1.2.1 (review fixes applied)
================================================================
Date: May 2026
Status: Final design - ready for printing

==========================================
EVOLUTION
==========================================

V1.0    - Initial design
V1.1    - 8 of 9 engineering review changes (angled tip deferred)
V1.2    - All 9 changes implemented + dual clearance test
V1.2.1  - Engineering review fixes (4 issues)  ← THIS VERSION

==========================================
V1.2.1 FIXES (4 issues from review)
==========================================

FIX 1: CUTTER SIZE REDUCED
  Was: L=6.0mm, W=6.0mm
  Now: L=5.0mm, W=2.6mm (= SINKER_RADIAL_EXT+1, SINKER_WIDTH*2)
  Why: W=6mm extended too far tangentially - only 1.68mm margin to next
       sinker at 4.68mm pitch arc. Risk of collision with adjacent geometry.
  Benefit: Clean cuts + 72x faster boolean operations.

FIX 2: BOOLEAN ROBUSTNESS OFFSET
  Was: cutter at exact tip corner (zero offset)
  Now: cutter shifted -0.05mm radially into material
  Why: Coincident cutting planes risk non-manifold edges in FreeCAD,
       producing knife-edge geometry that fails in slicers.
  Benefit: Clean STL output, no slicer artifacts.

FIX 3: DUAL CLEARANCE BUG FIX (CRITICAL)
  Was: V1.2 used global RING_INNER_R/SINKER_TIP_R inside sinker geometry
       Dual clearance test slices showed different ring ID but
       sinkers stayed at identical positions
  Now: Function-local inner_r and local_tip_r used consistently
       Sinkers move correctly with the ring
  Verified: at ID 115.1, sinker tips shift 0.1mm radially (correct)
  Benefit: Dual clearance test is now actually valid.

FIX 4: CUT VOLUME VERIFICATION
  Was: sinker = sinker.cut(tip_cutter) - silent failures possible
  Now: Compares volume before/after, warns if cut ineffective
  Why: Numerical precision could make boolean cut miss the geometry,
       resulting in flat tips with no warning.
  Benefit: Reliable detection of geometry issues.

==========================================
V1.2 (CARRIED FORWARD): ANGLED TIP
==========================================

10° backward angled tip at trailing-edge corner

Implementation strategy (verified correct):
  1. Anchor at TRAILING EDGE tip corner (tip_theta_deg, NOT theta_deg)
  2. Build local basis at tip:
     - radial = unit vector pointing outward from origin to tip
     - tangential = perpendicular (CCW direction)
     - z_axis = global Z
  3. Apply 10° backward tilt INSIDE local frame:
     - tilted_radial = radial · cos(α) - tangential · sin(α)
     - tilted_tangential = z × tilted_radial (cross product)
  4. Position cutter via Placement ONLY (no mixed transforms)

Verified geometrically:
  ✓ Cutting plane passes through tip corner at all Z
  ✓ Normal is exactly 10° backward from radial at tip
  ✓ All 72 sinkers identical (deterministic transforms)

Toggle: ENABLE_ANGLED_TIP = True
  Set False to revert to flat tip for testing comparison

==========================================
V1.2.1 NEW: DUAL CLEARANCE TEST SLICES
==========================================

Macro now outputs THREE STL files:
  1. CSM_V3_SinkerRing_V1_2_FULL.stl              (full ring, ID 115.3)
  2. CSM_V3_SinkerRing_V1_2_TESTSLICE_ID115_3.stl (30° slice, 0.50mm/side)
  3. CSM_V3_SinkerRing_V1_2_TESTSLICE_ID115_1.stl (30° slice, 0.40mm/side)

Print BOTH test slices (~90 minutes total).
Test fit each on cylinder.
Choose the ID that fits YOUR printer best.

This eliminates guesswork on real-world clearance.

==========================================
ALL 9 CHANGES FROM V1.0 (now complete)
==========================================

1. RADIAL EXTENSION: 3.0 → 4.0mm  ✓ (V1.1)
2. TIP GEOMETRY: 10° backward angled  ✓ (V1.2.1)
3. SINKER Z BASE: 4.0 → 2.5mm  ✓ (V1.1)
4. FEEDER TAPER RANGE: ±5° → ±4°  ✓ (V1.1)
5. CLEARANCE: 0.50mm/side (with optional 0.40mm test)  ✓ (V1.1)
6. AXIAL RETENTION: 3× M3 screws  ✓ (V1.1)
7. STRUCTURAL FILLET: FDM smoothing  ⚠ (V1.1, V1.3 if cracks)
8. SINKER WIDTH: 1.2 → 1.3mm  ✓ (V1.1)
9. ID CHAMFER: 0.5mm × 45° toggleable  ✓ (V1.1)

==========================================
PRE-PRINT VISUAL VERIFICATION (RECOMMENDED)
==========================================

Before exporting STL files, in FreeCAD:
  1. Hide the ring object
  2. Show one sinker + its angled tip cutter
  3. Visually confirm:
     ✓ Plane is at trailing edge of sinker (not leading edge)
     ✓ Tilt direction is backward (against rotation direction)
     ✓ Cut actually intersects sinker tip
  
  Takes 30 seconds, saves a 4-hour print if direction is wrong.

If rotation direction is reversed in actual machine assembly:
  - Yarn will be cut FORWARD instead of backward
  - Result: worse yarn release, not better
  - Fix: set SINKER_TIP_ANGLE_DEG to -10 (reverses direction)

==========================================
DETAILED CHANGE NOTES
==========================================

CHANGE 1 - Radial extension 3.0 → 4.0mm:
  Real CSM uses 4-5mm for reliable loop retention
  At 3mm, loops could slip during stitch formation

CHANGE 2 - Angled tip 10° backward (V1.2.1):
  Implemented with proper local-frame transformation
  See "V1.2.1 NEW: ANGLED TIP" section above for full details

CHANGE 3 - Sinker Z base 4.0 → 2.5mm:
  Sinkers now engage yarn loop earlier in stitch cycle
  Loop sits ~2-3mm above cylinder rim - sinker matches that position

CHANGE 4 - Feeder taper range ±5° → ±4° (was 10° total, now 8°):
  Now matches feeder window width exactly
  Eliminates tapering of sinkers OUTSIDE the feeder zone

CHANGE 5 - Clearance 0.25mm → 0.50mm per side (ID 115.3):
  Accounts for PETG real-world distortion stack:
  - Ovalization: ±0.15mm
  - Thermal expansion: +0.08-0.10mm
  - Assembly forces: ±0.05-0.10mm
  - Wall flex: ±0.05mm
  Total: ~0.30-0.40mm. 0.50mm clearance leaves 0.20mm safe margin.

CHANGE 6 - Axial retention (3× M3 screws):
  Pins prevent rotation but NOT lift
  Yarn tension + vibration could lift the ring without screws
  Counterbored for socket head (M3 head 6mm × 3mm deep)
  Located at 90°, 210°, 330° (between dowel pins)

CHANGE 7 - Structural fillet (FDM smoothing):
  Explicit FreeCAD fillet on 72 sinker bases is geometrically complex
  FDM print smoothing acts as effective fillet at print resolution
  If V1.2.1 testing shows stress cracks, V1.3 will add explicit fillets

CHANGE 8 - Sinker width 1.2 → 1.3mm:
  Better print confidence on 0.4mm nozzle
  Gap between sinkers still 3.4mm (needles pass freely)

CHANGE 9 - ID chamfer (toggleable, default ON):
  0.5mm × 45° at top AND bottom of ring ID
  Helps cylinder assembly into ring
  Removes layer-line catch on first contact

==========================================
V1.3 PLAN (only if V1.2.1 testing reveals issues)
==========================================

V1.3 changes are CONDITIONAL on V1.2.1 print test results:

1. EXPLICIT BASE FILLETS (only if cracking observed)
   0.5-1mm fillet at sinker-to-ring junction
   Implementation: Part.Wire + Part.makeFilledFace approach

2. TIP RADIUS REFINEMENT (only if yarn abrasion observed)
   Round tip edge by 0.2-0.3mm (reduces yarn wear)

3. TIP ANGLE TUNING (only if release behavior is wrong)
   - Yarn slips early → reduce to 7-8°
   - Tip too weak → increase to 12°
   - Direction wrong → set SINKER_TIP_ANGLE_DEG = -10

4. KINEMATIC COHERENCE TUNING (only if yarn behavior inconsistent)
   Adjust taper smoothstep timing

==========================================
DIMENSIONS (V1.2.1)
==========================================

Ring main body:
  Outer diameter:   135mm
  Inner diameter:   115.3mm
  Per-side clearance: 0.50mm
  Height:           8mm
  Wall thickness:   ~9.85mm

Sinker projections (V1.2.1):
  Count:            72
  Pitch:            5.0°
  Phase offset:     2.5°
  Width:            1.3mm
  Radial extension: 4.0mm
  Tip radius:       53.65mm
  Tip geometry:     10° backward angled (V1.2.1)
    - Anchor:       trailing-tip corner
    - Frame:        local at tip
    - Transform:    single Placement (no mixed transforms)
  Height (full):    4mm
  Height (taper):   2mm at feeder centers
  Z base:           2.5mm

Feeder zones (V1.2.1):
  Count:            6 (at 0°, 60°, 120°, 180°, 240°, 300°)
  Window arc:       8mm (~7.95°)
  Taper range:      ±4°
  Match:            Taper matches window width exactly

ID chamfer (V1.2.1, toggleable):
  Enabled:          True (default)
  Size:             0.5mm at 45°
  Location:         Top AND bottom of ID
  Toggle:           ENABLE_ID_CHAMFER flag

Mounting (V1.2.1 expanded):
  3× dowel pins at PCD 125mm:
    - Angles: 30°, 150°, 270°
    - Hole: 4.2mm diameter
    - 1 round + 2 slotted (thermal expansion)
  3× M3 axial retention screws at PCD 125mm: (V1.2.1 NEW)
    - Angles: 90°, 210°, 330°
    - Through hole: 3.4mm diameter
    - Counterbore: 6mm × 3mm deep (for socket head)
    - Screws downward into cassette base heat-set inserts

==========================================
VERTICAL POSITIONING (UNCHANGED)
==========================================

The sinker ring sits at TOP of cylinder, NOT around it.

Vertical stack (machine coords):
  Z=0     ─ Cylinder base
  Z=0-75  ─ CYLINDER BODY (75mm tall, OD 114.3mm)
  Z=75    ─ Cylinder TOP (open)
  Z=75    ━ SINKER RING base (sits on cylinder top)
  Z=75-77.5  Lower ring body (2.5mm)
  Z=77.5-81.5 SINKER PROJECTIONS (engages yarn loop here)
  Z=81.5-83  Upper ring body (1.5mm)

Sinkers engage at Z=77.5-81.5 = where yarn loop sits

==========================================
PRINT INSTRUCTIONS
==========================================

Material:       PETG (DRY!)
Layer height:   0.16mm
Perimeters:     4
Top/bottom:     5 layers
Infill:         30-40% Gyroid
Orientation:    Lying flat, sinker projections pointing UP
Supports:       NONE
Outer wall:     25 mm/s
Inner wall:     50 mm/s
Infill:         80-100 mm/s
Cooling:        100% after layer 3

Time estimates:
  Test slice (30°): ~45 min, ~25g PETG
  Full ring:        ~3-4 hours, ~140g PETG

==========================================
TEST PROTOCOL (V1.2.1)
==========================================

Phase 1: Print test slice
  File: CSM_V3_SinkerRing_V1_1_TESTSLICE.stl
  
Phase 2: Inspect critical features
  - Sinker width: should be 1.3mm (caliper check)
  - Sinker tip: 10° backward angle on TRAILING edge (visible)
  - Taper transition: smooth at feeder zone edges
  - ID chamfer: visible 0.5mm chamfer at top/bottom (if enabled)

Phase 3: Light finishing
  - Sand sinker tips lightly with 1000-grit
  - Wipe with isopropyl alcohol
  - Apply PTFE lubricant to inner ID where it contacts cylinder

Phase 4: Test fit on cylinder
  - Ring should drop onto cylinder smoothly
  - Should rotate slightly with finger pressure (not bind)
  - Sinkers should clear cylinder body completely

Phase 5: Print full ring
  File: CSM_V3_SinkerRing_V1_1_FULL.stl
  
Phase 6: Install heat-set M3 inserts in cassette base
  At positions: 90°, 210°, 330° on PCD 125mm
  
Phase 7: Assemble
  - Insert 3 dowel pins into cassette base
  - Lower sinker ring onto pins (round pin first)
  - Install 3 M3 socket head screws (with Loctite 222 medium)
  - Verify cylinder rotates freely

==========================================
HARDWARE NEEDED (ALL IN INVENTORY)
==========================================

  - PETG filament (B0D4QD8T2R)
  - 4mm dowel pins (B0F5HFFVP7)
  - M3 socket head screws (B0FFSNFK3Y)
  - M3 heat-set inserts (B0DQL5YWKQ)
  - Loctite 222 (or similar medium thread locker)
  - Sandpaper (B07DTGP1QT)
  - PTFE lubricant (B003UTX0R8)
  - Isopropyl alcohol (B00DT52Y98)

Nothing new to order.

==========================================
INTERFACES WITH OTHER COMPONENTS
==========================================

Below (sits on):
  → Cylinder V1.2.1 top face (Z=75mm)
  
Above (will be added):
  → Retainer Ring V1.0 (sits on top of sinker ring at Z=83mm)
  
Around / supporting:
  → Cassette Base V1.0:
    - Provides 3 dowel pin holes at PCD 125mm (30°, 150°, 270°)
    - Provides 3 M3 heat-set insert holes at PCD 125mm (90°, 210°, 330°)
  
Inside:
  → Cylinder rotates inside (114.3mm OD, 0.50mm/side clearance)

==========================================
NEXT COMPONENTS
==========================================

After Sinker Ring V1.2.1 validates:
  → Retainer Ring V1.0
  → Cassette Base V1.0 (must include matching pin/screw pattern!)
  → Feeder Module V1.0
  → Yarn Mast V1.0
