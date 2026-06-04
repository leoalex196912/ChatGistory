# CSM V3 — Electrical Wiring Diagram V1.0

**Status:** Day 1 deliverable, electronics bench-test prep
**Created:** 2026-05-28
**Scope:** Complete mains→DC→logic→actuator wiring + signal architecture
**Phase:** 1 (initial powered bring-up, hanging-weight take-down)

> This document defines the wiring before the bench test. Use it as the
> assembly traveler when wiring on plywood/cardboard. Mark off items as
> built. Any deviation gets noted in a revision so the final installed
> machine matches what's documented here.

---

## §0 Component inventory (from BOM V12)

| Item | P/N | Role | Voltage / current |
|---|---|---|---|
| **Mean Well S-250-24** | B07Y7L664K | Main PSU | 24 VDC, 10 A out (240 W) |
| **LM2596 buck #1** | (BOM V12) | 24 V → 5 V for Mega + servos | 5 V, ≤ 3 A |
| **LM2596 buck #2** | (BOM V12) | 24 V → 5 V for Pi 4 (isolated rail) | 5 V, ≤ 3 A |
| **Arduino Mega 2560 REV3** | B0046AMGW0 | Real-time controller | 5 V via VIN, ~50 mA |
| **Raspberry Pi 4 4 GB** | B07V5JTMV9 | UI / pattern logic | 5 V, ~1.5 A typical |
| **TB6600 stepper driver** | B08SG7L54W | NEMA 23 driver | 24 V power, 5 V logic |
| **NEMA 23 + 5:1 HG5 gearbox** | StepperOnline | Cylinder drive | 24 V, 2.8 A peak |
| **MG90S metal-gear servo × 8** | (BOM V12, 6 active + 2 spare) | Feeder actuators | 5 V, ~150 mA active each |
| **7" touchscreen + Pi case** | B07V5JTMV9 (incl.) | UI display | 5 V via Pi |
| **E-stop mushroom button** | (TBD if not in BOM) | Mains interlock | NC contact, 250 V/10 A rated min |
| **Servo extensions × 6** | B0FXMDCP1H | JST-XH 3-pin M-F | – |
| **Inline AC fuse + holder** | (panel-mount, BOM check) | Mains protection | 2 A slow-blow (T2AL250V) |

---

## §1 Overview block diagram

```
                    230 VAC mains (or 115 VAC, switch on PSU)
                              │
                              │  L (brown)        N (blue)        PE (green/yellow)
                              ▼
                       ┌─────────────┐
                       │  E-STOP     │  Mushroom NC, breaks L line
                       │  (latching) │  (option: break L AND N for double-pole safety)
                       └──────┬──────┘
                              │
                       ┌──────▼──────┐
                       │  2 A T fuse │  inline before PSU
                       └──────┬──────┘
                              │
            ┌─────────────────▼─────────────────┐
            │       Mean Well S-250-24          │
            │   AC in: L / N / FG (earth)       │
            │   DC out: +V (×2) / −V (×2)       │
            │   24 VDC @ 10 A max               │
            └────────┬────────┬─────────┬───────┘
                     │+V      │+V       │−V
                     │ (24 V bus)       │ (24 V GND bus)
        ┌────────────┼────────┼─────────┼──────────┐
        │            │        │         │          │
   ┌────▼───┐  ┌────▼───┐ ┌──▼────┐ ┌──▼─────┐  ┌─▼──────┐
   │ TB6600 │  │ Buck#1 │ │Buck#2 │ │ Fan    │  │ Future │
   │ 24V    │  │ 24→5V  │ │ 24→5V │ │(optional)│ │accessory│
   │ Power  │  │ 3A     │ │ 3A    │ │        │  │(spare) │
   └────┬───┘  └────┬───┘ └──┬────┘ └────────┘  └────────┘
        │           │5V      │5V
        │       ┌───▼────┐ ┌─▼─────────────┐
        │       │ Mega   │ │ Raspberry Pi 4 │
        │       │ VIN/5V │ │ via 5V GPIO    │
        │       │ + GND  │ │ (or USB-C)     │
        │       └───┬────┘ └───┬────────────┘
        │           │           │
        │      ┌────┴───┐       │   HDMI
        │      │ 6× MG90S│       └──► 7" Touchscreen
        │      │ servos │           (5V via Pi USB or buck)
        │      │ JST-XH │
        │      └────────┘
        │
   STEP/DIR/EN
        │
   ┌────▼──────────┐
   │ NEMA 23 + HG5 │
   │  gearbox      │
   │ (cylinder)    │
   └───────────────┘

   Mega ←UART/USB→ Pi 4    (telemetry + commands; 115200 baud default)

   PE (earth) bonded at PSU FG terminal → frame (if metal) → mains earth.
```

