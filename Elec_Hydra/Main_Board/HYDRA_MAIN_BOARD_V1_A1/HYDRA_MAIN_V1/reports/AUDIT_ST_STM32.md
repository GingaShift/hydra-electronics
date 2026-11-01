# HYDRA Main Board V1 — audit STM32 et flash

Audit documentaire du 27 octobre 2026. Confiance élevée sur le brochage et les fonctions alternatives ; le choix exact du quartz et la référence d'achat de la flash restent à figer. Ce document valide une affectation proposée, pas le PCB routé.

## Conclusions critiques

- **À corriger : PB8/PB9 sont I2C1_SCL/SDA, jamais I2C2.** PB6/PB7 et PB8/PB9 constituent deux affectations du même contrôleur I2C1 : ce ne sont pas deux bus indépendants.
- **OK : USART3 sur PB10/PB11**, AF7, broches 29/30. Ces broches sont également I2C2 ; les réserver au Raspberry Pi empêche leur emploi simultané pour I2C2.
- **OK : second bus indépendant sur I2C3 PA8/PC9**, AF4, broches 41/40. Pour éviter PC9, employer les quatre PWM sur PA0–PA3/TIM2.
- **À corriger : PA9 ne doit pas recevoir directement VBUS 5 V quand VDD peut être absent.** AN4879 recommande, à VDD 3,0–3,6 V, 33 kΩ entre VBUS et PA9, puis 82 kΩ de PA9 à GND, tolérance 1 %. La limite absolue FT dépend de VDD et devient 4 V à VDD=0.
- **À clarifier avant achat : « W25Q128JVSSIQ » n'est pas une référence listée dans la table Winbond consultée.** La référence officielle correspondant au SOIC-8 208 mil est **W25Q128JVSIQ**, avec un seul S. Ne pas approuver une ligne fournisseur au nom ambigu sans MPN fabricant vérifié.

## Affectation recommandée, sans conflit

Source : DS8626 rev. 12, figure 12, tableaux 7 et 9. Les directions TX/RX sont celles du STM32. Tous les connecteurs logiques sont en 3,3 V.

| Fonction/net | Broche STM32 | Nº LQFP64 | Configuration |
|---|---|---:|---|
| RPi_RX / STM_TX | PB10 | 29 | USART3_TX AF7 |
| RPi_TX / STM_RX | PB11 | 30 | USART3_RX AF7 |
| Power_SCL | PB6 | 58 | I2C1_SCL AF4, drain ouvert |
| Power_SDA | PB7 | 59 | I2C1_SDA AF4, drain ouvert |
| Sensors_SCL | PA8 | 41 | I2C3_SCL AF4, drain ouvert |
| Sensors_SDA | PC9 | 40 | I2C3_SDA AF4, drain ouvert |
| Flash_CS_N | PB12 | 33 | GPIO sortie, repos haut, pull-up 10 kΩ |
| Flash_SCK | PB13 | 34 | SPI2_SCK AF5 |
| Flash_MISO | PB14 | 35 | SPI2_MISO AF5 |
| Flash_MOSI | PB15 | 36 | SPI2_MOSI AF5 |
| USB_DM | PA11 | 44 | OTG_FS_DM AF10 |
| USB_DP | PA12 | 45 | OTG_FS_DP AF10 |
| USB_VBUS_SENSE | PA9 | 42 | Entrée de détection VBUS, pont 33k/82k |
| SWDIO | PA13 | 46 | Debug AF0 |
| SWCLK | PA14 | 49 | Debug AF0 |
| SWO, option | PB3 | 55 | Trace SWO/JTDO AF0 |
| PWM_EXT1 | PA0 | 14 | TIM2_CH1 AF1 |
| PWM_EXT2 | PA1 | 15 | TIM2_CH2 AF1 |
| PWM_EXT3 | PA2 | 16 | TIM2_CH3 AF1 |
| PWM_EXT4 | PA3 | 17 | TIM2_CH4 AF1 |
| GPIO_EXT1 | PC6 | 37 | GPIO, direction selon usage |
| GPIO_EXT2 | PC7 | 38 | GPIO, direction selon usage |
| ADC_EXT1 | PC0 | 8 | ADC1/2/3_IN10, mode analogique |
| ADC_EXT2 | PC1 | 9 | ADC1/2/3_IN11, mode analogique |

Les quatre canaux TIM2 partagent leur base de temps : rapports cycliques indépendants, fréquence commune. Si des fréquences différentes sont nécessaires, répartir les sorties entre plusieurs timers. Alternative valide : PC6/PC7/PC8/PC9 = TIM3_CH1/2/3/4 AF2, mais PC9 devient indisponible pour I2C3 ; il faudrait alors déplacer USART3 sur PC10/PC11 et utiliser I2C2 PB10/PB11, ou revoir les besoins.

