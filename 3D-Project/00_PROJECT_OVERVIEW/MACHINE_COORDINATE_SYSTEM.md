# MACHINE_COORDINATE_SYSTEM.md — CSM V3 Coordinate Standard

```
Revision:  R1
Date:      2026-05-20
Status:    Active — all macros, Blender assemblies, animations, and
           documentation MUST follow this convention.
```

This is the **single coordinate authority** for the CSM V3 project. It
governs both static geometry (FreeCAD macros, STL exports) and dynamic
behavior (Blender animations, kinematic studies). Anything that places
a part, aims a camera, defines a motion, or labels a measurement
references this document.

The architecture is **frame-locked, polymer-flexible** — material may
change (PETG → PA12 → 6061), but the coordinate frame and interface
geometry do not. This document defines the frame.

---

## 1. Two coordinate frames

CSM V3 uses **two** named coordinate frames that coexist:

| Frame | Origin | Used for |
|---|---|---|
| **World** | cylinder axis ∩ aluminum plate top | full machine assembly, frame, drive train, feeders, electronics, touchscreen mast, service envelopes, Blender renders |
| **Cylinder-local** | cylinder axis ∩ cylinder bottom face (drive hub interface) | cassette internals (cylinder, cam, sinker, retainer, cassette base), needle motion, hook trajectory |

Each frame is referenced explicitly in macros by suffix:
`SOMETHING_Z` → local; `SOMETHING_WORLD_Z` → world.
Never mix.

---

## 2. Axis convention (right-handed)

```
+Z   upward (gravity-opposing)
+X   motor side       (NEMA 17 drive motor at X = +90)
−X   service side     (cylinder removal tool access)
+Y   operator / front (operator stands at +Y, faces machine looking in −Y)
−Y   rear / utility   (touchscreen mast at Y = −180, motor offset to Y = −100)
```

**Handedness:** right-handed (X × Y = +Z). When in doubt, point right
hand fingers from +X toward +Y; thumb gives +Z.