---

## §2 Power distribution detail

### §2.1 Mains side (DANGEROUS — do this last)

```
WALL OUTLET (NEMA 5-15 or your region)
   │
   │   L  ──[brown 16AWG, stranded, 600V-rated]──┐
   │   N  ──[blue 16AWG]──────────────────────┐  │
   │   PE ──[green/yellow 16AWG]──────┐        │  │
   │                                  │        │  │
   ▼                                  ▼        ▼  ▼
                                     PSU FG  E-STOP terminals
                                     terminal  │
                                               ▼
                                        2A T-fuse
                                               │
                                               ▼
                                        S-250-24 L, N
```

**Mains specs:**
- L (Live / Line / Hot) — **brown**
- N (Neutral) — **blue**
- PE (Protective Earth) — **green with yellow stripe**
- Wire: **16 AWG stranded, 600 V insulation** (THHN, SJOOW, or H05VV-F equivalent)
- E-stop: NC contact, latching mushroom, **double-pole preferred** (breaks L AND N)
- Inline fuse: **2 A slow-blow** (T2AL250V) panel-mounted between E-stop and PSU L terminal
- All mains connections via **ferrules** into screw terminals — no bare wire ends
- Heatshrink over every termination
- PSU input voltage selector switch: **set to 115 V or 230 V to match your mains BEFORE first power-on**

> ⚠ The PSU input switch is on the unit itself. Verify it matches your mains
> voltage with a multimeter on the wall outlet before plugging in. Wrong
> setting = instant smoke.

### §2.2 24 V DC bus

PSU output terminals (typically labeled `+V`, `+V`, `−V`, `−V` on the S-250) feed a small distribution arrangement. Easiest: a 4-position WAGO 221 or DIN-rail terminal block.

```
PSU +V ──────┬─────┬─────┬─────► TB6600 VCC
             │     │     └────► Buck #1 IN+ (Mega/servo 5V supply)
             │     └─────────► Buck #2 IN+ (Pi 5V supply)
             └───────────────► (spare for Phase 2)

PSU −V ──────┬─────┬─────┬─────► TB6600 GND
             │     │     └────► Buck #1 IN−
             │     └─────────► Buck #2 IN−
             └───────────────► (spare for Phase 2)
```

**24 V bus specs:**
- Trunk from PSU to distribution: **14 AWG** (2 m max to keep voltage drop <2 %)
- Branches: **16 AWG** to TB6600, **18 AWG** to bucks
- Optional but recommended: **10 A fast fuse on the +V trunk** between PSU and distribution (e.g. ATO blade fuse holder)
- Color: **red = +24 V**, **black = 0 V (GND)** — pick a convention and stick to it
- Ferrules on every conductor entering a screw terminal

### §2.3 5 V logic rails — TWO separate bucks

Two separate LM2596 modules. This decouples the Pi from servo/stepper transients.

```
Buck #1 OUT (5 V, ≤ 3 A) ──┬──► Mega VIN (5 V tolerant) + GND
                           │
                           └──► 6× MG90S servo V+ and GND
                               (signal wires go to Mega PWM pins)

Buck #2 OUT (5 V, ≤ 3 A) ──► Pi 4 5V pin (GPIO pin 2 or 4) + GND (pin 6)
                            (or via USB-C, see §2.4)
```

