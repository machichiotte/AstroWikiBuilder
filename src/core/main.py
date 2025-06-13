import os
from datetime import datetime
import argparse
from typing import Tuple, Dict, Any
import json

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
from src.collectors.implementations.exoplanet_eu import ExoplanetEUCollector
from src.collectors.implementations.open_exoplanet_collection import (
    OpenExoplanetCollector,
)

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


def setup_arguments() -> argparse.Namespace:
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


def initialize_collectors(args: argparse.Namespace) -> Dict[str, Any]:
    """Initialise les collecteurs de données basés sur les arguments."""
    collectors = {}
    mock_sources = args.use_mock

    if "nasa_exoplanet_archive" in args.sources:
        use_nasa_mock = "nasa_exoplanet_archive" in mock_sources
        collectors["nasa_exoplanet_archive"] = NASAExoplanetArchiveCollector(
            use_mock_data=use_nasa_mock
        )
        if use_nasa_mock:
            logger.info("Utilisation des données mockées pour NASA.")

    if "exoplanet_eu" in args.sources:
        use_eu_mock = "exoplanet_eu" in mock_sources
        eu_cache_path = CACHE_PATHS["exoplanet_eu"]["mock" if use_eu_mock else "real"]
        collectors["exoplanet_eu"] = ExoplanetEUCollector(
            cache_path=eu_cache_path, use_mock_data=use_eu_mock
        )
        if use_eu_mock:
            logger.info(
                f"Utilisation des données mockées pour Exoplanet.eu (chargement depuis {eu_cache_path})."
            )
        else:
            logger.info(
                f"ExoplanetEUCollector initialisé pour télécharger les données (cache dans {eu_cache_path})."
            )

    if "open_exoplanet" in args.sources:
        use_open_mock = "open_exoplanet" in mock_sources
        open_exoplanet_cache_path = CACHE_PATHS["open_exoplanet"][
            "mock" if use_open_mock else "real"
        ]
        collectors["open_exoplanet"] = OpenExoplanetCollector(
            cache_path=open_exoplanet_cache_path, use_mock_data=use_open_mock
        )
        if use_open_mock:
            logger.info(
                f"Utilisation des données mockées pour Open Exoplanet Catalogue (chargement depuis {open_exoplanet_cache_path})."
            )
        else:
            logger.info(
                f"OpenExoplanetCollector initialisé pour télécharger les données (cache dans {open_exoplanet_cache_path})."
            )

    logger.info(f"Collecteurs initialisés pour : {list(collectors.keys())}")
    return collectors


def fetch_and_process_data(collectors: Dict[str, Any], processor: DataProcessor):
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
        elif source_name == "nasa_exoplanet_archive":
            logger.info(f"Aucune étoile récupérée depuis {source_name}.")


def create_output_directories(
    output_dir: str = DEFAULT_OUTPUT_DIR, drafts_dir: str = DEFAULT_DRAFTS_DIR
):
    """Crée les répertoires de sortie nécessaires."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)
    logger.info(f"Répertoires de sortie créés : {output_dir}, {drafts_dir}")


def export_consolidated_data(processor: DataProcessor, output_dir: str, timestamp: str):
    """Exporte les données consolidées."""
    logger.info("Export des données consolidées...")
    try:
        processor.export_exoplanet_data(
            "csv", f"{output_dir}/exoplanets_consolidated_{timestamp}.csv"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export des données consolidées : {e}")


def log_statistics(stats: Dict[str, Any]):
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
    existing_map, missing_map = processor.check_wikipedia_status()

    # Export des résultats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    existing_path = f"{output_dir}/existing_articles_{timestamp}.json"
    missing_path = f"{output_dir}/missing_articles_{timestamp}.json"

    processor.export_wikipedia_status(existing_map, existing_path)
    processor.export_wikipedia_status(missing_map, missing_path)

    return existing_map, missing_map


def _run_draft_generation(
    processor: DataProcessor,
    existing_map: Dict,
    missing_map: Dict,
    drafts_dir: str,
    entity_type: str,
    get_entities_func: callable,
    generate_draft_func: callable,
    get_name_func: callable,
) -> None:
    """Génère les brouillons d'articles."""
    logger.info(f"Génération des brouillons pour les {entity_type}...")
    logger.info(f"Nombre d'entités dans missing_map: {len(missing_map)}")
    logger.info(
        f"Clés dans missing_map: {list(missing_map.keys())[:5]}..."
    )  # Affiche les 5 premières clés

    # Récupérer les entités
    entities = get_entities_func()
    logger.info(f"Nombre d'entités récupérées: {len(entities)}")

    # Générer les brouillons
    drafts = []
    for entity in entities:
        name = get_name_func(entity)
        logger.debug(f"Vérification de l'entité: {name}")
        if name in missing_map:
            logger.debug(f"Génération du draft pour: {name}")
            draft = generate_draft_func(entity)
            drafts.append((name, draft))
        else:
            logger.debug(f"Entité {name} non trouvée dans missing_map")

    # Sauvegarder les brouillons
    if drafts:
        save_drafts(drafts, [], drafts_dir, entity_type)
        logger.info(f"{len(drafts)} brouillons générés pour les {entity_type}")
    else:
        logger.info(f"Aucun brouillon généré pour les {entity_type}")


