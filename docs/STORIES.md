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
| S17 | Intégrer la série Mécanique de la rupture | Intégré et vérifié |
| S18 | Intégrer le fluage et le brasage, republier les corrections de rupture | Intégré et vérifié |
| S19 | Compléter la série brasage avec les cours 3 et 4 | Intégré et vérifié |
| S21 | Naviguer avec un panneau latéral repliable et lire les cours en paysage | Intégré et vérifié |
| S25 | Poser une question à un assistant IA connecté avec son propre compte OpenRouter | Publié — test réel OpenRouter à faire |
| S26 | Suivre un guide pas à pas, du compte OpenRouter à la première question | Intégré et vérifié sur branche |

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

## S17 — De la cassure au défaut acceptable

En tant qu’élève, je retrouve les quatre cours de rupture dans une matière dédiée et depuis les sujets correspondants du planning, puis je progresse de la reconnaissance des cassures à l’évaluation des défauts.

- Quatre cours disponibles sous des URL stables `Rupture/`, avec numéros, titres, prérequis et mots-clés tirés des sources déposées dans `Cours/Rupture/`.
- Navigation 1 ↔ 2 ↔ 3 ↔ 4, accès depuis l’accueil et la matière, sommaires et recherche des sections (clivage, Charpy, facteur K, diagramme FAD).
- Cours 1 et 2 liés au sujet 2.7 ; cours 3 et 4 liés au sujet 3.11 ; compléments ciblés pour les essais des matériaux et des soudures. Les supports de fatigue restent présents, les dates et horaires sont conservés.
- Sources, scripts et ancres préservés ; seuls les supports déclarés sont publiés. Aucun polycopié local n’est embarqué.
- Test de parcours en RED puis GREEN, tests et build valides ; interactions, partage, thèmes et affichage contrôlés aux largeurs 360, 390, 768 et 1280 px ; publication vérifiée sur GitHub Pages.

Preuve TDD du 5 octobre 2026 : RED de `uv run pytest tests/test_content.py -q -k rupture_series` sur la page matière absente. GREEN après inscription des quatre cours par `wiki ajouter` et ajustement du catalogue et du planning. Le test vérifie la progression, les prérequis, les recherches de sections, les liens des sujets 2.7, 3.11 et 2.23, la conservation des scripts et ancres et l’exclusion du dossier source de l’artefact. Aucun changement du générateur.

Validation locale : 85 tests Python et 23 parcours Chromium réussis ; catalogue et build valides (20 cours, 211 sections, 4 matières et 1 application). Les quatre cours réels sont contrôlés sous `/PolyWE/` : recherche, copie effective du lien de section, partage natif simulé, frise de la semaine 40, navigation 1 ↔ 2 ↔ 3 ↔ 4, 24 manipulations et leurs animations, 48 questions de quiz avec corrections et remise à zéro, mémorisation des cases et du thème. Modes clair et sombre testés aux largeurs 360, 390, 768 et 1280 px, sans débordement horizontal de page ni erreur JavaScript ou HTTP. Empreintes SHA-256 des quatre sources inchangées. Les contrôles portent sur l’intégration et le fonctionnement, pas sur une nouvelle validation scientifique des supports fournis.

Revue visuelle : les 24 schémas, les en-têtes sombres sur téléphone et un en-tête sur ordinateur ont été inspectés. Limite des sources conservées : certaines légendes de graphiques sont tronquées à 390 px, notamment `rupture-02#c4`, `rupture-03#c4` et `#c5`, `rupture-04#c2` et `#c4` avec certains réglages. Ce défaut interne aux SVG est distinct du débordement horizontal de page ; sa correction nécessite une évolution de présentation des supports, sans modifier leurs formules.

## S18 — Fluage et brasage

En tant qu’élève, je retrouve les premiers cours de fluage et de brasage depuis leurs matières, la recherche et les séances correspondantes du planning.

- `fluage-01` introduit le sujet 2.12 « Acier résistant au fluage » par la courbe et les mécanismes ; il ne prétend pas couvrir à lui seul le choix des aciers.
- `brasage-01` et `brasage-02` couvrent les bases puis les oxydes, flux, atmosphères et apports du sujet 1.16 « Brasage ». Progression 1 ↔ 2, sans inventer les cours de suite absents.
- Matières dédiées, prérequis et mots-clés issus des HTML, chemins publiés stables sous `Fluage/` et `Brasage/` ; le rangement source imbriqué du brasage reste inchangé.
- Liens de planning explicites sur les identifiants complets, dates et horaires conservés. Aucun fichier source de Planning ou Polycopies n’est publié.
- Les quatre sources de rupture déjà corrigées sont republiées en conservant leurs URL, ancres et clés de stockage. L’intégration ne réécrit aucune source.
- Test de parcours en RED puis GREEN, catalogue et build valides, contrôles navigateur des cours réels et des légendes SVG, puis vérification du déploiement public.

