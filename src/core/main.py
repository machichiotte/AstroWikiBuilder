# src/core/main.py
import os
from datetime import datetime
import argparse
from typing import List, Tuple, Dict, Any
import json

from src.models.entities.exoplanet import Exoplanet
from src.core.config import (
    logger,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_DRAFTS_DIR,
    AVAILABLE_SOURCES,
    CACHE_PATHS,
    DEFAULT_WIKI_USER_AGENT,
)

from src.collectors.implementations.nasa_exoplanet_archive_collector import (
    NASAExoplanetArchiveCollector,
)
# from src.collectors.implementations.exoplanet_eu import ExoplanetEUCollector
# from src.collectors.implementations.open_exoplanet_collection import OpenExoplanetCollector


from src.services.processors.data_processor import DataProcessor
from src.utils.wikipedia.wikipedia_checker import WikipediaChecker, WikiArticleInfo
from src.services.repositories.star_repository import StarRepository
from src.services.repositories.exoplanet_repository import ExoplanetRepository
from src.services.processors.statistics_service import StatisticsService
from src.services.external.wikipedia_service import WikipediaService
from src.services.external.export_service import ExportService

from src.utils.wikipedia.draft_utils import (
    build_exoplanet_article_draft,
    build_star_article_draft,
    persist_drafts_by_entity_type,
)
from src.models.entities.star import Star


# ============================================================================
# CONFIGURATION ET ARGUMENTS DE LIGNE DE COMMANDE
# ============================================================================


