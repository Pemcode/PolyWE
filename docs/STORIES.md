# Stories — Wiki IWE

Petites tranches livrables. Une story est terminée après ses critères d'acceptation et les vérifications prévues, pas simplement après l'écriture du code. L'utilisateur révise les contenus en parallèle.

| Story | Besoin | État |
| --- | --- | --- |
| S01 | Ajouter des matières et des cours sans changer le code | Livré |
| S02 | Parcourir les matières et ouvrir un cours avec un lien stable | Livré |
| S03 | Retrouver une notion et partager sa section | Livré |
| S04 | Construire et contrôler la publication GitHub Pages avec uv | Livré — site public vérifié |
| S05 | Relecture éditoriale des cours par l'utilisateur | En cours côté utilisateur |
| S06 | Favoris et reprise de lecture sur l'appareil | Plus tard |
| S07 | Consultation hors connexion | Plus tard |
| S08 | Intégrer le cours RDM 04 et ses sections | Intégré et vérifié |
| S09 | Retrouver les supports à partir du planning de formation | Intégré et vérifié |

## S01 — Catalogue extensible

En tant que mainteneur, j'ajoute un cours ou une matière en modifiant les données et en déposant le HTML, sans modifier le générateur.

- Identifiants uniques et stables ; matières déclarées ; prérequis référencés valides.
- Un cours disponible nécessite un fichier HTML existant situé dans le projet.
- Un cours à venir peut ne pas avoir de fichier et ne produit pas de lien. Un brouillon n'est pas publié.
- Les sections et leurs titres proviennent du HTML actuel, pas d'une liste entretenue à la main.
- Rejet d'un chemin sortant du projet, d'un fichier partagé par deux cours ou d'une ressource manquante.
- Une matière fictive dans les tests prouve l'absence de liste codée en dur.

Preuve TDD du 27 septembre 2026 : RED à l'import du module absent, puis GREEN (15 tests). Deux cas ajoutés pour séparer fichier source et URL publiée : RED sur le chemin publié sortant du projet, puis GREEN (17 tests de catalogue). Une erreur de données dans le test d'état à venir (identifiant avec underscore) a été corrigée pour respecter le contrat d'identifiants.

Au premier lot du 27 septembre 2026, les 63 sections des sept cours réels sont extraites du HTML. Le catalogue compte alors neuf entrées, dont deux à venir.

## S02 — Navigation statique

En tant qu'élève, je pars de l'accueil, choisis une matière, ouvre un cours et retrouve les prérequis et les cours voisins.

- Accueil et pages matières lisibles sans JavaScript ; cours à venir clairement identifiés et non cliquables.
- Ajout de navigation dans les copies générées seulement ; scripts et styles pédagogiques préservés.
- Liens et ressources valides à la racine et sous `/depot/` ; accès direct à une section conservé.
- Seuls les contenus déclarés et disponibles sont copiés ; les anciens fichiers générés retirés ne restent pas publiés.
- Génération déterministe ; pas de suppression en dehors du dossier de sortie réservé.

Preuve TDD du 27 septembre 2026 : RED à l'import du générateur absent, puis GREEN (9 tests de génération). Régression OneDrive reproduite avec un dossier généré marqué en lecture seule (RED : PermissionError), corrigée en conservant les répertoires lors du nettoyage (GREEN : 10 tests de génération). Total catalogue + génération : 27 tests verts sous Windows. Le cas spécifique Windows est ignoré sur Linux.

## S03 — Recherche et partage

En tant qu'élève, je retrouve une notion et partage le lien exact du passage dans WhatsApp.

- Recherche par titre de cours, notion et titre de section, insensible à la casse et aux accents ; filtres de matière.
- Un parcours relie plusieurs sections sans dupliquer leurs contenus.
- Partage sur action explicite ; inclut le titre et l'ancre ; copie du lien disponible si le partage natif manque.
- Fil d'Ariane accessible au clavier, présentation lisible sur mobile.
- Tests navigateur d'une recherche, d'un trajet vers un cours et du partage par copie sous un sous-chemin.

Preuve TDD du 27 septembre 2026 : 8 parcours RED avant les interactions JavaScript, plus 2 RED pour le partage d'une section sans ancre préexistante. GREEN après implémentation : 10 parcours Chromium, à la racine et sous `/promo/`, largeur de téléphone. Partage et presse-papiers simulés aux frontières des API : aucun message envoyé sur WhatsApp.

Contrôle complémentaire : accueil inspecté visuellement à 1440 px et 390 px ; sept cours réels chargés à 390 px, sans erreur JavaScript ni débordement horizontal détecté. Ce contrôle ne valide pas les calculs scientifiques ni chaque combinaison des simulateurs.

## S04 — Publication reproductible

En tant que mainteneur, je veux qu'une erreur de catalogue ou de lien soit détectée avant une publication.

- `uv.lock` versionné, installation reproductible ; même commande de test localement et en CI.
- Les pull requests testent et construisent sans publier.
- Sur la branche principale, GitHub Actions teste puis déploie uniquement `_site/` vers Pages.
- Documentation d'ajout d'un cours, de prévisualisation et d'activation de Pages.
- Dépôt destinataire : Pemcode/PolyWE. Les tests sont indépendants de la publication ; `PAGES_ENABLED=true` est nécessaire pour déployer.


