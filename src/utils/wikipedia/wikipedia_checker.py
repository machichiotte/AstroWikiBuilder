# src/utils/wikipedia/wikipedia_checker.py
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import unicodedata
import re
import logging

# =============================
# Logger / Configuration
# =============================
logger: logging.Logger = logging.getLogger(__name__)


# =============================
# Dataclasses
# =============================
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
            {"User-Agent": user_agent}  # Utiliser le user_agent fourni
        )
        logger.info(f"WikipediaChecker initialized with User-Agent: {user_agent}")

    def _normalize_title(self, title: str) -> str:
        title = title.lower()
        title = (
            unicodedata.normalize("NFKD", title)
            .encode("ASCII", "ignore")
            .decode("ASCII")
        )
        title = re.sub(r"[\s_\-]+", "-", title)
        title = re.sub(r"[^a-z0-9\-]", "", title)
        return title

    def check_article_existence_batch(
        self,
        titles_to_check: List[str],
        exoplanet_context: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> Dict[str, WikiArticleInfo]:
        if not titles_to_check:
            return {}

        if len(titles_to_check) > 50:
            raise ValueError("L'API MediaWiki limite à 50 titres par requête.")

        initial_results: Dict[str, WikiArticleInfo] = (
            self.build_empty_article_info_results(titles_to_check)
        )

        try:
            data: Dict[str, Any] = self.fetch_raw_article_query_from_mediawiki(
                titles_to_check
            )
        except requests.RequestException as e:
            logger.error(f"Erreur Wikipedia API: {e}")
            for title in titles_to_check:
                initial_results[title].url = f"Erreur API: {e}"
            return initial_results

        normalized_map, redirect_map, resolved_map = (
            self.build_title_normalization_and_redirect_maps(data, titles_to_check)
        )

        self.resolve_article_existence_from_pages(
            data,
            resolved_map,
            redirect_map,
            normalized_map,
            initial_results,
            exoplanet_context,
        )

        return initial_results

    def build_empty_article_info_results(
        self, titles: List[str]
    ) -> Dict[str, WikiArticleInfo]:
        return {
            title: WikiArticleInfo(exists=False, title=title, queried_title=title)
            for title in titles
        }

    def fetch_raw_article_query_from_mediawiki(
        self, titles: List[str]
    ) -> Dict[str, Any]:
        params = {
            "action": "query",
            "titles": "|".join(titles),
            "format": "json",
            "prop": "info|redirects",
            "inprop": "url",
            "redirects": 1,
            "utf8": 1,
        }
        response: requests.Response = self.session.get(
            self.BASE_URL, params=params, timeout=10
        )
        response.raise_for_status()
        return response.json().get("query", {})

    def build_title_normalization_and_redirect_maps(
        self, data: Dict[str, Any], queried_titles: List[str]
    ) -> tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
        normalized_map: Dict[Any, Any] = {
            i["from"]: i["to"] for i in data.get("normalized", [])
        }
        redirect_map: Dict[Any, Any] = {
            i["from"]: i["to"] for i in data.get("redirects", [])
        }
        resolved_to_queried = {}

        for title in queried_titles:
            current = normalized_map.get(title, title)
            resolved_to_queried[current] = title
            if current in redirect_map:
                resolved_to_queried[redirect_map[current]] = title

        return normalized_map, redirect_map, resolved_to_queried

    def resolve_article_existence_from_pages(
        self,
        data: Dict[str, Any],
        resolved_to_queried: Dict[str, str],
        redirect_map: Dict[str, str],
        normalized_map: Dict[str, str],
        results: Dict[str, WikiArticleInfo],
        exoplanet_context: Optional[Dict[str, Dict[str, Any]]],
    ) -> None:
        for page_id, page in data.get("pages", {}).items():
            api_title = page.get("title")
            original: str | None = resolved_to_queried.get(api_title)

            if not original:
                for r_from, r_to in redirect_map.items():
                    if r_to == api_title:
                        original = normalized_map.get(r_from, r_from)
                        if original in results:
                            break
                if not original:
                    logger.warning(f"Pas de correspondance trouvée pour {api_title}")
                    continue

            if "missing" in page or page_id == "-1":
                results[original] = WikiArticleInfo(
                    exists=False,
                    title=api_title,
                    queried_title=original,
                )
                continue

            is_redirect: bool = original in redirect_map
            redirect_target: str | None = (
                redirect_map.get(original) if is_redirect else None
            )
            host_star: Any | None = (
                exoplanet_context.get(original, {}).get("st_name")
                if exoplanet_context
                else None
            )

            if host_star and self._normalize_title(api_title) == self._normalize_title(
                host_star
            ):
                results[original] = WikiArticleInfo(
                    exists=False,
                    title=api_title,
                    queried_title=original,
                    is_redirect=is_redirect,
                    redirect_target=redirect_target,
                    url=page.get("fullurl"),
                    host_star=host_star,
                )
                continue

            results[original] = WikiArticleInfo(
                exists=True,
                title=api_title,
                queried_title=original,
                is_redirect=is_redirect,
                redirect_target=redirect_target,
                url=page.get("fullurl"),
                host_star=host_star,
            )
