"""Parcours du contenu publié : les liens partagés restent utilisables."""
import json
import re
from pathlib import Path

from conftest import copy_real_project
from wiki.build import build
from wiki.catalogue import CourseHTML


RDM_04_URL = "RDM/04-directions-principales-mohr.html"


def test_rdm_04_is_reachable_from_subject_previous_course_search_and_route(tmp_path):
    # Construire le catalogue réel dans une copie, sans toucher aux sources locales.
    copy_real_project(tmp_path)
    output = build(tmp_path)
    assert (output / RDM_04_URL).is_file(), "Le cours RDM 04 doit être publié."

    def page(path):
        parsed = CourseHTML()
        parsed.feed((output / path).read_text(encoding="utf-8"))
        return parsed

    assert "../" + RDM_04_URL in page("matieres/rdm.html").links
    assert "04-directions-principales-mohr.html" in page("RDM/03-tenseur-deformations.html").links
    assert "03-tenseur-deformations.html" in page(RDM_04_URL).links
    assert "c4" in page(RDM_04_URL).ids
    assert "../" + RDM_04_URL + "#c4" in page("parcours/contraintes-residuelles.html").links
    index = json.loads((output / "assets/recherche.json").read_text(encoding="utf-8"))
    assert any(row["url"] == RDM_04_URL + "#c4" and "tricercle" in row["titre"].lower() for row in index)


