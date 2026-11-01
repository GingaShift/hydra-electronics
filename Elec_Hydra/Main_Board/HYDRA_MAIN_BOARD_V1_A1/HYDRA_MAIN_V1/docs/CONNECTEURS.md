# Connecteurs et intégration — HYDRA Main Board V1

Brochages relevés dans `design.json` le 27 octobre 2026. Les numéros désignent les **contacts/cavités**, pas une position « gauche/droite » déduite d’une photographie. Ce document décrit la carte effectivement conçue et remplace les conventions de câblage du rapport de recherche préalable.

## Pièces à acheter pour les câbles

| Repère | Fonction et embase PCB | Partie câble compatible | Contacts / remarques |
|---|---|---|---|
| **J1** | Molex **43650-0221**, Micro-Fit 3.0, 1×2, pas 3 mm, vertical **SMD** avec maintien mécanique | Molex **43645-0200**, femelle simple rangée 2 voies | 2× **43030-0007**, femelles étamées, AWG20–24, isolant ≤1,85 mm ; AWG24 adapté à cette carte |
| **J2** | Molex **53253-0470**, Micro-Latch 2.0, 1×4, vertical THT | Molex **51065-0400** | 4× **50212-8100** en sachet ou **50212-8000** en bande ; AWG24–30, isolant ≤1,40 mm |
| **J3** | Molex **53253-0370**, Micro-Latch 2.0, 1×3, vertical THT | Molex **51065-0300** | 3× mêmes contacts 50212 ; câble adaptateur spécifique vers Navigator décrit plus bas |
| **J4** | Molex **53253-1070**, Micro-Latch 2.0, 1×10, vertical THT | Molex **51065-1000** | 10× mêmes contacts 50212 ; logique et alimentation auxiliaire limitée |
| **J5** | GCT **USB4105-GF-A**, USB-C USB 2.0, contacts SMD et ancrages de coque traversants | Câble USB-C **avec données USB 2.0**, vers ordinateur hôte USB-A ou USB-C | Pas de sertissage utilisateur. La carte est un périphérique USB ; elle ne fournit pas VBUS |
| **J6** | Würth **61301021121**, barrette mâle THT 2×5, pas **2,54 mm** | Embout femelle 2×5 au pas 2,54 mm, câblé à l’adaptateur SWD par numéro de broche | Ce n’est pas le connecteur Cortex Debug 1,27 mm. Vérifier le brochage de l’adaptateur ; pas de détrompage électrique |

**J1 n’accepte pas le 43025-0200 double rangée.** Le choix SMD du 43650-0221 est intentionnel : les trous de maintien ne transforment pas ses contacts électriques en THT. Pour les Micro-Latch, les trous électriques symétriques permettent une insertion de l’embase à 180° : le côté détrompage et le repère 1 doivent être contrôlés à l’assemblage. La vue arrière côté fils est le miroir de la vue d’accouplement ; vérifier un câble prototype au multimètre.

## J1 — entrée PowerBoard 5 V

| Broche | Net | Câble |
|---:|---|---|
| 1 | `PB_5V` | +5 V PowerBoard, 4,75–5,25 V sur le connecteur, rouge |
| 2 | `GND` | Masse, noir |

Cette entrée alimente la logique HYDRA, sans puissance pour éclairages, ESC ou actionneurs. Le fusible F1 puis D1 rejoignent `+5V_SYS` ; l’autre source arrive de J5 par F2 et D2. Les cathodes des diodes sont du côté `+5V_SYS`. La masse reste commune aux équipements.

## J2 — I2C PowerBoard et alerte INA226

| Broche | Net | Fonction |
|---:|---|---|
| 1 | `PB_SDA` | Données I2C, open drain |
| 2 | `PB_SCL` | Horloge I2C, open drain |
| 3 | `INA_ALERT` | Alerte commune, open drain, **active basse** |
| 4 | `GND` | Référence commune |

**Aucun VCC sur J2.** Les INA226 sont alimentés localement par les cartes de puissance. Les niveaux hauts du bus doivent être compatibles 3,3 V ; ne pas conserver des pull-ups de modules vers 5 V. Ne pas multiplier les pull-ups : calculer leur parallèle, puis vérifier le courant à l’état bas et les temps de montée. Commencer à 100 kHz avec câbles courts.

Exemple valide d’adressage de **neuf INA226**, adresses I2C **7 bits** :

| Capteur | Adresse | Strap A1 | Strap A0 |
|---:|---|---|---|
| 1 | `0x40` | GND | GND |
| 2 | `0x41` | GND | VS |
| 3 | `0x42` | GND | SDA |
| 4 | `0x43` | GND | SCL |
| 5 | `0x44` | VS | GND |
| 6 | `0x45` | VS | VS |
| 7 | `0x46` | VS | SDA |
| 8 | `0x47` | VS | SCL |
| 9 | `0x48` | SDA | GND |