def parse_cli_arguments() -> argparse.Namespace:
    """Configure et parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Générateur d'articles Wikipedia pour les exoplanètes"
    )

    parser.add_argument(
        "--sources",
        nargs="+",
        choices=AVAILABLE_SOURCES,
        default=["nasa_exoplanet_archive"],
        help="Sources de données à utiliser (par défaut: nasa_exoplanet_archive)",
    )

    parser.add_argument(
        "--use-mock",
        nargs="+",
        choices=AVAILABLE_SOURCES,
        default=[],
        help="Utiliser les données mockées pour les sources spécifiées",
    )

    parser.add_argument(
        "--skip-wikipedia-check",
        action="store_true",
        help="Ignorer l'étape de vérification des articles Wikipedia",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f'Directory for storing output files. Default: "{DEFAULT_OUTPUT_DIR}"',
    )

    parser.add_argument(
        "--drafts-dir",
        type=str,
        default=DEFAULT_DRAFTS_DIR,
        help=f'Directory for storing generated Wikipedia draft articles. Default: "{DEFAULT_DRAFTS_DIR}"',
    )

    args = parser.parse_args()
    logger.info(
        f"Arguments reçus : Sources={args.sources}, Mocks={args.use_mock}, "
        f"SkipWikiCheck={args.skip_wikipedia_check}, "
        f"OutputDir={args.output_dir}, DraftsDir={args.drafts_dir}"
    )
    return args


# ============================================================================
# INITIALISATION DES SERVICES ET COLLECTEURS
# ============================================================================


def initialize_services() -> Tuple[
    ExoplanetRepository,
    StarRepository,
    StatisticsService,
    WikipediaService,
    ExportService,
]:
    """Initialise et retourne les services principaux."""
    exoplanet_repository = ExoplanetRepository()
    star_repository = StarRepository()
    stat_service = StatisticsService()

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


def _initialize_collectors(args: argparse.Namespace) -> Dict[str, Any]:
    """Initialise les collecteurs de données basés sur les arguments."""
    collectors = {}
    mock_sources = args.use_mock

    # Définition des sources de données à collecter
    # data_sources = ["nasa_exoplanet_archive", "exoplanet_eu", "open_exoplanet"]
    data_sources = ["nasa_exoplanet_archive"]
    for source in data_sources:
        if source in args.sources:
            use_mock = source in mock_sources
            cache_path = CACHE_PATHS[source]["mock" if use_mock else "real"]
            collector = _get_collector_instance(source, use_mock, cache_path)
            collectors[source] = collector
            log_collector_initialization(source, use_mock, cache_path)

    logger.info(f"Collecteurs initialisés pour : {list(collectors.keys())}")
    return collectors


def _get_collector_instance(source: str, use_mock: bool, cache_path: str) -> Any:
    """Retourne une instance du collecteur approprié basée sur la source."""
    if source == "nasa_exoplanet_archive":
        return NASAExoplanetArchiveCollector(
            use_mock_data=use_mock,
            custom_cache_filename=cache_path,
        )
    # elif source == "exoplanet_eu":
    #     return ExoplanetEUCollector(cache_path=cache_path, use_mock_data=use_mock)
    # elif source == "open_exoplanet":
    #     return OpenExoplanetCollector(cache_path=cache_path, use_mock_data=use_mock)
    else:
        raise ValueError(f"Source inconnue : {source}")


def log_collector_initialization(source: str, use_mock: bool, cache_path: str) -> None:
    """Enregistre un message dans le journal pour chaque collecteur initialisé."""
    if use_mock:
        logger.info(
            f"Utilisation des données mockées pour {source} (chargement depuis {cache_path})."
        )
    else:
        logger.info(
            f"{source}Collector initialisé pour télécharger les données (cache dans {cache_path})."
        )


# ============================================================================
# COLLECTE ET TRAITEMENT DES DONNÉES
# ============================================================================


def fetch_and_ingest_collected_data(
    collectors: Dict[str, Any], processor: DataProcessor
):
    """Récupère les données des collecteurs et les traite."""
    for source_name, collector in collectors.items():
        logger.info(f"Collecte des données depuis {source_name}...")

        try:
            exoplanets, stars = collector.collect_exoplanets_and_stars_from_source()

            if not isinstance(exoplanets, list):
                raise TypeError(
                    f"Exoplanets doit être une liste, reçu {type(exoplanets)}"
                )

            if stars is not None and not isinstance(stars, list):
                raise TypeError(
                    f"Stars doit être une liste ou None, reçu {type(stars)}"
                )

        except Exception as e:
            logger.warning(f"Erreur lors de la collecte depuis {source_name}: {e}")
            continue

        if exoplanets:
            processor.ingest_exoplanets_from_source(exoplanets, source_name)
        else:
            logger.info(f"Aucune exoplanète récupérée depuis {source_name}.")

        if stars:
            processor.ingest_stars_from_source(stars, source_name)
        else:
            logger.info(f"Aucune étoile récupérée depuis {source_name}.")


# ============================================================================
# GESTION DES RÉPERTOIRES ET EXPORT
# ============================================================================


def _create_output_directories(
    output_dir: str = DEFAULT_OUTPUT_DIR, drafts_dir: str = DEFAULT_DRAFTS_DIR
):
    """Crée les répertoires de sortie nécessaires."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)
    logger.info(f"Répertoires de sortie créés : {output_dir}, {drafts_dir}")


