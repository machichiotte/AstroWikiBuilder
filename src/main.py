# src/main.py
import os
from datetime import datetime
import csv
import argparse
from src.data_collectors.nasa_exoplanet import NASAExoplanetCollector
from src.data_collectors.exoplanet_eu import ExoplanetEUCollector
from src.models.exoplanet import Exoplanet
# Temporairement commenté
# from src.data_collectors.open_exoplanet import OpenExoplanetCollector
from src.utils.data_processor import DataProcessor
from src.utils.wikipedia_generator import WikipediaGenerator
import json
from typing import List, Tuple

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
    #if 'exoplanet_eu' in args.sources:
    #    collectors['exoplanet_eu'] = ExoplanetEUCollector("data/exoplanet_eu.csv")
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
    os.makedirs(f"{drafts_dir}/missing", exist_ok=True)
    os.makedirs(f"{drafts_dir}/existing", exist_ok=True)
    
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
    print("\nVérification des articles Wikipedia...")
    print("Début de la séparation des articles...")
    existing_articles, missing_articles = processor.separate_articles_by_status()
    print("Séparation des articles terminée.")
    
    # Création des fichiers pour les articles existants
    existing_csv_path = f"{output_dir}/existing_wikipedia_links_{timestamp}.csv"
    existing_json_path = f"{output_dir}/existing_wikipedia_links_{timestamp}.json"
    
    # Formatage et écriture des données des articles existants
    print("Formatage des données des articles existants...")
    existing_json_data, existing_csv_data = processor.format_wiki_links_data(existing_articles)
    print("Formatage des données des articles existants terminé.")
    
    # Écriture du CSV des articles existants
    print("\nÉcriture du CSV des articles existants...")
    with open(existing_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Exoplanète', 'Nom Article', 'Type', 'URL', 'Cible Redirection', 'Étoile Hôte'])
        writer.writerows(existing_csv_data)
    print("Écriture du CSV des articles existants terminée.")
    
    # Écriture du JSON des articles existants
    print("Écriture du JSON des articles existants...")
    with open(existing_json_path, 'w', encoding='utf-8') as f:
        json.dump(existing_json_data, f, ensure_ascii=False, indent=2)
    print("Écriture du JSON des articles existants terminée.")
    
    print("\nInformations des articles existants exportées dans :")
    print(f"- CSV : {existing_csv_path}")
    print(f"- JSON : {existing_json_path}")
    
    # Création des fichiers pour les articles manquants
    missing_csv_path = f"{output_dir}/missing_wikipedia_links_{timestamp}.csv"
    missing_json_path = f"{output_dir}/missing_wikipedia_links_{timestamp}.json"
    
    # Formatage et écriture des données des articles manquants
    print("Formatage des données des articles manquants...")
    missing_json_data, missing_csv_data = processor.format_wiki_links_data(missing_articles)
    print("Formatage des données des articles manquants terminé.")
    
    # Écriture du CSV des articles manquants
    print("\nÉcriture du CSV des articles manquants...")
    with open(missing_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Exoplanète', 'Nom Article'])
        writer.writerows(missing_csv_data)
    print("Écriture du CSV des articles manquants terminée.")
    
    # Écriture du JSON des articles manquants
    print("Écriture du JSON des articles manquants...")
    with open(missing_json_path, 'w', encoding='utf-8') as f:
        json.dump(missing_json_data, f, ensure_ascii=False, indent=2)
    print("Écriture du JSON des articles manquants terminée.")
    
    print("\nInformations des articles manquants exportées dans :")
    print(f"- CSV : {missing_csv_path}")
    print(f"- JSON : {missing_json_path}")
    
    if missing_articles:
        print(f"\nNombre d'exoplanètes sans article : {len(missing_articles)}")
        
        # Exporter les exoplanètes sans article (données complètes)
        processor.export_to_csv(f"{output_dir}/missing_wikipedia_links_{timestamp}.csv", [e for e, _ in missing_articles])
        processor.export_to_json(f"{output_dir}/missing_wikipedia_links_{timestamp}.json", [e for e, _ in missing_articles])
        
        # Générer les brouillons pour les articles manquants
        missing_drafts = []
        for exoplanet in exoplanets:
            if not any(e.name == exoplanet.name for e, _ in existing_articles):
                draft = generate_draft(exoplanet)
                missing_drafts.append((exoplanet.name, draft))
        
        # Générer les brouillons pour les articles existants
        existing_drafts = []
        for exoplanet in exoplanets:
            if any(e.name == exoplanet.name for e, _ in existing_articles):
                draft = generate_draft(exoplanet)
                existing_drafts.append((exoplanet.name, draft))
        
        # Afficher le bilan
        print("\nBilan de la génération des brouillons :")
        print(f"- {len(missing_drafts)} brouillons générés pour les articles manquants")
        print(f"- {len(existing_drafts)} brouillons générés pour les articles existants")
        print(f"- Total : {len(missing_drafts) + len(existing_drafts)} brouillons")
        
        # Sauvegarder les brouillons
        save_drafts(missing_drafts, existing_drafts)
    else:
        print("\nToutes les exoplanètes ont déjà un article sur Wikipedia.")

def generate_draft(exoplanet: Exoplanet) -> str:
    """
    Génère le contenu d'un brouillon d'article pour une exoplanète.
    
    Args:
        exoplanet: L'exoplanète pour laquelle générer le brouillon
        
    Returns:
        str: Le contenu du brouillon
    """
    generator = WikipediaGenerator()
    return generator.generate_article_content(exoplanet)

def save_drafts(missing_drafts: List[Tuple[str, str]], existing_drafts: List[Tuple[str, str]], drafts_dir: str = "drafts") -> None:
    """
    Sauvegarde les brouillons dans les fichiers appropriés.
    
    Args:
        missing_drafts: Liste des brouillons pour les articles manquants
        existing_drafts: Liste des brouillons pour les articles existants
        drafts_dir: Répertoire de sauvegarde des brouillons
    """
    # Créer les répertoires si nécessaire
    os.makedirs(f"{drafts_dir}/missing", exist_ok=True)
    os.makedirs(f"{drafts_dir}/existing", exist_ok=True)
    
    # Sauvegarder les brouillons manquants
    for name, content in missing_drafts:
        safe_filename = clean_filename(name.replace(' ', '_'))
        filename = f"{drafts_dir}/missing/{safe_filename}.wiki"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Sauvegarder les brouillons existants
    for name, content in existing_drafts:
        safe_filename = clean_filename(name.replace(' ', '_'))
        filename = f"{drafts_dir}/existing/{safe_filename}.wiki"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    main() 