**Angular convention (cylinder rotation θ):**
- θ = 0° aligned with +X axis (motor side, Hall sensor reference, cylinder Slot #0)
- θ increases counter-clockwise looking from +Z (standard mathematical convention)
- Slot N is at θ = N × 5.0° (72 slots × 5° = 360°)

---

## 3. Origin definitions

### World origin (Z = 0, X = 0, Y = 0)

**Z = 0**: bottom face of the wood base, where the rubber feet make contact
with the table. Equivalently: top of the table the machine sits on.

**X = 0, Y = 0**: cylinder rotation axis projected onto Z = 0. The
cylinder, drive hub, and drive shaft all share the X = Y = 0 axis line.

### Cylinder-local origin

**Z = 0** in cylinder-local coords: bottom face of the cylinder
(where it sits on the drive hub boss).

**X = Y = 0** in cylinder-local: cylinder rotation axis. Coincides
with world X = Y = 0. The two frames differ **only in Z offset**.

---

## 4. World ↔ Cylinder-local transform

```python
# LOCKED CONSTANT -- governs all world↔local conversions
CYL_BOTTOM_WORLD_Z = 181.0   # mm

# Convert any cylinder-local Z to world Z:
def world_z(local_z):
    return local_z + CYL_BOTTOM_WORLD_Z

# Convert any world Z to cylinder-local:
def local_z(world_z_val):
    return world_z_val - CYL_BOTTOM_WORLD_Z
```

**X and Y coordinates are identical in both frames** (both share the
cylinder axis as their (0, 0) line).

The offset 181 mm is derived from:
- Wood base 18 mm (Z=0..18) + uprights 188 mm + wood upper deck 18 mm + aluminum plate 6 mm
- Aluminum plate top = 18 + 188 + 18 + 6 = 230 mm world Z
- Cassette base bottom (cylinder-local Z = 49 = CAM_DATUM_Z) sits ON that plate top
- World Z of cylinder local Z = 0  =  230 − 49 = **181 mm**

---

## 5. Derived world Z constants

Computed from cylinder-local datums (`MACHINE_DATUMS.md`) using
`world_z(local_z)`:

| Feature | Local Z (mm) | World Z (mm) | Source |
|---|---:|---:|---|
| Wood base bottom | — | 0 | this doc |
| Wood base top | — | 18 | this doc |
| Top of 4× uprights / wood upper deck bottom | — | 206 | this doc |
| Wood upper deck top | — | 224 | this doc |
| Aluminum plate top / cassette base bottom | 49 | 230 | CAM_DATUM_Z |
| Cassette base outer disc top | 63 | 244 | CASSETTE_TOP_Z |
| Cylinder bottom | 0 | 181 | CYLINDER_Z0 |
| Cylinder top / sinker register plane | 75 | 256 | CYLINDER_TOP_Z / SINKER_Z |
| Sinker ring top | 83 | 264 | SINKER_Z + sinker_height |
| Retainer ring bottom (= hook peak plane) | 83 | **264** | HOOK_PEAK_Z |
| Retainer ring top | ~91 | ~272 | retainer V1.0 geometry |
| Feeder reference (provisional, Phase 1.5 will validate) | 90 | 271 | FEEDER_REFERENCE_Z |
| Max machine height (touchscreen + cone envelope) | — | 430 | poster target |

**Note:** `HOOK_PEAK_WORLD_Z = RETAINER_BOTTOM_WORLD_Z = 264`. The
needle hook peaks exactly at the retainer entrance plane. The retainer
lip then governs loop rise above that point. This is intentional and
intuitive — knits work because the hook reaches the loop transfer
plane at the peak of the cam cycle.

---

## 6. Cylinder angular phase (θ)

For kinematic studies (Phase 1.5 and beyond), cylinder rotation drives
needle motion. We standardize the following phase variables:

| Variable | Meaning | Domain |
|---|---|---|
| `θ` | cylinder angular position | 0° .. 360° (periodic) |
| `Z_needle(θ)` | needle vertical displacement, cam-driven | varies through cam cycle |
| `Y_feed` | yarn entry tangent direction (feeder-relative) | fixed per feeder position |
| `hook_open(θ)` | latch state (open / closed) — placeholder boolean until validated | 0 / 1 |
| `sinker_phase(θ)` | sinker timing offset relative to needle phase — placeholder for future ribber sync | radians |

Phase 0 (θ = 0°) places **Slot #0 at the Hall sensor index magnet**
(see ICD R3 Interface 9). This is also the +X direction.

Direction convention for cylinder rotation: **CCW looking from above**
(looking in −Z direction). This is the standard direction Erlbacher
and tru-knit machines run.

---

## 7. Kinematic notation for Phase 1.5 Blender study

When animating the cassette in Blender (Phase 1.5 milestone), use this
notation in script constants:

```python
# Cylinder angular position (degrees, runtime-variable)
THETA_DEG = 0.0

# Cam-driven needle motion (cylinder local Z, varies with theta)
# Cam track engages butts at cylinder local Z = 19..31 (per ICD I2)
# Cam lift = 8 mm (smoothstep cubic, per Cam Ring V6.5)
CAM_LIFT_MAX = 8.0
HOOK_REST_LOCAL_Z = 75.0    # needle hook resting (cam low)
HOOK_PEAK_LOCAL_Z = 83.0    # needle hook at peak lift (cam high)

# Yarn entry vector (feeder centerline → cylinder centerline,
# horizontal at FEEDER_REFERENCE_Z + adjustment)
YARN_ENTRY_RADIUS = 95.0    # feeder yarn exit at radius 95 (per feeder design)
YARN_DROP_ANGLE_DEG = 30.0  # yarn descent angle below horizontal toward hook
```

These constants become the input to the Phase 1.5 motion-validation
script, which animates a single needle through 360° of cylinder
rotation and renders the resulting hook trajectory.

---

## 8. Service envelope alignment

Service envelopes (defined in `SERVICE_ENVELOPES.md`) are specified
in **world coordinates only**. They are reserved volumes — no fixed
geometry may occupy them. Examples:

- **SE1 (cylinder removal):** vertical column above the cassette,
  centered on world X = Y = 0, from Z = 272 (retainer top) to Z = 395+.
- **SE5 (belt replacement):** horizontal slot at world Z ≈ 220 (drive
  belt centerline) allowing 30 mm motor X-travel toward the drive shaft.

The transform in section 4 lets cassette-local features and
world-frame envelopes coexist deterministically.

---

## 9. Cross-references

- **Datum dimensions:** `MACHINE_DATUMS.md` (cylinder-local)
- **Interface control:** `INTERFACE_CONTROL.md` (R3 and later)
- **Service envelopes:** `SERVICE_ENVELOPES.md`
- **Phase 1.5 kinematic validation:** future
  `00_PROJECT_OVERVIEW/full_assembly/blender_scripts/needle_motion_study.py`

---

## 10. Change control

Any change to:
- Axis convention
- Origin location
- `CYL_BOTTOM_WORLD_Z` value
- Angular convention (CW/CCW or θ=0 alignment)

...is **architecturally breaking**. It must:
1. Bump this document's revision (R1 → R2)
2. Be propagated to all 11+ existing macros simultaneously
3. Update every world-coord reference in Blender scripts
4. Update `MACHINE_DATUMS.md` and `INTERFACE_CONTROL.md` cross-refs

In practice, this document should not change after R1 except to add
clarifications. Pick a coordinate frame and stay with it.

---

## Revision History

| Rev | Date | Author | Changes |
|---|---|---|---|
| R1 | 2026-05-20 | leoalex196912 | Initial coordinate standard. Locks world frame, cylinder-local frame, world↔local transform (CYL_BOTTOM_WORLD_Z = 181 mm), angular convention, and Phase 1.5 kinematic notation. |
