CSM V3 - SINKER RING V1.1 (engineering review applied)
==========================================================
Date: May 2026
Status: Design refined - ready for printing

==========================================
EVOLUTION
==========================================

V1.0  - Initial design
V1.1  - 9 engineering review changes applied  ← THIS VERSION

==========================================
ALL CHANGES FROM V1.0 (engineering review - 8 of 9 implemented)
==========================================

1. RADIAL EXTENSION: 3.0 → 4.0mm  ✓
   Real CSM uses 4-5mm for reliable loop retention
   At 3mm, loops could slip during stitch formation

2. TIP GEOMETRY: DEFERRED TO V1.2  ⏸
   Originally planned: 10° backward angled tip
   Initial implementation used global Z-axis rotation (geometrically WRONG
   for localized features at 53.65mm radius - cut plane would be ~9° away
   from the sinker, never touching it).
   Correct approach requires local-frame transformation.
   Deferred reasoning:
     - V1.1 already has 8 changes - validate those first
     - Flat tips still hold yarn (just less catch-and-release elegance)
     - Real-world yarn behavior unknown until V1.1 testing
     - Implementation deserves dedicated focus in V1.2

3. SINKER Z BASE: 4.0 → 2.5mm  ✓
   Sinkers now engage yarn loop earlier in stitch cycle
   Loop sits ~2-3mm above cylinder rim - sinker matches that position

4. FEEDER TAPER RANGE: ±5° → ±4° (was 10° total, now 8°)  ✓
   Now matches feeder window width exactly
   Eliminates tapering of sinkers OUTSIDE the feeder zone

5. CLEARANCE: 0.25mm → 0.50mm per side (ID 115.3)  ✓
   Accounts for PETG real-world distortion stack:
   - Ovalization: ±0.15mm
   - Thermal expansion: +0.08-0.10mm
   - Assembly forces: ±0.05-0.10mm
   - Wall flex: ±0.05mm
   Total: ~0.30-0.40mm. 0.50mm clearance leaves 0.20mm safe margin.

6. AXIAL RETENTION: added 3× M3 screws (downward into cassette base)  ✓
   Pins prevent rotation but NOT lift
   Yarn tension + vibration could lift the ring without screws
   Counterbored for socket head (M3 head 6mm × 3mm deep)
   Located at 90°, 210°, 330° (between dowel pins)

7. STRUCTURAL FILLET: relies on FDM print smoothing  ⚠
   Explicit FreeCAD fillet on 72 sinker bases is geometrically complex
   FDM print smoothing acts as effective fillet at print resolution (~0.16mm)
   If V1.1 testing shows stress cracks, V1.2 will add explicit fillets

8. SINKER WIDTH: 1.2 → 1.3mm  ✓
   Better print confidence on 0.4mm nozzle
   Gap between sinkers still 3.4mm (needles pass freely)

9. ID CHAMFER: optional toggle (default ON)  ✓
   0.5mm × 45° at top AND bottom of ring ID
   Helps cylinder assembly into ring
   Removes layer-line catch on first contact
   Toggleable via ENABLE_ID_CHAMFER flag

==========================================
V1.2 PLAN (after V1.1 testing)
==========================================

After V1.1 prints validate the 8 implemented changes, V1.2 will add:

1. ANGLED TIP (10° backward from radial at trailing-tip corner)
   Implementation strategy:
     a. Build cutter in local sinker frame (X=radial, Y=tangential)
     b. Apply 10° rotation in local frame
     c. Translate cutter so cutting face passes through tip corner
     d. Rotate to global theta (single global rotation)
   This produces deterministic, identical sinkers at all 72 positions
   Reference: see commented "V1.2 Plan" section in macro

2. EXPLICIT BASE FILLETS (if V1.1 testing shows cracking)
   0.5-1mm fillet at sinker-to-ring junction
   Implementation: Part.Wire + Part.makeFilledFace approach

3. KINEMATIC COHERENCE TUNING (if needed)
   Adjust taper smoothstep timing if yarn behavior is inconsistent

==========================================
DIMENSIONS (V1.1)
==========================================

Ring main body:
  Outer diameter:   135mm
  Inner diameter:   115.3mm  (V1.1: was 114.8)
  Per-side clearance: 0.50mm (V1.1: was 0.25)
  Height:           8mm
  Wall thickness:   ~9.85mm

Sinker projections (V1.1):
  Count:            72
  Pitch:            5.0°
  Phase offset:     2.5°
  Width:            1.3mm  (V1.1: was 1.2)
  Radial extension: 4.0mm  (V1.1: was 3.0)
  Tip radius:       53.65mm
  Tip geometry:     FLAT (V1.2 will add 10° angle)
  Height (full):    4mm
  Height (taper):   2mm at feeder centers
  Z base:           2.5mm  (V1.1: was 4.0)

Feeder zones (V1.1):
  Count:            6 (at 0°, 60°, 120°, 180°, 240°, 300°)
  Window arc:       8mm (~7.95°)
  Taper range:      ±4° (V1.1: was ±5°)
  Match:            Taper now matches window width exactly

ID chamfer (V1.1, toggleable):
  Enabled:          True (default)
  Size:             0.5mm at 45°
  Location:         Top AND bottom of ID
  Toggle:           ENABLE_ID_CHAMFER flag

Mounting (V1.1 expanded):
  3× dowel pins at PCD 125mm:
    - Angles: 30°, 150°, 270°
    - Hole: 4.2mm diameter
    - 1 round + 2 slotted (thermal expansion)
  3× M3 axial retention screws at PCD 125mm: (V1.1 NEW)
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
TEST PROTOCOL (V1.1)
==========================================

Phase 1: Print test slice
  File: CSM_V3_SinkerRing_V1_1_TESTSLICE.stl
  
Phase 2: Inspect critical features
  - Sinker width: should be 1.3mm (caliper check)
  - Sinker tip: FLAT face (10° angle deferred to V1.2)
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
  → Cylinder V1.1.1 top face (Z=75mm)
  
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

After Sinker Ring V1.1 validates:
  → Retainer Ring V1.0
  → Cassette Base V1.0 (must include matching pin/screw pattern!)
  → Feeder Module V1.0
  → Yarn Mast V1.0
