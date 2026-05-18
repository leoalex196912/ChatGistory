# INTERFACE_CONTROL.md — CSM V3 Interface Control Document (ICD)

```
Revision:  R1
Date:      2026-05-17
Status:    Active — locked interfaces, change requires version bump on BOTH mating parts
```

This is the **interface control document** for the CSM V3 modular machine.
It captures every mating relationship between components: what bolts to what,
what registers in what, what rotates inside what.

When an interface here changes:
1. The **change must be propagated to BOTH mating parts simultaneously.**
2. The version of both parts must bump (e.g. V1.0 → V2.0 if interface changed).
3. This document gets a new revision (R1 → R2).
4. Update `MACHINE_DATUMS.md` if a datum plane shifted.

The purpose is to allow **individual components to evolve independently**
without breaking the assembly, as long as their external interfaces stay
consistent with this ICD.

---

## Convention: PCD = Pitch Circle Diameter (in mm)

---

## Interface 1: Drive Hub ↔ Cylinder

| Property | Value | Locked by |
|---|---|---|
| Mating method | Boss into pocket + bolt circle | both V2.4.2 + V3.0 |
| Concentric registration | D18.0 boss → D18.2 pocket (0.20mm slip fit) | Drive Hub V2.4.2 |
| Bolt PCD | 70.0 | both |
| Bolt count | 4× M5 | both |
| Bolt angular offset | 45° (45/135/225/315) | both |
| Hardware | M5 brass heat-set inserts in cylinder (B0DPQJ4W3Z) | BOM_V11 |
| Bolt direction | Up from below drive hub flange, through countersinks, threaded into cylinder inserts | Drive Hub V2.4.2 |

---

## Interface 2: Cylinder ↔ Cam Ring

| Property | Value | Locked by |
|---|---|---|
| Mating method | Rotational concentric clearance (cylinder rotates inside stationary cam) | both V3.0 + V6.5 |
| Cylinder OD | 114.30 | Cylinder V3.0 |
| Cam Ring ID | 115.00 | Cam Ring V6.5 |
| Radial clearance | 0.35mm/side | derived |
| Cam track Z range | Z=19 to Z=31 (cylinder local), engages butts | Cam Ring V6.5 + cylinder slot geometry |
| Cam lift | 8mm (smoothstep cubic) | Cam Ring V6.5 |
| Butt zone | within cylinder slot opening (Z=12-75) | Cylinder V3.0 |

---

## Interface 3: Cam Ring ↔ Cassette Base

| Property | Value | Locked by |
|---|---|---|
| Mating method | Cam ring bolts UP from below into cassette base | both V6.5 + V1.1 |
| Bolt PCD | 155.0 | both |
| Bolt count | 6× M5 | both |
| Bolt angular offset | 30° (30/90/150/210/270/330) | both |
| Pin PCD | 145.0 | both |
| Pin count | 6× D4 dowels | both |
| Pin angular offset | 0° (0/60/120/180/240/300, alternating with bolts) | both |
| Cam ring top Z | 49.0 (= CAM_DATUM_Z) | both |

---

## Interface 4: Cassette Base ↔ Sinker Ring

| Property | Value | Locked by |
|---|---|---|
| Mating method | Sinker drops into register pocket on pedestal top | both V1.1 + V1.2.1 |
| Pedestal OD | 150.0 | Cassette Base V1.1 |
| Pedestal ID | 128.0 (annular) | Cassette Base V1.1 |
| Pedestal height | 12.0 (= SINKER_Z - CASSETTE_TOP_Z) | Cassette Base V1.1 |
| Register pocket diameter | 135.30 | Cassette Base V1.1 |
| Register pocket depth | 1.0mm | Cassette Base V1.1 |
| Sinker Ring OD | 135.00 | Sinker Ring V1.2.1 |
| Slip fit clearance | 0.15mm/side | derived |
| Sinker register plane (top of pocket) | Z=75 (= SINKER_Z) | both |

---

## Interface 5: Cassette Base ↔ Feeder Modules (+ Retainer Ring, shared)

| Property | Value | Locked by |
|---|---|---|
| Bolt PCD | 190.0 | Cassette Base V1.1 |
| Bolt count | 6× M4 | Cassette Base V1.1 |
| Bolt angular offset | 0° (0/60/120/180/240/300) | Cassette Base V1.1 |
| Phase 1 active feeders | 2 (positions 0° and 180°) | architecture decision |
| Retainer Ring mount | Shares same 6 bolt pattern (positions 60/120/240/300 unused by feeders) | proposed for Retainer V1.0 |

---

## Interface 6: Cassette Base ↔ Frame (wood mid-shelf via aluminum plate)

| Property | Value | Locked by |
|---|---|---|
| Bolt PCD | 180.0 | Cassette Base V1.1 |
| Bolt count | 4× M5 | Cassette Base V1.1 |
| Bolt angular offset | 45° (45/135/225/315) | Cassette Base V1.1 |
| Aluminum plate footprint | 150 × 150 × 6 mm 6061 | BOM (purchased) |
| Plate corner radius | 75 × √2 = 106mm (each bolt at r=90 within corner) | derived |
| Wood mid-shelf material | 500 × 400 × 18 mm hardwood | architectural |
| Hardware | M5 with T-nuts in 2020 channel (B0GG4N5GR4) | BOM_V11 |

---

## Interface 7: Cassette Base + Sinker Ring ↔ Retainer Ring (LOCKED in V1.0)

