import os
from datetime import datetime
import argparse
from typing import Tuple, Dict, Any
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
    generate_exoplanet_draft,
    generate_star_draft,
    save_drafts,
)
from src.models.entities.star import Star


def _setup_arguments() -> argparse.Namespace:
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


def _initialize_services() -> Tuple[
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
            _log_message(source, use_mock, cache_path)

    logger.info(f"Collecteurs initialisés pour : {list(collectors.keys())}")
    return collectors


def _get_collector_instance(source: str, use_mock: bool, cache_path: str) -> Any:
    """Retourne une instance du collecteur approprié basée sur la source."""
    if source == "nasa_exoplanet_archive":
        return NASAExoplanetArchiveCollector(use_mock_data=use_mock)
    # elif source == "exoplanet_eu":
    #     return ExoplanetEUCollector(cache_path=cache_path, use_mock_data=use_mock)
    # elif source == "open_exoplanet":
    #     return OpenExoplanetCollector(cache_path=cache_path, use_mock_data=use_mock)
    else:
        raise ValueError(f"Source inconnue : {source}")


def _log_message(source: str, use_mock: bool, cache_path: str) -> None:
    """Enregistre un message dans le journal pour chaque collecteur initialisé."""
    if use_mock:
        logger.info(
            f"Utilisation des données mockées pour {source} (chargement depuis {cache_path})."
        )
    else:
        logger.info(
            f"{source}Collector initialisé pour télécharger les données (cache dans {cache_path})."
        )


def _fetch_and_process_data(collectors: Dict[str, Any], processor: DataProcessor):
    """Récupère les données des collecteurs et les traite."""
    for source_name, collector in collectors.items():
        logger.info(f"Collecte des données depuis {source_name}...")

        try:
            exoplanets, stars = collector.fetch_data()

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
            processor.add_exoplanets_from_source(exoplanets, source_name)
        else:
            logger.info(f"Aucune exoplanète récupérée depuis {source_name}.")

        if stars:
            processor.add_stars_from_source(stars, source_name)
        else:
            logger.info(f"Aucune étoile récupérée depuis {source_name}.")


def _create_output_directories(
    output_dir: str = DEFAULT_OUTPUT_DIR, drafts_dir: str = DEFAULT_DRAFTS_DIR
):
    """Crée les répertoires de sortie nécessaires."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)
    logger.info(f"Répertoires de sortie créés : {output_dir}, {drafts_dir}")


def _export_consolidated_data(
    processor: DataProcessor, output_dir: str, timestamp: str
):
    """Exporte les données consolidées."""
    logger.info("Export des données consolidées...")
    try:
        processor.export_exoplanet_data(
            "csv", f"{output_dir}/exoplanets_consolidated_{timestamp}.csv"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export des données consolidées : {e}")


def _log_statistics(stats: Dict[str, Any]):
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


def save_statistics(stats: Dict[str, Any], output_dir: str, timestamp: str):
    """Sauvegarde les statistiques dans un fichier JSON."""
    # Créer le répertoire des statistiques s'il n'existe pas
    stats_dir = os.path.join(output_dir, "statistics")
    os.makedirs(stats_dir, exist_ok=True)

    # Sauvegarder les statistiques
    stats_path = os.path.join(stats_dir, f"statistics_{timestamp}.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    logger.info(f"Statistiques sauvegardées dans {stats_path}")


def check_and_export_wikipedia_status(
    processor: DataProcessor, output_dir: str
) -> Tuple[
    Dict[str, Dict[str, WikiArticleInfo]], Dict[str, Dict[str, WikiArticleInfo]]
]:
    """Vérifie et exporte le statut des articles Wikipedia."""
    logger.info("Vérification du statut des articles Wikipedia...")
    existing_map, missing_map = (
        processor.get_and_separate_wikipedia_articles_by_status()
    )

    # Export des résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    existing_path = f"{output_dir}/existing_articles_{timestamp}.json"
    missing_path = f"{output_dir}/missing_articles_{timestamp}.json"

    processor.export_wikipedia_links_data(existing_path, existing_map, "existing")
    processor.export_wikipedia_links_data(missing_path, missing_map, "missing")

    return existing_map, missing_map


def _generate_stats(
    stat_service: StatisticsService,
    processor: DataProcessor,
):
    stats = {
        "exoplanet": stat_service.generate_statistics_exoplanet(
            processor.get_all_exoplanets()
        ),
        "star": stat_service.generate_statistics_star(processor.get_all_stars()),
    }

    # Affichage et sauvegarde des statistiques
    _log_statistics(stats)


def _generate_and_save_star_drafts(
    processor: DataProcessor,
    drafts_dir: str,
) -> None:
    """
    Génère et sauvegarde les brouillons d'étoiles en filtrant les objets valides.
    """
    stars = processor.get_all_stars()

    logger.info(f"Nombre total d'objets retournés par get_all_stars: {len(stars)}")
    star_drafts = {}

    for star in stars:
        star_name = getattr(star, "st_name", "UNKNOWN")
        if isinstance(star, Star):
            logger.info(f"Génération draft étoile: {star_name} (type: {type(star)})")
            star_drafts[star_name] = generate_star_draft(star)
        else:
            logger.warning(f"Objet ignoré (type: {type(star)}) pour {star_name}")

    save_drafts(
        star_drafts,
        {},
        drafts_dir,
        "star",
    )


def _generate_and_save_exoplanet_drafts(
    processor: DataProcessor,
    drafts_dir: str,
) -> None:
    """
    Génère et sauvegarde les brouillons d'exoplanetes en filtrant les objets valides.
    """
    exoplanets = processor.get_all_exoplanets()
    logger.info(
        f"Nombre total d'objets retournés par get_all_exoplanets: {len(exoplanets)}"
    )
    exoplanet_drafts = {}
    for exoplanet in exoplanets:
        exoplanet_name: str = exoplanet.pl_name
        if isinstance(exoplanet, Exoplanet):
            logger.info(
                f"Génération draft exoplanet: {exoplanet_name} (type: {type(exoplanet)})"
            )
            exoplanet_drafts[exoplanet_name] = generate_exoplanet_draft(exoplanet)
        else:
            logger.warning(
                f"Objet ignoré (type: {type(exoplanet)}) pour {exoplanet_name}"
            )
    save_drafts(
        exoplanet_drafts,
        {},
        drafts_dir,
        "exoplanet",
    )


def main():
    """Point d'entrée principal du programme."""
    args = _setup_arguments()

    _create_output_directories(args.output_dir, args.drafts_dir)

    # Initialisation des services
    (
        exoplanet_repository,
        star_repository,
        stat_service,
        wiki_service,
        export_service,
    ) = _initialize_services()

    # Initialisation des collecteurs
    collectors = _initialize_collectors(args)

    # Initialisation du processeur de données
    processor = DataProcessor(
        exoplanet_repository=exoplanet_repository,
        star_repository=star_repository,
        stat_service=stat_service,
        wiki_service=wiki_service,
        export_service=export_service,
    )

    # Collecte et traitement des données
    _fetch_and_process_data(collectors, processor)

    # Export des données consolidées
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    _export_consolidated_data(processor, args.output_dir, timestamp)

    _generate_stats(stat_service, processor)

    # Vérification des articles Wikipedia et génération des drafts
    # if not args.skip_wikipedia_check:
    #    existing_map, missing_map = check_and_export_wikipedia_status(
    #        processor, args.output_dir
    #    )
    # else:
    #    existing_map = {}
    #    missing_map = {}

    _generate_and_save_exoplanet_drafts(processor, args.drafts_dir)
    _generate_and_save_star_drafts(processor, args.drafts_dir)

    logger.info("Traitement terminé avec succès.")


if __name__ == "__main__":
    main()