def export_consolidated_exoplanet_data(
    processor: DataProcessor, output_dir: str, timestamp: str
):
    """Exporte les données consolidées."""
    logger.info("Export des données consolidées...")
    try:
        processor.export_all_exoplanets(
            "csv", f"{output_dir}/exoplanets_consolidated_{timestamp}.csv"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export des données consolidées : {e}")


# ============================================================================
# ANALYSE ET STATISTIQUES
# ============================================================================


def log_collected_statistics(stats: Dict[str, Any]):
    """Affiche les statistiques collectées."""
    # Statistiques des exoplanètes
    logger.info("Statistiques des exoplanètes collectées :")
    logger.info(f"  Total : {stats.get('exoplanet', {}).get('total', 0)}")

    logger.info("  Par méthode de découverte :")
    for method, count in (
        stats.get("exoplanet", {}).get("discovery_methods", {}).items()
    ):
        logger.info(f"    - {method} : {count}")

    logger.info("  Par année de découverte :")
    for year, count in sorted(
        stats.get("exoplanet", {}).get("discovery_years", {}).items(),
        key=lambda x: str(x[0]),
    ):
        logger.info(f"    - {year} : {count}")

    logger.info("  Par plage de masse (MJ) :")
    for range_name, count in stats.get("exoplanet", {}).get("mass_ranges", {}).items():
        logger.info(f"    - {range_name} : {count}")

    logger.info("  Par plage de rayon (RJ) :")
    for range_name, count in (
        stats.get("exoplanet", {}).get("radius_ranges", {}).items()
    ):
        logger.info(f"    - {range_name} : {count}")

    # Statistiques des étoiles
    logger.info("\nStatistiques des étoiles collectées :")
    logger.info(f"  Total : {stats.get('star', {}).get('total_stars', 0)}")

    logger.info("  Par type spectral :")
    for spectral_type, count in stats.get("star", {}).get("spectral_types", {}).items():
        logger.info(f"    - {spectral_type} : {count}")

    logger.info("  Par source de données :")
    for source, count in stats.get("star", {}).get("data_points_by_source", {}).items():
        logger.info(f"    - {source} : {count}")


def export_statistics_to_json(stats: Dict[str, Any], output_dir: str, timestamp: str):
    """Sauvegarde les statistiques dans un fichier JSON."""
    # Créer le répertoire des statistiques s'il n'existe pas
    stats_dir = os.path.join(output_dir, "statistics")
    os.makedirs(stats_dir, exist_ok=True)

    # Sauvegarder les statistiques
    stats_path = os.path.join(stats_dir, f"statistics_{timestamp}.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    logger.info(f"Statistiques sauvegardées dans {stats_path}")


def generate_and_log_statistics(
    stat_service: StatisticsService,
    processor: DataProcessor,
):
    stats = {
        "exoplanet": stat_service.generate_statistics_exoplanet(
            processor.collect_all_exoplanets()
        ),
        "star": stat_service.generate_statistics_star(processor.collect_all_stars()),
    }

    # Affichage et sauvegarde des statistiques
    log_collected_statistics(stats)


# ============================================================================
# GESTION DES ARTICLES WIKIPEDIA
# ============================================================================


def resolve_and_export_wikipedia_article_status(
    processor: DataProcessor, output_dir: str
) -> Tuple[
    Dict[str, Dict[str, WikiArticleInfo]], Dict[str, Dict[str, WikiArticleInfo]]
]:
    """Vérifie et exporte le statut des articles Wikipedia."""
    logger.info("Vérification du statut des articles Wikipedia...")
    existing_map, missing_map = processor.resolve_wikipedia_status_for_exoplanets()

    # Export des résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    existing_path = f"{output_dir}/existing_articles_{timestamp}.json"
    missing_path = f"{output_dir}/missing_articles_{timestamp}.json"

    processor.export_exoplanet_wikipedia_links_by_status(
        existing_path, existing_map, "existing"
    )
    processor.export_exoplanet_wikipedia_links_by_status(
        missing_path, missing_map, "missing"
    )

    return existing_map, missing_map


# ============================================================================
# GÉNÉRATION DES BROUILLONS D'ARTICLES
# ============================================================================


def generate_and_persist_star_drafts(
    processor: DataProcessor,
    drafts_dir: str,
    exoplanets: List[Exoplanet] = None,
) -> None:
    """
    Génère et sauvegarde les brouillons d'étoiles en filtrant les objets valides.
    Si des exoplanètes sont fournies, elles seront utilisées pour enrichir le contenu des étoiles.
    """
    stars: List[Star] = processor.collect_all_stars()

    # Créer un index des exoplanètes par nom d'étoile hôte
    exoplanets_by_star_name: Dict[str, List[Exoplanet]] = {}
    if exoplanets:
        for exoplanet in exoplanets:
            if hasattr(exoplanet, "st_name") and exoplanet.st_name:
                star_name = str(exoplanet.st_name)
                if star_name not in exoplanets_by_star_name:
                    exoplanets_by_star_name[star_name] = []
                exoplanets_by_star_name[star_name].append(exoplanet)

    logger.info(f"Nombre total d'objets retournés par get_all_stars: {len(stars)}")
    logger.info(
        f"Index créé pour {len(exoplanets_by_star_name)} étoiles avec exoplanètes"
    )

    star_drafts = {}
    for star in stars:
        star_name: str = getattr(star, "st_name", "UNKNOWN")
        if isinstance(star, Star):
            # Récupérer les exoplanètes de cette étoile
            star_exoplanets = exoplanets_by_star_name.get(star_name, [])
            if star_exoplanets:
                star_drafts[star_name] = build_star_article_draft(
                    star, exoplanets=star_exoplanets
                )
            else:
                logger.info(
                    f"Génération draft étoile: {star_name} (aucune exoplanète connue)"
                )

        else:
            logger.warning(f"Objet ignoré (type: {type(star)}) pour {star_name}")

    persist_drafts_by_entity_type(
        star_drafts,
        {},
        drafts_dir,
        "star",
    )


def generate_and_persist_exoplanet_drafts(
    processor: DataProcessor,
    drafts_dir: str,
) -> None:
    """
    Génère et sauvegarde les brouillons d'exoplanetes en filtrant les objets valides.
    """
    exoplanets: List[Exoplanet] = processor.collect_all_exoplanets()
    total = len(exoplanets)
    logger.info(f"Nombre total d'objets retournés par get_all_exoplanets: {total}")
    exoplanet_drafts = {}
    for idx, exoplanet in enumerate(exoplanets, 1):
        exoplanet_name: str = exoplanet.pl_name
        if isinstance(exoplanet, Exoplanet):
            if idx % 100 == 0 or idx == total:
                logger.info(f"Progression: {idx}/{total} exoplanètes traitées...")
            exoplanet_drafts[exoplanet_name] = build_exoplanet_article_draft(exoplanet)
        else:
            logger.warning(
                f"Objet ignoré (type: {type(exoplanet)}) pour {exoplanet_name}"
            )
    logger.info(f"Nombre total de brouillons générés: {len(exoplanet_drafts)}")
    persist_drafts_by_entity_type(
        exoplanet_drafts,
        {},
        drafts_dir,
        "exoplanet",
    )


# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================


def main():
    """Point d'entrée principal du programme."""
    args: argparse.Namespace = parse_cli_arguments()

    _create_output_directories(args.output_dir, args.drafts_dir)

    # Initialisation des services
    (
        exoplanet_repository,
        star_repository,
        stat_service,
        wiki_service,
        export_service,
    ) = initialize_services()

    # Initialisation des collecteurs
    collectors: Dict[str, Any] = _initialize_collectors(args)

    # Initialisation du processeur de données
    processor = DataProcessor(
        exoplanet_repository=exoplanet_repository,
        star_repository=star_repository,
        stat_service=stat_service,
        wiki_service=wiki_service,
        export_service=export_service,
    )

    # Collecte et traitement des données
    fetch_and_ingest_collected_data(collectors, processor)

    # Export des données consolidées
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_consolidated_exoplanet_data(processor, args.output_dir, timestamp)

    generate_and_log_statistics(stat_service, processor)

    # Vérification des articles Wikipedia et génération des drafts
    # if not args.skip_wikipedia_check:
    #    existing_map, missing_map = check_and_export_wikipedia_status(
    #        processor, args.output_dir
    #    )
    # else:
    #    existing_map = {}
    #    missing_map = {}

    generate_and_persist_exoplanet_drafts(processor, args.drafts_dir)
    generate_and_persist_star_drafts(
        processor, args.drafts_dir, processor.collect_all_exoplanets()
    )

    logger.info("Traitement terminé avec succès.")


if __name__ == "__main__":
    main()
