import os
from datetime import datetime
import csv
import argparse
from src.data_collectors.nasa_exoplanet import NASAExoplanetCollector
from src.data_collectors.exoplanet_eu import ExoplanetEUCollector
# Temporairement commenté
# from src.data_collectors.open_exoplanet import OpenExoplanetCollector
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
    # Configuration des arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Générateur d\'articles Wikipedia pour les exoplanètes')
    parser.add_argument('--use-mock-data', action='store_true', help='Utiliser les données mockées de la NASA')
    parser.add_argument('--sources', nargs='+', choices=['nasa', 'exoplanet_eu', 'open_exoplanet'],
                      default=['nasa', 'exoplanet_eu'],
                      help='Sources de données à utiliser (par défaut: nasa exoplanet_eu)')
    args = parser.parse_args()
    
    # Initialisation des collecteurs
    collectors = {}
    if 'nasa' in args.sources:
        collectors['nasa'] = NASAExoplanetCollector(use_mock_data=args.use_mock_data)
    if 'exoplanet_eu' in args.sources:
        collectors['exoplanet_eu'] = ExoplanetEUCollector("data/exoplanet_eu.csv")
    # Temporairement commenté
    # if 'open_exoplanet' in args.sources:
    #     collectors['open_exoplanet'] = OpenExoplanetCollector()
    
    # Initialisation du processeur de données
    processor = DataProcessor()
    
    # Collecte des données
    for source, collector in collectors.items():
        print(f"\nCollecte des données depuis {source}...")
        exoplanets = collector.fetch_data()
        processor.add_exoplanets(exoplanets, source)
    
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
    for year, count in sorted(stats['discovery_years'].items(), key=lambda x: str(x[0])):
        print(f"- {year} : {count}")
    
    # Vérification des articles Wikipédia
    print("\nVérification des exoplanètes sans article sur Wikipedia...")
    exoplanets_without_articles = processor.filter_exoplanets_without_articles()
    
    if exoplanets_without_articles:
        print(f"\nNombre d'exoplanètes sans article : {len(exoplanets_without_articles)}")
        
        # Création du fichier CSV pour les liens
        links_csv_path = f"{output_dir}/wikipedia_links_{timestamp}.csv"
        with open(links_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Exoplanète', 'Nom Article', 'Type', 'URL', 'Cible Redirection'])
            
            # Afficher les informations détaillées
            for exoplanet, article_info in exoplanets_without_articles:
                print(f"\nExoplanète : {exoplanet.name}")
                if article_info:
                    print("Articles existants :")
                    for name, info in article_info.items():
                        status = "redirection vers " + info.redirect_target if info.is_redirect else "article direct"
                        print(f"  - {name} : {status}")
                        if info.url:
                            print(f"    URL : {info.url}")
                        # Écrire dans le CSV
                        writer.writerow([
                            exoplanet.name,
                            name,
                            'Redirection' if info.is_redirect else 'Direct',
                            info.url,
                            info.redirect_target if info.is_redirect else ''
                        ])
                else:
                    print("Aucun article existant")
                    # Écrire dans le CSV même pour les exoplanètes sans article
                    writer.writerow([exoplanet.name, '', '', '', ''])
        
        print(f"\nInformations des liens exportées dans : {links_csv_path}")
        
        # Exporter les exoplanètes sans article
        processor.export_to_csv(f"{output_dir}/missing_articles_{timestamp}.csv", [e for e, _ in exoplanets_without_articles])
        
        # Génération des brouillons d'articles
        print("\nGénération des brouillons d'articles...")
        generator = WikipediaGenerator()
        for exoplanet, _ in exoplanets_without_articles:
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