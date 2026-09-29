# Mettre à jour PolyWE

La routine se lance en **double-cliquant sur `Mettre-a-jour.cmd`** à la racine du projet. Elle utilise uv et propose quatre actions : ajouter, vérifier, prévisualiser, publier. Git et uv doivent être disponibles ; sur un nouveau poste, commencer par `uv sync --locked` et configurer son accès GitHub.

## Un nouveau cours ou document arrive

1. **Déposer le fichier dans le dossier de sa matière**, par exemple `RDM/` ou `Metallurgie/`. Un nouveau dossier est possible. Garder les images, CSS et scripts à proximité du HTML, selon ses liens relatifs.
2. Ouvrir `Mettre-a-jour.cmd`, puis **1 — Ajouter**. Coller le chemin du fichier : dans l’Explorateur, clic droit → Copier en tant que chemin. Les guillemets et les accents sont acceptés.
3. Choisir le cours déjà annoncé, ou créer un nouveau support. L’assistant propose les matières existantes et la création d’une matière. Les identifiants doivent rester stables ; les titres peuvent contenir des accents.
4. Si nécessaire, donner des mots-clés, les chemins des ressources associées et un sujet de planning. Rechercher ce dernier par un mot ou un code IWE, puis le sélectionner. Répéter pour plusieurs sujets ; Entrée termine la sélection. Un rattachement vaut pour toutes les séances de ce sujet, sans inventer une date de cours.
5. Confirmer l’enregistrement. L’assistant construit une copie de contrôle avant de modifier le catalogue : une erreur de lien ou de référence bloque l’ajout et conserve les métadonnées précédentes.
6. **3 — Aperçu** ouvre le site dans le navigateur. Vérifier la matière, le support et son accès depuis le planning. Arrêter l’aperçu avec Ctrl+C pour revenir au menu.
7. **4 — Publier** exécute les tests, construit le site, affiche les fichiers concernés et demande de taper `publier`. GitHub refait les contrôles, y compris les parcours navigateur, puis déploie automatiquement.

**Pour un cours déjà annoncé**, choisir l’entrée existante plutôt que créer un nouveau cours : son identifiant, son adresse et les liens déjà prévus dans la frise seront conservés. Les cours RDM 05 à 07 sont désormais intégrés.

Aucun support n’est enregistré au simple dépôt d’un fichier. L’enregistrement l’inscrit comme `disponible` pour la prochaine publication. Pour garder un brouillon, laisser le fichier non enregistré jusqu’à sa relecture ; si une annonce est souhaitée, utiliser une entrée `a_venir` dans le catalogue.

## Corriger un support déjà publié

Modifier son **fichier source existant**, puis ouvrir l’aperçu et publier. Il n’est pas nécessaire de refaire l’ajout ou de modifier le catalogue à chaque correction. La recherche et le sommaire sont reconstruits à partir du HTML actuel.

Garder les chemins `url` et les ancres déjà partagées. Le menu vérifie les liens internes mais ne connaît pas les anciens liens collés dans WhatsApp. Pour renommer un fichier source, utiliser l’ajout en ligne de commande avec son `--id` existant, puis traiter séparément le retrait Git de l’ancien fichier si nécessaire. Le renommage ne doit pas changer son URL publique.

## PDF et documents Office

Formats acceptés : `.pdf`, `.docx`, `.pptx`, `.xlsx`, en plus des cours `.html`.

L’ajout d’un document crée uniquement une petite page dans `Supports/<identifiant>.html`. Cette page apparaît dans la matière, la recherche et les sujets de planning choisis ; elle propose l’ouverture et le téléchargement du fichier original ainsi que le partage du lien. Le PDF ou document Office est déclaré dans `fichiers_associes` et reste intact. Son contenu intégral n’est pas indexé : renseigner un titre et des mots-clés utiles.

Pour une nouvelle version, remplacer le document **au même chemin** et publier. Ne pas relancer l’ajout : sa page et son lien de partage existent déjà. Les documents Office s’ouvrent dans l’application disponible sur l’appareil ; leur conversion en PDF n’est pas automatique.

