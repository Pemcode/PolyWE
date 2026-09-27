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

## S01 — Catalogue extensible

En tant que mainteneur, j'ajoute un cours ou une matière en modifiant les données et en déposant le HTML, sans modifier le générateur.

- Identifiants uniques et stables ; matières déclarées ; prérequis référencés valides.
- Un cours disponible nécessite un fichier HTML existant situé dans le projet.
- Un cours à venir peut ne pas avoir de fichier et ne produit pas de lien. Un brouillon n'est pas publié.
- Les sections et leurs titres proviennent du HTML actuel, pas d'une liste entretenue à la main.
- Rejet d'un chemin sortant du projet, d'un fichier partagé par deux cours ou d'une ressource manquante.
- Une matière fictive dans les tests prouve l'absence de liste codée en dur.

Preuve TDD du 27 septembre 2026 : RED à l'import du module absent, puis GREEN (15 tests). Deux cas ajoutés pour séparer fichier source et URL publiée : RED sur le chemin publié sortant du projet, puis GREEN (17 tests de catalogue). Une erreur de données dans le test d'état à venir (identifiant avec underscore) a été corrigée pour respecter le contrat d'identifiants.

Les 63 sections des sept cours réels sont extraites du HTML. Le catalogue compte neuf entrées, dont deux à venir.

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
