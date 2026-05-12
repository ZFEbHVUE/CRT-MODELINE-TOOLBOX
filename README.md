# CRT Modeline Toolbox

**CRT modeline calculation and verification tool for arcade CRT monitors**

*Stéphane "ZFEbHVUE" — v2.0*

---

## Overview

CRT Modeline Toolbox is a Python/Tkinter GUI tool for generating and verifying modelines for CRT monitors running at 15kHz, 25kHz, and 31kHz — the frequencies used by arcade monitors, PAL/NTSC TV sets, and retro gaming setups.

It is designed to complement [SwitchRes](https://github.com/antonioginer/switchres) (by Calamity / Antonio Giner) and [Batocera-CRT-Script](https://github.com/ZFEbHVUE/Batocera-CRT-Script), providing a visual and interactive way to understand, calculate, and verify the timing parameters behind a modeline.

## GUI toolbox
![CRT-MODELINE-TOOLBOX GUI](docs/gui_main.png)

---

## Background

A CRT modeline is not a set of arbitrary numbers — it encodes the precise timing of the video signal sent to the monitor:

- **Pixel clock** (MHz) — how fast pixels are drawn
- **H/V active** — the visible resolution
- **H/V Front Porch, Sync, Back Porch** — the blanking intervals that allow the electron beam to fly back and the chassis circuits to synchronise

The key relationships are:

```
H_total  = H_active + H_FrontPorch + H_Sync + H_BackPorch
Hfreq    = pixel_clock / H_total
V_total  = V_active + V_FrontPorch + V_Sync + V_BackPorch
Vfreq    = Hfreq / V_total          (progressive)
Vfreq    = Hfreq × 2 / V_total      (interlaced)
```

For a 15kHz CRT, the PAL canonical values are:

```
Hfreq    = 15.625 kHz  →  H_total time = 64.000 µs
Vfreq    = 50.000 Hz   →  V_total time = 20.000 ms (per field)
```

The tool converts between the **time domain** (µs/ms porches as used in SwitchRes `crt_range`) and the **pixel domain** (integer counts as used in `xrandr --newmode`), and shows you exactly where rounding errors occur.

---

## Features

### Generate tab

- Select a monitor preset (20+ presets from Calamity/SwitchRes built-in)
- All parameters editable via **slider + direct keyboard entry** — both stay synchronised
- Multi-range monitors (e.g. Arcade 15/31kHz) — select the active range from a dropdown
- Hfreq slider auto-switches the range on multi-range presets
- Displays two CRT Range lines side by side:
  - **Calamity values (fixed)** — the original preset, unchanged
  - **Calculated from modeline** — recalculated from the integer pixel counts after rounding, showing the inevitable quantisation error
- Full timing table in both px/lines and µs/ms
- Verification against monitor limits (Hfreq range, Vfreq range, progressive/interlaced line count limits)
- Generates the `Modeline` string and the three `xrandr` commands ready to copy
- **Copy xrandr** — copies to clipboard
- **Apply xrandr** — executes directly on the running system

### Verify tab

- Paste any modeline (SwitchRes output or xrandr format)
- Instantly shows all timing parameters decomposed in µs/ms
- Verifies against the selected monitor preset
- Auto-selects the correct range for multi-range monitors
- Shows the CRT Range calculated from the modeline — useful to generate a custom `crt_range` for `switchres.ini`

---

## Monitor presets

All presets are sourced from Calamity's official SwitchRes monitor definitions.

| Preset | Ranges |
|---|---|
| PAL TV | 15kHz |
| NTSC TV | 15kHz |
| Generic 15kHz | 15kHz |
| Arcade 15kHz | 15kHz |
| Arcade 15kHz EX | 15kHz |
| Arcade 25kHz | 25kHz |
| Arcade 31kHz | 31kHz |
| Arcade 15/25kHz | 15kHz + 25kHz |
| Arcade 15/31kHz | 15kHz + 31kHz |
| Arcade 15/25/31kHz | 15kHz + 25kHz + 31kHz |
| Wells Gardner D9800/D9400 | 15 / 18 / 25 / 31 / 33 / 36kHz |
| Wells Gardner D9200 | 15 / 24 / 31 / 37kHz |
| Wells Gardner K7000 | 15kHz |
| Wells Gardner 25K7131 | 15kHz |
| Nanao MS-2930/2931 | 15 / 24 / 31kHz |
| Nanao MS9-29 | 15 / 24kHz |
| Hantarex MTC 9110 / Polo | 15kHz |
| Hantarex Polostar 25 | 15 / 16 / 25 / 31kHz |
| Makvision 2929D | 31kHz |
| Wei-Ya M3129 | 15 / 24 / 31kHz |
| Rodotron 666B-29 | 15 / 24 / 31kHz |
| PC CRT 31kHz/120Hz | 31kHz/60Hz + 31kHz/120Hz |
| PC CRT 70kHz/120Hz | 70kHz/60Hz + 70kHz/120Hz |
| **DP custom (ZFEbHVUE)** | 15kHz PAL — extended VSyncPulse for DP2VGA adapters |

### DP custom preset

The `DP custom (ZFEbHVUE)` preset uses a VSyncPulse of **0.480 ms** instead of Calamity's standard **0.192 ms**. This was found empirically to be necessary for certain DisplayPort-to-VGA adapters (specifically adapters based on the **Realtek RTD2166** chip with integrated oscillator) when used with AMD GPU DisplayPort outputs at 15kHz for 768x576i PAL content.

The standard 6-line VSync pulse is too short for these adapters to lock. The extended pulse gives the adapter sufficient time to detect and synchronise the vertical sync signal.

---

## Technical notes

### Why CRT Range values never round-trip exactly

The CRT Range stores porches as **continuous time values** (µs/ms). Converting to pixels requires multiplying by `TERM_H` or `TERM_V` and rounding to the nearest integer. This introduces a small but irreducible quantisation error:

```
HFrontPorch_input  = 2.000 µs   (from crt_range)
→ HFP pixels       = round(2.000 × TERM_H) = 26 px
→ HFrontPorch_calc = 26 / 997 / 15625 × 10⁶ = 1.990 µs  ≠ 2.000
```

The pixel is the atomic unit — you cannot have exactly 2.000 µs if it does not fall on an integer pixel boundary. This is why the two CRT Range displays in the tool will never show identical values, and why Calamity's `crt_range` values are tolerance windows rather than exact targets.

### Interlaced mode

In interlaced mode (576i, 480i), the frame is split into two fields. The `Div_Interlace = 2` factor is applied to the Vfreq calculation:

```
Vfreq = Hfreq × 2 / V_total   (interlaced)
```

For PAL 768x576i: `15625 × 2 / 625 = 50.000 Hz` exactly.

---

## Installation

Requires Python 3 and Tkinter (standard library, no pip dependencies).

```bash
# Ubuntu / Debian
sudo apt install python3-tk

# Clone and run
git clone https://github.com/ZFEbHVUE/CRT-MODELINE-TOOLBOX
cd CRT-MODELINE-TOOLBOX
python3 crt_modeline_toolbox_en.py
```

---

## Usage

### Generating a modeline

1. Select your monitor from the **Monitor** dropdown
2. For multi-range monitors, select the active frequency range from **Range**
3. Set **H Width**, **V Height**, **Hfreq**, **Vfreq** using sliders or keyboard
4. Check **Interlaced** if needed
5. Fine-tune the CRT Range porches if necessary
6. Read the **Modeline** and **xrandr command** output
7. Use **Copy xrandr** or **Apply xrandr**

### Verifying an existing modeline

1. Switch to the **Verify** tab
2. Paste your modeline — e.g. output from `switchres 768 576 50 -m arcade_15 -c`
3. Select the target monitor preset
4. All timings, frequencies, and limit checks are displayed instantly

---

## Related projects

- [Batocera-CRT-Script](https://github.com/ZFEbHVUE/Batocera-CRT-Script) — CRT support scripts for Batocera Linux (main project)
- [SwitchRes](https://github.com/antonioginer/switchres) — modeline calculator by Calamity (Antonio Giner)
- [GroovyMAME](https://github.com/antonioginer/GroovyMAME) — MAME fork with native SwitchRes integration

---

## Acknowledgements

- **Calamity (Antonio Giner)** — for SwitchRes and the monitor preset database
- **Epsylon** (neo-arcadia.com) — for the foundational technical documentation on 240p modelines and Master Clock derivation
- **Substring (Gil)** — for GroovyArcade, the patched kernel enabling KMS mode switching, and many technical discussions

---

## License

MIT
