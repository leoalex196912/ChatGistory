# CSM V3 Cylinder V1.1.7

## Status: PRODUCTION-READY (engineering review fixes applied)

## Project Location
`C:\3D-Project\01_MECHANICAL\02_CASSETTE_HEAD\cylinder\`

## Files In This Package

```
CSM_V3_Cylinder_V1_1_7_Package/
├── freecad_macros/
│   ├── CSM_V3_Cylinder_V1_1_7.FCMacro        (production - generates STL)
│   └── CSM_V3_Cylinder_V1_1_7_VIZ.FCMacro    (visualization with needles+spring)
├── blueprints/
│   └── Cylinder_V1_1_7_Blueprint.svg          (ready-to-view standalone SVG)
├── images/
│   (PNGs generated when you RUN the macro on Windows FreeCAD)
├── STL_outputs/
│   (STLs generated when you RUN the macro on Windows FreeCAD)
└── documentation/
    ├── README.md                              (this file)
    ├── VERSION_HISTORY.md
    └── CHAT_HISTORY_LATEST.txt
```

## Critical Specifications

| Parameter | Value | Notes |
|---|---|---|
| Cylinder OD | 114.3mm | Legare 4.5" standard |
| Cylinder ID | 88.0mm | Bore for drive hub |
| Height | 75.0mm | Total axial length |
| Slot count | 72 | Standard adult sock |
| Slot W × D | 1.22 × 2.00mm | For 12g needle ribbon |
| Slot length | 52.0mm | Stem zone |
| Slot chamfer | 0.8mm | Lead-in at top (V1.1.3 fix) |
| Butt cavity | 8.5 × 4.0mm | At Z=19-23mm (cam zone) |
| Spring groove Z | 60.4-63.6mm | Center Z=62mm (V1.1.7 fix) |
| Spring groove depth | 1.8mm | Less protrusion (V1.1.7 fix) |
| Hub pocket | 18.20mm × 3mm | Mates V1.3 drive hub |
| Bolts | 4× M5 @ PCD 70mm | Counterbored from below |
| Edge chamfer | 0.6mm | Top and bottom OD |

## Hardware Required

- **Cylinder spring**: FlyDesigns Common Thickness 0.110" / 2.79mm wire (purchased)
- **Needles**: 72× FlyDesigns AutoKnitter/Legare 12G (have 100)
- **Bolts**: 4× M5 socket head from screw kit
- **Loctite 603**: For bolt thread retention

## How To Use The Macros

### Step 1: Move files to project location
Copy these files to:
```
C:\3D-Project\01_MECHANICAL\02_CASSETTE_HEAD\cylinder\freecad_macros\
```

### Step 2: Run production macro
1. Open FreeCAD GUI (NOT freecadcmd headless)
2. Menu: Macro → Macros... 
3. Select `CSM_V3_Cylinder_V1_1_7.FCMacro`
4. Click Execute

This generates:
- `CSM_V3_Cylinder_V1_1_7_FULL.stl` (production cylinder)
- `CSM_V3_Cylinder_V1_1_7_TESTWEDGE.stl` (print first!)
- 4× PNG renders in `images/`
- 1× SVG blueprint in `blueprints/`

### Step 3: Run visualization macro (optional - to inspect with needles+spring)
Run `CSM_V3_Cylinder_V1_1_7_VIZ.FCMacro` to see the cylinder with 9 needles and the FlyDesigns spring rendered. Generates 5 additional PNG views including cross-section.

## Print Sequence (CRITICAL)

### Step 1: Print test wedge FIRST
- File: `CSM_V3_Cylinder_V1_1_7_TESTWEDGE.stl`
- Time: 30-45 minutes
- Material: ~10g PETG
- Settings:
  - Layer height: 0.20mm (or 0.16mm for higher precision)
  - Walls: 5
  - Top/bottom: 6 layers
  - Infill: 40% gyroid
  - Orientation: cylinder upright (axis Z)
  - Supports: NONE
  - Speed: ~40mm/s walls

### Step 2: Test fit
Insert a needle in each slot pair:
- Slots 1-2: 1.18mm (tightest)
- Slots 3-4: 1.20mm
- Slots 5-6: 1.22mm (TARGET)
- Slot 7: 1.24mm
- Slot 8: 1.26mm
- Slot 9: 1.28mm (loosest)

Each needle should:
- Slide smoothly up/down (no binding)
- Not rattle excessively (no slop)
- Spring back when flexed

Also verify:
- FlyDesigns spring fits in groove
- Spring wire centerline at Z=62mm
- Spring protrudes ~1mm past cyl OD

### Step 3: Print full cylinder
- File: `CSM_V3_Cylinder_V1_1_7_FULL.stl`
- Time: 4-6 hours
- Material: ~120g PETG
- Same settings as test wedge

If test wedge showed a different optimal slot width, edit `SLOT_WIDTH` in the macro and regenerate before printing full cylinder.

## Assembly Notes

1. Apply Loctite 603 to all 4 M5 bolts
2. Place cylinder onto V1.3 drive hub (boss enters pocket)
3. Insert M5 bolts through cylinder counterbores into hub
4. Tighten cross-pattern to ~5 Nm
5. Allow Loctite 603 to cure 24h
6. Install FlyDesigns spring:
   - Wrap around cylinder OD in spring groove (Z=60.4-63.6mm)
   - Twist ends together to close ring (per FlyDesigns instructions)
7. Insert needles from TOP of cylinder:
   - Lead-in chamfer guides needle
   - Push needle butt L into butt cavity
   - Spring should hold needle stem inward against back wall
8. Verify all 72 needles slide freely
9. Verify spring tension holds needles when cylinder tilted

## Validation

After assembly:
- [ ] Cylinder rotates smoothly on bearings (no binding)
- [ ] All 72 needles slide freely in slots
- [ ] Spring holds needles inward (no falling out when tilted)
- [ ] Hook clearance above cylinder top: ~2.5mm at rest
- [ ] Needle butts protrude past cylinder OD into cam ring path

## Version History

| Version | Date | Key Change |
|---|---|---|
| V1.0 | Apr 2026 | Initial 72-slot design |
| V1.1 | Apr 2026 | Added spring groove (initially at bottom - WRONG) |
| V1.1.1 | Apr 2026 | Refined spring groove dimensions |
| V1.1.2 | May 2026 | Added PNG export |
| V1.1.3 | May 2026 | Larger chamfer (0.4→0.8), groove relocation |
| V1.1.4 | May 2026 | Slot depth 1.90→2.00, batch boolean, wedge widths |
| V1.1.5 (viz) | May 2026 | Added spring visualization (still at bottom) |
| V1.1.6 | May 2026 | **Spring moved BOTTOM→TOP per Erlbacher reference** |
| **V1.1.7** | **May 2026** | **Z 68→62mm, depth 1.2→1.8, needle position fix** |

## Engineering Review Fixes In V1.1.7

**Fix #1**: Spring Z center 68mm → 62mm
- Better stem leverage (more lever arm)
- Material above groove: 5.4mm → 11.4mm (stronger top edge)

**Fix #2**: Spring groove depth 1.2mm → 1.8mm
- Spring protrusion: 1.59mm → 0.99mm
- Reduces yarn carrier snag risk

**Fix #3**: Needle radial position (visualization)
- Stems now positioned against back wall of slot
- Mechanically correct (spring naturally pushes needles inward)

## Z-Axis Layout (Final)

```
Z=75.0  ━━━━━━━━━━━━━ Cylinder TOP
        ━━ chamfer ━━
        |
        | 11.4mm solid material
        |
Z=63.6  ┃━━━━━━━━━━━┃ Spring groove TOP
Z=62.0  ┃    ●━━●    ┃ ← FlyDesigns 0.110" spring
Z=60.4  ┃━━━━━━━━━━━┃ Spring groove BOTTOM
        |
        | Stem zone (slot continues below)
        |
Z=23.0  ━━━━━━━━━━━━━ Slot bottom
Z=23.0  ┃   Butt    ┃ Butt cavity (8.5×4mm)
Z=19.0  ┃  cavity   ┃ (engaged by CAM ring)
        |
        | Solid base
        |
Z=0     ━━━━━━━━━━━━━ Cylinder BOTTOM (hub pocket)
```
