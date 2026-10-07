# Instructions pour les agents

Ce dépôt construit le wiki public de révision de la promo DU Ingénierie du soudage / IWE, publié sur GitHub Pages. De nouveaux cours y arrivent régulièrement, au fil du planning de la formation. Deux activités se succèdent :

- **rédiger les cours** : des pages HTML autonomes rangées dans `Cours/<Matière>/` (actuellement confié à Claude Code) ;
- **intégrer et publier** : catalogue, planning, tests, build, commit et déploiement GitHub Pages (actuellement confié à Codex).

Chaque tâche relève de l'une ou de l'autre. Sauf demande explicite du propriétaire :

- l'agent qui rédige ne modifie ni le catalogue, ni le planning, ni les tests, et ne committe pas ;
- l'agent qui intègre ne réécrit pas le contenu d'un cours.

## Cycle d'un nouveau cours

1. **Partir du planning.**
   - Chaque cours répond à un ou plusieurs sujets de `planning-formation.json`. Les trouver avec `uv run python -m wiki sujets "<mot ou code IWE>"`.
   - Retenir l'identifiant du sujet, pas seulement son code : un même code peut recouvrir plusieurs intitulés (2.23, 3.6, 4.12…).
   - Le titre du cours reprend ou précise l'intitulé du sujet. Un écart important se justifie dans la fiche d'intégration.
   - Une série peut servir plusieurs sujets : la rupture couvre 2.7 et 3.11. Une matière du wiki ne correspond pas forcément à un thème du planning.
   - Pour proposer le cours suivant, regarder en priorité les sujets des semaines à venir encore sans support.
2. **Réunir les sources.**
   - Les polycopiés reçus sont rangés dans `Polycopies/`, un dossier par polycopié (par exemple `IWE_2.7_3.11_Tancret_Mecanique_de_la_rupture/`). Ce dossier est local et ignoré par Git.
   - Leur reproduction est interdite. Ne jamais recopier leurs images, scans ou passages : redessiner en SVG, reformuler et renvoyer aux pages.
   - Les PDF de `Planning/` gardent leur règle propre.
3. **Proposer un plan.**
   - Si le sujet est vaste, proposer un plan de série : nombre de cours, périmètre de chacun, pages de la source.
   - Centrer ce plan sur les attendus du certificat IWE et raboter ce qui en est éloigné.
   - Attendre sa validation. Rédiger ensuite un cours à la fois, chacun après le feu vert du propriétaire.
4. **Rédiger et contrôler**, selon les sections « Rédaction des cours » et « Contrôle qualité d'un cours ».
5. **Livrer.**
   - Déposer la page dans `Cours/<Matière>/` sous le nom `<Matière>, cours N _ <titre court>.html`.
   - Terminer par un résumé court du contenu et des priorités de travail.
   - Ajouter une **fiche d'intégration** pour l'agent qui publie :
     - l'identifiant proposé : `<matière>-NN`, ou celui d'un cours déjà annoncé ;
     - le titre aligné sur le planning ;
     - la matière : existante, ou nouvelle avec une phrase de description ;
     - les identifiants des sujets ;
     - les ancres utiles en complément d'autres sujets (`#cN`) ;
     - les prérequis et les mots-clés ;
     - l'URL proposée, `<Matière>/NN-slug.html` ;
     - les limites connues.
6. **Intégrer et publier**, selon « Stories et TDD » et « Routine de réception des supports ».
   - Étapes : story, test de parcours RED puis GREEN, `wiki ajouter` avec des métadonnées explicites, liens du planning et `docs/PLANNING.md`, vérifications, commit, push, puis contrôle de GitHub Actions et du site.
   - L'intégration ne modifie pas la source. Un défaut constaté est consigné dans la story et signalé, pour être corrigé dans la source.
7. **Corriger ensuite.** Modifier la source en place, en conservant son nom, ses ancres et ses clés de stockage, puis republier.

## Rédaction des cours

### Esprit

- Toujours ultra pédagogue, bienveillant, au tutoiement, pour un lecteur qui peut partir de zéro.
- Deux niveaux d'enseignement dans chaque chapitre.
- Dans chaque chapitre, des animations, graphiques et diagrammes dynamiques et interactifs pour une bonne imprégnation des concepts, qu'ils soient mathématiques, physiques, métallurgiques ou autres.
- Ne pas hésiter à faire des cours longs et complets.
- Des cours ludiques, qui favorisent la mémorisation, avec des visualisations adaptées à une mémoire photographique.
- Poser des questions avant de rédiger si et seulement si c'est pertinent, 3 au maximum : niveau, formation, périmètre, notations attendues.

