# src/main.py
import os
from datetime import datetime
import argparse
from typing import List, Tuple, Dict, Any
import logging

# Project imports
from src.data_collectors.nasa_exoplanet_archive import NASAExoplanetArchiveCollector
# Code commenté utile : Imports pour d'autres sources de données
# from src.data_collectors.exoplanet_eu import ExoplanetEUCollector
# from src.data_collectors.open_exoplanet import OpenExoplanetCollector

from src.models.exoplanet import Exoplanet
from src.utils.data_processor import DataProcessor
from src.utils.wikipedia_checker import WikipediaChecker
from src.services.exoplanet_repository import ExoplanetRepository
from src.services.statistics_service import StatisticsService
from src.services.wikipedia_service import WikipediaService
from src.services.export_service import ExportService
from src.utils.draft_utils import generate_draft, save_drafts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_arguments() -> argparse.Namespace:
    """Configure et parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description='Générateur d\'articles Wikipedia pour les exoplanètes')

    # --- Arguments pour les Sources ---
    parser.add_argument('--sources', nargs='+', choices=['nasa', 'exoplanet_eu', 'open_exoplanet'],
                        default=['nasa'],
                        help='Sources de données à utiliser (par défaut: nasa)')

    # --- Arguments pour les Mocks ---
    parser.add_argument('--use-mock', nargs='+', choices=['nasa'],
                        default=[], # Par défaut, aucune source n'utilise de mock
                        help='Utiliser les données mockées pour les sources spécifiées (ex: --use-mock nasa).')

    # --- Arguments pour le Workflow ---
    parser.add_argument('--skip-wikipedia-check', action='store_true',
                        help='Ignorer l\'étape de vérification des articles Wikipedia et la génération de brouillons.')

    args = parser.parse_args()
    logger.info(f"Arguments reçus : Sources={args.sources}, Mocks={args.use_mock}, SkipWikiCheck={args.skip_wikipedia_check}")
    return args

def initialize_services() -> Tuple[ExoplanetRepository, StatisticsService, WikipediaService, ExportService]:
    """Initialise et retourne les services principaux."""
    repository = ExoplanetRepository()
    stat_service = StatisticsService()
    wiki_user_agent = 'AstroWikiBuilder/1.1 (bot; machichiotte@gmail.com or your_project_contact_page)'
    wikipedia_checker = WikipediaChecker(user_agent=wiki_user_agent)
    wiki_service = WikipediaService(wikipedia_checker=wikipedia_checker)
    export_service = ExportService()
    logger.info("Services initialisés.")
    return repository, stat_service, wiki_service, export_service

def initialize_collectors(args: argparse.Namespace) -> Dict[str, Any]:
    """Initialise les collecteurs de données basés sur les arguments."""
    collectors = {}
    
    # Vérifie quelles sources doivent utiliser des mocks
    mock_sources = args.use_mock

    # Initialise NASA si demandé
    if 'nasa' in args.sources:
        use_nasa_mock = 'nasa' in mock_sources
        collectors['nasa'] = NASAExoplanetArchiveCollector(use_mock_data=use_nasa_mock)
        if use_nasa_mock:
            logger.info("Utilisation des données mockées pour NASA.")

    # Initialise Exoplanet.eu si demandé (actuellement commenté)
    if 'exoplanet_eu' in args.sources:
        use_eu_mock = 'exoplanet_eu' in mock_sources
        if use_eu_mock:
            logger.info("Utilisation des données mockées pour Exoplanet.eu (logique à implémenter).")
        # Code commenté utile :
        # collectors['exoplanet_eu'] = ExoplanetEUCollector("data/exoplanet_eu_mock.csv" if use_eu_mock else "data/exoplanet_eu.csv")
        pass # Garder commenté jusqu'à implémentation

    # Initialise Open Exoplanet si demandé (actuellement commenté)
    if 'open_exoplanet' in args.sources:
        use_open_mock = 'open_exoplanet' in mock_sources
        if use_open_mock:
             logger.info("Utilisation des données mockées pour Open Exoplanet (logique à implémenter).")
        # Code commenté utile :
        # collectors['open_exoplanet'] = OpenExoplanetCollector(use_mock=use_open_mock) # Supposant une option 'use_mock'
        pass # Garder commenté jusqu'à implémentation

    logger.info(f"Collecteurs initialisés pour : {list(collectors.keys())}")
    return collectors

# Les fonctions fetch_and_process_data, create_output_directories,
# export_consolidated_data, log_statistics restent inchangées.
# Nous les incluons ici pour la complétude du fichier.

def fetch_and_process_data(collectors: Dict[str, Any], processor: DataProcessor):
    """Récupère les données des collecteurs et les traite."""
    for source_name, collector in collectors.items():
        logger.info(f"Collecte des données depuis {source_name}...")
        exoplanets = collector.fetch_data()
        if exoplanets:
            processor.add_exoplanets_from_source(exoplanets, source_name)
        else:
            logger.warning(f"Aucune exoplanète récupérée depuis {source_name}.")

def create_output_directories(output_dir: str = "output", drafts_dir: str = "drafts"):
    """Crée les répertoires de sortie nécessaires."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)
    os.makedirs(os.path.join(drafts_dir, "missing"), exist_ok=True)
    os.makedirs(os.path.join(drafts_dir, "existing"), exist_ok=True)
    logger.info(f"Répertoires de sortie créés : {output_dir}, {drafts_dir}")