def exoplanet_run_draft_generation(
    processor: DataProcessor,
    existing_map: Dict,
    missing_map: Dict,
    is_wikipedia_check_skipped: bool,
    drafts_dir: str,
):
    """Génère les brouillons pour les exoplanètes."""
    if is_wikipedia_check_skipped:
        logger.info("Génération des brouillons pour toutes les exoplanètes...")
        drafts = []
        for exoplanet in processor.get_all_exoplanets():
            draft = generate_exoplanet_draft(exoplanet, None)
            drafts.append((exoplanet.pl_name, draft))
        save_drafts(drafts, [], drafts_dir, "exoplanètes")
        logger.info(f"{len(drafts)} brouillons générés pour les exoplanètes")
    else:
        _run_draft_generation(
            processor,
            existing_map,
            missing_map,
            drafts_dir,
            "exoplanètes",
            processor.get_all_exoplanets,
            generate_exoplanet_draft,
            lambda x: x.pl_name,
        )


def star_run_draft_generation(
    processor: DataProcessor,
    existing_map: Dict,
    missing_map: Dict,
    is_wikipedia_check_skipped: bool,
    drafts_dir: str,
):
    """Génère les brouillons pour les étoiles."""
    if is_wikipedia_check_skipped:
        logger.info("Génération des brouillons pour toutes les étoiles...")
        drafts = []
        for star in processor.get_all_stars():
            draft = generate_star_draft(star, None)
            drafts.append((star.st_name, draft))
        save_drafts(drafts, [], drafts_dir, "étoiles")
        logger.info(f"{len(drafts)} brouillons générés pour les étoiles")
    else:
        _run_draft_generation(
            processor,
            existing_map,
            missing_map,
            drafts_dir,
            "étoiles",
            processor.get_all_stars,
            generate_star_draft,
            lambda x: x.st_name,
        )


def main():
    """Point d'entrée principal du programme."""
    # Configuration
    args = setup_arguments()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Création des répertoires
    create_output_directories(args.output_dir, args.drafts_dir)

    # Initialisation des services
    (
        exoplanet_repository,
        star_repository,
        stat_service,
        wiki_service,
        export_service,
    ) = initialize_services()

    # Initialisation des collecteurs
    collectors = initialize_collectors(args)

    # Initialisation du processeur de données
    processor = DataProcessor(
        exoplanet_repository=exoplanet_repository,
        star_repository=star_repository,
        stat_service=stat_service,
        wiki_service=wiki_service,
        export_service=export_service,
    )

    # Collecte et traitement des données
    fetch_and_process_data(collectors, processor)

    # Export des données consolidées
    export_consolidated_data(processor, args.output_dir, timestamp)

    # Affichage et sauvegarde des statistiques
    stats = processor.get_statistics()
    log_statistics(stats)
    save_statistics(stats, args.output_dir, timestamp)

    # Vérification et génération des brouillons Wikipedia
    if not args.skip_wikipedia_check:
        existing_map, missing_map = check_and_export_wikipedia_status(
            processor, args.output_dir
        )

        # Génération des brouillons
        exoplanet_run_draft_generation(
            processor,
            existing_map,
            missing_map,
            args.skip_wikipedia_check,
            args.drafts_dir,
        )
        star_run_draft_generation(
            processor,
            existing_map,
            missing_map,
            args.skip_wikipedia_check,
            args.drafts_dir,
        )

    logger.info("Traitement terminé avec succès.")


if __name__ == "__main__":
    main()
