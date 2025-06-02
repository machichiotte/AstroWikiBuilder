# src/utils/wikipedia/wikipedia_checker.py
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import unicodedata
import re
import logging

# Configuration du logger
logger = logging.getLogger(__name__)


@dataclass
class WikiArticleInfo:
    """Information sur un article Wikipedia"""

    exists: bool
    title: str
    queried_title: str
    is_redirect: bool = False
    redirect_target: Optional[str] = None
    url: Optional[str] = None
    host_star: Optional[str] = None


class WikipediaChecker:
    """
    Classe pour vérifier l'existence des articles sur Wikipedia en français
    """

    BASE_URL = "https://fr.wikipedia.org/w/api.php"

    def __init__(
        self, user_agent: str = "AstroWikiBuilder/1.0 (bot; machichiotte@gmail.com)"
    ):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": user_agent  # Utiliser le user_agent fourni
            }
        )
        logger.info(f"WikipediaChecker initialized with User-Agent: {user_agent}")

    def normalize_title(self, title: str) -> str:
        title = title.lower()
        title = (
            unicodedata.normalize("NFKD", title)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )
        title = re.sub(r"[\s_\-]+", "-", title)
        title = re.sub(r"[^a-z0-9\-]", "", title)
        return title

    def check_multiple_articles(
        self,
        titles_to_check: List[str],
        exoplanet_context: Dict[str, Dict[str, Any]] = None,
    ) -> Dict[str, WikiArticleInfo]:
        """
        Vérifie l'existence de plusieurs articles (jusqu'à 50) en une seule requête.

        Args:
            titles_to_check: Liste des titres d'articles à vérifier (max 50). These are the exoplanet names or aliases.
            exoplanet_context: Dictionnaire optionnel mappant chaque titre original de la requête (nom d'exoplanète)
                               à un dictionnaire contenant des informations contextuelles comme `{'host_star_name': '...', 'aliases': ['alias1', ...]}`.
                               Le titre principal de l'exoplanète doit être l'une des clés de `titles_to_check`.

        Returns:
            Dict[str, WikiArticleInfo]: Dictionnaire avec les titres originaux (queried_title) comme clés.
        """
        if not titles_to_check:
            return {}
        if len(titles_to_check) > 50:
            # This should be handled by the calling method (batching)
            raise ValueError("L'API MediaWiki limite à 50 titres par requête.")

        # Initialize results with default "not found" for each queried title
        results: Dict[str, WikiArticleInfo] = {
            title: WikiArticleInfo(exists=False, title=title, queried_title=title)
            for title in titles_to_check
        }

        params = {
            "action": "query",
            "titles": "|".join(titles_to_check),
            "format": "json",
            "prop": "info|redirects",  # 'redirects' here gets info if the page *is* a redirect source
            "inprop": "url",
            "redirects": 1,  # Resolve redirects (i.e. if 'X' redirects to 'Y', query for 'X' will return info for 'Y')
            "utf8": 1,
        }

        try:
            response = self.session.get(
                self.BASE_URL, params=params, timeout=10
            )  # Added timeout
            response.raise_for_status()
            data = response.json().get("query", {})
        except requests.RequestException as e:
            # logger.error(f"Wikipedia API request error: {e}") # Use logger here
            for title in titles_to_check:  # Mark all as failed due to API error
                results[title] = WikiArticleInfo(
                    exists=False, title=title, queried_title=title, url=f"Error: {e}"
                )
            return results

        normalized_map = data.get("normalized", [])
        title_normalization_map = {item["from"]: item["to"] for item in normalized_map}

        redirect_map = {item["from"]: item["to"] for item in data.get("redirects", [])}

        # This map will link the final resolved title (after normalization and redirection) back to the original queried title
        resolved_to_queried_map: Dict[str, str] = {}
        for queried_title in titles_to_check:
            current_title = queried_title
            # Step 1: Normalization (e.g. "alpha centauri bb" -> "Alpha Centauri Bb")
            if current_title in title_normalization_map:
                current_title = title_normalization_map[current_title]

            # Step 2: Redirection (e.g. "Proxima b" redirects to "Proxima Centauri b")
            # The API with 'redirects=1' resolves this, so `page.title` will be the target.
            # We need to know if a redirect happened for the *original* queried_title.
            resolved_to_queried_map[current_title] = (
                queried_title  # map normalized title to original
            )
            if (
                current_title in redirect_map
            ):  # if normalized title was a redirect source
                resolved_to_queried_map[redirect_map[current_title]] = (
                    queried_title  # map redirect target to original
                )

        for page_id, page_info in data.get("pages", {}).items():
            api_title = page_info.get(
                "title"
            )  # This is the title returned by the API (could be a redirect target)

            # Find which original queried_title this page_info corresponds to
            # This is tricky because the API might return a page_info with a title that was a redirect target.
            original_queried_title = None
            if api_title in resolved_to_queried_map:
                original_queried_title = resolved_to_queried_map[api_title]
            elif (
                api_title in titles_to_check
            ):  # Direct match, no normalization or redirect from API's perspective for this title
                original_queried_title = api_title
            else:  # Fallback: try to find based on page_info['title'] being a key in redirect_map's values
                for r_from, r_to in redirect_map.items():
                    if r_to == api_title:  # api_title is a redirect target
                        normalized_r_from = title_normalization_map.get(r_from, r_from)
                        if normalized_r_from in titles_to_check:
                            original_queried_title = normalized_r_from
                            break
                        elif (
                            r_from in titles_to_check
                        ):  # if the original non-normalized redirect source was queried
                            original_queried_title = r_from
                            break
                if not original_queried_title:
                    # logger.warning(f"Could not map API title '{api_title}' back to any queried title. Skipping.")
                    continue

            if "missing" in page_info or page_id == "-1":
                results[original_queried_title] = WikiArticleInfo(
                    exists=False, title=api_title, queried_title=original_queried_title
                )
                continue

            is_redirect_source = (
                original_queried_title in redirect_map
            )  # Was the *original queried title* a redirect?
            redirect_target = (
                redirect_map.get(original_queried_title) if is_redirect_source else None
            )

            # Contextual check: if the page found is the host star page, it's not the exoplanet page.
            # This logic needs the context (host star name for the original_queried_title).
            host_star_name_for_original_title = None
            if exoplanet_context and original_queried_title in exoplanet_context:
                host_star_name_for_original_title = exoplanet_context[
                    original_queried_title
                ].get("host_star_name")

            if host_star_name_for_original_title:
                # If the (potentially redirected) title is the host star, then the exoplanet article itself doesn't exist.
                # The `api_title` is the final title of the page found by MediaWiki.
                if self.normalize_title(api_title) == self.normalize_title(
                    host_star_name_for_original_title
                ):
                    results[original_queried_title] = WikiArticleInfo(
                        exists=False,
                        title=api_title,
                        queried_title=original_queried_title,
                        is_redirect=is_redirect_source,  # It might be a redirect TO the host star page
                        redirect_target=redirect_target,
                        url=page_info.get("fullurl"),  # URL to the host star page
                    )
                    continue  # Skip marking as exists=True

            results[original_queried_title] = WikiArticleInfo(
                exists=True,
                title=api_title,  # The actual title of the page found
                queried_title=original_queried_title,
                is_redirect=is_redirect_source,
                redirect_target=redirect_target,
                url=page_info.get("fullurl"),
            )

        return results
