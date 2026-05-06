CSM V3 - DRIVE HUB V1.3 (PRODUCTION-PERFECT)
==============================================
Date: April 2026

Macro: CSM_V3_DriveHub_V1_3.FCMacro

VERSIONING NOTE:
Drive hub now uses INDEPENDENT version counter (per project policy).
Earlier files named V2.4, V2.4.1, V2.4.2 were actually V1.0, V1.1, V1.2.
This file is V1.3.
The previous V2.4.x files can be archived or deleted.

V1.3 - 4 SURGICAL FIXES FROM V1.2:

FIX 1: Slot root relief hole (3mm dia)
  Eliminates stress concentration at slot termination point.
  Standard machining practice for slots ending in solid material.
  Drilled at -Y end of slot, located at slot_y_start = -8.075mm.

FIX 2: Chamfer filter bug fixed
  V1.2 filter (r > 8mm) accidentally chamfered nut pocket hex edges
  due to their geometry after rotation. New filter requires:
    - Edge is horizontal (Z constant)
    - Edge is at known structural Z-level (top/bottom of body/flange/boss)
    - Edge radius matches outer cylinder OD (50/90/18 mm)
  Result: only true outer edges of top-hat profile are chamfered.

FIX 3: Dead code removed
  CLAMP_BOLT_Y_OFFSET was defined but never used. Removed.

FIX 4: SVG-code consistency
  Blueprint now shows CSK 3.2mm (was 3.0mm in V1.1+ but SVG missed update).
  Blueprint title and labels updated to V1.3.

REJECTED FROM REVIEW:
  - Slot stopping inside outer wall (would PREVENT clamp action)
  - Bolt offset architecture change (different clamp design entirely)

INHERITED FROM V1.2 (slot geometry):
  Slot crosses shaft bore cleanly with -Y material spine intact.

INHERITED FROM V1.1 (PETG print quality):
  - SHAFT_BORE 12.15mm
  - CLAMP_NUT_FLAT 8.6mm, CLAMP_NUT_H 4.8mm
  - CSK_TOP_D 10.2mm, CSK_DEPTH 3.2mm
  - CLAMP_SLOT_W 2.2mm

INHERITED FROM V1.0 (architecture):
  - Top-hat profile: 50mm body + 90mm flange + 18mm boss
  - Total height 28mm
  - 12.15mm shaft bore for FEYRINX 12mm h8
  - Split-clamp design with 2x M5 horizontal bolts
  - 4x M5 cassette mount bolts at PCD 70mm
  - Path A architecture (no pulley drilling)

HARDWARE - ALL ALREADY OWNED:
  - 2x M5 socket head cap screws ~12mm (clamp)
  - 2x M5 hex nuts (clamp nut pockets)
  - 4x M5 flathead countersunk screws ~16mm (cassette mount)
  - 4x M5 brass heat-set inserts (cassette base)
  All from B0FFSNFK3Y assortment + B0DPQJ4W3Z inserts.

PRINT SETTINGS:
  Material:     PETG (DRY)
  Layer:        0.2mm
  Perimeters:   5
  Top/bottom:   6 solid layers
  Infill:       50% Gyroid
  Orientation:  flange face DOWN on bed
  Supports:     NONE
  Speed:        40mm/s walls, 100mm/s infill

VALIDATION:
After printing, verify:
1. Slot crosses bore cleanly (not closed at outer edge)
2. Slot relief hole visible at -Y end of slot (3mm dia)
3. Outer chamfers ONLY on true outer cylinder edges
4. Nut pockets sharp/square (NOT chamfered) for proper nut grip
5. Test fit on shaft - hand pressure slides hub on
