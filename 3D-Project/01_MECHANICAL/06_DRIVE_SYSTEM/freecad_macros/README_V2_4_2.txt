CSM V3 - DRIVE HUB V2.4.2 (SLOT GEOMETRY FIX)
================================================
Date: April 2026

Macro: CSM_V3_DriveHub_V2_4_2.FCMacro

V2.4.2 SINGLE CHANGE: Clamp slot geometry corrected

THE ISSUE WITH V2.4.1:
The V2.4.1 slot started at Y=0 (shaft center) and extended outward
to Y=+26 (past +Y outer edge). The code COMMENT claimed a 6mm
material bridge below the shaft, but the actual geometry didn't
match - the slot terminated AT the shaft center, leaving a thin
sliver of material at the slot bottom.

THE FIX:
V2.4.2 slot extends from Y=-8.075 to Y=+26.0
- Slot CLEANLY CROSSES the shaft bore (Y = ±6.075)
- 2mm overshoot on -Y side past bore edge (clean print)
- 17mm of material remains on -Y side as structural 'spine'
- Clamp action works correctly: bolts squeeze +Y closed, gripping shaft

WHY THIS MATTERS:
1. Geometry now matches stated design intent
2. Cleaner print (no thin material slivers)
3. Symmetric clamp deflection (predictable behavior)
4. Same clamp force, better mechanical reliability

INHERITED FROM V2.4.1 (PETG print refinements):
- SHAFT_BORE 12.15mm (PETG-safe)
- CLAMP_NUT_FLAT 8.6mm (tighter grip)
- CLAMP_NUT_H 4.8mm (deeper trap)
- CSK_TOP_D 10.2mm (margin)
- CSK_DEPTH 3.2mm (full flush)
- CLAMP_SLOT_W 2.2mm (more clamp travel)

EVERYTHING ELSE UNCHANGED FROM V2.4:
- Top-hat profile: 50mm body + 90mm flange + 18mm boss
- Total height: 28mm
- Path A architecture (no pulley drilling)
- 4x M5 cassette mount bolts at 70mm PCD
- 2x M5 horizontal clamp bolts

PRINT/ASSEMBLY: Same as V2.4.1 (see prior README)

VERIFICATION:
The slot should be visible in FreeCAD as a 2.2mm wide channel that:
- Extends from one outer edge of the body
- Goes through the shaft bore
- Stops 2mm past the opposite side of the bore
- Does NOT reach the opposite outer edge

If the part appears split into two pieces, you have the V2.4 bug - 
re-run V2.4.2.
