# src/main.py
import os
from datetime import datetime
import csv
import argparse
import json
from typing import List, Tuple, Dict, Any # Added Dict, Any
import logging # Added logging

# Project imports
from src.data_collectors.nasa_exoplanet_archive import NASAExoplanetArchiveCollector
# from src.data_collectors.exoplanet_eu import ExoplanetEUCollector # Still commented
# from src.data_collectors.open_exoplanet import OpenExoplanetCollector # Still commented

from src.models.exoplanet import Exoplanet
# Import new services and the refactored DataProcessor
from src.utils.data_processor import DataProcessor
from src.utils.wikipedia_checker import WikipediaChecker, WikiArticleInfo # Assuming WikiArticleInfo is here
from src.services.exoplanet_repository import ExoplanetRepository
from src.services.statistics_service import StatisticsService
from src.services.wikipedia_service import WikipediaService
from src.services.export_service import ExportService

from src.utils.wikipedia_generator import WikipediaGenerator # Keep this for draft generation

# Setup basic logging
# You can customize format and level further if needed
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Create a logger for this module

def clean_filename(filename):
    invalid_chars = '<>:"/\\|?*\t\n\r'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    while '__' in filename:
        filename = filename.replace('__', '_')
    filename = filename.strip('_')
    return filename

def main():
    parser = argparse.ArgumentParser(description='Générateur d\'articles Wikipedia pour les exoplanètes')
    parser.add_argument('--use-mock-data', action='store_true', help='Utiliser les données mockées de la NASA')
    parser.add_argument('--sources', nargs='+', choices=['nasa', 'exoplanet_eu', 'open_exoplanet'],
                        default=['nasa'], # Defaulting to only nasa since exoplanet_eu is commented
                        help='Sources de données à utiliser (par défaut: nasa)')
    args = parser.parse_args()
    
    # --- 1. Initialize services ---
    repository = ExoplanetRepository()
    stat_service = StatisticsService()
    
    # Configure User-Agent for WikipediaChecker
    # It's good practice to set a descriptive User-Agent for any bot/script accessing web APIs
    # Replace 'your_project_name', 'your_contact_info' with actual details
    wiki_user_agent = 'AstroWikiBuilder/1.1 (bot; machichiotte@gmail.com or your_project_contact_page)'
    wikipedia_checker_instance = WikipediaChecker(user_agent=wiki_user_agent)
    
    wiki_service = WikipediaService(wikipedia_checker=wikipedia_checker_instance)
    export_service = ExportService()

    # --- 2. Initialize DataProcessor with injected services ---
    processor = DataProcessor(
        repository=repository,
        stat_service=stat_service,
        wiki_service=wiki_service,
        export_service=export_service
    )
    
    collectors = {}
    if 'nasa' in args.sources:
        collectors['nasa'] = NASAExoplanetArchiveCollector(use_mock_data=args.use_mock_data)
        
    # if 'exoplanet_eu' in args.sources:
    #     collectors['exoplanet_eu'] = ExoplanetEUCollector("data/exoplanet_eu.csv")
    # if 'open_exoplanet' in args.sources:
    #     collectors['open_exoplanet'] = OpenExoplanetCollector()
    
    all_fetched_exoplanets_for_drafts: List[Exoplanet] = [] # To collect all for drafts later

    for source_name_collector, collector in collectors.items():
        logger.info(f"Collecte des données depuis {source_name_collector}...")
        exoplanets_from_collector = collector.fetch_data()
        if exoplanets_from_collector:
            # The processor now uses add_exoplanets_from_source
            processor.add_exoplanets_from_source(exoplanets_from_collector, source_name_collector)
            all_fetched_exoplanets_for_drafts.extend(exoplanets_from_collector) # Collect for drafts
        else:
            logger.warning(f"Aucune exoplanète récupérée depuis {source_name_collector}.")
            
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"
    drafts_dir_base = "drafts" # Renamed to avoid conflict with save_drafts parameter
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir_base, exist_ok=True) # Create base drafts directory
    # Subdirectories for drafts will be created by save_drafts if needed, or ensure here
    os.makedirs(os.path.join(drafts_dir_base, "missing"), exist_ok=True)
    os.makedirs(os.path.join(drafts_dir_base, "existing"), exist_ok=True)
    
    logger.info("Export des données consolidées...")
    # Use the new export method in DataProcessor
    try:
        processor.export_exoplanet_data('csv', f"{output_dir}/exoplanets_consolidated_{timestamp}.csv")
        processor.export_exoplanet_data('json', f"{output_dir}/exoplanets_consolidated_{timestamp}.json")
    except Exception as e:
        logger.error(f"Erreur lors de l'export des données consolidées : {e}")

    stats = processor.get_statistics()
    logger.info("Statistiques des exoplanètes collectées :")
    logger.info(f"Nombre total d'exoplanètes consolidées : {stats.get('total_exoplanets', 0)}")
    
    logger.info("Points de données par source :") # Updated stat key
    for source, count in stats.get('data_points_by_source', {}).items():
        logger.info(f"- {source} : {count}")
        
    logger.info("Par méthode de découverte :")
    for method, count in stats.get('discovery_methods', {}).items():
        logger.info(f"- {method} : {count}")
        
    logger.info("Par année de découverte :")
    # Ensure years are treated as comparable, e.g., integers or strings
    # Sorting by str(x[0]) is fine if years are consistently numbers.
    for year, count in sorted(stats.get('discovery_years', {}).items(), key=lambda x: str(x[0])):
        logger.info(f"- {year} : {count}")
        
    logger.info("Vérification des articles Wikipedia...")
    # This method now returns Dict[str, Dict[str, WikiArticleInfo]] for existing and missing
    existing_wiki_data_map, missing_wiki_data_map = processor.get_and_separate_wikipedia_articles_by_status()
    logger.info("Séparation des articles Wikipedia terminée.")

    # --- Export Wikipedia links data using the new processor method ---
    # This handles both CSV and JSON export internally via ExportService
    try:
        if existing_wiki_data_map:
            processor.export_wikipedia_links_data(
                filename_base=f"{output_dir}/exoplanet",
                status_to_export="existing"
            )
            logger.info(f"Données des liens Wikipedia existants exportées vers {output_dir}/")
        else:
            logger.info("Aucun article Wikipedia existant trouvé à exporter.")

        if missing_wiki_data_map:
            processor.export_wikipedia_links_data(
                filename_base=f"{output_dir}/exoplanet",
                status_to_export="missing"
            )
            logger.info(f"Données des liens Wikipedia manquants exportées vers {output_dir}/")
        else:
            logger.info("Aucun article Wikipedia manquant trouvé (ou toutes les exoplanètes ont un article).")

    except Exception as e:
        logger.error(f"Erreur lors de l'export des données de liens Wikipedia : {e}")

    # --- Draft Generation Logic ---
    # Get all consolidated exoplanets from the repository for draft generation
    all_consolidated_exoplanets = processor.get_all_exoplanets()

    if not all_consolidated_exoplanets:
        logger.warning("Aucune exoplanète dans le référentiel, la génération de brouillons est ignorée.")
    else:
        missing_drafts_list: List[Tuple[str, str]] = []
        existing_drafts_list: List[Tuple[str, str]] = []

        logger.info("Génération des brouillons...")
        for exoplanet_obj in all_consolidated_exoplanets:
            draft_content = generate_draft(exoplanet_obj) # Uses your existing helper
            
            # Check against the maps returned by get_and_separate_wikipedia_articles_by_status
            if exoplanet_obj.name in missing_wiki_data_map:
                missing_drafts_list.append((exoplanet_obj.name, draft_content))
            elif exoplanet_obj.name in existing_wiki_data_map:
                # Even if an article exists, you might want to generate a draft for comparison or update
                existing_drafts_list.append((exoplanet_obj.name, draft_content))
            else:
                # This case implies the exoplanet was not in either map,
                # which could happen if no Wikipedia check was done for it or an error occurred.
                # Or, if all_consolidated_exoplanets contains items not processed by wiki check.
                # For safety, assume it's "missing" if not explicitly "existing".
                # However, the separate_articles_by_status should cover all checked exoplanets.
                # A more robust check might be needed if exoplanets can be added after wiki check.
                # For now, if it's not in existing_wiki_data_map, assume a draft might be needed if desired.
                # Let's stick to the definitions from separate_articles_by_status
                logger.debug(f"Exoplanète {exoplanet_obj.name} non trouvée dans les résultats de statut Wikipedia distincts, "
                             f"ne générant pas de brouillon dans les catégories standard existant/manquant.")


        logger.info("Bilan de la génération des brouillons :")
        logger.info(f"{len(missing_drafts_list)} brouillons générés pour les articles considérés comme manquants.")
        logger.info(f"{len(existing_drafts_list)} brouillons générés pour les articles considérés comme existants.")
        logger.info(f"Total : {len(missing_drafts_list) + len(existing_drafts_list)} brouillons générés.")
        
        if missing_drafts_list or existing_drafts_list:
            save_drafts(missing_drafts_list, existing_drafts_list, drafts_dir=drafts_dir_base)
            logger.info(f"Brouillons sauvegardés dans le répertoire : {drafts_dir_base}")
        else:
            logger.info("Aucun brouillon n'a été généré.")

    logger.info("Traitement principal terminé.")