| Property | Value | Locked by |
|---|---|---|
| Mating method | Retainer sits ABOVE sinker, mounts to cassette base via shared feeder bolts at PCD 190 | both V1.1 + V1.0 |
| Retainer Ring OD | 200.0 | Retainer Ring V1.0 (matches cassette base OD) |
| Retainer Ring through-bore | D118.0 (cylinder OD 114.3 + 1.85mm radial clearance) | Retainer Ring V1.0 |
| Loop-control lip diameter | D104.0 effective loop aperture | Retainer Ring V1.0 |
| Lip height (from top of ring) | 2.0mm (top portion only, ring is 8mm total) | Retainer Ring V1.0 |
| Retainer assembly Z (bottom face) | 83.0 (= SINKER_Z + sinker_height 8) | architecture |
| Lip underside world Z | 89.0 | derived |
| Hook clearance under lip | 6.0mm (lip at Z=89-91 vs HOOK_PEAK_Z=83) | derived |
| Mount bolt PCD | 190.0 (SAME as Cassette Base feeder PCD) | both V1.1 + V1.0 |
| Mount bolt count | 6× M4 | both |
| Phase 1 usage | Feeders at 0/180 (2 active); retainer secures at 60/120/240/300 | architecture |
| Phase 1.5 usage | All 6 bolts shared via stack-mount (bolt → cassette → spacer → retainer) | architecture |
| Spacer requirement | 6× printed spacers D8 × 20mm (closes gap between cassette top Z=63 and retainer bottom Z=83) | to design |
| Bolt length | M4 × ~50mm (or threaded rod with nuts) | to verify when ordering |
| Material | PA12 nylon (wear surface, yarn slides on lip underside) | Retainer Ring V1.0 |

---

## Interface 8: Cassette Base ↔ Ribber (Phase 2 provision)

| Property | Value | Locked by |
|---|---|---|
| Bolt PCD | 140.0 | Cassette Base V1.1 (Phase 2 provision) |
| Bolt count | 6× M4 | Cassette Base V1.1 |
| Bolt angular offset | 0° (0/60/120/180/240/300) | Cassette Base V1.1 |
| Used in Phase 1? | NO — holes provisioned, capped/empty | architecture decision |
| Ribber assembly | NOT DESIGNED YET (deferred to Phase 2) | future |

---

## Interface 9: Hall Sensor Index

| Property | Value | Locked by |
|---|---|---|
| Magnet PCD | 95.0 | Cylinder V3.0 |
| Magnet pocket | D6.0 × 2.2mm deep (for B0F4KS6KV3 magnets) | Cylinder V3.0 |
| Angular position | 0° (aligned with Slot #0) | Cylinder V3.0 |
| Pulses per revolution | 1 (master index) | architecture |
| Hall sensor part | SS49E (B09MSDC3GR) | BOM_V11 |

---

## Locked Versions As Of This Document (R1)

| Component | Version | Macro file |
|---|---|---|
| Cylinder | V3.0 | `02_CASSETTE_HEAD/cylinder/freecad_macros/CSM_V3_Cylinder_V3_0.FCMacro` |
| Cam Ring | V6.5 (FINAL) | `02_CASSETTE_HEAD/cam_ring/freecad_macros/CSM_V3_CamRing_V6_5.FCMacro` |
| Sinker Ring | V1.2.1 (LOCKED) | `02_CASSETTE_HEAD/sinker_ring/freecad_macros/CSM_V3_SinkerRing_V1_2_1.FCMacro` |
| **Cassette Base** | **V1.1** | `02_CASSETTE_HEAD/cassette_base/freecad_macros/CSM_V3_CassetteBase_V1_1.FCMacro` |
| Drive Hub | V2.4.2 (Done) | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_DriveHub_V2_4_2.FCMacro` |
| Motor Mount | V1.3 (Done) | `06_DRIVE_SYSTEM/freecad_macros/CSM_V3_MotorMount_V1_3.FCMacro` |
| Bearing Housings | V2.5 (Done) | `05_BEARINGS_SHAFT/freecad_macros/CSM_V3_BearingHousings_V2_5.FCMacro` |
| Retainer Ring | V1.0 (LOCKED) | `02_CASSETTE_HEAD/retainer_ring/freecad_macros/CSM_V3_RetainerRing_V1_0.FCMacro` |
| Feeder Module | NOT YET | — |
| Yarn Mast | NOT YET | — |
| Cassette Base (Phase 2 ribber mount) | provisioned in V1.1 | — |

---

## How to Use This Document

**When designing a new component:**
1. Find every interface this component touches (e.g. Retainer Ring → Interface 7 + Interface 5)
2. Copy the locked values exactly into the component's macro parameter section
3. Do NOT modify these values without going through the change process (below)

**When proposing an interface change:**
1. Identify all mating parts that depend on the interface
2. Decide whether to absorb the change in one part or split between both
3. If split, bump BOTH parts' versions
4. Update this document (R1 → R2)
5. Update MACHINE_DATUMS.md if a datum plane shifted
6. Commit all changes together with a clear message describing what changed and why

---

## Revision History

| Rev | Date | Changes |
|---|---|---|
| R1 | 2026-05-17 | Initial ICD. Captures interfaces 1-9 from locked V3 architecture. |
| R2 | 2026-05-17 | Lock Interface 7 with Retainer Ring V1.0 final geometry. Retainer OD = 200 (was 172, fixed for bolt PCD compatibility). All other interfaces unchanged. |
