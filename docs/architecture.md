# Architecture — fm-usb-mpx-tuner

## Vue d'ensemble

La carte est un **périphérique USB composite** qui fournit à [fm-monitor](https://github.com/LyonelB/fm-monitor) l'ensemble des données nécessaires à une analyse FM complète :

```
                    ┌─────────────────────────────────────────────┐
Antenne FM (SMA)    │            fm-usb-mpx-tuner                 │
      │             │                                             │
      ▼             │  ┌─────────────┐     ┌──────────────────┐  │
  TEF6687HN/V205   ─┼─►│             │ I²C │                  │  │
  55.46667 MHz ref  │  │  TEF6687    │◄───►│  STM32F072CBU6   ├──┼──► CDC /dev/ttyACM0
                    │  │  (tuner)    │     │                  │  │     Signal RF + RDS
                    │  │             │─I²S─►  SPI1 slave      ├──┼──► USB Audio hw:Tuner
                    │  │  Audio 48k  │     │  48kHz stéréo    │  │     Audio démodulé
                    │  │             │     │                  │  │
                    │  │  MPX analog─┼──►TLV9062──►PCM1863──►│  │
                    │  │             │     │  SPI2 master     ├──┼──► USB Audio hw:MPX
                    │  └─────────────┘     │  192kHz mono     │  │     MPX composite
                    │                      │                  │  │
                    │                      │  I²S ──►PCM5102A─┼──┼──► Mini jack 3,5mm
                    │                      └──────────────────┘  │     Audio analogique
                    │                                             │
                    │  TPS7A2033 (3,3V LNA)  AMS1117 (3,3V dig.) │
                    └─────────────────────────────────────────────┘
                                        │
                                       USB-C
                                        │
                                 Raspberry Pi
                                 (fm-monitor)
```

---

## 1. Réception RF — TEF6687HN/V205

Le TEF6687 est un tuner FM/AM NXP à conversion directe. Il intègre LNA, mélangeur, filtre IF et démodulateur FM. Sur ce projet il fournit **trois sorties** :

| Sortie | Type | Destination |
|--------|------|-------------|
| I²S audio | Numérique 48 kHz / 32 bit stéréo | STM32 SPI1 → USB `hw:Tuner` + PCM5102A |
| MPX composite | Analogique ~300 mVrms | TLV9062 → PCM1863 → USB `hw:MPX` |
| I²C | Métriques RF + groupes RDS | STM32 → USB CDC `/dev/ttyACM0` |

### Paramètres clés

| Paramètre | Valeur |
|-----------|--------|
| Plage FM | 65–108 MHz |
| Sensibilité | −107 dBm typ. |
| Sortie MPX | ~300 mVrms |
| I²S | 48 kHz / 32 bit stéréo |
| Référence clock | 55,46667 MHz (X2) |
| Interface contrôle | I²C addr 0x61 |

---

## 2. Microcontrôleur — STM32F072CBU6

Le STM32F072 (Cortex-M0, 48 MHz, 128 KB flash, 16 KB RAM) gère l'ensemble de la logique USB.

### Pourquoi le STM32F072 ?
- **USB Full-Speed natif** — oscillateur interne HSI48 + CRS (Clock Recovery System) → pas besoin de crystal USB
- **2× SPI/I²S** — reçoit simultanément TEF6687 (48 kHz) et PCM1863 (192 kHz)
- **Référence éprouvée** — utilisé par le projet FMDX Headless TEF Lite SE, firmware FM-DX-Tuner
- Package **QFN-48** (CBU6) — adapté PCBA automatisé

### Topologie I²S

```
TEF6687 (maître I²S)  ──BCK/WS/SD──►  STM32 SPI1 (esclave)   48 kHz stéréo
STM32 SPI2 (maître)   ──BCK/WS──────► PCM1863                192 kHz mono
PCM1863               ──SD──────────► STM32 SPI2 (esclave)   données ADC
```

### Périphériques utilisés

| Périphérique | Rôle |
|-------------|------|
| SPI1 / I²S slave | Réception audio TEF6687 48 kHz |
| SPI2 / I²S master | Clock + réception données PCM1863 192 kHz |
| I²C1 | Contrôle TEF6687 (tuning, RSSI, RDS) |
| USB (CDC + Audio) | Interface hôte : 3 interfaces composites |
| DMA CH1–CH4 | Transferts I²S sans CPU — vers buffers USB |

### USB — Périphérique composite

```
USB Composite Device
├── Interface 0 : CDC Control
├── Interface 1 : CDC Data (/dev/ttyACM0)
│     Protocol XDR-GTK — Signal RF + RDS groupes
├── Interface 2 : USB Audio Control
├── Interface 3 : USB Audio Streaming 0 (hw:Tuner)
│     Stéréo / 16 bit / 48 kHz — audio démodulé
└── Interface 4 : USB Audio Streaming 1 (hw:MPX)
      Mono / 24 bit / 192 kHz — MPX composite brut
```

**Budget bande passante USB Full-Speed :**

| Flux | Débit |
|------|-------|
| Audio 48 kHz / 16 bit / 2ch | 1,5 Mbit/s |
| MPX 192 kHz / 24 bit / 1ch | 4,6 Mbit/s |
| CDC overhead | < 0,1 Mbit/s |
| **Total** | **~6,2 Mbit/s** |

Budget isochronous USB FS = **8 Mbit/s** → marge ~23 % ✅

---

## 3. Buffer MPX — TLV9062

Le signal MPX du TEF6687 (~300 mVrms, impédance source ~600 Ω) est adapté avant l'ADC :

- Configuration **buffer unitaire** (gain = 1) — le PCM1863 dispose d'un PGA interne (−12 à +40 dB) qui gère le gain
- **Couplage AC** 10 µF (C17) : élimine tout offset DC présent en sortie TEF6687
- **Résistance série** 100 Ω (R7) : protège la sortie op-amp contre la capacité d'entrée du PCM1863 (~10 pF)
- Bande passante TLV9062 (GBW 10 MHz) : couvre largement RDS à 57 kHz et ses harmoniques

---

## 4. ADC MPX — PCM1863

Le PCM1863 (Texas Instruments) numérise le signal MPX composite à haute résolution.

| Paramètre | Valeur |
|-----------|--------|
| Résolution | 24 bits |
| Fréquence d'échantillonnage | 192 kHz |
| SNR | 103 dB (A-weighted) |
| THD+N | −90 dB |
| Plage d'entrée | ±1 Vrms (PGA = 0 dB) |
| Interface | I²S + I²C (contrôle PGA) |
| Package | TSSOP-24 |

**Pourquoi 192 kHz ?**  
Le signal MPX s'étend jusqu'à 57 kHz (RDS) + harmoniques ≈ 75 kHz.  
192 kHz → fréquence de Nyquist = 96 kHz → marge suffisante pour capturer tout le spectre MPX sans aliasing.

**Utilisation dans fm-monitor :**  
`mpx_analyzer.py` passe de `SAMPLE_RATE = 171000` (RTL-SDR) à `SAMPLE_RATE = 192000`. Tous les filtres (19 kHz, 38 kHz, 57 kHz) fonctionnent identiquement — seul le paramètre `fs` change.

---

## 5. DAC audio — PCM5102A

Le PCM5102A reçoit le même flux I²S 48 kHz que celui envoyé à l'USB `hw:Tuner`. Il fournit une sortie analogique sur le mini jack 3,5 mm TRS pour écoute directe ou monitoring local.

| Paramètre | Valeur |
|-----------|--------|
| SNR | 112 dB (A-weighted) |
| Sortie | 2,1 Vrms sur 10 kΩ |
| Format | I²S standard, 32 bits |
| Mode | Hardware (pas d'interface I²C) |

---

## 6. Alimentation

Deux régimes d'alimentation séparés à partir du 5 V USB :

```
USB 5 V
  │
  ├── AMS1117-3.3 ──────────────────► 3,3 V numérique
  │                                   STM32F072, logique PCM1863/PCM5102A
  │
  └── TPS7A2033 (ultra low-noise) ──► 3,3 V analogique
      9 µVrms, PSRR 75 dB             TEF6687, TLV9062, AVDD PCM1863/PCM5102A
```

Séparation par **ferrites FB1–FB4** (600 Ω @ 100 MHz) entre les deux domaines.

| Composant | Courant typ. |
|-----------|-------------|
| STM32F072 | 15 mA |
| TEF6687 | 45 mA |
| PCM5102A | 12 mA |
| PCM1863 | 15 mA |
| TLV9062 | 2 mA |
| TPS7A2033 | 1 mA |
| **Total** | **~90 mA** |

---

## 7. Protection USB — USBLC6-2P6 + ACM2012

- **USBLC6-2P6** (D1) : TVS bidirectionnelle sur D+ et D−, clamp < 3,3 V, temps de réponse < 1 ns
- **ACM2012-202-2P** (FL1) : filtre mode commun 200 Ω @ 100 MHz — atténue les émissions conduites

---

## 8. Boîtier — Hammond 1455L1201

| Paramètre | Valeur |
|-----------|--------|
| Dimensions extérieures | 120 × 55 × 30 mm |
| Matériau | Aluminium extrudé anodisé |
| PCB cible | 112 × 48 mm |

Perçages panneaux d'extrémité :

| Panneau | Connecteurs |
|---------|-------------|
| Gauche | USB-C (9,5 × 3,5 mm), LED statut ø3 mm |
| Droit | SMA antenne ø6,5 mm, mini jack 3,5 mm ø6 mm |

---

## 9. Intégration fm-monitor — résumé

| Canal | Device Linux | Consommateur | Métriques |
|-------|-------------|-------------|-----------|
| CDC | `/dev/ttyACM0` | `tef_driver.py` | dBf, SNR, multipath, offset, PI, PS, RT, MS |
| USB Audio 0 | `hw:Tuner` | `tef_audio_analyzer.py` | Level L/R, SNR audio, MPX power |
| USB Audio 1 | `hw:MPX` | `mpx_analyzer.py` (fs=192000) | Déviation ±75kHz, pilote 19kHz, stéréo 38kHz, RDS 57kHz, L/R décodés, SNR |
