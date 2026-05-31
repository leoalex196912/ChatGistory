# INTERFACE_CONTROL.md — CSM V3 Interface Control Document (ICD)

```
Revision:  R6
Date:      2026-05-24
Status:    Active — locked interfaces, change requires version bump on
           BOTH mating parts AND an ICD revision bump.
           R6 elevates Interface 11 (Take-Down Column) to "stitch-
           formation parameter" status -- Phase 1.5 D-4b proved
           take-down tension is coupled to capture stability, not
           independent of it. Also formalizes the Phase-2 automated
           take-down architecture (dual-roller servo nip system) and
           explicitly classifies the Phase-1 hanging weight as a
           bring-up / debug / calibration tool, not a production
           solution.
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
   A8.  Shaft bearing stack        = floating-top, fixed-bottom
                                     (Interface 12) -- lower thrust
                                     bearing resolves axial load;
                                     upper bearing free for thermal growth

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

### Interface 5: Cassette Base ↔ Feeder Modules  *(R4 update — actuator change)*

| Property | Value | Locked by |
|---|---|---|
| Bolt PCD | 190.0 (invariant A5) | Cassette Base V1.1 |
| Bolt count | 6× M4 | Cassette Base V1.1 |
| Bolt angular offset | 0° (0/60/120/180/240/300) | Cassette Base V1.1 |
| Hardware | M4 brass heat-set inserts in cassette base | per material — PETG/PA12 supports inserts |
| Phase 1 active feeders | 2 (positions F1 θ=0° and F4 θ=180°) | architecture decision (ANGULAR_REFERENCE_STANDARD) |
| Retainer Ring mount | Shares same 6 bolt pattern (positions 60/120/240/300 unused by feeders) | Interface 7 |
| **Feeder actuator (Phase 1)** | **MG90S metal-gear servo (22.8×12.2×28.5 body, 32 mm tab-to-tab)** | R4 — matches BOM V11 (8× purchased: 6 active + 2 spare). REPLACES the R3 NEMA 11 spec. |
| Servo control signal | PWM 50 Hz, 1.0–2.0 ms pulse, 180° rotation | MG90S spec |
| Servo power | 6 V (via LM2596 buck from 24 V S-250 PSU) | BOM B008BHB4L8 |
| Feeder yarn exit Z (world) | 271 (= FEEDER_REFERENCE_Z + CYL_BOTTOM_WORLD_Z = 90 + 181) | provisional; validated in Phase 1.5 |
| Feeder yarn exit radius | 95 mm (approx, at PCD 190 / 2) | Feeder Module V1.0 spec |
| Service envelope | SE3 reserved per feeder position | SERVICE_ENVELOPES.md |

**R4 Note:** The feeder module 3D-printed enclosure (currently
`FeederModule V1.0` with a 28×32 mm motor cavity) needs **V1.1** to
fit the MG90S servo (smaller cavity 23×13 mm with 2× M2 mounting
tabs at 28 mm pitch). Cavity and bolt-pattern change only — the
external footprint and PCD 190 mount geometry unchanged.

**R5 Design Rule — Feeder Control Philosophy:**
MG90S servos introduce backlash, positional uncertainty, PWM timing
jitter, and gear wear. Phase 1 feeder logic must treat servos as
**"guided yarn presentation,"** not as "precision synchronized
textile actuation." Specifically:
- ✅ ACCEPTABLE: yarn guide positioning, tension modulation, simple
  swing-in / swing-out of feeder fingers, color-change selection.
- ❌ NOT ACCEPTABLE in Phase 1: needle-by-needle synchronized
  selection (per-stitch jacquard), high-frequency yarn cutting,
  precision-timed yarn injection mid-stitch.
- Phase 2 may upgrade to NEMA-class steppers for selected feeders
  if precision selection becomes a requirement. Bolt pattern at
  PCD 190 is unchanged, so the swap is per-feeder without
  architectural impact.

### Interface 6: Cassette Base ↔ Frame + Drive Motor  *(R4 update — motor change)*

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
| Hardware | M5 with T-nuts in 2020 channel + M5 through wood upper deck into aluminum plate inserts | BOM_V11 |
| **Drive motor** | **NEMA 23 + 5:1 planetary gearbox (23HS22-2804S-HG5)** | R4 — replaces R3 NEMA 17 |
| Drive motor body | 57×57×56 mm + 50 mm gearbox = 106 mm total length | NEMA 23 + HG5 spec |
| Drive motor mount | 4× M5 at PCD square 47.14 mm | NEMA 23 frame |
| Drive motor position | World (X=+90, Y=−100, Z_bot=18) | MD.MOTOR_X/Y/Z |
| Drive belt | HTD 5M, 405 mm pitch length, 15 mm wide (kit B0C6Y1462P) | BOM_V11 |
| Drive pulleys | 60T (gearbox, 14 mm bore) + 20T (drive shaft, 12 mm bore) | BOM_V11 |
| Total reduction | 5 × 3 = **15:1** motor → cylinder | gearbox + belt |

**R4 Note:** `Motor Mount V1.3` was designed for NEMA 17 geometry
(M3 mount PCD 31). NEMA 23 has M5 mount PCD 47.14. **Motor Mount
needs V1.4** to accommodate the larger NEMA 23 + gearbox stack.
Existing Motor Mount V1.3 STL is now obsolete for the drive train
(may be reusable for other purposes).

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

### Interface 12: Shaft / Bearing Stack  *(R5 NEW — formalization)*

The 12 mm drive shaft connects the gearbox-driven 20T pulley (bottom)
to the Drive Hub V2.4.2 (top, which drives the cylinder). The shaft
passes through `BearingHousings V2.5` (top + bottom pair). Until R5
this stack was implied; R5 formalizes the axial constraint strategy.

**Architecture: floating top, fixed bottom.**

```
Drive Hub V2.4.2  (top of shaft)
  └ pressed onto / clamped on shaft top
     ↑ shaft Z = drive hub bottom Z

     ░ 12 mm drive shaft (FEYRINX h8, B08HX2LG53, 300 mm) ░