**5 V bus specs:**
- Adjust each LM2596 to **5.10 V ± 0.05 V** under no load **before** connecting downstream (use multimeter on a load-free buck output)
- 100 µF electrolytic across each buck output (input + output) for transient suppression — many LM2596 modules already have this
- **Servo power and Pi power must NOT share the same buck.** Servo current spikes cause voltage dips that crash the Pi.
- **Mega and servos can share Buck #1** — Mega is tolerant of small dips and the analog reference doesn't depend on VIN

### §2.4 Pi 4 power option

Pi 4 needs a clean 5 V at up to 3 A. Two options:

**Option A (recommended for bench test):** Pi from its own wall-wart USB-C supply (the BOM CanaKit starter includes one). Keeps Pi totally isolated from machine power during bench testing. The machine still works if Pi is unplugged.

**Option B (integrated):** Buck #2 output → Pi 4 GPIO pin 2 (5 V) and pin 6 (GND). Skip the USB-C connector. This is cleaner for the final installation but harder to debug.

For Day-1 bench test → **Option A**. Switch to Option B once the bench test confirms everything works.

---

## §3 Signal architecture

### §3.1 Mega ↔ Pi 4 link

```
Mega                                Pi 4
─────                              ─────
 USB-B port  ── USB cable ──►  USB 3.0 port (any)
                                  │
                                  └── shows up as /dev/ttyACM0 on Pi
                                      (or /dev/ttyUSB0 if FT232)

UART speed: 115200 baud, 8N1
Protocol:   line-based ASCII for bring-up;
            switch to packetized binary at Phase 2
```

Pi sends commands like `SET_SPEED 250\n`, Mega responds `OK\n` or `FAULT <code>\n`. Telemetry from Mega comes back as `T <encoder> <servo_pos> <state>\n` at ~10 Hz.

(Full protocol gets defined in Day-2 deliverable; this diagram shows the physical link only.)

### §3.2 Mega ↔ TB6600

```
Mega digital pins         TB6600 inputs
─────────────────         ─────────────
D5  ──── 220Ω ──────────► PUL+   (step pulse)
D6  ──── 220Ω ──────────► DIR+   (direction)
D7  ──── 220Ω ──────────► ENA+   (enable, active LOW)
GND  ──────────────────► PUL− / DIR− / ENA−  (common cathode)
```

**TB6600 microstep & current** settings via on-board DIP switches:
- Microstep: **8 µstep** for Phase 1 (smooth, plenty of resolution)
- Current: **2.5 A** (NEMA 23 rated 2.8 A; leave 10 % margin)
- Verify against the table printed on the TB6600 enclosure

### §3.3 Mega ↔ Servos

Six MG90S servos, three-pin JST-XH each (signal / V+ / GND).

```
Mega PWM pins              Each servo
─────────────              ──────────
D9  ─────────────────────► Servo 0 signal
D10 ─────────────────────► Servo 1 signal
D11 ─────────────────────► Servo 2 signal
D12 ─────────────────────► Servo 3 signal
D44 ─────────────────────► Servo 4 signal     (Timer 5)
D45 ─────────────────────► Servo 5 signal     (Timer 5)

Servo V+  ◄── Buck #1 5 V rail
Servo GND ◄── Buck #1 GND rail (also common with Mega GND)
```

**Important:** Mega GND and Buck #1 GND **must be tied together** at one point — otherwise the PWM signal has no common reference. Single short link between Mega GND pin and Buck #1 GND output. Star ground from the buck output, not chain.

(Servo channels 6 and 7 are spares; wire only if needed.)

### §3.4 NEMA 23 motor wiring

```
TB6600 motor outputs       NEMA 23 (4-wire, bipolar)
────────────────────       ────────────────────────
A+ ─────────────────────► A coil +  (typically red)
A− ─────────────────────► A coil −  (typically blue)
B+ ─────────────────────► B coil +  (typically green)
B− ─────────────────────► B coil −  (typically black)
```

Verify your specific motor's pinout against its datasheet — colors vary by manufacturer. If the motor spins the wrong direction during first test, swap A+ ↔ A− (or B+ ↔ B−).

### §3.5 E-stop signal path

The mushroom button has TWO contact sets:

