#!/usr/bin/env python3
"""
Générateur de schéma KiCad 8 pour fm-usb-mpx-tuner.
Lit les symboles existants dans les fichiers FMDX et produit fm-usb-mpx-tuner.kicad_sch.

Usage : python3 gen_sch.py
"""

import re, uuid, os, sys

SCH_DIR = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────

def uid():
    return str(uuid.uuid4())

def extract_symbol(path, sym_name):
    """Extrait la définition (symbol "NAME" ...) depuis un fichier .kicad_sch."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    pattern = rf'\(symbol "{re.escape(sym_name)}"'
    start = content.find(f'(symbol "{sym_name}"')
    if start == -1:
        return None
    depth = 0
    i = start
    while i < len(content):
        if content[i] == '(':
            depth += 1
        elif content[i] == ')':
            depth -= 1
            if depth == 0:
                return content[start:i+1]
        i += 1
    return None

# ──────────────────────────────────────────────────────────
# Symbol definitions — custom ICs not in standard KiCad libs
# ──────────────────────────────────────────────────────────

PCM1863_SYM = '''\
    (symbol "PCM1863"
      (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 14 0) (effects (font (size 1.27 1.27))))
      (property "Value" "PCM1863" (at 0 11.5 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_SO:TSSOP-24_4.4x7.8mm_P0.65mm"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "https://www.ti.com/lit/ds/symlink/pcm1863.pdf"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "TI PCM1863 Stereo ADC 24-bit 192kHz I2S"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "PCM1863_1_1"
        (rectangle (start -7.62 10.16) (end 7.62 -15.24)
          (stroke (width 0.254) (type default)) (fill (type background)))
        (pin input line (at -10.16 8.89 0) (length 2.54)
          (name "VIN1LP" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 6.35 0) (length 2.54)
          (name "VIN1LN" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -10.16 3.81 0) (length 2.54)
          (name "VREF" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 -17.78 90) (length 2.54)
          (name "AGND" (effects (font (size 1.27 1.27))))
          (number "4" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 1.27 0) (length 2.54)
          (name "VIN1RP" (effects (font (size 1.27 1.27))))
          (number "5" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 -1.27 0) (length 2.54)
          (name "VIN1RN" (effects (font (size 1.27 1.27))))
          (number "6" (effects (font (size 1.27 1.27)))))
        (pin no_connect line (at -10.16 -3.81 0) (length 2.54)
          (name "NC8" (effects (font (size 1.27 1.27))))
          (number "8" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 12.7 270) (length 2.54)
          (name "AVDD" (effects (font (size 1.27 1.27))))
          (number "12" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 2.54 -17.78 90) (length 2.54)
          (name "DGND" (effects (font (size 1.27 1.27))))
          (number "13" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 2.54 12.7 270) (length 2.54)
          (name "DVDD" (effects (font (size 1.27 1.27))))
          (number "14" (effects (font (size 1.27 1.27)))))
        (pin input line (at 10.16 8.89 180) (length 2.54)
          (name "SCKI" (effects (font (size 1.27 1.27))))
          (number "15" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 10.16 6.35 180) (length 2.54)
          (name "LRCK" (effects (font (size 1.27 1.27))))
          (number "16" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 10.16 3.81 180) (length 2.54)
          (name "BCK" (effects (font (size 1.27 1.27))))
          (number "17" (effects (font (size 1.27 1.27)))))
        (pin output line (at 10.16 1.27 180) (length 2.54)
          (name "DOUT" (effects (font (size 1.27 1.27))))
          (number "18" (effects (font (size 1.27 1.27)))))
        (pin no_connect line (at 10.16 -1.27 180) (length 2.54)
          (name "DIN" (effects (font (size 1.27 1.27))))
          (number "19" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 10.16 -3.81 180) (length 2.54)
          (name "GPIO0" (effects (font (size 1.27 1.27))))
          (number "20" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 10.16 -6.35 180) (length 2.54)
          (name "GPIO1" (effects (font (size 1.27 1.27))))
          (number "21" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 10.16 -8.89 180) (length 2.54)
          (name "SDA" (effects (font (size 1.27 1.27))))
          (number "22" (effects (font (size 1.27 1.27)))))
        (pin input line (at 10.16 -11.43 180) (length 2.54)
          (name "SCL" (effects (font (size 1.27 1.27))))
          (number "23" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 5.08 12.7 270) (length 2.54)
          (name "IOVDD" (effects (font (size 1.27 1.27))))
          (number "24" (effects (font (size 1.27 1.27)))))
      )
    )'''

PCM5102A_SYM = '''\
    (symbol "PCM5102A"
      (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 12.7 0) (effects (font (size 1.27 1.27))))
      (property "Value" "PCM5102A" (at 0 10.16 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "https://www.ti.com/lit/ds/symlink/pcm5102a.pdf"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "TI PCM5102A Stereo DAC 32-bit 384kHz I2S"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "PCM5102A_1_1"
        (rectangle (start -7.62 8.89) (end 7.62 -13.97)
          (stroke (width 0.254) (type default)) (fill (type background)))
        (pin input line (at -10.16 7.62 0) (length 2.54)
          (name "SCK" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 5.08 0) (length 2.54)
          (name "BCK" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 2.54 0) (length 2.54)
          (name "DIN" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 0 0) (length 2.54)
          (name "LRCK" (effects (font (size 1.27 1.27))))
          (number "4" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -2.54 -16.51 90) (length 2.54)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "5" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 -2.54 0) (length 2.54)
          (name "DEMP" (effects (font (size 1.27 1.27))))
          (number "6" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 -5.08 0) (length 2.54)
          (name "FMT" (effects (font (size 1.27 1.27))))
          (number "7" (effects (font (size 1.27 1.27)))))
        (pin input line (at -10.16 -7.62 0) (length 2.54)
          (name "XSMT" (effects (font (size 1.27 1.27))))
          (number "8" (effects (font (size 1.27 1.27)))))
        (pin output line (at 10.16 5.08 180) (length 2.54)
          (name "OUTN_L" (effects (font (size 1.27 1.27))))
          (number "9" (effects (font (size 1.27 1.27)))))
        (pin output line (at 10.16 7.62 180) (length 2.54)
          (name "OUTP_L" (effects (font (size 1.27 1.27))))
          (number "10" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 11.43 270) (length 2.54)
          (name "AVDD" (effects (font (size 1.27 1.27))))
          (number "11" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 2.54 11.43 270) (length 2.54)
          (name "CPVDD" (effects (font (size 1.27 1.27))))
          (number "12" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 10.16 -2.54 180) (length 2.54)
          (name "VCP" (effects (font (size 1.27 1.27))))
          (number "13" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 10.16 -5.08 180) (length 2.54)
          (name "VCOM" (effects (font (size 1.27 1.27))))
          (number "14" (effects (font (size 1.27 1.27)))))
        (pin output line (at 10.16 0 180) (length 2.54)
          (name "OUTP_R" (effects (font (size 1.27 1.27))))
          (number "15" (effects (font (size 1.27 1.27)))))
        (pin output line (at 10.16 2.54 180) (length 2.54)
          (name "OUTN_R" (effects (font (size 1.27 1.27))))
          (number "16" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 5.08 11.43 270) (length 2.54)
          (name "DVDD" (effects (font (size 1.27 1.27))))
          (number "17" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 2.54 -16.51 90) (length 2.54)
          (name "DGND" (effects (font (size 1.27 1.27))))
          (number "18" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -2.54 11.43 270) (length 2.54)
          (name "AGND" (effects (font (size 1.27 1.27))))
          (number "19" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 -16.51 90) (length 2.54)
          (name "GND2" (effects (font (size 1.27 1.27))))
          (number "20" (effects (font (size 1.27 1.27)))))
      )
    )'''

TPS7A2033_SYM = '''\
    (symbol "TPS7A2033"
      (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 6.35 0) (effects (font (size 1.27 1.27))))
      (property "Value" "TPS7A2033" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_TO_SOT_SMD:SOT-23-5"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "https://www.ti.com/lit/ds/symlink/tps7a20.pdf"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "TI TPS7A2033 Ultra-low-noise LDO 3.3V 200mA SOT-23-5"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "TPS7A2033_1_1"
        (rectangle (start -3.81 2.54) (end 3.81 -5.08)
          (stroke (width 0.254) (type default)) (fill (type background)))
        (pin power_in line (at 0 5.08 270) (length 2.54)
          (name "IN" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))
        (pin input line (at -6.35 0 0) (length 2.54)
          (name "EN" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 -7.62 90) (length 2.54)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "4" (effects (font (size 1.27 1.27)))))
        (pin power_out line (at 6.35 0 180) (length 2.54)
          (name "OUT" (effects (font (size 1.27 1.27))))
          (number "5" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -6.35 -2.54 0) (length 2.54)
          (name "NR" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )'''

AMS1117_SYM = '''\
    (symbol "AMS1117-3.3"
      (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
      (property "Value" "AMS1117-3.3" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "Package_TO_SOT_SMD:SOT-223-3_TabPin2"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Description" "1A LDO 3.3V SOT-223"
        (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "AMS1117-3.3_1_1"
        (rectangle (start -3.81 1.27) (end 3.81 -3.81)
          (stroke (width 0.254) (type default)) (fill (type background)))
        (pin power_in line (at 0 3.81 270) (length 2.54)
          (name "IN" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27)))))
        (pin power_out line (at 6.35 0 180) (length 2.54)
          (name "OUT" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 0 -6.35 90) (length 2.54)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )'''

POWER_3V3_SYM = '''\
    (symbol "power:+3V3"
      (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "+3V3" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "+3V3_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27))
          (stroke (width 0)) (fill (type none)))
      )
      (symbol "+3V3_1_1"
        (pin power_in line (at 0 0 270) (length 0)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )'''

POWER_3V3A_SYM = '''\
    (symbol "power:+3V3A"
      (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "+3V3A" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "+3V3A_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 1.524 1.27) (xy 2.286 2.54))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 2.286 2.54) (xy 3.048 1.27))
          (stroke (width 0)) (fill (type none)))
      )
      (symbol "+3V3A_1_1"
        (pin power_in line (at 0 0 270) (length 0)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )'''

POWER_5V_SYM = '''\
    (symbol "power:+5V"
      (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "+5V" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "+5V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27))
          (stroke (width 0)) (fill (type none)))
      )
      (symbol "+5V_1_1"
        (pin power_in line (at 0 0 270) (length 0)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )'''

POWER_GND_SYM = '''\
    (symbol "power:GND"
      (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy -0.762 -1.905) (xy 0.762 -1.905))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy -0.254 -2.54) (xy 0.254 -2.54))
          (stroke (width 0)) (fill (type none)))
      )
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )'''

POWER_AGND_SYM = '''\
    (symbol "power:AGND"
      (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "AGND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "AGND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy -1.27 -1.27) (xy 1.27 -1.27))
          (stroke (width 0)) (fill (type none)))
        (polyline (pts (xy -0.762 -1.905) (xy 0.762 -1.905))
          (stroke (width 0)) (fill (type none)))
      )
      (symbol "AGND_1_1"
        (pin power_in line (at 0 0 270) (length 0)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )'''

# ──────────────────────────────────────────────────────────
# Composant instance builder
# ──────────────────────────────────────────────────────────

def sym_inst(lib_id, ref, val, x, y, footprint="", datasheet="", unit=1,
             in_bom="yes", on_board="yes", mirror="", extra_props=None):
    mirror_str = f'\n    (mirror {mirror})' if mirror else ""
    fp_str = footprint or ""
    ds_str = datasheet or "~"
    props = extra_props or {}
    extra = ""
    for k, v in props.items():
        extra += f'''
    (property "{k}" "{v}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))'''

    return f'''
  (symbol
    (lib_id "{lib_id}")
    (at {x} {y} 0){mirror_str}
    (unit {unit})
    (exclude_from_sim no)
    (in_bom {in_bom})
    (on_board {on_board})
    (uuid "{uid()}")
    (property "Reference" "{ref}" (at {x+2.54} {y-2.54} 0) (effects (font (size 1.27 1.27))))
    (property "Value" "{val}" (at {x+2.54} {y+2.54} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "{fp_str}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "{ds_str}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))\
{extra}
  )'''

def power_sym(lib_id, ref, x, y):
    return f'''
  (symbol
    (lib_id "{lib_id}")
    (at {x} {y} 0)
    (unit 1)
    (exclude_from_sim no) (in_bom yes) (on_board yes)
    (uuid "{uid()}")
    (property "Reference" "{ref}" (at {x} {y+2.54} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Value" "{lib_id.split(":")[1]}" (at {x} {y+2.54} 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
    (property "Datasheet" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (hide yes)))
  )'''

def net_label(name, x, y, angle=0):
    return f'''
  (net_tie_pad_groups "")
  (label "{name}"
    (at {x} {y} {angle})
    (fields_autoplaced yes)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{uid()}")
  )'''

def global_label(name, shape, x, y, angle=0):
    return f'''
  (global_label "{name}"
    (shape {shape})
    (at {x} {y} {angle})
    (fields_autoplaced yes)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{uid()}")
    (property "Intersheet References" "" (at {x} {y} 0)
      (effects (font (size 1.27 1.27)) (hide yes)))
  )'''

def no_connect(x, y):
    return f'\n  (no_connect (at {x} {y}) (uuid "{uid()}"))'

def wire(x1, y1, x2, y2):
    return f'''
  (wire
    (pts (xy {x1} {y1}) (xy {x2} {y2}))
    (stroke (width 0) (type default))
    (uuid "{uid()}")
  )'''

def text_note(txt, x, y, size=1.27):
    return f'''
  (text "{txt}"
    (at {x} {y} 0)
    (effects (font (size {size} {size})) (justify left))
    (uuid "{uid()}")
  )'''

def rect_note(x1, y1, x2, y2, label):
    """Rectangle de délimitation de section."""
    return f'''
  (rectangle
    (start {x1} {y1}) (end {x2} {y2})
    (stroke (width 0.1) (type dash))
    (fill (type none))
    (uuid "{uid()}")
  )
  (text "{label}"
    (at {x1+1} {y1+2} 0)
    (effects (font (size 1.5 1.5) (bold yes)) (justify left))
    (uuid "{uid()}")
  )'''

# ──────────────────────────────────────────────────────────
# Main schematic builder
# ──────────────────────────────────────────────────────────

def build_schematic():
    src_tef = os.path.join(SCH_DIR, "TEF6687.kicad_sch")
    src_hta = os.path.join(SCH_DIR, "Headless TEF Audio board.kicad_sch")

    # Extract symbols from reference files
    tef668x_def = extract_symbol(src_tef, "New_Library:TEF668x") or ""
    usblc6_def  = extract_symbol(src_tef, "Power_Protection:USBLC6-2P6") or ""
    stm_def     = extract_symbol(src_tef, "MCU_ST_STM32F0:STM32F072CBTx") or ""
    xtal_def    = extract_symbol(src_tef, "Device:Crystal_GND24") or ""
    fb_def      = extract_symbol(src_tef, "Device:FerriteBead_Small") or ""
    c_def       = extract_symbol(src_tef, "Device:C_Small") or ""
    r_def       = extract_symbol(src_tef, "Device:R_Small") or ""
    tlv_def     = extract_symbol(src_hta, "Amplifier_Operational:TLV9062xD") or ""
    jack_def    = extract_symbol(src_hta, "Connector_Audio:AudioJack3_Ground") or ""

    # ── lib_symbols ───────────────────────────────────────
    lib_symbols = f'''\
  (lib_symbols
{tef668x_def}
{usblc6_def}
{stm_def}
{xtal_def}
{fb_def}
{c_def}
{r_def}
{tlv_def}
{jack_def}
{PCM1863_SYM}
{PCM5102A_SYM}
{TPS7A2033_SYM}
{AMS1117_SYM}
{POWER_3V3_SYM}
{POWER_3V3A_SYM}
{POWER_5V_SYM}
{POWER_GND_SYM}
{POWER_AGND_SYM}
  )'''

    # ── Component instances ────────────────────────────────
    # Coordinates in mm, A3 sheet (420x297mm)
    # Layout:
    #   x≈15-80 : Power + SMA
    #   x≈100-165: TEF6687
    #   x≈185-295: STM32F072
    #   x≈310-380: USB ifaces / PCM5102A
    #   x≈90-165 : TLV9062 + PCM1863 (y≈200-260)

    components = ""

    # Section labels
    components += rect_note(10, 10, 100, 90,   "Alimentation USB")
    components += rect_note(10, 95, 180, 195,  "RF — TEF6687HN/V205 (U1)")
    components += rect_note(185, 80, 380, 195, "MCU — STM32F072CBU6 (U2)")
    components += rect_note(10, 200, 250, 285, "Chemin MPX — TLV9062 (U4) + PCM1863 (U5)")
    components += rect_note(255, 200, 415, 285,"Audio DAC — PCM5102A (U3) + Mini Jack (J3)")

    # ── POWER SECTION ───────────────────────
    # USB-C connector (simplified as generic conn)
    components += sym_inst("New_Library:TEF668x", "U1", "TEF6687HN/V205",
        105, 145, "TEFHeadlessLib:TEF6687", "https://www.nxp.com")

    components += sym_inst("MCU_ST_STM32F0:STM32F072CBTx", "U2", "STM32F072CBU6",
        255, 140,
        "Package_DFN_QFN:QFN-48-1EP_7x7mm_P0.5mm_EP5.6x5.6mm",
        "https://www.st.com/resource/en/datasheet/stm32f072cb.pdf")

    components += sym_inst("Amplifier_Operational:TLV9062xD", "U4_A", "TLV9062",
        90, 235, "Package_TO_SOT_SMD:SOT-23-8",
        "https://www.ti.com/lit/ds/symlink/tlv9062.pdf", unit=1)

    components += sym_inst("PCM1863", "U5", "PCM1863",
        170, 245, "Package_SO:TSSOP-24_4.4x7.8mm_P0.65mm")

    components += sym_inst("PCM5102A", "U3", "PCM5102A",
        320, 235, "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm")

    components += sym_inst("TPS7A2033", "U6", "TPS7A2033",
        40, 55, "Package_TO_SOT_SMD:SOT-23-5")

    components += sym_inst("AMS1117-3.3", "U7", "AMS1117-3.3",
        75, 55, "Package_TO_SOT_SMD:SOT-223-3_TabPin2")

    components += sym_inst("Power_Protection:USBLC6-2P6", "D1", "USBLC6-2P6",
        350, 35, "Package_TO_SOT_SMD:SOT-23-6")

    # Crystal X2 (55.46667 MHz for TEF6687)
    components += sym_inst("Device:Crystal_GND24", "X2", "55.46667MHz",
        60, 185, "Crystal:Crystal_SMD_HC-49-SD",
        "~", extra_props={"ki_description": "TEF6687 reference clock"})

    # Crystal X1 (8 MHz for STM32)
    components += sym_inst("Device:Crystal_GND24", "X1", "8MHz",
        220, 185, "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm")

    # Audio jack J3
    components += sym_inst("Connector_Audio:AudioJack3_Ground", "J3", "Mini Jack 3.5mm TRS",
        385, 240, "Connector_Audio:Jack_3.5mm_CUI_SJ-3523-SMT_Horizontal")

    # Ferrite beads FB1-FB4
    for i, (fx, fy) in enumerate([(30,75),(50,75),(70,75),(90,75)], 1):
        components += sym_inst("Device:FerriteBead_Small", f"FB{i}", "600R@100MHz",
            fx, fy, "Inductor_SMD:L_0402_1005Metric")

    # ── Net labels — I2S bus TEF6687 ↔ STM32 SPI1 ──────
    # (placed near U1 right side and U2 left side)
    labels = ""

    # TEF6687 side
    labels += net_label("TEF_I2S_SD", 140, 131)     # pin 16 I2S_SD_0
    labels += net_label("TEF_I2S_WS", 140, 128.5)   # pin 17
    labels += net_label("TEF_I2S_BCK", 140, 126)    # pin 18
    labels += net_label("TEF_SDA", 140, 110)         # pin 24
    labels += net_label("TEF_SCL", 140, 107.5)       # pin 25
    labels += net_label("TEF_MPX_OUT", 70, 142)      # DAC_L or dedicated MPX output

    # STM32 side — SPI1 (I2S slave for TEF6687 audio)
    labels += net_label("TEF_I2S_SD", 185, 162)      # PA7/I2S1_SD
    labels += net_label("TEF_I2S_WS", 185, 159.5)   # PA4/I2S1_WS
    labels += net_label("TEF_I2S_BCK", 185, 157)    # PA5/I2S1_CK
    labels += net_label("TEF_SDA", 185, 132)         # PB7/I2C1_SDA
    labels += net_label("TEF_SCL", 185, 129.5)      # PB6/I2C1_SCL

    # STM32 side — SPI2 (I2S master for PCM1863)
    labels += net_label("PCM1863_DOUT", 185, 149.5)  # PB14
    labels += net_label("PCM1863_LRCK", 185, 147)   # PB12
    labels += net_label("PCM1863_BCK", 185, 144.5)  # PB13

    # PCM5102A side (I2S from STM32)
    labels += net_label("PCM5102_DIN", 325, 167.5)   # STM32 output
    labels += net_label("PCM5102_LRCK", 325, 170)
    labels += net_label("PCM5102_BCK", 325, 172.5)
    labels += net_label("PCM5102_DIN", 295, 232)     # PCM5102A input
    labels += net_label("PCM5102_LRCK", 295, 234.5)
    labels += net_label("PCM5102_BCK", 295, 237)

    # PCM1863 connections
    labels += net_label("TEF_MPX_OUT", 60, 238)      # TLV9062 input
    labels += net_label("MPX_BUF_OUT", 115, 235)     # TLV9062 → PCM1863
    labels += net_label("MPX_BUF_OUT", 145, 245)     # PCM1863 input
    labels += net_label("PCM1863_DOUT", 198, 246)
    labels += net_label("PCM1863_LRCK", 198, 248.5)
    labels += net_label("PCM1863_BCK", 198, 251)

    # USB
    labels += net_label("USB_DM", 325, 125)           # STM32 PA11
    labels += net_label("USB_DP", 325, 122.5)         # STM32 PA12
    labels += net_label("USB_DM", 330, 30)
    labels += net_label("USB_DP", 330, 32.5)

    # PCM5102A → mini jack
    labels += net_label("AUDIO_L", 345, 227.5)
    labels += net_label("AUDIO_R", 345, 230)
    labels += net_label("AUDIO_L", 370, 240)
    labels += net_label("AUDIO_R", 370, 242.5)

    # Power symbols (instances of power symbols placed at component pins)
    power = ""
    # +5V at USB-C, LDOs input
    power += power_sym("power:+5V", "#PWR01", 40, 42)
    power += power_sym("power:+5V", "#PWR02", 75, 42)
    power += power_sym("power:+5V", "#PWR03", 350, 22)

    # +3V3D digital domain
    power += power_sym("power:+3V3", "#PWR04", 255, 80)
    power += power_sym("power:+3V3", "#PWR05", 320, 208)
    power += power_sym("power:+3V3", "#PWR06", 170, 222)

    # +3V3A analog domain
    power += power_sym("power:+3V3A", "#PWR07", 105, 105)
    power += power_sym("power:+3V3A", "#PWR08", 90, 215)

    # GND
    power += power_sym("power:GND", "#PWR09", 255, 200)
    power += power_sym("power:GND", "#PWR10", 40, 75)
    power += power_sym("power:GND", "#PWR11", 75, 75)
    power += power_sym("power:GND", "#PWR12", 350, 55)
    power += power_sym("power:GND", "#PWR13", 170, 278)
    power += power_sym("power:GND", "#PWR14", 320, 262)

    # AGND
    power += power_sym("power:AGND", "#PWR15", 105, 185)
    power += power_sym("power:AGND", "#PWR16", 90, 272)

    # No-connects
    nc = ""
    # TEF6687 unused pins
    nc += no_connect(140, 101)   # GPIO0-2
    nc += no_connect(140, 103.5)
    nc += no_connect(140, 106)
    nc += no_connect(70, 132)    # AM inputs
    nc += no_connect(70, 135)
    # PCM1863 unused input pair 2
    nc += no_connect(145, 238)
    nc += no_connect(145, 241)
    nc += no_connect(145, 243.5)
    nc += no_connect(145, 246)
    # PCM5102A VCP, VCOM caps external
    nc += no_connect(345, 230)

    # Notes
    notes = ""
    notes += text_note("Protocole CDC: XDR-GTK (identique FM-DX-Tuner)", 185, 75, 1.0)
    notes += text_note("USB composite: CDC + Audio 48kHz (hw:Tuner) + Audio 192kHz (hw:MPX)", 185, 78, 1.0)
    notes += text_note("X2 charge caps: 12pF NP0/C0G (C15-C16)", 55, 200, 1.0)
    notes += text_note("Couplage AC: C17 10uF avant VIN1LP/VIN1RN du PCM1863", 10, 290, 1.0)
    notes += text_note("SPI1 (I2S slave) -> TEF6687 audio 48kHz | SPI2 (I2S master) -> PCM1863 MPX 192kHz", 185, 200, 1.0)

    # ── Assemble ──────────────────────────────────────────
    schematic = f'''\
(kicad_sch
  (version 20231120)
  (generator "fm-usb-mpx-tuner-gen")
  (generator_version "1.0")
  (uuid "{uid()}")
  (paper "A3")
  (title_block
    (title "fm-usb-mpx-tuner")
    (date "2026-04-25")
    (rev "v1.0")
    (company "LyonelB")
    (comment 1 "TEF6687HN/V205 + STM32F072CBU6 + PCM1863 + PCM5102A + TLV9062")
    (comment 2 "USB composite: CDC (XDR-GTK) + USB Audio 48kHz + USB Audio 192kHz")
    (comment 3 "CERN-OHL-S v2 — https://github.com/LyonelB/fm-usb-mpx-tuner")
    (comment 4 "Firmware: FM-DX-Tuner (kkonradpl) — compatible fm-monitor (LyonelB)")
  )

{lib_symbols}

{components}
{labels}
{power}
{nc}
{notes}
)
'''
    return schematic

# ──────────────────────────────────────────────────────────
# Write output
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_path = os.path.join(SCH_DIR, "fm-usb-mpx-tuner.kicad_sch")
    sch = build_schematic()
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sch)
    size_kb = os.path.getsize(out_path) // 1024
    print(f"Schéma généré : {out_path} ({size_kb} KB)")
    print(f"Ouvrir avec KiCad 8 : kicad {out_path}")
