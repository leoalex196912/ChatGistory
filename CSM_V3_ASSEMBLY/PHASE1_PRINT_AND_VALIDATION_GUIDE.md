# CSM V3 — Phase 1 Print & Validation Guide

**Status:** Phase 1 bring-up traveler
**Created:** 2026-05-27
**Scope:** Four first-print parts (A, B, D, I) — print, dry-fit, calibrate, record
**Purpose:** Single source of truth for print settings + first-fit measurements.
The measurements captured here drive the next macro revisions (V1.2F, V1.0B, etc.)
and become the project's foundational assembly datums.

> **How to use this doc:** Print it, fill the blank `____` fields at the bench
> with a pen, then transcribe back into this file and commit. Each filled-in
> measurement is a permanent calibration record. Do not delete old values —
> strike them through so the history stays visible.

---

## 0. Part Index & Commit Provenance

| Part | Name | Version | Commit | Macro |
|---|---|---|---|---|
| A | Cassette Spacers (×6) | V1.0 | `33e96e3` | `01_MECHANICAL/02_CASSETTE_HEAD/cassette_spacers/freecad_macros/CSM_V3_CassetteSpacer_V1_0.FCMacro` |
| B | Feeder Module | V1.2E | `5e23e06` | `CSM_V3_ASSEMBLY/feeder_module/freecad_macros/CSM_V3_FeederModule_V1_2E.FCMacro` |
| D | Take-Down Hook Adapter | **V1.0H** (current candidate) + V2.0 (alt., wire hooks) | `dd93e76` … `fa674f6` | V1.0H: `CSM_V3_ASSEMBLY/take_down/freecad_macros/CSM_V3_TakeDownHookAdapter_V1_0H.FCMacro` • V2.0 alt: `…/CSM_V3_TakeDownHookAdapter_V2_0.FCMacro` |
| I | Needle Set & Index Collar | V1.0A | `0850699` | `CSM_V3_ASSEMBLY/needle_jig/freecad_macros/CSM_V3_NeedleSetCollar_V1_0A.FCMacro` |
| SR | Sinker Ring | V1.2.1 (LOCKED, ready to print) | `76fe6f4` | `3D-Project/01_MECHANICAL/02_CASSETTE_HEAD/sinker_ring/freecad_macros/CSM_V3_SinkerRing_V1_2_1.FCMacro` |
| CB | Cassette Base | V1.1 (LOCKED) — **OUTSOURCED, see §1.5** | `b758110` | `3D-Project/01_MECHANICAL/02_CASSETTE_HEAD/cassette_base/freecad_macros/CSM_V3_CassetteBase_V1_1.FCMacro` |
| RR | Retainer Ring | V1.0 (LOCKED) — **OUTSOURCED, see §1.5** | `b758110` | `3D-Project/01_MECHANICAL/02_CASSETTE_HEAD/retainer_ring/freecad_macros/CSM_V3_RetainerRing_V1_0.FCMacro` |
| F | PSU Terminal Guard | **Measurement Required — Not Yet Released** | — | (to be created at `CSM_V3_ASSEMBLY/electronics/psu_guard/`) |

Parts A / B / D / I are **first-print candidates**, NOT production-final.
Part F is **not released** — see §7. Do not print until installed-wiring
measurements are recorded and a final form factor is chosen.

---

## 1. Print Queue Summary

### Recommended print order (risk-stratified)

| # | Part | Practical objective | Why this order |
|---|---|---|---|
| 1 | **D** Take-Down Hook | **Verify printer behavior** | Fast, cheap, no assembly dependency |
| 2 | **A** Cassette Spacers | **Verify dimensional accuracy** | Tiny print, blocks no other work |
| 3 | **I** Needle Collar | **Establish machine datums** | Locks real needle envelope → `NEEDLE_SET_H` |
| 4 | **SR** Sinker Ring (test slices first) | **Verify cassette-ID fit** | Print BOTH dual-clearance test slices (ID115.1 + ID115.3) before the full ring; pick the slice that drops cleanly over the cylinder, then print FULL |
| 5 | **B** Feeder Module | **Verify purchased-component integration** | Print after pigtail dims verified (§2); may go straight to print OR receive a V1.2F update first |

> This sequence mirrors how machine builders normally de-risk a new platform:
> calibrate the printer first, then verify dimensional repeatability, then
> establish the real machine datums, then integrate purchased components
> against those datums.

