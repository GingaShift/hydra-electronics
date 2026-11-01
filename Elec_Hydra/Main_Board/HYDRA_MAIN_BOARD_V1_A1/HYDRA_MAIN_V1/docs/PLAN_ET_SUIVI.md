# HYDRA Main Board V1 — conception et suivi

Cahier des charges : mission utilisateur du 27 octobre 2026. Exécution autonome explicitement demandée.

1. Auditer les ébauches et les outils; comparer les composants aux sources constructeur.
2. Figer les sources 5 V/USB, protections et régulation; établir les interfaces et le pin mapping.
3. Générer un schéma natif lisible et les bibliothèques locales, puis vérifier connectivité et ERC.
4. Placer et router un PCB quatre couches; intégrer le logo extrait du document officiel.
5. Exécuter les contrôles disponibles, corriger les erreurs et exporter uniquement les états cohérents.
6. Produire BOM, connectique, guide d’intégration et rapports; archiver le projet complet.

## Critères
- Aucune commande moteur, fuite, BAR30, IMU ou Lumen dupliquée.
- Huit GPIO accessibles; deux bus I2C indépendants; UART 3,3 V et SWD.
- Sources USB et PowerBoard isolées; aucune entrée 48 V.
- Conformité PCB vérifiée avec de vrais outils ou limitations explicites.
- Contour mécanique provisoire.

## Journal
- Audit initial : PCB fourni vide (79 octets). Sources en syntaxe KiCad 10.
- BME280 : empreintes C24/R7 incorrectes dans l’ébauche; bloc à reconstruire.
- LSM6DSL retiré selon le cahier des charges.
- KiCad absent initialement; installation native en cours.

- Schéma natif4feuilles et bibliothèques générés.
- Revue électrique indépendante intégrée; PC8/quartz corrigés.
- PCB placé/routé75x60mm; plansGND/3V3 remplis.
- ERC0, DRC0, aucune liaison non routée et aucune divergence XML/pad.
- Gerbers/Drill/BOM/POS exportés. Qualification physique et mécanique restante : NO-GO commande automatique.
