import pandas as pd
import json
from pathlib import Path

def convert_csv_to_json(csv_path: str, json_path: str):
    """
    Convertit un fichier CSV en JSON
    """
    print(f"Lecture du fichier CSV : {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"Conversion en JSON...")
    json_data = df.to_dict(orient='records')
    
    print(f"Écriture du fichier JSON : {json_path}")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print("Conversion terminée !")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python csv_to_json.py <input_csv> <output_json>")
        sys.exit(1)
    csv_path = sys.argv[1]
    json_path = sys.argv[2]
    convert_csv_to_json(csv_path, json_path) 