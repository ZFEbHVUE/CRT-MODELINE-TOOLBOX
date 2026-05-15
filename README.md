# CRT Modeline Toolbox v2.0
**by Stéphane "ZFEbHVUE"**

A Python toolkit for calculating, verifying, importing and saving CRT modelines — with deep integration for Batocera Linux and SwitchRes.

---

## Overview

CRT Modeline Toolbox v2.0 generates and verifies XFree86-format modelines for CRT monitors driven at 15 kHz (arcade/NTSC/PAL) in a Batocera/MAME retro-gaming context. It replicates and extends the Calamity monitor preset system used by SwitchRes, while exposing every intermediate value for analysis and debugging.

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
- Distributes blanking pixels using the largest-remainder method to avoid rounding drift
- Reports `Vfreq error` in real time

### Import / Export
- **Paste CRT Range** — paste a `crt_range0` line from switchres.ini, fills all sliders
- **Import Modeline** — paste a raw XFree86 modeline, fills all sliders (H in px, V in px, H timings in µs, V timings in ms)
- **Save CRT Range** — saves the full configuration (range + modeline + xrandr) to a `.crt` file
- **Load CRT Range** — restores a saved configuration
- **Save Modeline** — saves the modeline + xrandr commands to a `.modeline` file
- **Load Modeline** — loads a `.modeline` file and fills all sliders

### Verification
- Checks Hfreq ∈ [hmin, hmax] and Vfreq ∈ [vfmin, vfmax]
- Checks active lines ∈ [pLmin, pLmax] (progressive) or [iLmin, iLmax] (interlaced)
- Displays the **CRT Range back-calculated from the generated modeline** (ready for switchres.ini)
- Displays the **Calamity fixed preset values** for comparison

### Signal Diagram
- Visual representation of H blanking zones (HFP, HSYNC, HBP) and V blanking zones (VFP, VSYNC, VBP)
- Color-coded, with legend aligned inside the active area

---

## Technical Details

### Modeline Format

```
Modeline "name" pclk  Hact Hbeg Hend Htot  Vact Vbeg Vend Vtot  [interlace] [±hsync] [±vsync]

pclk (MHz)  = Hfreq × H_total / 1,000,000
Hfreq (Hz)  = pclk × 1,000,000 / H_total
Vfreq (Hz)  = Hfreq × Div / V_total       (Div=2 interlaced, Div=1 progressive)
```

### _safe_round — Rounding Fix

Python 3 uses banker's rounding: `round(772.5) = 772` (rounds to even). This causes H_total to be computed as 772 instead of 773 for some NTSC presets.

The toolbox uses `_safe_round()` which applies `math.ceil()` when the fractional part falls in [0.4, 0.6]:

```python
def _safe_round(f):
    frac = f % 1
    return math.ceil(f) if 0.4 <= frac <= 0.6 else round(f)
```

Applied in both `calculate_from_range()` and `optimize_modeline()`.

### HBP / VBP as Exact Remainder

Individual rounding of HFP, HSYNC, HBP can cause their sum to differ from the intended H_total by ±1 pixel. The toolbox computes HBP (and VBP) as the exact remainder:

```python
H_total = _safe_round(H / denom_H)
HFP     = round(hfp_t * TH)
HSYNC   = round(hs_t  * TH)
HBP     = H_total - H - HFP - HSYNC   # exact, no accumulated rounding error
```

---

## NTSC 480i — Root Cause Analysis

### The Problem

The Calamity NTSC preset:
```
crt_range0  15734-15735, 59.94-59.94, 1.500, 4.700, 4.700, 0.191, 0.191, 0.953,
            0, 0, 192, 240, 448, 480
```

gives `H_total_float = 772.499...` — exactly on the 772/773 boundary. Both Python and SwitchRes (C++) round this to 772. The working pixel clock requires H_total = **773** → pclk = 12.162382 MHz. With H_total = 772 → pclk = 12.147 MHz → CRT/adapter cannot sync.

### The Working Modeline

Found empirically for ANX9832/RTD2166 adapters on a 15 kHz CRT:
```
12.162382 640 658 716 773 480 488 493 525 interlace -hsync -vsync
```

```
HFP=18  HSYNC=58  HBP=57   H_total=773   Hfreq=15,734 Hz
VFP=8   VSYNC=5   VBP=32   V_total=525   Vfreq=59.940 Hz
pclk = 15734 × 773 / 1,000,000 = 12.162382 MHz
```

### SwitchRes Source Analysis (modeline.cpp)

Even with a correctly crafted crt_range, SwitchRes generates a different (unstable) modeline at 15705 Hz instead of 15734 Hz. Reading the SwitchRes source revealed the full cascade.

#### Step 1 — interlace_incr = 0.5

```cpp
double interlace_incr = !cs->interlace_force_even && interlace == 2 ? 0.5 : 0;
vvt_ini = total_lines_for_yres(...) + interlace_incr;  // 262 + 0.5 = 262.5
t_mode->hfreq = t_mode->vfreq * vvt_ini;               // 59.829 × 262.5 = 15705 Hz
```

For interlaced modes with `interlace_force_even=0` (default), SwitchRes adds 0.5 to the field line count before computing Hfreq. This shifts Hfreq by ~30 Hz, explaining the 15705 Hz result.

#### Step 2 — max_vfreq_for_yres — The Critical Threshold

```cpp
return range->hfreq_max / (yres / interlace + round_near(range->hfreq_max * vertical_blank));
```

With `hfreq_max=15735` and `vertical_blank = vfp+vs+vbp` (in seconds):