Prévoir les pull-up I2C **vers 3,3 V** sur chaque bus ; vérifier celles des cartes distantes avant d'ajouter des résistances en parallèle. Les ADC externes restent entre GND et VDDA : ne pas leur attribuer la tolérance 5 V des entrées numériques FT. Les protections et filtres des entrées exposées doivent être dimensionnés selon le signal réel.

## Brochage physique complet STM32F405RGT6

LQFP64, corps 10×10 mm, pas 0,5 mm ; empreinte KiCad `Package_QFP:LQFP-64_10x10mm_P0.5mm`. Numérotation vue de dessus.

| Nº | Nom | Nº | Nom | Nº | Nom | Nº | Nom |
|---:|---|---:|---|---:|---|---:|---|
| 1 | VBAT | 17 | PA3 | 33 | PB12 | 49 | PA14 |
| 2 | PC13 | 18 | VSS | 34 | PB13 | 50 | PA15 |
| 3 | PC14/OSC32_IN | 19 | VDD | 35 | PB14 | 51 | PC10 |
| 4 | PC15/OSC32_OUT | 20 | PA4 | 36 | PB15 | 52 | PC11 |
| 5 | PH0/OSC_IN | 21 | PA5 | 37 | PC6 | 53 | PC12 |
| 6 | PH1/OSC_OUT | 22 | PA6 | 38 | PC7 | 54 | PD2 |
| 7 | NRST | 23 | PA7 | 39 | PC8 | 55 | PB3 |
| 8 | PC0 | 24 | PC4 | 40 | PC9 | 56 | PB4 |
| 9 | PC1 | 25 | PC5 | 41 | PA8 | 57 | PB5 |
| 10 | PC2 | 26 | PB0 | 42 | PA9 | 58 | PB6 |
| 11 | PC3 | 27 | PB1 | 43 | PA10 | 59 | PB7 |
| 12 | VSSA | 28 | PB2/BOOT1 | 44 | PA11 | 60 | BOOT0 |
| 13 | VDDA | 29 | PB10 | 45 | PA12 | 61 | PB8 |
| 14 | PA0 | 30 | PB11 | 46 | PA13 | 62 | PB9 |
| 15 | PA1 | 31 | VCAP_1 | 47 | VCAP_2 | 63 | VSS |
| 16 | PA2 | 32 | VDD | 48 | VDD | 64 | VDD |

## Circuit de support obligatoire

- VDD 19/32/48/64 → 3,3 V, 100 nF local par broche et un réservoir 4,7 µF proche ; VSS 18/63 → GND. Bien relier les deux pins VSS même si le symbole les superpose.
- VCAP_1 31 et VCAP_2 47 → **chacun son 2,2 µF céramique vers GND**, faible ESR (<2 Ω), très près du pad ; ne pas les relier au 3,3 V ni les utiliser pour alimenter autre chose. Le LQFP64 possède les deux VCAP.
- VDDA 13 → 3,3 V analogique, découplage 100 nF + 1 µF vers VSSA 12 ; ferrite possible si justifiée. VREF+ et VREF− ne sont pas des broches séparées dans ce boîtier : la référence analogique suit VDDA/VSSA.
- VBAT 1 → VDD avec 100 nF si aucune batterie de sauvegarde ; ne pas laisser flottante.
- NRST 7 : bouton vers GND, 100 nF vers GND et accès sur SWD. Pull-up interne présent ; un pull-up externe 10 kΩ est possible.
- BOOT0 60 : pull-down 10 kΩ, bouton/jumper vers 3,3 V. PB2/BOOT1 28 : pull-down 10 kΩ pour garantir le mode mémoire système quand BOOT0=1. Séquence DFU : maintenir BOOT0 haut, donner un reset, puis relâcher BOOT0. Mode normal BOOT0=0.
- SWD : 3,3 V de référence, GND, SWDIO, SWCLK, NRST ; SWO facultatif. Ne pas connecter une alimentation 5 V de programmateur sur VDD.

## Quartz HSE et USB DFU ROM

**OK : quartz passif 8 MHz entre PH0 5 et PH1 6.** Deux capacités de charge vers GND, une à chaque extrémité, valeurs déterminées par la datasheet du quartz : `CL = C1*C2/(C1+C2) + Cparasite`. Par exemple, CL=8 pF et parasite estimée à 2 pF donnent C1=C2≈12 pF ; ce n'est pas une valeur universelle. Confirmer CL, ESR, niveau d'excitation et marge de démarrage avec la référence achetée et le layout. Pour un oscillateur actif en mode HSE bypass, appliquer l'horloge sur PH0 et laisser PH1 libre : ne pas copier les capacités de charge d'un quartz passif.

