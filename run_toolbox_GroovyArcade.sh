#!/bin/bash
# ============================================================
# CRT Modeline Toolbox — GroovyArcade launcher
# Copy this script + crt_modeline_batocera.py to ~ (e.g. /home/arcade)
# Usage:  bash run_toolbox_groovyarcade.sh
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLBOX="$SCRIPT_DIR/crt_modeline_GroovyArcade.py"
export DISPLAY="${DISPLAY:-:0}"

if [ ! -f "$TOOLBOX" ]; then
    echo "ERROR: $TOOLBOX not found"
    exit 1
fi

# Check python3
if ! command -v python3 >/dev/null; then
    echo "ERROR: python3 not found — install with:  sudo pacman -S python"
    exit 1
fi

# Check pygame, offer install hints (GroovyArcade = Arch Linux)
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "pygame is not installed. Install it with ONE of:"
    echo "  sudo pacman -Sy python-pygame          (preferred, Arch package)"
    echo "  python3 -m pip install pygame --break-system-packages"
    exit 1
fi

echo "Launching CRT Modeline Toolbox..."
exec python3 "$TOOLBOX"
