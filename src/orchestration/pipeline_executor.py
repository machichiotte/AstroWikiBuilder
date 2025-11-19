# src/orchestration/pipeline_executor.py
"""
Module d'orchestration du pipeline principal.

Responsabilité :
- Orchestrer toutes les étapes du workflow
- Coordonner les différents pipelines (data, draft)
- Gérer le flux global de l'application
"""

import argparse
from datetime import datetime

from src.core.config import logger, DEFAULT_CONSOLIDATED_DIR
from src.services.processors.data_processor import DataProcessor
from src.utils.directory_utils import create_output_directories

from src.orchestration.service_initializer import (
    initialize_services,
    initialize_collectors,
)
from src.orchestration.data_pipeline import (
    fetch_and_ingest_data,
    export_consolidated_data,
    generate_and_export_statistics,
)
from src.orchestration.draft_pipeline import (
    generate_and_persist_exoplanet_drafts,
    generate_and_persist_star_drafts,
)


def execute_pipeline(args: argparse.Namespace) -> None:
    """
    Exécute le pipeline complet de l'application.

    Ce pipeline comprend :
    1. Création des répertoires de sortie
    2. Initialisation des services et collecteurs
    3. Collecte et ingestion des données
    4. Export des données consolidées
    5. Génération des statistiques
    6. Génération des brouillons Wikipedia

    Args:
        args: Arguments parsés de la ligne de commande

    Example:
        >>> from src.orchestration.cli_parser import parse_cli_arguments
        >>> args = parse_cli_arguments()
        >>> execute_pipeline(args)
    """
    logger.info("Démarrage du pipeline AstroWikiBuilder...")

    # Étape 1 : Création des répertoires de sortie
    _setup_output_directories(args)

    # Étape 2 : Initialisation des services et collecteurs
    services = initialize_services()
    collectors = initialize_collectors(args)

    # Étape 3 : Initialisation du processeur de données
    processor = _initialize_data_processor(services)

    # Étape 4 : Collecte et traitement des données
    fetch_and_ingest_data(collectors, processor)

    # Étape 5 : Export des données consolidées
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_consolidated_data(processor, args.output_dir, timestamp)

    # Étape 6 : Génération et affichage des statistiques
    stat_service = services[2]  # StatisticsService est à l'index 2
    generate_and_export_statistics(stat_service, processor, args.output_dir, timestamp)

    # Étape 7 : Génération des brouillons Wikipedia
    if not args.skip_wikipedia_check:
        logger.info("Génération des brouillons Wikipedia...")
        generate_and_persist_exoplanet_drafts(processor, args.drafts_dir)
        exoplanets = processor.collect_all_exoplanets()
        generate_and_persist_star_drafts(processor, args.drafts_dir, exoplanets)
    else:
        logger.info(
            "Génération de brouillons Wikipedia ignorée (--skip-wikipedia-check)"
        )

    logger.info("Pipeline terminé avec succès !")


def _setup_output_directories(args: argparse.Namespace) -> None:
    """
    Crée les répertoires de sortie nécessaires.

    Args:
        args: Arguments contenant les chemins des répertoires
    """
    consolidated_dir = getattr(args, "consolidated_dir", DEFAULT_CONSOLIDATED_DIR)
    create_output_directories(args.output_dir, args.drafts_dir, consolidated_dir)


def _initialize_data_processor(services: tuple) -> DataProcessor:
    """
    Initialise le DataProcessor avec tous les services.

    Args:
        services: Tuple contenant (exo_repo, star_repo, stat_service, wiki_service, export_service)

    Returns:
        DataProcessor: Instance configurée du processeur
    """
    (
        exoplanet_repository,
        star_repository,
        stat_service,
        wiki_service,
        export_service,
    ) = services

    processor = DataProcessor(
        exoplanet_repository=exoplanet_repository,
        star_repository=star_repository,
        stat_service=stat_service,
        wiki_service=wiki_service,
        export_service=export_service,
    )

    logger.info("DataProcessor initialisé.")
    return processor
