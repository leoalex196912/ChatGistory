CSM V3 - CYLINDER V1.1.1 (FINAL)
==================================
Date: April 2026
Status: LOCKED - Ready for printing

==========================================
WHAT IS THE CYLINDER?
==========================================

The cylinder is the rotating heart of the CSM. It carries 72 latch
needles in vertical slots. The cylinder rotates while the cam ring,
sinker ring, and retainer ring stay stationary.

As the cylinder rotates, needle butts ride on the cam profile,
causing each needle to rise and fall to form stitches.

==========================================
KEY DIMENSIONS (LOCKED)
==========================================

Cylinder body:
  Outer diameter:   114.3mm (4.5" Legare standard)
  Inner diameter:   88.0mm  (clears drive hub upper extension)
  Height:           75.0mm
  Wall thickness:   13.15mm
  Material:         PETG (DRY)

Needle slots (72 total):
  Pitch:            5.0deg (360/72)
  Slot width:       1.20-1.22mm (TEST WEDGE first to verify)
  Slot depth:       1.80mm
  Slot length:      from cylinder top down ~30mm (stem zone)
  Butt cavity:      below slot, accommodates butt projection

Spring groove (V1.1.1):
  Z bottom:         17.9mm
  Z top:            21.1mm
  Width:            3.2mm
  Depth:            1.2mm
  Purpose:          Holds FlyDesigns Common Thickness cylinder spring
                    Spring wraps around cylinder OD externally

==========================================
TEST WEDGE PROTOCOL (CRITICAL!)
==========================================

DO NOT print full cylinder before validating slot fit.

Phase 1: Slot width validation
  Print 3 test wedges with different slot widths:
    - 1.20mm
    - 1.22mm  
    - 1.25mm
  Test fit with actual 12g latch needle from FlyDesigns
  Pick the width that gives best fit (slight friction, no binding)

Phase 2: Spring fit validation
  Print test wedge with V1.1.1 spring groove
  Test fit with actual cylinder spring
  Verify spring sits in groove without binding

Phase 3: Print full cylinder ONLY AFTER both phases pass

==========================================
PRINT INSTRUCTIONS
==========================================

Material:       PETG (DRY filament essential!)
Layer height:   0.16mm (NOT 0.2mm)
Perimeters:     5
Top/bottom:     6 layers
Infill:         40-50% Cubic
Orientation:    Vertical (Z axis along cylinder axis)
                Cylinder bore facing up
Supports:       NONE (vertical orientation eliminates need)
Outer wall speed: 25 mm/s (slow for slot quality)
Inner wall speed: 50 mm/s
Infill speed:   80-100 mm/s
Cooling:        100% after layer 3
Monotonic top:  ON

Time estimates:
  Test wedge: ~30 min, ~15g PETG
  Full cylinder: ~6-8 hours, ~250g PETG

POST-PRINT FINISHING:
  1. Inspect each slot - should be uniform
  2. Light sand slots with 1000-grit if needed
  3. Test fit one needle in each slot before assembly
  4. Apply small amount of PTFE lubricant to slots

==========================================
HARDWARE NEEDED (ALL IN INVENTORY)
==========================================

  - PETG filament (B0D4QD8T2R)
  - 12g latch needles (FlyDesigns)
  - Cylinder springs (FlyDesigns Common Thickness)
  - Sandpaper (B07DTGP1QT)
  - PTFE lubricant (B003UTX0R8)
  - IPA (B00DT52Y98)

==========================================
INTERFACES WITH OTHER COMPONENTS
==========================================

Below:
  Cylinder bottom mounts to → Drive Hub V1.3
  Drive hub bolts to        → 12mm shaft
  Shaft supported by        → Bearing Housings V2.5.1 (top + bottom)

Around:
  Cylinder rotates inside   → Cam Ring V6.5 (stationary)
  Cylinder spring sits in   → External groove on cylinder OD

Above:
  Cylinder top supports     → Sinker Ring V1.0 (sits at Z=75)
  Then                      → Retainer Ring V1.0 (above sinker ring)

==========================================
CHANGES FROM V1.1
==========================================

V1.1.1 corrected the spring groove dimensions:
  - Z bottom: 17.9mm (was 18.0)
  - Z top: 21.1mm (was 22.0 → now = 17.9 + 3.2 width)
  - Centers spring on butt rest position
  - Allows proper spring engagement with butts
