import json
from pathlib import Path

import pytest

HTML = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Préchauffage</title><style>.demo { color: red; }</style></head><body>
<h1>Préchauffage</h1><section id="intro"><h2>Comprendre le préchauffage</h2>
<p>Une explication.</p><a href="#calcul">Calcul</a></section>
<section id="calcul"><h2>Le t<sub>8/5</sub> en pratique</h2>
<input id="temperature" type="range"><p id="valeur"></p></section>
<script>document.getElementById('valeur').textContent = 'Animation active';</script>
</body></html>"""


@pytest.fixture
def project(tmp_path):
    (tmp_path / "Thermique").mkdir()
    (tmp_path / "Thermique" / "introduction.html").write_text(HTML, encoding="utf-8")
    data = {
        "version": 2,
        "matieres": [{"id": "thermique", "titre": "Thermique", "description": "Une nouvelle matière."}],
        "cours": [{"id": "th-01", "matiere": "thermique", "repere": "Cours 01", "ordre": 1,
                   "titre": "Préchauffage", "fichier": "Thermique/introduction.html",
                   "statut": "disponible", "mots_cles": ["ZAT", "HAZ"], "prerequis_conseilles": []}],
        "parcours": []
    }
    save_catalogue(tmp_path, data)
    return tmp_path, data


def save_catalogue(root, data):
    (root / "catalogue-cours.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def add_planning(project):
    root, catalogue = project
    (root / "Planning").mkdir()
    (root / "Planning/source.pdf").write_bytes(b"%PDF-1.4\nfixture")
    plan = {
        "version": 1, "phase_reference": "pre-rentree",
        "sources": [{"id": "source", "titre": "Planning source", "fichier": "Planning/source.pdf"}],
        "themes": [{"id": "thermique", "titre": "Thermique"}, {"id": "examens", "titre": "Examens"}],
        "phases": [
            {"id": "pre-rentree", "titre": "Pré-rentrée IWE1", "debut": "2026-09-23", "fin": "2026-10-02", "source": "source"},
            {"id": "formation", "titre": "Formation DU", "debut": "2026-10-05", "fin": "2027-02-26", "source": "source"}],
        "sujets": [
            {"id": "chauffer", "titre": "Traitements thermiques", "theme": "thermique", "code": "2.8", "supports": [{"cours": "th-01", "ancre": "calcul"}]},
            {"id": "sans-support", "titre": "Notion à documenter", "theme": "thermique", "supports": []},
            {"id": "examen", "titre": "Examen matériaux", "theme": "examens", "supports": []}],
        "seances": [
            {"id": "s1", "phase": "pre-rentree", "date": "2026-09-23", "sujet": "chauffer", "horaire": "08:00–12:30"},
            {"id": "s2", "phase": "pre-rentree", "date": "2026-09-28", "sujet": "chauffer", "horaire": "08:00–11:25"},
            {"id": "s3", "phase": "pre-rentree", "date": "2026-09-28", "sujet": "sans-support"},
            {"id": "s4", "phase": "formation", "date": "2027-01-12", "sujet": "examen", "horaire": "10:15–12:00"}]}
    (root / "planning-formation.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return root, catalogue, plan


@pytest.fixture
def planning_project(project):
    return add_planning(project)
