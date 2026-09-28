# Révisions IWE — Promo DU Ingénierie du soudage

Site de la promo : **[Révisions IWE](https://pemcode.github.io/PolyWE/)**.

Dépôt : [Pemcode/PolyWE](https://github.com/Pemcode/PolyWE).

Site statique destiné à GitHub Pages. Les cours interactifs restent des fichiers HTML éditables. Un catalogue JSON organise les matières, les cours et les parcours ; un générateur Python construit les pages et leur navigation.

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

## Ajouter ou remplacer un cours

1. Déposer le HTML dans le dossier de sa matière.
2. Ajouter ou modifier une entrée dans `catalogue-cours.json`.
3. Lancer `uv run python -m wiki check`, les tests et le build ; vérifier le cours en prévisualisation.

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
- Le cours RDM 04 est disponible. Le cours RDM 05 est déjà déclaré `a_venir` : compléter cette entrée à sa réception au lieu d'en ajouter un doublon.
- Les sections sont extraites du HTML à chaque build : première rubrique h2/h3 de chaque section avec `id`, ou titre h2/h3 portant son propre `id`. Conserver les ancres déjà partagées.
- Si un cours utilise des fichiers locaux externes, les déclarer individuellement dans `fichiers_associes`, avec leur chemin depuis la racine du projet. Les conserver dans le dossier du cours et vérifier leurs liens relatifs à son `url`. Les dépendances distantes, comme Google Fonts, restent distantes.

Le catalogue porte les titres de navigation et de l'onglet publié. Le corps des cours et leurs titres pédagogiques restent ceux des HTML sources. Les sources que l'utilisateur révise ne sont jamais réécrites par le générateur.

## Ajouter une matière ou un parcours

Ajouter un objet dans `matieres` avec un `id` sans accents (ex. `controles`), un `titre` et une `description`. Les nouveaux cours le référencent via `matiere`. Aucune modification du code ni des menus n'est nécessaire.

Un objet de `parcours` comporte `id`, `titre`, `description` et `etapes`. Chaque étape référence `cours` et `ancre`. Exemple : `{"cours": "met-03", "ancre": "s6"}`. Le build refuse une étape vers un cours indisponible ou une ancre inexistante.

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
uv run python -m wiki build
```

Les tests rapides utilisent des cours fictifs pour vérifier l'ajout de matières, les états, les liens, les ressources et la conservation des sources. Les tests navigateur lancent leur propre serveur local et vérifient les parcours à la racine et sous `/promo/`, avec une largeur de téléphone. Les groupes de dépendances et leurs versions sont verrouillés dans `uv.lock`.

## Publier les mises à jour avec GitHub Pages

Le site est en ligne à **https://pemcode.github.io/PolyWE/**. Le propriétaire a rendu le dépôt public ; la source Pages est **GitHub Actions** et la variable de dépôt `PAGES_ENABLED` vaut `true`.

1. Modifier les HTML et le catalogue. Conserver les chemins `url` et les ancres déjà partagés. Un cours pas encore prêt reste en `brouillon`.
2. Exécuter les vérifications décrites ci-dessus et contrôler le cours en prévisualisation.
3. Committer et pousser sur `main`. Le workflow teste, construit puis publie uniquement `_site/`. Suivre son résultat dans [GitHub Actions](https://github.com/Pemcode/PolyWE/actions). Les pull requests testent et construisent sans déployer.

Un lancement manuel est aussi possible dans **Actions → Vérifier et publier le wiki → Run workflow**. Pour reconfigurer le dépôt : **Settings → Pages → Source : GitHub Actions** ; puis **Settings → Secrets and variables → Actions → Variables → `PAGES_ENABLED=true`**.

Les liens relatifs fonctionnent sous `/PolyWE/` et sur un domaine à la racine. Le dépôt public et l'adresse du site sont deux surfaces distinctes : `.gitignore` exclut les sauvegardes historiques ; le générateur exclut les brouillons de l'artefact du site. Un brouillon suivi dans un dépôt public reste lisible dans ce dépôt.

## Partager dans WhatsApp

Placer **https://pemcode.github.io/PolyWE/** dans la description du groupe et épingler le message d'annonce. Chacun peut naviguer par matière, rechercher une notion ou suivre un parcours reliant plusieurs cours.

Dans un cours, **Partager** ouvre le menu de partage de l'appareil ; **Copier le lien** permet de coller l'adresse dans WhatsApp. **Partager cette section** cible directement le passage concerné. Le partage natif et la copie proposent un repli si le navigateur ne fournit pas l'API attendue. Les adresses restent valables quand le contenu d'un cours est mis à jour, à condition de conserver son `url` et ses ancres.

Références de configuration : [uv](https://docs.astral.sh/uv/guides/projects/), [uv dans GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/), [workflow GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
