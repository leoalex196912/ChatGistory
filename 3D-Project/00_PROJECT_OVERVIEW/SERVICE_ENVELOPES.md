# SERVICE_ENVELOPES.md — CSM V3 Reserved Service Volumes

```
Revision:  R1
Date:      2026-05-20
Status:    Active — protected volumes. No fixed geometry may occupy.
```

This document defines the **five service envelopes** that the CSM V3
machine reserves to remain serviceable in production, not just buildable
on a bench.

A service envelope is a **3D volume in world coordinates** reserved for
a maintenance operation (cylinder removal, belt replacement, etc.).
Within an envelope, **no fixed geometry may exist** — no structural
member, no motor, no electronics box, no wire harness, no decorative
element. Transient occupants (the moving part of a service operation,
e.g. the cylinder being lifted along SE1) are permitted; permanent
occupants are not.

Service envelopes are first-class architectural objects, equal in
weight to physical components. They are referenced by:

- `INTERFACE_CONTROL.md` (R3) §2 (summary table)
- Every component macro that mentions a clearance value
- Phase 1.5 kinematic validation script (collision check)
- Blender assembly renders (semi-transparent visualization in
  service-view mode)

---

## Schema (used for every envelope below)

```
SE# | Name
═══════════════════════════════════════════════════════════
PURPOSE              what maintenance op the envelope enables
PROTECTED VOLUME     world-coord bounding region
ENTRY DIRECTION      which axis/face the operator/tool approaches
                     from
TOOL ACCESS          what physical access is required to perform op
PROHIBITED GEOMETRY  what shall NOT exist in this volume
FUTURE-RISK NOTES    Phase 2/3 components that could regress this
                     envelope if not designed against it
```

---

## SE1  |  Cylinder Removal

```
PURPOSE
  Lift the cylinder vertically out of the cassette to:
   - replace a broken needle
   - swap to a different gauge (12g → 14g) cylinder
   - clean lint accumulation in slot bottoms
   - inspect spring groove or needle butt wear

  Must be possible WITHOUT disconnecting:
   - touchscreen mast wiring
   - touchscreen mast itself
   - any of the 4× 2020 precision uprights
   - feeder module wiring harnesses
   - drive belt (only the cylinder bolts to drive hub need to release)
   - electronics enclosure

  Releasing 4× M5 cylinder-to-drive-hub bolts (Interface 1) is the
  only required disassembly. Then cylinder lifts straight up.

PROTECTED VOLUME
  Vertical column on cylinder axis (world X=Y=0):
    Lower:  Z = 272 mm (top of retainer ring, after retainer removed)
    Upper:  Z = 430 mm (max machine height per poster spec)
    Radius: 60 mm    (cylinder OD/2 = 57.15 + 3 mm hand-clearance)
  Volume ≈ π·(60²)·158 ≈ 1.78 × 10⁶ mm³

  Note: retainer ring is removed first via 6× M4 bolts at PCD 190
  (Interface 7). SE1 reserves clearance AFTER retainer is off, for
  the cylinder lift itself.

ENTRY DIRECTION
  Vertical from above (+Z). Operator stands at +Y front, reaches
  over the cassette assembly. Cylinder lifts straight up out of cam
  ring without rotation.

TOOL ACCESS
   - 4 mm hex driver from below to release Drive Hub bolts (Interface 1)
   - hand grip on cylinder top face for lifting
     (cylinder is ~520 g in PETG, ~1.5 kg if production aluminum)
   - optional: M5 eye-bolts threaded into 2 of the 4 heat-set inserts
     for a lifting handle / lanyard

PROHIBITED GEOMETRY
  No fixed structure within the column at Z = 272..430, radius 60 mm.
  Specifically:
   - no horizontal members
   - no cable runs
   - no decorative bridges
   - no future ribber ring (see future-risk below)
   - no overhead yarn-guide arm

FUTURE-RISK NOTES
  SE1 RISK A: Phase 2 ribber disk
    A ribber that mounts ABOVE the cassette could block cylinder lift.
    Mitigation: ribber must either (a) mount BELOW the cassette base
    (using Interface 8 PCD 140 from below), or (b) be removable as a
    pre-step with a quick-release (single tool, < 30 s).

  SE1 RISK B: Phase 3 vacuum take-down hood
    A vacuum cap covering the cylinder top would prevent lifting.
    Mitigation: vacuum hood must be a separate Phase 3 module that
    disconnects independently before SE1 is invoked.

  SE1 RISK C: Touchscreen arm overhang
    If the touchscreen arm articulates forward over the cassette, it
    could enter the column. Mitigation: arm geometry must respect a
    "no-fly zone" of X = ±60, Y = ±60 at Z ≥ 272.
```

---

## SE2  |  Cam Ring Extraction

