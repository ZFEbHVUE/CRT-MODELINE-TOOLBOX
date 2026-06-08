#!/usr/bin/env python3
# ==============================================================================
# CRT MODELINE TOOLBOX — BATOCERA / PYGAME VERSION
# Stéphane "ZFEbHVUE" — v2.5
# 640×480 — no Tkinter needed, only pygame
# Usage: DISPLAY=:0 python3 crt_modeline_batocera.py
# ==============================================================================
import pygame, sys, math, os, re, subprocess

# ── Colours ────────────────────────────────────────────────────────────────────
BG      = (30, 30, 46)
BG2     = (42, 42, 62)
BG3     = (49, 49, 69)
FG      = (205, 214, 244)
FG2     = (166, 173, 200)
ACCENT  = (137, 180, 250)
GREEN_C = (166, 227, 161)
RED_C   = (243, 139, 168)
YELLOW  = (249, 226, 175)
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
C_ACT   = (67, 160, 71)
C_HBP   = (13, 71, 161)
C_HFP   = (25, 118, 210)
C_HSYNC = (144, 202, 249)
C_VBP   = (183, 28, 28)
C_VFP   = (229, 57, 53)
C_VSYNC = (239, 154, 154)

# ══════════════════════════════════════════════════════════════════════════════
# MONITOR PRESETS (Calamity/SwitchRes)
# ══════════════════════════════════════════════════════════════════════════════
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
            {"lb": "18KHz", "hmin": 18001, "hmax": 19000, "vfmin": 40, "vfmax": 80,
             "hfp": 2.187, "hs": 4.688, "hbp": 6.719, "vfp": 0.140, "vs": 0.191, "vbp": 0.950,
             "pLmin": 288, "pLmax": 320, "iLmin": 0, "iLmax": 0},
            {"lb": "25KHz", "hmin": 20501, "hmax": 29000, "vfmin": 40, "vfmax": 80,
             "hfp": 2.910, "hs": 3.000, "hbp": 4.440, "vfp": 0.451, "vs": 0.164, "vbp": 1.048,
             "pLmin": 320, "pLmax": 384, "iLmin": 0, "iLmax": 0},
            {"lb": "31KHz", "hmin": 29001, "hmax": 32000, "vfmin": 40, "vfmax": 80,
             "hfp": 0.636, "hs": 3.813, "hbp": 1.906, "vfp": 0.318, "vs": 0.064, "vbp": 1.048,
             "pLmin": 384, "pLmax": 480, "iLmin": 0, "iLmax": 0},
            {"lb": "33KHz", "hmin": 32001, "hmax": 34000, "vfmin": 40, "vfmax": 80,
             "hfp": 0.636, "hs": 3.813, "hbp": 1.906, "vfp": 0.020, "vs": 0.106, "vbp": 0.607,
             "pLmin": 480, "pLmax": 576, "iLmin": 0, "iLmax": 0},
            {"lb": "36KHz", "hmin": 34001, "hmax": 38000, "vfmin": 40, "vfmax": 80,
             "hfp": 1.000, "hs": 3.200, "hbp": 2.200, "vfp": 0.020, "vs": 0.106, "vbp": 0.607,
             "pLmin": 576, "pLmax": 600, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Wells Gardner D9200": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15250, "hmax": 16500, "vfmin": 40, "vfmax": 80,
             "hfp": 2.187, "hs": 4.688, "hbp": 6.719, "vfp": 0.190, "vs": 0.191, "vbp": 1.018,
             "pLmin": 224, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "24KHz", "hmin": 23900, "hmax": 24420, "vfmin": 40, "vfmax": 80,
             "hfp": 2.910, "hs": 3.000, "hbp": 4.440, "vfp": 0.451, "vs": 0.164, "vbp": 1.148,
             "pLmin": 384, "pLmax": 400, "iLmin": 0, "iLmax": 0},
            {"lb": "31KHz", "hmin": 31000, "hmax": 32000, "vfmin": 40, "vfmax": 80,
             "hfp": 0.636, "hs": 3.813, "hbp": 1.906, "vfp": 0.318, "vs": 0.064, "vbp": 1.048,
             "pLmin": 400, "pLmax": 512, "iLmin": 0, "iLmax": 0},
            {"lb": "37KHz", "hmin": 37000, "hmax": 38000, "vfmin": 40, "vfmax": 80,
             "hfp": 1.000, "hs": 3.200, "hbp": 2.200, "vfp": 0.020, "vs": 0.106, "vbp": 0.607,
             "pLmin": 512, "pLmax": 600, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Wells Gardner K7000": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 15800, "vfmin": 49.5, "vfmax": 63.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.160, "vbp": 1.056,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Wells Gardner 25K7131": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 16670, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.160, "vbp": 1.056,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Nanao MS-2930/2931": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15450, "hmax": 16050, "vfmin": 50, "vfmax": 65,
             "hfp": 3.190, "hs": 4.750, "hbp": 6.450, "vfp": 0.191, "vs": 0.191, "vbp": 1.164,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "24KHz", "hmin": 23900, "hmax": 24900, "vfmin": 50, "vfmax": 65,
             "hfp": 2.870, "hs": 3.000, "hbp": 4.440, "vfp": 0.451, "vs": 0.164, "vbp": 1.148,
             "pLmin": 384, "pLmax": 400, "iLmin": 0, "iLmax": 0},
            {"lb": "31KHz", "hmin": 31000, "hmax": 32000, "vfmin": 50, "vfmax": 65,
             "hfp": 0.330, "hs": 3.580, "hbp": 1.750, "vfp": 0.316, "vs": 0.063, "vbp": 1.137,
             "pLmin": 480, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Nanao MS9-29": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15450, "hmax": 16050, "vfmin": 50, "vfmax": 65,
             "hfp": 3.910, "hs": 4.700, "hbp": 6.850, "vfp": 0.190, "vs": 0.191, "vbp": 1.018,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "24KHz", "hmin": 23900, "hmax": 24900, "vfmin": 50, "vfmax": 65,
             "hfp": 2.910, "hs": 3.000, "hbp": 4.440, "vfp": 0.451, "vs": 0.164, "vbp": 1.048,
             "pLmin": 384, "pLmax": 400, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Hantarex MTC 9110 / Polo": {
        "ranges": [{"lb": "15KHz", "hmin": 15625, "hmax": 16670, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 2.000, "hs": 4.700, "hbp": 8.000, "vfp": 0.064, "vs": 0.160, "vbp": 1.056,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.69, "dV": 60.0
    },
    "Hantarex Polostar 25": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15700, "hmax": 15800, "vfmin": 50, "vfmax": 65,
             "hfp": 1.800, "hs": 0.400, "hbp": 7.400, "vfp": 0.064, "vs": 0.160, "vbp": 1.056,
             "pLmin": 192, "pLmax": 256, "iLmin": 0, "iLmax": 0},
            {"lb": "16KHz", "hmin": 16200, "hmax": 16300, "vfmin": 50, "vfmax": 65,
             "hfp": 0.200, "hs": 0.400, "hbp": 8.000, "vfp": 0.040, "vs": 0.040, "vbp": 0.640,
             "pLmin": 256, "pLmax": 264, "iLmin": 512, "iLmax": 528},
            {"lb": "25KHz", "hmin": 25300, "hmax": 25400, "vfmin": 50, "vfmax": 65,
             "hfp": 0.200, "hs": 0.400, "hbp": 8.000, "vfp": 0.040, "vs": 0.040, "vbp": 0.640,
             "pLmin": 384, "pLmax": 400, "iLmin": 768, "iLmax": 800},
            {"lb": "31KHz", "hmin": 31500, "hmax": 31600, "vfmin": 50, "vfmax": 65,
             "hfp": 0.170, "hs": 0.350, "hbp": 5.500, "vfp": 0.040, "vs": 0.040, "vbp": 0.640,
             "pLmin": 400, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 15.75, "dV": 60.0
    },
    "Makvision 2929D": {
        "ranges": [{"lb": "31KHz", "hmin": 30000, "hmax": 40000, "vfmin": 47, "vfmax": 90,
                    "hfp": 0.600, "hs": 2.500, "hbp": 2.800, "vfp": 0.032, "vs": 0.096, "vbp": 0.448,
                    "pLmin": 384, "pLmax": 640, "iLmin": 0, "iLmax": 0}],
        "dH": 35.0, "dV": 60.0
    },
    "Wei-Ya M3129": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15250, "hmax": 16500, "vfmin": 40, "vfmax": 80,
             "hfp": 2.187, "hs": 4.688, "hbp": 6.719, "vfp": 0.190, "vs": 0.191, "vbp": 1.018,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "24KHz", "hmin": 23900, "hmax": 24420, "vfmin": 40, "vfmax": 80,
             "hfp": 2.910, "hs": 3.000, "hbp": 4.440, "vfp": 0.451, "vs": 0.164, "vbp": 1.048,
             "pLmin": 384, "pLmax": 400, "iLmin": 0, "iLmax": 0},
            {"lb": "31KHz", "hmin": 31000, "hmax": 32000, "vfmin": 40, "vfmax": 80,
             "hfp": 0.636, "hs": 3.813, "hbp": 1.906, "vfp": 0.318, "vs": 0.064, "vbp": 1.048,
             "pLmin": 400, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "Rodotron 666B-29": {
        "ranges": [
            {"lb": "15KHz", "hmin": 15450, "hmax": 16050, "vfmin": 50, "vfmax": 65,
             "hfp": 3.190, "hs": 4.750, "hbp": 6.450, "vfp": 0.191, "vs": 0.191, "vbp": 1.164,
             "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576},
            {"lb": "24KHz", "hmin": 23900, "hmax": 24900, "vfmin": 50, "vfmax": 65,
             "hfp": 2.870, "hs": 3.000, "hbp": 4.440, "vfp": 0.451, "vs": 0.164, "vbp": 1.148,
             "pLmin": 384, "pLmax": 400, "iLmin": 0, "iLmax": 0},
            {"lb": "31KHz", "hmin": 31000, "hmax": 32500, "vfmin": 50, "vfmax": 65,
             "hfp": 0.330, "hs": 3.580, "hbp": 1.750, "vfp": 0.316, "vs": 0.063, "vbp": 1.137,
             "pLmin": 400, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 15.69, "dV": 60.0
    },
    "PC CRT 31kHz/120Hz": {
        "ranges": [
            {"lb": "31KHz/120Hz", "hmin": 31400, "hmax": 31600, "vfmin": 100, "vfmax": 130,
             "hfp": 0.671, "hs": 2.683, "hbp": 3.353, "vfp": 0.034, "vs": 0.101, "vbp": 0.436,
             "pLmin": 200, "pLmax": 256, "iLmin": 0, "iLmax": 0},
            {"lb": "31KHz/60Hz", "hmin": 31400, "hmax": 31600, "vfmin": 50, "vfmax": 65,
             "hfp": 0.671, "hs": 2.683, "hbp": 3.353, "vfp": 0.034, "vs": 0.101, "vbp": 0.436,
             "pLmin": 400, "pLmax": 512, "iLmin": 0, "iLmax": 0}],
        "dH": 31.45, "dV": 60.0
    },
    "PC CRT 70kHz/120Hz": {
        "ranges": [
            {"lb": "70KHz/120Hz", "hmin": 30000, "hmax": 70000, "vfmin": 100, "vfmax": 130,
             "hfp": 2.201, "hs": 0.275, "hbp": 4.678, "vfp": 0.063, "vs": 0.032, "vbp": 0.633,
             "pLmin": 192, "pLmax": 320, "iLmin": 0, "iLmax": 0},
            {"lb": "70KHz/60Hz", "hmin": 30000, "hmax": 70000, "vfmin": 50, "vfmax": 65,
             "hfp": 2.201, "hs": 0.275, "hbp": 4.678, "vfp": 0.063, "vs": 0.032, "vbp": 0.633,
             "pLmin": 400, "pLmax": 1024, "iLmin": 0, "iLmax": 0}],
        "dH": 60.0, "dV": 60.0
    },
    "DP custom (ZFEbHVUE)": {
        "ranges": [{"lb": "15KHz PAL", "hmin": 15625, "hmax": 15750, "vfmin": 49.5, "vfmax": 65.0,
                    "hfp": 1.990, "hs": 4.686, "hbp": 8.024, "vfp": 0.064, "vs": 0.480, "vbp": 1.024,
                    "pLmin": 192, "pLmax": 288, "iLmin": 448, "iLmax": 576}],
        "dH": 15.625, "dV": 50.0
    },
}
PRESET_NAMES = list(PRESETS.keys())

# ══════════════════════════════════════════════════════════════════════════════
# CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════
def _safe_round(f):
    import math
    frac = f % 1
    return math.ceil(f) if 0.4 <= frac <= 0.6 else round(f)

def verify_modeline(s):
    """Parse a raw XFree86 modeline string into a result dict."""
    parts = s.strip().split()
    if len(parts) < 9: return None
    try:
        pclk=float(parts[0])
        X1,X2,X3,X4=int(parts[1]),int(parts[2]),int(parts[3]),int(parts[4])
        Y1,Y2,Y3,Y4=int(parts[5]),int(parts[6]),int(parts[7]),int(parts[8])
    except ValueError: return None
    interlaced="interlace" in s.lower()
    Div=2 if interlaced else 1
    Hfreq=pclk*1e6/X4; Vfreq=Hfreq*Div/Y4
    return dict(X1=X1,X2=X2,X3=X3,X4=X4,Y1=Y1,Y2=Y2,Y3=Y3,Y4=Y4,
                HFP=X2-X1,HSYNC=X3-X2,HBP=X4-X3,VFP=Y2-Y1,VSYNC=Y3-Y2,VBP=Y4-Y3,
                pclk=pclk,Hfreq=Hfreq,Vfreq_actual=Vfreq,interlaced=interlaced)

def select_range(preset_name, hfreq_hz):
    p = PRESETS.get(preset_name)
    if not p: return PRESETS["Arcade 15kHz"]["ranges"][0]
    for r in p["ranges"]:
        if r["hmin"] <= hfreq_hz <= r["hmax"]: return r
    return p["ranges"][0]

def get_screen_resolution():
    """Get current resolution via batocera-resolution."""
    import re
    try:
        out=subprocess.check_output(
            ["batocera-resolution","currentMode"],
            env={**os.environ,"DISPLAY":os.environ.get("DISPLAY",":0.0")},
            stderr=subprocess.DEVNULL).decode().strip()
        # Format: 769x576.50.00
        m=re.match(r'(\d+)x(\d+)',out)
        if m: return int(m.group(1)),int(m.group(2))
    except: pass
    try:
        out=subprocess.check_output(
            ["xrandr","--display",os.environ.get("DISPLAY",":0.0")],
            stderr=subprocess.DEVNULL).decode()
        m=re.search(r'current (\d+) x (\d+)',out)
        if m: return int(m.group(1)),int(m.group(2))
    except: pass
    return 768,576

def move_window_center_x11(win_w,win_h,scr_w,scr_h):
    """Move window via XMoveWindow (no WM needed)."""
    x=max(0,(scr_w-win_w)//2); y=max(0,(scr_h-win_h)//2)
    try:
        import ctypes
        x11=ctypes.cdll.LoadLibrary('libX11.so.6')
        dpy=x11.XOpenDisplay(None)
        wid=pygame.display.get_wm_info().get('window',0)
        if dpy and wid:
            x11.XMoveWindow(dpy,ctypes.c_ulong(wid),
                            ctypes.c_int(x),ctypes.c_int(y))
            x11.XFlush(dpy); x11.XCloseDisplay(dpy)
    except: pass

def fmt_crt_range(r, hfp, hs, hbp, vfp, vs, vbp):
    return (f"crt_range0  {r['hmin']}-{r['hmax']}, {r['vfmin']:.2f}-{r['vfmax']:.2f}, "
            f"{hfp:.3f}, {hs:.3f}, {hbp:.3f}, {vfp:.3f}, {vs:.3f}, {vbp:.3f}, "
            f"0, 0, {r['pLmin']}, {r['pLmax']}, {r['iLmin']}, {r['iLmax']}")

def calculate_from_range(H, V, Hfreq, Vfreq, interlaced, r):
    Div=2 if interlaced else 1
    H_T=1.0/Hfreq; V_T=1.0/Vfreq
    hfp_t=r["hfp"]*1e-6; hs_t=r["hs"]*1e-6; hbp_t=r["hbp"]*1e-6
    vfp_t=r["vfp"]*1e-3; vs_t=r["vs"]*1e-3; vbp_t=r["vbp"]*1e-3
    denom_H=1.0-hfp_t/H_T-hs_t/H_T-hbp_t/H_T
    denom_V=1.0-vfp_t/V_T-vs_t/V_T-vbp_t/V_T
    TH=H/(H_T*denom_H); TV=V/(V_T*denom_V)
    H_total=_safe_round(H/denom_H)
    HFP=round(hfp_t*TH); HSYNC=round(hs_t*TH); HBP=H_total-H-HFP-HSYNC
    V_total=_safe_round(V/denom_V)
    VFP=round(vfp_t*TV); VSYNC=round(vs_t*TV); VBP=V_total-V-VFP-VSYNC
    X1,X2=H,H+HFP; X3,X4=H+HFP+HSYNC,H+HFP+HSYNC+HBP
    Y1,Y2=V,V+VFP; Y3,Y4=V+VFP+VSYNC,V+VFP+VSYNC+VBP
    pclk=Hfreq*X4/1e6; vfa=Hfreq*Div/Y4
    # SwitchRes V-blank threshold
    threshold_ms=22500.0/r["hmax"]
    line_ms=1000.0/(Hfreq*Div)
    vblank_ms=(VFP+VSYNC+VBP)*line_ms
    switchres_ok=vblank_ms<threshold_ms
    return dict(X1=X1,X2=X2,X3=X3,X4=X4,Y1=Y1,Y2=Y2,Y3=Y3,Y4=Y4,
                HFP=HFP,HSYNC=HSYNC,HBP=HBP,VFP=VFP,VSYNC=VSYNC,VBP=VBP,
                pclk=pclk,Hfreq=Hfreq,Vfreq_actual=vfa,interlaced=interlaced,
                switchres_ok=switchres_ok,vblank_ms=vblank_ms,threshold_ms=threshold_ms)

def calc_timings(res):
    X4,Y4=res["X4"],res["Y4"]; Hf=res["Hfreq"]; Vf=res["Vfreq_actual"]
    H_T,V_T=1/Hf,1/Vf
    return {"H_actif_us":res["X1"]*H_T/X4*1e6,"HFP_us":res["HFP"]*H_T/X4*1e6,
            "HSYNC_us":res["HSYNC"]*H_T/X4*1e6,"HBP_us":res["HBP"]*H_T/X4*1e6,
            "H_total_us":H_T*1e6,"V_actif_ms":res["Y1"]*V_T/Y4*1e3,
            "VFP_ms":res["VFP"]*V_T/Y4*1e3,"VSYNC_ms":res["VSYNC"]*V_T/Y4*1e3,
            "VBP_ms":res["VBP"]*V_T/Y4*1e3,"V_total_ms":V_T*1e3}

def distribute_ls(total, targets, minimums):
    n=len(targets); slack=total-sum(minimums)
    if slack<0: result=list(minimums); result[-1]=max(1,result[-1]+slack); return result
    excess=[max(0.0,t-m) for t,m in zip(targets,minimums)]
    total_excess=sum(excess)
    if total_excess==0: result=list(minimums); result[-1]+=slack; return result
    ratios=[e/total_excess for e in excess]
    continuous=[slack*r for r in ratios]
    floors=[math.floor(c) for c in continuous]
    remainders=[c-f for c,f in zip(continuous,floors)]
    remaining=slack-sum(floors)
    indices=sorted(range(n),key=lambda i:remainders[i],reverse=True)
    for i in range(int(remaining)): floors[indices[i]]+=1
    return [minimums[i]+floors[i] for i in range(n)]

def optimize_modeline(H, V, Hfreq_target, Vfreq_target, interlaced, r):
    Div=2 if interlaced else 1; Hfreq=Hfreq_target
    hfp_t=r["hfp"]*1e-6; hs_t=r["hs"]*1e-6; hbp_t=r["hbp"]*1e-6
    vfp_t=r["vfp"]*1e-3; vs_t=r["vs"]*1e-3; vbp_t=r["vbp"]*1e-3
    V_T_tgt=1.0/Vfreq_target
    denom_Vt=1.0-vfp_t/V_T_tgt-vs_t/V_T_tgt-vbp_t/V_T_tgt
    TERM_Vt=V/(V_T_tgt*denom_Vt) if denom_Vt>0 else V*1.1
    VFP_min=max(1,math.floor(vfp_t*TERM_Vt*0.5)); VS_min=max(1,math.floor(vs_t*TERM_Vt*0.5))
    VBP_min=max(1,math.floor(vbp_t*TERM_Vt*0.5)); V_total_min=V+VFP_min+VS_min+VBP_min
    V_total_ideal=Hfreq*Div/Vfreq_target
    candidates=sorted(set(max(V_total_min,round(V_total_ideal)+d) for d in range(-10,11)))
    candidates=[vt for vt in candidates if vt>=V_total_min]
    best_V=min(candidates,key=lambda vt:abs(Hfreq*Div/vt-Vfreq_target))
    Vfreq_actual=Hfreq*Div/best_V
    V_T_act=1.0/Vfreq_actual
    denom_Va=1.0-vfp_t/V_T_act-vs_t/V_T_act-vbp_t/V_T_act
    TERM_Va=V/(V_T_act*denom_Va) if denom_Va>0 else V*1.1
    VFP_tgt=vfp_t*TERM_Va; VS_tgt=vs_t*TERM_Va; VBP_tgt=vbp_t*TERM_Va
    VFP_min2=max(1,math.floor(VFP_tgt*0.5)); VS_min2=max(1,math.floor(VS_tgt*0.5)); VBP_min2=max(1,math.floor(VBP_tgt*0.5))
    VFP,VSYNC,VBP=distribute_ls(best_V-V,[VFP_tgt,VS_tgt,VBP_tgt],[VFP_min2,VS_min2,VBP_min2])
    # SwitchRes threshold check
    hmax=r["hmax"]; threshold_ms=22500.0/hmax
    line_ms=1000.0/(Hfreq*Div)
    vblank_ms=(VFP+VSYNC+VBP)*line_ms
    switchres_ok=vblank_ms<threshold_ms
    # Reduce VBP repeatedly until under SwitchRes threshold
    while not switchres_ok and VBP>VBP_min2:
        VBP-=1; vblank_ms=(VFP+VSYNC+VBP)*line_ms; switchres_ok=vblank_ms<threshold_ms
    H_T=1.0/Hfreq; denom_H=1.0-hfp_t/H_T-hs_t/H_T-hbp_t/H_T
    TERM_H=H/(H_T*denom_H) if denom_H>0 else H*1.15
    HFP_tgt=hfp_t*TERM_H; HS_tgt=hs_t*TERM_H; HBP_tgt=hbp_t*TERM_H
    H_total=max(H+max(1,math.floor(HFP_tgt*0.5))+max(1,math.floor(HS_tgt*0.5))+max(1,math.floor(HBP_tgt*0.5)),
                _safe_round(H/denom_H) if denom_H>0 else H+50)
    pclk=Hfreq*H_total/1e6
    HFP_tgt2=hfp_t*Hfreq*H_total; HS_tgt2=hs_t*Hfreq*H_total; HBP_tgt2=hbp_t*Hfreq*H_total
    HFP_min2=max(1,math.floor(HFP_tgt2*0.5)); HS_min2=max(1,math.floor(HS_tgt2*0.5)); HBP_min2=max(1,math.floor(HBP_tgt2*0.5))
    HFP,HSYNC,HBP=distribute_ls(H_total-H,[HFP_tgt2,HS_tgt2,HBP_tgt2],[HFP_min2,HS_min2,HBP_min2])
    X1,X2=H,H+HFP; X3,X4=H+HFP+HSYNC,H+HFP+HSYNC+HBP
    Y1,Y2=V,V+VFP; Y3,Y4=V+VFP+VSYNC,V+VFP+VSYNC+VBP
    return dict(X1=X1,X2=X2,X3=X3,X4=X4,Y1=Y1,Y2=Y2,Y3=Y3,Y4=Y4,
                HFP=HFP,HSYNC=HSYNC,HBP=HBP,VFP=VFP,VSYNC=VSYNC,VBP=VBP,
                pclk=pclk,Hfreq=Hfreq,switchres_ok=switchres_ok,
                vblank_ms=vblank_ms,threshold_ms=threshold_ms,
                Vfreq_actual=Vfreq_actual,interlaced=interlaced,
                Vfreq_error=abs(Vfreq_actual-Vfreq_target))

# ══════════════════════════════════════════════════════════════════════════════
# PYGAME UI WIDGETS
# ══════════════════════════════════════════════════════════════════════════════
class Fonts:
    _cache = {}
    @staticmethod
    def get(size, bold=False):
        key=(size,bold)
        if key not in Fonts._cache:
            Fonts._cache[key]=pygame.font.SysFont("sans",size,bold=bold)
        return Fonts._cache[key]
    @staticmethod
    def mono(size):
        key=("mono",size)
        if key not in Fonts._cache:
            Fonts._cache[key]=pygame.font.SysFont("monospace",size)
        return Fonts._cache[key]

def draw_text(surf,text,x,y,color=FG,size=13,bold=False,anchor="topleft"):
    f=Fonts.get(size,bold); s=f.render(str(text),True,color)
    r=s.get_rect(); setattr(r,anchor,(x,y)); surf.blit(s,r); return r

def draw_rect(surf,rect,color,border=0,radius=3):
    pygame.draw.rect(surf,color,rect,border,border_radius=radius)

class Button:
    def __init__(self,x,y,w,h,text,callback=None):
        self.rect=pygame.Rect(x,y,w,h); self.text=text
        self.callback=callback; self.hovered=False; self.focused=False
    def draw(self,surf):
        col=ACCENT if (self.hovered or self.focused) else BG3
        draw_rect(surf,self.rect,col,radius=4)
        if self.focused:
            draw_rect(surf,self.rect.inflate(4,4),(255,220,0),border=2,radius=5)
        draw_text(surf,self.text,self.rect.centerx,self.rect.centery,
                  BLACK if (self.hovered or self.focused) else FG,11,anchor="center")
    def activate(self):
        if self.callback: self.callback()
    def handle(self,event):
        if event.type==pygame.MOUSEMOTION:
            self.hovered=self.rect.collidepoint(event.pos)
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()

class TextInput:
    def __init__(self,x,y,w,h=20,value="",color=FG,mono=False,callback=None):
        self.rect=pygame.Rect(x,y,w,h); self.value=value
        self.focused=False; self.nav_hl=False; self.color=color; self.mono=mono; self.callback=callback
    def draw(self,surf):
        draw_rect(surf,self.rect,BG2,radius=3)
        if self.nav_hl and not self.focused:
            draw_rect(surf,self.rect.inflate(4,4),(255,220,0),border=2,radius=4)
        draw_rect(surf,self.rect,ACCENT if self.focused else BG3,border=1,radius=3)
        f=Fonts.mono(11) if self.mono else Fonts.get(11)
        s=f.render(self.value,True,self.color)
        clip=surf.get_clip(); surf.set_clip(self.rect.inflate(-4,-2))
        surf.blit(s,(self.rect.x+3,self.rect.y+(self.rect.h-s.get_height())//2))
        surf.set_clip(clip)
    def handle(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            self.focused=self.rect.collidepoint(event.pos)
        if event.type==pygame.KEYDOWN and self.focused:
            if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
                self.focused=False
                if self.callback: self.callback(self.value)
            elif event.key==pygame.K_BACKSPACE: self.value=self.value[:-1]
            elif event.key==pygame.K_ESCAPE: self.focused=False
            elif event.unicode and event.unicode.isprintable(): self.value+=event.unicode
    def set_value(self,v): self.value=str(v)
    def get_float(self,default=0.0):
        try: return float(self.value)
        except: return default
    def get_int(self,default=0):
        try: return int(float(self.value))
        except: return default

class Slider:
    def __init__(self,x,y,w,h,min_v,max_v,value,step=0.001,callback=None):
        self.rect=pygame.Rect(x,y,w,h); self.min_v=min_v; self.max_v=max_v
        self.value=value; self.step=step; self.callback=callback; self.dragging=False
        self.focused=False
    def _val_to_x(self,v):
        ratio=(v-self.min_v)/(self.max_v-self.min_v)
        return self.rect.x+int(ratio*self.rect.w)
    def _x_to_val(self,x):
        ratio=max(0.0,min(1.0,(x-self.rect.x)/self.rect.w))
        v=self.min_v+ratio*(self.max_v-self.min_v)
        v=round(v) if self.step>=1 else round(v/self.step)*self.step
        return max(self.min_v,min(self.max_v,v))
    def nudge(self,direction,fast=False):
        step=self.step*(10 if fast else 1)
        self.value=max(self.min_v,min(self.max_v,self.value+direction*step))
        if self.callback: self.callback(self.value)
    def draw(self,surf):
        track=pygame.Rect(self.rect.x,self.rect.centery-2,self.rect.w,4)
        draw_rect(surf,track,BG3,radius=2)
        sx=self._val_to_x(self.value)
        fill=pygame.Rect(self.rect.x,self.rect.centery-2,sx-self.rect.x,4)
        draw_rect(surf,fill,ACCENT,radius=2)
        thumb_col=(255,220,0) if self.focused else ACCENT
        pygame.draw.circle(surf,thumb_col,(sx,self.rect.centery),8 if self.focused else 7)
        pygame.draw.circle(surf,BG2,(sx,self.rect.centery),5)
    def handle(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.rect.collidepoint(event.pos):
                self.dragging=True; self.value=self._x_to_val(event.pos[0])
        if event.type==pygame.MOUSEMOTION and self.dragging:
            self.value=self._x_to_val(event.pos[0])
        if event.type==pygame.MOUSEBUTTONUP and event.button==1:
            if self.dragging:
                self.dragging=False
                if self.callback: self.callback(self.value)
    def set_value(self,v): self.value=max(self.min_v,min(self.max_v,v))

class SliderRow:
    H=28
    def __init__(self,x,y,w,label,min_v,max_v,value,step=0.001,is_int=False,fmt="{:.3f}",callback=None):
        self.label=label; self.is_int=is_int; self.fmt=fmt; self.callback=callback
        lw=168; ew=68; sw=w-lw-ew-8
        self.label_rect=pygame.Rect(x,y,lw,self.H)
        self.entry=TextInput(x+lw,y+4,ew,20,
                             str(int(value)) if is_int else fmt.format(value),
                             color=YELLOW,mono=True)
        self.slider=Slider(x+lw+ew+4,y+6,sw,16,min_v,max_v,value,step)
        self.entry.callback=self._from_entry
        self.slider.callback=self._from_slider
        self._focused=False
    @property
    def focused(self): return self._focused
    @focused.setter
    def focused(self,v): self._focused=v; self.slider.focused=v
    def _fmt(self,v): return str(int(round(v))) if self.is_int else self.fmt.format(v)
    def _from_slider(self,v):
        self.entry.set_value(self._fmt(v))
        if self.callback: self.callback()
    def _from_entry(self,text):
        try:
            v=float(text); self.slider.set_value(v)
            if self.callback: self.callback()
        except: pass
    def key_input(self,key,mod=0,unicode=""):
        fast=bool(mod&pygame.KMOD_CTRL)
        if key==pygame.K_LEFT:
            self.slider.nudge(-1,fast); self.entry.set_value(self._fmt(self.slider.value))
        elif key==pygame.K_RIGHT:
            self.slider.nudge(+1,fast); self.entry.set_value(self._fmt(self.slider.value))
        elif key in (pygame.K_RETURN,pygame.K_KP_ENTER):
            if self.entry.focused:
                self.entry.focused=False
                self._from_entry(self.entry.value)
            else:
                self.entry.focused=True
        elif key==pygame.K_BACKSPACE and self.entry.focused:
            self.entry.value=self.entry.value[:-1]
        elif unicode and (unicode.isdigit() or unicode in '.-'):
            # Direct digit/number entry → activate field and type
            if not self.entry.focused:
                self.entry.value=""; self.entry.focused=True
            self.entry.value+=unicode
    def draw(self,surf):
        if self._focused:
            bg=pygame.Rect(self.label_rect.x-2,self.label_rect.y,
                           self.label_rect.w+self.entry.rect.w+self.slider.rect.w+20,self.H)
            draw_rect(surf,bg,(50,50,70),radius=3)
        draw_text(surf,self.label,self.label_rect.x+4,self.label_rect.y+8,
                  (255,220,0) if self._focused else FG2,11)
        self.entry.draw(surf); self.slider.draw(surf)
    def handle(self,event):
        self.entry.handle(event); self.slider.handle(event)
    def set_value(self,v):
        self.slider.set_value(float(v)); self.entry.set_value(self._fmt(float(v)))
    def get_value(self):
        v=self.entry.get_float()
        return int(round(v)) if self.is_int else v

class Dropdown:
    def __init__(self,x,y,w,h,options,selected=0,callback=None):
        self.rect=pygame.Rect(x,y,w,h); self.options=options
        self.selected=selected; self.open=False; self.callback=callback
        self.hovered_item=-1; self.focused=False
    @property
    def value(self): return self.options[self.selected] if self.options else ""
    def set_by_value(self,val):
        if val in self.options: self.selected=self.options.index(val)
    def draw(self,surf):
        # Box only (popup drawn separately via draw_popup for correct z-order)
        draw_rect(surf,self.rect,BG2,radius=3)
        draw_rect(surf,self.rect,ACCENT if self.open else BG3,border=1,radius=3)
        if self.focused:
            draw_rect(surf,self.rect.inflate(4,4),(255,220,0),border=2,radius=4)
        draw_text(surf,self.value,self.rect.x+5,self.rect.y+5,FG,11)
        ax=self.rect.right-12; ay=self.rect.centery
        pygame.draw.polygon(surf,FG2,[(ax,ay-3),(ax+8,ay-3),(ax+4,ay+3)])
    def draw_popup(self,surf,oy=0):
        """Draw the open list as an overlay. oy = y offset (scroll)."""
        if not self.open: return
        item_h=20; n=min(len(self.options),10); ddh=n*item_h
        ddr=pygame.Rect(self.rect.x,self.rect.bottom+oy,self.rect.w,ddh)
        draw_rect(surf,ddr,BG2,radius=3)
        draw_rect(surf,ddr,ACCENT,border=2,radius=3)
        for i,opt in enumerate(self.options[:10]):
            ir=pygame.Rect(ddr.x,ddr.y+i*item_h,ddr.w,item_h)
            if i==self.hovered_item or i==self.selected: draw_rect(surf,ir,BG3)
            draw_text(surf,opt,ir.x+5,ir.y+4,FG,11)
    def activate(self):
        self.open=not self.open
    def handle(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.rect.collidepoint(event.pos): self.open=not self.open
            elif self.open:
                item_h=20
                for i in range(min(len(self.options),8)):
                    ir=pygame.Rect(self.rect.x,self.rect.bottom+i*item_h,self.rect.w,item_h)
                    if ir.collidepoint(event.pos):
                        self.selected=i; self.open=False
                        if self.callback: self.callback(self.options[i]); return
                self.open=False
        if event.type==pygame.MOUSEMOTION and self.open:
            item_h=20; self.hovered_item=-1
            for i in range(min(len(self.options),8)):
                ir=pygame.Rect(self.rect.x,self.rect.bottom+i*item_h,self.rect.w,item_h)
                if ir.collidepoint(event.pos): self.hovered_item=i

class ScrollArea:
    def __init__(self,x,y,w,h):
        self.rect=pygame.Rect(x,y,w,h); self.scroll_y=0; self.content_h=h; self.surf=None
    def begin(self,content_h):
        self.content_h=max(content_h,self.rect.h)
        self.surf=pygame.Surface((self.rect.w,self.content_h)); self.surf.fill(BG)
    def end(self,screen):
        visible=pygame.Rect(0,self.scroll_y,self.rect.w,self.rect.h)
        screen.blit(self.surf,self.rect.topleft,visible)
        if self.content_h>self.rect.h:
            bar_h=max(20,int(self.rect.h*self.rect.h/self.content_h))
            bar_y=self.rect.y+int(self.scroll_y/self.content_h*self.rect.h)
            draw_rect(screen,pygame.Rect(self.rect.right-5,bar_y,4,bar_h),BG3,radius=2)
    def handle_scroll(self,event):
        if event.type==pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_y-=event.y*20
                self.scroll_y=max(0,min(self.scroll_y,self.content_h-self.rect.h))

class Checkbox:
    def __init__(self,x,y,label,checked=False,callback=None):
        self.rect=pygame.Rect(x,y,16,16); self.label=label
        self.checked=checked; self.callback=callback; self.focused=False
    def draw(self,surf):
        draw_rect(surf,self.rect,BG2,radius=2)
        draw_rect(surf,self.rect,ACCENT if self.checked else BG3,border=1,radius=2)
        if self.focused:
            draw_rect(surf,self.rect.inflate(4,4),(255,220,0),border=2,radius=3)
        if self.checked:
            pygame.draw.line(surf,ACCENT,(self.rect.x+3,self.rect.centery),(self.rect.x+6,self.rect.bottom-3),2)
            pygame.draw.line(surf,ACCENT,(self.rect.x+6,self.rect.bottom-3),(self.rect.right-2,self.rect.y+3),2)
        draw_text(surf,self.label,self.rect.right+5,self.rect.y,FG2,11)
    def activate(self):
        self.checked=not self.checked
        if self.callback: self.callback(self.checked)
    def handle(self,event):
        full=pygame.Rect(self.rect.x,self.rect.y,self.rect.w+80,self.rect.h)
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if full.collidepoint(event.pos): self.activate()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
class GeoSpin:
    """Compact vertical label+entry for geometry (horizontal layout)."""
    W=82; H=42
    def __init__(self,x,y,label,min_v,max_v,init,step=1,is_float=False,callback=None):
        self.label=label; self.min_v=min_v; self.max_v=max_v
        self.step=step; self.is_float=is_float; self.callback=callback
        self.focused=False
        fmt="{:.2f}" if is_float else "{:.0f}"
        val=fmt.format(init)
        self.entry=TextInput(x,y+16,self.W,20,val,color=YELLOW,mono=True)
        self._x=x; self._y=y; self.value=float(init)
        self.entry.callback=self._confirm
    def _confirm(self,text):
        try:
            v=max(self.min_v,min(self.max_v,float(text)))
            self.value=v; self._update_entry()
            if self.callback: self.callback()
        except: self._update_entry()
    def _update_entry(self):
        fmt="{:.2f}" if self.is_float else "{:.0f}"
        self.entry.set_value(fmt.format(self.value))
    def nudge(self,d,fast=False):
        s=self.step*(10 if fast else 1)
        self.value=max(self.min_v,min(self.max_v,self.value+d*s))
        self._update_entry()
        if self.callback: self.callback()
    def get_value(self):
        try: return max(self.min_v,min(self.max_v,float(self.entry.value)))
        except: return self.value
    def set_value(self,v):
        self.value=float(v); self._update_entry()
    def draw(self,surf):
        if self.focused:
            draw_rect(surf,pygame.Rect(self._x-2,self._y,self.W+4,self.H+2),(255,220,0),border=1,radius=3)
        draw_text(surf,self.label,self._x,self._y,(255,220,0) if self.focused else FG2,10)
        self.entry.draw(surf)
    def handle(self,event):
        self.entry.handle(event)
    def move(self,x,y):
        self._x=x; self._y=y
        self.entry.rect.x=x; self.entry.rect.y=y+16


class FileDialog:
    """Modal file save/load dialog with filename entry + file list."""
    def __init__(self,title,directory,mode="save",default_name="",on_confirm=None):
        self.title=title; self.directory=directory; self.mode=mode
        self.on_confirm=on_confirm; self.active=True
        self.files=[]
        try:
            self.files=sorted(f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f)))
        except: self.files=[]
        self.sel=0; self.scroll=0
        # Modal centered box
        self.W=440; self.H=300
        self.name=default_name
        self.name_focused=(mode=="save")
        self.in_list=(mode=="load" and len(self.files)>0)
        if self.in_list: self.name_focused=False
    def draw(self,surf,sw,sh):
        # Dim background
        overlay=pygame.Surface((sw,sh)); overlay.set_alpha(180); overlay.fill((0,0,0))
        surf.blit(overlay,(0,0))
        bx=(sw-self.W)//2; by=(sh-self.H)//2
        box=pygame.Rect(bx,by,self.W,self.H)
        draw_rect(surf,box,BG2,radius=6); draw_rect(surf,box,ACCENT,border=2,radius=6)
        draw_text(surf,self.title,bx+12,by+10,ACCENT,13,bold=True)
        draw_text(surf,f"Dir: {self.directory}",bx+12,by+30,FG2,9)
        # Filename entry
        ny=by+48
        draw_text(surf,"Name:",bx+12,ny+3,FG2,11)
        er=pygame.Rect(bx+60,ny,self.W-130,22)
        draw_rect(surf,er,BG,radius=3)
        draw_rect(surf,er,(255,220,0) if self.name_focused else BG3,border=2 if self.name_focused else 1,radius=3)
        draw_text(surf,self.name+(".txt" if self.name and not self.name.endswith(".txt") else ""),er.x+4,er.y+4,YELLOW,11)
        # File list
        ly=ny+32
        draw_text(surf,"Existing files (↑↓ select):",bx+12,ly,FG2,10); ly+=16
        list_rect=pygame.Rect(bx+12,ly,self.W-24,self.H-(ly-by)-50)
        draw_rect(surf,list_rect,BG,radius=3)
        item_h=18; maxv=list_rect.h//item_h
        for i in range(self.scroll,min(len(self.files),self.scroll+maxv)):
            iy=list_rect.y+(i-self.scroll)*item_h
            if i==self.sel and self.in_list:
                draw_rect(surf,pygame.Rect(list_rect.x,iy,list_rect.w,item_h),(255,220,0))
                draw_text(surf,self.files[i],list_rect.x+4,iy+2,BLACK,10)
            else:
                draw_text(surf,self.files[i],list_rect.x+4,iy+2,FG,10)
        # Buttons hint
        draw_text(surf,"ENTER=confirm   ESC=cancel   TAB=switch name/list",
                  bx+12,by+self.H-24,FG2,9)
    def handle_key(self,event):
        if event.key==pygame.K_ESCAPE:
            self.active=False; return
        if event.key==pygame.K_TAB:
            if self.files: self.in_list=not self.in_list; self.name_focused=not self.in_list
            return
        if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
            if self.in_list and self.files:
                self.name=self.files[self.sel].replace(".txt","")
            fn=self.name.strip()
            if fn:
                if not fn.endswith(".txt"): fn+=".txt"
                self.active=False
                if self.on_confirm: self.on_confirm(os.path.join(self.directory,fn))
            return
        if self.in_list:
            if event.key==pygame.K_UP: self.sel=max(0,self.sel-1)
            elif event.key==pygame.K_DOWN: self.sel=min(len(self.files)-1,self.sel+1)
            elif event.key==pygame.K_BACKSPACE:
                self.in_list=False; self.name_focused=True
            else:
                u=getattr(event,'unicode','')
                if u and u.isprintable():
                    self.in_list=False; self.name_focused=True; self.name+=u
        elif self.name_focused:
            if event.key==pygame.K_BACKSPACE: self.name=self.name[:-1]
            else:
                u=getattr(event,'unicode','')
                if u and u.isprintable() and u not in '/\\': self.name+=u


# ══════════════════════════════════════════════════════════════════════════════
class App:
    W,H_WIN=640,480
    TAB_H=26; STATUS_H=16
    TABS=["Setup","CRT","Results","Verify","Diagram"]

    def __init__(self):
        pygame.init()
        # Open window at full screen resolution, draw 640x480 canvas centered
        self.scr_w,self.scr_h=get_screen_resolution()
        self.screen=pygame.display.set_mode((self.scr_w,self.scr_h))
        self.canvas=pygame.Surface((self.W,self.H_WIN))
        self.cx=(self.scr_w-self.W)//2
        self.cy=(self.scr_h-self.H_WIN)//2
        pygame.display.set_caption("CRT Modeline Toolbox v2.5 — ZFEbHVUE")
        pygame.key.set_repeat(280, 60)  # repeat: 280ms delay, 60ms interval
        self.clock=pygame.time.Clock()
        self.dialog=None
        self.current_tab=0; self._res=None; self._r_live=None
        self._current_range=None; self._custom_mode=False; self._fixed_range=None
        self.status=""; self.status_col=FG2
        self._focus_idx=0  # focused widget index per tab
        self._focus_per_tab=[0]*len(self.TABS)
        # Joystick init
        pygame.joystick.init()
        self._joy=None
        if pygame.joystick.get_count()>0:
            self._joy=pygame.joystick.Joystick(0); self._joy.init()
            self.status=f"Joystick: {self._joy.get_name()}"; self.status_col=GREEN_C
        self._joy_repeat=0; self._joy_axis_x=0; self._joy_axis_y=0
        CY=self.TAB_H+4; CA=self.H_WIN-self.TAB_H-self.STATUS_H-8
        self.scroll=[ScrollArea(0,CY,self.W,CA) for _ in self.TABS]
        self._build_setup(); self._build_crt_range(); self._build_results(); self._build_verify()
        # Pre-set scroll content heights so auto-scroll works before first draw
        self.scroll[0].content_h=self._setup_h
        self.scroll[1].content_h=self._crt_range_h
        self.scroll[2].content_h=460
        self.scroll[3].content_h=500
        self._apply_preset(PRESET_NAMES[3])  # Arcade 15kHz
        self._set_focus(0)  # focus first widget

    def _cy(self): return self.TAB_H+4

    # ── BUILD SETUP ──────────────────────────────────────────────────────────
    def _build_setup(self):
        x0,y,W=6,4,self.W-12
        self.dd_preset=Dropdown(x0,y,220,22,PRESET_NAMES,3,callback=self._apply_preset)
        self.dd_range=Dropdown(x0+228,y,100,22,["15KHz"],callback=self._on_range_select)
        self.chk_interlaced=Checkbox(x0+338,y+3,"Int.",callback=lambda v:self._calc())
        self.ti_output=TextInput(x0+410,y+1,55,20,"DP-1")
        y+=30
        self.sw_width=SliderRow(x0,y,W,"H Width (px)",64,3840,640,step=1,is_int=True,fmt="{:.0f}",callback=self._calc)
        y+=SliderRow.H+2
        self.sw_height=SliderRow(x0,y,W,"V Height (px)",32,2160,480,step=1,is_int=True,fmt="{:.0f}",callback=self._calc)
        y+=SliderRow.H+2
        self.sw_hfreq=SliderRow(x0,y,W,"Hfreq (kHz)",15.0,70.0,15.69,step=0.001,callback=self._on_hfreq)
        y+=SliderRow.H+2
        self.sw_vfreq=SliderRow(x0,y,W,"Vfreq (Hz)",49.0,130.0,60.0,step=0.01,fmt="{:.3f}",callback=self._calc)
        y+=SliderRow.H+8
        self.ti_paste=TextInput(x0,y+1,W-66,20,"",color=YELLOW,mono=True)
        self.btn_parse=Button(x0+W-60,y,60,22,"Parse →",self._parse_paste)
        y+=26
        # Import Modeline row
        self.ti_import=TextInput(x0,y+1,W-66,20,"",color=YELLOW,mono=True,
                                  callback=lambda v: self._import_modeline(v))
        self.btn_import=Button(x0+W-60,y,60,22,"Import →",lambda: self._import_modeline(self.ti_import.value))
        y+=28
        self.sw_hfp_px=SliderRow(x0,y,W,"H Front Porch (px)",1,300,31,step=1,is_int=True,fmt="{:.0f}",callback=self._from_pixels)
        y+=SliderRow.H+2
        self.sw_hs_px=SliderRow(x0,y,W,"H Sync (px)",1,300,73,step=1,is_int=True,fmt="{:.0f}",callback=self._from_pixels)
        y+=SliderRow.H+2
        self.sw_hbp_px=SliderRow(x0,y,W,"H Back Porch (px)",1,500,125,step=1,is_int=True,fmt="{:.0f}",callback=self._from_pixels)
        y+=SliderRow.H+2
        self.sw_vfp_px=SliderRow(x0,y,W,"V Front Porch (px)",1,100,2,step=1,is_int=True,fmt="{:.0f}",callback=self._from_pixels)
        y+=SliderRow.H+2
        self.sw_vs_px=SliderRow(x0,y,W,"V Sync (px)",1,100,6,step=1,is_int=True,fmt="{:.0f}",callback=self._from_pixels)
        y+=SliderRow.H+2
        self.sw_vbp_px=SliderRow(x0,y,W,"V Back Porch (px)",1,200,32,step=1,is_int=True,fmt="{:.0f}",callback=self._from_pixels)
        # Geometry section — 4 horizontal compact spinboxes
        y+=6
        gx=x0; gs=GeoSpin.W+10
        self.geo_hmove=GeoSpin(gx,y,"H move\n=H_shift",-200,200,0,step=1,callback=self._apply_geometry)
        self.geo_vmove=GeoSpin(gx+gs,y,"V move\n=V_shift",-100,100,0,step=1,callback=self._apply_geometry)
        self.geo_hsize=GeoSpin(gx+gs*2,y,"H_size\n(zoom H)",0.50,2.00,1.00,step=0.01,is_float=True,callback=self._apply_geometry)
        self.geo_vsize=GeoSpin(gx+gs*3,y,"V_size ⚗\n(zoom V)",0.50,2.00,1.00,step=0.01,is_float=True,callback=self._apply_geometry)
        self.lbl_geo_info=""  # updated by _refresh_display
        y+=GeoSpin.H+6
        self._setup_h=y+8

    # ── BUILD CRT RANGE ──────────────────────────────────────────────────────
    def _build_crt_range(self):
        x0,y,W=6,4,self.W-12
        self.sw_hfp=SliderRow(x0,y,W,"H Front Porch (µs)",0.05,12.0,2.0,callback=self._calc); y+=SliderRow.H+2
        self.sw_hs=SliderRow(x0,y,W,"H Sync (µs)",0.05,10.0,4.7,callback=self._calc); y+=SliderRow.H+2
        self.sw_hbp=SliderRow(x0,y,W,"H Back Porch (µs)",0.05,15.0,8.0,callback=self._calc); y+=SliderRow.H+2
        self.sw_vfp=SliderRow(x0,y,W,"V Front Porch (ms)",0.01,2.0,0.064,callback=self._calc); y+=SliderRow.H+2
        self.sw_vs=SliderRow(x0,y,W,"V Sync (ms)",0.01,2.0,0.192,callback=self._calc); y+=SliderRow.H+2
        self.sw_vbp=SliderRow(x0,y,W,"V Back Porch (ms)",0.01,3.0,1.024,callback=self._calc); y+=SliderRow.H+10
        self._crt_range_h=y+160

    # ── BUILD RESULTS ────────────────────────────────────────────────────────
    def _build_results(self):
        x0,y,W=6,4,self.W-12; bw=82; gap=4
        # Row 1: Copy | Apply | Optimise | ☐ Δ VFP [entry]
        self.btn_copy=Button(x0,y,bw,22,"Copy xrandr",self._copy_xrandr)
        self.btn_apply=Button(x0+bw+gap,y,bw,22,"Apply xrandr",self._apply_xrandr)
        self.btn_opt=Button(x0+(bw+gap)*2,y,bw,22,"⚡ Optimise",self._optimise)
        self.chk_vfp_lock=Checkbox(x0+(bw+gap)*3,y+3,"Δ VFP",callback=lambda v:None)
        self.ti_vfp_val=TextInput(x0+(bw+gap)*3+50,y+1,40,20,"3",color=YELLOW,mono=True)
        y+=28
        # Row 2: Save/Load CRT Range | Save/Load Modeline
        self.btn_save=Button(x0,y,bw,22,"💾 Save CRT",self._save)
        self.btn_load=Button(x0+bw+gap,y,bw,22,"📂 Load CRT",self._load)
        self.btn_save_ml=Button(x0+(bw+gap)*2,y,bw,22,"🎬 Save ML",self._save_modeline)
        self.btn_load_ml=Button(x0+(bw+gap)*3,y,bw,22,"📂 Load ML",self._load_modeline)

    # ── LOGIC ────────────────────────────────────────────────────────────────
    def _build_verify(self):
        x0,y,W=6,4,self.W-12
        self.ti_verify=TextInput(x0,y+18,W-130,20,"",color=YELLOW,mono=True,
                                  callback=lambda v:self._do_verify(v))
        self.btn_verify=Button(x0+W-124,y+17,58,22,"Verify",lambda:self._do_verify(self.ti_verify.value))
        self.btn_verify_load=Button(x0+W-62,y+17,62,22,"📂 Load",self._load_verify)
        self.dd_verify_mon=Dropdown(x0,y+58,220,22,PRESET_NAMES,3,callback=lambda v:self._do_verify(self.ti_verify.value))
        self._verify_res=None

    def _load_verify(self):
        d="/userdata" if os.path.isdir("/userdata") else os.path.expanduser("~")
        self.dialog=FileDialog("Load Modeline to Verify",d,"load","",self._do_load_verify)

    def _do_load_verify(self,path):
        try:
            with open(path) as f: lines=f.readlines()
            for line in lines:
                s=line.strip()
                if s.startswith("Modeline"):
                    parts=s.split('"')
                    if len(parts)>=3:
                        ml=parts[2].strip()
                        self.ti_verify.set_value(ml); self._do_verify(ml); return
                # also accept a bare modeline line (starts with a float pclk)
                tok=s.split()
                if len(tok)>=9:
                    try:
                        float(tok[0]); int(tok[1])
                        self.ti_verify.set_value(s); self._do_verify(s); return
                    except: pass
            self.status="No modeline found in file"; self.status_col=RED_C
        except Exception as e: self.status=f"Load error: {e}"; self.status_col=RED_C

    def _do_verify(self,text):
        res=verify_modeline(text.strip())
        if not res:
            self.status="Verify: invalid modeline"; self.status_col=RED_C
            self._verify_res=None; return
        self._verify_res=res
        self.status=f"Verified: {res['X1']}x{res['Y1']} {res['Hfreq']/1000:.3f}kHz"
        self.status_col=GREEN_C

    def _apply_preset(self,name):
        p=PRESETS.get(name)
        if not p: return
        self.dd_preset.set_by_value(name)
        labels=[x["lb"] for x in p["ranges"]]
        self.dd_range.options=labels; self.dd_range.selected=0
        self.sw_hfreq.set_value(p["dH"]); self.sw_vfreq.set_value(p["dV"])
        self._load_range(p["ranges"][0]); self._calc()

    def _load_range(self,r):
        self._current_range=r; self._custom_mode=False
        self._fixed_range=dict(r)  # Calamity reference (fixed to preset)
        self.sw_hfp.set_value(r["hfp"]); self.sw_hs.set_value(r["hs"])
        self.sw_hbp.set_value(r["hbp"]); self.sw_vfp.set_value(r["vfp"])
        self.sw_vs.set_value(r["vs"]); self.sw_vbp.set_value(r["vbp"])
        self.sw_hfreq.set_value((r["hmin"]+r["hmax"])/2/1000)

    def _on_range_select(self,lb):
        name=self.dd_preset.value; p=PRESETS.get(name)
        if not p: return
        for r in p["ranges"]:
            if r["lb"]==lb: self._load_range(r); self._calc(); return

    def _on_hfreq(self):
        if not self._custom_mode:
            hfreq_hz=self.sw_hfreq.get_value()*1000
            r=select_range(self.dd_preset.value,hfreq_hz)
            if r is not self._current_range:
                self._current_range=r
                self.sw_hfp.set_value(r["hfp"]); self.sw_hs.set_value(r["hs"])
                self.sw_hbp.set_value(r["hbp"]); self.sw_vfp.set_value(r["vfp"])
                self.sw_vs.set_value(r["vs"]); self.sw_vbp.set_value(r["vbp"])
                self.dd_range.set_by_value(r["lb"])
        self._calc()

    def _make_rl(self):
        r=self._current_range or PRESETS["Arcade 15kHz"]["ranges"][0]
        return {"hfp":self.sw_hfp.get_value(),"hs":self.sw_hs.get_value(),
                "hbp":self.sw_hbp.get_value(),"vfp":self.sw_vfp.get_value(),
                "vs":self.sw_vs.get_value(),"vbp":self.sw_vbp.get_value(),
                **{k:r[k] for k in ("hmin","hmax","vfmin","vfmax","pLmin","pLmax","iLmin","iLmax")}}


    def _apply_geometry(self, *_):
        if self._res and self._r_live:
            self._refresh_display(self._res, self._r_live)

    def _refresh_display(self, res, r_live):
        self._res=res; self._r_live=r_live
        try: hmove=int(round(self.geo_hmove.get_value()))
        except: hmove=0
        try: vmove=int(round(self.geo_vmove.get_value()))
        except: vmove=0
        try: hsize=max(0.5,float(self.geo_hsize.get_value()))
        except: hsize=1.0
        try: vsize=max(0.5,float(self.geo_vsize.get_value()))
        except: vsize=1.0
        rg=dict(res)
        # H_size
        if abs(hsize-1.0)>0.001:
            Hb=max(3,round((res["X4"]-res["X1"])/hsize))
            Hfp=max(1,round(res["HFP"]/hsize)); Hs=max(1,round(res["HSYNC"]/hsize)); Hbp=max(1,Hb-Hfp-Hs)
            rg["HFP"]=Hfp; rg["HSYNC"]=Hs; rg["HBP"]=Hbp
            rg["X2"]=res["X1"]+Hfp; rg["X3"]=rg["X2"]+Hs; rg["X4"]=rg["X3"]+Hbp
            rg["pclk"]=res["Hfreq"]*rg["X4"]/1e6
        # V_size
        if abs(vsize-1.0)>0.001:
            Vb=rg["VFP"]+rg["VSYNC"]+rg["VBP"]
            Vbn=max(rg["VSYNC"]+2,round(Vb/vsize)); rem=Vbn-rg["VSYNC"]
            r_vfp=rg["VFP"]/(rg["VFP"]+rg["VBP"]) if (rg["VFP"]+rg["VBP"])>0 else 0.2
            Vfp=max(1,round(rem*r_vfp)); Vbp=max(1,rem-Vfp)
            rg["VFP"]=Vfp; rg["VBP"]=Vbp; rg["Y2"]=rg["Y1"]+Vfp
            rg["Y3"]=rg["Y2"]+rg["VSYNC"]; rg["Y4"]=rg["Y3"]+Vbp
            Div=2 if rg["interlaced"] else 1; rg["Vfreq_actual"]=rg["Hfreq"]*Div/rg["Y4"]
        # H_move
        hfp_c=rg["X2"]-rg["X1"]; hbp_c=rg["X4"]-rg["X3"]
        hmc=max(-(hbp_c-1),min(hfp_c-1,hmove)); self._hmove_clamped=hmc
        rg["X2"]-=hmc; rg["X3"]-=hmc
        # V_move
        vfp_a=rg["Y2"]-rg["Y1"]-vmove; vbp_a=rg["Y4"]-rg["Y3"]+vmove
        if vfp_a<1 or vbp_a<1:
            lms=1000.0/(rg["Hfreq"]*(2 if rg["interlaced"] else 1))
            ra=dict(r_live)
            ra["vfp"]=max(r_live["vfp"],(rg["VFP"]+max(0,1-vfp_a))*lms)
            ra["vbp"]=max(r_live["vbp"],(rg["VBP"]+max(0,1-vbp_a))*lms)
            nr=optimize_modeline(rg["X1"],rg["Y1"],rg["Hfreq"],rg["Vfreq_actual"],rg["interlaced"],ra)
            rg=nr; rg["pclk"]=rg["Hfreq"]*rg["X4"]/1e6
            rg["Y2"]-=vmove; rg["Y3"]-=vmove
        else:
            rg["Y2"]-=vmove; rg["Y3"]-=vmove
        rg["HFP"]=rg["X2"]-rg["X1"]; rg["HBP"]=rg["X4"]-rg["X3"]
        rg["VFP"]=rg["Y2"]-rg["Y1"]; rg["VBP"]=rg["Y4"]-rg["Y3"]
        self._rg=rg
        # Update pixel sliders
        self.sw_hfp_px.set_value(rg["HFP"]); self.sw_hs_px.set_value(rg["HSYNC"])
        self.sw_hbp_px.set_value(rg["HBP"]); self.sw_vfp_px.set_value(rg["VFP"])
        self.sw_vs_px.set_value(rg["VSYNC"]); self.sw_vbp_px.set_value(rg["VBP"])

    def _import_modeline(self, text):
        s=text.strip()
        # Strip optional Modeline "name" prefix
        import re as _re
        m=_re.match(r'(?i)(?:Modeline\s+"[^"]*"\s+)?(.*)',s)
        if m: s=m.group(1)
        res=verify_modeline(s)
        if not res: self.status="Import error: invalid modeline"; self.status_col=RED_C; return
        Hf=res["Hfreq"]; Vf=res["Vfreq_actual"]; i=res["interlaced"]
        # Back-compute µs/ms timing values
        X4=res["X4"]; Y4=res["Y4"]
        HFP_us=res["HFP"]/X4/Hf*1e6; HS_us=res["HSYNC"]/X4/Hf*1e6; HBP_us=res["HBP"]/X4/Hf*1e6
        Div=2 if i else 1
        VFP_ms=res["VFP"]/Y4/Vf*1e3; VS_ms=res["VSYNC"]/Y4/Vf*1e3; VBP_ms=res["VBP"]/Y4/Vf*1e3
        self.sw_width.set_value(res["X1"]); self.sw_height.set_value(res["Y1"])
        self.sw_hfreq.set_value(Hf/1000); self.sw_vfreq.set_value(Vf)
        self.chk_interlaced.checked=i
        self.sw_hfp.set_value(round(HFP_us,3)); self.sw_hs.set_value(round(HS_us,3))
        self.sw_hbp.set_value(round(HBP_us,3)); self.sw_vfp.set_value(round(VFP_ms,3))
        self.sw_vs.set_value(round(VS_ms,3)); self.sw_vbp.set_value(round(VBP_ms,3))
        self._calc()
        self.status=f"Imported: {res['X1']}x{res['Y1']} {Hf/1000:.3f}kHz {Vf:.3f}Hz"
        self.status_col=GREEN_C

    def _save_modeline(self):
        if not self._res: return
        rg=getattr(self,"_rg",self._res)
        name=f"modeline_{rg['X1']}x{rg['Y1']}{'i' if rg['interlaced'] else ''}"
        d="/userdata" if os.path.isdir("/userdata") else os.path.expanduser("~")
        self.dialog=FileDialog("Save Modeline",d,"save",name,self._do_save_ml)

    def _do_save_ml(self,path):
        rg=getattr(self,"_rg",self._res); r=self._r_live or {}; t=calc_timings(rg)
        name=f"{rg['X1']}x{rg['Y1']}{'i' if rg['interlaced'] else ''}"
        try:
            with open(path,"w") as f:
                ml=self._modeline_str_rg(rg)
                crt=fmt_crt_range(r,t["HFP_us"],t["HSYNC_us"],t["HBP_us"],t["VFP_ms"],t["VSYNC_ms"],t["VBP_ms"])
                f.write(f"# Modeline\nModeline \"{name}\" {ml}\n\n# CRT Range\n{crt}\n")
            self.status=f"Saved: {path}"; self.status_col=GREEN_C
        except Exception as e: self.status=f"Save error: {e}"; self.status_col=RED_C

    def _load_modeline(self):
        d="/userdata" if os.path.isdir("/userdata") else os.path.expanduser("~")
        self.dialog=FileDialog("Load Modeline",d,"load","",self._do_load_ml)

    def _do_load_ml(self,path):
        try:
            with open(path) as f: lines=f.readlines()
            for line in lines:
                s=line.strip()
                if s.startswith("Modeline"):
                    parts=s.split('"')
                    if len(parts)>=3:
                        self.ti_import.set_value(parts[2].strip())
                        self._import_modeline(parts[2].strip()); return
            self.status="No Modeline in file"; self.status_col=RED_C
        except Exception as e: self.status=f"Load error: {e}"; self.status_col=RED_C

    def _modeline_str_rg(self, rg):
        istr=" interlace" if rg["interlaced"] else ""
        return (f"{rg['pclk']:.6f} {rg['X1']} {rg['X2']} {rg['X3']} {rg['X4']} "
                f"{rg['Y1']} {rg['Y2']} {rg['Y3']} {rg['Y4']}{istr} -hsync -vsync")


    def _calc(self):
        try:
            H=self.sw_width.get_value(); V=self.sw_height.get_value()
            Hf=self.sw_hfreq.get_value()*1000; Vf=self.sw_vfreq.get_value()
            i=self.chk_interlaced.checked; rl=self._make_rl()
            self._res=calculate_from_range(H,V,Hf,Vf,i,rl); self._r_live=rl
            res=self._res
            self.sw_hfp_px.set_value(res["HFP"]); self.sw_hs_px.set_value(res["HSYNC"])
            self.sw_hbp_px.set_value(res["HBP"]); self.sw_vfp_px.set_value(res["VFP"])
            self.sw_vs_px.set_value(res["VSYNC"]); self.sw_vbp_px.set_value(res["VBP"])
        except: pass

    def _from_pixels(self):
        try:
            H=self.sw_width.get_value(); V=self.sw_height.get_value()
            Hf=self.sw_hfreq.get_value()*1000; i=self.chk_interlaced.checked; Div=2 if i else 1
            r=self._current_range or PRESETS["Arcade 15kHz"]["ranges"][0]
            HFP=self.sw_hfp_px.get_value(); HSYNC=self.sw_hs_px.get_value()
            HBP=self.sw_hbp_px.get_value(); VFP=self.sw_vfp_px.get_value()
            VSYNC=self.sw_vs_px.get_value(); VBP=self.sw_vbp_px.get_value()
            H_tot=H+HFP+HSYNC+HBP; V_tot=V+VFP+VSYNC+VBP
            pclk=Hf*H_tot/1e6; Vf_act=Hf*Div/V_tot
            self.sw_hfp.set_value(round(HFP/H_tot/Hf*1e6,3)); self.sw_hs.set_value(round(HSYNC/H_tot/Hf*1e6,3))
            self.sw_hbp.set_value(round(HBP/H_tot/Hf*1e6,3)); self.sw_vfp.set_value(round(VFP/V_tot/Vf_act*1e3,3))
            self.sw_vs.set_value(round(VSYNC/V_tot/Vf_act*1e3,3)); self.sw_vbp.set_value(round(VBP/V_tot/Vf_act*1e3,3))
            self._res=dict(X1=H,X2=H+HFP,X3=H+HFP+HSYNC,X4=H_tot,
                           Y1=V,Y2=V+VFP,Y3=V+VFP+VSYNC,Y4=V_tot,
                           HFP=HFP,HSYNC=HSYNC,HBP=HBP,VFP=VFP,VSYNC=VSYNC,VBP=VBP,
                           pclk=pclk,Hfreq=Hf,Vfreq_actual=Vf_act,interlaced=i)
        except: pass

    def _parse_paste(self):
        raw=self.ti_paste.value.strip()
        raw=re.sub(r'^crt_range\d*\s*','',raw).strip()
        parts=[p.strip() for p in raw.split(',')]
        if len(parts)<14: self.status="Parse error: need 14 fields"; self.status_col=RED_C; return
        try:
            hr=parts[0].split('-'); hmin,hmax=float(hr[0]),float(hr[1])
            vr=parts[1].split('-'); vfmin,vfmax=float(vr[0]),float(vr[1])
            hfp,hs,hbp=float(parts[2]),float(parts[3]),float(parts[4])
            vfp,vs,vbp=float(parts[5]),float(parts[6]),float(parts[7])
            pLmin,pLmax=int(float(parts[10])),int(float(parts[11]))
            iLmin,iLmax=int(float(parts[12])),int(float(parts[13]))
        except Exception as e: self.status=f"Parse error: {e}"; self.status_col=RED_C; return
        r={"lb":"custom","hmin":hmin,"hmax":hmax,"vfmin":vfmin,"vfmax":vfmax,
           "hfp":hfp,"hs":hs,"hbp":hbp,"vfp":vfp,"vs":vs,"vbp":vbp,
           "pLmin":pLmin,"pLmax":pLmax,"iLmin":iLmin,"iLmax":iLmax}
        self._current_range=r; self._custom_mode=True
        self._fixed_range=dict(r)
        self.sw_hfp.set_value(hfp); self.sw_hs.set_value(hs); self.sw_hbp.set_value(hbp)
        self.sw_vfp.set_value(vfp); self.sw_vs.set_value(vs); self.sw_vbp.set_value(vbp)
        self.sw_hfreq.set_value((hmin+hmax)/2/1000)
        self.dd_range.options=["custom"]; self.dd_range.selected=0
        self._calc(); self.status="CRT Range parsed — Custom mode"; self.status_col=GREEN_C

    def _modeline_str(self):
        rg=getattr(self,'_rg',self._res)
        if not rg: return ""
        istr=" interlace" if rg["interlaced"] else ""
        return (f"{rg['pclk']:.6f} {rg['X1']} {rg['X2']} {rg['X3']} {rg['X4']} "
                f"{rg['Y1']} {rg['Y2']} {rg['Y3']} {rg['Y4']}{istr} -hsync -vsync")

    def _xrandr_str(self):
        if not self._res: return ""
        rg=getattr(self,'_rg',self._res)
        if not rg: return ""
        i=rg["interlaced"]; H=rg["X1"]; V=rg["Y1"]; name=f"{H}x{V}{'i' if i else ''}"
        ml=self._modeline_str(); out=self.ti_output.value or "DP-1"
        return (f'xrandr --newmode "{name}" {ml}\n'
                f'xrandr --addmode {out} "{name}"\n'
                f'xrandr --output {out} --mode "{name}"')

    def _copy_xrandr(self):
        try:
            xr=self._xrandr_str()
            subprocess.run(["xclip","-selection","clipboard"],input=xr.encode(),check=True)
            self.status="Copied!"; self.status_col=GREEN_C
        except:
            self.status="xclip not available"; self.status_col=YELLOW

    def _apply_xrandr(self):
        xr=self._xrandr_str()
        if not xr: return
        for cmd in [l for l in xr.split("\n") if l.strip()]:
            try: subprocess.run(cmd.split(),check=True)
            except Exception as e: self.status=f"Error: {e}"; self.status_col=RED_C; return
        self.status="Modeline applied!"; self.status_col=GREEN_C

    def _optimise(self):
        try:
            H=self.sw_width.get_value(); V=self.sw_height.get_value()
            Hf=self.sw_hfreq.get_value()*1000; Vf=self.sw_vfreq.get_value()
            i=self.chk_interlaced.checked; rl=self._make_rl()
            res=optimize_modeline(H,V,Hf,Vf,i,rl); t=calc_timings(res)
            self.sw_hfp.set_value(round(t["HFP_us"],3)); self.sw_hs.set_value(round(t["HSYNC_us"],3))
            self.sw_hbp.set_value(round(t["HBP_us"],3)); self.sw_vfp.set_value(round(t["VFP_ms"],3))
            self.sw_vs.set_value(round(t["VSYNC_ms"],3)); self.sw_vbp.set_value(round(t["VBP_ms"],3))
            self.sw_hfp_px.set_value(res["HFP"]); self.sw_hs_px.set_value(res["HSYNC"])
            self.sw_hbp_px.set_value(res["HBP"]); self.sw_vfp_px.set_value(res["VFP"])
            self.sw_vs_px.set_value(res["VSYNC"]); self.sw_vbp_px.set_value(res["VBP"])
            # Apply Δ VFP if enabled
            if self.chk_vfp_lock.checked:
                try: vfp_val=int(float(self.ti_vfp_val.value))
                except: vfp_val=0
                if vfp_val!=0:
                    new_vfp=vfp_val if vfp_val>0 else max(1,res["VFP"]+vfp_val)
                    new_vbp=res["VBP"]+(res["VFP"]-new_vfp)
                    if new_vbp>=1 and new_vfp>=1:
                        res["VFP"]=new_vfp; res["VBP"]=new_vbp
                        res["Y2"]=res["Y1"]+new_vfp; res["Y3"]=res["Y2"]+res["VSYNC"]
                        res["Y4"]=res["Y3"]+new_vbp
                        Div_r=2 if i else 1; line_ms=1000.0/(Hf*Div_r)
                        vb=( new_vfp+res["VSYNC"]+new_vbp)*line_ms; thr=22500.0/rl["hmax"]
                        res["switchres_ok"]=vb<thr; res["vblank_ms"]=vb; res["threshold_ms"]=thr
            self._res=res; self._r_live=rl
            self._refresh_display(res,rl)
            ve=res.get("Vfreq_error",0)
            sr_ok=res.get("switchres_ok",True)
            sr=" SR✓" if sr_ok else " SR✗"
            self.status=f"Optimised — Vfreq err: {ve:.6f} Hz{sr}"
            self.status_col=GREEN_C if (ve<1e-6 and sr_ok) else YELLOW
        except Exception as e: self.status=f"Error: {e}"; self.status_col=RED_C

    def _save(self):
        if not self._res: return
        rg=getattr(self,"_rg",self._res)
        name=f"crt_range_{rg['X1']}x{rg['Y1']}{'i' if rg['interlaced'] else ''}"
        d="/userdata" if os.path.isdir("/userdata") else os.path.expanduser("~")
        self.dialog=FileDialog("Save CRT Range",d,"save",name,self._do_save_crt)

    def _do_save_crt(self,path):
        res=getattr(self,"_rg",self._res); r=self._r_live or {}; t=calc_timings(res)
        name=f"{res['X1']}x{res['Y1']}{'i' if res['interlaced'] else ''}"
        crt_calc=fmt_crt_range(r,t["HFP_us"],t["HSYNC_us"],t["HBP_us"],
                                 t["VFP_ms"],t["VSYNC_ms"],t["VBP_ms"])
        try:
            with open(path,"w") as f:
                f.write(f"# CRT Modeline Toolbox — {name}\n\n")
                f.write(f"# Calculated\n{crt_calc}\n\n")
                f.write(f"# Modeline\nModeline \"{name}\" {self._modeline_str()}\n\n")
                f.write(f"# xrandr\n{self._xrandr_str()}\n")
            self.status=f"Saved: {path}"; self.status_col=GREEN_C
        except Exception as e: self.status=f"Save error: {e}"; self.status_col=RED_C

    def _load(self):
        d="/userdata" if os.path.isdir("/userdata") else os.path.expanduser("~")
        self.dialog=FileDialog("Load CRT Range",d,"load","",self._do_load_crt)

    def _do_load_crt(self,path):
        try:
            with open(path) as f: lines=f.readlines()
            for line in lines:
                s=line.strip()
                if s.startswith("crt_range"):
                    self.ti_paste.set_value(s); self._parse_paste(); return
            self.status="No crt_range in file"; self.status_col=RED_C
        except Exception as e: self.status=f"Load error: {e}"; self.status_col=RED_C

    # ── DRAW ─────────────────────────────────────────────────────────────────
    def draw(self):
        # Draw on canvas, then blit centered on screen
        self.canvas.fill(BG); self._draw_tabs()
        if self.current_tab==0: self._draw_setup()
        elif self.current_tab==1: self._draw_crt_range()
        elif self.current_tab==2: self._draw_results()
        elif self.current_tab==3: self._draw_verify()
        elif self.current_tab==4: self._draw_diagram()
        # Overlay: draw any open dropdown popup on top (correct z-order)
        self._draw_open_dropdown()
        self._draw_status()
        self.screen.fill((0,0,0))
        self.screen.blit(self.canvas,(self.cx,self.cy))
        if self.dialog and self.dialog.active:
            self.dialog.draw(self.screen,self.scr_w,self.scr_h)
        pygame.display.flip()

    def _draw_open_dropdown(self):
        """Draw open dropdown popup as overlay on canvas (above scroll content)."""
        dds=[]
        if self.current_tab==0: dds=[self.dd_preset,self.dd_range]
        elif self.current_tab==3: dds=[self.dd_verify_mon]
        for dd in dds:
            if dd.open:
                sa=self.scroll[self.current_tab]
                # Map scroll-surface y → canvas y
                oy=sa.rect.y - sa.scroll_y
                dd.draw_popup(self.canvas,oy)
                break

    def _draw_tabs(self):
        tw=self.W//len(self.TABS)
        tab_bar_focused=getattr(self,'_tab_focused',False)
        for i,name in enumerate(self.TABS):
            r=pygame.Rect(i*tw,0,tw-1,self.TAB_H)
            draw_rect(self.canvas,r,BG2 if i==self.current_tab else BG3,radius=3)
            if i==self.current_tab:
                col=(255,220,0) if tab_bar_focused else ACCENT
                draw_rect(self.canvas,pygame.Rect(r.x,r.bottom-3,r.w,3),col)
            draw_text(self.canvas,name,r.centerx,r.centery,FG,12,
                      bold=(i==self.current_tab),anchor="center")
        if tab_bar_focused:
            draw_text(self.canvas,"← → change tab",self.W//2,self.TAB_H+2,
                      (255,220,0),9,anchor="midtop")

    def _draw_status(self):
        y=self.H_WIN-self.STATUS_H
        draw_rect(self.canvas,pygame.Rect(0,y,self.W,self.STATUS_H),BG3)
        draw_text(self.canvas,self.status,6,y+2,self.status_col,10)
        if self._res:
            res=self._res
            info=f"pclk={res['pclk']:.4f}MHz  Hf={res['Hfreq']/1000:.3f}kHz  Vf={res['Vfreq_actual']:.3f}Hz  Htot={res['X4']}  Vtot={res['Y4']}"
            draw_text(self.canvas,info,self.W//2,y+2,FG2,9,anchor="midtop")

    def _draw_scrollable(self,tab_idx,content_h,draw_fn):
        sa=self.scroll[tab_idx]
        # Use a generous surface, let draw_fn report real height
        sa.begin(max(content_h,800))
        real_h=draw_fn(sa.surf)
        if real_h: sa.content_h=max(real_h+10,sa.rect.h)
        sa.scroll_y=max(0,min(sa.scroll_y,max(0,sa.content_h-sa.rect.h)))
        sa.end(self.canvas)

    def _draw_setup(self):
        def fn(surf):
            y=4
            # Monitor / Range row
            draw_text(surf,"Monitor:",6,y+5,FG2,11); self.dd_preset.draw(surf)
            draw_text(surf,"Range:",228,y+5,FG2,11); self.dd_range.draw(surf)
            self.chk_interlaced.draw(surf)
            draw_text(surf,"Out:",390,y+5,FG2,11); self.ti_output.draw(surf)
            y+=30; draw_rect(surf,pygame.Rect(6,y-2,self.W-12,1),BG3)
            # Parameters
            draw_text(surf,"Parameters",6,y+2,ACCENT,11,bold=True); y+=18
            for sw in (self.sw_width,self.sw_height,self.sw_hfreq,self.sw_vfreq):
                sw.label_rect.y=y; sw.entry.rect.y=y+4; sw.slider.rect.y=y+6
                sw.draw(surf); y+=SliderRow.H+2
            y+=4; draw_rect(surf,pygame.Rect(6,y,self.W-12,1),BG3); y+=4
            # Paste CRT Range + Import Modeline
            draw_text(surf,"Paste CRT Range / Import Modeline",6,y+2,ACCENT,11,bold=True); y+=16
            self.ti_paste.rect.y=y; self.btn_parse.rect.y=y
            self.ti_paste.draw(surf); self.btn_parse.draw(surf); y+=26
            self.ti_import.rect.y=y; self.btn_import.rect.y=y
            draw_text(surf,"ML:",6,y+5,FG2,11)
            self.ti_import.rect.x=30; self.ti_import.rect.y=y
            self.ti_import.draw(surf); self.btn_import.draw(surf); y+=28
            draw_rect(surf,pygame.Rect(6,y,self.W-12,1),BG3); y+=4
            # Direct Porch (px/lines)
            draw_text(surf,"Direct Porch (px / lines)",6,y+2,ACCENT,11,bold=True); y+=16
            for sw in (self.sw_hfp_px,self.sw_hs_px,self.sw_hbp_px,
                       self.sw_vfp_px,self.sw_vs_px,self.sw_vbp_px):
                sw.label_rect.y=y; sw.entry.rect.y=y+4; sw.slider.rect.y=y+6
                sw.draw(surf); y+=SliderRow.H+2
            y+=4; draw_rect(surf,pygame.Rect(6,y,self.W-12,1),BG3); y+=4
            # Geometry — 4 horizontal compact spinboxes
            draw_text(surf,"Geometry  -g  h_size:h_shift:v_shift",6,y+2,ACCENT,11,bold=True); y+=14
            gx=6; gs=GeoSpin.W+10
            for i,spn in enumerate((self.geo_hmove,self.geo_vmove,self.geo_hsize,self.geo_vsize)):
                spn.move(gx+i*gs,y)
                spn.draw(surf)
            y+=GeoSpin.H+4
            # Geo info line
            rg=getattr(self,"_rg",None)
            if rg:
                hmc=getattr(self,"_hmove_clamped",0)
                sr=f"{self.geo_hsize.get_value():.2f}:{hmc}:{int(self.geo_vmove.get_value())}"
                info=f"HFP={rg['HFP']} HBP={rg['HBP']} VFP={rg['VFP']} VBP={rg['VBP']}  -g \"{sr}\""
                draw_text(surf,info,gx,y,YELLOW,10); y+=14
            return y
        self._draw_scrollable(0,self._setup_h,fn)

    def _draw_crt_range(self):
        def fn(surf):
            y=4
            draw_text(surf,"CRT Range (µs / ms)",6,y,ACCENT,11,bold=True); y+=16
            for sw in (self.sw_hfp,self.sw_hs,self.sw_hbp,self.sw_vfp,self.sw_vs,self.sw_vbp):
                sw.label_rect.y=y; sw.entry.rect.y=y+4; sw.slider.rect.y=y+6
                sw.draw(surf); y+=SliderRow.H+2
            y+=8; draw_rect(surf,pygame.Rect(6,y,self.W-12,1),BG3); y+=6
            # CRT Range — Calamity (fixed to preset) — compact single block
            draw_text(surf,"CRT Range — Calamity (fixed to preset):",6,y,ACCENT,10,bold=True); y+=13
            fr=getattr(self,"_fixed_range",None)
            if fr:
                fixed_str=fmt_crt_range(fr,fr["hfp"],fr["hs"],fr["hbp"],fr["vfp"],fr["vs"],fr["vbp"])
                draw_text(surf,fixed_str,6,y,YELLOW,8); y+=12
            else:
                draw_text(surf,"(custom mode — no preset)",6,y,FG2,9); y+=12
            y+=4; draw_rect(surf,pygame.Rect(6,y,self.W-12,1),BG3); y+=6
            draw_text(surf,"Timings",6,y,ACCENT,11,bold=True); y+=16
            if self._res:
                res=self._res; t=calc_timings(res)
                rows=[("H active",f"{res['X1']}px",f"{t['H_actif_us']:.3f}µs"),
                      ("H Front Porch",f"{res['HFP']}px",f"{t['HFP_us']:.3f}µs"),
                      ("H Sync",f"{res['HSYNC']}px",f"{t['HSYNC_us']:.3f}µs"),
                      ("H Back Porch",f"{res['HBP']}px",f"{t['HBP_us']:.3f}µs"),
                      ("H total",f"{res['X4']}px",f"{t['H_total_us']:.3f}µs"),
                      ("","",""),
                      ("V active",f"{res['Y1']}px",f"{t['V_actif_ms']:.3f}ms"),
                      ("V Front Porch",f"{res['VFP']}px",f"{t['VFP_ms']:.3f}ms"),
                      ("V Sync",f"{res['VSYNC']}px",f"{t['VSYNC_ms']:.3f}ms"),
                      ("V Back Porch",f"{res['VBP']}px",f"{t['VBP_ms']:.3f}ms"),
                      ("V total",f"{res['Y4']}px",f"{t['V_total_ms']:.3f}ms")]
                for label,px,tim in rows:
                    if label:
                        draw_text(surf,label,18,y,FG2,11)
                        draw_text(surf,px,230,y,YELLOW,11,anchor="topleft")
                        draw_text(surf,tim,310,y,FG,11,anchor="topleft")
                    y+=16
            return y
        self._draw_scrollable(1,self._crt_range_h,fn)

    def _draw_results(self):
        def fn(surf):
            y=4
            # Row 1: Copy | Apply | Optimise | ☐ Δ VFP [entry]
            for btn in (self.btn_copy,self.btn_apply,self.btn_opt):
                btn.rect.y=y; btn.draw(surf)
            self.chk_vfp_lock.rect.y=y+3; self.chk_vfp_lock.draw(surf)
            self.ti_vfp_val.rect.y=y+1; self.ti_vfp_val.draw(surf)
            y+=28
            # Row 2: Save/Load CRT | Save/Load Modeline
            for btn in (self.btn_save,self.btn_load,self.btn_save_ml,self.btn_load_ml):
                btn.rect.y=y; btn.draw(surf)
            y+=28; draw_rect(surf,pygame.Rect(6,y,self.W-12,1),BG3); y+=6
            if not self._res:
                draw_text(surf,"No modeline — calculate first",self.W//2,y+20,FG2,12,anchor="midtop"); return
            res=self._res; r=self._r_live or {}; t=calc_timings(res)
            Hf=res["Hfreq"]; Va=res["Vfreq_actual"]; i=res["interlaced"]
            H=res["X1"]; V=res["Y1"]
            draw_text(surf,"pclk",6,y,FG2,10); draw_text(surf,f"{res['pclk']:.6f} MHz",55,y,FG,10)
            draw_text(surf,"Hfreq",200,y,FG2,10); draw_text(surf,f"{Hf/1000:.6f} kHz",248,y,FG,10)
            draw_text(surf,"Vfreq",390,y,FG2,10); draw_text(surf,f"{Va:.6f} Hz",435,y,FG,10)
            y+=14
            draw_text(surf,"H total",6,y,FG2,10); draw_text(surf,f"{res['X4']}px",55,y,FG,10)
            draw_text(surf,"V total",200,y,FG2,10); draw_text(surf,f"{res['Y4']}px",248,y,FG,10)
            draw_text(surf,"Interlaced" if i else "Progressive",390,y,ACCENT,10)
            y+=18
            hok=r.get("hmin",0)<=Hf<=r.get("hmax",99999)
            vok=r.get("vfmin",0)<=Va<=r.get("vfmax",999)
            lok=(r.get("iLmin",0)<=V<=r.get("iLmax",9999) if i and r.get("iLmax",0)>0
                 else r.get("pLmin",0)<=V<=r.get("pLmax",9999))
            for ok,txt in [(hok,f"Hfreq {Hf/1000:.3f}kHz"),(vok,f"Vfreq {Va:.3f}Hz"),(lok,f"V={V}px")]:
                col=GREEN_C if ok else RED_C
                draw_text(surf,"✓" if ok else "✗",6,y,col,12); draw_text(surf,txt,20,y,col,11); y+=14
            # SR V-blank indicator
            sr_ok=res.get("switchres_ok",True)
            vb=res.get("vblank_ms",0); thr=res.get("threshold_ms",1.43)
            sr_col=GREEN_C if sr_ok else RED_C
            sr_sym="✓" if sr_ok else "✗"
            draw_text(surf,f"SR V-blank: {vb:.3f}/{thr:.3f} ms {sr_sym}",6,y,sr_col,10); y+=14
            y+=4
            crt_calc=fmt_crt_range(r,t["HFP_us"],t["HSYNC_us"],t["HBP_us"],t["VFP_ms"],t["VSYNC_ms"],t["VBP_ms"])
            draw_text(surf,"CRT Range (calculated):",6,y,ACCENT,10,bold=True); y+=13
            draw_text(surf,crt_calc,6,y,YELLOW,9); y+=13; y+=4
            name=f"{H}x{V}{'i' if i else ''}"; ml=self._modeline_str()
            draw_text(surf,"Modeline:",6,y,ACCENT,10,bold=True); y+=13
            draw_text(surf,f'"{name}" {ml}',6,y,YELLOW,9); y+=13; y+=4
            draw_text(surf,"xrandr commands:",6,y,ACCENT,10,bold=True); y+=13
            for line in self._xrandr_str().split("\n"):
                draw_text(surf,line,6,y,FG,9); y+=12
            return y
        self._draw_scrollable(2,460,fn)

    def _draw_verify(self):
        def fn(surf):
            y=4
            draw_text(surf,"Modeline to verify:",6,y,ACCENT,11,bold=True); y+=14
            self.ti_verify.rect.y=y; self.btn_verify.rect.y=y-1; self.btn_verify_load.rect.y=y-1
            self.ti_verify.draw(surf); self.btn_verify.draw(surf); self.btn_verify_load.draw(surf); y+=30
            draw_text(surf,"Monitor:",6,y+4,FG2,11)
            self.dd_verify_mon.rect.y=y; self.dd_verify_mon.draw(surf); y+=30
            draw_rect(surf,pygame.Rect(6,y,self.W-12,1),BG3); y+=8
            res=self._verify_res
            if not res:
                draw_text(surf,"Paste a modeline and press Verify",self.W//2,y+20,FG2,11,anchor="midtop")
                return y+40
            # Metrics
            draw_text(surf,"Metrics",6,y,ACCENT,11,bold=True); y+=15
            draw_text(surf,f"pclk {res['pclk']:.6f} MHz   Hfreq {res['Hfreq']/1000:.4f} kHz   Vfreq {res['Vfreq_actual']:.4f} Hz",
                      12,y,FG,10); y+=14
            draw_text(surf,f"H total {res['X4']} px   V total {res['Y4']} px   {'Interlaced' if res['interlaced'] else 'Progressive'}",
                      12,y,FG,10); y+=18
            # Porches
            draw_text(surf,"Porches",6,y,ACCENT,11,bold=True); y+=15
            draw_text(surf,f"H: active {res['X1']}  FP {res['HFP']}  Sync {res['HSYNC']}  BP {res['HBP']}",12,y,FG,10); y+=14
            draw_text(surf,f"V: active {res['Y1']}  FP {res['VFP']}  Sync {res['VSYNC']}  BP {res['VBP']}",12,y,FG,10); y+=18
            # Verification vs selected monitor
            draw_text(surf,"Verification",6,y,ACCENT,11,bold=True); y+=15
            mon=self.dd_verify_mon.value
            p=PRESETS.get(mon)
            if p:
                r=select_range(mon,res["Hfreq"])
                Hf=res["Hfreq"]; Va=res["Vfreq_actual"]; i=res["interlaced"]; V=res["Y1"]
                hok=r["hmin"]<=Hf<=r["hmax"]; vok=r["vfmin"]<=Va<=r["vfmax"]
                lok=(r["iLmin"]<=V<=r["iLmax"] if i and r["iLmax"]>0 else r["pLmin"]<=V<=r["pLmax"])
                checks=[(hok,f"Hfreq {Hf/1000:.3f} kHz in [{r['hmin']/1000:.2f}-{r['hmax']/1000:.2f}]"),
                        (vok,f"Vfreq {Va:.3f} Hz in [{r['vfmin']:.1f}-{r['vfmax']:.1f}]"),
                        (lok,f"V lines {V} in [{r['iLmin'] if i else r['pLmin']}-{r['iLmax'] if i else r['pLmax']}]")]
                for ok,txt in checks:
                    col=GREEN_C if ok else RED_C
                    draw_text(surf,("✓ " if ok else "✗ ")+txt,12,y,col,10); y+=14
                # SR V-blank
                Div=2 if i else 1; line_ms=1000.0/(Hf*Div)
                vb=(res["VFP"]+res["VSYNC"]+res["VBP"])*line_ms; thr=22500.0/r["hmax"]
                col=GREEN_C if vb<thr else RED_C
                draw_text(surf,("✓ " if vb<thr else "✗ ")+f"SR V-blank {vb:.3f}/{thr:.3f} ms",12,y,col,10); y+=14
                allok=hok and vok and lok and vb<thr
                draw_text(surf,"► MODELINE VALID" if allok else "► OUT OF RANGE",12,y+4,
                          GREEN_C if allok else RED_C,12,bold=True); y+=22
            return y
        self._draw_scrollable(3,500,fn)

    def _draw_diagram(self):
        if not self._res:
            draw_text(self.canvas,"No modeline — calculate first",
                      self.W//2,self._cy()+60,FG2,13,anchor="midtop"); return
        res=self._res; t=calc_timings(res)
        H_total=res["X4"]; V_total=res["Y4"]
        H=res["X1"]; V=res["Y1"]
        HBP=res["HBP"]; HFP=res["HFP"]; HSYNC=res["HSYNC"]
        VBP=res["VBP"]; VFP=res["VFP"]; VSYNC=res["VSYNC"]
        CY=self._cy(); CA=self.H_WIN-CY-self.STATUS_H-4; CW=self.W
        sx=CW/H_total; sy=CA/V_total
        x_act=round(HBP*sx); x_hfp=round((HBP+H)*sx); x_sync=round((HBP+H+HFP)*sx)
        y_act=CY+round(VBP*sy); y_vfp=CY+round((VBP+V)*sy)
        MIN=4
        vfp_h=max(round(VFP*sy),MIN); vsync_h=max(round(VSYNC*sy),MIN)
        y_sync=min(y_vfp+vfp_h,CY+CA-vsync_h)

        def r(x0,y0,x1,y1,col): pygame.draw.rect(self.canvas,col,pygame.Rect(x0,y0,x1-x0,y1-y0))
        r(0,CY,CW,y_act,C_VBP); r(x_act,y_act,x_hfp,y_vfp,C_ACT)
        r(0,y_act,x_act,CY+CA,C_HBP); r(x_hfp,y_act,x_sync,CY+CA,C_HFP)
        r(x_sync,y_act,CW,CY+CA,C_HSYNC); r(x_act,y_vfp,x_hfp,y_sync,C_VFP)
        r(x_act,y_sync,x_hfp,CY+CA,C_VSYNC)

        cx=(x_act+x_hfp)//2
        def lbl(x,y,txt,col=WHITE,sz=10): draw_text(self.canvas,txt,x,y,col,sz,anchor="center")
        lbl(cx,CY+(y_act-CY)//2,f"V Back Porch  {VBP}px / {t['VBP_ms']:.3f}ms")
        if x_act>28: lbl(x_act//2,(y_act+CY+CA)//2,f"HBP\n{HBP}px")
        if CW-x_sync>18: lbl((x_sync+CW)//2,(y_act+CY+CA)//2,f"HS\n{HSYNC}px",(50,50,80))
        if y_sync-y_vfp>10: lbl(cx,(y_vfp+y_sync)//2,f"VFP {VFP}px")
        if CY+CA-y_sync>8: lbl(cx,(y_sync+CY+CA)//2,f"VS {VSYNC}px",(100,60,60))
        lbl(cx,y_act+14,f"Active  {H} × {V}",WHITE,14)
        lbl(cx,y_act+30,f"pclk {res['pclk']:.3f}MHz  Hf {res['Hfreq']/1000:.3f}kHz  Vf {res['Vfreq_actual']:.3f}Hz",WHITE,10)
        lx_h=cx-190; lx_v=cx+10; ly=y_act+48; dy=15
        draw_text(self.canvas,"── Horizontal ──",lx_h+12,ly-12,WHITE,9,bold=True)
        draw_text(self.canvas,"── Vertical ──",  lx_v+12,ly-12,WHITE,9,bold=True)
        h_rows=[(C_ACT,"H active",H,t['H_actif_us'],"µs"),(C_HBP,"H Back",HBP,t['HBP_us'],"µs"),
                (C_HFP,"H Front",HFP,t['HFP_us'],"µs"),(C_HSYNC,"H Sync",HSYNC,t['HSYNC_us'],"µs"),
                (YELLOW,"H total",H_total,t['H_total_us'],"µs")]
        v_rows=[(C_ACT,"V active",V,t['V_actif_ms'],"ms"),(C_VBP,"V Back",VBP,t['VBP_ms'],"ms"),
                (C_VFP,"V Front",VFP,t['VFP_ms'],"ms"),(C_VSYNC,"V Sync",VSYNC,t['VSYNC_ms'],"ms"),
                (YELLOW,"V total",V_total,t['V_total_ms'],"ms")]
        for j,(col,lbl_,num,tim,unit) in enumerate(h_rows):
            y2=ly+j*dy; pygame.draw.rect(self.canvas,col,pygame.Rect(lx_h,y2-1,8,8))
            draw_text(self.canvas,lbl_,lx_h+12,y2,WHITE,9)
            draw_text(self.canvas,f"{num}px",lx_h+88,y2,WHITE,9,anchor="topright")
            draw_text(self.canvas,f"{tim:.2f}{unit}",lx_h+94,y2,(200,200,200),9)
        for j,(col,lbl_,num,tim,unit) in enumerate(v_rows):
            y2=ly+j*dy; pygame.draw.rect(self.canvas,col,pygame.Rect(lx_v,y2-1,8,8))
            draw_text(self.canvas,lbl_,lx_v+12,y2,WHITE,9)
            draw_text(self.canvas,f"{num}px",lx_v+88,y2,WHITE,9,anchor="topright")
            draw_text(self.canvas,f"{tim:.2f}{unit}",lx_v+94,y2,(200,200,200),9)

    # ── EVENTS ───────────────────────────────────────────────────────────────
    def _nav_widgets(self):
        """Ordered list: None at index 0 = tab bar, then widgets."""
        t=self.current_tab
        if t==0:
            return [None,
                    self.dd_preset,self.dd_range,self.chk_interlaced,
                    self.sw_width,self.sw_height,self.sw_hfreq,self.sw_vfreq,
                    self.btn_parse,self.btn_import,
                    self.sw_hfp_px,self.sw_hs_px,self.sw_hbp_px,
                    self.sw_vfp_px,self.sw_vs_px,self.sw_vbp_px,
                    self.geo_hmove,self.geo_vmove,self.geo_hsize,self.geo_vsize]
        elif t==1:
            return [None,
                    self.sw_hfp,self.sw_hs,self.sw_hbp,
                    self.sw_vfp,self.sw_vs,self.sw_vbp]
        elif t==2:
            return [None,
                    self.btn_copy,self.btn_apply,self.btn_opt,
                    self.chk_vfp_lock,self.ti_vfp_val,
                    self.btn_save,self.btn_load,
                    self.btn_save_ml,self.btn_load_ml]
        elif t==3:
            return [None,self.ti_verify,self.btn_verify,self.btn_verify_load,self.dd_verify_mon]
        return [None]

    def _set_focus(self,idx):
        widgets=self._nav_widgets()
        idx=idx%len(widgets)
        for i,w in enumerate(widgets):
            if w is None: continue
            if isinstance(w,TextInput):
                w.nav_hl=(i==idx)
                if i!=idx: w.focused=False
            else:
                w.focused=(i==idx)
        self._focus_per_tab[self.current_tab]=idx
        self._tab_focused=(idx==0)
        self._autoscroll_to(widgets[idx])

    def _widget_y(self,w):
        """Get widget Y position in scroll surface."""
        if w is None: return 0
        if hasattr(w,'label_rect'): return w.label_rect.y
        if hasattr(w,'_y'): return w._y
        if hasattr(w,'rect'): return w.rect.y
        return 0

    def _autoscroll_to(self,w):
        """Scroll so focused widget is visible."""
        sa=self.scroll[self.current_tab]
        if w is None:
            sa.scroll_y=0; return
        widgets=self._nav_widgets()
        idx=self._focus_per_tab[self.current_tab]
        wy=self._widget_y(w)
        vis_h=sa.rect.h; margin=40
        # If last focusable widget, scroll to bottom to reveal trailing content
        if idx==len(widgets)-1:
            sa.scroll_y=max(0,sa.content_h-vis_h)
            return
        if wy < sa.scroll_y+margin:
            sa.scroll_y=max(0,wy-margin)
        elif wy > sa.scroll_y+vis_h-margin*2:
            sa.scroll_y=min(max(0,sa.content_h-vis_h),wy-vis_h+margin*3)

    def _manual_scroll(self,delta):
        """Scroll current tab content by delta px (keyboard/joystick)."""
        sa=self.scroll[self.current_tab]
        sa.scroll_y=max(0,min(sa.scroll_y+delta,max(0,sa.content_h-sa.rect.h)))

    def _focused_widget(self):
        widgets=self._nav_widgets()
        idx=self._focus_per_tab[self.current_tab]%max(1,len(widgets))
        return widgets[idx]  # None = tab bar

    def _nav_next(self,d=1):
        widgets=self._nav_widgets()
        if not widgets: return
        idx=(self._focus_per_tab[self.current_tab]+d)%len(widgets)
        self._set_focus(idx)

    def _activate_focused(self):
        w=self._focused_widget()
        if w is None: return
        if isinstance(w,Button): w.activate()
        elif isinstance(w,Checkbox): w.activate()
        elif isinstance(w,Dropdown): w.activate()
        elif isinstance(w,GeoSpin): w.entry.focused=True
        elif isinstance(w,SliderRow): w.entry.focused=True
        elif isinstance(w,TextInput): w.focused=True

    def _nudge_focused(self,direction,fast=False):
        w=self._focused_widget()
        if w is None:
            self.current_tab=(self.current_tab+direction)%len(self.TABS)
            self._focus_per_tab[self.current_tab]=0
            self._set_focus(0); return
        if isinstance(w,SliderRow):
            w.slider.nudge(direction,fast)
            w.entry.set_value(w._fmt(w.slider.value))
        elif isinstance(w,GeoSpin):
            w.nudge(direction,fast)
        elif isinstance(w,Dropdown):
            n=len(w.options); w.selected=(w.selected+direction)%n
            if w.callback: w.callback(w.options[w.selected])

    def _handle_joy(self):
        if not self._joy: return
        # Read axes (left stick or D-pad)
        ax=0; ay=0
        try:
            ax=self._joy.get_axis(0); ay=self._joy.get_axis(1)
        except: pass
        DEAD=0.4
        self._joy_axis_x=1 if ax>DEAD else (-1 if ax<-DEAD else 0)
        self._joy_axis_y=1 if ay>DEAD else (-1 if ay<-DEAD else 0)

    def _widgets_for_tab(self,tab):
        if tab==0:
            return [self.dd_preset,self.dd_range,self.chk_interlaced,self.ti_output,
                    self.sw_width,self.sw_height,self.sw_hfreq,self.sw_vfreq,
                    self.ti_paste,self.btn_parse,self.ti_import,self.btn_import,
                    self.sw_hfp_px,self.sw_hs_px,self.sw_hbp_px,
                    self.sw_vfp_px,self.sw_vs_px,self.sw_vbp_px,
                    self.geo_hmove,self.geo_vmove,self.geo_hsize,self.geo_vsize]
        elif tab==1:
            return [self.sw_hfp,self.sw_hs,self.sw_hbp,self.sw_vfp,self.sw_vs,self.sw_vbp]
        elif tab==2:
            return [self.btn_copy,self.btn_apply,self.btn_opt,
                    self.chk_vfp_lock,self.ti_vfp_val,
                    self.btn_save,self.btn_load,self.btn_save_ml,self.btn_load_ml]
        elif tab==3:
            return [self.ti_verify,self.btn_verify,self.btn_verify_load,self.dd_verify_mon]
        return []

    def _adj_event(self,event):
        """Offset mouse coords: screen→canvas, then canvas→scroll."""
        class E:
            def __init__(s,e,pos):
                s.type=e.type; s.pos=pos
                if hasattr(e,'button'): s.button=e.button
                if hasattr(e,'unicode'): s.unicode=e.unicode
                if hasattr(e,'key'): s.key=e.key
        if not hasattr(event,'pos'): return event
        # Step 1: screen → canvas coords
        cx=event.pos[0]-self.cx; cy=event.pos[1]-self.cy
        if not (0<=cx<self.W and 0<=cy<self.H_WIN): return event
        # Step 2: canvas → scroll-adjusted coords
        sa=self.scroll[self.current_tab]
        if self.current_tab in (0,1,2):
            if self._cy()<=cy<self.H_WIN-self.STATUS_H:
                adj_y=cy-self._cy()+sa.scroll_y
                return E(event,(cx,adj_y))
            return E(event,(cx,cy))
        return E(event,(cx,cy))

    def handle_events(self):
        # Joystick repeating input
        self._handle_joy()
        self._joy_repeat=(self._joy_repeat+1)%8
        if self._joy_repeat==0:
            if self._joy_axis_y!=0: self._nav_next(self._joy_axis_y)
            if self._joy_axis_x!=0: self._nudge_focused(self._joy_axis_x)

        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            # Modal dialog eats all keyboard input
            if self.dialog and self.dialog.active:
                if event.type==pygame.KEYDOWN:
                    self.dialog.handle_key(event)
                    if not self.dialog.active: self.dialog=None
                continue
            # Joystick buttons
            if event.type==pygame.JOYBUTTONDOWN:
                if event.button in (0,1):   self._activate_focused()   # A/B
                elif event.button==4: self._manual_scroll(-80)         # LB scroll up
                elif event.button==5: self._manual_scroll(+80)         # RB scroll down
                elif event.button==6:       # L2 → prev tab
                    self.current_tab=(self.current_tab-1)%len(self.TABS)
                    self._set_focus(self._focus_per_tab[self.current_tab])
                elif event.button==7:       # R2 → next tab
                    self.current_tab=(self.current_tab+1)%len(self.TABS)
                    self._set_focus(self._focus_per_tab[self.current_tab])
                elif event.button==9:       # START → next tab
                    self.current_tab=(self.current_tab+1)%len(self.TABS)
                    self._set_focus(self._focus_per_tab[self.current_tab])
            # Joystick hat (D-pad)
            if event.type==pygame.JOYHATMOTION:
                hx,hy=event.value
                if hy!=0: self._nav_next(-hy)
                if hx!=0: self._nudge_focused(hx)

            # Keyboard
            if event.type==pygame.KEYDOWN:
                # Check if a SliderRow entry has focus → let it eat the event
                focused_entry=None
                for w in self._widgets_for_tab(self.current_tab):
                    if isinstance(w,SliderRow) and w.entry.focused:
                        focused_entry=w; break
                    if isinstance(w,GeoSpin) and w.entry.focused:
                        focused_entry=w; break
                    if isinstance(w,TextInput) and w.focused:
                        focused_entry=w; break
                if focused_entry is not None:
                    if isinstance(focused_entry,SliderRow):
                        focused_entry.key_input(event.key,event.mod,
                                                getattr(event,'unicode',''))
                    elif isinstance(focused_entry,GeoSpin):
                        if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
                            focused_entry.entry.focused=False
                            focused_entry._confirm(focused_entry.entry.value)
                        else:
                            focused_entry.entry.handle(event)
                    elif isinstance(focused_entry,TextInput):
                        if event.key in (pygame.K_RETURN,pygame.K_KP_ENTER):
                            focused_entry.focused=False
                            if focused_entry.callback: focused_entry.callback(focused_entry.value)
                        else:
                            focused_entry.handle(event)
                    else:
                        focused_entry.handle(event)
                    continue

                if event.key==pygame.K_ESCAPE: return False
                elif event.key==pygame.K_TAB:
                    d=-1 if (event.mod&pygame.KMOD_SHIFT) else 1; self._nav_next(d)
                elif event.key in (pygame.K_DOWN,pygame.K_s): self._nav_next(+1)
                elif event.key in (pygame.K_UP,pygame.K_w):   self._nav_next(-1)
                elif event.key==pygame.K_LEFT:
                    self._nudge_focused(-1,bool(event.mod&pygame.KMOD_CTRL))
                elif event.key==pygame.K_RIGHT:
                    self._nudge_focused(+1,bool(event.mod&pygame.KMOD_CTRL))
                elif event.key in (pygame.K_RETURN,pygame.K_KP_ENTER,pygame.K_SPACE):
                    self._activate_focused()
                elif event.key==pygame.K_PAGEUP:
                    self._manual_scroll(-80)
                elif event.key==pygame.K_PAGEDOWN:
                    self._manual_scroll(+80)
                else:
                    # Forward digits/numpad directly to focused SliderRow
                    w=self._focused_widget()
                    if isinstance(w,SliderRow):
                        uni=getattr(event,'unicode','')
                        if uni and (uni.isdigit() or uni in '.-'):
                            w.key_input(event.key,event.mod,uni); continue
                    elif isinstance(w,GeoSpin):
                        uni=getattr(event,'unicode','')
                        if uni and (uni.isdigit() or uni in '.-'):
                            if not w.entry.focused: w.entry.value=""; w.entry.focused=True
                            w.entry.value+=uni; continue
                    elif isinstance(w,TextInput):
                        uni=getattr(event,'unicode','')
                        if uni and (uni.isdigit() or uni in '.-'):
                            if not w.focused: w.value=""; w.focused=True
                            w.value+=uni; continue
                    for w2 in self._widgets_for_tab(self.current_tab): w2.handle(event)
                continue

            if event.type==pygame.MOUSEWHEEL:
                self.scroll[self.current_tab].handle_scroll(event); continue
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                tw=self.W//len(self.TABS)
                cx=event.pos[0]-self.cx; cy=event.pos[1]-self.cy
                if 0<=cx<self.W and 0<=cy<self.TAB_H:
                    self.current_tab=cx//tw
                    self._set_focus(self._focus_per_tab[self.current_tab]); continue
            adj=self._adj_event(event)
            for w in self._widgets_for_tab(self.current_tab): w.handle(adj)
        return True

    def run(self):
        while True:
            if not self.handle_events(): break
            self.draw(); self.clock.tick(30)
        pygame.quit(); sys.exit()

# ══════════════════════════════════════════════════════════════════════════════
if __name__=="__main__":
    if "DISPLAY" not in os.environ: os.environ["DISPLAY"]=":0"
    App().run()
