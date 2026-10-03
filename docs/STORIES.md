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
| S10 | Ajouter des supports et publier avec une routine guidée | Intégré et vérifié |
| S11 | Intégrer les cours RDM 05 à 07 | Intégré et vérifié |
| S12 | Intégrer le jeu Mohr Forge sans le mettre au centre | Livré — site public vérifié |
| S13 | Intégrer le cours RDM 08 sur les caractéristiques des sections | Livré — site public vérifié |
| S14 | Regrouper les sources dans Cours sans casser les liens publiés | Intégré et vérifié |
| S15 | Intégrer les trois premiers cours de fatigue | Intégré et vérifié |
| S16 | Compléter la série fatigue avec la propagation et la loi de Paris | Intégré et vérifié |

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

## S10 — Routine de mise à jour

En tant que mainteneur, je dépose un fichier dans le projet, je l’enregistre avec un assistant puis je vérifie et publie depuis un menu Windows ou une commande uv.

- Ajout d’un HTML ou d’un document PDF/Office sans édition manuelle du JSON ; choix de la matière, création d’une matière et rattachement facultatif à un sujet du planning.
- Activation d’un cours à venir en conservant son identifiant, son URL, ses prérequis et ses liens de planning. Les sources existantes restent intactes.
- Les documents disposent d’une page partageable avec téléchargement, navigation, recherche et accès depuis la frise. Aucun document existant n’est inscrit automatiquement.
- Validation du site candidat avant enregistrement ; une erreur de fichier, de lien ou de planning laisse les métadonnées inchangées.
- Préparation avec tests et build ; aperçu local ; publication explicite des seuls contenus déclarés après affichage des fichiers concernés. Les brouillons, fichiers ignorés et modifications de code ne sont pas embarqués par la routine.
- Un échec réseau est signalé ; un commit de contenu déjà créé peut être poussé au prochain essai. Le succès du push est distingué du déploiement Pages.
- Guide court pour ajout, correction d’un fichier existant, documents et dépannage ; tests de parcours et vérification navigateur sous un sous-chemin.

Preuve TDD du 28 septembre 2026 : RED exécuté sur `tests/test_maintenance.py` à l’import du module absent. GREEN après implémentation de l’inscription, de la validation en copie et de la publication ciblée. Un second RED a reproduit la perte d’une URL implicite lors du remplacement d’un fichier ; GREEN après conservation de l’adresse précédente.

Validation finale : 61 tests Python sous Windows et 20 parcours Chromium réussis. Les nouveaux tests utilisent de vrais dépôts Git et remotes locaux pour vérifier la sélection des contenus, l’annulation, le refus d’un index prérempli ou de changements hors contenu, l’historique complet et la reprise après un push en échec sans commit supplémentaire. L’assistant est parcouru avec activation d’un support annoncé. Les erreurs d’ajout conservent les sources et métadonnées ; les PDF locaux de Planning et les fichiers ignorés sont refusés.

La commande réelle `preparer` passe sur le projet : tests, build et bilan. Lanceur Windows testé par son chemin complet avec ouverture et fermeture du menu. Nouveau document consulté depuis la frise, téléchargé puis partagé par copie à la racine et sous `/promo/`. Rendu inspecté à 390 et 1440 px, sans débordement ni erreur JavaScript. Les cours existants et les deux JSON éditoriaux restent inchangés ; aucun document réel supplémentaire n’a été publié pendant les essais.

## S11 — Étendre la série RDM jusqu’aux diagrammes de sollicitations

En tant qu’élève, je poursuis les cours après Mohr avec Hooke et les critères de résistance, puis le torseur de cohésion et les diagrammes de sollicitations.

