"""Construction d'un site statique à partir des seuls contenus déclarés."""
import json
import posixpath
import re
import shutil
from html import escape as h
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from .catalogue import CatalogueError, CourseHTML, load_catalogue
from .planning import load_planning, render_planning

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MARKER = "wiki-iwe-generated\n"


def link(current, target, anchor=""):
    relative = posixpath.relpath(target, posixpath.dirname(current) or ".")
    return quote(relative, safe="/-._~") + ("#" + quote(anchor, safe="-._~") if anchor else "")


def write(output, name, text):
    target = output / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def shell(current, title, body, has_planning=False, extra_head=""):
    planning_nav = f'<a href="{link(current, "planning.html")}">Planning</a>' if has_planning else ""
    css = link(current, "assets/wiki.css")
    js = link(current, "assets/wiki.js")
    home = link(current, "index.html")
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h(title)} · Révisions IWE</title>
<meta name="description" content="Cours interactifs et parcours de révision de la promo DU Ingénierie du soudage / IWE.">
<meta property="og:title" content="{h(title)} · Révisions IWE"><meta property="og:type" content="website">
<link rel="stylesheet" href="{css}"><script id="wiki-runtime" defer src="{js}"></script>{extra_head}</head>
<body class="wiki-shell"><a class="wiki-skip" href="#contenu">Aller au contenu</a>
<header class="wiki-top"><a class="wiki-brand" href="{home}"><span class="wiki-mark" aria-hidden="true">W</span> Révisions IWE</a>
<nav aria-label="Navigation principale">{planning_nav}<a href="{home}#matieres">Matières</a><a href="{home}#rechercher">Rechercher</a><a href="{home}#parcours">Parcours</a></nav></header>
<main id="contenu" class="wiki-main">{body}</main>
<footer class="wiki-bottom">Supports de révision de la promo · DU Ingénierie du soudage · Polytech Nantes<br>Un complément aux cours et aux TD de la formation.</footer></body></html>"""


def course_card(course, current):
    title = h(course["titre"])
    repere = h(course.get("repere", "Cours"))
    if course["statut"] == "a_venir":
        return f'<article class="wiki-card wiki-planned"><span class="wiki-eyebrow">{repere}</span><h3>{title}</h3><p class="wiki-tag">À venir</p></article>'
    url = link(current, course["url"])
    tags = " · ".join(course["ressources"])
    return f'<article class="wiki-card"><span class="wiki-eyebrow">{repere}</span><h3><a href="{url}">{title}</a></h3><p>{h(tags)}</p><span class="wiki-card-end">{len(course["sections"])} sections <span aria-hidden="true">↗</span></span></article>'


def app_card(app, current):
    title = h(app["titre"])
    genre = h(app.get("genre", "Application interactive"))
    description = f'<p>{h(app["description"])}</p>' if app.get("description") else ""
    if app["statut"] == "a_venir":
        return f'<article class="wiki-card wiki-app-card wiki-planned"><span class="wiki-eyebrow">{genre}</span><h3>{title}</h3>{description}<p class="wiki-tag">À venir</p></article>'
    tags = " · ".join(app["ressources"])
    return f'<article class="wiki-card wiki-app-card"><span class="wiki-eyebrow">{genre}</span><h3><a href="{link(current, app["url"])}">{title}</a></h3>{description}<span class="wiki-card-end">{h(tags)} <span aria-hidden="true">↗</span></span></article>'


def app_page(app, subject):
    """Copie publiée d'une application : barre du wiki ajoutée, source et routes internes intactes."""
    current = app["url"]
    head = (f'<link rel="stylesheet" href="{link(current, "assets/wiki.css")}"><script id="wiki-runtime" defer src="{link(current, "assets/wiki.js")}"></script>'
            f'<meta name="wiki-application" content="{h(app["id"])}"><meta name="wiki-course-title" content="{h(app["titre"])}">')
    nav = f"""<nav class="wiki-nav wiki-app-nav" aria-label="Navigation du wiki"><div class="wiki-nav-inner">
<div class="wiki-crumbs"><a href="{link(current, "index.html")}">Révisions IWE</a><span aria-hidden="true">/</span><a href="{link(current, f"matieres/{subject['id']}.html")}">{h(subject['titre'])}</a><span aria-current="page">{h(app['titre'])}</span></div>
<div class="wiki-actions"><button type="button" data-wiki-share="native">Partager</button><button type="button" data-wiki-share="copy">Copier le lien</button><span class="wiki-status" role="status" id="wiki-share-status"></span></div>
<label class="wiki-copy-fallback" hidden>Lien à copier<input readonly aria-label="Lien à copier"></label></div></nav>"""
    html = re.sub(r"</head\s*>", lambda _: head + '\n</head>', app["_source"], count=1, flags=re.I)
    return re.sub(r"(<body\b[^>]*>)", lambda m: m.group(1) + '\n' + nav, html, count=1, flags=re.I)