Les PDF sources de `Planning/` conservent leur règle spécifique : locaux et ignorés par Git. La routine refuse de les enregistrer comme documents génériques ; leur publication demanderait une autorisation distincte.

## Les mêmes actions en terminal

Depuis la racine du projet :

```powershell
uv run python -m wiki gerer       # menu complet
uv run python -m wiki ajouter     # assistant d’ajout
uv run python -m wiki preparer    # tests, build et bilan
uv run python -m wiki apercu      # navigateur + serveur local ; Ctrl+C pour arrêter
uv run python -m wiki publier     # contrôles, confirmation, commit et push
```

L’option `apercu --port 8001` permet de changer de port si 8000 est occupé. L’aperçu doit être relancé après une modification.

Pour une intégration reproductible, l’ajout accepte aussi des paramètres. Exemples à adapter aux fichiers réellement présents :

```powershell
# Remplacer le fichier source d’un cours existant, en conservant ses métadonnées.
uv run python -m wiki ajouter "RDM/cours-05.html" --id rdm-05

# Nouveau document dans une matière existante.
uv run python -m wiki ajouter "RDM/fiche-synthese.pdf" --id rdm-fiche --matiere rdm --titre "Fiche de synthèse RDM" --mot-cle contraintes

# Rechercher l’identifiant d’un sujet pour ajouter --sujet IDENTIFIANT à l’ajout.
uv run python -m wiki sujets "rdm"

# Nouvelle matière et ressources explicitement déclarées.
uv run python -m wiki ajouter "Controles/ultrasons.html" --id cnd-01 --matiere controles --nouvelle-matiere "Contrôles non destructifs" --titre "Contrôle par ultrasons" --ressource "Controles/schema.svg"
```

`--sujet`, `--ressource` et `--mot-cle` peuvent être répétés. L’ajout par commande enregistre directement les paramètres fournis après validation ; il ne pousse rien sur GitHub. Les réglages avancés, prérequis, parcours et changements de séances restent éditables dans les deux JSON, décrits dans le README et [PLANNING.md](PLANNING.md).

## Vérifier la publication ou reprendre un incident

Le message « Envoyé sur GitHub » confirme le **push**, pas encore la mise en ligne. Ouvrir le lien [GitHub Actions](https://github.com/Pemcode/PolyWE/actions), attendre la réussite du workflow, puis consulter [le site](https://pemcode.github.io/PolyWE/). Une correction conserve les liens WhatsApp existants.

| Message ou situation | Que faire |
| --- | --- |
| Lien ou fichier introuvable | Corriger le chemin dans le HTML ou déclarer le fichier associé. Relancer l’ajout ; le catalogue n’a pas été modifié par l’échec. |
| Tests en échec | Lire le premier échec et corriger avant de relancer. Aucun commit n’a été créé. |
| Fichiers déjà dans l’index Git | Terminer ou désélectionner la sélection Git existante. La routine ne la modifie pas. |
| Modifications ou commits hors contenu | Les traiter via le circuit de développement habituel. La routine est réservée aux supports et aux deux JSON ; elle ne publie pas automatiquement du code. |
| GitHub contient des commits absents localement | Préserver ses modifications locales, puis synchroniser avec `git pull --ff-only`. Ne pas forcer le push. |
| Échec du push après le commit | Rétablir la connexion ou l’accès GitHub puis relancer Publier. Le commit local est réutilisé. |
| GitHub Actions en échec | Ouvrir le job en échec, corriger puis publier. Le dernier site déployé reste en ligne. |
| Aucune mise à jour à publier | Les contenus déclarés n’ont pas changé. Un fichier nouveau doit d’abord être enregistré. |

Les fichiers non déclarés ne sont jamais ajoutés par cette routine. Les modifications de code, tests et documentation suivent un commit de développement séparé. `_site/` reste généré et ignoré par Git ; GitHub Actions le reconstruit pour Pages.