def generate_draft(exoplanet: Exoplanet) -> str:
    """
    Génère le contenu d'un brouillon d'article pour une exoplanète.
    """
    generator = WikipediaGenerator() # Consider if this generator should be injected too
    return generator.generate_article_content(exoplanet)

def save_drafts(missing_drafts: List[Tuple[str, str]], 
                existing_drafts: List[Tuple[str, str]], 
                drafts_dir: str = "drafts") -> None: # Parameter name matches call
    """
    Sauvegarde les brouillons dans les fichiers appropriés.
    """
    # Ensure subdirectories exist (though main might have created them already)
    missing_dir = os.path.join(drafts_dir, "missing")
    existing_dir = os.path.join(drafts_dir, "existing")
    os.makedirs(missing_dir, exist_ok=True)
    os.makedirs(existing_dir, exist_ok=True)
    
    logger.info(f"Sauvegarde de {len(missing_drafts)} brouillons manquants dans {missing_dir}")
    for name, content in missing_drafts:
        safe_filename = clean_filename(name) # .replace(' ', '_') is not needed if clean_filename handles spaces
        filename = os.path.join(missing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")
            
    logger.info(f"Sauvegarde de {len(existing_drafts)} brouillons existants dans {existing_dir}")
    for name, content in existing_drafts:
        safe_filename = clean_filename(name)
        filename = os.path.join(existing_dir, f"{safe_filename}.wiki")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Impossible de sauvegarder le brouillon {filename}: {e}")

if __name__ == "__main__":
    main()