# HYDRA Main Board V1 — alimentation, connecteurs, liaison Navigator

Vérification indépendante du 27 octobre 2026. Sources primaires fabricants uniquement pour les choix électriques et mécaniques. Ce document propose le câblage ; il ne valide pas une empreinte, un schéma ou un PCB non encore confronté au composant réel.

## Décisions à reprendre

- **Alimentation proposée V1 :** entrée PowerBoard 5 V / 4,75–5,25 V et USB VBUS protégées chacune, OR par deux Schottky, puis LDO **AP7361C-33E-13**, SOT223. Limite de conception 3V3 = **250 mA maximum continu**, dont 50 mA maximum sur le connecteur d’extension. Imposer une ambiance interne ≤60 °C et mesurer le régulateur sur le premier prototype.
- **UART recommandé :** utiliser le connecteur **SERIAL 3 du Navigator**, port documenté `/dev/ttyAMA1`, en logique 3,3 V, avec un câble adaptateur JST GH 6 voies → Molex Micro-Latch 3 voies. Ne pas brancher son +5 V. La disponibilité physique est documentée ; la disponibilité logicielle sur le véhicule doit être réservée et vérifiée.
- **Connecteurs :** Micro-Fit 3.0 **43045-0200** coudé THT 2 contacts pour le 5 V ; Micro-Latch **53253-0370**, **53253-0470**, **53253-1070** verticaux THT pour UART, I2C/ALERT et extension.
- **Bloquants avant fabrication :** réserver SERIAL 3 dans la configuration réellement utilisée ; définir le séquencement des cartes INA226 ; vérifier sur les dessins Molex le sens physique du pin 1 et les trous de maintien. Le budget USB avant configuration doit être prouvé par mesure et par un état firmware dédié.

## Chemin d’énergie concret

PowerBoard : `J_PWR.1 → F_PWR → D_PWR anode → cathode → +5V_OR`.

USB : `VBUS connecteur USB-C → F_USB → D_USB anode → cathode → +5V_OR`.

`+5V_OR → CIN → U_LDO.IN → U_LDO.OUT → +3V3`, avec toutes les masses communes. Les deux **cathodes** sont réunies ; les anodes ne le sont jamais. Les diodes bloquent le retour fonctionnel entre sources, mais une Schottky conserve un courant de fuite, qui augmente à chaud. Aucun +5V_OR ne doit être présenté comme une sortie 5 V régulée.

