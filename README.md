# CRT Modeline Toolbox

**Interactive calculation, verification and optimisation tool for CRT monitor modelines**

*Stéphane "ZFEbHVUE" — v2.0*

---

## GUI toolbox
![CRT-MODELINE-TOOLBOX GUI](docs/gui_main.png)

---

## Overview

**CRT Modeline Toolbox** is a Python/Tkinter desktop application for generating, verifying and optimising video modelines destined for CRT monitors running at 15 kHz, 25 kHz or 31 kHz — the native frequencies of arcade monitors, PAL/NTSC television sets and retro gaming setups.

It is designed to complement:
- [SwitchRes](https://github.com/antonioginer/switchres) by **Calamity** (Antonio Giner) — the reference modeline calculator used by GroovyMAME and RetroArch
- [Batocera-CRT-Script](https://github.com/ZFEbHVUE/Batocera-CRT-Script) — CRT support scripts for Batocera Linux

The toolbox bridges the gap between the **time domain** (µs/ms porch values stored in `switchres.ini` `crt_range` lines) and the **pixel domain** (integer counts used in `xrandr --newmode` modeline strings), while making the rounding errors and physical constraints fully visible and interactive.

---

## Background — what is a CRT modeline?

A modeline encodes the complete timing of the video signal sent to a CRT monitor. Every value has a precise physical meaning:

```
Modeline "768x576i" 15.578125  768 799 872 997  576 578 603 625  interlace -hsync -vsync
                    │           │   │   │   │    │   │   │   │
                    pixel_clock H1  H2  H3  H4   V1  V2  V3  V4
```

| Field | Meaning |
|---|---|
| `pixel_clock` | Dot clock in MHz — drives the DAC |
| `H1` | Horizontal active resolution |
| `H2` | H1 + H Front Porch |
| `H3` | H2 + H Sync pulse |
| `H4` | H3 + H Back Porch = **H total** |
| `V1` | Vertical active resolution |
| `V2` | V1 + V Front Porch |
| `V3` | V2 + V Sync pulse |
| `V4` | V3 + V Back Porch = **V total** |

The key timing relationships are:

```
Hfreq  =  pixel_clock × 10⁶ / H_total                    (Hz)
Vfreq  =  Hfreq / V_total              (progressive)
Vfreq  =  Hfreq × 2 / V_total         (interlaced)

H_total_time  =  1 / Hfreq            →  64.000 µs  for PAL 15.625 kHz
V_total_time  =  1 / Vfreq            →  20.000 ms  for PAL 50 Hz (per field)
```

For PAL 15 kHz, the canonical values are:
- **Hfreq = 15.625 kHz** → H_total time = **64.000 µs** exactly
- **Vfreq = 50.000 Hz** → V_total time = **20.000 ms** per field exactly

---

## Physical meaning of the blanking intervals

Each porch and sync interval has a specific physical role in the CRT signal:

| Interval | Physical role |
|---|---|
| **H Front Porch** | Time for the scan line circuits to settle before the sync pulse is detected |
| **H Sync** | Pulse that triggers the horizontal oscillator reset in the chassis |
| **H Back Porch** | Beam flyback time (right → left) + circuit stabilisation before visible image |
| **V Front Porch** | Time after last visible line before the vertical sync pulse |
| **V Sync** | Pulse that resets the vertical deflection oscillator |
| **V Back Porch** | Beam flyback time (bottom → top) + stabilisation before first visible line |

The **CRT_RANGE** values in `switchres.ini` define **minimum physical times** (in µs/ms) for each interval based on the monitor chassis characteristics. SwitchRes uses them as constraints, not exact targets — the actual pixel counts are scaled proportionally via TERM_H / TERM_V.

---

## Why CRT Range values never round-trip exactly

The CRT Range stores porch times as **continuous floating-point values** (µs/ms). Converting to pixel counts requires multiplication by TERM_H or TERM_V followed by integer rounding — an irreducible quantisation error:

```
HFrontPorch input  =  2.000 µs          (Calamity's crt_range)
→ HFP pixels       =  round(2.000 × TERM_H)  =  31 px
→ HFrontPorch back =  31 / 997 / 15625 × 10⁶  =  1.990 µs  ≠  2.000
```

The pixel is the atomic unit of the signal. This is why the toolbox always shows **two distinct CRT Range lines** — the Calamity reference (frozen at preset selection) and the values back-calculated from the generated modeline — so the quantisation error is immediately visible.

---

## Features

### Generate tab

#### Monitor / Range
- Select from **23 monitor presets** (sourced from Calamity/SwitchRes built-in definitions)
- Multi-range monitors (Arcade 15/25/31 kHz, Wells Gardner D9800 with 6 ranges, etc.) — select the active frequency range from the **Range** dropdown
- Changing Hfreq auto-switches the range on multi-range presets

#### Paste CRT Range
- Paste any `crt_range0` line directly from a `switchres.ini` or a saved file
- Press **Enter** or **Parse → apply to sliders** to load all values into the sliders instantly
- Accepts the full format with or without the `crt_range0` prefix

#### Parameters (µs / ms domain)
All values are editable via **slider + direct keyboard entry** — both stay synchronised:
- **H Width** and **V Height** — active resolution in pixels
- **Hfreq** — target horizontal frequency in kHz (auto-switches range on multi-range presets)
- **Vfreq** — target vertical frequency in Hz

#### CRT Range (µs / ms domain)
Six sliders with direct keyboard entry for the porch and sync times:
- **H Front Porch**, **H Sync**, **H Back Porch** in µs
- **V Front Porch**, **V Sync**, **V Back Porch** in ms

Changes trigger recalculation via the TERM_H / TERM_V proportional method — the same algorithm used by SwitchRes.

#### Direct Porch Adjustment (px / lines)
A dedicated frame with six additional sliders in the **integer pixel / line domain**:
- **H Front Porch (px)**, **H Sync (px)**, **H Back Porch (px)**
- **V Front Porch (lines)**, **V Sync (lines)**, **V Back Porch (lines)**

When you adjust a pixel slider:
- The modeline is recalculated directly from the pixel counts
- The µs/ms sliders update automatically with the back-calculated times
- This is particularly useful for directly setting VSync to a specific number of lines without computing the equivalent ms manually

When you adjust a µs/ms slider:
- The pixel sliders update automatically with the resulting pixel counts

Both domains are always synchronised.

#### CRT Range displays
Two side-by-side read-only fields:
- **Calamity values (fixed to preset)** — the original preset values, unchanged as long as the preset is not switched. Relabelled **Custom (pasted)** when a custom range is loaded via Paste
- **Calculated from generated modeline** — the CRT Range back-calculated from the actual integer pixel counts, showing the quantisation error versus Calamity's reference

#### Timings table
Full breakdown of all horizontal and vertical intervals in both px/lines and µs/ms:

| Parameter | px/lines | Time | Unit |
|---|---|---|---|
| H active | 768 | 49.300 | µs |
| H Front Porch | 31 | 1.990 | µs |
| H Sync | 73 | 4.686 | µs |
| H Back Porch | 125 | 8.024 | µs |
| **H total** | **997** | **64.000** | **µs** |
| V active | 576 | 18.432 | ms |
| V Front Porch | 2 | 0.064 | ms |
| V Sync | 8 | 0.256 | ms |
| V Back Porch | 39 | 1.248 | ms |
| **V total** | **625** | **20.000** | **ms** |

#### Metrics
- Pixel clock (MHz), Hfreq (kHz), Vfreq (Hz)
- H total (px), V total (lines), H blanking (px)

#### Verification
Three colour-coded checks against the selected monitor preset:
- ✓ / ✗  Hfreq within [hmin–hmax] Hz
- ✓ / ✗  Vfreq within [vfmin–vfmax] Hz
- ✓ / ✗  V lines within progressive or interlaced limits

#### Modeline and xrandr command
Ready-to-use output in both formats:
```
Modeline "768x576i" 15.578125 768 799 872 997 576 578 603 625 interlace -hsync -vsync

xrandr --newmode "768x576i" 15.578125 768 799 872 997 576 578 603 625 interlace -hsync -vsync
xrandr --addmode DP-1 "768x576i"
xrandr --output DP-1 --mode "768x576i"
```

#### Action buttons
| Button | Action |
|---|---|
| **Copy xrandr** | Copies the three xrandr commands to the clipboard |
| **Apply xrandr** | Executes the xrandr commands directly on the running system |
| **⚡ Optimise (LS)** | Runs the least-squares optimiser (see below) |
| **💾 Save CRT Range** | Saves the current result to a named text file |
| **📂 Load CRT Range** | Opens a previously saved file and applies it to the sliders |

---

### Verify tab

Paste any modeline string (SwitchRes output or xrandr format) and instantly see:
- Full timing decomposition in px/lines and µs/ms
- Hfreq, Vfreq, pixel_clock computed from the raw numbers
- Verification against the selected monitor preset (auto-selects the correct frequency range for multi-range monitors)
- CRT Range back-calculated from the modeline — useful for generating a custom `crt_range` line for `switchres.ini`
- Ready-to-use xrandr commands

---

## Least-squares optimiser (⚡ Optimise LS)

The optimiser solves the problem of finding the **best integer modeline** for a given set of target frequencies.

### Why it is needed

SwitchRes's TERM_H / TERM_V method produces good modelines for any given Vfreq, but the resulting Vfreq is determined by rounding V_total — it may not hit the target exactly. For example, PAL 50 Hz requires V_total = 625 exactly, which only works if Hfreq × 2 / 625 = 50.000 exactly — which is true only for Hfreq = 15.625 kHz.

### Algorithm

**Step 1 — Hfreq exact**
The pixel clock is a continuous floating-point value, so Hfreq can always be achieved exactly:
```
pixel_clock = Hfreq_target × H_total / 10⁶  (MHz, exact)
```

**Step 2 — optimal integer V_total**
V_total must be an integer. The algorithm searches ±10 lines around the ideal value:
```
V_total_ideal = Hfreq_target × Div / Vfreq_target
```
and selects the integer that minimises `|Hfreq × Div / V_total − Vfreq_target|`.

For PAL: V_total_ideal = 15625 × 2 / 50 = 625.000 → exact, Vfreq error = 0.000000 Hz.

**Step 3 — TERM_V proportional targets**
Rather than using raw minimum times as targets (which produces physically small porches), the optimiser uses the same **TERM_V proportional scaling** as SwitchRes to compute target pixel counts. This ensures the porch proportions remain physically meaningful.

**Step 4 — largest-remainder distribution**
The blanking pixels are distributed among the three components (FP, Sync, BP) using the **largest-remainder method** (also used in proportional electoral systems) — the integer rounding method that minimises the total squared error.

### Result for 768×576i @ 15.625 kHz / 50 Hz

```
V Front Porch =  2 lines  (0.064 ms)  ← matches Calamity
V Sync        =  8 lines  (0.256 ms)  ← slightly more than Calamity's 6 lines
V Back Porch  = 39 lines  (1.248 ms)  ← proportional
V total       = 625       (20.000 ms) ← PAL exact ✓
Vfreq error   = 0.000000 Hz ✓
```

### Physical caveat

The optimiser targets are based on **Calamity's generic CRT_RANGE** values, which are conservative envelopes valid for a monitor category (e.g., all 15 kHz arcade monitors), not the exact physical requirements of a specific chassis. The optimal porch values for a given monitor can only be determined precisely by oscilloscope measurement or empirical testing. The optimiser guarantees mathematical correctness within the CRT_RANGE constraints — physical validation on the actual hardware is always recommended.

---

## DP custom (ZFEbHVUE) preset

The `DP custom (ZFEbHVUE)` preset uses a **V Sync pulse of 0.480 ms** instead of Calamity's standard 0.192 ms. This was found empirically to be necessary for DisplayPort-to-VGA adapters based on the **Realtek RTD2166** chip (which integrates its oscillator into the die — no external crystal is visible on the PCB) when used with AMD GPU DisplayPort outputs for 768×576i PAL content.

The standard 6-line V Sync pulse (~0.192 ms) is too short for these adapters to reliably detect and lock the vertical sync signal. Extending it to 0.480 ms resolves the issue.

Note that the RTD2166's integrated oscillator means its reference frequency is fixed inside the silicon — adapters built around this chip may behave differently from apparently identical units due to silicon revision differences or manufacturing variations, even when sharing the same part number.

---

## Monitor presets

All presets are sourced from Calamity's official SwitchRes monitor definitions.

| Preset | Frequency ranges |
|---|---|
| PAL TV | 15 kHz fixed |
| NTSC TV | 15 kHz fixed |
| Generic 15 kHz | 15 kHz |
| Arcade 15 kHz | 15 kHz |
| Arcade 15 kHz EX | 15 kHz |
| Arcade 25 kHz | 25 kHz |
| Arcade 31 kHz | 31 kHz |
| Arcade 15/25 kHz | 15 kHz + 25 kHz |
| Arcade 15/31 kHz | 15 kHz + 31 kHz |
| Arcade 15/25/31 kHz | 15 kHz + 25 kHz + 31 kHz |
| Wells Gardner D9800/D9400 | 15 / 18 / 25 / 31 / 33 / 36 kHz |
| Wells Gardner D9200 | 15 / 24 / 31 / 37 kHz |
| Wells Gardner K7000 | 15 kHz |
| Wells Gardner 25K7131 | 15 kHz |
| Nanao MS-2930/2931 | 15 / 24 / 31 kHz |
| Nanao MS9-29 | 15 / 24 kHz |
| Hantarex MTC 9110 / Polo | 15 kHz |
| Hantarex Polostar 25 | 15 / 16 / 25 / 31 kHz |
| Makvision 2929D | 31 kHz |
| Wei-Ya M3129 | 15 / 24 / 31 kHz |
| Rodotron 666B-29 | 15 / 24 / 31 kHz |
| PC CRT 31 kHz/120 Hz | 31 kHz/60 Hz + 31 kHz/120 Hz |
| PC CRT 70 kHz/120 Hz | 70 kHz/60 Hz + 70 kHz/120 Hz |
| **DP custom (ZFEbHVUE)** | 15 kHz PAL — extended V Sync for DP2VGA |

---

## Save and Load CRT Range

The **💾 Save CRT Range** button saves the current result to a named text file containing:
- Monitor name and active range
- Resolution, Hfreq, Vfreq
- Calamity reference CRT Range (for comparison)
- Calculated CRT Range (from the generated modeline)
- Modeline string
- xrandr commands

Example saved file:
```
# CRT Modeline Toolbox — ZFEbHVUE
# Monitor  : Arcade 15kHz  [15KHz]
# Resolution: 768x576i  Hfreq=15.625 kHz  Vfreq=50.000 Hz  Interlaced=Yes

# --- Calamity preset (reference) ---
crt_range0  15625-16200, 49.50-65.00, 2.000, 4.700, 8.000, 0.064, 0.192, 1.024, 0, 0, 192, 288, 448, 576

# --- Calculated from generated modeline ---
crt_range0  15625-16200, 49.50-65.00, 1.990, 4.686, 8.024, 0.064, 0.256, 1.248, 0, 0, 192, 288, 448, 576

# --- Modeline ---
Modeline "768x576i" 15.578125 768 799 872 997 576 578 603 625 interlace -hsync -vsync

# --- xrandr commands ---
xrandr --newmode "768x576i" 15.578125 768 799 872 997 576 578 603 625 interlace -hsync -vsync
xrandr --addmode DP-1 "768x576i"
xrandr --output DP-1 --mode "768x576i"
```

The **📂 Load CRT Range** button opens a previously saved file, automatically finds the **calculated** `crt_range0` line (not the Calamity reference), and applies it to all sliders — exactly as if you had pasted it manually.

On GNOME/Ubuntu, the file dialogs use the native GTK dialog (via `zenity`) which supports folder creation. On other systems it falls back to Tkinter's built-in dialog.

---

## Installation

### Requirements

- Python 3.8 or later
- Tkinter (included in the Python standard library)
- `zenity` (optional — for native GTK file dialogs with folder creation on GNOME/Ubuntu)

```bash
# Ubuntu / Debian
sudo apt install python3-tk zenity

# Clone and run
git clone https://github.com/ZFEbHVUE/CRT-MODELINE-TOOLBOX
cd CRT-MODELINE-TOOLBOX
python3 crt_modeline_toolbox_en.py
```

No pip dependencies — the toolbox uses only Python standard library modules (`tkinter`, `subprocess`, `math`).

---

## Usage guide

### Generating a modeline

1. Select your **Monitor** from the dropdown
2. For multi-range monitors, select the active frequency band from **Range**
3. Set **H Width**, **V Height**, **Hfreq**, **Vfreq** using sliders or keyboard
4. Tick **Interlaced** for 576i / 480i modes
5. Adjust **CRT Range µs/ms** sliders if needed, or use **Direct Porch Adjustment px/lines** for integer control
6. Click **⚡ Optimise (LS)** to find the best integer distribution for exact Hfreq/Vfreq targets
7. Read the **Modeline** and **xrandr command** in the results panel
8. Use **Copy xrandr** or **Apply xrandr** to use the modeline
9. Optionally **💾 Save CRT Range** to keep the result for later

### Using a custom CRT Range

Paste a `crt_range0` line (from `switchres.ini`, a saved file, or Calamity's documentation) into the **Paste CRT Range** field and press Enter or the Parse button. All sliders will update immediately.

### Verifying an existing modeline

1. Switch to the **Verify** tab
2. Paste your modeline — e.g. the output of `switchres 768 576 50 -m arcade_15 -c`
3. Select the target monitor preset
4. All timings, frequencies and limit checks are displayed instantly
5. The calculated CRT Range can be used in a custom `crt_range` line for `switchres.ini`

### Comparing SwitchRes output with the toolbox

```bash
# Get SwitchRes modeline
switchres 768 576 50 -m arcade_15 -c
# → Modeline "768x576_50i 15.675000KHz 50.000000Hz" 15.627975 768 799 872 997 576 583 589 627 interlace -hsync -vsync
```

Paste this into the Verify tab with the Arcade 15 kHz preset — the toolbox will show the full timing decomposition and confirm that V Sync = 6 lines (0.192 ms) at 15.675 kHz, which may be too short for some DP2VGA adapters.

---

## Related projects

| Project | Description |
|---|---|
| [Batocera-CRT-Script](https://github.com/ZFEbHVUE/Batocera-CRT-Script) | CRT support scripts for Batocera Linux — primary project |
| [SwitchRes](https://github.com/antonioginer/switchres) | Reference modeline calculator by Calamity |
| [GroovyMAME](https://github.com/antonioginer/GroovyMAME) | MAME fork with native SwitchRes integration |
| [GroovyArcade](https://github.com/substring/GroovyArcade) | Arch Linux distro for CRT arcade cabinets |

---

## Acknowledgements

- **Calamity (Antonio Giner)** — for SwitchRes and the complete monitor preset database
- **Epsylon** (neo-arcadia.com) — for the foundational technical documentation on Master Clocks, pixel clocks and 240p modelines, system by system
- **Substring (Gil)** — for GroovyArcade, the patched Linux kernel enabling KMS mode switching, and many technical discussions on the CRT scene
- **Rion (Daniel Rion)** — for the CRT expertise and contributions to Batocera-CRT-Script

---

## License

MIT