- Activer l’entrée `rdm-05` existante et ajouter `rdm-06` et `rdm-07`, avec titres, numéros, prérequis et mots-clés cohérents avec les sources.
- Accès depuis la matière, navigation 4 ↔ 5 ↔ 6 ↔ 7, recherche des sections réelles et partage de leurs ancres.
- Tous les nouveaux cours sont disponibles depuis les séances « Notions fondamentales de RDM ». Les sections sur la statique/les liaisons et les cas types complètent le sujet « Théorie de base des systèmes de structure » ; la section fatigue rejoint le sujet annuel « Fatigue ». Aucun horaire ni examen n’est modifié.
- Sources HTML conservées octet pour octet, scripts et quiz fonctionnels dans les copies publiées. Aucun autre document local ajouté.
- Test de parcours en RED avant l’inscription, puis suite Python, build et contrôles navigateur sous `/PolyWE/` à 390 et 1440 px.

Preuve TDD du 29 septembre 2026 : RED de `test_rdm_05_to_07_continue_series_and_are_reachable_from_planning` sur l’absence de la page du cours 5. GREEN après inscription des trois sources avec la routine, complétion des métadonnées et rattachements aux sujets du planning. Le test protège les liens depuis la matière, la succession 4 ↔ 5 ↔ 6 ↔ 7, la recherche, les ancres du planning et la conservation des sources dans la copie de contrôle.

Validation : 62 tests Python sous Windows et 20 parcours Chromium réussis ; build et contrôle de 463 liens locaux/ancres. Le catalogue contient 11 cours disponibles et 104 sections, dont 31 nouvelles sections. Contrôle des trois cours réels sous `/PolyWE/` à 390 et 1440 px : recherche jusqu’à une section, copie du lien, partage natif simulé, accès depuis la semaine 40, navigation entre cours et quiz/réinitialisation. Un cas du calculateur 3D du cours 5, la torsion du cours 6 et une console chargée du diagrammeur du cours 7 ont été manipulés. Aucune erreur JavaScript ni débordement horizontal détecté ; accueil des trois cours inspecté sur mobile. Ces essais vérifient le fonctionnement des interfaces, pas le fond scientifique des calculs.

Les empreintes SHA-256 des trois HTML sont inchangées. Séances, dates, phases et sources PDF du planning inchangées ; seuls les liens vers les supports ont évolué. La documentation distingue le complément introductif sur la fatigue du futur enseignement spécialisé.

## S12 — Un jeu d’entraînement accessible, sans prendre le centre du wiki

En tant qu’élève, depuis la matière RDM, un cours sur les contraintes et déformations ou la recherche, j’ouvre le jeu Mohr Forge publié avec le wiki, puis je reviens au wiki.

- Le jeu devient une source du dépôt (`applications/mohr-forge/`). Le catalogue le déclare comme application de la matière RDM, sans nom de matière codé dans le générateur. L’ancien dépôt imbriqué est archivé localement, hors Git.
- Seuls les fichiers déclarés sont publiés, à l’adresse stable `RDM/mohr-forge/index.html`. Tests, documentation et scripts du jeu ne le sont pas. Une application en brouillon n’est pas publiée ; à venir, elle n’a pas de lien.
- Place discrète : l’accueil reste centré sur les matières, avec une simple mention dans la carte RDM. La page RDM présente une section « S’entraîner », les cours liés proposent le jeu en pied de page et la recherche le trouve.
- La copie publiée reçoit la barre du wiki (fil d’Ariane, partage) ; la source reste intacte. Les routes internes du jeu (`#histoire`, `#laboratoire`…) ne bloquent pas le contrôle des liens.
- Liens valides à la racine et sous un sous-chemin. La routine d’ajout de supports valide toujours un site candidat complet ; `publier` n’embarque pas le code du jeu.
- La CI exécute les tests du moteur du jeu (Node, sans npm) et ses parcours Chromium avant toute publication.

Preuve TDD du 30 septembre 2026 : RED exécuté avec `uv run pytest -q` (19 échecs). Les applications n’étaient pas lues par le catalogue (`KeyError: 'url'`), rien n’était publié et la liste des entrées du build (`build_inputs`) n’existait pas. Les trois parcours de `tests/browser/test_applications.py` échouaient faute de section « S’entraîner ». GREEN après implémentation : validation des applications dans le catalogue, publication fichier par fichier avec barre du wiki, reconnaissance des routes internes par la balise `wiki-application`, section de matière, lien en pied des cours liés, entrée de recherche et build candidat complet. Un test garde aussi le refus de `publier` pour le code d’une application.

