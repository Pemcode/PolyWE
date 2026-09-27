import argparse
from pathlib import Path

from .build import build
from .catalogue import CatalogueError, load_catalogue


def main():
    parser = argparse.ArgumentParser(description="Construire le wiki IWE pour GitHub Pages")
    parser.add_argument("command", choices=["check", "build"])
    args = parser.parse_args()
    try:
        if args.command == "check":
            data = load_catalogue(Path.cwd())
            available = [c for c in data["cours"] if c["statut"] == "disponible"]
            print(f"Catalogue valide : {len(available)} cours disponibles, {sum(len(c['sections']) for c in available)} sections.")
        else:
            print(f"Site construit et liens contrôlés : {build(Path.cwd())}")
    except CatalogueError as exc:
        parser.exit(1, f"Erreur : {exc}\n")


if __name__ == "__main__":
    main()