```
PURPOSE
  Un-bolt the cam ring from cassette base bottom and drop it off
  the cylinder. Required to:
   - replace cam ring (production upgrade PETG → 6061)
   - inspect cam track for wear
   - clean cam track of yarn / lint debris
   - upgrade to a different cam profile (e.g. tighter knit / looser
     knit cam variants)

  Cylinder must remain in place (or SE1 is invoked first). Cam ring
  is annular and slides radially outward over the cylinder OD once
  bolts are released.

PROTECTED VOLUME
  Annular ring at world Z = 200..230 (cam ring vertical span):
    Inner radius: 82.5  mm  (cam ring ID/2 = 57.5 + cylinder clearance)
    Outer radius: 110.0 mm  (cam ring OD/2 = 82.5 + 27 mm hand)
  Plus tool-access cone from below:
    Apex at world (0, 0, 175) (drive hub flange level)
    Base radius 90 mm at Z = 200

ENTRY DIRECTION
  Bolt access: from below (-Z), through the gap between drive hub
  flange (world Z 165 ish) and cassette base bottom (Z=230).
  Radial extraction: lateral (any direction) once bolts are out.

TOOL ACCESS
   - 4 mm hex driver, 90 mm reach minimum, to access 6× M5 bolts at
     cam ring PCD 155 from below
   - both hands free to support the cam ring (weight ~200 g PETG,
     ~800 g 6061 aluminum) during radial slide

PROHIBITED GEOMETRY
  Below cassette base (Z = 200..230, radius 82..110):
   - no motor mount can occupy this annular band
   - no electronics can be positioned within the access cone
   - no cable bundle may cross the cam ring extraction radial path
   - the 4× 2020 uprights are at radius √(150² + 120²) ≈ 192 mm —
     well outside the 110 mm boundary, so they're safe

FUTURE-RISK NOTES
  SE2 RISK A: Motor mount V1.4 redesign
    The current Motor Mount V1.3 was designed for an older Z layout.
    The new V1.4 must NOT occupy the annular access band at radius
    82..110, Z 200..230.

  SE2 RISK B: Sock take-down hardware (Phase 2)
    Weighted claw or roller cartridge mounted below cassette could
    block the tool-access cone. Mitigation: take-down hardware must
    mount at world Z < 165 (below drive hub flange) OR be a quick-
    release module that detaches before SE2.

  SE2 RISK C: Phase 2 ribber
    If ribber mounts to Interface 8 (PCD 140 below cassette base), it
    occupies exactly the access cone for SE2. Ribber must be removable
    in < 30 s as a quick-release.
```

---

## SE3  |  Feeder Swing-Out

```
PURPOSE
  Remove or install a single feeder module at any of 6 PCD-190
  positions (0/60/120/180/240/300°). Required to:
   - upgrade from Phase 1 (2 feeders) to Phase 2 (6 feeders)
   - replace a failed feeder
   - swap yarn type per feeder (different cone)
   - clean tensioner/yarn guide
   - service the NEMA 11 feeder motor

  Each feeder must be removable independently — installing one feeder
  shall not require disturbing any other.

PROTECTED VOLUME
  Per-position wedge at world Z = 224..295 (from upper deck top to
  yarn cone height area), at PCD 190 ± 30° (60° angular wedge per
  feeder), radial extent from 70 mm to 155 mm (PCD 190/2 − 25 mm
  inward to PCD 190/2 + 60 mm outward).

  Six wedges total, one per feeder position. Wedge centers at
  θ = 0°, 60°, 120°, 180°, 240°, 300°.

ENTRY DIRECTION
  Tool: from above (+Z) — hex driver to 2× M4 bolts at PCD 190.
  Module extraction: radial outward (away from cylinder axis).
  Re-installation: radial inward, then bolt-down from above.

TOOL ACCESS
   - 3 mm hex driver, 120 mm reach minimum, vertical from above to
     M4 bolts at PCD 190 (height: feeder top at Z ~ 295)
   - both hands to grip feeder module during slide
   - eye line from operator (+Y) to see the feeder position being
     serviced; back feeders (θ = 120, 180, 240) require leaning over

PROHIBITED GEOMETRY
  Within each feeder wedge:
   - no decorative element (yarn cone from adjacent feeder must not
     overhang into neighbor wedge)
   - no wire harness laid on top of the cassette base in this band
   - no Phase 2 ribber arm reaching outward past PCD 165

  Across all 6 wedges: feeder envelopes do not overlap each other
  (60° wedge width × 6 = 360°, exact tiling).

FUTURE-RISK NOTES
  SE3 RISK A: Adjacent feeder bodies
    At full Phase 2 (6 feeders installed), each feeder's swing-out
    arc must not collide with the next feeder's body. Feeder module
    V1.0 design must constrain its lateral footprint to a 50°
    angular wedge (leaving 10° clearance to each neighbor's wedge).

  SE3 RISK B: Yarn cone overhang
    A yarn cone wider than the feeder base could overhang into the
    next feeder's wedge. Specification: yarn cone OD ≤ 75 mm at the
    base (i.e. ≤ 1.25 × cone post diameter).

  SE3 RISK C: Phase 2 wiring density
    6 feeder motors → 6 wiring bundles. These bundles must not cross
    a feeder wedge from above, or SE3 becomes a 2-handed cable-
    juggling exercise. Wiring runs must descend vertically along an
    upright, not laterally across the cassette top.

  SE3 RISK D: SE4 collision (yarn threading path)
    Front-facing feeders (θ near 0°, the operator-side direction) must
    leave SE4 yarn threading arc clear. See SE4.
```