> Rationale: D and A confirm the printer is dimensionally well-behaved on
> small parts before committing 75 g (I) or 103 g (B) of filament. Part I
> unlocks the needle measurements that may also inform feeder yarn-path
> tuning. Part B is intentionally last so that any pigtail surprise from
> bench measurement can be folded into V1.2F before printing 4–6 hours of
> filament.

### Print settings

| Part | Material | Orientation | Supports | Est. mass | Est. time | Layers / walls / infill |
|---|---|---|---|---|---|---|
| **D** Take-Down Hook | PETG | Ring flat, hooks UP in printer (= DOWN in use) | None | ~19 g | ~45 min | 0.2 / 3 / 30% gyroid |
| **A** Cassette Spacers ×6 | PETG (PA12 prod) | Upright, bore vertical, 6 on bed | None | ~5 g total | ~30 min | 0.2 / 3 / 50% gyroid |
| **I** Needle Collar | PLA or PETG | Datum-hub-down, collar axis vertical | None | ~75 g | ~3–4 h | 0.2 / 3 / 20% |
| **B** Feeder Module | PETG (PA12 prod) | Base flat on bed, block vertical, post tall | None* | ~103 g | ~4–6 h | 0.2 / 3 / 30% |
| **SR** Sinker Ring (test slice) | PETG | Ring flat on bed | None | ~3 g | ~10 min | 0.2 / 3 / 30% |
| **SR** Sinker Ring (full) | PETG (PA12 prod for Phase 2) | Ring flat on bed | None | ~50 g (est) | ~2–3 h | 0.2 / 3 / 30% gyroid |

> **Printer bed constraint:** 230 × 230 nominal, **220 × 220 reliable working area**.
> Any part with footprint > 200 mm has ≤ 10 mm corner margin and is treated as
> bed-marginal (first-layer adhesion risk). Both 200 mm cassette discs are
> therefore **outsourced** — see §1.5 below.

## 1.5 Outsourced Parts (bed-exceeding or bed-marginal)

The two largest Phase 1 parts share **Ø 200 mm OD** (locked to match per ICD R2).
With a 220 × 220 working area both fit, but at the very edge of reliable
adhesion — and these are structural cassette rings where first-layer
delamination would be catastrophic. **Both are sent to an SLS / MJF service
as single pieces** rather than split-and-bond, because:

- Splitting the cassette base cleanly is impractical (pedestal step, register
  pocket, four overlapping bolt-circle patterns intersect at the split line)
- SLS PA12 / MJF PA12 give isotropic strength (no layer-adhesion plane) and
  better dimensional accuracy than FDM at this size class
- Both rings define **datum surfaces** that mate with other locked parts —
  splitting introduces a glued seam at exactly the wrong place

### Parts and upload paths

| Part | STL to upload | File size | Local relative path |
|---|---|---|---|
| **CB** Cassette Base V1.1 | `CSM_V3_CassetteBase_V1_1_FULL.stl` | 7.3 MB | `3D-Project/01_MECHANICAL/02_CASSETTE_HEAD/cassette_base/CSM_V3_CassetteBase_V1_1_FULL.stl` |
| **RR** Retainer Ring V1.0 | `CSM_V3_RetainerRing_V1_0_FULL.stl` | 2.4 MB | `3D-Project/01_MECHANICAL/02_CASSETTE_HEAD/retainer_ring/CSM_V3_RetainerRing_V1_0_FULL.stl` |

### Recommended specification

| Spec | Recommendation | Why |
|---|---|---|
| Material | **PA12 nylon (SLS or MJF)** | Industry-standard structural; isotropic; no layer-adhesion plane; better dim accuracy than FDM at 200 mm scale |
| Color | Natural / white / grey (any) | Cosmetic only; functional surface is internal |
| Finish | Standard / unfinished | Don't pay for vapor smoothing — internal datum surfaces should stay as-printed |
| Tolerance class | Standard (±0.3 mm or service default) | Verify bore + bolt-hole IDs after receipt |
| Quantity | 1 each | No spares yet; revisit after first-fit |

### Approximate cost & lead time (Craftcloud / JLC3DP / Sculpteo / Shapeways)

| Part | PA12 SLS, qty 1 | Lead time inc. shipping |
|---|---|---|
| Retainer Ring V1.0 | $15–25 | 5–10 business days |
| Cassette Base V1.1 | $30–50 | 5–10 business days |
| **Order together** | **$45–75 total** | Save shipping by combining |

Order **both in the same service order** — same shipping, matching production
batch (more consistent tolerances), single receiving event.

### Post-receipt inspection (treat like §1 critical-dimensions)

