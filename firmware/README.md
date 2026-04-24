# Firmware — fm-usb-mpx-tuner

Firmware STM32F072CBT6 pour le tuner FM USB MPX.

## Prérequis

- **STM32CubeIDE** ≥ 1.14 (ou **arm-none-eabi-gcc** + **make**)
- **ST-LINK** (V2 ou intégré Nucleo) ou **DFU** via USB natif STM32F072
- Bibliothèques : STM32CubeF0 HAL (incluse via CubeMX `.ioc`)

## Structure

```
firmware/
├── Core/
│   ├── Inc/
│   │   ├── main.h
│   │   ├── tef6687.h      # Pilote I²C TEF6687
│   │   └── usb_cdc_cmd.h  # Parseur commandes CDC
│   └── Src/
│       ├── main.c
│       ├── tef6687.c      # Tuning, RSSI, MPX enable
│       └── usb_cdc_cmd.c  # Protocole série USB
├── USB_DEVICE/            # Middleware USB (généré CubeMX)
├── Drivers/               # STM32CubeF0 HAL
├── fm-usb-mpx-tuner.ioc   # Fichier projet CubeMX
├── Makefile               # Build sans IDE
└── README.md
```

## Build avec STM32CubeIDE

1. `File → Import → Existing Projects into Workspace`
2. Sélectionner le dossier `firmware/`
3. `Project → Build All` (Ctrl+B)
4. `Run → Debug` ou `Run → Run` (ST-LINK connecté)

## Build avec Make

```bash
cd firmware
make -j4
# Sortie : build/fm-usb-mpx-tuner.elf + .bin + .hex
```

## Flashage

### Via ST-LINK (SWD)
```bash
make flash
# ou :
openocd -f interface/stlink.cfg -f target/stm32f0x.cfg \
        -c "program build/fm-usb-mpx-tuner.hex verify reset exit"
```

### Via DFU (USB natif — sans programmateur)
```bash
# Passer en mode DFU : maintenir BOOT0 haut au reset
dfu-util -a 0 -s 0x08000000:leave -D build/fm-usb-mpx-tuner.bin
```

## Protocole CDC (port COM virtuel, 115200 8N1)

| Commande | Description | Exemple |
|----------|-------------|---------|
| `TUNE <freq>` | Accorder en MHz (65,0–108,0) | `TUNE 98.2` |
| `RSSI` | Lire RSSI en dBµV | → `RSSI 62` |
| `SNR` | Lire SNR estimé | → `SNR 28` |
| `STEREO` | État décodeur stéréo | → `STEREO ON` |
| `RDS` | Dernière trame RDS (PS/RT) | → `RDS "FRANCE INFO"` |
| `VOL <0-100>` | Volume sortie audio DAC | `VOL 80` |
| `MPX ON\|OFF` | Activer/désactiver sortie MPX | `MPX ON` |
| `MUTE ON\|OFF` | Mute DAC (soft mute PCM5102A) | `MUTE OFF` |
| `INFO` | Firmware version + build date | → `fm-usb-mpx-tuner v1.0` |

## Configuration I²S

| Paramètre | Valeur |
|-----------|--------|
| Mode | Maître transmetteur |
| Standard | I²S Philips |
| Longueur données | 32 bits |
| Fréquence échantillonnage | 48 kHz |
| MCLK | Activé (256 × Fs = 12,288 MHz) |

## Licence

MIT — utilisation libre y compris commerciale.