---

## SE4  |  Yarn Threading Access

```
PURPOSE
  Operator must be able to see and reach into the yarn path to thread
  yarn manually: from feeder yarn exit, through tensioner, through the
  yarn guide, down to the needle hook capture zone.

  Threading is a frequent operation (every cone change, every yarn
  break, every machine start-up). Friction here multiplies operator
  cost over the machine's life.

PROTECTED VOLUME
  Front arc at world Z = 264..295 (hook-peak plane up to cone top),
  spanning +Y half of cassette circumference: from θ = 270° (right-
  front) through θ = 0° (front-center, but note θ=0° is +X axis here)
  ... wait, θ here is the cassette angular coordinate. Let me restate:

  The "operator side" is the +Y direction. Threading access protected
  arc spans the half of the cassette circumference facing +Y:
   - radial extent: from cylinder OD (radius 57) outward to PCD 190
     (radius 95) plus 50 mm hand reach beyond = radius 145
   - vertical extent: world Z = 240..300
   - angular extent: 180° arc centered on +Y (so all "front" feeder
     positions and the operator's hand path are protected)

ENTRY DIRECTION
  From operator standing position at Y = +400 mm (in front of the
  machine), looking and reaching in the −Y direction. Hand path
  approaches yarn from the front, going forward and slightly down.

TOOL ACCESS
   - operator's hands (both)
   - operator's eyes — uninterrupted line of sight from standing
     height (~1500 mm above floor) down to the cassette top
   - no need for tools; threading is hand work

PROHIBITED GEOMETRY
  Front half of cassette top zone (+Y side):
   - no structural upright in the hand path (the 4× precision-frame
     uprights are at corners ±150, ±120 — none in the +Y centerline)
   - touchscreen mast at Y = −180 is on the back side, safely clear
   - no cable harness running across the front of the cassette
   - no yarn cone positioned to block the visual sight line from
     above (cones at front feeder positions must be coaxial with the
     feeder post, not laterally displaced)

FUTURE-RISK NOTES
  SE4 RISK A: Feeder wiring bundles
    Wiring from feeders to electronics must descend ALONG an upright
    on the −Y (back) side, NOT cross the front of the cassette.

  SE4 RISK B: Phase 2 patterning indicator lights
    LED status indicators (per feeder) must mount on the rear or top
    face of the feeder body, not project forward into the threading
    arc.

  SE4 RISK C: Touchscreen arm articulation
    If the touchscreen arm tilts forward toward the operator, it
    must not enter the threading arc. Arm range of motion to be
    constrained to Z ≥ 310 (above the threading arc upper limit).
```

---

## SE5  |  Belt Replacement

```
PURPOSE
  Slacken the HTD 5M timing belt by sliding the NEMA 17 drive motor
  toward the drive shaft, then lift the belt off both pulleys. Required
  to:
   - replace a worn or broken belt
   - swap belts (e.g. 380 mm pitch length → 400 mm if motor offset
     changes)
   - inspect pulley teeth for wear or debris
   - clean belt of yarn/lint contamination

PROTECTED VOLUME
  Motor X-travel slot: rectangular volume at world Y = −100, Z = 18..58
  (wood-base top to NEMA 17 body top), X = 60..120 (motor body footprint
  travels from current X=90 toward drive shaft).

  Plus vertical clearance above both pulleys:
   - Drive shaft pulley (60T) at world (0, 0, ~80): clear column up to
     Z ≥ 160 with radius 60 mm
   - Motor pulley (16T) at world (90, -100, ~80): clear column up to
     Z ≥ 160 with radius 25 mm

ENTRY DIRECTION
  Operator: from front (+Y) reaching back to motor area.
  Tool: from motor side (+X, accessible from machine side) for motor
  mount bolts.
  Belt removal: lift belt upward (+Z) over each pulley once tension
  is released.

TOOL ACCESS
   - 4 mm hex driver to release motor mount bolts (sliding bolts in
     slotted mount)
   - hands to grip belt and lift over pulleys
   - clear visual access to motor mount slot from front (+Y) or side
     (+X)

PROHIBITED GEOMETRY
  In the motor X-travel slot (X = 60..120, Y = −100, Z = 18..58):
   - no electronics module
   - no wire bundle anchored in this band
   - no decorative element

  Above the pulleys (Z = 80..160, on cylinder axis and motor axis):
   - no cross-brace between uprights at this height
   - no horizontal wiring run
   - no Phase 2 hardware (ribber arm, vacuum tube) crossing this band

FUTURE-RISK NOTES
  SE5 RISK A: Touchscreen mast pulley collision
    Touchscreen mast is at world Y = −180. Motor pulley is at Y = −100.
    Distance 80 mm. If the touchscreen mast crossbar were ever lowered
    to motor pulley height (Z ~80), the mast would enter the belt
    removal arc. Mitigation: mast crossbar locked at Z ≥ 200 OR mast
    moved further back.

  SE5 RISK B: Phase 2 ribber drive
    If the Phase 2 ribber gets its own drive belt/pulley set, the second
    belt's removal envelope must not overlap SE5. Either share the
    drive belt (kinematically chain ribber off the main shaft) or place
    ribber drive on the opposite side (X = −90).

  SE5 RISK C: Cable routing
    Power and signal cables from NEMA 17 must enter from the +X side
    (motor side), descending vertically to wood-base channel, not
    crossing the belt area. Cables must have enough service loop to
    allow the 30 mm motor travel without strain.
```