| Part | Dimension | Nominal | Measured | Pass? |
|---|---|---|---|---|
| CB | Outer disc OD | 200.0 mm | ____ | ☐ |
| CB | Cam-bolt PCD (M5 × 6 at 155 mm) | 155.0 mm | ____ | ☐ |
| CB | Cam-pin PCD (D? × 6 at 145 mm) | 145.0 mm | ____ | ☐ |
| CB | Feeder PCD (M4 × 6 at 190 mm) | 190.0 mm | ____ | ☐ |
| CB | Frame-mount PCD (M5 × 4 at 180 mm) | 180.0 mm | ____ | ☐ |
| CB | Sinker pedestal OD | 150.0 mm | ____ | ☐ |
| CB | Cassette top Z (above frame mount face) | per macro | ____ | ☐ |
| RR | Outer ring OD | 200.0 mm | ____ | ☐ |
| RR | Inner ring ID | per macro | ____ | ☐ |
| RR | Bolt holes align with CB feeder PCD (190) | yes | ☐ | ☐ |
| BOTH | Surfaces flat (no warp from cooling) | < 0.3 mm deviation | ____ | ☐ |
| BOTH | Threads / press-fits test cleanly | go/no-go | ____ | ☐ |

If any dimension is out by more than the service tolerance (±0.3 mm typical),
contact the service for reprint before continuing assembly. The cassette
base + retainer ring fit determines the geometry of every other locked
cassette part — they are the **datum-defining components**.

\* **Feeder post note:** the D15 × 130 mm cone post is the tall, slender feature.
If first-layer adhesion is marginal, add a 5 mm sacrificial raft pad under the
post only. Print times are estimates — confirm in your slicer.

### Critical dimensions to inspect post-print (before assembly)

| Part | Dimension | Nominal | Measured | Pass? |
|---|---|---|---|---|
| A | Spacer length (gap to bridge) | 20.0 mm | ____ | ☐ |
| A | Bore (M4 clearance) | 4.5 mm | ____ | ☐ |
| A | OD | 8.0 mm | ____ | ☐ |
| B | Base plate footprint | 95 × 70 mm | ____ | ☐ |
| B | Mount-hole pitch (PCD-190 chord) | see macro | ____ | ☐ |
| B | Pigtail slot bore | 4.3 mm | ____ | ☐ |
| B | Support-block thickness (T) | 10.0 mm | ____ | ☐ |
| D | Ring OD | 75.0 mm | ____ | ☐ |
| D | Cord-eye bore | 6.0 mm | ____ | ☐ |
| D | Hook tip-to-tip span | (4 hooks @ r33) | ____ | ☐ |
| I | Skirt bore (slip over cyl OD) | 115.10 mm | ____ | ☐ |
| I | Open center | Ø92 mm | ____ | ☐ |
| I | Push-pad height (NEEDLE_SET_H) | 9.0 mm (PROV) | ____ | ☐ |
| SR | Test slice ID — choose fit | 115.3 / 115.1 | _____ wins | ☐ |
| SR | Ring OD | 135.0 mm | ____ | ☐ |
| SR | Ring ID (chosen) | 115.3 mm (nominal) | ____ | ☐ |
| SR | Sinker tip-to-tip span (sample) | ~107.3 mm (2× tip radius) | ____ | ☐ |
| SR | Sample sinker pitch (3 adjacent) | 15.0° / ~14.04 mm arc | ____ | ☐ |
| SR | Drop fit over cylinder (free + smooth?) | yes | ☐ yes ☐ tight ☐ loose | ☐ |
| SR | Sinker base — visible cracks after 24h? | none | ☐ none ☐ hairlines ☐ cracks | ☐ |

---

## 2. First-Fit Inspection Checklist — Feeder Module V1.2E

The feeder yarn-exit clamp has the **most supplier-geometry unknowns**. These
measurements directly drive **V1.2F**.

### Ceramic pigtail (B0FLJK48BB) measurements

| Measurement | Macro assumption | Actual | Notes |
|---|---|---|---|
| Stem thread spec | M4 | ____ | Try an M4 nut: spins free = M4 |
| Usable thread length (sleeve→tip) | ≥ 18 mm | ____ mm | Must clear block T + 2 nuts |
| Jam-nut thickness | 3.2 mm | ____ mm | × 2 nuts |
| Jam-nut A/F (across flats) | 7 mm | ____ mm | |
| Metal sleeve OD | ~6 mm | ____ mm | seats against inboard face |
| Eye offset from stem axis | ~12 mm | ____ mm | sets eye-Z swing range |

