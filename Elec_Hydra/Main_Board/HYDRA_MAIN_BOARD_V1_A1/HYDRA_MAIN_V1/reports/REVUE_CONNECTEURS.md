# Revue des références réellement choisies — HYDRA Main V1

État relu : `HYDRA_MAIN_V1/design.json`, connecteurs et empreintes locales, 27 octobre 2026. Aucun fichier principal modifié par cette revue.

| Élément | Vérification | Verdict |
|---|---|---|
| J1 Molex 43650-0221 | Embase Micro-Fit 3.0 simple rangée, 2 voies, verticale **SMD**, maintien mécanique par trous. L’empreinte locale porte `attr smd`, deux pads SMD 1,27 × 2,54 mm à x=±1,5/y=3,135 et deux trous NPTH Ø2,41 à x=±3,65/y=−0,285. Pas de contradiction entre type du composant et type de l’empreinte. Le choix SMD a été confirmé par le responsable du projet. | OK pour le choix de type ; contrôle dimensionnel final selon dessin/échantillon à conserver |
| Câble J1 | **43645-0200**, simple rangée 2 voies, avec contacts femelles **43030-0007** pour AWG20–24. Le 43025-0200 proposé dans ma recherche initiale était destiné au 43045 double rangée : **ne pas l’utiliser avec J1 actuel**. | OK |
| D1/D2 | Le câblage JSON met les cathodes pin1 sur +5V_SYS et les anodes pin2 sur PB_FUSED / USB_FUSED : OR dans le bon sens. SS14-13-F attribué à Diodes Inc. n’a pas pu être validé par une datasheet primaire accessible ; le responsable a décidé le remplacement par **SS14-E3/61T Vishay**, SMA, dont la documentation primaire est disponible. | OK après mise à jour effective MPN/fabricant ; ne pas réutiliser les données PMEG pour SS14 |
| F1/F2 | **1206L050/15YR**, fusibles PPTC 1206 15 V, 0,5 A de maintien à 20 °C, 0,35 A à 60 °C ; R1max=0,75 Ω. Cohérent avec empreinte 1206 et budget 250 mA sous ambiance définie. | OK |
| U2 | **AP7361C-33E-13** : 1=IN, 2=GND et languette, 3=OUT, pas d’EN. JSON et empreinte locale SOT-223-3_TabPin2 respectent cette affectation. | OK |

Le rapport `research_power_connectors.md` était une proposition préalable, pas un relevé de la carte produite. Pour le câblage, **`HYDRA_MAIN_V1/docs/CONNECTEURS.md` fait foi** : ses brochages J2/J3/J4 reprennent les nets actuels, qui diffèrent des conventions initialement proposées.

Sources primaires :

- [Molex 43650-0221](https://www.molex.com/en-us/products/part-detail/436500221), notamment « Surface Mount » et « Vertical ».
- [Molex 43645-0200](https://www.molex.com/en-us/products/part-detail/436450200).
- [Molex Micro-Fit 3.0, correspondance des familles 43645 ↔ 43650 et contacts 43030](https://www.content.molex.com/dxdam/51/51a0d355-e3c6-469a-ad15-4585d36e4d38/987650-5984.pdf).
- [Molex 43030-0007, AWG20–24](https://www.molex.com/en-us/products/part-detail/430300007).
- [Vishay SS12–SS16, spécifications et SMA](https://www.vishay.com/docs/88746/ss12.pdf).
- [Littelfuse 1206L, février 2024](https://www.littelfuse.com/assetdocs/littelfuse-ptc-1206l-datasheet?assetguid=2b6a1515-d4ee-4c83-8bd4-152b4901b8f5).
- [Diodes AP7361C, brochage et thermique SOT223](https://www.diodes.com/datasheet/download/AP7361C.pdf).

Cette revue ne constitue pas un GO fabrication : la thermique à 250 mA, le courant USB avant configuration et le séquencement des bus demandent les validations de prototype déjà identifiées.
