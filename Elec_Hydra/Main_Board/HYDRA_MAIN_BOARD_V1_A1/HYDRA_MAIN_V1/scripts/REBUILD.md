# Reconstruction facultative (écrase le projet généré)

Le projet livré est déjà routé. Pour le reconstruire à partir du modèle, dans une copie de travail :

1. Installer KiCad9.0.9 avec bibliothèques symboles/empreintes et bindingsPython, `sexpdata`, Freerouting1.9.0/Java17 et un affichage disponible (ou Xvfb).
2. Adapter `ROOT` dans `generate.py` au dossier standard KiCad contenant `symbols/` et `footprints/`. Le chemin standard `/usr/share/kicad` est utilisé automatiquement si les outils du dossier initial sont absents. Le modèle de projet est inclus dans `scripts/templates`.
3. `python3 scripts/generate.py` : schémas, bibliothèques, propriétés et `design.json`.
4. Python avec `pcbnew` : `python3 scripts/pcb.py` : placement, USB prédéfini, fanouts d’alimentation, plans remplis, exportDSN.
5. `java -jar freerouting-1.9.0.jar -da -de reports/HYDRA_unrouted.dsn -do reports/HYDRA_fast.ses -mp 15 -mt 1 -oit 50` ; attendre la fin et vérifier que leSES est non vide. Un afficheur X est nécessaire avec1.9.0.
6. `kicad-cli sch export netlist HYDRA_MAIN_V1.kicad_sch --format kicadxml -o reports/schematic_netlist.xml`.
7. `python3 scripts/finalize.py` avec `pcbnew` : importSES obligatoire, correspondance au schéma et remplissage final. Vérifier CONNECTIVITY.json.
8. Relancer ERC/DRC sans exclusion et avec la parité schéma; réexporterPDF, Gerber,Drill etPOS. Ne jamais réutiliser un ancien rapport après une modification.

`deliver.py` génère les tableaux/BOM mais copie également les rapports de revue depuis le dossier de travail initial. Sur une autre machine, les copies de revues absentes sont ignorées; elles n’interviennent pas dans la validité du projet KiCad livré. Les revues sont déjà présentes dans l’archive.

PourA1, après pcb.py, exécuter finish_status.py puis réexporter leDSN avec les couches internes de typepower avant Freerouting. La session finale fournie HYDRA_fast.ses inclut cette liaison; il n’est pas nécessaire de recalculer le routage pour utiliser la carte livrée. finish_status.py utilise numpy.