### Fit checks (☐ pass / ✗ fail → revision)

- ☐ Pigtail stem passes through slot cleanly (4.3 mm bore OK)
- ☐ Metal sleeve seats **flush** against inboard face (no rocking)
- ☐ Bent neck passes through ridge **center channel** during insertion
- ☐ Both jam nuts reach the outboard face with thread to spare
- ☐ Both jam nuts are wrench-accessible
- ☐ MG90S servo presses into rear cavity, 2× M2 screws align
- ☐ Servo cable exits the cable slot without pinching
- ☐ Base mounts flat to cassette at PCD-190 (M4 holes align)

### Outcome
- Required revision (V1.2F)? ☐ No ☐ Yes → what: ____________________
- Confirmed/changed params for V1.2F: ____________________

---

## 3. Needle Calibration Sheet — Needle Collar V1.0A

**Highest-value measurement section.** This locks `NEEDLE_SET_H`, a foundational
assembly datum that future revisions and the kinematic model depend on.

### Cylinder + needle reference (from MACHINE_DATUMS R5)

| Datum | Value |
|---|---|
| Cylinder OD | 114.30 mm |
| Cylinder top face Z (cyl-local) | 75.0 |
| Hook peak Z at cam lift (cyl-local) | 83.0 (8 mm above top) |
| Slot count / pitch | 72 / 5.0° |
| Slot width | 1.22 mm |
| Needle | FlyDesigns 12g latch |

### Collar fit

- ☐ Collar drops over cylinder OD smoothly (0.8 mm dia clearance)
- ☐ Lead-in chamfer guides blind start
- ☐ Datum hub bottoms on top-face annulus (no rock, seats square)
- ☐ Open Ø92 center gives finger access + bore visibility
- ☐ Wide index notch (slot 0) aligns with θ=0 reference

### Collar fit — measured play (locks future revisions)

The current design gives **0.8 mm diametral clearance**
(cyl OD 114.30, collar bore 115.10). Measure what that actually produces
after PETG/PLA print shrinkage. The result could fix the collar fit
spec for every future revision.

| Measurement | Value | Action if extreme |
|---|---|---|
| Collar rotational free-play on cylinder | ____ ° | <2° = good; >10° = tighten bore |
| Collar radial play at skirt OD (lateral wobble) | ____ mm | <0.3 mm = good; >0.8 mm = tighten |
| Vertical seating drop (held above, dropped, settled at) | ____ mm | should equal datum-hub seat exactly |

**Fit verdict:** ☐ ideal → lock 0.8 mm clear  ☐ tighten → next rev  ☐ loosen → next rev

### THE key measurement

| Measurement | Provisional | **Actual** | Notes |
|---|---|---|---|
| **Hook-tip rest height above cyl top** | — | **____ mm** | with needle seated low/at rest |
| `NEEDLE_SET_H` to set in V1.0B | 9.0 (guess) | **____ mm** | = the measured rest height |
| Latch clearance (latch swings free) | — | ____ | ☐ free ☐ binds |

### Full needle vertical envelope (capture once, save many revisions)

While a needle is installed for the measurement above, also capture the
complete vertical envelope. This data feeds future sinker / cam-profile /
needle-guard / installation-tooling work. Takes one extra minute now —
saves a reinstall later.

| Feature | Z above cyl top (mm) | Notes |
|---|---|---|
| Needle **butt** top | ____ | seats in slot bottom; sets max retract Z |
| Hook **tip** | ____ | same as `NEEDLE_SET_H` measurement above |
| Latch **pivot** (rivet) | ____ | latch swing reference |
| Latch **tip when fully closed** | ____ | upper bound when latch over hook |
| Latch **tip when fully open** | ____ | lower bound when latch out of yarn path |
| Needle butt depth into slot | ____ | (= cyl top Z − butt top Z, signed) |

### SINGLE-NEEDLE PRE-FLIGHT (required before seating all 72)

> Do this **before** dropping all 72 needles. A failure mode discovered with
> one needle costs one needle; with 72 it can damage many. This is the
> single highest-value check in the whole guide.

1. ☐ Insert **one** needle into a slot (preferably the slot 0 reference)
2. ☐ Drop the collar over the cylinder OD and seat it on the datum
3. ☐ Look straight down through the open Ø92 center
4. ☐ Verify the push pad lands on the needle **shank**, NOT on:
   - ☐ hook throat
   - ☐ latch tongue
   - ☐ latch rivet/pivot
   - ☐ needle butt (wrong axial position)
