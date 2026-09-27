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