---

## Implicit Reservation: Sock Take-Down Column

The take-down column is defined in **Interface 11** (ICD R3) as a
**system**, not a service envelope — but the same "no fixed
geometry" rule applies. For completeness:

```
PURPOSE       Sock fabric must hang from cylinder bore exit (world
              Z ≈ 170) DOWN through the wood base D100 hole and
              beyond.
VOLUME        Vertical cylinder on world (0, 0): radius 50 mm,
              Z = 170 down to Z = -∞ (below the machine).
PROHIBITED    No motor, electronics, cable, structural member, or
              future Phase 3 sensor may occupy this column except as
              part of the take-down mechanism itself.
FUTURE        Phase 2: weighted claw or roller (within the column)
              Phase 3: vacuum-assist tube (within the column)
              Both are PART of the column system, not violations.
```

This is documented here for completeness; the primary specification
lives in `INTERFACE_CONTROL.md` R3 Interface 11.

---

## Combined-Envelope Rule

No service envelope may overlap another in a way that requires
sequential service operations. Specifically:

- SE1 (cylinder removal) is independent of SE2 (cam ring extraction).
  Either can be performed without invoking the other.
- SE3 (feeder swing-out) is independent of SE4 (yarn threading).
  Threading does not require feeder removal; removal does not require
  threading.
- SE5 (belt replacement) is mechanically isolated from all cassette
  operations (SE1-SE4) by the upper deck. None of the cassette
  envelopes intrude below the upper deck where SE5 lives.

**The take-down column is the one volume that intersects multiple
envelopes** — it passes through the cassette area (intersecting SE1
column from above) and continues down through the wood base. This is
acceptable because SE1 only protects Z ≥ 272 and the take-down
column is most relevant at Z ≤ 170 (inside cylinder bore and below).
The intersection at Z = 170..272 is the cylinder bore interior,
which is part of normal machine operation, not a service envelope
conflict.

---

## Future Service Envelopes (placeholder)

When Phase 2/3 components are added, this document will gain:

- **SE6: Ribber removal** (Phase 2) — extract ribber disk from
  Interface 8 PCD 140 mount
- **SE7: Vacuum hood swing-aside** (Phase 3) — disconnect vacuum
  assembly from take-down column to invoke SE1

Each new envelope follows the same 6-field schema and must be
checked against the combined-envelope rule.

---

## Cross-References

- **Coordinate authority:** `MACHINE_COORDINATE_SYSTEM.md` R1
- **Dimensional reference:** `MACHINE_DATUMS.md` R2 final
- **Interface control:** `INTERFACE_CONTROL.md` R3 (§2 summary, §3 details)
- **Phase 1.5 kinematic validation:** future
  `00_PROJECT_OVERVIEW/full_assembly/blender_scripts/needle_motion_study.py`

---

## Revision History

| Rev | Date | Changes |
|---|---|---|
| R1 | 2026-05-20 | Initial service-envelope document. Defines SE1–SE5 with the standard 6-field schema (purpose, protected volume, entry direction, tool access, prohibited geometry, future-risk notes). Includes the explicit clauses: SE1 cylinder removal does not require disconnecting touchscreen mast, uprights, or feeder wiring; SE5 includes 30 mm motor X-travel for belt tensioning. Implicit take-down-column reservation cross-referenced to ICD R3 Interface 11. Placeholders for future SE6 (ribber) and SE7 (vacuum hood). |