5. ☐ Lift collar off, inspect needle for marks or bend
6. ☐ Try a second slot (180° opposite) to rule out one-off slot variance

**Pre-flight result:** ☐ PASS → proceed to needle freedom test below
                       ☐ FAIL → STOP, record what the pad hit:
                       ____________________ → revision required (V1.0B+)

### Needle freedom test (catches invisible friction damage)

A pad can miss the hook and still lightly scrape the shank. The damage
may be invisible to the eye but will show up as needle friction —
which for a knitting machine is often a more important indicator than
visible marks.

After removing the collar from the single-needle pre-flight above:

- ☐ Needle slides freely through full travel by fingertip
- ☐ No scratch marks visible on needle shank
- ☐ Latch still swings freely after the test
- ☐ Needle returns under gravity when cylinder is held vertical
- ☐ Friction feel matches a fresh (untested) needle from the same batch

If any check fails → STOP, do not populate 72 needles. Revision required.

### Full-population pad contact verification (☐ pass / ✗ fail → revision)

- ☐ Push pads contact needle **shank/back**, NOT hook throat
- ☐ Push pads do NOT touch latch tongues
- ☐ All 72 pads engage; none miss a needle
- ☐ Collar does not rock or bind when seated with needles present
- ☐ Needles end at uniform height after seating
- ☐ Pre-flight (single-needle) test above PASSED before this step

### Outcome
- `NEEDLE_SET_H` locked value: **____ mm** → release **V1.0B "validated"**
- Other params changed: ____________________

---

## 3.5 Take-Down Hook — Failure Mode Diagnostic (REQUIRED before any redesign)

**Context:** During Phase 1 handling, a printed hook stem broke under
light touch. Before iterating on hook geometry (V1.0J / V2.0 / further),
capture the failure data so the next revision targets the real root cause
rather than guessed parameters.

> A 3 mm PETG cantilever printed correctly should feel noticeably **flexible
> before failure**, not snap. "Breaks by touch" most often indicates a
> *print quality* issue, not a *design* issue. Diagnose first.

### What part broke?

- ☐ Take-Down Hook Adapter, version **V1.0F** / **V1.0G** / **V1.0H** ____ (circle one)
- ☐ Other part, name: ____________________

### Fracture location (most informative)

- ☐ At the ring top surface (hook root) → root-fillet stress concentration
- ☐ One layer above the ring → layer adhesion at the first stem layer
- ☐ Midway up the stem → general bending failure
- ☐ At the barb / sphere tip → tip stress riser
- ☐ Multiple locations → systemic print problem

**Photo of fracture (attach to commit, or paste path):** ____________________

> The fracture face tells the story. Photograph at high resolution with
> good light. Layer adhesion failure shows individual layer lines on the
> break face; bulk failure shows a fibrous / matte texture.

### Print parameters

| Parameter | Value | Notes |
|---|---|---|
| PETG brand / batch | ____ | wet PETG = bad layer adhesion |
| Nozzle temperature | ____ °C | PETG ideal ~240-250; below 235 = poor adhesion |
| Bed temperature | ____ °C | typical 70-85 |
| Layer height | ____ mm | 0.2 is standard; 0.28+ = weak |
| Wall count | ____ | **3+ recommended**, 2 walls = too few for small features |
| Infill % | ____ | 30+ |
| Print speed at stem | ____ mm/s | small features need ≤30 mm/s for proper adhesion |
| Part cooling fan at stem | ____ % | PETG **needs less cooling** than PLA; >60% causes layer issues |
| Z-seam position | ____ | random / aligned / sharpest corner |
| Filament dry? | ☐ y ☐ n ☐ unknown | wet PETG = 30-50% strength loss |

### How was the part removed from the bed?

- ☐ Lifted gently after cooling
- ☐ Pried with spatula
- ☐ Flexed off
- ☐ Broke during removal ← important, indicates the break may be a removal artifact not a design failure

### Diagnostic flow

1. ☐ Photograph fracture surface
2. ☐ Fill all print parameter fields above
3. ☐ If wet filament / low temp / over-cooling / 2 walls is the cause →
   **reprint V1.0H** with corrected settings before any geometry change
4. ☐ If fracture at root after correct print → revision needed:
   ☐ **V1.0J** = V1.0H + conical fillet (continuous root fillet, not sphere)
   ☐ **V2.0** = wire-hook carrier (already designed, architectural alternative)
5. ☐ If fracture at stem mid / tip → barb redesign or material change

### V1.0J candidate (conical root fillet) — NOT YET WRITTEN

If diagnostic shows the V1.0H sphere blend is still inadequate at the
root, the next geometry candidate is:

