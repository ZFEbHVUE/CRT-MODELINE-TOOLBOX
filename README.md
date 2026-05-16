# CRT Modeline Toolbox v2.0
**by Stéphane "ZFEbHVUE"**

A Python toolkit for calculating, verifying, importing and saving CRT modelines — with deep integration for Batocera Linux and SwitchRes.

![CRT Modeline Toolbox GUI](docs/gui_main.png)

---

## Overview

CRT Modeline Toolbox v2.0 generates and verifies XFree86-format modelines for CRT monitors driven at 15 kHz (arcade/NTSC/PAL) in a Batocera/MAME retro-gaming context. It replicates and extends the Calamity monitor preset system used by SwitchRes, while exposing every intermediate value for analysis and debugging.

The toolbox was developed and validated on **Batocera Linux** with an **AMD Radeon R7 380X** (GCN 3rd gen), outputting via DisplayPort to DP→VGA adapters (ANX9832 and RTD2166 chipsets) connected to a 15 kHz CRT.

---

## Files

| File | Description |
|---|---|
| `crt_modeline_toolbox_v2.0.py` | Full desktop Tkinter GUI — for use on a normal PC screen |
| `crt_modeline_toolbox_640x480_v2.0.py` | Compact Tkinter GUI — for use on a 640×480 CRT screen |
| `crt_modeline_batocera.py` | Pure pygame version — for use inside Batocera Linux |

---

## Features

### Modeline Generation
- 10 Calamity monitor presets (NTSC, PAL, Arcade 15 kHz, Arcade 15ex, Arcade 25 kHz, Arcade 31 kHz, etc.)
- Automatic calculation of H_total and V_total from timing values (µs/ms)
- **Direct Porch Adjustment** — fine-tune HFP, HSYNC, HBP, VFP, VSYNC, VBP in pixels/lines
- Full output: Modeline string + xrandr command (`--display :0.0`)

### Optimiser (Largest-Remainder)
- Finds the optimal V_total for a target Vfreq
- Distributes blanking pixels using the largest-remainder method
- **Lock VFP** checkbox — forces a specific VFP line count and redistributes the excess to VBP (essential for hardware with VFP constraints, see below)
- SwitchRes threshold indicator: shows `SR V-blank: X.XXX/X.XXX ms ✓/✗` in real time
- Automatic VBP reduction if the V blanking total exceeds the SwitchRes threshold

### Import / Export
- **Paste CRT Range** — paste a `crt_range0` line from switchres.ini, fills all sliders
- **Import Modeline** — paste a raw XFree86 modeline, fills all sliders (H in px, V in px, H timings in µs, V timings in ms)
- **Save CRT Range** — saves the full configuration to a `.crt` file
- **Load CRT Range** — restores a saved configuration
- **Save Modeline** — saves the modeline + xrandr commands to a `.modeline` file
- **Load Modeline** — loads a `.modeline` file and fills all sliders

### Verification
- Checks Hfreq ∈ [hmin, hmax] and Vfreq ∈ [vfmin, vfmax]
- Checks active lines ∈ [pLmin, pLmax] (progressive) or [iLmin, iLmax] (interlaced)
- Displays the **CRT Range back-calculated from the generated modeline** (ready for switchres.ini)
- Displays the **Calamity fixed preset values** for comparison

### Signal Diagram
- Visual representation of H and V blanking zones, color-coded with legend

---

## Technical Details

### Modeline Format

```
Modeline "name" pclk  Hact Hbeg Hend Htot  Vact Vbeg Vend Vtot  [interlace] [±hsync] [±vsync]

pclk (MHz)  = Hfreq × H_total / 1,000,000
Hfreq (Hz)  = pclk × 1,000,000 / H_total
Vfreq (Hz)  = Hfreq × Div / V_total       (Div=2 interlaced, Div=1 progressive)
```

### _safe_round — H_total Rounding Fix

Python 3 uses banker's rounding: `round(772.5) = 772` (rounds to even). For some NTSC presets this causes H_total=772 instead of the correct 773, producing a wrong pixel clock.

The toolbox uses `_safe_round()` which applies `math.ceil()` when the fractional part falls in [0.4, 0.6]:

```python
def _safe_round(f):
    frac = f % 1
    return math.ceil(f) if 0.4 <= frac <= 0.6 else round(f)
```

Applied in both `calculate_from_range()` and `optimize_modeline()`.

### HBP / VBP as Exact Remainder

Individual rounding of HFP, HSYNC, HBP can cause their sum to differ from H_total by ±1 pixel. The toolbox always computes HBP (and VBP) as the exact remainder, eliminating accumulated rounding error:

```python
H_total = _safe_round(H / denom_H)
HFP     = round(hfp_t * TH)
HSYNC   = round(hs_t  * TH)
HBP     = H_total - H - HFP - HSYNC
```

### vbp Floor in fmt_crt_range

When back-calculating a crt_range from a modeline, vbp is floored (not rounded) to avoid crossing the SwitchRes threshold (see below):

```python
vbp_floor = math.floor(vbp * 1000) / 1000
```

---

