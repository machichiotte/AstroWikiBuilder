# src/utils/data_processor.py
import logging
from typing import Any

from src.mappers.nasa_exoplanet_archive_mapper import NasaExoplanetArchiveMapper
from src.models.entities.exoplanet_entity import Exoplanet
from src.models.entities.star_entity import Star
from src.services.external.export_service import ExportService
from src.services.external.wikipedia_service import WikipediaService
from src.services.processors.statistics_service import StatisticsService
from src.services.repositories.exoplanet_repository import ExoplanetRepository
from src.services.repositories.star_repository import StarRepository
from src.utils.wikipedia.wikipedia_checker import WikiArticleInfo

# Setup basic logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Processeur principal pour la gestion des données astronomiques.
    Coordonne l'ingestion, la collecte, l'analyse et l'export des données.
    """

    def __init__(
        self,
        exoplanet_repository: ExoplanetRepository,
        star_repository: StarRepository,
        stat_service: StatisticsService,
        wiki_service: WikipediaService,
        export_service: ExportService,
    ):
        self.exoplanet_repository = exoplanet_repository
        self.star_repository = star_repository
        self.stat_service = stat_service
        self.wiki_service = wiki_service
        self.export_service = export_service
        self.nea_mapper = NasaExoplanetArchiveMapper()
        logger.info("DataProcessor initialized with all services.")

    # ============================================================================
    # INGESTION DES DONNÉES DEPUIS LES SOURCES EXTERNES
    # ============================================================================

    def ingest_exoplanets_from_source(
        self, exoplanets: list[Exoplanet], source_name: str
    ) -> None:
        """Ajoute ou fusionne les exoplanètes dans le référentiel."""
        self.exoplanet_repository.add_exoplanets(exoplanets, source_name)

    def ingest_stars_from_source(self, stars: list[Star], source_name: str) -> None:
        """Ajoute ou fusionne les étoiles dans le référentiel."""
        self.star_repository.add_stars(stars, source_name)

    # ============================================================================
    # COLLECTE DES DONNÉES DEPUIS LE RÉFÉRENTIEL
    # ============================================================================

    def collect_all_exoplanets(self) -> list[Exoplanet]:
        """Récupère toutes les exoplanètes consolidées."""
        return self.exoplanet_repository.get_all_exoplanets()

    def collect_all_stars(self) -> list[Star]:
        """Récupère toutes les étoiles consolidées."""
        return self.star_repository.get_all_stars()

    # ============================================================================
    # ANALYSE ET STATISTIQUES DES DONNÉES
    # ============================================================================

    def generate_data_statistics(self) -> dict[str, Any]:
        """Retourne des statistiques sur les données collectées."""
        statistics_star: dict[str, Any] = self.compute_star_statistics()
        statistics_exoplanet: dict[str, Any] = self.compute_exoplanet_statistics()
        return {"exoplanet": statistics_exoplanet, "star": statistics_star}

    def compute_exoplanet_statistics(self) -> dict[str, Any]:
        """Retourne des statistiques sur les données collectées."""
        all_exoplanets: list[Exoplanet] = self.exoplanet_repository.get_all_exoplanets()
        return self.stat_service.generate_statistics_exoplanet(all_exoplanets)

    def compute_star_statistics(self) -> dict[str, Any]:
        """Retourne des statistiques sur les données collectées."""
        all_stars: list[Star] = self.star_repository.get_all_stars()
        return self.stat_service.generate_statistics_star(all_stars)

    # ============================================================================
    # GESTION DES ARTICLES WIKIPEDIA
    # ============================================================================

    def resolve_wikipedia_status_for_exoplanets(
        self,
    ) -> tuple[
        dict[str, dict[str, WikiArticleInfo]], dict[str, dict[str, WikiArticleInfo]]
    ]:
        """
        Récupère les informations des articles Wikipedia et les sépare en existants et manquants.
        """
        logger.info(
            "Starting process to get and separate Wikipedia articles by status."
        )
        all_articles_info: dict[str, dict[str, WikiArticleInfo]] = (
            self.fetch_wikipedia_articles_for_exoplanets()
        )
        if not all_articles_info:
            logger.warning("No Wikipedia article information was retrieved.")
            return {}, {}

        existing_articles, missing_articles = (
            self.wiki_service.split_by_article_existence(all_articles_info)
        )
        logger.info(
            f"Separation complete: {len(existing_articles)} exoplanets with existing articles, "
            f"{len(missing_articles)} exoplanets with no articles found for any name/alias."
        )
        return existing_articles, missing_articles

    def fetch_wikipedia_articles_for_exoplanets(
        self,
    ) -> dict[str, dict[str, WikiArticleInfo]]:
        """
        Récupère les informations des articles Wikipedia pour toutes les exoplanètes du référentiel.
        """
        all_exoplanets: list[Exoplanet] = self.exoplanet_repository.get_all_exoplanets()
        if not all_exoplanets:
            logger.warning(
                "No exoplanets in exoplanet_repository to check Wikipedia for."
            )
            return {}
        return self.wiki_service.fetch_articles_for_exoplanet_batch(all_exoplanets)

    # ============================================================================
    # EXPORT DES DONNÉES
    # ============================================================================

    def export_all_exoplanets(self, format_type: str, filename: str) -> None:
        """Exporte toutes les données d'exoplanètes."""
        all_exoplanets: list[Exoplanet] = self.exoplanet_repository.get_all_exoplanets()
        if format_type.lower() == "csv":
            self.export_service.export_exoplanets_to_csv(filename, all_exoplanets)
        elif format_type.lower() == "json":
            self.export_service.export_exoplanets_to_json(filename, all_exoplanets)
        else:
            logger.error(f"Unsupported export format: {format_type}")
            raise ValueError(f"Unsupported export format: {format_type}")

    def export_exoplanet_wikipedia_links_by_status(
        self,
        filename_base: str,
        wiki_data_map_to_export: dict[str, dict[str, WikiArticleInfo]],
        status_description_for_filename: str,
    ) -> None:
        """
        Exporte les données formatées des liens Wikipedia en CSV et JSON.
        wiki_data_map_to_export: Le dictionnaire de données (déjà filtré) à exporter.
        status_description_for_filename: Une chaîne comme "existing" ou "missing" pour le nom de fichier.
        """
        logger.info(
            f"Preparing to export Wikipedia links data for status: {status_description_for_filename}"
        )
        all_exoplanets_from_repo: list[Exoplanet] = (
            self.exoplanet_repository.get_all_exoplanets()
        )  # Still needed for context in format_wiki_links_data_for_export
        if not all_exoplanets_from_repo:
            logger.warning(
                "No exoplanets in exoplanet_repository to generate Wikipedia link data for."
            )
            return

        if not wiki_data_map_to_export:
            logger.info(
                f"No data to export for status '{status_description_for_filename}'."
            )
            return

        # data_to_format is now directly wiki_data_map_to_export
        formatted_list: list[dict[str, Any]] = (
            self.wiki_service.format_article_links_for_export(
                all_exoplanets_from_repo,  # Pass all exoplanets for context
                wiki_data_map_to_export,  # Pass the already filtered map
            )
        )

        if not formatted_list:
            logger.info(
                f"No formatted data to export for status '{status_description_for_filename}'."
            )
            return

        csv_filename: str = (
            f"{filename_base}_{status_description_for_filename}_wiki_links.csv"
        )
        json_filename: str = (
            f"{filename_base}_{status_description_for_filename}_wiki_links.json"
        )

        # Define headers for CSV for consistent output
        headers: list[str] = [
            "exoplanet_primary_name",
            "queried_name",
            "article_exists",
            "wikipedia_title",
            "is_redirect",
            "redirect_target",
            "url",
            "host_star",
        ]
        self.export_service.export_generic_list_of_dicts_to_csv(
            csv_filename, formatted_list, headers=headers
        )
        self.export_service.export_generic_list_of_dicts_to_json(
            json_filename, formatted_list
        )
        logger.info(
            f"Wikipedia links data for '{status_description_for_filename}' exported to {csv_filename} and {json_filename}"
        )
