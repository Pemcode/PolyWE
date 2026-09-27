# Instructions pour les agents

## Objectif et choix actés

Construire le wiki de révision de la promo DU Ingénierie du soudage / IWE, pour GitHub Pages. Le nombre de matières et de cours doit pouvoir augmenter sans modifier le code de navigation. Le site est public une fois publié.

## Architecture simple

- HTML/CSS/JavaScript natifs pour le site ; petit générateur Python ; catalogue JSON versionné comme source des métadonnées. Pas de serveur, de base SQL ni de framework frontend sans besoin démontré.
- `catalogue-cours.json` décrit matières, cours et parcours. `fichier` désigne la source et `url` le chemin publié stable. Les sections sont extraites des HTML à chaque génération pour éviter un inventaire périmé.
- Garder des identifiants et chemins stables. Un cours `a_venir` n'a aucun lien de lecture. Un cours `brouillon` n'est pas publié.
- Les HTML des matières sont les sources éditoriales. L'utilisateur est en train de les réviser : ne pas les écraser, renommer ou réécrire sans tâche explicite. Le générateur enrichit uniquement les copies dans `_site/`.
- Ne publier que les cours disponibles explicitement inscrits au catalogue et leurs ressources déclarées. Ne jamais copier tout le dossier de travail dans le site.
- Tous les liens doivent fonctionner sous `https://compte.github.io/depot/` et sur un domaine à la racine.

## Stories et TDD

- Prendre une story de `docs/STORIES.md`, avec critères d'acceptation observables, avant chaque évolution fonctionnelle.
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
- Prévisualisation : `uv run python -m http.server 8000 --directory _site --bind 127.0.0.1`.
- Versionner le lockfile ; ignorer environnement virtuel, caches, captures et fichiers générés.

## Discipline de travail

- Lire l'état courant avant de modifier un fichier ; préserver les changements concurrents de l'utilisateur.
- Pas de délégation à des sous-agents sauf demande explicite de l'utilisateur.
- Ne pas corriger le fond scientifique sans tâche dédiée. Ne pas inventer de validation officielle, de sources ou de cours disponibles.
- Pas de compte élève, suivi collectif, service externe ou publication automatique des brouillons dans la première version.
- Garder les sauvegardes historiques locales hors du dépôt et de l'artefact publié.
- Le dépôt désigné est `https://github.com/Pemcode/PolyWE`. GitHub Pages est validé, mais le dépôt est initialement privé et l’offre actuelle refuse Pages (API 422). Ne pas changer la visibilité sans instruction du propriétaire. La variable de dépôt `PAGES_ENABLED=true` autorise les étapes de publication après activation de Pages ; les tests fonctionnent indépendamment.
