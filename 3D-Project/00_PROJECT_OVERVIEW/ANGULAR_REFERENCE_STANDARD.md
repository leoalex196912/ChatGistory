# ANGULAR_REFERENCE_STANDARD.md — CSM V3 Top-View Angular Convention

```
Revision:  R1
Date:      2026-05-20
Status:    Active — canonical angular reference. Locks all angular
           positions on the cylinder, cam ring, sinker, retainer,
           cassette base, feeder modules, sensors, and assembly
           coordinates.
```

This document is the **canonical angular reference** for CSM V3. It
exists because the project has three coexisting angular conventions
that can otherwise drift apart:

1. **Cartesian axis convention** — `+X = motor side, +Y = operator
   side` (from `MACHINE_COORDINATE_SYSTEM.md`).
2. **Cylinder angular coordinate θ** — defined relative to +X axis
   (θ = 0° aligned with +X, ICD R3 invariant B4).
3. **Human / operator intuition** — "front" naturally feels like
   θ = 0° to humans, even though it isn't in this machine.

Without an explicit canonical reference, every future feeder
position, sensor placement, ribber sync calculation, and pattern
control script risks getting the angular wrong by 90°.

---

## Canonical Top View

The diagram below is **the** reference. All component layouts must
match this orientation.

```
                  −Y (rear / utility side)
                       │
              θ = 270°│
                       │
       Touchscreen Mast (X=0, Y=−180)
                       │
                       │
                       ●─────────────────────● ← upright (+150, −120)
                  ╲   │   ╱
                   ╲  │  ╱
                    ╲ │ ╱
   Service      Motor│Motor Pulley (16T) @ (+90, −100)
   side (−X) ╌╌╌╌╌╌╌╌●╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌●╌╌╌╌╌╌╌→  +X (motor side)
   θ=180°            │                          θ=0°
                    ╱ │ ╲                        ↑
                   ╱  │  ╲                       │
                  ╱   │   ╲                Hall sensor @ θ=0°
              θ = 90° │                    Slot #0       @ θ=0°
                       │                    (NOT at operator front)
                       │
              ●─────────────────────● ← upright (+150, +120)
                       │
                       │
                  +Y (operator / front)
                       │
                       │
                  ▲ Operator stands here

  Cylinder rotation: CCW looking from +Z (= above)
  i.e. θ increases counter-clockwise when viewed from above.
```

### Key callouts on this diagram

| Position | World (X, Y) | Angle θ | Role |
|---|---|---|---|
| +X axis | (positive, 0) | **0°** | Hall sensor index, Slot #0, motor pulley side |
| +Y axis | (0, positive) | **90°** | Operator / front (where you stand to thread yarn) |
| −X axis | (negative, 0) | 180° | Service side (cylinder removal tool access) |
| −Y axis | (0, negative) | 270° | Rear / utility (touchscreen mast, motor body) |
| Motor pulley | (+90, −100) | atan2(−100, 90) ≈ 312° | NEMA 17 drive pulley center |
| Touchscreen mast | (0, −180) | 270° | Y < 0, exactly on −Y axis |
| Take-down column | (0, 0) | undefined (on axis) | sock exit, all phases |

---

## The "θ=0° is NOT front" rule

**This is the single most important clause in this document.**

Humans intuitively assume:
- "front of machine" = θ = 0°
- "feeder 1 (front-right)" = θ ≈ 30°
- "0° rotation = no rotation = pointing forward"

In CSM V3, **none of those are true**. The conventions are:

- **Front of machine = operator side = +Y axis = θ = 90°** (not 0°)
- **θ = 0° is the motor side (+X axis), aligned with the cylinder's
  Hall index magnet and Slot #0.** This is the master phase reference
  for the entire machine.
- "Zero rotation" of the cylinder (θ = 0°) means Slot #0 is pointing
  at the motor, NOT at the operator.

This convention was chosen because the Hall sensor and Slot #0 are
**physical features** that must align with a specific axis, while
"front" is a label that can move. Anchoring θ = 0° to the physical
Hall index gives a hardware-grounded reference. The operator-front
convention is layered on top as `OPERATOR_THETA = 90°`.