Migration : 29 fichiers du jeu copiés à l’identique (empreintes SHA-256 vérifiées) dans `applications/mohr-forge/`. La CI autonome, `pyproject.toml`, `uv.lock` et le build `dist/` du jeu sont remplacés par ceux du wiki. L’ancien dépôt imbriqué, avec son historique, est archivé dans `.sauvegardes/` ; son exclusion locale Git est retirée.

Validation : 81 tests Python et 23 parcours Chromium du wiki, dont le vrai jeu joué sous `/PolyWE/` sur téléphone (matière → jeu → histoire → laboratoire 3D → retour à la matière). S’y ajoutent 25 tests Node et 34 parcours Chromium du jeu depuis son nouvel emplacement. Une simulation de polices larges, comme sur les runners Linux de la CI, a révélé un débordement de la navigation du jeu à 320 px. Un test de régression l’a reproduit (RED), puis l’a vu corrigé en autorisant le retour à la ligne (GREEN). Catalogue valide : 11 cours, 104 sections, 1 application ; build et contrôle des liens réussis. Le contrôle visuel du jeu publié couvre 84 vues à la racine et sous `/PolyWE/`, aux quatre largeurs, sans débordement ni erreur JS/HTTP. Accueil, page RDM, pied du cours 4, jeu avec la barre du wiki et recherche inspectés à 1440 et 390 px.