## NTSC 480i — Root Cause Analysis

### Context

The goal is to get SwitchRes to generate a stable 640×480i NTSC modeline on Batocera with an AMD R7 380X + DP→VGA adapter. The working empirical modeline found by trial and error is:

```
12.162382 640 658 716 773 480 488 493 525 interlace -hsync -vsync
  HFP=18  HSYNC=58  HBP=57   H_total=773   Hfreq=15,734 Hz
  VFP=8   VSYNC=5   VBP=32   V_total=525   Vfreq=59.940 Hz
```

### Problem 1 — H_total=772 vs 773

The Calamity NTSC preset gives `H_total_float = 772.499` — exactly on the 772/773 boundary. Both Python and SwitchRes (C++) round this to 772. With H_total=772, pclk=12.147 MHz → CRT/adapter cannot sync.

**Fix:** `_safe_round()` uses `math.ceil()` for ambiguous cases, giving H_total=773 → pclk=12.162 MHz ✓

### Problem 2 — SwitchRes Generates Hfreq=15705 Hz

Even with a correct crt_range, SwitchRes generates Hfreq=15705 Hz (outside [15734–15735]) instead of 15734 Hz. Reading the SwitchRes source (`modeline.cpp`) revealed the full cascade.

#### interlace_incr = 0.5

For interlaced modes with `interlace_force_even=0` (default), SwitchRes adds 0.5 to the field line count:

```cpp
double interlace_incr = !cs->interlace_force_even && interlace == 2 ? 0.5 : 0;
vvt_ini = total_lines_for_yres(...) + interlace_incr;  // 262 + 0.5 = 262.5
t_mode->hfreq = t_mode->vfreq * vvt_ini;               // 59.829 × 262.5 = 15705 Hz !
```

#### max_vfreq_for_yres — The Critical Threshold

```cpp
return range->hfreq_max / (yres / interlace + round_near(range->hfreq_max * vertical_blank));
```

With `hfreq_max=15735` and `vertical_blank = vfp+vs+vbp` (in seconds):

```
15735 × 0.001430 = 22.501 → round_near = 23 → max_vfreq = 15735/263 = 59.829 Hz  ✗
15735 × 0.001429 = 22.484 → round_near = 22 → max_vfreq = 15735/262 = 60.057 Hz  ✓
```

**Critical threshold: `vfp+vs+vbp < 22.5 / hfreq_max × 1000 ms`**

For NTSC: `< 22.5/15735 × 1000 = 1.4298 ms`

#### The Full Cascade

```
vfp+vs+vbp = 0.254+0.159+1.017 = 1.430 ms  →  round_near(22.501) = 23
→ max_vfreq = 15735/263 = 59.829 Hz
→ vfreq_real = min(59.94, 59.829) = 59.829 Hz
→ vvt_ini = 262 + 0.5 = 262.5
→ hfreq = 59.829 × 262.5 = 15705 Hz   ← outside [15734–15735] !
→ pclk = 773 × 15705 / 1,000,000 = 12.140 MHz   ← unstable
```

#### Why vbp rounds to 1.017 instead of 1.016

The exact V blanking for 45 lines at 15734 Hz is:

```
exact = 45 / (15734 × 2) = 1.429296 ms
```

But rounding each timing independently to 3 decimal places:

```
vfp = 8/31468 × 1000 = 0.254  (rounds up)
vs  = 5/31468 × 1000 = 0.159  (rounds up)
vbp = 32/31468 × 1000 = 1.01684 → 1.017  ← rounds up, crosses threshold!
sum = 1.430 ms  >  1.4298 ms  ✗
```

**Fix:** use `floor` for vbp: `1.016 ms`. Sum = 1.429 ms < threshold ✓

### Problem 3 — VFP Distribution and GPU Constraints (AMD R7 380X)

Even with the correct H_total=773, V_total=525, and threshold satisfied, the VFP (V Front Porch) line count matters critically. Tests on a **AMD R7 380X** under Batocera with ANX9832 and RTD2166 DP→VGA adapters showed:

- VFP = 7 lines (0.222 ms) → image unstable on both adapters
- VFP = 3 lines (0.095 ms) → **stable image on both adapters** ✓

This behaviour is consistent across both adapters, pointing to a **GPU-level constraint** rather than an adapter issue. AMD GCN display engines have known timing constraints for low-resolution interlaced output on standard (non-CRT-Emudriver) drivers. The `interlace_force_even` flag in SwitchRes exists specifically for AMD APU/GPU hardware on Linux.

The working crt_range found empirically:

```
crt_range0  15734-15735, 59.94-59.94, 1.480, 4.768, 4.686, 0.095, 0.222, 1.112, 0, 0, 192, 240, 448, 480
```

Verification:
```
vfp+vs+vbp = 0.095+0.222+1.112 = 1.429 ms < 1.4298 ms ✓
VFP  = round(0.095 × 31468/1000) =  3 lines
VSync= round(0.222 × 31468/1000) =  7 lines
VBP  = round(1.112 × 31468/1000) = 35 lines
Total = 45 lines → V_total = 525 ✓
```