Aucune fiche d’intégration séparée n’a été trouvée parmi les fichiers livrés ; les métadonnées sont établies à partir des titres, prérequis et sections des HTML et des identifiants renvoyés par `wiki sujets fluage` et `wiki sujets brasage`.

Preuve TDD du 6 octobre 2026 : RED de `uv run pytest tests/test_content.py -q -k fluage_and_brasage` sur l’absence des trois pages publiées. GREEN après inscription par `wiki ajouter` et renseignement des métadonnées : matières, planning, recherche, navigation du brasage, prérequis et conservation des ancres et scripts. Aucun changement du générateur.

Validation locale : 86 tests Python et 23 parcours Chromium réussis ; catalogue et build valides (23 cours, 247 sections, 6 matières, 1 application). Contrôle des trois nouveaux cours et des quatre cours de rupture corrigés sous `/PolyWE/` : 43 manipulations, animations, 84 questions de quiz et remise à zéro, thèmes, mémorisation des cases, recherche, copie effective des liens de section, partage natif simulé, prérequis, navigation et planning (semaines 40 à 42). Le contrôle de l’animation de vieillissement du brasage 2 a été ajusté pour observer sa lecture chiffrée : cette animation ne modifie pas le graphique de température homologue. Pas d’erreur JavaScript ou HTTP ni de débordement horizontal de page constaté. Les sept empreintes de sources sont inchangées depuis la réception ; les URL, ancres et clés de stockage des quatre cours de rupture sont conservées.

Contrôle SVG aux largeurs 360, 390, 768 et 1280 px, en clair et sombre : comparaison des boîtes de texte au viewBox après chargement des polices, avec tolérance de 2 unités. Les valeurs extrêmes prises individuellement donnent 1 320 états contrôlés sans débordement, puis 176 états supplémentaires dans le mode « zone plastique » du cours Rupture 3 également sans débordement. Le contrôle complémentaire de 168 états avec les curseurs simultanément au minimum ou au maximum retrouve deux défauts résiduels dans Rupture 3 (12 occurrences selon largeur et thème), consignés ci-dessous. Aucun texte hors cadre relevé dans les trois nouveaux cours pour ces configurations. Captures des nouveaux schémas, du mode sombre mobile, de l’affichage ordinateur et des légendes corrigées inspectées. Cette intégration n’effectue pas une nouvelle validation scientifique des cours livrés.

Défauts résiduels à corriger dans la source `rupture-03`, sans changer ses ancres :
- `#c4`, mode « Zone plastique » (`m4v`, option `pz`), curseurs `m4K` et `m4R` au maximum : la légende « rY = 1,6 mm » dépasse à droite, aux quatre largeurs.
- `#c5`, curseurs au maximum simultanément : la légende « ténacité typique des aciers : 50 à 150 MPa·√m » dépasse à gauche à 360 et 390 px.

Les corrections livrées des autres légendes de rupture sont conservées et republiées. La modification locale de `AGENTS.md` reste hors de ce commit de contenus et d’intégration.

## S19 — Exécuter, concevoir et contrôler le brasage

En tant qu’élève, je poursuis la série de brasage par les procédés et le mode opératoire, puis la conception, les familles de métaux et le contrôle des joints.

- `brasage-03` et `brasage-04` disponibles sous `Brasage/03-procedes-mode-operatoire.html` et `Brasage/04-conception-metaux-controle.html`, sans changer les URL des cours 1 et 2.
- La matière présente les quatre cours dans l’ordre ; progression 1 ↔ 2 ↔ 3 ↔ 4, prérequis, recherche des sections et partage.
- Les deux cours sont associés à `1-16-brasage`, sans modifier les dates et horaires ; documentation du planning actualisée.
- Sources livrées conservées à l’identique ; les limites observées sont consignées pour correction par l’auteur.
- Test de parcours RED puis GREEN, tests et build verts, interactions et SVG contrôlés aux quatre largeurs, puis publication GitHub Pages vérifiée.

Aucune fiche d’intégration séparée trouvée pour ces deux cours ; leurs métadonnées reprennent les en-têtes et sections des sources. Le sujet est confirmé par `wiki sujets brasage`.

