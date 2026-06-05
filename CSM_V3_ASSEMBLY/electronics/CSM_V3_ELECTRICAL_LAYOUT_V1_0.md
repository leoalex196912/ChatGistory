# CSM V3 — Electrical Physical Layout V1.0

**Status:** Day 1.5 companion to `CSM_V3_WIRING_V1_0.md`
**Created:** 2026-05-28
**Scope:** Two physical layouts — bench-test plywood (this week) and final wood-base mount
**Phase:** 1

> The wiring diagram (`CSM_V3_WIRING_V1_0.md`) defines what connects to what.
> This document defines **where each component physically lives**, its
> footprint, and how it bolts down. Use the bench-test layout for the
> 5–7 day wait window; switch to the final layout when ready to integrate.

---

## §0 Two layouts at a glance

| Layout | Substrate | Purpose | When |
|---|---|---|---|
| **Bench test** | ~600 × 400 mm plywood or cardboard | Validate electronics WITHOUT machine assembly | This week |
| **Final machine** | Wood Base V1.1 (500 × 400 × 18 mm hardwood) | Production mount | After bench test passes |

Component positions are different on each because:
- Bench test is laid out for **probing and debugging**: every wire reachable, every screw inspectable, generous spacing
- Final machine is laid out for **service and operation**: short cable runs, operator-reachable controls, no interference with cassette / motor / take-down

---

## §1 BENCH-TEST LAYOUT (this week)

### §1.1 Substrate

```
Plywood or cardboard, ~600 × 400 mm × 6 mm thick.
Any flat insulating sheet works. Pine, MDF, hardboard, cardboard, even foam board.
Do NOT use metal — risk of short-circuits.
```

Free hardware-store plywood scrap is ideal. Lay it on a workbench with corners overhanging so you can reach screws underneath.

### §1.2 Layout (top view, +X right, +Y back)

```
   Y=+400 ╔═══════════════════════════════════════════════════════╗
          ║                                                       ║
          ║   ┌───────────────────┐         ┌─────────────────┐   ║
          ║   │  S-250-24 PSU     │         │  Buck #1 (5V)   │   ║
          ║   │  199 x 110        │         │  Mega+servo rail │   ║
          ║   │  CHASSIS DOWN     │         └─────────────────┘   ║
          ║   │  vents UP         │         ┌─────────────────┐   ║
          ║   │                   │         │  Buck #2 (5V)   │   ║
          ║   │  terminals at +Y  │         │  Pi rail        │   ║
          ║   └─────────┬─────────┘         └─────────────────┘   ║
          ║             │                                          ║
          ║   AC pigtail ▼                       24 V bus terminal ║
          ║   to wall    │   ┌─────────────────┐  ┌──────────────┐ ║
          ║   ┌──────────┘   │  Arduino Mega   │  │ TB6600       │ ║
          ║   │              │  102 x 54       │  │ 96 x 56 x 37 │ ║
          ║   │ 2A T-fuse    │  on standoffs   │  │ (DIP set:    │ ║
          ║   │ E-stop NC    │                 │  │  8 microstep,│ ║
          ║   │              └────┬────────────┘  │  2.5 A)      │ ║
          ║   └────────┬──────────┘               └──────┬───────┘ ║
          ║            │ USB-B to laptop                 │ to NEMA ║
          ║            │ (Pi later)                      │ 23 wires║
          ║            │                                 │         ║
          ║            ▼ servo signals + servo extension rails     ║
          ║                                                        ║
          ║   ┌─────────────────────────────────────────────────┐  ║
          ║   │     Six MG90S servos (open frame, free pulleys) │  ║
          ║   │     Numbered 0..5, JST-XH leads to Mega         │  ║
          ║   └─────────────────────────────────────────────────┘  ║
          ║                                                        ║
   Y=0    ╚═══════════════════════════════════════════════════════╝
        X=0                                                    X=+600
```

### §1.3 Bench-test fasteners

Use **#6 wood screws** or **3M VHB tape squares**. Keep it removable:

