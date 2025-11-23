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

from src.core.config import DEFAULT_CONSOLIDATED_DIR, logger
from src.orchestration.data_pipeline import (
    export_consolidated_data,
    fetch_and_ingest_data,
    generate_and_export_statistics,
)
from src.orchestration.draft_pipeline import (
    generate_and_persist_exoplanet_drafts,
    generate_and_persist_star_drafts,
)
from src.orchestration.service_initializer import (
    initialize_collectors,
    initialize_services,
)
from src.services.processors.data_processor import DataProcessor
from src.utils.directory_util import create_output_directories


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
    if args.skip_wikipedia_check:
        # Mode test : générer tous les drafts sans vérifier l'existence sur Wikipedia
        logger.info(
            "Génération de tous les brouillons Wikipedia (sans vérification d'existence)..."
        )
        generate_and_persist_exoplanet_drafts(processor, args.drafts_dir)
        exoplanets = processor.collect_all_exoplanets()
        generate_and_persist_star_drafts(processor, args.drafts_dir, exoplanets)
    else:
        # Mode production : générer uniquement les drafts pour les articles non-existants
        logger.info("Vérification de l'existence des articles Wikipedia...")
        existing_articles, missing_articles = processor.resolve_wikipedia_status_for_exoplanets()

        logger.info(
            f"Résultats de la vérification : {len(existing_articles)} exoplanètes avec articles existants, "
            f"{len(missing_articles)} exoplanètes sans articles"
        )

        if missing_articles:
            logger.info(
                f"Génération des brouillons pour {len(missing_articles)} exoplanètes sans articles..."
            )
            # Filtrer les exoplanètes pour ne garder que celles sans articles
            all_exoplanets = processor.collect_all_exoplanets()
            exoplanets_to_draft = [exo for exo in all_exoplanets if exo.pl_name in missing_articles]

            # Générer les drafts uniquement pour les exoplanètes sans articles
            from src.utils.wikipedia.draft_util import (
                build_exoplanet_article_draft,
                persist_drafts_by_entity_type,
            )

            exoplanet_drafts = {}
            for exoplanet in exoplanets_to_draft:
                exoplanet_drafts[exoplanet.pl_name] = build_exoplanet_article_draft(exoplanet)

            persist_drafts_by_entity_type(exoplanet_drafts, {}, args.drafts_dir, "exoplanet")
            logger.info(f"Brouillons d'exoplanètes générés : {len(exoplanet_drafts)}")

            # Générer les drafts pour les étoiles correspondantes
            generate_and_persist_star_drafts(processor, args.drafts_dir, exoplanets_to_draft)
        else:
            logger.info("Aucun brouillon à générer : tous les articles existent déjà sur Wikipedia")

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