Preuve de publication du 2 octobre 2026 : [run n° 9, 36975927559](https://github.com/Pemcode/PolyWE/actions/runs/36975927559), commit `31db69c`, tests Linux (dont Node 24 via `actions/setup-node@v7`), build et déploiement réussis. HTTP 200 vérifié pour [le jeu](https://pemcode.github.io/PolyWE/RDM/mohr-forge/index.html), [scene3d.js](https://pemcode.github.io/PolyWE/RDM/mohr-forge/js/scene3d.js) et [la matière RDM](https://pemcode.github.io/PolyWE/matieres/rdm.html), avec « S’entraîner » et le lien du jeu ; HTTP 404 confirmé pour [le répertoire de tests](https://pemcode.github.io/PolyWE/RDM/mohr-forge/tests/).

## S13 — Intégrer le cours RDM 08

En tant qu’élève, j’ouvre le cours sur les caractéristiques des sections depuis la matière RDM, le cours 7 ou la recherche, puis j’utilise ses simulations et son quiz.

- Le cours `rdm-08` est disponible à l’adresse stable `RDM/08-caracteristiques-sections.html`, avec les prérequis indiqués dans sa source : cours 6 et 7, et cours 4 pour les axes principaux.
- La matière RDM et la navigation 7 ↔ 8 donnent accès au cours ; ses sections réelles figurent au sommaire et dans la recherche, notamment Huygens (`#c3`).
- La source HTML, ses ancres et ses scripts restent intacts. Les simulations, le quiz et le partage sont vérifiés sous `/PolyWE/` sur téléphone et ordinateur.
- Tests et build verts avant publication ; accès public au cours et à ses liens contrôlé après déploiement.

Preuve TDD du 2 octobre 2026 : RED exécuté avec `uv run pytest tests/test_content.py -k rdm_08 -q`, sur l’absence du cours publié. GREEN après enregistrement par `wiki ajouter` et ajustement des métadonnées : accès depuis la matière, navigation 7 ↔ 8, prérequis, recherche de Huygens, conservation des ancres et des scripts. Aucun changement du générateur.

Validation locale : 82 tests Python et 23 parcours Chromium du wiki réussis ; catalogue valide (12 cours, 114 sections, 1 application), build et liens contrôlés. Contrôle du cours réel à la racine et sous `/PolyWE/`, à 390 et 1440 px : cinq simulations manipulées, quiz répondu puis remis à zéro, recherche « Huygens », navigation 7 ↔ 8 et copie effective du lien de `#c3`. Aucune erreur JavaScript ou HTTP locale ni débordement horizontal de page détecté. Captures de l’accueil du cours, du calculateur de sections composées et du quiz inspectées. Empreinte SHA-256 de la source inchangée : `d9ce014796006dd3acf61ad99a44ff74998abeffe76fc589e9e5040a3d2352f4`. Ces vérifications portent sur le fonctionnement, pas sur une validation scientifique.

Preuve de publication du 2 octobre 2026 : [run n° 11, 36976863962](https://github.com/Pemcode/PolyWE/actions/runs/36976863962), commit `e2394f9`, tests Linux, build et déploiement réussis. HTTP 200 pour [le cours 8](https://pemcode.github.io/PolyWE/RDM/08-caracteristiques-sections.html), [la matière RDM](https://pemcode.github.io/PolyWE/matieres/rdm.html), [le cours 7](https://pemcode.github.io/PolyWE/RDM/07-diagrammes-sollicitations.html) et [l’index de recherche](https://pemcode.github.io/PolyWE/assets/recherche.json). Liens 7 ↔ 8 et entrée de recherche de Huygens (`#c3`) contrôlés ; ancres et scripts du cours publié identiques à ceux de la source. Mohr Forge et `scene3d.js` restent accessibles en HTTP 200, son répertoire `tests/` renvoie toujours 404.

## S14 — Sources regroupées dans Cours

En tant que mainteneur, je range les supports dans `Cours/<matière>/` tout en conservant les adresses du site déjà partagées.

- Le catalogue référence les fichiers déplacés dans `Cours/Metallurgie/` et `Cours/RDM/`, sans réécrire les sources et sans changer leurs URL ni identifiants.
- Les anciens liens de cours, leurs ancres, la recherche, les parcours, le planning et l’application Mohr Forge restent accessibles après reconstruction.
- La routine et sa documentation utilisent les nouveaux chemins locaux ; l’ajout d’un support reste validé par un build candidat complet.
- Les tests de contenu lisent l’emplacement source déclaré, sans imposer son ancien dossier.
- Contrôles locaux et déploiement GitHub Pages réussis avant vérification des adresses publiques.

Preuve TDD du 2 octobre 2026 : RED de `test_relocated_sources_preserve_existing_bookmarks_and_scripts` sur le fichier introuvable à l’ancien emplacement. GREEN après changement des champs `fichier` et adaptation du test RDM 08 pour lire le chemin déclaré dans le catalogue. Les 12 identifiants et URL de cours sont conservés ; aucun changement du générateur ou de la routine n’a été nécessaire.

Validation : 83 tests Python et 23 parcours Chromium réussis ; catalogue valide (12 cours, 114 sections, 1 application), build et 522 liens/ancres contrôlés. Les 38 fichiers de l’artefact sont équivalents à ceux construits depuis le commit précédent, hors normalisation Git des fins de ligne de deux fichiers de Mohr Forge. Empreintes SHA-256 des 12 sources déplacées inchangées. L’application et ses fichiers restent à leurs emplacements ; aucun calendrier ou PDF source n’est modifié.

Lors de la migration, le dossier local `Cours/Fatigue/` est vide. Aucun nouveau support de fatigue n’est donc inventorié ni publié ; les fichiers déposés ensuite sont intégrés dans S15.

## S15 — Les bases de la fatigue des métaux

En tant qu’élève, je retrouve les nouveaux supports de fatigue depuis une matière dédiée, le planning ou une recherche et je progresse des cycles à l’amorçage.

- Trois supports disponibles : cycles de chargement, courbe de Wöhler et amorçage des fissures. Numéros, titres, mots-clés et prérequis tirés des fichiers déposés.
- Une matière « Fatigue des métaux » apparaît automatiquement dans la navigation ; progression 1 ↔ 2 ↔ 3, sommaires et partage des sections.
- Le sujet 3.8 « Fatigue » propose les trois cours, en conservant l’introduction RDM existante. Les sujets de rupture reçoivent seulement des sections complémentaires pertinentes ; leurs dates et horaires ne changent pas.
- Sources sous `Cours/Fatigue/`, URL stables sous `Fatigue/`, scripts, thèmes et quiz préservés. Aucun cours absent n’est annoncé comme disponible.
- Test du parcours en RED avant inscription, puis tests et build verts, vérification des interactions et du partage sur mobile et ordinateur avant publication.

Preuve TDD du 2 octobre 2026 : RED exécuté avec `uv run pytest tests/test_content.py -q -k fatigue`, sur l’absence de la page matière. GREEN après enregistrement des trois HTML par `wiki ajouter` et ajustement des métadonnées : matière, progression, planning, prérequis, index des sections, conservation des ancres et des scripts. Aucun changement du générateur.

Validation locale : 84 tests Python et 23 parcours Chromium réussis ; catalogue et build valides (15 cours, 151 sections, 3 matières et 1 application). Contrôle des trois cours réels sous `/PolyWE/`, à 390 et 1440 px : recherche ciblée, copie effective des liens avec ancres, partage natif simulé, accès depuis la semaine 49 du planning, progression 1 ↔ 2 ↔ 3, un simulateur par cours, quiz et réinitialisation, thème clair/sombre et persistance après rechargement. Aucune erreur JavaScript ou HTTP locale ni débordement horizontal détecté. Captures de la matière, des cours et d’un simulateur inspectées. Les trois empreintes SHA-256 des sources restent inchangées ; les scripts et ancres sont conservés dans les copies publiées. Ces contrôles vérifient le fonctionnement, sans validation scientifique des calculs.

## S16 — Propagation et loi de Paris

En tant qu’élève, je poursuis le cours sur l’amorçage avec la propagation des fissures et retrouve la loi de Paris depuis la matière, la recherche et le planning.

- Cours `fatigue-04` disponible à `Fatigue/04-propagation-loi-paris.html`, avec les cours 1 à 3 en prérequis et navigation 3 ↔ 4.
- Douze sections réelles indexées ; la recherche de la loi de Paris donne accès à `#c4`.
- Le sujet 3.8 propose le cours complet ; les sujets 2.7 et 3.11 reçoivent respectivement les compléments sur la cassure (`#c2`) et le diagramme de propagation (`#c3`), sans changer les dates ni horaires.
- Source conservée à l’identique, scripts et ancres préservés ; contrôle des simulateurs, du quiz, du thème et du partage sur mobile et ordinateur.
- Test du parcours en RED puis GREEN, build et tests utiles réussis avant publication ; vérification de l’accès public après déploiement.

Preuve TDD du 3 octobre 2026 : extension du test de parcours fatigue à la quatrième étape ; RED exécuté avec `uv run pytest tests/test_content.py -q -k fatigue`, sur l’absence du lien 3 → 4. GREEN après inscription par `wiki ajouter` et ajustement des métadonnées et du planning. Le test couvre les quatre cours, les prérequis du cours 4, les sections de recherche, les compléments de planning et la conservation des scripts et ancres.

Validation locale : 84 tests Python et 23 parcours Chromium réussis ; catalogue et build valides (16 cours, 163 sections, 1 application). Cours réel contrôlé sous `/PolyWE/`, à 390 et 1440 px : navigation 3 ↔ 4, recherche « loi de Paris », copie du lien `#c4`, partage natif simulé, accès depuis la semaine 49, trois simulateurs manipulés (Paris, durée de propagation, classes FAT), quiz et réinitialisation, thème clair/sombre et persistance. Captures du cours et du graphique inspectées ; aucune erreur JavaScript ou HTTP ni débordement horizontal détecté. Empreinte SHA-256 de la source inchangée ; aucune correction du fond scientifique.