Preuve TDD du 6 octobre 2026 : extension du test `fluage_and_brasage` aux cours 3 et 4 ; RED exécuté avec `uv run pytest tests/test_content.py -q -k fluage_and_brasage` sur l’absence des deux pages publiées. GREEN après inscription par `wiki ajouter` et renseignement des métadonnées. Le test contrôle la progression des quatre cours, les prérequis, la recherche, les liens de planning et la conservation des scripts et ancres. Aucun changement du générateur.

Contrôle des deux cours réels sous `/PolyWE/` : 12 manipulations et leurs animations, 24 questions de quiz et remise à zéro, mémorisation des cases et des thèmes, recherche, copie effective des liens de section, partage natif simulé, accès depuis la semaine 41 et navigation 1 ↔ 2 ↔ 3 ↔ 4. Modes clair et sombre aux largeurs 360, 390, 768 et 1280 px, sans débordement horizontal de page ni erreur JavaScript ou HTTP. Les captures des 12 schémas, des en-têtes sur téléphone et ordinateur et de la matière ont été inspectées.

Contrôle des légendes SVG : 1 336 états vérifiés après chargement des polices (réglages initiaux, extrêmes individuels et simultanés, boutons de préréglage), aux quatre largeurs et dans les deux thèmes. Aucun texte hors viewBox détecté avec une tolérance de 2 unités. Empreintes SHA-256 des deux sources inchangées ; cette intégration vérifie le fonctionnement sans nouvelle validation scientifique. La modification locale de `AGENTS.md` reste hors du commit.

Validation locale : 86 tests Python et 23 parcours Chromium réussis ; catalogue et build valides (25 cours, 271 sections, 6 matières, 1 application).


## S20 — Réviser le soudage à l’électrode enrobée

En tant qu’élève, je retrouve les quatre premiers cours du sujet IWE 1.9 depuis l’accueil, la matière, le planning et la recherche.

- Nouvelle matière « Soudage à l’électrode enrobée », cours `electrode-enrobee-01` à `electrode-enrobee-04` disponibles et ordonnés : poste de soudage, réglages de l’arc, électrodes, préparation et exécution.
- URL stables sous `ElectrodeEnrobee/`, navigation entre cours, prérequis issus des en-têtes, sections indexées et partageables.
- Rattachement à `1-9-soudage-a-lelectrode-enrobee`, sans modification des séances ; documentation du planning actualisée.
- Sources conservées à l’identique, scripts et ancres préservés. Le cinquième cours annoncé n’est pas disponible.
- Test de parcours RED puis GREEN, tests et build valides, vérification des interactions et de l’affichage, commit et push sur `main`, puis contrôle du déploiement Pages.

Aucune fiche d’intégration séparée présente : les métadonnées sont tirées des en-têtes et sections des quatre HTML. Le sujet est confirmé par `wiki sujets "1.9"`. L’intégration ne constitue pas une nouvelle validation scientifique.


Preuve TDD du 7 octobre 2026 : RED exécuté avec `uv run pytest tests/test_content.py -q -k electrode_enrobee` sur l’absence des quatre pages publiées. GREEN après inscription par `wiki ajouter`, renseignement des URL et des prérequis. Le parcours contrôle l’accès depuis l’accueil, la matière, le planning et la recherche des six chapitres de chaque cours, la progression, les prérequis, les scripts et ancres conservés et l’absence de cours 5 disponible. Aucun changement du générateur.

Validation locale : 87 tests Python et 23 parcours Chromium réussis ; catalogue et build valides (29 cours, 319 sections, 7 matières, 1 application). Les séances et les autorisations des PDF restent inchangées.

Contrôle des quatre cours réels sous `/PolyWE/` : 24 manipulations et leurs animations, 48 questions de quiz et remise à zéro, cases mémorisées après rechargement, persistance du thème, partage de section via l’API native simulée, recherche sans accents vers le chapitre de soufflage magnétique, liens de la matière et du planning. Vérification des modes clair et sombre aux largeurs 360, 390, 768 et 1280 px. Les 2 880 états contrôlés (initiaux, extrêmes individuels et simultanés des curseurs, boutons de préréglage) ne présentent aucun débordement horizontal de page ni aucun texte SVG hors viewBox avec une tolérance de 2 unités. Aucune erreur JavaScript ou HTTP locale. Captures des 24 manipulations et des quatre en-têtes mobiles sombres inspectées. Empreintes SHA-256 des quatre sources inchangées depuis la réception.

La mise à jour existante de `AGENTS.md` est versionnée dans un commit de documentation distinct, conformément à la demande de synchroniser toutes les modifications sur `main`. Le cinquième cours annoncé reste à livrer ; aucune nouvelle validation scientifique n’est revendiquée.

