# Revue électrique indépendante — HYDRA MAIN V1

27 octobre 2026. Périmètre : les 87 éléments de `HYDRA_MAIN_V1/design.json`, leur modèle `scripts/design.py`, brochages et valeurs de support ; hors routage et validation de fabrication.

## Deux corrections identifiées

### 1. LED STATUS sur PC13 : à corriger

Dans le JSON examiné, U1.2/PC13 alimente R12 puis l'anode D5 ; la cathode D5 est à GND. Le GPIO fournit donc le courant de LED. **ST interdit explicitement PC13/PC14/PC15 comme sources de courant pour une LED** (DS8626, tableau 7 note 3 et tableau 49 note 1).

Correction minimale : `LED_STATUS` sur **U1.39/PC8**, libre ; U1.2 devient NC. Cette correction est déjà présente dans `scripts/design.py` au dernier contrôle, mais le JSON lu conservait encore PC13 : régénérer les livrables et leur ERC avant de figer le PCB.

### 2. HSE ABM8 8 MHz CL18 pF : marge de démarrage insuffisante

La datasheet Abracon ABM8 spécifie à 8–9,999 MHz **ESR maximal 400 Ω**, C0 maximal 3 pF, CL standard 18 pF. C10=C11=30 pF donne bien CL≈18 pF avec 3 pF parasites, mais cette cohérence de charge ne suffit pas à valider le quartz.

Selon AN2867 §3.4 : `gmcrit = 4 × ESR × (2πf)² × (C0+CL)²`.

Pour le quartz initial : **gmcrit=1,783 mA/V**, au-dessus de **Gmcritmax=1 mA/V** du STM32F405. Avec gm=5 mA/V, la marge est **2,80**, inférieure à 5. Le démarrage HSE et donc le DFU USB ne sont pas garantis sur les limites fabricant. Un essai sur un exemplaire ne lève pas cette incompatibilité de dimensionnement.

**Remplacement précis recommandé : ECS-80-10-33-CHN-TR**, ECS Inc., boîtier 3225 à 4 pads : 8 MHz, CL10 pF, ESRmax400 Ω, C0max**5 pF**, tolérance ±10 ppm, stabilité ±25 ppm, −40/+85 °C. Broches 1/3 signal, 2/4 masse, compatibles avec le symbole et le motif 3225 actuels. Ne pas lui appliquer le C0=3 pF de l'Abracon.

Avec C10=C11=**14 pF C0G** et l'hypothèse de 3 pF parasites : CL≈10 pF ; gmcrit=**0,910 mA/V**, marge=**5,50**, critère ST respecté sur les paramètres documentés. Les parasites réels, le niveau d'excitation et le démarrage sur plage de température restent à qualifier au prototype.

Le MPN est confirmé sur le site ECS. Le catalogue JLC/LCSC le référence **C7270713** ; les recherches de ce jour affichent un stock fournisseur, et DigiKey affiche plusieurs milliers de pièces. Ce sont des indications de disponibilité à revérifier lors de la commande, pas des réservations.

## Contrôles sans autre défaut critique identifié

| Bloc | Résultat du contrôle |
|---|---|
| Alimentation MCU | VDD19/32/48/64 et VBAT1 au 3,3 V ; VSS18/63 et VSSA12 à GND. Quatre 100 nF et 4,7 µF présents. |
| VCAP | C6/C7 chacun 2,2 µF vers GND ; VCAP1/2 séparés du 3,3 V. |
| Analogique | VDDA13 derrière FB1, avec 100 nF et 4,7 µF ; cohérent. |
| Boot/reset/debug | BOOT0 et BOOT1 au repos bas par 10 kΩ ; bouton BOOT vers 3,3 V ; reset vers GND, 100 nF et pull-up 10 kΩ ; SWDIO46/SWCLK49/SWO55 cohérents. |
| Interfaces MCU | USART3 PB10/PB11 ; I2C1 PB6/PB7 ; I2C3 PA8/PC9 ; SPI2 PB13/14/15 + CS PB12 ; TIM2 PA0–PA3 ; ADC PC0/PC1 : aucune collision. |
| USB-C | CC1/CC2 ont chacun leur 5,1 kΩ vers GND ; A/B D+ réunis et A/B D− réunis ; DM→PA11, DP→PA12 ; protection USBLC6 alimentée par VBUS ; aucun pull-up USB externe erroné. |
| PA9/VBUS | R8=33 kΩ en haut, R9=82 kΩ en bas : pont ST respecté. À VBUS=5,5 V et tolérances 1 % défavorables, PA9≈3,944 V <4 V même à VDD=0. |
| Flash | W25Q128JVSIQ : pins1/2/3/4/5/6/7/8 et MOSI/MISO corrects ; CS/WP/HOLD ont leurs pull-up 10 kΩ ; 100 nF local et 4,7 µF présents. |
| BME280 | GND1/7, CSB2=VDDIO6=VDD8=3,3 V, SDI3=SDA, SCK4=SCL ; SDO5 haut par 10 kΩ → adresse0x77 ; pull-up4,7 kΩ et deux100 nF conformes Bosch. Empreinte numérotée dans le sens horaire approprié. |
| LDO | AP7361C-33E-13 : 1=IN, 2=GND/tab, 3=OUT corrects ; C13/C14=4,7 µF cohérents. Ne pas substituer la variante ER ou un AMS1117 sans reprendre le brochage. |

**Verdict de cette revue : À corriger** pour la version initiale PC13 + quartz CL18 pF. Après PC8, remplacement ECS CL10 pF et régénération cohérente, aucun autre défaut électrique critique n'a été identifié dans le périmètre demandé. Le routage en cours reste à vérifier séparément.

## Sources primaires

- [ST DS8626 rev.12](https://www.st.com/resource/en/datasheet/stm32f405rg.pdf) : brochages, restrictions PC13, HSE et alimentation.
- [ST AN2867 rev.24](https://www.st.com/resource/en/application_note/an2867-oscillator-design-guide-for-stm8afals-stm32-mcus-and-mpus-stmicroelectronics.pdf) : §3.4, formule de marge HSE.
- [Abracon ABM8, révision29/07/2020](https://abracon.com/Resonators/abm8.pdf) : ESR400 Ω à8MHz, CL18pF et C0max3pF.
- [ECS, MPN exact ECS-80-10-33-CHN-TR](https://ecsxtal.com/products/crystals/surface-mount-crystals/ecs-80-10-33-chn-tr/) et [datasheet ECX-32](https://ecsxtal.com/store/pdf/ecx-32.pdf) : paramètres, boîtier et brochage.
- [ST AN4879 rev.12](https://www.st.com/resource/en/application_note/an4879-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf) : §2.6, pont PA9.
- [Winbond W25Q128JV rev.F](https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf) : brochage flash.
- [Bosch BME280 rev.1.24](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf) : §7, connexion I2C.
- [Diodes AP7361C](https://www.diodes.com/assets/Datasheets/AP7361C.pdf) : brochage SOT223 E et condensateurs.
- Disponibilité : [JLC C7270713](https://jlcpcb.com/partdetail/ECS-ECS_80_10_33_CHNTR/C7270713), [DigiKey](https://www.digikey.com/en/products/detail/ecs-inc/ECS-80-10-33-CHN-TR/12759418).