`VS` est l’alimentation locale de l’INA226, pas la tension batterie mesurée. Les seize adresses possibles vont de 0x40 à 0x4F. Le BME280 interne est à 0x77 sur le bus interne : il ne remplace pas un INA et n’occupe pas l’une de ces adresses. La plage de mesure INA226 recommandée est 0–36 V ; 40 V est une limite absolue.

Les sorties ALERT des INA226 peuvent être réunies. Configurer toutes les alertes actives basses ; après interruption, lire les registres des capteurs concernés pour identifier la ou les causes. Une interruption commune ne donne pas seule l’identité du capteur.

### Séquencement et travail sur établi

**Si HYDRA est alimentée par USB alors que la PowerBoard/les INA sont éteints, débrancher J2.** SCL de l’INA226 est limité à VS+0,3 V : les pull-ups d’une carte alimentée peuvent injecter dans une carte éteinte. L’ordre inverse doit aussi être maîtrisé pour éviter des signaux externes sur une HYDRA éteinte. Couper l’alimentation avant branchement ; pas de connexion à chaud déclarée compatible.

Pour une intégration permanente, garantir que tous les VS INA sont présents avant l’activation du bus et qu’aucun module ne s’éteint seul, ou prévoir une isolation/buffer dont le comportement hors tension est documenté. Une résistance série seule ne garantit pas cette isolation. La procédure établi « J2 débranché » est une règle d’exploitation du prototype, pas une preuve d’immunité à tous les ordres d’alimentation.

## J3 — UART 3,3 V vers Navigator

| Broche HYDRA J3 | Net | Direction du point de vue HYDRA |
|---:|---|---|
| 1 | `UART_TX` | Sortie vers Navigator |
| 2 | `UART_RX` | Entrée depuis Navigator |
| 3 | `GND` | Masse commune |

Utiliser **SERIAL 3 du Navigator**, documenté `/dev/ttyAMA1`, plutôt que récupérer GPIO14/15 sous le Navigator. Il s’agit d’un port d’extension officiellement exposé, en logique 3,3 V. Réserver le port dans l’image BlueOS réellement installée ; vérifier qu’aucune télémétrie, GPS, console ou autre service ne l’ouvre. Le nom et la configuration sont ceux documentés par Blue Robotics ; les contrôler sur la machine cible avant de figer le logiciel.

| HYDRA J3 | Navigator SERIAL 3, JST GH 6 voies | Fil |
|---:|---:|---|
| **1** TX | **3** RX entrant Navigator | HYDRA TX → Navigator RX |
| **2** RX | **2** TX sortant Navigator | Navigator TX → HYDRA RX |
| **3** GND | **6** GND | Masse |
| Aucun | **1** +5 V | **Ne pas câbler** |
| Aucun | **4, 5** | Non câblés |

Côté Navigator : boîtier câble **JST GHR-06V-S**, contacts **SSHL-002T-P0.2**. L’embase Navigator documentée est **BM06B-GHS-TBT(LF)(SN)(N)**. Le câble comporte trois conducteurs effectivement raccordés et **croise TX/RX**. J3 n’alimente ni le Raspberry Pi ni le Navigator. Éviter les états où une extrémité continue de piloter une carte éteinte ; débrancher le câble pendant les essais de séquencement non validés.

## J4 — extension logique V2, huit signaux

| Broche | Net | Usage prévu |
|---:|---|---|
| 1 | `EXT_PWM1` | PWM logique 3,3 V |
| 2 | `EXT_PWM2` | PWM logique 3,3 V |
| 3 | `EXT_PWM3` | PWM logique 3,3 V |
| 4 | `EXT_PWM4` | PWM logique 3,3 V |
| 5 | `EXT_GPIO1` | GPIO logique 3,3 V |
| 6 | `EXT_GPIO2` | GPIO logique 3,3 V |
| 7 | `EXT_ADC1` | Entrée analogique dans la plage 0–3,3 V |
| 8 | `EXT_ADC2` | Entrée analogique dans la plage 0–3,3 V |
| 9 | `GND` | Masse |
| 10 | `+3V3` | Alimentation auxiliaire, **50 mA maximum total** |

Les 50 mA concernent l’alimentation auxiliaire totale ; ce n’est pas une permission de tirer 50 mA par sortie MCU. Respecter les limites par GPIO, groupe de broches et alimentation STM32. Les sorties nécessitant moteurs, relais, électrovannes ou autres charges de puissance ont besoin d’un étage de puissance externe. Les ADC ne sont pas des entrées 5 V.

## J5 — USB-C de service

