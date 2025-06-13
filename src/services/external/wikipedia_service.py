# src/services/external/wikipedia_service.py
import logging
from typing import List, Dict, Any, Optional
from src.models.entities.exoplanet import Exoplanet
from src.utils.wikipedia.wikipedia_checker import WikipediaChecker

logger = logging.getLogger(__name__)


class WikipediaService:
    def __init__(self, wikipedia_checker: WikipediaChecker):
        self.wikipedia_checker = wikipedia_checker
        logger.info("WikipediaService initialized.")

    def get_all_articles_info_for_exoplanets(
        self, exoplanets: List[Exoplanet]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Vérifie l'existence des articles Wikipedia pour les exoplanètes.
        Returns a dictionary mapping Exoplanet name to a dictionary of its article infos (name/alias -> info dict).
        """
        logger.info(
            f"Starting Wikipedia article check for {len(exoplanets)} exoplanets."
        )

        all_results = {}
        titles_to_check = []
        context_for_titles = {}

        # Map titles to be checked to their exoplanet context (name, host_star_name, aliases)
        for exoplanet in exoplanets:
            all_results[exoplanet.pl_name] = {}  # Initialize results for this exoplanet

            titles_for_this_exoplanet = [exoplanet.pl_name]
            if exoplanet.pl_altname:
                titles_for_this_exoplanet.extend(exoplanet.pl_altname)

            host_star_name = exoplanet.st_name

            for title_to_check in titles_for_this_exoplanet:
                titles_to_check.append(title_to_check)
                # A more robust way would be to pass exoplanet objects to checker, but that increases coupling.
                context_for_titles[title_to_check] = {
                    "exoplanet_name": exoplanet.pl_name,  # To map back the result
                    "host_star_name": host_star_name,
                    "is_primary_name": title_to_check == exoplanet.pl_name,
                }

        # Check in batches
        batch_size = 50
        for i in range(0, len(titles_to_check), batch_size):
            batch_titles = titles_to_check[i : i + batch_size]
            batch_context = {title: context_for_titles[title] for title in batch_titles}

            batch_results = self.wikipedia_checker.check_multiple_articles(
                batch_titles, exoplanet_context=batch_context
            )

            # Now, map these flat results back to the per-exoplanet structure
            for queried_title, wiki_info in batch_results.items():
                exoplanet_name_origin = context_for_titles[queried_title][
                    "exoplanet_name"
                ]
                if exoplanet_name_origin in all_results:
                    all_results[exoplanet_name_origin][queried_title] = wiki_info
                else:
                    logger.warning(
                        f"Exoplanet name '{exoplanet_name_origin}' from context not found in initial results for title '{queried_title}'."
                    )

        return all_results

    def format_wikipedia_links_for_exoplanets(
        self,
        exoplanets: List[Exoplanet],
        exoplanet_articles_info: Dict[str, Dict[str, Any]],
        only_existing: bool = False,  # If true, only format for exoplanets with at least one existing article
        only_missing: bool = False,  # If true, only format for exoplanets with no existing articles
    ) -> List[Dict[str, Any]]:
        """
        Formate les liens Wikipedia pour les exoplanètes.
        Retourne une liste de dictionnaires plats pour l'export CSV.
        """
        logger.info(
            f"Formatting Wikipedia link data for {len(exoplanet_articles_info)} exoplanets..."
        )

        formatted_list = []

        # Create a quick lookup for exoplanets by name
        exoplanet_map = {exo.pl_name: exo for exo in exoplanets}

        for exoplanet_name, articles in exoplanet_articles_info.items():
            exoplanet_obj = exoplanet_map.get(exoplanet_name)
            if not exoplanet_obj:
                logger.warning(
                    f"Exoplanet object for '{exoplanet_name}' not found during formatting. Skipping."
                )
                continue

            has_any_existing_article = any(info.exists for info in articles.values())

            if (only_existing and not has_any_existing_article) or (
                only_missing and has_any_existing_article
            ):
                continue

            # Pour chaque article (nom principal et alias), créer une entrée dans la liste
            for title, info in articles.items():
                formatted_list.append(
                    {
                        "exoplanet_primary_name": exoplanet_name,
                        "queried_name": title,
                        "article_exists": info.exists,
                        "wikipedia_title": info.title if info.exists else None,
                        "is_redirect": info.is_redirect if info.exists else False,
                        "redirect_target": info.redirect_target
                        if info.exists
                        else None,
                        "url": info.url if info.exists else None,
                        "host_star": exoplanet_obj.st_name,
                    }
                )

        return formatted_list

    def separate_articles_by_status(self, all_articles_info: Dict[str, Dict[str, Any]]):
        """
        Sépare les exoplanètes en deux groupes :
        - Celles avec au moins un article Wikipédia existant
        - Celles sans aucun article existant
        Retourne (existing_articles, missing_articles)
        """
        existing_articles = {}
        missing_articles = {}
        for exoplanet_name, articles in all_articles_info.items():
            if any(info.exists for info in articles.values()):
                existing_articles[exoplanet_name] = articles
            else:
                missing_articles[exoplanet_name] = articles
        return existing_articles, missing_articles
