#!/usr/bin/env python3
# ==============================================================================
# CRT MODELINE TOOLBOX — CRT VERSION
# Stéphane "ZFEbHVUE" — v2.0
# Compact GUI for 640×480 CRT displays
# python3 crt_modeline_crt.py
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import math
import re

# ==============================================================================
# MONITOR PRESETS (source: Calamity/SwitchRes)
# ==============================================================================
PRESETS = {
    "PAL TV": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 15625, "vfmin": 50.0, "vfmax": 50.0,
                    "hfp": 1.500, "hs": 4.700, "hbp": 5.800, "vfp": 0.064, "vs": 0.160, "vbp": 1.056,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.625, "dV": 50.0
    },
    "NTSC TV": {
        "ranges": [{"lb": "15KHz", "hmin": 15734, "hmax": 15735, "vfmin": 59.94, "vfmax": 59.94,
                    "hfp": 1.500, "hs": 4.700, "hbp": 4.700, "vfp": 0.191, "vs": 0.191, "vbp": 0.953,
                    "pLmin": 192, "pLmax": 240, "iLmin": 448, "iLmax": 480}],
        "dH": 15.734, "dV": 59.94
    },
    "Generic 15kHz": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 15750, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.192, "vbp": 1.024,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Arcade 15kHz": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 16200, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.192, "vbp": 1.024,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Arcade 15kHz EX": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 16500, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.192, "vbp": 1.024,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Arcade 25kHz": {
        "ranges": [{"lb": "25KHz", "hmin": 24960, "hmax": 24960, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 0.800, "hs": 4.000, "hbp": 3.200, "vfp": 0.080, "vs": 0.200, "vbp": 1.000,
                    "pLmin": 384, "pLmax": 400, "iLmin": 768, "iLmax": 800}],
        "dH": 24.96, "dV": 60.0
    },
    "Arcade 31kHz": {
        "ranges": [{"lb": "31KHz", "hmin": 31400, "hmax": 31500, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 0.940, "hs": 3.770, "hbp": 1.890, "vfp": 0.349, "vs": 0.064, "vbp": 1.017,
                    "pLmin": 400, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 31.45, "dV": 60.0
    },
    "Arcade 15/25kHz": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15625, "hmax": 16200, "vfmin": 49.5, "vfmax": 65.0,
             "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.192, "vbp": 1.024,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "25KHz", "hmin": 24960, "hmax": 24960, "vfmin": 49.5, "vfmax": 65.0,
             "hfp": 0.800, "hs": 4.000, "hbp": 3.200, "vfp": 0.080, "vs": 0.200, "vbp": 1.000,
             "pLmin": 384, "pLmax": 400, "iLmin": 768, "iLmax": 800}],
        "dH": 15.69, "dV": 60.0
    },
    "Arcade 15/31kHz": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15625, "hmax": 16200, "vfmin": 49.5, "vfmax": 65.0,
             "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.192, "vbp": 1.024,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "31KHz", "hmin": 31400, "hmax": 31500, "vfmin": 49.5, "vfmax": 65.0,
             "hfp": 0.940, "hs": 3.770, "hbp": 1.890, "vfp": 0.349, "vs": 0.064, "vbp": 1.017,
             "pLmin": 384, "pLmax": 480, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Arcade 15/25/31kHz": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15625, "hmax": 16200, "vfmin": 49.5, "vfmax": 65.0,
             "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.192, "vbp": 1.024,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "25KHz", "hmin": 24960, "hmax": 24960, "vfmin": 49.5, "vfmax": 65.0,
             "hfp": 0.800, "hs": 4.000, "hbp": 3.200, "vfp": 0.080, "vs": 0.200, "vbp": 1.000,
             "pLmin": 384, "pLmax": 400, "iLmin": 768, "iLmax": 800},
            {"lb": "31KHz", "hmin": 31400, "hmax": 31500, "vfmin": 49.5, "vfmax": 65.0,
             "hfp": 0.940, "hs": 3.770, "hbp": 1.890, "vfp": 0.349, "vs": 0.064, "vbp": 1.017,
             "pLmin": 400, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Wells Gardner D9800/D9400": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15250, "hmax": 18000, "vfmin": 40, "vfmax": 80,
             "hfp": 2.187, "hs": 4.688, "hbp": 6.719, "vfp": 0.190, "vs": 0.191, "vbp": 1.018,
             "pLmin": 224, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "25KHz", "hmin": 20501, "hmax": 29000, "vfmin": 40, "vfmax": 80,
             "hfp": 2.910, "hs": 3.000, "hbp": 4.440, "vfp": 0.451, "vs": 0.164, "vbp": 1.048,
             "pLmin": 320, "pLmax": 384, "iLmin": 0, "iLmax": 0},
            {"lb": "31KHz", "hmin": 29001, "hmax": 32000, "vfmin": 40, "vfmax": 80,
             "hfp": 0.636, "hs": 3.813, "hbp": 1.906, "vfp": 0.318, "vs": 0.064, "vbp": 1.048,
             "pLmin": 384, "pLmax": 480, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Wells Gardner K7000": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 15800, "vfmin": 49.5, "vfmax": 63.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.160, "vbp": 1.056,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Nanao MS-2930/2931": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15450, "hmax": 16050, "vfmin": 50, "vfmax": 65,
             "hfp": 3.190, "hs": 4.750, "hbp": 6.450, "vfp": 0.191, "vs": 0.191, "vbp": 1.164,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "31KHz", "hmin": 31000, "hmax": 32000, "vfmin": 50, "vfmax": 65,
             "hfp": 0.330, "hs": 3.580, "hbp": 1.750, "vfp": 0.316, "vs": 0.063, "vbp": 1.137,
             "pLmin": 480, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Hantarex MTC 9110 / Polo": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 16670, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.160, "vbp": 1.056,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Makvision 2929D": {
        "ranges": [{"lb": "31KHz", "hmin": 30000, "hmax": 40000, "vfmin": 47, "vfmax": 90,
                    "hfp": 0.600, "hs": 2.500, "hbp": 2.800, "vfp": 0.032, "vs": 0.096, "vbp": 0.448,
                    "pLmin": 384, "pLmax": 640, "iLmin": 0, "iLmax": 0}],
        "dH": 35.0, "dV": 60.0
    },
    "DP custom (ZFEbHVUE)": {
        "ranges": [{"lb": "15KHz PAL", "hmin": 15625, "hmax": 15750, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 1.990, "hs": 4.686, "hbp": 8.024, "vfp": 0.064, "vs": 0.480, "vbp": 1.024,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.625, "dV": 50.0
    },
}

# ==============================================================================
# COLORS (same dark theme)
# ==============================================================================
BG     = "#1e1e2e"
BG2    = "#2a2a3e"
BG3    = "#313145"
FG     = "#cdd6f4"
FG2    = "#a6adc8"
ACCENT = "#89b4fa"
GREEN  = "#a6e3a1"
RED    = "#f38ba8"
YELLOW = "#f9e2af"
FONT   = ("Sans", 8)
FONT_S = ("Sans", 8)
FONT_M = ("Monospace", 8)
FONT_B = ("Sans", 8, "bold")

# ==============================================================================
# COMPACT SLIDER+ENTRY WIDGET
# ==============================================================================
class SliderEntry:
    def __init__(self, parent, label, from_, to, resolution=0.001,
                 is_int=False, fmt="{:.3f}", slider_len=120):
        self.is_int    = is_int
        self.fmt       = fmt
        self._cb       = None
        self._updating = False

        self.frame = tk.Frame(parent, bg=BG)

        tk.Label(self.frame, text=label, fg=FG2, bg=BG, font=FONT_S,
                 width=18, anchor="w").pack(side="left")

        self.entry = tk.Entry(self.frame, width=8, bg=BG2, fg=FG,
                              insertbackground=FG, font=FONT_M,
                              relief="flat", bd=2)
        self.entry.pack(side="left", padx=(0, 4))
        self.entry.bind("<Return>",   self._from_entry)
        self.entry.bind("<FocusOut>", self._from_entry)

        self._var = tk.DoubleVar(value=float(from_))
        self.scale = tk.Scale(
            self.frame, from_=from_, to=to, resolution=resolution,
            orient="horizontal", variable=self._var, showvalue=0,
            length=slider_len, bg=BG, fg=FG2, troughcolor=BG3,
            activebackground=ACCENT, highlightthickness=0,
            sliderlength=12, command=self._from_scale
        )
        self.scale.pack(side="left", fill="x", expand=True)
        self.scale.bind("<ButtonRelease-1>", self._on_release)

    def _fmt(self, v):
        return str(int(round(float(v)))) if self.is_int else self.fmt.format(float(v))

    def _from_scale(self, val):
        if self._updating: return
        self._updating = True
        self.entry.delete(0, "end")
        self.entry.insert(0, self._fmt(val))
        self._updating = False

    def _on_release(self, _=None):
        if self._cb: self._cb()

    def _from_entry(self, _=None):
        try:
            v = float(self.entry.get())
            self._updating = True
            self._var.set(v)
            self._updating = False
            if self._cb: self._cb()
        except ValueError:
            pass

    def set_value(self, v):
        self._updating = True
        fv = float(v)
        self._var.set(fv)
        self.entry.delete(0, "end")
        self.entry.insert(0, self._fmt(fv))
        self._updating = False

    def get_value(self):
        try:
            v = float(self.entry.get())
            return int(round(v)) if self.is_int else v
        except ValueError:
            return self._var.get()

    def set_callback(self, cb): self._cb = cb
    def pack(self, **kw): self.frame.pack(**kw)
    def grid(self, **kw): self.frame.grid(**kw)

# ==============================================================================
# CALCULATIONS (identical to main version)
# ==============================================================================
def select_range(preset_name, hfreq_hz):
    p = PRESETS.get(preset_name)
    if not p:
        return PRESETS["Arcade 15kHz"]["ranges"][0]
    for r in p["ranges"]:
        if r["hmin"] <= hfreq_hz <= r["hmax"]:
            return r
    return p["ranges"][0]

def fmt_crt_range(r, hfp, hs, hbp, vfp, vs, vbp):
    return (f"crt_range0  {r['hmin']}-{r['hmax']}, "
            f"{r['vfmin']:.2f}-{r['vfmax']:.2f}, "
            f"{hfp:.3f}, {hs:.3f}, {hbp:.3f}, "
            f"{vfp:.3f}, {vs:.3f}, {vbp:.3f}, "
            f"0, 0, {r['pLmin']}, {r['pLmax']}, {r['iLmin']}, {r['iLmax']}")

def _safe_round(f):
    """Round float to int, using ceil when near X.5 to avoid sync instability."""
    frac = f % 1
    return math.ceil(f) if 0.4 <= frac <= 0.6 else round(f)

def calculate_from_range(H, V, Hfreq, Vfreq, interlaced, r):
    Div = 2 if interlaced else 1
    H_T = 1.0 / Hfreq;  V_T = 1.0 / Vfreq
    hfp_t = r["hfp"]*1e-6; hs_t = r["hs"]*1e-6; hbp_t = r["hbp"]*1e-6
    vfp_t = r["vfp"]*1e-3; vs_t = r["vs"]*1e-3; vbp_t = r["vbp"]*1e-3
    denom_H = 1.0 - hfp_t/H_T - hs_t/H_T - hbp_t/H_T
    denom_V = 1.0 - vfp_t/V_T - vs_t/V_T - vbp_t/V_T
    TH = H / (H_T * denom_H)
    TV = V / (V_T * denom_V)
    def _sr(f): return _safe_round(f)
    H_total = _sr(H / denom_H)
    HFP=round(hfp_t*TH); HSYNC=round(hs_t*TH); HBP=H_total-H-HFP-HSYNC
    V_total = _sr(V / denom_V)
    VFP=round(vfp_t*TV); VSYNC=round(vs_t*TV); VBP=V_total-V-VFP-VSYNC
    X1,X2 = H, H+HFP;           X3,X4 = H+HFP+HSYNC, H+HFP+HSYNC+HBP
    Y1,Y2 = V, V+VFP;           Y3,Y4 = V+VFP+VSYNC, V+VFP+VSYNC+VBP
    return dict(X1=X1,X2=X2,X3=X3,X4=X4,Y1=Y1,Y2=Y2,Y3=Y3,Y4=Y4,
                HFP=HFP,HSYNC=HSYNC,HBP=HBP,VFP=VFP,VSYNC=VSYNC,VBP=VBP,
                pclk=Hfreq*X4/1e6, Hfreq=Hfreq,
                Vfreq_actual=Hfreq*Div/Y4, interlaced=interlaced)

def calc_timings(res):
    X4,Y4 = res["X4"],res["Y4"]
    Hf,Vf = res["Hfreq"],res["Vfreq_actual"]
    H_T,V_T = 1/Hf, 1/Vf
    return {
        "H_actif_us": res["X1"]*H_T/X4*1e6, "HFP_us":  res["HFP"]*H_T/X4*1e6,
        "HSYNC_us":   res["HSYNC"]*H_T/X4*1e6, "HBP_us": res["HBP"]*H_T/X4*1e6,
        "H_total_us": H_T*1e6,
        "V_actif_ms": res["Y1"]*V_T/Y4*1e3, "VFP_ms":  res["VFP"]*V_T/Y4*1e3,
        "VSYNC_ms":   res["VSYNC"]*V_T/Y4*1e3, "VBP_ms": res["VBP"]*V_T/Y4*1e3,
        "V_total_ms": V_T*1e3,
    }

def verify_modeline(s):
    parts = s.strip().split()
    if len(parts) < 9: return None
    try:
        pclk = float(parts[0])
        X1,X2,X3,X4 = int(parts[1]),int(parts[2]),int(parts[3]),int(parts[4])
        Y1,Y2,Y3,Y4 = int(parts[5]),int(parts[6]),int(parts[7]),int(parts[8])
    except ValueError: return None
    interlaced = "interlace" in s.lower()
    Div = 2 if interlaced else 1
    Hfreq = pclk*1e6/X4
    return dict(X1=X1,X2=X2,X3=X3,X4=X4,Y1=Y1,Y2=Y2,Y3=Y3,Y4=Y4,
                HFP=X2-X1,HSYNC=X3-X2,HBP=X4-X3,
                VFP=Y2-Y1,VSYNC=Y3-Y2,VBP=Y4-Y3,
                pclk=pclk, Hfreq=Hfreq,
                Vfreq_actual=Hfreq*Div/Y4, interlaced=interlaced)

def distribute_ls(total, targets, minimums):
    n = len(targets)
    slack = total - sum(minimums)
    if slack < 0:
        result = list(minimums); result[-1] = max(1, result[-1]+slack); return result
    excess = [max(0.0, t-m) for t,m in zip(targets, minimums)]
    total_excess = sum(excess)
    if total_excess == 0:
        result = list(minimums); result[-1] += slack; return result
    ratios = [e/total_excess for e in excess]
    continuous = [slack*r for r in ratios]
    floors = [math.floor(c) for c in continuous]
    remainders = [c-f for c,f in zip(continuous, floors)]
    remaining = slack - sum(floors)
    indices = sorted(range(n), key=lambda i: remainders[i], reverse=True)
    for i in range(int(remaining)): floors[indices[i]] += 1
    return [minimums[i]+floors[i] for i in range(n)]

def optimize_modeline(H, V, Hfreq_target, Vfreq_target, interlaced, r):
    Div = 2 if interlaced else 1
    Hfreq = Hfreq_target
    hfp_t=r["hfp"]*1e-6; hs_t=r["hs"]*1e-6; hbp_t=r["hbp"]*1e-6
    vfp_t=r["vfp"]*1e-3; vs_t=r["vs"]*1e-3; vbp_t=r["vbp"]*1e-3
    V_T_tgt = 1.0/Vfreq_target
    denom_Vt = 1.0 - vfp_t/V_T_tgt - vs_t/V_T_tgt - vbp_t/V_T_tgt
    TERM_Vt  = V/(V_T_tgt*denom_Vt) if denom_Vt>0 else V*1.1
    VFP_min=max(1,math.floor(vfp_t*TERM_Vt*0.5)); VS_min=max(1,math.floor(vs_t*TERM_Vt*0.5))
    VBP_min=max(1,math.floor(vbp_t*TERM_Vt*0.5))
    V_total_min=V+VFP_min+VS_min+VBP_min
    V_total_ideal=Hfreq*Div/Vfreq_target
    candidates=sorted(set(max(V_total_min,round(V_total_ideal)+d) for d in range(-10,11)))
    candidates=[vt for vt in candidates if vt>=V_total_min]
    best_V=min(candidates,key=lambda vt:abs(Hfreq*Div/vt-Vfreq_target))
    Vfreq_actual=Hfreq*Div/best_V
    V_T_act=1.0/Vfreq_actual
    denom_Va=1.0-vfp_t/V_T_act-vs_t/V_T_act-vbp_t/V_T_act
    TERM_Va=V/(V_T_act*denom_Va) if denom_Va>0 else V*1.1
    VFP_tgt=vfp_t*TERM_Va; VS_tgt=vs_t*TERM_Va; VBP_tgt=vbp_t*TERM_Va
    VFP_min2=max(1,math.floor(VFP_tgt*0.5)); VS_min2=max(1,math.floor(VS_tgt*0.5))
    VBP_min2=max(1,math.floor(VBP_tgt*0.5))
    VFP,VSYNC,VBP=distribute_ls(best_V-V,[VFP_tgt,VS_tgt,VBP_tgt],[VFP_min2,VS_min2,VBP_min2])
    # SwitchRes threshold check
    hmax=r["hmax"]; threshold_ms=22500.0/hmax
    line_ms=1000.0/(Hfreq*Div)
    vblank_ms=(VFP+VSYNC+VBP)*line_ms
    switchres_ok=vblank_ms<threshold_ms
    if not switchres_ok and VBP>VBP_min2:
        VBP-=1; vblank_ms=(VFP+VSYNC+VBP)*line_ms; switchres_ok=vblank_ms<threshold_ms
    H_T=1.0/Hfreq; denom_H=1.0-hfp_t/H_T-hs_t/H_T-hbp_t/H_T
    TERM_H=H/(H_T*denom_H) if denom_H>0 else H*1.15
    HFP_tgt=hfp_t*TERM_H; HS_tgt=hs_t*TERM_H; HBP_tgt=hbp_t*TERM_H
    HFP_min=max(1,math.floor(HFP_tgt*0.5)); HS_min=max(1,math.floor(HS_tgt*0.5))
    HBP_min=max(1,math.floor(HBP_tgt*0.5))
    H_total=max(H+HFP_min+HS_min+HBP_min,_safe_round(H/denom_H) if denom_H>0 else H+50)
    HFP_tgt2=hfp_t*Hfreq*H_total; HS_tgt2=hs_t*Hfreq*H_total; HBP_tgt2=hbp_t*Hfreq*H_total
    HFP_min2=max(1,math.floor(HFP_tgt2*0.5)); HS_min2=max(1,math.floor(HS_tgt2*0.5))
    HBP_min2=max(1,math.floor(HBP_tgt2*0.5))
    HFP,HSYNC,HBP=distribute_ls(H_total-H,[HFP_tgt2,HS_tgt2,HBP_tgt2],[HFP_min2,HS_min2,HBP_min2])
    X1,X2=H,H+HFP; X3,X4=H+HFP+HSYNC,H+HFP+HSYNC+HBP
    Y1,Y2=V,V+VFP; Y3,Y4=V+VFP+VSYNC,V+VFP+VSYNC+VBP
    return dict(X1=X1,X2=X2,X3=X3,X4=X4,Y1=Y1,Y2=Y2,Y3=Y3,Y4=Y4,
                HFP=HFP,HSYNC=HSYNC,HBP=HBP,VFP=VFP,VSYNC=VSYNC,VBP=VBP,
                pclk=Hfreq*X4/1e6,Hfreq=Hfreq,Vfreq_actual=Vfreq_actual,
                interlaced=interlaced,
                Vfreq_error=abs(Vfreq_actual-Vfreq_target),Hfreq_error=0.0,
                switchres_ok=switchres_ok,vblank_ms=vblank_ms,threshold_ms=threshold_ms)

# ==============================================================================
# COMPACT APPLICATION — 640×480
# ==============================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CRT Modeline Toolbox — CRT v2.0")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(640, 480)
        self._current_range = None
        self._custom_mode   = False
        self._last_res      = None
        self._build_styles()
        self._build_ui()
        self._apply_preset()

    def _build_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".", background=BG, foreground=FG,
                     fieldbackground=BG2, font=FONT, borderwidth=0)
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=BG3, foreground=FG2,
                     padding=[8,3], font=FONT)
        s.map("TNotebook.Tab",
              background=[("selected",BG2)], foreground=[("selected",ACCENT)])
        s.configure("TFrame",      background=BG)
        s.configure("TLabel",      background=BG, foreground=FG)
        s.configure("TLabelframe", background=BG, foreground=ACCENT, bordercolor=BG3)
        s.configure("TLabelframe.Label", background=BG, foreground=ACCENT, font=FONT_B)
        s.configure("TCombobox",   fieldbackground=BG2, foreground=FG,
                     selectbackground=BG2, selectforeground=FG)
        s.map("TCombobox",
              fieldbackground=[("readonly",BG2)],
              foreground=[("readonly",FG)],
              selectbackground=[("readonly",BG2)],
              selectforeground=[("readonly",FG)])
        s.configure("TButton",     background=BG3, foreground=FG, padding=[5,2])
        s.map("TButton", background=[("active",ACCENT)], foreground=[("active",BG)])
        s.configure("TEntry",      fieldbackground=BG2, foreground=FG)
        s.configure("Treeview", background=BG2, foreground=FG,
                     fieldbackground=BG2, rowheight=18, font=FONT_S)
        s.configure("Treeview.Heading", background=BG3, foreground=ACCENT, font=FONT_S)
        s.map("Treeview", background=[("selected", BG3)])
        self.option_add("*TCombobox*Listbox.foreground", FG)
        self.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        self.option_add("*TCombobox*Listbox.selectForeground", BG)

    def _style_cmb(self, cmb):
        """Force dark dropdown listbox on any combobox — works on all Linux themes."""
        def _fix():
            try:
                pw = cmb.tk.eval(f'ttk::combobox::PopdownWindow {cmb._w}')
                cmb.tk.eval(
                    f'{pw}.f.l configure '
                    f'-background {BG2} -foreground {FG} '
                    f'-selectbackground {ACCENT} -selectforeground {BG} '
                    f'-font {{Sans 9}}'
                )
            except Exception:
                pass
        cmb.configure(postcommand=_fix)

    def _text_ro(self, parent, height=1, width=60):
        t = tk.Text(parent, height=height, width=width, bg=BG2, fg=YELLOW,
                    font=FONT_M, relief="flat", bd=2,
                    state="disabled", wrap="char")
        return t

    def _set_text(self, w, text):
        w.config(state="normal")
        w.delete("1.0", "end")
        w.insert("1.0", text)
        w.config(state="disabled")

    def _scrollable(self, parent):
        """Return (canvas, inner_frame) — inner_frame is the scrollable container."""
        canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
        vsb    = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner = ttk.Frame(canvas)
        win   = canvas.create_window((0,0), window=inner, anchor="nw")
        def _cfg(e): canvas.configure(scrollregion=canvas.bbox("all"))
        def _cvcfg(e): canvas.itemconfig(win, width=e.width)
        def _mw(e): canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        inner.bind("<Configure>",   _cfg)
        canvas.bind("<Configure>",  _cvcfg)
        canvas.bind_all("<MouseWheel>", _mw)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1,"units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1,"units"))
        return inner

    # ==========================================================================
    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)
        self.tab_setup  = ttk.Frame(nb)
        self.tab_range  = ttk.Frame(nb)
        self.tab_result = ttk.Frame(nb)
        self.tab_verify = ttk.Frame(nb)
        nb.add(self.tab_setup,  text=" Setup ")
        nb.add(self.tab_range,  text=" CRT Range ")
        nb.add(self.tab_result, text=" Results ")
        nb.add(self.tab_verify, text=" Verify ")
        self._build_setup(self.tab_setup)
        self._build_range(self.tab_range)
        self._build_result(self.tab_result)
        self._build_verify(self.tab_verify)

    # ==========================================================================
    # TAB 1 — SETUP
    # ==========================================================================
    def _build_setup(self, parent):
        inner = self._scrollable(parent)

        # Monitor / Range row
        frm_mon = tk.Frame(inner, bg=BG)
        frm_mon.pack(fill="x", padx=4, pady=3)
        tk.Label(frm_mon, text="Monitor", fg=FG2, bg=BG, font=FONT_S,
                 width=8, anchor="w").pack(side="left")
        self.cmb_preset = ttk.Combobox(frm_mon, values=list(PRESETS.keys()),
                                        state="readonly", width=20)
        self.cmb_preset.set("Arcade 15kHz")
        self.cmb_preset.pack(side="left", padx=(0,6))
        self.cmb_preset.bind("<<ComboboxSelected>>", lambda e: self._apply_preset())
        self._style_cmb(self.cmb_preset)

        tk.Label(frm_mon, text="Range", fg=FG2, bg=BG,
                 font=FONT_S).pack(side="left", padx=(0,4))
        self.cmb_range = ttk.Combobox(frm_mon, values=[], state="readonly", width=12)
        self.cmb_range.pack(side="left")
        self.cmb_range.bind("<<ComboboxSelected>>", lambda e: self._on_range_select())
        self._style_cmb(self.cmb_range)

        # Interlaced + Output row
        frm_opt = tk.Frame(inner, bg=BG)
        frm_opt.pack(fill="x", padx=4, pady=2)
        tk.Label(frm_opt, text="Interlaced", fg=FG2, bg=BG,
                 font=FONT_S).pack(side="left")
        self.var_interlaced = tk.IntVar(value=0)
        tk.Checkbutton(frm_opt, variable=self.var_interlaced,
                       bg=BG, fg=FG, selectcolor=BG3, activebackground=BG,
                       command=self._calc_gen).pack(side="left", padx=(0,12))
        tk.Label(frm_opt, text="Output", fg=FG2, bg=BG,
                 font=FONT_S).pack(side="left")
        self.e_output = tk.Entry(frm_opt, width=7, bg=BG2, fg=FG,
                                  insertbackground=FG, font=FONT_M,
                                  relief="flat", bd=2)
        self.e_output.insert(0, "DP-1")
        self.e_output.pack(side="left", padx=4)
        self.e_output.bind("<Return>",   lambda e: self._calc_gen())
        self.e_output.bind("<FocusOut>", lambda e: self._calc_gen())

        tk.Label(frm_opt, text="Name", fg=FG2, bg=BG,
                 font=FONT_S).pack(side="left", padx=(8,0))
        self.e_name = tk.Entry(frm_opt, width=12, bg=BG2, fg=YELLOW,
                                insertbackground=FG, font=FONT_M,
                                relief="flat", bd=2)
        self.e_name.pack(side="left", padx=4)
        self.e_name.bind("<Return>",   lambda e: self._calc_gen())
        self.e_name.bind("<FocusOut>", lambda e: self._calc_gen())

        tk.Frame(inner, bg=BG3, height=1).pack(fill="x", padx=4, pady=3)

        # Resolution + frequency sliders
        tk.Label(inner, text="Parameters", fg=ACCENT, bg=BG,
                 font=FONT_B).pack(anchor="w", padx=6, pady=(0,2))

        self.sw_width  = SliderEntry(inner,"H Width (px)",  64, 3840, 1,    is_int=True, fmt="{:.0f}")
        self.sw_height = SliderEntry(inner,"V Height (px)", 32, 2160, 1,    is_int=True, fmt="{:.0f}")
        self.sw_hfreq  = SliderEntry(inner,"Hfreq (kHz)",  15.0, 70.0, 0.001)
        self.sw_vfreq  = SliderEntry(inner,"Vfreq (Hz)",   49.0, 130.0, 0.01, fmt="{:.3f}")

        self.sw_width.set_value(640);   self.sw_width.set_callback(self._calc_gen)
        self.sw_height.set_value(480);  self.sw_height.set_callback(self._calc_gen)
        self.sw_hfreq.set_value(15.69); self.sw_hfreq.set_callback(self._on_hfreq_cb)
        self.sw_vfreq.set_value(60.0);  self.sw_vfreq.set_callback(self._calc_gen)

        for sw in (self.sw_width, self.sw_height, self.sw_hfreq, self.sw_vfreq):
            sw.pack(fill="x", padx=4, pady=2)

        tk.Frame(inner, bg=BG3, height=1).pack(fill="x", padx=4, pady=3)

        # Paste CRT Range
        tk.Label(inner, text="Paste CRT Range / Import Modeline", fg=ACCENT, bg=BG,
                 font=FONT_B).pack(anchor="w", padx=6, pady=(0,2))
        frm_paste = tk.Frame(inner, bg=BG)
        frm_paste.pack(fill="x", padx=4, pady=2)
        tk.Label(frm_paste, text="CRT Range:", fg=FG2, bg=BG,
                 font=FONT_S, width=10).pack(side="left")
        self.e_crt_paste = tk.Entry(frm_paste, bg=BG2, fg=YELLOW,
                                     insertbackground=FG, font=FONT_M,
                                     relief="flat", bd=2)
        self.e_crt_paste.pack(side="left", fill="x", expand=True, padx=(0,4))
        self.e_crt_paste.bind("<Return>", lambda e: self._parse_crt_range())
        ttk.Button(frm_paste, text="Parse",
                   command=self._parse_crt_range).pack(side="left")

        frm_imp = tk.Frame(inner, bg=BG)
        frm_imp.pack(fill="x", padx=4, pady=2)
        tk.Label(frm_imp, text="Modeline:", fg=FG2, bg=BG,
                 font=FONT_S, width=10).pack(side="left")
        self.e_import = tk.Entry(frm_imp, bg=BG2, fg=YELLOW,
                                  insertbackground=FG, font=FONT_M,
                                  relief="flat", bd=2)
        self.e_import.pack(side="left", fill="x", expand=True, padx=(0,4))
        self.e_import.bind("<Return>", lambda e: self._import_modeline())
        ttk.Button(frm_imp, text="Import →",
                   command=self._import_modeline).pack(side="left")

        tk.Frame(inner, bg=BG3, height=1).pack(fill="x", padx=4, pady=3)

        # Direct pixel/line porch sliders
        tk.Label(inner, text="Direct Porch Adjustment (px / lines)", fg=ACCENT, bg=BG,
                 font=FONT_B).pack(anchor="w", padx=6, pady=(0,2))

        self.sw_hfp_px = SliderEntry(inner,"H Front Porch (px)",1,300,1,is_int=True,fmt="{:.0f}")
        self.sw_hs_px  = SliderEntry(inner,"H Sync (px)",       1,300,1,is_int=True,fmt="{:.0f}")
        self.sw_hbp_px = SliderEntry(inner,"H Back Porch (px)", 1,500,1,is_int=True,fmt="{:.0f}")
        self.sw_vfp_px = SliderEntry(inner,"V Front Porch (ln)",1,100,1,is_int=True,fmt="{:.0f}")
        self.sw_vs_px  = SliderEntry(inner,"V Sync (lines)",    1,100,1,is_int=True,fmt="{:.0f}")
        self.sw_vbp_px = SliderEntry(inner,"V Back Porch (ln)", 1,200,1,is_int=True,fmt="{:.0f}")
        for sw in (self.sw_hfp_px,self.sw_hs_px,self.sw_hbp_px,
                   self.sw_vfp_px,self.sw_vs_px,self.sw_vbp_px):
            sw.set_callback(self._calc_from_pixels)
            sw.pack(fill="x", padx=4, pady=2)

    # ==========================================================================
    # TAB 2 — CRT RANGE
    # ==========================================================================
    def _build_range(self, parent):
        inner = self._scrollable(parent)

        # µs / ms sliders
        tk.Label(inner, text="Time domain (µs / ms)", fg=ACCENT, bg=BG,
                 font=FONT_B).pack(anchor="w", padx=6, pady=(4,2))

        self.sw_hfp = SliderEntry(inner,"H Front Porch (µs)",0.05,12.0,0.001)
        self.sw_hs  = SliderEntry(inner,"H Sync (µs)",       0.05,10.0,0.001)
        self.sw_hbp = SliderEntry(inner,"H Back Porch (µs)", 0.05,15.0,0.001)
        self.sw_vfp = SliderEntry(inner,"V Front Porch (ms)",0.01, 2.0,0.001)
        self.sw_vs  = SliderEntry(inner,"V Sync (ms)",       0.01, 2.0,0.001)
        self.sw_vbp = SliderEntry(inner,"V Back Porch (ms)", 0.01, 3.0,0.001)
        for sw in (self.sw_hfp,self.sw_hs,self.sw_hbp,
                   self.sw_vfp,self.sw_vs,self.sw_vbp):
            sw.set_callback(self._calc_gen)
            sw.pack(fill="x", padx=4, pady=2)

        tk.Frame(inner, bg=BG3, height=1).pack(fill="x", padx=4, pady=3)

        # Timings table
        tk.Label(inner, text="Timings", fg=ACCENT, bg=BG,
                 font=FONT_B).pack(anchor="w", padx=6, pady=(0,2))
        cols = ("Parameter", "px/lines", "Time", "Unit")
        self.tree_gen = ttk.Treeview(inner, columns=cols,
                                      show="headings", height=11)
        col_w = {"Parameter": 110, "px/lines": 60, "Time": 70, "Unit": 30}
        for c in cols:
            self.tree_gen.heading(c, text=c)
            self.tree_gen.column(c, width=col_w[c], anchor="center")
        self.tree_gen.pack(fill="x", padx=4, pady=4)

    # ==========================================================================
    # TAB 3 — RESULTS
    # ==========================================================================
    def _build_result(self, parent):
        inner = self._scrollable(parent)

        # Compact metrics grid
        frm_m = ttk.LabelFrame(inner, text="Metrics")
        frm_m.pack(fill="x", padx=4, pady=3)
        metrics = [
            ("Pixel clock","lbl_pclk"), ("Hfreq (kHz)","lbl_hfreq"),
            ("Vfreq (Hz)", "lbl_vfreq"),("H total (px)","lbl_htot"),
            ("V total (px)","lbl_vtot"),("H blanking","lbl_hblk"),
        ]
        for i,(label,attr) in enumerate(metrics):
            f = tk.Frame(frm_m, bg=BG2, padx=6, pady=2)
            f.grid(row=i//3, column=i%3, padx=3, pady=2, sticky="ew")
            frm_m.columnconfigure(i%3, weight=1)
            tk.Label(f,text=label,fg=FG2,bg=BG2,font=("Sans",7)).pack(anchor="w")
            lbl = tk.Label(f,text="—",fg=FG,bg=BG2,font=("Sans",9,"bold"))
            lbl.pack(anchor="w")
            setattr(self, attr, lbl)

        # Verification
        frm_chk = ttk.LabelFrame(inner, text="Verification")
        frm_chk.pack(fill="x", padx=4, pady=2)
        self.lbl_chk_h = tk.Label(frm_chk,text="",bg=BG,font=FONT_S)
        self.lbl_chk_h.pack(anchor="w", padx=4)
        self.lbl_chk_v = tk.Label(frm_chk,text="",bg=BG,font=FONT_S)
        self.lbl_chk_v.pack(anchor="w", padx=4)
        self.lbl_chk_l = tk.Label(frm_chk,text="",bg=BG,font=FONT_S)
        self.lbl_chk_l.pack(anchor="w", padx=4)

        # CRT Range fixed
        self.frm_cf = ttk.LabelFrame(inner, text="CRT Range — Calamity (fixed)")
        self.frm_cf.pack(fill="x", padx=4, pady=2)
        self.txt_crt_fixed = self._text_ro(self.frm_cf, height=2)
        self.txt_crt_fixed.pack(fill="x", padx=4, pady=3)

        # CRT Range calculated
        frm_cc = ttk.LabelFrame(inner, text="CRT Range — calculated")
        frm_cc.pack(fill="x", padx=4, pady=2)
        self.txt_crt_calc = self._text_ro(frm_cc, height=2)
        self.txt_crt_calc.pack(fill="x", padx=4, pady=3)

        # Modeline
        frm_ml = ttk.LabelFrame(inner, text="Modeline")
        frm_ml.pack(fill="x", padx=4, pady=2)
        self.txt_modeline = self._text_ro(frm_ml, height=2)
        self.txt_modeline.pack(fill="x", padx=4, pady=3)

        # xrandr
        frm_xr = ttk.LabelFrame(inner, text="xrandr command")
        frm_xr.pack(fill="x", padx=4, pady=2)
        self.txt_xrandr = self._text_ro(frm_xr, height=3)
        self.txt_xrandr.pack(fill="x", padx=4, pady=3)

        # Buttons — row 1: xrandr + optimiser + Lock VFP
        frm_btn = tk.Frame(inner, bg=BG)
        frm_btn.pack(fill="x", padx=4, pady=(4,0))

        frm_btn1 = tk.Frame(frm_btn, bg=BG)
        frm_btn1.pack(fill="x", pady=(0,2))
        for text, cmd in [
            ("Copy",      self._copy_xrandr),
            ("Apply",     self._apply_xrandr),
            ("⚡ Opt LS", self._optimise_ls),
        ]:
            ttk.Button(frm_btn1, text=text, command=cmd).pack(side="left", padx=2)
        self.var_vfp_lock = tk.IntVar(value=0)
        ttk.Checkbutton(frm_btn1, text="Lock VFP", variable=self.var_vfp_lock).pack(
            side="left", padx=(6,2))
        self.spn_vfp_lock = tk.Spinbox(frm_btn1, from_=1, to=30, width=3,
                                        bg=BG2, fg=YELLOW, insertbackground=FG,
                                        buttonbackground=BG2, relief="flat", font=FONT_S)
        self.spn_vfp_lock.delete(0,"end"); self.spn_vfp_lock.insert(0,"3")
        self.spn_vfp_lock.pack(side="left", padx=(0,2))
        tk.Label(frm_btn1, text="l", fg=FG2, bg=BG, font=FONT_S).pack(side="left", padx=(0,6))
        self.lbl_ls_error = tk.Label(frm_btn1, text="", fg=YELLOW, bg=BG, font=FONT_S)
        self.lbl_ls_error.pack(side="left", padx=2)

        # Row 2 — save/load + diagram
        frm_btn2 = tk.Frame(frm_btn, bg=BG)
        frm_btn2.pack(fill="x", pady=(0,2))
        for text, cmd in [
            ("💾 Save CRT", self._save_crt_range),
            ("📂 Load CRT", self._load_crt_range),
            ("🎬 Save ML",  self._save_modeline),
            ("📂 Load ML",  self._load_modeline),
            ("📺 Diagram",  self._show_diagram),
        ]:
            ttk.Button(frm_btn2, text=text, command=cmd).pack(side="left", padx=2)

    # ==========================================================================
    # TAB 4 — VERIFY
    # ==========================================================================
    def _build_verify(self, parent):
        inner = self._scrollable(parent)

        frm_in = ttk.LabelFrame(inner, text="Modeline to verify")
        frm_in.pack(fill="x", padx=4, pady=3)
        self.e_modeline_in = tk.Entry(frm_in, bg=BG2, fg=FG,
                                       insertbackground=FG, font=FONT_M,
                                       relief="flat", bd=2)
        self.e_modeline_in.insert(0,"13.038390 640 666 727 831 480 483 489 523 interlace -hsync -vsync")
        self.e_modeline_in.pack(fill="x", padx=4, pady=4)
        self.e_modeline_in.bind("<Return>",   lambda e: self._calc_ver())
        self.e_modeline_in.bind("<FocusOut>", lambda e: self._calc_ver())

        frm_sel = tk.Frame(inner, bg=BG)
        frm_sel.pack(fill="x", padx=4, pady=2)
        tk.Label(frm_sel,text="Monitor:",fg=FG2,bg=BG,font=FONT_S).pack(side="left")
        self.cmb_preset_v = ttk.Combobox(frm_sel, values=list(PRESETS.keys()),
                                          state="readonly", width=18)
        self.cmb_preset_v.set("Arcade 15kHz")
        self.cmb_preset_v.pack(side="left", padx=4)
        self.cmb_preset_v.bind("<<ComboboxSelected>>", lambda e: self._calc_ver())
        self._style_cmb(self.cmb_preset_v)
        tk.Label(frm_sel,text="Output:",fg=FG2,bg=BG,font=FONT_S).pack(side="left",padx=(8,0))
        self.e_output_v = tk.Entry(frm_sel,width=6,bg=BG2,fg=FG,
                                    insertbackground=FG,font=FONT_M,relief="flat",bd=2)
        self.e_output_v.insert(0,"DP-1")
        self.e_output_v.pack(side="left", padx=4)
        ttk.Button(frm_sel,text="Verify",command=self._calc_ver).pack(side="left",padx=4)
        self.lbl_range_v = tk.Label(frm_sel,text="",fg=ACCENT,bg=BG,font=FONT_B)
        self.lbl_range_v.pack(side="left")

        frm_chk = ttk.LabelFrame(inner, text="Verification")
        frm_chk.pack(fill="x", padx=4, pady=2)
        self.lbl_v_chk_h = tk.Label(frm_chk,text="",bg=BG,font=FONT_S)
        self.lbl_v_chk_h.pack(anchor="w", padx=4)
        self.lbl_v_chk_v = tk.Label(frm_chk,text="",bg=BG,font=FONT_S)
        self.lbl_v_chk_v.pack(anchor="w", padx=4)
        self.lbl_v_chk_l = tk.Label(frm_chk,text="",bg=BG,font=FONT_S)
        self.lbl_v_chk_l.pack(anchor="w", padx=4)

        frm_vm = tk.Frame(inner,bg=BG)
        frm_vm.pack(fill="x",padx=4,pady=2)
        frm_vm.columnconfigure(0,weight=1); frm_vm.columnconfigure(1,weight=1)
        for i,(label,attr) in enumerate([
            ("Pixel clock","lbl_v_pclk"),("Hfreq (kHz)","lbl_v_hfreq"),
            ("Vfreq (Hz)","lbl_v_vfreq"),("H total","lbl_v_htot"),
            ("V total","lbl_v_vtot"),("Mode","lbl_v_mode")
        ]):
            f=tk.Frame(frm_vm,bg=BG2,padx=4,pady=2)
            f.grid(row=i//3,column=i%3,padx=2,pady=2,sticky="ew")
            frm_vm.columnconfigure(i%3,weight=1)
            tk.Label(f,text=label,fg=FG2,bg=BG2,font=("Sans",7)).pack(anchor="w")
            lbl=tk.Label(f,text="—",fg=FG,bg=BG2,font=("Sans",8,"bold"))
            lbl.pack(anchor="w")
            setattr(self,attr,lbl)

        frm_vcalc = ttk.LabelFrame(inner, text="CRT Range — calculated")
        frm_vcalc.pack(fill="x", padx=4, pady=2)
        self.txt_v_crt_calc = self._text_ro(frm_vcalc, height=2)
        self.txt_v_crt_calc.pack(fill="x", padx=4, pady=3)

        frm_vxr = ttk.LabelFrame(inner, text="xrandr command")
        frm_vxr.pack(fill="x", padx=4, pady=2)
        self.txt_v_xrandr = self._text_ro(frm_vxr, height=3)
        self.txt_v_xrandr.pack(fill="x", padx=4, pady=3)

    # ==========================================================================
    # LOGIC — identical to main version
    # ==========================================================================
    def _apply_preset(self):
        name = self.cmb_preset.get()
        p    = PRESETS.get(name)
        if not p: return
        self.sw_hfreq.set_value(p["dH"])
        self.sw_vfreq.set_value(p["dV"])
        labels = [x["lb"] for x in p["ranges"]]
        self.cmb_range["values"] = labels
        self.cmb_range.set(labels[0])
        self._load_range(p["ranges"][0])
        self._calc_gen()

    def _load_range(self, r):
        self._current_range = r
        self._custom_mode   = False
        self.sw_hfp.set_value(r["hfp"]); self.sw_hs.set_value(r["hs"])
        self.sw_hbp.set_value(r["hbp"]); self.sw_vfp.set_value(r["vfp"])
        self.sw_vs.set_value(r["vs"]);   self.sw_vbp.set_value(r["vbp"])
        mid = (r["hmin"]+r["hmax"])/2/1000
        self.sw_hfreq.set_value(round(mid,3))
        if r["lb"] in self.cmb_range["values"]: self.cmb_range.set(r["lb"])
        self._set_text(self.txt_crt_fixed,
                       fmt_crt_range(r,r["hfp"],r["hs"],r["hbp"],r["vfp"],r["vs"],r["vbp"]))
        self.frm_cf.config(text="CRT Range — Calamity (fixed)")

    def _on_range_select(self):
        name = self.cmb_preset.get()
        p    = PRESETS.get(name)
        if not p: return
        lb = self.cmb_range.get()
        for r in p["ranges"]:
            if r["lb"] == lb:
                self._load_range(r); self._calc_gen(); return

    def _on_hfreq_cb(self):
        name     = self.cmb_preset.get()
        hfreq_hz = self.sw_hfreq.get_value()*1000
        r        = select_range(name, hfreq_hz)
        if not self._custom_mode and r is not self._current_range:
            self._current_range = r
            self.sw_hfp.set_value(r["hfp"]); self.sw_hs.set_value(r["hs"])
            self.sw_hbp.set_value(r["hbp"]); self.sw_vfp.set_value(r["vfp"])
            self.sw_vs.set_value(r["vs"]);   self.sw_vbp.set_value(r["vbp"])
            if r["lb"] in self.cmb_range["values"]: self.cmb_range.set(r["lb"])
            self._set_text(self.txt_crt_fixed,
                           fmt_crt_range(r,r["hfp"],r["hs"],r["hbp"],r["vfp"],r["vs"],r["vbp"]))
            self.frm_cf.config(text="CRT Range — Calamity (fixed)")
        self._calc_gen()

    def _parse_crt_range(self):
        import re
        raw = self.e_crt_paste.get().strip()
        raw = re.sub(r'^crt_range\d*\s*','',raw).strip()
        parts = [p.strip() for p in raw.split(',')]
        if len(parts) < 14:
            messagebox.showerror("Parse error","Expected: hmin-hmax, vfmin-vfmax, hfp, hs, hbp, vfp, vs, vbp, 0, 0, pLmin, pLmax, iLmin, iLmax")
            return
        try:
            hrange=parts[0].split('-'); hmin,hmax=float(hrange[0]),float(hrange[1])
            vrange=parts[1].split('-'); vfmin,vfmax=float(vrange[0]),float(vrange[1])
            hfp=float(parts[2]); hs=float(parts[3]); hbp=float(parts[4])
            vfp=float(parts[5]); vs=float(parts[6]); vbp=float(parts[7])
            pLmin=int(float(parts[10])); pLmax=int(float(parts[11]))
            iLmin=int(float(parts[12])); iLmax=int(float(parts[13]))
        except Exception as e:
            messagebox.showerror("Parse error",str(e)); return
        r={"lb":"custom","hmin":hmin,"hmax":hmax,"vfmin":vfmin,"vfmax":vfmax,
           "hfp":hfp,"hs":hs,"hbp":hbp,"vfp":vfp,"vs":vs,"vbp":vbp,
           "pLmin":pLmin,"pLmax":pLmax,"iLmin":iLmin,"iLmax":iLmax}
        self._current_range = r
        self._custom_mode   = True
        self.sw_hfp.set_value(hfp); self.sw_hs.set_value(hs); self.sw_hbp.set_value(hbp)
        self.sw_vfp.set_value(vfp); self.sw_vs.set_value(vs); self.sw_vbp.set_value(vbp)
        mid=(hmin+hmax)/2/1000
        self.sw_hfreq.set_value(round(mid,3))
        self.cmb_range["values"]=["custom"]; self.cmb_range.set("custom")
        self._set_text(self.txt_crt_fixed,fmt_crt_range(r,hfp,hs,hbp,vfp,vs,vbp))
        self.frm_cf.config(text="CRT Range — Custom (pasted)")
        self._calc_gen()

    def _calc_from_pixels(self):
        try:
            H=self.sw_width.get_value(); V=self.sw_height.get_value()
            Hf=self.sw_hfreq.get_value()*1000; i=self.var_interlaced.get()
            Div=2 if i else 1
            r=self._current_range or PRESETS["Arcade 15kHz"]["ranges"][0]
            HFP=int(self.sw_hfp_px.get_value()); HSYNC=int(self.sw_hs_px.get_value())
            HBP=int(self.sw_hbp_px.get_value()); VFP=int(self.sw_vfp_px.get_value())
            VSYNC=int(self.sw_vs_px.get_value()); VBP=int(self.sw_vbp_px.get_value())
            H_total=H+HFP+HSYNC+HBP; V_total=V+VFP+VSYNC+VBP
            pclk=Hf*H_total/1e6; Vf_act=Hf*Div/V_total
            hfp_us=HFP/H_total/Hf*1e6; hs_us=HSYNC/H_total/Hf*1e6; hbp_us=HBP/H_total/Hf*1e6
            vfp_ms=VFP/V_total/Vf_act*1e3; vs_ms=VSYNC/V_total/Vf_act*1e3; vbp_ms=VBP/V_total/Vf_act*1e3
            self.sw_hfp.set_value(round(hfp_us,3)); self.sw_hs.set_value(round(hs_us,3))
            self.sw_hbp.set_value(round(hbp_us,3)); self.sw_vfp.set_value(round(vfp_ms,3))
            self.sw_vs.set_value(round(vs_ms,3));   self.sw_vbp.set_value(round(vbp_ms,3))
            res=dict(X1=H,X2=H+HFP,X3=H+HFP+HSYNC,X4=H_total,
                     Y1=V,Y2=V+VFP,Y3=V+VFP+VSYNC,Y4=V_total,
                     HFP=HFP,HSYNC=HSYNC,HBP=HBP,VFP=VFP,VSYNC=VSYNC,VBP=VBP,
                     pclk=pclk,Hfreq=Hf,Vfreq_actual=Vf_act,interlaced=i)
            r_live={"hfp":hfp_us,"hs":hs_us,"hbp":hbp_us,
                    "vfp":vfp_ms,"vs":vs_ms,"vbp":vbp_ms,
                    **{k:r[k] for k in ("hmin","hmax","vfmin","vfmax","pLmin","pLmax","iLmin","iLmax")}}
            self._refresh_display(res, r_live)
        except Exception: return

    def _calc_gen(self):
        try:
            H=self.sw_width.get_value(); V=self.sw_height.get_value()
            Hf=self.sw_hfreq.get_value()*1000; Vf=self.sw_vfreq.get_value()
            i=self.var_interlaced.get()
            r=self._current_range or PRESETS["Arcade 15kHz"]["ranges"][0]
            r_live={"hfp":self.sw_hfp.get_value(),"hs":self.sw_hs.get_value(),
                    "hbp":self.sw_hbp.get_value(),"vfp":self.sw_vfp.get_value(),
                    "vs":self.sw_vs.get_value(),"vbp":self.sw_vbp.get_value(),
                    **{k:r[k] for k in ("hmin","hmax","vfmin","vfmax","pLmin","pLmax","iLmin","iLmax")}}
        except Exception: return
        res=calculate_from_range(H,V,Hf,Vf,i,r_live)
        self.sw_hfp_px.set_value(res["HFP"]); self.sw_hs_px.set_value(res["HSYNC"])
        self.sw_hbp_px.set_value(res["HBP"]); self.sw_vfp_px.set_value(res["VFP"])
        self.sw_vs_px.set_value(res["VSYNC"]); self.sw_vbp_px.set_value(res["VBP"])
        self._refresh_display(res, r_live)

    def _refresh_display(self, res, r_live):
        self._last_res = res
        t=calc_timings(res)
        Hf=res["Hfreq"]; V=res["Y1"]; i=res["interlaced"]
        out=self.e_output.get() or "DP-1"

        self.lbl_pclk.config( text=f"{res['pclk']:.4f} MHz")
        self.lbl_hfreq.config(text=f"{Hf/1000:.6f}")
        self.lbl_vfreq.config(text=f"{res['Vfreq_actual']:.6f}")
        self.lbl_htot.config( text=str(res["X4"]))
        self.lbl_vtot.config( text=str(res["Y4"]))
        self.lbl_hblk.config( text=str(res["HFP"]+res["HSYNC"]+res["HBP"]))

        # Timings table
        self.tree_gen.delete(*self.tree_gen.get_children())
        for row in [
            ("H active",      res["X1"],    f"{t['H_actif_us']:.3f}", "µs"),
            ("H Front Porch", res["HFP"],   f"{t['HFP_us']:.3f}",     "µs"),
            ("H Sync",        res["HSYNC"], f"{t['HSYNC_us']:.3f}",   "µs"),
            ("H Back Porch",  res["HBP"],   f"{t['HBP_us']:.3f}",     "µs"),
            ("H total",       res["X4"],    f"{t['H_total_us']:.3f}", "µs"),
            ("—", "", "", ""),
            ("V active",      res["Y1"],    f"{t['V_actif_ms']:.3f}", "ms"),
            ("V Front Porch", res["VFP"],   f"{t['VFP_ms']:.3f}",     "ms"),
            ("V Sync",        res["VSYNC"], f"{t['VSYNC_ms']:.3f}",   "ms"),
            ("V Back Porch",  res["VBP"],   f"{t['VBP_ms']:.3f}",     "ms"),
            ("V total",       res["Y4"],    f"{t['V_total_ms']:.3f}", "ms"),
        ]:
            self.tree_gen.insert("", "end", values=row)

        hok=r_live["hmin"]<=round(Hf)<=r_live["hmax"]
        vok=r_live["vfmin"]<=round(res["Vfreq_actual"],2)<=r_live["vfmax"]
        if i:
            lok=r_live["iLmin"]<=V<=r_live["iLmax"] if r_live["iLmax"]>0 else False
            lstr=f"[{r_live['iLmin']}–{r_live['iLmax']}] interlaced"
        else:
            lok=r_live["pLmin"]<=V<=r_live["pLmax"]
            lstr=f"[{r_live['pLmin']}–{r_live['pLmax']}] progressive"
        self.lbl_chk_h.config(
            text=f"{'✓' if hok else '✗'}  Hfreq {Hf/1000:.3f} kHz ∈ [{r_live['hmin']}–{r_live['hmax']}] Hz",
            fg=GREEN if hok else RED)
        self.lbl_chk_v.config(
            text=f"{'✓' if vok else '✗'}  Vfreq {res['Vfreq_actual']:.3f} Hz ∈ [{r_live['vfmin']}–{r_live['vfmax']}] Hz",
            fg=GREEN if vok else RED)
        self.lbl_chk_l.config(
            text=f"{'✓' if lok else '✗'}  V={V} ∈ {lstr}",
            fg=GREEN if lok else RED)

        self._set_text(self.txt_crt_calc,
                       fmt_crt_range(r_live,t["HFP_us"],t["HSYNC_us"],t["HBP_us"],
                                     t["VFP_ms"],t["VSYNC_ms"],t["VBP_ms"]))
        istr=" interlace" if i else ""
        H=res["X1"]; auto_name=f"{H}x{V}{'i' if i else ''}"
        custom=self.e_name.get().strip()
        name=custom if custom else auto_name
        ml=(f"{res['pclk']:.6f} {res['X1']} {res['X2']} {res['X3']} {res['X4']} "
            f"{res['Y1']} {res['Y2']} {res['Y3']} {res['Y4']}{istr} -hsync -vsync")
        self._set_text(self.txt_modeline, f'Modeline "{name}" {ml}')
        self._set_text(self.txt_xrandr,
                       f'xrandr --display :0.0 --newmode "{name}" {ml}\n'
                       f'xrandr --display :0.0 --addmode {out} "{name}"\n'
                       f'xrandr --display :0.0 --output {out} --mode "{name}"')

    def _calc_ver(self):
        raw=self.e_modeline_in.get().strip()
        res=verify_modeline(raw)
        if not res:
            messagebox.showerror("Error","Invalid modeline"); return
        name=self.cmb_preset_v.get()
        r=select_range(name, res["Hfreq"])
        self.lbl_range_v.config(text=f"→ {r['lb']}")
        t=calc_timings(res)
        for attr,val in [("lbl_v_pclk",f"{res['pclk']:.4f} MHz"),
                          ("lbl_v_hfreq",f"{res['Hfreq']/1000:.6f}"),
                          ("lbl_v_vfreq",f"{res['Vfreq_actual']:.6f}"),
                          ("lbl_v_htot",str(res["X4"])),
                          ("lbl_v_vtot",str(res["Y4"])),
                          ("lbl_v_mode","Interlaced" if res["interlaced"] else "Progressive")]:
            getattr(self,attr).config(text=val)
        hok=r["hmin"]<=round(res["Hfreq"])<=r["hmax"]
        vok=r["vfmin"]<=round(res["Vfreq_actual"],2)<=r["vfmax"]
        V=res["Y1"]; i=res["interlaced"]
        if i:
            lok=r["iLmin"]<=V<=r["iLmax"] if r["iLmax"]>0 else False
            lstr=f"[{r['iLmin']}–{r['iLmax']}] interlaced"
        else:
            lok=r["pLmin"]<=V<=r["pLmax"]
            lstr=f"[{r['pLmin']}–{r['pLmax']}] progressive"
        self.lbl_v_chk_h.config(
            text=f"{'✓' if hok else '✗'}  Hfreq {res['Hfreq']/1000:.3f} kHz ∈ [{r['hmin']}–{r['hmax']}] Hz",
            fg=GREEN if hok else RED)
        self.lbl_v_chk_v.config(
            text=f"{'✓' if vok else '✗'}  Vfreq {res['Vfreq_actual']:.3f} Hz ∈ [{r['vfmin']}–{r['vfmax']}] Hz",
            fg=GREEN if vok else RED)
        self.lbl_v_chk_l.config(
            text=f"{'✓' if lok else '✗'}  V={V} ∈ {lstr}",
            fg=GREEN if lok else RED)
        self._set_text(self.txt_v_crt_calc,
                       fmt_crt_range(r,t["HFP_us"],t["HSYNC_us"],t["HBP_us"],
                                     t["VFP_ms"],t["VSYNC_ms"],t["VBP_ms"]))
        istr=" interlace" if res["interlaced"] else ""
        ml_name=f"{res['X1']}x{res['Y1']}{'i' if res['interlaced'] else ''}"
        ml=(f"{res['pclk']} {res['X1']} {res['X2']} {res['X3']} {res['X4']} "
            f"{res['Y1']} {res['Y2']} {res['Y3']} {res['Y4']}{istr} -hsync -vsync")
        out=self.e_output_v.get() or "DP-1"
        self._set_text(self.txt_v_xrandr,
                       f'xrandr --display :0.0 --newmode "{ml_name}" {ml}\n'
                       f'xrandr --display :0.0 --addmode {out} "{ml_name}"\n'
                       f'xrandr --display :0.0 --output {out} --mode "{ml_name}"')

    def _optimise_ls(self):
        try:
            H=self.sw_width.get_value(); V=self.sw_height.get_value()
            Hf=self.sw_hfreq.get_value()*1000; Vf=self.sw_vfreq.get_value()
            i=self.var_interlaced.get()
            r=self._current_range or PRESETS["Arcade 15kHz"]["ranges"][0]
            r_live={"hfp":self.sw_hfp.get_value(),"hs":self.sw_hs.get_value(),
                    "hbp":self.sw_hbp.get_value(),"vfp":self.sw_vfp.get_value(),
                    "vs":self.sw_vs.get_value(),"vbp":self.sw_vbp.get_value(),
                    **{k:r[k] for k in ("hmin","hmax","vfmin","vfmax","pLmin","pLmax","iLmin","iLmax")}}
        except Exception: return
        res=optimize_modeline(H,V,Hf,Vf,i,r_live)
        # VFP lock
        if self.var_vfp_lock.get():
            try: vfp_target=int(self.spn_vfp_lock.get())
            except ValueError: vfp_target=None
            if vfp_target and vfp_target!=res["VFP"]:
                diff=res["VFP"]-vfp_target
                new_vfp=vfp_target; new_vbp=res["VBP"]+diff
                if new_vbp>=1 and new_vfp>=1:
                    res["VFP"]=new_vfp; res["VBP"]=new_vbp
                    res["Y2"]=res["Y1"]+new_vfp
                    res["Y3"]=res["Y2"]+res["VSYNC"]
                    res["Y4"]=res["Y3"]+new_vbp
                    Div_r=2 if i else 1
                    line_ms=1000.0/(res["Hfreq"]*Div_r)
                    thr_ms=22500.0/r_live["hmax"]
                    vb_ms=(new_vfp+res["VSYNC"]+new_vbp)*line_ms
                    res["switchres_ok"]=vb_ms<thr_ms
                    res["vblank_ms"]=vb_ms; res["threshold_ms"]=thr_ms
        t=calc_timings(res)
        self.sw_hfp.set_value(round(t["HFP_us"],3)); self.sw_hs.set_value(round(t["HSYNC_us"],3))
        self.sw_hbp.set_value(round(t["HBP_us"],3)); self.sw_vfp.set_value(round(t["VFP_ms"],3))
        self.sw_vs.set_value(round(t["VSYNC_ms"],3)); self.sw_vbp.set_value(round(t["VBP_ms"],3))
        self.sw_hfp_px.set_value(res["HFP"]); self.sw_hs_px.set_value(res["HSYNC"])
        self.sw_hbp_px.set_value(res["HBP"]); self.sw_vfp_px.set_value(res["VFP"])
        self.sw_vs_px.set_value(res["VSYNC"]); self.sw_vbp_px.set_value(res["VBP"])
        ve=res["Vfreq_error"]
        sr_ok=res.get("switchres_ok",True)
        vb_ms=res.get("vblank_ms",0); thr_ms=res.get("threshold_ms",0)
        sr_txt=f"  SR:{vb_ms:.3f}/{thr_ms:.3f}{'✓' if sr_ok else '✗'}"
        self.lbl_ls_error.config(
            text=f"Vfreq:{ve:.6f}{'✓' if ve<1e-6 else ''}{sr_txt}",
            fg=GREEN if (ve<1e-6 and sr_ok) else YELLOW)
        self._refresh_display(res, r_live)

    def _copy_xrandr(self):
        self.txt_xrandr.config(state="normal")
        t=self.txt_xrandr.get("1.0","end").strip()
        self.txt_xrandr.config(state="disabled")
        self.clipboard_clear(); self.clipboard_append(t)

    def _apply_xrandr(self):
        self.txt_xrandr.config(state="normal")
        text=self.txt_xrandr.get("1.0","end").strip()
        self.txt_xrandr.config(state="disabled")
        for cmd in [l for l in text.split("\n") if l.strip()]:
            try: subprocess.run(cmd.split(), check=True)
            except Exception as e:
                messagebox.showerror("xrandr error",str(e)); return
        messagebox.showinfo("xrandr","Modeline applied successfully.")

    def _import_modeline(self):
        raw = self.e_import.get().strip()
        raw = re.sub(r'^[Mm]odeline\s+"[^"]*"\s*', '', raw).strip()
        parts = raw.split()
        if len(parts) < 9:
            messagebox.showerror("Import", "Expected: pclk X1 X2 X3 X4 Y1 Y2 Y3 Y4 [interlace]")
            return
        try:
            pclk=float(parts[0])
            X1,X2,X3,X4=int(parts[1]),int(parts[2]),int(parts[3]),int(parts[4])
            Y1,Y2,Y3,Y4=int(parts[5]),int(parts[6]),int(parts[7]),int(parts[8])
        except ValueError as e:
            messagebox.showerror("Import", str(e)); return
        interlaced="interlace" in raw.lower(); Div=2 if interlaced else 1
        Hf=pclk*1e6/X4; Vf=Hf*Div/Y4
        HFP=X2-X1; HSYNC=X3-X2; HBP=X4-X3
        VFP=Y2-Y1; VSYNC=Y3-Y2; VBP=Y4-Y3
        self.sw_width.set_value(X1); self.sw_height.set_value(Y1)
        self.sw_hfreq.set_value(round(Hf/1000,3)); self.sw_vfreq.set_value(round(Vf,3))
        self.var_interlaced.set(1 if interlaced else 0)
        self.sw_hfp_px.set_value(HFP); self.sw_hs_px.set_value(HSYNC)
        self.sw_hbp_px.set_value(HBP); self.sw_vfp_px.set_value(VFP)
        self.sw_vs_px.set_value(VSYNC); self.sw_vbp_px.set_value(VBP)
        r=self._current_range or PRESETS["Arcade 15kHz"]["ranges"][0]
        res=dict(X1=X1,X2=X2,X3=X3,X4=X4,Y1=Y1,Y2=Y2,Y3=Y3,Y4=Y4,
                 HFP=HFP,HSYNC=HSYNC,HBP=HBP,VFP=VFP,VSYNC=VSYNC,VBP=VBP,
                 pclk=pclk,Hfreq=Hf,Vfreq_actual=Vf,interlaced=interlaced)
        t=calc_timings(res)
        self.sw_hfp.set_value(round(t["HFP_us"],3)); self.sw_hs.set_value(round(t["HSYNC_us"],3))
        self.sw_hbp.set_value(round(t["HBP_us"],3)); self.sw_vfp.set_value(round(t["VFP_ms"],3))
        self.sw_vs.set_value(round(t["VSYNC_ms"],3)); self.sw_vbp.set_value(round(t["VBP_ms"],3))
        r_live={"hfp":t["HFP_us"],"hs":t["HSYNC_us"],"hbp":t["HBP_us"],
                "vfp":t["VFP_ms"],"vs":t["VSYNC_ms"],"vbp":t["VBP_ms"],
                **{k:r[k] for k in ("hmin","hmax","vfmin","vfmax","pLmin","pLmax","iLmin","iLmax")}}
        self._refresh_display(res, r_live)

    def _save_modeline(self):
        if not self._last_res:
            messagebox.showwarning("Save", "Generate a modeline first."); return
        res=self._last_res; i=res["interlaced"]
        H=res["X1"]; V=res["Y1"]; istr=" interlace" if i else ""
        auto=f"{H}x{V}{'i' if i else ''}"
        name=self.e_name.get().strip() or auto
        out=self.e_output.get().strip() or "DP-1"
        ml=(f"{res['pclk']:.6f} {res['X1']} {res['X2']} {res['X3']} {res['X4']} "
            f"{res['Y1']} {res['Y2']} {res['Y3']} {res['Y4']}{istr} -hsync -vsync")
        content=(f"# Modeline: {name}\n"
                 f"Modeline \"{name}\" {ml}\n"
                 f"xrandr --display :0.0 --newmode \"{name}\" {ml}\n"
                 f"xrandr --display :0.0 --addmode {out} \"{name}\"\n"
                 f"xrandr --display :0.0 --output {out} --mode \"{name}\"\n")
        fp=filedialog.asksaveasfilename(title="Save Modeline",defaultextension=".modeline",
            filetypes=[("Modeline","*.modeline"),("Text","*.txt"),("All","*.*")],
            initialfile=f"{name}.modeline")
        if not fp: return
        try:
            with open(fp,"w",encoding="utf-8") as f: f.write(content)
            messagebox.showinfo("Saved",f"Saved: {fp}")
        except Exception as e: messagebox.showerror("Error",str(e))

    def _load_modeline(self):
        fp=filedialog.askopenfilename(title="Load Modeline",
            filetypes=[("Modeline","*.modeline"),("Text","*.txt"),("All","*.*")])
        if not fp: return
        try:
            lines=open(fp,"r",encoding="utf-8").readlines()
        except Exception as e: messagebox.showerror("Error",str(e)); return
        for line in lines:
            s=line.strip()
            if s.startswith("Modeline"):
                m=re.match(r'Modeline\s+"([^"]+)"\s+(.*)',s)
                if m:
                    self.e_import.delete(0,"end")
                    self.e_import.insert(0,m.group(2))
                    self.e_name.delete(0,"end")
                    self.e_name.insert(0,m.group(1))
                    self._import_modeline(); return
        messagebox.showerror("Error","No Modeline line found.")

    def _save_crt_range(self):
        self.txt_crt_calc.config(state="normal")
        crt_calc=self.txt_crt_calc.get("1.0","end").strip()
        self.txt_crt_calc.config(state="disabled")
        if not crt_calc:
            messagebox.showwarning("Nothing to save","Generate a modeline first."); return
        self.txt_crt_fixed.config(state="normal")
        crt_fixed=self.txt_crt_fixed.get("1.0","end").strip()
        self.txt_crt_fixed.config(state="disabled")
        self.txt_modeline.config(state="normal")
        modeline=self.txt_modeline.get("1.0","end").strip()
        self.txt_modeline.config(state="disabled")
        self.txt_xrandr.config(state="normal")
        xrandr=self.txt_xrandr.get("1.0","end").strip()
        self.txt_xrandr.config(state="disabled")
        filepath=filedialog.asksaveasfilename(
            title="Save CRT Range",defaultextension=".txt",
            filetypes=[("Text files","*.txt"),("All files","*.*")],
            initialfile="my_crt_range.txt")
        if not filepath: return
        content=(f"# CRT Modeline Toolbox — ZFEbHVUE\n"
                 f"# Monitor  : {self.cmb_preset.get()}  [{self.cmb_range.get()}]\n\n"
                 f"# --- Calamity preset ---\n{crt_fixed}\n\n"
                 f"# --- Calculated from modeline ---\n{crt_calc}\n\n"
                 f"# --- Modeline ---\n{modeline}\n\n"
                 f"# --- xrandr ---\n{xrandr}\n")
        try:
            with open(filepath,"w",encoding="utf-8") as f: f.write(content)
            messagebox.showinfo("Saved",f"Saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Save error",str(e))

    def _load_crt_range(self):
        filepath=filedialog.askopenfilename(
            title="Load CRT Range",
            filetypes=[("Text files","*.txt"),("All files","*.*")])
        if not filepath: return
        try:
            with open(filepath,"r",encoding="utf-8") as f: lines=f.readlines()
        except Exception as e:
            messagebox.showerror("Load error",str(e)); return
        crt_line=None; after_calc=False
        for line in lines:
            s=line.strip()
            if "Calculated from" in s: after_calc=True; continue
            if s.startswith("crt_range"):
                crt_line=s
                if after_calc: break
        if not crt_line:
            messagebox.showerror("Load error","No crt_range line found."); return
        self.e_crt_paste.delete(0,"end")
        self.e_crt_paste.insert(0,crt_line)
        self._parse_crt_range()

    def _show_diagram(self):
        res=self._last_res
        if not res:
            messagebox.showwarning("Diagram","Generate a modeline first."); return
        H_total=res["X4"]; V_total=res["Y4"]
        H=res["X1"]; V=res["Y1"]
        HBP=res["HBP"]; HFP=res["HFP"]; HSYNC=res["HSYNC"]
        VBP=res["VBP"]; VFP=res["VFP"]; VSYNC=res["VSYNC"]
        interlaced=res["interlaced"]
        t=calc_timings(res)
        C_ACT="#43a047"; C_HBP="#0d47a1"; C_HFP="#1976d2"; C_HSYNC="#90caf9"
        C_VBP="#b71c1c"; C_VFP="#e53935"; C_VSYNC="#ef9a9a"
        top=tk.Toplevel(self)
        top.title(f"Diagram {H}x{V}{'i' if interlaced else ''}")
        top.configure(bg=BG); top.resizable(True,True)
        tk.Label(top,
                 text=f"H:{H_total}px/{t['H_total_us']:.2f}µs  V:{V_total}px/{t['V_total_ms']:.2f}ms  {'Interlaced' if interlaced else 'Progressive'}",
                 bg=BG,fg=YELLOW,font=("Monospace",7)).pack(side="bottom",pady=(0,4))
        CW,CH=560,380
        sx=CW/H_total; sy=CH/V_total
        x_act=round(HBP*sx); x_hfp=round((HBP+H)*sx); x_sync=round((HBP+H+HFP)*sx)
        y_act=round(VBP*sy); y_vfp=round((VBP+V)*sy)

        # Minimum 4px for V Front Porch and V Sync zones
        MIN = 4
        vfp_h   = max(round(VFP*sy), MIN)
        vsync_h = max(round(VSYNC*sy), MIN)
        y_sync  = min(y_vfp + vfp_h, CH - vsync_h)
        y_send  = CH   # end always at canvas bottom
        cv=tk.Canvas(top,width=CW,height=CH,bg="#111122",highlightthickness=0)
        cv.pack(padx=6,pady=6)
        def rect(x0,y0,x1,y1,fill):
            cv.create_rectangle(x0,y0,x1,y1,fill=fill,outline="#222233",width=1)
        def clbl(x,y,txt,col="#fff",sz=7,bold=False,anchor="center"):
            cv.create_text(x,y,text=txt,fill=col,
                           font=("Sans",sz,"bold" if bold else "normal"),
                           justify="left",anchor=anchor)
        def dot(x,y,col):
            cv.create_rectangle(x,y,x+8,y+8,fill=col,outline="")
        rect(0,0,CW,y_act,C_VBP)
        rect(x_act,y_act,x_hfp,y_vfp,C_ACT)
        rect(0,y_act,x_act,CH,C_HBP)
        rect(x_hfp,y_act,x_sync,CH,C_HFP)
        rect(x_sync,y_act,CW,CH,C_HSYNC)
        rect(x_act,y_vfp,x_hfp,y_sync,C_VFP)
        rect(x_act,y_sync,x_hfp,CH,C_VSYNC)
        cx=(x_act+x_hfp)//2; cy=(y_act+y_vfp)//2
        # Labels on small zones
        clbl(cx,y_act//2,f"V Back Porch  {VBP}px / {t['VBP_ms']:.3f}ms","#fff",7)
        if x_act>20: clbl(x_act//2,(y_act+CH)//2,f"HBP\n{HBP}px\n{t['HBP_us']:.2f}µs","#fff",7)
        if x_sync-x_hfp>22: clbl((x_hfp+x_sync)//2,(y_act+CH)//2,f"HFP\n{HFP}px","#fff",7)
        if CW-x_sync>16: clbl((x_sync+CW)//2,(y_act+CH)//2,f"HS\n{HSYNC}","#222",7)
        if y_sync-y_vfp>10: clbl(cx,(y_vfp+y_sync)//2,f"VFP {VFP}px","#fff",7)
        if CH-y_sync>8: clbl(cx,(y_sync+CH)//2,f"VS {VSYNC}px","#333",7)
        clbl(cx, y_act + 22, f"Active  {H} × {V}", "#ffffff", 16, True)
        clbl(cx, y_act + 42, f"pclk {res['pclk']:.3f} MHz    Hfreq {res['Hfreq']/1000:.3f} kHz    Vfreq {res['Vfreq_actual']:.3f} Hz", "#000000", 10)

        # Two columns — dot + left-aligned text
        lx_h  = cx - 200
        lx_v  = cx + 10
        ly    = cy - 38
        dy    = 19

        X_DOT  =   0
        X_LBL  =  14
        X_NUM  = 100
        X_TIME = 106

        clbl(lx_h + X_LBL, ly - 14, "── Horizontal ──", "#ffffff", 9, True, anchor="w")
        clbl(lx_v + X_LBL, ly - 14, "── Vertical ──",   "#ffffff", 9, True, anchor="w")

        h_rows = [
            (C_ACT,   "H active", f"{H}",       f"{t['H_actif_us']:.2f}µs"),
            (C_HBP,   "H Back",   f"{HBP}",     f"{t['HBP_us']:.2f}µs"),
            (C_HFP,   "H Front",  f"{HFP}",     f"{t['HFP_us']:.2f}µs"),
            (C_HSYNC, "H Sync",   f"{HSYNC}",   f"{t['HSYNC_us']:.2f}µs"),
            (YELLOW,  "H total",  f"{H_total}", f"{t['H_total_us']:.2f}µs"),
        ]
        v_rows = [
            (C_ACT,   "V active", f"{V}",       f"{t['V_actif_ms']:.2f}ms"),
            (C_VBP,   "V Back",   f"{VBP}",     f"{t['VBP_ms']:.2f}ms"),
            (C_VFP,   "V Front",  f"{VFP}",     f"{t['VFP_ms']:.2f}ms"),
            (C_VSYNC, "V Sync",   f"{VSYNC}",   f"{t['VSYNC_ms']:.2f}ms"),
            (YELLOW,  "V total",  f"{V_total}", f"{t['V_total_ms']:.2f}ms"),
        ]

        for i, (col, lbl, num, tim) in enumerate(h_rows):
            y = ly + i * dy
            dot(lx_h + X_DOT, y - 5, col)
            clbl(lx_h + X_LBL,  y, lbl, "#fff", 9, anchor="w")
            clbl(lx_h + X_NUM,  y, f"{num}px", "#fff", 9, anchor="e")
            clbl(lx_h + X_TIME, y, tim, "#ddd", 9, anchor="w")

        for i, (col, lbl, num, tim) in enumerate(v_rows):
            y = ly + i * dy
            dot(lx_v + X_DOT, y - 5, col)
            clbl(lx_v + X_LBL,  y, lbl, "#fff", 9, anchor="w")
            clbl(lx_v + X_NUM,  y, f"{num}px", "#fff", 9, anchor="e")
            clbl(lx_v + X_TIME, y, tim, "#ddd", 9, anchor="w")


if __name__ == "__main__":
    App().mainloop()
