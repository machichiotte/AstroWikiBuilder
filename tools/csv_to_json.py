import pandas as pd
import json
import math
from pathlib import Path

def convert_csv_to_json(csv_path: str, json_path: str):
    """
    Convertit un fichier CSV en JSON
    """
    print(f"Lecture du fichier CSV : {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Fonction pour supprimer les clés avec valeur None ou NaN
    def drop_none_and_nan(d):
        return {k: v for k, v in d.items() if v is not None and not (isinstance(v, float) and math.isnan(v))}

    print(f"Conversion en JSON...")
    json_data = [drop_none_and_nan(record) for record in df.to_dict(orient='records')]

    print(f"Écriture du fichier JSON : {json_path}")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print("Conversion terminée !")

def convert_csv_column_to_json(csv_path: str, json_path: str, column: str):
    """
    Convertit une seule colonne d'un fichier CSV en JSON (liste des valeurs non nulles/non NaN).
    """
    print(f"Lecture du fichier CSV : {csv_path}")
    df = pd.read_csv(csv_path)

    if column not in df.columns:
        print(f"Colonne '{column}' non trouvée dans le CSV.")
        return

    # Récupère la colonne, enlève les NaN/None, convertit en liste
    values = df[column].dropna().tolist()

    print(f"Écriture du fichier JSON : {json_path}")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(values, f, indent=2, ensure_ascii=False)

    print("Conversion terminée (colonne unique) !")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        csv_path = sys.argv[1]
        json_path = sys.argv[2]
        convert_csv_to_json(csv_path, json_path)
    elif len(sys.argv) == 4:
        csv_path = sys.argv[1]
        json_path = sys.argv[2]
        column = sys.argv[3]
        convert_csv_column_to_json(csv_path, json_path, column)
    else:
        print("Usage:")
        print("  python csv_to_json.py <input_csv> <output_json>")
        print("  python csv_to_json.py <input_csv> <output_json> <column_name>")
        sys.exit(1)