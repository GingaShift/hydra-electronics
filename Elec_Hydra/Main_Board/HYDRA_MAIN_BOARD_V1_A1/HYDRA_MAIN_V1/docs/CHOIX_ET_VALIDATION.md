# Choix techniques et réserves avant fabrication

## Sources et audit de départ

Les fichiers joints Elec_Hydra(1) et (2) ainsi que Capteurs(1) et (2) étaient identiques octet pour octet. Le PCB fourni ne contenait aucun placement ni cuivre. La STM32 et la Flash ont été conservées comme choix fonctionnels. Le support STM32 a été reconstruit : deux VCAP de 2,2 µF, quatre découplages VDD de 100 nF, réservoir 4,7 µF, VDDA filtrée par ferrite et 100 nF/4,7 µF. VBAT est reliée à3V3, sans pile. L’IMU et les interfaces actionneurs des ébauches sont retirées. Les empreintes manifestement erronées des passifs BME280 ont été remplacées.

Les sources KiCad10 ont été inspectées sous forme native textuelle, pas ouvertes avec KiCad10. Le nouveau projet a été généré et relu/exporté par KiCad9.0.9. Il n’y a pas eu d’essai d’ouverture dans l’interface graphique KiCad10. Les rapports proviennent des outils natifs9.0.9.

## Alimentation

Deux entrées protégées par PPTC1206L050/15YR et Schottky Vishay SS14-E3/61T aboutissent à +5V_SYS. Le suffixe SYS désigne la tension après diode, pas un rail de précision5V. Les cathodes sont communes; le courant d’une source ne peut pas alimenter fonctionnellement l’autre source. La fuite inverse intrinsèque des Schottky subsiste, surtout à chaud; il ne s’agit pas d’une isolation galvanique ni d’un blocage à fuite nulle.

Entrée PowerBoard contractuelle4,75–5,25V, USB VBUS5V standard, sans Power Delivery. Le LDO AP7361C-33E-13 accepte2,2–6V; **ne jamais lui appliquer12/24/48V**. Les diodes/fusibles ne sont pas un écrêteur de surtension garanti sous6V; une alimentation hors plage est interdite. Le rail peut rester régulé avec une chute diode/câble raisonnable : l’entrée doit rester au-dessus de3,3V + dropout + marge. Vérifier le minimum réel pendant les transitoires.

Le boîtier SOT223 E a IN1, GND2/languette, OUT3, contrairement à l’AMS1117. CIN/COUT4,7µF X7R0805; COUT effectif requis≥2,2µF après tolérance, polarisation et température. Le grand pad GND et ses vias dissipent vers le plan continu. Le routage logique0,2mm sur cuivre externe35µm est prévu pour250mA maximum; ce courant reste une limite de système, pas celle d’un actionneur.

Budget conservateur : MCU120mA, Flash25mA, BME1mA, voyants4mA, bus/pull-up5mA, auxiliaires/marge45mA =200mA; extension50mA =250mA maximum. Les mesures externes INA sont alimentées sur la PowerBoard. Au pire en négligeant la chute diode, P_LDO=(5,25−3,3)×0,25=0,488W. Avec θJA typique110°C/W : +54°C. Ambiance interne de conception≤60°C et contrôle thermique obligatoire du premier prototype. Ne pas interpréter le courant nominal1A du LDO comme un courant disponible sur cette carte.

Un buck TPS62162 abaisserait les pertes pour une charge durable importante ou une ambiance plus chaude, mais exigerait inductance, boucle de commutation et qualification supplémentaires. LDO retenu pour le bruit et la simplicité à cette charge. Deux LM66100 constituent une piste d’évolution pour diminuer la chute et la fuite, sous réserve d’appliquer exactement le montage de sélection constructeur; aucun circuit idéal improvisé n’est intégré enV1.

## Horloge et démarrage

Quartz ECS-80-10-33-CHN-TR8MHz CL10pF, C0max5pF, ESRmax400Ω; condensateurs14pF C0G. Avec3pF de parasites estimés, CL≈14/2+3=10pF. Calcul ST gmcrit=4×ESR×(2πf)²×(C0+CL)²≈0,910mA/V et marge≈5,50 pour gm5mA/V; critère minimal5. Le quartz CL18pF initial ne convenait pas à ce calcul. La capacité parasite et la marge doivent être confirmées sur prototype; essayer les limites de température et d’alimentation, pas seulement un démarrage à25°C.

BOOT0 :10kΩ vers GND, bouton vers3V3. BOOT1/PB2 :10kΩ vers GND. NRST :10kΩ vers3V3,100nF et bouton versGND. SWD accessible avec SWO optionnel. Entrer en ROM DFU : USB branché, maintenir BOOT, appuyer puis relâcher RESET, relâcher BOOT; tester l’énumération ST DFU. Le HSE8MHz convient aux conditions du chargeur ROM ST. La voie USB applicative demande un firmware USB device, PLL48MHz et gestion VBUS.

## USB et voyants