- Replace base-blend sphere (r 2.0) with a **conical frustum**
  - D 6 at ring surface tapering to D 3 over 3 mm of stem height
  - Smooth tangent transition (no curvature discontinuity)
- All other V1.0H params unchanged
- Will not write/run V1.0J until diagnostic data justifies it

### V2.0 status

The V2.0 wire-hook carrier macro and STL **exist in the repo** as an
architectural alternative but are NOT the locked version. They are kept
ready in case post-diagnostic analysis confirms that printed PETG hooks
are fundamentally inadequate. Until then, V1.0H remains the candidate
and Phase 1 plan calls for proving the printed-hook design first, then
switching to wire hooks only if needed.

---

## 4. Take-Down Weight Tuning Table — Hook Adapter V1.0H

Empirical machine-characterization data. Start light, step up 50 g at a time.

| Weight | Yarn | Result | Notes |
|---|---|---|---|
| 250 g | ____ | ☐ missed captures ☐ stable ☐ over-tension | (B1 slack symptom = too light) |
| 300 g | ____ | ☐ missed ☐ stable ☐ over | |
| 350 g | ____ | ☐ missed ☐ stable ☐ over | |
| 400 g | ____ | ☐ missed ☐ stable ☐ over | |
| 450 g | ____ | ☐ missed ☐ stable ☐ over | |
| 500 g | ____ | ☐ missed ☐ stable ☐ over | (D1 stress symptom = too heavy: needle bend / yarn break) |

**Hook adapter fit checks:**
- ☐ 4 hooks engage bottom course evenly (no single-point load)
- ☐ Rounded barbs hold without laddering on removal
- ☐ Cord ties through eye; weight self-centers
- ☐ Ring + weight drop cleanly through D100 take-down column
- ☐ Watch: spider torsional flex on off-axis cord swing — note if excessive

**Optimal Phase 1 window found:** ____ g for ____ yarn

---

## 5. Revision Trigger Notes

Define what justifies a **macro revision** vs. what is **normal tuning**, to
prevent unnecessary CAD churn.

### Normal tuning (NO macro change — adjust in hardware)
- Minor insertion drag on collar or feeder slot
- Take-down weight selection (that's what the table is for)
- Pigtail rotation/tangential position within its adjustment range
- Slight needle height non-uniformity correctable by re-seating

### Geometry revision REQUIRED (bump the macro version)
- Pad hits latch tongue or hook throat → Needle Collar revision
- Pigtail thread is NOT M4, or thread too short for block T → Feeder V1.2F
- Metal sleeve cannot seat flush → Feeder V1.2F
- Bent neck won't pass ridge channel → widen channel, Feeder V1.2F
- Collar rocks/binds on datum (not square) → Needle Collar revision
- Cassette spacer length ≠ 20 mm gap (MD mismatch) → investigate datum, not just part
- Take-down hooks ladder fabric or single-point load → Hook Adapter revision

### Locked-once-measured parameters (update macro, then freeze)
- `NEEDLE_SET_H` (Needle Collar) — from §3
- Pigtail thread spec / block T (Feeder) — from §2
- Take-down weight target (operational, not geometry) — from §4

### Post-bring-up cleanup backlog (non-blocking, do when convenient)

These are known maintainability/refactor items that should NOT be tackled
during bring-up but are tracked here so they don't get lost.

| Item | Trigger | Suggested rev |
|---|---|---|
| Sinker Ring: switch from hardcoded constants to `import machine_datums as MD` | When CYL_OD / SLOT_COUNT next change, OR during any other sinker geometry edit | V1.2.2 |
| Sinker Ring: explicit 0.3 mm base fillets for stress relief | Only if V1.2.1 print shows hairline cracks at sinker root after 24 h (see §1 SR inspection row) | V1.3 |
| Feeder V1.2E: cosmetic "world" vs "cyl-local" label fix in print output | Next feeder revision (functional, not blocking) | V1.2F or later |

---

## 6. Print Orientation Notes

> Screenshots/photos can be pasted under each part as you slice them. Textual
> orientation guidance below is authoritative until images are added.

### A — Cassette Spacers
- **Bed face:** one flat end of the cylinder (bore vertical)
- **Why:** clean straight bore wall, no support in the M4 through-hole
- **Layout:** all 6 standing upright in one print
- **Seam:** anywhere (compression-only part, non-cosmetic)

### B — Feeder Module ★ most orientation-sensitive
- **Bed face:** base plate underside flat on bed
- **Block:** prints vertically → best layer continuity at the support-block
  root (the jam-load path) and cleanest horizontal pigtail-slot bore
- **Post:** D15 × 130 mm prints tall; add raft pad only if adhesion marginal
- **Ridge:** points up in print → no overhang, no support
- **Critical cosmetic / functional faces:** inboard block face (sleeve seat)
  and outboard block face (jam-nut bearing) — keep these clean; orient seam away
- **Supports:** none expected (servo cavity opens upward, cable slot horizontal)

### D — Take-Down Hook Adapter
- **Bed face:** ring bottom flat on bed; **hooks point UP in printer = DOWN in use**
- **Why:** hooks print as clean vertical columns with sphere tips; no support
- **Spider eye:** prints upward, cord bore is horizontal → small bridge, OK
- **Seam:** on outer ring OD, away from hooks

### I — Needle Collar
- **Bed face:** datum-hub-down (collar axis vertical, skirt pointing up)
- **Why:** push-pad undersides (the needle-contact reference) print as clean
  upward-facing surfaces; datum-hub seating face is flat on bed = most accurate
- **Chamfer:** lead-in chamfer at skirt bottom prints as the top in this
  orientation — verify it didn't need bridging (it's a 45° so should be fine)
