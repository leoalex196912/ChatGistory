CSM V3 - CASSETTE HEAD COMPONENTS
====================================
Date: May 2026

This folder contains all components of the cassette head -
the knitting mechanism that sits on top of the rotating cylinder.

COMPONENT STATUS:
=================

✅ cylinder/         V1.1.1 LOCKED  (rotating shaft with 72 needle slots)
✅ cam_ring/         V6.5 FINAL     (stationary, lifts/lowers needles)
✅ sinker_ring/      V1.0 LOCKED    (holds yarn loops while needle drops)
⏳ retainer_ring/    NOT YET        (prevents loops from rising too high)
⏳ cassette_base/    NOT YET        (200mm OD support structure)

ASSEMBLY ORDER (BOTTOM → TOP):
==============================

1. Drive system (in 06_DRIVE_SYSTEM)
   - Bearing housings, drive hub, motor mount
   
2. Cylinder mounts to drive hub
   Z=0 to Z=75mm (75mm tall)

3. Cam Ring stationary around cylinder OD
   Mounted to cassette base
   
4. Sinker Ring sits on top of cylinder
   Z=75 to Z=83mm
   Sinkers project over open cylinder top

5. Retainer Ring sits above sinker ring
   Z>83mm
   
6. Cassette Base (the structural foundation)
   Holds cam ring + sinker ring + retainer ring
   Mounts to 2020 frame

DIMENSIONS REFERENCE:
=====================

Cylinder OD:        114.3mm (4.5" Legare)
Cam Ring OD:        165mm
Cam Ring ID:        115mm (clears cylinder)
Sinker Ring OD:     135mm
Sinker Ring ID:     114.8mm (0.25mm/side over cylinder)
Cassette Base OD:   200mm (planned)

KEY DESIGN DECISIONS:
=====================

✓ 72 needles, 5° pitch, 12g latch needles (FlyDesigns)
✓ 6 feeders at 60° intervals (F1-F6)
✓ Smoothstep cubic easing (cam profile + sinker tapers)
✓ Top lip in cam knit zone (V6.4+)
✓ Sinker tapering NOT removal (all 72 retained)
✓ PETG primary material, PA12 for retainer ring