UPPER bearing 6001-2RS   ── floating axially
  │ inside upper bearing housing seat
  │ axial gap on both sides (no preload from above)
  │ rotates freely; absorbs shaft thermal growth
  ↓

LOWER bearing 6001-2RS   ── axially fixed
  │ inside lower bearing housing seat
  │ inner race clamped between shaft collar (above) and 51101 thrust (below)
  ↓
51101 thrust bearing     ── axial load path
  │ takes upward cassette/yarn force AND downward belt-pull component
  │ sits between lower 6001 inner race and shaft collar #2
  ↓
Shaft collar #2 (12 mm)  ── axially clamps the stack
  │ B0DMMB1FHF
  │ tightened against thrust bearing inner race
  ↓
Pulley HTD 20T (12 mm bore)
  │ pinned/grub-screwed to shaft
  │ sits BELOW the lower bearing -- belt overhang below frame
  ↓ shaft bottom
```

**Why floating-top, fixed-bottom:**
- Axial load on shaft is primarily DOWNWARD (cassette weight + yarn tension + belt-pull component) → resolved at lower thrust bearing
- Upward load is small (only momentary during yarn pull-up events) → also resolved at lower thrust (51101 takes load in both directions)
- Upper bearing is purely RADIAL — no axial constraint → allows shaft thermal growth without binding
- Belt side-load on shaft below lower bearing → cantilever moment; lower bearing handles the radial component, upper bearing stabilizes the moment couple

| Property | Value | Locked by |
|---|---|---|
| Shaft | FEYRINX 12 mm h8 hardened, 300 mm length, ground finish | BOM B08HX2LG53 |
| Upper bearing | 6001-2RS (28 OD × 12 ID × 8 W) — radial only, axial-float seat | BOM |
| Lower bearing | 6001-2RS (28 OD × 12 ID × 8 W) — radial + fixed axially | BOM |
| Thrust bearing | 51101 (28 OD × 12 ID × 9 W) — under lower 6001 | BOM B0G25X5L23 |
| Shaft collars | 12 mm clamping collars (4-pack, B0DMMB1FHF) — 2 used minimum | BOM |
| Bearing housing | `BearingHousings V2.5.1` (printed PETG) | locked |
| Axial constraint | LOWER bearing fixed; UPPER bearing floating | R5 invariant |
| Pulley axial position | BELOW the lower bearing pair (i.e. extending below Bearing Housing bottom) | R5 |
| Preload | LIGHT — Smalley CM25-L1 wave spring optional (BOM Section 3) | R5 |
| Service | Pulley + collar removal via SE5 (belt replacement) | SERVICE_ENVELOPES.md |

**Design rules (DO):**
- ✅ Lock lower bearing inner race against shaft collar + thrust bearing as a sandwich
- ✅ Leave the upper bearing inner race FREE on the shaft (slip fit, no collar above it)
- ✅ Apply Loctite 603 only to the lower 6001 outer race if seat is loose; never on the upper bearing
- ✅ Pulley grub screw uses Loctite 222 (low-strength, removable)

**Design rules (DON'T):**
- ❌ Do NOT clamp BOTH bearings axially. Will preload the shaft and bind under thermal growth.
- ❌ Do NOT mount the pulley BETWEEN the two bearings. Belt side-load between bearings inverts the load path and amplifies wobble.
- ❌ Do NOT replace the 51101 thrust with another 6001 radial. Radial bearings don't take pure axial loads cleanly.

This interface is now part of the DO-NOT-BREAK invariant set (added below as A8). Changes require R5 → R6 with full bearing-stack review.

---

### Interface 11: Sock Take-Down Column  *(R3 NEW)*

| Property | Value | Locked by |
|---|---|---|
| Geometry | Vertical column on cylinder axis (world X = Y = 0) | invariant C2 |
| Upper boundary | Drive hub bore exit (world Z ≈ 170) | derived |
| Lower boundary | Through D100 hole in wood base (world Z = 0 → ‑∞) | R3 |
| Wood base hole diameter | 100.0 mm | R3 |
| Hole clearance | radius 50 mm clear of any structure | R3 invariant |
| Phase 1 take-down method | **Hanging weight (manual)** — BRING-UP TOOL ONLY | R6 |
| Phase 2 take-down method | **Dual-roller servo-controlled nip system** | R6 (specified) |
| Phase 3 take-down method | Closed-loop tension with optical length sensing (or vacuum) | future |
| Obstruction rule | NO motors, electronics, cables, or structural members may occupy this column | invariant C2 |

Forgetting this column is the single most common architecture mistake
in DIY circular sock machines. Without it, knit fabric climbs, stitch
tension destabilizes, and dropped stitches multiply. The column is
**reserved space** even in Phase 1 where only a hanging weight uses
it.

**R6 Design Rule — Take-down tension is a stitch-formation parameter,
not a fabric-handling parameter.**

Phase 1.5 D-4b simulator results proved this: scenario B1 (slack)
shows that ±2 mm of yarn slack changes capture margin sign. Since
slack is governed by take-down tension, take-down tension is
*coupled* to stitch formation — not downstream of it.

Implications:

- ✅ Phase 1 hanging weight = isolation tool: lets us tune the
  cassette / cam / yarn-capture mechanics WITHOUT a second
  coupled control system (powered take-down dynamics).
- ✅ Adjustable / stackable weights during bring-up are valuable:
  they let us sweep take-down tension experimentally without
  changing firmware or motor controllers.
- ❌ Hanging weight is NOT the production solution. Sock fabric mass
  grows during knitting (1 g/round to 50+ g for a full sock), so a
  fixed-mass weight gives varying tension. Production needs
  active control.
- 🔄 Phase 2 architecture: **dual-roller servo-controlled nip**.

**Phase 2 take-down architecture (R6 specified):**

```
   fabric tube exits cylinder bore
       ↓
   ┌─────────────────────────────────┐
   │  driven roller (rubber-coated)  │ ← stepper or DC gearmotor
   │  ~25 mm OD × 80 mm long          │   pulls fabric at controlled rate
   │  ───[sock fabric]───             │   synced to cylinder rotation
   │  spring-loaded idler roller      │ ← nip pressure
   │  ~25 mm OD × 80 mm long          │
   └─────────────────────────────────┘
       ↓
   encoder or tension sensor (closed-loop)
       ↓
   sock exits to collection bin