- **Index notches:** vertical on skirt OD, no support
- **Seam:** away from the wide θ=0 reference notch so it stays legible

### SR — Sinker Ring
- **Bed face:** ring flat (axial direction Z = perpendicular to bed)
- **Why:** sinker projections print as in-plane horizontal cantilevers in a
  single layer — strongest in tension (catch-and-release loads are radial,
  not axial); ring ID + sinker tips on the same layer for best concentricity
- **Test slices first:** print **both** `_TESTSLICE_ID115_1.stl` and
  `_TESTSLICE_ID115_3.stl` (small ~10 min prints). The slice that drops
  cleanly over the cylinder OD = your real-world clearance lock. Then print
  the matching FULL STL.
- **Supports:** none expected (all sinker overhangs are short in-plane)
- **Seam:** outer ring OD, between two adjacent feeder windows
- **Material note:** PETG for Phase 1; if cyclic-load hairlines appear after
  24 h dwell test, jump to V1.3 with base fillets and/or PA12-CF

---

## 7. Part F — PSU Terminal Guard — Pre-Design Measurement Sheet

**Status:** Measurement Required / Not Yet Released. No STL generated.
No macro committed. Do **not** print until all sections below are filled in
and a final form factor is chosen.

> **Why this part is different:** Parts A / B / D / I could be printed,
> tested, and iterated safely. Part F covers **mains-voltage terminals** —
> the entire purpose is to prevent contact with energized conductors, so it
> must fit correctly on the first print. The installed wiring envelope is
> more important than the bare PSU dimensions.

### Bring-up sequence (DO NOT skip steps)

1. ☐ Mount the PSU in its final location on the deck/frame
2. ☐ Wire it exactly as it will be used (mains in, DC out, earth, all terminals)
3. ☐ Take photos (see below) of the **wired** terminal area
4. ☐ Take measurements (see below) with wires installed
5. ☐ Choose form factor (see hierarchy below)
6. ☐ Generate V1.0 macro using the actual numbers; review; print; install
7. ☐ Re-verify safety checklist with guard in place before first power-on

### PSU identification

- PSU model number (exact variant): ____________________
  *(e.g. S-250-24, S-250-12 — verify the label, do not assume from BOM line)*

### Bare-PSU dimensions (calipers)

| Measurement | Value | Notes |
|---|---|---|
| Body L × W × H | ____ × ____ × ____ mm | overall metal enclosure |
| Terminal-end face W × H | ____ × ____ mm | the short end where terminals live |
| Terminal strip width (end-to-end) | ____ mm | first screw to last screw |
| Distance from chassis edge to first terminal | ____ mm | important — clearance for guard wall |
| Terminal height above PSU base | ____ mm | strip-bottom Z reference |
| Terminal protrusion (screw heads / wires past end face) | ____ mm | sets minimum guard depth |
| Existing PSU-side fastener type & position | ____________________ | only relevant if PSU-mounted (not preferred) |

### Installed envelope (with wiring connected)

