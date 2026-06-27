# CSM V3 — Project Cover & Overview Drawings

This folder contains two complementary architecture illustrations of the
complete CSM V3 machine.

## 1. `CSM_V3_MACHINE_COVER.png` — Canonical Project Cover

**Use this as the project's cover image** (READMEs, presentations, docs).

Professionally rendered isometric engineering illustration showing:

- Complete machine in 3/4 isometric view with all 14 modules labeled
- Cassette-stack close-up showing the retainer ring, 72-needle cylinder,
  spring groove, cam ring, sinker ring, cassette base
- "Cylinder — what it really looks like" section view + top view
- Machine dimensions (720 mm × 500 × 400)
- 14 Modules Overview index with color coding
- Yarn path & feeder layout (PCD 190, 6 feeders @ 60°)
- Key features panel
- Layer color key

### Dimensions shown on the cover

Most are direct from `machine_datums.py`. A few cylinder-internal
dimensions (butt cavity width 8.5 mm, butt cavity height 4 mm, "PCD 70")
are illustrative and may not be exact CAD values — verify against the
cylinder macro if you need them for manufacturing.

The slot length, spring groove position, cylinder OD/ID, and cassette
stack outer dimensions match `machine_datums.py` and the locked V3.1
specifications from physical test (WEDGE_B slot 7 winner: SLOT_DEPTH
= 4.70, SPRING_GROOVE_DEPTH = 3.10).

## 2. `CSM_V3_MACHINE_OVERVIEW_AUTO.png` / `.pdf` — Auto-Generated Diagram

Secondary, **data-driven** illustration auto-generated from
`machine_datums.py` via `generate_machine_overview.py`.

Use this when:

- You change `machine_datums.py` and want to verify the architecture
  visually
- You want a regenerable, lower-cost reference (no manual artwork
  required)
- You want a PDF/vector version for printable engineering reference

Both files are committed to GitHub as part of the project documentation.

## 14 modules listed on the cover

```
1.  Knitting Cylinder (V3.1, 72 slots)        Layer 1 — Precision
2.  Cam Ring (V6.5)                           Layer 1
3.  Sinker Ring (V1.2.1)                      Layer 1
4.  Cassette Base + Retainer + 6× Spacers     Layer 1
5.  6× Feeder Assembly (servo-driven)         Layer 1 / 3
6.  Drive System (NEMA 23 + HG5 5:1 + belt)   Layer 2
7.  Bearing & Shaft Stack                     Layer 2
8.  Take-Down (V1.0H hook / V2 dual-roller)   Layer 1
9.  Frame (wood base + 2020 + alu plate)      Layer 2
10. HMI (dual 2020 mast + 7" touchscreen + Pi 4)  Layer 3
11. Electronics (S-250-24 PSU + Mega + bucks + TB6600)  Layer 3
12. Operator Panel (E-stop + AC inlet + fuse)  Layer 3
13. Ribber Disk (provisioned for Phase 2)     Layer 1 (future)
14. Yarn Path (6 cones + ceramic pigtails)    Layer 1 / 5
```

## Architecture invariants (locked)

| Invariant | Value | Reference |
|---|---|---|
| Master datum (top of aluminum plate) | Z = 230 mm | ICD invariant B3 |
| Cylinder OD | 114.30 mm | machine_datums |
| Slot count | 72 @ 5° pitch | machine_datums |
| Slot depth | 4.70 mm | V3.1 locked from WEDGE_B |
| Spring groove depth | 3.10 mm | V3.1 locked |
| Cassette stack PCDs | 145 (cam pin), 155 (cam bolt), 180 (frame), 190 (feeder) | machine_datums |
| Master frame | 4× 2020 at (±150, ±120) × 188 mm | machine_datums (now 200 mm with 12 mm wood) |
| HMI mast | dual 2020 at (±75, -210) × 400 mm | ICD I10 / Module 10 |