```

Properties:
- Compact under-base packaging (fits within Interface 11 column)
- Low inertia (responds quickly to commanded rate changes)
- Easy speed synchronization (target: ~5–10 mm fabric per cylinder revolution)
- Scalable: can add tension-feedback loop in Phase 3
- Acceptable in Phase 2 without full closed-loop (open-loop rate
  control is usually adequate once tuned)

NOT chosen alternatives and why:
- Vacuum extraction: requires blower + ducting + cleaning of lint;
  larger packaging; harder to test/iterate.
- Conveyor: doesn't fit the Ø100 column; fabric doesn't ride flat.
- Constant-force spring: works in theory but harder to design than
  servo nip in a one-off prototype.

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
| Cylinder | **V3.1** (locked 2026-05-24 from WEDGE_B V2 physical test, slot 7) | 1 | `02_CASSETTE_HEAD/cylinder/freecad_macros/CSM_V3_Cylinder_V3_0.FCMacro` (file unchanged, internal version V3.1) |
| Cam Ring | V6.5 (FINAL) | 1 | `02_CASSETTE_HEAD/cam_ring/freecad_macros/CSM_V3_CamRing_V6_5.FCMacro` |
| Sinker Ring | V1.2.1 (LOCKED) | 1 | `02_CASSETTE_HEAD/sinker_ring/freecad_macros/CSM_V3_SinkerRing_V1_2_1.FCMacro` |
| Cassette Base | V1.1 | 1 | `02_CASSETTE_HEAD/cassette_base/freecad_macros/CSM_V3_CassetteBase_V1_1.FCMacro` |
| Retainer Ring | V1.0 (LOCKED) | 1 | `02_CASSETTE_HEAD/retainer_ring/freecad_macros/CSM_V3_RetainerRing_V1_0.FCMacro` |
| Cassette Spacer (×6) | V1.0 (LOCKED 2026-05-24) | 1 | `02_CASSETTE_HEAD/cassette_spacers/freecad_macros/CSM_V3_CassetteSpacer_V1_0.FCMacro` |
| Drive Hub | V2.4.2 (Done) | 2 | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_DriveHub_V2_4_2.FCMacro` |
| Motor Mount | V1.3 (**OBSOLETE for drive** — V1.4 needed for NEMA 23 + gearbox) | 2 | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_MotorMount_V1_3.FCMacro` |
| Bearing Housings | V2.5 (Done) | 2 | `05_BEARINGS_SHAFT/freecad_macros/CSM_V3_BearingHousings_V2_5.FCMacro` |
| Wood Base | V1.0 (NEEDS V1.1 — add D100 take-down hole) | 2 | `CSM_V3_ASSEMBLY/frame/wood_base/freecad_macros/CSM_V3_WoodBase_V1_0.FCMacro` |
| Wood Upper Deck | **NOT YET** | 2 | to build at `CSM_V3_ASSEMBLY/frame/wood_upper_deck/` |
| Aluminum Plate | V1.0 (NEEDS V1.1 — resize 150 → 250) | 2 | `CSM_V3_ASSEMBLY/frame/mount_plate_6061/freecad_macros/CSM_V3_MountPlate6061_V1_0.FCMacro` |
| 2020 Upright | V1.0 (NEEDS V1.1 — shorten 267 → 188, reposition) | 2 | `CSM_V3_ASSEMBLY/frame/upright_2020/freecad_macros/CSM_V3_Upright2020_V1_0.FCMacro` |
| Touchscreen Mast | **NOT YET** | 3 | to build at `CSM_V3_ASSEMBLY/frame/touchscreen_mast/` |
| ~~NEMA 17 motor (drive)~~ | **OBSOLETE** — replaced by NEMA 23 + gearbox | 3 | `CSM_V3_ASSEMBLY/drive_bought/nema17_stepper/` (archive) |
| NEMA 23 + 5:1 gearbox (drive) | **NEEDS BUILD** | 3 | `CSM_V3_ASSEMBLY/drive_bought/nema23_gearbox/` (to create) |
| HTD 60T pulley (14 mm bore) | V1.0 (built — verify bore) | 3 | `CSM_V3_ASSEMBLY/drive_bought/pulley_htd_60t/` |
| HTD 20T pulley (12 mm bore) | **NEEDS BUILD** (was 16T in R3) | 3 | `CSM_V3_ASSEMBLY/drive_bought/pulley_htd_20t/` (to create) |
| HTD belt 405 mm | V1.0 (built) | 3 | `CSM_V3_ASSEMBLY/drive_bought/belt_htd_5m/` |
| Bearings + shaft | NOT YET | 3 | `CSM_V3_ASSEMBLY/bearings_bought/` |
| Feeder Module | **V1.2E** (first-print candidate 2026-05-27 — adjustable ceramic-pigtail clamp, MG90S servo cavity, ±3 mm tangential + ±20° rotational tuning; V1.0 / V1.1 archived) | 3 | `CSM_V3_ASSEMBLY/feeder_module/freecad_macros/CSM_V3_FeederModule_V1_2E.FCMacro` |
| Electronics (Mega/TB6600/S-250/Pi 4) | V1.0 boxes built; cable routing TBD | 3 | `CSM_V3_ASSEMBLY/electronics/` |
| MG90S servo (×6 + 2 spare) | NOT YET as STL | 3 | to add at `CSM_V3_ASSEMBLY/electronics/servo_mg90s/` |
| LM2596 buck converter | NOT YET as STL | 3 | to add at `CSM_V3_ASSEMBLY/electronics/lm2596_buck/` |
| Touchscreen 7" | NOT YET | 3 | `CSM_V3_ASSEMBLY/electronics/touchscreen_7in/` |
| Take-Down Hook Adapter | **V1.0H** (current candidate — D3.0 hooks, 8 mm length, 2 mm root fillet, 3.2× stronger than V1.0F); **V2.0** (architectural alternative — wire-hook carrier, available if printed PETG hooks prove inadequate after failure diagnosis per Phase 1 Guide §3.5). Status PENDING physical failure-mode diagnosis. | 1 | V1.0H: `CSM_V3_ASSEMBLY/take_down/freecad_macros/CSM_V3_TakeDownHookAdapter_V1_0H.FCMacro` • V2.0 (alt): `…/CSM_V3_TakeDownHookAdapter_V2_0.FCMacro` |
| Needle Set & Index Collar | **V1.0A** (Phase 1 assembly aid, 2026-05-27 — clips over cyl OD, datum hub on top face, 72 segmented push pads set uniform needle height, 72 index notches; `NEEDLE_SET_H=9.0` PROVISIONAL, lock to V1.0B after first physical needle measurement) | 1 (tooling) | `CSM_V3_ASSEMBLY/needle_jig/freecad_macros/CSM_V3_NeedleSetCollar_V1_0A.FCMacro` |
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
| R4 | 2026-05-22 | **BOM ALIGNMENT.** Reconciled Interface 5 + Interface 6 with the actual physical inventory in `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`. (a) **Interface 5 feeder actuator**: NEMA 11 stepper → **MG90S metal-gear servo** (8 purchased: 6 active + 2 spare). PWM not step/dir. Feeder Module V1.0 cavity needs V1.1 redesign for 23×13 servo footprint. (b) **Interface 6 drive motor**: NEMA 17 → **NEMA 23 + 5:1 planetary gearbox (23HS22-2804S-HG5)** ($95 StepperOnline). Body 57×57×56 + 50 mm gearbox = 106 mm total. Motor Mount V1.3 OBSOLETE → V1.4 needed (M5 PCD 47.14 vs old M3 PCD 31). (c) **Interface 6 pulleys**: HTD 5M 60T+16T → actual **60T+20T+405mm belt** (kit B0C6Y1462P). New belt ratio 3:1; total reduction = 5×3 = **15:1**. Big pulley bore 12→14 mm (gearbox shaft). (d) §5 locked-versions table refreshed: NEMA 17 STL flagged OBSOLETE; NEMA 23+gearbox STL needs build; 20T pulley needs build; Feeder Module V1.1 needed. All invariants in DO-NOT-BREAK section unchanged. |
| R5 | 2026-05-22 | **Shaft-stack formalization + feeder control philosophy.** (a) NEW **Interface 12** (Shaft / Bearing Stack) — formalizes the floating-top / fixed-bottom bearing architecture on the 12 mm drive shaft. Lower 6001 + 51101 thrust + shaft collar resolves axial load; upper 6001 floats radially to allow thermal growth. Pulley sits BELOW lower bearing (not between). DO / DON'T design rules added. (b) NEW **invariant A8**: shaft bearing stack architecture is now part of the DO-NOT-BREAK invariant set. (c) NEW **R5 Design Rule** under Interface 5: MG90S feeders are "guided yarn presentation," NOT precision synchronized actuation. Defines which feeder operations are acceptable in Phase 1 vs. require a Phase 2 stepper upgrade. (d) Updated revision banner to reflect R5 scope. |
| R6 | 2026-05-24 | **Take-down as stitch-formation parameter (Interface 11 elevation).** Phase 1.5 D-4b results showed scenario B1 (slack) reaches catastrophic capture failure at only ±2 mm slack — proving take-down tension is *coupled to* stitch formation, not downstream of it. (a) NEW **R6 Design Rule** under Interface 11: "Take-down tension is a stitch-formation parameter, not a fabric-handling parameter." Explains why hanging weight (Phase 1) is a bring-up / isolation tool, not the production solution. (b) **Phase 2 take-down architecture formally specified**: dual-roller servo-controlled nip system (rubber drive roller + spring-loaded idler + stepper/DC gearmotor + encoder closed-loop). Replaces vague R3 "weighted claw / roller system" placeholder. (c) Documented why alternatives (vacuum, conveyor, constant-force spring) were not chosen for Phase 2. (d) Phase 3 take-down now specified as closed-loop tension with optical length sensing (or vacuum-assist as alternative). |

---

## Cross-References

- **Coordinate authority:** `MACHINE_COORDINATE_SYSTEM.md` (R1)
- **Dimensional reference:** `MACHINE_DATUMS.md` (R2 final)
- **Service envelopes (full):** `SERVICE_ENVELOPES.md` (next deliverable)
- **Project overview:** `~/.claude/projects/C--3D-Project/memory/project_csm_v3_overview.md`
- **BOM:** `04_PURCHASING/BOM_V11/CSM_V3_BOM_V11.html`
- **Phase 1.5 kinematic script:** future `full_assembly/blender_scripts/needle_motion_study.py`
