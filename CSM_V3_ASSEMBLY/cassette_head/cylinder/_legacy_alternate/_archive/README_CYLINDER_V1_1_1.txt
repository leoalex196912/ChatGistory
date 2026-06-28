CSM V3 - CYLINDER V1.1.1 (refined spring groove)
==================================================
Date: April 2026

CHANGES FROM V1.1:
  Spring groove parameters refined per engineering review:
  
  Parameter         V1.1     V1.1.1   Reason
  ---------------   ------   ------   --------------------------------
  Width (axial)     3.0mm    3.2mm    PETG shrink margin
                                      (3.0 prints ~2.85 - too tight)
  Depth (radial)    1.5mm    1.2mm    More spring exposed = more flex
                                      (less friction, better cam balance)
  Z bottom          19.0mm   17.9mm   Better centered on butt rest
  Z top             22.0mm   21.1mm   (= 17.9 + 3.2 width)
  Z center          20.5mm   19.5mm   Captures L-bend horizontal at rest

WHY THESE CHANGES:
  Width: After PETG ~0.15mm shrink, designed 3.0mm prints as ~2.85mm.
         A 2.79mm wire in 2.85mm slot has only 0.06mm clearance - too tight.
         Designed 3.2mm prints as ~3.05mm = 0.26mm clearance - comfortable.
         
  Depth: At 1.5mm depth, spring is more recessed (1.4mm exposed).
         Reviewer noted this constrains spring flex. CSM springs need to
         flex outward when cam pushes butt. Less exposed = stiffer = more
         friction load on cam = potential needle binding.
         At 1.2mm depth: 1.6mm exposed = better flex compliance.
         
  Z position: My V1.1 had Z=19-22 which captures upper butt cavity.
              Reviewer argued for 17.5-20.5 to match horizontal L-bend
              at rest. Compromise: Z=17.9-21.1 (center 19.5).
              Captures the horizontal L-bend portion when needle is at rest.

DIMENSIONAL SUMMARY (V1.1.1):
  Cylinder OD:        114.3mm (Legare 4.5" standard)
  Cylinder ID:        88.0mm
  Height:             75mm
  Slot count:         72
  Slot W x D:         1.22 x 1.90mm rectangular
  Slot length:        52mm axial (Z=23 to Z=75)
  Slot top chamfer:   0.4mm lead-in
  Wall between slots: 3.77mm
  Butt cavity:        8.5 x 4.0mm at Z=19-23
  Hub pocket:         D18.20 x 3mm + 0.5mm chamfer
  Bolt pattern:       4x M5 @ PCD 70mm
  Spring groove:      W3.2 x D1.2mm at Z=17.9-21.1

OUTPUTS (same files as V1.1, refined geometry):
  1. Full 72-slot cylinder (CSM_V3_Cylinder_V1_1_1_FULL.stl)
  2. 30 deg test wedge (CSM_V3_Cylinder_V1_1_1_TESTWEDGE.stl)
  3. Top + side blueprint (Cylinder_V1_1_1_Blueprint.svg)

==========================================
SPRING ENGINEERING NOTES (from review)
==========================================

Spring force balance:
  Cam lift force needed: ~0.5-1.0 N per needle
  Spring stiffness (empirical): 0.8-1.5 N/mm
  At 1mm cam deflection: F = 0.8-1.5 N

  V1.1 (depth 1.5mm): F estimated 1.2-1.8 N - TOO HIGH
  V1.1.1 (depth 1.2mm): F estimated 0.7-1.1 N - MATCHES CAM ✓

Friction analysis (steel wire on steel needle butt):
  μ_dry = 0.2, μ_oiled = 0.1
  Force 1N -> friction 0.2N (acceptable)
  Force 2N -> friction 0.4N (degrades motion)
  V1.1.1 keeps friction in acceptable range.

The system isn't about holding needles tight - it's about:
  "Just enough force to return needle - but not resist cam"

==========================================
REMAINING RISK: SPRING NOT YET MEASURED
==========================================

These parameters use FlyDesigns published spec (.110" / 2.79mm).
When springs arrive, validate with caliper.
If actual wire diameter differs, adjust SPRING_GROOVE_W proportionally.

==========================================
TEST PROTOCOL (when wedge prints)
==========================================

Phase 1 (now - validate slot fit):
  - Print test wedge
  - Insert needle into each slot pair (1.20/1.22/1.25)
  - Pick winning slot width

Phase 2 (when springs arrive - validate groove):
  - Try fitting a length of spring wire in groove
  - Should sit with ~half wire diameter exposed
  - Test SPRING TENSION:
    * Press wire DEEP into groove - should release with light force
    * Pull wire OUT of groove - should resist but not bind
  - If too tight: file groove slightly OR reprint with wider groove
  - If too loose: reprint with narrower groove

Phase 3 (when both validated):
  - Set SLOT_WIDTH and SPRING_GROOVE_W to winning values
  - Print full cylinder

==========================================
HARDWARE TO ORDER NOW
==========================================

3x Cylinder Springs Common Thickness from FlyDesigns
URL: flydesigns.com/products/sock-machine-accessories-cylinder-springs-common-thickness
Price: 3 x $6 = $18 + shipping

ORDER NOTE: "Please ship OPEN/STRAIGHT for sizing flexibility"

==========================================
NEXT STEPS
==========================================

Phase 1 (this delivery): Cylinder V1.1.1 - DONE
Phase 2 (next): Sinker Ring V1.0
Phase 3 (next): Cam Ring V6
Phase 4 (next): Retainer Ring V1.0
Phase 5 (next): Cassette Base V1.0