AN2606 rev. 70, chapitre 34 : la ROM STM32F40xxx/41xxx sait programmer via USB FS sur PA11/PA12 et USART3 sur PB10/PB11. **Le DFU exige HSE après détection**, fréquence entière en MHz entre 4 et 26 MHz ; ST préfère 8 MHz à 25 MHz pour faciliter l'autodétection. Aucun pull-up externe sur USB_DP n'est requis. Conserver SWD comme accès de secours. Les lots peuvent embarquer les ROM V3.x ou V9.1 : ne pas supposer que les fonctions I2C/SPI de la ROM V9 existent sur tous les exemplaires.

Une configuration applicative possible avec HSE=8 MHz est PLLM=8, PLLN=336, PLLP=2, PLLQ=7 : CPU 168 MHz et USB 48 MHz. Le firmware doit réellement configurer cette horloge. SPI2 dépend d'APB1 ; à APB1=42 MHz, son horloge maître maximale pratique est 21 MHz (division minimale par 2).

## W25Q128JVSIQ — connexion et empreinte

Alimentation 2,7–3,6 V ; utiliser 3,3 V et 100 nF entre 8 et 4 près du boîtier. Brochage : **1=/CS, 2=DO/IO1 (MISO), 3=/WP/IO2, 4=GND, 5=DI/IO0 (MOSI), 6=CLK, 7=/HOLD ou /RESET/IO3, 8=VCC**. SPI simple : placer 10 kΩ de 1, 3 et 7 vers 3,3 V ; les pull-up de 3/7 fixent les états au démarrage sans empêcher une évolution ultérieure. Attention : l'option IQ a QE fixé à 1 en usine ; ne pas présenter /WP et /HOLD comme des protections matérielles actives garanties sur cette variante.

Code S : SOIC-8 **208 mil**, corps nominal 5,28×5,28 mm, pas 1,27 mm, envergure nominale 7,90 mm. Empreinte cohérente : `Package_SO:SOIC-8_5.3x5.3mm_P1.27mm` ; le SOIC-8 étroit 3,9 mm est incorrect. Le STM32F405 n'a pas de périphérique QuadSPI dédié : cette connexion exploite SPI2 simple.

## Réemploi des fichiers fournis

`Elec_Hydra(1).kicad_sch` contient déjà U1 `STM32F405RGTx` avec l'empreinte LQFP64 correcte, U3 `W25Q128JVS` avec le SOIC-8 large correct, C4/C5=2,2 µF et un quartz **Y1=12 MHz** avec C7/C8=22 pF. Les symboles/empreintes constituent une base réutilisable. Le changement vers 8 MHz exige une référence quartz et des capacités recalculées ; 12 MHz reste dans la plage DFU mais ne correspond pas au choix 8 MHz proposé. Les valeurs et empreintes présentes ne prouvent pas à elles seules les connexions ni le placement. Pas de validation ERC/DRC ni de GO fabrication dans cet audit partiel.

## Sources primaires

1. [ST DS8626 rev. 12, mars 2026, STM32F405xx/407xx](https://www.st.com/resource/en/datasheet/stm32f405rg.pdf) — figure 12 p.43 ; tableaux 7/9 ; alimentation et limites électriques.
2. [ST AN4488 rev. 7, octobre 2018](https://www.st.com/resource/en/application_note/an4488-getting-started-with-stm32f4xxxx-mcu-hardware-development-stmicroelectronics.pdf) — §2 alimentation, §3 reset, §4 boot, §5 debug, §6 quartz.
3. [ST AN2606 rev. 70, février 2026](https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf) — chapitre 34, pp.161–169, tables 73–76 : ROM V3.x et V9.x, DFU et HSE.
4. [ST AN4879 rev. 12, juin 2026](https://www.st.com/resource/en/application_note/an4879-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf) — §2.6, pp.11–12 : PA9 hors alimentation et pont 33 kΩ/82 kΩ.
5. [Winbond W25Q128JV rev. F, 27 mars 2018](https://www.winbond.com/resource-files/w25q128jv%20revf%2003272018%20plus.pdf) — pp.5,16,67,74–76 : brochage, QE, boîtier et références. Révision primaire accessible ; disponibilité actuelle de la référence non établie par ce document.

**Verdict de ce bloc : À corriger** pour l'hypothèse I2C2 sur PB8/PB9 et la protection PA9 si VBUS direct ; **à clarifier** pour le MPN flash et le quartz. Brochage recommandé ci-dessus : **OK** sous les réserves fonctionnelles indiquées.
