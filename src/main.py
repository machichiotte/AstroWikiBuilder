import os
from datetime import datetime
from src.data_collectors.nasa_exoplanet import NASAExoplanetCollector
from src.data_collectors.exoplanet_eu import ExoplanetEUCollector
from src.data_collectors.open_exoplanet import OpenExoplanetCollector
from src.utils.data_processor import DataProcessor
from src.utils.wikipedia_generator import WikipediaGenerator

def clean_filename(filename):
    # Liste des caractères invalides pour Windows
    invalid_chars = '<>:"/\\|?*\t\n\r'
    # Remplacer les caractères invalides par des underscores
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    # Supprimer les underscores consécutifs
    while '__' in filename:
        filename = filename.replace('__', '_')
    # Supprimer les underscores au début et à la fin
    filename = filename.strip('_')
    return filename

def main():
    # Initialisation des collecteurs
    #nasa_collector = NASAExoplanetCollector()
    exoplanet_eu_collector = ExoplanetEUCollector("data/exoplanet_eu.csv")
   # open_exoplanet_collector = OpenExoplanetCollector()
    
    # Initialisation du processeur de données
    processor = DataProcessor()
    
    # Collecte des données
  #  print("\nCollecte des données depuis la NASA Exoplanet Archive...")
   # nasa_exoplanets = nasa_collector.fetch_data()
    #processor.add_exoplanets(nasa_exoplanets, "nasa")
    
    print("\nCollecte des données depuis Exoplanet.eu...")
    exoplanet_eu_data = exoplanet_eu_collector.fetch_data()
    processor.add_exoplanets(exoplanet_eu_data, "exoplanet_eu")
    
  #  print("\nCollecte des données depuis Open Exoplanet Catalogue...")
   # open_exoplanet_data = open_exoplanet_collector.fetch_data()
   # processor.add_exoplanets(open_exoplanet_data, "open_exoplanet")
    
    # Génération des noms de fichiers avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"
    drafts_dir = "drafts"
    
    # Création des dossiers s'ils n'existent pas
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)
    
    # Export des données consolidées
    print("\nExport des données consolidées...")
    processor.export_to_csv(f"{output_dir}/exoplanets_{timestamp}.csv")
    processor.export_to_json(f"{output_dir}/exoplanets_{timestamp}.json")
    
    # Affichage des statistiques
    stats = processor.get_statistics()
    print("\nStatistiques des exoplanètes collectées :")
    print(f"Nombre total d'exoplanètes : {stats['total_exoplanets']}")
    print("\nPar source :")
    for source, count in stats['sources'].items():
        print(f"- {source} : {count}")
    print("\nPar méthode de découverte :")
    for method, count in stats['discovery_methods'].items():
        print(f"- {method} : {count}")
    print("\nPar année de découverte :")
    for year, count in sorted(stats['discovery_years'].items()):
        print(f"- {year} : {count}")
    
    # Vérification des articles Wikipédia
    print("\nVérification des exoplanètes sans article sur Wikipedia...")
    exoplanets_without_articles = processor.filter_exoplanets_without_articles()
    
    if exoplanets_without_articles:
        print(f"\nNombre d'exoplanètes sans article : {len(exoplanets_without_articles)}")
        processor.export_to_csv(f"{output_dir}/missing_articles_{timestamp}.csv", exoplanets_without_articles)
        
        # Génération des brouillons d'articles
        print("\nGénération des brouillons d'articles...")
        generator = WikipediaGenerator()
        for exoplanet in exoplanets_without_articles:
            content = generator.generate_article_content(exoplanet)
            safe_filename = clean_filename(exoplanet.name.replace(' ', '_'))
            filename = f"{drafts_dir}/{safe_filename}.wiki"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Brouillon généré pour {exoplanet.name}")
    else:
        print("\nToutes les exoplanètes ont déjà un article sur Wikipedia.")

if __name__ == "__main__":
    main() 