| Component | Mount method on plywood |
|---|---|
| PSU | 4 × #6 wood screws through its M4 chassis holes (use M4-to-#6 washers) |
| Mega | 4 × M3 nylon standoffs to M3 self-tap into plywood |
| TB6600 | 2 × #6 screws through its flange mounting holes |
| LM2596 buck #1, #2 | 2 × #6 screws OR a 20×20 mm 3M VHB pad |
| Servos | Loose for the bench test; can be in any small box or zip-tied to plywood |
| AC pigtail | Strain-relief clamp at plywood edge, ~3 mm cable tie |
| Fuse holder | Panel-mount option: drill Ø12 mm hole and use the nut. In-line option: just leave the fuse in line, no panel mount. |
| E-stop | Hard-bolt to a small piece of scrap wood you can reach from the keyboard — 22 mm Ø mounting hole |

### §1.4 Bench-test wire-routing rules

- Keep mains side (AC entrance, E-stop, fuse, PSU L/N/PE) on **one corner** of the plywood, physically separated by at least 50 mm from low-voltage DC and signal wires
- Use a black sharpie to label every wire on both ends before connecting
- Run all DC wires along the X axis, all signal wires along the Y axis if possible — easier to trace at 2 AM
- One **kill switch on the wall outlet** in addition to the E-stop — until the E-stop is proven, pulling the wall plug is the real safety

---

## §2 FINAL MACHINE LAYOUT (Wood Base V1.1)

### §2.1 Wood base reference (from `machine_datums.py`)

```
WOOD_BASE_W = 500.0          (X dimension, "wide")
WOOD_BASE_D = 400.0          (Y dimension, "deep")
WOOD_BASE_T = 18.0           (Z thickness)
TAKEDOWN_HOLE_D = 100.0      at center (0, 0)
UPRIGHT_X_POSITIONS = (+150, -150)
UPRIGHT_Y_POSITIONS = (+120, -120)
MOTOR_X, MOTOR_Y = (+85, -47)    NEMA 23 mounts at gearbox side
```

### §2.2 Available real estate

The four perimeter strips outside the upright cage:

| Zone | X range | Y range | Width × Length | Available area |
|---|---|---|---|---|
| LEFT | −250 to −150 | −200 to +200 | 100 × 400 | 40 000 mm² |
| RIGHT | +150 to +250 | −200 to +200 | 100 × 400 | 40 000 mm² |
| FRONT | −150 to +150 | −200 to −120 | 300 × 80 | 24 000 mm² |
| BACK | −150 to +150 | +120 to +200 | 300 × 80 | 24 000 mm² |

Inside the upright cage is **reserved** for the cassette + motor + take-down column (do not place electronics there).

### §2.3 Component placement on wood base (top view)

```
   Y=+200 ╔══════════════════════════════════════════════════════╗
          ║                                                      ║
          ║  ┌──────┐     ┌─[BUCK #1]──[BUS]──[BUCK #2]─┐         ║
          ║  │      │     │   43x21    50x20    43x21   │   BACK  ║
          ║  │      │     │  (-50,+160) (0,+180)(+50,+160)│ strip ║
          ║  │      │     └──────────────────────────────┘        ║
   Y=+120 ║  │ PSU  │  ●──────────────────●                       ║
          ║  │      │                     │     ┌────────────┐    ║
          ║  │ 199  │                     │     │  Mega 2560 │    ║
          ║  │  x   │                     │     │  102 x 54  │    ║
          ║  │ 110  │     CAGE INTERIOR   │     │  (+200,+75)│    ║
          ║  │      │   (reserved for     │     └────────────┘    ║
          ║  │ at   │    motor + drive +  │                       ║
          ║  │(-195,│    take-down)       │     ┌────────────┐    ║
          ║  │  0)  │                     │     │  TB6600    │    ║
          ║  │      │     ○takedown       │     │  96 x 56   │    ║
          ║  │      │      Ø100           │     │(+200,-47)  │    ║
          ║  │      │                     │     │ (near motor)│   ║
          ║  │      │      ▦motor         │     └────────────┘    ║
   Y=−120 ║  └──────┘  ●──────────────────●                       ║
          ║                                                      ║
          ║  ┌──────────────────────────────────────────────┐    ║
          ║  │  FRONT OPERATOR PANEL (vertical, see §2.5)   │    ║
          ║  │  AC inlet | 2A fuse | E-stop | status LEDs   │    ║
          ║  └──────────────────────────────────────────────┘    ║
   Y=−200 ╚══════════════════════════════════════════════════════╝
        X=−250                                                X=+250
```

