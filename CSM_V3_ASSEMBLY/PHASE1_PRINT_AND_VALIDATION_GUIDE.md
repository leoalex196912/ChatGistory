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
| D | Take-Down Hook Adapter | V1.0F | `dd93e76` | `CSM_V3_ASSEMBLY/take_down/freecad_macros/CSM_V3_TakeDownHookAdapter_V1_0F.FCMacro` |
| I | Needle Set & Index Collar | V1.0A | `0850699` | `CSM_V3_ASSEMBLY/needle_jig/freecad_macros/CSM_V3_NeedleSetCollar_V1_0A.FCMacro` |

All four are **first-print candidates**, NOT production-final.

---

## 1. Print Queue Summary

| Part | Material | Orientation | Supports | Est. mass | Est. time | Layers / walls / infill |
|---|---|---|---|---|---|---|
| **A** Cassette Spacers ×6 | PETG (PA12 prod) | Upright, bore vertical, 6 on bed | None | ~5 g total | ~30 min | 0.2 / 3 / 50% gyroid |
| **B** Feeder Module | PETG (PA12 prod) | Base flat on bed, block vertical, post tall | None* | ~103 g | ~4–6 h | 0.2 / 3 / 30% |
| **D** Take-Down Hook | PETG | Ring flat, hooks UP in printer (= DOWN in use) | None | ~19 g | ~45 min | 0.2 / 3 / 30% gyroid |
| **I** Needle Collar | PLA or PETG | Datum-hub-down, collar axis vertical | None | ~75 g | ~3–4 h | 0.2 / 3 / 20% |

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

### THE key measurement

| Measurement | Provisional | **Actual** | Notes |
|---|---|---|---|
| **Hook-tip rest height above cyl top** | — | **____ mm** | with needle seated low/at rest |
| `NEEDLE_SET_H` to set in V1.0B | 9.0 (guess) | **____ mm** | = the measured rest height |
| Latch clearance (latch swings free) | — | ____ | ☐ free ☐ binds |

### Pad contact verification (☐ pass / ✗ fail → revision)

- ☐ Push pads contact needle **shank/back**, NOT hook throat
- ☐ Push pads do NOT touch latch tongues
- ☐ All 72 pads engage; none miss a needle
- ☐ Collar does not rock or bind when seated with needles present
- ☐ Needles end at uniform height after seating

### Outcome
- `NEEDLE_SET_H` locked value: **____ mm** → release **V1.0B "validated"**
- Other params changed: ____________________

---

## 4. Take-Down Weight Tuning Table — Hook Adapter V1.0F

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

---

## Sign-off

| Part | Printed | Inspected | Fit-validated | Version locked |
|---|---|---|---|---|
| A Cassette Spacers | ☐ | ☐ | ☐ | ☐ |
| B Feeder Module | ☐ | ☐ | ☐ | ☐ V1.2F? |
| D Take-Down Hook | ☐ | ☐ | ☐ | ☐ |
| I Needle Collar | ☐ | ☐ | ☐ | ☐ V1.0B |

**First-knit readiness gate:** all four fit-validated + `NEEDLE_SET_H` locked
+ take-down window found → proceed to first knit attempt.
