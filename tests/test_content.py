"""Parcours du contenu publié : les liens partagés restent utilisables."""
import json
from pathlib import Path
import shutil

from wiki.build import build
from wiki.catalogue import CourseHTML


REPOSITORY = Path(__file__).resolve().parents[1]
RDM_04_URL = "RDM/04-directions-principales-mohr.html"


def test_rdm_04_is_reachable_from_subject_previous_course_search_and_route(tmp_path):
    # Construire le catalogue réel dans une copie, sans toucher aux sources locales.
    catalogue = REPOSITORY / "catalogue-cours.json"
    shutil.copyfile(catalogue, tmp_path / catalogue.name)
    data = json.loads(catalogue.read_text(encoding="utf-8"))
    for course in data["cours"]:
        if course["statut"] != "disponible":
            continue
        for source in [course["fichier"], *course.get("fichiers_associes", [])]:
            target = tmp_path / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPOSITORY / source, target)
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
    catalogue = REPOSITORY / "catalogue-cours.json"
    shutil.copyfile(catalogue, tmp_path / catalogue.name)
    shutil.copyfile(REPOSITORY / "planning-formation.json", tmp_path / "planning-formation.json")
    data = json.loads(catalogue.read_text(encoding="utf-8"))
    originals = {}
    for course in data["cours"]:
        if course["statut"] != "disponible":
            continue
        for source in [course["fichier"], *course.get("fichiers_associes", [])]:
            target = tmp_path / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPOSITORY / source, target)
            originals[source] = target.read_bytes()
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