#!/bin/bash
# Lance l'application en utilisant le framebuffer SPI
# Utiliser QT_QPA_FB pour définir le framebuffer si différent de /dev/fb1
export QT_QPA_PLATFORM=linuxfb
export QT_QPA_FB=${QT_QPA_FB:-/dev/fb1}
python3 "$(dirname "$0")/../main.py"

