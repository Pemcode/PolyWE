# Révisions IWE — Promo DU Ingénierie du soudage

Projet : [Pemcode/PolyWE](https://github.com/Pemcode/PolyWE).

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
  "titre": "Directions principales et cercle de Mohr",
  "statut": "disponible",
  "fichier": "RDM/cours-4-version-relue.html",
  "url": "RDM/04-directions-principales-mohr.html",
  "prerequis_conseilles": ["rdm-02", "rdm-03"],
  "mots_cles": ["Mohr", "contraintes principales"],
  "ressources": ["cours", "exercices corrigés"],
  "fichiers_associes": []
}
```

- `id` est l'identité stable du cours. `ordre` règle sa place dans la matière.
- `fichier` désigne le fichier source local. Il peut changer lors d'un remplacement.
- `url` est le chemin publié : le conserver après partage. Il utilise un sous-dossier et l'extension `.html`.
- `disponible` publie le cours ; `a_venir` affiche une carte sans lien ; `brouillon` exclut complètement le cours du site et de la recherche. Les deux derniers états n'exigent aucun fichier.
- Les cours RDM 04 et 05 sont déjà déclarés `a_venir` : compléter ces entrées au lieu d'en ajouter des doublons.
- Les sections sont extraites du HTML à chaque build : première rubrique h2/h3 de chaque section avec `id`, ou titre h2/h3 portant son propre `id`. Conserver les ancres déjà partagées.
- Si un cours utilise des fichiers locaux externes, les déclarer individuellement dans `fichiers_associes`, avec leur chemin depuis la racine du projet. Les conserver dans le dossier du cours et vérifier leurs liens relatifs à son `url`. Les dépendances distantes, comme Google Fonts, restent distantes.

Le catalogue porte les titres de navigation et de l'onglet publié. Le corps des cours et leurs titres pédagogiques restent ceux des HTML sources. Les sources que l'utilisateur révise ne sont jamais réécrites par le générateur.

## Ajouter une matière ou un parcours

Ajouter un objet dans `matieres` avec un `id` sans accents (ex. `controles`), un `titre` et une `description`. Les nouveaux cours le référencent via `matiere`. Aucune modification du code ni des menus n'est nécessaire.

Un objet de `parcours` comporte `id`, `titre`, `description` et `etapes`. Chaque étape référence `cours` et `ancre`. Exemple : `{"cours": "met-03", "ancre": "s6"}`. Le build refuse une étape vers un cours indisponible ou une ancre inexistante.

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

## Publier avec GitHub Pages

1. Dépôt de la promo : [Pemcode/PolyWE](https://github.com/Pemcode/PolyWE).
2. Avant le premier push, terminer la relecture des contenus à publier ou passer les cours concernés en `brouillon`.
3. Dans le dépôt : **Settings → Pages → Build and deployment → Source : GitHub Actions**.
4. Dans **Settings → Secrets and variables → Actions → Variables**, définir `PAGES_ENABLED` à `true` une fois Pages activé. Envoyer ensuite le projet sur la branche principale du dépôt, ou lancer le workflow manuellement. Le workflow teste, construit et publie uniquement `_site/`. Les pull requests testent et construisent sans déployer.
5. Récupérer l'adresse fournie par le déploiement et la placer dans la description du groupe WhatsApp.

Les fichiers restent lisibles sous `https://compte.github.io/depot/` sans saisir ce préfixe dans le code : les liens du site sont relatifs. Le dépôt public et l'adresse du site sont deux surfaces distinctes : `.gitignore` exclut les sauvegardes historiques ; le générateur exclut les brouillons de l'artefact du site. Un brouillon suivi dans un dépôt public reste lisible dans ce dépôt.

Au premier raccordement, le dépôt est privé et l’API GitHub refuse Pages avec l’offre actuelle. La publication reste donc désactivée tant que `PAGES_ENABLED` n’est pas activé ; les contrôles continuent de s’exécuter. Le choix entre dépôt public et offre compatible avec un dépôt privé appartient au propriétaire. Les aperçus WhatsApp réels nécessitent ensuite l’URL publiée. Le partage natif et la copie ont une solution de repli quand le navigateur ne propose pas l'API attendue.

Références de configuration : [uv](https://docs.astral.sh/uv/guides/projects/), [uv dans GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/), [workflow GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