### Livrable

- Chaque cours est une page HTML unique et autonome.
  - Le CSS est dans `<style>`, le JavaScript dans `<script>`, et les dessins sont en SVG générés par JavaScript.
  - Pas d'images ni de bibliothèques externes. Seule exception : les polices Google Fonts, avec polices de secours.
  - La page doit fonctionner hors ligne.
- Les cours sont longs et complets : environ 2 h 30 à 3 h de travail chacun, exercices compris.
- Reprendre à l'identique la base CSS et les utilitaires JavaScript (quiz, check-list, sommaire, thème) du cours précédent de la série. Pour une nouvelle série, reprendre ceux de la série la plus récente. Seuls le contenu et les manipulations changent.
- Contraintes du wiki :
  - Chaque chapitre est une `<section id="cN">` avec un titre `<h2>`. Les autres blocs gardent les ancres `avant`, `exos`, `quiz-s`, `fiche`, `gloss` et `check`. Le générateur en tire la recherche et les liens du planning : une ancre publiée ne change plus.
  - Les clés de stockage du navigateur sont préfixées par la matière (`<matière>-coursN-check`, `<matière>-theme`), car toutes les pages du site partagent la même origine.
  - Pas de lien vers un autre fichier de `Cours/` : la navigation entre cours vient du catalogue. Tout fichier annexe doit être signalé dans la fiche d'intégration.
  - Le dernier cours d'une série annonce la fin de la série au lieu d'un cours suivant, dans l'encadré final, le quiz et la check-list.
- Les fichiers de travail (fragments, assemblage, scripts de vérification, captures) restent hors du dépôt.
- Si un document de référence est fourni (polycopié, annales) :
  - aligner les notations, les conventions de signe et les renvois de pages sur ce document ;
  - signaler de façon neutre ses éventuelles erreurs ou ambiguïtés.

### Direction visuelle (identique pour toute une série)

- Esthétique « dessin technique » : fond papier millimétré léger.
- Polices : Barlow Condensed pour les titres, Atkinson Hyperlegible pour le texte, STIX Two Text pour les formules.
- Chaque chapitre s'ouvre sur un cartouche de plan en trois cases : numéro | titre et sous-titre | « Image à retenir » (un emoji et une phrase-image).
- Code couleur fixe, expliqué en tête de chaque cours et respecté partout (textes, formules, manipulations) :
  - les causes en couleurs chaudes (rouge, violet) ;
  - les effets en couleurs froides (bleu, bleu-vert) ;
  - les paramètres ou liens en vert ;
  - les actions ou forces en orange ;
  - les vecteurs géométriques en noir ;
  - les encadrés « métier » en bronze.
- Mode clair et mode sombre.
- Responsive, sans aucun débordement horizontal sur téléphone : les formules passent à la ligne, les tableaux et formules larges défilent dans leur propre cadre.

### Structure de chaque page

1. **En-tête.**
   - Un titre-cartouche à 4 cases : numéro du cours, durée conseillée, prérequis, « à la fin tu sais ».
   - Un chapeau d'introduction et le rappel du code couleur.
2. **Sommaire collant** qui surligne la section en cours de lecture.
3. **« Avant de commencer ».**
   - Le rappel du cours précédent en 3 cases.
   - La correspondance avec le document de référence (s'il existe) et avec le sujet du planning (code IWE et intitulé).
   - Pourquoi ce cours compte dans la pratique.
   - Le plan du cours.
4. **5 à 7 chapitres**, chacun avec :
   - « 👁 Niveau 1 : voir » : l'intuition, une analogie concrète, une image mentale, très peu de formules ;
   - une manipulation interactive (SVG et JavaScript), avec des curseurs, des boutons d'exemples, une animation « lecture », des valeurs calculées en direct et un message qui commente ce qu'on observe ;
   - « 🎓 Niveau 2 : maîtriser » : définitions rigoureuses, démonstrations, formules encadrées, pièges d'examen ;
   - des encadrés typés : 📖 définition, 💡 astuce, ⚠️ piège, mnémotechnique, 🔥 métier.
5. **Exercices corrigés** : 6 exercices et un défi.
   - Chaque exercice est étiqueté N1 ou N2 et indique les chapitres concernés.
   - Chaque sous-question a), b), c) est sur sa propre ligne.
   - La correction est masquée derrière « Voir la correction » et détaillée pas à pas, avec les unités.
