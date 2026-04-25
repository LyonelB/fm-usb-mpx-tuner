# fm-usb-mpx-tuner

Tuner FM USB composite pour monitoring broadcast — alimente [fm-monitor](https://github.com/LyonelB/fm-monitor) avec toutes ses sources de données.

## Présentation

Périphérique USB composite qui expose **trois canaux simultanés** vers le Raspberry Pi :

| Interface USB | Type | Contenu | Consommé par |
|--------------|------|---------|--------------|
| `/dev/ttyACM0` | CDC série | Signal RF (dBf, SNR, multipath) + groupes RDS | `tef_driver.py` |
| `hw:Tuner` | USB Audio 48 kHz stéréo | Audio démodulé L/R | `tef_audio_analyzer.py` |
| `hw:MPX` | USB Audio 192 kHz mono | Signal MPX composite brut | `mpx_analyzer.py` |

Sortie analogique de secours : **mini jack 3,5 mm TRS** (audio stéréo via DAC I²S).

## Architecture

```
Antenne FM (SMA)
      │
      ▼
┌──────────────────┐  I²C   ┌─────────────────────────────────────┐
│  TEF6687HN/V205  │◄──────►│          STM32F072CBU6              │
│  (tuner FM/AM)   │        │                                     │
│                  │  I²S   │  SPI1/I²S slave ──► USB Audio 0    ├──► hw:Tuner
│  Audio 48 kHz   ─┼───────►│  stéréo 16 bit / 48 kHz            │    (fm-monitor)
│                  │        │                                     │
│  MPX (analog)   ─┼──┐     │  SPI2/I²S master ◄─ PCM1863       │
│                  │  │     │  mono 24 bit / 192 kHz ──► USB Audio 1 ├──► hw:MPX
│  crystal         │  │     │                                     │    (fm-monitor)
│  55.46667 MHz    │  │     │  CDC (XDR-GTK protocol) ───────────├──► /dev/ttyACM0
└──────────────────┘  │     │                                     │    (fm-monitor)
                      │     │  I²S ──────────────────────────────┼──► PCM5102A
                      │     └─────────────────────────────────────┘         │
                      │                                                      ▼
                      │      TLV9062                                  mini jack 3,5 mm
                      └──────(buffer)──────────────────► PCM1863
                                                         (ADC 192 kHz)
```

## Composants principaux

| Ref | Composant | Rôle |
|-----|-----------|------|
| U1 | TEF6687HN/V205 | Tuner FM/AM — MPX + I²S + RDS natif |
| U2 | STM32F072CBU6 | MCU Cortex-M0, USB FS natif (HSI48+CRS) |
| U3 | PCM5102A | DAC I²S → mini jack 3,5 mm (audio analogique) |
| U4 | TLV9062 | Buffer MPX (TEF6687 → PCM1863, impédance) |
| U5 | PCM1863 | ADC MPX 192 kHz / 24 bit → USB Audio `hw:MPX` |
| U6 | TPS7A2033 | LDO 3,3 V ultra low-noise (RF + audio) |
| D1 | USBLC6-2P6 | Protection ESD lignes USB |
| X1 | 8 MHz | Résonateur STM32F072 |
| X2 | 55,46667 MHz | Crystal TEF6687 (référence RF) |
| FL1 | ACM2012-202-2P | Filtre mode commun USB |
| J1 | USB-C | Alimentation 5 V + données USB 2.0 FS |
| J2 | SMA femelle | Entrée antenne FM 50 Ω |
| J3 | Mini jack 3,5 mm TRS | Sortie audio analogique stéréo |

Voir la [BOM complète](docs/bom.csv) pour références LCSC/Mouser et prix.

## Compatibilité fm-monitor

Le firmware implémente le protocole **XDR-GTK** sur le port CDC — identique au firmware [FM-DX-Tuner](https://github.com/kkonradpl/FM-DX-Tuner).  
`tef_driver.py` fonctionne sans modification.

Le flux MPX USB (`hw:MPX`, 192 kHz) remplace le RTL-SDR comme source de `mpx_analyzer.py` :

```python
# config.json — section tef
{
  "tef": {
    "enabled": true,
    "serial_port": "/dev/ttyACM0",
    "alsa_device": "hw:Tuner",
    "mpx_device":  "hw:MPX",        # nouveau — MPX 192 kHz
    "mpx_sample_rate": 192000
  }
}
```

Métriques disponibles avec cette carte :

| Métrique | Disponible |
|----------|-----------|
| Signal dBf + SNR RF | ✅ (CDC) |
| PI Code, PS, RT, MS | ✅ (CDC) |
| Niveaux L/R audio | ✅ (hw:Tuner) |
| Déviation FM ±75 kHz | ✅ (hw:MPX) |
| Pilote 19 kHz | ✅ (hw:MPX) |
| Stéréo 38 kHz | ✅ (hw:MPX) |
| RDS RF 57 kHz | ✅ (hw:MPX) |
| SNR audio | ✅ (hw:MPX) |

## Structure du dépôt

```
fm-usb-mpx-tuner/
├── docs/
│   ├── architecture.md     # Description détaillée
│   ├── bom.csv             # Bill of Materials complet
│   └── schematic.html      # Schéma interactif
├── firmware/
│   ├── README.md           # Build, flash, DFU
│   └── src/                # Sources STM32 (STM32CubeIDE)
├── hardware/
│   ├── schematic/          # KiCad .kicad_sch
│   ├── pcb/                # Layout PCB .kicad_pcb
│   └── fab/                # Gerbers, positions, BOM JLCPCB
├── .gitignore
├── LICENSE                 # CERN-OHL-S v2
└── README.md
```

## Mise en route

### Branchement

```
Antenne FM ──SMA──► fm-usb-mpx-tuner ──USB-C──► Raspberry Pi
                                       │
                                       └─mini jack──► ampli / casque (optionnel)
```

### Détection sur le Raspberry Pi

```bash
ls /dev/ttyACM0          # port CDC série
aplay -l | grep Tuner    # interface audio 48 kHz
aplay -l | grep MPX      # interface audio 192 kHz
```

### Firmware — flash initial

```bash
# Mode DFU : relier BOOT0 à 3,3 V, brancher USB, flasher
dfu-util -a 0 -s 0x08000000:leave -D build/fm-usb-mpx-tuner.bin

# Via ST-LINK (SWD)
openocd -f interface/stlink.cfg -f target/stm32f0x.cfg \
        -c "program build/fm-usb-mpx-tuner.hex verify reset exit"
```

## Licence

Hardware : **CERN-OHL-S v2** — voir [LICENSE](LICENSE).  
Firmware : **MIT** — voir [firmware/LICENSE](firmware/LICENSE).