If you ever find yourself writing code that assumes "front = θ = 0°",
you have a bug. Convert via:
```python
OPERATOR_FRONT_THETA = 90.0   # NEVER 0
```

---

## Slot Numbering on Cylinder

72 slots on the cylinder, indexed 0–71. Slot #N is at angular
position:
```
slot_angle(N)  =  N × (360° / 72)  =  N × 5°
```

Therefore:
| Slot # | θ (deg) | Direction |
|---:|---:|---|
| 0 | 0 | +X (motor side, Hall index here) |
| 18 | 90 | +Y (operator front) |
| 36 | 180 | −X (service side) |
| 54 | 270 | −Y (rear / mast) |

Slot numbering increases **counter-clockwise** viewed from above
(matches cylinder rotation direction). At cylinder rotation phase
θ_cyl = 0°, Slot #0 sits at +X and produces the Hall index pulse.
After 5° of cylinder rotation (CCW), Slot #1 has moved to where
Slot #0 was; Slot #0 has moved 5° CCW (now at θ_machine = 5°).

---

## Bolt-Pattern Angular Positions (canonical)

All angular offsets reference the machine frame (+X axis = 0°), not
the cylinder.

| Pattern | PCD | Count | θ positions (deg) | Used by |
|---|---:|---:|---|---|
| Cylinder ↔ Drive Hub | 70 | 4 | **45, 135, 225, 315** (45° offset) | Interface 1 |
| Cam ring bolts | 155 | 6 | **30, 90, 150, 210, 270, 330** (30° offset) | Interface 3 |
| Cam ring dowels | 145 | 6 | **0, 60, 120, 180, 240, 300** (0° offset, alternates with bolts) | Interface 3 |
| Feeder mounts / Retainer | 190 | 6 | **0, 60, 120, 180, 240, 300** (0° offset) | Interfaces 5, 7 |
| Frame mounts | 180 | 4 | **45, 135, 225, 315** (45° offset) | Interface 6 |
| Ribber mounts | 140 | 6 | **0, 60, 120, 180, 240, 300** (0° offset) | Interface 8 (Phase 2) |

These angular offsets are part of the locked invariants. Changing
them affects mating components and requires an ICD revision bump.

---

## Feeder Position Numbering (Phase 1 + Phase 2)

Six feeder positions at PCD 190 (Interface 5). Numbered F1–F6 by
their θ angle:

| Feeder | θ (deg) | Direction | Phase 1 active? |
|---|---:|---|---|
| **F1** | 0 | +X (motor side) | ✓ YES |
| F2 | 60 | front-right (between +X and +Y) | — Phase 2 |
| F3 | 120 | front-left (between +Y and −X) | — Phase 2 |
| **F4** | 180 | −X (service side) | ✓ YES |
| F5 | 240 | rear-left (between −X and −Y) | — Phase 2 |
| F6 | 300 | rear-right (between −Y and +X) | — Phase 2 |

**Phase 1 active feeders: F1 (θ=0°, motor side) and F4 (θ=180°,
service side).** They are diametrically opposite — providing the
cleanest 2-feed knit pattern.

Phase 1 inactive positions (F2, F3, F5, F6) are used by the Retainer
Ring V1.0 mounting bolts (per Interface 7 shared bolt pattern). When
upgrading to Phase 2 six-feeder configuration, the retainer is
re-mounted using stack-mount spacers so that all 6 bolts serve both
feeder + retainer simultaneously.

---

## Why Phase 1 Feeders Are at F1/F4, Not Front/Back

