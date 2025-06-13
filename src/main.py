# src/main.py
import os
from datetime import datetime
import argparse
from typing import List, Tuple, Dict, Any
import logging

# Project imports
from src.data_collectors.nasa_exoplanet_archive_collector import (
    NASAExoplanetArchiveCollector,
)

from src.data_collectors.exoplanet_eu import ExoplanetEUCollector
from src.data_collectors.open_exoplanet_collection import OpenExoplanetCollector

from src.utils.data_processor import DataProcessor
from src.utils.wikipedia.wikipedia_checker import (
    WikipediaChecker,
    WikiArticleInfo,
)
from src.services.star_repository import StarRepository
from src.services.exoplanet_repository import ExoplanetRepository
from src.services.statistics_service import StatisticsService
from src.services.wikipedia_service import WikipediaService
from src.services.export_service import ExportService

from src.utils.draft_utils import (
    generate_exoplanet_draft,
    generate_star_draft,
    save_drafts,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def setup_arguments() -> argparse.Namespace:
    """Configure et parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Générateur d'articles Wikipedia pour les exoplanètes"
    )

    # --- Arguments pour les Sources ---
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=["nasa_exoplanet_archive", "exoplanet_eu", "open_exoplanet"],
        default=["nasa_exoplanet_archive"],
        help="Sources de données à utiliser (par défaut: nasa_exoplanet_archive)",
    )

    # --- Arguments pour les Mocks ---
    parser.add_argument(
        "--use-mock",
        nargs="+",
        choices=["nasa_exoplanet_archive", "exoplanet_eu", "open_exoplanet"],
        default=[],  # Par défaut, aucune source n'utilise de mock
        help="Utiliser les données mockées pour les sources spécifiées (ex: --use-mock nasa_exoplanet_archive).",
    )

    # --- Arguments pour le Workflow ---
    parser.add_argument(
        "--skip-wikipedia-check",
        action="store_true",
        help="Ignorer l'étape de vérification des articles Wikipedia et la génération de brouillons.",
    )

    # --- Arguments for Output Directories ---
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help='Directory for storing output files (consolidated data, logs, etc.). Default: "output"',
    )
    parser.add_argument(
        "--drafts-dir",
        type=str,
        default="drafts",
        help='Directory for storing generated Wikipedia draft articles. Default: "drafts"',
    )

    args = parser.parse_args()
    logger.info(
        f"Arguments reçus : Sources={args.sources}, Mocks={args.use_mock}, SkipWikiCheck={args.skip_wikipedia_check}, OutputDir={args.output_dir}, DraftsDir={args.drafts_dir}"
    )
    return args


def initialize_services() -> Tuple[
    ExoplanetRepository, StatisticsService, WikipediaService, ExportService
]:
    """Initialise et retourne les services principaux."""
    exoplanet_repository = ExoplanetRepository()
    star_repository = StarRepository()
    stat_service = StatisticsService()

    default_user_agent = "AstroWikiBuilder/1.1 (bot; machichiotte@gmail.com or your_project_contact_page)"
    wiki_user_agent = os.environ.get("WIKI_USER_AGENT", default_user_agent)
    if wiki_user_agent == default_user_agent:
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

    # Vérifie quelles sources doivent utiliser des mocks
    mock_sources = args.use_mock

    # Initialise NASA si demandé
    if "nasa_exoplanet_archive" in args.sources:
        use_nasa_mock = "nasa_exoplanet_archive" in mock_sources
        collectors["nasa_exoplanet_archive"] = NASAExoplanetArchiveCollector(
            use_mock_data=use_nasa_mock
        )
        if use_nasa_mock:
            logger.info("Utilisation des données mockées pour NASA.")

    # Initialise Exoplanet.eu si demandé
    if "exoplanet_eu" in args.sources:
        use_eu_mock = "exoplanet_eu" in mock_sources
        eu_cache_path = (
            "data/cache/exoplanet_eu_mock.csv"
            if use_eu_mock
            else "data/cache/exoplanet_eu_downloaded.csv"
        )
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

    # Initialise Open Exoplanet si demandé
    if "open_exoplanet" in args.sources:
        use_open_mock = "open_exoplanet" in mock_sources
        open_exoplanet_cache_path = (
            "data/cache/open_exoplanet_mock.csv"
            if use_open_mock
            else "data/cache/open_exoplanet_downloaded.txt"
        )
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


def create_output_directories(output_dir: str = "output", drafts_dir: str = "drafts"):
    """Crée les répertoires de sortie nécessaires."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(drafts_dir, exist_ok=True)

    # The unknown_status directory is handled by save_drafts in draft_utils.py if that logic was successfully updated.
    # If not, drafts of unknown status are logged and placed in 'missing'.
    logger.info(
        f"Répertoires de sortie créés : {output_dir}, {drafts_dir} (missing/existing subdirs created)"
    )


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
    logger.info("Statistiques des exoplanètes collectées :")
    logger.info(f"  Total : {stats.get('total_exoplanets', 0)}")
    logger.info("  Par source :")
    for source, count in stats.get("data_points_by_source", {}).items():
        logger.info(f"    - {source} : {count}")
    logger.info("  Par méthode de découverte :")
    for method, count in stats.get("disc_methods", {}).items():
        logger.info(f"    - {method} : {count}")
    logger.info("  Par année de découverte :")
    for year, count in sorted(
        stats.get("discovery_years", {}).items(), key=lambda x: str(x[0])
    ):
        logger.info(f"    - {year} : {count}")


def check_and_export_wikipedia_status(
    processor: DataProcessor, output_dir: str
) -> Tuple[
    Dict[str, Dict[str, WikiArticleInfo]], Dict[str, Dict[str, WikiArticleInfo]]
]:
    """Vérifie le statut Wikipedia et exporte les liens."""
    logger.info("Vérification des articles Wikipedia...")
    existing_map, missing_map = (
        processor.get_and_separate_wikipedia_articles_by_status()
    )
    logger.info(
        f"{len(existing_map)} articles existants, {len(missing_map)} articles manquants."
    )

    try:
        if existing_map:
            processor.export_wikipedia_links_data(
                f"{output_dir}/exoplanet", existing_map, "existing"
            )
            logger.info("Liens Wikipedia existants exportés.")
        if missing_map:
            processor.export_wikipedia_links_data(
                f"{output_dir}/exoplanet", missing_map, "missing"
            )
            logger.info("Liens Wikipedia manquants exportés.")
    except Exception as e:
        logger.error(f"Erreur lors de l'export des liens Wikipedia : {e}")
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
    """Génère et sauvegarde les brouillons d'articles de manière générique.

    Args:
        processor: Le processeur de données
        existing_map: Map des entités existantes
        missing_map: Map des entités manquantes
        drafts_dir: Répertoire de destination des brouillons
        entity_type: Type d'entité ('exoplanètes' ou 'étoiles')
        get_entities_func: Fonction pour récupérer les entités (get_all_exoplanets ou get_all_stars)
        generate_draft_func: Fonction pour générer le brouillon (generate_exoplanet_draft ou generate_star_draft)
        get_name_func: Fonction pour extraire le nom de l'entité
    """
    all_entities = get_entities_func()
    if not all_entities:
        logger.warning(f"Aucune {entity_type} pour la génération de brouillons.")
        return

    missing_drafts: List[Tuple[str, str]] = []
    existing_drafts: List[Tuple[str, str]] = []

    logger.info(f"Génération des brouillons de {entity_type}...")
    for entity in all_entities:
        name = get_name_func(entity)
        draft_content = generate_draft_func(entity)

        if name in missing_map:
            missing_drafts.append((name, draft_content))
        elif name in existing_map:
            existing_drafts.append((name, draft_content))
        else:
            missing_drafts.append((name, draft_content))

    logger.info(
        f"{len(missing_drafts)} brouillons 'manquants' (ou statut inconnu), {len(existing_drafts)} brouillons 'existants'."
    )

    if missing_drafts or existing_drafts:
        save_drafts(
            missing_drafts,
            existing_drafts,
            drafts_dir=drafts_dir,
            entity=entity_type,
        )
        logger.info(f"Brouillons sauvegardés dans {drafts_dir}")
    else:
        logger.info("Aucun brouillon n'a été généré.")


def exoplanet_run_draft_generation(
    processor: DataProcessor,
    existing_map: Dict,
    missing_map: Dict,
    is_wikipedia_check_skipped: bool,
):
    """Génère et sauvegarde les brouillons d'articles d'exoplanètes."""
    _run_draft_generation(
        processor=processor,
        existing_map=existing_map,
        missing_map=missing_map,
        drafts_dir="drafts/exoplanet",
        entity_type="exoplanètes",
        get_entities_func=processor.get_all_exoplanets,
        generate_draft_func=generate_exoplanet_draft,
        get_name_func=lambda exoplanet: exoplanet.pl_name.value,
    )


def star_run_draft_generation(
    processor: DataProcessor,
    existing_map: Dict,
    missing_map: Dict,
    is_wikipedia_check_skipped: bool,
):
    """Génère et sauvegarde les brouillons d'articles d'étoiles."""
    _run_draft_generation(
        processor=processor,
        existing_map=existing_map,
        missing_map=missing_map,
        drafts_dir="drafts/star",
        entity_type="étoiles",
        get_entities_func=processor.get_all_stars,
        generate_draft_func=generate_star_draft,
        get_name_func=lambda star: star.st_name.value,
    )


def main():
    """Fonction principale orchestrant le processus."""
    args = setup_arguments()

    # Initialisation
    (
        exoplanet_repository,
        star_repository,
        stat_service,
        wiki_service,
        export_service,
    ) = initialize_services()

    processor = DataProcessor(
        exoplanet_repository,
        star_repository,
        stat_service,
        wiki_service,
        export_service,
    )
    collectors = initialize_collectors(args)

    # Création des répertoires
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir
    drafts_dir = args.drafts_dir
    create_output_directories(output_dir, drafts_dir)

    # Collecte et traitement
    fetch_and_process_data(collectors, processor)

    # Star draft generation
    # --- Contrôle du Workflow ---
    if not args.skip_wikipedia_check:
        # Vérification Wikipedia et Génération des brouillons
        existing_map, missing_map = check_and_export_wikipedia_status(
            processor, output_dir
        )
        star_run_draft_generation(
            processor,
            existing_map,
            missing_map,
            is_wikipedia_check_skipped=False,
        )
    else:
        logger.info(
            "Vérification Wikipedia ignorée. Génération des brouillons pour toutes les étoiles."
        )
        star_run_draft_generation(processor, {}, {}, is_wikipedia_check_skipped=True)

    # Export et statistiques
    export_consolidated_data(processor, output_dir, timestamp)
    log_statistics(processor.get_statistics())

    # --- Contrôle du Workflow ---
    if not args.skip_wikipedia_check:
        # Vérification Wikipedia et Génération des brouillons
        existing_map, missing_map = check_and_export_wikipedia_status(
            processor, output_dir
        )
        exoplanet_run_draft_generation(
            processor,
            existing_map,
            missing_map,
            is_wikipedia_check_skipped=False,
        )
    else:
        logger.info(
            "Vérification Wikipedia ignorée. Génération des brouillons pour toutes les exoplanètes."
        )
        exoplanet_run_draft_generation(
            processor, {}, {}, is_wikipedia_check_skipped=True
        )

    logger.info("Traitement principal terminé.")


if __name__ == "__main__":
    main()
