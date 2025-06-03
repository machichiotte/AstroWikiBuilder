# src/services/wikipedia_service.py
import logging
from typing import List, Dict, Tuple, Any
from src.models.data_source_exoplanet import DataSourceExoplanet
from src.utils.wikipedia.wikipedia_checker import (
    WikipediaChecker,
    WikiArticleInfo,
)

logger = logging.getLogger(__name__)


class WikipediaService:
    def __init__(self, wikipedia_checker: WikipediaChecker):
        self.checker = wikipedia_checker
        logger.info("WikipediaService initialized.")

    def get_all_articles_info_for_exoplanets(
        self, exoplanets: List[DataSourceExoplanet]
    ) -> Dict[str, Dict[str, WikiArticleInfo]]:
        """
        Obtient les informations de tous les articles Wikipedia pour chaque exoplanète.
        Returns a dictionary mapping Exoplanet name to a dictionary of its article infos (name/alias -> WikiArticleInfo).
        """
        logger.info(
            f"Starting Wikipedia article check for {len(exoplanets)} exoplanets."
        )
        all_results: Dict[str, Dict[str, WikiArticleInfo]] = {}

        titles_to_batch_check: List[str] = []
        # Map titles to be checked to their exoplanet context (name, host_star_name, aliases)
        # This helps the checker decide if a found page is actually the host star.
        context_for_titles: Dict[str, Dict[str, Any]] = {}

        for exoplanet in exoplanets:
            all_results[exoplanet.name] = {}  # Initialize results for this exoplanet

            titles_for_this_exoplanet = [exoplanet.name]
            if exoplanet.other_names:
                titles_for_this_exoplanet.extend(exoplanet.other_names)

            host_star_name = exoplanet.host_star.value if exoplanet.host_star else None

            for title_to_check in titles_for_this_exoplanet:
                if (
                    title_to_check not in titles_to_batch_check
                ):  # Avoid duplicate checks if same alias used by multiple planets (unlikely but possible)
                    titles_to_batch_check.append(title_to_check)
                # Store context for each title. If a title is an alias for multiple planets,
                # the last one's context will be stored. This assumes titles are unique enough.
                # A more robust way would be to pass exoplanet objects to checker, but that increases coupling.
                context_for_titles[title_to_check] = {
                    "exoplanet_name": exoplanet.name,  # To map back the result
                    "host_star_name": host_star_name,
                    "is_primary_name": title_to_check == exoplanet.name,
                }

        # Batch process all unique titles
        batch_size = 50  # As per WikipediaChecker's limit
        total_titles_to_check = len(titles_to_batch_check)
        checked_article_infos: Dict[
            str, WikiArticleInfo
        ] = {}  # title_queried -> WikiArticleInfo

        for i in range(0, total_titles_to_check, batch_size):
            batch_titles = titles_to_batch_check[i : i + batch_size]
            logger.info(
                f"Checking Wikipedia batch: {i // batch_size + 1}/{(total_titles_to_check + batch_size - 1) // batch_size} ({len(batch_titles)} titles)"
            )

            # Prepare specific context for this batch
            batch_context = {
                title: {"host_star_name": context_for_titles[title]["host_star_name"]}
                for title in batch_titles
                if title in context_for_titles
            }

            try:
                # `check_multiple_articles` returns Dict[queried_title, WikiArticleInfo]
                batch_wiki_infos = self.checker.check_multiple_articles(
                    batch_titles, exoplanet_context=batch_context
                )
                checked_article_infos.update(batch_wiki_infos)
            except Exception as e:
                logger.error(f"Error checking Wikipedia batch {batch_titles}: {e}")
                for title in batch_titles:  # Mark all in batch as error
                    checked_article_infos[title] = WikiArticleInfo(
                        exists=False,
                        title=title,
                        queried_title=title,
                        url=f"Error: {e}",
                    )

        # Now, map these flat results back to the per-exoplanet structure
        for queried_title, wiki_info in checked_article_infos.items():
            if queried_title in context_for_titles:
                exoplanet_name_origin = context_for_titles[queried_title][
                    "exoplanet_name"
                ]
                if exoplanet_name_origin in all_results:
                    all_results[exoplanet_name_origin][queried_title] = wiki_info
                else:
                    logger.warning(
                        f"Exoplanet name '{exoplanet_name_origin}' from context not found in initial results for title '{queried_title}'."
                    )
            else:
                logger.warning(
                    f"Queried title '{queried_title}' from Wikipedia check not found in context map."
                )

        logger.info("Wikipedia article check finished.")
        return all_results

    def separate_articles_by_status(
        self, all_exoplanet_articles_info: Dict[str, Dict[str, WikiArticleInfo]]
    ) -> Tuple[
        Dict[str, Dict[str, WikiArticleInfo]], Dict[str, Dict[str, WikiArticleInfo]]
    ]:
        """
        Sépare les informations d'articles par exoplanète en deux dictionnaires : existants et manquants.
        Un article est considéré existant pour une exoplanète si AU MOINS UN de ses noms/alias a un article Wikipedia.
        """
        logger.info("Separating articles by status...")
        existing_articles_map: Dict[str, Dict[str, WikiArticleInfo]] = {}
        missing_articles_map: Dict[str, Dict[str, WikiArticleInfo]] = {}

        for exoplanet_name, articles_for_exo in all_exoplanet_articles_info.items():
            has_any_existing_article = any(
                info.exists for info in articles_for_exo.values()
            )

            if has_any_existing_article:
                existing_articles_map[exoplanet_name] = articles_for_exo
            else:
                missing_articles_map[exoplanet_name] = articles_for_exo

        logger.info(
            f"Separation complete. Existing: {len(existing_articles_map)}, Missing: {len(missing_articles_map)}"
        )
        return existing_articles_map, missing_articles_map

    def format_wiki_links_data_for_export(
        self,
        exoplanets: List[
            DataSourceExoplanet
        ],  # Need full exoplanet objects for context like host_star
        exoplanet_articles_info: Dict[str, Dict[str, WikiArticleInfo]],
        only_existing: bool = False,  # If true, only format for exoplanets with at least one existing article
        only_missing: bool = False,  # If true, only format for exoplanets with no existing articles
    ) -> List[Dict[str, Any]]:
        """
        Formate les données des liens Wikipedia pour l'export (par exemple, en JSON ou pour CSV).
        Chaque item de la liste représente une tentative de lien (un nom/alias d'une exoplanète).
        """
        logger.info(
            f"Formatting Wikipedia link data for {len(exoplanet_articles_info)} exoplanets..."
        )
        formatted_data = []

        # Create a quick lookup for exoplanets by name
        exoplanet_map = {exo.name: exo for exo in exoplanets}

        for exoplanet_name, articles in exoplanet_articles_info.items():
            exoplanet_obj = exoplanet_map.get(exoplanet_name)
            if not exoplanet_obj:
                logger.warning(
                    f"Exoplanet object for '{exoplanet_name}' not found during formatting. Skipping."
                )
                continue

            has_any_existing = any(info.exists for info in articles.values())

            if only_existing and not has_any_existing:
                continue
            if only_missing and has_any_existing:
                continue

            for (
                queried_name,
                info,
            ) in articles.items():  # queried_name is the name/alias that was checked
                record = {
                    "exoplanet_primary_name": exoplanet_name,
                    "queried_name": queried_name,  # The name/alias used for the Wikipedia query
                    "article_exists": info.exists,
                    "wikipedia_title": info.title
                    if info.exists
                    else None,  # Actual title on Wikipedia
                    "is_redirect": info.is_redirect if info.exists else None,
                    "redirect_target": info.redirect_target
                    if info.exists and info.is_redirect
                    else None,
                    "url": info.url if info.exists else None,
                    "host_star": exoplanet_obj.host_star.value
                    if exoplanet_obj.host_star
                    else None,
                }
                formatted_data.append(record)

        logger.info(f"Formatting complete. {len(formatted_data)} records generated.")
        return formatted_data
