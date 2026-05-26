# CRT Modeline Toolbox v2.5
**by Stéphane "ZFEbHVUE"**

A Python toolkit for calculating, verifying, importing and saving CRT modelines — with deep integration for Batocera Linux and SwitchRes.

![CRT Modeline Toolbox GUI](docs/gui_main.png)

---

## Overview

CRT Modeline Toolbox v2.5 generates and verifies XFree86-format modelines for CRT monitors driven at 15 kHz (arcade/NTSC/PAL) in a Batocera/MAME retro-gaming context. It replicates and extends the Calamity monitor preset system used by SwitchRes, while exposing every intermediate value for analysis and debugging.

The toolbox was developed and validated on **Batocera Linux** with:
- **AMD Radeon R7 380X** (GCN 3rd gen) — Dell T5500
- **AMD Radeon RX 6400 XT** (RDNA 2)

Output via DisplayPort → DP→VGA adapters (ANX9832 and RTD2166 chipsets) connected to 15 kHz CRT monitors.

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

### Optimiser (Largest-Remainder)
- Finds the optimal V_total for a target Vfreq
- Distributes blanking pixels using the largest-remainder method
- **Δ VFP** control — adjust the V Front Porch relative to the optimised value:
  - Positive value → absolute target (e.g. `8` sets VFP=8 lines exactly)
  - Negative value → relative offset (e.g. `-5` reduces VFP by 5 lines)
  - Essential for hardware with VFP constraints (see GPU section below)
- **SwitchRes threshold indicator** — shows `SR V-blank: X.XXX/X.XXX ms ✓/✗` in real time
- Automatic VBP reduction if the V blanking total exceeds the SwitchRes threshold

### Geometry (SwitchRes `-g h_size:h_shift:v_shift`)
- **H move (px) = H_shift** — shift image horizontally (modifies X2/X3, H_total unchanged)
- **V move (lines) = V_shift** — shift image vertically (modifies Y2/Y3, V_total unchanged)
  - Auto re-optimisation if VFP or VBP would go below 1 line
- **H_size** — horizontal zoom: scales H blanking → changes H_total and pclk
- **V_size ⚗** — vertical zoom (experimental): scales total V blanking proportionally
- All geometry applied from the base modeline in real time — no accumulation
- SwitchRes `-g` command generated automatically in the xrandr block

### Import / Export
- **Paste CRT Range** — paste a `crt_range0` line, fills all sliders
- **Import Modeline** — paste a raw XFree86 modeline, fills all sliders
- **Save / Load CRT Range** — `.crt` file (full configuration)
- **Save / Load Modeline** — `.modeline` file (modeline + xrandr commands)

### Verification
- Checks Hfreq ∈ [hmin, hmax] and Vfreq ∈ [vfmin, vfmax]
- Checks active lines ∈ [pLmin, pLmax] or [iLmin, iLmax]
- Displays **CRT Range back-calculated from generated modeline** (ready for switchres.ini)
- Displays **Calamity fixed preset values** for comparison

### Signal Diagram
- Visual representation of H and V blanking zones, color-coded

---

## Technical Details

### Modeline Format

```
Modeline "name" pclk  Hact Hbeg Hend Htot  Vact Vbeg Vend Vtot  [interlace] [±hsync] [±vsync]

pclk (MHz)  = Hfreq × H_total / 1,000,000
Hfreq (Hz)  = pclk × 1,000,000 / H_total
Vfreq (Hz)  = Hfreq × Div / V_total       (Div=2 interlaced, Div=1 progressive)
```

### V timing — relationship with Hfreq

Each V line = 1 complete H period. For interlaced (Div=2):

```
VFP_ms = VFP_lines / (Hfreq × 2) × 1000

NTSC 480i at 15734 Hz:  1 line = 1/(15734×2) × 1000 = 0.0318 ms
PAL  576i at 15625 Hz:  1 line = 1/(15625×2) × 1000 = 0.0320 ms
```

### _safe_round — H_total rounding fix

Python 3 banker's rounding: `round(772.5) = 772`. For some NTSC presets this causes H_total=772 instead of 773.

```python
def _safe_round(f):
    frac = f % 1
    return math.ceil(f) if 0.4 <= frac <= 0.6 else round(f)
```

### HBP / VBP as exact remainder

```python
H_total = _safe_round(H / denom_H)
HFP     = round(hfp_t * TH)
HSYNC   = round(hs_t  * TH)
HBP     = H_total - H - HFP - HSYNC   # exact, no accumulated rounding error
```

---

## SwitchRes Threshold — Critical Analysis

### The threshold

SwitchRes (`modeline.cpp`, `max_vfreq_for_yres`):

```cpp
return hfreq_max / (yres / interlace + round_near(hfreq_max * vertical_blank));
```

When `round_near(hfreq_max × vertical_blank) ≥ X.5`, SwitchRes rounds up, reducing `max_vfreq` below the target and generating Hfreq ~30 Hz outside the specified range.

