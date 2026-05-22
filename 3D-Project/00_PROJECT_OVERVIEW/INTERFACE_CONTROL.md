# INTERFACE_CONTROL.md — CSM V3 Interface Control Document (ICD)

```
Revision:  R3
Date:      2026-05-20
Status:    Active — locked interfaces, change requires version bump on
           BOTH mating parts AND an ICD revision bump.
```

This is the **interface control document** for the CSM V3 modular
machine. It captures every mating relationship between components,
every reserved volume, and every architectural invariant that any
future change must respect.

The architecture is **frame-locked, polymer-flexible**: material
selection per component may evolve from PETG → PA12 → 6061, but the
interfaces defined here must not.

---

## ⚠ DO-NOT-BREAK INVARIANTS — MACHINE CONSTITUTION

```
═══════════════════════════════════════════════════════════════════════
LOCKED ARCHITECTURE INVARIANTS  —  BREAKING CHANGE WARNING
═══════════════════════════════════════════════════════════════════════
Modifying ANY of the following requires:
  - bumping this ICD revision (R3 → R4)
  - bumping the version of every dependent component macro
  - re-validating all 5 service envelopes
  - written justification in the ICD revision history
  - sign-off in chat-history before commit

A. DIMENSIONAL INVARIANTS
   A1.  Cylinder OD                = 114.30 mm  (Legare 4.5" standard)
   A2.  Cam Ring ID                = 115.00 mm  (0.35 mm/side clearance)
   A3.  Cam ring bolt PCD          = 155.0  mm  (6× M5, 30° offset)
   A4.  Cam ring dowel PCD         = 145.0  mm  (6× D4, alternating)
   A5.  Cassette feeder PCD        = 190.0  mm  (6× M4, 60° — shared by
                                                 feeders AND retainer)
   A6.  Cassette frame-mount PCD   = 180.0  mm  (4× M5, 45° offset)
   A7.  CYL_BOTTOM_WORLD_Z         = 181.0  mm  (world↔local transform)

B. GEOMETRIC / DATUM INVARIANTS
   B1.  Cylinder-local Z origin    = cylinder bottom face
                                     (where it sits on drive hub boss)
   B2.  CAM_DATUM_Z = 49           = cassette base bottom mating plane
                                     (cylinder-local)
   B3.  Aluminum plate top face    = WORLD MASTER DATUM (Z = 230 mm)
                                     — precision reference for cassette,
                                     drive shaft, and bearing alignment
   B4.  θ = 0°  alignment          = cylinder slot #0 ∥ +X axis
                                     = Hall sensor magnet at θ = 0°
                                     = motor side
   B5.  Coordinate handedness      = right-handed
                                     (+X motor, +Y operator, +Z up)

C. PHILOSOPHICAL / ARCHITECTURAL INVARIANTS
   C1.  Cassette = removable knitting head, mounts as ONE unit to
        the aluminum master-datum plate.
   C2.  Sock take-down column (cylinder axis, world X = Y = 0,
        from drive hub bore exit DOWNWARD through D100 hole in
        wood base) MUST remain unobstructed by motors, electronics,
        cables, or structural members.
   C3.  Service envelopes SE1–SE5 are protected volumes — no fixed
        geometry may occupy them (see §2 and SERVICE_ENVELOPES.md).
   C4.  Three-layer subsystem separation (Precision / Structural /
        Automation) is the design organizing principle. Components
        belong to exactly one layer.

Everything else in this document is revisable through normal
version-bump workflow without an ICD revision bump.
═══════════════════════════════════════════════════════════════════════
```

---

## §0  Three-Layer Architecture

CSM V3 is organized into three subsystems with different iteration
rates and tolerance requirements:

