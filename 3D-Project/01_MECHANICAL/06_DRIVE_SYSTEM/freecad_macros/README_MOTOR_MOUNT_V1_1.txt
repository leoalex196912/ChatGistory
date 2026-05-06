CSM V3 - NEMA 23 MOTOR MOUNT V1.1
====================================
Date: April 2026

Macro: CSM_V3_MotorMount_V1_1.FCMacro

V1.1 CHANGES FROM V1.0 (review-driven refinements):

ACCEPTED FROM REVIEW:
  1. RIB_T 4mm -> 6mm
     Rigidity insurance against motor weight (1.5kg) + belt tension load.
     Cube-of-thickness rule: 50% thicker rib = ~3.4x flex resistance.
     ~5g extra material, 10 minutes more print time. Pure win.

  2. MOTOR_BOLT_CSK_D 10.2 -> 11.0mm
     Counterbore now properly fits M5 washer.
     Prevents PETG creep at bolt-head contact area.

  3. FOOT_SLOT_HEAD_D 10.2 -> 11.0mm
     Same fix for foot slots.

REJECTED FROM REVIEW:
  - Slot Y spacing 60 -> 40mm (reviewer assumed different frame)
    User confirmed 420x320 base with rails at +/-30mm = 60mm spacing.
    KEPT at 60mm.
  - Slot friction relief pockets (adjustment doesn't depend on smooth slide)
  - Reduce to 2 slots (4 needed for moment resistance; reviewer agreed)

DEFERRED FROM REVIEW (V1.2 if testing reveals need):
  - Fillet rib bases (FreeCAD makeFillet fragile on fused complex parts)
    Print and test V1.1 first. If flex observed, add fillets in V1.2.

CONFIRMED OK FROM V1.0:
  - Bolt length 16mm gives 8mm engagement in gearbox (adequate)
  - 4 slots correctly resist motor torque pivoting moment
  - Belt tension math: 97.3mm nominal, 30mm slot adjustment range

==========================================
FRAME LAYOUT (your 420x320x18mm base)
==========================================

Mount 2x 2020 aluminum extrusions ON TOP of wood base, parallel:

       420mm long (X axis)
   <-------------------------->
   +--------------------------+
   |                          |
   |      Rail 2 (Y=+30)      |  ^
   |   ====================   |  |
   |                          |  |
   |   [bracket span 100mm]   |  | 320mm wide
   |                          |  | (Y axis)
   |   ====================   |  |
   |      Rail 1 (Y=-30)      |  |
   |                          |  v
   +--------------------------+
   <- 18mm thick hardwood base ->

Rail spec:
  - 2x 2020 extrusions (B0D89YS5VP), ~400mm long each
  - Mounted parallel, 60mm center-to-center
  - Use M5 dowel pins or wood screws to attach extrusion to wood base
  - Run along 420mm (X) direction

Bracket on rails:
  - 100mm wide foot bridges both rails
  - 4 bolts in foot: 2 per rail
  - Bolts engage top T-slot via T-nuts (B0GG4N5GR4)
  - Bracket slides along X for belt tension

==========================================
COMPLETE BUILD SEQUENCE
==========================================

1. Print bracket (V1.1 macro)
2. Cut 2x 2020 extrusions to length (~400mm each)
3. Mount extrusions to wood base at +/-30mm Y spacing
4. Slide T-nuts into rail top slots
5. Place bracket on rails, loose-tighten foot bolts
6. Mount NEMA 23 + gearbox to plate
7. Install pulley on gearbox shaft
8. Wrap belt, slide bracket to tension
9. Tighten foot bolts

HARDWARE (all already owned):
  - 4x M5 SHCS ~16mm (motor)
  - 4x M5 SHCS ~12mm + 4x M5 T-nuts (foot)
  - 4-8x M5 washers (under SHCS heads, prevents PETG creep)

PRINT SETTINGS: same as V1.0
  - PETG, 0.2mm layer, 5 perimeters, 50% Gyroid
  - Foot face DOWN
  - ~3 hours, ~150g material
