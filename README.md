# fm-usb-mpx-tuner

Tuner FM USB autonome avec sortie MPX composite et sortie audio stéréo démodulée.

## Présentation

Ce projet est un récepteur FM alimenté par USB, conçu pour les applications broadcast et monitoring.  
Il expose deux sorties simultanées :

- **MPX** — signal composite FM brut (19 kHz pilote, L+R, L−R DSB-SC, RDS) sur BNC/SMA, pour alimenter un encoder RDS ou un analyseur de spectre.
- **Audio stéréo** — L/R démodulés et convertis en analogique via un DAC I²S haute qualité, sur jack 3,5 mm TRS.

Le tout tient dans un boîtier Hammond extrudé **1455L1201** (120 × 55 × 30 mm).

## Architecture

```
Antenne FM
    │
    ▼
┌──────────────┐    I²C/SPI    ┌─────────────────┐
│  TEF6687 V205│ ◄────────────►│  STM32F072CBT6  │◄──── USB (Type-C)
│  (tuner IC)  │               │  (USB Audio/CDC) │
└──────┬───────┘               └─────────────────┘
       │                                │
       │ MPX composite                  │ I²S
       ▼                                ▼
┌─────────────┐               ┌──────────────────┐
│  TLV9062    │               │    PCM5102A      │
│  (buffer)   │               │    (I²S DAC)     │
└──────┬──────┘               └────────┬─────────┘
       │                               │
       ▼                               ▼
   BNC/SMA out                  Jack 3,5 mm stéréo
  (MPX ~1 Vpp)                  (audio L/R)
```

## Composants principaux

| Référence | Composant | Description |
|-----------|-----------|-------------|
| U1 | TEF6687 V205 | Tuner FM/AM Silicon Labs, sortie MPX + I²S |
| U2 | STM32F072CBT6 | MCU ARM Cortex-M0, USB Full-Speed natif |
| U3 | PCM5102A | DAC I²S stéréo 32 bits, 112 dB SNR |
| U4 | TLV9062 | Op-amp rail-to-rail, buffer sortie MPX |
| U5 | AMS1117-3.3 | LDO 3,3 V / 1 A (alim. USB 5 V → 3,3 V) |
| X1 | 8 MHz crystal | Horloge STM32 |
| J1 | USB Type-C | Alimentation + données USB 2.0 FS |
| J2 | SMA femelle | Entrée antenne 50 Ω |
| J3 | BNC femelle | Sortie MPX (~1 Vpp / 75 Ω) |
| J4 | Jack 3,5 mm TRS | Sortie audio stéréo |
| — | Hammond 1455L1201 | Boîtier extrudé aluminium 120×55×30 mm |

Voir la [BOM complète](docs/bom.csv) pour références Mouser/LCSC et quantités.

## Structure du dépôt

```
fm-usb-mpx-tuner/
├── docs/
│   ├── architecture.md     # Description détaillée de l'architecture
│   ├── bom.csv             # Bill of Materials
│   └── schematic.svg       # Schéma de principe (interactif HTML : schematic.html)
├── firmware/
│   ├── README.md           # Build & flash instructions
│   └── src/                # Sources STM32 (STM32CubeIDE / Makefile)
├── hardware/
│   ├── schematic/          # Fichiers KiCad (.kicad_sch)
│   ├── pcb/                # Layout PCB KiCad (.kicad_pcb)
│   └── fab/                # Gerbers, drill, BOM pick-and-place
├── .gitignore
├── LICENSE                 # CERN-OHL-S v2
└── README.md
```

## Mise en route rapide

### Matériel requis
- Câble USB-C
- Antenne FM 50 Ω (dipôle, fouet ou SMA→MCX)
- Récepteur MPX ou jack audio

### Firmware
```bash
cd firmware
# avec STM32CubeIDE : importer le projet, Build & Flash
# ou avec make :
make flash TARGET=fm-usb-mpx-tuner INTERFACE=stlink
```

### Contrôle USB
Le STM32 expose un CDC série virtuel. Protocole simple :
```
TUNE 98.2        # accorder à 98,2 MHz
RSSI             # lire le niveau du signal
VOL 80           # volume DAC (0–100)
MPX ON/OFF       # activer/désactiver la sortie MPX
```

## Licence

Hardware : **CERN-OHL-S v2** — voir [LICENSE](LICENSE).  
Firmware : **MIT** — voir [firmware/LICENSE](firmware/LICENSE).