USB-C USB2 device uniquement, deux CC5,1kΩ indépendantes, D+/D− des deux orientations réunies, SBU NC, blindage relié àGND. USBLC6-2SC6 placé dans le trajet des données, condensateur VBUS100nF, résistances série22Ω côtéMCU. PA9 reçoit VBUS par33kΩ/82kΩ (maximum voisin de3,8V àVBUS5,25V, avant tolérances), au lieu du5V direct. Le raccordement a été repris pour garder la liaison principale courte surF.Cu, avec un croisement local au connecteur.

L’impédance différentielle doit être revue avec **le stackup précis du fabricant**. Le projet ne prétend pas disposer d’une impédance90Ω mesurée ou contrôlée, ni d’un résultat d’essai USB. Ne pas considérer ERC/DRC comme une preuve d’intégrité USB.

Avant configuration USB2 :≤100mA, après configuration seulement selon le descripteur et l’accord de l’hôte; en suspension≤2,5mA. Le firmware doit démarrer à faible consommation, éteindre Flash et chargesV2 tant que l’hôte n’a pas autorisé le courant, et gérer la suspension. Les résistances CC seules n’autorisent pas1,5/3A. Les essais correspondants ne sont pas exécutés; la V1 n’est pas déclarée périphérique USB certifié.

D3 PWR_5V verte :3,3kΩ, environ0,8mA. D4 PWR_3V3 verte :2,2kΩ, environ0,6mA. D5 STATUS bleue :1kΩ, typiquement0,3–0,5mA selon Vf. D6 DATA jaune :2,2kΩ, environ0,6mA. Ces courants sont des estimations avecVf typiques, pas une garantie photométrique à faible courant. STATUS utilisePC8; PC13 ne doit pas fournir le courant d’une LED. DATA est surPD2 et reste indépendante des lignes UART.

## Interfaces

I2C1 PB6/PB7 pour les INA226, pull-up2,2kΩ amovibles uniquement sur cette carte, vitesse initiale100kHz. Pour200pF de bus, tr≈0,8473×2,2k×200pF=373ns, inférieur à1µs en mode standard. Mesurer si le faisceau ou les cartes augmentent la capacité; ne pas annoncer400kHz sans mesure. ALERT est drain ouvert regroupable, pull-up10kΩ, série1kΩ et EXTI8/PB8, déclenchement descendant. Jusqu’à9adresses sur16disponibles. Le rail48V exige un composant de mesure adapté : jamais un INA226 directement au48V.

I2C3 PA8/PC9, pull-up4,7kΩ, BME280 à0x77 (CSBhaut, SDOhaut par10kΩ). Deux100nF locaux pourVDD/VDDIO. Flash W25Q128JVSIQ, SPI2 PB13/14/15, PB12 CS, WP/HOLD tirés au haut10kΩ. Démarrer SPI à faible fréquence, puis qualifier la fréquence maximale; l’écriture/effacement est à gérer contre les pertes d’alimentation et l’usure.

TIM2 PA0–PA3 fournit quatre PWM à base de temps commune. PC6/PC7 sont deux GPIO polyvalents; PC0/PC1 deux ADC. Aucun driver n’est présent. Les ADC sont limités à0..VDDA même si certains GPIO possèdent d’autres tolérances en mode numérique.

## Layout et mécanique

F.Cu signaux/composants, In1.Cu planGND continu, In2.Cu plan3V3, B.Cu signaux secondaires. Pas de routage de signal sur les plans internes. Cuivre35µm et FR4 sont hypothèses de fabrication. Épaisseur/stackup définitifs, hauteurs, orientation des verrous et enveloppeUSB à confronter à la mécanique avant commande. Vias traversantsØ0,6/perçage0,3mm; clearance nominale0,18mm; sérigraphie0,8mm minimum et0,12mm de trait pour les petits repères. Confirmer ces valeurs avec le fabricant retenu. Logo officiel wordmark40mm issu des tracés vectoriels du PDF, sans redessin approximatif; sa provenance et les petits détails sont documentés séparément.

## Qualification à réaliser

1. Valider contour/fixations/hauteurs et branchement des câbles sur une impression1:1 ou un prototype mécanique.
2. Contrôler les références achetées contre la BOM et les dessins, notamment le sens des Micro-Latch et le connecteur Micro-Fit SMD.
3. Réserver réellement SERIAL3 dans BlueOS/ArduSub et confirmer le croisementTX/RX; aucune configuration logicielle n’a été appliquée au ROV.
4. Qualifier l’alimentation sur banc : deux sources simultanées, débranchement, chute, fuite inverse, courantUSB et thermiqueLDO.
5. Programmer par SWD, vérifier HSE, ROMDFU, USB des deux orientations, BME280, ID/écriture/lectureFlash, busINA/ALERT et huitGPIO.
6. Revoir le stackup USB avec le fabricant et effectuer les essais de communication/ESD nécessaires.

**Verdict : NO-GO commande automatique.** La mécanique provisoire et les qualifications physiques/USB restent ouvertes. Aucun matériel n’a été fabriqué, programmé ou testé pendant cette mission.
