# Lecture des plannings et liens vers les supports

## Sources et périmètre

- `Planning/planning IWE1_2026_version 3.pdf`, une page : 8 journées, du 23 septembre au 2 octobre 2026. Les 22 séances regroupent les créneaux successifs d'un même sujet dans une journée.
- `Planning/Edt_MAT5 soudage_26-27_31-08-26.pdf`, une page : du 5 octobre 2026 au 26 février 2027. Document prévisionnel.

Les PDF sont conservés localement et exclus du dépôt et du site publics ; seules leur transcription et leurs références sont publiées.

Les tableaux ont été extraits par cellules puis vérifiés sur les rendus PDF, notamment les horaires de la pré-rentrée et la légende des publics. La transcription totalise 191 séances ou périodes, réparties sur 23 semaines ISO. Les périodes répétées de pratique, de congés ou d'entreprise sont regroupées à l'affichage ; le nombre de cartes est donc inférieur à celui des entrées.

La légende annuelle distingue le cyan « MAT5 Soudage et DU IS », l'orange « MAT5 et DU IS », le jaune « MAT5 » et le bleu « MAT5 Soudage ». Les deux derniers sont exclus de cette vue DU : HES/langues, journée Compétences, conduite de réunion, CAO Thermo et CFAO. Les cours CND orange sont conservés. Les cellules rouges et violettes n'ont pas d'explication dans la légende : leur texte est conservé, sans inventer de sens supplémentaire à leur couleur.

Les créneaux vides ne deviennent pas des heures libres. Les indications de groupe (GR1/2/3, A/B), de contrat professionnel et de stage sont conservées sans attribuer un groupe à l'utilisateur. Les périodes entreprise et vacances peuvent se superposer dans le document selon le statut de l'élève.

## Matières de pré-rentrée

Les codes ci-dessous viennent du planning ; les liens avec les fiches du wiki sont des rapprochements éditoriaux par thème, pas un découpage officiel par créneau.

| Code | Sujet du planning | Supports associés actuellement |
| --- | --- | --- |
| 2.2 | Diagrammes de phases et alliages | Diagramme plomb–étain (`met-base`) |
| 2.1 | Structures et propriétés des métaux | Structure du fer, section `met-01#s1` |
| 2.3 | Alliages fer–carbone | Cours `met-01` |
| 2.8 | Traitements thermiques | Cinétique TTT/TRC (`met-02`) et traitements thermiques/soudage (`met-03`) |
| 3.1 | Théorie de base des systèmes de structure | Statique et liaisons (`rdm-06#c2`, `rdm-06#c3`), cas types de poutres (`rdm-07#c5`) |
| 3.2 | Notions fondamentales de RDM | Série `rdm-01` à `rdm-07`, disponible |
| 2.14 | Introduction à la corrosion | Pas de support associé pour le moment |
| 1.1 | Introduction à la technologie du soudage | Pas de support associé pour le moment |
| 2.7 | Ruptures et différents types de rupture | Compléments : le film d’une rupture par fatigue (`fatigue-01#c6`) et la lecture d’une cassure (`fatigue-04#c2`) |
| 3.11 | Introduction à la mécanique de la rupture | Compléments : fissures dormantes (`fatigue-03#c5`) et diagramme de propagation (`fatigue-04#c3`) |
| 2.4 | Élaboration des aciers | Pas de support associé pour le moment |
| 2.23 | Essais des matériaux | Pas de support associé pour le moment |

Le lundi 28 septembre : RDM de 8 h à 11 h 25, puis corrosion de 11 h 30 à 12 h 30 et de 14 h à 15 h. Le planning ne permet pas d'attribuer un numéro précis de fiche RDM à une heure : la série est proposée sur chacune des séances de RDM.

## Suite de formation

Quatre familles organisent les enseignements : procédés (1.x), métallurgie et matériaux (2.x), RDM et conception (3.x), fabrication/contrôle/qualité (4.x). Les examens et périodes pratiques ont leurs propres filtres.

Les liens complémentaires déjà possibles sont ciblés : structure du joint → `met-03#s4`, fissuration → `met-03#s6`, conception des joints → `rdm-02#c6`, contraintes/déformations → `rdm-03#c5` et `met-03#s4`. Le sujet annuel « Fatigue » (3.8) propose les quatre cours de la première série de la matière « Fatigue des métaux » : cycles de chargement (`fatigue-01`), courbe de Wöhler (`fatigue-02`), amorçage (`fatigue-03`) et propagation / loi de Paris (`fatigue-04`). L’introduction de `rdm-05#c6` reste proposée en complément. Cette série disponible ne prétend pas couvrir tout le module. La matière du wiki se retrouve dans la famille « RDM et conception » du planning, sans modifier le calendrier. Un même code du PDF peut recouvrir plusieurs libellés ; les sujets ont donc des identifiants propres, plutôt qu'une correspondance automatique par numéro seul.

| Examen indiqué | Date | Horaire |
| --- | --- | --- |
| Procédés | 17 décembre 2026 | 10 h 15–12 h |
| Matériaux | 12 janvier 2027 | 10 h 15–12 h |
| CND | 22 janvier 2027 | 10 h 15–12 h |
| Conception | 27 janvier 2027 | 8 h–9 h 45 |
| Fabrication | 11 février 2027 | 8 h–9 h 45 |

La date d'un examen ou d'une séance reste celle du PDF prévisionnel, à actualiser si la formation diffuse une nouvelle version.

## Entretenir la frise

`planning-formation.json` est la transcription versionnée, consommée par le générateur sans dépendance PDF à l'exécution :

- `sources` référence les PDF locaux. `publier` vaut `false` par défaut : le fichier n'est ni copié ni lié et sa présence n'est pas exigée en CI. Ne le passer à `true` qu'après autorisation explicite du propriétaire pour le document concerné ; le fichier doit alors être disponible dans le dépôt pour le build.
- `phases` définit les étapes, dates et source ; `phase_reference` désigne la pré-rentrée comme point de départ avant la formation.
- `themes` définit les filtres ; `sujets` porte les intitulés, codes et `supports`.
- Un support contient `cours` (identifiant du catalogue) et éventuellement `ancre`. Un cours à venir n'a pas de lien ; un brouillon disparaît des supports. Passer un cours annoncé en disponible active ses liens déjà déclarés.
- `seances` référence un sujet et une phase avec une date ISO ; `horaire`, `intervenant` et `note` sont facultatifs. Les plages horaires affichées peuvent inclure les pauses du planning.

Pour un nouveau cours, ajouter son identifiant aux supports du bon sujet une seule fois : toutes les séances de ce sujet en bénéficient. Pour une nouvelle version PDF, relire les cellules concernées et modifier la transcription, puis lancer `uv run python -m wiki check`, les tests et le build. Déposer un PDF seul ne modifie pas le calendrier.

`planning.html#semaine-2026-40` ouvre une semaine précise. Les paramètres `phase`, `matiere` et `supports=1` conservent une vue filtrée. La semaine actuelle est déterminée dans le navigateur en heure de Paris, sans figer la date lors du build. Les cours utilisent des liens relatifs compatibles avec `/PolyWE/`.