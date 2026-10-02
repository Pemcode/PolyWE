# Révisions IWE — Promo DU Ingénierie du soudage

Site de la promo : **[Révisions IWE](https://pemcode.github.io/PolyWE/)**.

Dépôt : [Pemcode/PolyWE](https://github.com/Pemcode/PolyWE).

Site statique destiné à GitHub Pages. Les cours interactifs restent des fichiers HTML éditables. Un catalogue JSON organise les matières, les cours et les parcours ; un générateur Python construit les pages et leur navigation.

## Routine quotidienne

**Double-cliquer sur `Mettre-a-jour.cmd`** pour ouvrir le menu.

1. Déposer le nouveau fichier dans le dossier de sa matière.
2. **Ajouter** : choisir le cours annoncé ou créer un support ; sélectionner la matière et, si utile, le sujet de planning. HTML, PDF, Word, PowerPoint et Excel sont acceptés.
3. **Aperçu** : vérifier le résultat dans le navigateur.
4. **Publier** : les tests et le build s’exécutent ; confirmer les fichiers affichés. GitHub Actions contrôle puis met Pages à jour.

Pour corriger un cours ou document existant, modifier son fichier puis passer directement à l’aperçu et à la publication. Aucun JSON à rééditer pour une simple correction.

En terminal : `uv run python -m wiki gerer`. Voir le **[guide de mise à jour](docs/MISE_A_JOUR.md)** pour les exemples, les documents et la reprise après une erreur.

## Démarrer avec uv

```powershell
uv sync --locked
uv run pytest
uv run python -m wiki check
uv run python -m wiki build
uv run python -m http.server 8000 --directory _site --bind 127.0.0.1
```

Ouvrir http://127.0.0.1:8000. Arrêter le serveur avec Ctrl+C. Relancer la construction après une modification ; il n'y a pas de serveur de développement supplémentaire ni de compilation JavaScript.

`_site/` est une sortie générée : ne pas la modifier à la main. Les dossiers `.sauvegardes/`, `.venv/`, les tests et les documents de travail ne sont pas copiés dans le site.

## Catalogue : réglages avancés

L’assistant d’ajout renseigne `catalogue-cours.json` et, si demandé, les supports du planning. L’édition manuelle reste possible pour les prérequis, les parcours, les états et les ajustements éditoriaux.

Exemple d'entrée, à adapter avec un fichier réellement présent :

```json
{
  "id": "rdm-04",
  "matiere": "rdm",
  "repere": "Cours 04",
  "ordre": 4,
  "titre": "Directions principales et tricercle de Mohr",
  "statut": "disponible",
  "fichier": "RDM/RDM, cours 4 _ directions principales et tricercle de Mohr.html",
  "url": "RDM/04-directions-principales-mohr.html",
  "prerequis_conseilles": ["rdm-01", "rdm-02", "rdm-03"],
  "mots_cles": ["Mohr", "tricercle", "contraintes principales"],
  "ressources": ["cours", "exercices corrigés"],
  "fichiers_associes": []
}
```

- `id` est l'identité stable du cours. `ordre` règle sa place dans la matière.
- `fichier` désigne le fichier source local. Il peut changer lors d'un remplacement.
- `url` est le chemin publié : le conserver après partage. Il utilise un sous-dossier et l'extension `.html`.
- `disponible` publie le cours ; `a_venir` affiche une carte sans lien ; `brouillon` exclut complètement le cours du site et de la recherche. Les deux derniers états n'exigent aucun fichier.
- Les cours RDM 01 à 07 sont disponibles, de Hooke aux diagrammes de sollicitations. Lorsqu’un prochain cours possède déjà une entrée `a_venir`, compléter cette entrée plutôt qu’en créer un doublon.
- Les sections sont extraites du HTML à chaque build : première rubrique h2/h3 de chaque section avec `id`, ou titre h2/h3 portant son propre `id`. Conserver les ancres déjà partagées.
- Si un cours utilise des fichiers locaux externes, les déclarer individuellement dans `fichiers_associes`, avec leur chemin depuis la racine du projet. Les conserver dans le dossier du cours et vérifier leurs liens relatifs à son `url`. Les dépendances distantes, comme Google Fonts, restent distantes.

Le catalogue porte les titres de navigation et de l'onglet publié. Le corps des cours et leurs titres pédagogiques restent ceux des HTML sources. Les sources que l'utilisateur révise ne sont jamais réécrites par le générateur.

## Ajouter une matière ou un parcours

Ajouter un objet dans `matieres` avec un `id` sans accents (ex. `controles`), un `titre` et une `description`. Les nouveaux cours le référencent via `matiere`. Aucune modification du code ni des menus n'est nécessaire.

Un objet de `parcours` comporte `id`, `titre`, `description` et `etapes`. Chaque étape référence `cours` et `ancre`. Exemple : `{"cours": "met-03", "ancre": "s6"}`. Le build refuse une étape vers un cours indisponible ou une ancre inexistante.

## Applications interactives

Un jeu ou un simulateur complète une matière sans occuper l’accueil. Son code est versionné dans `applications/<id>/` et déclaré dans la liste `applications` du catalogue. Premier exemple : **[Mohr Forge](https://pemcode.github.io/PolyWE/RDM/mohr-forge/index.html)**, le laboratoire 3D des contraintes et déformations et son mode histoire, rattaché à la RDM.

```json
{
  "id": "mohr-forge",
  "titre": "Mohr Forge",
  "genre": "Jeu d’entraînement",
  "matiere": "rdm",
  "statut": "disponible",
  "ordre": 1,
  "source": "applications/mohr-forge",
  "entree": "index.html",
  "fichiers": ["index.html", "assets/style.css", "js/app.js"],
  "publication": "RDM/mohr-forge",
  "cours_lies": ["rdm-01", "rdm-02", "rdm-03", "rdm-04", "rdm-05"],
  "mots_cles": ["Mohr", "tricercle"],
  "ressources": ["laboratoire 3D", "mode histoire"]
}
```

- Seuls les `fichiers` listés sont publiés, dans le dossier `publication` : tests, documentation et scripts de l’application restent hors du site. Déclarer chaque nouveau fichier nécessaire au jeu.
- L’application apparaît dans la section « S’entraîner » de sa matière, en pied des `cours_lies` et dans la recherche ; l’accueil ne mentionne que leur nombre dans la carte de la matière.
- La copie publiée reçoit la barre du wiki (retour à la matière, partage) ; la source reste jouable seule, par exemple avec `applications/mohr-forge/Jouer.cmd`.
- Les états `disponible`, `a_venir` et `brouillon` suivent les règles des cours. Une application est du code : la routine **Publier** ne l’embarque pas, ses évolutions passent par les commits de développement.

## Planning de formation

La [frise de formation](https://pemcode.github.io/PolyWE/planning.html) relie les séances aux supports disponibles. Elle propose la semaine actuelle, les filtres de période/matière et les examens, avec les références des deux plannings sources. L'affichage reste consultable sans JavaScript. Les PDF sources sont conservés localement, hors du dépôt et du site publics.

`planning-formation.json` sépare les séances, sujets et sources du catalogue des cours. Ajouter un cours aux `supports` d'un sujet le fait apparaître sur toutes les séances correspondantes ; son état de disponibilité vient du catalogue. Après une modification du planning, `uv run python -m wiki check` vérifie aussi ses dates, références et ancres. Voir [l'analyse et la procédure de mise à jour](docs/PLANNING.md).

Pour partager une semaine, utiliser « Lien vers cette semaine », par exemple [la semaine du 28 septembre](https://pemcode.github.io/PolyWE/planning.html#semaine-2026-40). Les filtres sont conservés dans l'adresse de la page.

## Tests et TDD

Les règles sont dans [AGENTS.md](AGENTS.md), les critères et preuves dans [docs/STORIES.md](docs/STORIES.md). Cycle attendu : une story → un test en échec → implémentation minimale → refactorisation → vérification.

```powershell
uv run pytest
uv sync --locked --group browser
uv run --group browser playwright install chromium
uv run --group browser pytest tests/browser
node --test applications/mohr-forge/tests/*.test.cjs
uv run --group browser pytest applications
uv run python -m wiki build
```

Les moteurs des applications sont testés avec Node 24 seul, sans npm ni dépendance ; leurs parcours Chromium utilisent l’environnement uv du wiki. Le contrôle visuel du jeu publié s’obtient avec `uv run --group browser python applications/mohr-forge/scripts/visual_check.py`.

Les tests rapides utilisent des cours fictifs pour vérifier l'ajout de matières, les états, les liens, les ressources et la conservation des sources. Les tests navigateur lancent leur propre serveur local et vérifient les parcours à la racine et sous `/promo/`, avec une largeur de téléphone. Les groupes de dépendances et leurs versions sont verrouillés dans `uv.lock`.

## Publier les mises à jour avec GitHub Pages

Le site est en ligne à **https://pemcode.github.io/PolyWE/**. Le propriétaire a rendu le dépôt public ; la source Pages est **GitHub Actions** et la variable de dépôt `PAGES_ENABLED` vaut `true`.

Pour les contenus, utiliser **Publier** dans le menu ou `uv run python -m wiki publier` : tests, build, liste des fichiers, confirmation, commit et push sur `main`. La routine sélectionne seulement les supports déclarés et les deux JSON ; elle conserve les fichiers non déclarés et refuse les changements de code en attente.

Pour une évolution du code, suivre les tests ci-dessus puis faire un commit et un push de développement habituels. Dans les deux cas, le workflow contrôle puis publie uniquement `_site/`. Suivre son résultat dans [GitHub Actions](https://github.com/Pemcode/PolyWE/actions). Les pull requests testent et construisent sans déployer.

Un lancement manuel est aussi possible dans **Actions → Vérifier et publier le wiki → Run workflow**. Pour reconfigurer le dépôt : **Settings → Pages → Source : GitHub Actions** ; puis **Settings → Secrets and variables → Actions → Variables → `PAGES_ENABLED=true`**.

Les liens relatifs fonctionnent sous `/PolyWE/` et sur un domaine à la racine. Le dépôt public et l'adresse du site sont deux surfaces distinctes : `.gitignore` exclut les sauvegardes historiques ; le générateur exclut les brouillons de l'artefact du site. Un brouillon suivi dans un dépôt public reste lisible dans ce dépôt.

## Partager dans WhatsApp

Placer **https://pemcode.github.io/PolyWE/** dans la description du groupe et épingler le message d'annonce. Chacun peut naviguer par matière, rechercher une notion ou suivre un parcours reliant plusieurs cours.

Dans un cours, **Partager** ouvre le menu de partage de l'appareil ; **Copier le lien** permet de coller l'adresse dans WhatsApp. **Partager cette section** cible directement le passage concerné. Le partage natif et la copie proposent un repli si le navigateur ne fournit pas l'API attendue. Les adresses restent valables quand le contenu d'un cours est mis à jour, à condition de conserver son `url` et ses ancres.

Références de configuration : [uv](https://docs.astral.sh/uv/guides/projects/), [uv dans GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/), [workflow GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