def validate_site(output):
    output = Path(output).resolve()
    pages = {}
    for path in output.rglob("*.html"):
        parser = CourseHTML()
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = parser
    checked = 0
    for path, parser in pages.items():
        for raw in parser.links:
            url = urlsplit(raw)
            if url.scheme or url.netloc:
                continue
            if url.path.startswith("/"):
                raise CatalogueError(f"lien incompatible avec un sous-chemin Pages : {path.name} → {raw}")
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target = target / "index.html"
            if not target.is_relative_to(output) or not target.is_file():
                raise CatalogueError(f"lien local introuvable : {path.name} → {raw}")
            # Dans une application, #laboratoire ou #histoire/2 sont des routes internes, pas des sections.
            routed = target in pages and "wiki-application" in pages[target].meta
            if url.fragment and target in pages and not routed and unquote(url.fragment) not in pages[target].ids:
                raise CatalogueError(f"lien vers une ancre absente : {path.name} → {raw}")
            checked += 1
    return checked


def build(root):
    root = Path(root).resolve()
    data = load_catalogue(root)
    plan = load_planning(root, data)
    output = root / "_site"
    # Ne nettoyer que notre sortie marquée, jamais un lien/jonction ou un dossier arbitraire.
    if output.is_symlink() or output.is_junction() or output.resolve() != root / "_site":
        raise CatalogueError("dossier de sortie non autorisé")
    if output.exists():
        marker = output / ".wiki-generated"
        if not marker.is_file() or marker.read_text(encoding="utf-8") != MARKER:
            raise CatalogueError("dossier de sortie existant sans marqueur du générateur")
        entries = list(output.rglob("*"))
        if any(p.is_symlink() or p.is_junction() or not p.resolve().is_relative_to(output) for p in entries):
            raise CatalogueError("lien ou jonction interdite dans la sortie")
        # OneDrive peut marquer les dossiers en lecture seule. Conserver les
        # répertoires et le marqueur ; retirer uniquement les fichiers générés.
        for entry in entries:
            if entry.is_file() and entry != marker:
                entry.unlink()
    output.mkdir(exist_ok=True)
    write(output, ".wiki-generated", MARKER)
    write(output, ".nojekyll", "")
    for asset in ("wiki.css", "wiki.js") + (("planning.css", "planning.js") if plan else ()):
        write(output, "assets/" + asset, (ASSETS / asset).read_text(encoding="utf-8"))
    courses = sorted((c for c in data["cours"] if c["statut"] != "brouillon"), key=lambda c: (c["ordre"], c["id"]))
    available = [c for c in courses if c["statut"] == "disponible"]
    by_id = {c["id"]: c for c in courses}
    # Les applications complètent une matière ; l'accueil reste organisé par matières.
    apps = sorted((a for a in data["applications"] if a["statut"] != "brouillon"), key=lambda a: (a["ordre"], a["id"]))
    live_apps = [a for a in apps if a["statut"] == "disponible"]
    subjects = [s for s in data["matieres"] if any(item["matiere"] == s["id"] for item in [*courses, *apps])]
    subject_by_id = {s["id"]: s for s in subjects}
    subject_cards = []
    for subject in subjects:
        grouped = [c for c in courses if c["matiere"] == subject["id"]]
        count = sum(c["statut"] == "disponible" for c in grouped)
        current = f"matieres/{subject['id']}.html"
        cards = "".join(course_card(c, current) for c in grouped)
        subject_apps = [a for a in apps if a["matiere"] == subject["id"]]
        training = f'<section class="wiki-training" aria-labelledby="s-entrainer"><div class="wiki-section-title"><h2 id="s-entrainer">S’entraîner</h2><span>Jeux et applications interactives</span></div><div class="wiki-grid">{"".join(app_card(a, current) for a in subject_apps)}</div></section>' if subject_apps else ""
        body = f'<p class="wiki-eyebrow">Matière · {count} cours disponibles</p><h1>{h(subject["titre"])}</h1><p class="wiki-lead">{h(subject.get("description", ""))}</p><div class="wiki-grid">{cards}</div>{training}'
        write(output, current, shell(current, subject["titre"], body, has_planning=bool(plan)))
        playable = sum(a["statut"] == "disponible" for a in subject_apps)
        mention = f" · {playable} application{'s' if playable > 1 else ''}" if playable else ""
        subject_cards.append(f'<a class="wiki-subject" href="{current}"><span class="wiki-eyebrow">{count} cours disponibles{mention}</span><h3>{h(subject["titre"])}</h3><p>{h(subject.get("description", ""))}</p><span aria-hidden="true">Explorer →</span></a>')
    route_cards = []
    for route in data["parcours"]:
        current = f"parcours/{route['id']}.html"
        steps = []
        for step in route["etapes"]:
            course = by_id[step["cours"]]
            label = next((s["titre"] for s in course["sections"] if s["ancre"] == step["ancre"]), course["titre"])
            href = link(current, course["url"], step["ancre"])
            steps.append(f'<li><a href="{href}">{h(label)}</a><p>{h(subject_by_id[course["matiere"]]["titre"])} · {h(course.get("repere", ""))}</p></li>')
        body = f'<p class="wiki-eyebrow">Applications au soudage · {len(steps)} étapes</p><h1>{h(route["titre"])}</h1><p class="wiki-lead">{h(route.get("description", ""))}</p><ol class="wiki-steps">{"".join(steps)}</ol>'
        write(output, current, shell(current, route["titre"], body, has_planning=bool(plan)))
        route_cards.append(f'<article class="wiki-card"><span class="wiki-eyebrow">{len(steps)} étapes</span><h3><a href="{current}">{h(route["titre"])}</a></h3><p>{h(route.get("description", ""))}</p></article>')
    options = ''.join(f'<option value="{s["id"]}">{h(s["titre"])}</option>' for s in subjects)
    planning_teaser = '<a class="wiki-planning-teaser" href="planning.html"><span><strong>Suivre le fil de la formation</strong><small>Pré-rentrée, semaines de cours et examens : les supports au bon moment.</small></span><span aria-hidden="true">Explorer le planning →</span></a>' if plan else ""
    total_sections = sum(len(c["sections"]) for c in available)
    body = f"""<section class="wiki-hero"><p class="wiki-eyebrow">Polytech Nantes · DU Ingénierie du soudage</p>
<h1>Comprendre.<br>Relier. <em>Réviser.</em></h1>
<p class="wiki-lead">Les cours interactifs de la promo, réunis pour préparer l’IWE. Suivez une matière ou retrouvez directement la notion qui vous intéresse.</p>
<p class="wiki-stats"><strong>{len(available)}</strong> cours <span> / </span><strong>{len(subjects)}</strong> matières <span> / </span><strong>{total_sections}</strong> sections</p></section>
{planning_teaser}<section id="rechercher" class="wiki-search"><h2>Une notion en tête ?</h2><form id="wiki-search-form" role="search">
<label for="wiki-query">Rechercher une notion, un cours ou une section</label><div class="wiki-search-row"><input id="wiki-query" type="search" placeholder="Préchauffage, Mohr, règle du levier…" autocomplete="off">
<label class="wiki-sr" for="wiki-subject-filter">Filtrer par matière</label><select id="wiki-subject-filter"><option value="">Toutes les matières</option>{options}</select><button type="submit">Rechercher</button></div></form>
<p id="wiki-search-status" role="status">Explorez les matières ci-dessous ou recherchez un sujet précis.</p><ul id="wiki-results" class="wiki-results"></ul><noscript>La recherche nécessite JavaScript. Les matières et les cours restent accessibles ci-dessous.</noscript></section>
<section id="matieres"><div class="wiki-section-title"><h2>Avancer par matière</h2><span>Les bases, dans l’ordre</span></div><div class="wiki-grid">{''.join(subject_cards)}</div></section>
<section id="parcours"><div class="wiki-section-title"><h2>Faire le lien avec le soudage</h2><span>Des parcours entre les cours</span></div><div class="wiki-grid">{''.join(route_cards)}</div></section>"""
    write(output, "index.html", shell("index.html", "Accueil", body, has_planning=bool(plan)))
    if plan:
        for source in plan['sources']:
            if not source.get('publier', False):
                continue
            target = output / source['fichier']
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / source['fichier'], target)
        extra = '<link rel="stylesheet" href="assets/planning.css"><script defer src="assets/planning.js"></script>'
        write(output, 'planning.html', shell('planning.html', 'Planning de formation', render_planning(plan, data, link), has_planning=True, extra_head=extra))
    search_rows = []
    for course in available:
        current = course["url"]
        subject = subject_by_id[course["matiere"]]
        siblings = [c for c in available if c["matiere"] == course["matiere"]]
        position = siblings.index(course)
        previous_next = []
        for index, label in ((position-1, "← Cours précédent"), (position+1, "Cours suivant →")):
            if 0 <= index < len(siblings):
                other = siblings[index]
                previous_next.append(f'<a href="{link(current, other["url"])}">{label} : {h(other["titre"])}</a>')
        prerequisites = []
        for ident in course["prerequis_conseilles"]:
            prerequisite = by_id.get(ident)
            if prerequisite and prerequisite["statut"] == "disponible":
                prerequisites.append(f'<a href="{link(current, prerequisite["url"])}">{h(prerequisite["titre"])}</a>')
        home = link(current, "index.html")
        subject_url = link(current, f"matieres/{subject['id']}.html")
        section_links = ''.join(f'<li><a href="#{quote(s["ancre"])}">{h(s["titre"])}</a></li>' for s in course["sections"])
        planning_link = f'<a class="wiki-planning-link" href="{link(current, "planning.html")}">Planning</a>' if plan else ""
        nav = f"""<nav class="wiki-nav" aria-label="Navigation du wiki"><div class="wiki-nav-inner">
<div class="wiki-crumbs"><a href="{home}">Révisions IWE</a><span aria-hidden="true">/</span><a href="{subject_url}">{h(subject['titre'])}</a><span aria-current="page">{h(course.get('repere', 'Cours'))}</span></div>
<details class="wiki-course-menu"><summary>Sommaire du cours</summary><ol>{section_links}</ol></details>
{planning_link}<div class="wiki-actions"><button type="button" data-wiki-share="native">Partager</button><button type="button" data-wiki-share="copy">Copier le lien</button><span class="wiki-status" role="status" id="wiki-share-status"></span></div>
<label class="wiki-copy-fallback" hidden>Lien à copier<input readonly aria-label="Lien à copier"></label></div></nav>"""
        footer = '<footer class="wiki-course-footer">'
        if prerequisites:
            footer += '<p>Prérequis conseillés : ' + ' · '.join(prerequisites) + '</p>'
        related = [a for a in live_apps if course["id"] in a["cours_lies"]]
        if related:
            footer += '<p class="wiki-training-link">S’entraîner : ' + ' · '.join(f'<a href="{link(current, a["url"])}">{h(a["titre"])}</a> <span>({h(a.get("genre", "Application interactive")).lower()})</span>' for a in related) + '</p>'
        footer += '<nav aria-label="Cours voisins">' + ''.join(previous_next) + '</nav></footer>'
        head = f'<link rel="stylesheet" href="{link(current, "assets/wiki.css")}"><script id="wiki-runtime" defer src="{link(current, "assets/wiki.js")}"></script><meta property="og:title" content="{h(course["titre"])}"><meta name="wiki-course-title" content="{h(course["titre"])}">'
        html = re.sub(r"<title\b[^>]*>.*?</title>", lambda _: '<title>'+h(subject['titre']+' — '+course.get('repere','Cours')+' — '+course['titre'])+'</title>', course["_source"], count=1, flags=re.I | re.S)
        html = re.sub(r"</head\s*>", lambda _: head+'\n</head>', html, count=1, flags=re.I)
        html = re.sub(r"(<body\b[^>]*>)", lambda m: m.group(1)+'\n'+nav, html, count=1, flags=re.I)
        html = re.sub(r"</body\s*>", lambda _: footer+'\n</body>', html, count=1, flags=re.I)
        write(output, current, html)
        for asset in course['fichiers_associes']:
            dest = output / asset
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / asset, dest)
        common = {'cours_id': course['id'], 'cours': course['titre'], 'matiere': subject['id'], 'matiere_titre': subject['titre'], 'mots_cles': course['mots_cles'], 'ressources': course['ressources']}
        search_rows.append({**common, 'titre': course['titre'], 'url': link('index.html', current), 'type': 'cours'})
        for section in course['sections']:
            search_rows.append({**common, 'titre': section['titre'], 'url': link('index.html', current, section['ancre']), 'type': 'section'})
    for app in live_apps:
        subject = subject_by_id[app["matiere"]]
        for source, target in app["_files"]:
            if target != app["url"]:
                (output / target).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / source, output / target)
        write(output, app["url"], app_page(app, subject))
        search_rows.append({'cours_id': app['id'], 'cours': app['titre'], 'matiere': subject['id'], 'matiere_titre': subject['titre'],
                            'mots_cles': app['mots_cles'], 'ressources': app['ressources'], 'titre': app['titre'],
                            'url': link('index.html', app['url']), 'type': 'application'})
    write(output, 'assets/recherche.json', json.dumps(search_rows, ensure_ascii=False, indent=2)+'\n')
    validate_site(output)
    return output
