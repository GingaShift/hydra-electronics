# Revue finale indépendante — HYDRA MAIN V1 A1 compacte

27 octobre 2026. Relecture du PCB natif livré dans `HYDRA_MAIN_V1_OPT` et comparaison avec le modèle électrique de la version A0. Aucun fichier de conception modifié par cette revue.

**Aucun nouveau défaut bloquant identifié dans ce périmètre. Le statut reste NO-GO pour une commande automatique.**

La révision A1 conserve exactement les références, valeurs, nets, symboles, empreintes, fabricants et MPN du modèle électrique A0. Les 84 composants physiques sont présents sur le PCB ; le logo porte le total à **85 empreintes**. Les trois PWR_FLAG du modèle ne sont pas des composants physiques. La comparaison des nets de chaque pastille physique avec le modèle ne révèle aucun écart.

Le contour natif est un rectangle fermé de **75 × 60 mm**, contre 90 × 75 mm en A0, soit une réduction de surface de **33,3 %**. Le PCB relu contient réellement **quatre couches cuivre, 675 segments et 118 vias**. Les plans GND sur In1.Cu et +3V3 sur In2.Cu sont remplis et chacun possède une seule région principale ; aucune piste de signal n'est présente sur les couches internes.

DRC avec parité schéma/PCB relancé sous KiCad 9.0.9 : **0 violation, 0 connexion non routée, 0 écart de parité**. Le rapport ERC livré reste à **0 violation** ; le modèle électrique et le schéma ne sont pas modifiés par cette compaction. Aucun texte visible de carte ou d'empreinte ne dépasse le contour. La boîte englobante du titre `MAIN BOARD V1` se termine à y=59,479 mm, à l'intérieur du bord de 60 mm.

Les conclusions électriques précédentes restent applicables : brochages J1–J6 cohérents, D1/D2 cathodes vers +5V_SYS, U2 AP7361C-33E-13 avec IN=1, GND=2 et languette=2, OUT=3. La compaction ne constitue pas une qualification supplémentaire de l'alimentation, de l'USB ou des interfaces.

Les réserves physiques restent inchangées : mécanique et orientation des câbles à valider sur cette nouvelle implantation, stackup et liaison USB à qualifier, séquencement des interfaces et alimentation/thermique à tester sur prototype. Les fichiers de fabrication et de placement sont des exports d'ingénierie ; aucune qualification physique, configuration BlueOS ou validation de commande PCBA n'est revendiquée. Les contrôles numériques réussis ne lèvent pas ces réserves.