A common future temptation is to put the two Phase 1 feeders at
"front" and "back" (i.e. θ = 90° and θ = 270°, F2.5/F5.5 — which
aren't actual feeder positions). This is **wrong** because:

1. The retainer ring mounts in 4 of 6 PCD-190 positions. If feeders
   take F2.5 / F5.5, those aren't real bolt holes — the retainer
   could only use 4 of the 6 (already a constraint), and feeders
   would have NO bolt holes.
2. The 6-position grid is locked at θ = 0°, 60°, 120°, 180°, 240°,
   300°. Feeders can ONLY go at those angles.
3. F1 + F4 (diametrically opposite) provides the simplest 2-feed
   pattern: yarn enters from both sides 180° apart. This is how
   Erlbacher and tru-knit machines run their 2-feed configuration.

So the operator threads yarn from the side (motor side or service
side), not from the front. The front is reserved for operator hand
access (SE4 yarn threading envelope).

---

## Cylinder Rotation Direction

```
Rotation direction:    CCW looking from +Z (above)
                       i.e. cylinder rotates from +X toward +Y
                       in the top-down view.

Equivalent statements:
   - At θ_cyl = 0°: Slot #0 is at machine +X axis (motor side)
   - At θ_cyl = 90°: Slot #0 has moved to machine +Y axis (front)
                     Slot #18 is now at +X axis (passes Hall sensor)
   - At θ_cyl = 360° (full rotation): all slots have returned home,
                                       72 Hall pulses have occurred
                                       (actually 1 pulse — Slot #0
                                       passes Hall once per revolution)
```

The Hall index fires **once per cylinder revolution**, when Slot #0
crosses the +X axis sensor position.

Motor → cylinder gear ratio is 60:16 = 3.75. So:
- Motor 1 revolution = 1/3.75 of cylinder revolution
- For Slot #0 to make one full revolution, motor turns 3.75 times.
- Motor rotation direction must be set so that the cylinder rotates
  CCW viewed from above. Motor rotation direction depends on:
  belt routing (parallel run vs crossed), motor wiring (A+/A−, B+/B−),
  and stepper driver micro-step direction setting.
- This is calibrated at first power-up, not pre-determined here.

---

## Operator Position and Sight Lines

```
Operator standing position:        ~ (X=0, Y=+400, Z=1500)
Operator eye height:               ~ 1500 mm above floor
Operator-to-cassette distance:     ~ 400 mm
Cassette top in operator FOV:      world Z 230..295 (cassette stack)

Touchscreen position (mast):       world (0, -180, ~400 ish)
   Note: touchscreen is BEHIND cassette from operator POV.
         Operator looks PAST cassette to see touchscreen.
         Or touchscreen tilts forward toward operator via arm.

Operator threading direction:      hands enter from +Y toward −Y
                                   (forward into the machine).
```

---

## Common Mistakes (DO NOT)

1. **DO NOT** assume θ = 0° is the operator front. It is the motor
   side. Front is θ = 90° (+Y).
2. **DO NOT** number feeders F1..F6 starting from the front. F1 is
   at θ = 0° (motor side), not at the operator side.
3. **DO NOT** place sensors at θ = 0° unless they are the Hall index.
   That angular slot is reserved for the master phase reference.
4. **DO NOT** orient the touchscreen mast on the +Y side ("front") —
   it goes on the −Y side ("rear") so the operator can stand at +Y
   without the mast blocking their view of the cassette.
5. **DO NOT** rotate the machine 90° in Blender for a "better camera
   angle" without rotating the coordinate diagram with it. The
   coordinate system is part of the machine, not a render setting.
6. **DO NOT** write code that converts angles incorrectly between
   cylinder-local rotation θ_cyl and machine-frame angular position
   θ_machine. They coincide at θ_cyl = 0°, then diverge.

---

## Cross-References

- **Coordinate authority:** `MACHINE_COORDINATE_SYSTEM.md` R1
- **Dimensional reference:** `MACHINE_DATUMS.md` R2 final
- **Interface control:** `INTERFACE_CONTROL.md` R3 — especially
  invariant B4 (θ = 0° at +X) and Interface 9 (Hall sensor),
  Interface 5 (Feeder PCD 190 with 0° offset)
- **Service envelopes:** `SERVICE_ENVELOPES.md` R1 — SE4 (yarn
  threading on operator side, +Y direction)

---

## Revision History

| Rev | Date | Changes |
|---|---|---|
| R1 | 2026-05-20 | Initial angular reference standard. Locks: top-view diagram, "θ=0° is NOT front" rule, slot numbering (Slot #N at N×5°), bolt-pattern angular positions for all 7 patterns, feeder position numbering F1–F6 with Phase 1 active = F1 (θ=0°) and F4 (θ=180°), cylinder CCW rotation direction, operator position assumptions, common mistakes list. Created to prevent angular semantic drift between Cartesian axes, cylinder θ, and human "front" intuition. |