### §2.4 Component placements (precise coordinates)

#### PSU — S-250-24 (199 × 110 × 50 mm)

```
Center:           (X = −195, Y = 0)
Long axis:        along Y (so 199 mm long runs back-to-front)
Footprint X:      −250 to −140
Footprint Y:      −99.5 to +99.5
Height:           Z = 18 to Z = 68 (bottom on wood base top, vents up)
Terminal end:     at Y = +99.5 (facing BACK strip — keeps wires away from operator)
Chassis screws:   4 × M4 through its bottom mounting holes
                  Hole pattern per Mean Well datasheet (typical 188 × 90 inner spread)
Fastener into wood: M4 × 25 mm wood screw OR M4 × 30 with washer + nut from underside
```

> ⚠ The PSU body extends to X = −140, which is **10 mm past the upright line at X = −150**. The uprights are 20×20 posts at (−150, ±120) — their Y is ±120, outside PSU Y range (−100 to +100). PSU clears them laterally with ~20 mm gap.

#### TB6600 stepper driver (96 × 56 × 37 mm)

```
Center:           (X = +200, Y = −47)
Footprint X:      +152 to +248
Footprint Y:      −75 to −19
Mount:            2 × M3 × 16 mm wood screws through driver flange tabs
Wires to motor:   short run (~50 mm) to NEMA 23 at (+85, −47)
Cable management: zip-tie ferrule the motor wires at the wood base edge
```

#### Arduino Mega 2560 (102 × 54 mm board)

```
Center:           (X = +200, Y = +75)
Footprint X:      +149 to +251 (slightly overhangs wood edge — OK, USB end faces out)
Footprint Y:      +48 to +102
Mount:            4 × M3 × 10 mm nylon standoffs to M3 self-tap into wood
Standoff height:  10 mm (airflow under PCB, prevents wood-moisture absorption)
USB-B port:       faces +X (off-base side) for easy programming access
```

#### LM2596 bucks × 2 (43 × 21 mm each)

```
Buck #1 (Mega+servos):
  Center:         (X = −50, Y = +160)
  Footprint X:    −71.5 to −28.5
  Footprint Y:    +149.5 to +170.5
  Mount:          2 × M3 × 8 mm standoffs OR a 20×20 mm 3M VHB pad
  
Buck #2 (Pi):
  Center:         (X = +50, Y = +160)
  Footprint X:    +28.5 to +71.5
  Footprint Y:    +149.5 to +170.5
  Mount:          Same as Buck #1
  
Spacing rule:    Keep the two bucks ≥ 50 mm apart so the LM2596 inductors don't
                 magnetically couple under load.
```

#### 24 V distribution terminal block (WAGO 221-415 or similar, ~50 × 20 mm)

```
Center:           (X = 0, Y = +180)
Mount:            DIN-rail clip OR 2 × M3 wood screws to the base directly
Function:         Bus tap point — PSU +V / −V trunk lands here, branches fan
                  out to TB6600, Buck #1, Buck #2, future accessory
Wire labels:      "+24V BUS" / "0V BUS" with shrink-tube labels at each leg
```

### §2.5 Front operator panel (vertical sub-assembly)

A small vertical panel L-bracketed to the front edge of the wood base. Operator interface lives here.