État S04 au 27 septembre 2026 : livré sur [le site public](https://pemcode.github.io/PolyWE/). Le propriétaire a rendu le dépôt public ; GitHub Pages a ensuite été activé avec la source GitHub Actions et `PAGES_ENABLED=true`. Installation verrouillée, tests Python (26 réussis et un cas Windows ignoré sous Linux), dix parcours Chromium, build et déploiement ont réussi : [première publication](https://github.com/Pemcode/PolyWE/actions/runs/36343734282). Pas de test qui se contente de reproduire le texte du YAML. Références et procédure dans README.md.

Vérification de l'adresse publiée : 17 fichiers servis en HTTP 200, 243 liens locaux et ancres contrôlés à partir des fichiers téléchargés. Navigation mobile à 390 px sur les sept cours, recherche « prechauffage » jusqu'à la section `#s6`, copie effective de son URL HTTPS dans le presse-papiers, parcours de préchauffage et deux cours RDM à venir sans lien. Aucune erreur JavaScript ni débordement horizontal détecté sur les pages visitées. Accueil également chargé à 1440 px. Le partage natif reste couvert par les tests navigateur avec API simulée ; aucun message WhatsApp n'a été envoyé.

## S08 — Intégrer le cours RDM 04

En tant qu'élève, j'ouvre le cours sur les directions principales et le tricercle de Mohr depuis la matière RDM, le cours précédent ou une recherche.

- L'entrée existante `rdm-04` devient disponible à l'adresse stable `RDM/04-directions-principales-mohr.html`, avec ses prérequis annoncés (cours 1 à 3).
- Le cours 3 mène au cours 4 et le cours 4 permet de revenir au cours 3. Le cours 5 reste à venir.
- Les sections réelles sont présentes au sommaire et dans la recherche ; le lien vers le tricercle cible `#c4`.
- Le parcours « Comprendre les contraintes résiduelles » se prolonge vers cette section sur le tricercle et la triaxialité.
- Le HTML source reste intact. Vérification sur mobile des interactions, du quiz et du partage d'une section ; tests et build verts avant publication.

Preuve TDD du 28 septembre 2026 : RED exécuté avec `uv run pytest tests/test_content.py -q` : le cours 4 n'était pas publié, car encore `a_venir`. GREEN après mise à jour du catalogue et du parcours : le test vérifie les liens depuis la matière, le cours 3, la recherche et le parcours des contraintes résiduelles. Aucun changement du générateur n'a été nécessaire.

Validation locale : 28 tests Python et 10 parcours Chromium réussis ; catalogue et build valides (8 cours disponibles, 73 sections, seul le cours 5 à venir). Le nouveau cours comporte 10 sections. Empreinte SHA-256 du HTML source inchangée. Contrôle du cours réel sous `/PolyWE/` à 390 px et 1440 px : recherche « tricercle », navigation 3 ↔ 4, lien de parcours, copie dans le presse-papiers et partage de `#c4` avec API native simulée. Simulations du tricercle et des valeurs propres manipulées, quiz utilisé et réinitialisé ; aucune erreur JavaScript ni débordement horizontal détecté. Accueil du cours et simulateur inspectés visuellement sur mobile. Ces contrôles portent sur le fonctionnement, pas sur une validation scientifique des calculs.

## S09 — Frise de formation

En tant qu'élève, je situe ma semaine de formation, retrouve ses matières et ouvre les supports disponibles.

- Frise chronologique par semaine, séances par jour, pré-rentrée IWE1 puis formation DU ; dates, horaires et références des plannings sources visibles. Les PDF restent locaux sans autorisation explicite de publication.
- Pré-rentrée détaillée du 23 septembre au 2 octobre 2026. Planning annuel jusqu'au 26 février 2027 ; créneaux MAT5 seuls exclus selon la légende. Pratique et groupes, congés et examens visibles.
- Matières de planning distinctes des fiches du wiki : rapprochements éditoriaux explicites, sans inventer une répartition des fiches par heure. Supports absents ou à venir signalés ; aucun brouillon exposé.
- Filtres période, matière et supports disponibles ; état conservé dans l'URL, ancres de semaine partageables. Accès à la semaine actuelle calculé en heure de Paris ; lien direct vers une autre semaine prioritaire.
- Navigation depuis l'accueil et les cours. Consultation sans JavaScript, utilisation au clavier et sur téléphone, aucun défilement horizontal de page.
- Données extensibles sans modifier le code de navigation ; dates, références, ancres et PDF autorisés manquants bloquent le build avant publication.

Preuve TDD du 28 septembre 2026 : RED des tests Python sur le module `wiki.planning` absent ; huit parcours navigateur RED sur la page inexistante (HTTP 404). GREEN final : 13 tests de planning et huit parcours de frise, à la racine et sous `/promo/`. La suite complète passe : 41 tests Python sous Windows et 18 parcours Chromium (un cas Windows est ignoré en CI Linux).

Validation du contenu réel sous `/PolyWE/` : 23 semaines ; recherche des supports RDM depuis la semaine 40 et ouverture du cours 4 ; cinq dates d'examen contrôlées ; références des deux plannings visibles ; ouverture de semaine au clavier et accès aux cours sans JavaScript. Rendu inspecté à 1440 et 390 px, sans erreur JavaScript ni débordement horizontal détecté. Les données et limites d'interprétation sont consignées dans `docs/PLANNING.md`.


Ajustement S09 : le contrôle automatique a refusé le push des PDF bruts faute d'autorisation spécifique. La frise est livrée avec les PDF locaux, exclus de Git et de l'artefact. Vérification finale : 354 liens valides, les deux adresses PDF renvoient une erreur 404 dans la prévisualisation, les deux fichiers originaux restent présents localement. Test RED exécuté sur la copie implicite d'un PDF, puis GREEN avec publication désactivée par défaut. Le build fonctionne aussi quand ces fichiers locaux sont absents ; les PDF ne sont exigés que si leur publication est explicitement activée.
