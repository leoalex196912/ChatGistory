# CSM_V3_ASSEMBLY

```
Created:    2026-05-20
Purpose:    Isolated workspace for the "real-geometry full-assembly"
            build. Everything new lives here. The existing locked
            mechanical components (cylinder, cam ring, sinker,
            cassette base, retainer, drive hub, motor mount, bearing
            housings) stay in their original folders under 3D-Project/
            and are imported by the assembly script -- not modified.
```

## Why this folder exists

The previous Blender render was half engineering geometry + half
primitive boxes/cylinders. To fix that, we are modeling every
remaining component (frame, motor, pulleys, belt, bearings,
electronics, screen, yarn cones, etc.) as a proper parametric
FreeCAD macro that exports an STL.

This folder isolates all that new work from the existing locked
geometry tree. Nothing in `3D-Project/01_MECHANICAL/02_CASSETTE_HEAD/`
gets touched.

## Layout

```
CSM_V3_ASSEMBLY/
  frame/
    wood_shelf_mid/    -- 500x400x18 hardwood, top at Z=49
    wood_base/         -- 500x400x18 hardwood, bottom of stand
    upright_2020/      -- 4x 20x20mm anodized aluminum extrusion
    mount_plate_6061/  -- 150x150x6 aluminum, under cassette base

  drive_bought/
    nema17_stepper/    -- 42.3x42.3x40 motor body + 5mm shaft
    pulley_htd_60t/    -- HTD 5M, OD 97.5, 12mm bore (cylinder side)
    pulley_htd_16t/    -- HTD 5M, OD 27.4, 5mm bore (motor side)
    belt_htd_5m/       -- closed-loop HTD 5M belt, 15mm wide

  bearings_bought/
    bearing_6001_2rs/  -- 28 OD x 12 ID x 8 W, x2
    shaft_12mm/        -- 12mm OD FEYRINX h8 steel shaft

  electronics/
    arduino_mega_2560/ -- 101x53x15 mm
    tb6600_driver/     -- 96x56x33 mm with heatsink fins
    lrs50_psu/         -- 99x82x30 mm Mean Well power supply
    touchscreen_7in/   -- 165x100x10 mm HDMI screen
    touchscreen_arm/   -- 3D-printed goose-neck arm to mount screen
                          on a 2020 upright

  decor/
    yarn_cone/         -- truncated cone, base D70 x top D40 x H130

  full_assembly/
    blender_scripts/   -- stage1..stageN.py (import + materials +
                          lighting + camera + render)
    renders/           -- CSM_V3_Assembly_Hero.png and variants
    assembly_manifest.md  -- single source of truth for what STLs
                             the assembly loads and from where
```

## Conventions per component

Each component folder has:
```
<component>/
  freecad_macros/
    CSM_V3_<Name>_V1_0.FCMacro    -- parametric source
  CSM_V3_<Name>_V1_0.stl          -- generated output (committed)
  _archive/                       -- previous versions (created on V2+)
```

Naming: `CSM_V3_<PartName>_V<major>_<minor>[.<patch>]`

Macro style: matches the existing project pattern
  - Header banner with date + what + why
  - PARAMETER section first (all dimensions named, no magic numbers)
  - DERIVED section computing dependent values
  - STARTUP REPORT printing key dims for verification
  - BUILD section with numbered `[N/M]` progress prints
  - EXPORT section saving STL via Part.export([...], path)
  - GUI-guarded PNG section: `if FreeCAD.GuiUp:` so headless runs work

## How to rebuild any single component

Each macro runs HEADLESSLY via FreeCAD's bundled Python (no GUI):

```
"C:\Program Files\FreeCAD 1.1\bin\python.exe" path\to\CSM_V3_X_V1_0.FCMacro
```

That writes the STL next to the macro. No FreeCAD app needs to be open.

## How to rebuild the full assembly render

After any component changes:

```
"C:\Program Files\Blender Foundation\Blender X.X\blender.exe" \
   --background --python full_assembly\blender_scripts\render_hero.py
```

Output: `full_assembly\renders\CSM_V3_Assembly_Hero.png`

## Cross-references

- Locked component dimensions: `../3D-Project/00_PROJECT_OVERVIEW/MACHINE_DATUMS.md`
- Interface control: `../3D-Project/00_PROJECT_OVERVIEW/INTERFACE_CONTROL.md`
- BOM (purchased parts): `../3D-Project/04_PURCHASING/BOM_V11/`
