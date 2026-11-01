# Exports d’ingénierie A1 — ne pas commander automatiquement

Gerbers quatre couches, masque, sérigraphie, pâte, contour et perçages PTH/NPTH proviennent du même projet final que la BOM et le fichier de positions. Le schéma, le routage et les exports sont réels. ERC0/DRC0 ne lèvent pas les réserves mécaniques, de stackupUSB, de thermique ou d’assemblage.

Spécification proposée :4couches FR4,1,6mm total, cuivre nominal35µm, masque au choix, ENIG recommandé pour la finesse des pastilles. **Le fabricant doit définir le stackup avant de revendiquer une impédanceUSB contrôlée.** Ne pas envoyer le dossier à l’usine comme une autorisation d’assemblage. Les CSV ne sont pas prévalidés contre une base de stock fournisseur.

Les fichiers sont rendus avec gerbv, indépendant du générateurKiCad; voir les captures de revue et les réserves dans reports/VALIDATION.md.

Format Gerber RS-274X sans attributsX2, export natifKiCad; géométrie identique. Lecture/rendu indépendant avecgerbv et inspection des vues de dessus, perçages et deux plans internes. Les attributs de net restent disponibles dans le projet et le netlistXML.