```
Contact set 1: BREAKS MAINS L line     (primary safety, in §2.1)
Contact set 2: GROUNDS Mega D2 pin     (signal to firmware)
```

When pressed:
- **Hardware-level:** mains is physically broken, PSU shuts off, motors lose power immediately
- **Signal-level:** D2 reads HIGH on press (via 10 kΩ pull-up) — Mega ISR sets state machine to `FAULT_ESTOP`, halts any commanded motion, signals Pi to display the fault

Pi can NOT release the E-stop. The user must twist-release the mushroom button manually. After release, Mega boots clean to `IDLE` state and Pi prompts the user to confirm before re-enabling.

---

## §4 Earthing strategy

Single-point earth at the PSU. **Do NOT create earth loops.**

```
Mains PE (wall outlet, green/yellow)
   │
   ▼
PSU FG terminal  ◄── single bonding point
   │
   ├──► Frame earth (only if metal frame; wood frame = skip)
   │
   ├──► Mega GND (via Buck #1 GND chain, not separate wire)
   │
   └──► Pi 4 GND (via Buck #2 GND, or via USB cable to Mega)
```

DC side `−V` of the PSU is usually internally bonded to FG inside the PSU. Don't add a second bond elsewhere — that creates a ground loop and produces noise on the 5 V rails.

---

## §5 Wire / connector / fuse table

| Run | Wire | Color | Connector | Fuse |
|---|---|---|---|---|
| Mains L (E-stop ⇄ fuse ⇄ PSU L) | 16 AWG stranded 600 V | brown | ferrule into screw terminal | 2 A T (slow-blow) |
| Mains N | 16 AWG 600 V | blue | ferrule | – |
| Mains PE | 16 AWG 600 V | green/yellow | ring-lug to PSU FG | – |
| 24 V trunk (PSU → distribution) | 14 AWG | red | ferrule | 10 A fast (optional) |
| 24 V → TB6600 | 16 AWG | red | ferrule | – |
| 0 V trunk + branches | matched gauge | black | ferrule | – |
| 24 V → buck #1, buck #2 | 18 AWG | red / black | ferrule | – |
| 5 V → Mega VIN | 22 AWG | red | dupont or screw to Mega VIN | – |
| 5 V → Pi (if internal) | 18 AWG | red / black | 2.5×5.5 mm barrel OR direct to GPIO | – |
| Servo V+ / GND | 22 AWG | red / brown | JST-XH 3-pin | – |
| Servo signal | 22 AWG | orange | JST-XH 3-pin | – |
| TB6600 step / dir / en | 24 AWG | varied | dupont | – |
| Mega ↔ Pi | USB-A to USB-B | factory cable | – | – |
| NEMA 23 motor (4-wire) | 18 AWG | per motor | ferrule into TB6600 screw terminals | – |
| E-stop signal to Mega D2 | 24 AWG | yellow | dupont | – |

---

## §6 Wire color convention (lock now)

| Color | Meaning | Used for |
|---|---|---|
| Brown | Mains Live | Mains side only |
| Blue | Mains Neutral | Mains side only |
| Green/yellow | Mains PE | Earth bonding only |
| **Red** | DC positive (24 V or 5 V depending on context, labeled with tape) | All DC supply rails |
| **Black** | DC return (0 V / GND) | All DC returns |
| Orange | PWM / step / signal | Mega outputs to actuators |
| Yellow | Sensor / input signal | Mega inputs (E-stop, encoder, limit) |
| White | UART / SPI / I²C | Inter-controller signals |
| Grey | Ground reference, signal common | Multi-board GND ties |

> Pick this convention and **never** use a brown wire for anything except mains Live. The day you have to chase a fault at 2 AM you will thank yourself.

---

## §7 Bench-test procedure (Day 1 evening)

Build the wiring on a sheet of plywood / cardboard. Do not energize the machine frame yet.

### Stage 1 — PSU only