Choix simple : deux **PMEG4010BEA,115** Nexperia, SOD323, 40 V / 1 A, pin 1 cathode et pin 2 anode. À 25 °C, VF maximum vaut 350 mV à 100 mA et 470 mV à 500 mA ; IR maximum à 10 V vaut 20 µA. Ne pas affirmer « zéro courant inverse » et vérifier le comportement à chaud et l’absence de tension parasite sur les connecteurs débranchés. À 250 mA, prévoir environ 0,08–0,12 W dans la diode conductrice et du cuivre ; la classe 1 A est conditionnée par la température du point de soudure. [Nexperia PMEG4010BEA, pages 1–3](https://assets.nexperia.com/documents/data-sheet/PMEG4010BEA.pdf).

Une **SS14-E3/61T** Vishay en SMA est une alternative plus grosse et facile à assembler, 1 A / 40 V. Il faut figer le fabricant exact, pas seulement « SS14 ». Ses caractéristiques de fuite doivent aussi être considérées. [Vishay SS12–SS16](https://www.vishay.com/docs/88746/ss12.pdf).

Mettre F_PWR et F_USB **avant** les diodes, près des connecteurs. Référence proposée : **Littelfuse 1206L050/15YR**, PPTC 1206, 15 V, Ihold=0,50 A et Itrip=1 A à 20 °C, R1max=0,75 Ω. Son maintien publié est 0,35 A à 60 °C et 0,31 A à 70 °C ; le placer loin du LDO pour conserver la marge à 250 mA. En prenant 0,75 Ω et VF=0,47 V, le minimum PowerBoard de 4,75 V laisse encore environ 4,09 V à l’entrée LDO à 250 mA : marge suffisante sur 3,3 V. Vérifier les tolérances réelles de câble et température. Un fusible ne limite pas à 100 mA le courant d’un périphérique USB et ne protège pas une GPIO. Prévoir points de test VBUS brut, 5V_PWR brut, +5V_OR, +3V3 et GND. [Littelfuse 1206L, février 2024, valeurs et courbes de déclassement](https://www.littelfuse.com/assetdocs/littelfuse-ptc-1206l-datasheet?assetguid=2b6a1515-d4ee-4c83-8bd4-152b4901b8f5).

Si l’exigence signifie une isolation de retour à très faible fuite garantie à chaud, remplacer l’OR Schottky par un vrai circuit de sélection et relire son schéma d’application. Deux **LM66100DCKR** peuvent remplir ce rôle ; **ne pas relier CE à GND en supposant conserver le blocage inverse** : la fonction RCB impose CE relié à VOUT. Le montage OR croisé possède une subtilité lorsque les entrées sont égales ; préférer l’application fabricant avec priorité et sortie continue, pas un schéma improvisé. [TI LM66100, §8.3.2 et §9.2](https://www.ti.com/lit/ds/symlink/lm66100.pdf) ; [TI LM66100-Q1, §9.2.2 pour la subtilité des tensions égales](https://www.ti.com/lit/ds/symlink/lm66100-q1.pdf).

## Régulateur : choix et thermique

**AP7361C-33E-13** est une solution V1 plus sûre thermiquement qu’un AP2112K ou TLV75533PDBVR standard, au prix de sa surface SOT223. **Brochage de la variante E : 1=IN, 2=GND, 3=OUT, languette=GND. Pas d’EN sur cette variante.** Ne pas utiliser un symbole AMS1117 ou la variante SOT223R sans remappage. Placer 4,7 µF X7R en entrée et en sortie au plus près ; la capacité effective de sortie sous polarisation/température doit rester ≥2,2 µF. Relier le grand pad 2 au cuivre GND pour dissiper. [Diodes AP7361C, pages 1–2, 6 et mécanique SOT223](https://www.diodes.com/datasheet/download/AP7361C.pdf).

Calcul conservateur, sans crédit de chute dans la diode : `P=(5,25−3,3)×I`. À 200 mA : 0,390 W ; à 250 mA : **0,488 W**. Avec θJA typique SOT223 110 °C/W du fabricant : élévations de 43 °C et 54 °C. À 60 °C ambiant interne, le dernier cas donne environ **114 °C de jonction** ; ce calcul de premier ordre reste à qualifier sur le PCB et dans le boîtier. La température ambiante est celle de l’air autour de la carte, pas celle de l’eau extérieure. À 85 °C, ne pas revendiquer une marge confortable à 250 mA : utiliser davantage de cuivre avec mesure, une variante à pad thermique ou un buck.

Pour comparaison, AP2112K-3.3TRG1 SOT25 : θJA publié 184 °C/W, soit +90 °C à 0,488 W ; le « 600 mA » n’est pas un budget thermique. Le TLV75533PDBVR DBV standard : θJA JEDEC **231,1 °C/W**, et 100,8 sur carte EVM. **60,3 °C/W concerne le boîtier DYD à pad thermique sur EVM**, pas le DBV standard. Ces boîtiers ne sont donc pas retenus ici à 250 mA sans étude de cuivre/ambiance. [Diodes AP2112](https://www.diodes.com/assets/Datasheets/AP2112.pdf) ; [TI TLV755P Rev D, tableau thermique page 5](https://www.ti.com/lit/ds/symlink/tlv755p.pdf).

Un buck tel que **TPS62162DSGR**, fixe 3,3 V / 1 A, réduit la chaleur si le boîtier est chaud ou si 250 mA devient une charge fréquente. Le montage de référence emploie 2,2 µH, 10 µF d’entrée et 22 µF de sortie, avec un placement de commutation strict ; à 0,825 W en sortie et rendement hypothétique 90 %, la perte du convertisseur est ~92 mW. Le rendement de 90 % est une hypothèse de budget à vérifier, pas une garantie à ce point. Ici le LDO SOT223 est défendable car la puissance reste <0,5 W et l’assemblage est plus simple ; préférer le buck si l’ambiance >60 °C n’est pas exclue. [TI TPS62162, application fixe et layout](https://www.ti.com/lit/ds/symlink/tps62162.pdf).

Ne jamais alimenter +3V3 depuis un adaptateur SWD ou une carte externe : les LDO choisis ne sont pas des dispositifs d’isolation inverse. La broche VTref SWD doit être un **sens de tension**, sans strap d’alimentation de l’adaptateur.

## Budget et contrainte USB

Réserver **200 mA maximum** à la logique interne (MCU, flash, BME280, voyants, pull-ups, marge) et **50 mA maximum total** à la broche 3V3 d’extension. Les 50 mA ne sont ni par GPIO, ni un courant d’actionneur ; chaque courant GPIO et les sommes par port/MCU doivent rester dans les limites STM32. Les INA226 externes sont alimentés par leurs cartes, sans VCC dans le connecteur I2C à quatre contacts.

En USB 2.0 FS/HS classique : **100 mA maximum avant configuration, 500 mA maximum après configuration acceptée**, et le descripteur doit annoncer une consommation maximale cohérente ; la limite de suspension est 2,5 mA. Des résistances CC 5,1 kΩ n’autorisent pas à supposer 1,5 A ou 3 A sans détection de l’annonce Rp. [USB-IF, procédure d’interopérabilité Type-C, §2.2](https://usb.org/sites/default/files/3.2%20Interoperability%20Testing%20v1.03%20w%20USB%20Type-C.pdf).

Pour rendre l’alimentation USB seule crédible : démarrer à basse fréquence, flash externe en veille, sorties et LED de fonction désactivées, extension non chargée, puis n’activer l’état 200–250 mA qu’après `SET_CONFIGURATION`. Fixer une cible **≤80 mA mesurés** avant configuration pour garder de la marge sous 100 mA. Cette cible exige une vérification firmware/mesure ; un F405 à 168 MHz et flash active ne permet pas de l’assumer. Traiter aussi reset USB, déconfiguration et suspend. Une alimentation de laboratoire USB-C sans hôte n’énumère jamais : autoriser le mode pleine charge uniquement avec une alimentation dédiée identifiée correctement, ou par configuration laboratoire explicite.

Le VBUS-sense doit mesurer le VBUS du **connecteur**, avant OR, afin de distinguer câble USB présent et alimentation par PowerBoard. Le cumul des capacités vues à la connexion et l’appel de courant doivent être vérifiés ; ne pas ajouter arbitrairement de gros électrolytique directement sur VBUS. Le fusible et l’OR ne constituent pas une limitation active d’appel de courant.

## Connecteurs et empreintes exactes

Toutes les références sont Molex. Les modèles THT peuvent nécessiter une soudure manuelle séparée de l’assemblage SMT économique.

| Fonction | Référence PCB | Boîtier câble femelle | Contacts femelles conseillés | Empreinte KiCad |
|---|---|---|---|---|
| Entrée 5 V, 2 contacts | **43045-0200** coudé THT, Micro-Fit 3.0 | **43025-0200** | **43030-0007** en sachet, AWG20–24, étamés ; câble AWG24 adapté | `Connector_Molex:Molex_Micro-Fit_3.0_43045-0200_2x01_P3.00mm_Horizontal` |
| UART, 3 contacts | **53253-0370**, vertical THT | **51065-0300** | **50212-8100** en sachet / **50212-8000** en bande, AWG24–30 | `Connector_Molex:Molex_Micro-Latch_53253-0370_1x03_P2.00mm_Vertical` |
| I2C + ALERT, 4 contacts | **53253-0470**, vertical THT | **51065-0400** | mêmes contacts 50212 | `Connector_Molex:Molex_Micro-Latch_53253-0470_1x04_P2.00mm_Vertical` |
| Extension, 10 contacts | **53253-1070**, vertical THT | **51065-1000** | mêmes contacts 50212 | `Connector_Molex:Molex_Micro-Latch_53253-1070_1x10_P2.00mm_Vertical` |

Les 43030-0007 admettent un isolant ≤1,85 mm ; les 50212 admettent un isolant ≤1,40 mm. Utiliser la pince et le réglage de sertissage prévus pour le contact/fil, avec essai d’arrachement ; ne pas souder un fil à la place d’un sertissage puis le considérer équivalent. [Molex 430300007](https://www.molex.com/en-us/products/part-detail/430300007) ; [Molex 502128000 et alternative sachet](https://www.molex.com/en-us/products/part-detail/502128000).

### Contrôles mécaniques obligatoires

**Micro-Fit 43045-0200 :** THT coudé avec maintien plastique, pas une version verticale ou SMT. Entraxe électrique 3 mm ; trous de maintien non métallisés à conserver. Le dessin impose une position à **10,16 mm maximum du bord selon son détail de localisation**, pour éviter l’interférence câble/carte. Le câble sort horizontalement ; réserver l’espace du boîtier, du verrou et de sa manipulation. Vérifier la version de l’empreinte à l’aide du dessin : [dessin Molex officiel 430450200, 2 pages](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/430/43045/430450200_sd.pdf?inline=) et [dessin boîtier 430250200](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/430/43025/430250200_sd.pdf?inline=).

**Micro-Latch 53253 :** trous électriques Ø0,80 ±0,05 mm recommandés par Molex, entraxe 2,00 ±0,10 mm non cumulatif, queue 3,5 ±0,5 mm pour PCB 1,6 mm. Distance pin1–pinN : 4/6/18 mm pour 3/4/10 voies ; largeur externe C : 8/10/22 mm. Le plan de perçage est symétrique : **le PCB n’empêche pas de monter le connecteur à 180°**. Le repère de circuit 1 moulé et le côté du détrompage doivent apparaître sur le plan d’assemblage et la sérigraphie. [Dessin Molex commun 532530000-SD Rev A, toutes tailles dont 0370/0470/1070](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/532/53253/532530370_sd.pdf?inline=).

Ne jamais déduire « gauche=1 » sans préciser la vue. Définir les tables suivantes par **numéro de cavité/contact moulé**, puis contrôler la continuité d’un câble prototype. La vue d’accouplement du boîtier câble et la vue arrière côté fils sont en miroir. Les brochages ci-dessous sont des conventions HYDRA proposées, pas une convention électrique imposée par Molex.

## Brochages recommandés

| Connecteur HYDRA | Broche | Signal | Observation |
|---|---:|---|---|
| PWR 2 voies | 1 | +5V_PWR_IN | Rouge ; 4,75–5,25 V sur le connecteur, courant carte seulement |
| PWR 2 voies | 2 | GND | Noir |
| UART 3 voies | 1 | GND | Référence commune obligatoire |
| UART 3 voies | 2 | HYDRA_TX | Sortie STM32 3,3 V vers RX Navigator |
| UART 3 voies | 3 | HYDRA_RX | Entrée STM32 depuis TX Navigator |
| I2C/ALERT 4 voies | 1 | GND | Pas de tension d’alimentation sur ce câble |
| I2C/ALERT 4 voies | 2 | I2C_EXT_SCL | Open drain, niveau haut 3,3 V |
| I2C/ALERT 4 voies | 3 | I2C_EXT_SDA | Open drain, niveau haut 3,3 V |
| I2C/ALERT 4 voies | 4 | INA_ALERT_N | Wired-OR, actif bas |
| EXT 10 voies | 1 | GND | Retour |
| EXT 10 voies | 2 | +3V3_EXT | 50 mA total maximum, protéger ou au moins limiter/documenter |
| EXT 10 voies | 3–10 | GPIO_EXT1…GPIO_EXT8 | Logique 3,3 V uniquement ; pas de charge de puissance |

Il faut reprendre les numéros GPIO STM32 de l’allocation globale et réserver les états au reset avant de figer l’extension. Ajouter 33–100 Ω en série sur UART près des sorties comme option de damping/protection modérée ; ces résistances ne rendent pas une entrée tolérante à une alimentation absente.

## Navigator : preuve et limites

Blue Robotics expose officiellement SERIAL1, SERIAL3 et SERIAL4 sous forme de JST GH 6 voies : 1=+5V, **2=TX sortant**, **3=RX entrant**, 4/5 non connectés, **6=GND**. SERIAL3 est documenté `/dev/ttyAMA1`, SERIAL4 `/dev/ttyAMA2`. Les niveaux UART sont 3,3 V. Le port SERIAL1 est mini-UART `/dev/ttyS0` et recommandé par Blue Robotics pour une radio ; choisir SERIAL3 évite de dépendre de la console GPIO14/15 et du mini-UART.

| Câble adaptateur | Pin Navigator SERIAL3, JST GH | Pin HYDRA UART, Micro-Latch |
|---|---:|---:|
| GND | 6 | 1 |
| Navigator RX ← HYDRA TX | 3 | 2 |
| Navigator TX → HYDRA RX | 2 | 3 |
| +5V | 1 | **Pas de fil** |
| Réservés | 4, 5 | Pas de fil |

Côté Navigator, boîtier **JST GHR-06V-S**, contacts **SSHL-002T-P0.2** ; le connecteur PCB Navigator est **BM06B-GHS-TBT(LF)(SN)(N)**. [Guide matériel Navigator, Serial Devices](https://bluerobotics.com/learn/navigator-hardware-setup/).

Verdict matériel : **OK**, aucun besoin de modifier le Navigator ou de récupérer des pins sous la carte. Verdict système : **À vérifier**. Le nom du port et son utilisation doivent être confirmés dans l’image BlueOS utilisée, sans service ArduPilot, télémétrie, GPS ou console qui le revendique. La documentation Raspberry Pi confirme que les UART supplémentaires du Pi4 sont des PL011 et nécessitent la bonne configuration Device Tree ; GPIO14/15 correspond au port primaire et peut porter une console. [Documentation Raspberry Pi UART](https://www.raspberrypi.com/documentation/computers/configuration.html#configure-uarts).

## Bus externe INA226 et ALERT

Le besoin 6–9 INA226 tient dans les **16 adresses 7 bits 0x40–0x4F**. Pour neuf capteurs, attribuer 0x40…0x48 sans doublon ; documenter A1/A0 de chaque carte. Pour les quatre premières adresses : A1=GND et A0=GND/VS/SDA/SCL ; puis A1=VS et A0=GND/VS/SDA/SCL pour 0x44…0x47 ; 0x48 correspond à A1=SDA, A0=GND. BME280 interne à 0x77 n’est pas dans cette plage et devrait rester sur son bus interne dédié.

INA226 : tension de mesure recommandée **0–36 V**, alimentation **2,7–5,5 V** et mesure indépendante de VS. Ne pas utiliser 40 V, limite absolue, comme tension de fonctionnement. ALERT est une sortie open drain ; relier les ALERT en parallèle, pull-up unique vers 3,3 V, configurer la polarité active basse, et lire les registres de tous les INA concernés après interruption. La ligne partagée ne fournit pas directement l’identité du capteur. [TI INA226 Rev C, brochage, limites et programmation](https://www.ti.com/lit/ds/symlink/ina226.pdf).

Prévoir les pull-ups externes sur HYDRA en options : **2,2–4,7 kΩ** sur SCL/SDA, **10 kΩ** sur ALERT, tous vers 3,3 V. Une seule paire effective SCL/SDA ; retirer ou intégrer au calcul les pull-ups des modules. Avec neuf modules à 4,7 kΩ, leur parallèle vaut ~522 Ω : trop agressif sans étude du courant bas. Débuter à 100 kHz, câblage court et topologie maîtrisée ; mesurer temps de montée et capacité totale avant 400 kHz. Le calcul de premier ordre est `tr≈0,8473×Rp×Cb` ; 4,7 kΩ/400 pF donne ~1,59 µs, donc même 100 kHz demande alors de réduire Rp ou la capacité.

**Séquence d’alimentation à figer :** l’INA226 spécifie SCL≤VS+0,3 V ; une carte INA éteinte ne doit pas recevoir 3,3 V de pull-up sur SCL. Réciproquement, des modules restés alimentés et munis de pull-ups ne doivent pas injecter dans un STM32 HYDRA éteint. Les résistances série n’apportent pas d’isolation garantie. Le connecteur à quatre fils sans rail d’alimentation ne permet pas de garantir ce point seul. Choisir soit une règle système « tous les VS INA présents avant bus actif, aucun module éteint individuellement, aucune traction externe quand HYDRA est éteinte », soit des isolateurs/buffers à comportement hors tension documenté sur les cartes concernées et une validation de leur activation. **Bloquant si l’ordre d’alimentation reste indéfini ou si les INA peuvent être arrêtés individuellement sans isolation.**

## Vérifications de prototype

Mesurer courant USB avant configuration/reset/suspend, courant au maximum 3V3, température LDO à 5,25 V et ambiance visée, et +3V3 pendant branchement/débranchement successif des deux sources. Tester les deux sources simultanées, l’une éteinte et l’autre présente, ainsi que le retour éventuel sur VBUS et PowerBoard. Vérifier chaque câble au multimètre par numéro de cavité ; utiliser ensuite un échange UART avec checksum et un scan I2C à toutes les adresses allouées. Ces vérifications ne remplacent pas ERC/DRC et contrôle des dessins.