## S21 — Panneau latéral et lecture paysage

En tant qu’élève sur ordinateur portable, je navigue depuis un panneau latéral plutôt que depuis un bandeau en haut de page, et je vois une manipulation entière sur un seul écran ; sur téléphone, la navigation reste à portée de pouce sans gêner la lecture.

- Toutes les pages publiées (accueil, matières, parcours, planning, cours, documents, applications) remplacent le bandeau supérieur par un panneau latéral gauche : marque, recherche, accueil, planning, matières dépliables avec leurs cours disponibles, parcours. Les brouillons, les cours à venir et les applications n’y figurent pas ; les applications restent hors de l’accueil.
- Sur un cours : matière, titre, sommaire du cours avec la section en cours de lecture surlignée, cours précédent et suivant, partage et copie du lien. Les boutons « Partager cette section » restent dans le contenu.
- Sur un écran d’au moins 1 000 px, le panneau est ouvert par défaut et se replie en rail d’icônes ; l’état est mémorisé dans le navigateur (`wiki-panneau`). Les applications démarrent avec le panneau replié. En dessous, il devient un tiroir fermé par défaut, ouvert par un bouton « Menu » et refermé par Échap, le fond, le bouton de fermeture ou un lien suivi.
- Sur un écran paysage assez large, les cours utilisent la largeur disponible : contenu élargi, manipulations à un seul schéma affichées côte à côte (schéma à gauche, réglages et lectures à droite), quiz et check-list sur deux colonnes. Le sommaire horizontal du cours laisse la place à celui du panneau quand le panneau est ouvert. En portrait et sur téléphone, la présentation des sources est conservée.
- Thème clair ou sombre suivi par le panneau et les pages du wiki ; aucun débordement horizontal à 360, 390, 768, 1280 et 1440 px ; liens valides à la racine et sous un sous-chemin ; sources des cours intactes, scripts et ancres préservés.
- Tests de parcours RED puis GREEN ; vérification au navigateur des cours réels.

Preuve TDD du 7 octobre 2026 : RED de `uv run --group browser pytest tests/browser/test_navigation_panel.py` (10 échecs : ni panneau, ni bouton « Menu », bandeau encore présent, manipulation empilée). GREEN après implémentation : 10 réussis, à la racine et sous `/promo/`. Les parcours existants qui utilisaient le bandeau ouvrent d’abord le menu sur téléphone ; le parcours paysage a été ajusté au choix final (lectures et commentaire sous le schéma). Suites complètes : 86 tests Python, 33 parcours Chromium et 34 tests navigateur des applications.

Mesure sur les 153 manipulations des cours réels, nombre plus hautes que la fenêtre avant → après : 86 → 18 à 1280×800, 98 → 13 à 1366×768, 38 → 2 à 1440×900, 1 → 1 à 1920×1080 (hauteur médiane : 1,09 → 0,83 écran à 1366×768). Les dessins mesurés par les cours restent à l’échelle 1 après regroupement. Balayage des 43 pages publiées à 360, 390, 768, 1280 et 1440 px, en clair et en sombre : aucun débordement horizontal ni erreur JavaScript. Captures du panneau ouvert, du rail, du tiroir sur téléphone, de l’accueil, d’une matière, du planning et du jeu inspectées.

Limites : la série Métallurgie garde sa largeur d’origine, ses figures s’allongeant avec la largeur ; les manipulations à deux schémas ou à matrices restent empilées ; quelques manipulations très riches en réglages dépassent encore un écran de 768 px de haut.

## S22 — Suggestions de recherche pendant la saisie

En tant qu’élève, je saisis le début d’une notion dans le panneau latéral et j’accède directement au cours ou au chapitre pertinent, sans devoir valider une recherche complète.

- Dès le premier caractère, une liste propose au plus huit cours, sections ou applications publiés, avec leur contexte. Les titres et débuts de mots priment sur les mots-clés ; accents et casse sont ignorés, les fragments et recherches à plusieurs mots fonctionnent.
- Un clic mène directement au cours ou à son ancre, depuis toute page, à la racine et sous un sous-chemin GitHub Pages. Un lien permet de voir tous les résultats ; Entrée sans sélection conserve la recherche complète.
- Flèches haut/bas et Entrée permettent de choisir au clavier ; Échap ferme d’abord les suggestions, sans fermer le tiroir mobile. Effacement, sortie du champ et clic extérieur ferment la liste. Les états sont annoncés aux lecteurs d’écran.
- Une réponse lente ne remplace pas une saisie plus récente ou effacée ; l’index est partagé avec la recherche complète et une erreur permet une nouvelle tentative à la saisie suivante.
- Liste lisible en clair et sombre, sur téléphone et ordinateur, panneau ouvert ou replié ; aucun débordement horizontal. Soumission classique conservée sans JavaScript. Sources pédagogiques intactes.
- Tests de parcours RED puis GREEN, suites utiles et build valides, contrôle visuel des pages réelles avant publication.