J5 sert aux données USB 2.0 et à l’alimentation de laboratoire. Brancher un câble de données à un ordinateur hôte ; un câble de charge seul ne permet pas l’énumération. A6/B6 portent D+, A7/B7 portent D− ; CC1/CC2 sont séparés et disposent chacun de leur Rd. La présence physique d’un connecteur pouvant supporter plusieurs ampères n’autorise pas cette consommation.

Le firmware doit conserver une consommation USB ≤100 mA avant configuration et annoncer son budget après configuration ; la suspension demande aussi un mode approprié. La cible de projet avant configuration est ≤80 mA pour garder une marge. La pleine charge interne/extension ne doit pas être autorisée avant la configuration acceptée ou un mode laboratoire correctement défini. Tester l’USB dans les deux orientations du câble. Quand la PowerBoard est éteinte, appliquer la règle **J2 débranché** ci-dessus.

## J6 — SWD au pas 2,54 mm

| Broche | Signal | Note |
|---:|---|---|
| 1 | +3V3 / VTref | Référence de tension **à lire par la sonde** ; ne pas alimenter la carte depuis la sonde |
| 2 | SWDIO | Données SWD |
| 3 | GND | Masse |
| 4 | SWCLK | Horloge SWD |
| 5 | GND | Masse |
| 6 | SWO | Trace facultative |
| 7 | NC | Non raccordé |
| 8 | NC | Non raccordé |
| 9 | GND | Masse |
| 10 | NRST | Reset cible |

Le dessin du PCB utilise une numérotation impair/pair de deux rangées. Repérer le pad 1 et contrôler chaque fil d’un adaptateur ST-Link/J-Link. Un câble Cortex 10 broches au pas 1,27 mm ne s’accouple pas directement. J6 étant non détrompé, valider l’orientation avant de brancher.

## Lumen : trajet séparé

Les **Lumen ne traversent pas HYDRA Main Board**. Leur alimentation vient de la distribution de puissance prévue pour l’éclairage ; leurs fils jaunes de commande reçoivent le **même PWM d’un canal Navigator**, avec la masse de référence commune. Le partage d’un signal commande leur luminosité ensemble. Ni le courant d’éclairage, ni son signal de commande ne passent par J1–J6.

La commande Lumen est un PWM de type servo, environ 1100 µs pour éteint à 1900 µs pour pleine luminosité, pas un PWM de puissance ajouté sur J4. Vérifier le canal de sortie Navigator choisi et la configuration ArduPilot/BlueOS du véhicule avant mise sous tension de l’éclairage.

## Validation encore nécessaire

Ces références et tableaux ne constituent pas un GO fabrication. Contrôler les empreintes contre les dessins fabricant et un échantillon, l’orientation pin1/verrou et la continuité des câbles. Au prototype : mesurer courant USB avant configuration et en suspension, températures d’alimentation à la charge maximale, absence de retour significatif vers les sources éteintes, UART SERIAL 3 et I2C à neuf adresses. Les essais de séquencement doivent inclure toutes les combinaisons d’alimentation réellement permises.

## Sources officielles

- [Molex 43650-0221 — embase SMD verticale](https://www.molex.com/en-us/products/part-detail/436500221).
- [Molex 43645-0200 — boîtier simple rangée 2 voies](https://www.molex.com/en-us/products/part-detail/436450200).
- [Molex Micro-Fit — compatibilités 43645/43650 et contacts 43030](https://www.content.molex.com/dxdam/51/51a0d355-e3c6-469a-ad15-4585d36e4d38/987650-5984.pdf).
- [Molex 43030-0007](https://www.molex.com/en-us/products/part-detail/430300007) et [50212-8000 / alternative sachet 8100](https://www.molex.com/en-us/products/part-detail/502128000).
- [Molex Micro-Latch, dessin commun 53253](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/532/53253/532530370_sd.pdf?inline=) ; [boîtier 51065-0300 et familles associées](https://www.molex.com/en-us/products/part-detail/510650300).
- [GCT USB4105 — fiche et ressources fabricant](https://gct.co/connector/usb4105).
- [Würth 6130xx21121 — dessin barrette double 2,54 mm](https://www.we-online.com/components/products/datasheet/6130xx21121.pdf).
- [Blue Robotics — Navigator Hardware Setup, UART et brochages](https://bluerobotics.com/learn/navigator-hardware-setup/).
- [Raspberry Pi — configuration des UART](https://www.raspberrypi.com/documentation/computers/configuration.html#configure-uarts).
- [TI INA226 — adresses, limites SCL/VS et ALERT](https://www.ti.com/lit/ds/symlink/ina226.pdf).
- [Blue Robotics — Lumen, installation et PWM](https://bluerobotics.com/learn/lumen-light-r2-installation/).
- [USB-IF — courants de périphérique non configuré/configuré/suspendu, §2.2](https://usb.org/sites/default/files/3.2%20Interoperability%20Testing%20v1.03%20w%20USB%20Type-C.pdf).