def export_consolidated_data(processor: DataProcessor, output_dir: str, timestamp: str):
    """Exporte les données consolidées."""
    logger.info("Export des données consolidées...")
    try:
        processor.export_exoplanet_data('csv', f"{output_dir}/exoplanets_consolidated_{timestamp}.csv")
        processor.export_exoplanet_data('json', f"{output_dir}/exoplanets_consolidated_{timestamp}.json")
    except Exception as e:
        logger.error(f"Erreur lors de l'export des données consolidées : {e}")

def log_statistics(stats: Dict[str, Any]):
    """Affiche les statistiques collectées."""
    logger.info("Statistiques des exoplanètes collectées :")
    logger.info(f"  Total : {stats.get('total_exoplanets', 0)}")
    logger.info("  Par source :")
    for source, count in stats.get('data_points_by_source', {}).items():
        logger.info(f"    - {source} : {count}")
    logger.info("  Par méthode de découverte :")
    for method, count in stats.get('discovery_methods', {}).items():
        logger.info(f"    - {method} : {count}")
    logger.info("  Par année de découverte :")
    for year, count in sorted(stats.get('discovery_years', {}).items(), key=lambda x: str(x[0])):
        logger.info(f"    - {year} : {count}")

def check_and_export_wikipedia_status(processor: DataProcessor, output_dir: str) -> Tuple[Dict, Dict]:
    """Vérifie le statut Wikipedia et exporte les liens."""
    logger.info("Vérification des articles Wikipedia...")
    existing, missing = processor.get_and_separate_wikipedia_articles_by_status()
    logger.info(f"{len(existing)} articles existants, {len(missing)} articles manquants.")

    try:
        if existing:
            processor.export_wikipedia_links_data(f"{output_dir}/exoplanet", "existing")
            logger.info(f"Liens Wikipedia existants exportés.")
        if missing:
            processor.export_wikipedia_links_data(f"{output_dir}/exoplanet", "missing")
            logger.info(f"Liens Wikipedia manquants exportés.")
    except Exception as e:
        logger.error(f"Erreur lors de l'export des liens Wikipedia : {e}")
    return existing, missing

def run_draft_generation(processor: DataProcessor, existing_map: Dict, missing_map: Dict, drafts_dir: str):
    """Génère et sauvegarde les brouillons d'articles."""
    all_exoplanets = processor.get_all_exoplanets()
    if not all_exoplanets:
        logger.warning("Aucune exoplanète pour la génération de brouillons.")
        return

    # In the 'skip_wikipedia_check' scenario, existing_map and missing_map
    # will be empty, causing all drafts to go into 'missing_drafts'.
    # This effectively makes all generated drafts considered "new" or "unclassified"
    # for Wikipedia status.
    missing_drafts: List[Tuple[str, str]] = []
    existing_drafts: List[Tuple[str, str]] = []

    logger.info("Génération des brouillons...")
    for exoplanet in all_exoplanets:
        draft_content = generate_draft(exoplanet)
        if exoplanet.name in missing_map:
            missing_drafts.append((exoplanet.name, draft_content))
        elif exoplanet.name in existing_map:
            existing_drafts.append((exoplanet.name, draft_content))
        else:
            # If Wikipedia check is skipped, all exoplanets will fall here
            # and be treated as "missing" for draft saving purposes.
            missing_drafts.append((exoplanet.name, draft_content))
            logger.debug(f"{exoplanet.name} non trouvé dans les listes wiki. Ajouté aux brouillons manquants par défaut.")

    logger.info(f"{len(missing_drafts)} brouillons 'manquants', {len(existing_drafts)} brouillons 'existants'.")

    if missing_drafts or existing_drafts:
        save_drafts(missing_drafts, existing_drafts, drafts_dir)
        logger.info(f"Brouillons sauvegardés dans {drafts_dir}")
    else:
        logger.info("Aucun brouillon n'a été généré.")


def main():
    """Fonction principale orchestrant le processus."""
    args = setup_arguments()

    # Initialisation
    repository, stat_service, wiki_service, export_service = initialize_services()
    processor = DataProcessor(repository, stat_service, wiki_service, export_service)
    collectors = initialize_collectors(args)

    # Création des répertoires
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "output"
    drafts_dir = "drafts"
    create_output_directories(output_dir, drafts_dir)

    # Collecte et traitement
    fetch_and_process_data(collectors, processor)

    # Export et statistiques
    export_consolidated_data(processor, output_dir, timestamp)
    log_statistics(processor.get_statistics())

    # --- Contrôle du Workflow ---
    if not args.skip_wikipedia_check:
        # Vérification Wikipedia et Génération des brouillons
        existing_map, missing_map = check_and_export_wikipedia_status(processor, output_dir)
        run_draft_generation(processor, existing_map, missing_map, drafts_dir)
    else:
        logger.info("Vérification Wikipedia ignorée. Génération des brouillons pour toutes les exoplanètes.")
        # When skipping Wikipedia check, we still want to generate drafts.
        # Since we don't have Wikipedia status, we'll treat all as "missing" for draft purposes.
        # Pass empty maps to run_draft_generation so all exoplanets fall into the 'else' block.
        run_draft_generation(processor, {}, {}, drafts_dir)

    logger.info("Traitement principal terminé.")

if __name__ == "__main__":
    main()