| Measurement | Value | Notes |
|---|---|---|
| Largest cable OD entering terminal area | ____ mm | mains cable usually dominates |
| Wire bundle OD after dressing | ____ mm | sum of all wires bundled |
| Minimum wire bend radius required | ____ mm | sets wire-exit slot geometry |
| Wire exit direction (down / side / up) | ____________________ | drives slot face placement |
| Clearance available around terminal end (mm in each direction): | | |
| &nbsp;&nbsp;&nbsp;&nbsp; +X (right) | ____ mm | |
| &nbsp;&nbsp;&nbsp;&nbsp; −X (left) | ____ mm | |
| &nbsp;&nbsp;&nbsp;&nbsp; +Z (above) | ____ mm | |
| &nbsp;&nbsp;&nbsp;&nbsp; −Y (outboard, away from PSU) | ____ mm | |

### Terminal cover envelope (proximity to surrounding structure)

| Measurement | Value |
|---|---|
| Distance from terminal screws to nearest frame member | ____ mm |
| Distance from terminal screws to nearest wood panel | ____ mm |
| Distance from terminal screws to nearest moving component | ____ mm |

### Fastener information (for deck-mount preferred path)

| Item | Value |
|---|---|
| Existing nearby deck mounting holes available | ____ mm pitch / ____ mm from PSU |
| Preferred fastener size | ☐ M3 ☐ M4 ☐ wood screw ☐ other ____ |
| Captive insert available in deck? | ☐ yes ☐ no — through-bolt with washer |

### Photo requirements (attach in commit or paste below)

- ☐ Terminal end, straight-on
- ☐ Top-down
- ☐ Side, showing wire exit path
- ☐ Ruler or calipers visible in at least one image

> Photos often reveal interference issues that numeric measurements miss —
> these are not optional.

### Safety checklist (verify ALL with guard installed, before first power-on)

- ☐ No exposed mains terminals reachable by a fingertip (≥12 mm probe test)
- ☐ Guard does not obstruct PSU ventilation slots
- ☐ Guard removable for service **without** disconnecting wiring
- ☐ Wire strain does not transfer to terminal screws (strain relief works)
- ☐ AC and DC wiring remain visually distinguishable (color/route)
- ☐ Terminal labels remain readable, or replicated on the guard exterior
- ☐ Earth/PE conductor visibly bonded and not loosened by guard installation

### Form-factor selection hierarchy

In order of preference:

1. **Deck-mounted protective tunnel over the terminal area** (PREFERRED)
   - PSU can be replaced without redesigning the guard
   - No dependency on PSU chassis-hole locations
   - Less risk of blocking PSU ventilation
   - Survives a future S-250 → other PSU swap
2. Simple removable terminal shroud (snap or screw to nearby deck point)
3. Hinged cover with latched access
4. PSU-chassis-mounted guard (LAST RESORT — couples guard to PSU revision)

### Service-access requirements (decide before V1.0 macro)

- ☐ Insulated-screwdriver slot to tighten terminal screws without removing guard
- ☐ Removable inspection panel for voltage verification with meter
- ☐ Cable-tie anchor points or integral strain-relief bridge
- ☐ Snap-off side panel for periodic re-torque checks

### V1.0 release gate

Part F V1.0 may not be released until **all of the following** are true:

- ☐ Every measurement above is filled in (no blanks)
- ☐ All four photos taken and committed
- ☐ Form factor chosen and rationale recorded
- ☐ Safety checklist reviewed for design intent (not just installation)
- ☐ Final fastener / mount strategy locked
- ☐ Reviewed by you, then macro drafted, reviewed inline, then printed

---

## Sign-off

| Part | Printed | Inspected | Fit-validated | Version locked |
|---|---|---|---|---|
| A Cassette Spacers | ☐ | ☐ | ☐ | ☐ |
| B Feeder Module | ☐ | ☐ | ☐ | ☐ V1.2F? |
| D Take-Down Hook | ☐ | ☐ | ☐ | ☐ |
| I Needle Collar | ☐ | ☐ | ☐ | ☐ V1.0B |
| SR Sinker Ring | ☐ test slice ☐ full | ☐ | ☐ | ☐ (already V1.2.1 LOCKED) |
| CB Cassette Base | ☐ outsourced ordered ☐ received | ☐ | ☐ | ☐ (already V1.1 LOCKED) |
| RR Retainer Ring | ☐ outsourced ordered ☐ received | ☐ | ☐ | ☐ (already V1.0 LOCKED) |
| F PSU Terminal Guard | ☐ | ☐ | ☐ | ☐ Measurement Required |

**First-knit readiness gate:** all four mechanical parts (A/B/D/I) fit-validated
+ `NEEDLE_SET_H` locked + take-down window found → proceed to first knit attempt.

**First powered-session gate:** Part F released and installed + safety
checklist (§7) verified → proceed to first powered session.
