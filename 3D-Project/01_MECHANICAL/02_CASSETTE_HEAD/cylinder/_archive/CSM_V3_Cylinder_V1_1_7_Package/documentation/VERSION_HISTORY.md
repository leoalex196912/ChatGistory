# CSM V3 Cylinder Version History

| Version | Date | Critical Change |
|---|---|---|
| V1.0 | Apr 2026 | Initial 72-slot Legare-compatible design |
| V1.1 | Apr 2026 | Added cylinder spring groove (initially BOTTOM - WRONG) |
| V1.1.1 | Apr 2026 | Refined spring groove geometry (still wrong location) |
| V1.1.2 | May 2026 | Added PNG export to macro (was missing) |
| V1.1.3 | May 2026 | SLOT_CHAMFER 0.4→0.8mm, groove relocation refinement |
| V1.1.4 | May 2026 | SLOT_DEPTH 1.90→2.00mm, batch boolean optimization, wedge widths expanded |
| V1.1.4_VIZ | May 2026 | Added needle visualization (9 needles, 3 lift states) |
| V1.1.5_VIZ | May 2026 | Added FlyDesigns spring visualization (still at bottom - WRONG) |
| V1.1.6 | May 2026 | **CRITICAL FIX**: Spring moved BOTTOM→TOP per Erlbacher reference |
| V1.1.6_VIZ | May 2026 | Visualization updated for top spring |
| **V1.1.7** | **May 2026** | **PRODUCTION-READY**: Z 68→62, depth 1.2→1.8, needle position fix |
| V1.1.7_VIZ | May 2026 | Visualization with all 3 fixes applied |

## Detailed Change Log

### V1.0 → V1.1 (Spring groove added)
- Added groove for FlyDesigns Common Thickness 0.110" spring
- INITIAL POSITION WAS WRONG: placed at bottom near butt cavity
- Reasoning: incorrectly believed spring engaged the butt L-bend
- Reality: spring engages the STEM near the top

### V1.1.1 (Spring geometry refinement)
- SPRING_GROOVE_W: 3.0 → 3.2mm (PETG shrink margin)
- SPRING_GROOVE_DEPTH: 1.5 → 1.2mm (more spring exposed)
- SPRING_GROOVE_Z: refined to 17.9-21.1mm
- Still wrong position (bottom)

### V1.1.2 (PNG export fix)
- Added missing FreeCADGui.saveImage() calls
- 4 PNG renders: full ISO, full TOP, wedge ISO, wedge TOP
- No geometry changes

### V1.1.3 (Engineering review fixes)
- SLOT_CHAMFER: 0.4 → 0.8mm (better visible entry relief)
- Spring groove fixed structural overlap with butt cavity
  - Was 17.9-21.1, now (in V1.1.3 only) 15.5-18.7
- External slot flare REJECTED (kept straight slots per Legare)

### V1.1.4 (Reviewer fixes 2)
- SLOT_DEPTH: 1.90 → 2.00mm (PETG print tolerance)
- Wedge widths: [1.20, 1.20, 1.22, 1.22, 1.25, 1.25] → [1.18, 1.20, 1.22, 1.24, 1.26, 1.28]
- Batch boolean: fuse all cutters before single .cut() operation
- BUTT_DEPTH = SLOT_DEPTH (linked, was 1.90 fixed)

### V1.1.4_VIZ (Visualization with needles)
- 9 needles in 3 lift states (REST/MID/PEAK)
- Each needle has: stem, butt L-bend, hook curve, pivot, latch
- Cylinder set to 30% transparency
- Cross-section view added

### V1.1.5_VIZ (Spring visualization added)
- Added FlyDesigns spring as torus
- Still at BOTTOM groove (Z=15.5-18.7) - WRONG
- User questioned design - "how are needles held without top spring?"

### V1.1.6 (CRITICAL CORRECTION - spring moved to TOP)
- Authoritative reference: Erlbacher Knitting Machines documentation
- Spring is NOT at butt - it's near the top, engaging stems
- Spring groove relocated: Z=15.5-18.7 (bottom) → Z=66.4-69.6 (TOP)
- Bottom groove DELETED (was never correct)
- All 4 needle visualizations updated for new position

### V1.1.7 (Engineering review final fixes)
**Three fixes applied:**

**Fix #1**: Spring Z center 68 → 62mm
- More material above groove (5.4 → 11.4mm)
- Better stem leverage
- Still in classical "below hooks, above cams" zone per Erlbacher

**Fix #2**: Spring groove depth 1.2 → 1.8mm
- Spring protrusion past OD: 1.59 → 0.99mm
- Reduces yarn carrier snag risk
- Still 1.14mm engagement with stem outer edge

**Fix #3**: Needle radial position correction (visualization)
- OLD: NEEDLE_RADIAL_CENTER = CYL_OUTER_R - SLOT_DEPTH/2  (centered)
- NEW: NEEDLE_RADIAL_CENTER = CYL_OUTER_R - SLOT_DEPTH + STEM_D/2 + 0.05 (against back wall)
- Mechanically correct: spring tension pushes stem inward against slot back

## Geometry Comparison Across Versions

| Param | V1.1.4 | V1.1.6 | V1.1.7 |
|---|---|---|---|
| Spring Z center | 17.1mm | 68.0mm | **62.0mm** |
| Spring groove depth | 1.2mm | 1.2mm | **1.8mm** |
| Spring protrusion past OD | 1.59mm | 1.59mm | **0.99mm** |
| Material above groove | 53.9mm | 5.4mm | **11.4mm** |
| Material below groove | 15.5mm | 47.7mm | **37.4mm** |
| Spring engages | (butt - WRONG) | Stem | **Stem** |
| Bottom groove? | Yes (15.5-18.7) | No (deleted) | **No** |

## Status

- V1.0 through V1.1.5_VIZ: SUPERSEDED (wrong spring location)
- V1.1.6: SUPERSEDED (spring too high, groove too shallow)
- **V1.1.7: PRODUCTION-READY** (all engineering review fixes applied)