Preuve TDD du 8 octobre 2026 : RED exécuté avec `uv run --group browser pytest tests/browser/test_search_suggestions.py -q -x` sur l’absence de liste de suggestions. GREEN après implémentation, puis ajout d’une régression repérée au contrôle visuel : une nouvelle saisie conservait le défilement précédent sur écran bas (RED : 2 échecs ; GREEN après remise en haut de la liste). Les 16 nouveaux parcours passent, à la racine et sous `/promo/` : fragments, accents, mots-clés, plusieurs termes, clavier, mobile, liens directs, recherche complète, cache partagé, panne de l’index et réponses tardives.

Validation : 87 tests Python, 49 parcours Chromium du wiki, 25 tests Node et 34 parcours Chromium des applications ; catalogue et build valides (29 cours, 319 sections, 7 matières, 1 application). Le classement et le chargement de l’index sont partagés avec la recherche complète ; aucune dépendance ni service externe ajouté.

QA du site réel sous `/PolyWE/` : 84 configurations sur six pages représentatives (accueil, planning, matière Brasage, cours Brasage 1, cours RDM 2, Mohr Forge), en clair et sombre, à 360, 390, 768, 1280, 1366 et 1440 px, plus un écran de 390 × 420 px. Saisie `bra`, recherche sans accents `capillarite`, huit propositions au maximum, parcours clavier complet, visibilité de l’option sélectionnée au-dessus du lien collant, fermeture, repli et réouverture du panneau vérifiés. Aucun débordement horizontal ni erreur JavaScript ou HTTP locale. Six captures inspectées ; les captures mobiles finales attendent la fin de l’animation du tiroir. Sources des cours, catalogue et planning inchangés ; le dossier local non suivi de soudage sous flux reste hors publication.

## S23 — Réviser le soudage à l’arc sous flux

En tant qu’élève, je retrouve les trois premiers cours d’arc submergé depuis la matière, le panneau latéral, le planning et la recherche assistée.

- Nouvelle matière « Soudage à l’arc sous flux (arc submergé) », cours `arc-submerge-01` à `arc-submerge-03` : procédé 12 et installation ; flux, fils et métal déposé ; paramètres et forme du cordon.
- URL stables sous `ArcSubmerge/`, progression 1 ↔ 2 ↔ 3, prérequis conseillés issus des en-têtes, sections indexées et partageables.
- Rattachement au sujet `1-10-arc-submerge` (IWE 1.10), sans changer les séances ni les autorisations des PDF. Documentation du planning actualisée.
- Sources livrées conservées à l’identique : ancres, scripts, clés de stockage. Le quatrième cours annoncé n’est pas présenté comme disponible. Les défauts éventuellement constatés sont consignés ici pour correction dans les sources.
- Parcours RED puis GREEN, tests et build valides ; QA des trois cours en clair et sombre, sur téléphone et en paysage, panneau ouvert et replié ; commit, push, contrôle de GitHub Actions et du site public.

Aucune fiche d’intégration séparée présente : métadonnées tirées des en-têtes et chapitres, sujet confirmé par `wiki sujets "1.10"`. Cette intégration ne constitue pas une nouvelle validation scientifique du contenu.

Preuve TDD du 8 octobre 2026 : RED exécuté avec `uv run pytest tests/test_content.py -q -k arc_submerge` sur l’absence des trois pages publiées. GREEN après inscription par `wiki ajouter` et renseignement des métadonnées. Le parcours vérifie les liens depuis l’accueil, la matière et le planning, les six chapitres de chaque cours dans la recherche, les prérequis, les cours voisins, la conservation des scripts et ancres, et l’absence de quatrième cours disponible. Aucun changement du générateur.

Validation locale : 88 tests Python et 49 parcours Chromium du wiki réussis ; catalogue et build valides (32 cours, 355 sections, 8 matières, 1 application). Les séances et les autorisations des PDF sont inchangées.