```
┌─ Layer 1: PRECISION KNITTING CORE  ────────────────────────────┐
│  Cylinder · Cam Ring · Sinker Ring · Retainer Ring ·           │
│  Cassette Base · (future) Ribber                                │
│  Iteration: SLOW. Tolerances: tight. Mounts as one removable    │
│  cassette to the master datum plate.                            │
└─────────────────────────────────────────────────────────────────┘
┌─ Layer 2: STRUCTURAL MACHINE FRAME  ───────────────────────────┐
│  Wood base · 4× 2020 uprights · Wood upper deck · Aluminum     │
│  master-datum plate · Drive hub · Bearing housings ·           │
│  12 mm shaft · Motor mount                                      │
│  Iteration: MEDIUM. Vibration isolation between Layer 3 sources │
│  and Layer 1 precision zone.                                    │
└─────────────────────────────────────────────────────────────────┘
┌─ Layer 3: AUTOMATION / CONTROL  ───────────────────────────────┐
│  NEMA 17 drive motor · HTD pulleys + belt · Feeder modules     │
│  (with NEMA 11 motors) · Electronics enclosure (Mega, TB6600,  │
│  LRS-50) · Touchscreen 7" + dual-upright mast · Yarn mast      │
│  Iteration: FAST. Mechanically isolated from Layer 1.           │
│  Touchscreen mast does NOT touch the precision frame.           │
└─────────────────────────────────────────────────────────────────┘
```

Layer assignment determines where a component is documented, what
its version bump cadence looks like, and which interfaces it can
modify. A component cannot belong to two layers.

---

## §1  Datum Chain

The single alignment chain that governs the whole machine:

```
ALUMINUM PLATE TOP FACE  (world Z = 230, master datum)
        │
        ├── Cassette Base bottom (cylinder-local Z = 49)
        │     ├── Cam Ring top (registered by PCD 155 bolts + PCD 145 pins)
        │     │     └── Cylinder OD (concentric clearance fit, 115.0/114.3)
        │     │           └── Drive Hub boss (PCD 70 bolt circle into
        │     │                                cylinder bottom inserts)
        │     │                 └── 12 mm drive shaft
        │     │                       └── Bearing housing alignment
        │     │                             └── (orthogonal to aluminum
        │     │                                  plate top normal vector)
        │     ├── Sinker register pocket (D135.30)
        │     │     └── Sinker Ring OD 135 (slip fit)
        │     └── Feeder PCD 190 + Retainer PCD 190 (shared)
        │           ├── Feeder Modules (Phase 1: 2 of 6 positions)
        │           └── Retainer Ring (uses remaining 4 positions)
        │
        └── Frame mount PCD 180 (4× M5) into aluminum plate
              └── Aluminum plate is itself bolted to wood upper deck
                    └── Wood upper deck rests on 4× 2020 uprights
                          └── Uprights bolt into wood base (Z = 18)
                                └── Wood base on rubber feet (Z = 0)
```

**Alignment rule:** the aluminum plate top face is the only true
precision plane. Wood layers below provide damping and stiffness, but
their flatness is not part of the precision chain. Cassette alignment
is set against the plate, then locked.

---

## §2  Service Envelopes (summary)

Five reserved volumes ensure the machine is serviceable in production,
not just buildable on a bench. Full definitions in
`SERVICE_ENVELOPES.md`. No fixed geometry may occupy these volumes.

| ID | Name | Purpose | Volume summary |
|---|---|---|---|
| **SE1** | Cylinder removal | Lift cylinder vertically out of cassette without disassembling cam ring or feeders | Column on cylinder axis, world Z = 272 (retainer top) up to Z ≥ 395; radius ≥ cylinder OD/2 + 5 mm |
| **SE2** | Cam ring extraction | Un-bolt cam ring from cassette base bottom and drop it off | Radial ring at world Z 212–230, D165 → D200, accessed from below |
| **SE3** | Feeder swing-out | Remove a feeder module via 2× M4 + radial slide | Per-position clearance: 60 mm radial outside PCD 190 + tool access from above at PCD 190 |
| **SE4** | Yarn threading | Operator can see + thread yarn from feeder exit to needle hook from front (+Y) | Horizontal arc at world Z 264–280, front half of cassette (Y > 0); no upright in operator hand path |
| **SE5** | Belt replacement | Slacken belt by sliding motor toward drive shaft, remove belt over pulley | Motor X-travel slot: 30 mm toward drive shaft; vertical clearance ≥ 80 mm above pulleys |