```
Panel dimensions: 200 × 60 × 3 mm
Material:         3 mm plywood OR 2 mm aluminum (aluminum preferred for EMI shielding)
Position:         centered at X = 0, mounted on the Y = −200 edge
Top of panel:     Z = 18 + 60 = 78  (just below wood-upper-deck level)
Mount:            2 × small L-brackets (15 × 15 mm) on rear face of panel, M4 wood
                  screws into the wood base front edge

Cutouts (front face, left to right):
┌─────────────────────────────────────────────────────┐
│                                                     │
│  IEC C14 inlet      Fuse holder      E-STOP         │
│  cutout 27 × 19     Ø12 mm           Ø22 mm         │
│  at X = −70         at X = −25       at X = +20     │
│                                                     │
│                                       ● ● POWER     │
│                                       ● ● FAULT     │
│                                       LEDs Ø5 mm    │
│                                       at X = +75    │
└─────────────────────────────────────────────────────┘
       60 mm tall × 200 mm wide

Cable entries:    Through the wood base side (back face of operator panel)
                  Bring AC mains in at IEC inlet, route inside the cage to PSU
                  E-stop NC contacts wire back into mains-side circuit
                  LED wires come from Mega digital pins via current-limiting Rs
```

### §2.6 Cable routing rules on the wood base

1. **Mains AC** runs in the FRONT zone only, between the operator panel and the PSU AC terminals. Keep it on the −Y side of any DC wires.
2. **24 V DC** runs in the BACK zone from PSU terminals to the distribution block, then branches out.
3. **5 V** rails run on the BACK and RIGHT strips: Buck #1 → Mega and feeder servo extensions; Buck #2 → Pi (if on-machine).
4. **Signal wires** (PWM, UART, step/dir/en) run along the RIGHT strip.
5. **Crossing AC and DC**: only at right angles, with at least 50 mm vertical separation (mains side close to wood, DC slightly elevated, or vice-versa)
6. **Cable strain relief**: use Heyco bushings or rubber grommets at every cable that enters or exits the wood base perimeter
7. **Earth bonding** wire (PSU FG → frame if metal): runs back-to-front along the wood base centerline

### §2.7 Mounting hardware bill of materials for the final layout

| Item | Qty | Use |
|---|---|---|
| M4 × 25 mm wood screw | 4 | PSU chassis |
| M4 washer | 4 | Under PSU screw heads |
| M3 × 16 mm wood screw | 2 | TB6600 flange |
| M3 × 10 mm nylon standoff | 4 | Mega |
| M3 × 6 mm screw | 8 | Mega standoff top + bottom |
| M3 × 8 mm standoff | 4 | Bucks (or 4× VHB pads) |
| M3 × 12 mm wood screw | 2 | DIN-rail clip or terminal block |
| L-bracket 15 × 15 mm | 2 | Front operator panel |
| M4 × 10 mm wood screw | 2 | L-bracket to wood base |
| M3 × 8 mm screw | 2 | L-bracket to panel |
| Rubber grommet Ø8 mm | 4 | Cable entry strain reliefs |
| Cable ties 100 mm | 20 | Cable routing |
| Ferrule kit (0.5 – 2.5 mm²) | 1 | Every conductor into a screw terminal |

---

## §3 Cross-references

- `CSM_V3_WIRING_V1_0.md` — electrical schematic, fuse values, wire colors
- `INTERFACE_CONTROL.md` (R6) — frame architecture, Interface 6 (cassette to frame) and Interface 10 (touchscreen mast)
- `machine_datums.py` — single source for all wood-base + upright coordinates
- `CSM_V3_WoodBase_V1_1.FCMacro` — current wood-base STL (already includes the D100 take-down hole; does NOT yet include electronics mounting holes)

---

## §4 What's still TBD

These need real-world decisions or measurements:

- [ ] PSU chassis-screw hole pattern (Mean Well datasheet figure — verify with calipers when unit is in hand)
- [ ] TB6600 flange-hole pitch (verify on actual unit)
- [ ] Whether Raspberry Pi 4 goes on touchscreen mast (recommended) OR also on wood base — Pi+touchscreen sub-assembly design is a separate document
- [ ] E-stop button model (BOM still doesn't show one ordered — pick a 22 mm panel mount, NC+NC double-pole, 10A/250V rated)
- [ ] IEC C14 inlet model and exact cutout dimensions (depends on chosen part)
- [ ] Wood-base electronics-mounting holes (drilled in V1.2 wood base, not V1.1 — V1.1 doesn't have them; mark and drill once layout is finalized)

---

## §5 Revision log

| Rev | Date | Author | Change |
|---|---|---|---|
| V1.0 | 2026-05-28 | claude | Initial layout — bench test + final wood base + operator panel |
