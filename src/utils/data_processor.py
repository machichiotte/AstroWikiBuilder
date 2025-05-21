# src/utils/data_processor.py
import logging
from typing import List, Dict, Tuple, Any
from src.models.exoplanet import Exoplanet
from src.utils.wikipedia_checker import WikiArticleInfo 
from src.services.exoplanet_repository import ExoplanetRepository
from src.services.statistics_service import StatisticsService
from src.services.wikipedia_service import WikipediaService
from src.services.export_service import ExportService

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self,
                 repository: ExoplanetRepository,
                 stat_service: StatisticsService,
                 wiki_service: WikipediaService,
                 export_service: ExportService):
        self.repository = repository
        self.stat_service = stat_service
        self.wiki_service = wiki_service
        self.export_service = export_service
        logger.info("DataProcessor initialized with all services.")

    def add_exoplanets_from_source(self, exoplanets: List[Exoplanet], source_name: str) -> None:
        """Ajoute ou fusionne les exoplanètes dans le référentiel."""
        self.repository.add_exoplanets(exoplanets, source_name)

    def get_all_exoplanets(self) -> List[Exoplanet]:
        """Récupère toutes les exoplanètes consolidées."""
        return self.repository.get_all_exoplanets()

    def get_statistics(self) -> Dict[str, Any]:
        """Retourne des statistiques sur les données collectées."""
        all_exoplanets = self.repository.get_all_exoplanets()
        return self.stat_service.generate_statistics(all_exoplanets)

    def get_wikipedia_article_information_for_all_exoplanets(self) -> Dict[str, Dict[str, WikiArticleInfo]]:
        """
        Récupère les informations des articles Wikipedia pour toutes les exoplanètes du référentiel.
        """
        all_exoplanets = self.repository.get_all_exoplanets()
        if not all_exoplanets:
            logger.warning("No exoplanets in repository to check Wikipedia for.")
            return {}
        return self.wiki_service.get_all_articles_info_for_exoplanets(all_exoplanets)
        
    def get_and_separate_wikipedia_articles_by_status(self) -> Tuple[Dict[str, Dict[str, WikiArticleInfo]], Dict[str, Dict[str, WikiArticleInfo]]]:
        """
        Récupère les informations des articles Wikipedia et les sépare en existants et manquants.
        """
        logger.info("Starting process to get and separate Wikipedia articles by status.")
        all_articles_info = self.get_wikipedia_article_information_for_all_exoplanets()
        if not all_articles_info:
            logger.warning("No Wikipedia article information was retrieved.")
            return {}, {}
        
        existing_articles, missing_articles = self.wiki_service.separate_articles_by_status(all_articles_info)
        logger.info(f"Separation complete: {len(existing_articles)} exoplanets with existing articles, "
                    f"{len(missing_articles)} exoplanets with no articles found for any name/alias.")
        return existing_articles, missing_articles

    def export_exoplanet_data(self, format_type: str, filename: str) -> None:
        """Exporte toutes les données d'exoplanètes."""
        all_exoplanets = self.repository.get_all_exoplanets()
        if format_type.lower() == 'csv':
            self.export_service.export_exoplanets_to_csv(filename, all_exoplanets)
        elif format_type.lower() == 'json':
            self.export_service.export_exoplanets_to_json(filename, all_exoplanets)
        else:
            logger.error(f"Unsupported export format: {format_type}")
            raise ValueError(f"Unsupported export format: {format_type}")

    def export_wikipedia_links_data(self,
                                    filename_base: str,
                                    status_to_export: str = "all" # "all", "existing", "missing"
                                   ) -> None:
        """
        Exporte les données formatées des liens Wikipedia en CSV et JSON.
        status_to_export: "all", "existing", ou "missing" pour filtrer ce qui est exporté.
        """
        logger.info(f"Preparing to export Wikipedia links data for status: {status_to_export}")
        all_exoplanets_from_repo = self.repository.get_all_exoplanets()
        if not all_exoplanets_from_repo:
            logger.warning("No exoplanets in repository to generate Wikipedia link data for.")
            return

        all_wiki_infos = self.get_wikipedia_article_information_for_all_exoplanets()
        if not all_wiki_infos:
            logger.warning("No Wikipedia information retrieved, cannot export links data.")
            return

        data_to_format: Dict[str, Dict[str, WikiArticleInfo]]
        if status_to_export == "existing":
            existing_map, _ = self.wiki_service.separate_articles_by_status(all_wiki_infos)
            data_to_format = existing_map
        elif status_to_export == "missing":
            _, missing_map = self.wiki_service.separate_articles_by_status(all_wiki_infos)
            data_to_format = missing_map
        elif status_to_export == "all":
            data_to_format = all_wiki_infos
        else:
            logger.error(f"Invalid status_to_export: {status_to_export}. Must be 'all', 'existing', or 'missing'.")
            return

        if not data_to_format:
            logger.info(f"No data to export for status '{status_to_export}'.")
            return
            
        formatted_list = self.wiki_service.format_wiki_links_data_for_export(
            all_exoplanets_from_repo, # Pass all exoplanets for context
            data_to_format # Pass the filtered map
        )

        if not formatted_list:
            logger.info(f"No formatted data to export for status '{status_to_export}'.")
            return

        csv_filename = f"{filename_base}_{status_to_export}_wiki_links.csv"
        json_filename = f"{filename_base}_{status_to_export}_wiki_links.json"

        # Define headers for CSV for consistent output
        headers = [
            'exoplanet_primary_name', 'queried_name', 'article_exists', 
            'wikipedia_title', 'is_redirect', 'redirect_target', 'url', 'host_star'
        ]
        self.export_service.export_generic_list_of_dicts_to_csv(csv_filename, formatted_list, headers=headers)
        self.export_service.export_generic_list_of_dicts_to_json(json_filename, formatted_list)
        logger.info(f"Wikipedia links data for '{status_to_export}' exported to {csv_filename} and {json_filename}")
