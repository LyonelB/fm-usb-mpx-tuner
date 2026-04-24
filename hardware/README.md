# Hardware — fm-usb-mpx-tuner

Fichiers KiCad pour le schéma et le PCB du tuner FM USB MPX.

## Logiciel requis

- **KiCad** ≥ 7.0 (https://www.kicad.org/)
- Bibliothèques standard KiCad (incluses dans l'installation)

## Structure

```
hardware/
├── schematic/
│   ├── fm-usb-mpx-tuner.kicad_pro   # Projet KiCad
│   ├── fm-usb-mpx-tuner.kicad_sch   # Schéma principal
│   ├── Headless TEF Audio board.kicad_sch  # Schéma référence TEF6687
│   └── TEF6687.kicad_sch            # Symbole/schéma TEF6687
├── pcb/
│   └── fm-usb-mpx-tuner.kicad_pcb   # Layout PCB (à venir)
└── fab/
    ├── gerbers/                      # Fichiers Gerber pour fabrication
    ├── bom-jlcpcb.csv               # BOM format JLCPCB SMT Assembly
    └── positions.csv                # Pick-and-place centroïdes
```

## Dimensions PCB

| Paramètre | Valeur |
|-----------|--------|
| Format | 112 × 48 mm |
| Couches | 2 (top Cu + bottom Cu) |
| Épaisseur | 1,6 mm FR4 |
| Finish | HASL ou ENIG |
| Couleur solder mask | Noir (recommandé) |
| Sérigraphie | Blanche |

Taille dictée par le boîtier **Hammond 1455L1201** (longueur utile intérieure ≈ 116 mm, largeur ≈ 51 mm, avec jeu de 2 mm de chaque côté).

## Règles de design (DRC)

| Règle | Valeur |
|-------|--------|
| Clearance min. | 0,15 mm |
| Largeur piste min. | 0,15 mm |
| Piste alimentation 3,3 V | ≥ 0,5 mm |
| Via drill min. | 0,3 mm (mécanique) |
| Via annular ring | 0,15 mm |

## Notes de placement

- **TEF6687** (U1) : centré sur le PCB, face signal RF vers le connecteur SMA. Plan de masse solid sous U1.
- **STM32F072** (U2) : à 20 mm de U1, condensateurs découplage 100 nF en 0402 au plus près des pins VDD.
- **PCM5102A** (U3) : séparation plan analogique / numérique. AVDD filtré par ferrite L1.
- **AMS1117** (U5) : proche du connecteur USB-C, condensateur 47 µF en sortie.
- **Cristal** (X1) : longueur pistes XTAL < 5 mm, plan de masse sous le crystal.

## Fabrication

Gerbers compatibles **JLCPCB**, **PCBWay**, **Eurocircuits** :

```
Layers : F.Cu, B.Cu, F.Mask, B.Mask, F.Silkscreen, B.Silkscreen, Edge.Cuts, F.Paste
```

L'assemblage SMT peut être confié à JLCPCB (fichiers `fab/bom-jlcpcb.csv` + `fab/positions.csv`). Composants traversants (connecteurs, crystal) à souder manuellement.