The take-down column (invariant C2) is a sixth protected volume but
conceptually a SYSTEM, not just a service envelope — see Interface 11.

---

## §3  Interfaces

Convention: **PCD** = Pitch Circle Diameter (mm). All linear units mm,
all angular units degrees.

### Interface 1: Drive Hub ↔ Cylinder

| Property | Value | Locked by |
|---|---|---|
| Mating method | Boss into pocket + bolt circle | both V2.4.2 + V3.0 |
| Concentric registration | D18.0 boss → D18.2 pocket (0.20 mm slip fit) | Drive Hub V2.4.2 |
| Bolt PCD | 70.0 | both |
| Bolt count | 4× M5 | both |
| Bolt angular offset | 45° (45/135/225/315) | both |
| Hardware | M5 brass heat-set inserts in cylinder (B0DPQJ4W3Z) | BOM_V11 |
| Bolt direction | Up from below drive hub flange, through countersinks, threaded into cylinder inserts | Drive Hub V2.4.2 |

### Interface 2: Cylinder ↔ Cam Ring

| Property | Value | Locked by |
|---|---|---|
| Mating method | Rotational concentric clearance (cylinder rotates inside stationary cam) | both V3.0 + V6.5 |
| Cylinder OD | 114.30 (invariant A1) | Cylinder V3.0 |
| Cam Ring ID | 115.00 (invariant A2) | Cam Ring V6.5 |
| Radial clearance | 0.35 mm/side | derived |
| Cam track Z range | Z=19 to Z=31 (cylinder local), engages butts | Cam Ring V6.5 + cylinder slot geometry |
| Cam lift | 8 mm (smoothstep cubic) → HOOK_PEAK_Z = 83 | Cam Ring V6.5 |
| Butt zone | within cylinder slot opening (Z = 12-75) | Cylinder V3.0 |

### Interface 3: Cam Ring ↔ Cassette Base

| Property | Value | Locked by |
|---|---|---|
| Mating method | Cam ring bolts UP from below into cassette base | both V6.5 + V1.1 |
| Bolt PCD | 155.0 (invariant A3) | both |
| Bolt count | 6× M5 | both |
| Bolt angular offset | 30° (30/90/150/210/270/330) | both |
| Pin PCD | 145.0 (invariant A4) | both |
| Pin count | 6× D4 dowels | both |
| Pin angular offset | 0° (0/60/120/180/240/300, alternating with bolts) | both |
| Cam ring top Z | 49.0 (= CAM_DATUM_Z, invariant B2) | both |

### Interface 4: Cassette Base ↔ Sinker Ring

| Property | Value | Locked by |
|---|---|---|
| Mating method | Sinker drops into register pocket on pedestal top | both V1.1 + V1.2.1 |
| Pedestal OD | 150.0 | Cassette Base V1.1 |
| Pedestal ID | 128.0 (annular) | Cassette Base V1.1 |
| Pedestal height | 12.0 (= SINKER_Z − CASSETTE_TOP_Z) | Cassette Base V1.1 |
| Register pocket diameter | 135.30 | Cassette Base V1.1 |
| Register pocket depth | 1.0 mm | Cassette Base V1.1 |
| Sinker Ring OD | 135.00 | Sinker Ring V1.2.1 |
| Slip fit clearance | 0.15 mm/side | derived |
| Sinker register plane (top of pocket) | Z = 75 (= SINKER_Z, cylinder-local) = 256 world | both |

### Interface 5: Cassette Base ↔ Feeder Modules  *(R3 update)*

