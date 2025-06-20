import json
import random
import math
import argparse
import csv
import os


def load_exoplanets(input_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".csv":
        with open(input_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            exoplanets = list(reader)
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            exoplanets = json.load(f)
    return exoplanets


def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_csv(data, path):
    if not data:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def get_random_exoplanets(
    n=100,
    input_path="../data/cache/nasa_exoplanet_archive/nea_mock_complete.csv",
    output_path="../data/generated/random_exoplanets.json",
    output_format="json",
    input_format=None,
    filter_method=None,
    min_mass=None,
    max_mass=None,
    replace_nan=True,
):
    # Lire le fichier (json ou csv)
    exoplanets = load_exoplanets(input_path)

    # Filtrage optionnel
    if filter_method:
        exoplanets = [
            exo for exo in exoplanets if exo.get("disc_method") == filter_method
        ]
    if min_mass is not None:
        exoplanets = [
            exo
            for exo in exoplanets
            if exo.get("pl_mass") and float(exo["pl_mass"]) >= min_mass
        ]
    if max_mass is not None:
        exoplanets = [
            exo
            for exo in exoplanets
            if exo.get("pl_mass") and float(exo["pl_mass"]) <= max_mass
        ]

    # Sélectionner n exoplanètes aléatoires
    n = min(n, len(exoplanets))
    random_exoplanets = random.sample(exoplanets, n)

    # Remplacer les NaN et les champs vides par la chaîne "NaN"
    if replace_nan:
        for exoplanet in random_exoplanets:
            for key, value in exoplanet.items():
                if isinstance(value, float) and math.isnan(value) or value == "":
                    exoplanet[key] = "NaN"

    # Sauvegarder les exoplanètes sélectionnées dans le format choisi
    if output_format == "json":
        save_json(random_exoplanets, output_path)
    elif output_format == "csv":
        save_csv(random_exoplanets, output_path)
    else:
        print(json.dumps(random_exoplanets, indent=2, ensure_ascii=False))

    # Afficher un résumé
    print(f"Source: {input_path}")
    print(f"Total exoplanètes dans la source: {len(exoplanets)}")
    print(
        f"{n} exoplanètes aléatoires extraites et sauvegardées dans {output_path} (format: {output_format})"
    )
    if filter_method:
        print(f"Filtre méthode de découverte: {filter_method}")
    if min_mass is not None or max_mass is not None:
        print(f"Filtre masse: {min_mass} <= masse <= {max_mass}")


def main():
    parser = argparse.ArgumentParser(
        description="Sélectionne des exoplanètes aléatoires depuis un fichier CSV ou JSON et génère un CSV + un JSON."
    )
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Fichier source (CSV ou JSON)"
    )
    parser.add_argument(
        "-n", type=int, default=100, help="Nombre d'exoplanètes à sélectionner"
    )
    parser.add_argument(
        "--outdir", type=str, default="data/generated", help="Répertoire de sortie"
    )
    args = parser.parse_args()

    exoplanets = load_exoplanets(args.input)
    n = min(args.n, len(exoplanets))
    random_exoplanets = random.sample(exoplanets, n)

    # Remplacer les NaN et les champs vides par "NaN" (optionnel)
    for exoplanet in random_exoplanets:
        for key, value in exoplanet.items():
            if isinstance(value, float) and math.isnan(value) or value == "":
                exoplanet[key] = "NaN"

    # Générer les noms de fichiers avec le nombre d'exoplanètes
    json_path = os.path.join(args.outdir, f"random_exoplanets_{n}.json")
    csv_path = os.path.join(args.outdir, f"random_exoplanets_{n}.csv")

    save_json(random_exoplanets, json_path)
    save_csv(random_exoplanets, csv_path)

    print(f"{n} exoplanètes aléatoires extraites de {args.input}")
    print(f"JSON généré : {json_path}")
    print(f"CSV généré  : {csv_path}")


if __name__ == "__main__":
    main()
