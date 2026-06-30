# Module 10 HMI -- RC1 Acceptance Checklist

CAD freeze: 2026-06-29.  Physical validation pending.

This document is the gate between **CAD complete** (where Module 10 sits
today) and **manufacturing complete** (which the first full machine
assembly will determine).  Each box becomes a single doc-only commit
when verified.  When every box is ticked, Module 10 is permanently
frozen and the four current DRAFT parts (P07, P08, P09, P10) can be
promoted to RC1 in a single batch.

---

## Mechanical

- [ ] All STL files print without supports
- [ ] All holes fit their nominal hardware (M5, M2.5, M3) with at most light deburring
- [ ] M5 heat-set inserts seat fully in their pockets (B0DPQJ4W3Z)
- [ ] No interference between any two HMI parts when assembled
- [ ] All fasteners remain accessible after the assembly is complete
- [ ] Two mast base sockets seat fully over the 2020 mast extrusions
- [ ] Cross beam drops cleanly onto mast tops; 12 mm pocket engages
- [ ] Touchscreen frame's 4 corner windows accommodate the ELECROW PCD
- [ ] Tilt lock arc slot achieves full +/-20 deg tilt without binding
- [ ] Pi carrier hangs square below the beam
- [ ] Pi fan cover stacks on Pi carrier with 11 mm standoffs as planned

## Electrical

- [ ] Pi fan airflow verified to point toward Pi PCB (arrow on fan body)
- [ ] HDMI cable bend radius acceptable from Pi to touchscreen
- [ ] USB-C power cable bend radius acceptable
- [ ] LED strip wiring complete and routes through cable channel
- [ ] All cables fit into the rear cable channel (8 x 4 mm)
- [ ] Fan power wired correctly: red -> Pi pin 4 (+5V), black -> pin 6 (GND)
- [ ] Touchscreen powers up and displays at 1024 x 600
- [ ] Touchscreen touch input is responsive

## Assembly

- [ ] Assembly order validated against the macro print-block notes
- [ ] No hidden fasteners that require disassembling adjacent parts to access
- [ ] No tool-access impossibilities (screwdrivers, allen keys, heat-set tool)
- [ ] Assembly manual matches the hardware actually used (BOM)
- [ ] Stack-up budget verified (Pi Carrier 10 mm + Pi PCB 1.6 mm + Fan Cover
      standoff 11 mm clears the 10 mm fan body)
- [ ] Mast Base Socket V1.3 lateral T-nut bolts (M5 x 12) thread into 2020 slot
- [ ] Cross Beam V1.2 mast bolts (M5 x 30) self-tap into 2020 center bore
- [ ] No screwdriver clearance problems for the tilt lock thumb screws

## Documentation

- [ ] STEP exported for each part
- [ ] STL exported for each part
- [ ] PNG views generated for each part
- [ ] PDF drawing generated for each part
- [ ] Each macro reports volume, mass (PETG @ 1.27 g/cm^3), and CoM
- [ ] Each macro's wall-thickness check passes all rules
- [ ] machine_datums.py HMI_* block has no remaining hardcoded magic numbers
- [ ] Assembly notes in each macro's print block are current

## Promotion plan

When every box above is checked, in a single doc-only commit:

| Part | Current | After validation |
|---|---|---|
| P03 Pi Carrier | RC1 | RELEASE |
| P05 Touchscreen Frame | RC1 | RELEASE |
| P06 Display Tilt Lock | RC1 | RELEASE |
| P07 Rear Cable Cover | DRAFT | RC1 |
| P08 Cable Clamp | DRAFT | RC1 |
| P09 LED Strip Holder | DRAFT | RC1 |
| P10 Expansion Plate | DRAFT | RC1 |

P01, P02, P04 stay at their current status (FROZEN, FROZEN, RELEASE).

---

## Reference

Per-part files live under `CSM_V3_ASSEMBLY/hmi/<part>/`.  Each folder
contains the FreeCAD macro, the rendered STL + STEP, and the engineering
drawing (PNG + PDF).

Interface contract: `3D-Project/00_PROJECT_OVERVIEW/machine_datums.py`,
`HMI_*` block, marked `HMI_INTERFACE_VERSION = "1.0"`.