QA des trois cours construits sous `/PolyWE/` : 18 animations, 36 questions de quiz et remise à zéro, cases et thème mémorisés après rechargement, copie et partage de section simulés, navigation depuis la matière et la semaine 41, suggestions `SAW` et `basicite` vers les nouveaux supports. Modes clair et sombre aux largeurs 360, 390, 768, 1280, 1366 et 1440 px ; tiroir mobile, panneau ouvert et replié vérifiés. Les 8 904 états contrôlés (réglages initiaux, extrêmes individuels et simultanés des curseurs, préréglages et leurs extrêmes) ne présentent aucun débordement horizontal, aucune valeur indéfinie et aucun texte SVG hors viewBox avec une tolérance de 2 unités. Aucune erreur JavaScript ou HTTP locale. Les 18 manipulations tiennent dans la hauteur de 768 px en paysage à 1366 px de large. Captures des 18 manipulations et des trois en-têtes mobiles sombres inspectées ; empreintes SHA-256 des sources inchangées.

Défaut graphique mineur de la source à corriger par l’auteur : cours 1, manipulation 1, la fin de la légende « aspiration du flux non fondu » est partiellement masquée par le tube contact à 1366 × 768. Le dessin et ses réglages restent utilisables ; la source est conservée à l’identique. Le quatrième cours annoncé dans les pages reste à livrer.

## S24 — Terminer les procédés et ouvrir les essais destructifs

En tant qu’élève, je retrouve les cinq nouveaux cours depuis leur matière, le planning et la recherche, avec les prérequis et la progression des séries.

- Les séries Électrode enrobée et Arc submergé comprennent respectivement leurs cinq et quatre cours ; leurs URL existantes restent stables.
- La nouvelle matière « Essais destructifs et métallographiques » présente, dans l’ordre, traction, dureté et examens métallographiques (`essais-01` à `essais-03`).
- Les cours de procédés complètent les sujets IWE 1.9 et 1.10 ; les trois cours d’essais sont rattachés à `2-23-essais-des-materiaux`, avec leur chapitre 6 en complément de `2-23-essais-des-soudures`. Les supports existants sont conservés, les séances et autorisations des PDF restent inchangées.
- Les scripts, ancres et sources livrés sont préservés. La correction déjà fournie de la légende du cours Arc submergé 1 est également publiée et contrôlée.
- Tests RED puis GREEN, catalogue et build valides ; contrôle navigateur des interactions, thèmes, recherche, partage, téléphone, panneau ouvert et replié, et lecture paysage à 1366 × 768 ; publication et site public vérifiés.

Métadonnées issues des en-têtes et des correspondances au planning des cinq sources, aucune fiche d’intégration séparée présente. Cette intégration ne constitue pas une nouvelle validation scientifique du contenu.

Preuve TDD du 9 octobre 2026 : RED exécuté avec `uv run pytest tests/test_content.py -q -k 'arc_submerge or electrode_enrobee or essais'` : trois échecs sur les pages encore absentes. GREEN après inscription des cinq cours par `wiki ajouter`, métadonnées et rattachements explicites : trois parcours réussis. Les tests vérifient la progression complète des procédés, les prérequis, les chapitres indexés, les scripts et ancres conservés, ainsi que les liens distincts des essais vers les deux sujets 2.23 et la conservation des supports de rupture.

Validation locale : 89 tests Python et 49 parcours Chromium du wiki réussis ; catalogue et build valides (37 cours, 415 sections, 9 matières, 1 application). Les dates, horaires et autorisations des PDF sont inchangés. Aucun changement du générateur ni des applications.

QA des cinq cours construits sous `/PolyWE/` : 30 manipulations, leurs 27 animations disponibles, 60 questions de quiz et remise à zéro ; mémorisation des cases et du thème après rechargement, copie et partage de section simulés, accès depuis les trois matières et le planning, suggestions `traction` et accès direct à `Vickers`. Modes clair et sombre aux largeurs 360, 390, 768, 1280, 1366 et 1440 px, tiroir mobile et panneau ouvert/replié. Les 12 852 états contrôlés (initiaux, extrêmes individuels et simultanés des curseurs, préréglages et leurs extrêmes) ne montrent aucun débordement horizontal, aucune valeur indéfinie ni texte SVG hors viewBox avec une tolérance de 2 unités. Aucune erreur JavaScript ou HTTP locale. Les 30 manipulations tiennent dans la hauteur de 768 px en paysage à 1366 px de large à l’état initial. Captures des 30 manipulations et des cinq en-têtes mobiles sombres inspectées.

Limites des sources signalées à l’auteur : Brinell (`essais-02#c2`), découpe et lecture de macrographie (`essais-03#c2`, `essais-03#c6`) disposent de curseurs et préréglages fonctionnels mais pas de lecture automatique ; le repère d’épaisseur sur le film du négatoscope (`electrode-enrobee-05#c3`) est peu contrasté en thème clair. Ces limites n’empêchent pas l’utilisation des cours ; les sources restent inchangées.