```
hfreq_max × (vfp+vs+vbp) < 22.5   →  correct Hfreq  ✓
hfreq_max × (vfp+vs+vbp) ≥ 22.5   →  Hfreq drops ~30 Hz  ✗
```

**Critical threshold: `vfp+vs+vbp < 22.5 / hfreq_max` seconds**

For NTSC at hmax=15735: `< 1.4298 ms`  
For PAL at hmax=15750: `< 1.4286 ms`

In lines (interlaced): `total V blanking < 22.5 × 2 = 45 lines` (NTSC)

### The SwitchRes 15705 Hz bug

With NTSC Calamity preset (1.500+4.700+4.700 = 10.900 µs H blank):
```
H_total_float = 640 / (1 - 10.900/63.549) = 772.499...
```

Python `round(772.499) = 772` (banker's rounding to even). `_safe_round` gives 773 ✓.

SwitchRes generates Hfreq=**15705 Hz** (outside [15734–15735]) due to `interlace_incr=0.5`:
```cpp
vvt_ini = total_lines_for_yres(...) + 0.5;  // 262 + 0.5 = 262.5
hfreq   = vfreq_real × vvt_ini;             // 59.829 × 262.5 = 15705 Hz
```

The root cause: individual rounding of vfp/vs/vbp to 3 decimal places pushes the total over the 1.4298 ms threshold:
```
vbp_exact  = 32 / 31468 × 1000 = 1.01684 ms
round(...)                      = 1.017 ms  ← crosses threshold!
floor(... × 1000) / 1000        = 1.016 ms  ← stays below ✓
```

The toolbox applies `_safe_round` in both `calculate_from_range()` and `optimize_modeline()`.

---

## GPU Hardware Constraints

### VFP minimum per GPU

Testing on Batocera Linux with DP→VGA adapters on CRT:

| GPU | Min VFP (interlaced) | Notes |
|---|---|---|
| R7 380X (GCN 3) | **3 lines** | Works at 15 kHz with ANX9832/RTD2166 |
| RX 6400 XT (RDNA 2) | **8 lines** | Standard AMD driver, no CRT Emudriver |

This GPU-level constraint is consistent across both ANX9832 and RTD2166 adapters, confirming it is a GPU display engine limitation rather than an adapter issue.

The `interlace_force_even` parameter in SwitchRes exists specifically for AMD GPU compatibility on Linux.

### pclk minimum

The RX 6400 XT with standard drivers refuses dotclocks below ~16 MHz for 15 kHz interlaced modes. Always verify that the generated pclk is within an acceptable range:

```
R7 380X : accepts pclk ≈ 12 MHz (e.g. 640×480i NTSC)
RX 6400 XT : requires pclk ≥ ~16 MHz for stable output
```

### Using Δ VFP

To find the minimum working VFP for your hardware:
1. Tick **Δ VFP**, set value to `1`
2. Click **⚡ Optimise (LS)**
3. Apply xrandr → stable? → done. If not, increment by 1 and repeat.
4. Once found, **Save Modeline** or **Save CRT Range**

For R7 380X: start at `3`. For RX 6400 XT: start at `8`.

---

## Geometry — H_size / V_size / H_move / V_move

### H_move and V_move

Direct porch manipulation, keeps H_total and V_total unchanged:

```
H_move = +N  →  X2-=N, X3-=N  (image shifts right)
H_move = -N  →  X2+=N, X3+=N  (image shifts left)
V_move = +N  →  Y2-=N, Y3-=N  (image shifts down)
V_move = -N  →  Y2+=N, Y3+=N  (image shifts up)
```

These values are identical to SwitchRes `h_shift` and `v_shift` in the `-g` parameter.

**V_move limit**: VFP is typically small (3–8 lines). Moving down more than VFP−1 lines is impossible without re-optimisation. The toolbox automatically re-optimises with increased VFP target when the requested move exceeds available VFP.

**Important**: for CRT TV overscan compensation, prefer adjusting `--screenoffset` in ES (`es.arg.override`) rather than V_move, to avoid mode-dependent position loss on game exit.

### H_size

Scales H blanking proportionally, keeping H_active and Hfreq fixed:

```
h_size=1.05  →  H_blank / 1.05  →  H_total decreases  →  pclk decreases
             →  image appears 5% wider (beam traces same pixels in less time)
```

### V_size (experimental ⚗)

Scales total V blanking proportionally, keeps V_active and VSync fixed:

```
v_size=1.1  →  V_blank / 1.1  →  V_total decreases  →  Vfreq increases slightly
            →  image appears 10% taller
```

Note: for NTSC 480i with 45 total blanking lines and tight Vfreq range [59.94–59.94], the margin for V_size is very limited.

---

## NTSC 480i — Working Configuration

### Working modeline (R7 380X, ANX9832/RTD2166)

```
12.162382 640 658 716 773 480 488 493 525 interlace -hsync -vsync
  HFP=18  HSYNC=58  HBP=57   H_total=773   Hfreq=15,734 Hz
  VFP=8   VSYNC=5   VBP=32   V_total=525   Vfreq=59.940 Hz
```

### Working crt_range for SwitchRes (custom monitor)

```
crt_range0  15734-15735, 59.94-59.94, 1.480, 4.769, 4.688, 0.095, 0.222, 1.112, 0, 0, 192, 240, 448, 480
```

Note: `vfp=0.095 ms` (3 lines) is much smaller than Calamity standard (0.191 ms). This was found empirically — the R7 380X requires a short VFP for stable interlaced sync on this hardware combination.

### Batocera bypass (pre-load modeline)

Since SwitchRes cannot reliably reproduce the exact working modeline, pre-load it at startup:

**`/userdata/system/custom.sh`**
```bash
xrandr --display :0.0 --newmode "640x480" 12.162382 640 658 716 773 480 488 493 525 interlace -hsync -vsync
xrandr --display :0.0 --addmode DP-1 "640x480"
```

**`/userdata/system/videomodes.conf`**
```
640x480.59.94
```

`setMode_CVT` finds `640x480.59.94` in videomodes.conf and applies the pre-loaded modeline directly, bypassing SwitchRes.

---

## switchres.ini Common Pitfalls

### Duplicate crt_range0

```ini
crt_range0  15734-15735, ...   ← custom range
crt_range0  auto               ← silently overwrites the above!
```

Remove all duplicate `crt_rangeN auto` entries. Check with:
```bash
grep "crt_range0" /etc/switchres.ini
```

### crt_range for games vs ES resolution

Never use a crt_range derived from a geometry-adjusted ES modeline for MAME/game resolutions. The large H blanking values produce excessive pclk for low resolutions:

```
Custom H_blank = 14 µs  →  H_total(320px) = 412  →  pclk = 6.5 MHz  ← black screen!
Standard H_blank = 8 µs →  H_total(320px) = 348  →  pclk = 5.5 MHz  ← ok
```

Use the **standard Arcade 15kHz Calamity range** for MAME and apply geometry only to the ES resolution via `custom.sh`.

---

## SwitchRes Source Fix (PR candidate)

In `modeline.cpp`, `total_lines_for_yres()`:

```cpp
// Before — misses boundary case (floating-point equality)
while ((vfreq * vvt < range->hfreq_min) && (vfreq * (vvt + 1) < range->hfreq_max)) vvt++;

// After
while ((vfreq * vvt < range->hfreq_min) && (vfreq * (vvt + 1) <= range->hfreq_max)) vvt++;
```

**Note:** this fix alone may cause V_total=527 instead of 525 for NTSC. The crt_range vbp floor fix (keeping total < 1.4298 ms) must be applied alongside.

---

## Hardware Tested

| Configuration | 240p 15 kHz | 480i NTSC | 576i PAL |
|---|---|---|---|
| R7 380X + ANX9832 | ✓ | ✓ VFP≥3 | ✓ |
| R7 380X + RTD2166 | ✓ | ✓ VFP≥3 | ✓ |
| RX 6400 XT + ANX9832 | ✓ | ✓ VFP≥8 | ✓ VFP≥8 |
| RX 6400 XT + RTD2166 | ✓ | ✓ VFP≥8 | ✓ VFP≥8 |

**Platform:** Batocera Linux, standard AMD driver (no CRT Emudriver)  
**Output:** DP-1 for CRT, HDMI-1 for LCD marquee  

> CRT Emudriver would likely relax the VFP and pclk constraints observed with standard AMD drivers.

---

## Usage

### Desktop version
```bash
python3 crt_modeline_toolbox_v2.0.py
```

1. Select **Monitor** preset and **Range**
2. Set resolution, Hfreq, Vfreq, Interlaced
3. Click **⚡ Optimise (LS)**
4. Set **Δ VFP** if needed for your GPU (R7 380X: 3, RX 6400 XT: 8)
5. Adjust **Geometry** (H_move/V_move) to center the image on screen
6. Check **SR V-blank ✓** indicator
7. **Copy xrandr** to test, **Save Modeline** to keep

### Finding the working VFP for your hardware

1. Tick **Δ VFP**, start at `1`
2. **⚡ Optimise** → **Apply xrandr** → stable? → done
3. If black screen: increment by 1, repeat
4. Note the minimum value for your GPU

### Centering image on TV (overscan compensation)

Use `es.arg.override` in Batocera for ES content positioning (survives game launches):

```
# /userdata/system/es.arg.override
screensizeoffset_x  -40
screensizeoffset_y  -40
screenoffset_x  20
screenoffset_y  25
```

For image position on the physical screen, adjust **V_move** in the modeline — this is a hardware-level fix that persists across all ES states.

---

## Repository

https://github.com/ZFEbHVUE/CRT-MODELINE-TOOLBOX

---

## License

GPL-2.0+