| Property | Value | Locked by |
|---|---|---|
| Bolt PCD | 190.0 (invariant A5) | Cassette Base V1.1 |
| Bolt count | 6× M4 | Cassette Base V1.1 |
| Bolt angular offset | 0° (0/60/120/180/240/300) | Cassette Base V1.1 |
| Hardware | M4 brass heat-set inserts in cassette base | per material — PETG/PA12 supports inserts |
| Phase 1 active feeders | 2 (positions 0° and 180°) | architecture decision |
| Retainer Ring mount | Shares same 6 bolt pattern (positions 60/120/240/300 unused by feeders) | Interface 7 |
| Feeder motor (Phase 1) | NEMA 11 stepper (28×28×32 body) | R3 decision — replaces NEMA 8 |
| Feeder yarn exit Z (world) | 271 (= FEEDER_REFERENCE_Z + CYL_BOTTOM_WORLD_Z = 90 + 181) | provisional; validated in Phase 1.5 |
| Feeder yarn exit radius | 95 mm (approx, at PCD 190 / 2) | Feeder Module V1.0 spec |
| Service envelope | SE3 reserved per feeder position | SERVICE_ENVELOPES.md |

### Interface 6: Cassette Base ↔ Frame  *(R3 major rewrite)*

The frame is **completely re-architected** from R2. There is no longer
a "wood mid-shelf" the size of the wood base. Instead, a compact upper
deck holds the precision cassette, with all dimensions measured from
the cylinder axis (FRAME_ORIGIN_XY = (0, 0)).

| Property | Value | Locked by |
|---|---|---|
| Cassette mount bolt PCD | 180.0 (invariant A6) | Cassette Base V1.1 |
| Bolt count | 4× M5 | Cassette Base V1.1 |
| Bolt angular offset | 45° (45/135/225/315) | Cassette Base V1.1 |
| Aluminum plate (master datum) | 250 × 250 × 6 mm, 6061-T6 mill finish | R3 — replaces R2 150×150 |
| Aluminum plate top Z | 230 world (invariant B3) | R3 |
| Wood upper deck | 320 × 260 × 18 mm hardwood | R3 NEW |
| Wood upper deck top Z | 224 world | R3 |
| 2020 uprights | 4 ×, 188 mm length, at world (±150, ±120) | R3 NEW positions |
| Upright top Z | 206 world | R3 |
| Wood base | 500 × 400 × 18 mm hardwood, with D100 center take-down hole | R3 (hole NEW) |
| Wood base top Z | 18 world | R3 |
| Hardware | M5 with T-nuts in 2020 channel + M5 through wood upper deck into aluminum plate inserts | BOM_V11 (TBD final fastener spec) |

### Interface 7: Cassette Base + Sinker Ring ↔ Retainer Ring  *(unchanged from R2)*

| Property | Value | Locked by |
|---|---|---|
| Mating method | Retainer sits ABOVE sinker, mounts to cassette base via shared feeder bolts at PCD 190 | both V1.1 + V1.0 |
| Retainer Ring OD | 200.0 | Retainer Ring V1.0 |
| Retainer Ring through-bore | D118.0 | Retainer Ring V1.0 |
| Loop-control lip diameter | D104.0 effective loop aperture | Retainer Ring V1.0 |
| Lip height (from top of ring) | 2.0 mm (top portion only, ring is 8 mm total) | Retainer Ring V1.0 |
| Retainer assembly Z (bottom face, cylinder-local) | 83 = HOOK_PEAK_Z = world 264 | architecture |
| Lip underside world Z | 270 | derived |
| Hook clearance under lip | 6 mm (lip at 270-272 vs HOOK_PEAK_WORLD_Z = 264) | derived |
| Mount bolt PCD | 190.0 (SAME as cassette feeder PCD — invariant A5) | both V1.1 + V1.0 |
| Mount bolt count | 6× M4 | both |
| Phase 1 usage | Feeders at 0/180 (2 active); retainer secures at 60/120/240/300 | architecture |
| Phase 1.5 usage | All 6 bolts shared via stack-mount (bolt → cassette → spacer → retainer) | architecture |
| Spacer requirement | 6× printed spacers D8 × 20 mm (closes gap between cassette top and retainer bottom) | to design |
| Bolt length | M4 × ~50 mm (or threaded rod with nuts) | to verify when ordering |
| Material | PA12 nylon (wear surface, yarn slides on lip underside) | Retainer Ring V1.0 |

