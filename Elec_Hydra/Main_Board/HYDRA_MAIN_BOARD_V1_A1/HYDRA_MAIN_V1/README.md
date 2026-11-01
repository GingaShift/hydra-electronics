# HYDRA MAIN BOARD V1 — A1 compacte

Projet de conception électronique du 27 octobre 2026. Ouvrir **HYDRA_MAIN_V1.kicad_pro** avec KiCad 9.0.9 ou ultérieur. Le projet est autonome : symboles et empreintes sont inclus dans `libraries`, avec tables relatives au projet. Le schéma comporte quatre feuilles. Le PCB a un contour provisoire **75 × 60 mm**, quatre couches et quatre fixations M2,5 (trous NPTH Ø2,7 mm). Le contour et les volumes connecteurs ne sont pas validés par la mécanique du ROV.

**STATUT : prototype d’ingénierie, NO-GO pour une commande de fabrication automatique.** Les fichiers sont réels; la conception et les contrôles numériques ne remplacent pas la qualification du premier matériel. Lire `docs/CHOIX_ET_VALIDATION.md`, les rapports KiCad et `docs/CONNECTEURS.md` avant toute commande. Les exports éventuels sont identifiés comme exports d’ingénierie.

## Contenu

- Schéma natif `.kicad_sch`, version PDF et PCB placé/routé `.kicad_pcb`.
- Symboles/empreintes locales, logo officiel extrait du PDF fourni.
- `docs/BOM.csv`, BOM détaillée, affectation complète des 64 broches, connectique et intégration.
- `reports/ERC.*`, `DRC.*`, `CONNECTIVITY.json` : résultats effectifs; `VALIDATION.md` donne leur interprétation.
- `previews` : vues du PCB, schéma et intégration; `fabrication` : exports réels pour revue.
- `scripts` et `design.json` : modèle de conception et génération reproductible. **Ne pas lancer les générateurs sur une version modifiée manuellement : ils reconstruisent le projet.** Les bibliothèques standards KiCad et `sexpdata` sont requis pour une reconstruction, pas pour ouvrir/utiliser le projet livré.

## Architecture

La STM32F405RGT6 surveille le BME280 interne, lit la Power Board par I2C et journalise en Flash SPI. Elle communique avec la Pi4 via le port SERIAL3 exposé par la Navigator. Aucune IMU, commande ESC, fuite, BAR30, commande Lumen ou puissance de bras/pince n’est dupliquée. Les huit broches V2 sont des signaux logiques sans drivers.

Les deux Lumen reçoivent leur énergie de la Power Board et le PWM commun de la Navigator. Aucun de ces fils ne traverse cette Main Board.

## Limites essentielles

5 V nominal uniquement; aucun raccordement au 48 V. Aucun 5 V externe sur les GPIO/ADC. Le connecteur d’extension fournit au plus 50 mA de 3,3 V au total. Alimentation et masses des cartes UART/I2C doivent suivre les règles d’intégration : débrancher les signaux vers une carte éteinte pendant les essais USB. SWD VTref est une mesure, pas une entrée d’alimentation. Ne pas alimenter le rail 3,3 V depuis un programmateur.

Le firmware applicatif et la configuration BlueOS ne font pas partie de cette livraison PCB. La programmation SWD et le démarrage du chargeur ROM USB sont prévus matériellement; leur fonctionnement sur carte assemblée n’a pas été testé.

Les modèles3D standards KiCad ne sont pas embarqués; aucune validation mécanique en3D n’est revendiquée. Les symboles et empreintes nécessaires au schéma et auPCB sont locaux.