6. **Quiz interactif** de 12 questions à choix multiples, avec une explication pour chaque réponse et un score.
7. **Fiche mémoire** : 9 cases (emoji, titre, formule clé, une phrase), puis une « visite du musée », une courte histoire qui enchaîne les 9 images dans l'ordre.
8. **Glossaire** de tous les termes, symboles et sigles du cours.
9. **Check-list** « suis-je prêt pour la suite ? » : 10 points, avec les cases cochées mémorisées dans le navigateur.
10. **Annonce du cours suivant** (ou de la fin de la série), puis pied de page.

### Règles pédagogiques

- Définir chaque symbole, sigle, abréviation et terme technique ou de jargon à sa première apparition dans chaque cours, même s'il a été défini dans un cours précédent. Cela inclut les notations mathématiques (∂, Σ, diag, transposée…).
- Écrire la formule littérale avant les valeurs numériques, avec les unités partout et des ordres de grandeur.
- Des visualisations pensées pour la mémoire photographique : une image forte par chapitre, des couleurs constantes, des schémas épurés.
- Un ton ludique : analogies du quotidien, défis, quiz, musée mnémotechnique.

### Neutralité

- Le site est public et les cours doivent pouvoir être partagés : aucune référence aux échanges de la conversation, à la situation personnelle de l'utilisateur, à ses délais ou à ses questions.
- Les références aux documents sources sont formulées de façon neutre (« le polycopié… », « le cours de référence… »).

### Contrôle qualité d'un cours

- Recalculer toutes les valeurs numériques : exercices, quiz, exemples des manipulations. Le défi doit pouvoir se rejouer dans la manipulation qui lui correspond.
- Vérifier les formules, les conventions de signe, et la cohérence avec les cours précédents, le document de référence et le sujet du planning.
- Tester la page dans un navigateur (Playwright via `uv run --group browser`) :
  - aucune erreur JavaScript, et toutes les manipulations fonctionnent ;
  - en mode clair et en mode sombre ;
  - sans débordement aux largeurs 360, 390, 768 et 1280 px ;
  - aucun texte de SVG ne sort de son cadre ni n'est tronqué, à chaque largeur et pour les réglages extrêmes des manipulations : comparer la boîte de chaque `<text>` au `viewBox` ;
  - contrôle visuel des schémas : étiquettes lisibles, rien ne se chevauche.
- Livrer, puis faire le résumé court et la fiche d'intégration (étape 5 du cycle).

## Objectif et choix actés

Construire le wiki de révision de la promo DU Ingénierie du soudage / IWE, pour GitHub Pages. Le nombre de matières et de cours doit pouvoir augmenter sans modifier le code de navigation. Le site est public une fois publié.

## Architecture simple

- HTML/CSS/JavaScript natifs pour le site ; petit générateur Python ; catalogue JSON versionné comme source des métadonnées. Pas de serveur, de base SQL ni de framework frontend sans besoin démontré.
- `catalogue-cours.json` décrit matières, cours et parcours. `fichier` désigne la source et `url` le chemin publié stable. Les sections sont extraites des HTML à chaque génération pour éviter un inventaire périmé.
- `planning-formation.json` décrit les phases, séances, sujets et sources PDF déclarées. Les supports référencent les identifiants du catalogue et éventuellement une ancre ; ne pas déduire une affectation des fiches à des heures que le planning ne précise pas. Les PDF de `Planning/` restent locaux et ignorés par Git ; `publier` vaut `false` par défaut. Ne publier un PDF que sur autorisation explicite du propriétaire. Voir `docs/PLANNING.md`.
- Garder des identifiants et chemins stables. Un cours `a_venir` n'a aucun lien de lecture. Un cours `brouillon` n'est pas publié.
- Les sources des matières sont rangées dans `Cours/<matière>/`. Le champ `fichier` suit cet emplacement ; les `url` publiées restent stables (notamment `RDM/…` et `Metallurgie/…`).
- Les HTML des matières sont les sources éditoriales. L'utilisateur est en train de les réviser : ne pas les écraser, renommer ou réécrire sans tâche explicite. Le générateur enrichit uniquement les copies dans `_site/`.
- Ne publier que les cours disponibles explicitement inscrits au catalogue et leurs ressources déclarées. Ne jamais copier tout le dossier de travail dans le site.
- Les applications interactives (jeux, simulateurs) sont du code versionné dans `applications/<id>/` et déclaré dans la liste `applications` du catalogue : seuls leurs `fichiers` sont publiés sous `publication`. Elles complètent une matière (section « S’entraîner », pied des cours liés, recherche) sans place centrale sur l’accueil. `publier` ne les embarque jamais ; leurs évolutions suivent le circuit de développement.
- Tous les liens doivent fonctionner sous `https://compte.github.io/depot/` et sur un domaine à la racine.

