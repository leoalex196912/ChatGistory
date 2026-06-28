CSM V3 - SINKER RING V1.0
============================
Date: May 2026

==========================================
WHAT IS THE SINKER RING?
==========================================

The sinker ring is a stationary component that sits at the TOP of
the rotating cylinder. It has 72 small projections ("sinkers") that
hold yarn loops while needles drop to form stitches.

Function in knitting cycle:
1. Needle rises in cylinder slot (cam ring lifts it)
2. Yarn feeder places yarn in needle hook
3. Needle drops - old loop slides off latch
4. Old loop catches on sinker projection (sinker holds it up)
5. Needle drops through, forming the stitch

==========================================
KEY DIMENSIONS
==========================================

Ring main body:
  Outer diameter:   135mm
  Inner diameter:   114.8mm (0.5mm clearance over 114.3mm cylinder)
  Height:           8mm
  Wall thickness:   ~10.1mm

Sinker projections:
  Count:            72 (one per needle slot)
  Pitch:            5.0° (360/72)
  Phase offset:     2.5° from needle slots (between needles)
  Width:            1.2mm circumferential
  Radial extension: 3.0mm inward from ring ID
  Tip radius:       54.4mm (over open top of cylinder)
  Height (full):    4mm
  Height (taper):   2mm at feeder window centers
  Z position:       4-8mm (upper half of ring)

Feeder windows:
  Count:            6 (at 0°, 60°, 120°, 180°, 240°, 300°)
  Window arc:       ~8mm (~8°)
  Taper range:      ±5° from feeder center
  Easing:           SMOOTHSTEP cubic (jerk-free)
  Modified sinkers: 12 of 72 (2 per feeder)

Mounting:
  3 dowel pins at PCD 125mm (62.5mm radius)
  Pin angles: 30°, 150°, 270° (between feeders)
  Pattern: 1 round + 2 slotted (thermal compensation)
  Pin hole: 4.2mm diameter (4.0mm pin + 0.2mm clearance)

==========================================
VERTICAL POSITIONING (CRITICAL!)
==========================================

The sinker ring is NOT around the cylinder body.
It sits at the TOP of the cylinder.

Vertical stack:
  Z=0     ─ Cylinder base (drive hub)
  Z=0-75  ─ CYLINDER BODY (75mm tall, OD 114.3mm)
  Z=75    ─ Cylinder TOP (open)
  Z=75    ━ SINKER RING base (sits on cylinder top)
  Z=75-79 ─ Lower ring body (4mm, around cylinder edge)
  Z=79-83 ─ SINKER PROJECTIONS (extend inward, over open cylinder top)

Why this works:
  - Sinker tips at radius 54.4mm
  - Cylinder OD radius is 57.15mm
  - Sinker tips are 2.75mm INSIDE cylinder OD
  - BUT they're ABOVE Z=79mm, where cylinder body has ENDED
  - So sinkers project over the OPEN TOP of cylinder
  - No interference with rotating cylinder body

==========================================
WHY 72 SINKERS WITH TAPER (NOT REMOVAL)
==========================================

Earlier engineering review confirmed:
  - NEVER remove sinkers at feeder zones
  - All 72 sinkers must remain (structural function)
  - Only TAPER height in feeder zones (4mm → 2mm)

The taper allows:
  - Yarn to enter feeder window without hitting sinker tops
  - Sinkers still hold loops (just at lower height)
  - Smooth transitions (smoothstep easing)

Without sinkers in feeder zones:
  - Loops would not be held during feeder operation
  - Stitches would drop or be inconsistent
  - Knitting would fail at feeder positions

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
TEST PROTOCOL
==========================================

Phase 1: Print test slice (30° sector covering one feeder)
  - File: CSM_V3_SinkerRing_V1_0_TESTSLICE.stl
  - Time: ~45 min
  - Validates: sinker geometry, taper transitions, feeder window

Phase 2: Inspect test slice
  - Sinker projections: should be visible and well-defined
  - Width: 1.2mm (verify with calipers)
  - Taper: smooth transition at feeder zone
  - No obvious print defects

Phase 3: Light finishing
  - Sand sinker tips lightly with 1000-grit
  - Wipe with isopropyl alcohol
  - Apply PTFE lubricant to contact surfaces

Phase 4: Test fit
  - Sinker ring should sit on top of cylinder
  - Cylinder should rotate freely (0.25mm/side clearance)
  - Sinkers should be above cylinder body

Phase 5: If test passes - print full ring
  - File: CSM_V3_SinkerRing_V1_0_FULL.stl
  - Time: ~3-4 hours

==========================================
DESIGN DECISIONS
==========================================

Why 1.2mm sinker width?
  - At 5° pitch, 1.2mm sinker leaves 3.5mm gap
  - Needles can rise through gaps without obstruction
  - Sinkers structurally robust at this width
  - Print tolerance: ±0.1mm acceptable

Why 3.0mm radial extension?
  - Far enough to hold yarn loop reliably
  - Not so far as to interfere with needle hook
  - Tip at 54.4mm = 10.4mm from cylinder centerline

Why 4mm full height / 2mm minimum?
  - 4mm ensures positive loop retention
  - 2mm at feeder zones allows yarn entry
  - 2:1 ratio is standard for CSM design

Why ±5° taper range?
  - Total taper zone: 10° per feeder
  - 2 sinkers per feeder zone are tapered
  - Smooth smoothstep transition (no jerk)
  - 12 of 72 sinkers modified (17%)

Why pin pattern 30°/150°/270°?
  - 60° offset from feeders (not in same angular zones)
  - 120° apart (3-pin pattern, kinematic)
  - 1 round + 2 slotted = thermal expansion tolerance

==========================================
INTERFACES WITH OTHER COMPONENTS
==========================================

Below (sits on):
  → Cylinder V1.1.1 top face (Z=75mm)
  
Above (will be added):
  → Retainer Ring V1.0 (sits on top of sinker ring at Z=83mm)
  
Around:
  → Cassette Base V1.0 (mounting structure)
  
Inside:
  → Cylinder rotates inside (114.3mm OD, 0.25mm/side clearance)

==========================================
HARDWARE NEEDED
==========================================

Already have (from Orders.xlsx):
  - PETG filament (B0D4QD8T2R)
  - 4mm dowel pins (B0F5HFFVP7)
  - Sandpaper (B07DTGP1QT)
  - PTFE lubricant (B003UTX0R8)
  - Isopropyl alcohol (B00DT52Y98)

Nothing new to order.

==========================================
NEXT COMPONENT
==========================================

After Sinker Ring validates:
  → Retainer Ring V1.0 (PA12, sits above sinker ring)
  → Cassette Base V1.0 (200mm, supports entire stack)
  → Feeder Module V1.0 (mechanical + servo)
  → Yarn Mast V1.0
