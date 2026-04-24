# Architecture — fm-usb-mpx-tuner

## Vue d'ensemble

Le tuner est organisé en trois domaines fonctionnels :

1. **Réception RF** — TEF6687 V205
2. **Traitement numérique / USB** — STM32F072CBT6
3. **Sorties analogiques** — PCM5102A (audio) + TLV9062 (MPX)

---

## 1. Réception RF — TEF6687 V205

Le TEF6687 est un tuner FM/AM Silicon Labs à conversion directe. Il intègre :

- LNA, mélangeur, filtre IF et démodulateur FM en un seul boîtier QFN-32
- Sortie **MPX composite** analogique (pilote 19 kHz, L+R, L−R DSB-SC, RDS 57 kHz)
- Sortie **I²S numérique** (L+R démodulé, 32 bits, 48 kHz)
- Interface de contrôle **I²C** (adresse 0x61 par défaut)
- Alimentation : 3,3 V

### Paramètres clés

| Paramètre | Valeur |
|-----------|--------|
| Plage FM | 65–108 MHz |
| Sensibilité | −107 dBm typ. |
| SNR audio | 70 dB typ. |
| Sortie MPX | 300 mVrms typ. |
| Interface MCU | I²C + interruption |

---

## 2. Microcontrôleur — STM32F072CBT6

Le STM32F072 (Cortex-M0, 48 MHz, 128 KB flash, 16 KB RAM) a été retenu pour :

- **USB Full-Speed natif** sans crystal USB (HSI48 interne avec CRS)
- Périphériques disponibles : I²C × 2, SPI × 2, I²S × 1, USART × 4
- Package LQFP-48, facile à souder à la main

### Rôle dans le système

```
USB Host (PC)
     │  USB CDC (Virtual COM) ou USB Audio
     ▼
STM32F072
     ├── I²C1 ──────► TEF6687 (commandes de tuning, lecture RSSI)
     ├── I²S1 ◄─────── TEF6687 (audio 48 kHz / 32 bits stéréo)
     ├── I²S1 ──────► PCM5102A (même bus, mode maître STM32)
     └── GPIO ──────► LED statut, MPX enable
```

**USB Audio Class** — le STM32 peut se déclarer périphérique audio USB 2.0 Full-Speed (2× 24 bits / 48 kHz stéréo) et streamer l'audio démodulé directement vers le PC sans driver.

**USB CDC** — mode alternatif pour le contrôle bas-niveau du tuner via terminal série.

---

## 3. DAC audio — PCM5102A

Le PCM5102A (Texas Instruments) est un DAC I²S stéréo sans interface de contrôle (hardware mode) :

- SNR : 112 dB (A-weighted)
- THD+N : −93 dB
- Alimentation : 3,3 V (numérique) + 3,3 V (analogique, filtré séparément)
- Package TSSOP-20
- Sortie : 2,1 Vrms à pleine échelle sur charge 10 kΩ

Les broches `SCK/BCK/LRCK/DIN` sont câblées directement sur le bus I²S du STM32.  
`FMT[1:0]` = 00 (I²S standard), `DEMP` = 0, `XSMT` (soft mute) piloté par GPIO.

---

## 4. Buffer MPX — TLV9062

Le signal MPX brut du TEF6687 (~300 mVrms) est adapté par un TLV9062 :

- Configuration : amplificateur non-inverseur, gain ≈ 3,3 → **~1 Vrms** sur charge haute impédance
- Bande passante : > 100 kHz (couvre RDS à 57 kHz et ses harmoniques)
- Alimentation rail-to-rail 3,3 V
- Couplage AC obligatoire (condensateur 10 µF) — le TEF6687 peut présenter un offset DC
- Résistance série 100 Ω en sortie : protège l'op-amp contre la capacité du câble RCA
- Sortie sur connecteur **RCA femelle** (phono), impédance source < 200 Ω

### Connexion vers HiFiBerry DAC+ ADC

```
fm-usb-mpx-tuner          câble RCA→jack 3,5 mm       Raspberry Pi
  J3 RCA (MPX) ────────────────────────────────► HiFiBerry line-in
                                                  (PCM1863 ADC, 24 bit)
                                                        │
                                                        ▼
                                               logiciel fm-monitor
                                               (analyse spectre MPX,
                                                mesure RDS, pilote 19 kHz,
                                                deviation ±75 kHz)
```

**Niveau de signal :** ~1 Vrms (−3 dBu) — dans la plage nominale du PCM1863 (entrée max ±1 Vrms en mode line).  
**Câble à utiliser :** RCA mâle → jack 3,5 mm TS (mono) — le MPX est un signal composite mono.  
**Attention :** utiliser l'entrée **gauche** (Tip) du jack HiFiBerry ; le canal droit peut rester non connecté ou être câblé sur le même signal (Tip = Ring).

---

## 5. Alimentation

```
USB 5 V (500 mA max)
    │
    ├── AMS1117-3.3 ──► 3,3 V numérique (STM32, TEF6687, PCM5102A digital)
    │
    └── Ferrite + C ──► 3,3 V analogique (PCM5102A AVDD, TLV9062)
```

Consommation estimée :

| Bloc | Courant typ. |
|------|-------------|
| STM32F072 | 15 mA |
| TEF6687 | 45 mA |
| PCM5102A | 12 mA |
| TLV9062 | 2 mA |
| **Total** | **~74 mA** |

---

## 6. Boîtier — Hammond 1455L1201

| Dimension | Valeur |
|-----------|--------|
| Longueur | 120 mm |
| Largeur | 55 mm |
| Hauteur | 30 mm |
| Matériau | Aluminium extrudé anodisé |

PCB cible : 112 × 48 mm (panneaux d'extrémité Hammond : 57 × 31 mm).

Perçages panneaux :
- **Panneau gauche** : USB-C (9,5 × 3,5 mm), LED ø3 mm
- **Panneau droit** : SMA antenne, RCA MPX, jack 3,5 mm audio
