#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSM V3 -- ENGINEERING POSTER SET

Composes the existing rendered PNGs (Y1-Y3, K_triad_*, D1-D5, capture-margin
plots) into 6 labeled engineering plates:

  Poster 3  Yarn Path & Knitting Logic        (behavior first)
  Poster 4  Kinematic Triad
  Poster 2  Drivetrain & Power Flow
  Poster 5  Service & Maintenance Architecture
  Poster 6  Dynamic Failure Analysis
  Poster 1  Machine Architecture Overview     (aesthetics last)

No 3D rendering -- pure matplotlib + image composition. Designed for
clarity / annotation, not photorealism. Each poster answers ONE question.

Usage:
  py build_posters.py [poster_number]    # e.g. 3, or no arg for all
"""
import os, sys, csv
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
except ImportError:
    print("Need matplotlib: py -m pip install matplotlib"); sys.exit(1)

RENDERS = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders"
OUT_DIR = os.path.join(RENDERS, "posters")
os.makedirs(OUT_DIR, exist_ok=True)

def load_image(name):
    path = os.path.join(RENDERS, name)
    if not os.path.exists(path):
        print(f"  WARN missing: {path}")
        return None
    return mpimg.imread(path)

def panel(ax, img, title=None, hide_axes=True):
    if img is not None:
        ax.imshow(img)
    if title:
        ax.set_title(title, fontsize=11, fontweight='bold', loc='left')
    if hide_axes:
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values(): s.set_visible(False)

def title_block(fig, poster_num, title, subtitle):
    fig.text(0.02, 0.97, f"POSTER {poster_num}", fontsize=10, color='#666666',
             fontweight='bold')
    fig.text(0.02, 0.945, title, fontsize=18, fontweight='bold', color='#1a2a4a')
    fig.text(0.02, 0.925, subtitle, fontsize=11, color='#333333', style='italic')
    fig.text(0.98, 0.97, "CSM V3 PHASE 1", fontsize=9, color='#888888',
             ha='right', fontweight='bold')
    fig.text(0.98, 0.945, "behavioral plate", fontsize=9, color='#888888',
             ha='right', style='italic')

def annotation_block(ax, lines, x=0.02, y=0.98, ha='left', va='top',
                     fontsize=9, color='#222', bg='#f4f4f0'):
    text = "\n".join(lines)
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va,
            fontsize=fontsize, color=color,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=bg,
                      edgecolor='#888888', linewidth=0.8))

# ============================================================
# POSTER 3 -- Yarn Path & Knitting Logic
# ============================================================
def build_poster_3():
    print("Building Poster 3 -- Yarn Path & Knitting Logic")
    fig = plt.figure(figsize=(17, 12), facecolor='#fafafa')
    title_block(fig, "3", "Yarn Path & Knitting Logic",
                "how thread becomes fabric -- cone, tensioner, capture, loop, take-down")

    # 4-panel layout: left big = Y1 full 3/4 isometric; right column = Y2 side,
    # Y3 top, D3 triad close-up
    gs = fig.add_gridspec(3, 3, left=0.04, right=0.98, top=0.90, bottom=0.05,
                          wspace=0.10, hspace=0.18,
                          height_ratios=[1, 1, 1], width_ratios=[1.6, 1, 1])

    ax1 = fig.add_subplot(gs[:, 0])
    panel(ax1, load_image("CSM_V3_YarnPath_Y1_full.png"),
          title="Full machine yarn route (3/4 view)")
    annotation_block(ax1, [
        "WAYPOINTS (Phase-1.5 capture flow)",
        "1. Cone-top    (yarn unwinds from spool)",
        "2. Upper guide eye",
        "3. Tensioner   (yarn drag modulation)",
        "4. Feeder nozzle exit  (Z = 271 mm, r = 95 mm)",
        "5. HOOK PEAK   (Z = 264 mm, r = 56.15 mm)",
        "6. Loop formation  (knock-over by sinker)",
        "7. Fabric tube descent (through cylinder bore)",
        "8. Take-down exit  (Ø100 mm hole in wood base)",
        "",
        "Yarn ownership transitions (Slot #0 frame of",
        "reference) define knitting rhythm at 1:15",
        "motor-to-cylinder reduction (5x gearbox * 3x belt).",
    ], x=0.02, y=0.98, fontsize=8.5)

    ax2 = fig.add_subplot(gs[0, 1:])
    panel(ax2, load_image("CSM_V3_YarnPath_Y2_side.png"),
          title="Vertical journey: cone -> cassette -> take-down (side section)")

    ax3 = fig.add_subplot(gs[1, 1:])
    panel(ax3, load_image("CSM_V3_YarnPath_Y3_top.png"),
          title="In-plane geometry (top view): feeder F1 / F4 + capture aperture")

    ax4 = fig.add_subplot(gs[2, 1:])
    panel(ax4, load_image("CSM_V3_KinematicTriad_K_triad_top.png"),
          title="Loop control aperture (retainer lip ID 104 mm, hook sweep at 113 mm)")
    annotation_block(ax4, [
        "Yarn capture zone = annular band",
        "between retainer lip ID (104) and",
        "hook sweep circle (113.3). 9.3 mm",
        "radial budget per stitch. Compliance,",
        "feeder lag, hook timing all eat into",
        "this margin (see Poster 6).",
    ], x=0.02, y=0.05, va='bottom', fontsize=8)

    out = os.path.join(OUT_DIR, "P3_yarn_path_and_knitting_logic.png")
    plt.savefig(out, dpi=120, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  -> {out}")

# ============================================================
# POSTER 4 -- Kinematic Triad
# ============================================================
def build_poster_4():
    print("Building Poster 4 -- Kinematic Triad")
    fig = plt.figure(figsize=(17, 11), facecolor='#fafafa')
    title_block(fig, "4", "Kinematic Triad -- Why Stitch Formation Works",
                "feeder exit / retainer lip / hook peak -- the 9.3 mm radial budget")

    gs = fig.add_gridspec(2, 2, left=0.04, right=0.98, top=0.88, bottom=0.04,
                          wspace=0.10, hspace=0.18)

    for ax, src, ttl in [
        (fig.add_subplot(gs[0, 0]), "CSM_V3_KinematicTriad_K_triad_3q.png",
         "3/4 perspective: cassette top with triad geometry"),
        (fig.add_subplot(gs[0, 1]), "CSM_V3_KinematicTriad_K_triad_top.png",
         "Top: retainer lip aperture + hook sweep + feeders F1/F4"),
        (fig.add_subplot(gs[1, 0]), "CSM_V3_KinematicTriad_K_triad_side.png",
         "Side section: vertical Z stack of cassette"),
        (fig.add_subplot(gs[1, 1]), "CSM_V3_KinematicTriad_K_triad_front.png",
         "Front: cassette + drive train + retainer lip plane"),
    ]:
        panel(ax, load_image(src), title=ttl)

    # Big text box bottom-right summarizing the triad geometry
    fig.text(0.62, 0.115, "TRIAD GEOMETRY (world Z, mm)", fontsize=11,
             fontweight='bold', color='#1a2a4a')
    fig.text(0.62, 0.04,
             "Cylinder top         256\n"
             "Hook PEAK            264   <- critical capture plane\n"
             "Retainer lip ubside  270   <- upper safety bound\n"
             "Feeder exit          271   <- yarn presentation plane\n"
             "\n"
             "Hook cam stroke       8 mm  (Z 256 .. 264)\n"
             "Retainer clearance    6 mm  (above hook peak)\n"
             "Feeder above hook     7 mm  (gravity drop window)\n"
             "Lip-to-hook aperture  9.3 mm radial",
             fontsize=9, color='#222', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff8e8',
                       edgecolor='#aaa', linewidth=0.8))

    out = os.path.join(OUT_DIR, "P4_kinematic_triad.png")
    plt.savefig(out, dpi=120, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  -> {out}")

# ============================================================
# POSTER 2 -- Drivetrain & Power Flow
# ============================================================
def build_poster_2():
    print("Building Poster 2 -- Drivetrain & Power Flow")
    fig = plt.figure(figsize=(17, 11), facecolor='#fafafa')
    title_block(fig, "2", "Drivetrain & Power Flow",
                "NEMA 23 -> 5:1 gearbox -> 3:1 belt -> 12 mm shaft -> cylinder")

    gs = fig.add_gridspec(2, 2, left=0.04, right=0.98, top=0.88, bottom=0.05,
                          wspace=0.10, hspace=0.18)

    # Use D2 side, D1 iso, D3 triad-of-drivetrain-from-top
    panel(fig.add_subplot(gs[0, 0]), load_image("CSM_V3_Diagram_D2_side_section.png"),
          title="Vertical stack (side): motor + gearbox + pulleys + shaft")
    panel(fig.add_subplot(gs[0, 1]), load_image("CSM_V3_Diagram_D1_isometric.png"),
          title="Drivetrain in machine context (3/4)")
    panel(fig.add_subplot(gs[1, 0]), load_image("CSM_V3_Diagram_D5_layer_separation.png"),
          title="Layer separation: precision / structural / automation")

    # Right-bottom: text spec block, power flow
    ax_text = fig.add_subplot(gs[1, 1])
    ax_text.axis('off')
    ax_text.text(0.02, 0.98,
        "POWER PATH (BOM-aligned)\n"
        "\n"
        "  NEMA 23 stepper      2.8 N.m holding\n"
        "      |   PWM step/dir via TB6600 4A driver\n"
        "      v\n"
        "  5:1 planetary gearbox   ~14 N.m at output\n"
        "      |   gearbox output: 14 mm shaft\n"
        "      v\n"
        "  60T HTD 5M pulley       Ø97.5 mm\n"
        "      |   HTD belt, 405 mm pitch, 15 mm wide\n"
        "      v\n"
        "  20T HTD 5M pulley       Ø33.3 mm\n"
        "      |   3:1 belt reduction\n"
        "      v\n"
        "  12 mm h8 drive shaft (300 mm)\n"
        "      |   floating-top / fixed-bottom\n"
        "      |   bearings 6001-2RS + 51101 thrust\n"
        "      v\n"
        "  Drive Hub V2.4.2\n"
        "      |   M5 x 4 at PCD 70, into cylinder\n"
        "      v\n"
        "  Cylinder V3.0  (114.3 mm OD, 72 slots)\n"
        "\n"
        "TOTAL REDUCTION: 15:1 motor -> cylinder\n"
        "EST. CYLINDER TORQUE: ~25-30 N.m (after losses)\n"
        "BELT TENSION TRAVEL: 30 mm motor X-slot (SE5)",
        fontsize=9, color='#222', fontfamily='monospace', va='top',
        bbox=dict(boxstyle='round,pad=0.7', facecolor='#fff8e8',
                  edgecolor='#aaa', linewidth=0.8))

    out = os.path.join(OUT_DIR, "P2_drivetrain_power_flow.png")
    plt.savefig(out, dpi=120, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  -> {out}")

# ============================================================
# POSTER 5 -- Service & Maintenance
# ============================================================
def build_poster_5():
    print("Building Poster 5 -- Service & Maintenance")
    fig = plt.figure(figsize=(17, 11), facecolor='#fafafa')
    title_block(fig, "5", "Service & Maintenance Architecture",
                "five protected envelopes SE1-SE5 -- can a human actually maintain this?")

    gs = fig.add_gridspec(2, 2, left=0.04, right=0.98, top=0.88, bottom=0.05,
                          wspace=0.10, hspace=0.18)

    panel(fig.add_subplot(gs[0, 0]), load_image("CSM_V3_AssemblyDrawing_C_iso.png"),
          title="ISO view with all 5 service envelopes overlaid")
    panel(fig.add_subplot(gs[0, 1]), load_image("CSM_V3_AssemblyDrawing_C_top.png"),
          title="Top: envelope footprint + maintenance vectors")
    panel(fig.add_subplot(gs[1, 0]), load_image("CSM_V3_AssemblyDrawing_C_front.png"),
          title="Front: extraction arrows (red=lift, blue=feeder, yellow=belt, green=take-down)")

    ax_text = fig.add_subplot(gs[1, 1])
    ax_text.axis('off')
    ax_text.text(0.02, 0.98,
        "SERVICE ENVELOPES (SE1-SE5)\n"
        "\n"
        "SE1  Cylinder removal\n"
        "     Vertical lift through Z=272..395\n"
        "     -- without disturbing mast, uprights, feeders\n"
        "\n"
        "SE2  Cam ring extraction\n"
        "     Annular ring at Z=200..230\n"
        "     -- M5 access from below\n"
        "\n"
        "SE3  Feeder swing-out\n"
        "     6 wedges at PCD 190, 60 deg each\n"
        "     -- M4 access from above\n"
        "\n"
        "SE4  Yarn threading\n"
        "     Front +Y arc Z=240..300\n"
        "     -- operator hand path, eye line\n"
        "\n"
        "SE5  Belt replacement\n"
        "     Motor X-travel 30 mm slot\n"
        "     -- belt lift over pulleys\n"
        "\n"
        "I-11 Sock take-down column\n"
        "     Vertical Ø100 mm reserved\n"
        "     -- gravity / weight / vacuum (future)\n"
        "\n"
        "All envelopes are independently invokable.\n"
        "Maintenance vectors documented in\n"
        "SERVICE_ENVELOPES.md R1.",
        fontsize=9, color='#222', fontfamily='monospace', va='top',
        bbox=dict(boxstyle='round,pad=0.7', facecolor='#eef8ee',
                  edgecolor='#aaa', linewidth=0.8))

    out = os.path.join(OUT_DIR, "P5_service_maintenance.png")
    plt.savefig(out, dpi=120, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  -> {out}")

# ============================================================
# POSTER 6 -- Dynamic Failure Analysis
# ============================================================
def build_poster_6():
    print("Building Poster 6 -- Dynamic Failure Analysis")
    fig = plt.figure(figsize=(17, 12), facecolor='#fafafa')
    title_block(fig, "6", "Dynamic Failure Analysis -- Operating Envelope",
                "Phase 1.5 simulator results -- tolerances derived from behavior, not intuition")

    gs = fig.add_gridspec(3, 2, left=0.04, right=0.98, top=0.88, bottom=0.05,
                          wspace=0.10, hspace=0.22, height_ratios=[1.2, 1.2, 0.8])

    panel(fig.add_subplot(gs[0, :]), load_image("operating_envelope_plot.png"),
          title="A. Operating envelope: worst-case capture margin vs sweep parameter")
    panel(fig.add_subplot(gs[1, :]), load_image("delta_from_nominal_plot.png"),
          title="B. Delta from nominal -- Δm(θ) = m_failure - m_nominal")

    ax_text = fig.add_subplot(gs[2, :])
    ax_text.axis('off')
    ax_text.text(0.02, 0.95,
        "TOLERANCES DERIVED FROM BEHAVIOR (acceptable at +-2 mm Z capture margin)",
        fontsize=11, fontweight='bold', color='#1a2a4a', va='top')
    ax_text.text(0.02, 0.78,
        "A1  Feeder lag           <= 10 deg     PHASE-sensitive  (narrow capture window only)\n"
        "B1  Yarn slack           <=  2 mm      AMPLITUDE-sensitive  (uniform offset, gravity)\n"
        "D1  Yarn miss / overlift =   0 mm      AMPLITUDE-sensitive  (nominal already at edge)",
        fontsize=10, fontfamily='monospace', color='#222', va='top')
    ax_text.text(0.02, 0.30,
        "DIAGNOSTIC IMPLICATIONS:\n"
        "  - Phase-asymmetric failures -> timing problem (feeder lag, gearbox backlash, belt windup)\n"
        "  - Uniform offset failures   -> tension or geometry problem (take-down, retainer setup)\n"
        "  - HIERARCHY OF FRAGILITY: D1 miss > B1 slack > A1 lag",
        fontsize=9.5, color='#333', va='top', style='italic')

    out = os.path.join(OUT_DIR, "P6_failure_analysis.png")
    plt.savefig(out, dpi=120, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  -> {out}")

# ============================================================
# POSTER 1 -- Architecture Overview
# ============================================================
def build_poster_1():
    print("Building Poster 1 -- Architecture Overview")
    fig = plt.figure(figsize=(17, 11), facecolor='#fafafa')
    title_block(fig, "1", "Machine Architecture Overview",
                "compact industrial knitting head -- suspended precision core, layered subsystems")

    gs = fig.add_gridspec(2, 3, left=0.04, right=0.98, top=0.88, bottom=0.05,
                          wspace=0.08, hspace=0.18, width_ratios=[1.6, 1, 1])

    panel(fig.add_subplot(gs[:, 0]), load_image("CSM_V3_Diagram_D1_isometric.png"),
          title="Full isometric -- BOM-aligned geometry")
    panel(fig.add_subplot(gs[0, 1]), load_image("CSM_V3_Diagram_D4_top_plan.png"),
          title="Top plan: PCDs + theta=0 ref")
    panel(fig.add_subplot(gs[0, 2]), load_image("CSM_V3_Diagram_D5_layer_separation.png"),
          title="Layer separation (exploded)")
    panel(fig.add_subplot(gs[1, 1]), load_image("CSM_V3_Diagram_D2_side_section.png"),
          title="Side elevation")
    panel(fig.add_subplot(gs[1, 2]), load_image("CSM_V3_Diagram_D3_triad.png"),
          title="Triad close-up")

    out = os.path.join(OUT_DIR, "P1_architecture_overview.png")
    plt.savefig(out, dpi=120, facecolor=fig.get_facecolor())
    plt.close()
    print(f"  -> {out}")

# ============================================================
# DISPATCH
# ============================================================
ALL_POSTERS = {
    "1": build_poster_1,
    "2": build_poster_2,
    "3": build_poster_3,
    "4": build_poster_4,
    "5": build_poster_5,
    "6": build_poster_6,
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for n in sys.argv[1:]:
            if n in ALL_POSTERS:
                ALL_POSTERS[n]()
    else:
        # Per user-recommended order: 3, 4, 2, 5, 6, 1
        for n in ["3", "4", "2", "5", "6", "1"]:
            ALL_POSTERS[n]()
    print(f"\nAll output in {OUT_DIR}")