1. ☐ Wire mains side per §2.1 with E-stop and fuse
2. ☐ Verify PSU input voltage selector matches your mains (slide switch)
3. ☐ With NOTHING connected to PSU output: plug in
4. ☐ Multimeter on PSU output: should read **24.0 V ± 0.2 V**
5. ☐ Press E-stop: PSU should de-energize within ~1 second
6. ☐ Release E-stop: PSU re-energizes
7. ☐ Adjust the +V trimpot if needed (you measured its location for the guard)

### Stage 2 — Bucks + Mega

1. ☐ E-stop pressed (PSU off)
2. ☐ Wire Buck #1 input to 24 V bus
3. ☐ With Buck #1 output disconnected, release E-stop, adjust Buck #1 to **5.10 V** with multimeter, then E-stop again
4. ☐ Wire Buck #1 output to Mega VIN and GND
5. ☐ Release E-stop. Mega power LED should light. Plug USB to laptop.
6. ☐ Upload a blink sketch. LED 13 should blink.
7. ☐ Press E-stop. Mega should lose power within 1 second.

### Stage 3 — Bucks #2 + Pi

1. ☐ Repeat the same procedure for Buck #2 — adjust to 5.10 V no-load first
2. ☐ Wire Buck #2 to Pi 5 V GPIO (or use the USB-C wall wart for Option A)
3. ☐ Pi should boot, display should come up on the 7" touchscreen
4. ☐ E-stop test: Pi should also lose power if Buck #2 is fed from machine PSU (Option B); if using Option A wall wart, Pi stays up but Mega goes down — verify Pi gracefully shows "Mega disconnected"

### Stage 4 — TB6600 + NEMA 23

1. ☐ E-stop pressed. Wire TB6600 power (24 V), step/dir/enable (Mega D5/D6/D7), and motor coils.
2. ☐ Set TB6600 DIP switches: 8 µstep, 2.5 A current limit
3. ☐ Release E-stop. Upload a slow-pulse sketch to Mega.
4. ☐ Motor should rotate slowly and smoothly. If it stutters or skips: check microstep + current settings.
5. ☐ E-stop press: motor should stop immediately (mains gone)

### Stage 5 — Servos

1. ☐ E-stop pressed. Wire one MG90S to Mega D9 + Buck #1 5 V rail
2. ☐ Release E-stop. Run a sweep sketch (90° back and forth).
3. ☐ Confirm clean motion. If the servo jitters: voltage too low or noise on 5 V rail (separate Pi to a different buck).
4. ☐ Add servos one at a time up to 6. Verify all positions hold.

### Pass criteria

- ☐ PSU output stable 24.00 ± 0.10 V under combined load (stepper + 6 servos commanded)
- ☐ Both 5 V rails stable 5.00 ± 0.10 V under same load
- ☐ E-stop reliably kills power (both stages tested 3 times)
- ☐ Mega + Pi both boot clean after E-stop release
- ☐ Stepper motion is smooth (no skipping, no audible whine beyond normal stepper hum)
- ☐ All 6 servos hold position without jitter

If all pass: electronics are validated, no machine-installation issues will be electrical. If any fail: fix on the bench, not in the machine.

---

## §8 Open items / questions

These are TBD or need decisions before the final install (not blocking the bench test):

- [ ] Mains plug type for your region (US NEMA 5-15? Europe Schuko? UK BS 1363?) — affects the inlet connector spec
- [ ] E-stop mushroom button: BOM doesn't show this purchased yet — confirm it's on order or order one. Look for **22 mm panel-mount, NC + NC (double pole), latching, rated 10 A / 250 V min**
- [ ] AC inlet: panel-mount IEC-C14 (kettle plug) is standard for machines like this and lets you use any region's cable — recommend this over hard-wired mains
- [ ] PSU mounting: confirm orientation on deck (vents should not be obstructed)
- [ ] Future encoder on cylinder: where will encoder signals route? Add 2 wires (A, B + V+ + GND = 4 wires) to the 24V-bus side now if possible
- [ ] Cable strain reliefs: 1 grommet per cable entry point on the deck

---

## §9 Revision log

| Rev | Date | Author | Change |
|---|---|---|---|
| V1.0 | 2026-05-28 | claude | Initial wiring diagram, derived from BOM V12 + datasheet S-250-24 |