La correction livrée de la légende « aspiration du flux non fondu » (`arc-submerge-01#c1`) est contrôlée à 390 et 1366 px : elle est désormais placée à gauche du tube d’aspiration et reste lisible. Empreintes SHA-256 des cinq nouveaux cours et de cette source corrigée inchangées depuis leur réception pour l’intégration.

## S25 — Assistant de révision IA avec le compte OpenRouter du visiteur

En tant qu’élève, je pose une question depuis n’importe quelle page du wiki et j’obtiens une réponse courte, appuyée sur les sections des cours et citée, en payant ma propre consommation avec mon compte OpenRouter.

- Un bouton discret « Chat » en bas à droite de toutes les pages publiées (accueil, matières, parcours, planning, cours, documents, applications) ouvre un panneau ; sur téléphone, il se place au-dessus du bouton « Menu » et le panneau occupe l’écran. Thème clair ou sombre suivi, aucun débordement horizontal, panneau accessible (dialogue nommé, Échap ferme et rend le focus). Les sources des cours restent intactes.
- Connexion par OAuth PKCE (S256) : le visiteur part sur OpenRouter et revient sur la même page ; le code n’est échangé que si une connexion a été lancée depuis ce navigateur, puis il disparaît de l’adresse. Clé conservée dans le navigateur sous `polywe_chat_key` ; déconnexion possible. Aucune clé dans le code ni dans le dépôt. Le panneau indique que les questions partent chez OpenRouter et chez le fournisseur du modèle, facturées au visiteur.
- Le build publie `assets/chat-extraits.json` : texte des sections des seuls cours disponibles, sans scripts, styles ni dessins, avec un identifiant stable `COURS-ANCRE` (`RDM-04-C3`). À chaque question, le texte sélectionné à l’ouverture passe en premier, puis les trois sections les plus pertinentes du site entier, chacune réduite à son meilleur passage.
- Requête en streaming vers `chat/completions` : prompt système imposé, modèle choisi parmi les candidats vérifiés au chargement (présents chez OpenRouter et compatibles avec les outils, GPT-6.1 Sol par défaut), `reasoning.effort` bas, 1 500 tokens au plus, trois derniers échanges, outil `openrouter:web_search` limité à une recherche Exa sur `ALLOWED_DOMAINS`.
- Rendu sans HTML issu du modèle : gras, italique, listes, code et liens http(s) seulement. Les `[ID]` deviennent des liens vers la section ; un identifiant absent des extraits envoyés est signalé « source non vérifiée ». Sources web listées, badge « Hors cours » avec un bouton « Vérifier sur le web » qui relance la question, tokens et coût affichés discrètement. Messages clairs pour 401 (reconnexion), 402, 429, réponse tronquée et panne réseau.
- Tests RED puis GREEN : build (extraits, brouillons exclus, widget sur chaque type de page), cœur du widget sous Node sans dépendance (PKCE, requête, citations, rendu sûr, flux), parcours Chromium avec OpenRouter simulé, à la racine et sous un sous-chemin.

Décision du propriétaire : ce service externe, facultatif et payé par chaque visiteur, lève pour l’assistant l’exclusion « pas de service externe » de la première version. Le site reste statique, sans serveur ni secret.

Preuve TDD du 9 octobre 2026 : RED exécuté avant implémentation avec `uv run pytest tests/test_chat.py` (3 échecs : `chat-extraits.json` absent, widget non inclus) et `node --test tests/js/*.test.cjs` (module absent). Les parcours `tests/browser/test_chat_widget.py`, écrits avec le widget, ont été exécutés contre un `chat-widget.js` vide : 20 échecs sur l’absence du bouton « Chat ». GREEN après implémentation : 3 tests Python, 12 tests Node et 22 parcours Chromium (11 à la racine et sous `/promo/`). Une seconde boucle RED/GREEN a corrigé le classement mesuré sur le site réel : quiz et check-lists exclus des extraits, titre du cours réservé au départage, au moins deux mots de la question exigés (une question hors sujet n’envoie plus d’extrait), « avant » et « après » ignorés.

Validation locale : 91 tests Python, 71 parcours Chromium du wiki, 25 tests Node des applications et 12 de l’assistant, 34 parcours Chromium des applications ; catalogue et build valides (37 cours, 415 sections, 357 extraits pour l’assistant, 1,99 Mo, 643 Ko compressés, chargés seulement quand le visiteur connecté utilise le champ de question).

