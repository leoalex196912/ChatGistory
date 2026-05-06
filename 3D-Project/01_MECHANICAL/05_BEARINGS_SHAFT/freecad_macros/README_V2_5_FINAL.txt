CSM V3 - BEARING HOUSINGS V2.5 (FINAL with documentation fixes)
=================================================================
Date: April 2026

Macro: CSM_V3_BearingHousings_V2_5.FCMacro

DOCUMENTATION FIXES APPLIED (post-review):
  1. Console output: "[V2.3 NEW]" -> "[V2.5 NEW]" (was leftover from V2.3)
  2. Console output: "Force at 0.5mm = 30N" -> "Force at 3.20mm = 35N"
     (was V2.4 leftover, now matches actual V2.5 preload target)
  3. SVG label: "solid PETG top (~10.5mm)" -> "(~3.1mm in V2.5)"
     (was wrong even in V2.4 - actual was 6.8mm; V2.5 actual is 3.1mm)
  4. Spacer tube length: confirmed 22.9mm everywhere (no 30.8 references)

OPTIONAL IMPROVEMENT NOT APPLIED:
  - Extended spring guidance lip (0.5-1mm extra wall before chamfer)
  - Reviewer marked as "optional/nice upgrade"
  - Current 5.5mm pocket already provides 5.5mm guidance even at free height
  - Following "stop polishing, start printing" principle

SPRING CONTAINMENT VERIFIED:
  Free height (zero load):      Spring 6.63mm, in 5.5mm pocket = 5.5mm guided
  At 35N preload (3.20mm comp): Spring 3.43mm, 2.07mm pocket walls above spring
  At 50N max load:              Spring 2.06mm, 3.44mm pocket walls above spring
  Spring is well-guided through entire compression range.

==========================================
KEY V2.5 VALUES (ALL VERIFIED CONSISTENT)
==========================================
SPRING_TARGET_F       = 35 N
SPRING_COMPRESSION    = 3.20 mm
SPRING_OPERATING_H    = 3.43 mm
SPRING_FREE_H         = 6.63 mm
SPRING_WORK_H         = 2.06 mm (50N max - DO NOT EXCEED)
SPRING_RATE           = 10.94 N/mm
SPRING_POCKET_D       = 25.7 mm
SPRING_POCKET_H       = 5.5 mm
SPRING_POCKET_CHAMFER = 0.5 mm
SPACER_POCKET_D       = 28.10 mm (matches bearing pocket)
SPACER_POCKET_H       = 1.6 mm
SPACER_TUBE_LEN       = 22.9 mm
SPACER_TUBE_TOL       = 0.1 mm
BLOCK_GAP             = 11.0 mm
PRELOAD_MARGIN        = 1.37 mm to work height (70% of max)

==========================================
HARDWARE ORDER LIST
==========================================
1. Smalley CM25-L1 wave springs x 2
   Source: smalley.com/wave-spring/cm25-l1
   Try free samples first!

2. Spacer washers x 2 (specs: 19 ID x 28 OD x 1.6mm, 18-8 SS)
   Source: McMaster-Carr (call 630-833-0300 for exact match)

3. Aluminum tube (optional, PETG print works for prototype)
   Spec: 18mm OD x 12mm ID, cut to 22.9mm

4. Wood base 420 x 320 x 18mm
   Source: Home Depot or local lumber

ALL OTHER HARDWARE: already in inventory (see BOM V9)