def test_rdm_05_to_07_continue_series_and_are_reachable_from_planning(tmp_path):
    copy_real_project(tmp_path, planning=True)
    originals = {p.relative_to(tmp_path).as_posix(): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    output = build(tmp_path)
    urls = {
        "rdm-05": "RDM/05-hooke-criteres-resistance.html",
        "rdm-06": "RDM/06-torseur-cohesion.html",
        "rdm-07": "RDM/07-diagrammes-sollicitations.html",
    }
    for url in urls.values():
        assert (output / url).is_file(), f"Le nouveau cours doit être publié : {url}"

    def page(path):
        parsed = CourseHTML()
        parsed.feed((output / path).read_text(encoding="utf-8"))
        return parsed

    subject = page("matieres/rdm.html")
    sequence = [RDM_04_URL, *urls.values()]
    for first, second in zip(sequence, sequence[1:]):
        assert Path(second).name in page(first).links
        assert Path(first).name in page(second).links
    index = json.loads((output / "assets/recherche.json").read_text(encoding="utf-8"))
    for ident, url, word in (("rdm-05", urls["rdm-05"], "von Mises"),
                            ("rdm-06", urls["rdm-06"], "cohésion"),
                            ("rdm-07", urls["rdm-07"], "charges réparties")):
        assert "../" + url in subject.links
        assert url in page("planning.html").links
        assert any(row["cours_id"] == ident and row["type"] == "section" and word in row["titre"] for row in index)
    plan = json.loads((tmp_path / "planning-formation.json").read_text(encoding="utf-8"))
    topics = {t["id"]: t for t in plan["sujets"]}
    rdm = topics["3-2-notions-fondamentales-de-rdm"]["supports"]
    assert {"rdm-05", "rdm-06", "rdm-07"} <= {s["cours"] for s in rdm}
    assert {"cours": "rdm-05", "ancre": "c6"} in topics["3-8-fatigue"]["supports"]
    assert urls["rdm-05"] + "#c6" in page("planning.html").links
    assert urls["rdm-06"] + "#c2" in page("planning.html").links
    assert urls["rdm-07"] + "#c5" in page("planning.html").links
    assert all((tmp_path / name).read_bytes() == original for name, original in originals.items())


MOHR_FORGE = "RDM/mohr-forge/index.html"


def test_mohr_forge_is_published_with_rdm_without_taking_the_home_page(tmp_path):
    copy_real_project(tmp_path)
    output = build(tmp_path)
    game = output / "RDM/mohr-forge"
    for name in ("index.html", "assets/style.css", "js/scene3d.js", "js/story.js", "js/lab.js"):
        assert (game / name).is_file(), name
    assert not (game / "tests").exists() and not (game / "docs").exists() and not (output / "applications").exists()

    def page(path):
        parsed = CourseHTML()
        parsed.feed((output / path).read_text(encoding="utf-8"))
        return parsed

    assert "../" + MOHR_FORGE in page("matieres/rdm.html").links
    for url in ("RDM/02-tenseur-contraintes.html", "RDM/03-tenseur-deformations.html", RDM_04_URL, "RDM/05-hooke-criteres-resistance.html"):
        assert "mohr-forge/index.html" in page(url).links, url
    assert "mohr-forge/index.html" not in page("RDM/07-diagrammes-sollicitations.html").links
    assert not any("mohr-forge" in link for link in page("index.html").links)
    assert "../../matieres/rdm.html" in page(MOHR_FORGE).links
    index = json.loads((output / "assets/recherche.json").read_text(encoding="utf-8"))
    assert any(row["type"] == "application" and row["url"] == MOHR_FORGE and "Mohr" in row["mots_cles"] for row in index)


def test_rdm_08_is_reachable_and_preserves_the_interactive_source(tmp_path):
    data, _ = copy_real_project(tmp_path)
    output = build(tmp_path)
    url = "RDM/08-caracteristiques-sections.html"
    assert (output / url).is_file(), "Le cours RDM 08 doit être publié."

    def page(path):
        parsed = CourseHTML()
        parsed.feed((output / path).read_text(encoding="utf-8"))
        return parsed

    assert "../" + url in page("matieres/rdm.html").links
    assert Path(url).name in page("RDM/07-diagrammes-sollicitations.html").links
    published = page(url)
    for prerequisite in ("04-directions-principales-mohr.html", "06-torseur-cohesion.html", "07-diagrammes-sollicitations.html"):
        assert prerequisite in published.links
    assert "#c3" in published.links
    index = json.loads((output / "assets/recherche.json").read_text(encoding="utf-8"))
    assert any(row["url"] == url + "#c3" and "Huygens" in row["titre"] for row in index)

    source_path = next(c["fichier"] for c in data["cours"] if c["id"] == "rdm-08")
    source_bytes = (tmp_path / source_path).read_bytes()
    assert source_bytes == (Path(__file__).resolve().parents[1] / source_path).read_bytes()
    source = source_bytes.decode("utf-8")
    original = CourseHTML()
    original.feed(source)
    assert original.ids <= published.ids
    html = (output / url).read_text(encoding="utf-8")
    scripts = re.findall(r"<script\b[^>]*>.*?</script>", source, flags=re.S)
    assert scripts and all(script in html for script in scripts)


def test_relocated_sources_preserve_existing_bookmarks_and_scripts(tmp_path):
    data, _ = copy_real_project(tmp_path, planning=True)
    migrated_ids = {"met-base", "met-01", "met-02", "met-03"} | {f"rdm-{n:02}" for n in range(1, 9)}
    existing = [c for c in data["cours"] if c["id"] in migrated_ids and c["statut"] == "disponible"]
    originals = {c["id"]: (tmp_path / c["fichier"]).read_bytes() for c in existing}
    output = build(tmp_path)
    shared = ["Metallurgie/00-diagramme-plomb-etain.html", "Metallurgie/01-fer-carbone.html#s3",
              "Metallurgie/03-martensite-traitements-thermiques-soudage.html#s6",
              "RDM/04-directions-principales-mohr.html#c4", "RDM/08-caracteristiques-sections.html#c3"]
    index = json.loads((output / "assets/recherche.json").read_text(encoding="utf-8"))
    indexed = {row["url"] for row in index}
    for bookmark in shared:
        assert bookmark in indexed
        path, _, anchor = bookmark.partition("#")
        parser = CourseHTML()
        parser.feed((output / path).read_text(encoding="utf-8"))
        assert not anchor or anchor in parser.ids
    for course in existing:
        assert course["fichier"].startswith("Cours/")
        assert not (output / course["fichier"]).is_file()
        assert (tmp_path / course["fichier"]).read_bytes() == originals[course["id"]]
        published = (output / course["url"]).read_text(encoding="utf-8")
        scripts = re.findall(r"<script\b[^>]*>.*?</script>", originals[course["id"]].decode("utf-8-sig"), flags=re.S)
        assert scripts and all(script in published for script in scripts)
    assert (output / MOHR_FORGE).is_file()
    assert not (output / "Cours/RDM").exists()
    assert not (output / "Cours/Metallurgie").exists()


def test_fatigue_courses_are_reachable_from_subject_planning_and_search(tmp_path):
    data, plan = copy_real_project(tmp_path, planning=True)
    output = build(tmp_path)
    urls = ["Fatigue/01-cycles-chargement.html", "Fatigue/02-courbe-wohler.html", "Fatigue/03-amorcage-fissures.html"]
    assert (output / "matieres/fatigue.html").is_file(), "La matière fatigue doit être accessible."

    def page(path):
        parsed = CourseHTML()
        parsed.feed((output / path).read_text(encoding="utf-8"))
        return parsed

    assert "matieres/fatigue.html" in page("index.html").links
    for first, second in zip(urls, urls[1:]):
        assert Path(second).name in page(first).links
        assert Path(first).name in page(second).links
    courses = {c["id"]: c for c in data["cours"]}
    topic = next(t for t in plan["sujets"] if t["id"] == "3-8-fatigue")
    index = json.loads((output / "assets/recherche.json").read_text(encoding="utf-8"))
    for n, (url, anchor) in enumerate(zip(urls, ["c3", "c5", "c5"]), 1):
        ident = f"fatigue-{n:02}"
        assert "../" + url in page("matieres/fatigue.html").links
        assert url in page("planning.html").links
        assert {"cours": ident} in topic["supports"]
        assert any(row["cours_id"] == ident and row["type"] == "section" and row["url"] == url + "#" + anchor for row in index)
        course = courses[ident]
        source = (tmp_path / course["fichier"]).read_text(encoding="utf-8-sig")
        parsed = CourseHTML()
        parsed.feed(source)
        assert parsed.ids <= page(url).ids
        scripts = re.findall(r"<script\b[^>]*>.*?</script>", source, flags=re.S)
        published = (output / url).read_text(encoding="utf-8")
        assert scripts and all(script in published for script in scripts)
    assert "../RDM/04-directions-principales-mohr.html" in page(urls[2]).links
    assert "../RDM/05-hooke-criteres-resistance.html" in page(urls[2]).links
    assert urls[0] + "#c6" in page("planning.html").links
    assert urls[2] + "#c5" in page("planning.html").links