### Interface 8: Cassette Base ↔ Ribber  *(Phase 2 provision, unchanged)*

| Property | Value | Locked by |
|---|---|---|
| Bolt PCD | 140.0 | Cassette Base V1.1 (Phase 2 provision) |
| Bolt count | 6× M4 | Cassette Base V1.1 |
| Bolt angular offset | 0° (0/60/120/180/240/300) | Cassette Base V1.1 |
| Used in Phase 1? | NO — holes provisioned, capped/empty | architecture |
| Ribber assembly | NOT DESIGNED YET (deferred to Phase 2) | future |

### Interface 9: Hall Sensor Index  *(elevated in R3)*

| Property | Value | Locked by |
|---|---|---|
| Magnet PCD | 95.0 | Cylinder V3.0 |
| Magnet pocket | D6.0 × 2.2 mm deep (for B0F4KS6KV3 magnets) | Cylinder V3.0 |
| Angular position | 0° (= +X axis = motor side = Slot #0, invariant B4) | Cylinder V3.0 |
| Pulses per revolution | 1 (master index) | architecture |
| Hall sensor part | SS49E (B09MSDC3GR) | BOM_V11 |
| Hall sensor mount | TBD — on bearing housing or motor mount, must face cylinder bottom at PCD 95 | future |

**θ = 0° is the master phase reference for the entire machine.** All
feeder timing, cam phase analysis, ribber sync, and future pattern
control reference this angular origin.

### Interface 10: Touchscreen Mast ↔ Wood Base  *(R3 NEW)*

| Property | Value | Locked by |
|---|---|---|
| Mating method | Dual 2020 uprights + top crossbar, bolted to wood base via T-nuts | R3 |
| Mast base center | (X = 0, Y = −180) world | R3 |
| Mast upright spacing | X = ±30 from mast center | R3 |
| Mast upright length | 400 mm | R3 |
| Top crossbar length | 60 mm | R3 |
| Mast top Z | 418 world (= WOOD_BASE_TOP_Z + MAST_UPRIGHT_LEN) | derived |
| Touchscreen size | 165 × 100 × 10 mm (7" capacitive HDMI) | BOM |
| Touchscreen mount arm | 3D-printed, clamps to crossbar OR uprights | TBD design |
| Mechanical isolation | **NOT connected to precision frame uprights** | invariant C4 |

The touchscreen mast is part of Layer 3 (Automation/Control). Tap
forces, vibration, and resonance from the touchscreen are isolated
from the precision cassette by mounting only to the wood base.

### Interface 11: Sock Take-Down Column  *(R3 NEW)*

| Property | Value | Locked by |
|---|---|---|
| Geometry | Vertical column on cylinder axis (world X = Y = 0) | invariant C2 |
| Upper boundary | Drive hub bore exit (world Z ≈ 170) | derived |
| Lower boundary | Through D100 hole in wood base (world Z = 0 → ‑∞) | R3 |
| Wood base hole diameter | 100.0 mm | R3 |
| Hole clearance | radius 50 mm clear of any structure | R3 invariant |
| Phase 1 take-down method | Hanging weight (manual) | architecture |
| Phase 2 take-down method | Weighted claw / roller system | future |
| Phase 3 take-down method | Vacuum assist + optical length sensing | future |
| Obstruction rule | NO motors, electronics, cables, or structural members may occupy this column | invariant C2 |

Forgetting this column is the single most common architecture mistake
in DIY circular sock machines. Without it, knit fabric climbs, stitch
tension destabilizes, and dropped stitches multiply. The column is
**reserved space** even in Phase 1 where only a hanging weight uses
it.

---

## §4  Upgrade Path (Phases)

| Phase | Goal | Components added | Validation |
|---|---|---|---|
| **1** | Static architecture + 2-feeder Phase 1 build | Frame, drive train, 2 feeder modules, basic electronics, manual yarn management | Visual render proves architecture; first physical assembly |
| **1.5** | **Kinematic truth validation** (NEW gate) | None new — Blender motion study of: needle lift through 8 mm cam cycle, hook trajectory, feeder yarn intercept, retainer clearance, sinker timing | Blender animation + collision check before any feeder hardware is printed |
| **2** | 6 active feeders, color changes, ribber disk | 4 more feeder modules at 60/120/240/300, ribber assembly at PCD 140, yarn tension feedback | Multi-feed knit test, pattern complexity test |
| **3** | Closed-loop intelligent system | Vacuum take-down (in column from Interface 11), electronic patterning, automatic heel/toe shaping, optical length sensing | Production-quality sock output |

Each phase's components mount via interfaces defined here. No phase
requires re-architecting the precision core, the frame, or the
coordinate system. This is enabled by the invariants section above.

---

## §5  Locked Versions

| Component | Version | Layer | Macro file |
|---|---|---|---|
| Cylinder | V3.0 | 1 | `02_CASSETTE_HEAD/cylinder/freecad_macros/CSM_V3_Cylinder_V3_0.FCMacro` |
| Cam Ring | V6.5 (FINAL) | 1 | `02_CASSETTE_HEAD/cam_ring/freecad_macros/CSM_V3_CamRing_V6_5.FCMacro` |
| Sinker Ring | V1.2.1 (LOCKED) | 1 | `02_CASSETTE_HEAD/sinker_ring/freecad_macros/CSM_V3_SinkerRing_V1_2_1.FCMacro` |
| Cassette Base | V1.1 | 1 | `02_CASSETTE_HEAD/cassette_base/freecad_macros/CSM_V3_CassetteBase_V1_1.FCMacro` |
| Retainer Ring | V1.0 (LOCKED) | 1 | `02_CASSETTE_HEAD/retainer_ring/freecad_macros/CSM_V3_RetainerRing_V1_0.FCMacro` |
| Drive Hub | V2.4.2 (Done) | 2 | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_DriveHub_V2_4_2.FCMacro` |
| Motor Mount | V1.3 (Done — may need V1.4 for new layout) | 2 | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_MotorMount_V1_3.FCMacro` |
| Bearing Housings | V2.5 (Done) | 2 | `05_BEARINGS_SHAFT/freecad_macros/CSM_V3_BearingHousings_V2_5.FCMacro` |
| Wood Base | V1.0 (NEEDS V1.1 — add D100 take-down hole) | 2 | `CSM_V3_ASSEMBLY/frame/wood_base/freecad_macros/CSM_V3_WoodBase_V1_0.FCMacro` |
| Wood Upper Deck | **NOT YET** | 2 | to build at `CSM_V3_ASSEMBLY/frame/wood_upper_deck/` |
| Aluminum Plate | V1.0 (NEEDS V1.1 — resize 150 → 250) | 2 | `CSM_V3_ASSEMBLY/frame/mount_plate_6061/freecad_macros/CSM_V3_MountPlate6061_V1_0.FCMacro` |
| 2020 Upright | V1.0 (NEEDS V1.1 — shorten 267 → 188, reposition) | 2 | `CSM_V3_ASSEMBLY/frame/upright_2020/freecad_macros/CSM_V3_Upright2020_V1_0.FCMacro` |
| Touchscreen Mast | **NOT YET** | 3 | to build at `CSM_V3_ASSEMBLY/frame/touchscreen_mast/` |
| NEMA 17 motor (drive) | V1.0 (built) | 3 | `CSM_V3_ASSEMBLY/drive_bought/nema17_stepper/` |
| HTD pulleys + belt | NOT YET | 3 | `CSM_V3_ASSEMBLY/drive_bought/` |
| Bearings + shaft | NOT YET | 3 | `CSM_V3_ASSEMBLY/bearings_bought/` |
| Feeder Module | **NOT YET** | 3 | to build at `CSM_V3_ASSEMBLY/feeder_module/` |
| Electronics (Mega/TB6600/PSU) | NOT YET | 3 | `CSM_V3_ASSEMBLY/electronics/` |
| Touchscreen 7" | NOT YET | 3 | `CSM_V3_ASSEMBLY/electronics/touchscreen_7in/` |
| Ribber (Phase 2) | provisioned only | 1 | future |

---

## How to Use This Document

**When designing a new component:**
1. Identify which layer (1/2/3) it belongs to
2. Find every interface this component touches (e.g. Feeder Module → I5)
3. Copy the locked values exactly into the component's macro parameter section
4. Verify your component does not intrude into any SE1–SE5 service envelope or the Interface 11 take-down column
5. Do NOT modify locked values without going through the change process below

**When proposing an interface change:**
1. Determine whether the change touches an invariant in the DO-NOT-BREAK block. If yes, it is a full ICD revision (R3 → R4).
2. Identify all mating parts that depend on the interface
3. Decide whether to absorb the change in one part or split between both
4. If split, bump BOTH parts' versions
5. Update this document; update `MACHINE_DATUMS.md` if a datum shifted
6. Re-validate all 5 service envelopes
7. Commit all changes together with a clear message describing what changed and why

---

## Revision History

| Rev | Date | Changes |
|---|---|---|
| R1 | 2026-05-17 | Initial ICD. Captures interfaces 1-9 from locked V3 architecture. |
| R2 | 2026-05-17 | Lock Interface 7 with Retainer Ring V1.0 final geometry. Retainer OD = 200 (was 172, fixed for bolt PCD compatibility). All other interfaces unchanged. |
| R3 | 2026-05-20 | Major architectural revision. (a) NEW DO-NOT-BREAK invariants block (machine constitution); (b) NEW §0 three-layer architecture; (c) NEW §1 datum chain; (d) NEW §2 service envelopes SE1–SE5 (summary; full doc in `SERVICE_ENVELOPES.md`); (e) Interface 5 updated (NEMA 11 feeder motors, FEEDER_REFERENCE_Z 78→90 provisional); (f) Interface 6 major rewrite (frame architecture: wood base 500×400 w/ D100 hole + 4× 2020 uprights at ±150 ±120 × 188 mm + wood upper deck 320×260×18 + aluminum plate 250×250×6 master datum). The R2 "wood mid-shelf 500×400" is DELETED; (g) Interface 9 elevated (θ=0° = master phase reference); (h) NEW Interface 10 (Touchscreen Mast — dual 2020, isolated from precision frame); (i) NEW Interface 11 (Sock Take-Down Column — D100 through wood base, reserved space invariant); (j) NEW §4 Phase 1/1.5/2/3 upgrade path with kinematic-validation gate at 1.5; (k) §5 locked-versions refreshed with layer assignment + new components flagged NEEDS V1.1 or NOT YET. |

---

## Cross-References

- **Coordinate authority:** `MACHINE_COORDINATE_SYSTEM.md` (R1)
- **Dimensional reference:** `MACHINE_DATUMS.md` (R2 final)
- **Service envelopes (full):** `SERVICE_ENVELOPES.md` (next deliverable)
- **Project overview:** `~/.claude/projects/C--3D-Project/memory/project_csm_v3_overview.md`
- **BOM:** `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`
- **Phase 1.5 kinematic script:** future `full_assembly/blender_scripts/needle_motion_study.py`
