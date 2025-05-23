import json
import random
import math

def get_random_exoplanets(n=12):
    # Lire le fichier JSON complet
    with open('data/nasa_mock_data_complete.json', 'r') as f:
        exoplanets = json.load(f)
    
    # Sélectionner n exoplanètes aléatoires
    random_exoplanets = random.sample(exoplanets, n)
    
    # Remplacer les NaN et les champs vides par la chaîne "NaN"
    for exoplanet in random_exoplanets:
        for key, value in exoplanet.items():
            if isinstance(value, float) and math.isnan(value) or value == "":
                exoplanet[key] = "NaN"
    
    # Sauvegarder les exoplanètes sélectionnées dans un nouveau fichier
    with open('data/random_exoplanets.json', 'w') as f:
        json.dump(random_exoplanets, f, indent=2)
    
    print(f"{n} exoplanètes aléatoires ont été extraites et sauvegardées dans data/random_exoplanets.json")

if __name__ == "__main__":
    get_random_exoplanets() 