QA du site réel sous `/PolyWE/`, OpenRouter simulé : 144 configurations (accueil, planning, matière RDM, cours RDM 4, cours Brasage 1, Mohr Forge ; 360, 390, 768, 1280, 1366 et 1440 px ; clair et sombre ; connecté ou non). Bouton dans l’écran, jamais sur le bouton « Menu » ni sur la barre de quête de Mohr Forge, panneau dans l’écran, aucun débordement horizontal, Échap ferme, aucune erreur JavaScript. Captures du panneau de connexion et d’une réponse citée (téléphone et 1366 px, clair et sombre) et de Mohr Forge inspectées. Pertinence vérifiée sur douze questions types (préchauffage, loi de Paris, Mohr, brasage, étuvage, carbone équivalent, Charpy, basicité, Vickers, t8/5, martensite, question hors sujet).

Limites : le conteneur de développement n’accède pas à `openrouter.ai`. Les identifiants des modèles viennent de sources secondaires et sont vérifiés par le widget au chargement ; Gemini 4 Argon n’était pas publié par OpenRouter début octobre 2026 et reste masqué tant qu’il est absent. La forme exacte des annotations `url_citation` dans le flux de l’outil web est gérée dans les deux emplacements connus et reste à confirmer. Connexion, crédits, recherche web et facturation réelles relèvent d’un test manuel avec un compte.

## S26 — Guide pas à pas de l’assistant de révision

En tant qu’élève qui découvre le bouton « Chat », je trouve facilement un guide qui m’accompagne de la création de mon compte OpenRouter jusqu’à ma première question, puis m’aide à lire la réponse et à régler un problème.

- Une page `assistant.html`, construite par le générateur avec le panneau du wiki et l’assistant : six étapes numérotées et ancrées (`#etape-1` à `#etape-6`) — créer le compte, ajouter des crédits, se connecter depuis le wiki, protéger sa clé, poser une question, lire la réponse — puis ce qui est envoyé et gardé, et les solutions aux messages d’erreur.
- Accès bien placés : un encadré sur l’accueil à côté du planning ; une entrée « Assistant IA » dans le panneau de toutes les pages, y compris en rail ; un lien vers le guide dans le chat, au moment de se connecter et en pied du panneau.
- Sur la page, l’état de l’appareil (connecté ou non) s’affiche ; un bouton ouvre l’assistant et des questions d’exemple le préremplissent sans rien envoyer.
- Aucune donnée inventée sur OpenRouter : étapes décrites sans libellé d’écran non vérifié, coût donné en ordre de grandeur, montant exact renvoyé à l’affichage d’OpenRouter et à la ligne de coût sous chaque réponse.
- Liens valides à la racine et sous un sous-chemin ; clair et sombre ; aucun débordement horizontal à 360, 390, 768, 1280 et 1440 px.
- Tests RED puis GREEN, build valide, contrôle visuel.

Preuve TDD du 9 octobre 2026 : RED exécuté avec `uv run pytest tests/test_guide.py` (2 échecs : page `assistant.html` et encadré d’accueil absents) et `uv run --group browser pytest tests/browser/test_assistant_guide.py` (10 échecs). GREEN après implémentation : 2 tests Python et 10 parcours Chromium, à la racine et sous `/promo/` (accès depuis l’accueil, le panneau d’un cours et l’écran de connexion du chat ; état de l’appareil ; ouverture de l’assistant ; question d’exemple placée dans le champ sans aucune requête).

Validation locale : 93 tests Python, 81 parcours Chromium du wiki, 37 tests Node, 34 parcours Chromium des applications ; build et liens valides. QA sous `/PolyWE/` : accueil, guide et cours RDM 4 à 360, 390, 768, 1280, 1366 et 1440 px, clair et sombre, connecté ou non (72 configurations) : aucun débordement horizontal ni erreur JavaScript, état de l’appareil exact. Captures de l’accueil (encadrés côte à côte sur ordinateur, empilés sur téléphone) et du guide inspectées ; corrigés au passage : titre trop grand qui isolait « IA », identifiant coupé en fin de ligne, guillemets séparés de leur texte.

Sources des faits OpenRouter : inscription par Google, GitHub ou e-mail, crédits prépayés par carte ou cryptomonnaie avec frais d’achat, d’après plusieurs guides publics concordants ; les libellés d’écran et l’éventuelle limite de crédit à l’autorisation n’ont pas pu être vérifiés et ne sont pas décrits. Coût par question estimé d’après les paramètres de l’assistant et le tarif public du modèle par défaut, présenté comme ordre de grandeur.