The VFP boundary values for reference (at Hfreq≈15734 Hz interlaced):

| VFP lines | vfp max (ms) |
|---|---|
| 1 | 0.032 |
| 2 | 0.064 |
| **3 (works)** | **0.111** |
| 4 | 0.143 |
| 5 | 0.175 |
| 6 | 0.207 |
| 7 (fails) | 0.238 |

To find the correct VFP for your hardware, use the **Lock VFP** feature in the optimizer and test values starting from 1 upward until the image is stable.

---

## Batocera Integration

### Call Chain

```
emulationstation-standalone
  └─ batocera-resolution defineMode <res>
  │     └─ switchres → computes modeline → xrandr --newmode / --addmode
  └─ batocera-resolution setMode_CVT <res>
        └─ if <res> in videomodes.conf → xrandr --mode  (bypass SwitchRes)
           else → apply modeline from defineMode
```

### Bypass SwitchRes for NTSC 480i

For critical modes where SwitchRes cannot reliably reproduce the exact modeline, pre-load the known-good modeline at startup. When `defineMode` tries `xrandr --newmode "640x480" [switchres_modeline]`, it fails silently because the name already exists, and the correct modeline stays in place.

**`/userdata/system/custom.sh`**
```bash
xrandr --display :0.0 --newmode "640x480" 12.162382 640 658 716 773 480 488 493 525 interlace -hsync -vsync
xrandr --display :0.0 --addmode DP-1 "640x480"
```

**`/userdata/system/videomodes.conf`**
```
640x480.59.94
```

`setMode_CVT` finds `640x480.59.94` in videomodes.conf and applies the pre-loaded modeline directly via `xrandr --output DP-1 --mode "640x480" --rate "59.94"`. SwitchRes is bypassed entirely for this mode.

### switchres.ini — Common Pitfalls

**Duplicate crt_range0** — the second entry silently overwrites the first:
```ini
crt_range0  15734-15735, ...   ← your custom range
crt_range0  auto               ← silently overwrites the above!
```

Remove all duplicate `crt_rangeN` entries. Verify with:
```bash
grep "crt_range0" /etc/switchres.ini
```

---

## SwitchRes Source Fix (PR candidate)

In `modeline.cpp`, `total_lines_for_yres()` — the `<` strict comparison prevents the while loop from executing when `vfreq × (vvt+1)` equals `hfreq_max` exactly (floating-point boundary condition):

```cpp
// Before
while ((vfreq * vvt < range->hfreq_min) && (vfreq * (vvt + 1) < range->hfreq_max)) vvt++;

// After
while ((vfreq * vvt < range->hfreq_min) && (vfreq * (vvt + 1) <= range->hfreq_max)) vvt++;
```

**Note:** this fix alone is not sufficient and can produce V_total=527 instead of 525 when combined with `interlace_incr=0.5`. The crt_range threshold fix (vbp floor) must be applied first. The complete fix for the NTSC preset would also require adjusting H_total rounding in `get_line_params`.

---

## Hardware Tested

| Configuration | 240p 15 kHz progressive | 480i 15 kHz interlaced |
|---|---|---|
| R7 380X + ANX9832 (DP→VGA) | ✓ stable | ✓ stable with VFP=3 lines |
| R7 380X + RTD2166 (DP→VGA) | ✓ stable | ✓ stable with VFP=3 lines |

**GPU:** AMD Radeon R7 380X (Dell T5500) — Batocera Linux, standard AMD driver (no CRT Emudriver)
**Output:** DP-1 for CRT, HDMI-1 for LCD marquee

> Note: CRT Emudriver would likely relax the VFP constraints observed on standard AMD drivers.

---

## Usage

### Desktop version
```bash
python3 crt_modeline_toolbox_v2.0.py
```

1. Select **Monitor** preset and **Range**
2. Set **H Width**, **V Height**, **Hfreq**, **Vfreq**, **Interlaced** toggle
3. Paste a `crt_range0` line or adjust sliders manually
4. Fine-tune porches in **Direct Porch Adjustment**
5. Click **⚡ Optimise (LS)** to find optimal V_total
6. For hardware with VFP constraints (AMD GCN): tick **Lock VFP** and set the target line count (start with 3), then optimise
7. Check the **SR V-blank** indicator — must show ✓ for SwitchRes compatibility
8. **Copy xrandr** or **Apply xrandr** to test the modeline
9. **🎬 Save Modeline** to save for later reuse

### Finding the right VFP for your hardware
1. Check **Lock VFP**, set value to **1**
2. Click **⚡ Optimise (LS)**
3. Apply xrandr → if image is stable, done; if not, increment VFP by 1 and repeat
4. Once the stable value is found, **Save CRT Range** for SwitchRes

### Import an existing modeline
Paste a raw modeline in the **Modeline:** field and click **Import →**. All sliders are filled automatically using `calc_timings()` which correctly divides timing values by H_total/V_total — avoiding the inflated µs values caused by a missing division.

---

## Repository

https://github.com/ZFEbHVUE/CRT-MODELINE-TOOLBOX

---

## License

GPL-2.0+