## Stories et TDD

- Prendre une story de `docs/STORIES.md`, avec critères d'acceptation observables, avant chaque évolution fonctionnelle. La rédaction ou la correction du contenu d'un cours n'en demande pas ; son intégration au wiki en demande une (exemple : S17).
- RED : écrire un test de comportement qui échoue pour la bonne raison et l'exécuter.
- GREEN : écrire le minimum pour le faire passer. REFACTOR : clarifier sans ajouter de fonctionnalités.
- Noter brièvement le résultat RED/GREEN dans la story ; ne pas prétendre avoir exécuté un test non exécuté.
- Les tests portent sur les parcours et risques réels : ajout de matière, états des cours, fichiers et ancres manquants, liens sous un sous-chemin GitHub Pages, conservation des scripts, recherche et partage.
- Pas de tests miroir, de métrique de couverture arbitraire ni de tests pour une simple correction typographique. Un bug fonctionnel reçoit un test de régression.
- Définition de terminé : critères satisfaits, tests utiles verts, build validé, documentation mise à jour. Vérifier au navigateur les interactions ou changements de mise en page significatifs.

## Outillage : uv

- Gérer Python et les dépendances avec `uv`, `pyproject.toml` et `uv.lock`. Ne pas ajouter pip, Poetry, npm ou un second gestionnaire pour ce projet sans nécessité explicite.
- Installation : `uv sync --locked`. Tests : `uv run pytest`. Construction : `uv run python -m wiki build`. Contrôle du catalogue : `uv run python -m wiki check`.
- Tests navigateur : `uv sync --locked --group browser`, `uv run --group browser playwright install chromium`, puis `uv run --group browser pytest tests/browser`.
- Applications : `node --test applications/*/tests/*.test.cjs` (Node 24 seul, sans npm ni dépendance), puis `uv run --group browser pytest applications`.
- Prévisualisation : `uv run python -m http.server 8000 --directory _site --bind 127.0.0.1`.
- Versionner le lockfile ; ignorer environnement virtuel, caches, captures et fichiers générés.

## Discipline de travail

- Lire l'état courant avant de modifier un fichier ; préserver les changements concurrents de l'utilisateur.
- Pas de délégation à des sous-agents sauf demande explicite de l'utilisateur.
- Ne pas corriger le fond scientifique sans tâche dédiée. Ne pas inventer de validation officielle, de sources ou de cours disponibles.
- Pas de compte élève, suivi collectif, service externe ou publication automatique des brouillons dans la première version.
- Garder les sauvegardes historiques locales hors du dépôt et de l'artefact publié.
- Le dépôt `https://github.com/Pemcode/PolyWE` a été rendu public par le propriétaire. GitHub Pages est activé via GitHub Actions à l’adresse `https://pemcode.github.io/PolyWE/`. La variable de dépôt `PAGES_ENABLED=true` autorise la publication après les contrôles sur `main` ; les pull requests ne déploient pas. Ne pas changer la visibilité sans instruction du propriétaire.

## Routine de réception des supports

- Procédure utilisateur : `Mettre-a-jour.cmd` ou `uv run python -m wiki gerer`, documentée dans `docs/MISE_A_JOUR.md`.
- Pour un ajout demandé, préférer `uv run python -m wiki ajouter FICHIER --id ...` avec les métadonnées explicites, en partant de la fiche d'intégration du cours. Réutiliser l’identifiant d’un cours annoncé ; le rattachement au planning reste un choix éditorial explicite via `--sujet`.
- Pour une correction, modifier seulement la source demandée, préserver URL et ancres, puis vérifier. Les documents PDF/Office utilisent une page HTML d’accès et `fichiers_associes`, sans nouveau stockage.
- `preparer` lance tests et build ; `apercu` ouvre le site local ; `publier` est réservé aux contenus. Les évolutions de code et documentation suivent les commits de développement habituels, avec les vérifications utiles avant le push.
- Ne pas contourner une exclusion Git ni inscrire automatiquement les fichiers déposés. La routine ne modifie pas l’autorisation propre aux PDF sources de Planning.
