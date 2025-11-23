# src/utils/wikipedia/wikipedia_checker.py
import logging
import re
import unicodedata
from dataclasses import dataclass
from typing import Any

import requests

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
    redirect_target: str | None = None
    url: str | None = None
    host_star: str | None = None


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
            {"User-Agent": user_agent}
        )  # Utiliser le user_agent fourni
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
        titles_to_check: list[str],
        exoplanet_context: dict[str, dict[str, Any]] | None = None,
    ) -> dict[str, WikiArticleInfo]:
        if not titles_to_check:
            return {}

        if len(titles_to_check) > 50:
            raise ValueError("L'API MediaWiki limite à 50 titres par requête.")

        initial_results: dict[str, WikiArticleInfo] = (
            self.build_empty_article_info_results(titles_to_check)
        )

        try:
            data: dict[str, Any] = self.fetch_raw_article_query_from_mediawiki(
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
        self, titles: list[str]
    ) -> dict[str, WikiArticleInfo]:
        return {
            title: WikiArticleInfo(exists=False, title=title, queried_title=title)
            for title in titles
        }

    def fetch_raw_article_query_from_mediawiki(
        self, titles: list[str]
    ) -> dict[str, Any]:
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
        self, data: dict[str, Any], queried_titles: list[str]
    ) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
        normalized_map: dict[Any, Any] = {
            i["from"]: i["to"] for i in data.get("normalized", [])
        }
        redirect_map: dict[Any, Any] = {
            i["from"]: i["to"] for i in data.get("redirects", [])
        }
        resolved_to_queried = {}

        for title in queried_titles:
            current = normalized_map.get(title, title)
            resolved_to_queried[current] = title
            if current in redirect_map:
                resolved_to_queried[redirect_map[current]] = title

        return normalized_map, redirect_map, resolved_to_queried

    def _find_original_title(
        self,
        api_title: str,
        resolved_to_queried: dict[str, str],
        # Les arguments ci-dessous sont retirés de la signature pour simplifier
        # et éviter la logique redondante et erronée.
        # redirect_map: dict[str, str],
        # normalized_map: dict[str, str],
        # results: dict[str, WikiArticleInfo],
    ) -> str | None:
        """
        Trouve le titre original (queried_title) associé au titre retourné par l'API (api_title).
        Se base UNIQUEMENT sur la map de résolution (resolved_to_queried) qui doit être complète.
        """
        return resolved_to_queried.get(api_title)

    def _create_wiki_article_info(
        self,
        original: str,
        api_title: str,
        page: dict[str, Any],
        redirect_map: dict[str, str],
        exoplanet_context: dict[str, dict[str, Any]] | None,
    ) -> WikiArticleInfo:
        page_id = str(page.get("pageid", "-1"))
        if "missing" in page or page_id == "-1":
            return WikiArticleInfo(
                exists=False,
                title=api_title,
                queried_title=original,
            )

        is_redirect: bool = original in redirect_map
        redirect_target: str | None = (
            redirect_map.get(original) if is_redirect else None
        )
        host_star: Any | None = (
            exoplanet_context.get(original, {}).get("st_name")
            if exoplanet_context
            else None
        )

        # Check for host star conflict
        if host_star and self._normalize_title(api_title) == self._normalize_title(
            host_star
        ):
            return WikiArticleInfo(
                exists=False,
                title=api_title,
                queried_title=original,
                is_redirect=is_redirect,
                redirect_target=redirect_target,
                url=page.get("fullurl"),
                host_star=host_star,
            )

        return WikiArticleInfo(
            exists=True,
            title=api_title,
            queried_title=original,
            is_redirect=is_redirect,
            redirect_target=redirect_target,
            url=page.get("fullurl"),
            host_star=host_star,
        )

    def resolve_article_existence_from_pages(
        self,
        data: dict[str, Any],
        resolved_to_queried: dict[str, str],
        redirect_map: dict[str, str],
        normalized_map: dict[str, str],
        results: dict[str, WikiArticleInfo],
        exoplanet_context: dict[str, dict[str, Any]] | None,
    ) -> None:
        for page in data.get("pages", {}).values():
            api_title = page.get("title")

            # Correction de l'appel pour correspondre à la signature simplifiée
            original = self._find_original_title(api_title, resolved_to_queried)

            if not original:
                logger.warning(f"Pas de correspondance trouvée pour {api_title}")
                continue

            results[original] = self._create_wiki_article_info(
                original, api_title, page, redirect_map, exoplanet_context
            )
