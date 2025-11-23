# src/orchestration/service_initializer.py
"""
Module d'initialisation des services et collecteurs.

Responsabilité :
- Initialiser tous les services (repositories, statistics, wikipedia, export)
- Initialiser les collecteurs de données
- Factory pattern pour les collecteurs
"""

import argparse
import os
from typing import Any

from src.collectors.implementations.exoplanet_eu_collector import ExoplanetEUCollector
from src.collectors.implementations.nasa_exoplanet_archive_collector import (
    NasaExoplanetArchiveCollector,
)
from src.collectors.implementations.open_exoplanet_catalogue_collector import (
    OpenExoplanetCatalogueCollector,
)
from src.core.config import (
    CACHE_PATHS,
    DEFAULT_WIKI_USER_AGENT,
    logger,
)
from src.services.external.export_service import ExportService
from src.services.external.wikipedia_service import WikipediaService
from src.services.processors.statistics_service import StatisticsService
from src.services.repositories.exoplanet_repository import ExoplanetRepository
from src.services.repositories.star_repository import StarRepository
from src.utils.wikipedia.wikipedia_checker import WikipediaChecker


def initialize_services() -> tuple[
    ExoplanetRepository,
    StarRepository,
    StatisticsService,
    WikipediaService,
    ExportService,
]:
    """
    Initialise et retourne tous les services principaux.

    Returns:
        Tuple contenant :
        - ExoplanetRepository: Repository pour les exoplanètes
        - StarRepository: Repository pour les étoiles
        - StatisticsService: Service de statistiques
        - WikipediaService: Service Wikipedia
        - ExportService: Service d'export

    Example:
        >>> repos, star_repo, stats, wiki, export = initialize_services()
    """
    exoplanet_repository = ExoplanetRepository()
    star_repository = StarRepository()
    stat_service = StatisticsService()

    # Configuration du Wikipedia User-Agent
    wiki_user_agent = os.environ.get("WIKI_USER_AGENT", DEFAULT_WIKI_USER_AGENT)
    if wiki_user_agent == DEFAULT_WIKI_USER_AGENT:
        logger.info(f"Using default Wikipedia User-Agent: {wiki_user_agent}")
    else:
        logger.info(
            f"Using Wikipedia User-Agent from environment variable WIKI_USER_AGENT: {wiki_user_agent}"
        )

    wikipedia_checker = WikipediaChecker(user_agent=wiki_user_agent)
    wiki_service = WikipediaService(wikipedia_checker=wikipedia_checker)
    export_service = ExportService()

    logger.info("Services initialisés.")
    return (
        exoplanet_repository,
        star_repository,
        stat_service,
        wiki_service,
        export_service,
    )


def initialize_collectors(args: argparse.Namespace) -> dict[str, Any]:
    """
    Initialise les collecteurs de données basés sur les arguments CLI.

    Args:
        args: Arguments parsés de la ligne de commande

    Returns:
        Dict[str, Any]: Dictionnaire {source_name: collector_instance}

    Example:
        >>> collectors = initialize_collectors(args)
        >>> nasa_collector = collectors.get('nasa_exoplanet_archive')
    """
    collectors = {}
    mock_sources = args.use_mock

    # Sources de données disponibles
    data_sources = [
        "nasa_exoplanet_archive",
        "exoplanet_eu",
        "open_exoplanet",
    ]

    for source in data_sources:
        if source in args.sources:
            use_mock = source in mock_sources
            cache_path = CACHE_PATHS[source]["mock" if use_mock else "real"]
            collector = _get_collector_instance(source, use_mock, cache_path)
            collectors[source] = collector
            _log_collector_initialization(source, use_mock, cache_path)

    logger.info(f"Collecteurs initialisés pour : {list(collectors.keys())}")
    return collectors


def _get_collector_instance(source: str, use_mock: bool, cache_path: str) -> Any:
    """
    Factory pour créer une instance du collecteur approprié.

    Args:
        source: Nom de la source de données
        use_mock: Utiliser les données mockées ou non
        cache_path: Chemin du fichier de cache

    Returns:
        Instance du collecteur approprié

    Raises:
        ValueError: Si la source est inconnue
    """
    if source == "nasa_exoplanet_archive":
        return NasaExoplanetArchiveCollector(
            use_mock_data=use_mock,
            custom_cache_filename=cache_path,
        )
    elif source == "exoplanet_eu":
        return ExoplanetEUCollector(cache_dir=cache_path, use_mock_data=use_mock)
    elif source == "open_exoplanet":
        return OpenExoplanetCatalogueCollector(cache_dir=cache_path, use_mock_data=use_mock)
    else:
        raise ValueError(f"Source inconnue : {source}")


def _log_collector_initialization(source: str, use_mock: bool, cache_path: str) -> None:
    """
    Enregistre un message dans le journal pour chaque collecteur initialisé.

    Args:
        source: Nom de la source
        use_mock: Utilisation de données mockées
        cache_path: Chemin du cache
    """
    if use_mock:
        logger.info(
            f"Utilisation des données mockées pour {source} (chargement depuis {cache_path})."
        )
    else:
        logger.info(
            f"{source}Collector initialisé pour télécharger les données (cache dans {cache_path})."
        )