```
15735 × 0.001430 = 22.501 → round_near = 23 → max_vfreq = 15735/263 = 59.829 Hz ✗
15735 × 0.001429 = 22.484 → round_near = 22 → max_vfreq = 15735/262 = 60.057 Hz ✓
```

Critical threshold: `vertical_blank < 22.5 / 15735 = 1.4298 ms`

#### Step 3 — The Full Cascade

```
vfp+vs+vbp = 0.254+0.159+1.017 = 1.430 ms  →  round_near(22.501) = 23
→ max_vfreq = 15735/263 = 59.829 Hz
→ vfreq_real = min(59.94, 59.829) = 59.829 Hz
→ vvt (field lines, integer) = 262
→ vvt_ini = 262 + 0.5 = 262.5    (interlace_incr)
→ hfreq = 59.829 × 262.5 = 15705 Hz   ← outside [15734–15735] !
→ pclk = 773 × 15705 / 1,000,000 = 12.140 MHz   ← unstable
```

#### Step 4 — Why vbp rounds to 1.017 instead of 1.016

The V timings are derived from integer line counts. The exact total is:

```
VFP=8, VSync=5, VBP=32 → 45 lines
exact_total = 45 / (15734 × 2) = 1.429296 ms
```

But rounding each value independently to 3 decimal places:

```
vfp = 8/31468 × 1000 = 0.25421 → 0.254  (rounds up)
vs  = 5/31468 × 1000 = 0.15888 → 0.159  (rounds up)
vbp = 32/31468 × 1000 = 1.01684 → 1.017  (rounds up ← crosses threshold!)
sum = 1.430 ms  >  threshold 1.4298 ms  ✗
```

The individual rounding errors accumulate and push the sum over the threshold.

### The Fix

Use `floor` for vbp to stay below the threshold:

```
vbp = 1.016 ms   (floor of 1.01684)
sum = 0.254 + 0.159 + 1.016 = 1.429 ms  <  1.4298 ms  ✓
```

**Correct crt_range for NTSC 480i:**
```
crt_range0  15734-15735, 59.94-59.94, 1.480, 4.769, 4.688, 0.254, 0.159, 1.016,
            0, 0, 192, 240, 448, 480
```

Result in SwitchRes:
```
max_vfreq = 15735/262 = 60.057 Hz
vfreq_real = min(59.94, 60.057) = 59.94 Hz
vvt_ini = 262 + 0.5 = 262.5
hfreq = 59.94 × 262.5 = 15734.25 Hz  ✓  (inside [15734–15735])
vtotal = 262.5 × 2 = 525             ✓
pclk ≈ 12.162 MHz                    ✓
```

### SwitchRes Source Fix (PR candidate)

In `modeline.cpp`, `total_lines_for_yres()`, line 430 — the `<` strict comparison prevents the while loop from executing when `vfreq × (vvt+1)` equals `hfreq_max` exactly (floating-point boundary):

```cpp
// Before (misses the boundary case)
while ((vfreq * vvt < range->hfreq_min) && (vfreq * (vvt + 1) < range->hfreq_max)) vvt++;

// After (inclusive upper bound)
while ((vfreq * vvt < range->hfreq_min) && (vfreq * (vvt + 1) <= range->hfreq_max)) vvt++;
```

---

## Batocera Integration

### Call Chain

```
emulationstation-standalone
  └─ batocera-resolution defineMode <res>
  │     └─ switchres → computes modeline → xrandr --newmode / --addmode
  └─ batocera-resolution setMode_CVT <res>
        └─ if <res> in videomodes.conf → xrandr --mode  (bypass SwitchRes)
           else → xrandr --mode from defineMode result
```

### Bypass SwitchRes for NTSC 480i

SwitchRes cannot reliably reproduce the exact working modeline due to the issues described above. The solution is to pre-load the known-good modeline at startup. When `defineMode` subsequently tries `xrandr --newmode "640x480" [switchres_modeline]`, it fails silently because the name already exists, and the correct modeline stays in place.

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

### switchres.ini — Duplicate crt_range0 Pitfall

If switchres.ini contains two `crt_range0` lines:
```ini
crt_range0  15734-15735, ...   ← your custom range
crt_range0  auto               ← overwrites the previous!
```

The second entry silently overwrites the first. SwitchRes only sees `auto` and ignores the custom range. Remove all duplicate `crt_rangeN` entries.

---

## Hardware Tested

| Adapter | 240p 15 kHz progressive | 480i 15 kHz interlaced |
|---|---|---|
| ANX9832 (DP→VGA) | ✓ stable | ✓ stable (exact modeline required) |
| RTD2166 (DP→VGA) | ✓ stable | ✓ stable (exact modeline required) |

GPU: AMD Radeon R9 380 (Dell T5500) — DP-1 for CRT, HDMI-1 for LCD marquee.

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
6. **Copy xrandr** or **Apply xrandr** to use the modeline
7. **🎬 Save Modeline** to save for later reuse

### Import an existing modeline
Paste a raw modeline in the **Modeline:** field and click **Import →**. All sliders are filled automatically. The conversion uses `calc_timings()` which correctly divides by H_total and V_total — avoiding the wrong conversion that previously inflated µs values by a factor of ~773.

### Derive crt_range from a working modeline
After importing, the **CRT Range — calculated from generated modeline** box shows the back-calculated `crt_range0` ready for switchres.ini. Apply the **vbp floor rule**: use `math.floor(vbp_exact × 1000) / 1000` to ensure the total V blanking stays below the 1.4298 ms threshold.

---

## Repository

https://github.com/ZFEbHVUE/CRT-MODELINE-TOOLBOX

---

## License

GPL-2.0+
